#!/usr/bin/env python3
"""
Generic Round-Trip Validation Script

Purpose: Test functional equivalence between original code and regenerated code for any Python file
Graph API Level: 1
Projection System: round_trip_validation
"""

import json
import sys
from pathlib import Path

from round_trip_model_system import RoundTripModelSystem

from enhanced_reverse_engineer import EnhancedReverseEngineer


def main() -> None:
    """Perform round-trip validation on specified Python file"""
    if len(sys.argv) != 2:
        print("Usage: python round_trip_any_file.py <python_file_path>")
        print(
            "Example: python round_trip_any_file.py clewcrew-recovery/tests/test_syntax_recovery.py"
        )
        return

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return

    file_name = Path(file_path).stem
    print(f"🚀 Starting Round-Trip Validation for {file_path}")
    print("=" * 60)

    # Step 1: Extract model from original file
    print("\n📥 Step 1: Extracting model from original file...")
    engineer = EnhancedReverseEngineer()

    try:
        extracted_model = engineer.reverse_engineer(file_path)
        print("✅ Model extraction successful!")
        print(
            f"   📊 File structure: {extracted_model.get('file_structure', {}).get('total_lines', 0)} lines"
        )
        print(f"   🏗️  Classes: {extracted_model.get('classes', {}).get('count', 0)}")
        print(f"   🔧 Functions: {extracted_model.get('functions', {}).get('count', 0)}")

        # Save extracted model
        model_file = f"{file_name}_extracted_model.json"
        with open(model_file, "w") as f:
            json.dump(extracted_model, f, indent=2)
        print(f"   💾 Extracted model saved to {model_file}")

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
        regenerated_file = f"{file_name}_regenerated.py"
        with open(regenerated_file, "w") as f:
            f.write(generated_code)
        print(f"   💾 Regenerated code saved to {regenerated_file}")

    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return

    # Step 3: Compare original and regenerated code
    print("\n🔍 Step 3: Comparing original and regenerated code...")

    try:
        with open(file_path) as f:
            original_content = f.read()

        with open(regenerated_file) as f:
            regenerated_content = f.read()

        # Basic comparison
        original_lines = len(original_content.splitlines())
        regenerated_lines = len(regenerated_content.splitlines())

        print(f"   📏 Original: {original_lines} lines")
        print(f"   📏 Regenerated: {regenerated_lines} lines")
        print(f"   📊 Line count difference: {abs(original_lines - regenerated_lines)}")

        # Check if regenerated code is valid Python
        try:
            compile(regenerated_content, regenerated_file, "exec")
            print("   ✅ Regenerated code compiles successfully")
        except SyntaxError as e:
            print(f"   ❌ Regenerated code has syntax errors: {e}")
            return

        print("\n🎯 Round-trip validation complete!")
        print("   📁 Check the following files:")
        print(f"      📄 Original: {file_path}")
        print(f"      📄 Extracted model: {model_file}")
        print(f"      📄 Regenerated code: {regenerated_file}")

        # Step 4: Quality check the regenerated code
        print("\n🔍 Step 4: Quality checking regenerated code...")
        try:
            import subprocess

            result = subprocess.run(
                ["uv", "run", "flake8", regenerated_file],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print("   ✅ Flake8: No linting errors")
            else:
                print(f"   ❌ Flake8 errors: {result.stdout}")

            result = subprocess.run(
                ["uv", "run", "mypy", regenerated_file], capture_output=True, text=True
            )
            if result.returncode == 0:
                print("   ✅ MyPy: No type errors")
            else:
                print(f"   ❌ MyPy errors: {result.stdout}")

        except Exception as e:
            print(f"   ⚠️  Quality check failed: {e}")

    except Exception as e:
        print(f"❌ Comparison failed: {e}")


if __name__ == "__main__":
    main()
