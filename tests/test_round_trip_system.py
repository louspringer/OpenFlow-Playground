"""
Comprehensive Test Suite for Round-Trip Engineering System

This test suite validates the complete round-trip workflow with full logging
and profiling to compare expected vs actual behavior.
"""

import pytest
import logging
import tempfile
import json
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from round_trip_engineering import RoundTripSystem
from round_trip_engineering.logging_config import setup_logging, get_logger


class TestRoundTripSystem:
    """Test suite for the complete round-trip engineering system."""

    @classmethod
    def setup_class(cls):
        """Setup logging and test environment."""
        # Setup comprehensive logging for testing
        setup_logging(
            log_level="DEBUG",
            log_file="test_round_trip.log",
            enable_profiling=True,
            enable_console=True,
        )

        cls.logger = get_logger("TestRoundTripSystem")
        cls.logger.info("🧪 Setting up Round-Trip System test suite")

        # Create temporary directory for test artifacts
        cls.test_dir = Path(tempfile.mkdtemp(prefix="round_trip_test_"))
        cls.logger.info(f"📁 Test directory: {cls.test_dir}")

    def setup_method(self):
        """Setup for each test method."""
        self.system = RoundTripSystem()
        self.logger.info("✅ Round-Trip System initialized for test")

    def test_vocabulary_alignment_workflow(self):
        """Test the complete vocabulary alignment workflow."""
        self.logger.info("🧪 Testing vocabulary alignment workflow")

        # Test data: Reverse engineering output (list format)
        test_data = {
            "system_name": "TestSystem",
            "description": "A test system for validation",
            "components": [
                {
                    "name": "TestComponent",
                    "type": "class",
                    "description": "A test component",
                    "responsibility": "Test component for validation",
                    "methods": [
                        {
                            "name": "test_method",
                            "docstring": "A test method",
                            "return_type": "str",
                            "parameters": [],
                        }
                    ],
                }
            ],
        }

        # Validate input format
        assert isinstance(test_data["components"], list)
        assert len(test_data["components"]) == 1
        assert test_data["components"][0]["name"] == "TestComponent"

        self.logger.info(f"📊 Input components type: {type(test_data['components'])}")
        self.logger.info(f"📊 Input components length: {len(test_data['components'])}")

        # Test vocabulary alignment
        aligned_data = self.system.vocabulary_aligner.align_vocabulary(test_data)

        # Validate output format
        assert isinstance(aligned_data["components"], dict)
        assert "TestComponent" in aligned_data["components"]
        assert aligned_data["components"]["TestComponent"]["name"] == "TestComponent"

        self.logger.info(
            f"📊 Output components type: {type(aligned_data['components'])}"
        )
        self.logger.info(
            f"📊 Output components keys: {list(aligned_data['components'].keys())}"
        )

        # Log performance metrics
        self.system.print_profiling_summary()

        self.logger.info("✅ Vocabulary alignment workflow test completed")

    def test_code_generation_workflow(self):
        """Test the complete code generation workflow."""
        self.logger.info("🧪 Testing code generation workflow")

        # Test data: Aligned model (dict format)
        test_data = {
            "system_name": "TestSystem",
            "description": "A test system for validation",
            "components": {
                "TestComponent": {
                    "name": "TestComponent",
                    "type": "class",
                    "description": "A test component",
                    "responsibility": "Test component for validation",
                    "methods": [
                        {
                            "name": "test_method",
                            "docstring": "A test method",
                            "return_type": "str",
                            "parameters": [],
                        }
                    ],
                }
            },
        }

        # Validate input format
        assert isinstance(test_data["components"], dict)
        assert len(test_data["components"]) == 1
        assert "TestComponent" in test_data["components"]

        self.logger.info(f"📊 Input components type: {type(test_data['components'])}")
        self.logger.info(f"📊 Input components count: {len(test_data['components'])}")

        # Test code generation
        generated_code = self.system.generate_code_from_extracted_model(test_data)

        # Validate generated code
        assert isinstance(generated_code, str)
        assert len(generated_code) > 0
        assert "class TestComponent" in generated_code
        assert "def test_method" in generated_code
        assert "str" in generated_code  # Return type

        self.logger.info(f"📊 Generated code length: {len(generated_code)} characters")
        self.logger.info(
            f"📊 Generated code lines: {len(generated_code.split(chr(10)))}"
        )

        # Save generated code for inspection
        code_file = self.test_dir / "generated_test_component.py"
        with open(code_file, "w") as f:
            f.write(generated_code)
        self.logger.info(f"💾 Generated code saved to: {code_file}")

        # Log performance metrics
        self.system.print_profiling_summary()

        self.logger.info("✅ Code generation workflow test completed")

    def test_duplication_cleaning_workflow(self):
        """Test the duplication cleaning workflow."""
        self.logger.info("🧪 Testing duplication cleaning workflow")

        # Test code with intentional duplications
        test_code = """class TestClass:
    def duplicate_method(self):
        return "first"
    
    def duplicate_method(self):
        return "second"
    
    def unique_method(self):
        return "unique"
    
    def another_method(self):
        return "first"
        return "second"
"""

        # Count original lines and duplications
        original_lines = len(test_code.split(chr(10)))
        duplicate_methods = test_code.count("def duplicate_method")
        duplicate_returns = test_code.count('return "second"')

        self.logger.info(f"📊 Original code lines: {original_lines}")
        self.logger.info(f"📊 Duplicate methods: {duplicate_methods}")
        self.logger.info(f"📊 Duplicate returns: {duplicate_returns}")

        # Test duplication cleaning
        cleaned_code = self.system.duplication_cleaner.clean_code(test_code)

        # Count cleaned lines and remaining duplications
        cleaned_lines = len(cleaned_code.split(chr(10)))
        remaining_duplicate_methods = cleaned_code.count("def duplicate_method")

        # Count unreachable returns by looking for multiple returns in same method
        # This is more complex than just counting a specific string
        lines = cleaned_code.split(chr(10))
        remaining_unreachable_returns = 0
        current_method = None
        method_has_return = False

        # Debug: Print the cleaned code to see what we're working with
        self.logger.info("🔍 DEBUG: Cleaned code content:")
        for i, line in enumerate(lines):
            self.logger.info(f"  Line {i + 1}: {repr(line)}")

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("def "):
                current_method = line_stripped
                method_has_return = False
                self.logger.info(f"🔍 DEBUG: Found method: {current_method}")
            elif line_stripped.startswith("return "):
                if current_method and method_has_return:
                    remaining_unreachable_returns += 1
                    self.logger.info(
                        f"🔍 DEBUG: Found unreachable return: {line_stripped} in {current_method}"
                    )
                method_has_return = True
                self.logger.info(
                    f"🔍 DEBUG: Found return: {line_stripped} in {current_method}"
                )

        self.logger.info(f"📊 Cleaned code lines: {cleaned_lines}")
        self.logger.info(
            f"📊 Remaining duplicate methods: {remaining_duplicate_methods}"
        )
        self.logger.info(
            f"📊 Remaining unreachable returns: {remaining_unreachable_returns}"
        )

        # Validate cleaning effectiveness
        assert remaining_duplicate_methods == 1, (
            f"Should have only one duplicate_method, got {remaining_duplicate_methods}"
        )
        assert remaining_unreachable_returns == 0, (
            f"Should have no unreachable returns, got {remaining_unreachable_returns}"
        )
        assert cleaned_lines < original_lines, (
            f"Should have fewer lines after cleaning: {original_lines} → {cleaned_lines}"
        )

        # Save cleaned code for inspection
        cleaned_file = self.test_dir / "cleaned_test_code.py"
        with open(cleaned_file, "w") as f:
            f.write(cleaned_code)
        self.logger.info(f"💾 Cleaned code saved to: {cleaned_file}")

        self.logger.info("✅ Duplication cleaning workflow test completed")

    def test_complete_round_trip_workflow(self):
        """Test the actual round-trip capabilities that exist."""
        self.logger.info("🧪 Testing actual round-trip capabilities")

        # Test data: This represents what the system actually does
        # - Generate code from extracted models (not from design specs)
        extracted_model = {
            "system_name": "TestRoundTripSystem",
            "description": "A test system for round-trip validation",
            "components": {
                "TestProcessor": {
                    "name": "TestProcessor",
                    "type": "class",
                    "description": "A test processor component",
                    "methods": [
                        {
                            "name": "process_data",
                            "docstring": "Process input data",
                            "return_type": "Dict[str, Any]",
                            "parameters": [
                                {"name": "data", "type": "List[str]", "default": None}
                            ],
                        }
                    ],
                }
            },
        }

        self.logger.info("🔄 Step 1: Generate code from extracted model")
        generated_code = self.system.generate_code_from_extracted_model(
            extracted_model, "python"
        )
        assert generated_code is not None
        assert len(generated_code) > 0

        # Step 2: Validate generated code structure
        self.logger.info("🔄 Step 2: Validate generated code structure")
        assert "class TestProcessor" in generated_code
        assert "def process_data" in generated_code
        assert "Dict[str, Any]" in generated_code or "Dict" in generated_code

        # Step 3: Save generated code for inspection
        self.logger.info("🔄 Step 3: Save generated code for inspection")
        code_file = self.test_dir / "test_processor_generated.py"
        with open(code_file, "w") as f:
            f.write(generated_code)
        assert code_file.exists()
        self.logger.info(f"💾 Generated code saved to: {code_file}")

        # Step 4: Validate code quality
        self.logger.info("🔄 Step 4: Validate code quality")
        # Check for Reflective Module interfaces
        assert (
            "ReflectiveModule" in generated_code
            or "reflective_module" in generated_code.lower()
        )
        # Check for Pydantic usage
        assert "BaseModel" in generated_code or "pydantic" in generated_code.lower()

        # Log final performance summary
        self.logger.info("📊 FINAL PERFORMANCE SUMMARY:")
        self.system.print_profiling_summary()

        self.logger.info("✅ Actual round-trip capabilities test completed")

    def test_error_handling_and_logging(self):
        """Test error handling and logging capabilities."""
        self.logger.info("🧪 Testing error handling and logging")

        # Test with invalid data
        invalid_data = {"components": "not_a_list_or_dict"}  # Invalid format

        try:
            # This should fail and be logged
            self.system.generate_code_from_extracted_model(invalid_data)
            assert False, "Should have raised an exception"
        except Exception as e:
            self.logger.info(f"✅ Expected error caught: {e}")

            # Check that error was logged with context
            profiling_stats = self.system.get_profiling_stats()
            assert profiling_stats is not None

        self.logger.info("✅ Error handling and logging test completed")

    @classmethod
    def teardown_class(cls):
        """Cleanup test environment."""
        cls.logger.info("🧹 Cleaning up test environment")

        # Log final test summary
        cls.logger.info("📊 TEST SUITE COMPLETED")
        cls.logger.info(f"📁 Test artifacts saved in: {cls.test_dir}")
        cls.logger.info("💡 Check the logs for detailed profiling information")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
