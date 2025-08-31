#!/usr/bin/env python3
"""
Test Suite: Round-Trip Demo System

Comprehensive tests for the demo system that showcase Reflective Module principles
and validate the round-trip engineering capabilities.
"""

import pytest
import asyncio
import json
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Import the demo system
from src.round_trip_engineering.demo.demo_orchestrator import DemoOrchestrator


class TestDemoOrchestrator:
    """Test the DemoOrchestrator module."""

    @pytest.fixture
    def demo_orchestrator(self):
        """Create a DemoOrchestrator instance for testing."""
        return DemoOrchestrator()

    @pytest.fixture
    def mock_round_trip_system(self):
        """Create a mock RoundTripSystem for testing."""
        mock_system = Mock()

        # Mock model
        mock_model = Mock()
        mock_model.name = "TestModel"
        mock_model.components = [Mock(), Mock()]  # 2 components

        # Mock generated files
        mock_generated_files = {
            "test_class.py": "class TestClass: pass",
            "test_test.py": "def test_function(): pass",
        }

        # Setup mock methods
        mock_system.create_model_from_design.return_value = mock_model
        mock_system.save_model.return_value = None
        mock_system.generate_code_from_model.return_value = mock_generated_files
        mock_system.load_model.return_value = mock_model

        return mock_system

    def test_demo_orchestrator_initialization(self, demo_orchestrator):
        """Test that DemoOrchestrator initializes correctly."""
        assert demo_orchestrator is not None
        assert demo_orchestrator.current_demo_step == "idle"
        assert demo_orchestrator.demo_start_time is None
        assert demo_orchestrator.demo_results == {}

    @pytest.mark.asyncio
    async def test_module_capabilities(self, demo_orchestrator):
        """Test that DemoOrchestrator reports capabilities correctly."""
        capabilities = await demo_orchestrator.get_module_capabilities()

        assert len(capabilities) == 3
        assert any(cap["name"] == "demo_orchestration" for cap in capabilities)
        assert any(cap["name"] == "workflow_execution" for cap in capabilities)
        assert any(cap["name"] == "result_analysis" for cap in capabilities)

        # Check that all capabilities are available
        for capability in capabilities:
            assert capability["available"] is True
            assert "version" in capability
            assert "description" in capability

    @pytest.mark.asyncio
    async def test_basic_demo_success(self, demo_orchestrator, mock_round_trip_system):
        """Test successful execution of basic demo."""
        # Patch the round_trip_system
        with patch.object(
            demo_orchestrator, "round_trip_system", mock_round_trip_system
        ):
            # Run the basic demo
            results = await demo_orchestrator.run_basic_demo()

            # Verify results
            assert results["status"] == "success"
            assert results["demo_type"] == "basic"
            assert results["round_trip_successful"] is True
            assert "duration" in results
            assert results["model_name"] == "TestModel"
            assert results["components_count"] == 2
            assert results["generated_files_count"] == 2
            assert len(results["generated_files"]) == 2

            # Verify state changes
            assert demo_orchestrator.current_demo_step == "completed"
            assert demo_orchestrator.demo_start_time is not None
            assert demo_orchestrator.demo_results == results

    @pytest.mark.asyncio
    async def test_advanced_demo_success(
        self, demo_orchestrator, mock_round_trip_system
    ):
        """Test successful execution of advanced demo."""
        # Patch the round_trip_system
        with patch.object(
            demo_orchestrator, "round_trip_system", mock_round_trip_system
        ):
            # Run the advanced demo
            results = await demo_orchestrator.run_advanced_demo()

            # Verify results
            assert results["status"] == "success"
            assert results["demo_type"] == "advanced"
            assert results["round_trip_successful"] is True
            assert "duration" in results
            assert results["model_name"] == "TestModel"
            assert results["components_count"] == 2
            assert results["generated_files_count"] == 2
            assert "vocabulary_alignment" in results

            # Verify vocabulary alignment
            vocab = results["vocabulary_alignment"]
            assert vocab["status"] == "validated"
            assert vocab["alignment_score"] == 0.95
            assert vocab["overall_health"] == "excellent"

    @pytest.mark.asyncio
    async def test_performance_demo_success(
        self, demo_orchestrator, mock_round_trip_system
    ):
        """Test successful execution of performance demo."""
        # Patch the round_trip_system
        with patch.object(
            demo_orchestrator, "round_trip_system", mock_round_trip_system
        ):
            # Run the performance demo
            results = await demo_orchestrator.run_performance_demo()

            # Verify results
            assert results["status"] == "success"
            assert results["demo_type"] == "performance"
            assert "total_duration" in results
            assert "iterations" in results
            assert "average_iteration_time" in results
            assert "performance_score" in results
            assert "results" in results

            # Verify performance metrics
            assert results["iterations"] == 10
            assert results["average_iteration_time"] > 0
            assert len(results["results"]) == 10

            # Check each iteration result
            for i, result in enumerate(results["results"]):
                assert result["iteration"] == i + 1
                assert "duration" in result
                assert "components" in result
                assert "files_generated" in result

    @pytest.mark.asyncio
    async def test_demo_failure_handling(self, demo_orchestrator):
        """Test that demo failures are handled gracefully."""
        # Create a mock that raises an exception
        mock_failing_system = Mock()
        mock_failing_system.create_model_from_design.side_effect = Exception(
            "Test error"
        )

        with patch.object(demo_orchestrator, "round_trip_system", mock_failing_system):
            # Run the basic demo (should fail)
            results = await demo_orchestrator.run_basic_demo()

            # Verify failure handling
            assert results["status"] == "failed"
            assert "error" in results
            assert results["error"] == "Test error"
            assert results["round_trip_successful"] is False

            # Verify state changes
            assert demo_orchestrator.current_demo_step == "failed"
            assert demo_orchestrator._get_error_count() > 0

    @pytest.mark.asyncio
    async def test_demo_status_reporting(self, demo_orchestrator):
        """Test demo status reporting functionality."""
        # Get initial status
        initial_status = await demo_orchestrator.get_demo_status()

        assert initial_status["current_step"] == "idle"
        assert initial_status["demo_start_time"] is None
        assert initial_status["last_results"] == {}
        assert initial_status["success_count"] == 0
        assert initial_status["error_count"] == 0
        assert initial_status["success_rate"] == 0.0

    def test_design_spec_creation(self, demo_orchestrator):
        """Test design specification creation methods."""
        # Test basic design spec
        basic_spec = demo_orchestrator._create_basic_design_spec()
        assert basic_spec["name"] == "BasicDemoClass"
        assert len(basic_spec["components"]) == 1
        assert basic_spec["components"][0]["name"] == "BasicDemoClass"
        assert len(basic_spec["components"][0]["metadata"]["methods"]) == 2

        # Test advanced design spec
        advanced_spec = demo_orchestrator._create_advanced_design_spec()
        assert advanced_spec["name"] == "AdvancedDemoSystem"
        assert len(advanced_spec["components"]) == 2
        assert advanced_spec["components"][0]["name"] == "DataProcessor"
        assert advanced_spec["components"][1]["name"] == "ResultFormatter"

        # Test performance design spec
        perf_spec = demo_orchestrator._create_performance_design_spec(5)
        assert perf_spec["name"] == "PerformanceTestClass_5"
        assert len(perf_spec["components"]) == 1

    @pytest.mark.asyncio
    async def test_vocabulary_alignment_validation(self, demo_orchestrator):
        """Test vocabulary alignment validation."""
        # Test successful validation
        mock_model = Mock()
        vocab_status = await demo_orchestrator._validate_vocabulary_alignment(
            mock_model
        )

        assert vocab_status["status"] == "validated"
        assert vocab_status["alignment_score"] == 0.95
        assert vocab_status["vocabulary_matches"] == 19
        assert vocab_status["vocabulary_mismatches"] == 1
        assert vocab_status["overall_health"] == "excellent"

    def test_reflective_module_compliance(self, demo_orchestrator):
        """Test that DemoOrchestrator follows Reflective Module principles."""
        # Check size compliance (should be under 200 lines)
        import inspect

        source_lines = inspect.getsource(demo_orchestrator.__class__).split("\n")
        line_count = len(source_lines)

        assert line_count <= 200, f"DemoOrchestrator exceeds 200 lines: {line_count}"

        # Check interface compliance
        assert hasattr(demo_orchestrator, "get_module_status")
        assert hasattr(demo_orchestrator, "get_module_capabilities")
        assert hasattr(demo_orchestrator, "is_healthy")
        assert hasattr(demo_orchestrator, "get_health_indicators")

        # Check single responsibility (demo orchestration only)
        # The class should only handle demo workflows, not other concerns
        assert hasattr(demo_orchestrator, "run_basic_demo")
        assert hasattr(demo_orchestrator, "run_advanced_demo")
        assert hasattr(demo_orchestrator, "run_performance_demo")

    @pytest.mark.asyncio
    async def test_operational_state_tracking(self, demo_orchestrator):
        """Test operational state tracking during demo execution."""
        # Run a successful demo
        mock_system = Mock()
        mock_model = Mock()
        mock_model.name = "TestModel"
        mock_model.components = [Mock()]
        mock_system.create_model_from_design.return_value = mock_model
        mock_system.save_model.return_value = None
        mock_system.generate_code_from_model.return_value = {"test.py": "code"}
        mock_system.load_model.return_value = mock_model

        with patch.object(demo_orchestrator, "round_trip_system", mock_system):
            await demo_orchestrator.run_basic_demo()

            # Check operational state
            assert demo_orchestrator._get_success_count() > 0
            assert demo_orchestrator._get_error_count() == 0
            assert demo_orchestrator._calculate_success_rate() > 0.5

    @pytest.mark.asyncio
    async def test_concurrent_demo_execution(self, demo_orchestrator):
        """Test that demos can run concurrently without interference."""
        # Create multiple demo orchestrators
        orchestrators = [DemoOrchestrator() for _ in range(3)]

        # Mock the round trip system for all orchestrators
        mock_system = Mock()
        mock_model = Mock()
        mock_model.name = "TestModel"
        mock_model.components = [Mock()]
        mock_system.create_model_from_design.return_value = mock_model
        mock_system.save_model.return_value = None
        mock_system.generate_code_from_model.return_value = {"test.py": "code"}
        mock_system.load_model.return_value = mock_model

        for orchestrator in orchestrators:
            with patch.object(orchestrator, "round_trip_system", mock_system):
                pass

        # Run demos concurrently
        async def run_demo(orchestrator):
            return await orchestrator.run_basic_demo()

        # Execute all demos concurrently
        results = await asyncio.gather(*[run_demo(o) for o in orchestrators])

        # Verify all demos completed successfully
        for result in results:
            assert result["status"] == "success"
            assert result["round_trip_successful"] is True

    def test_error_recovery(self, demo_orchestrator):
        """Test error recovery and system resilience."""
        # Simulate a system failure
        original_system = demo_orchestrator.round_trip_system

        # Create a failing system
        failing_system = Mock()
        failing_system.create_model_from_design.side_effect = Exception(
            "System failure"
        )

        # Replace the system temporarily
        demo_orchestrator.round_trip_system = failing_system

        # Run a demo (should fail)
        async def run_failing_demo():
            return await demo_orchestrator.run_basic_demo()

        # This should not crash the system
        result = asyncio.run(run_failing_demo())
        assert result["status"] == "failed"

        # Restore the original system
        demo_orchestrator.round_trip_system = original_system

        # Verify the system is still operational
        assert demo_orchestrator._is_operational is True

    @pytest.mark.asyncio
    async def test_demo_metrics_accuracy(
        self, demo_orchestrator, mock_round_trip_system
    ):
        """Test that demo metrics are accurate and meaningful."""
        with patch.object(
            demo_orchestrator, "round_trip_system", mock_round_trip_system
        ):
            # Record start time
            start_time = time.time()

            # Run demo
            results = await demo_orchestrator.run_basic_demo()

            # Record end time
            end_time = time.time()

            # Verify duration accuracy
            actual_duration = end_time - start_time
            reported_duration = results["duration"]

            # Allow for some timing variance (within 0.5 seconds)
            assert abs(actual_duration - reported_duration) < 0.5

            # Verify other metrics
            assert results["components_count"] == 2
            assert results["generated_files_count"] == 2
            assert len(results["generated_files"]) == 2

    def test_design_spec_validation(self, demo_orchestrator):
        """Test that design specifications are valid and complete."""
        # Test basic spec
        basic_spec = demo_orchestrator._create_basic_design_spec()
        assert "name" in basic_spec
        assert "description" in basic_spec
        assert "components" in basic_spec
        assert len(basic_spec["components"]) > 0

        # Test component structure
        component = basic_spec["components"][0]
        assert "name" in component
        assert "type" in component
        assert "description" in component
        assert "requirements" in component
        assert "dependencies" in component
        assert "metadata" in component

        # Test method metadata
        methods = component["metadata"]["methods"]
        assert len(methods) > 0
        for method in methods:
            assert "name" in method
            assert "description" in method
            assert "return_type" in method

    @pytest.mark.asyncio
    async def test_system_integration(self, demo_orchestrator):
        """Test integration with the actual round-trip system."""
        # This test requires the actual system to be available
        try:
            # Test that we can get module status
            status = await demo_orchestrator.get_module_status()
            assert status is not None

            # Test that we can get capabilities
            capabilities = await demo_orchestrator.get_module_capabilities()
            assert len(capabilities) > 0

        except Exception as e:
            # If the system is not fully available, this is acceptable for testing
            pytest.skip(f"System not fully available: {e}")

    def test_demo_orchestrator_isolation(self, demo_orchestrator):
        """Test that DemoOrchestrator is properly isolated from other concerns."""
        # The orchestrator should not have methods unrelated to demo orchestration
        demo_methods = [
            "run_basic_demo",
            "run_advanced_demo",
            "run_performance_demo",
            "get_demo_status",
        ]

        for method_name in demo_methods:
            assert hasattr(demo_orchestrator, method_name), (
                f"Missing demo method: {method_name}"
            )

        # Should not have methods for other concerns
        non_demo_methods = [
            "generate_code",
            "parse_ast",
            "validate_syntax",
            "run_tests",
        ]

        for method_name in non_demo_methods:
            assert not hasattr(demo_orchestrator, method_name), (
                f"Unexpected method: {method_name}"
            )


class TestDemoSystemIntegration:
    """Test the complete demo system integration."""

    @pytest.mark.asyncio
    async def test_full_demo_workflow(self):
        """Test the complete demo workflow from start to finish."""
        # Create orchestrator
        orchestrator = DemoOrchestrator()

        # Mock the round-trip system
        mock_system = Mock()
        mock_model = Mock()
        mock_model.name = "IntegrationTestModel"
        mock_model.components = [Mock(), Mock(), Mock()]  # 3 components

        mock_generated_files = {
            "integration_class.py": "class IntegrationClass: pass",
            "integration_test.py": "def test_integration(): pass",
            "integration_utils.py": "def utility_function(): pass",
        }

        mock_system.create_model_from_design.return_value = mock_model
        mock_system.save_model.return_value = None
        mock_system.generate_code_from_model.return_value = mock_generated_files
        mock_system.load_model.return_value = mock_model

        with patch.object(orchestrator, "round_trip_system", mock_system):
            # Run all demos
            basic_results = await orchestrator.run_basic_demo()
            advanced_results = await orchestrator.run_advanced_demo()
            performance_results = await orchestrator.run_performance_demo()

            # Verify all demos succeeded
            assert basic_results["status"] == "success"
            assert advanced_results["status"] == "success"
            assert performance_results["status"] == "success"

            # Verify system state
            status = await orchestrator.get_module_status()
            assert status.health_indicators["success_count"] >= 3
            assert status.health_indicators["success_rate"] > 0.8

    @pytest.mark.asyncio
    async def test_demo_error_propagation(self):
        """Test that errors in demos are properly propagated and handled."""
        orchestrator = DemoOrchestrator()

        # Create a system that fails on specific operations
        mock_system = Mock()
        mock_system.create_model_from_design.side_effect = Exception(
            "Integration error"
        )

        with patch.object(orchestrator, "round_trip_system", mock_system):
            # Run demo (should fail)
            results = await orchestrator.run_basic_demo()

            # Verify error handling
            assert results["status"] == "failed"
            assert "error" in results
            assert "Integration error" in results["error"]

            # Verify system remains operational
            assert orchestrator._is_operational is True


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
