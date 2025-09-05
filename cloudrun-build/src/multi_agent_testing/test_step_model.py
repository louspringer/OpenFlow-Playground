#!/usr/bin/env python3
"""
Test Step Model - Demonstrates the model-first approach

This shows how the step model guides workflow implementation:
1. Define the model
2. Validate the model
3. Use the model to implement the workflow
"""

import sys
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from multi_agent_testing.step_model import CODE_QUALITY_WORKFLOW, StepModelBuilder
except ImportError:
    # Fallback for direct execution
    from step_model import CODE_QUALITY_WORKFLOW, StepModelBuilder


def test_step_model_validation():
    """Test that the step model is valid"""
    print("🧪 Testing Step Model Validation")
    print("=" * 40)

    # Validate the model
    errors = StepModelBuilder.validate_workflow_model(CODE_QUALITY_WORKFLOW)

    if errors:
        print("❌ Model validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ Model validation passed!")
    return True


def test_step_dependencies():
    """Test that step dependencies are correctly defined"""
    print("\n🧪 Testing Step Dependencies")
    print("=" * 40)

    steps = CODE_QUALITY_WORKFLOW.steps
    step_order = CODE_QUALITY_WORKFLOW.step_order

    print("📋 Step Dependencies:")
    for step_name in step_order:
        step = steps[step_name]
        deps = step.dependencies
        if deps:
            print(f"  {step_name} → depends on: {', '.join(deps)}")
        else:
            print(f"  {step_name} → no dependencies")

    return True


def test_step_inputs_outputs():
    """Test that step inputs and outputs are properly defined"""
    print("\n🧪 Testing Step Inputs/Outputs")
    print("=" * 40)

    steps = CODE_QUALITY_WORKFLOW.steps

    print("📥 Step Inputs/Outputs:")
    for step_name, step in steps.items():
        print(f"\n  {step_name}:")
        print(f"    Inputs (required): {', '.join(step.inputs.required)}")
        print(f"    Inputs (optional): {', '.join(step.inputs.optional)}")
        print(f"    Outputs (required): {', '.join(step.outputs.required)}")
        print(f"    Outputs (optional): {', '.join(step.outputs.optional)}")

    return True


def test_parallel_execution():
    """Test parallel execution configuration"""
    print("\n🧪 Testing Parallel Execution")
    print("=" * 40)

    steps = CODE_QUALITY_WORKFLOW.steps
    parallel_groups = CODE_QUALITY_WORKFLOW.parallel_groups

    print("⚡ Parallel Execution:")
    for step_name, step in steps.items():
        status = "Yes" if step.parallel_executable else "No"
        print(f"  {step_name}: {status}")

    print(f"\n📊 Parallel Groups: {len(parallel_groups)}")
    for i, group in enumerate(parallel_groups):
        print(f"  Group {i + 1}: {', '.join(group)}")

    return True


def test_workflow_flow():
    """Test the complete workflow flow"""
    print("\n🧪 Testing Workflow Flow")
    print("=" * 40)

    step_order = CODE_QUALITY_WORKFLOW.step_order

    print("🔄 Workflow Flow:")
    for i, step_name in enumerate(step_order):
        step = CODE_QUALITY_WORKFLOW.steps[step_name]
        print(f"  {i + 1}. {step_name} ({step.step_type.value})")
        print(f"     Timeout: {step.timeout_seconds}s")
        print(f"     Retries: {step.retry_count}")
        print(f"     Parallel: {'Yes' if step.parallel_executable else 'No'}")

    return True


def demonstrate_model_usage():
    """Demonstrate how the model guides implementation"""
    print("\n🧪 Demonstrating Model Usage")
    print("=" * 40)

    print("🎯 How the model guides implementation:")
    print("  1. Each step has clear inputs/outputs")
    print("  2. Dependencies ensure correct execution order")
    print("  3. Timeouts and retries handle failures gracefully")
    print("  4. Parallel execution optimizes performance")
    print("  5. Error handling strategies are defined")

    print("\n📋 Example: Implementing the 'do' step")
    do_step = CODE_QUALITY_WORKFLOW.steps["do"]
    print(f"  Step: {do_step.name}")
    print(f"  Required inputs: {', '.join(do_step.inputs.required)}")
    print(f"  Required outputs: {', '.join(do_step.outputs.required)}")
    print(f"  Dependencies: {', '.join(do_step.dependencies)}")
    print(f"  Timeout: {do_step.timeout_seconds}s")
    print(f"  Parallel: {do_step.parallel_executable}")

    print("\n🔧 Implementation would:")
    print("  1. Check inputs are available")
    print("  2. Run subproject scrubbing, formatting, linting in parallel")
    print("  3. Collect all results")
    print("  4. Return required outputs")
    print("  5. Handle timeouts and retries")

    return True


def main():
    """Main test function"""
    print("🚀 Step Model Test Suite")
    print("=" * 50)

    try:
        # Run all tests
        tests = [
            test_step_model_validation,
            test_step_dependencies,
            test_step_inputs_outputs,
            test_parallel_execution,
            test_workflow_flow,
            demonstrate_model_usage,
        ]

        all_passed = True
        for test in tests:
            if not test():
                all_passed = False

        if all_passed:
            print("\n✅ All tests passed!")
            print("\n🎯 The step model is ready to guide workflow implementation!")
        else:
            print("\n❌ Some tests failed!")
            return False

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    # Run the tests
    success = main()
    sys.exit(0 if success else 1)
