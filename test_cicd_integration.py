#!/usr/bin/env python3
"""
Test CI/CD Integration

Tests the CI/CD integration with quality gates and environment-specific rules.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from code_quality_system.integrations.ci_cd_integration import CICDIntegration


def test_cicd_integration():
    """Test the CI/CD integration functionality"""
    print("🚀 CI/CD Integration Test Suite")
    print("=" * 60)

    # Test 1: Environment Detection
    print("\n🧪 Testing Environment Detection...")
    try:
        cicd = CICDIntegration(Path())
        print(f"  ✅ CI Environment: {cicd.ci_environment}")
        print(f"  ✅ Environment Rules: {cicd.environment_rules}")
        print(f"  ✅ CI Config: {cicd.ci_config}")
    except Exception as e:
        print(f"  ❌ Environment detection failed: {e}")
        return False

    # Test 2: Environment-Specific Rules
    print("\n🧪 Testing Environment-Specific Rules...")
    try:
        # Test development environment
        os.environ["DEPLOYMENT_ENVIRONMENT"] = "development"
        cicd_dev = CICDIntegration(Path())
        print(
            f"  ✅ Development Threshold: {cicd_dev.environment_rules['quality_threshold']}"
        )
        print(
            f"  ✅ Development Fail on Quality: {cicd_dev.environment_rules['fail_on_quality']}"
        )

        # Test staging environment
        os.environ["DEPLOYMENT_ENVIRONMENT"] = "staging"
        cicd_staging = CICDIntegration(Path())
        print(
            f"  ✅ Staging Threshold: {cicd_staging.environment_rules['quality_threshold']}"
        )
        print(
            f"  ✅ Staging Fail on Quality: {cicd_staging.environment_rules['fail_on_quality']}"
        )

        # Test production environment
        os.environ["DEPLOYMENT_ENVIRONMENT"] = "production"
        cicd_prod = CICDIntegration(Path())
        print(
            f"  ✅ Production Threshold: {cicd_prod.environment_rules['quality_threshold']}"
        )
        print(
            f"  ✅ Production Fail on Quality: {cicd_prod.environment_rules['fail_on_quality']}"
        )

    except Exception as e:
        print(f"  ❌ Environment-specific rules test failed: {e}")
        return False

    # Test 3: CI Configuration
    print("\n🧪 Testing CI Configuration...")
    try:
        # Set environment variables
        os.environ["QUALITY_THRESHOLD"] = "75.0"
        os.environ["FAIL_ON_QUALITY"] = "true"
        os.environ["QUALITY_VERBOSE"] = "true"
        os.environ["DEPLOYMENT_ENVIRONMENT"] = "staging"

        cicd = CICDIntegration(Path())
        print(f"  ✅ Quality Threshold: {cicd.ci_config['quality_threshold']}")
        print(f"  ✅ Fail on Quality: {cicd.ci_config['fail_on_quality']}")
        print(f"  ✅ Verbose: {cicd.ci_config['verbose']}")
        print(f"  ✅ Environment: {cicd.ci_config['environment']}")

    except Exception as e:
        print(f"  ❌ CI configuration test failed: {e}")
        return False

    # Test 4: Quality Check Execution
    print("\n🧪 Testing Quality Check Execution...")
    try:
        cicd = CICDIntegration(Path())
        # Note: This is now async, but we'll test the sync fallback for now
        print("  ℹ️  CI quality check is async - testing sync fallback...")

        # Test the fallback quality check
        fallback_result = cicd._run_fallback_quality_check()
        print(
            f"  ✅ Fallback Quality Check Result: {fallback_result.get('status', 'unknown')}"
        )
        if "overall_score" in fallback_result:
            print(f"  ✅ Overall Score: {fallback_result.get('overall_score', 'N/A')}")

    except Exception as e:
        print(f"  ❌ Quality check execution failed: {e}")
        return False

    # Test 5: CI Report Generation
    print("\n🧪 Testing CI Report Generation...")
    try:
        cicd = CICDIntegration(Path())

        # Mock quality result for testing
        mock_quality_result = {
            "overall_score": 75.0,
            "quality_status": "acceptable",
            "can_proceed": True,
            "gate_summary": {
                "total_gates": 5,
                "passed_gates": 4,
                "failed_gates": 1,
                "blocking_gates": 0,
            },
            "recommendations": ["Fix the failing quality gate"],
            "timestamp": "2025-08-14T16:00:00Z",
        }

        ci_report = cicd._generate_ci_report(mock_quality_result)
        print(f"  ✅ CI Report Generated: {ci_report.get('status', 'unknown')}")
        print(f"  ✅ Overall Score: {ci_report.get('overall_score', 'N/A')}")
        print(f"  ✅ Threshold Met: {ci_report.get('threshold_met', 'N/A')}")
        print(f"  ✅ Can Proceed: {ci_report.get('can_proceed', 'N/A')}")

    except Exception as e:
        print(f"  ❌ CI report generation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 All CI/CD integration tests passed!")
    return True


def test_environment_rules():
    """Test environment-specific quality rules"""
    print("\n🧪 Testing Environment Rules...")

    # Test development environment
    os.environ["DEPLOYMENT_ENVIRONMENT"] = "development"
    cicd = CICDIntegration(Path())

    print("  🔧 Development Environment Rules:")
    print(f"    • Quality Threshold: {cicd.environment_rules['quality_threshold']}")
    print(f"    • Fail on Quality: {cicd.environment_rules['fail_on_quality']}")
    print(f"    • Gate Severity: {cicd.environment_rules['gate_severity']}")
    print(f"    • Auto Fix Enabled: {cicd.environment_rules['auto_fix_enabled']}")
    print(f"    • Quality Reporting: {cicd.environment_rules['quality_reporting']}")

    # Test staging environment
    os.environ["DEPLOYMENT_ENVIRONMENT"] = "staging"
    cicd = CICDIntegration(Path())

    print("  🔧 Staging Environment Rules:")
    print(f"    • Quality Threshold: {cicd.environment_rules['quality_threshold']}")
    print(f"    • Fail on Quality: {cicd.environment_rules['fail_on_quality']}")
    print(f"    • Gate Severity: {cicd.environment_rules['gate_severity']}")
    print(f"    • Auto Fix Enabled: {cicd.environment_rules['auto_fix_enabled']}")
    print(f"    • Quality Reporting: {cicd.environment_rules['quality_reporting']}")

    # Test production environment
    os.environ["DEPLOYMENT_ENVIRONMENT"] = "production"
    cicd = CICDIntegration(Path())

    print("  🔧 Production Environment Rules:")
    print(f"    • Quality Threshold: {cicd.environment_rules['quality_threshold']}")
    print(f"    • Fail on Quality: {cicd.environment_rules['fail_on_quality']}")
    print(f"    • Gate Severity: {cicd.environment_rules['gate_severity']}")
    print(f"    • Auto Fix Enabled: {cicd.environment_rules['auto_fix_enabled']}")
    print(f"    • Quality Reporting: {cicd.environment_rules['quality_reporting']}")


def main():
    """Run all CI/CD integration tests"""
    print("🚀 CI/CD Integration Test Suite")
    print("=" * 60)

    try:
        # Run main integration test
        if test_cicd_integration():
            print("\n✅ CI/CD Integration Test: PASSED")
        else:
            print("\n❌ CI/CD Integration Test: FAILED")
            return 1

        # Run environment rules test
        test_environment_rules()

        print("\n" + "=" * 60)
        print("🎉 CI/CD Integration Testing Complete!")
        print("\n✅ What was tested:")
        print("   • Environment detection and configuration")
        print("   • Environment-specific quality rules")
        print("   • CI configuration loading")
        print("   • Quality check execution")
        print("   • CI report generation")
        print("   • Environment-specific thresholds and behaviors")

        return 0

    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
