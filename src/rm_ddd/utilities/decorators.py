"""
RM-DDD Decorators

Decorators for domain modeling and validation.
"""

from functools import wraps
from typing import Callable, Any, Dict, List
import inspect

from ..domain.entities import Entity, AggregateRoot
from ..domain.services import DomainService
from ..core.types import ValidationResult


def domain_entity(domain_context: str):
    """Decorator for domain entities"""

    def decorator(cls):
        if not issubclass(cls, Entity):
            raise TypeError("@domain_entity can only be applied to Entity subclasses")

        cls._domain_context = domain_context
        cls._is_domain_entity = True

        # Add automatic validation
        original_init = cls.__init__

        @wraps(original_init)
        def enhanced_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            validation_result = self.validate_domain_invariants()
            if not validation_result.is_valid:
                raise ValueError(f"Domain invariant violation: {validation_result.errors}")

        cls.__init__ = enhanced_init
        return cls

    return decorator


def aggregate_root(domain_context: str, max_size: int = 100):
    """Decorator for aggregate roots"""

    def decorator(cls):
        if not issubclass(cls, AggregateRoot):
            raise TypeError("@aggregate_root can only be applied to AggregateRoot subclasses")

        cls._domain_context = domain_context
        cls._max_aggregate_size = max_size
        cls._is_aggregate_root = True

        # Add size validation
        original_init = cls.__init__

        @wraps(original_init)
        def enhanced_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self._validate_aggregate_size()

        cls.__init__ = enhanced_init

        # Add size validation method
        def _validate_aggregate_size(self):
            """Validate aggregate size constraints"""
            # This would check actual aggregate size in a real implementation
            pass

        cls._validate_aggregate_size = _validate_aggregate_size
        return cls

    return decorator


def domain_service(domain_context: str, stateless: bool = True):
    """Decorator for domain services"""

    def decorator(cls):
        if not issubclass(cls, DomainService):
            raise TypeError("@domain_service can only be applied to DomainService subclasses")

        cls._domain_context = domain_context
        cls._is_stateless = stateless
        cls._is_domain_service = True

        if stateless:
            # Add validation to ensure no instance variables are modified
            cls = _add_stateless_validation(cls)

        return cls

    return decorator


def ubiquitous_language(term_mapping: Dict[str, str]):
    """Decorator to enforce ubiquitous language"""

    def decorator(cls):
        cls._ubiquitous_language_mapping = term_mapping

        # Validate class and method names against mapping
        _validate_ubiquitous_language(cls, term_mapping)

        return cls

    return decorator


def _add_stateless_validation(cls):
    """Add stateless validation to a class"""
    original_init = cls.__init__

    def enhanced_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self._initial_state = self._capture_state()

    def _capture_state(self):
        """Capture initial state for stateless validation"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def _validate_stateless(self):
        """Validate that the service remains stateless"""
        current_state = self._capture_state()
        if current_state != self._initial_state:
            raise ValueError("Domain service must remain stateless")

    cls.__init__ = enhanced_init
    cls._capture_state = _capture_state
    cls._validate_stateless = _validate_stateless

    # Wrap all public methods to validate statelessness
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("_") and name != "__init__":
            setattr(cls, name, _wrap_with_stateless_validation(method))

    return cls


def _wrap_with_stateless_validation(method):
    """Wrap a method with stateless validation"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self._validate_stateless()
        return result

    return wrapper


def _validate_ubiquitous_language(cls, term_mapping: Dict[str, str]):
    """Validate ubiquitous language usage in a class"""
    class_name = cls.__name__

    # Check class name
    if class_name.lower() not in [term.lower() for term in term_mapping.values()]:
        print(f"Warning: Class name '{class_name}' not found in ubiquitous language mapping")

    # Check method names
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("_"):
            if name.lower() not in [term.lower() for term in term_mapping.values()]:
                print(f"Warning: Method name '{name}' not found in ubiquitous language mapping")


def validate_domain_invariants(func: Callable) -> Callable:
    """Decorator to validate domain invariants before method execution"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "validate_domain_invariants"):
            validation_result = self.validate_domain_invariants()
            if not validation_result.is_valid:
                raise ValueError(f"Domain invariant violation: {validation_result.errors}")

        return func(self, *args, **kwargs)

    return wrapper


def track_domain_events(func: Callable) -> Callable:
    """Decorator to track domain events in aggregate methods"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "get_domain_events"):
            initial_events = len(self.get_domain_events())
            result = func(self, *args, **kwargs)
            final_events = len(self.get_domain_events())

            if final_events > initial_events:
                # Events were added, could trigger event publishing
                pass

            return result
        else:
            return func(self, *args, **kwargs)

    return wrapper


def enforce_aggregate_boundaries(func: Callable) -> Callable:
    """Decorator to enforce aggregate boundaries"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "get_aggregate_boundaries"):
            boundaries = self.get_aggregate_boundaries()
            # Validate that the operation is within aggregate boundaries
            # This would be implemented based on specific business rules
            pass

        return func(self, *args, **kwargs)

    return wrapper
