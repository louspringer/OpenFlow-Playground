#!/usr/bin/env python3
"""
Test Integrated Workflow - End-to-End LangGraph Workflow Testing

This script tests the complete integrated system:
1. Step model validation
2. Agent session management
3. LangGraph workflow execution
4. Real tool integration
5. Multi-agent collaboration
"""

import asyncio
import sys
import time
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from multi_agent_testing.agent_session_manager import AgentSessionManager
    from multi_agent_testing.langgraph_orchestrator import LangGraphOrchestrator
    from multi_agent_testing.step_model import CODE_QUALITY_WORKFLOW, StepModelBuilder
except ImportError:
    # Fallback for direct execution
    from agent_session_manager import AgentSessionManager
    from langgraph_orchestrator import LangGraphOrchestrator
    from step_model import CODE_QUALITY_WORKFLOW, StepModelBuilder


async def test_step_model():
    """Test the step model validation"""
    print("🧪 Testing Step Model")
    print("=" * 40)

    # Validate the workflow model
    errors = StepModelBuilder.validate_workflow_model(CODE_QUALITY_WORKFLOW)

    if errors:
        print("❌ Step model validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ Step model validation passed!")
    print(f"📋 Workflow: {CODE_QUALITY_WORKFLOW.name}")
    print(f"🔄 Steps: {len(CODE_QUALITY_WORKFLOW.steps)}")

    return True


async def test_agent_session_manager():
    """Test the agent session manager"""
    print("\n🧪 Testing Agent Session Manager")
    print("=" * 40)

    try:
        # Initialize session manager
        session_manager = AgentSessionManager("test_integrated_sessions")

        # Start new iteration
        iteration = session_manager.start_new_iteration()
        print(f"✅ Started iteration {iteration}")

        # Test context updates
        from multi_agent_testing.agent_session_manager import AgentType

        for agent_type in AgentType:
            session_manager.update_agent_context(
                agent_type, {"test_context": f"Test context for {agent_type.value}"}
            )
            print(f"✅ Updated context for {agent_type.value}")

        # Test cross-agent context
        for agent_type in AgentType:
            cross_context = session_manager.get_cross_agent_context(agent_type)
            other_agents = len(cross_context.get("other_agents_findings", {}))
            print(f"✅ {agent_type.value} cross-context: {other_agents} other agents")

        # Test synthesis
        synthesis = session_manager.synthesize_iteration_results()
        print(
            f"✅ Synthesis generated: {len(synthesis.get('recommendations', []))} recommendations"
        )

        return True

    except Exception as e:
        print(f"❌ Agent session manager test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_langgraph_orchestrator():
    """Test the LangGraph orchestrator"""
    print("\n🧪 Testing LangGraph Orchestrator")
    print("=" * 40)

    try:
        # Initialize orchestrator
        orchestrator = LangGraphOrchestrator(".", "test_integrated_sessions")

        # Show workflow summary
        summary = orchestrator.get_workflow_summary()
        print("📊 Workflow Summary:")
        print(f"  Current iteration: {summary['current_iteration']}")
        print(f"  Total iterations: {summary['total_iterations']}")
        print(f"  Workflow available: {summary['workflow_available']}")

        return True

    except Exception as e:
        print(f"❌ LangGraph orchestrator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_workflow_execution():
    """Test the complete workflow execution"""
    print("\n🧪 Testing Complete Workflow Execution")
    print("=" * 40)

    try:
        # Initialize orchestrator
        orchestrator = LangGraphOrchestrator(".", "test_integrated_sessions")

        print("🚀 Starting complete workflow...")
        start_time = time.time()

        # Run the workflow
        results = await orchestrator.run_workflow()

        end_time = time.time()
        execution_time = end_time - start_time

        # Display results
        print("\n📋 Workflow Results:")
        print(f"  Success: {results['workflow_success']}")
        print(f"  Iterations completed: {results['iterations_completed']}")
        print(f"  Final stage: {results['final_stage']}")
        print(f"  Total agent findings: {results['total_agent_findings']}")
        print(f"  Execution time: {execution_time:.2f} seconds")

        if results.get("synthesis"):
            synthesis = results["synthesis"]
            print(
                f"  Cross-agent patterns: {len(synthesis.get('cross_agent_patterns', []))}"
            )
            print(
                f"  Collaborative insights: {len(synthesis.get('collaborative_insights', []))}"
            )
            print(f"  Recommendations: {len(synthesis.get('recommendations', []))}")

        if results.get("learning_outcomes"):
            print(f"  Learning outcomes: {len(results['learning_outcomes'])}")
            for outcome in results["learning_outcomes"][:3]:  # Show first 3
                print(f"    - {outcome}")

        if results.get("error_message"):
            print(f"  Error: {results['error_message']}")

        # Show final workflow summary
        final_summary = orchestrator.get_workflow_summary()
        print("\n📊 Final Workflow Summary:")
        print(f"  Current iteration: {final_summary['current_iteration']}")
        print(f"  Total iterations: {final_summary['total_iterations']}")

        if final_summary.get("learning_summary"):
            learning = final_summary["learning_summary"]
            print(f"  Cumulative findings: {learning.get('cumulative_findings', 0)}")

        return results["workflow_success"]

    except Exception as e:
        print(f"❌ Workflow execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_agent_collaboration():
    """Test agent collaboration and context sharing"""
    print("\n🧪 Testing Agent Collaboration")
    print("=" * 40)

    try:
        from multi_agent_testing.agent_session_manager import AgentType

        # Initialize session manager
        session_manager = AgentSessionManager("test_collaboration_sessions")

        # Start new iteration
        iteration = session_manager.start_new_iteration()
        print(f"✅ Started collaboration iteration {iteration}")

        # Simulate agent findings
        from datetime import datetime

        from multi_agent_testing.agent_session_manager import AgentFinding

        # Security expert findings
        security_finding = AgentFinding(
            agent_type=AgentType.SECURITY,
            finding_id="sec_collab_001",
            category="security",
            severity="high",
            description="Potential security vulnerability in authentication",
            recommendations=["Implement proper input validation", "Add rate limiting"],
            confidence=0.9,
            timestamp=datetime.now().isoformat(),
            metadata={"test": True},
            cross_references=[],
        )

        session_manager.add_agent_finding(AgentType.SECURITY, security_finding)
        print("✅ Added security finding")

        # Quality expert findings
        quality_finding = AgentFinding(
            agent_type=AgentType.QUALITY,
            finding_id="qual_collab_001",
            category="code_quality",
            severity="medium",
            description="Code complexity could be reduced",
            recommendations=["Extract complex methods", "Add type hints"],
            confidence=0.8,
            timestamp=datetime.now().isoformat(),
            metadata={"test": True},
            cross_references=[],
        )

        session_manager.add_agent_finding(AgentType.QUALITY, quality_finding)
        print("✅ Added quality finding")

        # DevOps expert findings
        devops_finding = AgentFinding(
            agent_type=AgentType.DEVOPS,
            finding_id="devops_collab_001",
            category="devops",
            severity="low",
            description="Deployment pipeline could be optimized",
            recommendations=["Add parallel stages", "Implement caching"],
            confidence=0.7,
            timestamp=datetime.now().isoformat(),
            metadata={"test": True},
            cross_references=[],
        )

        session_manager.add_agent_finding(AgentType.DEVOPS, devops_finding)
        print("✅ Added DevOps finding")

        # Test cross-agent context
        print("\n🔍 Testing Cross-Agent Context:")
        for agent_type in AgentType:
            cross_context = session_manager.get_cross_agent_context(agent_type)
            other_agents = len(cross_context.get("other_agents_findings", {}))
            print(
                f"  {agent_type.value}: {other_agents} other agents' findings available"
            )

        # Test synthesis
        synthesis = session_manager.synthesize_iteration_results()
        print("\n🧠 Synthesis Results:")
        print(f"  Total findings: {synthesis.get('total_findings', 0)}")
        print(
            f"  Cross-agent patterns: {len(synthesis.get('cross_agent_patterns', []))}"
        )
        print(
            f"  Collaborative insights: {len(synthesis.get('collaborative_insights', []))}"
        )
        print(f"  Recommendations: {len(synthesis.get('recommendations', []))}")

        # Show some recommendations
        if synthesis.get("recommendations"):
            print("\n📋 Top Recommendations:")
            for i, rec in enumerate(synthesis["recommendations"][:3]):
                print(f"  {i+1}. {rec}")

        return True

    except Exception as e:
        print(f"❌ Agent collaboration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    print("🚀 Integrated Workflow Test Suite")
    print("=" * 60)

    try:
        # Run all tests
        tests = [
            ("Step Model", test_step_model),
            ("Agent Session Manager", test_agent_session_manager),
            ("LangGraph Orchestrator", test_langgraph_orchestrator),
            ("Agent Collaboration", test_agent_collaboration),
            ("Complete Workflow", test_workflow_execution),
        ]

        results = {}
        all_passed = True

        for test_name, test_func in tests:
            print(f"\n{'='*60}")
            print(f"🧪 Running: {test_name}")
            print(f"{'='*60}")

            try:
                result = await test_func()
                results[test_name] = result

                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
                    all_passed = False

            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = False
                all_passed = False

        # Summary
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")

        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {test_name}: {status}")

        if all_passed:
            print("\n🎉 All tests passed! The integrated workflow is working!")
            print("🚀 Ready for production use!")
        else:
            print("\n⚠️ Some tests failed. Check the output above for details.")

        return all_passed

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the async tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
