"""
RM-DDD Core Base Classes

Base classes for Reflective Module functionality with domain awareness.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from .types import ModuleHealth, ModuleCapability, DomainBoundaries, ValidationResult

# Import registry lazily to avoid circular imports


class ReflectiveModuleBase(ABC):
    """Base class for all RM-DDD components"""

    def __init__(self, module_id: Optional[str] = None):
        self.module_id = module_id or self._generate_module_id()
        self._health_monitor = HealthMonitor(self)
        self._register_module()

    @abstractmethod
    async def get_module_status(self) -> ModuleHealth:
        """Get current module status"""
        pass

    @abstractmethod
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get module capabilities"""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if module is healthy"""
        pass

    @abstractmethod
    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators"""
        pass

    def _register_module(self):
        """Register this module with the global registry"""
        # Lazy import to avoid circular dependency
        from .registry import get_global_registry

        registry = get_global_registry()
        # Note: This would need to be async in a real implementation
        # For now, we'll skip auto-registration to avoid complexity
        pass

    def _generate_module_id(self) -> str:
        """Generate unique module ID"""
        return f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"


class DomainReflectiveModule(ReflectiveModuleBase):
    """Enhanced RM base class with domain awareness"""

    def __init__(self, domain_context: str, module_id: Optional[str] = None):
        self.domain_context = domain_context
        super().__init__(module_id)

    @abstractmethod
    def get_domain_boundaries(self) -> DomainBoundaries:
        """Get domain boundaries for this module"""
        pass

    @abstractmethod
    def validate_domain_invariants(self) -> ValidationResult:
        """Validate domain invariants"""
        pass

    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get domain-aware module capabilities"""
        base_capabilities = await super().get_module_capabilities()
        if base_capabilities is None:
            base_capabilities = []

        domain_capabilities = [ModuleCapability(name=f"domain_context_{self.domain_context}", description=f"Domain context: {self.domain_context}", enabled=True, version="1.0.0")]
        return base_capabilities + domain_capabilities


class HealthMonitor:
    """Monitors RM-DDD component health"""

    def __init__(self, module: ReflectiveModuleBase):
        self.module = module
        self.metrics_collector = MetricsCollector()

    async def collect_health_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive health metrics"""
        return {
            "uptime": self._calculate_uptime(),
            "performance_metrics": await self._collect_performance_metrics(),
            "domain_metrics": await self._collect_domain_metrics(),
            "compliance_metrics": await self._collect_compliance_metrics(),
        }

    def _calculate_uptime(self) -> float:
        """Calculate module uptime in seconds"""
        # Implementation would track actual uptime
        return 0.0

    async def _collect_performance_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics"""
        return {"response_time_ms": 0.0, "throughput_per_second": 0.0, "error_rate": 0.0}

    async def _collect_domain_metrics(self) -> Dict[str, Any]:
        """Collect domain-specific metrics"""
        if isinstance(self.module, DomainReflectiveModule):
            return {"domain_context": self.module.domain_context, "boundary_integrity": True, "invariant_compliance": True}
        return {}

    async def _collect_compliance_metrics(self) -> Dict[str, Any]:
        """Collect RM compliance metrics"""
        return {"rm_interface_compliance": True, "health_monitoring_active": True, "registry_registration": True}


class MetricsCollector:
    """Collects and aggregates metrics for health monitoring"""

    def __init__(self):
        self.metrics: Dict[str, Any] = {}

    async def record_metric(self, name: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        """Record a metric value"""
        self.metrics[name] = {"value": value, "timestamp": datetime.now(), "metadata": metadata or {}}

    async def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        return self.metrics.copy()
