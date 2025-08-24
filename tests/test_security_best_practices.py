#!/usr/bin/env python3
"""
Security Best Practices Test Suite

This test demonstrates using established open-source security tools
instead of building custom security scanners.
"""

import subprocess
import tempfile
import os
from pathlib import Path
import pytest


class TestSecurityBestPractices:
    """Test security best practices using established tools"""

    def test_bandit_integration(self):
        """Test that Bandit can detect security issues"""
        # Create a temporary file with security issues
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                """
# Test file with security vulnerabilities
import os
import hashlib

# Security Issue 1: Hardcoded password
password = "secret123"

# Security Issue 2: Weak hash function
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()  # MD5 is weak

# Security Issue 3: Command injection vulnerability
def run_command(user_input):
    os.system(f"echo {user_input}")  # Command injection risk
"""
            )
            temp_file = f.name

        try:
            # Run Bandit on the file
            result = subprocess.run(
                ["bandit", temp_file], capture_output=True, text=True, cwd=os.getcwd()
            )

            # Bandit should find security issues
            assert result.returncode == 1, "Bandit should detect security issues"

            # Check that specific issues were found
            output = result.stdout + result.stderr

            # Should detect hardcoded password
            assert (
                "hardcoded_password_string" in output
            ), "Should detect hardcoded password"

            # Should detect weak hash
            assert "hashlib" in output, "Should detect weak hash usage"

            # Should detect command injection
            assert (
                "start_process_with_a_shell" in output
            ), "Should detect command injection"

            print("✅ Bandit successfully detected security issues")

        finally:
            # Clean up
            os.unlink(temp_file)

    def test_security_tool_availability(self):
        """Test that required security tools are available"""
        # Check Bandit
        try:
            result = subprocess.run(
                ["bandit", "--version"], capture_output=True, text=True
            )
            assert result.returncode == 0, "Bandit should be available"
            print("✅ Bandit is available")
        except FileNotFoundError:
            pytest.skip("Bandit not available")

    def test_security_scanning_workflow(self):
        """Test a complete security scanning workflow using established tools"""
        # This demonstrates the proper workflow:
        # 1. Use Bandit for Python security
        # 2. Use Gitleaks for secret detection (when available)
        # 3. Use Trivy for dependency scanning (when available)
        # 4. Use Semgrep for pattern-based scanning (when available)

        print("🔒 Security Scanning Workflow (Best Practices):")
        print("  1. ✅ Bandit - Python security scanning")
        print("  2. ⏳ Gitleaks - Secret detection (to be installed)")
        print("  3. ⏳ Trivy - Vulnerability scanning (to be installed)")
        print("  4. ⏳ Semgrep - Pattern-based scanning (to be installed)")
        print("  5. ❌ Custom security scanner - NOT RECOMMENDED")

        # Verify Bandit works
        result = subprocess.run(["bandit", "--version"], capture_output=True, text=True)
        assert result.returncode == 0, "Bandit should work"

        print("✅ Security workflow validation passed")


def main():
    """Run security best practices tests"""
    print("🚀 Testing Security Best Practices...")

    test_suite = TestSecurityBestPractices()

    try:
        test_suite.test_bandit_integration()
        test_suite.test_security_tool_availability()
        test_suite.test_security_scanning_workflow()

        print("🎉 All Security Best Practices Tests Passed!")
        print("\n📋 Summary:")
        print("  ✅ Use established tools (Bandit, Gitleaks, Trivy, Semgrep)")
        print("  ❌ Don't build custom security scanners")
        print("  🔒 Follow OWASP and industry best practices")

        return True

    except Exception as e:
        print(f"❌ Security Best Practices Test Failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
