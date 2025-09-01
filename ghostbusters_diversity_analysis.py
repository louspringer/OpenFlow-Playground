#!/usr/bin/env python3
"""
🎯 ASK THE DIVERSITY SYSTEM: What do you think about the Ghostbusters problem?

This script uses your proven diversity hypothesis system to analyze the Ghostbusters issue
from multiple AI perspectives.
"""

import sys
from pathlib import Path

from multi_dimensional_smoke_test import MultiDimensionalSmokeTest

# Add the multi_agent_testing module to path
sys.path.append(str(Path(__file__).parent / "src" / "multi_agent_testing"))


def create_ghostbusters_scenario() -> dict:
    """Create a scenario about the Ghostbusters problem for diversity analysis"""

    scenario: dict = {
        "ghostbusters_analysis": {
            "context": """
PROBLEM: The Ghostbusters system was supposed to battle hallucinations and support the 'diversity is the only free lunch' principle, but it became bloated and ineffective.

WHAT HAPPENED:
- Original intent: Multi-agent delusion detection to battle AI hallucinations
- Reality: 6 "expert agents" that just do file existence checks (ls pyproject.toml)
- Token cost: 3K-5K tokens per run for regex pattern matching
- Value: Zero - could be done with shell commands
- Size: 5,482 lines of async complexity for simple operations

WHAT WAS REMOVED:
- src/ghostbusters/ (5,482 lines of bloat)
- 6 agents doing file existence checks
- Complex LangGraph orchestration for simple tasks
- Async wrappers around basic file operations

WHAT WAS KEPT:
- src/multi_agent_testing/ (working diversity system)
- multi_dimensional_smoke_test.py (26KB, proven working)
- test_diversity_hypothesis.py (19KB, proven working)
- Real multi-agent analysis with 1.00 diversity score

QUESTION: What do you think about this problem and solution? What blind spots might we have missed?
            """,
            "expected_diversity_score": 0.9,
            "expected_findings": 15,
        }
    }

    return scenario


def analyze_ghostbusters_with_diversity() -> list:
    """Use the diversity system to analyze the Ghostbusters problem"""

    print("🎯 ASKING THE DIVERSITY SYSTEM: What do you think about Ghostbusters?")
    print("=" * 80)

    # Create the diversity system
    diversity_system = MultiDimensionalSmokeTest()

    # Add our custom scenario
    diversity_system.scenarios.update(create_ghostbusters_scenario())

    # Define the analysis question
    analysis_question = """
Analyze the Ghostbusters problem and solution from your unique perspective:

1. What blind spots might we have missed in our analysis?
2. What risks or unintended consequences could arise from our cleanup?
3. What alternative approaches should we consider?
4. How well does this solution align with the 'diversity is the only free lunch' principle?
5. What would you do differently?

Focus on your specific role perspective and provide unique insights.
"""

    print(f"📊 Available models: {list(diversity_system.models.keys())}")
    print(f"🎭 Available roles: {list(diversity_system.roles.keys())}")
    print(f"📝 Available formats: {list(diversity_system.response_formats.keys())}")
    print()

    # Test with a few key models and roles
    test_configs = [
        {
            "model": "gpt4",
            "role": "skeptical_partner",
            "temperature": 0.7,
            "format": "json_structured",
        },
        {
            "model": "claude",
            "role": "risk_assessor",
            "temperature": 0.7,
            "format": "risk_matrix",
        },
        {
            "model": "perplexity",
            "role": "quality_gatekeeper",
            "temperature": 0.7,
            "format": "bullet_points",
        },
    ]

    results = []

    for i, config in enumerate(test_configs, 1):
        print(f"🔍 Running analysis {i}/3: {config['model']} as {config['role']}")
        print("-" * 50)

        try:
            # Create the prompt for this role
            role_prompt = f"{diversity_system.roles[config['role']]}\n\n{analysis_question}"

            # Call the LLM
            response = diversity_system.call_llm(
                model_name=config["model"],
                prompt=role_prompt,
                temperature=config["temperature"],
            )

            if "error" in response:
                print(f"❌ Error with {config['model']}: {response['error']}")
                continue

            # Extract the content
            if "choices" in response and response["choices"]:
                content = response["choices"][0]["message"]["content"]
                print(f"✅ {config['model']} ({config['role']}) response:")
                print(content)
                print()

                results.append(
                    {
                        "model": config["model"],
                        "role": config["role"],
                        "response": content,
                        "format": config["format"],
                    }
                )
            else:
                print(f"⚠️ Unexpected response format from {config['model']}")
                print(response)

        except Exception as e:
            print(f"❌ Error analyzing with {config['model']}: {e}")
            continue

    # Summary
    print("=" * 80)
    print(f"📊 DIVERSITY ANALYSIS COMPLETE: {len(results)} successful analyses")
    print()

    if results:
        print("🎯 KEY INSIGHTS FROM DIVERSITY SYSTEM:")
        for result in results:
            print(f"  • {result['model']} ({result['role']}): {result['format']} analysis")
        print()
        print("💡 This demonstrates the power of diverse AI perspectives!")
    else:
        print("❌ No successful analyses - check API keys and connectivity")

    return results


if __name__ == "__main__":
    print("🚀 Ghostbusters Diversity Analysis")
    print("Using your proven diversity hypothesis system to analyze the problem")
    print()

    # Check if we have the required modules
    try:
        from multi_dimensional_smoke_test import MultiDimensionalSmokeTest

        print("✅ Diversity system imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the right directory and the diversity system is available")
        sys.exit(1)

    # Run the analysis
    results = analyze_ghostbusters_with_diversity()

    print("🎯 Analysis complete! The diversity system has spoken.")
