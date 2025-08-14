#!/usr/bin/env python3
"""Secure CLI tool for code quality automation"""

import subprocess
import sys
from pathlib import Path


def run_command_safe(cmd_list, description, cwd=None):
    """Run a command safely without shell=True"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        print(f"⚠️ {description} completed with issues")
        if result.stderr:
            print(f"   Stderr: {result.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False


def main():
    """Main automation sequence"""
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target_dir).resolve()

    print("🎯 Secure Code Quality Automation Tool")
    print(f"🎯 Target Directory: {target_path}")
    print("🎯 Starting automated quality improvement...")

    # Step 1: Black formatting
    black_cmd = ["python3", "-m", "black", ".", "--line-length", "88"]
    black_success = run_command_safe(black_cmd, "Black formatting", cwd=target_path)

    # Step 2: Ruff linting with auto-fixes
    ruff_cmd = ["python3", "-m", "ruff", "check", ".", "--fix", "--unsafe-fixes"]
    ruff_success = run_command_safe(
        ruff_cmd, "Ruff linting with auto-fixes", cwd=target_path
    )

    # Step 3: Check remaining issues
    check_cmd = ["python3", "-m", "ruff", "check", ".", "--output-format", "concise"]
    print("\n🔍 Checking remaining issues...")
    try:
        result = subprocess.run(
            check_cmd, capture_output=True, text=True, cwd=target_path
        )
        if result.returncode == 0:
            print("✅ No remaining linting issues!")
        else:
            issue_count = result.stdout.count("Found")
            print(f"⚠️ {issue_count} issues remaining")
            print("   Run 'ruff check .' to see details")
    except Exception as e:
        print(f"❌ Issue check failed: {e}")

    # Step 4: Pre-commit check (only on Python files)
    python_files = list(target_path.rglob("*.py"))
    if python_files:
        file_paths = [str(f.relative_to(target_path)) for f in python_files]
        precommit_cmd = ["python3", "-m", "pre_commit", "run", "--files"] + file_paths
        precommit_success = run_command_safe(
            precommit_cmd, "Pre-commit checks", cwd=target_path
        )
    else:
        print("\n⚠️ No Python files found for pre-commit checks")
        precommit_success = True

    # Summary
    print("\n🎉 AUTOMATION COMPLETE!")
    print(f"📁 Target: {target_path}")
    print(f"✅ Black: {'Passed' if black_success else 'Failed'}")
    print(f"✅ Ruff: {'Passed' if ruff_success else 'Failed'}")
    print(f"✅ Pre-commit: {'Passed' if precommit_success else 'Failed'}")

    if all([black_success, ruff_success, precommit_success]):
        print("✨ CODE IS CLEAN AS A WHISTLE! ✨")
    else:
        print("⚠️ Some steps failed - check output above")

    return 0 if all([black_success, ruff_success, precommit_success]) else 1


if __name__ == "__main__":
    sys.exit(main())
