"""
RM-DDD Health Monitoring

Health monitoring system for RM-DDD components.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum

from .types import ModuleHealth, ModuleStatus, ModuleCapability, DomainHealth


class HealthStatusType(Enum):
    """Health status types"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthIndicator:
    """Individual health indicator"""

    name: str
    value: Any
    unit: Optional[str] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    status: HealthStatusType = HealthStatusType.HEALTHY
    last_updated: datetime = field(default_factory=datetime.now)


class HealthMonitor:
    """Advanced health monitoring for RM-DDD components"""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.indicators: Dict[str, HealthIndicator] = {}
        self.start_time = datetime.now()
        self.last_health_check = datetime.now()

    def add_indicator(self, name: str, value: Any, unit: Optional[str] = None, threshold_warning: Optional[float] = None, threshold_critical: Optional[float] = None):
        """Add a health indicator"""
        status = self._evaluate_indicator_status(value, threshold_warning, threshold_critical)

        self.indicators[name] = HealthIndicator(name=name, value=value, unit=unit, threshold_warning=threshold_warning, threshold_critical=threshold_critical, status=status)

    def update_indicator(self, name: str, value: Any):
        """Update an existing health indicator"""
        if name in self.indicators:
            indicator = self.indicators[name]
            status = self._evaluate_indicator_status(value, indicator.threshold_warning, indicator.threshold_critical)

            self.indicators[name] = HealthIndicator(
                name=name, value=value, unit=indicator.unit, threshold_warning=indicator.threshold_warning, threshold_critical=indicator.threshold_critical, status=status
            )

    def _evaluate_indicator_status(self, value: Any, warning_threshold: Optional[float], critical_threshold: Optional[float]) -> HealthStatusType:
        """Evaluate indicator status based on thresholds"""
        if not isinstance(value, (int, float)):
            return HealthStatusType.HEALTHY

        if critical_threshold is not None and value >= critical_threshold:
            return HealthStatusType.UNHEALTHY
        elif warning_threshold is not None and value >= warning_threshold:
            return HealthStatusType.DEGRADED
        else:
            return HealthStatusType.HEALTHY

    def get_overall_status(self) -> ModuleStatus:
        """Get overall module status based on indicators"""
        if not self.indicators:
            return ModuleStatus.AVAILABLE

        statuses = [indicator.status for indicator in self.indicators.values()]

        if HealthStatusType.UNHEALTHY in statuses:
            return ModuleStatus.UNAVAILABLE
        elif HealthStatusType.DEGRADED in statuses:
            return ModuleStatus.DEGRADED
        else:
            return ModuleStatus.AVAILABLE

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        overall_status = self.get_overall_status()

        return {
            "module_name": self.module_name,
            "overall_status": overall_status,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "last_health_check": self.last_health_check,
            "total_indicators": len(self.indicators),
            "healthy_indicators": sum(1 for i in self.indicators.values() if i.status == HealthStatusType.HEALTHY),
            "degraded_indicators": sum(1 for i in self.indicators.values() if i.status == HealthStatusType.DEGRADED),
            "unhealthy_indicators": sum(1 for i in self.indicators.values() if i.status == HealthStatusType.UNHEALTHY),
            "indicators": {
                name: {"value": indicator.value, "unit": indicator.unit, "status": indicator.status.value, "last_updated": indicator.last_updated} for name, indicator in self.indicators.items()
            },
        }

    def get_indicators_dict(self) -> Dict[str, Any]:
        """Get indicators as dictionary for RM interface"""
        return {name: indicator.value for name, indicator in self.indicators.items()}


class DomainHealthMonitor(HealthMonitor):
    """Domain-specific health monitoring"""

    def __init__(self, module_name: str, domain_context: str):
        super().__init__(module_name)
        self.domain_context = domain_context
        self._setup_domain_indicators()

    def _setup_domain_indicators(self):
        """Setup domain-specific health indicators"""
        self.add_indicator("domain_context", self.domain_context)
        self.add_indicator("boundary_integrity", True)
        self.add_indicator("invariant_compliance", True)
        self.add_indicator("language_consistency", 1.0, threshold_warning=0.8)
        self.add_indicator("complexity_score", 0.0, threshold_warning=0.7, threshold_critical=0.9)

    def update_domain_metrics(self, boundary_integrity: bool, invariant_compliance: bool, language_consistency: float, complexity_score: float):
        """Update domain-specific metrics"""
        self.update_indicator("boundary_integrity", boundary_integrity)
        self.update_indicator("invariant_compliance", invariant_compliance)
        self.update_indicator("language_consistency", language_consistency)
        self.update_indicator("complexity_score", complexity_score)

    def get_domain_health(self) -> DomainHealth:
        """Get domain health information"""
        return DomainHealth(
            domain_context=self.domain_context,
            boundary_integrity=self.indicators["boundary_integrity"].value,
            invariant_compliance=self.indicators["invariant_compliance"].value,
            language_consistency=self.indicators["language_consistency"].value,
            complexity_score=self.indicators["complexity_score"].value,
        )
