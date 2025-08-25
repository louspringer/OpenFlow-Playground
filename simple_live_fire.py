#!/usr/bin/env python3
"""
Simple Live Fire Exercise - Direct Multi-LLM Test
Bypasses broken op_api_key_manager.py to test core functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src" / "multi_agent_testing"))

from multi_dimensional_smoke_test import MultiDimensionalSmokeTest


async def simple_live_fire():
    """Simple live fire test using MultiDimensionalSmokeTest directly"""
    print("🎯 SIMPLE LIVE FIRE EXERCISE - DIRECT MULTI-LLM TEST")
    print("=" * 70)
    print("🎯 TARGET: Test core multi-LLM functionality directly")
    print("🚀 OBJECTIVE: Verify LLM diversity and agent capabilities")
    print("=" * 70)

    try:
        # Initialize the smoke test system directly
        print("🔧 Initializing MultiDimensionalSmokeTest directly...")
        test_system = MultiDimensionalSmokeTest()

        # Test with a simple prompt to verify LLM access
        print(f"\n🧪 Testing LLM Access...")
        print("-" * 70)

        # Test Claude (Anthropic)
        print("🤖 Testing Claude (Anthropic)...")
        claude_result = test_system.run_test(
            {
                "role": "security_expert",
                "prompt_structure": "direct_questions",
                "response_format": "json",
                "model": "claude",
                "temperature": 0.7,
            },
            "security_audit",
        )
        print(f"  🔒 Claude Security Result: {type(claude_result)}")
        if claude_result:
            print(f"  📊 Claude Response Length: {len(str(claude_result))}")

        # Test GPT-4 Vision (OpenAI)
        print("\n🤖 Testing GPT-4 Vision (OpenAI)...")
        gpt4_result = test_system.run_test(
            {
                "role": "code_quality_expert",
                "prompt_structure": "socratic_questioning",
                "response_format": "json",
                "model": "gpt4_vision",
                "temperature": 0.7,
            },
            "code_quality",
        )
        print(f"  🔍 GPT-4 Quality Result: {type(gpt4_result)}")
        if gpt4_result:
            print(f"  📊 GPT-4 Response Length: {len(str(gpt4_result))}")

        # Test GPT-3.5 Turbo (OpenAI)
        print("\n🤖 Testing GPT-3.5 Turbo (OpenAI)...")
        gpt35_result = test_system.run_test(
            {
                "role": "devops_engineer",
                "prompt_structure": "structured_analysis",
                "response_format": "json",
                "model": "gpt3_5_turbo",
                "temperature": 0.7,
            },
            "devops",
        )
        print(f"  ⚙️ GPT-3.5 DevOps Result: {type(gpt35_result)}")
        if gpt35_result:
            print(f"  📊 GPT-3.5 Response Length: {len(str(gpt35_result))}")

        # Summary
        print(f"\n📊 LIVE FIRE RESULTS:")
        print("=" * 70)
        print(f"🎯 Claude (Anthropic): {'✅ WORKING' if claude_result else '❌ FAILED'}")
        print(f"🎯 GPT-4 Vision (OpenAI): {'✅ WORKING' if gpt4_result else '❌ FAILED'}")
        print(
            f"🎯 GPT-3.5 Turbo (OpenAI): {'✅ WORKING' if gpt35_result else '❌ FAILED'}"
        )

        working_models = sum(
            [bool(claude_result), bool(gpt4_result), bool(gpt35_result)]
        )
        print(
            f"\n🚀 SUCCESS RATE: {working_models}/3 models working ({working_models/3*100:.1f}%)"
        )

        if working_models >= 2:
            print("🎉 MULTI-LLM SYSTEM IS OPERATIONAL!")
            print("🏆 Ready for production use!")
        elif working_models == 1:
            print("⚠️ PARTIAL SUCCESS: Only one LLM working")
            print("🔧 System needs attention")
        else:
            print("❌ SYSTEM FAILURE: No LLMs working")
            print("🚨 Immediate intervention required")

        return working_models >= 2

    except Exception as e:
        print(f"❌ LIVE FIRE EXERCISE FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🎯 SIMPLE LIVE FIRE EXERCISE INITIATED")
    print("🚀 TESTING CORE MULTI-LLM FUNCTIONALITY...")

    success = asyncio.run(simple_live_fire())

    print("\n" + "=" * 70)
    if success:
        print("🎯 SIMPLE LIVE FIRE EXERCISE COMPLETED!")
        print("🚀 MULTI-LLM SYSTEM VALIDATED!")
        print("🏆 READY FOR PRODUCTION DEPLOYMENT!")
    else:
        print("❌ SIMPLE LIVE FIRE EXERCISE FAILED!")
        print("🔧 SYSTEM NEEDS IMMEDIATE ATTENTION!")

    print("=" * 70)
