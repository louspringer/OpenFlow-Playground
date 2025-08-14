#!/usr/bin/env python3
"""Cost analysis for diversity systems"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any


def estimate_tokens(text: str) -> int:
    """Estimate token count for text (rough approximation)"""
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4


@dataclass
class CostMetric:
    """Represents a cost metric for diversity analysis"""

    metric_name: str
    value: float
    unit: str
    timestamp: str
    context: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "metric_name": self.metric_name,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "context": self.context,
        }


@dataclass
class CostBreakdown:
    """Breakdown of costs by component"""

    component: str
    cost_per_request: float
    requests_per_hour: int
    hourly_cost: float
    daily_cost: float
    monthly_cost: float

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "component": self.component,
            "cost_per_request": self.cost_per_request,
            "requests_per_hour": self.requests_per_hour,
            "hourly_cost": self.hourly_cost,
            "daily_cost": self.daily_cost,
            "monthly_cost": self.monthly_cost,
        }


class CostAnalysis:
    """Analyzes costs of diversity systems"""

    def __init__(self):
        """Initialize the cost analyzer"""
        self.cost_metrics: list[CostMetric] = []
        self.cost_breakdowns: list[CostBreakdown] = []
        self.analysis_timestamp = datetime.now().isoformat()

    def add_cost_metric(
        self, metric_name: str, value: float, unit: str, context: str = ""
    ):
        """Add a cost metric"""
        metric = CostMetric(
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=datetime.now().isoformat(),
            context=context,
        )
        self.cost_metrics.append(metric)

    def calculate_model_costs(
        self, models: list[str], requests_per_hour: int = 100
    ) -> list[CostBreakdown]:
        """Calculate costs for different AI models"""
        # Approximate costs per 1K tokens (as of 2024)
        model_costs = {
            "gpt4": 0.03,  # $0.03 per 1K tokens
            "gpt4o": 0.005,  # $0.005 per 1K tokens
            "gpt4_turbo": 0.01,  # $0.01 per 1K tokens
            "claude": 0.015,  # $0.015 per 1K tokens
            "claude_web": 0.015,
            "claude_haiku": 0.00025,
            "claude_opus": 0.015,
            "perplexity": 0.001,
            "mixtral": 0.00014,
        }

        breakdowns = []
        for model in models:
            cost_per_1k_tokens = model_costs.get(model, 0.01)  # Default cost
            avg_tokens_per_request = 500  # Estimate

            cost_per_request = (cost_per_1k_tokens * avg_tokens_per_request) / 1000
            hourly_cost = cost_per_request * requests_per_hour
            daily_cost = hourly_cost * 24
            monthly_cost = daily_cost * 30

            breakdown = CostBreakdown(
                component=f"Model: {model}",
                cost_per_request=cost_per_request,
                requests_per_hour=requests_per_hour,
                hourly_cost=hourly_cost,
                daily_cost=daily_cost,
                monthly_cost=monthly_cost,
            )
            breakdowns.append(breakdown)

        self.cost_breakdowns.extend(breakdowns)
        return breakdowns

    def calculate_diversity_benefits(
        self, diversity_score: float, base_cost: float
    ) -> dict[str, Any]:
        """Calculate cost-benefit of diversity improvements"""
        # Higher diversity typically means better quality, fewer rework costs
        quality_improvement = diversity_score * 0.3  # 30% max improvement
        rework_reduction = diversity_score * 0.2  # 20% max reduction

        # Calculate savings
        quality_savings = base_cost * quality_improvement
        rework_savings = base_cost * rework_reduction
        total_savings = quality_savings + rework_savings

        # Net cost (costs minus savings)
        net_cost = base_cost - total_savings

        return {
            "diversity_score": diversity_score,
            "base_cost": base_cost,
            "quality_improvement": quality_improvement,
            "rework_reduction": rework_reduction,
            "quality_savings": quality_savings,
            "rework_savings": rework_savings,
            "total_savings": total_savings,
            "net_cost": net_cost,
            "roi": (total_savings / base_cost) * 100 if base_cost > 0 else 0,
        }

    def optimize_diversity_cost(
        self, target_diversity: float, budget: float
    ) -> dict[str, Any]:
        """Optimize diversity system for cost and performance"""
        # Find most cost-effective models for target diversity

        # Sort models by cost-effectiveness (diversity per dollar)
        model_efficiency = {
            "claude_haiku": 0.8,  # High diversity, low cost
            "mixtral": 0.75,  # Good diversity, very low cost
            "perplexity": 0.7,  # Good diversity, low cost
            "gpt4o": 0.6,  # Good diversity, medium cost
            "claude": 0.5,  # Medium diversity, medium cost
            "gpt4": 0.4,  # High diversity, high cost
            "claude_opus": 0.3,  # High diversity, high cost
        }

        # Select models to meet target diversity within budget
        selected_models = []
        current_diversity = 0.0
        current_cost = 0.0

        for model, efficiency in sorted(
            model_efficiency.items(), key=lambda x: x[1], reverse=True
        ):
            if current_diversity >= target_diversity:
                break

            model_cost = self.calculate_model_costs([model], 50)[0]  # 50 requests/hour
            if current_cost + model_cost.monthly_cost <= budget:
                selected_models.append(model)
                current_diversity += efficiency * 0.15  # Each model adds diversity
                current_cost += model_cost.monthly_cost

        return {
            "target_diversity": target_diversity,
            "achieved_diversity": min(current_diversity, 1.0),
            "budget": budget,
            "total_cost": current_cost,
            "selected_models": selected_models,
            "cost_efficiency": (
                current_diversity / current_cost if current_cost > 0 else 0
            ),
        }

    def generate_cost_report(self) -> dict[str, Any]:
        """Generate comprehensive cost analysis report"""
        total_monthly_cost = sum(bd.monthly_cost for bd in self.cost_breakdowns)
        total_daily_cost = sum(bd.daily_cost for bd in self.cost_breakdowns)

        # Group by component type
        model_costs = [
            bd for bd in self.cost_breakdowns if bd.component.startswith("Model:")
        ]
        infrastructure_costs = [
            bd
            for bd in self.cost_breakdowns
            if "infrastructure" in bd.component.lower()
        ]

        return {
            "summary": {
                "total_monthly_cost": total_monthly_cost,
                "total_daily_cost": total_daily_cost,
                "total_components": len(self.cost_breakdowns),
                "analysis_timestamp": self.analysis_timestamp,
            },
            "cost_breakdowns": [bd.to_dict() for bd in self.cost_breakdowns],
            "component_summary": {
                "models": len(model_costs),
                "infrastructure": len(infrastructure_costs),
                "other": len(self.cost_breakdowns)
                - len(model_costs)
                - len(infrastructure_costs),
            },
            "cost_metrics": [cm.to_dict() for cm in self.cost_metrics],
            "recommendations": [
                "Use Claude Haiku and Mixtral for cost-effective diversity",
                "Monitor token usage to optimize costs",
                "Consider batch processing for multiple requests",
                "Implement caching for repeated analyses",
            ],
        }

    def save_report(self, filename: str = None):
        """Save cost analysis report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cost_analysis_report_{timestamp}.json"

        report = self.generate_cost_report()
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        return filename
