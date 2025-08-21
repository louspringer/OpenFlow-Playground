#!/usr/bin/env python3
"""
Debug script to test V3 directly
"""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from round_trip_engineering.enhanced_reverse_engineer_v3 import (
    EnhancedReverseEngineerV3,
)


def test_v3_directly():
    """Test V3 with a simple file"""

    # Create a simple test file
    content = """class TestClass:
    def test_method(self):
        pass

def test_function():
    pass
"""

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(content)
        temp_file = f.name

    try:
        print(f"📝 Created test file: {temp_file}")
        print(f"📄 Content:\n{content}")

        # Test V3
        engineer = EnhancedReverseEngineerV3()
        result = engineer.reverse_engineer_file(temp_file)

        print(f"\n🔍 V3 Result Keys: {list(result.keys())}")
        print(f"📦 Classes: {result.get('classes', 'NOT FOUND')}")
        print(f"🔧 Functions: {result.get('functions', 'NOT FOUND')}")

        # Check if keys exist
        if "classes" in result:
            print("✅ 'classes' key found")
        else:
            print("❌ 'classes' key missing")

        if "functions" in result:
            print("✅ 'functions' key found")
        else:
            print("❌ 'functions' key missing")

    finally:
        import os

        os.unlink(temp_file)


if __name__ == "__main__":
    test_v3_directly()
