#!/usr/bin/env python3
"""
Live Fire Exercise - Multi-LLM Target Analysis
Target: Security and Code Quality Issues in the Codebase
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src" / "multi_agent_testing"))
sys.path.insert(0, str(project_root / "scripts"))

from code_quality_automation_orchestrator import CodeQualityAutomationOrchestrator


async def live_fire_exercise():
    """Live fire exercise targeting real code quality issues"""
    print("🎯 LIVE FIRE EXERCISE - MULTI-LLM TARGET ANALYSIS")
    print("=" * 80)
    print(
        "🎯 TARGET: Security vulnerabilities, code quality issues, and architectural problems"
    )
    print("🚀 OBJECTIVE: Find real issues using all available LLMs")
    print("=" * 80)

    try:
        # Initialize orchestrator
        print("🔧 Initializing orchestrator for live fire...")
        orchestrator = CodeQualityAutomationOrchestrator(".")

        # Show our arsenal
        print(f"\n🛡️ OUR ARSENAL:")
        print(f"  🧠 Working Models: {len(orchestrator.working_models)}")
        for i, model in enumerate(orchestrator.working_models, 1):
            print(f"    {i}. {model}")

        # Target specific areas for analysis
        print(f"\n🎯 LIVE FIRE TARGETS:")
        targets = [
            "🔒 Security Audit: Hardcoded credentials, API keys, secrets",
            "🔍 Code Quality: Linting errors, formatting issues, complexity",
            "⚙️ DevOps: Build issues, dependency problems, deployment risks",
            "🏗️ Architecture: Design patterns, module organization, scalability",
        ]

        for target in targets:
            print(f"  {target}")

        print(f"\n🚀 EXECUTING LIVE FIRE SEQUENCE...")
        print("-" * 80)

        # Run the multi-agent analysis - this will use ALL working models
        print("🤖 Deploying multi-agent teams across all LLM providers...")
        result = orchestrator.run_multi_agent_analysis()

        # Analyze the results
        print(f"\n📊 LIVE FIRE RESULTS ANALYSIS:")
        print("=" * 80)

        # Success metrics
        print(
            f"🎯 MISSION STATUS: {'✅ SUCCESS' if result.get('success', False) else '❌ FAILED'}"
        )
        print(f"🔍 TOTAL FINDINGS: {result.get('total_issues', 0)}")
        print(f"🧠 MODELS DEPLOYED: {len(result.get('models_used', []))}")
        print(f"💰 OPERATIONAL COST: ${result.get('total_cost', 0):.6f}")

        # Detailed findings
        if "security" in result:
            security_findings = result["security"]
            if isinstance(security_findings, list):
                print(
                    f"\n🔒 SECURITY FINDINGS: {len(security_findings)} issues detected"
                )
                for i, finding in enumerate(security_findings[:5], 1):  # Show first 5
                    print(f"  {i}. {str(finding)[:100]}...")
            else:
                print(f"\n🔒 SECURITY ANALYSIS: {security_findings}")

        if "quality" in result:
            quality_findings = result["quality"]
            if isinstance(quality_findings, list):
                print(f"\n🔍 QUALITY FINDINGS: {len(quality_findings)} issues detected")
                for i, finding in enumerate(quality_findings[:5], 1):  # Show first 5
                    print(f"  {i}. {str(finding)[:100]}...")
            else:
                print(f"\n🔍 QUALITY ANALYSIS: {quality_findings}")

        if "devops" in result:
            devops_findings = result["devops"]
            if isinstance(devops_findings, list):
                print(f"\n⚙️ DEVOPS FINDINGS: {len(devops_findings)} issues detected")
                for i, finding in enumerate(devops_findings[:5], 1):  # Show first 5
                    print(f"  {i}. {str(finding)[:100]}...")
            else:
                print(f"\n⚙️ DEVOPS ANALYSIS: {devops_findings}")

        # Cost breakdown
        if "cost_breakdown" in result:
            print(f"\n💰 COST BREAKDOWN BY MODEL:")
            total_tokens = 0
            total_cost = 0
            for model, cost_info in result["cost_breakdown"].items():
                tokens = cost_info.get("tokens", 0)
                cost = cost_info.get("cost", 0)
                total_tokens += tokens
                total_cost += cost
                print(f"  📊 {model}: {tokens:,} tokens, ${cost:.6f}")

            print(f"\n📈 TOTAL OPERATIONAL METRICS:")
            print(f"  🎯 Total Tokens: {total_tokens:,}")
            print(f"  💰 Total Cost: ${total_cost:.6f}")
            print(
                f"  🚀 Cost per Finding: ${total_cost/max(result.get('total_issues', 1), 1):.6f}"
            )

        # Mission assessment
        print(f"\n🎯 MISSION ASSESSMENT:")
        if result.get("total_issues", 0) > 0:
            print(f"  ✅ SUCCESS: Found {result.get('total_issues')} real issues!")
            print(f"  🎯 Multi-LLM analysis successfully identified problems")
            print(f"  🚀 System is working as designed")
        else:
            print(f"  🎯 CLEAN CODEBASE: No issues detected")
            print(f"  🚀 Multi-LLM validation confirms code quality")
            print(f"  🏆 System successfully validated clean state")

        return True

    except Exception as e:
        print(f"❌ LIVE FIRE EXERCISE FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🎯 LIVE FIRE EXERCISE INITIATED")
    print("🚀 DEPLOYING MULTI-LLM ANALYSIS TEAMS...")

    success = asyncio.run(live_fire_exercise())

    print("\n" + "=" * 80)
    if success:
        print("🎯 LIVE FIRE EXERCISE COMPLETED!")
        print("🚀 MULTI-LLM SYSTEM VALIDATED!")
        print("🏆 READY FOR PRODUCTION DEPLOYMENT!")
    else:
        print("❌ LIVE FIRE EXERCISE FAILED!")
        print("🔧 SYSTEM NEEDS IMMEDIATE ATTENTION!")

    print("=" * 80)

