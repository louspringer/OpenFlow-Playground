#!/usr/bin/env python3
"""
Test Suite: ClassGenerator Refactoring
Tests all refactored ClassGenerator modules in isolation and integration.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import the refactored modules
from src.round_trip_engineering.generators.class_generator import ClassGenerator
from src.round_trip_engineering.generators.class_structure_generator import (
    ClassStructureGenerator,
)
from src.round_trip_engineering.generators.method_validator import MethodValidator
from src.round_trip_engineering.generators.method_processor import MethodCompleter
from src.round_trip_engineering.generators.operational_methods_generator import (
    OperationalMethodsGenerator,
)
from src.round_trip_engineering.generators.base_reflective_module import (
    BaseReflectiveModule,
)


class TestBaseReflectiveModule:
    """Test the BaseReflectiveModule base class."""

    def test_base_module_initialization(self):
        """Test that BaseReflectiveModule initializes correctly."""

        # Create a concrete implementation for testing
        class TestModule(BaseReflectiveModule):
            async def get_module_capabilities(self):
                return [{"name": "test", "description": "Test capability"}]

        module = TestModule()
        assert module._error_count == 0
        assert module._success_count == 0
        assert module._is_operational is True

    def test_operational_state_tracking(self):
        """Test operational state tracking methods."""

        class TestModule(BaseReflectiveModule):
            async def get_module_capabilities(self):
                return [{"name": "test", "description": "Test capability"}]

        module = TestModule()

        # Test success tracking
        module._track_success()
        assert module._success_count == 1
        assert module._get_success_count() == 1

        # Test error tracking
        module._track_error()
        assert module._error_count == 1
        assert module._get_error_count() == 1

        # Test success rate calculation
        success_rate = module._calculate_success_rate()
        assert success_rate == 0.5  # 1 success, 1 error

    @pytest.mark.asyncio
    async def test_module_status_reporting(self):
        """Test module status reporting."""

        class TestModule(BaseReflectiveModule):
            async def get_module_capabilities(self):
                return [{"name": "test", "description": "Test capability"}]

        module = TestModule()
        module._track_success()
        module._track_success()

        status = await module.get_module_status()
        # Fix: Use the actual enum value instead of string comparison
        assert status.status.value == "available"  # ModuleStatus.AVAILABLE.value
        assert status.message == "Module is fully operational"
        assert len(status.capabilities) == 1
        assert status.health_indicators["success_rate"] == 1.0

    @pytest.mark.asyncio
    async def test_health_checking(self):
        """Test health checking methods."""

        class TestModule(BaseReflectiveModule):
            async def get_module_capabilities(self):
                return [{"name": "test", "description": "Test capability"}]

        module = TestModule()

        # Test healthy state
        is_healthy = await module.is_healthy()
        assert is_healthy is True

        # Test unhealthy state
        module._track_error()
        module._track_error()
        is_healthy = await module.is_healthy()
        assert is_healthy is False


class TestClassStructureGenerator:
    """Test the ClassStructureGenerator module."""

    def test_class_structure_generator_initialization(self):
        """Test that ClassStructureGenerator initializes correctly."""
        generator = ClassStructureGenerator()
        assert generator is not None

    def test_generate_class_structure_basic(self):
        """Test basic class structure generation."""
        generator = ClassStructureGenerator()

        enhanced_ast = {"bases": [], "docstring": "Test class"}

        result = generator.generate_class_structure("TestClass", enhanced_ast)

        assert "class TestClass(ReflectiveModule):" in result
        assert '"""\n    Test class\n    """' in result

    def test_generate_class_structure_with_inheritance(self):
        """Test class structure generation with inheritance."""
        generator = ClassStructureGenerator()

        enhanced_ast = {
            "bases": ["BaseClass", "MixinClass"],
            "docstring": "Inheriting class",
        }

        result = generator.generate_class_structure("InheritingClass", enhanced_ast)

        assert "class InheritingClass(BaseClass, MixinClass):" in result
        assert '"""\n    Inheriting class\n    """' in result

    def test_generate_class_structure_without_docstring(self):
        """Test class structure generation without docstring."""
        generator = ClassStructureGenerator()

        enhanced_ast = {"bases": [], "docstring": ""}

        result = generator.generate_class_structure("NoDocClass", enhanced_ast)

        assert "class NoDocClass(ReflectiveModule):" in result
        # Fix: Check for the actual generated docstring format
        assert '"""Generated class NoDocClass"""' in result

    @pytest.mark.asyncio
    async def test_module_capabilities(self):
        """Test module capabilities reporting."""
        generator = ClassStructureGenerator()
        capabilities = await generator.get_module_capabilities()

        assert len(capabilities) == 2
        assert any(cap["name"] == "class_structure_generation" for cap in capabilities)
        assert any(cap["name"] == "reflective_module_interface" for cap in capabilities)


class TestMethodValidator:
    """Test the MethodValidator module."""

    def test_method_validator_initialization(self):
        """Test that MethodValidator initializes correctly."""
        validator = MethodValidator()
        assert validator is not None

    def test_valid_method_source(self):
        """Test validation of valid method source."""
        validator = MethodValidator()

        # Fix: Use proper indentation for the method body as it would appear in a class
        valid_source = """def test_method(self):
    return True"""

        is_valid = validator.is_valid_method_source(valid_source)
        assert is_valid is True

    def test_invalid_method_source_no_def(self):
        """Test validation of invalid method source without 'def'."""
        validator = MethodValidator()

        invalid_source = """test_method(self):
    return True"""

        is_valid = validator.is_valid_method_source(invalid_source)
        assert is_valid is False

    def test_invalid_method_source_bad_indentation(self):
        """Test validation of method source with bad indentation."""
        validator = MethodValidator()

        invalid_source = """def test_method(self):
return True"""  # Bad indentation

        is_valid = validator.is_valid_method_source(invalid_source)
        assert is_valid is False

    def test_async_method_source(self):
        """Test validation of async method source."""
        validator = MethodValidator()

        # Fix: Use proper indentation and complete method body as it would appear in a class
        async_source = """async def async_method(self):
    await asyncio.sleep(0)
    return True"""

        is_valid = validator.is_valid_method_source(async_source)
        assert is_valid is True

    @pytest.mark.asyncio
    async def test_module_capabilities(self):
        """Test module capabilities reporting."""
        validator = MethodValidator()
        capabilities = await validator.get_module_capabilities()

        assert len(capabilities) == 2
        assert any(cap["name"] == "method_validation" for cap in capabilities)
        assert any(cap["name"] == "reflective_module_interface" for cap in capabilities)


class TestMethodCompleter:
    """Test the MethodCompleter module."""

    def test_method_completer_initialization(self):
        """Test that MethodCompleter initializes correctly."""
        completer = MethodCompleter()
        assert completer is not None

    def test_complete_method_source_basic(self):
        """Test basic method source completion."""
        completer = MethodCompleter()

        incomplete_source = """def test_method(self):
    if True:
        return True"""

        completed = completer.complete_method_source(incomplete_source)

        # Should add proper indentation and structure
        assert "def test_method(self):" in completed
        assert "    if True:" in completed
        assert "        return True" in completed

    def test_complete_method_source_with_try_block(self):
        """Test method source completion with try block."""
        completer = MethodCompleter()

        incomplete_source = """def test_method(self):
    try:
        result = self.process_data()
        return result"""

        completed = completer.complete_method_source(incomplete_source)

        # Should complete the try block
        assert "try:" in completed
        assert "except Exception as e:" in completed
        assert "return None" in completed

    def test_complete_method_source_with_dictionary(self):
        """Test method source completion with dictionary."""
        completer = MethodCompleter()

        incomplete_source = """def test_method(self):
    return {
        "status": "success",
        "data": self.get_data()
    }"""

        completed = completer.complete_method_source(incomplete_source)

        # Should preserve the dictionary structure
        assert "return {" in completed
        assert '"status": "success"' in completed
        assert '"data": self.get_data()' in completed

    @pytest.mark.asyncio
    async def test_module_capabilities(self):
        """Test module capabilities reporting."""
        completer = MethodCompleter()
        capabilities = await completer.get_module_capabilities()

        assert len(capabilities) == 2
        assert any(cap["name"] == "method_completion" for cap in capabilities)
        assert any(cap["name"] == "reflective_module_interface" for cap in capabilities)


class TestOperationalMethodsGenerator:
    """Test the OperationalMethodsGenerator module."""

    def test_operational_methods_generator_initialization(self):
        """Test that OperationalMethodsGenerator initializes correctly."""
        generator = OperationalMethodsGenerator()
        assert generator is not None

    def test_generate_operational_methods(self):
        """Test generation of operational methods."""
        generator = OperationalMethodsGenerator()

        methods = generator.generate_operational_methods("TestClass")

        assert "async def get_module_status(self) -> ModuleHealth:" in methods
        assert "async def get_module_capabilities(self) -> List[ModuleCapability]:" in methods
        assert "async def is_healthy(self) -> bool:" in methods
        assert "async def get_health_indicators(self) -> Dict[str, Any]:" in methods
        assert "TestClass" in methods  # Class name should be included

    def test_generate_basic_operational_methods_fallback(self):
        """Test fallback operational methods generation."""
        generator = OperationalMethodsGenerator()

        methods = generator._generate_basic_operational_methods("TestClass")

        assert "async def get_module_status(self) -> ModuleHealth:" in methods
        assert "async def get_module_capabilities(self) -> List[ModuleCapability]:" in methods
        assert "TestClass" in methods

    @pytest.mark.asyncio
    async def test_module_capabilities(self):
        """Test module capabilities reporting."""
        generator = OperationalMethodsGenerator()
        capabilities = await generator.get_module_capabilities()

        assert len(capabilities) == 2
        assert any(cap["name"] == "operational_methods_generation" for cap in capabilities)
        assert any(cap["name"] == "reflective_module_interface" for cap in capabilities)


class TestClassGeneratorIntegration:
    """Test the integrated ClassGenerator with all its components."""

    def test_class_generator_initialization(self):
        """Test that ClassGenerator initializes with all components."""
        generator = ClassGenerator()

        # Check that all component modules are available
        assert hasattr(generator, "class_structure_generator")
        assert hasattr(generator, "method_validator")
        assert hasattr(generator, "method_completer")
        assert hasattr(generator, "operational_methods_generator")

        # Check that components are instances of the right classes
        assert isinstance(generator.class_structure_generator, ClassStructureGenerator)
        assert isinstance(generator.method_validator, MethodValidator)
        assert isinstance(generator.method_completer, MethodCompleter)
        assert isinstance(generator.operational_methods_generator, OperationalMethodsGenerator)

    def test_class_generator_orchestration(self):
        """Test that ClassGenerator properly orchestrates its components."""
        generator = ClassGenerator()

        # Test that the generator can access component capabilities
        assert generator.class_structure_generator is not None
        assert generator.method_validator is not None
        assert generator.method_completer is not None
        assert generator.operational_methods_generator is not None

    @pytest.mark.asyncio
    async def test_integrated_module_capabilities(self):
        """Test that all components report capabilities correctly."""
        generator = ClassGenerator()

        # Test each component's capabilities
        structure_capabilities = await generator.class_structure_generator.get_module_capabilities()
        validator_capabilities = await generator.method_validator.get_module_capabilities()
        completer_capabilities = await generator.method_completer.get_module_capabilities()
        operational_capabilities = await generator.operational_methods_generator.get_module_capabilities()

        # Verify capabilities are reported
        assert len(structure_capabilities) > 0
        assert len(validator_capabilities) > 0
        assert len(completer_capabilities) > 0
        assert len(operational_capabilities) > 0


class TestReflectiveModuleCompliance:
    """Test that all modules comply with ReflectiveModule principles."""

    @pytest.mark.parametrize(
        "module_class",
        [
            ClassStructureGenerator,
            MethodValidator,
            MethodCompleter,
            OperationalMethodsGenerator,
            ClassGenerator,
        ],
    )
    def test_module_size_compliance(self, module_class):
        """Test that all modules are under the 200-line limit."""
        import inspect

        source_lines = inspect.getsource(module_class).split("\n")
        line_count = len(source_lines)

        assert line_count <= 200, f"{module_class.__name__} exceeds 200 lines: {line_count}"

    @pytest.mark.parametrize(
        "module_class",
        [
            ClassStructureGenerator,
            MethodValidator,
            MethodCompleter,
            OperationalMethodsGenerator,
        ],
    )
    def test_module_inheritance_compliance(self, module_class):
        """Test that all modules inherit from BaseReflectiveModule."""
        assert issubclass(module_class, BaseReflectiveModule), f"{module_class.__name__} must inherit from BaseReflectiveModule"

    @pytest.mark.parametrize(
        "module_class",
        [
            ClassStructureGenerator,
            MethodValidator,
            MethodCompleter,
            OperationalMethodsGenerator,
        ],
    )
    @pytest.mark.asyncio
    async def test_module_interface_compliance(self, module_class):
        """Test that all modules implement the required interface methods."""
        module = module_class()

        # Test required methods exist and are callable
        assert hasattr(module, "get_module_status")
        assert hasattr(module, "get_module_capabilities")
        assert hasattr(module, "is_healthy")
        assert hasattr(module, "get_health_indicators")

        # Test methods can be called
        status = await module.get_module_status()
        capabilities = await module.get_module_capabilities()
        health = await module.is_healthy()
        indicators = await module.get_health_indicators()

        # Verify return types are reasonable
        assert status is not None
        assert isinstance(capabilities, list)
        assert isinstance(health, bool)
        assert isinstance(indicators, dict)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
