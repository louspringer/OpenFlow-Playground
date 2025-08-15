#!/usr/bin/env python3
"""
Test script for Expert Agent Quality Integration

This script tests the quality integration methods added to expert agents.
"""

import asyncio
import sys
from pathlib import Path

# Add the clewcrew-agents to the path
sys.path.insert(0, str(Path(__file__).parent / "clewcrew-agents" / "src"))

# Import expert agents
from clewcrew_agents import CodeQualityExpert, SecurityExpert  # noqa: E402


async def test_security_expert_quality_integration():
    """Test SecurityExpert quality integration methods"""
    print("🧪 Testing SecurityExpert Quality Integration...")

    try:
        expert = SecurityExpert()
        project_path = Path()

        # Test quality metric generation
        print("  🔄 Testing generate_quality_metrics...")
        metrics = await expert.generate_quality_metrics(project_path)

        print(f"    ✅ Quality score: {metrics['quality_score']:.1f}")
        print(f"    ✅ Issues found: {metrics['issues_found']}")
        print(f"    ✅ Critical issues: {metrics['critical_issues']}")
        print(f"    ✅ High issues: {metrics['high_issues']}")
        print(f"    ✅ Confidence: {metrics['confidence']:.2f}")
        print(f"    ✅ Risk score: {metrics['risk_score']:.1f}")

        # Test quality recommendations
        print("  🔄 Testing provide_quality_recommendations...")
        recommendations = await expert.provide_quality_recommendations(project_path)
        print(f"    ✅ Recommendations: {len(recommendations)}")
        for rec in recommendations[:3]:  # Show first 3
            print(f"      • {rec}")

        # Test quality impact assessment
        print("  🔄 Testing assess_quality_impact...")
        mock_changes = [
            {"content": "password = 'secret123'"},
            {"content": "import subprocess\nsubprocess.run(['rm', '-rf', '/'])"},
        ]
        impact = await expert.assess_quality_impact(mock_changes)
        print(f"    ✅ Impact assessment: {impact['quality_impact']}")
        print(f"    ✅ Risk level: {impact['risk_level']}")
        print(f"    ✅ Security risks: {len(impact['security_risks'])}")

        # Test quality metric configuration
        print("  🔄 Testing quality metric configuration...")
        metric_name = expert.get_quality_metric_name()
        metric_weight = expert.get_quality_metric_weight()
        print(f"    ✅ Metric name: {metric_name}")
        print(f"    ✅ Metric weight: {metric_weight}")

        return True

    except Exception as e:
        print(f"  ❌ SecurityExpert quality integration test failed: {e}")
        return False


async def test_code_quality_expert_quality_integration():
    """Test CodeQualityExpert quality integration methods"""
    print("\n🧪 Testing CodeQualityExpert Quality Integration...")

    try:
        expert = CodeQualityExpert()
        project_path = Path()

        # Test quality metric generation
        print("  🔄 Testing generate_quality_metrics...")
        metrics = await expert.generate_quality_metrics(project_path)

        print(f"    ✅ Quality score: {metrics['quality_score']:.1f}")
        print(f"    ✅ Issues found: {metrics['issues_found']}")
        print(f"    ✅ Flake8 issues: {len(metrics['flake8_issues'])}")
        print(f"    ✅ Code style issues: {len(metrics['code_style_issues'])}")
        print(f"    ✅ Complexity issues: {len(metrics['complexity_issues'])}")
        print(f"    ✅ Confidence: {metrics['confidence']:.2f}")

        # Test quality recommendations
        print("  🔄 Testing provide_quality_recommendations...")
        recommendations = await expert.provide_quality_recommendations(project_path)
        print(f"    ✅ Recommendations: {len(recommendations)}")
        for rec in recommendations[:3]:  # Show first 3
            print(f"      • {rec}")

        # Test quality impact assessment
        print("  🔄 Testing assess_quality_impact...")
        mock_changes = [
            {"content": "def simple_function():\n    pass"},
            {
                "content": "import *\nfrom os import *\n# TODO: Fix this later\n# FIXME: Need to refactor"
            },
        ]
        impact = await expert.assess_quality_impact(mock_changes)
        print(f"    ✅ Impact assessment: {impact['quality_impact']}")
        print(f"    ✅ Risk level: {impact['risk_level']}")
        print(f"    ✅ Quality risks: {len(impact['quality_risks'])}")

        # Test quality metric configuration
        print("  🔄 Testing quality metric configuration...")
        metric_name = expert.get_quality_metric_name()
        metric_weight = expert.get_quality_metric_weight()
        print(f"    ✅ Metric name: {metric_name}")
        print(f"    ✅ Metric weight: {metric_weight}")

        return True

    except Exception as e:
        print(f"  ❌ CodeQualityExpert quality integration test failed: {e}")
        return False


async def test_quality_metric_consistency():
    """Test consistency between expert quality metrics and adapter mapping"""
    print("\n🧪 Testing Quality Metric Consistency...")

    try:
        from src.code_quality_system.multi_agent_integration import (
            QualityMultiAgentAdapter,
        )

        # Create adapter
        adapter = QualityMultiAgentAdapter(Path())
        mapping = adapter.get_agent_quality_mapping()

        # Test SecurityExpert consistency
        security_expert = SecurityExpert()
        security_metric_name = security_expert.get_quality_metric_name()
        security_metric_weight = security_expert.get_quality_metric_weight()

        # Find the mapping entry for security_expert
        security_mapping = None
        for agent_name, agent_mapping in mapping.items():
            if agent_mapping["metric_name"] == security_metric_name:
                security_mapping = agent_mapping
                break

        if security_mapping:
            expected_weight = security_mapping["weight"]
            if abs(security_metric_weight - expected_weight) < 0.01:
                print(
                    f"  ✅ SecurityExpert metric consistency: {security_metric_name}  = \
     {security_metric_weight}"
                )
            else:
                print(
                    f"  ❌ SecurityExpert weight mismatch: expected {expected_weight}, got {security_metric_weight}"
                )
                return False
        else:
            print(
                f"  ❌ SecurityExpert metric {security_metric_name} not found in adapter mapping"
            )
            return False

        # Test CodeQualityExpert consistency
        code_quality_expert = CodeQualityExpert()
        code_quality_metric_name = code_quality_expert.get_quality_metric_name()
        code_quality_metric_weight = code_quality_expert.get_quality_metric_weight()

        # Find the mapping entry for code_quality_expert
        code_quality_mapping = None
        for agent_name, agent_mapping in mapping.items():
            if agent_mapping["metric_name"] == code_quality_metric_name:
                code_quality_mapping = agent_mapping
                break

        if code_quality_mapping:
            expected_weight = code_quality_mapping["weight"]
            if abs(code_quality_metric_weight - expected_weight) < 0.01:
                print(
                    f"  ✅ CodeQualityExpert metric consistency: {code_quality_metric_name}  = \
     {code_quality_metric_weight}"
                )
            else:
                print(
                    f"  ❌ CodeQualityExpert weight mismatch: expected {expected_weight}, got {code_quality_metric_weight}"
                )
                return False
        else:
            print(
                f"  ❌ CodeQualityExpert metric {code_quality_metric_name} not found in adapter mapping"
            )
            return False

        return True

    except Exception as e:
        print(f"  ❌ Quality metric consistency test failed: {e}")
        return False


async def main():
    """Run all quality integration tests"""
    print("🚀 Expert Agent Quality Integration Test Suite")
    print("=" * 70)

    tests = [
        test_security_expert_quality_integration,
        test_code_quality_expert_quality_integration,
        test_quality_metric_consistency,
    ]

    results = []
    for test in tests:
        if await test():
            results.append(True)
        else:
            results.append(False)
        print()

    # Summary
    print("=" * 70)
    print("📊 Quality Integration Test Results")
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print(
            "🎉 All tests passed! Expert agent quality integration is working correctly."
        )
        print("\n✅ Quality Integration Status:")
        print("   • SecurityExpert: Quality methods implemented and tested")
        print("   • CodeQualityExpert: Quality methods implemented and tested")
        print("   • QualityMultiAgentAdapter: Integration mapping verified")
        print("   • Metric consistency: All expert agents aligned with adapter")
        return 0

    print("❌ Some tests failed. Please review the logs above.")
    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
