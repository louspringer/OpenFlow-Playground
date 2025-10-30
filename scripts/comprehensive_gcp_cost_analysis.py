#!/usr/bin/env python3
"""
Comprehensive GCP Cost Analysis Script
Analyzes current GCP deployment costs including GKE clusters and provides detailed cost estimates.
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ComprehensiveGCPCostAnalyzer:
    """Comprehensive GCP cost analyzer including GKE clusters."""

    def __init__(self, project_id: str = "gen-lang-client-0128452200"):
        self.project_id = project_id
        self.analysis_results = {}

    def run_gcloud_command(self, command: List[str]) -> Dict[str, Any]:
        """Run a gcloud command and return parsed JSON output."""
        try:
            result = subprocess.run(command + ["--format=json"], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON output: {e}")
            return {}

    def get_gke_clusters(self) -> Dict[str, Any]:
        """Get GKE cluster information and costs."""
        logger.info("Analyzing GKE clusters...")

        clusters = self.run_gcloud_command(["gcloud", "container", "clusters", "list"])

        cluster_details = {}
        for cluster in clusters:
            cluster_name = cluster.get("name", "")
            location = cluster.get("location", "")

            # Get detailed cluster info
            try:
                detail = self.run_gcloud_command(["gcloud", "container", "clusters", "describe", cluster_name, f"--location={location}"])

                if isinstance(detail, dict):
                    cluster_details[cluster_name] = {
                        "name": cluster_name,
                        "location": location,
                        "status": cluster.get("status", "UNKNOWN"),
                        "currentMasterVersion": cluster.get("currentMasterVersion", ""),
                        "currentNodeCount": cluster.get("currentNodeCount", 0),
                        "nodePools": detail.get("nodePools", []),
                        "nodeConfig": detail.get("nodeConfig", {}),
                        "resourceUsageExportConfig": detail.get("resourceUsageExportConfig"),
                    }
            except Exception as e:
                logger.warning(f"Could not get details for cluster {cluster_name}: {e}")

        return cluster_details

    def get_compute_instances(self) -> Dict[str, Any]:
        """Get compute instances information."""
        logger.info("Analyzing compute instances...")

        instances = self.run_gcloud_command(["gcloud", "compute", "instances", "list", "--filter=status:RUNNING"])

        instance_details = {}
        for instance in instances:
            instance_name = instance.get("name", "")
            instance_details[instance_name] = {
                "name": instance_name,
                "zone": instance.get("zone", "").split("/")[-1],
                "machineType": instance.get("machineType", "").split("/")[-1],
                "status": instance.get("status", ""),
                "preemptible": instance.get("scheduling", {}).get("preemptible", False),
                "creationTimestamp": instance.get("creationTimestamp", ""),
                "disks": instance.get("disks", []),
            }

        return instance_details

    def calculate_gke_costs(self, cluster_details: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate GKE cluster costs."""
        logger.info("Calculating GKE costs...")

        # GKE pricing (as of 2024)
        # Management fee: $0.10 per cluster per hour
        # Node costs: Based on machine type
        # e2-small: ~$0.0335/hour
        # Preemptible e2-small: ~$0.0101/hour

        gke_costs = {}

        for cluster_name, cluster_info in cluster_details.items():
            if cluster_info.get("status") == "RUNNING":
                # Management fee
                management_fee_per_hour = 0.10
                daily_management_fee = management_fee_per_hour * 24
                monthly_management_fee = daily_management_fee * 30

                # Node costs
                node_pools = cluster_info.get("nodePools", [])
                total_node_cost_per_hour = 0
                node_breakdown = {}

                for pool in node_pools:
                    pool_name = pool.get("name", "")
                    node_count = pool.get("initialNodeCount", 0)
                    config = pool.get("config", {})
                    machine_type = config.get("machineType", "e2-small")
                    is_preemptible = config.get("preemptible", False)

                    # Cost per hour based on machine type and preemptible status
                    if machine_type == "e2-small":
                        if is_preemptible:
                            cost_per_hour = 0.0101
                        else:
                            cost_per_hour = 0.0335
                    else:
                        # Default to e2-small pricing if unknown
                        cost_per_hour = 0.0101 if is_preemptible else 0.0335

                    pool_cost_per_hour = node_count * cost_per_hour
                    total_node_cost_per_hour += pool_cost_per_hour

                    node_breakdown[pool_name] = {
                        "node_count": node_count,
                        "machine_type": machine_type,
                        "preemptible": is_preemptible,
                        "cost_per_hour": cost_per_hour,
                        "pool_cost_per_hour": pool_cost_per_hour,
                    }

                # Calculate daily and monthly costs
                daily_node_cost = total_node_cost_per_hour * 24
                monthly_node_cost = daily_node_cost * 30

                total_daily_cost = daily_management_fee + daily_node_cost
                total_monthly_cost = monthly_management_fee + monthly_node_cost

                gke_costs[cluster_name] = {
                    "management_fee": {"per_hour": management_fee_per_hour, "daily": daily_management_fee, "monthly": monthly_management_fee},
                    "node_costs": {"per_hour": total_node_cost_per_hour, "daily": daily_node_cost, "monthly": monthly_node_cost},
                    "total": {"per_hour": management_fee_per_hour + total_node_cost_per_hour, "daily": total_daily_cost, "monthly": total_monthly_cost},
                    "node_breakdown": node_breakdown,
                    "current_node_count": cluster_info.get("currentNodeCount", 0),
                }

        return gke_costs

    def calculate_compute_costs(self, instance_details: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate compute instance costs."""
        logger.info("Calculating compute instance costs...")

        compute_costs = {}

        for instance_name, instance_info in instance_details.items():
            machine_type = instance_info.get("machineType", "e2-small")
            is_preemptible = instance_info.get("preemptible", False)

            # Cost per hour based on machine type and preemptible status
            if machine_type == "e2-small":
                if is_preemptible:
                    cost_per_hour = 0.0101
                else:
                    cost_per_hour = 0.0335
            else:
                # Default to e2-small pricing if unknown
                cost_per_hour = 0.0101 if is_preemptible else 0.0335

            daily_cost = cost_per_hour * 24
            monthly_cost = daily_cost * 30

            compute_costs[instance_name] = {
                "machine_type": machine_type,
                "preemptible": is_preemptible,
                "cost_per_hour": cost_per_hour,
                "daily_cost": daily_cost,
                "monthly_cost": monthly_cost,
                "zone": instance_info.get("zone", ""),
            }

        return compute_costs

    def get_cloud_functions(self) -> Dict[str, Any]:
        """Get Cloud Functions deployment status."""
        logger.info("Analyzing Cloud Functions...")

        functions = self.run_gcloud_command(["gcloud", "functions", "list", "--regions=us-central1"])

        function_details = {}
        for func in functions:
            func_name = func.get("name", "").split("/")[-1]
            function_details[func_name] = {
                "state": func.get("state", "UNKNOWN"),
                "trigger": func.get("trigger", {}),
                "region": func.get("region", "us-central1"),
                "environment": func.get("environment", "1st gen"),
            }

        return function_details

    def get_firestore_info(self) -> Dict[str, Any]:
        """Get Firestore database information."""
        logger.info("Analyzing Firestore database...")

        databases = self.run_gcloud_command(["gcloud", "firestore", "databases", "list"])

        firestore_info = {}
        for db in databases:
            db_name = db.get("name", "").split("/")[-1]
            firestore_info[db_name] = {
                "location": db.get("locationId", "us-central1"),
                "type": db.get("type", "FIRESTORE_NATIVE"),
                "free_tier": db.get("freeTier", True),
                "create_time": db.get("createTime", ""),
                "app_engine_integration": db.get("appEngineIntegrationMode", "DISABLED"),
            }

        return firestore_info

    def calculate_firestore_costs(self, firestore_info: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Firestore costs."""
        logger.info("Calculating Firestore costs...")

        firestore_costs = {}

        for db_name, db_info in firestore_info.items():
            if db_info.get("free_tier", True):
                firestore_costs[db_name] = {"tier": "Free Tier", "daily_cost": 0.0, "monthly_cost": 0.0, "limits": {"storage": "1GB", "reads": "50K/day", "writes": "20K/day", "deletes": "20K/day"}}
            else:
                # Paid tier estimation (rough)
                firestore_costs[db_name] = {"tier": "Paid Tier", "daily_cost": 0.17, "monthly_cost": 5.0, "note": "Cost depends on usage"}  # Rough estimate

        return firestore_costs

    def generate_daily_cost_breakdown(self) -> Dict[str, Any]:
        """Generate detailed daily cost breakdown."""
        logger.info("Generating daily cost breakdown...")

        # Get all cost components
        gke_costs = self.analysis_results.get("gke_costs", {})
        compute_costs = self.analysis_results.get("compute_costs", {})
        firestore_costs = self.analysis_results.get("firestore_costs", {})

        daily_breakdown = {
            "gke_clusters": {},
            "compute_instances": {},
            "firestore": {},
            "totals": {"gke_daily": 0.0, "compute_daily": 0.0, "firestore_daily": 0.0, "total_daily": 0.0, "total_monthly": 0.0},
        }

        # GKE costs
        for cluster_name, cluster_cost in gke_costs.items():
            daily_breakdown["gke_clusters"][cluster_name] = {
                "daily_cost": cluster_cost["total"]["daily"],
                "monthly_cost": cluster_cost["total"]["monthly"],
                "node_count": cluster_cost["current_node_count"],
                "management_fee_daily": cluster_cost["management_fee"]["daily"],
                "node_costs_daily": cluster_cost["node_costs"]["daily"],
            }
            daily_breakdown["totals"]["gke_daily"] += cluster_cost["total"]["daily"]

        # Compute instance costs
        for instance_name, instance_cost in compute_costs.items():
            daily_breakdown["compute_instances"][instance_name] = {
                "daily_cost": instance_cost["daily_cost"],
                "monthly_cost": instance_cost["monthly_cost"],
                "machine_type": instance_cost["machine_type"],
                "preemptible": instance_cost["preemptible"],
            }
            daily_breakdown["totals"]["compute_daily"] += instance_cost["daily_cost"]

        # Firestore costs
        for db_name, db_cost in firestore_costs.items():
            daily_breakdown["firestore"][db_name] = {"daily_cost": db_cost["daily_cost"], "monthly_cost": db_cost["monthly_cost"], "tier": db_cost["tier"]}
            daily_breakdown["totals"]["firestore_daily"] += db_cost["daily_cost"]

        # Calculate totals
        daily_breakdown["totals"]["total_daily"] = daily_breakdown["totals"]["gke_daily"] + daily_breakdown["totals"]["compute_daily"] + daily_breakdown["totals"]["firestore_daily"]
        daily_breakdown["totals"]["total_monthly"] = daily_breakdown["totals"]["total_daily"] * 30

        return daily_breakdown

    def run_analysis(self) -> Dict[str, Any]:
        """Run complete comprehensive cost analysis."""
        logger.info("Starting comprehensive GCP cost analysis...")

        # Get all resource information
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "project_id": self.project_id,
            "gke_clusters": self.get_gke_clusters(),
            "compute_instances": self.get_compute_instances(),
            "cloud_functions": self.get_cloud_functions(),
            "firestore": self.get_firestore_info(),
        }

        # Calculate costs
        self.analysis_results["gke_costs"] = self.calculate_gke_costs(self.analysis_results["gke_clusters"])
        self.analysis_results["compute_costs"] = self.calculate_compute_costs(self.analysis_results["compute_instances"])
        self.analysis_results["firestore_costs"] = self.calculate_firestore_costs(self.analysis_results["firestore"])

        # Generate daily breakdown
        self.analysis_results["daily_breakdown"] = self.generate_daily_cost_breakdown()

        return self.analysis_results

    def print_summary(self):
        """Print a comprehensive summary of the analysis."""
        print("\n" + "=" * 80)
        print("🔍 COMPREHENSIVE GCP COST ANALYSIS SUMMARY")
        print("=" * 80)

        # Project info
        print(f"\n📋 Project: {self.project_id}")

        # GKE Clusters
        gke_clusters = self.analysis_results.get("gke_clusters", {})
        print(f"\n🚀 GKE Clusters: {len(gke_clusters)}")
        for cluster_name, cluster_info in gke_clusters.items():
            status = cluster_info.get("status", "UNKNOWN")
            node_count = cluster_info.get("currentNodeCount", 0)
            status_emoji = "✅" if status == "RUNNING" else "❌" if status == "ERROR" else "⚠️"
            print(f"  {status_emoji} {cluster_name}: {status} ({node_count} nodes)")

        # Compute Instances
        compute_instances = self.analysis_results.get("compute_instances", {})
        print(f"\n💻 Compute Instances: {len(compute_instances)}")
        for instance_name, instance_info in compute_instances.items():
            machine_type = instance_info.get("machineType", "unknown")
            preemptible = " (Preemptible)" if instance_info.get("preemptible", False) else ""
            print(f"  🖥️ {instance_name}: {machine_type}{preemptible}")

        # Cloud Functions
        functions = self.analysis_results.get("cloud_functions", {})
        print(f"\n⚡ Cloud Functions: {len(functions)}")
        for func_name, func_info in functions.items():
            state = func_info.get("state", "UNKNOWN")
            status_emoji = "✅" if state == "ACTIVE" else "❌" if state == "FAILED" else "⚠️"
            print(f"  {status_emoji} {func_name}: {state}")

        # Firestore
        firestore = self.analysis_results.get("firestore", {})
        print(f"\n🗄️ Firestore Databases: {len(firestore)}")
        for db_name, db_info in firestore.items():
            tier = "Free" if db_info.get("free_tier", True) else "Paid"
            print(f"  📊 {db_name}: {tier} tier")

        # Daily Cost Breakdown
        daily_breakdown = self.analysis_results.get("daily_breakdown", {})
        totals = daily_breakdown.get("totals", {})

        print(f"\n💰 DAILY COST BREAKDOWN:")
        print(f"  🚀 GKE Clusters: ${totals.get('gke_daily', 0):.4f}/day")
        print(f"  💻 Compute Instances: ${totals.get('compute_daily', 0):.4f}/day")
        print(f"  🗄️ Firestore: ${totals.get('firestore_daily', 0):.4f}/day")
        print(f"  📊 TOTAL DAILY: ${totals.get('total_daily', 0):.4f}/day")
        print(f"  📅 TOTAL MONTHLY: ${totals.get('total_monthly', 0):.4f}/month")

        # Detailed GKE breakdown
        gke_costs = self.analysis_results.get("gke_costs", {})
        if gke_costs:
            print(f"\n🚀 GKE DETAILED COSTS:")
            for cluster_name, cluster_cost in gke_costs.items():
                print(f"  📊 {cluster_name}:")
                print(f"    Management Fee: ${cluster_cost['management_fee']['daily']:.4f}/day")
                print(f"    Node Costs: ${cluster_cost['node_costs']['daily']:.4f}/day")
                print(f"    Total: ${cluster_cost['total']['daily']:.4f}/day")

                # Node pool breakdown
                for pool_name, pool_info in cluster_cost.get("node_breakdown", {}).items():
                    preemptible = " (Preemptible)" if pool_info.get("preemptible", False) else ""
                    print(f"      {pool_name}: {pool_info['node_count']}x {pool_info['machine_type']}{preemptible} = ${pool_info['pool_cost_per_hour']:.4f}/hour")

        print("\n" + "=" * 80)


def main():
    """Main function."""
    analyzer = ComprehensiveGCPCostAnalyzer()

    try:
        results = analyzer.run_analysis()
        analyzer.print_summary()

        # Save results to file
        output_file = "data/comprehensive_gcp_cost_analysis.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n📄 Detailed analysis saved to: {output_file}")

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
