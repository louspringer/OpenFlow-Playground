"""
RM-DDD Repositories

Repository pattern implementations with RM compliance.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

from ..core.base import DomainReflectiveModule
from ..core.types import ModuleHealth, ModuleStatus, ModuleCapability, ValidationResult
from .entities import Entity

T = TypeVar("T", bound=Entity)
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """Abstract repository interface (domain layer)"""

    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        """Get entity by ID"""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save entity"""
        pass

    @abstractmethod
    async def delete(self, entity_id: ID) -> bool:
        """Delete entity"""
        pass

    @abstractmethod
    async def find_by_criteria(self, criteria: "DomainCriteria") -> List[T]:
        """Find entities by domain criteria"""
        pass


class RepositoryRM(Repository[T, ID], DomainReflectiveModule):
    """RM-compliant repository base class"""

    def __init__(self, domain_context: str, entity_type: str):
        self.entity_type = entity_type
        super().__init__(domain_context)

    async def get_module_status(self) -> ModuleHealth:
        """Get repository health status"""
        is_healthy = await self.is_healthy()
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if is_healthy else ModuleStatus.DEGRADED,
            message=f"Repository for {self.entity_type}",
            capabilities=await self.get_module_capabilities(),
            indicators=await self.get_health_indicators(),
        )

    async def is_healthy(self) -> bool:
        """Check repository health"""
        try:
            # Perform health check (e.g., database connectivity)
            await self._perform_health_check()
            return True
        except Exception:
            return False

    @abstractmethod
    async def _perform_health_check(self):
        """Perform repository-specific health check"""
        pass

    async def get_health_indicators(self) -> dict:
        """Get repository health indicators"""
        return {"entity_type": self.entity_type, "domain_context": self.domain_context, "repository_type": self.__class__.__name__}

    def get_domain_boundaries(self) -> "DomainBoundaries":
        """Get domain boundaries for repository"""
        from ..core.types import DomainBoundaries

        return DomainBoundaries(context=self.domain_context, bounded_context_rules=[f"Repository for {self.entity_type} in {self.domain_context}", "Provides data access for domain entities"])

    def validate_domain_invariants(self) -> ValidationResult:
        """Validate repository invariants"""
        result = ValidationResult(is_valid=True)

        if not self.entity_type:
            result.add_error("Repository must specify entity type")

        return result


class DomainCriteria:
    """Domain criteria for repository queries"""

    def __init__(self, filters: Optional[dict] = None, ordering: Optional[List[str]] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        self.filters = filters or {}
        self.ordering = ordering or []
        self.limit = limit
        self.offset = offset or 0
