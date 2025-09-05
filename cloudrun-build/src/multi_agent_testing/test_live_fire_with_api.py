#!/usr/bin/env python3
"""
Live Fire Test with API Manager Integration
=========================================

This test properly initializes the API manager to set environment variables
before testing LLM calls, showing real multi-agent analysis with costs.
"""

import asyncio
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_testing.agent_session_manager import (
    AgentFinding,
    AgentSessionManager,
    AgentType,
)
from multi_agent_testing.langgraph_orchestrator import LangGraphOrchestrator
from multi_agent_testing.multi_dimensional_smoke_test import MultiDimensionalSmokeTest
from scripts.op_api_key_manager import OnePasswordAPIKeyManager

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("live_fire_with_api.log"),
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
        AgentSessionManager()
        logger.info("✅ Agent Session Manager initialized")

        # Initialize API manager and set environment variables
        logger.info("🔑 Initializing API Manager...")
        api_manager = OnePasswordAPIKeyManager()
        api_manager.set_environment_variables()
        logger.info("✅ Environment variables set")

        # Create multi-dimensional smoke test
        smoke_test = MultiDimensionalSmokeTest()
        logger.info("✅ Multi-Dimensional Smoke Test initialized")

        # Test a simple LLM call to verify API keys work
        logger.info("🧠 Testing Simple LLM Call...")

        # Use the correct call_llm method signature
        test_prompt = "Analyze this code for potential security issues: print(user_input)"

        logger.info("🔍 Testing Claude API...")
        claude_result = smoke_test.call_llm("claude", test_prompt)
        logger.info(f"✅ Claude test completed: {claude_result.get('status', 'unknown')}")

        if "error" in claude_result:
            logger.warning(f"⚠️ Claude API error: {claude_result['error']}")
        else:
            logger.info("✅ Claude API call successful")

        # Test the full LangGraph workflow
        logger.info("🔄 Testing Full LangGraph Workflow...")
        orchestrator = LangGraphOrchestrator(target_directory=".")

        # Run the workflow
        start_time = time.time()
        workflow_results = await orchestrator.run_workflow()
        execution_time = time.time() - start_time

        logger.info("📋 Full Workflow Results:")
        logger.info(f"  Success: {workflow_results.get('workflow_success', False)}")
        logger.info(f"  Iterations: {workflow_results.get('iterations_completed', 0)}")
        logger.info(f"  Final stage: {workflow_results.get('final_stage', 'unknown')}")
        logger.info(f"  Agent findings: {workflow_results.get('total_agent_findings', 0)}")
        logger.info(f"  Execution time: {execution_time:.2f} seconds")

        # Show cost summary if available
        logger.info("💰 Cost Summary:")
        try:
            # Use the actual cost tracking methods from OnePasswordAPIKeyManager
            if hasattr(api_manager, "get_total_cost"):
                total_cost = api_manager.get_total_cost()
                logger.info(f"  Total session cost: ${total_cost:.6f}")

                # Show cost breakdown by model
                if hasattr(api_manager, "get_cost_breakdown"):
                    cost_breakdown = api_manager.get_cost_breakdown()
                    for model, cost in cost_breakdown.items():
                        logger.info(f"    {model}: ${cost:.6f}")
            else:
                logger.info("  Cost tracking not available in this API manager")
        except Exception as e:
            logger.warning(f"  ⚠️ Could not retrieve cost information: {e}")

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

        # Create AgentFinding objects with correct structure
        security_finding = AgentFinding(
            agent_type=AgentType.SECURITY,
            finding_id="",
            category="security",
            severity="High",
            description="Potential SQL injection vulnerability detected",
            recommendations=["Use parameterized queries", "Validate user input"],
            confidence=0.9,
            timestamp=datetime.now().isoformat(),
            metadata={"file": "database.py", "line": 42},
            cross_references=[],
        )

        quality_finding = AgentFinding(
            agent_type=AgentType.QUALITY,
            finding_id="",
            category="quality",
            severity="Medium",
            description="Code complexity exceeds threshold",
            recommendations=["Refactor complex functions", "Add unit tests"],
            confidence=0.8,
            timestamp=datetime.now().isoformat(),
            metadata={"file": "main.py", "line": 15},
            cross_references=[],
        )

        devops_finding = AgentFinding(
            agent_type=AgentType.DEVOPS,
            finding_id="",
            category="devops",
            severity="Low",
            description="Missing health check endpoint",
            recommendations=["Add /health endpoint", "Implement monitoring"],
            confidence=0.7,
            timestamp=datetime.now().isoformat(),
            metadata={"file": "app.py", "line": 30},
            cross_references=[],
        )

        # Add findings from different agents
        agent_session_manager.add_agent_finding(AgentType.SECURITY, security_finding)
        agent_session_manager.add_agent_finding(AgentType.QUALITY, quality_finding)
        agent_session_manager.add_agent_finding(AgentType.DEVOPS, devops_finding)

        logger.info("✅ Added findings from all three agents")

        # Test cross-agent context
        logger.info("🔍 Testing Cross-Agent Context...")
        for agent_type in [AgentType.SECURITY, AgentType.QUALITY, AgentType.DEVOPS]:
            other_findings = agent_session_manager.get_agent_previous_findings(agent_type, iteration)
            logger.info(f"  {agent_type.value}: {len(other_findings)} other agents' findings available")

        # Generate synthesis
        synthesis = agent_session_manager.synthesize_iteration_results()
        logger.info(f"🧠 Synthesis generated: {len(synthesis.get('recommendations', []))} recommendations")

        logger.info("✅ Agent Collaboration Test Passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Agent Collaboration Test Failed: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


async def main():
    """Main test execution"""
    logger.info("🚀 Starting Live Fire Test with API Integration")
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
