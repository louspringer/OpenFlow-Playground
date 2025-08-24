"""
Report Generator for Security Scanning

This module generates comprehensive security reports from scanning results,
including multiple output formats and detailed analysis.
"""

import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates comprehensive security reports from scanning results

    Features:
    - Multiple output formats (JSON, console, HTML, Markdown)
    - Severity-based categorization
    - Performance metrics integration
    - Actionable recommendations
    - False positive filtering
    """

    def __init__(self, config=None):
        """
        Initialize report generator

        Args:
            config: Configuration manager (optional)
        """
        self.config = config

        logger.debug("Report generator initialized")

    def generate_report(
        self,
        findings: list[dict[str, Any]],
        performance_metrics: dict[str, Any],
        project_path: str,
        scan_duration: float,
    ) -> dict[str, Any]:
        """
        Generate comprehensive security report

        Args:
            findings: List of security findings
            performance_metrics: Performance metrics from worker pool
            project_path: Path to project that was scanned
            scan_duration: Total scan duration in seconds

        Returns:
            Comprehensive security report
        """
        # Separate real issues from false positives
        real_issues = [f for f in findings if not f.get("false_positive", False)]
        false_positives = [f for f in findings if f.get("false_positive", False)]

        # Group findings by severity
        findings_by_severity = self._group_findings_by_severity(real_issues)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            real_issues, performance_metrics
        )

        # Create comprehensive report
        report = {
            "summary": {
                "project_path": project_path,
                "scan_duration": scan_duration,
                "files_scanned": performance_metrics.get("tasks_completed", 0),
                "findings_count": len(real_issues),
                "false_positives_count": len(false_positives),
                "status": "completed" if real_issues else "clean",
                "critical_issues": len(findings_by_severity.get("CRITICAL", [])),
                "high_issues": len(findings_by_severity.get("HIGH", [])),
                "medium_issues": len(findings_by_severity.get("MEDIUM", [])),
                "low_issues": len(findings_by_severity.get("LOW", [])),
            },
            "performance": performance_metrics,
            "findings_by_severity": findings_by_severity,
            "all_findings": real_issues,
            "false_positives": false_positives,
            "recommendations": recommendations,
            "metadata": {
                "generator_version": "1.0.0",
                "scan_timestamp": self._get_timestamp(),
                "total_files_processed": performance_metrics.get("tasks_completed", 0),
                "scan_efficiency": self._calculate_scan_efficiency(
                    performance_metrics, scan_duration
                ),
            },
        }

        return report

    def _group_findings_by_severity(
        self, findings: list[dict[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Group findings by severity level

        Args:
            findings: List of security findings

        Returns:
            Dictionary of findings grouped by severity
        """
        grouped = {}

        for finding in findings:
            severity = finding.get("severity", "LOW")
            if severity not in grouped:
                grouped[severity] = []
            grouped[severity].append(finding)

        return grouped

    def _generate_recommendations(
        self, findings: list[dict[str, Any]], performance_metrics: dict[str, Any]
    ) -> list[str]:
        """
        Generate actionable recommendations based on findings

        Args:
            findings: List of security findings
            performance_metrics: Performance metrics

        Returns:
            List of recommendations
        """
        recommendations = []

        # Count findings by severity
        critical_count = len([f for f in findings if f.get("severity") == "CRITICAL"])
        high_count = len([f for f in findings if f.get("severity") == "HIGH"])

        # Critical issues
        if critical_count > 0:
            recommendations.append(
                f"🚨 IMMEDIATE ACTION REQUIRED: {critical_count} critical security issues found. "
                "Review and fix these immediately before any deployment."
            )

        # High priority issues
        if high_count > 0:
            recommendations.append(
                f"⚠️ HIGH PRIORITY: {high_count} high-severity security issues found. "
                "Address these before production deployment."
            )

        # Performance recommendations
        if performance_metrics:
            worker_count = performance_metrics.get("worker_count", 0)
            throughput = performance_metrics.get("throughput", 0)

            if throughput < 100:  # Less than 100 files/second
                recommendations.append(
                    "🔧 PERFORMANCE: Consider increasing worker count or optimizing file processing "
                    f"for better throughput (current: {throughput:.1f} files/second)"
                )

            if worker_count < 4:
                recommendations.append(
                    "🔧 PERFORMANCE: Consider increasing worker count for better parallel processing "
                    f"(current: {worker_count} workers)"
                )

        # Pattern-specific recommendations
        pattern_counts = {}
        for finding in findings:
            pattern = finding.get("pattern_name", "Unknown")
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        for pattern, count in pattern_counts.items():
            if count > 5:
                recommendations.append(
                    f"🔍 PATTERN ALERT: {count} instances of '{pattern}' found. "
                    "Consider implementing automated detection for this pattern."
                )

        # General recommendations
        if not findings:
            recommendations.append(
                "✅ No immediate security issues detected. Continue with regular security practices."
            )
        else:
            recommendations.append(
                "🔍 Review all findings and implement fixes based on severity and business impact."
            )

        return recommendations

    def _calculate_scan_efficiency(
        self, performance_metrics: dict[str, Any], scan_duration: float
    ) -> dict[str, Any]:
        """
        Calculate scan efficiency metrics

        Args:
            performance_metrics: Performance metrics from worker pool
            scan_duration: Total scan duration

        Returns:
            Dictionary of efficiency metrics
        """
        files_processed = performance_metrics.get("tasks_completed", 0)

        if scan_duration <= 0 or files_processed <= 0:
            return {
                "files_per_second": 0,
                "efficiency_score": 0,
                "worker_utilization": 0,
            }

        files_per_second = files_processed / scan_duration
        worker_count = performance_metrics.get("worker_count", 1)

        # Calculate efficiency score (0-100)
        # Base score on throughput and worker utilization
        base_score = min(100, files_per_second * 10)  # 10 files/sec = 100 score

        # Adjust for worker utilization
        worker_utilization = performance_metrics.get("average_cpu_usage", 0) / 100
        efficiency_score = base_score * (0.7 + 0.3 * worker_utilization)

        return {
            "files_per_second": files_per_second,
            "efficiency_score": min(100, efficiency_score),
            "worker_utilization": worker_utilization * 100,
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime

        return datetime.now().isoformat()

    def export_json(
        self, report: dict[str, Any], output_file: str = "security_report.json"
    ) -> str:
        """
        Export report to JSON file

        Args:
            report: Security report to export
            output_file: Output file path

        Returns:
            Path to exported file
        """
        try:
            with open(output_file, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Security report exported to {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Failed to export JSON report: {e}")
            raise

    def print_console_report(self, report: dict[str, Any]):
        """
        Print formatted report to console

        Args:
            report: Security report to print
        """
        summary = report["summary"]
        findings_by_severity = report["findings_by_severity"]
        recommendations = report["recommendations"]
        performance = report["performance"]

        print("\n🔒 Security Scan Report")
        print("=" * 50)
        print(f"Project: {summary['project_path']}")
        print(f"Scan Duration: {summary['scan_duration']:.2f}s")
        print(f"Files Scanned: {summary['files_scanned']}")
        print(f"Findings: {summary['findings_count']}")
        print(f"False Positives: {summary['false_positives_count']}")
        print(f"Status: {summary['status'].upper()}")

        print(f"\n📊 Findings by Severity:")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity in findings_by_severity:
                count = len(findings_by_severity[severity])
                icon = (
                    "🚨"
                    if severity == "CRITICAL"
                    else "⚠️"
                    if severity == "HIGH"
                    else "🔍"
                )
                print(f"  {icon} {severity}: {count}")

        print(f"\n🎯 Critical Findings: {summary['critical_issues']}")
        if summary["critical_issues"] > 0:
            critical_findings = findings_by_severity.get("CRITICAL", [])
            for finding in critical_findings[:3]:  # Show first 3
                print(
                    f"  🚨 {finding['pattern_name']} in {finding['file_path']}:{finding['line_number']}"
                )
                print(f"     {finding['matched_text'][:50]}...")

            if summary["critical_issues"] > 3:
                print(
                    f"  ... and {summary['critical_issues'] - 3} more critical findings"
                )

        print(f"\n💡 Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")

        if performance:
            print(f"\n📈 Performance Summary:")
            print(f"  Workers: {performance.get('worker_count', 0)}")
            print(f"  Throughput: {performance.get('throughput', 0):.1f} files/second")
            print(f"  Success Rate: {performance.get('success_rate', 0) * 100:.1f}%")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
