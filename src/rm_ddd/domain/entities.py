"""
RM-DDD Domain Entities

Entity and Aggregate Root implementations with RM compliance.
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from ..core.base import DomainReflectiveModule
from ..core.types import ModuleHealth, ModuleStatus, ModuleCapability, DomainBoundaries, ValidationResult

EntityId = TypeVar("EntityId")


class Entity(DomainReflectiveModule, Generic[EntityId], ABC):
    """Base class for domain entities"""

    def __init__(self, entity_id: EntityId, domain_context: str):
        self.id = entity_id
        self._version = 1
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        super().__init__(domain_context)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id and type(self) == type(other)

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    @abstractmethod
    def get_domain_boundaries(self) -> DomainBoundaries:
        """Define entity domain boundaries"""
        pass

    @abstractmethod
    def validate_domain_invariants(self) -> ValidationResult:
        """Validate entity invariants"""
        pass

    def _update_version(self):
        """Update entity version for optimistic locking"""
        self._version += 1
        self._updated_at = datetime.now()

    async def get_module_status(self) -> ModuleHealth:
        """Get entity health status"""
        is_healthy = await self.is_healthy()
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if is_healthy else ModuleStatus.DEGRADED,
            message=f"Entity {self.__class__.__name__} with ID {self.id}",
            capabilities=await self.get_module_capabilities(),
            indicators=await self.get_health_indicators(),
        )

    async def is_healthy(self) -> bool:
        """Check if entity is healthy"""
        validation_result = self.validate_domain_invariants()
        return validation_result.is_valid

    async def get_health_indicators(self) -> dict:
        """Get entity health indicators"""
        validation_result = self.validate_domain_invariants()
        return {
            "entity_id": str(self.id),
            "version": self._version,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "domain_context": self.domain_context,
            "invariant_violations": len(validation_result.errors),
            "invariant_warnings": len(validation_result.warnings),
            "is_valid": validation_result.is_valid,
        }


class AggregateRoot(Entity[EntityId], ABC):
    """Base class for aggregate roots"""

    def __init__(self, entity_id: EntityId, domain_context: str):
        super().__init__(entity_id, domain_context)
        self._domain_events: List["DomainEvent"] = []

    def add_domain_event(self, event: "DomainEvent"):
        """Add domain event to be published"""
        self._domain_events.append(event)

    def get_domain_events(self) -> List["DomainEvent"]:
        """Get pending domain events"""
        return self._domain_events.copy()

    def clear_domain_events(self):
        """Clear domain events after publishing"""
        self._domain_events.clear()

    @abstractmethod
    def get_aggregate_boundaries(self) -> "AggregateBoundaries":
        """Define aggregate consistency boundaries"""
        pass

    async def get_health_indicators(self) -> dict:
        """Get aggregate health indicators"""
        base_indicators = await super().get_health_indicators()
        base_indicators.update({"pending_domain_events": len(self._domain_events), "aggregate_type": self.__class__.__name__})
        return base_indicators


class AggregateBoundaries:
    """Defines aggregate consistency boundaries"""

    def __init__(self, aggregate_root: str, internal_entities: List[str], consistency_rules: List[str], invariants: List[str]):
        self.aggregate_root = aggregate_root
        self.internal_entities = internal_entities
        self.consistency_rules = consistency_rules
        self.invariants = invariants

    def validate_consistency(self, aggregate: AggregateRoot) -> ValidationResult:
        """Validate aggregate consistency"""
        result = ValidationResult(is_valid=True)

        # Check consistency rules
        for rule in self.consistency_rules:
            if not self._evaluate_consistency_rule(rule, aggregate):
                result.add_error(f"Consistency rule violated: {rule}")

        # Check invariants
        for invariant in self.invariants:
            if not self._evaluate_invariant(invariant, aggregate):
                result.add_error(f"Invariant violated: {invariant}")

        return result

    def _evaluate_consistency_rule(self, rule: str, aggregate: AggregateRoot) -> bool:
        """Evaluate a consistency rule (placeholder implementation)"""
        # In a real implementation, this would evaluate actual business rules
        return True

    def _evaluate_invariant(self, invariant: str, aggregate: AggregateRoot) -> bool:
        """Evaluate an invariant (placeholder implementation)"""
        # In a real implementation, this would evaluate actual business invariants
        return True
