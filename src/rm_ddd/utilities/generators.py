"""
RM-DDD Code Generators

Code generation utilities for RM-DDD components.
"""

from typing import Dict, Any, List, Optional
import os


class RMDDDCodeGenerator:
    """Code generator for RM-DDD components"""

    def __init__(self):
        self.templates = self._load_templates()

    def generate_entity(self, entity_name: str, domain_context: str, attributes: List[Dict[str, Any]]) -> str:
        """Generate entity class code"""
        template = self.templates["entity"]
        # Simple string replacement for now
        return template.replace("{{ entity_name }}", entity_name).replace("{{ domain_context }}", domain_context)

    def generate_value_object(self, vo_name: str, attributes: List[Dict[str, Any]]) -> str:
        """Generate value object class code"""
        template = self.templates["value_object"]
        return template.replace("{{ vo_name }}", vo_name)

    def generate_repository_interface(self, entity_name: str, domain_context: str) -> str:
        """Generate repository interface code"""
        template = self.templates["repository_interface"]
        return template.replace("{{ entity_name }}", entity_name).replace("{{ domain_context }}", domain_context)

    def generate_domain_service(self, service_name: str, domain_context: str, methods: List[Dict[str, Any]]) -> str:
        """Generate domain service code"""
        template = self.templates["domain_service"]
        return template.replace("{{ service_name }}", service_name).replace("{{ domain_context }}", domain_context)

    def generate_aggregate_root(self, aggregate_name: str, domain_context: str, entities: List[str], invariants: List[str]) -> str:
        """Generate aggregate root code"""
        template = self.templates["aggregate_root"]
        return template.replace("{{ aggregate_name }}", aggregate_name).replace("{{ domain_context }}", domain_context)

    def generate_domain_event(self, event_name: str, aggregate_name: str, event_data: List[Dict[str, Any]]) -> str:
        """Generate domain event code"""
        template = self.templates["domain_event"]
        return template.replace("{{ event_name }}", event_name).replace("{{ aggregate_name }}", aggregate_name)

    def _load_templates(self) -> Dict[str, str]:
        """Load string templates for code generation"""
        return {
            "entity": ENTITY_TEMPLATE,
            "value_object": VALUE_OBJECT_TEMPLATE,
            "repository_interface": REPOSITORY_INTERFACE_TEMPLATE,
            "domain_service": DOMAIN_SERVICE_TEMPLATE,
            "aggregate_root": AGGREGATE_ROOT_TEMPLATE,
            "domain_event": DOMAIN_EVENT_TEMPLATE,
        }


# Template constants
ENTITY_TEMPLATE = """
from rm_ddd import Entity, domain_entity, ValidationResult
from typing import Optional
from uuid import UUID

@domain_entity("{{ domain_context }}")
class {{ entity_name }}(Entity[UUID]):
    def __init__(self, entity_id: UUID{% for attr in attributes %}, {{ attr.name }}: {{ attr.type }}{% endfor %}):
        super().__init__(entity_id, "{{ domain_context }}")
        {% for attr in attributes %}
        self.{{ attr.name }} = {{ attr.name }}
        {% endfor %}
    
    def get_domain_boundaries(self) -> DomainBoundaries:
        return DomainBoundaries(
            context="{{ domain_context }}",
            bounded_context_rules=["{{ entity_name }} belongs to {{ domain_context }}"]
        )
    
    def validate_domain_invariants(self) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Add domain-specific validation logic here
        {% for attr in attributes %}
        {% if attr.required %}
        if not self.{{ attr.name }}:
            result.add_error("{{ attr.name }} is required")
        {% endif %}
        {% endfor %}
        return result
"""

VALUE_OBJECT_TEMPLATE = """
from rm_ddd import ImmutableValueObject, ValidationResult
from dataclasses import dataclass

@dataclass(frozen=True)
class {{ vo_name }}(ImmutableValueObject):
    {% for attr in attributes %}
    {{ attr.name }}: {{ attr.type }}
    {% endfor %}
    
    def validate(self) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Add validation logic here
        {% for attr in attributes %}
        {% if attr.required %}
        if not self.{{ attr.name }}:
            result.add_error("{{ attr.name }} is required")
        {% endif %}
        {% endfor %}
        return result
"""

REPOSITORY_INTERFACE_TEMPLATE = """
from rm_ddd import RepositoryRM, DomainCriteria
from typing import List, Optional
from uuid import UUID

class {{ entity_name }}Repository(RepositoryRM[{{ entity_name }}, UUID]):
    def __init__(self):
        super().__init__("{{ domain_context }}", "{{ entity_name }}")
    
    async def get_by_id(self, entity_id: UUID) -> Optional[{{ entity_name }}]:
        # Implement repository logic
        pass
    
    async def save(self, entity: {{ entity_name }}) -> {{ entity_name }}:
        # Implement save logic
        pass
    
    async def delete(self, entity_id: UUID) -> bool:
        # Implement delete logic
        pass
    
    async def find_by_criteria(self, criteria: DomainCriteria) -> List[{{ entity_name }}]:
        # Implement query logic
        pass
    
    async def _perform_health_check(self):
        # Implement health check logic
        pass
"""

DOMAIN_SERVICE_TEMPLATE = """
from rm_ddd import DomainService, domain_service, ValidationResult
from typing import List

@domain_service("{{ domain_context }}", stateless=True)
class {{ service_name }}(DomainService):
    def __init__(self):
        super().__init__("{{ domain_context }}", "{{ service_name }}")
    
    {% for method in methods %}
    async def {{ method.name }}(self{% for param in method.parameters %}, {{ param.name }}: {{ param.type }}{% endfor %}) -> {{ method.return_type }}:
        \"\"\"{{ method.description }}\"\"\"
        # Implement business logic
        pass
    
    {% endfor %}
    
    def get_domain_boundaries(self) -> DomainBoundaries:
        return DomainBoundaries(
            context="{{ domain_context }}",
            bounded_context_rules=["{{ service_name }} operates within {{ domain_context }}"]
        )
    
    def validate_domain_invariants(self) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Add validation logic
        return result
"""

AGGREGATE_ROOT_TEMPLATE = """
from rm_ddd import AggregateRoot, aggregate_root, ValidationResult
from typing import List
from uuid import UUID

@aggregate_root("{{ domain_context }}")
class {{ aggregate_name }}(AggregateRoot[UUID]):
    def __init__(self, entity_id: UUID):
        super().__init__(entity_id, "{{ domain_context }}")
        # Initialize aggregate state
    
    def get_domain_boundaries(self) -> DomainBoundaries:
        return DomainBoundaries(
            context="{{ domain_context }}",
            bounded_context_rules=["{{ aggregate_name }} manages {{ domain_context }}"]
        )
    
    def get_aggregate_boundaries(self) -> AggregateBoundaries:
        return AggregateBoundaries(
            aggregate_root="{{ aggregate_name }}",
            internal_entities=[{% for entity in entities %}"{{ entity }}"{% if not loop.last %}, {% endif %}{% endfor %}],
            consistency_rules=[],
            invariants=[{% for invariant in invariants %}"{{ invariant }}"{% if not loop.last %}, {% endif %}{% endfor %}]
        )
    
    def validate_domain_invariants(self) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Validate aggregate invariants
        {% for invariant in invariants %}
        # Check: {{ invariant }}
        {% endfor %}
        return result
"""

DOMAIN_EVENT_TEMPLATE = """
from rm_ddd import DomainEvent
from typing import Dict, Any
from uuid import UUID

class {{ event_name }}(DomainEvent):
    def __init__(self, aggregate_id: UUID{% for data in event_data %}, {{ data.name }}: {{ data.type }}{% endfor %}):
        super().__init__(aggregate_id)
        {% for data in event_data %}
        self.{{ data.name }} = {{ data.name }}
        {% endfor %}
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            {% for data in event_data %}
            '{{ data.name }}': self.{{ data.name }}{% if not loop.last %},{% endif %}
            {% endfor %}
        }
"""
