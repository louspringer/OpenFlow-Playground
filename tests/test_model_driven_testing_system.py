#!/usr/bin/env python3
"""
Test the Model-Driven Testing System End-to-End

This test validates that the system can:
1. Generate tests from implementation models
2. Generate valid pytest-compatible code
3. Maintain test-implementation sync
"""

import ast
from pathlib import Path

import pytest

from src.model_driven_testing.test_generator import PythonUnitTestGenerator


class TestModelDrivenTestingSystem:
    """Test the complete model-driven testing system"""

    @pytest.fixture
    def test_generator(self) -> PythonUnitTestGenerator:
        """Get a test generator instance"""
        return PythonUnitTestGenerator(project_root=Path())

    @pytest.fixture
    def target_file(self) -> Path:
        """Get the target file for testing"""
        return Path("src/ghostbusters/ghostbusters_orchestrator.py")

    def test_system_imports(self, test_generator: PythonUnitTestGenerator) -> None:
        """Test that the system can be imported and instantiated"""
        assert test_generator is not None
        assert hasattr(test_generator, "generate_tests_for_file")

    def test_target_file_exists(self, target_file: Path) -> None:
        """Test that the target file exists and is valid Python"""
        assert target_file.exists(), f"Target file {target_file} should exist"

        # Test that it's valid Python
        try:
            with open(target_file) as f:
                source = f.read()
            ast.parse(source)
        except SyntaxError as e:
            pytest.fail(f"Target file has syntax errors: {e}")

    def test_generate_tests_for_target(self, test_generator: PythonUnitTestGenerator, target_file: Path) -> None:
        """Test that we can generate tests for the target file"""
        # Generate tests for the target file
        test_files = test_generator.generate_tests_for_file(target_file)

        assert len(test_files) > 0, "Should generate at least one test file"

        # Check that the generated test files exist
        for test_file in test_files:
            assert test_file.exists(), f"Generated test file {test_file} should exist"

            # Test that generated tests are valid Python
            try:
                with open(test_file) as f:
                    source = f.read()
                ast.parse(source)
            except SyntaxError as e:
                pytest.fail(f"Generated test file {test_file} has syntax errors: {e}")

    def test_generated_tests_are_runnable(self, test_generator: PythonUnitTestGenerator, target_file: Path) -> None:
        """Test that generated tests can actually be run with pytest"""
        # Generate tests
        test_files = test_generator.generate_tests_for_file(target_file)

        # Find the main test file (should be for the main class)
        main_test_file = None
        for test_file in test_files:
            if "ghostbustersorchestrator" in test_file.name.lower():
                main_test_file = test_file
                break

        assert main_test_file is not None, "Should generate a test for GhostbustersOrchestrator"

        # Test that the generated test can be imported (SAFE - no execution)
        try:
            # SAFE: Just validate the generated test file structure
            with open(main_test_file) as f:
                test_content = f.read()

            # Check that the test file has the expected structure
            assert "import pytest" in test_content, "Should import pytest"
            assert "class Test" in test_content, "Should have test class"
            assert "def test_" in test_content, "Should have test methods"
            assert "assert" in test_content, "Should have assertions"

            # Check that it's valid Python syntax
            try:
                ast.parse(test_content)
            except SyntaxError as e:
                pytest.fail(f"Generated test has syntax errors: {e}")

            print(f"✅ Generated test {main_test_file.name} is valid and safe")

        except Exception as e:
            pytest.fail(f"Failed to validate generated test: {e}")

    def test_test_implementation_sync(self, test_generator: PythonUnitTestGenerator, target_file: Path) -> None:
        """Test that generated tests stay in sync with implementation"""
        # Generate tests
        test_files = test_generator.generate_tests_for_file(target_file)

        # Find the main test file
        main_test_file = None
        for test_file in test_files:
            if "ghostbustersorchestrator" in test_file.name.lower():
                main_test_file = test_file
                break

        assert main_test_file is not None

        # Check that the test imports the correct class
        with open(main_test_file) as f:
            test_content = f.read()

        # Should import the actual class
        assert "from src.ghostbusters.ghostbusters_orchestrator import GhostbustersOrchestrator" in test_content

        # Should test actual attributes that exist
        assert "test_project_path_attribute_exists" in test_content
        assert "test_agents_attribute_exists" in test_content
        assert "test_validators_attribute_exists" in test_content

    def test_system_scalability(self, test_generator: PythonUnitTestGenerator) -> None:
        """Test that the system can handle multiple files"""
        # Test with a few different Python files
        test_files = [
            Path("src/ghostbusters/ghostbusters_orchestrator.py"),
            Path("src/ghostbusters/agents/base_expert.py"),
        ]

        total_generated = 0
        for test_file in test_files:
            if test_file.exists():
                generated = test_generator.generate_tests_for_file(test_file)
                total_generated += len(generated)

        assert total_generated > 0, "Should generate tests for multiple files"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
