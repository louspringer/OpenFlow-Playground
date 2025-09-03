#!/usr/bin/env python3
"""
Quality Monitoring Framework

Implements monitoring-driven quality requirements that adapt based on real usage patterns
and operational experience, avoiding RDI pollution while maintaining quality guard rails.
"""

import time
import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@dataclass
class QualityMetric:
    """Quality metric with adaptive thresholds."""

    name: str
    value: float
    threshold: float
    adaptive_threshold: bool = True
    usage_pattern: str = "normal"
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class QualityIncident:
    """Quality incident for driving requirement improvement."""

    id: str
    component: str
    metric: str
    threshold_violation: float
    impact: str
    root_cause: str
    resolution: str
    timestamp: datetime = None
    lessons_learned: str = ""

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class QualityMonitoringFramework:
    """Monitoring-driven quality framework that adapts based on real usage."""

    def __init__(self):
        """Initialize the quality monitoring framework."""
        self.metrics_file = Path("quality_metrics.json")
        self.incidents_file = Path("quality_incidents.json")
        self.adaptive_thresholds = {}
        self.usage_patterns = {}
        self.quality_metrics = self._load_metrics()
        self.quality_incidents = self._load_incidents()

    def _load_metrics(self) -> List[Dict[str, Any]]:
        """Load quality metrics from file."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load quality metrics: {e}")
        return []

    def _save_metrics(self):
        """Save quality metrics to file."""
        try:
            with open(self.metrics_file, "w") as f:
                json.dump(self.quality_metrics, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving quality metrics: {e}")

    def _load_incidents(self) -> List[Dict[str, Any]]:
        """Load quality incidents from file."""
        if self.incidents_file.exists():
            try:
                with open(self.incidents_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load quality incidents: {e}")
        return []

    def _save_incidents(self):
        """Save quality incidents to file."""
        try:
            with open(self.incidents_file, "w") as f:
                json.dump(self.quality_incidents, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving quality incidents: {e}")

    def record_metric(self, metric: QualityMetric):
        """Record a quality metric with adaptive threshold handling."""
        metric_dict = asdict(metric)
        self.quality_metrics.append(metric_dict)

        # Update adaptive thresholds based on usage patterns
        if metric.adaptive_threshold:
            self._update_adaptive_threshold(metric)

        # Check for threshold violations
        if metric.value > metric.threshold:
            self._handle_threshold_violation(metric)

        self._save_metrics()

    def _update_adaptive_threshold(self, metric: QualityMetric):
        """Update adaptive thresholds based on usage patterns."""
        key = f"{metric.name}_{metric.usage_pattern}"

        if key not in self.adaptive_thresholds:
            self.adaptive_thresholds[key] = {"values": [], "threshold": metric.threshold, "pattern": metric.usage_pattern}

        # Add current value to pattern history
        self.adaptive_thresholds[key]["values"].append(metric.value)

        # Keep only last 100 values for pattern analysis
        if len(self.adaptive_thresholds[key]["values"]) > 100:
            self.adaptive_thresholds[key]["values"] = self.adaptive_thresholds[key]["values"][-100:]

        # Calculate adaptive threshold based on pattern
        values = self.adaptive_thresholds[key]["values"]
        if len(values) >= 10:  # Need minimum data for pattern analysis
            # Use 95th percentile as adaptive threshold
            sorted_values = sorted(values)
            percentile_95 = sorted_values[int(len(sorted_values) * 0.95)]

            # Only adjust if new threshold is significantly different
            current_threshold = self.adaptive_thresholds[key]["threshold"]
            if abs(percentile_95 - current_threshold) > current_threshold * 0.1:  # 10% change
                self.adaptive_thresholds[key]["threshold"] = percentile_95
                print(f"🔄 Adaptive threshold updated for {metric.name} ({metric.usage_pattern}): {current_threshold:.2f} -> {percentile_95:.2f}")

    def _handle_threshold_violation(self, metric: QualityMetric):
        """Handle threshold violations and create incidents."""
        incident_id = f"QUAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        incident = QualityIncident(
            id=incident_id,
            component=metric.name,
            metric=metric.name,
            threshold_violation=metric.value - metric.threshold,
            impact=self._assess_impact(metric),
            root_cause="Threshold violation detected",
            resolution="Investigation required",
            lessons_learned="",
        )

        incident_dict = asdict(incident)
        self.quality_incidents.append(incident_dict)
        self._save_incidents()

        print(f"🚨 Quality incident created: {incident_id} - {metric.name} threshold violation")

    def _assess_impact(self, metric: QualityMetric) -> str:
        """Assess the impact of a threshold violation."""
        violation_ratio = metric.value / metric.threshold

        if violation_ratio > 2.0:
            return "Critical - System may be unstable"
        elif violation_ratio > 1.5:
            return "High - Significant performance degradation"
        elif violation_ratio > 1.2:
            return "Medium - Noticeable performance impact"
        else:
            return "Low - Minor performance impact"

    def get_adaptive_threshold(self, metric_name: str, usage_pattern: str = "normal") -> float:
        """Get adaptive threshold for a metric and usage pattern."""
        key = f"{metric_name}_{usage_pattern}"
        if key in self.adaptive_thresholds:
            return self.adaptive_thresholds[key]["threshold"]
        return 1.0  # Default threshold

    def analyze_usage_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns and recommend threshold adjustments."""
        analysis = {"patterns": {}, "recommendations": [], "trends": {}}

        for key, data in self.adaptive_thresholds.items():
            metric_name, pattern = key.rsplit("_", 1)

            if metric_name not in analysis["patterns"]:
                analysis["patterns"][metric_name] = {}

            values = data["values"]
            if len(values) >= 10:
                analysis["patterns"][metric_name][pattern] = {
                    "current_threshold": data["threshold"],
                    "average": sum(values) / len(values),
                    "max": max(values),
                    "min": min(values),
                    "trend": self._calculate_trend(values),
                }

                # Generate recommendations
                if data["threshold"] < max(values) * 0.9:
                    analysis["recommendations"].append(
                        {"metric": metric_name, "pattern": pattern, "recommendation": "Consider increasing threshold", "current": data["threshold"], "suggested": max(values) * 0.95}
                    )

        return analysis

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values."""
        if len(values) < 5:
            return "insufficient_data"

        # Simple linear trend calculation
        recent_avg = sum(values[-5:]) / 5
        older_avg = sum(values[-10:-5]) / 5 if len(values) >= 10 else sum(values[:-5]) / (len(values) - 5)

        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"

    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "metrics_summary": self._get_metrics_summary(),
            "incidents_summary": self._get_incidents_summary(),
            "adaptive_thresholds": self.adaptive_thresholds,
            "usage_patterns": self.analyze_usage_patterns(),
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of quality metrics."""
        if not self.quality_metrics:
            return {"total_metrics": 0, "violations": 0}

        total_metrics = len(self.quality_metrics)
        violations = sum(1 for m in self.quality_metrics if m.get("value", 0) > m.get("threshold", 0))

        return {"total_metrics": total_metrics, "violations": violations, "violation_rate": violations / total_metrics if total_metrics > 0 else 0}

    def _get_incidents_summary(self) -> Dict[str, Any]:
        """Get summary of quality incidents."""
        if not self.quality_incidents:
            return {"total_incidents": 0, "resolved": 0}

        total_incidents = len(self.quality_incidents)
        resolved = sum(1 for i in self.quality_incidents if i.get("resolution") != "Investigation required")

        return {"total_incidents": total_incidents, "resolved": resolved, "resolution_rate": resolved / total_incidents if total_incidents > 0 else 0}

    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate quality improvement recommendations."""
        recommendations = []

        # Analyze patterns and generate recommendations
        pattern_analysis = self.analyze_usage_patterns()
        recommendations.extend(pattern_analysis.get("recommendations", []))

        # Generate incident-based recommendations
        unresolved_incidents = [i for i in self.quality_incidents if i.get("resolution") == "Investigation required"]
        if unresolved_incidents:
            recommendations.append({"type": "incident_resolution", "recommendation": f"Resolve {len(unresolved_incidents)} unresolved quality incidents", "priority": "high"})

        return recommendations


def main():
    """Main function for quality monitoring framework."""
    framework = QualityMonitoringFramework()

    # Example usage
    print("🔍 Quality Monitoring Framework")
    print("==============================")

    # Record some example metrics
    framework.record_metric(QualityMetric(name="response_time", value=1.5, threshold=2.0, usage_pattern="normal"))

    framework.record_metric(QualityMetric(name="response_time", value=2.5, threshold=2.0, usage_pattern="normal"))  # This will trigger a threshold violation

    # Generate and display report
    report = framework.generate_quality_report()
    print(f"\n📊 Quality Report:")
    print(f"Total Metrics: {report['metrics_summary']['total_metrics']}")
    print(f"Violations: {report['metrics_summary']['violations']}")
    print(f"Total Incidents: {report['incidents_summary']['total_incidents']}")
    print(f"Resolved: {report['incidents_summary']['resolved']}")

    if report["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec.get('recommendation', 'N/A')}")


if __name__ == "__main__":
    main()
