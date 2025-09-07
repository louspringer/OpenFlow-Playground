"""
RM-DDD Validators

Validation utilities for domain logic and RM compliance.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from ..core.types import ValidationResult
from ..domain.entities import Entity, AggregateRoot


class DomainValidator:
    """Utility for domain validation"""

    @staticmethod
    def validate_entity_invariants(entity: Entity) -> ValidationResult:
        """Validate entity invariants"""
        result = ValidationResult(is_valid=True)

        # Check entity ID
        if entity.id is None:
            result.add_error("Entity ID cannot be None")

        # Check domain context
        if not hasattr(entity, "domain_context") or not entity.domain_context:
            result.add_error("Entity must have a domain context")

        # Check version
        if hasattr(entity, "_version") and entity._version < 1:
            result.add_error("Entity version must be >= 1")

        return result

    @staticmethod
    def validate_aggregate_boundaries(aggregate: AggregateRoot) -> ValidationResult:
        """Validate aggregate boundary rules"""
        result = ValidationResult(is_valid=True)

        # Check aggregate size
        if hasattr(aggregate, "_max_aggregate_size"):
            # Implementation would count aggregate members
            pass

        # Check domain events
        if hasattr(aggregate, "_domain_events"):
            events = aggregate.get_domain_events()
            if len(events) > 100:  # Arbitrary limit
                result.add_warning("Large number of pending domain events")

        return result

    @staticmethod
    def validate_ubiquitous_language(obj: Any, term_mapping: Dict[str, str]) -> ValidationResult:
        """Validate ubiquitous language usage"""
        result = ValidationResult(is_valid=True)

        # Check class name
        class_name = obj.__class__.__name__
        if class_name.lower() not in [term.lower() for term in term_mapping.values()]:
            result.add_warning(f"Class name '{class_name}' not found in ubiquitous language mapping")

        return result

    @staticmethod
    def validate_domain_boundaries(boundaries: "DomainBoundaries") -> ValidationResult:
        """Validate domain boundaries"""
        result = ValidationResult(is_valid=True)

        if not boundaries.context:
            result.add_error("Domain context cannot be empty")

        if not boundaries.bounded_context_rules:
            result.add_warning("No bounded context rules defined")

        return result

    @staticmethod
    def validate_value_object_constraints(value_object: Any) -> ValidationResult:
        """Validate value object constraints"""
        result = ValidationResult(is_valid=True)

        # Check immutability
        if hasattr(value_object, "__setattr__"):
            # This is a basic check - in practice, you'd use more sophisticated immutability detection
            pass

        # Check equality implementation
        if not hasattr(value_object, "__eq__"):
            result.add_error("Value object must implement __eq__")

        if not hasattr(value_object, "__hash__"):
            result.add_error("Value object must implement __hash__")

        return result


class RMComplianceValidator:
    """Validator for RM compliance"""

    @staticmethod
    def validate_rm_interface(module: Any) -> ValidationResult:
        """Validate RM interface compliance"""
        result = ValidationResult(is_valid=True)

        required_methods = ["get_module_status", "get_module_capabilities", "is_healthy", "get_health_indicators"]

        for method in required_methods:
            if not hasattr(module, method):
                result.add_error(f"Missing required RM method: {method}")
            elif not callable(getattr(module, method)):
                result.add_error(f"RM method {method} is not callable")

        return result

    @staticmethod
    def validate_health_monitoring(module: Any) -> ValidationResult:
        """Validate health monitoring implementation"""
        result = ValidationResult(is_valid=True)

        # Check health indicators
        if hasattr(module, "get_health_indicators"):
            try:
                indicators = module.get_health_indicators()
                if not isinstance(indicators, dict):
                    result.add_error("Health indicators must be a dictionary")
            except Exception as e:
                result.add_error(f"Error getting health indicators: {e}")

        # Check module status
        if hasattr(module, "get_module_status"):
            try:
                status = module.get_module_status()
                if not hasattr(status, "status"):
                    result.add_error("Module status must have a status attribute")
            except Exception as e:
                result.add_error(f"Error getting module status: {e}")

        return result

    @staticmethod
    def validate_registry_integration(module: Any) -> ValidationResult:
        """Validate registry integration"""
        result = ValidationResult(is_valid=True)

        # Check if module has module_id
        if not hasattr(module, "module_id"):
            result.add_error("Module must have a module_id")
        elif not module.module_id:
            result.add_error("Module ID cannot be empty")

        return result


class DomainModelValidator:
    """Validator for domain model consistency"""

    @staticmethod
    def validate_entity_relationships(entities: List[Entity]) -> ValidationResult:
        """Validate relationships between entities"""
        result = ValidationResult(is_valid=True)

        # Check for circular dependencies
        entity_ids = {entity.id for entity in entities}

        for entity in entities:
            # This would check actual relationships in a real implementation
            pass

        return result

    @staticmethod
    def validate_aggregate_consistency(aggregates: List[AggregateRoot]) -> ValidationResult:
        """Validate aggregate consistency rules"""
        result = ValidationResult(is_valid=True)

        for aggregate in aggregates:
            # Check aggregate boundaries
            if hasattr(aggregate, "get_aggregate_boundaries"):
                boundaries = aggregate.get_aggregate_boundaries()
                boundary_result = DomainValidator.validate_aggregate_boundaries(aggregate)
                if not boundary_result.is_valid:
                    result.errors.extend(boundary_result.errors)
                    result.is_valid = False

        return result

    @staticmethod
    def validate_domain_events(events: List[Any]) -> ValidationResult:
        """Validate domain events"""
        result = ValidationResult(is_valid=True)

        for event in events:
            # Check event structure
            if not hasattr(event, "event_id"):
                result.add_error("Domain event must have event_id")

            if not hasattr(event, "aggregate_id"):
                result.add_error("Domain event must have aggregate_id")

            if not hasattr(event, "occurred_at"):
                result.add_error("Domain event must have occurred_at")

        return result


class BusinessRuleValidator:
    """Validator for business rules and invariants"""

    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def validate_business_rules(self, entity: Any) -> ValidationResult:
        """Validate business rules for an entity"""
        result = ValidationResult(is_valid=True)

        for rule in self.rules:
            if not self._evaluate_rule(rule, entity):
                result.add_error(f"Business rule violated: {rule.get('description', 'Unknown rule')}")

        return result

    def _evaluate_rule(self, rule: Dict[str, Any], entity: Any) -> bool:
        """Evaluate a business rule"""
        # This would implement actual business rule evaluation
        # For now, return True as a placeholder
        return True

    def validate_invariants(self, entity: Any) -> ValidationResult:
        """Validate business invariants"""
        result = ValidationResult(is_valid=True)

        # Check if entity has invariant validation
        if hasattr(entity, "validate_domain_invariants"):
            invariant_result = entity.validate_domain_invariants()
            if not invariant_result.is_valid:
                result.errors.extend(invariant_result.errors)
                result.is_valid = False

        return result
