#!/usr/bin/env python3
"""
Test Selected Models - Focused Multi-LLM Analysis
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src" / "multi_agent_testing"))
sys.path.insert(0, str(project_root / "scripts"))

from code_quality_automation_orchestrator import CodeQualityAutomationOrchestrator


async def test_selected_models():
    """Test the multi-agent analysis system with available models"""
    print("🚀 Testing Multi-Agent Analysis System")
    print("=" * 70)

    try:
        # Initialize orchestrator
        print("🔧 Initializing orchestrator...")
        orchestrator = CodeQualityAutomationOrchestrator(".")

        # Show what models are available
        print(f"\n📊 Available Working Models: {len(orchestrator.working_models)}")
        for i, model in enumerate(orchestrator.working_models, 1):
            print(f"  {i}. {model}")

        print(f"\n📊 Provider Distribution:")
        openai_count = sum(1 for m in orchestrator.working_models if "gpt" in m)
        anthropic_count = sum(1 for m in orchestrator.working_models if "claude" in m)
        print(f"  🧠 OpenAI: {openai_count} models")
        print(f"  🤖 Anthropic: {anthropic_count} models")

        # Test the multi-agent analysis
        print(f"\n🧪 Running Multi-Agent Analysis...")
        print("-" * 70)

        # Run analysis - this will use all available working models
        result = orchestrator.run_multi_agent_analysis()

        print(f"\n📈 Analysis Results:")
        print(f"  ✅ Success: {result.get('success', False)}")
        print(f"  🔍 Issues Found: {result.get('total_issues', 0)}")
        print(f"  🧠 Models Used: {result.get('models_used', [])}")
        print(f"  💰 Total Cost: ${result.get('total_cost', 0):.6f}")

        # Show detailed cost breakdown if available
        if "cost_breakdown" in result:
            print(f"\n💰 Cost Breakdown by Model:")
            for model, cost_info in result["cost_breakdown"].items():
                tokens = cost_info.get("tokens", 0)
                cost = cost_info.get("cost", 0)
                print(f"  📊 {model}: {tokens} tokens, ${cost:.6f}")

        # Show analysis details if available
        if "security" in result:
            print(
                f"\n🔒 Security Analysis: {len(result['security']) if isinstance(result['security'], list) else 'Completed'}"
            )
        if "quality" in result:
            print(
                f"\n🔍 Quality Analysis: {len(result['quality']) if isinstance(result['quality'], list) else 'Completed'}"
            )
        if "devops" in result:
            print(
                f"\n⚙️ DevOps Analysis: {len(result['devops']) if isinstance(result['devops'], list) else 'Completed'}"
            )

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_selected_models())

    print("\n" + "=" * 70)
    if success:
        print("✅ Multi-Agent Analysis Test PASSED!")
        print("🎉 System working with available models!")
    else:
        print("❌ Multi-Agent Analysis Test FAILED!")

    print("=" * 70)
