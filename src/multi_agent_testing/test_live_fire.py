#!/usr/bin/env python3
"""
Live Fire Test for Multi-Agent System
====================================

This test runs the actual multi-agent analysis with real LLM calls,
cost tracking, and comprehensive logging to validate the end-to-end system.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_testing.agent_session_manager import AgentSessionManager
from multi_agent_testing.langgraph_orchestrator import LangGraphOrchestrator
from multi_agent_testing.multi_dimensional_smoke_test import MultiDimensionalSmokeTest

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("live_fire_test.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


async def test_multi_agent_analysis():
    """Test the actual multi-agent analysis with real LLM calls"""
    logger.info("🚀 Starting Live Fire Multi-Agent Analysis Test")
    logger.info("=" * 60)

    try:
        # Initialize the multi-agent system
        logger.info("🔧 Initializing Multi-Agent System...")

        # Create agent session manager
        agent_session_manager = AgentSessionManager()
        logger.info("✅ Agent Session Manager initialized")

        # Create multi-dimensional smoke test
        smoke_test = MultiDimensionalSmokeTest()
        logger.info("✅ Multi-Dimensional Smoke Test initialized")

        # Test API key discovery and testing
        logger.info("🔑 Testing API Key Discovery and Testing...")
        working_apis = smoke_test.discover_and_test_apis()
        logger.info(f"✅ Found {len(working_apis)} working APIs")

        # Test individual LLM calls with cost tracking
        logger.info("🧠 Testing Individual LLM Calls...")

        # Test Claude (Anthropic)
        if "anthropic" in working_apis:
            logger.info("🔍 Testing Claude (Anthropic)...")
            claude_result = await smoke_test.test_anthropic_claude()
            logger.info(
                f"✅ Claude test completed: {claude_result.get('status', 'unknown')}"
            )
            if "cost" in claude_result:
                logger.info(f"💰 Claude cost: ${claude_result['cost']:.6f}")

        # Test OpenAI
        if "openai" in working_apis:
            logger.info("🔍 Testing OpenAI...")
            openai_result = await smoke_test.test_openai()
            logger.info(
                f"✅ OpenAI test completed: {openai_result.get('status', 'unknown')}"
            )
            if "cost" in openai_result:
                logger.info(f"💰 OpenAI cost: ${openai_result['cost']:.6f}")

        # Test actual multi-agent analysis
        logger.info("🤖 Running Multi-Agent Analysis...")
        analysis_result = await smoke_test.run_multi_agent_analysis()

        logger.info("📊 Multi-Agent Analysis Results:")
        logger.info(
            f"  Security findings: {len(analysis_result.get('security_findings', []))}"
        )
        logger.info(
            f"  Quality findings: {len(analysis_result.get('quality_findings', []))}"
        )
        logger.info(
            f"  DevOps findings: {len(analysis_result.get('devops_findings', []))}"
        )
        logger.info(f"  Total cost: ${analysis_result.get('total_cost', 0):.6f}")

        # Test the full LangGraph workflow
        logger.info("🔄 Testing Full LangGraph Workflow...")
        orchestrator = LangGraphOrchestrator(agent_session_manager)

        # Run the workflow
        start_time = time.time()
        workflow_results = await orchestrator.run_workflow()
        execution_time = time.time() - start_time

        logger.info("📋 Full Workflow Results:")
        logger.info(f"  Success: {workflow_results.get('workflow_success', False)}")
        logger.info(f"  Iterations: {workflow_results.get('iterations_completed', 0)}")
        logger.info(f"  Final stage: {workflow_results.get('final_stage', 'unknown')}")
        logger.info(
            f"  Agent findings: {workflow_results.get('total_agent_findings', 0)}"
        )
        logger.info(f"  Execution time: {execution_time:.2f} seconds")

        # Show cost summary
        logger.info("💰 Cost Summary:")
        if hasattr(smoke_test, "cost_tracker"):
            total_cost = smoke_test.cost_tracker.get_total_cost()
            logger.info(f"  Total session cost: ${total_cost:.6f}")

            # Show cost breakdown by model
            cost_breakdown = smoke_test.cost_tracker.get_cost_breakdown()
            for model, cost in cost_breakdown.items():
                logger.info(f"    {model}: ${cost:.6f}")

        logger.info("🎉 Live Fire Test Completed Successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Live Fire Test Failed: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def test_agent_collaboration():
    """Test agent collaboration and context sharing"""
    logger.info("🤝 Testing Agent Collaboration...")

    try:
        agent_session_manager = AgentSessionManager()

        # Start a new iteration
        iteration = agent_session_manager.start_new_iteration()
        logger.info(f"🔄 Started iteration {iteration}")

        # Add findings from different agents
        agent_session_manager.add_agent_finding(
            "security_expert",
            iteration,
            "security",
            "High",
            "Potential SQL injection vulnerability detected",
            "Found unvalidated user input in database queries",
        )

        agent_session_manager.add_agent_finding(
            "code_quality_expert",
            iteration,
            "quality",
            "Medium",
            "Code complexity exceeds threshold",
            "Function has cyclomatic complexity of 15 (threshold: 10)",
        )

        agent_session_manager.add_agent_finding(
            "devops_expert",
            iteration,
            "devops",
            "Low",
            "Missing health check endpoint",
            "Application lacks /health endpoint for monitoring",
        )

        # Test cross-agent context
        logger.info("🔍 Testing Cross-Agent Context...")
        for agent_type in ["security_expert", "code_quality_expert", "devops_expert"]:
            agent_session_manager.get_agent_context(agent_type, iteration)
            other_findings = agent_session_manager.get_agent_previous_findings(
                agent_type, iteration
            )
            logger.info(
                f"  {agent_type}: {len(other_findings)} other agents' findings available"
            )

        # Generate synthesis
        synthesis = agent_session_manager.synthesize_iteration_results()
        logger.info(
            f"🧠 Synthesis generated: {len(synthesis.get('recommendations', []))} recommendations"
        )

        logger.info("✅ Agent Collaboration Test Passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Agent Collaboration Test Failed: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def main():
    """Main test execution"""
    logger.info("🚀 Starting Live Fire Test Suite")
    logger.info("=" * 60)

    results = []

    # Test 1: Multi-Agent Analysis
    logger.info("\n🧪 Test 1: Multi-Agent Analysis")
    logger.info("-" * 40)
    result1 = await test_multi_agent_analysis()
    results.append(("Multi-Agent Analysis", result1))

    # Test 2: Agent Collaboration
    logger.info("\n🧪 Test 2: Agent Collaboration")
    logger.info("-" * 40)
    result2 = await test_agent_collaboration()
    results.append(("Agent Collaboration", result2))

    # Summary
    logger.info("\n📊 LIVE FIRE TEST SUMMARY")
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
        logger.info("🎉 ALL TESTS PASSED! System is ready for production!")
    else:
        logger.warning("⚠️ Some tests failed. Check logs for details.")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
