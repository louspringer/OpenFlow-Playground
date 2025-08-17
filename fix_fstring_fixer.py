#!/usr/bin/env python3
"""Script to regenerate the deterministic f-string fixer"""

import json
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path.cwd()))

from round_trip_model_system import RoundTripModelSystem


def main():
    """Regenerate the deterministic f-string fixer"""
    print("🔧 Regenerating deterministic f-string fixer...")

    # Load the extracted model
    with open("enhanced_reverse_engineered_model.json") as f:
        extracted_model = json.load(f)

    # Create the round-trip system
    system = RoundTripModelSystem()

    # Generate code from the extracted model
    generated_code = system.generate_code_from_extracted_model(extracted_model)

    # Write the regenerated code
    with open("scripts/deterministic_fstring_fixer.py", "w") as f:
        f.write(generated_code)

    print("✅ Deterministic f-string fixer regenerated successfully!")


if __name__ == "__main__":
    main()
