#!/usr/bin/env python3
"""Test model generation from the round trip model system"""

import json

from round_trip_model_system import RoundTripModelSystem


def main():
    # Load the model
    with open("round_trip_regression_test_model.json") as f:
        model = json.load(f)

    # Create the system
    system = RoundTripModelSystem()

    # Create model from design
    result = system.create_model_from_design(model)
    print(f"✅ Created model: {result.name}")
    print(f"📦 Components: {len(result.components)}")

    # Generate code from model
    generated_files = system.generate_code_from_model(result.name)
    print(f"🚀 Generated {len(generated_files)} files")

    # Show generated code
    for filename, content in generated_files.items():
        print(f"\n{'=' * 50}")
        print(f"📄 {filename}")
        print(f"{'=' * 50}")
        print(content[:1000] + "..." if len(content) > 1000 else content)


if __name__ == "__main__":
    main()
