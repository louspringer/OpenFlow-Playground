#!/usr/bin/env python3
"""
Test Script: Profiling + Activity Model Validation Hypothesis

This script demonstrates the hypothesis that if our activity modeling is correct,
the profiling trace should match our activity model predictions.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from round_trip_engineering.enhanced_reverse_engineer import EnhancedReverseEngineer
from round_trip_engineering.activity_model_validator import ActivityModelValidator


def test_profiling_activity_validation_hypothesis():
    """Test the hypothesis: profiling trace should match activity model predictions."""

    print("🧪 Testing Profiling + Activity Model Validation Hypothesis")
    print("=" * 70)

    # File to test
    source_file = "src/round_trip_engineering/enhanced_reverse_engineer.py"

    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return

    print(f"📄 Testing with source file: {source_file}")
    print()

    # Step 1: Reverse engineer with profiling
    print("🔄 STEP 1: Reverse Engineering with Profiling")
    print("-" * 50)

    reverse_engineer = EnhancedReverseEngineer()
    extracted_model = reverse_engineer.reverse_engineer_file(source_file)

    print(f"✅ Extracted model with {len(extracted_model.get('components', {}))} components")

    # Step 2: Get execution trace from profiling
    print("\n📊 STEP 2: Execution Trace from Profiling")
    print("-" * 50)

    execution_trace = reverse_engineer.get_execution_trace()
    performance_summary = reverse_engineer.get_performance_summary()

    print(f"📈 Total function calls: {performance_summary.get('total_function_calls', 0)}")
    print(f"⏱️  Total execution time: {performance_summary.get('total_execution_time', 0):.6f}s")
    print(f"🐌 Average time per call: {performance_summary.get('average_time_per_call', 0):.6f}s")

    print("\n🔍 Top 5 Bottlenecks:")
    for i, bottleneck in enumerate(performance_summary.get("bottlenecks", [])[:5]):
        print(f"  {i+1}. {bottleneck['function']} - {bottleneck['cumulative_time']:.6f}s ({bottleneck['call_count']} calls)")

    print("\n📞 Most Called Functions:")
    for i, func in enumerate(performance_summary.get("most_called_functions", [])[:5]):
        print(f"  {i+1}. {func['function']} - {func['call_count']} calls")

    # Step 3: Extract activity models from reverse engineering
    print("\n🎯 STEP 3: Activity Model Extraction")
    print("-" * 50)

    # Extract activity models that were already generated during reverse engineering
    activity_models = {}

    components = extracted_model.get("components", {})
    for component_name, component_info in components.items():
        methods = component_info.get("methods", [])
        for method in methods:
            method_name = method.get("name", "unknown")
            # Extract the activity model that was already generated during reverse engineering
            activity_model = method.get("activity_model", {})
            if activity_model:
                activity_models[f"{component_name}.{method_name}"] = activity_model

    print(f"✅ Found {len(activity_models)} activity models from reverse engineering")

    # Step 4: Validate activity models
    print("\n🔍 STEP 4: Activity Model Validation")
    print("-" * 50)

    validator = ActivityModelValidator()
    validation_results = {}

    for method_name, method_info in activity_models.items():
        # Get the full method info from the component
        component_name = method_name.split(".")[0]
        method_name_only = method_name.split(".")[1]

        # Find the method in the component
        component_methods = components[component_name].get("methods", [])
        method_info_full = next((m for m in component_methods if m.get("name") == method_name_only), None)

        if method_info_full:
            validation_result = validator.validate_method_activity_model(method_info_full)
            validation_results[method_name] = validation_result

    print(f"✅ Validated {len(validation_results)} activity models")

    # Step 5: Compare profiling trace with activity models
    print("\n🔍 STEP 5: Profiling Trace vs Activity Model Comparison")
    print("-" * 50)

    print("🎯 Hypothesis: Profiling trace should match activity model predictions")
    print()

    # Analyze the relationship between profiling and activity models
    trace_functions = {item["function"] for item in execution_trace}
    activity_functions = {name.split(".")[-1] for name in activity_models.keys()}

    print("📊 Function Coverage Analysis:")
    print(f"  Functions in profiling trace: {len(trace_functions)}")
    print(f"  Functions in activity models: {len(activity_functions)}")

    # Find functions that appear in both
    common_functions = trace_functions.intersection(activity_functions)
    print(f"  Functions in both: {len(common_functions)}")

    # Find functions only in profiling
    profiling_only = trace_functions - activity_functions
    print(f"  Functions only in profiling: {len(profiling_only)}")

    # Find functions only in activity models
    activity_only = activity_functions - trace_functions
    print(f"  Functions only in activity models: {len(activity_only)}")

    print()

    # Step 6: Detailed analysis of key functions
    print("🔍 STEP 6: Detailed Function Analysis")
    print("-" * 50)

    print("📈 High-Impact Functions (High cumulative time):")
    for bottleneck in performance_summary.get("bottlenecks", [])[:3]:
        func_name = bottleneck["function"]
        cumulative_time = bottleneck["cumulative_time"]
        call_count = bottleneck["call_count"]

        # Check if we have an activity model for this function
        has_activity_model = any(func_name in name for name in activity_models.keys())

        print(f"  🎯 {func_name}:")
        print(f"    ⏱️  Cumulative time: {cumulative_time:.6f}s")
        print(f"    📞 Call count: {call_count}")
        print(f"    📋 Activity model: {'✅ Yes' if has_activity_model else '❌ No'}")

        if has_activity_model:
            # Find the activity model
            activity_model = next((am for name, am in activity_models.items() if func_name in name), None)
            if activity_model:
                complexity = activity_model.get("complexity_score", 0)
                control_flow = activity_model.get("control_flow", {})
                print(f"    🧠 Complexity score: {complexity}")
                print(f"    🔄 Control flow patterns: {len(control_flow)}")

    print()

    # Step 7: Validation of the hypothesis
    print("🎯 STEP 7: Hypothesis Validation")
    print("-" * 50)

    # Calculate correlation metrics
    total_functions = len(trace_functions.union(activity_functions))
    overlap_ratio = len(common_functions) / total_functions if total_functions > 0 else 0

    print(f"📊 Overlap Analysis:")
    print(f"  Total unique functions: {total_functions}")
    print(f"  Functions in both: {len(common_functions)}")
    print(f"  Overlap ratio: {overlap_ratio:.2%}")

    print("\n🎯 Hypothesis Assessment:")
    if overlap_ratio >= 0.8:
        print("  ✅ STRONG SUPPORT: High overlap between profiling trace and activity models")
        print("  💡 This suggests our activity modeling accurately predicts execution behavior")
    elif overlap_ratio >= 0.6:
        print("  ⚠️  MODERATE SUPPORT: Moderate overlap between profiling trace and activity models")
        print("  💡 Some functions may be missing from activity models or profiling")
    else:
        print("  ❌ WEAK SUPPORT: Low overlap between profiling trace and activity models")
        print("  💡 This suggests our activity modeling may not accurately predict execution behavior")

    print()

    # Step 8: Recommendations
    print("💡 STEP 8: Recommendations")
    print("-" * 50)

    if profiling_only:
        print("🔍 Functions in profiling but not in activity models:")
        for func in sorted(profiling_only)[:5]:
            print(f"  - {func}")
        if len(profiling_only) > 5:
            print(f"  ... and {len(profiling_only) - 5} more")
        print("  💡 Consider adding activity models for these functions")

    if activity_only:
        print("\n📋 Functions in activity models but not in profiling:")
        for func in sorted(activity_only)[:5]:
            print(f"  - {func}")
        if len(activity_only) > 5:
            print(f"  ... and {len(activity_only) - 5} more")
        print("  💡 These functions may not be called during reverse engineering")

    print("\n🎯 Next Steps:")
    print("  1. Analyze functions with high cumulative time but no activity models")
    print("  2. Improve activity model coverage for frequently called functions")
    print("  3. Use profiling data to prioritize which functions need better modeling")
    print("  4. Validate that activity models accurately predict execution patterns")

    print("\n🎉 Hypothesis testing completed!")

    return {
        "overlap_ratio": overlap_ratio,
        "total_functions": total_functions,
        "common_functions": len(common_functions),
        "profiling_only": len(profiling_only),
        "activity_only": len(activity_only),
    }


if __name__ == "__main__":
    try:
        results = test_profiling_activity_validation_hypothesis()
        print(f"\n📊 Final Results: {results}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
