#!/usr/bin/env python3
"""
GCP Ghostbusters Main Module

This module provides the GCPGhostbustersOrchestrator for investigating
GCP-specific infrastructure and deployment quality issues.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Firestore client for testing
# In production, this would be: from google.cloud import firestore
db = None  # Placeholder for Firestore client


def mock_ghostbusters_analysis(project_path: str) -> dict[str, Any]:
    """
    Mock Ghostbusters analysis for testing purposes.

    Args:
        project_path: Path to the project to analyze

    Returns:
        Mock analysis results
    """
    return {
        "confidence_score": 0.95,
        "delusions_detected": [{"type": "security"}],
        "recovery_actions": [{"action": "fix"}],
        "errors": [],
    }


class GCPGhostbustersOrchestrator:
    """
    GCP Ghostbusters Orchestrator for cloud infrastructure investigation.

    This orchestrator specializes in GCP-specific quality analysis including
    Cloud Build, Cloud Run, and infrastructure as code validation.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize the GCP Ghostbusters Orchestrator"""
        self.config = config or {}
        self.gcp_services = {}
        self.infrastructure_issues = {}
        self.deployment_metrics = {}

        logger.info("☁️ GCP Ghostbusters Orchestrator initialized")

    def investigate_gcp_infrastructure(self, project_id: str) -> dict[str, Any]:
        """Investigate GCP infrastructure quality issues"""
        logger.info(f"🔍 Investigating GCP infrastructure for project: {project_id}")

        investigation_results = {
            "project_id": project_id,
            "timestamp": self._get_timestamp(),
            "gcp_services_analyzed": [],
            "infrastructure_issues": [],
            "deployment_quality": 0.0,
            "security_posture": "unknown",
            "cost_optimization": "unknown",
        }

        try:
            # Analyze Cloud Build configurations
            cloud_build_analysis = self._analyze_cloud_build(project_id)
            investigation_results["gcp_services_analyzed"].append("cloud_build")
            investigation_results["infrastructure_issues"].extend(
                cloud_build_analysis.get("issues", [])
            )

            # Analyze Cloud Run configurations
            cloud_run_analysis = self._analyze_cloud_run(project_id)
            investigation_results["gcp_services_analyzed"].append("cloud_run")
            investigation_results["infrastructure_issues"].extend(
                cloud_run_analysis.get("issues", [])
            )

            # Calculate overall metrics
            investigation_results[
                "deployment_quality"
            ] = self._calculate_deployment_quality(investigation_results)
            investigation_results["security_posture"] = self._assess_security_posture(
                investigation_results
            )
            investigation_results["cost_optimization"] = self._assess_cost_optimization(
                investigation_results
            )

            logger.info(
                f"✅ GCP investigation complete. Quality score: {investigation_results['deployment_quality']:.2f}"
            )

        except Exception as e:
            logger.error(f"❌ GCP investigation failed: {e}")
            investigation_results["error"] = str(e)

        self.infrastructure_issues[project_id] = investigation_results
        return investigation_results

    def _analyze_cloud_build(self, project_id: str) -> dict[str, Any]:
        """Analyze Cloud Build configuration quality"""
        analysis = {
            "service": "cloud_build",
            "issues": [],
            "config_files": [],
            "triggers": [],
        }

        try:
            # Look for Cloud Build configuration files
            config_files = list(Path().rglob("cloudbuild*.yaml"))
            analysis["config_files"] = [str(f) for f in config_files]

            if not config_files:
                analysis["issues"].append(
                    {
                        "type": "missing_config",
                        "severity": "medium",
                        "description": "No Cloud Build configuration files found",
                        "recommendation": "Create cloudbuild.yaml for automated builds",
                    }
                )
            else:
                # Analyze each config file
                for config_file in config_files:
                    config_issues = self._analyze_cloudbuild_config(config_file)
                    analysis["issues"].extend(config_issues)

            logger.info("🔍 Analyzed Cloud Build configuration")

        except Exception as e:
            logger.error(f"❌ Cloud Build analysis failed: {e}")
            analysis["issues"].append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "description": f"Failed to analyze Cloud Build: {e}",
                    "recommendation": "Check file permissions and configuration",
                }
            )

        return analysis

    def _analyze_cloudbuild_config(self, config_file: Path) -> list[dict[str, Any]]:
        """Analyze individual Cloud Build configuration file"""
        issues = []

        try:
            content = config_file.read_text()

            # Check for common issues
            if "latest" in content:
                issues.append(
                    {
                        "type": "latest_tag",
                        "severity": "medium",
                        "description": "Using 'latest' tag in Cloud Build",
                        "recommendation": "Use specific version tags for reproducibility",
                    }
                )

            if "gcr.io" in content:
                issues.append(
                    {
                        "type": "deprecated_registry",
                        "severity": "low",
                        "description": "Using deprecated gcr.io registry",
                        "recommendation": "Migrate to Artifact Registry (artifact-registry.googleapis.com)",
                    }
                )

            if "timeout" not in content:
                issues.append(
                    {
                        "type": "missing_timeout",
                        "severity": "low",
                        "description": "No timeout specified in Cloud Build",
                        "recommendation": "Add timeout to prevent hanging builds",
                    }
                )

        except Exception as e:
            logger.error(f"❌ Failed to analyze Cloud Build config {config_file}: {e}")
            issues.append(
                {
                    "type": "config_parse_error",
                    "severity": "high",
                    "description": f"Failed to parse Cloud Build config: {e}",
                    "recommendation": "Validate YAML syntax and structure",
                }
            )

        return issues

    def _analyze_cloud_run(self, project_id: str) -> dict[str, Any]:
        """Analyze Cloud Run configuration quality"""
        analysis = {"service": "cloud_run", "issues": [], "deployment_files": []}

        try:
            # Look for Cloud Run deployment files
            deployment_files = list(Path().rglob("*deploy*.yaml"))
            analysis["deployment_files"] = [str(f) for f in deployment_files]

            if not deployment_files:
                analysis["issues"].append(
                    {
                        "type": "missing_deployment",
                        "severity": "low",
                        "description": "No Cloud Run deployment files found",
                        "recommendation": "Create deployment manifests for Cloud Run services",
                    }
                )

            logger.info("🔍 Analyzed Cloud Run configuration")

        except Exception as e:
            logger.error(f"❌ Cloud Run analysis failed: {e}")
            analysis["issues"].append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "description": f"Failed to analyze Cloud Run: {e}",
                    "recommendation": "Check deployment configuration",
                }
            )

        return analysis

    def _calculate_deployment_quality(
        self, investigation_results: dict[str, Any]
    ) -> float:
        """Calculate overall deployment quality score"""
        issues = investigation_results.get("infrastructure_issues", [])

        if not issues:
            return 100.0

        # Weight issues by severity
        severity_weights = {"low": 1.0, "medium": 2.0, "high": 5.0, "critical": 10.0}

        total_weight = 0
        for issue in issues:
            severity = issue.get("severity", "low")
            weight = severity_weights.get(severity, 1.0)
            total_weight += weight

        # Calculate score (100 - weighted penalty)
        max_penalty = 50
        penalty = min(total_weight * 2, max_penalty)
        score = max(100.0 - penalty, 0.0)

        return round(score, 2)

    def _assess_security_posture(self, investigation_results: dict[str, Any]) -> str:
        """Assess overall security posture"""
        issues = investigation_results.get("infrastructure_issues", [])

        critical_security_issues = [
            i for i in issues if i.get("severity") == "critical"
        ]
        high_security_issues = [i for i in issues if i.get("severity") == "high"]

        if critical_security_issues:
            return "critical"
        if high_security_issues:
            return "high"
        if issues:
            return "medium"
        return "excellent"

    def _assess_cost_optimization(self, investigation_results: dict[str, Any]) -> str:
        """Assess cost optimization status"""
        issues = investigation_results.get("infrastructure_issues", [])

        cost_related_issues = [
            i for i in issues if "cost" in i.get("description", "").lower()
        ]

        if cost_related_issues:
            return "needs_optimization"
        return "optimized"

    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime

        return datetime.now().isoformat()

    def get_gcp_investigation_summary(self) -> dict[str, Any]:
        """Get summary of all GCP investigations"""
        return {
            "total_investigations": len(self.infrastructure_issues),
            "projects_investigated": list(self.infrastructure_issues.keys()),
            "overall_gcp_quality": self._calculate_overall_gcp_quality(),
            "service_coverage": list(
                {
                    service
                    for result in self.infrastructure_issues.values()
                    for service in result.get("gcp_services_analyzed", [])
                }
            ),
        }

    def _calculate_overall_gcp_quality(self) -> str:
        """Calculate overall GCP quality trend"""
        if not self.infrastructure_issues:
            return "no_data"

        scores = [
            result.get("deployment_quality", 0)
            for result in self.infrastructure_issues.values()
        ]
        avg_score = sum(scores) / len(scores)

        if avg_score >= 90:
            return "excellent"
        if avg_score >= 75:
            return "good"
        if avg_score >= 50:
            return "fair"
        return "poor"


def run_gcp_ghostbusters(project_id: str = "default") -> dict[str, Any]:
    """
    Run GCP Ghostbusters investigation on the specified project.

    Args:
        project_id: GCP project ID to investigate

    Returns:
        Investigation results dictionary
    """
    # Initialize orchestrator with GCP-specific configuration
    config = {
        "investigation_mode": "gcp_comprehensive",
        "quality_threshold": 80.0,
        "gcp_services": ["cloud_build", "cloud_run", "cloud_storage"],
    }

    orchestrator = GCPGhostbustersOrchestrator(config)

    # Run GCP investigation
    return orchestrator.investigate_gcp_infrastructure(project_id)


def ghostbusters_analyze(project_id: str = "default") -> dict[str, Any]:
    """
    Analyze GCP infrastructure using Ghostbusters (alias for run_gcp_ghostbusters).

    Args:
        project_id: GCP project ID to investigate

    Returns:
        Investigation results dictionary
    """
    return run_gcp_ghostbusters(project_id)


def ghostbusters_history(project_id: str = "default") -> dict[str, Any]:
    """
    Get GCP infrastructure investigation history.

    Args:
        project_id: GCP project ID to investigate

    Returns:
        Investigation history dictionary
    """
    orchestrator = GCPGhostbustersOrchestrator()
    return orchestrator.get_gcp_investigation_summary()


def ghostbusters_status(request) -> tuple[dict[str, Any], int]:
    """
    Get status of a GCP infrastructure analysis.

    Args:
        request: Request object containing analysis_id

    Returns:
        Tuple of (response_dict, status_code)
    """
    try:
        data = request.get_json() if request else {}
        analysis_id = data.get("analysis_id")

        if not analysis_id:
            return {
                "status": "error",
                "error_message": "Missing analysis_id parameter",
            }, 400

        # Mock response for testing
        # In production, this would query a database
        mock_analysis = {
            "analysis_id": analysis_id,
            "status": "completed",
            "confidence_score": 0.95,
            "delusions_detected": [{"type": "security"}],
            "recovery_actions": [{"action": "fix"}],
            "timestamp": "2024-01-01T00:00:00Z",
        }

        return {
            "analysis_id": analysis_id,
            "status": mock_analysis["status"],
            "confidence_score": mock_analysis["confidence_score"],
            "delusions_detected": len(mock_analysis["delusions_detected"]),
            "recovery_actions": len(mock_analysis["recovery_actions"]),
        }, 200

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get analysis status: {str(e)}",
        }, 500


if __name__ == "__main__":
    # Example usage
    results = run_gcp_ghostbusters("my-gcp-project")
    print("☁️ GCP Ghostbusters Investigation Results:")
    print(json.dumps(results, indent=2))
