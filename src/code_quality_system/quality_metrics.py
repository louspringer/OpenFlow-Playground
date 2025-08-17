#!/usr/bin/env python3
"""
Quality Metrics System

Calculates and tracks code quality scores based on various metrics.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class QualityScore:
    """Individual quality score for a specific metric"""

    metric_name: str
    score: float  # 0.0 to 100.0
    weight: float = 1.0  # Weight for overall calculation
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Validate score range"""
        if not 0.0 <= self.score <= 100.0:
            msg = f"Score must be between 0.0 and 100.0, got {self.score}"
            raise ValueError(msg)

        if self.weight < 0.0:
            msg = f"Weight must be non-negative, got {self.weight}"
            raise ValueError(msg)


@dataclass
class QualityMetrics:
    """Comprehensive quality metrics for a project or file"""

    project_path: Path
    scores: list[QualityScore] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def overall_score(self) -> float:
        """Calculate weighted overall quality score"""
        if not self.scores:
            return 0.0

        total_weight = sum(score.weight for score in self.scores)
        if total_weight == 0.0:
            return 0.0

        weighted_sum = sum(score.score * score.weight for score in self.scores)
        return weighted_sum / total_weight

    @property
    def score_breakdown(self) -> dict[str, float]:
        """Get breakdown of individual metric scores"""
        return {score.metric_name: score.score for score in self.scores}

    def add_score(self, score: QualityScore) -> None:
        """Add a quality score"""
        self.scores.append(score)

    def get_score(self, metric_name: str) -> Optional[QualityScore]:
        """Get score for a specific metric"""
        for score in self.scores:
            if score.metric_name == metric_name:
                return score
        return None

    def update_score(self, metric_name: str, new_score: float, **kwargs) -> None:
        """Update score for a specific metric"""
        existing_score = self.get_score(metric_name)
        if existing_score:
            existing_score.score = new_score
            existing_score.timestamp = datetime.now(timezone.utc)
            for key, value in kwargs.items():
                setattr(existing_score, key, value)
        else:
            self.add_score(QualityScore(metric_name, new_score, **kwargs))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "project_path": str(self.project_path),
            "overall_score": self.overall_score,
            "scores": [
                {
                    "metric_name": score.metric_name,
                    "score": score.score,
                    "weight": score.weight,
                    "details": score.details,
                    "timestamp": score.timestamp.isoformat(),
                }
                for score in self.scores
            ],
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }

    def save_to_file(self, file_path: Path) -> None:
        """Save metrics to a JSON file"""
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: Path) -> "QualityMetrics":
        """Load metrics from a JSON file"""
        with open(file_path) as f:
            data = json.load(f)

        # Reconstruct scores
        scores = []
        for score_data in data.get("scores", []):
            score = QualityScore(
                metric_name=score_data["metric_name"],
                score=score_data["score"],
                weight=score_data.get("weight", 1.0),
                details=score_data.get("details", {}),
                timestamp=datetime.fromisoformat(score_data["timestamp"]),
            )
            scores.append(score)

        # Reconstruct metadata
        metadata = data.get("metadata", {})
        timestamp = datetime.fromisoformat(data["timestamp"])

        return cls(
            project_path=Path(data["project_path"]),
            scores=scores,
            metadata=metadata,
            timestamp=timestamp,
        )


class QualityMetricsCalculator:
    """Calculates quality metrics from various sources"""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    def calculate_code_quality_score(
        self, flake8_issues: list[dict[str, Any]]
    ) -> QualityScore:
        """Calculate code quality score from flake8 issues"""
        if not flake8_issues:
            return QualityScore("code_quality", 100.0, weight=2.0)

        # Penalize based on number and severity of issues
        total_issues = len(flake8_issues)
        critical_issues = len(
            [i for i in flake8_issues if i.get("priority") == "critical"]
        )
        high_issues = len([i for i in flake8_issues if i.get("priority") == "high"])

        # Base score starts at 100
        score = 100.0

        # Penalize for issues
        score -= critical_issues * 10  # Critical issues are expensive
        score -= high_issues * 5  # High priority issues are costly
        score -= total_issues * 1  # Each issue has a small cost

        # Ensure score doesn't go below 0
        score = max(0.0, score)

        return QualityScore(
            "code_quality",
            score,
            weight=2.0,
            details={
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "flake8_issues": flake8_issues,
            },
        )

    def calculate_security_score(
        self, security_issues: list[dict[str, Any]]
    ) -> QualityScore:
        """Calculate security score from security analysis"""
        if not security_issues:
            return QualityScore("security", 100.0, weight=3.0)

        # Security issues are heavily weighted
        total_issues = len(security_issues)
        critical_issues = len(
            [i for i in security_issues if i.get("priority") == "critical"]
        )
        high_issues = len([i for i in security_issues if i.get("priority") == "high"])

        score = 100.0
        score -= critical_issues * 25  # Critical security issues are very expensive
        score -= high_issues * 15  # High priority security issues are costly
        score -= total_issues * 5  # Each security issue has significant cost

        score = max(0.0, score)

        return QualityScore(
            "security",
            score,
            weight=3.0,
            details={
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "security_issues": security_issues,
            },
        )

    def calculate_test_coverage_score(self, coverage_percentage: float) -> QualityScore:
        """Calculate test coverage score"""
        # Coverage is already a percentage, just normalize to 0-100
        score = min(100.0, coverage_percentage)

        return QualityScore(
            "test_coverage",
            score,
            weight=1.5,
            details={"coverage_percentage": coverage_percentage},
        )

    def calculate_performance_score(
        self, performance_metrics: dict[str, Any]
    ) -> QualityScore:
        """Calculate performance score from various metrics"""
        # This is a placeholder - implement based on your performance metrics
        score = 100.0

        # Example: penalize for slow operations
        if "slow_operations" in performance_metrics:
            slow_ops = performance_metrics["slow_operations"]
            score -= slow_ops * 5

        score = max(0.0, score)

        return QualityScore(
            "performance", score, weight=1.0, details=performance_metrics
        )

    def calculate_all_metrics(self, analysis_results: dict[str, Any]) -> QualityMetrics:
        """Calculate all quality metrics from analysis results"""
        metrics = QualityMetrics(self.project_path)

        # Calculate individual scores
        if "flake8_issues" in analysis_results:
            code_quality = self.calculate_code_quality_score(
                analysis_results["flake8_issues"]
            )
            metrics.add_score(code_quality)

        if "security_issues" in analysis_results:
            security = self.calculate_security_score(
                analysis_results["security_issues"]
            )
            metrics.add_score(security)

        if "coverage_percentage" in analysis_results:
            coverage = self.calculate_test_coverage_score(
                analysis_results["coverage_percentage"]
            )
            metrics.add_score(coverage)

        if "performance_metrics" in analysis_results:
            performance = self.calculate_performance_score(
                analysis_results["performance_metrics"]
            )
            metrics.add_score(performance)

        return metrics
