#!/usr/bin/env python3
"""
Fix auto_format_all.py using the canonical round-trip system
"""

import json

from round_trip_model_system import RoundTripModelSystem


def main():
    """Fix the auto_format_all.py file"""

    # Load the enhanced reverse engineered model
    with open("enhanced_reverse_engineered_model.json") as f:
        model = json.load(f)

    # Use the canonical round-trip system
    system = RoundTripModelSystem()

    # Use the CORRECT method: generate_code_from_extracted_model
    generated_code = system.generate_code_from_extracted_model(model)

    # Write the regenerated code
    with open("auto_format_all_regenerated.py", "w") as f:
        f.write(generated_code)

    print("✅ Successfully regenerated auto_format_all.py")
    print("📁 Output: auto_format_all_regenerated.py")


if __name__ == "__main__":
    main()
