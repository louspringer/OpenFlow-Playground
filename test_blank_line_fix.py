#!/usr/bin/env python3
"""
Test the blank line fix in the generator
"""

from round_trip_model_system import RoundTripModelSystem


def main():
    """Test the generator with a simple model"""
    print("🧪 Testing blank line fix...")

    # Create a simple test model
    test_model = {
        "system_name": "TestSystem",
        "description": "Test system for blank line fix",
        "purpose": "Testing",
        "components": {
            "TestClass": {
                "responsibility": "Test class",
                "methods": [
                    {
                        "name": "test_method",
                        "docstring": "Test method",
                        "return_type": "None",
                        "parameters": [],
                    }
                ],
                "class_decorators": [],
                "bases": [],
            }
        },
        "imports": [],
        "used_names": [],
        "module_assignments": {},
        "file_metadata": {"file_type": "module"},
    }

    # Test the generator
    system = RoundTripModelSystem()
    generated_code = system.generate_code_from_extracted_model(test_model)

    # Check for blank line issues
    lines = generated_code.split("\n")
    blank_line_count = 0
    consecutive_blank_lines = 0

    for line in lines:
        if line.strip() == "":
            blank_line_count += 1
            consecutive_blank_lines += 1
        else:
            consecutive_blank_lines = 0

    print("📊 Blank line analysis:")
    print(f"  Total blank lines: {blank_line_count}")
    print(f"  Max consecutive blank lines: {consecutive_blank_lines}")

    if consecutive_blank_lines <= 2:
        print("✅ Blank line fix successful!")
        return 0
    print("❌ Blank line fix failed!")
    return 1


if __name__ == "__main__":
    exit(main())
