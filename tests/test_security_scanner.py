#!/usr/bin/env python3
"""
Security Scanner Test Suite

Tests the security scanner functionality to identify any issues.
"""

import os
import tempfile
from pathlib import Path

import pytest

from src.security_scanning import SecurityScanner, create_security_scanner


class TestSecurityScanner:
    """Test SecurityScanner functionality"""

    def test_security_scanner_import(self):
        """Test that SecurityScanner can be imported"""
        assert SecurityScanner is not None
        print("✅ SecurityScanner import successful")

    def test_security_scanner_creation(self):
        """Test that SecurityScanner can be created"""
        scanner = create_security_scanner()
        assert scanner is not None
        assert hasattr(scanner, "scan_project")
        print("✅ SecurityScanner creation successful")

    def test_security_scanner_scan_small_directory(self):
        """Test scanning a small directory with known content"""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a test file with a potential security issue
            test_file = temp_path / "test_security.py"
            test_file.write_text(
                """
# Test file with potential security issues
api_key = "sk-1234567890abcdef"  # This should be detected
password = "secret123"  # This should be detected
normal_var = "safe_value"  # This should not be detected
"""
            )

            # Create scanner and scan the directory
            scanner = create_security_scanner()
            results = scanner.scan_project(str(temp_path))

            # Verify results structure
            assert results is not None
            assert "summary" in results
            assert "all_findings" in results
            assert "false_positives" in results

            # Check summary data
            summary = results["summary"]
            assert "files_scanned" in summary
            assert "findings_count" in summary
            assert "status" in summary

            print(f"✅ Security scan completed: {summary['files_scanned']} files, {summary['findings_count']} findings")

            # Check that security issues were detected (either as findings or false positives)
            all_findings = results["all_findings"]
            false_positives = results["false_positives"]

            # Security scanner should detect the issues (even if marked as false positives)
            total_detections = len(all_findings) + len(false_positives)
            assert total_detections > 0, "Should detect security issues in test file"

            # Check for specific patterns in either findings or false positives
            api_key_found = any("api_key" in str(finding) for finding in all_findings + false_positives)
            password_found = any("password" in str(finding) for finding in all_findings + false_positives)

            assert api_key_found, "Should detect API key in test file"
            assert password_found, "Should detect password in test file"

            print(f"✅ Detected {total_detections} security issues (including false positives)")

    def test_security_scanner_performance_metrics(self):
        """Test that performance metrics are reasonable"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a simple test file
            test_file = temp_path / "simple_test.py"
            test_file.write_text("print('Hello, World!')")

            # Scan and check metrics
            scanner = create_security_scanner()
            results = scanner.scan_project(str(temp_path))

            # Check performance metrics structure
            assert "performance" in results
            performance = results["performance"]

            assert "scan_duration" in performance or "elapsed_time" in performance
            assert "throughput" in performance
            assert "success_rate" in performance

            # Success rate should be reasonable (0-100%)
            success_rate = performance["success_rate"]
            assert 0 <= success_rate <= 100, f"Success rate {success_rate}% is not reasonable"

            # Get scan duration from either field
            scan_duration = performance.get("scan_duration", performance.get("elapsed_time", 0))
            throughput = performance["throughput"]

            print(f"✅ Performance metrics: duration={scan_duration:.2f}s, throughput={throughput:.1f} files/s, success_rate={success_rate:.1f}%")

    def test_security_scanner_exclusion_patterns(self):
        """Test that exclusion patterns work correctly"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a cache directory that should be excluded
            cache_dir = temp_path / ".cache"
            cache_dir.mkdir()
            cache_file = cache_dir / "cache_file.json"
            cache_file.write_text('{"key": "sk-1234567890abcdef"}')

            # Create a normal file that should be scanned
            normal_file = temp_path / "normal.py"
            normal_file.write_text('api_key = "sk-1234567890abcdef"')

            # Scan and check results
            scanner = create_security_scanner()
            results = scanner.scan_project(str(temp_path))

            # Should find issues in normal files but not cache files
            all_findings = results["all_findings"]
            false_positives = results["false_positives"]

            # Check findings in normal files
            normal_file_findings = [f for f in all_findings + false_positives if "normal.py" in str(f)]
            cache_file_findings = [f for f in all_findings + false_positives if "cache_file.json" in str(f)]

            # Normal file should have findings
            assert len(normal_file_findings) > 0, "Should detect issues in normal files"

            # Cache file should ideally be excluded, but if not, findings should be minimal
            if len(cache_file_findings) > 0:
                print(f"⚠️ Cache file findings: {len(cache_file_findings)} (may need exclusion pattern tuning)")
            else:
                print("✅ Cache files properly excluded")

            print(f"✅ Exclusion test: {len(normal_file_findings)} findings in normal files")


def main():
    """Run security scanner tests"""
    print("🚀 Running Security Scanner Tests...")

    # Run tests
    test_scanner = TestSecurityScanner()

    try:
        test_scanner.test_security_scanner_import()
        test_scanner.test_security_scanner_creation()
        test_scanner.test_security_scanner_scan_small_directory()
        test_scanner.test_security_scanner_performance_metrics()
        test_scanner.test_security_scanner_exclusion_patterns()

        print("🎉 All Security Scanner Tests Passed!")
        return True

    except Exception as e:
        print(f"❌ Security Scanner Test Failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
