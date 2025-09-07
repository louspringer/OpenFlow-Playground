"""
RM-DDD Bounded Contexts

Bounded context and context mapping implementations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

from ..core.types import ValidationResult


class ContextRelationshipType(Enum):
    """Types of relationships between bounded contexts"""

    UPSTREAM_DOWNSTREAM = "upstream_downstream"
    PARTNER = "partner"
    SHARED_KERNEL = "shared_kernel"
    CUSTOMER_SUPPLIER = "customer_supplier"
    CONFORMIST = "conformist"
    ANTICORRUPTION_LAYER = "anticorruption_layer"
    OPEN_HOST_SERVICE = "open_host_service"
    PUBLISHED_LANGUAGE = "published_language"


@dataclass
class BoundedContext:
    """Represents a bounded context"""

    name: str
    description: str
    domain_model: str
    ubiquitous_language: Dict[str, str] = field(default_factory=dict)
    entities: List[str] = field(default_factory=list)
    value_objects: List[str] = field(default_factory=list)
    aggregates: List[str] = field(default_factory=list)
    domain_services: List[str] = field(default_factory=list)
    repositories: List[str] = field(default_factory=list)
    domain_events: List[str] = field(default_factory=list)

    def validate(self) -> ValidationResult:
        """Validate bounded context"""
        result = ValidationResult(is_valid=True)

        if not self.name:
            result.add_error("Bounded context name cannot be empty")

        if not self.description:
            result.add_warning("Bounded context should have a description")

        if not self.domain_model:
            result.add_error("Bounded context must specify domain model")

        return result


@dataclass
class ContextRelationship:
    """Relationship between two bounded contexts"""

    upstream_context: str
    downstream_context: str
    relationship_type: ContextRelationshipType
    protocol: str
    anti_corruption_layer_required: bool = False
    shared_kernel_elements: List[str] = field(default_factory=list)

    def validate(self) -> ValidationResult:
        """Validate context relationship"""
        result = ValidationResult(is_valid=True)

        if not self.upstream_context:
            result.add_error("Upstream context cannot be empty")

        if not self.downstream_context:
            result.add_error("Downstream context cannot be empty")

        if self.upstream_context == self.downstream_context:
            result.add_error("Context cannot have relationship with itself")

        return result


@dataclass
class ContextMap:
    """Context map showing relationships between bounded contexts"""

    contexts: Dict[str, BoundedContext] = field(default_factory=dict)
    relationships: List[ContextRelationship] = field(default_factory=list)

    def add_context(self, context: BoundedContext):
        """Add a bounded context to the map"""
        self.contexts[context.name] = context

    def add_relationship(self, relationship: ContextRelationship):
        """Add a relationship between contexts"""
        # Validate that both contexts exist
        if relationship.upstream_context not in self.contexts:
            raise ValueError(f"Upstream context '{relationship.upstream_context}' not found")

        if relationship.downstream_context not in self.contexts:
            raise ValueError(f"Downstream context '{relationship.downstream_context}' not found")

        self.relationships.append(relationship)

    def get_upstream_contexts(self, context_name: str) -> List[str]:
        """Get upstream contexts for a given context"""
        upstream = []
        for rel in self.relationships:
            if rel.downstream_context == context_name:
                upstream.append(rel.upstream_context)
        return upstream

    def get_downstream_contexts(self, context_name: str) -> List[str]:
        """Get downstream contexts for a given context"""
        downstream = []
        for rel in self.relationships:
            if rel.upstream_context == context_name:
                downstream.append(rel.downstream_context)
        return downstream

    def validate(self) -> ValidationResult:
        """Validate context map"""
        result = ValidationResult(is_valid=True)

        # Validate all contexts
        for context in self.contexts.values():
            context_result = context.validate()
            if not context_result.is_valid:
                result.errors.extend(context_result.errors)
                result.is_valid = False
            result.warnings.extend(context_result.warnings)

        # Validate all relationships
        for relationship in self.relationships:
            rel_result = relationship.validate()
            if not rel_result.is_valid:
                result.errors.extend(rel_result.errors)
                result.is_valid = False
            result.warnings.extend(rel_result.warnings)

        # Check for circular dependencies
        for context_name in self.contexts:
            if self._has_circular_dependency(context_name, set()):
                result.add_error(f"Circular dependency detected involving context '{context_name}'")

        return result

    def _has_circular_dependency(self, context_name: str, visited: set) -> bool:
        """Check for circular dependencies in context relationships"""
        if context_name in visited:
            return True

        visited.add(context_name)

        # Check downstream contexts
        for downstream in self.get_downstream_contexts(context_name):
            if self._has_circular_dependency(downstream, visited.copy()):
                return True

        return False


class AntiCorruptionLayer:
    """Anti-corruption layer for context integration"""

    def __init__(self, source_context: str, target_context: str):
        self.source_context = source_context
        self.target_context = target_context
        self.translation_rules: Dict[str, str] = {}
        self.validation_rules: List[str] = []

    def add_translation_rule(self, source_term: str, target_term: str):
        """Add translation rule between contexts"""
        self.translation_rules[source_term] = target_term

    def add_validation_rule(self, rule: str):
        """Add validation rule for translated data"""
        self.validation_rules.append(rule)

    def translate(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate data from source context to target context"""
        translated_data = {}

        for key, value in source_data.items():
            if key in self.translation_rules:
                translated_key = self.translation_rules[key]
                translated_data[translated_key] = value
            else:
                # Keep original key if no translation rule
                translated_data[key] = value

        return translated_data

    def validate_translation(self, translated_data: Dict[str, Any]) -> ValidationResult:
        """Validate translated data"""
        result = ValidationResult(is_valid=True)

        # Apply validation rules
        for rule in self.validation_rules:
            # This would implement actual validation logic
            pass

        return result
