"""
RM-DDD (Reflective Module Domain-Driven Design) SDK

The foundational package and comprehensive ecosystem documentation for the entire
Beast Mode systematic development framework. This package serves as both the
reference implementation and the primary entry point for understanding the complete
ecosystem of systematic development tools, patterns, and methodologies.

Core Philosophy: "The Requirements ARE the Solution" - comprehensive requirements
definition becomes the solution architecture itself.
"""

from .core.base import ReflectiveModuleBase, DomainReflectiveModule
from .core.health import ModuleHealth, ModuleStatus, ModuleCapability, DomainHealth
from .core.registry import get_global_registry, ModuleRegistry
from .domain.entities import Entity, AggregateRoot
from .domain.value_objects import ValueObject, ImmutableValueObject
from .domain.services import DomainService
from .domain.repositories import Repository, RepositoryRM
from .domain.events import DomainEvent, DomainEventPublisher
from .domain.contexts import BoundedContext, ContextMap
from .utilities.decorators import domain_entity, aggregate_root, domain_service, ubiquitous_language
from .utilities.validators import DomainValidator, ValidationResult
from .utilities.generators import RMDDDCodeGenerator

__version__ = "0.1.0"
__author__ = "OpenFlow-Playground Team"
__email__ = "team@openflow-playground.com"

__all__ = [
    # Core RM functionality
    "ReflectiveModuleBase",
    "DomainReflectiveModule",
    "ModuleHealth",
    "ModuleStatus",
    "ModuleCapability",
    "DomainHealth",
    "get_global_registry",
    "ModuleRegistry",
    # DDD Pattern implementations
    "Entity",
    "AggregateRoot",
    "ValueObject",
    "ImmutableValueObject",
    "DomainService",
    "Repository",
    "RepositoryRM",
    "DomainEvent",
    "DomainEventPublisher",
    "BoundedContext",
    "ContextMap",
    # Utilities
    "domain_entity",
    "aggregate_root",
    "domain_service",
    "ubiquitous_language",
    "DomainValidator",
    "ValidationResult",
    "RMDDDCodeGenerator",
]
