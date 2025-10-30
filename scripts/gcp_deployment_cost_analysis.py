#!/usr/bin/env python3
"""
GCP Deployment Cost Analysis Script
Analyzes current GCP deployment costs and provides optimization recommendations.
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GCPCostAnalyzer:
    """Analyzes GCP deployment costs and provides recommendations."""
    
    def __init__(self, project_id: str = "gen-lang-client-0128452200"):
        self.project_id = project_id
        self.analysis_results = {}
        
    def run_gcloud_command(self, command: List[str]) -> Dict[str, Any]:
        """Run a gcloud command and return parsed JSON output."""
        try:
            result = subprocess.run(
                command + ["--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON output: {e}")
            return {}
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get current project information."""
        logger.info("Getting project information...")
        
        # Get project details
        project_info = self.run_gcloud_command([
            "gcloud", "projects", "describe", self.project_id
        ])
        
        # Get billing info
        billing_info = self.run_gcloud_command([
            "gcloud", "billing", "projects", "describe", self.project_id
        ])
        
        return {
            "project_id": self.project_id,
            "project_info": project_info,
            "billing_info": billing_info
        }
    
    def get_cloud_functions(self) -> Dict[str, Any]:
        """Get Cloud Functions deployment status."""
        logger.info("Analyzing Cloud Functions...")
        
        functions = self.run_gcloud_command([
            "gcloud", "functions", "list", "--regions=us-central1"
        ])
        
        function_details = {}
        for func in functions:
            func_name = func.get("name", "").split("/")[-1]
            function_details[func_name] = {
                "state": func.get("state", "UNKNOWN"),
                "trigger": func.get("trigger", {}),
                "region": func.get("region", "us-central1"),
                "environment": func.get("environment", "1st gen")
            }
            
            # Get detailed function info
            try:
                detail = self.run_gcloud_command([
                    "gcloud", "functions", "describe", func_name, "--region=us-central1"
                ])
                if isinstance(detail, dict):
                    function_details[func_name].update({
                        "memory": detail.get("buildConfig", {}).get("build", {}).get("memory", "256MB"),
                        "timeout": detail.get("buildConfig", {}).get("build", {}).get("timeout", "60s"),
                        "runtime": detail.get("buildConfig", {}).get("runtime", "python311"),
                        "url": detail.get("url", ""),
                        "state_messages": detail.get("stateMessages", [])
                    })
            except Exception as e:
                logger.warning(f"Could not get details for function {func_name}: {e}")
        
        return function_details
    
    def get_firestore_info(self) -> Dict[str, Any]:
        """Get Firestore database information."""
        logger.info("Analyzing Firestore database...")
        
        databases = self.run_gcloud_command([
            "gcloud", "firestore", "databases", "list"
        ])
        
        firestore_info = {}
        for db in databases:
            db_name = db.get("name", "").split("/")[-1]
            firestore_info[db_name] = {
                "location": db.get("locationId", "us-central1"),
                "type": db.get("type", "FIRESTORE_NATIVE"),
                "free_tier": db.get("freeTier", True),
                "create_time": db.get("createTime", ""),
                "app_engine_integration": db.get("appEngineIntegrationMode", "DISABLED")
            }
        
        return firestore_info
    
    def get_enabled_services(self) -> Dict[str, Any]:
        """Get enabled GCP services."""
        logger.info("Analyzing enabled services...")
        
        services = self.run_gcloud_command([
            "gcloud", "services", "list", "--enabled"
        ])
        
        service_info = {}
        for service in services:
            service_name = service.get("config", {}).get("name", "")
            service_info[service_name] = {
                "title": service.get("config", {}).get("title", ""),
                "state": service.get("state", "UNKNOWN")
            }
        
        return service_info
    
    def get_billing_budgets(self) -> Dict[str, Any]:
        """Get billing budget information."""
        logger.info("Analyzing billing budgets...")
        
        # Get billing account
        billing_accounts = self.run_gcloud_command([
            "gcloud", "billing", "accounts", "list"
        ])
        
        if not billing_accounts:
            return {"error": "No billing accounts found"}
        
        billing_account_id = billing_accounts[0].get("name", "").split("/")[-1]
        
        # Get budgets
        budgets = self.run_gcloud_command([
            "gcloud", "billing", "budgets", "list", 
            f"--billing-account={billing_account_id}"
        ])
        
        return {
            "billing_account_id": billing_account_id,
            "budgets": budgets
        }
    
    def calculate_cost_estimates(self) -> Dict[str, Any]:
        """Calculate estimated costs based on current deployment."""
        logger.info("Calculating cost estimates...")
        
        # Cloud Functions cost estimation
        functions = self.analysis_results.get("cloud_functions", {})
        function_costs = {}
        
        for func_name, func_info in functions.items():
            if func_info.get("state") == "ACTIVE":
                # Estimate based on typical usage
                memory_mb = 256  # Default
                timeout_sec = 60  # Default
                
                # Parse memory and timeout from function details
                memory_str = func_info.get("memory", "256MB")
                if "MB" in memory_str:
                    memory_mb = int(memory_str.replace("MB", ""))
                
                timeout_str = func_info.get("timeout", "60s")
                if "s" in timeout_str:
                    timeout_sec = int(timeout_str.replace("s", ""))
                
                # Cost calculation (approximate)
                # Cloud Functions pricing: $0.0000004 per GB-second
                # Assuming 1000 invocations per month, 1 second average execution
                monthly_invocations = 1000
                avg_execution_time = 1  # seconds
                memory_gb = memory_mb / 1024
                
                monthly_cost = (monthly_invocations * avg_execution_time * memory_gb * 0.0000004)
                
                function_costs[func_name] = {
                    "monthly_invocations": monthly_invocations,
                    "memory_mb": memory_mb,
                    "timeout_sec": timeout_sec,
                    "estimated_monthly_cost": round(monthly_cost, 4)
                }
        
        # Firestore cost estimation
        firestore_info = self.analysis_results.get("firestore", {})
        firestore_costs = {}
        
        for db_name, db_info in firestore_info.items():
            if db_info.get("free_tier", True):
                firestore_costs[db_name] = {
                    "tier": "Free Tier",
                    "estimated_monthly_cost": 0.0,
                    "limits": {
                        "storage": "1GB",
                        "reads": "50K/day",
                        "writes": "20K/day",
                        "deletes": "20K/day"
                    }
                }
            else:
                # Paid tier estimation
                firestore_costs[db_name] = {
                    "tier": "Paid Tier",
                    "estimated_monthly_cost": 5.0,  # Rough estimate
                    "note": "Cost depends on usage"
                }
        
        total_function_cost = sum(func.get("estimated_monthly_cost", 0) for func in function_costs.values())
        total_firestore_cost = sum(db.get("estimated_monthly_cost", 0) for db in firestore_costs.values())
        
        return {
            "cloud_functions": function_costs,
            "firestore": firestore_costs,
            "total_estimated_monthly_cost": total_function_cost + total_firestore_cost
        }
    
    def generate_recommendations(self) -> List[str]:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        # Check for failed functions
        functions = self.analysis_results.get("cloud_functions", {})
        failed_functions = [name for name, info in functions.items() if info.get("state") == "FAILED"]
        
        if failed_functions:
            recommendations.append(
                f"🚨 CRITICAL: {len(failed_functions)} Cloud Functions are in FAILED state: {', '.join(failed_functions)}. "
                "These should be redeployed or deleted to avoid potential charges."
            )
        
        # Check for unused services
        services = self.analysis_results.get("enabled_services", {})
        potentially_unused = [
            "analyticshub.googleapis.com",
            "artifactregistry.googleapis.com",
            "cloudbuild.googleapis.com"
        ]
        
        unused_services = [svc for svc in potentially_unused if svc in services]
        if unused_services:
            recommendations.append(
                f"💡 Consider disabling unused services to reduce costs: {', '.join(unused_services)}"
            )
        
        # Firestore optimization
        firestore_info = self.analysis_results.get("firestore", {})
        for db_name, db_info in firestore_info.items():
            if db_info.get("free_tier", True):
                recommendations.append(
                    f"✅ Firestore database '{db_name}' is on free tier - good for cost optimization"
                )
        
        # Budget monitoring
        budgets = self.analysis_results.get("billing_budgets", {})
        if budgets.get("budgets"):
            recommendations.append(
                "✅ Budget alerts are configured - good for cost monitoring"
            )
        else:
            recommendations.append(
                "⚠️ Consider setting up budget alerts to monitor costs"
            )
        
        return recommendations
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete cost analysis."""
        logger.info("Starting GCP deployment cost analysis...")
        
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "project_info": self.get_project_info(),
            "cloud_functions": self.get_cloud_functions(),
            "firestore": self.get_firestore_info(),
            "enabled_services": self.get_enabled_services(),
            "billing_budgets": self.get_billing_budgets(),
        }
        
        # Calculate costs
        self.analysis_results["cost_estimates"] = self.calculate_cost_estimates()
        
        # Generate recommendations
        self.analysis_results["recommendations"] = self.generate_recommendations()
        
        return self.analysis_results
    
    def print_summary(self):
        """Print a summary of the analysis."""
        print("\n" + "="*80)
        print("🔍 GCP DEPLOYMENT COST ANALYSIS SUMMARY")
        print("="*80)
        
        # Project info
        project_info = self.analysis_results.get("project_info", {})
        print(f"\n📋 Project: {self.project_id}")
        print(f"💰 Billing Enabled: {project_info.get('billing_info', {}).get('billingEnabled', 'Unknown')}")
        
        # Cloud Functions
        functions = self.analysis_results.get("cloud_functions", {})
        print(f"\n🚀 Cloud Functions: {len(functions)} deployed")
        for func_name, func_info in functions.items():
            state = func_info.get("state", "UNKNOWN")
            status_emoji = "✅" if state == "ACTIVE" else "❌" if state == "FAILED" else "⚠️"
            print(f"  {status_emoji} {func_name}: {state}")
            if func_info.get("state_messages"):
                for msg in func_info["state_messages"]:
                    print(f"    ⚠️ {msg.get('message', '')}")
        
        # Firestore
        firestore = self.analysis_results.get("firestore", {})
        print(f"\n🗄️ Firestore Databases: {len(firestore)}")
        for db_name, db_info in firestore.items():
            tier = "Free" if db_info.get("free_tier", True) else "Paid"
            print(f"  📊 {db_name}: {tier} tier")
        
        # Cost estimates
        costs = self.analysis_results.get("cost_estimates", {})
        print(f"\n💰 Cost Estimates (Monthly):")
        print(f"  Cloud Functions: ${sum(func.get('estimated_monthly_cost', 0) for func in costs.get('cloud_functions', {}).values()):.4f}")
        print(f"  Firestore: ${sum(db.get('estimated_monthly_cost', 0) for db in costs.get('firestore', {}).values()):.4f}")
        print(f"  Total Estimated: ${costs.get('total_estimated_monthly_cost', 0):.4f}")
        
        # Recommendations
        recommendations = self.analysis_results.get("recommendations", [])
        print(f"\n💡 Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")
        
        print("\n" + "="*80)

def main():
    """Main function."""
    analyzer = GCPCostAnalyzer()
    
    try:
        results = analyzer.run_analysis()
        analyzer.print_summary()
        
        # Save results to file
        output_file = "data/gcp_deployment_cost_analysis.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed analysis saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
