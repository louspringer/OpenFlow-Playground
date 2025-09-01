#!/usr/bin/env python3
"""
Security Scanner for OpenFlow-Playground

Integrates with GitGuardian API to provide actionable security insights
and integrates with the existing quality system.
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SecurityIssue:
    """Represents a security issue found by GitGuardian"""

    id: int
    detector_name: str
    detector_display_name: str
    severity: str
    status: str
    date: str
    filepath: str
    line_number: Optional[int]
    secret_type: str
    description: str
    remediation: str
    priority: str


@dataclass
class SecurityScanResult:
    """Results of a security scan"""

    timestamp: str
    total_issues: int
    high_severity: int
    medium_severity: int
    low_severity: int
    issues: list[SecurityIssue]
    summary: str
    actionable_items: list[str]


class GitGuardianSecurityScanner:
    """Security scanner using GitGuardian API"""

    def __init__(self, api_token: str, base_url: str = "https://api.gitguardian.com/v1"):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {"Authorization": f"Token {api_token}"}

    def get_security_incidents(self, days_back: int = 30) -> list[dict[str, Any]]:
        """Get security incidents from GitGuardian API"""
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days_back)

            params = {
                "date_after": start_date.isoformat() + "Z",
                "date_before": end_date.isoformat() + "Z",
                "per_page": 100,
            }

            response = requests.get(
                f"{self.base_url}/incidents/secrets",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()

            return response.json()
        except Exception as e:
            logger.error(f"Failed to get security incidents: {e}")
            return []

    def get_incident_details(self, incident_id: int) -> Optional[dict[str, Any]]:
        """Get detailed information about a specific incident"""
        try:
            response = requests.get(f"{self.base_url}/incidents/secrets/{incident_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get incident details for {incident_id}: {e}")
            return None

    def analyze_security_issues(self, incidents: list[dict[str, Any]]) -> SecurityScanResult:
        """Analyze security incidents and provide actionable insights"""
        security_issues = []

        for incident in incidents:
            incident_details = self.get_incident_details(incident["id"])
            if not incident_details:
                continue

            # Extract file information from occurrences
            for occurrence in incident_details.get("occurrences", []):
                issue = SecurityIssue(
                    id=incident["id"],
                    detector_name=incident["detector"]["name"],
                    detector_display_name=incident["detector"]["display_name"],
                    severity=incident["severity"],
                    status=incident["status"],
                    date=incident["date"],
                    filepath=occurrence.get("filepath", "Unknown"),
                    line_number=occurrence.get("post_line_start"),
                    secret_type=incident["detector"]["family"],
                    description=self._get_issue_description(incident),
                    remediation=self._get_remediation_steps(incident),
                    priority=self._calculate_priority(incident),
                )
                security_issues.append(issue)

        # Calculate statistics
        high_severity = len([i for i in security_issues if i.severity == "high"])
        medium_severity = len([i for i in security_issues if i.severity == "medium"])
        low_severity = len([i for i in security_issues if i.severity == "low"])

        # Generate actionable items
        actionable_items = self._generate_actionable_items(security_issues)

        # Create summary
        summary = self._create_summary(security_issues, high_severity, medium_severity, low_severity)

        return SecurityScanResult(
            timestamp=datetime.utcnow().isoformat(),
            total_issues=len(security_issues),
            high_severity=high_severity,
            medium_severity=medium_severity,
            low_severity=low_severity,
            issues=security_issues,
            summary=summary,
            actionable_items=actionable_items,
        )

    def _get_issue_description(self, incident: dict[str, Any]) -> str:
        """Generate a human-readable description of the security issue"""
        detector = incident["detector"]
        return f"{detector['display_name']} detected in {incident.get('occurrences_count', 0)} location(s)"

    def _get_remediation_steps(self, incident: dict[str, Any]) -> str:
        """Generate remediation steps based on the type of issue"""
        detector_name = incident["detector"]["name"]

        remediation_steps = {
            "company_email_password": "Remove hardcoded credentials, use environment variables or secure credential storage",
            "aws_access_key_id": "Rotate AWS access keys, remove from code, use IAM roles or environment variables",
            "github_token": "Revoke exposed token, generate new one, use environment variables",
            "generic": "Remove sensitive information from code, use secure configuration management",
        }

        return remediation_steps.get(detector_name, remediation_steps["generic"])

    def _calculate_priority(self, incident: dict[str, Any]) -> str:
        """Calculate priority based on severity and status"""
        if incident["severity"] == "high" and incident["status"] == "TRIGGERED":
            return "CRITICAL"
        if incident["severity"] == "high":
            return "HIGH"
        if incident["severity"] == "medium":
            return "MEDIUM"
        return "LOW"

    def _generate_actionable_items(self, issues: list[SecurityIssue]) -> list[str]:
        """Generate actionable items for the security team"""
        actionable_items = []

        # Group issues by type
        issue_types = {}
        for issue in issues:
            if issue.detector_name not in issue_types:
                issue_types[issue.detector_name] = []
            issue_types[issue.detector_name].append(issue)

        # Generate specific actions
        for detector_name, detector_issues in issue_types.items():
            if detector_name == "company_email_password":
                actionable_items.append(f"Review {len(detector_issues)} files with exposed email credentials")
                actionable_items.append("Implement secure credential management for email services")
            elif detector_name == "aws_access_key_id":
                actionable_items.append(f"Rotate {len(detector_issues)} exposed AWS access keys")
                actionable_items.append("Review AWS IAM policies and implement least privilege")
            elif detector_name == "github_token":
                actionable_items.append(f"Revoke {len(detector_issues)} exposed GitHub tokens")
                actionable_items.append("Implement secure token management and rotation")

        # Add general actions
        if issues:
            actionable_items.append("Update security policies to prevent credential exposure")
            actionable_items.append("Implement pre-commit hooks for credential scanning")
            actionable_items.append("Schedule security training for development team")

        return actionable_items

    def _create_summary(self, issues: list[SecurityIssue], high: int, medium: int, low: int) -> str:
        """Create a summary of the security scan results"""
        if not issues:
            return "No security issues detected in the specified time period."

        summary_parts = [
            f"Security scan completed with {len(issues)} total issues:",
            f"- High severity: {high}",
            f"- Medium severity: {medium}",
            f"- Low severity: {low}",
        ]

        if high > 0:
            summary_parts.append("⚠️  CRITICAL: High severity issues require immediate attention!")

        if medium > 0:
            summary_parts.append("⚠️  Medium severity issues should be addressed promptly.")

        return "\n".join(summary_parts)


class SecurityScanManager:
    """Manages security scanning operations and integration"""

    def __init__(self, api_token: str):
        self.scanner = GitGuardianSecurityScanner(api_token)
        self.results_file = Path("security_scan_results.json")

    def run_security_scan(self, days_back: int = 30) -> SecurityScanResult:
        """Run a comprehensive security scan"""
        logger.info("Starting security scan...")

        # Get incidents from GitGuardian
        incidents = self.scanner.get_security_incidents(days_back)
        logger.info(f"Retrieved {len(incidents)} security incidents")

        # Analyze issues
        scan_result = self.scanner.analyze_security_issues(incidents)
        logger.info(f"Analysis complete: {scan_result.total_issues} issues found")

        # Save results
        self._save_results(scan_result)

        return scan_result

    def _save_results(self, scan_result: SecurityScanResult):
        """Save scan results to file for integration with quality system"""
        try:
            # Convert dataclass to dict for JSON serialization
            results_dict = {
                "timestamp": scan_result.timestamp,
                "total_issues": scan_result.total_issues,
                "high_severity": scan_result.high_severity,
                "medium_severity": scan_result.medium_severity,
                "low_severity": scan_result.low_severity,
                "summary": scan_result.summary,
                "actionable_items": scan_result.actionable_items,
                "issues": [
                    {
                        "id": issue.id,
                        "detector_name": issue.detector_name,
                        "severity": issue.severity,
                        "status": issue.status,
                        "filepath": issue.filepath,
                        "line_number": issue.line_number,
                        "description": issue.description,
                        "remediation": issue.remediation,
                        "priority": issue.priority,
                    }
                    for issue in scan_result.issues
                ],
            }

            with open(self.results_file, "w") as f:
                json.dump(results_dict, f, indent=2)

            logger.info(f"Results saved to {self.results_file}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    def get_latest_results(self) -> Optional[SecurityScanResult]:
        """Get the latest scan results from file"""
        if not self.results_file.exists():
            return None

        try:
            with open(self.results_file) as f:
                data = json.load(f)

            # Reconstruct SecurityScanResult object
            issues = [
                SecurityIssue(
                    id=issue["id"],
                    detector_name=issue["detector_name"],
                    detector_display_name=issue["detector_name"],
                    severity=issue["severity"],
                    status=issue["status"],
                    date="",
                    filepath=issue["filepath"],
                    line_number=issue["line_number"],
                    secret_type="",
                    description=issue["description"],
                    remediation=issue["remediation"],
                    priority=issue["priority"],
                )
                for issue in data["issues"]
            ]

            return SecurityScanResult(
                timestamp=data["timestamp"],
                total_issues=data["total_issues"],
                high_severity=data["high_severity"],
                medium_severity=data["medium_severity"],
                low_severity=data["low_severity"],
                issues=issues,
                summary=data["summary"],
                actionable_items=data["actionable_items"],
            )
        except Exception as e:
            logger.error(f"Failed to load results: {e}")
            return None


def main():
    """Main function for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Security Scanner for OpenFlow-Playground")
    parser.add_argument("--api-token", help="GitGuardian API token (or use 1Password)")
    parser.add_argument("--days-back", type=int, default=30, help="Number of days to look back")
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

    # Initialize scanner
    manager = SecurityScanManager(api_token)

    # Run scan
    result = manager.run_security_scan(args.days_back)

    # Print results
    print("\n" + "=" * 60)
    print("SECURITY SCAN RESULTS")
    print("=" * 60)
    print(result.summary)
    print("\nActionable Items:")
    for item in result.actionable_items:
        print(f"• {item}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(
                {
                    "timestamp": result.timestamp,
                    "total_issues": result.total_issues,
                    "high_severity": result.high_severity,
                    "medium_severity": result.medium_severity,
                    "low_severity": result.low_severity,
                    "summary": result.summary,
                    "actionable_items": result.actionable_items,
                },
                f,
                indent=2,
            )
        print(f"\nDetailed results saved to: {args.output}")


if __name__ == "__main__":
    main()
