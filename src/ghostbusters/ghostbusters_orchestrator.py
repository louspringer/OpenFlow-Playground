#!/usr/bin/env python3
"""
Ghostbusters Orchestrator

This module provides the main GhostbustersOrchestrator class for paranormal investigation
of code quality issues and multi-agent testing coordination.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GhostbustersOrchestrator:
    """
    Ghostbusters Orchestrator for paranormal investigation of code quality issues.

    This orchestrator coordinates multiple agents to investigate and resolve
    code quality problems through systematic analysis and testing.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize the Ghostbusters Orchestrator"""
        self.config = config or {}
        self.agents = {}
        self.investigation_results = {}
        self.quality_metrics = {}

        logger.info("🧙‍♂️ Ghostbusters Orchestrator initialized")

    def add_agent(self, agent_name: str, agent_config: dict[str, Any]) -> bool:
        """Add an investigation agent to the orchestrator"""
        try:
            self.agents[agent_name] = agent_config
            logger.info(f"✅ Added agent: {agent_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to add agent {agent_name}: {e}")
            return False

    def investigate_quality_issues(self, target_path: str) -> dict[str, Any]:
        """Investigate quality issues in the target path"""
        logger.info(f"🔍 Investigating quality issues in: {target_path}")

        investigation_results = {
            "target_path": target_path,
            "timestamp": self._get_timestamp(),
            "agents_used": list(self.agents.keys()),
            "issues_found": [],
            "recommendations": [],
            "quality_score": 0.0,
        }

        try:
            # Run quality analysis
            quality_analysis = self._run_quality_analysis(target_path)
            investigation_results["issues_found"] = quality_analysis.get("issues", [])

            # Generate recommendations
            recommendations = self._generate_recommendations(quality_analysis)
            investigation_results["recommendations"] = recommendations

            # Calculate quality score
            quality_score = self._calculate_quality_score(quality_analysis)
            investigation_results["quality_score"] = quality_score

            logger.info(f"✅ Investigation complete. Quality score: {quality_score:.2f}")

        except Exception as e:
            logger.error(f"❌ Investigation failed: {e}")
            investigation_results["error"] = str(e)

        self.investigation_results[target_path] = investigation_results
        return investigation_results

    def _run_quality_analysis(self, target_path: str) -> dict[str, Any]:
        """Run comprehensive quality analysis"""
        analysis = {
            "path": target_path,
            "files_analyzed": 0,
            "issues": [],
            "metrics": {},
        }

        try:
            path = Path(target_path)
            if path.is_file():
                analysis["files_analyzed"] = 1
                analysis["issues"] = self._analyze_single_file(path)
            elif path.is_dir():
                analysis["files_analyzed"] = len(list(path.rglob("*.py")))
                analysis["issues"] = self._analyze_directory(path)

            logger.info(f"📊 Analyzed {analysis['files_analyzed']} files")

        except Exception as e:
            logger.error(f"❌ Quality analysis failed: {e}")
            analysis["error"] = str(e)

        return analysis

    def _analyze_single_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Analyze a single Python file for quality issues"""
        issues = []

        try:
            # Basic file analysis
            if file_path.suffix == ".py":
                content = file_path.read_text()

                # Check for common issues
                if "TODO" in content:
                    issues.append(
                        {
                            "type": "todo_found",
                            "severity": "low",
                            "description": "TODO comment found in code",
                            "line": content.count("\n") + 1,
                        }
                    )

                if "FIXME" in content:
                    issues.append(
                        {
                            "type": "fixme_found",
                            "severity": "medium",
                            "description": "FIXME comment found in code",
                            "line": content.count("\n") + 1,
                        }
                    )

                if "HACK" in content:
                    issues.append(
                        {
                            "type": "hack_found",
                            "severity": "high",
                            "description": "HACK comment found in code",
                            "line": content.count("\n") + 1,
                        }
                    )

                logger.info(f"🔍 Analyzed file: {file_path.name}")

        except Exception as e:
            logger.error(f"❌ File analysis failed for {file_path}: {e}")
            issues.append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "description": f"Failed to analyze file: {e}",
                    "line": 0,
                }
            )

        return issues

    def _analyze_directory(self, dir_path: Path) -> list[dict[str, Any]]:
        """Analyze a directory for quality issues"""
        all_issues = []

        try:
            python_files = list(dir_path.rglob("*.py"))

            for file_path in python_files:
                file_issues = self._analyze_single_file(file_path)
                all_issues.extend(file_issues)

            logger.info(f"📁 Analyzed directory: {dir_path.name}")

        except Exception as e:
            logger.error(f"❌ Directory analysis failed for {dir_path}: {e}")
            all_issues.append(
                {
                    "type": "analysis_error",
                    "severity": "critical",
                    "description": f"Failed to analyze directory: {e}",
                    "line": 0,
                }
            )

        return all_issues

    def _generate_recommendations(self, analysis: dict[str, Any]) -> list[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []

        issues = analysis.get("issues", [])

        if not issues:
            recommendations.append(
                "🎉 No quality issues found! Code is paranormally clean!"
            )
            return recommendations

        # Analyze issue patterns
        todo_count = len([i for i in issues if i.get("type") == "todo_found"])
        fixme_count = len([i for i in issues if i.get("type") == "fixme_found"])
        hack_count = len([i for i in issues if i.get("type") == "hack_found"])

        if todo_count > 0:
            recommendations.append(
                f"📝 Address {todo_count} TODO comments to improve code clarity"
            )

        if fixme_count > 0:
            recommendations.append(
                f"🔧 Fix {fixme_count} FIXME issues to resolve known problems"
            )

        if hack_count > 0:
            recommendations.append(
                f"🚨 Remove {hack_count} HACK comments - these indicate technical debt"
            )

        # General recommendations
        if len(issues) > 10:
            recommendations.append(
                "⚠️ High number of issues detected - consider code review session"
            )

        recommendations.append("🧪 Run comprehensive test suite to validate fixes")
        recommendations.append("📚 Update documentation for any API changes")

        return recommendations

    def _calculate_quality_score(self, analysis: dict[str, Any]) -> float:
        """Calculate overall quality score based on analysis"""
        issues = analysis.get("issues", [])

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
        max_penalty = 50  # Maximum penalty to prevent negative scores
        penalty = min(total_weight * 2, max_penalty)
        score = max(100.0 - penalty, 0.0)

        return round(score, 2)

    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime

        return datetime.now().isoformat()

    def get_investigation_summary(self) -> dict[str, Any]:
        """Get summary of all investigations"""
        return {
            "total_investigations": len(self.investigation_results),
            "recent_investigations": list(self.investigation_results.keys()),
            "overall_quality_trend": self._calculate_overall_trend(),
            "agent_status": dict.fromkeys(self.agents.keys(), "active"),
        }

    def _calculate_overall_trend(self) -> str:
        """Calculate overall quality trend"""
        if not self.investigation_results:
            return "no_data"

        scores = [
            result.get("quality_score", 0)
            for result in self.investigation_results.values()
        ]
        avg_score = sum(scores) / len(scores)

        if avg_score >= 90:
            return "excellent"
        if avg_score >= 75:
            return "good"
        if avg_score >= 50:
            return "fair"
        return "poor"


def run_ghostbusters(target_path: str = ".") -> dict[str, Any]:
    """
    Run Ghostbusters investigation on the specified target path.

    Args:
        target_path: Path to investigate (file or directory)

    Returns:
        Investigation results dictionary
    """
    # Initialize orchestrator with default configuration
    config = {
        "investigation_mode": "comprehensive",
        "quality_threshold": 80.0,
        "max_issues_per_file": 50,
    }

    orchestrator = GhostbustersOrchestrator(config)

    # Add default agents
    orchestrator.add_agent("quality_analyzer", {"type": "analysis", "enabled": True})
    orchestrator.add_agent("issue_detector", {"type": "detection", "enabled": True})
    orchestrator.add_agent(
        "recommendation_engine", {"type": "recommendation", "enabled": True}
    )

    # Run investigation
    return orchestrator.investigate_quality_issues(target_path)


if __name__ == "__main__":
    # Example usage
    results = run_ghostbusters(".")
    print("🧙‍♂️ Ghostbusters Investigation Results:")
    print(json.dumps(results, indent=2))
