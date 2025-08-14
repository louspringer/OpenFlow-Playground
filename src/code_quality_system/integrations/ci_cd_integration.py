#!/usr/bin/env python3
"""
CI/CD Integration

Integrates quality enforcement with CI/CD pipelines.
"""

from pathlib import Path
from typing import Any, Dict
import logging
import os

from ..quality_enforcer import QualityEnforcer, QualityEnforcementError


class CICDIntegration:
    """Integrates quality enforcement with CI/CD pipelines"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quality_enforcer = QualityEnforcer(project_path)
        self.logger = logging.getLogger(__name__)
        
        # CI/CD environment detection
        self.ci_environment = self._detect_ci_environment()
        self.ci_config = self._load_ci_config()
    
    def _detect_ci_environment(self) -> str:
        """Detect which CI/CD environment we're running in"""
        if os.getenv("GITHUB_ACTIONS"):
            return "github_actions"
        elif os.getenv("GITLAB_CI"):
            return "gitlab_ci"
        elif os.getenv("CIRCLECI"):
            return "circleci"
        elif os.getenv("JENKINS_URL"):
            return "jenkins"
        elif os.getenv("TRAVIS"):
            return "travis"
        elif os.getenv("AZURE_DEVOPS"):
            return "azure_devops"
        else:
            return "unknown"
    
    def _load_ci_config(self) -> Dict[str, Any]:
        """Load CI/CD specific configuration"""
        config = {
            "ci_environment": self.ci_environment,
            "quality_threshold": float(os.getenv("QUALITY_THRESHOLD", "70.0")),
            "fail_on_quality": os.getenv("FAIL_ON_QUALITY", "true").lower() == "true",
            "quality_report_path": os.getenv("QUALITY_REPORT_PATH", "quality_report.json"),
            "quality_metrics_path": os.getenv("QUALITY_METRICS_PATH", ".quality_metrics"),
            "verbose": os.getenv("QUALITY_VERBOSE", "false").lower() == "true"
        }
        
        self.logger.info(f"CI/CD Configuration: {config}")
        return config
    
    def run_ci_quality_check(self) -> Dict[str, Any]:
        """Run quality check for CI/CD pipeline"""
        self.logger.info(f"Running CI/CD quality check in {self.ci_environment}")
        
        try:
            # Configure enforcement based on CI environment
            self._configure_ci_enforcement()
            
            # Run quality check
            result = self._run_quality_check()
            
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
                "can_proceed": False
            }
    
    def _configure_ci_enforcement(self) -> None:
        """Configure quality enforcement for CI environment"""
        # In CI, we want strict enforcement
        self.quality_enforcer.configure_enforcement(
            enforcement_level="strict",
            block_on_failure=True,
            auto_fix_enabled=False
        )
        
        # Set quality threshold from CI config
        threshold = self.ci_config["quality_threshold"]
        self.logger.info(f"Setting quality threshold to {threshold}")
    
    def _run_quality_check(self) -> Dict[str, Any]:
        """Run the actual quality check"""
        # For CI, we need to run a full analysis
        # This would typically integrate with your multi-agent testing framework
        
        # For now, create a mock analysis result
        # In practice, this would come from your actual analysis tools
        analysis_results = self._get_ci_analysis_results()
        
        # Run quality enforcement
        return self.quality_enforcer.enforce_quality(analysis_results)
    
    def _get_ci_analysis_results(self) -> Dict[str, Any]:
        """Get analysis results for CI environment"""
        # This is a placeholder - in practice, you'd integrate with your actual tools
        
        # Check for existing analysis outputs
        analysis_results = {
            "flake8_issues": [],
            "security_issues": [],
            "coverage_percentage": 0.0,
            "performance_metrics": {}
        }
        
        # Look for flake8 output
        flake8_output = self.project_path / "flake8_report.json"
        if flake8_output.exists():
            import json
            try:
                with open(flake8_output, 'r') as f:
                    flake8_data = json.load(f)
                    analysis_results["flake8_issues"] = flake8_data
            except Exception as e:
                self.logger.warning(f"Could not load flake8 report: {e}")
        
        # Look for security scan output
        security_output = self.project_path / "security_scan.json"
        if security_output.exists():
            import json
            try:
                with open(security_output, 'r') as f:
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
    
    def _generate_ci_report(self, quality_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CI-specific quality report"""
        ci_report = {
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
            "status": "success" if quality_result.get("can_proceed", False) else "failed"
        }
        
        return ci_report
    
    def _get_build_info(self) -> Dict[str, Any]:
        """Get build information from CI environment"""
        build_info = {
            "ci_environment": self.ci_environment,
            "build_id": os.getenv("BUILD_ID", "unknown"),
            "build_number": os.getenv("BUILD_NUMBER", "unknown"),
            "commit_sha": os.getenv("GITHUB_SHA") or os.getenv("CI_COMMIT_SHA", "unknown"),
            "branch": os.getenv("GITHUB_REF") or os.getenv("CI_COMMIT_REF_NAME", "unknown"),
            "triggered_by": os.getenv("GITHUB_ACTOR") or os.getenv("GITLAB_USER_NAME", "unknown")
        }
        
        # Add environment-specific variables
        if self.ci_environment == "github_actions":
            build_info.update({
                "workflow": os.getenv("GITHUB_WORKFLOW", "unknown"),
                "job": os.getenv("GITHUB_JOB", "unknown"),
                "run_id": os.getenv("GITHUB_RUN_ID", "unknown")
            })
        elif self.ci_environment == "gitlab_ci":
            build_info.update({
                "pipeline_id": os.getenv("CI_PIPELINE_ID", "unknown"),
                "job_id": os.getenv("CI_JOB_ID", "unknown"),
                "stage": os.getenv("CI_JOB_STAGE", "unknown")
            })
        
        return build_info
    
    def _save_ci_report(self, ci_report: Dict[str, Any]) -> None:
        """Save CI report for artifacts and review"""
        report_path = Path(self.ci_config["quality_report_path"])
        
        # Ensure directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save report
        import json
        with open(report_path, 'w') as f:
            json.dump(ci_report, f, indent=2)
        
        self.logger.info(f"CI quality report saved to {report_path}")
        
        # Also save to quality metrics directory
        metrics_dir = Path(self.ci_config["quality_metrics_path"])
        metrics_dir.mkdir(exist_ok=True)
        
        metrics_file = metrics_dir / f"ci_metrics_{self._get_build_info()['build_id']}.json"
        with open(metrics_file, 'w') as f:
            json.dump(ci_report, f, indent=2)
        
        self.logger.info(f"CI metrics saved to {metrics_file}")
    
    def _take_ci_actions(self, ci_report: Dict[str, Any]) -> None:
        """Take CI-specific actions based on quality results"""
        if not ci_report["can_proceed"]:
            self.logger.error("Quality gates failed - taking CI actions")
            
            # Log detailed failure information
            self._log_ci_failure(ci_report)
            
            # Set CI status
            self._set_ci_status(ci_report)
            
            # Fail the build if configured to do so
            if self.ci_config["fail_on_quality"]:
                raise QualityEnforcementError(
                    f"Quality check failed with score {ci_report['overall_score']:.1f} "
                    f"(threshold: {ci_report['quality_threshold']:.1f})"
                )
        else:
            self.logger.info("Quality gates passed - CI can proceed")
            
            # Set success status
            self._set_ci_status(ci_report)
    
    def _log_ci_failure(self, ci_report: Dict[str, Any]) -> None:
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
    
    def _set_ci_status(self, ci_report: Dict[str, Any]) -> None:
        """Set CI status based on quality results"""
        if self.ci_environment == "github_actions":
            self._set_github_status(ci_report)
        elif self.ci_environment == "gitlab_ci":
            self._set_gitlab_status(ci_report)
        # Add other CI systems as needed
    
    def _set_github_status(self, ci_report: Dict[str, Any]) -> None:
        """Set GitHub Actions status"""
        # This would integrate with GitHub API to set commit status
        # For now, just log the intended action
        status = "success" if ci_report["can_proceed"] else "failure"
        self.logger.info(f"Would set GitHub status to: {status}")
    
    def _set_gitlab_status(self, ci_report: Dict[str, Any]) -> None:
        """Set GitLab CI status"""
        # This would integrate with GitLab API to set pipeline status
        # For now, just log the intended action
        status = "success" if ci_report["can_proceed"] else "failed"
        self.logger.info(f"Would set GitLab CI status to: {status}")
    
    def get_ci_summary(self) -> Dict[str, Any]:
        """Get summary of CI quality check results"""
        try:
            report_path = Path(self.ci_config["quality_report_path"])
            if report_path.exists():
                import json
                with open(report_path, 'r') as f:
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
