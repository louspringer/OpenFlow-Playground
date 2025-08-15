#!/usr/bin/env python3
"""
Quality Enforcer

Coordinates quality metrics calculation, gate evaluation, and enforcement actions.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from .quality_gates import GateResult, QualityGateManager
from .quality_metrics import QualityMetrics, QualityMetricsCalculator


class QualityEnforcer:
    """Main quality enforcement engine"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.metrics_calculator = QualityMetricsCalculator(project_path)
        self.gate_manager = QualityGateManager(project_path)

        # Configuration
        self.enforcement_level = "strict"  # strict, moderate, lenient
        self.auto_fix_enabled = False
        self.block_on_failure = True

    def enforce_quality(self, analysis_results: dict[str, Any]) -> dict[str, Any]:
        """Main quality enforcement method"""
        self.logger.info("Starting quality enforcement")

        try:
            # Step 1: Calculate quality metrics
            metrics = self.metrics_calculator.calculate_all_metrics(analysis_results)
            self.logger.info(
                f"Calculated overall quality score: {metrics.overall_score:.1f}"
            )

            # Step 2: Evaluate quality gates
            gate_results = self.gate_manager.evaluate_gates(metrics)
            self.logger.info(f"Evaluated {len(gate_results)} quality gates")

            # Step 3: Get enforcement summary
            gate_summary = self.gate_manager.get_gate_summary(gate_results)
            blocking_gates = self.gate_manager.get_blocking_gates(gate_results)

            # Step 4: Determine if operation can proceed
            can_proceed = len(blocking_gates) == 0

            # Step 5: Generate enforcement report
            enforcement_report = self._generate_enforcement_report(
                metrics, gate_results, gate_summary, can_proceed
            )

            # Step 6: Take enforcement actions if needed
            if not can_proceed and self.block_on_failure:
                self._take_enforcement_actions(blocking_gates, enforcement_report)

            # Step 7: Save metrics for tracking
            self._save_metrics(metrics)

            return enforcement_report

        except Exception as e:
            self.logger.error(f"Quality enforcement failed: {e}")
            return {"status": "error", "error": str(e), "can_proceed": False}

    def _generate_enforcement_report(
        self,
        metrics: QualityMetrics,
        gate_results: list[GateResult],
        gate_summary: dict[str, Any],
        can_proceed: bool,
    ) -> dict[str, Any]:
        """Generate comprehensive enforcement report"""

        # Group gate results by status (for potential future use)
        # passed_gates = [r for r in gate_results if r.status.value == "passed"]
        # failed_gates = [r for r in gate_results if r.status.value == "failed"]
        # warning_gates = [r for r in gate_results if r.status.value == "warning"]

        # Get detailed score breakdown
        score_breakdown = {}
        for score in metrics.scores:
            score_breakdown[score.metric_name] = {
                "score": score.score,
                "weight": score.weight,
                "details": score.details,
            }

        return {
            "status": "success",
            "timestamp": metrics.timestamp.isoformat(),
            "project_path": str(metrics.project_path),
            # Quality metrics
            "overall_score": metrics.overall_score,
            "score_breakdown": score_breakdown,
            # Gate evaluation results
            "gate_summary": gate_summary,
            "gate_results": [
                {
                    "name": result.gate_name,
                    "status": result.status.value,
                    "severity": result.severity.value,
                    "message": result.message,
                    "details": result.details,
                }
                for result in gate_results
            ],
            # Enforcement decision
            "can_proceed": can_proceed,
            "blocking_gates": len(self.gate_manager.get_blocking_gates(gate_results)),
            # Recommendations
            "recommendations": self._generate_recommendations(metrics, gate_results),
            # Configuration
            "enforcement_level": self.enforcement_level,
            "auto_fix_enabled": self.auto_fix_enabled,
        }

    def _generate_recommendations(
        self, metrics: QualityMetrics, gate_results: list[GateResult]
    ) -> list[str]:
        """Generate actionable recommendations based on results"""
        recommendations = []

        # Overall quality recommendations
        if metrics.overall_score < 70:
            recommendations.append(
                "Overall quality score is below 70. Focus on high-impact improvements first."
            )

        # Failed gates recommendations
        failed_gates = [r for r in gate_results if r.status.value == "failed"]
        for failed_gate in failed_gates:
            if failed_gate.gate_name == "security_critical":
                recommendations.append(
                    "CRITICAL: Address security vulnerabilities immediately before proceeding."
                )
            elif failed_gate.gate_name == "code_quality_minimum":
                recommendations.append(
                    "Fix code quality issues to meet minimum standards."
                )
            elif failed_gate.gate_name == "test_coverage":
                recommendations.append(
                    "Increase test coverage to meet quality standards."
                )

        # Performance recommendations
        performance_score = metrics.get_score("performance")
        if performance_score and performance_score.score < 60:
            recommendations.append(
                "Performance issues detected. Review and optimize slow operations."
            )

        # General recommendations
        if not recommendations:
            recommendations.append(
                "Quality standards met. Continue monitoring and incremental improvements."
            )

        return recommendations

    def _take_enforcement_actions(
        self, blocking_gates: list[GateResult], enforcement_report: dict[str, Any]
    ) -> None:
        """Take enforcement actions when gates fail"""
        self.logger.warning(
            f"Taking enforcement actions for {len(blocking_gates)} blocking gates"
        )

        # Log blocking issues
        for gate in blocking_gates:
            self.logger.error(f"BLOCKING: {gate.gate_name} - {gate.message}")

        # Save enforcement report for review
        enforcement_file = self.project_path / ".quality_enforcement_report.json"
        import json

        with open(enforcement_file, "w") as f:
            json.dump(enforcement_report, f, indent=2)

        # Raise exception to block operation
        msg = (
            f"Quality gates failed: {len(blocking_gates)} blocking issues found. "
            f"Check {enforcement_file} for details."
        )
        raise QualityEnforcementError(msg)

    def _save_metrics(self, metrics: QualityMetrics) -> None:
        """Save quality metrics for tracking and trending"""
        metrics_dir = self.project_path / ".quality_metrics"
        metrics_dir.mkdir(exist_ok=True)

        # Save current metrics
        current_file = metrics_dir / "current_metrics.json"
        metrics.save_to_file(current_file)

        # Save historical metrics with timestamp
        timestamp = metrics.timestamp.strftime("%Y%m%d_%H%M%S")
        historical_file = metrics_dir / f"metrics_{timestamp}.json"
        metrics.save_to_file(historical_file)

        self.logger.info(
            f"Saved quality metrics to {current_file} and {historical_file}"
        )

    def configure_enforcement(
        self,
        enforcement_level: str = None,
        auto_fix_enabled: bool = None,
        block_on_failure: bool = None,
    ) -> None:
        """Configure enforcement behavior"""
        if enforcement_level is not None:
            if enforcement_level not in ["strict", "moderate", "lenient"]:
                msg = f"Invalid enforcement level: {enforcement_level}"
                raise ValueError(msg)
            self.enforcement_level = enforcement_level
            self.logger.info(f"Set enforcement level to: {enforcement_level}")

        if auto_fix_enabled is not None:
            self.auto_fix_enabled = auto_fix_enabled
            self.logger.info(f"Auto-fix enabled: {auto_fix_enabled}")

        if block_on_failure is not None:
            self.block_on_failure = block_on_failure
            self.logger.info(f"Block on failure: {block_on_failure}")

    def get_quality_trends(self, days: int = 30) -> dict[str, Any]:
        """Get quality trends over time"""
        metrics_dir = self.project_path / ".quality_metrics"
        if not metrics_dir.exists():
            return {"error": "No metrics directory found"}

        # Load historical metrics
        historical_files = sorted(metrics_dir.glob("metrics_*.json"))
        if not historical_files:
            return {"error": "No historical metrics found"}

        # Load recent metrics
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        trends = {
            "overall_scores": [],
            "metric_scores": {},
            "gate_pass_rates": [],
            "period": f"Last {days} days",
        }

        for metrics_file in historical_files:
            try:
                metrics = QualityMetrics.load_from_file(metrics_file)
                if metrics.timestamp >= cutoff_date:
                    trends["overall_scores"].append(
                        {
                            "timestamp": metrics.timestamp.isoformat(),
                            "score": metrics.overall_score,
                        }
                    )

                    # Track individual metric trends
                    for score in metrics.scores:
                        if score.metric_name not in trends["metric_scores"]:
                            trends["metric_scores"][score.metric_name] = []

                        trends["metric_scores"][score.metric_name].append(
                            {
                                "timestamp": metrics.timestamp.isoformat(),
                                "score": score.score,
                            }
                        )
            except Exception as e:
                self.logger.warning(f"Could not load metrics from {metrics_file}: {e}")

        return trends

    def run_quick_quality_check(self) -> dict[str, Any]:
        """Run a quick quality check without full analysis"""
        self.logger.info("Running quick quality check")

        # Load current metrics if available
        current_metrics_file = (
            self.project_path / ".quality_metrics" / "current_metrics.json"
        )
        if current_metrics_file.exists():
            try:
                metrics = QualityMetrics.load_from_file(current_metrics_file)
                gate_results = self.gate_manager.evaluate_gates(metrics)
                gate_summary = self.gate_manager.get_gate_summary(gate_results)

                return {
                    "status": "success",
                    "overall_score": metrics.overall_score,
                    "gate_summary": gate_summary,
                    "can_proceed": gate_summary["can_proceed"],
                    "message": "Quick check completed using cached metrics",
                }
            except Exception as e:
                self.logger.warning(f"Could not load cached metrics: {e}")

        return {
            "status": "no_cached_metrics",
            "message": "No cached metrics available. Run full quality enforcement first.",
        }


class QualityEnforcementError(Exception):
    """Exception raised when quality enforcement blocks an operation"""
