#!/usr/bin/env python3
"""
Quality Gates System

Enforces quality thresholds and policies to ensure code meets quality standards.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class GateStatus(Enum):
    """Status of a quality gate"""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"


class GateSeverity(Enum):
    """Severity level of a quality gate"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GateResult:
    """Result of a quality gate evaluation"""

    gate_name: str
    status: GateStatus
    severity: GateSeverity
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: str(datetime.now()))

    @property
    def is_blocking(self) -> bool:
        """Whether this gate result should block the operation"""
        return self.status == GateStatus.FAILED and self.severity in [
            GateSeverity.HIGH,
            GateSeverity.CRITICAL,
        ]


@dataclass
class QualityGate:
    """Individual quality gate with configurable thresholds"""

    name: str
    description: str
    severity: GateSeverity
    threshold: float  # Minimum score required to pass
    metric_name: str  # Which metric this gate applies to
    enabled: bool = True
    custom_evaluator: Optional[Callable] = None

    def evaluate(self, score: float, **kwargs) -> GateResult:
        """Evaluate whether the gate passes based on the score"""
        if not self.enabled:
            return GateResult(
                gate_name=self.name,
                status=GateStatus.PASSED,
                severity=self.severity,
                message=f"Gate '{self.name}' is disabled",
            )

        if self.custom_evaluator:
            return self.custom_evaluator(score, **kwargs)

        # Default evaluation logic
        if score >= self.threshold:
            status = GateStatus.PASSED
            message = f"Gate '{self.name}' passed: {score:.1f} >= {self.threshold}"
        else:
            status = GateStatus.FAILED
            message = f"Gate '{self.name}' failed: {score:.1f} < {self.threshold}"

        return GateResult(
            gate_name=self.name,
            status=status,
            severity=self.severity,
            message=message,
            details={
                "score": score,
                "threshold": self.threshold,
                "metric_name": self.metric_name,
            },
        )


class QualityGateManager:
    """Manages multiple quality gates and their evaluation"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.gates: list[QualityGate] = []
        self.logger = logging.getLogger(__name__)

        # Initialize default gates
        self._setup_default_gates()

    def _setup_default_gates(self) -> None:
        """Set up default quality gates"""
        default_gates = [
            QualityGate(
                name="overall_quality",
                description="Overall quality score must be above threshold",
                severity=GateSeverity.HIGH,
                threshold=70.0,
                metric_name="overall",
            ),
            QualityGate(
                name="security_critical",
                description="No critical security issues allowed",
                severity=GateSeverity.CRITICAL,
                threshold=80.0,
                metric_name="security",
            ),
            QualityGate(
                name="code_quality_minimum",
                description="Code quality must meet minimum standards",
                severity=GateSeverity.MEDIUM,
                threshold=60.0,
                metric_name="code_quality",
            ),
            QualityGate(
                name="test_coverage",
                description="Test coverage must be above threshold",
                severity=GateSeverity.MEDIUM,
                threshold=70.0,
                metric_name="test_coverage",
            ),
            QualityGate(
                name="performance_baseline",
                description="Performance must meet baseline requirements",
                severity=GateSeverity.LOW,
                threshold=50.0,
                metric_name="performance",
            ),
        ]

        for gate in default_gates:
            self.add_gate(gate)

    def add_gate(self, gate: QualityGate) -> None:
        """Add a quality gate"""
        self.gates.append(gate)
        self.logger.info(f"Added quality gate: {gate.name}")

    def remove_gate(self, gate_name: str) -> bool:
        """Remove a quality gate by name"""
        for i, gate in enumerate(self.gates):
            if gate.name == gate_name:
                removed_gate = self.gates.pop(i)
                self.logger.info(f"Removed quality gate: {removed_gate.name}")
                return True
        return False

    def get_gate(self, gate_name: str) -> Optional[QualityGate]:
        """Get a quality gate by name"""
        for gate in self.gates:
            if gate.name == gate_name:
                return gate
        return None

    def update_gate(self, gate_name: str, **kwargs) -> bool:
        """Update a quality gate's properties"""
        gate = self.get_gate(gate_name)
        if gate:
            for key, value in kwargs.items():
                if hasattr(gate, key):
                    setattr(gate, key, value)
            self.logger.info(f"Updated quality gate: {gate_name}")
            return True
        return False

    def evaluate_gates(self, metrics: Any) -> list[GateResult]:
        """Evaluate all gates against the provided metrics"""
        results = []

        for gate in self.gates:
            if gate.metric_name == "overall":
                score = metrics.overall_score
            else:
                score_obj = metrics.get_score(gate.metric_name)
                score = score_obj.score if score_obj else 0.0

            result = gate.evaluate(score)
            results.append(result)

            # Log the result
            if result.status == GateStatus.FAILED:
                self.logger.warning(f"Gate '{gate.name}' failed: {result.message}")
            elif result.status == GateStatus.PASSED:
                self.logger.info(f"Gate '{gate.name}' passed: {result.message}")

        return results

    def get_blocking_gates(self, results: list[GateResult]) -> list[GateResult]:
        """Get gates that would block the operation"""
        return [result for result in results if result.is_blocking]

    def get_gate_summary(self, results: list[GateResult]) -> dict[str, Any]:
        """Get a summary of gate evaluation results"""
        total_gates = len(results)
        passed_gates = len([r for r in results if r.status == GateStatus.PASSED])
        failed_gates = len([r for r in results if r.status == GateStatus.FAILED])
        warning_gates = len([r for r in results if r.status == GateStatus.WARNING])
        error_gates = len([r for r in results if r.status == GateStatus.ERROR])

        blocking_gates = self.get_blocking_gates(results)

        return {
            "total_gates": total_gates,
            "passed_gates": passed_gates,
            "failed_gates": failed_gates,
            "warning_gates": warning_gates,
            "error_gates": error_gates,
            "blocking_gates": len(blocking_gates),
            "overall_status": "passed" if failed_gates == 0 else "failed",
            "can_proceed": len(blocking_gates) == 0,
        }

    def save_gates_config(self, file_path: Path) -> None:
        """Save gates configuration to a file"""
        config = {
            "gates": [
                {
                    "name": gate.name,
                    "description": gate.description,
                    "severity": gate.severity.value,
                    "threshold": gate.threshold,
                    "metric_name": gate.metric_name,
                    "enabled": gate.enabled,
                }
                for gate in self.gates
            ]
        }

        import json

        with open(file_path, "w") as f:
            json.dump(config, f, indent=2)

    def load_gates_config(self, file_path: Path) -> None:
        """Load gates configuration from a file"""
        import json

        with open(file_path) as f:
            config = json.load(f)

        # Clear existing gates
        self.gates.clear()

        # Load gates from config
        for gate_config in config.get("gates", []):
            gate = QualityGate(
                name=gate_config["name"],
                description=gate_config["description"],
                severity=GateSeverity(gate_config["severity"]),
                threshold=gate_config["threshold"],
                metric_name=gate_config["metric_name"],
                enabled=gate_config.get("enabled", True),
            )
            self.add_gate(gate)


# Custom gate evaluators
def no_critical_security_issues(score: float, **kwargs) -> GateResult:
    """Custom evaluator for security gate - no critical issues allowed"""
    security_issues = kwargs.get("security_issues", [])
    critical_issues = [i for i in security_issues if i.get("priority") == "critical"]

    if critical_issues:
        return GateResult(
            gate_name="security_critical",
            status=GateStatus.FAILED,
            severity=GateSeverity.CRITICAL,
            message=f"Critical security issues found: {len(critical_issues)}",
            details={"critical_issues": critical_issues},
        )

    return GateResult(
        gate_name="security_critical",
        status=GateStatus.PASSED,
        severity=GateSeverity.CRITICAL,
        message="No critical security issues found",
    )


def test_coverage_with_minimum_tests(score: float, **kwargs) -> GateResult:
    """Custom evaluator for test coverage - must have minimum number of tests"""
    coverage_percentage = kwargs.get("coverage_percentage", 0.0)
    total_tests = kwargs.get("total_tests", 0)
    min_tests_required = kwargs.get("min_tests_required", 10)

    if total_tests < min_tests_required:
        return GateResult(
            gate_name="test_coverage",
            status=GateStatus.FAILED,
            severity=GateSeverity.MEDIUM,
            message=f"Insufficient tests: {total_tests} < {min_tests_required}",
            details={
                "total_tests": total_tests,
                "min_tests_required": min_tests_required,
                "coverage_percentage": coverage_percentage,
            },
        )

    # Use the default score-based evaluation
    if score >= 70.0:
        return GateResult(
            gate_name="test_coverage",
            status=GateStatus.PASSED,
            severity=GateSeverity.MEDIUM,
            message=f"Test coverage passed: {coverage_percentage:.1f}%",
        )
    return GateResult(
        gate_name="test_coverage",
        status=GateStatus.FAILED,
        severity=GateSeverity.MEDIUM,
        message=f"Test coverage failed: {coverage_percentage:.1f}% < 70%",
    )
