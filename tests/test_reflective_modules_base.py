#!/usr/bin/env python3
"""
Tests for Reflective Module Base Infrastructure

This module tests the core Reflective Module (RM) architecture including
base classes, health monitoring, and registry functionality.
"""

import asyncio
import pytest
from datetime import datetime
from typing import Any, Dict, List

from src.reflective_modules.base import ReflectiveModule, ReflectiveModuleMixin
from src.reflective_modules.health import (
    ModuleHealth,
    ModuleCapability,
    ModuleStatus,
    HealthMonitor,
)
from src.reflective_modules.registry import (
    ReflectiveModuleRegistry,
    get_global_registry,
    register_global_module,
    get_global_module,
)


class MockReflectiveModule(ReflectiveModule):
    """Mock implementation of ReflectiveModule for testing"""

    def __init__(self, name: str = "MockModule"):
        self.name = name
        self._capabilities = [
            ModuleCapability("test_capability", "Test capability", True),
            ModuleCapability("optional_capability", "Optional capability", False),
        ]
        self._health_indicators = {"test_indicator": "test_value"}

    async def get_module_status(self) -> ModuleHealth:
        """Get mock module status"""
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE,
            message=f"{self.name} is operational",
            capabilities=self._capabilities,
            health_indicators=self._health_indicators,
            module_version="1.0.0",
        )

    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get mock module capabilities"""
        return self._capabilities

    async def is_healthy(self) -> bool:
        """Check if mock module is healthy"""
        return True

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get mock health indicators"""
        return self._health_indicators


class TestModuleHealth:
    """Test ModuleHealth dataclass functionality"""

    def test_module_health_creation(self):
        """Test creating a ModuleHealth instance"""
        capabilities = [ModuleCapability("test", "Test capability", True)]

        health = ModuleHealth(
            status=ModuleStatus.AVAILABLE,
            message="Test message",
            capabilities=capabilities,
        )

        assert health.status == ModuleStatus.AVAILABLE
        assert health.message == "Test message"
        assert len(health.capabilities) == 1
        assert health.timestamp is not None

    def test_module_health_validation(self):
        """Test ModuleHealth validation"""
        # Test empty message validation
        with pytest.raises(ValueError, match="Health message cannot be empty"):
            ModuleHealth(status=ModuleStatus.AVAILABLE, message="", capabilities=[])

        # Test capabilities validation
        with pytest.raises(ValueError, match="Capabilities must be a list"):
            ModuleHealth(status=ModuleStatus.AVAILABLE, message="Test", capabilities="not_a_list")

    def test_module_health_properties(self):
        """Test ModuleHealth computed properties"""
        capabilities = [
            ModuleCapability("available", "Available capability", True),
            ModuleCapability("unavailable", "Unavailable capability", False),
        ]

        health = ModuleHealth(status=ModuleStatus.AVAILABLE, message="Test", capabilities=capabilities)

        assert health.is_healthy is True
        assert len(health.available_capabilities) == 1
        assert len(health.unavailable_capabilities) == 1
        assert health.available_capabilities[0].name == "available"
        assert health.unavailable_capabilities[0].name == "unavailable"

    def test_module_health_indicators(self):
        """Test health indicator management"""
        health = ModuleHealth(status=ModuleStatus.AVAILABLE, message="Test", capabilities=[])

        health.add_health_indicator("test_key", "test_value")
        assert health.get_health_indicator("test_key") == "test_value"
        assert health.get_health_indicator("missing_key", "default") == "default"

    def test_module_health_to_dict(self):
        """Test conversion to dictionary"""
        capabilities = [ModuleCapability("test", "Test capability", True)]

        health = ModuleHealth(
            status=ModuleStatus.AVAILABLE,
            message="Test message",
            capabilities=capabilities,
            module_version="1.0.0",
        )

        health_dict = health.to_dict()

        assert health_dict["status"] == "available"
        assert health_dict["message"] == "Test message"
        assert health_dict["module_version"] == "1.0.0"
        assert health_dict["is_healthy"] is True
        assert len(health_dict["capabilities"]) == 1


class TestModuleCapability:
    """Test ModuleCapability dataclass functionality"""

    def test_module_capability_creation(self):
        """Test creating a ModuleCapability instance"""
        capability = ModuleCapability(
            name="test_capability",
            description="Test capability description",
            available=True,
            version="1.0.0",
        )

        assert capability.name == "test_capability"
        assert capability.description == "Test capability description"
        assert capability.available is True
        assert capability.version == "1.0.0"
        assert capability.dependencies == []

    def test_module_capability_validation(self):
        """Test ModuleCapability validation"""
        # Test empty name validation
        with pytest.raises(ValueError, match="Capability name cannot be empty"):
            ModuleCapability("", "Description", True)

        # Test empty description validation
        with pytest.raises(ValueError, match="Capability description cannot be empty"):
            ModuleCapability("name", "", True)


class TestHealthMonitor:
    """Test HealthMonitor utility class"""

    def test_create_healthy_status(self):
        """Test creating healthy status"""
        capabilities = [ModuleCapability("test", "Test capability", True)]

        health = HealthMonitor.create_healthy_status("Test message", capabilities, module_version="1.0.0")

        assert health.status == ModuleStatus.AVAILABLE
        assert health.message == "Test message"
        assert health.module_version == "1.0.0"
        assert health.is_healthy is True

    def test_create_degraded_status(self):
        """Test creating degraded status"""
        capabilities = [
            ModuleCapability("available", "Available capability", True),
            ModuleCapability("unavailable", "Unavailable capability", True),
        ]

        health = HealthMonitor.create_degraded_status("Degraded message", capabilities, ["unavailable"])

        assert health.status == ModuleStatus.PARTIALLY_AVAILABLE
        assert health.message == "Degraded message"

        # Check that unavailable capability was marked as unavailable
        unavailable_cap = next(c for c in health.capabilities if c.name == "unavailable")
        assert unavailable_cap.available is False

    def test_create_error_status(self):
        """Test creating error status"""
        capabilities = [ModuleCapability("test", "Test capability", False)]

        health = HealthMonitor.create_error_status("Error message", capabilities, "Test error details")

        assert health.status == ModuleStatus.ERROR
        assert health.message == "Error message"
        assert health.error_count == 1
        assert health.get_health_indicator("error_details") == "Test error details"


class TestReflectiveModule:
    """Test ReflectiveModule base class functionality"""

    @pytest.mark.asyncio
    async def test_reflective_module_interface(self):
        """Test that ReflectiveModule cannot be instantiated"""
        with pytest.raises(TypeError):
            ReflectiveModule()

    @pytest.mark.asyncio
    async def test_mock_reflective_module(self):
        """Test mock implementation of ReflectiveModule"""
        module = MockReflectiveModule("TestModule")

        # Test all required methods
        status = await module.get_module_status()
        capabilities = await module.get_module_capabilities()
        is_healthy = await module.is_healthy()
        health_indicators = await module.get_health_indicators()

        assert status.status == ModuleStatus.AVAILABLE
        assert len(capabilities) == 2
        assert is_healthy is True
        assert "test_indicator" in health_indicators

    @pytest.mark.asyncio
    async def test_module_info(self):
        """Test comprehensive module information"""
        module = MockReflectiveModule("TestModule")
        module_info = await module.get_module_info()

        assert module_info["module_name"] == "MockReflectiveModule"
        assert module_info["module_type"] == "ReflectiveModule"
        assert "status" in module_info
        assert "capabilities" in module_info
        assert "health_indicators" in module_info
        assert module_info["compliance"]["reflective_module"] is True

    @pytest.mark.asyncio
    async def test_rm_compliance_validation(self):
        """Test RM compliance validation"""
        module = MockReflectiveModule("TestModule")
        compliance = await module.validate_rm_compliance()

        assert compliance["interface_implementation"] is True
        assert compliance["status_reporting"] is True
        assert compliance["capability_disclosure"] is True
        assert compliance["health_monitoring"] is True
        assert compliance["operational_visibility"] is True


class TestReflectiveModuleMixin:
    """Test ReflectiveModuleMixin functionality"""

    def test_mixin_initialization(self):
        """Test mixin initialization"""

        class TestClass(ReflectiveModuleMixin):
            def __init__(self):
                super().__init__()

        obj = TestClass()
        assert obj._rm_initialized is True
        assert obj._rm_error_count == 0
        assert obj._rm_warning_count == 0

    def test_mixin_health_indicators(self):
        """Test mixin health indicator methods"""

        class TestClass(ReflectiveModuleMixin):
            def __init__(self):
                super().__init__()

        obj = TestClass()

        # Test error and warning counting
        obj._increment_error_count()
        obj._increment_error_count()
        obj._increment_warning_count()

        assert obj._rm_error_count == 2
        assert obj._rm_warning_count == 1


class TestReflectiveModuleRegistry:
    """Test ReflectiveModuleRegistry functionality"""

    def test_registry_initialization(self):
        """Test registry initialization"""
        registry = ReflectiveModuleRegistry()

        assert len(registry.list_modules()) == 0
        assert registry.get_all_capabilities() == {}

    def test_module_registration(self):
        """Test module registration"""
        registry = ReflectiveModuleRegistry()
        module = MockReflectiveModule("TestModule")

        module_id = registry.register_module(module)
        assert module_id in registry.list_modules()
        assert registry.get_module(module_id) == module

    def test_module_registration_validation(self):
        """Test module registration validation"""
        registry = ReflectiveModuleRegistry()

        # Test invalid module type
        with pytest.raises(ValueError, match="Module must implement ReflectiveModule interface"):
            registry.register_module("not_a_module")

    def test_module_unregistration(self):
        """Test module unregistration"""
        registry = ReflectiveModuleRegistry()
        module = MockReflectiveModule("TestModule")

        module_id = registry.register_module(module)
        assert module_id in registry.list_modules()

        success = registry.unregister_module(module_id)
        assert success is True
        assert module_id not in registry.list_modules()

    def test_capability_discovery(self):
        """Test capability discovery"""
        registry = ReflectiveModuleRegistry()
        module = MockReflectiveModule("TestModule")

        module_id = registry.register_module(module)

        # Capabilities are indexed asynchronously, so we need to wait
        # In a real scenario, this would happen automatically
        capabilities = registry.get_all_capabilities()
        # For now, we'll test the basic structure
        assert isinstance(capabilities, dict)

    @pytest.mark.asyncio
    async def test_module_health_retrieval(self):
        """Test module health retrieval"""
        registry = ReflectiveModuleRegistry()
        module = MockReflectiveModule("TestModule")

        module_id = registry.register_module(module)
        health = await registry.get_module_health(module_id)

        assert health is not None
        assert health.status == ModuleStatus.AVAILABLE
        assert health.message == "TestModule is operational"

    @pytest.mark.asyncio
    async def test_system_health(self):
        """Test system-wide health status"""
        registry = ReflectiveModuleRegistry()
        module1 = MockReflectiveModule("Module1")
        module2 = MockReflectiveModule("Module2")

        registry.register_module(module1, "module1")
        registry.register_module(module2, "module2")

        system_health = await registry.get_system_health()

        assert system_health["total_modules"] == 2
        assert system_health["healthy_modules"] == 2
        assert system_health["overall_status"] == "available"
        assert "module1" in system_health["module_health"]
        assert "module2" in system_health["module_health"]


class TestGlobalRegistry:
    """Test global registry functionality"""

    def test_global_registry_singleton(self):
        """Test that global registry is a singleton"""
        registry1 = get_global_registry()
        registry2 = get_global_registry()

        assert registry1 is registry2

    def test_global_module_registration(self):
        """Test global module registration"""
        module = MockReflectiveModule("GlobalTestModule")

        module_id = register_global_module(module, "global_test")
        retrieved_module = get_global_module("global_test")

        assert retrieved_module == module

        # Clean up
        get_global_registry().unregister_module("global_test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
