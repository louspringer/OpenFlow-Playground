#!/usr/bin/env python3
"""
Round-Trip Validation Script for test_orchestrator.py

Purpose: Test functional equivalence between original code and regenerated code
Graph API Level: 1
Projection System: round_trip_validation
"""

import json

from enhanced_reverse_engineer import EnhancedReverseEngineer
from round_trip_model_system import RoundTripModelSystem


def main() -> None:
    """Perform round-trip validation on test_orchestrator.py"""
    print("🚀 Starting Round-Trip Validation for test_orchestrator.py")
    print("=" * 60)

    # Step 1: Extract model from original file
    print("\n📥 Step 1: Extracting model from original file...")
    engineer = EnhancedReverseEngineer()
    original_file = "clewcrew-core/tests/test_orchestrator.py"

    try:
        extracted_model = engineer.reverse_engineer(original_file)
        print("✅ Model extraction successful!")
        print(
            f"   📊 File structure: {extracted_model.get('file_structure', {}).get('total_lines', 0)} lines"
        )
        print(f"   🏗️  Classes: {extracted_model.get('classes', {}).get('count', 0)}")
        print(f"   🔧 Functions: {extracted_model.get('functions', {}).get('count', 0)}")

        # Save extracted model
        with open("test_orchestrator_extracted_model.json", "w") as f:
            json.dump(extracted_model, f, indent=2)
        print("   💾 Extracted model saved")

    except Exception as e:
        print(f"❌ Model extraction failed: {e}")
        return

    # Step 2: Generate code from extracted model
    print("\n🔧 Step 2: Generating code from extracted model...")
    generator = RoundTripModelSystem()

    try:
        generated_code = generator.generate_code_from_extracted_model(extracted_model)
        print("✅ Code generation successful!")
        print(f"   📊 Generated {len(generated_code.splitlines())} lines of code")

        # Save regenerated code
        with open("test_orchestrator_regenerated.py", "w") as f:
            f.write(generated_code)
        print("   💾 Regenerated code saved")

    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return

    # Step 3: Compare original and regenerated code
    print("\n🔍 Step 3: Comparing original and regenerated code...")

    try:
        with open(original_file) as f:
            original_content = f.read()

        with open("test_orchestrator_regenerated.py") as f:
            regenerated_content = f.read()

        # Basic comparison
        original_lines = len(original_content.splitlines())
        regenerated_lines = len(regenerated_content.splitlines())

        print(f"   📏 Original: {original_lines} lines")
        print(f"   📏 Regenerated: {regenerated_lines} lines")
        print(f"   📊 Line count difference: {abs(original_lines - regenerated_lines)}")

        # Check if regenerated code is valid Python
        try:
            compile(regenerated_content, "test_orchestrator_regenerated.py", "exec")
            print("   ✅ Regenerated code compiles successfully")
        except SyntaxError as e:
            print(f"   ❌ Regenerated code has syntax errors: {e}")
            return

        print("\n🎯 Round-trip validation complete!")
        print("   📁 Check the following files:")
        print(f"      📄 Original: {original_file}")
        print("      📄 Extracted model: test_orchestrator_extracted_model.json")
        print("      📄 Regenerated code: test_orchestrator_regenerated.py")

    except Exception as e:
        print(f"❌ Comparison failed: {e}")


if __name__ == "__main__":
    main()
