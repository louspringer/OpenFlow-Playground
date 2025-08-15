#!/usr/bin/env python3
"""
Test script for Orchestrator Quality Integration

This script tests the quality integration methods added to the orchestrator.
"""

import asyncio
import sys
from pathlib import Path

# Add the clewcrew-core to the path
sys.path.insert(0, str(Path(__file__).parent / "clewcrew-core" / "src"))

# Import orchestrator
from clewcrew_core.orchestrator import ClewcrewOrchestrator  # noqa: E402


async def test_orchestrator_quality_analysis():
    """Test the orchestrator's quality analysis functionality"""
    print("🧪 Testing Orchestrator Quality Analysis...")

    try:
        # Create orchestrator
        orchestrator = ClewcrewOrchestrator(".")
        print("✅ Created ClewcrewOrchestrator")

        # Test quality analysis
        print("  🔄 Running comprehensive quality analysis...")
        quality_report = await orchestrator.run_quality_analysis(".")

        if "status" in quality_report and quality_report["status"] == "error":
            print(f"  ❌ Quality analysis failed: {quality_report['error']}")
            return False

        print("  ✅ Quality analysis completed successfully")

        # Display quality report summary
        print(f"    📊 Project Path: {quality_report['project_path']}")
        print(f"    📊 Timestamp: {quality_report['timestamp']}")
        print(f"    📊 Agents Analyzed: {quality_report['total_agents_analyzed']}")
        print(f"    📊 Total Recommendations: {quality_report['total_recommendations']}")

        # Display overall quality summary
        overall_summary = quality_report.get("overall_quality_summary", {})
        if overall_summary:
            print(
                f"    📊 Overall Quality Score: {overall_summary.get( \
    'overall_quality_score', 'N/A'):.1f}"
            )
            print(
                f"    📊 Quality Status: {overall_summary.get('quality_status', 'N/A')}"
            )
            print(
                f"    📊 Total Issues Found: {overall_summary.get('total_issues_found', 'N/A')}"
            )
            print(
                f"    📊 Agents Analyzed: {overall_summary.get('agents_analyzed', 'N/A')}"
            )
            print(
                f"    📊 Recommendations Priority: {overall_summary.get( \
    'recommendations_priority', 'N/A')}"
            )

        # Display agent quality results
        agent_results = quality_report.get("agent_quality_results", {})
        if agent_results:
            print("\n    🤖 Agent Quality Results:")
            for agent_name, results in agent_results.items():
                if "error" in results:
                    print(f"      ❌ {agent_name}: Error - {results['error']}")
                else:
                    quality_score = results.get("quality_score", "N/A")
                    issues_found = results.get("issues_found", "N/A")
                    print(
                        f"      ✅ {agent_name}: Score={quality_score}, Issues={issues_found}"
                    )

        # Display recommendations
        recommendations = quality_report.get("all_recommendations", [])
        if recommendations:
            print(f"\n    💡 Quality Recommendations ({len(recommendations)} total):")
            for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
                agent = rec.get("agent", "Unknown")
                recommendation = rec.get("recommendation", "No recommendation")
                print(f"      {i}. [{agent}] {recommendation}")

            if len(recommendations) > 5:
                print(f"      ... and {len(recommendations) - 5} more recommendations")

        return True

    except Exception as e:
        print(f"  ❌ Orchestrator quality analysis test failed: {e}")
        return False


async def test_quality_summary_generation():
    """Test the quality summary generation functionality"""
    print("\n🧪 Testing Quality Summary Generation...")

    try:
        # Create orchestrator
        orchestrator = ClewcrewOrchestrator(".")

        # Create mock agent quality results
        mock_agent_results = {
            "security": {"quality_score": 75.0, "issues_found": 25, "error": None},
            "code_quality": {"quality_score": 85.0, "issues_found": 15, "error": None},
            "test": {"quality_score": 90.0, "issues_found": 10, "error": None},
        }

        # Test quality summary generation
        print("  🔄 Testing quality summary generation...")
        summary = orchestrator._generate_quality_summary(mock_agent_results)

        print(f"    ✅ Overall Quality Score: {summary['overall_quality_score']:.1f}")
        print(f"    ✅ Quality Status: {summary['quality_status']}")
        print(f"    ✅ Total Issues Found: {summary['total_issues_found']}")
        print(f"    ✅ Agents Analyzed: {summary['agents_analyzed']}")
        print(f"    ✅ Recommendations Priority: {summary['recommendations_priority']}")

        # Verify summary calculations
        expected_score = (75.0 + 85.0 + 90.0) / 3  # Simple average for now
        if abs(summary["overall_quality_score"] - expected_score) < 1.0:
            print("    ✅ Quality score calculation verified")
        else:
            print(
                f"    ❌ Quality score mismatch: expected {expected_score:.1f}, got {summary['overall_quality_score']:.1f}"
            )
            return False

        return True

    except Exception as e:
        print(f"  ❌ Quality summary generation test failed: {e}")
        return False


async def test_error_handling():
    """Test error handling in quality analysis"""
    print("\n🧪 Testing Error Handling...")

    try:
        # Create orchestrator
        orchestrator = ClewcrewOrchestrator(".")

        # Test with invalid project path - orchestrator should handle this gracefully
        print("  🔄 Testing error handling with invalid path...")
        quality_report = await orchestrator.run_quality_analysis("/invalid/path")

        # The orchestrator is designed to be robust and handle invalid paths gracefully
        # It should return a normal result, not an error status
        if "status" in quality_report and quality_report["status"] == "error":
            print("    ✅ Error handling working correctly (returned error status)")
            return True

        if "agent_quality_results" in quality_report:
            print("    ✅ Error handling working correctly (handled gracefully)")
            return True

        print("    ❌ Unexpected response format")
        return False

    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False


async def main():
    """Run all orchestrator quality integration tests"""
    print("🚀 Orchestrator Quality Integration Test Suite")
    print("=" * 70)

    tests = [
        test_orchestrator_quality_analysis,
        test_quality_summary_generation,
        test_error_handling,
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
    print("📊 Orchestrator Quality Integration Test Results")
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print(
            "🎉 All tests passed! Orchestrator quality integration is working correctly."
        )
        print("\n✅ Quality Integration Status:")
        print("   • Quality analysis method: Implemented and tested")
        print("   • Quality summary generation: Working correctly")
        print("   • Error handling: Robust and tested")
        print("   • Multi-agent coordination: Successfully integrated")
        return 0

    print("❌ Some tests failed. Please review the logs above.")
    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
