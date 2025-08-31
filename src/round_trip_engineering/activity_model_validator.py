#!/usr/bin/env python3
"""
Activity Model Validator for Round-Trip Engineering

This module provides comprehensive validation of expected vs actual behavior
for methods and functions, enabling activity model validation as required
by the project model registry.
"""

import ast
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ActivityValidationResult:
    """Result from activity model validation"""

    method_name: str
    validation_passed: bool
    expected_activities: List[str]
    actual_activities: List[str]
    activity_match_score: float
    control_flow_validation: Dict[str, Any]
    behavior_pattern_validation: Dict[str, Any]
    complexity_validation: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    validation_time: float = 0.0


@dataclass
class MethodActivityModel:
    """Expected activity model for a method"""

    name: str
    expected_activities: List[str]
    expected_control_flow: Dict[str, Any]
    expected_behavior_patterns: List[str]
    expected_complexity_range: Tuple[int, int]
    expected_nesting_depth: int
    expected_return_type: str
    expected_parameters: List[str]


class ActivityModelValidator:
    """
    Validates that actual method behavior matches expected activity models.

    This enables the round-trip engineering system to ensure that generated
    code maintains the same behavioral characteristics as the original code.
    """

    def __init__(self):
        self.validation_results: Dict[str, ActivityValidationResult] = {}
        self.expected_models: Dict[str, MethodActivityModel] = {}
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules for different method types"""
        return {
            "data_processing": {
                "required_activities": ["assignment", "function_call"],
                "min_complexity": 2,
                "max_complexity": 10,
                "expected_patterns": ["data_processing"],
            },
            "validation": {
                "required_activities": ["conditional", "assertion"],
                "min_complexity": 1,
                "max_complexity": 5,
                "expected_patterns": ["validation"],
            },
            "error_handling": {
                "required_activities": ["exception_handling", "conditional"],
                "min_complexity": 2,
                "max_complexity": 8,
                "expected_patterns": ["error_handling"],
            },
            "iteration": {
                "required_activities": ["loop"],
                "min_complexity": 2,
                "max_complexity": 15,
                "expected_patterns": ["iteration"],
            },
            "configuration": {
                "required_activities": ["assignment"],
                "min_complexity": 1,
                "max_complexity": 5,
                "expected_patterns": ["configuration"],
            },
            "logging": {
                "required_activities": ["function_call"],
                "min_complexity": 1,
                "max_complexity": 3,
                "expected_patterns": ["logging"],
            },
            "resource_management": {
                "required_activities": ["context_manager"],
                "min_complexity": 1,
                "max_complexity": 5,
                "expected_patterns": ["resource_management"],
            },
        }

    def validate_method_activity_model(
        self,
        method_info: Dict[str, Any],
        expected_model: Optional[MethodActivityModel] = None,
    ) -> ActivityValidationResult:
        """
        Validate that a method's actual behavior matches expected activity model.

        Args:
            method_info: Extracted method information from reverse engineering
            expected_model: Expected activity model (if None, infer from behavior)

        Returns:
            Validation result with detailed analysis
        """
        start_time = time.time()

        try:
            method_name = method_info.get("name", "unknown_method")
            logger.info(f"🔍 Validating activity model for method: {method_name}")

            # Extract actual behavior from method info
            actual_activities = self._extract_actual_activities(method_info)
            actual_control_flow = method_info.get("control_flow", {})
            actual_behavior_patterns = method_info.get("behavior_patterns", [])
            actual_complexity = method_info.get("activity_model", {}).get(
                "complexity_score", 0
            )

            # Determine expected model if not provided
            if expected_model is None:
                expected_model = self._infer_expected_model(
                    method_info, actual_behavior_patterns
                )

            # Validate activities
            activity_validation = self._validate_activities(
                expected_model.expected_activities, actual_activities
            )

            # Validate control flow
            control_flow_validation = self._validate_control_flow(
                expected_model.expected_control_flow, actual_control_flow
            )

            # Validate behavior patterns
            behavior_pattern_validation = self._validate_behavior_patterns(
                expected_model.expected_behavior_patterns, actual_behavior_patterns
            )

            # Validate complexity
            complexity_validation = self._validate_complexity(
                expected_model.expected_complexity_range, actual_complexity
            )

            # Calculate overall validation score
            validation_passed = all(
                [
                    activity_validation["passed"],
                    control_flow_validation["passed"],
                    behavior_pattern_validation["passed"],
                    complexity_validation["passed"],
                ]
            )

            # Calculate activity match score
            activity_match_score = self._calculate_activity_match_score(
                expected_model.expected_activities, actual_activities
            )

            validation_time = time.time() - start_time

            result = ActivityValidationResult(
                method_name=method_name,
                validation_passed=validation_passed,
                expected_activities=expected_model.expected_activities,
                actual_activities=actual_activities,
                activity_match_score=activity_match_score,
                control_flow_validation=control_flow_validation,
                behavior_pattern_validation=behavior_pattern_validation,
                complexity_validation=complexity_validation,
                warnings=[],
                errors=[],
                validation_time=validation_time,
            )

            # Store result
            self.validation_results[method_name] = result

            logger.info(
                f"✅ Activity model validation completed for {method_name} in {validation_time:.3f}s"
            )
            return result

        except Exception as e:
            logger.error(
                f"❌ Activity model validation failed for {method_info.get('name', 'unknown')}: {e}"
            )
            return ActivityValidationResult(
                method_name=method_info.get("name", "unknown"),
                validation_passed=False,
                expected_activities=[],
                actual_activities=[],
                activity_match_score=0.0,
                control_flow_validation={"passed": False, "errors": [str(e)]},
                behavior_pattern_validation={"passed": False, "errors": [str(e)]},
                complexity_validation={"passed": False, "errors": [str(e)]},
                errors=[str(e)],
            )

    def _extract_actual_activities(self, method_info: Dict[str, Any]) -> List[str]:
        """Extract actual activities from method info"""
        try:
            activity_model = method_info.get("activity_model", {})
            activity_sequence = activity_model.get("activity_sequence", [])

            # Extract activity types
            activities = []
            for activity in activity_sequence:
                if isinstance(activity, dict) and "type" in activity:
                    activities.append(activity["type"])

            return activities

        except Exception as e:
            logger.error(f"❌ Error extracting actual activities: {e}")
            return []

    def _infer_expected_model(
        self, method_info: Dict[str, Any], behavior_patterns: List[str]
    ) -> MethodActivityModel:
        """Infer expected activity model from method behavior patterns"""
        try:
            method_name = method_info.get("name", "unknown")

            # Determine primary behavior pattern
            primary_pattern = behavior_patterns[0] if behavior_patterns else "general"

            # Get validation rules for this pattern
            rules = self.validation_rules.get(
                primary_pattern, self.validation_rules["data_processing"]
            )

            # Infer expected activities
            expected_activities = rules.get(
                "required_activities", ["assignment", "function_call"]
            )

            # Infer expected control flow
            expected_control_flow = {
                "has_conditionals": "validation" in behavior_patterns
                or "error_handling" in behavior_patterns,
                "has_loops": "iteration" in behavior_patterns,
                "has_exceptions": "error_handling" in behavior_patterns,
                "nesting_depth": 2 if "iteration" in behavior_patterns else 1,
            }

            # Infer expected behavior patterns
            expected_behavior_patterns = behavior_patterns.copy()

            # Infer complexity range
            min_complexity = rules.get("min_complexity", 1)
            max_complexity = rules.get("max_complexity", 10)

            # Infer return type and parameters
            expected_return_type = method_info.get("return_type", "Any")
            expected_parameters = [
                param.get("name", "param")
                for param in method_info.get("parameters", [])
            ]

            return MethodActivityModel(
                name=method_name,
                expected_activities=expected_activities,
                expected_control_flow=expected_control_flow,
                expected_behavior_patterns=expected_behavior_patterns,
                expected_complexity_range=(min_complexity, max_complexity),
                expected_nesting_depth=expected_control_flow["nesting_depth"],
                expected_return_type=expected_return_type,
                expected_parameters=expected_parameters,
            )

        except Exception as e:
            logger.error(f"❌ Error inferring expected model: {e}")
            # Return default model
            return MethodActivityModel(
                name=method_info.get("name", "unknown"),
                expected_activities=["assignment", "function_call"],
                expected_control_flow={
                    "has_conditionals": False,
                    "has_loops": False,
                    "has_exceptions": False,
                    "nesting_depth": 1,
                },
                expected_behavior_patterns=["data_processing"],
                expected_complexity_range=(1, 5),
                expected_nesting_depth=1,
                expected_return_type="Any",
                expected_parameters=[],
            )

    def _validate_activities(
        self, expected: List[str], actual: List[str]
    ) -> Dict[str, Any]:
        """Validate that actual activities match expected activities"""
        try:
            # Check for required activities
            missing_activities = [act for act in expected if act not in actual]
            extra_activities = [act for act in actual if act not in expected]

            passed = len(missing_activities) == 0

            return {
                "passed": passed,
                "missing_activities": missing_activities,
                "extra_activities": extra_activities,
                "coverage": (
                    len([act for act in expected if act in actual]) / len(expected)
                    if expected
                    else 1.0
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error validating activities: {e}")
            return {"passed": False, "error": str(e)}

    def _validate_control_flow(
        self, expected: Dict[str, Any], actual: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate control flow characteristics"""
        try:
            validation_results = {}

            # Validate conditional presence
            if "has_conditionals" in expected:
                expected_conditionals = expected["has_conditionals"]
                actual_conditionals = actual.get("has_conditionals", False)
                validation_results["conditionals"] = (
                    expected_conditionals == actual_conditionals
                )

            # Validate loop presence
            if "has_loops" in expected:
                expected_loops = expected["has_loops"]
                actual_loops = actual.get("has_loops", False)
                validation_results["loops"] = expected_loops == actual_loops

            # Validate exception handling
            if "has_exceptions" in expected:
                expected_exceptions = expected["has_exceptions"]
                actual_exceptions = actual.get("has_exceptions", False)
                validation_results["exceptions"] = (
                    expected_exceptions == actual_exceptions
                )

            # Validate nesting depth
            if "nesting_depth" in expected:
                expected_depth = expected["nesting_depth"]
                actual_depth = actual.get("nesting_depth", 0)
                validation_results["nesting_depth"] = actual_depth <= expected_depth

            # Overall validation
            passed = all(validation_results.values())

            return {
                "passed": passed,
                "validation_results": validation_results,
                "expected": expected,
                "actual": actual,
            }

        except Exception as e:
            logger.error(f"❌ Error validating control flow: {e}")
            return {"passed": False, "error": str(e)}

    def _validate_behavior_patterns(
        self, expected: List[str], actual: List[str]
    ) -> Dict[str, Any]:
        """Validate behavior patterns"""
        try:
            # Check for required patterns
            missing_patterns = [
                pattern for pattern in expected if pattern not in actual
            ]
            extra_patterns = [pattern for pattern in actual if pattern not in expected]

            passed = len(missing_patterns) == 0

            return {
                "passed": passed,
                "missing_patterns": missing_patterns,
                "extra_patterns": extra_patterns,
                "pattern_coverage": (
                    len([p for p in expected if p in actual]) / len(expected)
                    if expected
                    else 1.0
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error validating behavior patterns: {e}")
            return {"passed": False, "error": str(e)}

    def _validate_complexity(
        self, expected_range: Tuple[int, int], actual: int
    ) -> Dict[str, Any]:
        """Validate complexity score"""
        try:
            min_complexity, max_complexity = expected_range
            passed = min_complexity <= actual <= max_complexity

            return {
                "passed": passed,
                "expected_range": expected_range,
                "actual": actual,
                "within_range": passed,
                "too_simple": actual < min_complexity,
                "too_complex": actual > max_complexity,
            }

        except Exception as e:
            logger.error(f"❌ Error validating complexity: {e}")
            return {"passed": False, "error": str(e)}

    def _calculate_activity_match_score(
        self, expected: List[str], actual: List[str]
    ) -> float:
        """Calculate how well actual activities match expected activities"""
        try:
            if not expected:
                return 1.0 if not actual else 0.0

            # Calculate intersection
            intersection = set(expected) & set(actual)

            # Calculate union
            union = set(expected) | set(actual)

            # Jaccard similarity
            if not union:
                return 1.0

            return len(intersection) / len(union)

        except Exception as e:
            logger.error(f"❌ Error calculating activity match score: {e}")
            return 0.0

    def validate_file_activity_models(
        self, file_path: str, extracted_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate activity models for all methods in a file.

        Args:
            file_path: Path to the source file
            extracted_model: Extracted model from reverse engineering

        Returns:
            Comprehensive validation results for the file
        """
        try:
            logger.info(f"🔍 Validating activity models for file: {file_path}")

            validation_results = {
                "file_path": file_path,
                "validation_timestamp": time.time(),
                "method_validations": {},
                "overall_validation": {
                    "passed": True,
                    "total_methods": 0,
                    "passed_methods": 0,
                    "failed_methods": 0,
                    "average_match_score": 0.0,
                },
            }

            # Validate class methods
            components = extracted_model.get("components", {})
            if isinstance(components, dict):
                for class_name, class_info in components.items():
                    methods = class_info.get("methods", [])
                    for method_info in methods:
                        result = self.validate_method_activity_model(method_info)
                        validation_results["method_validations"][
                            f"{class_name}.{method_info['name']}"
                        ] = result

                        # Update overall statistics
                        validation_results["overall_validation"]["total_methods"] += 1
                        if result.validation_passed:
                            validation_results["overall_validation"][
                                "passed_methods"
                            ] += 1
                        else:
                            validation_results["overall_validation"][
                                "failed_methods"
                            ] += 1
                            validation_results["overall_validation"]["passed"] = False

            # Validate module functions
            module_functions = extracted_model.get("module_functions", [])
            for func_info in module_functions:
                result = self.validate_method_activity_model(func_info)
                validation_results["method_validations"][
                    f"module.{func_info['name']}"
                ] = result

                # Update overall statistics
                validation_results["overall_validation"]["total_methods"] += 1
                if result.validation_passed:
                    validation_results["overall_validation"]["passed_methods"] += 1
                else:
                    validation_results["overall_validation"]["failed_methods"] += 1
                    validation_results["overall_validation"]["passed"] = False

            # Calculate average match score
            if validation_results["overall_validation"]["total_methods"] > 0:
                total_score = sum(
                    result.activity_match_score
                    for result in validation_results["method_validations"].values()
                )
                validation_results["overall_validation"]["average_match_score"] = (
                    total_score
                    / validation_results["overall_validation"]["total_methods"]
                )

            logger.info(
                f"✅ File activity model validation completed: {validation_results['overall_validation']['passed_methods']}/{validation_results['overall_validation']['total_methods']} methods passed"
            )
            return validation_results

        except Exception as e:
            logger.error(f"❌ File activity model validation failed: {e}")
            return {
                "file_path": file_path,
                "error": str(e),
                "overall_validation": {"passed": False},
            }

    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable validation report"""
        try:
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("ACTIVITY MODEL VALIDATION REPORT")
            report_lines.append("=" * 80)
            report_lines.append("")

            # File summary
            file_path = validation_results.get("file_path", "unknown")
            overall = validation_results.get("overall_validation", {})

            report_lines.append(f"📁 File: {file_path}")
            report_lines.append(
                f"📊 Overall Status: {'✅ PASSED' if overall.get('passed', False) else '❌ FAILED'}"
            )
            report_lines.append(f"🔢 Total Methods: {overall.get('total_methods', 0)}")
            report_lines.append(f"✅ Passed: {overall.get('passed_methods', 0)}")
            report_lines.append(f"❌ Failed: {overall.get('failed_methods', 0)}")
            report_lines.append(
                f"📈 Average Match Score: {overall.get('average_match_score', 0.0):.2f}"
            )
            report_lines.append("")

            # Method details
            method_validations = validation_results.get("method_validations", {})
            if method_validations:
                report_lines.append("📋 Method Validation Details:")
                report_lines.append("-" * 60)

                for method_name, result in method_validations.items():
                    status = "✅ PASSED" if result.validation_passed else "❌ FAILED"
                    report_lines.append(f"{method_name}: {status}")
                    report_lines.append(
                        f"  Activity Match Score: {result.activity_match_score:.2f}"
                    )

                    if not result.validation_passed:
                        if result.control_flow_validation.get("errors"):
                            report_lines.append(
                                f"  Control Flow Errors: {result.control_flow_validation['errors']}"
                            )
                        if result.behavior_pattern_validation.get("errors"):
                            report_lines.append(
                                f"  Behavior Pattern Errors: {result.behavior_pattern_validation['errors']}"
                            )
                        if result.complexity_validation.get("errors"):
                            report_lines.append(
                                f"  Complexity Errors: {result.complexity_validation['errors']}"
                            )

                    report_lines.append("")

            report_lines.append("=" * 80)
            return "\n".join(report_lines)

        except Exception as e:
            logger.error(f"❌ Error generating validation report: {e}")
            return f"Error generating report: {e}"

    def save_validation_results(
        self, output_path: str, validation_results: Dict[str, Any]
    ) -> bool:
        """Save validation results to JSON file"""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w") as f:
                json.dump(validation_results, f, indent=2, default=str)

            logger.info(f"✅ Validation results saved to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Error saving validation results: {e}")
            return False


def main():
    """Main function for testing the activity model validator"""
    print("🚀 Activity Model Validator for Round-Trip Engineering")
    print("=" * 60)

    # Create validator
    validator = ActivityModelValidator()

    # Test with sample data
    sample_method = {
        "name": "test_method",
        "activity_model": {
            "activity_sequence": [
                {
                    "type": "assignment",
                    "description": "Assign to 1 target(s)",
                    "complexity": "simple",
                },
                {
                    "type": "function_call",
                    "description": "Call function: process_data",
                    "complexity": "medium",
                },
            ],
            "total_activities": 2,
            "activity_types": {"assignment": 1, "function_call": 1},
            "complexity_score": 3,
        },
        "control_flow": {
            "flow_map": {},
            "has_conditionals": False,
            "has_loops": False,
            "has_exceptions": False,
            "nesting_depth": 1,
        },
        "behavior_patterns": ["data_processing"],
        "return_type": "Dict[str, Any]",
        "parameters": [{"name": "data", "type": "List[str]"}],
    }

    # Validate the sample method
    result = validator.validate_method_activity_model(sample_method)

    print(f"✅ Validation completed for {result.method_name}")
    print(f"📊 Activity Match Score: {result.activity_match_score:.2f}")
    print(f"🔍 Validation Passed: {result.validation_passed}")
    print(f"⏱️  Validation Time: {result.validation_time:.3f}s")


if __name__ == "__main__":
    main()
