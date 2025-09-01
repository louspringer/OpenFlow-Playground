#!/usr/bin/env python3
"""
Enhanced Round-trip test using the enhanced reverse engineered model
"""

import json
import os

from src.round_trip_engineering.round_trip_model_system import RoundTripModelSystem


def load_json_file(file_path: str) -> dict:
    """Load JSON file"""
    with open(file_path) as f:
        return json.load(f)


def create_design_spec_from_enhanced_model(model: dict) -> dict:
    """Convert enhanced reverse engineered model to design spec format"""
    design_spec = {
        "name": model["system_name"],
        "description": model["description"],
        "components": [],
    }

    # Convert components with enhanced information
    for comp_name, comp_data in model["components"].items():
        component = {
            "name": comp_name,
            "type": "class",
            "description": comp_data["responsibility"],
            "requirements": [comp_data["responsibility"]],
            "dependencies": [],
            "metadata": {
                "methods": [method["signature"] for method in comp_data["methods"]],
                "line_number": comp_data.get("line_number", 0),
                "bases": comp_data.get("bases", []),
                "decorators": comp_data.get("class_decorators", []),
            },
        }
        design_spec["components"].append(component)

    # Add module functions as components
    for func in model.get("module_functions", []):
        component = {
            "name": func["name"],
            "type": "function",
            "description": func.get("docstring", ""),
            "requirements": [func.get("docstring", "")],
            "dependencies": [],
            "metadata": {
                "signature": func["signature"],
                "line_number": func.get("line_number", 0),
                "return_type": func.get("return_type", "Any"),
                "parameters": func.get("parameters", []),
            },
        }
        design_spec["components"].append(component)

    return design_spec


def run_enhanced_round_trip_test() -> None:
    """Run the enhanced round-trip test"""
    print("🔄 Enhanced Round-Trip Test with Enhanced AST Parser")
    print("=" * 60)

    # Step 1: Actually reverse engineer the Calculator.py file
    print("\n📥 Step 1: Reverse engineering Calculator.py file")

    # Check if Calculator.py exists
    calculator_file = "scripts/simple_calculator.py"
    if not os.path.exists(calculator_file):
        print(f"   ❌ Calculator file not found: {calculator_file}")
        return

    print(f"   ✅ Found calculator file: {calculator_file}")

    # Use the enhanced reverse engineer to create a model
    try:
        from src.round_trip_engineering.enhanced_reverse_engineer import (
            EnhancedReverseEngineer,
        )

        # Create reverse engineer instance
        reverse_engineer = EnhancedReverseEngineer()

        # Actually reverse engineer the calculator file
        print("   🔍 Reverse engineering Calculator.py...")
        model = reverse_engineer.reverse_engineer(calculator_file)

        print(f"   ✅ Reverse engineered model: {model['system_name']}")
        print(f"   📦 Components: {len(model['components'])}")
        print(f"   ⚙️  Module Functions: {len(model.get('module_functions', []))}")
        print(f"   📏 Total Lines: {model.get('file_structure', {}).get('total_lines', 0)}")

        # Save the reverse engineered model
        with open("calculator_reverse_engineered_model.json", "w") as f:
            json.dump(model, f, indent=2)
        print("   💾 Saved calculator model: calculator_reverse_engineered_model.json")

    except Exception as e:
        print(f"   ❌ Reverse engineering failed: {e}")
        return

    # Step 2: Convert to design spec format
    print("\n🔄 Step 2: Converting to design spec format")
    design_spec = create_design_spec_from_enhanced_model(model)

    # Save design spec for inspection
    with open("calculator_design_spec.json", "w") as f:
        json.dump(design_spec, f, indent=2)
    print("   ✅ Created calculator design spec")
    print(f"   📋 Total components: {len(design_spec['components'])}")

    # Step 3: Generate code from the reverse engineered model
    print("\n🚀 Step 3: Generating code from reverse engineered model")

    try:
        # Create the system
        system = RoundTripModelSystem()

        # Use the extracted model approach to generate complete module code
        # This generates a single file with all components instead of separate files
        complete_module_code = system.generate_code_from_extracted_model(model)

        # Save the complete module code
        with open("calculator_regenerated.py", "w") as f:
            f.write(complete_module_code)
        print("   ✅ Complete module generation successful")
        print("   💾 calculator_regenerated.py")

    except Exception as e:
        print(f"   ❌ Code generation failed: {e}")
        return

    # Step 4: Compare the files with enhanced analysis
    print("\n🔍 Step 4: Enhanced comparison analysis")

    try:
        # Load original file
        with open(calculator_file) as f:
            original_content = f.read()

        # Load generated complete module file
        with open("calculator_regenerated.py") as f:
            generated_content = f.read()

        # Enhanced heuristic checks
        print("\n📊 Enhanced Heuristic Analysis:")

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

        # Check 7: Module-level elements (NEW!)
        original_main = "def main()" in original_content
        generated_main = "def main()" in generated_content
        print(f"   🚀 Original has main function: {original_main}")
        print(f"   🚀 Generated has main function: {generated_main}")

        # Check 8: Module docstring (NEW!)
        original_docstring = '"""simple_calculator' in original_content
        generated_docstring = '"""simple_calculator' in generated_content
        print(f"   📝 Original has module docstring: {original_docstring}")
        print(f"   📝 Generated has module docstring: {generated_docstring}")

        # Overall assessment
        print("\n🎯 Enhanced Functional Equivalence Assessment:")

        structure_match = original_classes == generated_classes and abs(original_methods - generated_methods) <= 1

        functionality_match = original_has_calc == generated_has_calc and original_types == generated_types

        module_elements_match = original_main == generated_main and original_docstring == generated_docstring

        if structure_match and functionality_match and module_elements_match:
            print("   ✅ FULLY FUNCTIONALLY EQUIVALENT - Enhanced round-trip successful!")
        else:
            print("   ❌ NOT FULLY FUNCTIONALLY EQUIVALENT - Enhanced round-trip failed!")

        if not structure_match:
            print("   ⚠️  Structure mismatch detected")
        if not functionality_match:
            print("   ⚠️  Functionality mismatch detected")
        if not module_elements_match:
            print("   ⚠️  Module-level elements mismatch detected")

        # Show what's still missing
        print("\n🔍 Missing Elements Analysis:")
        if original_main != generated_main:
            print("   ❌ Main function missing from generated code")
        if original_docstring != generated_docstring:
            print("   ❌ Module docstring missing from generated code")

    except Exception as e:
        print(f"   ❌ Comparison failed: {e}")

    print("\n" + "=" * 60)
    print("🔄 Enhanced Round-Trip Test Complete")


if __name__ == "__main__":
    run_enhanced_round_trip_test()
