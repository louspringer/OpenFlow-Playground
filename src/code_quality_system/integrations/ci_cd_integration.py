#!/usr/bin/env python3
"""
CI/CD Integration

Integrates quality enforcement with CI/CD pipelines using multi-agent analysis.
"""

import logging
import os
from pathlib import Path
from typing import Any

from src.code_quality_system.multi_agent_integration import QualityMultiAgentAdapter
from src.code_quality_system.quality_enforcer import (
    QualityEnforcementError,
    QualityEnforcer,
)


class CICDIntegration:
    """Integrates quality enforcement with CI/CD pipelines using multi-agent analysis"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quality_enforcer = QualityEnforcer(project_path)
        self.quality_adapter = QualityMultiAgentAdapter(project_path)
        self.logger = logging.getLogger(__name__)

        # CI/CD environment detection
        self.ci_environment = self._detect_ci_environment()
        self.ci_config = self._load_ci_config()

        # Environment-specific quality rules
        self.environment_rules = self._load_environment_rules()

    def _detect_ci_environment(self) -> str:
        """Detect which CI/CD environment we're running in"""
        if os.getenv("GITHUB_ACTIONS"):
            return "github_actions"
        if os.getenv("GITLAB_CI"):
            return "gitlab_ci"
        if os.getenv("CIRCLECI"):
            return "circleci"
        if os.getenv("JENKINS_URL"):
            return "jenkins"
        if os.getenv("TRAVIS"):
            return "travis"
        if os.getenv("AZURE_DEVOPS"):
            return "azure_devops"
        return "unknown"

    def _load_ci_config(self) -> dict[str, Any]:
        """Load CI/CD specific configuration"""
        config = {
            "ci_environment": self.ci_environment,
            "quality_threshold": float(os.getenv("QUALITY_THRESHOLD", "70.0")),
            "fail_on_quality": os.getenv("FAIL_ON_QUALITY", "true").lower() == "true",
            "quality_report_path": os.getenv("QUALITY_REPORT_PATH", "quality_report.json"),
            "quality_metrics_path": os.getenv("QUALITY_METRICS_PATH", ".quality_metrics"),
            "verbose": os.getenv("QUALITY_VERBOSE", "false").lower() == "true",
            "environment": os.getenv("DEPLOYMENT_ENVIRONMENT", "development"),
        }

        self.logger.info(f"CI/CD Configuration: {config}")
        return config

    def _load_environment_rules(self) -> dict[str, Any]:
        """Load environment-specific quality rules"""
        environment = self.ci_config["environment"]

        # Environment-specific quality thresholds and rules
        rules = {
            "development": {
                "quality_threshold": 50.0,  # Lenient for rapid iteration
                "fail_on_quality": False,  # Don't block development
                "gate_severity": "medium",  # Medium severity gates
                "auto_fix_enabled": True,  # Allow auto-fixes
                "quality_reporting": "basic",
            },
            "staging": {
                "quality_threshold": 70.0,  # Moderate for validation
                "fail_on_quality": True,  # Block on moderate issues
                "gate_severity": "high",  # High severity gates
                "auto_fix_enabled": False,  # No auto-fixes in staging
                "quality_reporting": "detailed",
            },
            "production": {
                "quality_threshold": 85.0,  # Strict for production
                "fail_on_quality": True,  # Always block on issues
                "gate_severity": "critical",  # Critical severity gates
                "auto_fix_enabled": False,  # No auto-fixes in production
                "quality_reporting": "comprehensive",
            },
        }

        # Use environment-specific rules, fallback to development
        env_rules = rules[environment] if environment in rules else rules["development"]
        self.logger.info(f"Environment rules for {environment}: {env_rules}")

        return env_rules

    async def run_ci_quality_check(self) -> dict[str, Any]:
        """Run quality check for CI/CD pipeline"""
        self.logger.info(f"Running CI/CD quality check in {self.ci_environment}")

        try:
            # Configure enforcement based on CI environment
            self._configure_ci_enforcement()

            # Run quality check
            result = await self._run_quality_check()

            # Generate CI-specific report
            ci_report = self._generate_ci_report(result)

            # Save report for CI artifacts
            self._save_ci_report(ci_report)

            # Take CI-specific actions
            self._take_ci_actions(ci_report)

            return ci_report

        except Exception as e:
            self.logger.error(f"CI quality check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "ci_environment": self.ci_environment,
                "can_proceed": False,
            }

    def _configure_ci_enforcement(self) -> None:
        """Configure quality enforcement for CI environment"""
        # Use environment-specific rules
        env_rules = self.environment_rules

        # Configure enforcement based on environment
        enforcement_level = "strict" if env_rules["fail_on_quality"] else "moderate"
        block_on_failure = env_rules["fail_on_quality"]
        auto_fix_enabled = env_rules["auto_fix_enabled"]

        self.quality_enforcer.configure_enforcement(
            enforcement_level=enforcement_level,
            block_on_failure=block_on_failure,
            auto_fix_enabled=auto_fix_enabled,
        )

        # Set quality threshold from environment rules
        threshold = env_rules["quality_threshold"]
        self.logger.info(f"Setting quality threshold to {threshold} for {self.ci_config['environment']} environment")

        # Update CI config with environment-specific threshold
        self.ci_config["quality_threshold"] = threshold
        self.ci_config["fail_on_quality"] = env_rules["fail_on_quality"]

    async def _run_quality_check(self) -> dict[str, Any]:
        """Run the actual quality check using multi-agent analysis"""
        self.logger.info("Running multi-agent quality analysis for CI/CD")

        try:
            # Run multi-agent quality analysis
            # This integrates with our clewcrew framework
            multi_agent_results = await self._run_multi_agent_analysis()

            # Convert multi-agent results to quality metrics
            quality_metrics = await self.quality_adapter._convert_agent_results_to_metrics(multi_agent_results)

            # Run quality enforcement with the metrics
            enforcement_result = self.quality_enforcer.enforce_quality(quality_metrics)

            # Add multi-agent context to the result
            enforcement_result["multi_agent_analysis"] = {
                "agents_analyzed": len(multi_agent_results),
                "analysis_timestamp": multi_agent_results.get("timestamp", ""),
                "agent_results": multi_agent_results,
            }

            return enforcement_result

        except Exception as e:
            self.logger.error(f"Multi-agent quality analysis failed: {e}")
            # Fallback to basic analysis
            return self._run_fallback_quality_check()

    async def _run_multi_agent_analysis(self) -> dict[str, Any]:
        """Run quality analysis using the multi-agent framework"""
        try:
            # Import the orchestrator to run quality analysis
            import sys

            sys.path.insert(0, str(self.project_path / "clewcrew-core" / "src"))

            from clewcrew_core.orchestrator import ClewcrewOrchestrator

            # Create orchestrator and run quality analysis
            orchestrator = ClewcrewOrchestrator(str(self.project_path))

            return await orchestrator.run_quality_analysis(str(self.project_path))

        except Exception as e:
            self.logger.warning(f"Could not run multi-agent analysis: {e}")
            # Return empty results to trigger fallback
            return {}

    def _run_fallback_quality_check(self) -> dict[str, Any]:
        """Run fallback quality check when multi-agent analysis fails"""
        self.logger.info("Running fallback quality check")

        # Use the existing basic analysis logic
        analysis_results = self._get_ci_analysis_results()

        # Run quality enforcement
        return self.quality_enforcer.enforce_quality(analysis_results)

    def _get_ci_analysis_results(self) -> dict[str, Any]:
        """Get analysis results for CI environment"""
        # This is a placeholder - in practice, you'd integrate with your actual tools

        # Check for existing analysis outputs
        analysis_results = {
            "flake8_issues": [],
            "security_issues": [],
            "coverage_percentage": 0.0,
            "performance_metrics": {},
        }

        # Look for flake8 output
        flake8_output = self.project_path / "flake8_report.json"
        if flake8_output.exists():
            import json

            try:
                with open(flake8_output) as f:
                    flake8_data = json.load(f)
                    analysis_results["flake8_issues"] = flake8_data
            except Exception as e:
                self.logger.warning(f"Could not load flake8 report: {e}")

        # Look for security scan output
        security_output = self.project_path / "security_scan.json"
        if security_output.exists():
            import json

            try:
                with open(security_output) as f:
                    security_data = json.load(f)
                    analysis_results["security_issues"] = security_data
            except Exception as e:
                self.logger.warning(f"Could not load security scan: {e}")

        # Look for coverage report
        coverage_file = self.project_path / "coverage.xml"
        if coverage_file.exists():
            import xml.etree.ElementTree as ET

            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                coverage_elem = root.find(".//coverage")
                if coverage_elem is not None:
                    line_rate = float(coverage_elem.get("line-rate", "0"))
                    analysis_results["coverage_percentage"] = line_rate * 100.0
            except Exception as e:
                self.logger.warning(f"Could not parse coverage file: {e}")

        return analysis_results

    def _generate_ci_report(self, quality_result: dict[str, Any]) -> dict[str, Any]:
        """Generate CI-specific quality report"""
        return {
            "ci_environment": self.ci_environment,
            "timestamp": quality_result.get("timestamp", ""),
            "project_path": str(self.project_path),
            # Quality metrics
            "overall_score": quality_result.get("overall_score", 0.0),
            "quality_threshold": self.ci_config["quality_threshold"],
            "threshold_met": quality_result.get("overall_score", 0.0) >= self.ci_config["quality_threshold"],
            # Gate results
            "gate_summary": quality_result.get("gate_summary", {}),
            "can_proceed": quality_result.get("can_proceed", False),
            # CI-specific information
            "ci_config": self.ci_config,
            "build_info": self._get_build_info(),
            # Recommendations
            "recommendations": quality_result.get("recommendations", []),
            # Status
            "status": ("success" if quality_result.get("can_proceed", False) else "failed"),
        }

    def _get_build_info(self) -> dict[str, Any]:
        """Get build information from CI environment"""
        build_info = {
            "ci_environment": self.ci_environment,
            "build_id": os.getenv("BUILD_ID", "unknown"),
            "build_number": os.getenv("BUILD_NUMBER", "unknown"),
            "commit_sha": os.getenv("GITHUB_SHA") or os.getenv("CI_COMMIT_SHA", "unknown"),
            "branch": os.getenv("GITHUB_REF") or os.getenv("CI_COMMIT_REF_NAME", "unknown"),
            "triggered_by": os.getenv("GITHUB_ACTOR") or os.getenv("GITLAB_USER_NAME", "unknown"),
        }

        # Add environment-specific variables
        if self.ci_environment == "github_actions":
            build_info.update(
                {
                    "workflow": os.getenv("GITHUB_WORKFLOW", "unknown"),
                    "job": os.getenv("GITHUB_JOB", "unknown"),
                    "run_id": os.getenv("GITHUB_RUN_ID", "unknown"),
                }
            )
        elif self.ci_environment == "gitlab_ci":
            build_info.update(
                {
                    "pipeline_id": os.getenv("CI_PIPELINE_ID", "unknown"),
                    "job_id": os.getenv("CI_JOB_ID", "unknown"),
                    "stage": os.getenv("CI_JOB_STAGE", "unknown"),
                }
            )

        return build_info

    def _save_ci_report(self, ci_report: dict[str, Any]) -> None:
        """Save CI report for artifacts and review"""
        report_path = Path(self.ci_config["quality_report_path"])

        # Ensure directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)

        # Save report
        import json

        with open(report_path, "w") as f:
            json.dump(ci_report, f, indent=2)

        self.logger.info(f"CI quality report saved to {report_path}")

        # Also save to quality metrics directory
        metrics_dir = Path(self.ci_config["quality_metrics_path"])
        metrics_dir.mkdir(exist_ok=True)

        metrics_file = metrics_dir / f"ci_metrics_{self._get_build_info()['build_id']}.json"
        with open(metrics_file, "w") as f:
            json.dump(ci_report, f, indent=2)

        self.logger.info(f"CI metrics saved to {metrics_file}")

    def _take_ci_actions(self, ci_report: dict[str, Any]) -> None:
        """Take CI-specific actions based on quality results"""
        if not ci_report["can_proceed"]:
            self.logger.error("Quality gates failed - taking CI actions")

            # Log detailed failure information
            self._log_ci_failure(ci_report)

            # Set CI status
            self._set_ci_status(ci_report)

            # Fail the build if configured to do so
            if self.ci_config["fail_on_quality"]:
                error_message = f"Quality check failed with score {ci_report['overall_score']:.1f} (threshold: {ci_report['quality_threshold']:.1f})"
                raise QualityEnforcementError(error_message)
        else:
            self.logger.info("Quality gates passed - CI can proceed")

            # Set success status
            self._set_ci_status(ci_report)

    def _log_ci_failure(self, ci_report: dict[str, Any]) -> None:
        """Log detailed failure information for CI"""
        self.logger.error("=" * 60)
        self.logger.error("❌ CI QUALITY CHECK FAILED")
        self.logger.error("=" * 60)

        self.logger.error(f"Overall Quality Score: {ci_report['overall_score']:.1f}")
        self.logger.error(f"Quality Threshold: {ci_report['quality_threshold']:.1f}")
        self.logger.error(f"Threshold Met: {ci_report['threshold_met']}")

        if "gate_summary" in ci_report:
            gate_summary = ci_report["gate_summary"]
            self.logger.error(f"Total Gates: {gate_summary.get('total_gates', 0)}")
            self.logger.error(f"Failed Gates: {gate_summary.get('failed_gates', 0)}")
            self.logger.error(f"Blocking Gates: {gate_summary.get('blocking_gates', 0)}")

        if "recommendations" in ci_report:
            self.logger.error("Recommendations:")
            for rec in ci_report["recommendations"]:
                self.logger.error(f"  • {rec}")

        self.logger.error("=" * 60)

    def _set_ci_status(self, ci_report: dict[str, Any]) -> None:
        """Set CI status based on quality results"""
        if self.ci_environment == "github_actions":
            self._set_github_status(ci_report)
        elif self.ci_environment == "gitlab_ci":
            self._set_gitlab_status(ci_report)
        # Add other CI systems as needed

    def _set_github_status(self, ci_report: dict[str, Any]) -> None:
        """Set GitHub Actions status"""
        # This would integrate with GitHub API to set commit status
        # For now, just log the intended action
        status = "success" if ci_report["can_proceed"] else "failure"
        self.logger.info(f"Would set GitHub status to: {status}")

    def _set_gitlab_status(self, ci_report: dict[str, Any]) -> None:
        """Set GitLab CI status"""
        # This would integrate with GitLab API to set pipeline status
        # For now, just log the intended action
        status = "success" if ci_report["can_proceed"] else "failed"
        self.logger.info(f"Would set GitLab CI status to: {status}")

    def get_ci_summary(self) -> dict[str, Any]:
        """Get summary of CI quality check results"""
        try:
            report_path = Path(self.ci_config["quality_report_path"])
            if report_path.exists():
                import json

                with open(report_path) as f:
                    return json.load(f)
            else:
                return {"status": "no_report", "message": "No CI quality report found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def cleanup_ci_artifacts(self) -> None:
        """Clean up CI artifacts after build"""
        try:
            # Remove temporary quality reports
            report_path = Path(self.ci_config["quality_report_path"])
            if report_path.exists():
                report_path.unlink()
                self.logger.info(f"Cleaned up CI report: {report_path}")

            # Keep quality metrics for historical tracking
            self.logger.info("Quality metrics preserved for historical tracking")

        except Exception as e:
            self.logger.warning(f"Could not cleanup CI artifacts: {e}")
