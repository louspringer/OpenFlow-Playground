"""
Multi-Agent Integration for Quality System

This module provides integration between the quality system and the multi-agent testing framework,
enabling expert agents to contribute to quality analysis and enforcement.
"""

import logging
from pathlib import Path
from typing import Any, Optional

from .quality_enforcer import QualityEnforcer
from .quality_metrics import QualityScore


class QualityMultiAgentAdapter:
    """
    Adapter class that bridges the quality system with the multi-agent testing framework.

    This adapter:
    1. Coordinates quality analysis across multiple expert agents
    2. Converts expert agent outputs to quality metrics
    3. Aggregates results for comprehensive quality assessment
    4. Integrates with the quality enforcement system
    """

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quality_enforcer = QualityEnforcer(project_path)
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.agent_quality_mapping = {
            "security_expert": {
                "metric_name": "security",
                "weight": 3.0,
                "description": "Security analysis from SecurityExpert",
            },
            "code_quality_expert": {
                "metric_name": "code_quality",
                "weight": 2.0,
                "description": "Code quality analysis from CodeQualityExpert",
            },
            "devops_expert": {
                "metric_name": "operational_quality",
                "weight": 1.5,
                "description": "Operational quality from DevOpsExpert",
            },
            "test_expert": {
                "metric_name": "test_coverage",
                "weight": 1.5,
                "description": "Test coverage analysis from TestExpert",
            },
            "architecture_expert": {
                "metric_name": "architecture_quality",
                "weight": 1.0,
                "description": "Architecture quality from ArchitectureExpert",
            },
        }

    async def run_multi_agent_quality_analysis(self, agent_results: dict[str, Any]) -> dict[str, Any]:
        """
        Run quality analysis using results from multiple expert agents.

        Args:
            agent_results: Dictionary of results from expert agents

        Returns:
            Comprehensive quality analysis results
        """
        self.logger.info("Starting multi-agent quality analysis")

        try:
            # Step 1: Convert agent results to quality metrics
            quality_metrics = await self._convert_agent_results_to_metrics(agent_results)

            # Step 2: Aggregate quality metrics
            aggregated_metrics = self._aggregate_quality_metrics(quality_metrics)

            # Step 3: Run quality enforcement
            enforcement_results = self.quality_enforcer.enforce_quality(aggregated_metrics)

            # Step 4: Generate comprehensive report
            comprehensive_report = self._generate_comprehensive_report(agent_results, quality_metrics, aggregated_metrics, enforcement_results)

            self.logger.info("Multi-agent quality analysis completed successfully")
            return comprehensive_report

        except Exception as e:
            self.logger.error(f"Multi-agent quality analysis failed: {e}")
            return {"status": "error", "error": str(e), "can_proceed": False}

    async def _convert_agent_results_to_metrics(self, agent_results: dict[str, Any]) -> dict[str, QualityScore]:
        """
        Convert expert agent results to quality metrics.

        Args:
            agent_results: Raw results from expert agents

        Returns:
            Dictionary of quality scores by metric name
        """
        quality_scores = {}

        for agent_name, agent_result in agent_results.items():
            if agent_name in self.agent_quality_mapping:
                mapping = self.agent_quality_mapping[agent_name]
                metric_name = mapping["metric_name"]
                weight = mapping["weight"]

                # Convert agent result to quality score
                quality_score = self._convert_agent_result_to_score(agent_name, agent_result, metric_name, weight)

                if quality_score:
                    quality_scores[metric_name] = quality_score
                    self.logger.info(f"Converted {agent_name} result to {metric_name} score: {quality_score.score:.1f}")

        return quality_scores

    def _convert_agent_result_to_score(self, agent_name: str, agent_result: Any, metric_name: str, weight: float) -> Optional[QualityScore]:
        """
        Convert a single agent result to a quality score.

        Args:
            agent_name: Name of the expert agent
            agent_result: Result from the agent
            metric_name: Name of the quality metric
            weight: Weight for the quality score

        Returns:
            QualityScore object or None if conversion fails
        """
        try:
            if agent_name == "security_expert":
                return self._convert_security_result(agent_result, weight)
            if agent_name == "code_quality_expert":
                return self._convert_code_quality_result(agent_result, weight)
            if agent_name == "devops_expert":
                return self._convert_devops_result(agent_result, weight)
            if agent_name == "test_expert":
                return self._convert_test_result(agent_result, weight)
            if agent_name == "architecture_expert":
                return self._convert_architecture_result(agent_result, weight)

            self.logger.warning(f"Unknown agent type: {agent_name}")
            return None

        except Exception as e:
            self.logger.error(f"Failed to convert {agent_name} result: {e}")
            return None

    def _convert_security_result(self, result: Any, weight: float) -> QualityScore:
        """Convert SecurityExpert result to security quality score."""
        # Default security score
        score = 100.0
        details = {}

        if isinstance(result, dict):
            # Extract security issues from result
            security_issues = result.get("security_issues", [])
            critical_issues = result.get("critical_issues", [])
            high_issues = result.get("high_issues", [])

            # Calculate score based on issues
            if critical_issues:
                score -= len(critical_issues) * 25  # Critical issues are very expensive
            if high_issues:
                score -= len(high_issues) * 15  # High priority issues are costly
            if security_issues:
                score -= len(security_issues) * 5  # Each security issue has significant cost

            details = {
                "security_issues": security_issues,
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "total_issues": len(security_issues) + len(critical_issues) + len(high_issues),
            }

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(metric_name="security", score=score, weight=weight, details=details)

    def _convert_code_quality_result(self, result: Any, weight: float) -> QualityScore:
        """Convert CodeQualityExpert result to code quality score."""
        # Default code quality score
        score = 100.0
        details = {}

        if isinstance(result, dict):
            # Extract code quality issues from result
            flake8_issues = result.get("flake8_issues", [])
            code_style_issues = result.get("code_style_issues", [])
            complexity_issues = result.get("complexity_issues", [])

            # Calculate score based on issues
            if flake8_issues:
                score -= len(flake8_issues) * 2  # Flake8 issues are moderate cost
            if code_style_issues:
                score -= len(code_style_issues) * 1  # Style issues are low cost
            if complexity_issues:
                score -= len(complexity_issues) * 3  # Complexity issues are high cost

            details = {
                "flake8_issues": flake8_issues,
                "code_style_issues": code_style_issues,
                "complexity_issues": complexity_issues,
                "total_issues": len(flake8_issues) + len(code_style_issues) + len(complexity_issues),
            }

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(metric_name="code_quality", score=score, weight=weight, details=details)

    def _convert_devops_result(self, result: Any, weight: float) -> QualityScore:
        """Convert DevOpsExpert result to operational quality score."""
        # Default operational quality score
        score = 100.0
        details = {}

        if isinstance(result, dict):
            # Extract operational issues from result
            ci_cd_issues = result.get("ci_cd_issues", [])
            deployment_issues = result.get("deployment_issues", [])
            infrastructure_issues = result.get("infrastructure_issues", [])

            # Calculate score based on issues
            if ci_cd_issues:
                score -= len(ci_cd_issues) * 3  # CI/CD issues are moderate cost
            if deployment_issues:
                score -= len(deployment_issues) * 4  # Deployment issues are high cost
            if infrastructure_issues:
                score -= len(infrastructure_issues) * 2  # Infrastructure issues are moderate cost

            details = {
                "ci_cd_issues": ci_cd_issues,
                "deployment_issues": deployment_issues,
                "infrastructure_issues": infrastructure_issues,
                "total_issues": len(ci_cd_issues) + len(deployment_issues) + len(infrastructure_issues),
            }

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(
            metric_name="operational_quality",
            score=score,
            weight=weight,
            details=details,
        )

    def _convert_test_result(self, result: Any, weight: float) -> QualityScore:
        """Convert TestExpert result to test coverage score."""
        # Default test coverage score
        score = 100.0
        details = {}

        if isinstance(result, dict):
            # Extract test metrics from result
            coverage_percentage = result.get("coverage_percentage", 100.0)
            test_count = result.get("test_count", 0)
            test_failures = result.get("test_failures", 0)

            # Use coverage percentage as base score
            score = min(100.0, coverage_percentage)

            # Penalize for test failures
            if test_failures > 0:
                score -= test_failures * 5

            details = {
                "coverage_percentage": coverage_percentage,
                "test_count": test_count,
                "test_failures": test_failures,
            }

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(metric_name="test_coverage", score=score, weight=weight, details=details)

    def _convert_architecture_result(self, result: Any, weight: float) -> QualityScore:
        """Convert ArchitectureExpert result to architecture quality score."""
        # Default architecture quality score
        score = 100.0
        details = {}

        if isinstance(result, dict):
            # Extract architecture issues from result
            design_issues = result.get("design_issues", [])
            pattern_violations = result.get("pattern_violations", [])
            coupling_issues = result.get("coupling_issues", [])

            # Calculate score based on issues
            if design_issues:
                score -= len(design_issues) * 4  # Design issues are high cost
            if pattern_violations:
                score -= len(pattern_violations) * 2  # Pattern violations are moderate cost
            if coupling_issues:
                score -= len(coupling_issues) * 3  # Coupling issues are high cost

            details = {
                "design_issues": design_issues,
                "pattern_violations": pattern_violations,
                "coupling_issues": coupling_issues,
                "total_issues": len(design_issues) + len(pattern_violations) + len(coupling_issues),
            }

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(
            metric_name="architecture_quality",
            score=score,
            weight=weight,
            details=details,
        )

    def _aggregate_quality_metrics(self, quality_scores: dict[str, QualityScore]) -> dict[str, Any]:
        """
        Aggregate quality metrics into analysis results format.

        Args:
            quality_scores: Dictionary of quality scores by metric

        Returns:
            Aggregated analysis results for quality enforcement
        """
        aggregated_results = {
            "flake8_issues": [],
            "security_issues": [],
            "coverage_percentage": 0.0,
            "performance_metrics": {},
            "quality_scores": quality_scores,
        }

        # Extract specific metrics for quality enforcement
        if "security" in quality_scores:
            security_score = quality_scores["security"]
            if security_score.details.get("security_issues"):
                aggregated_results["security_issues"] = security_score.details["security_issues"]

        if "code_quality" in quality_scores:
            code_quality_score = quality_scores["code_quality"]
            if code_quality_score.details.get("flake8_issues"):
                aggregated_results["flake8_issues"] = code_quality_score.details["flake8_issues"]

        if "test_coverage" in quality_scores:
            test_coverage_score = quality_scores["test_coverage"]
            aggregated_results["coverage_percentage"] = test_coverage_score.score

        # Add performance metrics if available
        if "operational_quality" in quality_scores:
            operational_score = quality_scores["operational_quality"]
            aggregated_results["performance_metrics"] = operational_score.details

        return aggregated_results

    def _generate_comprehensive_report(
        self,
        agent_results: dict[str, Any],
        quality_scores: dict[str, QualityScore],
        aggregated_metrics: dict[str, Any],
        enforcement_results: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate comprehensive quality analysis report.

        Args:
            agent_results: Raw results from expert agents
            quality_scores: Converted quality scores
            aggregated_metrics: Aggregated metrics for enforcement
            enforcement_results: Results from quality enforcement

        Returns:
            Comprehensive quality analysis report
        """
        # Calculate overall quality score
        overall_score = 0.0
        total_weight = 0.0

        for score in quality_scores.values():
            overall_score += score.score * score.weight
            total_weight += score.weight

        if total_weight > 0:
            overall_score = overall_score / total_weight

        # Generate agent summary
        agent_summary = {}
        for agent_name, result in agent_results.items():
            if agent_name in self.agent_quality_mapping:
                mapping = self.agent_quality_mapping[agent_name]
                metric_name = mapping["metric_name"]

                if metric_name in quality_scores:
                    agent_summary[agent_name] = {
                        "metric": metric_name,
                        "score": quality_scores[metric_name].score,
                        "weight": quality_scores[metric_name].weight,
                        "status": "analyzed",
                    }
                else:
                    agent_summary[agent_name] = {"status": "failed_analysis"}
            else:
                agent_summary[agent_name] = {"status": "unknown_agent"}

        return {
            "status": "success",
            "timestamp": enforcement_results.get("timestamp", ""),
            "project_path": str(self.project_path),
            # Quality metrics
            "overall_quality_score": overall_score,
            "quality_scores": {
                name: {
                    "score": score.score,
                    "weight": score.weight,
                    "details": score.details,
                }
                for name, score in quality_scores.items()
            },
            # Agent analysis summary
            "agent_summary": agent_summary,
            "agents_analyzed": len([a for a in agent_summary.values() if a["status"] == "analyzed"]),
            "agents_failed": len([a for a in agent_summary.values() if a["status"] == "failed_analysis"]),
            # Quality enforcement results
            "enforcement_results": enforcement_results,
            "can_proceed": enforcement_results.get("can_proceed", False),
            "blocking_gates": enforcement_results.get("blocking_gates", 0),
            # Recommendations
            "recommendations": enforcement_results.get("recommendations", []),
            # Analysis metadata
            "analysis_type": "multi_agent_quality_analysis",
            "total_agents": len(agent_results),
            "successful_conversions": len(quality_scores),
        }

    def get_agent_quality_mapping(self) -> dict[str, dict[str, Any]]:
        """Get the current agent quality mapping configuration."""
        return self.agent_quality_mapping.copy()

    def update_agent_quality_mapping(self, agent_name: str, mapping: dict[str, Any]) -> bool:
        """
        Update the quality mapping for a specific agent.

        Args:
            agent_name: Name of the agent to update
            mapping: New mapping configuration

        Returns:
            True if update was successful, False otherwise
        """
        try:
            required_keys = ["metric_name", "weight", "description"]
            if not all(key in mapping for key in required_keys):
                self.logger.error(f"Invalid mapping for {agent_name}: missing required keys")
                return False

            self.agent_quality_mapping[agent_name] = mapping.copy()
            self.logger.info(f"Updated quality mapping for {agent_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update mapping for {agent_name}: {e}")
            return False

    def add_agent_quality_mapping(self, agent_name: str, mapping: dict[str, Any]) -> bool:
        """
        Add a new agent quality mapping.

        Args:
            agent_name: Name of the new agent
            mapping: Mapping configuration

        Returns:
            True if addition was successful, False otherwise
        """
        if agent_name in self.agent_quality_mapping:
            self.logger.warning(f"Agent {agent_name} already exists in mapping")
            return False

        return self.update_agent_quality_mapping(agent_name, mapping)

    def remove_agent_quality_mapping(self, agent_name: str) -> bool:
        """
        Remove an agent quality mapping.

        Args:
            agent_name: Name of the agent to remove

        Returns:
            True if removal was successful, False otherwise
        """
        if agent_name not in self.agent_quality_mapping:
            self.logger.warning(f"Agent {agent_name} not found in mapping")
            return False

        removed_mapping = self.agent_quality_mapping.pop(agent_name)
        self.logger.info(f"Removed quality mapping for {agent_name}: {removed_mapping}")
        return True
