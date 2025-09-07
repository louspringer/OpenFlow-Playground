"""
RM-DDD Domain Services

Domain service implementations with RM compliance.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional

from ..core.base import DomainReflectiveModule
from ..core.types import ModuleHealth, ModuleStatus, ModuleCapability, DomainBoundaries, ValidationResult


class DomainService(DomainReflectiveModule, ABC):
    """Base class for domain services"""

    def __init__(self, domain_context: str, service_name: str):
        self.service_name = service_name
        super().__init__(domain_context)

    @abstractmethod
    def get_domain_boundaries(self) -> DomainBoundaries:
        """Define service domain boundaries"""
        pass

    @abstractmethod
    def validate_domain_invariants(self) -> ValidationResult:
        """Validate service operates within domain boundaries"""
        pass

    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get service capabilities"""
        base_capabilities = await super().get_module_capabilities()
        service_capabilities = [ModuleCapability(name=f"domain_service_{self.service_name}", description=f"Domain service: {self.service_name}", enabled=await self.is_healthy(), version="1.0.0")]
        return base_capabilities + service_capabilities

    async def get_module_status(self) -> ModuleHealth:
        """Get service health status"""
        is_healthy = await self.is_healthy()
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if is_healthy else ModuleStatus.DEGRADED,
            message=f"Domain service {self.service_name} in {self.domain_context}",
            capabilities=await self.get_module_capabilities(),
            indicators=await self.get_health_indicators(),
        )

    async def is_healthy(self) -> bool:
        """Check if service is healthy"""
        validation_result = self.validate_domain_invariants()
        return validation_result.is_valid

    async def get_health_indicators(self) -> dict:
        """Get service health indicators"""
        validation_result = self.validate_domain_invariants()
        return {
            "service_name": self.service_name,
            "domain_context": self.domain_context,
            "invariant_violations": len(validation_result.errors),
            "invariant_warnings": len(validation_result.warnings),
            "is_valid": validation_result.is_valid,
        }
