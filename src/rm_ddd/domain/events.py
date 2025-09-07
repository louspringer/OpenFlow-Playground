"""
RM-DDD Domain Events

Domain event system with RM compliance and health monitoring.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from uuid import UUID, uuid4
import asyncio

from ..core.base import DomainReflectiveModule
from ..core.types import ModuleHealth, ModuleStatus, ModuleCapability, ValidationResult


class DomainEvent(ABC):
    """Base class for domain events"""

    def __init__(self, aggregate_id: Any, event_version: int = 1):
        self.event_id = uuid4()
        self.aggregate_id = aggregate_id
        self.event_version = event_version
        self.occurred_at = datetime.now()
        self.event_type = self.__class__.__name__
        self.correlation_id: Optional[str] = None
        self.causation_id: Optional[str] = None

    @abstractmethod
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "aggregate_id": str(self.aggregate_id),
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "event_data": self.get_event_data(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainEvent":
        """Create event from dictionary"""
        # This would be implemented by subclasses
        raise NotImplementedError("Subclasses must implement from_dict")


class DomainEventHandler(ABC):
    """Base class for domain event handlers"""

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event"""
        pass

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Get the event type this handler processes"""
        pass


class DomainEventPublisher(DomainReflectiveModule):
    """RM-compliant domain event publisher"""

    def __init__(self, domain_context: str):
        super().__init__(domain_context, "domain_event_publisher")
        self._handlers: Dict[str, List[DomainEventHandler]] = {}
        self._published_events: List[DomainEvent] = []
        self._failed_events: List[tuple] = []  # (event, error) tuples

    def subscribe(self, event_type: str, handler: DomainEventHandler):
        """Subscribe handler to event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: DomainEventHandler):
        """Unsubscribe handler from event type"""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass  # Handler not found

    async def publish(self, event: DomainEvent):
        """Publish domain event"""
        handlers = self._handlers.get(event.event_type, [])

        if not handlers:
            # No handlers registered, but still record the event
            self._published_events.append(event)
            return

        # Publish to all handlers
        tasks = []
        for handler in handlers:
            task = asyncio.create_task(self._handle_event(handler, event))
            tasks.append(task)

        # Wait for all handlers to complete
        await asyncio.gather(*tasks, return_exceptions=True)

        # Record published event
        self._published_events.append(event)

    async def _handle_event(self, handler: DomainEventHandler, event: DomainEvent):
        """Handle event with error tracking"""
        try:
            await handler.handle(event)
        except Exception as e:
            # Record failed event handling
            self._failed_events.append((event, e))
            # Log error but continue with other handlers
            await self._log_handler_error(handler, event, e)

    async def _log_handler_error(self, handler: DomainEventHandler, event: DomainEvent, error: Exception):
        """Log handler error for debugging"""
        # In a real implementation, this would use proper logging
        print(f"Error in handler {handler.__class__.__name__} for event {event.event_type}: {error}")

    async def get_module_status(self) -> ModuleHealth:
        """Get publisher health status"""
        is_healthy = await self.is_healthy()
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if is_healthy else ModuleStatus.DEGRADED,
            message=f"Domain event publisher for {self.domain_context}",
            capabilities=await self.get_module_capabilities(),
            indicators=await self.get_health_indicators(),
        )

    async def is_healthy(self) -> bool:
        """Check if publisher is healthy"""
        # Consider unhealthy if there are too many failed events
        failure_rate = len(self._failed_events) / max(len(self._published_events), 1)
        return failure_rate < 0.1  # Less than 10% failure rate

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get publisher health indicators"""
        return {
            "registered_handlers": len(self._handlers),
            "event_types": list(self._handlers.keys()),
            "total_events_published": len(self._published_events),
            "failed_events": len(self._failed_events),
            "failure_rate": len(self._failed_events) / max(len(self._published_events), 1),
            "domain_context": self.domain_context,
        }

    def get_domain_boundaries(self) -> "DomainBoundaries":
        """Get domain boundaries for event publisher"""
        from ..core.types import DomainBoundaries

        return DomainBoundaries(context=self.domain_context, bounded_context_rules=[f"Event publisher for {self.domain_context}", "Handles domain events within bounded context"])

    def validate_domain_invariants(self) -> ValidationResult:
        """Validate event publisher invariants"""
        result = ValidationResult(is_valid=True)

        # Check that handlers are properly registered
        for event_type, handlers in self._handlers.items():
            if not handlers:
                result.add_warning(f"No handlers registered for event type: {event_type}")

        # Check failure rate
        if self._published_events:
            failure_rate = len(self._failed_events) / len(self._published_events)
            if failure_rate > 0.1:
                result.add_error(f"High failure rate: {failure_rate:.2%}")

        return result


class EventStore(ABC):
    """Abstract event store interface"""

    @abstractmethod
    async def save_events(self, aggregate_id: str, events: List[DomainEvent], expected_version: int) -> None:
        """Save events for an aggregate"""
        pass

    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Get events for an aggregate"""
        pass

    @abstractmethod
    async def get_events_by_type(self, event_type: str, from_date: Optional[datetime] = None) -> List[DomainEvent]:
        """Get events by type"""
        pass


class InMemoryEventStore(EventStore):
    """In-memory event store implementation"""

    def __init__(self):
        self._events: Dict[str, List[DomainEvent]] = {}
        self._events_by_type: Dict[str, List[DomainEvent]] = {}

    async def save_events(self, aggregate_id: str, events: List[DomainEvent], expected_version: int) -> None:
        """Save events for an aggregate"""
        if aggregate_id not in self._events:
            self._events[aggregate_id] = []

        # Check version for optimistic concurrency
        current_version = len(self._events[aggregate_id])
        if current_version != expected_version:
            raise ValueError(f"Version mismatch: expected {expected_version}, got {current_version}")

        # Add events
        self._events[aggregate_id].extend(events)

        # Index by event type
        for event in events:
            event_type = event.event_type
            if event_type not in self._events_by_type:
                self._events_by_type[event_type] = []
            self._events_by_type[event_type].append(event)

    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Get events for an aggregate"""
        events = self._events.get(aggregate_id, [])
        return events[from_version:]

    async def get_events_by_type(self, event_type: str, from_date: Optional[datetime] = None) -> List[DomainEvent]:
        """Get events by type"""
        events = self._events_by_type.get(event_type, [])

        if from_date:
            events = [e for e in events if e.occurred_at >= from_date]

        return events
