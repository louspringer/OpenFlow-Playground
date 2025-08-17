#!/usr/bin/env python3
"""
Security Scanning Quality Integration

Integrates security scanning results with the existing quality system
to provide actionable security insights in quality gates.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .security_scanner import SecurityScanManager, SecurityScanResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SecurityQualityMetrics:
    """Security metrics for quality system integration"""

    total_security_issues: int
    high_severity_issues: int
    medium_severity_issues: int
    low_severity_issues: int
    security_score: float  # 0.0 to 100.0
    critical_issues: list[str]
    actionable_items: list[str]
    last_scan_timestamp: str


class SecurityQualityIntegrator:
    """Integrates security scanning with quality system"""

    def __init__(self, security_manager: SecurityScanManager):
        self.security_manager = security_manager
        self.quality_metrics_file = Path("security_quality_metrics.json")

    def run_security_quality_check(self, days_back: int = 30) -> SecurityQualityMetrics:
        """Run security scan and generate quality metrics"""
        logger.info("Running security quality check...")

        # Run security scan
        scan_result = self.security_manager.run_security_scan(days_back)

        # Calculate security score
        security_score = self._calculate_security_score(scan_result)

        # Identify critical issues
        critical_issues = self._identify_critical_issues(scan_result)

        # Generate quality metrics
        metrics = SecurityQualityMetrics(
            total_security_issues=scan_result.total_issues,
            high_severity_issues=scan_result.high_severity,
            medium_severity_issues=scan_result.medium_severity,
            low_severity_issues=scan_result.low_severity,
            security_score=security_score,
            critical_issues=critical_issues,
            actionable_items=scan_result.actionable_items,
            last_scan_timestamp=scan_result.timestamp,
        )

        # Save metrics for quality system
        self._save_quality_metrics(metrics)

        return metrics

    def _calculate_security_score(self, scan_result: SecurityScanResult) -> float:
        """Calculate security score from 0.0 to 100.0"""
        if scan_result.total_issues == 0:
            return 100.0

        # Weight different severity levels
        high_weight = 10.0
        medium_weight = 5.0
        low_weight = 1.0

        total_weighted_issues = (
            scan_result.high_severity * high_weight
            + scan_result.medium_severity * medium_weight
            + scan_result.low_severity * low_weight
        )

        # Calculate score (higher is better)
        max_possible_issues = 100  # Arbitrary maximum for scoring
        score = max(0.0, 100.0 - (total_weighted_issues / max_possible_issues) * 100.0)

        return round(score, 1)

    def _identify_critical_issues(self, scan_result: SecurityScanResult) -> list[str]:
        """Identify critical security issues that need immediate attention"""
        critical_issues = []

        # High severity issues are always critical
        if scan_result.high_severity > 0:
            critical_issues.append(
                f"{scan_result.high_severity} high severity security issues detected"
            )

        # Check for specific critical patterns
        for issue in scan_result.issues:
            if issue.detector_name in [
                "aws_access_key_id",
                "github_token",
                "company_email_password",
            ]:
                if issue.severity == "high":
                    critical_issues.append(
                        f"Critical: {issue.detector_display_name} in {issue.filepath}"
                    )

        # Add general critical warnings
        if scan_result.total_issues > 10:
            critical_issues.append(
                "High volume of security issues - review security practices"
            )

        return critical_issues

    def _save_quality_metrics(self, metrics: SecurityQualityMetrics):
        """Save security quality metrics for integration with quality system"""
        try:
            metrics_dict = {
                "timestamp": metrics.last_scan_timestamp,
                "total_security_issues": metrics.total_security_issues,
                "high_severity_issues": metrics.high_severity_issues,
                "medium_severity_issues": metrics.medium_severity_issues,
                "low_severity_issues": metrics.low_severity_issues,
                "security_score": metrics.security_score,
                "critical_issues": metrics.critical_issues,
                "actionable_items": metrics.actionable_items,
            }

            with open(self.quality_metrics_file, "w") as f:
                json.dump(metrics_dict, f, indent=2)

            logger.info(
                f"Security quality metrics saved to {self.quality_metrics_file}"
            )
        except Exception as e:
            logger.error(f"Failed to save quality metrics: {e}")

    def get_latest_quality_metrics(self) -> Optional[SecurityQualityMetrics]:
        """Get the latest security quality metrics"""
        if not self.quality_metrics_file.exists():
            return None

        try:
            with open(self.quality_metrics_file) as f:
                data = json.load(f)

            return SecurityQualityMetrics(
                total_security_issues=data["total_security_issues"],
                high_severity_issues=data["high_severity_issues"],
                medium_severity_issues=data["medium_severity_issues"],
                low_severity_issues=data["low_severity_issues"],
                security_score=data["security_score"],
                critical_issues=data["critical_issues"],
                actionable_items=data["actionable_items"],
                last_scan_timestamp=data["timestamp"],
            )
        except Exception as e:
            logger.error(f"Failed to load quality metrics: {e}")
            return None

    def generate_quality_report(self) -> dict[str, Any]:
        """Generate comprehensive quality report for integration"""
        metrics = self.get_latest_quality_metrics()
        if not metrics:
            return {"error": "No security quality metrics available"}

        # Determine quality status
        if metrics.security_score >= 90.0:
            status = "EXCELLENT"
            status_emoji = "🟢"
        elif metrics.security_score >= 70.0:
            status = "GOOD"
            status_emoji = "🟡"
        elif metrics.security_score >= 50.0:
            status = "FAIR"
            status_emoji = "🟠"
        else:
            status = "POOR"
            status_emoji = "🔴"

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics)

        return {
            "status": status,
            "status_emoji": status_emoji,
            "security_score": metrics.security_score,
            "total_issues": metrics.total_security_issues,
            "severity_breakdown": {
                "high": metrics.high_severity_issues,
                "medium": metrics.medium_severity_issues,
                "low": metrics.low_severity_issues,
            },
            "critical_issues": metrics.critical_issues,
            "actionable_items": metrics.actionable_items,
            "recommendations": recommendations,
            "last_scan": metrics.last_scan_timestamp,
        }

    def _generate_recommendations(self, metrics: SecurityQualityMetrics) -> list[str]:
        """Generate specific recommendations based on security metrics"""
        recommendations = []

        # Score-based recommendations
        if metrics.security_score < 50.0:
            recommendations.append("🚨 CRITICAL: Immediate security review required")
            recommendations.append("Implement emergency security measures")

        if metrics.security_score < 70.0:
            recommendations.append("⚠️  HIGH: Security improvements needed")
            recommendations.append("Review and fix high-severity issues")

        if metrics.security_score < 90.0:
            recommendations.append("📋 MEDIUM: Security optimization recommended")
            recommendations.append("Address medium-severity issues")

        # Issue-specific recommendations
        if metrics.high_severity_issues > 0:
            recommendations.append(
                f"🔴 Fix {metrics.high_severity_issues} high-severity issues immediately"
            )

        if metrics.medium_severity_issues > 5:
            recommendations.append(
                f"🟡 Address {metrics.medium_severity_issues} medium-severity issues"
            )

        if metrics.total_security_issues > 20:
            recommendations.append(
                "📊 High volume of issues - review security practices and policies"
            )

        # General recommendations
        recommendations.append("🔒 Implement pre-commit security scanning")
        recommendations.append("📚 Schedule security training for development team")
        recommendations.append("🔄 Establish regular security review cycles")

        return recommendations


class SecurityQualityGate:
    """Security quality gate for CI/CD integration"""

    def __init__(self, integrator: SecurityQualityIntegrator):
        self.integrator = integrator
        self.minimum_security_score = 70.0
        self.max_high_severity_issues = 0
        self.max_total_issues = 10

    def evaluate_security_gate(self) -> dict[str, Any]:
        """Evaluate if security meets quality gate requirements"""
        metrics = self.integrator.get_latest_quality_metrics()
        if not metrics:
            return {
                "passed": False,
                "reason": "No security metrics available",
                "recommendation": "Run security scan first",
            }

        # Check security score
        score_passed = metrics.security_score >= self.minimum_security_score

        # Check high severity issues
        high_severity_passed = (
            metrics.high_severity_issues <= self.max_high_severity_issues
        )

        # Check total issues
        total_issues_passed = metrics.total_security_issues <= self.max_total_issues

        # Overall gate evaluation
        gate_passed = score_passed and high_severity_passed and total_issues_passed

        # Generate detailed report
        report = {
            "gate_passed": gate_passed,
            "security_score": {
                "value": metrics.security_score,
                "required": self.minimum_security_score,
                "passed": score_passed,
            },
            "high_severity_issues": {
                "value": metrics.high_severity_issues,
                "max_allowed": self.max_high_severity_issues,
                "passed": high_severity_passed,
            },
            "total_issues": {
                "value": metrics.total_security_issues,
                "max_allowed": self.max_total_issues,
                "passed": total_issues_passed,
            },
            "critical_issues": metrics.critical_issues,
            "actionable_items": metrics.actionable_items,
            "recommendations": self._generate_gate_recommendations(
                metrics, gate_passed
            ),
        }

        return report

    def _generate_gate_recommendations(
        self, metrics: SecurityQualityMetrics, gate_passed: bool
    ) -> list[str]:
        """Generate recommendations based on gate evaluation"""
        recommendations = []

        if gate_passed:
            recommendations.append("✅ Security quality gate passed")
            if metrics.security_score < 90.0:
                recommendations.append("📈 Consider improving security score above 90.0")
        else:
            recommendations.append("❌ Security quality gate failed")

            if metrics.security_score < self.minimum_security_score:
                recommendations.append(
                    f"📊 Improve security score from {metrics.security_score} to {self.minimum_security_score}+"
                )

            if metrics.high_severity_issues > self.max_high_severity_issues:
                recommendations.append(
                    f"🔴 Fix {metrics.high_severity_issues} high-severity issues (max allowed: {self.max_high_severity_issues})"
                )

            if metrics.total_security_issues > self.max_total_issues:
                recommendations.append(
                    f"📋 Reduce total issues from {metrics.total_security_issues} to {self.max_total_issues} or fewer"
                )

        # Add specific actionable items
        recommendations.extend(metrics.actionable_items[:3])  # Top 3 actionable items

        return recommendations


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Security Quality Integration")
    parser.add_argument("--api-token", help="GitGuardian API token (or use 1Password)")
    parser.add_argument(
        "--days-back", type=int, default=30, help="Number of days to look back"
    )
    parser.add_argument(
        "--quality-gate", action="store_true", help="Run quality gate evaluation"
    )
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Get API token from 1Password if not provided
    api_token = args.api_token
    if not api_token:
        try:
            from .op_integration import CredentialManager
            credential_manager = CredentialManager()
            api_token = credential_manager.get_gitguardian_api_token()
            if not api_token:
                print("❌ Failed to get GitGuardian API token from 1Password")
                print("Please provide --api-token or ensure 1Password is configured")
                return
        except ImportError:
            print("❌ 1Password integration not available")
            print("Please provide --api-token")
            return
    
    # Initialize components
    security_manager = SecurityScanManager(api_token)
    integrator = SecurityQualityIntegrator(security_manager)

    if args.quality_gate:
        # Run quality gate evaluation
        gate = SecurityQualityGate(integrator)
        result = gate.evaluate_security_gate()

        print("\n" + "=" * 60)
        print("SECURITY QUALITY GATE EVALUATION")
        print("=" * 60)
        print(f"Gate Status: {'✅ PASSED' if result['gate_passed'] else '❌ FAILED'}")
        print(
            f"Security Score: {result['security_score']['value']}/{result['security_score']['required']}"
        )
        print(
            f"High Severity Issues: {result['high_severity_issues']['value']}/{result['high_severity_issues']['max_allowed']}"
        )
        print(
            f"Total Issues: {result['total_issues']['value']}/{result['total_issues']['max_allowed']}"
        )

        if result["critical_issues"]:
            print("\n🚨 Critical Issues:")
            for issue in result["critical_issues"]:
                print(f"  • {issue}")

        print("\n📋 Recommendations:")
        for rec in result["recommendations"]:
            print(f"  • {rec}")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\nDetailed results saved to: {args.output}")
    else:
        # Run security quality check
        metrics = integrator.run_security_quality_check(args.days_back)

        print("\n" + "=" * 60)
        print("SECURITY QUALITY CHECK RESULTS")
        print("=" * 60)
        print(f"Security Score: {metrics.security_score}/100.0")
        print(f"Total Issues: {metrics.total_security_issues}")
        print(f"High Severity: {metrics.high_severity_issues}")
        print(f"Medium Severity: {metrics.medium_severity_issues}")
        print(f"Low Severity: {metrics.low_severity_issues}")

        if metrics.critical_issues:
            print("\n🚨 Critical Issues:")
            for issue in metrics.critical_issues:
                print(f"  • {issue}")

        print("\n📋 Actionable Items:")
        for item in metrics.actionable_items:
            print(f"  • {item}")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(
                    {
                        "timestamp": metrics.last_scan_timestamp,
                        "security_score": metrics.security_score,
                        "total_issues": metrics.total_security_issues,
                        "high_severity": metrics.high_severity_issues,
                        "medium_severity": metrics.medium_severity_issues,
                        "low_severity": metrics.low_severity_issues,
                        "critical_issues": metrics.critical_issues,
                        "actionable_items": metrics.actionable_items,
                    },
                    f,
                    indent=2,
                )
            print(f"\nDetailed results saved to: {args.output}")


if __name__ == "__main__":
    main()
