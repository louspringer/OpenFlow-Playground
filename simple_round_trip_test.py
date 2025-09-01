#!/usr/bin/env python3
"""
Simple Round-trip test: reverse engineer → generate code → compare results
"""

import json

from round_trip_model_system import RoundTripModelSystem


def load_json_file(file_path: str) -> dict:
    """Load JSON file"""
    with open(file_path) as f:
        return json.load(f)


def fix_reverse_engineered_model(model: dict) -> dict:
    """Fix issues in the reverse engineered model"""
    # Fix the main function signature (remove incorrect 'self' parameter)
    if "module_functions" in model:
        for i, func in enumerate(model["module_functions"]):
            if func.startswith("main(self"):
                model["module_functions"][i] = "main() -> None"

    return model


def create_design_spec_from_model(model: dict) -> dict:
    """Convert reverse engineered model to design spec format"""
    design_spec = {
        "name": model["system_name"],
        "description": model["description"],
        "components": [],
    }

    # Convert components
    for comp_name, comp_data in model["components"].items():
        component = {
            "name": comp_name,
            "type": "class",
            "description": comp_data["responsibility"],
            "requirements": [comp_data["responsibility"]],
            "dependencies": [],
            "metadata": {"methods": comp_data["methods"]},
        }
        design_spec["components"].append(component)

    return design_spec


def run_round_trip_test() -> None:
    """Run the complete round-trip test"""
    print("🔄 Starting Round-Trip Test")
    print("=" * 50)

    # Step 1: Load the reverse engineered model
    print("\n📥 Step 1: Loading reverse engineered model")
    model = load_json_file("reverse_engineered_model_enhanced.json")

    # Fix issues in the model
    model = fix_reverse_engineered_model(model)
    print(f"   ✅ Loaded model: {model['system_name']}")
    print(f"   📦 Components: {len(model['components'])}")

    # Step 2: Convert to design spec format
    print("\n🔄 Step 2: Converting to design spec format")
    design_spec = create_design_spec_from_model(model)

    # Save design spec for inspection
    with open("round_trip_design_spec.json", "w") as f:
        json.dump(design_spec, f, indent=2)
    print("   ✅ Created design spec")

    # Step 3: Generate code from the design spec
    print("\n🚀 Step 3: Generating code from design spec")

    try:
        # Create the system
        system = RoundTripModelSystem()

        # Generate code
        model_obj = system.create_model_from_design(design_spec)
        generated_files = system.generate_code_from_model(model_obj.name)

        print("   ✅ Code generation successful")
        print(f"   📁 Generated {len(generated_files)} files")

        # Save the generated files for inspection
        for filename, content in generated_files.items():
            with open(f"round_trip_{filename}", "w") as f:
                f.write(content)
            print(f"      💾 {filename}")

    except Exception as e:
        print(f"   ❌ Code generation failed: {e}")
        return

    # Step 4: Compare the files
    print("\n🔍 Step 4: Comparing original vs generated code")

    try:
        # Load original file
        with open("scripts/simple_calculator.py") as f:
            original_content = f.read()

        # Load generated Calculator file
        with open("round_trip_Calculator.py") as f:
            generated_content = f.read()

        # Heuristic checks
        print("\n📊 Heuristic Analysis:")

        # Check 1: File structure
        original_lines = original_content.split("\n")
        generated_lines = generated_content.split("\n")
        print(f"   📏 Original lines: {len(original_lines)}")
        print(f"   📏 Generated lines: {len(generated_lines)}")

        # Check 2: Class count
        original_classes = original_content.count("class ")
        generated_classes = generated_content.count("class ")
        print(f"   🏗️  Original classes: {original_classes}")
        print(f"   🏗️  Generated classes: {generated_classes}")

        # Check 3: Method count
        original_methods = original_content.count("def ")
        generated_methods = generated_content.count("def ")
        print(f"   ⚙️  Original methods: {original_methods}")
        print(f"   ⚙️  Generated methods: {generated_methods}")

        # Check 4: Key functionality
        calc_methods = ["add", "subtract", "multiply", "divide"]
        original_has_calc = all(method in original_content for method in calc_methods)
        generated_has_calc = all(method in generated_content for method in calc_methods)

        print(f"   🧮 Original has calculator methods: {original_has_calc}")
        print(f"   🧮 Generated has calculator methods: {generated_has_calc}")

        # Check 5: Type annotations
        original_types = original_content.count("->")
        generated_types = generated_content.count("->")
        print(f"   🏷️  Original type annotations: {original_types}")
        print(f"   🏷️  Generated type annotations: {generated_types}")

        # Check 6: Return statements
        original_returns = original_content.count("return ")
        generated_returns = generated_content.count("return ")
        print(f"   ↩️  Original return statements: {original_returns}")
        print(f"   ↩️  Generated return statements: {generated_returns}")

        # Overall assessment
        print("\n🎯 Functional Equivalence Assessment:")

        structure_match = original_classes == generated_classes and abs(original_methods - generated_methods) <= 1

        functionality_match = original_has_calc == generated_has_calc and original_types == generated_types

        if structure_match and functionality_match:
            print("   ✅ FUNCTIONALLY EQUIVALENT - Round-trip successful!")
        else:
            print("   ❌ NOT FUNCTIONALLY EQUIVALENT - Round-trip failed!")

        if not structure_match:
            print("   ⚠️  Structure mismatch detected")
        if not functionality_match:
            print("   ⚠️  Functionality mismatch detected")

    except Exception as e:
        print(f"   ❌ Comparison failed: {e}")

    print("\n" + "=" * 50)
    print("🔄 Round-Trip Test Complete")


if __name__ == "__main__":
    run_round_trip_test()
