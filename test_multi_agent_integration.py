#!/usr/bin/env python3
"""
Test script for QualityMultiAgentAdapter

This script tests the integration between the quality system and multi-agent framework.
"""

import asyncio
from pathlib import Path

from src.code_quality_system.multi_agent_integration import QualityMultiAgentAdapter


async def test_quality_multi_agent_adapter():
    """Test the QualityMultiAgentAdapter class"""
    print("🧪 Testing QualityMultiAgentAdapter...")

    try:
        # Create adapter
        adapter = QualityMultiAgentAdapter(Path())
        print("✅ Created QualityMultiAgentAdapter")

        # Test agent quality mapping
        mapping = adapter.get_agent_quality_mapping()
        print(f"✅ Agent quality mapping: {len(mapping)} agents configured")

        # Test with mock agent results
        mock_agent_results = {
            "security_expert": {
                "security_issues": ["hardcoded_credential", "weak_encryption"],
                "critical_issues": ["sql_injection"],
                "high_issues": ["xss_vulnerability"],
            },
            "code_quality_expert": {
                "flake8_issues": ["E501", "F401"],
                "code_style_issues": ["missing_docstring"],
                "complexity_issues": ["high_cyclomatic_complexity"],
            },
            "devops_expert": {
                "ci_cd_issues": ["missing_tests"],
                "deployment_issues": ["no_rollback_plan"],
                "infrastructure_issues": ["missing_monitoring"],
            },
            "test_expert": {
                "coverage_percentage": 85.0,
                "test_count": 150,
                "test_failures": 2,
            },
            "architecture_expert": {
                "design_issues": ["tight_coupling"],
                "pattern_violations": ["singleton_anti_pattern"],
                "coupling_issues": ["circular_dependency"],
            },
        }

        # Run multi-agent quality analysis
        print("🔄 Running multi-agent quality analysis...")
        results = await adapter.run_multi_agent_quality_analysis(mock_agent_results)

        if results["status"] == "success":
            print("✅ Multi-agent quality analysis completed successfully")
            print(f"   Overall quality score: {results['overall_quality_score']:.1f}")
            print(f"   Agents analyzed: {results['agents_analyzed']}")
            print(f"   Can proceed: {results['can_proceed']}")
            print(f"   Blocking gates: {results['blocking_gates']}")

            # Show quality scores breakdown
            print("\n📊 Quality Scores Breakdown:")
            for metric, score_data in results["quality_scores"].items():
                print(
                    f"   {metric}: {score_data['score']:.1f} (weight: {score_data['weight']})"
                )

            # Show agent summary
            print("\n🤖 Agent Analysis Summary:")
            for agent, summary in results["agent_summary"].items():
                if summary["status"] == "analyzed":
                    print(f"   {agent}: {summary['metric']} = {summary['score']:.1f}")
                else:
                    print(f"   {agent}: {summary['status']}")

            # Show recommendations
            if results["recommendations"]:
                print("\n💡 Recommendations:")
                for rec in results["recommendations"]:
                    print(f"   • {rec}")

            return True
        print(
            f"❌ Multi-agent quality analysis failed: {results.get('error', 'Unknown error')}"
        )
        return False

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False


async def test_agent_mapping_management():
    """Test agent mapping management functionality"""
    print("\n🧪 Testing Agent Mapping Management...")

    try:
        adapter = QualityMultiAgentAdapter(Path())

        # Test adding new agent mapping
        new_mapping = {
            "custom_expert": {
                "metric_name": "custom_quality",
                "weight": 2.5,
                "description": "Custom quality analysis",
            }
        }

        success = adapter.add_agent_quality_mapping(
            "custom_expert", new_mapping["custom_expert"]
        )
        if success:
            print("✅ Added new agent mapping")

            # Verify it was added
            mapping = adapter.get_agent_quality_mapping()
            if "custom_expert" in mapping:
                print("✅ New agent mapping verified")
            else:
                print("❌ New agent mapping not found")
                return False
        else:
            print("❌ Failed to add new agent mapping")
            return False

        # Test updating existing mapping
        updated_mapping = {
            "metric_name": "custom_quality",
            "weight": 3.0,
            "description": "Updated custom quality analysis",
        }

        success = adapter.update_agent_quality_mapping("custom_expert", updated_mapping)
        if success:
            print("✅ Updated agent mapping")
        else:
            print("❌ Failed to update agent mapping")
            return False

        # Test removing agent mapping
        success = adapter.remove_agent_quality_mapping("custom_expert")
        if success:
            print("✅ Removed agent mapping")
        else:
            print("❌ Failed to remove agent mapping")
            return False

        return True

    except Exception as e:
        print(f"❌ Agent mapping management test failed: {e}")
        return False


async def test_quality_score_conversion():
    """Test quality score conversion for different agent types"""
    print("\n🧪 Testing Quality Score Conversion...")

    try:
        adapter = QualityMultiAgentAdapter(Path())

        # Test security expert conversion
        security_result = {
            "security_issues": ["weak_password"],
            "critical_issues": [],
            "high_issues": ["missing_authentication"],
        }

        security_score = adapter._convert_security_result(security_result, 3.0)
        if security_score:
            print(f"✅ Security score conversion: {security_score.score:.1f}")
        else:
            print("❌ Security score conversion failed")
            return False

        # Test code quality expert conversion
        code_quality_result = {
            "flake8_issues": ["E501", "F401"],
            "code_style_issues": [],
            "complexity_issues": [],
        }

        code_quality_score = adapter._convert_code_quality_result(
            code_quality_result, 2.0
        )
        if code_quality_score:
            print(f"✅ Code quality score conversion: {code_quality_score.score:.1f}")
        else:
            print("❌ Code quality score conversion failed")
            return False

        # Test test expert conversion
        test_result = {
            "coverage_percentage": 90.0,
            "test_count": 100,
            "test_failures": 1,
        }

        test_score = adapter._convert_test_result(test_result, 1.5)
        if test_score:
            print(f"✅ Test score conversion: {test_score.score:.1f}")
        else:
            print("❌ Test score conversion failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Quality score conversion test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Quality Multi-Agent Integration Test Suite")
    print("=" * 60)

    tests = [
        test_quality_multi_agent_adapter,
        test_agent_mapping_management,
        test_quality_score_conversion,
    ]

    results = []
    for test in tests:
        if await test():
            results.append(True)
        else:
            results.append(False)
        print()

    # Summary
    print("=" * 60)
    print("📊 Test Results Summary")
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("🎉 All tests passed! Multi-agent integration is working correctly.")
        return 0

    print("❌ Some tests failed. Please review the logs above.")
    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
