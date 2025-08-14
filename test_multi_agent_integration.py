#!/usr/bin/env python3
"""
Test script for multi-agent integration

This script tests the basic integration between the framework, core, and agents.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directories to the path
sys.path.insert(0, str(Path(__file__).parent / "clewcrew-framework" / "src"))
sys.path.insert(0, str(Path(__file__).parent / "clewcrew-core" / "src"))
sys.path.insert(0, str(Path(__file__).parent / "clewcrew-agents" / "src"))


async def test_agent_imports():
    """Test that all expert agents can be imported"""
    print("Testing agent imports...")

    try:
        from clewcrew_agents import (  # noqa: F401
            ArchitectureExpert,
            BuildExpert,
            CodeQualityExpert,
            DevOpsExpert,
            MCPExpert,
            ModelExpert,
            SecurityExpert,
            TestExpert,
        )

        print("✅ All expert agents imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import agents: {e}")
        return False


async def test_orchestrator_import():
    """Test that the orchestrator can be imported"""
    print("Testing orchestrator import...")

    try:
        from clewcrew_core import ClewcrewOrchestrator  # noqa: F401

        print("✅ Orchestrator imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import orchestrator: {e}")
        return False


async def test_framework_cli():
    """Test that the framework CLI can be imported"""
    print("Testing framework CLI import...")

    try:
        from clewcrew_framework.cli import main  # noqa: F401

        print("✅ Framework CLI imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import framework CLI: {e}")
        return False


async def test_orchestrator_creation():
    """Test that the orchestrator can be created"""
    print("Testing orchestrator creation...")

    try:
        from clewcrew_core import ClewcrewOrchestrator

        orchestrator = ClewcrewOrchestrator(".")
        print("✅ Orchestrator created successfully")

        # Test that agents are initialized
        print(f"   - Agents: {list(orchestrator.agents.keys())}")
        print(f"   - Validators: {list(orchestrator.validators.keys())}")
        print(f"   - Recovery Engines: {list(orchestrator.recovery_engines.keys())}")

        return True
    except Exception as e:
        print(f"❌ Failed to create orchestrator: {e}")
        return False


async def test_agent_detection():
    """Test that agents can detect hallucinations"""
    print("Testing agent hallucination detection...")

    try:
        from clewcrew_agents import SecurityExpert

        expert = SecurityExpert()
        result = await expert.detect_hallucinations(Path())

        print("✅ Security expert detection completed")
        print(f"   - Confidence: {result.confidence}")
        print(f"   - Hallucinations: {len(result.hallucinations)}")
        print(f"   - Recommendations: {len(result.recommendations)}")

        return True
    except Exception as e:
        print(f"❌ Failed to test agent detection: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Testing Multi-Agent Integration")
    print("=" * 50)

    tests = [
        test_agent_imports,
        test_orchestrator_import,
        test_framework_cli,
        test_orchestrator_creation,
        test_agent_detection,
    ]

    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()

    # Summary
    print("=" * 50)
    print("📊 Test Results Summary")
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("🎉 All tests passed! Multi-agent integration is working.")
        return 0

    print("❌ Some tests failed. Check the output above for details.")
    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
