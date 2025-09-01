#!/usr/bin/env python3
"""
Simple Live Fire Test for Multi-Agent System

This script tests the multi-agent system using only available API keys.
It provides command line options to specify API keys directly.
"""

import argparse
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.multi_agent_testing.multi_dimensional_smoke_test import (
    MultiDimensionalSmokeTest,
)


def main():
    """Main function for simple live fire test"""
    parser = argparse.ArgumentParser(description="Simple Live Fire Multi-Agent Test")
    parser.add_argument("--env-file", help="Path to .env file (default: ~/.env)")
    parser.add_argument("--anthropic-key", help="Anthropic API key (overrides .env)")
    parser.add_argument("--openai-key", help="OpenAI API key (overrides .env)")
    parser.add_argument("--google-key", help="Google API key (overrides .env)")
    parser.add_argument("--openrouter-key", help="OpenRouter API key (overrides .env)")
    parser.add_argument("--aws-access-key", help="AWS Access Key ID (overrides .env)")
    parser.add_argument("--aws-secret-key", help="AWS Secret Access Key (overrides .env)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--test-model",
        default="claude",
        choices=["claude", "claude_haiku", "claude_sonnet", "gpt4", "gpt35"],
        help="Model to test (default: claude)",
    )

    args = parser.parse_args()

    print("🔥 SIMPLE LIVE FIRE MULTI-AGENT TEST")
    print("=" * 50)

    # Set environment variables from command line if provided
    if args.anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = args.anthropic_key
        print("🔑 Set ANTHROPIC_API_KEY from command line")
    if args.openai_key:
        os.environ["OPENAI_API_KEY"] = args.openai_key
        print("🔑 Set OPENAI_API_KEY from command line")
    if args.google_key:
        os.environ["GOOGLE_API_KEY"] = args.google_key
        print("🔑 Set GOOGLE_API_KEY from command line")
    if args.openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_key
        print("🔑 Set OPENROUTER_API_KEY from command line")
    if args.aws_access_key:
        os.environ["AWS_ACCESS_KEY_ID"] = args.aws_access_key
        print("🔑 Set AWS_ACCESS_KEY_ID from command line")
    if args.aws_secret_key:
        os.environ["AWS_SECRET_ACCESS_KEY"] = args.aws_secret_key
        print("🔑 Set AWS_SECRET_ACCESS_KEY from command line")

    # Initialize test system
    print("🔧 Initializing Multi-Dimensional Smoke Test...")
    test = MultiDimensionalSmokeTest(env_file=args.env_file)

    if args.verbose:
        print("🔍 Available environment variables:")
        for key, value in os.environ.items():
            if "API_KEY" in key or "AWS_" in key:
                preview = value[:8] + "..." if len(value) > 8 else value
                print(f"  {key}: {preview}")
        print()

    # Check if we have the required API key for the test model
    required_env = None
    if args.test_model.startswith("claude"):
        required_env = "ANTHROPIC_API_KEY"
    elif args.test_model.startswith("gpt"):
        # Prefer OpenRouter if available, fallback to OpenAI
        if os.getenv("OPENROUTER_API_KEY"):
            required_env = "OPENROUTER_API_KEY"
        else:
            required_env = "OPENAI_API_KEY"
    elif args.test_model.startswith("gemini"):
        required_env = "GOOGLE_API_KEY"
    elif args.test_model.startswith("bedrock"):
        required_env = "AWS_ACCESS_KEY_ID"

    if required_env and not os.getenv(required_env):
        print(f"❌ ERROR: {required_env} environment variable is required for {args.test_model}")
        print(f"💡 Use --{required_env.lower().replace('_', '-')} to specify the API key")
        return 1

    print(f"🧪 Testing model: {args.test_model}")
    print(f"🔑 Using API key from: {required_env}")

    # Create a simple test configuration
    test_config = {
        "name": "simple_live_fire",
        "temperature": 0.3,
        "role": "skeptical_partner",
        "model": args.test_model,
        "prompt_structure": "direct_questions",
        "response_format": "json_structured",
    }

    try:
        print("🚀 Running live fire test...")
        result = test.run_test(test_config, "healthcare_cdc_pr")

        print("\n🎯 TEST RESULTS:")
        print(f"   Model: {args.test_model}")
        print(f"   Status: {'✅ SUCCESS' if result.get('real_llm_result') else '❌ FAILED'}")

        if result.get("real_llm_result"):
            print(f"   Response received: {len(str(result['real_llm_result']))} characters")
            if args.verbose:
                print(f"   Full response: {result['real_llm_result']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")

        print("\n🔥 LIVE FIRE TEST COMPLETE!")
        return 0

    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
