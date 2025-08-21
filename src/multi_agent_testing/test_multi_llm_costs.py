#!/usr/bin/env python3
"""
Multi-LLM Cost Test
===================

This test directly runs the multi-agent analysis to see real costs
from both Claude and OpenAI LLMs, bypassing workflow limits.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_testing.code_quality_automation_orchestrator import (
    CodeQualityAutomationOrchestrator,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("multi_llm_cost_test.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


async def test_multi_llm_analysis():
    """Test multi-LLM analysis with real cost tracking"""
    logger.info("🚀 Starting Multi-LLM Cost Test")
    logger.info("=" * 60)

    try:
        # Initialize the orchestrator
        logger.info("🔧 Initializing Code Quality Orchestrator...")
        orchestrator = CodeQualityAutomationOrchestrator(".")

        # Check what LLMs are available
        logger.info(f"📊 Available LLMs: {orchestrator.working_models}")
        logger.info(f"🔑 API Manager: {type(orchestrator.api_manager).__name__}")

        if not orchestrator.working_models:
            logger.error("❌ No working LLMs found!")
            return False

        # Show initial cost state
        if orchestrator.api_manager:
            logger.info("💰 Initial Cost State:")
            try:
                if hasattr(orchestrator.api_manager, "get_total_cost"):
                    initial_cost = orchestrator.api_manager.get_total_cost()
                    logger.info(f"  Total cost before test: ${initial_cost:.6f}")
                else:
                    logger.info("  Cost tracking methods not available")
            except Exception as e:
                logger.warning(f"  ⚠️ Could not get initial cost: {e}")

        # Run the actual multi-agent analysis
        logger.info("\n🤖 Running Multi-Agent Analysis...")
        start_time = time.time()

        analysis_result = orchestrator.run_multi_agent_analysis()

        execution_time = time.time() - start_time
        logger.info(f"⏱️ Analysis completed in {execution_time:.2f} seconds")

        # Check the results
        if analysis_result.get("success"):
            logger.info("✅ Multi-agent analysis completed successfully")

            # Show analysis results
            analysis_results = analysis_result.get("analysis_results", {})
            for perspective, result in analysis_results.items():
                if isinstance(result, dict):
                    logger.info(f"\n📊 {perspective.title()} Analysis Results:")
                    logger.info(f"  LLMs used: {result.get('llms_used', 'Unknown')}")
                    logger.info(f"  Total findings: {result.get('total_findings', 0)}")
                    logger.info(
                        f"  Total recommendations: {result.get('total_recommendations', 0)}"
                    )
                    logger.info(f"  Total insights: {result.get('total_insights', 0)}")
                else:
                    logger.info(f"\n📊 {perspective.title()}: {result}")
        else:
            logger.error(
                f"❌ Multi-agent analysis failed: {analysis_result.get('error')}"
            )
            return False

        # Show final cost state
        if orchestrator.api_manager:
            logger.info("\n💰 Final Cost State:")
            try:
                if hasattr(orchestrator.api_manager, "get_total_cost"):
                    final_cost = orchestrator.api_manager.get_total_cost()
                    logger.info(f"  Total cost after test: ${final_cost:.6f}")

                    if hasattr(orchestrator.api_manager, "get_cost_breakdown"):
                        cost_breakdown = orchestrator.api_manager.get_cost_breakdown()
                        logger.info("  Cost breakdown by model:")
                        for model, cost in cost_breakdown.items():
                            logger.info(f"    {model}: ${cost:.6f}")
                else:
                    logger.info("  Cost tracking methods not available")
            except Exception as e:
                logger.warning(f"  ⚠️ Could not get final cost: {e}")

        # Show cost summary if available
        if orchestrator.api_manager:
            logger.info("\n💰 Cost Summary:")
            try:
                if hasattr(orchestrator.api_manager, "print_cost_summary"):
                    orchestrator.api_manager.print_cost_summary()
                else:
                    logger.info("  print_cost_summary method not available")
            except Exception as e:
                logger.warning(f"  ⚠️ Could not print cost summary: {e}")

        logger.info("🎉 Multi-LLM Cost Test Completed Successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Multi-LLM Cost Test Failed: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def test_direct_llm_calls():
    """Test direct LLM calls to see individual costs"""
    logger.info("\n🧪 Testing Direct LLM Calls...")

    try:
        # Import the smoke test system
        from multi_agent_testing.multi_dimensional_smoke_test import (
            MultiDimensionalSmokeTest,
        )

        # Initialize the smoke test
        smoke_test = MultiDimensionalSmokeTest()

        # Test prompt
        test_prompt = (
            "Analyze this code for potential security issues: print(user_input)"
        )

        # Test Claude
        logger.info("🔒 Testing Claude...")
        claude_result = smoke_test.call_llm("claude", test_prompt)
        logger.info(f"  Claude result: {claude_result.get('status', 'unknown')}")

        # Test OpenAI
        logger.info("🤖 Testing OpenAI...")
        openai_result = smoke_test.call_llm("gpt4_vision", test_prompt)
        logger.info(f"  OpenAI result: {openai_result.get('status', 'unknown')}")

        logger.info("✅ Direct LLM calls completed")
        return True

    except Exception as e:
        logger.error(f"❌ Direct LLM calls failed: {e}")
        return False


async def main():
    """Main test execution"""
    logger.info("🚀 Starting Multi-LLM Cost Test Suite")
    logger.info("=" * 60)

    results = []

    # Test 1: Multi-Agent Analysis
    logger.info("\n🧪 Test 1: Multi-Agent Analysis")
    logger.info("-" * 40)
    result1 = await test_multi_llm_analysis()
    results.append(("Multi-Agent Analysis", result1))

    # Test 2: Direct LLM Calls
    logger.info("\n🧪 Test 2: Direct LLM Calls")
    logger.info("-" * 40)
    result2 = await test_direct_llm_calls()
    results.append(("Direct LLM Calls", result2))

    # Summary
    logger.info("\n📊 MULTI-LLM COST TEST SUMMARY")
    logger.info("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1

    logger.info(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! Multi-LLM cost tracking is working!")
    else:
        logger.warning("⚠️ Some tests failed. Check logs for details.")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
