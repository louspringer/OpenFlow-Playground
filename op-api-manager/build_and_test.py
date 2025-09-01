#!/usr/bin/env python3
"""
Simple build and test script for op-api-manager package.
"""

import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False


def main():
    """Main build and test function."""
    print("🚀 OP API Manager - Build and Test")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Make sure you're in the op-api-manager directory.")
        return 1

    # Install in development mode
    if not run_command("pip install -e .", "Installing package in development mode"):
        return 1

    # Install test dependencies
    if not run_command("pip install -e '.[test]'", "Installing test dependencies"):
        return 1

    # Run tests
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        return 1

    # Check if CLI works
    if not run_command("op-api-manager --help", "Testing CLI help command"):
        return 1

    # Try to import the package
    try:
        print("🔍 Testing package import...")
        from op_api_manager import CacheConfig, OnePasswordAPIKeyManager

        print("✅ Package import successful")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return 1

    print("\n🎉 Build and test completed successfully!")
    print("💡 You can now:")
    print("   • Run: op-api-manager --help")
    print("   • Import: from op_api_manager import OnePasswordAPIKeyManager")
    print("   • Test: python -m pytest tests/")

    return 0


if __name__ == "__main__":
    exit(main())
