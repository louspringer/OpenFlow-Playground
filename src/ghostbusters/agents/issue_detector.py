#!/usr/bin/env python3
"""
Issue Detector Agent

This agent specializes in detecting code quality issues and potential problems.
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class IssueDetector:
    """Agent for detecting code quality issues"""

    def __init__(self, config: dict[str, Any] = None):
        """Initialize the issue detector agent"""
        self.config = config or {}
        self.detection_patterns = {
            "todo": r"TODO|FIXME|HACK|XXX|BUG",
            "hardcoded": r"password|secret|key|token|api_key",
            "complexity": r"if.*if|for.*for|while.*while",
            "security": r"eval\(|exec\(|subprocess\.",
            "performance": r"\.append\(.*\)|\.extend\(.*\)",
        }

        logger.info("🔍 Issue Detector Agent initialized")

    def detect_issues(self, target_path: str) -> dict[str, Any]:
        """Detect issues in the target path"""
        logger.info(f"🔍 Detecting issues for: {target_path}")

        detection_results = {
            "target_path": target_path,
            "issues_detected": [],
            "severity_summary": {},
            "recommendations": [],
        }

        try:
            path = Path(target_path)
            if path.is_file():
                issues = self._detect_file_issues(path)
            elif path.is_dir():
                issues = self._detect_directory_issues(path)
            else:
                issues = []

            detection_results["issues_detected"] = issues

            # Generate severity summary
            detection_results["severity_summary"] = self._generate_severity_summary(issues)

            # Generate recommendations
            detection_results["recommendations"] = self._generate_issue_recommendations(issues)

            logger.info(f"✅ Issue detection complete. Found {len(issues)} issues")

        except Exception as e:
            logger.error(f"❌ Issue detection failed: {e}")
            detection_results["error"] = str(e)

        return detection_results

    def _detect_file_issues(self, file_path: Path) -> list[dict[str, Any]]:
        """Detect issues in a single file"""
        issues = []

        try:
            if file_path.suffix != ".py":
                return issues

            content = file_path.read_text()
            lines = content.splitlines()

            for line_num, line in enumerate(lines, 1):
                line_issues = self._analyze_line(line, line_num)
                issues.extend(line_issues)

        except Exception as e:
            logger.error(f"❌ Failed to analyze file {file_path}: {e}")
            issues.append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "line": 0,
                    "description": f"Failed to analyze file: {e}",
                    "file": str(file_path),
                }
            )

        return issues

    def _detect_directory_issues(self, dir_path: Path) -> list[dict[str, Any]]:
        """Detect issues in a directory"""
        all_issues = []

        try:
            python_files = list(dir_path.rglob("*.py"))

            for file_path in python_files:
                file_issues = self._detect_file_issues(file_path)
                all_issues.extend(file_issues)

        except Exception as e:
            logger.error(f"❌ Failed to analyze directory {dir_path}: {e}")
            all_issues.append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "line": 0,
                    "description": f"Failed to analyze directory: {e}",
                    "file": str(dir_path),
                }
            )

        return all_issues

    def _analyze_line(self, line: str, line_num: int) -> list[dict[str, Any]]:
        """Analyze a single line for issues"""
        issues = []
        stripped_line = line.strip()

        # Skip empty lines and comments
        if not stripped_line or stripped_line.startswith("#"):
            return issues

        # Check for TODO/FIXME patterns
        if re.search(self.detection_patterns["todo"], stripped_line, re.IGNORECASE):
            issues.append(
                {
                    "type": "todo_comment",
                    "severity": "low",
                    "line": line_num,
                    "description": "TODO/FIXME comment found",
                    "code": stripped_line,
                }
            )

        # Check for hardcoded credentials
        if re.search(self.detection_patterns["hardcoded"], stripped_line, re.IGNORECASE):
            if "=" in stripped_line and not any(var in stripped_line for var in ["os.getenv", "config.get"]):
                issues.append(
                    {
                        "type": "hardcoded_credential",
                        "severity": "high",
                        "line": line_num,
                        "description": "Potential hardcoded credential detected",
                        "code": stripped_line,
                    }
                )

        # Check for security issues
        if re.search(self.detection_patterns["security"], stripped_line):
            issues.append(
                {
                    "type": "security_risk",
                    "severity": "high",
                    "line": line_num,
                    "description": "Potential security risk detected",
                    "code": stripped_line,
                }
            )

        # Check for complexity issues
        if re.search(self.detection_patterns["complexity"], stripped_line):
            issues.append(
                {
                    "type": "complexity",
                    "severity": "medium",
                    "line": line_num,
                    "description": "High complexity detected",
                    "code": stripped_line,
                }
            )

        return issues

    def _generate_severity_summary(self, issues: list[dict[str, Any]]) -> dict[str, int]:
        """Generate summary of issues by severity"""
        summary = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for issue in issues:
            severity = issue.get("severity", "low")
            if severity in summary:
                summary[severity] += 1

        return summary

    def _generate_issue_recommendations(self, issues: list[dict[str, Any]]) -> list[str]:
        """Generate recommendations based on detected issues"""
        recommendations = []

        if not issues:
            recommendations.append("🎉 No issues detected! Code quality is excellent!")
            return recommendations

        # Count issue types
        issue_types = {}
        for issue in issues:
            issue_type = issue.get("type", "unknown")
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1

        # Generate specific recommendations
        if issue_types.get("todo_comment", 0) > 0:
            recommendations.append("📝 Address TODO/FIXME comments to improve code clarity")

        if issue_types.get("hardcoded_credential", 0) > 0:
            recommendations.append("🔒 Remove hardcoded credentials and use environment variables")

        if issue_types.get("security_risk", 0) > 0:
            recommendations.append("🛡️ Review security practices and implement safer alternatives")

        if issue_types.get("complexity", 0) > 0:
            recommendations.append("🔧 Simplify complex code structures for better maintainability")

        # General recommendations
        total_issues = len(issues)
        if total_issues > 20:
            recommendations.append("⚠️ High number of issues detected - consider comprehensive code review")

        recommendations.append("🧪 Run automated tests to validate fixes")
        recommendations.append("📚 Update documentation for any API changes")

        return recommendations
