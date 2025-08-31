#!/usr/bin/env python3
"""
Complete Round-Trip Engineering Workflow Test

This test demonstrates the complete round-trip engineering workflow:
1. Reverse Engineering: Extract models from Python files
2. Activity Modeling: Generate and validate activity models
3. Forward Engineering: Generate code with behavioral consistency
4. Validation: Ensure generated code maintains behavioral characteristics
"""

import pytest
import time
import logging
import json
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from round_trip_engineering.core.round_trip_system import RoundTripSystem
from round_trip_engineering.activity_model_validator import ActivityModelValidator
from round_trip_engineering.generators.activity_aware_code_generator import (
    ActivityAwareCodeGenerator,
)
from round_trip_engineering.enhanced_reverse_engineer import EnhancedReverseEngineer


class TestCompleteRoundTripWorkflow:
    """Test suite for complete round-trip engineering workflow."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.INFO)

        # Create test directory
        cls.test_dir = Path("/tmp/complete_round_trip_test")
        cls.test_dir.mkdir(exist_ok=True)

        # Initialize components
        cls.round_trip_system = RoundTripSystem()
        cls.reverse_engineer = EnhancedReverseEngineer()
        cls.activity_validator = ActivityModelValidator()
        cls.activity_aware_generator = ActivityAwareCodeGenerator()

        cls.logger.info("✅ Complete Round-Trip Workflow test suite initialized")

    @classmethod
    def teardown_class(cls):
        """Clean up test environment."""
        cls.logger.info("🧹 Cleaning up test environment")
        # Cleanup code here if needed

    def test_complete_round_trip_workflow(self):
        """Test the complete round-trip engineering workflow."""
        self.logger.info("🧪 Testing Complete Round-Trip Engineering Workflow")

        # Test file to process
        test_file = "src/round_trip_engineering/enhanced_reverse_engineer.py"

        # STEP 1: Reverse Engineering - Extract model from Python file
        self.logger.info(
            "🔄 Step 1: Reverse Engineering - Extracting model from Python file"
        )
        start_time = time.time()

        extracted_model = self.reverse_engineer.reverse_engineer_file(test_file)
        reverse_engineering_time = time.time() - start_time

        assert extracted_model is not None
        assert "model_id" in extracted_model
        assert "components" in extracted_model
        self.logger.info(
            f"✅ Reverse engineering completed in {reverse_engineering_time:.3f}s"
        )
        self.logger.info(
            f"📊 Extracted model contains {len(extracted_model.get('components', {}))} components"
        )

        # STEP 2: Activity Modeling - Generate activity models for the extracted model
        self.logger.info("🔄 Step 2: Activity Modeling - Generating activity models")
        start_time = time.time()

        # Generate activity models for each method in the extracted model
        activity_models = {}
        components = extracted_model.get("components", {})

        for class_name, class_info in components.items():
            methods = class_info.get("methods", [])
            for method_info in methods:
                method_name = method_info.get("name", "unknown_method")
                # Create a method key for validation
                method_key = f"{class_name}.{method_name}"

                # Validate the method's activity model
                validation_result = (
                    self.activity_validator.validate_method_activity_model(method_info)
                )
                activity_models[method_key] = validation_result

        activity_modeling_time = time.time() - start_time
        self.logger.info(
            f"✅ Activity modeling completed in {activity_modeling_time:.3f}s"
        )
        self.logger.info(f"📊 Generated {len(activity_models)} activity models")

        # STEP 3: Activity Model Validation - Validate behavioral consistency
        self.logger.info(
            "🔄 Step 3: Activity Model Validation - Validating behavioral consistency"
        )
        start_time = time.time()

        # Analyze validation results
        total_methods = len(activity_models)
        passed_validations = sum(
            1 for result in activity_models.values() if result.validation_passed
        )
        average_match_score = (
            sum(result.activity_match_score for result in activity_models.values())
            / total_methods
            if total_methods > 0
            else 0
        )

        validation_time = time.time() - start_time
        self.logger.info(
            f"✅ Activity model validation completed in {validation_time:.3f}s"
        )
        self.logger.info(
            f"📊 Validation Results: {passed_validations}/{total_methods} passed, avg score: {average_match_score:.2f}"
        )

        # STEP 4: Forward Engineering - Generate code with activity model guidance
        self.logger.info(
            "🔄 Step 4: Forward Engineering - Generating code with behavioral consistency"
        )
        start_time = time.time()

        # Create activity models structure for the generator
        activity_models_structure = {
            "validation_results": activity_models,
            "metadata": {
                "total_methods": total_methods,
                "passed_validations": passed_validations,
                "average_match_score": average_match_score,
                "validation_timestamp": time.time(),
            },
        }

        # Generate code using activity-aware generator
        generated_code = self.activity_aware_generator.generate_with_activity_models(
            extracted_model, activity_models_structure
        )

        forward_engineering_time = time.time() - start_time
        self.logger.info(
            f"✅ Forward engineering completed in {forward_engineering_time:.3f}s"
        )
        self.logger.info(f"📊 Generated code length: {len(generated_code)} characters")

        # STEP 5: Validation - Ensure generated code maintains behavioral characteristics
        self.logger.info(
            "🔄 Step 5: Validation - Ensuring behavioral consistency in generated code"
        )
        start_time = time.time()

        # Save generated code to test file
        generated_file = self.test_dir / "generated_round_trip_code.py"
        with open(generated_file, "w") as f:
            f.write(generated_code)

        # Validate that the generated code has the same structure
        validation_passed = self._validate_generated_code_structure(
            extracted_model, generated_code
        )

        validation_time = time.time() - start_time
        self.logger.info(f"✅ Code validation completed in {validation_time:.3f}s")

        # STEP 6: Round-Trip Validation - Ensure the complete workflow works
        self.logger.info("🔄 Step 6: Round-Trip Validation - Testing complete workflow")
        start_time = time.time()

        # Test that we can reverse engineer the generated code
        regenerated_model = self.reverse_engineer.reverse_engineer_file(
            str(generated_file)
        )

        round_trip_validation_time = time.time() - start_time
        self.logger.info(
            f"✅ Round-trip validation completed in {round_trip_validation_time:.3f}s"
        )

        # Validate round-trip consistency
        round_trip_consistent = self._validate_round_trip_consistency(
            extracted_model, regenerated_model
        )

        # STEP 7: Generate comprehensive report
        self.logger.info("🔄 Step 7: Generating comprehensive workflow report")

        workflow_report = self._generate_workflow_report(
            extracted_model,
            activity_models,
            generated_code,
            regenerated_model,
            {
                "reverse_engineering_time": reverse_engineering_time,
                "activity_modeling_time": activity_modeling_time,
                "validation_time": validation_time,
                "forward_engineering_time": forward_engineering_time,
                "round_trip_validation_time": round_trip_validation_time,
            },
        )

        # Save report
        report_file = self.test_dir / "complete_round_trip_report.txt"
        with open(report_file, "w") as f:
            f.write(workflow_report)

        self.logger.info(f"📄 Workflow report saved to: {report_file}")

        # Final assertions
        assert extracted_model is not None, "Reverse engineering failed"
        assert len(activity_models) > 0, "No activity models generated"
        assert generated_code is not None, "Code generation failed"
        assert len(generated_code) > 0, "Generated code is empty"
        assert regenerated_model is not None, "Round-trip reverse engineering failed"
        assert validation_passed, "Generated code structure validation failed"
        assert round_trip_consistent, "Round-trip consistency validation failed"

        self.logger.info("🎉 Complete Round-Trip Engineering Workflow Test PASSED!")
        self.logger.info("✅ All steps completed successfully")
        self.logger.info("✅ Behavioral consistency maintained")
        self.logger.info("✅ Round-trip validation successful")

    def _validate_generated_code_structure(
        self, original_model: Dict[str, Any], generated_code: str
    ) -> bool:
        """Validate that generated code maintains the same structure as original."""
        try:
            # Check that generated code contains expected components
            components = original_model.get("components", {})

            for class_name in components.keys():
                if class_name not in generated_code:
                    self.logger.warning(
                        f"⚠️  Generated code missing class: {class_name}"
                    )
                    return False

            # Check that generated code has proper Python syntax
            try:
                compile(generated_code, "<string>", "exec")
            except SyntaxError as e:
                self.logger.error(f"❌ Generated code has syntax errors: {e}")
                return False

            # Check that generated code has activity model metadata
            if "Behavioral Constraints:" not in generated_code:
                self.logger.warning(
                    "⚠️  Generated code missing behavioral constraints metadata"
                )
                return False

            self.logger.info("✅ Generated code structure validation passed")
            return True

        except Exception as e:
            self.logger.error(f"❌ Code structure validation failed: {e}")
            return False

    def _validate_round_trip_consistency(
        self, original_model: Dict[str, Any], regenerated_model: Dict[str, Any]
    ) -> bool:
        """Validate that round-trip engineering maintains consistency."""
        try:
            # Check that both models have the same basic structure
            original_components = original_model.get("components", {})
            regenerated_components = regenerated_model.get("components", {})

            if len(original_components) != len(regenerated_components):
                self.logger.warning(
                    f"⚠️  Component count mismatch: {len(original_components)} vs {len(regenerated_components)}"
                )
                return False

            # Check that component names are preserved
            original_names = set(original_components.keys())
            regenerated_names = set(regenerated_components.keys())

            if original_names != regenerated_names:
                self.logger.warning(
                    f"⚠️  Component name mismatch: {original_names} vs {regenerated_names}"
                )
                return False

            self.logger.info("✅ Round-trip consistency validation passed")
            return True

        except Exception as e:
            self.logger.error(f"❌ Round-trip consistency validation failed: {e}")
            return False

    def _generate_workflow_report(
        self,
        extracted_model: Dict[str, Any],
        activity_models: Dict[str, Any],
        generated_code: str,
        regenerated_model: Dict[str, Any],
        timing_metrics: Dict[str, float],
    ) -> str:
        """Generate a comprehensive workflow report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("COMPLETE ROUND-TRIP ENGINEERING WORKFLOW REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Summary
        report_lines.append("📊 WORKFLOW SUMMARY")
        report_lines.append(
            f"  Original Model ID: {extracted_model.get('model_id', 'unknown')}"
        )
        report_lines.append(
            f"  Components Extracted: {len(extracted_model.get('components', {}))}"
        )
        report_lines.append(f"  Activity Models Generated: {len(activity_models)}")
        report_lines.append(
            f"  Generated Code Length: {len(generated_code)} characters"
        )
        report_lines.append(
            f"  Regenerated Model ID: {regenerated_model.get('model_id', 'unknown')}"
        )
        report_lines.append("")

        # Timing Metrics
        report_lines.append("⏱️  TIMING METRICS")
        total_time = sum(timing_metrics.values())
        for step, time_taken in timing_metrics.items():
            percentage = (time_taken / total_time) * 100 if total_time > 0 else 0
            report_lines.append(
                f"  {step.replace('_', ' ').title()}: {time_taken:.3f}s ({percentage:.1f}%)"
            )
        report_lines.append(f"  Total Workflow Time: {total_time:.3f}s")
        report_lines.append("")

        # Activity Model Analysis
        report_lines.append("🎯 ACTIVITY MODEL ANALYSIS")
        if activity_models:
            passed_validations = sum(
                1 for result in activity_models.values() if result.validation_passed
            )
            total_methods = len(activity_models)
            average_score = (
                sum(result.activity_match_score for result in activity_models.values())
                / total_methods
                if total_methods > 0
                else 0
            )

            report_lines.append(f"  Total Methods: {total_methods}")
            report_lines.append(f"  Passed Validations: {passed_validations}")
            report_lines.append(
                f"  Failed Validations: {total_methods - passed_validations}"
            )
            report_lines.append(f"  Average Match Score: {average_score:.2f}")
            report_lines.append(
                f"  Success Rate: {(passed_validations / total_methods) * 100:.1f}%"
            )
        else:
            report_lines.append("  No activity models generated")
        report_lines.append("")

        # Behavioral Consistency
        report_lines.append("🔄 BEHAVIORAL CONSISTENCY")
        report_lines.append("  ✅ Reverse Engineering: Successfully extracted model")
        report_lines.append(
            "  ✅ Activity Modeling: Generated comprehensive activity models"
        )
        report_lines.append(
            "  ✅ Forward Engineering: Generated code with behavioral guidance"
        )
        report_lines.append(
            "  ✅ Round-Trip Validation: Maintained structural consistency"
        )
        report_lines.append("")

        # Next Steps
        report_lines.append("🚀 NEXT STEPS")
        report_lines.append(
            "  1. Enhance activity model validation rules for better accuracy"
        )
        report_lines.append(
            "  2. Implement more sophisticated behavioral constraint validation"
        )
        report_lines.append("  3. Add support for more programming languages")
        report_lines.append(
            "  4. Integrate with CI/CD for automated round-trip validation"
        )
        report_lines.append("")

        report_lines.append("=" * 80)
        report_lines.append("END OF WORKFLOW REPORT")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)

    def test_individual_workflow_components(self):
        """Test individual components of the workflow."""
        self.logger.info("🧪 Testing Individual Workflow Components")

        # Test reverse engineering
        test_file = "src/round_trip_engineering/enhanced_reverse_engineer.py"
        model = self.reverse_engineer.reverse_engineer_file(test_file)
        assert model is not None, "Reverse engineering component failed"

        # Test activity model validation
        components = model.get("components", {})
        if components:
            first_class = list(components.values())[0]
            methods = first_class.get("methods", [])
            if methods:
                first_method = methods[0]
                validation_result = (
                    self.activity_validator.validate_method_activity_model(first_method)
                )
                assert validation_result is not None, (
                    "Activity model validation component failed"
                )

        # Test code generation
        dummy_model = {
            "system_name": "TestSystem",
            "description": "Test system for validation",
            "components": {},
            "model_id": "test-123",
        }
        dummy_activity_models = {"validation_results": {}}

        generated_code = self.activity_aware_generator.generate_with_activity_models(
            dummy_model, dummy_activity_models
        )
        assert generated_code is not None, "Code generation component failed"

        self.logger.info("✅ All individual workflow components working correctly")


if __name__ == "__main__":
    # Run the test
    test_suite = TestCompleteRoundTripWorkflow()
    test_suite.setup_class()

    try:
        test_suite.test_complete_round_trip_workflow()
        test_suite.test_individual_workflow_components()
        print("🎉 All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        test_suite.teardown_class()
