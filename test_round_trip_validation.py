#!/usr/bin/env python3
"""
Simple test file for round-trip validation testing.
"""


def simple_function():
    """A simple function for testing."""
    x = 1
    y = 2
    result = x + y
    print(f"Result: {result}")
    return result


def another_function():
    """Another function for testing."""
    data = [1, 2, 3, 4, 5]
    total = sum(data)
    print(f"Total: {total}")
    return total


class TestClass:
    """A simple test class."""

    def __init__(self):
        self.value = 42

    def get_value(self):
        """Get the stored value."""
        return self.value

    def set_value(self, new_value):
        """Set a new value."""
        self.value = new_value
        return self.value


if __name__ == "__main__":
    # Test the functions
    result1 = simple_function()
    result2 = another_function()

    # Test the class
    obj = TestClass()
    print(f"Object value: {obj.get_value()}")
    obj.set_value(100)
    print(f"New value: {obj.get_value()}")


# Test round-trip validation
def test_round_trip():
    """Test round-trip validation with this file."""
    from src.round_trip_validation import RoundTripValidator

    validator = RoundTripValidator()

    # Create a mock extracted model based on what we know should be in this file
    mock_model = {
        "functions": [
            {"name": "simple_function"},
            {"name": "another_function"},
            {"name": "test_round_trip"},
        ],
        "classes": [{"name": "TestClass"}],
        "calls": [
            {"function": "print"},
            {"function": "sum"},
            {"function": "simple_function"},
            {"function": "another_function"},
            {"function": "obj.get_value"},
            {"function": "obj.set_value"},
        ],
        "imports": [{"name": "src.round_trip_validation.RoundTripValidator"}],
        "control_flow": [{"type": "If"}],
    }

    # Run validation against this file
    result = validator.validate_workflow_extraction(__file__, mock_model)

    print("\n" + "=" * 50)
    print("ROUND-TRIP VALIDATION TEST")
    print("=" * 50)
    print(f"Testing file: {__file__}")
    print(f"Validation passed: {result.get('validation_passed', False)}")
    print(
        f"Overall accuracy: {result.get('accuracy_metrics', {}).get('overall_accuracy', 0):.2%}"
    )

    # Print detailed results
    if "accuracy_metrics" in result:
        metrics = result["accuracy_metrics"]
        print(f"\nDetailed Metrics:")
        print(f"  Function accuracy: {metrics.get('function_accuracy', 0):.2%}")
        print(f"  Class accuracy: {metrics.get('class_accuracy', 0):.2%}")
        print(f"  Call accuracy: {metrics.get('call_accuracy', 0):.2%}")
        print(f"  Import accuracy: {metrics.get('import_accuracy', 0):.2%}")
        print(f"  Control flow accuracy: {metrics.get('control_flow_accuracy', 0):.2%}")

    return result


if __name__ == "__main__":
    # Run the round-trip test
    test_round_trip()
