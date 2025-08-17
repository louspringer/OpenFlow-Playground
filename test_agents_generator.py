#!/usr/bin/env python3
"""
Test the enhanced generator with agents.py file
"""

import json

from round_trip_model_system import RoundTripModelSystem


def main():
    """Test the enhanced generator with agents.py"""
    print("🧪 Testing enhanced generator with agents.py...")

    # First, reverse engineer the agents.py file
    import subprocess

    try:
        subprocess.run(
            [
                "python",
                "enhanced_reverse_engineer.py",
                "subprojects/tidb-agentx-hackathon/src/tidb_agentx_hackathon/agents.py",
            ],
            check=True,
        )
        print("✅ Reverse engineered agents.py")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to reverse engineer agents.py: {e}")
        return

    # Load the enhanced generator
    system = RoundTripModelSystem()

    # Load the reverse engineered model
    with open("enhanced_reverse_engineered_model.json") as f:
        model = json.load(f)

    # Generate fixed code
    generated_code = system.generate_code_from_extracted_model(model)

    # Save the test version
    with open("test_enhanced_agents.py", "w") as f:
        f.write(generated_code)

    print("✅ Generated test_enhanced_agents.py")

    # Check if the generated code contains the necessary imports
    if "from pydantic import BaseModel" in generated_code:
        print("✅ BaseModel import detected")
    else:
        print("❌ BaseModel import missing")

    if "from enum import Enum" in generated_code:
        print("✅ Enum import detected")
    else:
        print("❌ Enum import missing")

    if "Optional" in generated_code and "from typing import" in generated_code:
        print("✅ Optional import detected")
    else:
        print("❌ Optional import missing")


if __name__ == "__main__":
    main()
