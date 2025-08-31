#!/usr/bin/env python3
"""
Test Activity Model Validation for Round-Trip Engineering

This script demonstrates the activity model validation system that validates
expected vs actual behavior for methods and functions.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from round_trip_engineering.enhanced_reverse_engineer import EnhancedReverseEngineer
from round_trip_engineering.activity_model_validator import ActivityModelValidator


def test_activity_model_validation():
    """Test the complete activity model validation workflow"""
    print("🚀 Testing Activity Model Validation for Round-Trip Engineering")
    print("=" * 70)

    # Step 1: Reverse engineer a file to extract activity models
    print("🔄 Step 1: Reverse engineering file for activity modeling...")
    reverse_engineer = EnhancedReverseEngineer()

    # Test with the enhanced reverse engineer itself
    test_file = "src/round_trip_engineering/enhanced_reverse_engineer.py"

    try:
        extracted_model = reverse_engineer.reverse_engineer_file(test_file)
        print(f"✅ Successfully extracted model from {test_file}")
        print(f"📊 Model contains {len(extracted_model.get('components', {}))} classes")
        print(
            f"🔧 Model contains {len(extracted_model.get('module_functions', []))} module functions"
        )

    except Exception as e:
        print(f"❌ Failed to reverse engineer {test_file}: {e}")
        return False

    # Step 2: Validate activity models
    print("\n🔄 Step 2: Validating activity models...")
    validator = ActivityModelValidator()

    try:
        validation_results = validator.validate_file_activity_models(
            test_file, extracted_model
        )
        print(f"✅ Activity model validation completed")
        print(
            f"📊 Overall validation: {'✅ PASSED' if validation_results['overall_validation']['passed'] else '❌ FAILED'}"
        )
        print(
            f"🔢 Total methods: {validation_results['overall_validation']['total_methods']}"
        )
        print(f"✅ Passed: {validation_results['overall_validation']['passed_methods']}")
        print(f"❌ Failed: {validation_results['overall_validation']['failed_methods']}")
        print(
            f"📈 Average match score: {validation_results['overall_validation']['average_match_score']:.2f}"
        )

    except Exception as e:
        print(f"❌ Activity model validation failed: {e}")
        return False

    # Step 3: Generate validation report
    print("\n🔄 Step 3: Generating validation report...")
    try:
        report = validator.generate_validation_report(validation_results)
        print("📋 Validation Report:")
        print("-" * 50)
        print(report)

    except Exception as e:
        print(f"❌ Failed to generate report: {e}")
        return False

    # Step 4: Save validation results
    print("\n🔄 Step 4: Saving validation results...")
    try:
        output_path = "activity_model_validation_results.json"
        success = validator.save_validation_results(output_path, validation_results)
        if success:
            print(f"✅ Validation results saved to {output_path}")
        else:
            print("❌ Failed to save validation results")

    except Exception as e:
        print(f"❌ Failed to save results: {e}")
        return False

    print("\n🎉 Activity Model Validation Test Completed Successfully!")
    return True


def test_individual_method_validation():
    """Test individual method validation"""
    print("\n🧪 Testing Individual Method Validation")
    print("=" * 50)

    validator = ActivityModelValidator()

    # Test with a sample method
    sample_method = {
        "name": "process_data",
        "activity_model": {
            "activity_sequence": [
                {
                    "type": "assignment",
                    "description": "Assign to 1 target(s)",
                    "complexity": "simple",
                },
                {
                    "type": "function_call",
                    "description": "Call function: validate_input",
                    "complexity": "medium",
                },
                {
                    "type": "conditional",
                    "description": "If statement",
                    "complexity": "medium",
                },
                {
                    "type": "function_call",
                    "description": "Call function: transform_data",
                    "complexity": "medium",
                },
                {
                    "type": "return",
                    "description": "Return statement",
                    "complexity": "simple",
                },
            ],
            "total_activities": 5,
            "activity_types": {
                "assignment": 1,
                "function_call": 2,
                "conditional": 1,
                "return": 1,
            },
            "complexity_score": 8,
        },
        "control_flow": {
            "flow_map": {
                10: {"type": "conditional", "has_nested": False, "nesting_level": 1}
            },
            "has_conditionals": True,
            "has_loops": False,
            "has_exceptions": False,
            "nesting_depth": 1,
        },
        "behavior_patterns": ["data_processing", "validation"],
        "return_type": "Dict[str, Any]",
        "parameters": [{"name": "input_data", "type": "List[str]"}],
    }

    try:
        result = validator.validate_method_activity_model(sample_method)
        print(f"✅ Method validation completed for {result.method_name}")
        print(f"📊 Activity Match Score: {result.activity_match_score:.2f}")
        print(f"🔍 Validation Passed: {result.validation_passed}")
        print(f"⏱️  Validation Time: {result.validation_time:.3f}s")

        # Show detailed validation results
        print(f"\n📋 Detailed Results:")
        print(
            f"  Control Flow: {'✅ PASSED' if result.control_flow_validation['passed'] else '❌ FAILED'}"
        )
        print(
            f"  Behavior Patterns: {'✅ PASSED' if result.behavior_pattern_validation['passed'] else '❌ FAILED'}"
        )
        print(
            f"  Complexity: {'✅ PASSED' if result.complexity_validation['passed'] else '❌ FAILED'}"
        )

        return True

    except Exception as e:
        print(f"❌ Individual method validation failed: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Activity Model Validation Test Suite")
    print("=" * 70)

    # Test 1: Complete workflow
    success1 = test_activity_model_validation()

    # Test 2: Individual method validation
    success2 = test_individual_method_validation()

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Complete Workflow Test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"Individual Method Test: {'✅ PASSED' if success2 else '❌ FAILED'}")

    overall_success = success1 and success2
    print(
        f"\nOverall Test Result: {'🎉 ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print("\n✅ Activity Model Validation System is working correctly!")
        print(
            "🔍 The system can now validate expected vs actual behavior for methods and functions."
        )
        print(
            "🔄 This enables round-trip engineering to maintain behavioral consistency."
        )
    else:
        print("\n❌ Some tests failed. Check the output above for details.")

    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
