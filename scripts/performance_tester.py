#!/usr/bin/env python3
"""
Performance Testing Script

This script tests performance requirements for RDI methodology compliance.
It validates that all operations meet their performance requirements.
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add src to path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class PerformanceTester:
    """Performance testing system for RDI methodology compliance."""

    def __init__(self):
        """Initialize the performance tester."""
        self.test_results = []
        self.performance_requirements = {
            "pre_commit_hook": 5.0,  # seconds
            "safety_check": 3.0,  # seconds
            "health_check": 1.0,  # seconds
            "health_api": 2.0,  # seconds
            "rdi_validation": 10.0,  # seconds
            "incident_tracking": 1.0,  # seconds
        }

    def test_safety_check_performance(self) -> Dict[str, Any]:
        """Test safety check performance (REQ-PERF-002)."""
        print("🔍 Testing safety check performance...")

        start_time = time.time()
        try:
            result = subprocess.run(["uv", "run", "python", "scripts/safety_check_wrapper.py"], capture_output=True, text=True, timeout=5)
            execution_time = time.time() - start_time

            test_result = {
                "test": "safety_check_performance",
                "requirement": "REQ-PERF-002",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["safety_check"],
                "passed": execution_time <= self.performance_requirements["safety_check"],
                "status": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
            }

            if test_result["passed"]:
                print(f"  ✅ Safety check performance: {execution_time:.2f}s (threshold: {self.performance_requirements['safety_check']}s)")
            else:
                print(f"  ❌ Safety check performance: {execution_time:.2f}s (threshold: {self.performance_requirements['safety_check']}s)")

            return test_result

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            test_result = {
                "test": "safety_check_performance",
                "requirement": "REQ-PERF-002",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["safety_check"],
                "passed": False,
                "status": "timeout",
                "output": "",
                "error": "Safety check timed out",
            }
            print(f"  ❌ Safety check performance: TIMEOUT after {execution_time:.2f}s")
            return test_result

    def test_health_check_performance(self) -> Dict[str, Any]:
        """Test health check performance (REQ-PERF-004)."""
        print("🔍 Testing health check performance...")

        start_time = time.time()
        try:
            result = subprocess.run(["uv", "run", "python", "scripts/safety_check_wrapper.py", "--status"], capture_output=True, text=True, timeout=2)
            execution_time = time.time() - start_time

            test_result = {
                "test": "health_check_performance",
                "requirement": "REQ-PERF-004",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["health_check"],
                "passed": execution_time <= self.performance_requirements["health_check"],
                "status": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
            }

            if test_result["passed"]:
                print(f"  ✅ Health check performance: {execution_time:.2f}s (threshold: {self.performance_requirements['health_check']}s)")
            else:
                print(f"  ❌ Health check performance: {execution_time:.2f}s (threshold: {self.performance_requirements['health_check']}s)")

            return test_result

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            test_result = {
                "test": "health_check_performance",
                "requirement": "REQ-PERF-004",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["health_check"],
                "passed": False,
                "status": "timeout",
                "output": "",
                "error": "Health check timed out",
            }
            print(f"  ❌ Health check performance: TIMEOUT after {execution_time:.2f}s")
            return test_result

    def test_rdi_requirements_performance(self) -> Dict[str, Any]:
        """Test RDI requirements validation performance (REQ-PERF-006)."""
        print("🔍 Testing RDI requirements performance...")

        start_time = time.time()
        try:
            result = subprocess.run(["make", "rdi-requirements"], capture_output=True, text=True, timeout=15)
            execution_time = time.time() - start_time

            test_result = {
                "test": "rdi_requirements_performance",
                "requirement": "REQ-PERF-006",
                "execution_time": execution_time,
                "threshold": 5.0,  # RDI requirements should complete within 5 seconds
                "passed": execution_time <= 5.0,
                "status": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
            }

            if test_result["passed"]:
                print(f"  ✅ RDI requirements performance: {execution_time:.2f}s (threshold: 5.0s)")
            else:
                print(f"  ❌ RDI requirements performance: {execution_time:.2f}s (threshold: 5.0s)")

            return test_result

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            test_result = {
                "test": "rdi_requirements_performance",
                "requirement": "REQ-PERF-006",
                "execution_time": execution_time,
                "threshold": 5.0,
                "passed": False,
                "status": "timeout",
                "output": "",
                "error": "RDI requirements validation timed out",
            }
            print(f"  ❌ RDI requirements performance: TIMEOUT after {execution_time:.2f}s")
            return test_result

    def test_incident_tracking_performance(self) -> Dict[str, Any]:
        """Test incident tracking performance (REQ-PERF-007)."""
        print("🔍 Testing incident tracking performance...")

        start_time = time.time()
        try:
            result = subprocess.run(["uv", "run", "python", "scripts/incident_tracker.py", "metrics"], capture_output=True, text=True, timeout=3)
            execution_time = time.time() - start_time

            test_result = {
                "test": "incident_tracking_performance",
                "requirement": "REQ-PERF-007",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["incident_tracking"],
                "passed": execution_time <= self.performance_requirements["incident_tracking"],
                "status": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
            }

            if test_result["passed"]:
                print(f"  ✅ Incident tracking performance: {execution_time:.2f}s (threshold: {self.performance_requirements['incident_tracking']}s)")
            else:
                print(f"  ❌ Incident tracking performance: {execution_time:.2f}s (threshold: {self.performance_requirements['incident_tracking']}s)")

            return test_result

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            test_result = {
                "test": "incident_tracking_performance",
                "requirement": "REQ-PERF-007",
                "execution_time": execution_time,
                "threshold": self.performance_requirements["incident_tracking"],
                "passed": False,
                "status": "timeout",
                "output": "",
                "error": "Incident tracking timed out",
            }
            print(f"  ❌ Incident tracking performance: TIMEOUT after {execution_time:.2f}s")
            return test_result

    def run_all_performance_tests(self) -> Dict[str, Any]:
        """Run all performance tests."""
        print("🚀 Running all performance tests...")
        print("=" * 50)

        # Run all performance tests
        tests = [
            self.test_safety_check_performance,
            self.test_health_check_performance,
            self.test_rdi_requirements_performance,
            self.test_incident_tracking_performance,
        ]

        for test_func in tests:
            try:
                result = test_func()
                self.test_results.append(result)
            except Exception as e:
                error_result = {"test": test_func.__name__, "requirement": "UNKNOWN", "execution_time": 0, "threshold": 0, "passed": False, "status": "error", "output": "", "error": str(e)}
                self.test_results.append(error_result)
                print(f"  ❌ {test_func.__name__}: ERROR - {str(e)}")

        return self._generate_performance_summary()

    def _generate_performance_summary(self) -> Dict[str, Any]:
        """Generate performance test summary."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["passed"]])
        failed_tests = total_tests - passed_tests

        # Calculate average execution times
        avg_execution_time = sum(r["execution_time"] for r in self.test_results) / total_tests if total_tests > 0 else 0

        # Find slowest test
        slowest_test = max(self.test_results, key=lambda x: x["execution_time"]) if self.test_results else None

        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "avg_execution_time": avg_execution_time,
            "slowest_test": slowest_test,
            "test_results": self.test_results,
        }

        return summary

    def generate_performance_report(self) -> str:
        """Generate performance test report."""
        summary = self._generate_performance_summary()

        report = []
        report.append("# 📊 Performance Test Report")
        report.append("")
        report.append("## 📈 Summary")
        report.append(f"- **Total Tests**: {summary['total_tests']}")
        report.append(f"- **Passed Tests**: {summary['passed_tests']}")
        report.append(f"- **Failed Tests**: {summary['failed_tests']}")
        report.append(f"- **Success Rate**: {summary['success_rate']:.1f}%")
        report.append(f"- **Average Execution Time**: {summary['avg_execution_time']:.2f}s")
        report.append("")

        if summary["slowest_test"]:
            report.append("## 🐌 Slowest Test")
            report.append(f"- **Test**: {summary['slowest_test']['test']}")
            report.append(f"- **Execution Time**: {summary['slowest_test']['execution_time']:.2f}s")
            report.append(f"- **Threshold**: {summary['slowest_test']['threshold']}s")
            report.append("")

        if summary["test_results"]:
            report.append("## 📋 Test Details")
            for result in summary["test_results"]:
                report.append(f"### {result['test']}")
                report.append(f"- **Requirement**: {result['requirement']}")
                report.append(f"- **Status**: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")
                report.append(f"- **Execution Time**: {result['execution_time']:.2f}s")
                report.append(f"- **Threshold**: {result['threshold']}s")
                if result["error"]:
                    report.append(f"- **Error**: {result['error']}")
                report.append("")

        return "\n".join(report)


def main():
    """Main entry point for performance tester."""
    tester = PerformanceTester()

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        # Generate report only
        summary = tester.run_all_performance_tests()
        report = tester.generate_performance_report()
        print("\n" + "=" * 50)
        print(report)
        return 0 if summary["failed_tests"] == 0 else 1

    # Run performance tests
    summary = tester.run_all_performance_tests()

    # Print summary
    print("\n" + "=" * 50)
    print("📊 Performance Test Summary")
    print("=" * 50)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed Tests: {summary['passed_tests']}")
    print(f"Failed Tests: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Execution Time: {summary['avg_execution_time']:.2f}s")

    if summary["slowest_test"]:
        print(f"Slowest Test: {summary['slowest_test']['test']} ({summary['slowest_test']['execution_time']:.2f}s)")

    if summary["failed_tests"] == 0:
        print("\n✅ All performance tests passed!")
        return 0
    else:
        print(f"\n❌ {summary['failed_tests']} performance tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
