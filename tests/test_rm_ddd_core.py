"""
Tests for RM-DDD Core Components

Comprehensive test suite for the RM-DDD core functionality.
"""

import pytest
import asyncio
from datetime import datetime
from uuid import uuid4

from src.rm_ddd.core.types import ModuleStatus, ModuleCapability, ModuleHealth, DomainHealth
from src.rm_ddd.core.base import ReflectiveModuleBase, DomainReflectiveModule
from src.rm_ddd.core.registry import ModuleRegistry, get_global_registry
from src.rm_ddd.core.health import HealthMonitor, DomainHealthMonitor
from src.rm_ddd.domain.entities import Entity, AggregateRoot
from src.rm_ddd.domain.value_objects import Money, Email, Address
from src.rm_ddd.domain.events import DomainEvent, DomainEventPublisher
from src.rm_ddd.domain.services import DomainService
from src.rm_ddd.domain.repositories import RepositoryRM, DomainCriteria
from src.rm_ddd.domain.contexts import BoundedContext, ContextMap, ContextRelationship, ContextRelationshipType
from src.rm_ddd.utilities.validators import DomainValidator, RMComplianceValidator


class MockReflectiveModule(ReflectiveModuleBase):
    """Mock implementation for testing"""

    def __init__(self, module_id: str = None):
        super().__init__(module_id)
        self.health_status = ModuleStatus.AVAILABLE
        self.capabilities = [ModuleCapability(name="test_capability", description="Test capability")]
        self.indicators = {"test_indicator": 42}

    async def get_module_status(self) -> ModuleHealth:
        return ModuleHealth(status=self.health_status, message="Mock module", capabilities=self.capabilities, indicators=self.indicators)

    async def get_module_capabilities(self) -> list[ModuleCapability]:
        return self.capabilities

    async def is_healthy(self) -> bool:
        return self.health_status == ModuleStatus.AVAILABLE

    async def get_health_indicators(self) -> dict:
        return self.indicators


class MockDomainModule(DomainReflectiveModule):
    """Mock domain module for testing"""

    def __init__(self, domain_context: str = "test_domain"):
        super().__init__(domain_context)
        self.boundaries = None
        self.health_status = ModuleStatus.AVAILABLE
        self.capabilities = [ModuleCapability(name="test_capability", description="Test capability")]
        self.indicators = {"test_indicator": 42}

    async def get_module_status(self) -> ModuleHealth:
        return ModuleHealth(status=self.health_status, message="Mock domain module", capabilities=self.capabilities, indicators=self.indicators)

    async def get_module_capabilities(self) -> list[ModuleCapability]:
        # Get base capabilities from parent class
        base_capabilities = await super().get_module_capabilities()
        return base_capabilities + self.capabilities

    async def is_healthy(self) -> bool:
        return self.health_status == ModuleStatus.AVAILABLE

    async def get_health_indicators(self) -> dict:
        return self.indicators

    def get_domain_boundaries(self):
        from src.rm_ddd.core.types import DomainBoundaries

        return DomainBoundaries(context=self.domain_context, bounded_context_rules=["Test domain rules"])

    def validate_domain_invariants(self):
        from src.rm_ddd.core.types import ValidationResult

        return ValidationResult(is_valid=True)


class TestModuleTypes:
    """Test module type definitions"""

    def test_module_status_enum(self):
        """Test ModuleStatus enum values"""
        assert ModuleStatus.AVAILABLE == "available"
        assert ModuleStatus.DEGRADED == "degraded"
        assert ModuleStatus.UNAVAILABLE == "unavailable"
        assert ModuleStatus.STARTING == "starting"
        assert ModuleStatus.ERROR == "error"

    def test_module_capability_creation(self):
        """Test ModuleCapability creation"""
        capability = ModuleCapability(name="test_capability", description="Test capability", enabled=True, version="1.0.0")
        assert capability.name == "test_capability"
        assert capability.description == "Test capability"
        assert capability.enabled is True
        assert capability.version == "1.0.0"

    def test_module_health_creation(self):
        """Test ModuleHealth creation"""
        health = ModuleHealth(status=ModuleStatus.AVAILABLE, message="Test health", capabilities=[], indicators={"test": 42})
        assert health.status == ModuleStatus.AVAILABLE
        assert health.message == "Test health"
        assert health.indicators["test"] == 42


class TestReflectiveModuleBase:
    """Test ReflectiveModuleBase functionality"""

    def test_module_initialization(self):
        """Test module initialization"""
        module = MockReflectiveModule()
        assert module.module_id is not None
        assert hasattr(module, "_health_monitor")

    def test_module_id_generation(self):
        """Test module ID generation"""
        module1 = MockReflectiveModule()
        module2 = MockReflectiveModule()
        assert module1.module_id != module2.module_id

    @pytest.mark.asyncio
    async def test_module_status(self):
        """Test module status retrieval"""
        module = MockReflectiveModule()
        status = await module.get_module_status()
        assert isinstance(status, ModuleHealth)
        assert status.status == ModuleStatus.AVAILABLE

    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check functionality"""
        module = MockReflectiveModule()
        is_healthy = await module.is_healthy()
        assert is_healthy is True

        module.health_status = ModuleStatus.DEGRADED
        is_healthy = await module.is_healthy()
        assert is_healthy is False


class TestDomainReflectiveModule:
    """Test DomainReflectiveModule functionality"""

    def test_domain_module_initialization(self):
        """Test domain module initialization"""
        module = MockDomainModule("test_domain")
        assert module.domain_context == "test_domain"
        assert module.module_id is not None

    @pytest.mark.asyncio
    async def test_domain_capabilities(self):
        """Test domain capabilities"""
        module = MockDomainModule("test_domain")
        capabilities = await module.get_module_capabilities()

        # Should include base capabilities plus domain capability
        assert len(capabilities) >= 1
        domain_capability = next((cap for cap in capabilities if "domain_context" in cap.name), None)
        assert domain_capability is not None
        assert domain_capability.description == "Domain context: test_domain"


class TestModuleRegistry:
    """Test ModuleRegistry functionality"""

    @pytest.mark.asyncio
    async def test_registry_initialization(self):
        """Test registry initialization"""
        registry = ModuleRegistry()
        assert registry._by_id == {}
        assert registry._by_name == {}

    @pytest.mark.asyncio
    async def test_module_registration(self):
        """Test module registration"""
        registry = ModuleRegistry()
        module = MockReflectiveModule()

        module_id = await registry.register(module)
        assert module_id is not None
        assert module_id in registry._by_id
        assert registry._by_id[module_id] == module

    @pytest.mark.asyncio
    async def test_module_retrieval(self):
        """Test module retrieval"""
        registry = ModuleRegistry()
        module = MockReflectiveModule()

        module_id = await registry.register(module)
        retrieved_module = await registry.get(module_id)
        assert retrieved_module == module

    @pytest.mark.asyncio
    async def test_health_aggregation(self):
        """Test health aggregation"""
        registry = ModuleRegistry()
        module1 = MockReflectiveModule()
        module2 = MockReflectiveModule()

        await registry.register(module1)
        await registry.register(module2)

        health_status = await registry.health()
        assert len(health_status) == 2

        for module_id, health in health_status.items():
            assert isinstance(health, ModuleHealth)

    @pytest.mark.asyncio
    async def test_system_health(self):
        """Test system health calculation"""
        registry = ModuleRegistry()
        module1 = MockReflectiveModule()
        module2 = MockReflectiveModule()

        await registry.register(module1)
        await registry.register(module2)

        system_health = await registry.get_system_health()
        assert system_health["total_modules"] == 2
        assert system_health["healthy_modules"] == 2
        assert system_health["health_percentage"] == 100.0


class TestHealthMonitor:
    """Test HealthMonitor functionality"""

    def test_health_monitor_initialization(self):
        """Test health monitor initialization"""
        monitor = HealthMonitor("test_module")
        assert monitor.module_name == "test_module"
        assert monitor.indicators == {}

    def test_indicator_management(self):
        """Test health indicator management"""
        monitor = HealthMonitor("test_module")

        monitor.add_indicator("cpu_usage", 75.0, "%", 80.0, 90.0)
        assert "cpu_usage" in monitor.indicators

        indicator = monitor.indicators["cpu_usage"]
        assert indicator.value == 75.0
        assert indicator.unit == "%"
        assert indicator.threshold_warning == 80.0
        assert indicator.threshold_critical == 90.0

    def test_overall_status_calculation(self):
        """Test overall status calculation"""
        monitor = HealthMonitor("test_module")

        # Add healthy indicators
        monitor.add_indicator("cpu_usage", 50.0, "%", 80.0, 90.0)
        monitor.add_indicator("memory_usage", 60.0, "%", 85.0, 95.0)

        status = monitor.get_overall_status()
        assert status == ModuleStatus.AVAILABLE

        # Add degraded indicator
        monitor.add_indicator("disk_usage", 85.0, "%", 80.0, 90.0)
        status = monitor.get_overall_status()
        assert status == ModuleStatus.DEGRADED

        # Add critical indicator
        monitor.add_indicator("error_rate", 95.0, "%", 80.0, 90.0)
        status = monitor.get_overall_status()
        assert status == ModuleStatus.UNAVAILABLE


class TestDomainHealthMonitor:
    """Test DomainHealthMonitor functionality"""

    def test_domain_health_monitor_initialization(self):
        """Test domain health monitor initialization"""
        monitor = DomainHealthMonitor("test_module", "test_domain")
        assert monitor.module_name == "test_module"
        assert monitor.domain_context == "test_domain"
        assert "domain_context" in monitor.indicators

    def test_domain_metrics_update(self):
        """Test domain metrics update"""
        monitor = DomainHealthMonitor("test_module", "test_domain")

        monitor.update_domain_metrics(boundary_integrity=True, invariant_compliance=True, language_consistency=0.95, complexity_score=0.3)

        assert monitor.indicators["boundary_integrity"].value is True
        assert monitor.indicators["invariant_compliance"].value is True
        assert monitor.indicators["language_consistency"].value == 0.95
        assert monitor.indicators["complexity_score"].value == 0.3

    def test_domain_health_retrieval(self):
        """Test domain health retrieval"""
        monitor = DomainHealthMonitor("test_module", "test_domain")

        domain_health = monitor.get_domain_health()
        assert isinstance(domain_health, DomainHealth)
        assert domain_health.domain_context == "test_domain"


class TestValueObjects:
    """Test value object implementations"""

    def test_money_creation(self):
        """Test Money value object creation"""
        money = Money(100.0, "USD")
        assert money.amount == 100.0
        assert money.currency == "USD"

    def test_money_validation(self):
        """Test Money validation"""
        # Valid money
        money = Money(100.0, "USD")
        validation = money.validate()
        assert validation.is_valid

        # Invalid money (negative amount)
        with pytest.raises(ValueError):
            Money(-50.0, "USD")

        # Invalid money (invalid currency)
        with pytest.raises(ValueError):
            Money(100.0, "INVALID")

    def test_money_operations(self):
        """Test Money operations"""
        money1 = Money(100.0, "USD")
        money2 = Money(50.0, "USD")

        result = money1.add(money2)
        assert result.amount == 150.0
        assert result.currency == "USD"

        result = money1.multiply(2.0)
        assert result.amount == 200.0

    def test_email_creation(self):
        """Test Email value object creation"""
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_email_validation(self):
        """Test Email validation"""
        # Valid email
        email = Email("test@example.com")
        validation = email.validate()
        assert validation.is_valid

        # Invalid email
        with pytest.raises(ValueError):
            Email("invalid-email")

    def test_address_creation(self):
        """Test Address value object creation"""
        address = Address(street="123 Main St", city="Anytown", state="CA", zip_code="12345", country="USA")
        assert address.street == "123 Main St"
        assert address.city == "Anytown"


class TestDomainEvents:
    """Test domain event functionality"""

    def test_domain_event_creation(self):
        """Test domain event creation"""

        class TestEvent(DomainEvent):
            def get_event_data(self):
                return {"test": "data"}

        event = TestEvent(uuid4())
        assert event.aggregate_id is not None
        assert event.event_version == 1
        assert event.occurred_at is not None
        assert event.event_type == "TestEvent"

    def test_domain_event_publisher_initialization(self):
        """Test domain event publisher initialization"""
        publisher = DomainEventPublisher("test_domain")
        assert publisher.domain_context == "test_domain"
        assert publisher._handlers == {}

    @pytest.mark.asyncio
    async def test_domain_event_publishing(self):
        """Test domain event publishing"""
        publisher = DomainEventPublisher("test_domain")

        # Create a mock event
        class TestEvent(DomainEvent):
            def get_event_data(self):
                return {"test": "data"}

        event = TestEvent(uuid4())

        # Publish event (no handlers registered)
        await publisher.publish(event)

        # Check that event was recorded
        assert len(publisher._published_events) == 1
        assert publisher._published_events[0] == event


class TestBoundedContexts:
    """Test bounded context functionality"""

    def test_bounded_context_creation(self):
        """Test bounded context creation"""
        context = BoundedContext(name="test_context", description="Test bounded context", domain_model="TestDomain")
        assert context.name == "test_context"
        assert context.description == "Test bounded context"
        assert context.domain_model == "TestDomain"

    def test_bounded_context_validation(self):
        """Test bounded context validation"""
        # Valid context
        context = BoundedContext(name="test_context", description="Test bounded context", domain_model="TestDomain")
        validation = context.validate()
        assert validation.is_valid

        # Invalid context (empty name)
        context = BoundedContext(name="", description="Test bounded context", domain_model="TestDomain")
        validation = context.validate()
        assert not validation.is_valid
        assert "Bounded context name cannot be empty" in validation.errors

    def test_context_map_management(self):
        """Test context map management"""
        context_map = ContextMap()

        context1 = BoundedContext(name="context1", description="First context", domain_model="Domain1")
        context2 = BoundedContext(name="context2", description="Second context", domain_model="Domain2")

        context_map.add_context(context1)
        context_map.add_context(context2)

        assert len(context_map.contexts) == 2
        assert "context1" in context_map.contexts
        assert "context2" in context_map.contexts

    def test_context_relationships(self):
        """Test context relationships"""
        context_map = ContextMap()

        context1 = BoundedContext(name="context1", description="First context", domain_model="Domain1")
        context2 = BoundedContext(name="context2", description="Second context", domain_model="Domain2")

        context_map.add_context(context1)
        context_map.add_context(context2)

        relationship = ContextRelationship(upstream_context="context1", downstream_context="context2", relationship_type=ContextRelationshipType.UPSTREAM_DOWNSTREAM, protocol="HTTP")

        context_map.add_relationship(relationship)

        assert len(context_map.relationships) == 1
        upstream = context_map.get_upstream_contexts("context2")
        assert "context1" in upstream

        downstream = context_map.get_downstream_contexts("context1")
        assert "context2" in downstream


class TestValidators:
    """Test validation functionality"""

    def test_domain_validator_entity_validation(self):
        """Test domain validator entity validation"""

        # Create a mock entity
        class TestEntity(Entity):
            def __init__(self, entity_id):
                super().__init__(entity_id, "test_domain")

            def get_domain_boundaries(self):
                from src.rm_ddd.core.types import DomainBoundaries

                return DomainBoundaries(context="test_domain", bounded_context_rules=["Test rules"])

            def validate_domain_invariants(self):
                from src.rm_ddd.core.types import ValidationResult

                return ValidationResult(is_valid=True)

        entity = TestEntity(uuid4())
        validation = DomainValidator.validate_entity_invariants(entity)
        assert validation.is_valid

    def test_rm_compliance_validator(self):
        """Test RM compliance validator"""
        module = MockReflectiveModule()
        validation = RMComplianceValidator.validate_rm_interface(module)
        assert validation.is_valid

        # Test with missing method
        class IncompleteModule:
            pass

        incomplete_module = IncompleteModule()
        validation = RMComplianceValidator.validate_rm_interface(incomplete_module)
        assert not validation.is_valid
        assert len(validation.errors) > 0


if __name__ == "__main__":
    pytest.main([__file__])
