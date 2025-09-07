"""
RM-DDD Domain Layer

Domain-Driven Design pattern implementations with RM compliance.
"""

from .entities import Entity, AggregateRoot
from .value_objects import ValueObject, ImmutableValueObject
from .services import DomainService
from .repositories import Repository, RepositoryRM
from .events import DomainEvent, DomainEventPublisher, DomainEventHandler
from .contexts import BoundedContext, ContextMap, AntiCorruptionLayer

__all__ = [
    "Entity",
    "AggregateRoot",
    "ValueObject",
    "ImmutableValueObject",
    "DomainService",
    "Repository",
    "RepositoryRM",
    "DomainEvent",
    "DomainEventPublisher",
    "DomainEventHandler",
    "BoundedContext",
    "ContextMap",
    "AntiCorruptionLayer",
]
