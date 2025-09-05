#!/usr/bin/env python3
"""
🔧 Simple Multi-Agent Environment Setup

This script sets up the environment for multi-agent systems using existing
environment variables and .env files, without requiring 1Password authentication.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment_variables():
    """Load environment variables from .env file."""
    try:
        # Load from ~/.env
        env_file = Path.home() / ".env"
        if env_file.exists():
            print(f"📁 Loading environment from: {env_file}")
            load_dotenv(env_file)
            return True
        print("⚠️ No .env file found at ~/.env")
        return False
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return False


def check_api_keys():
    """Check which API keys are available."""
    print("🔍 Checking available API keys...")
    print()

    # Check for various API key patterns in the environment
    api_keys = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
        "Google/Gemini": "GOOGLE_API_KEY",
        "AWS": "AWS_ACCESS_KEY_ID",
        "HuggingFace": "HUGGINGFACE_API_KEY",
        "Cohere": "COHERE_API_KEY",
        "AI21": "AI21_API_KEY",
        "OpenRouter": "OPENROUTER_API_KEY",
        "Azure": "AZURE_API_KEY",
        "Unknown/Generic": "UNKNOWN_API_KEY",
    }

    available_keys = []
    missing_keys = []

    for service, env_var in api_keys.items():
        value = os.getenv(env_var)
        if value and value != "YOUR_API_KEY" and not value.startswith("YOUR_") and value.strip():
            available_keys.append(service)
            preview = value[:8] + "..." if len(value) > 8 else value
            print(f"  ✅ {service}: {preview}")
        else:
            missing_keys.append(service)
            print(f"  ❌ {service}: Not configured")

    print()
    print(f"📊 Summary: {len(available_keys)}/{len(api_keys)} services configured")

    return available_keys, missing_keys


def setup_multi_agent_environment():
    """Set up the environment for multi-agent systems."""
    try:
        print("🚀 Setting up multi-agent environment...")
        print()

        # Load environment variables
        if not load_environment_variables():
            print("⚠️ Continuing with system environment variables only")

        # Check available API keys
        available_keys, missing_keys = check_api_keys()

        if not available_keys:
            print("❌ No API keys found!")
            print("💡 Please configure API keys in your environment or .env file")
            return False

        # Set up working models based on available keys
        working_models = []

        if "OpenAI" in available_keys:
            working_models.extend(["gpt4_vision", "gpt5", "gpt4o", "gpt4o_mini", "gpt3_5_turbo"])
            print("🔑 OpenAI models available")

        if "Anthropic" in available_keys:
            working_models.extend(["claude_3_5_sonnet", "claude_3_haiku", "claude_3_opus"])
            print("🔑 Anthropic models available")

        if "Google/Gemini" in available_keys:
            working_models.extend(["gemini_pro", "gemini_flash", "gemini_pro_vision"])
            print("🔑 Google/Gemini models available")

        if "AWS" in available_keys:
            working_models.extend(["claude_bedrock", "titan_express", "llama2_bedrock"])
            print("🔑 AWS Bedrock models available")

        if "HuggingFace" in available_keys:
            working_models.append("huggingface")
            print("🔑 HuggingFace models available")

        if "Cohere" in available_keys:
            working_models.append("cohere")
            print("🔑 Cohere models available")

        if "AI21" in available_keys:
            working_models.append("ai21")
            print("🔑 AI21 models available")

        if "OpenRouter" in available_keys:
            working_models.append("openrouter")
            print("🔑 OpenRouter models available")

        if "Azure" in available_keys:
            working_models.extend(["gpt4_vision", "gpt5", "gpt4o", "gpt4o_mini", "gpt3_5_turbo"])
            print("🔑 Azure OpenAI models available")

        if "Unknown/Generic" in available_keys:
            working_models.extend(["generic_api", "custom_llm"])
            print("🔑 Generic/Unknown API models available")

        print()
        print("🎯 Multi-Agent Environment Setup Complete!")
        print()
        print(f"✅ Ready for multi-agent operations with {len(working_models)} models:")
        for model in working_models:
            print(f"  🤖 {model}")

        print()
        print("💡 Available services:")
        for service in available_keys:
            print(f"  🔑 {service}")

        if missing_keys:
            print()
            print("⚠️ Missing services (optional):")
            for service in missing_keys:
                print(f"  ❌ {service}")

        return True

    except Exception as e:
        print(f"❌ Error setting up multi-agent environment: {e}")
        return False


def test_multi_agent_readiness():
    """Test if the multi-agent system is ready to run."""
    try:
        print("🧪 Testing multi-agent system readiness...")
        print()

        # Load environment variables first
        load_environment_variables()

        # Check environment variables
        print("🔑 Environment Variables:")
        required_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "UNKNOWN_API_KEY",  # Add this since we have it
        ]

        ready = False
        real_keys = 0
        for var in required_vars:
            if os.getenv(var):
                value = os.getenv(var)
                preview = value[:8] + "..." if len(value) > 8 else value
                if value and value != "YOUR_API_KEY" and not value.startswith("YOUR_") and value.strip():
                    print(f"  ✅ {var}: {preview} (REAL)")
                    real_keys += 1
                    ready = True
                else:
                    print(f"  ⚠️ {var}: {preview} (PLACEHOLDER)")
            else:
                print(f"  ❌ {var}: Not set")

        print(f"\n📊 Found {real_keys} real API key(s)")

        print()

        if ready:
            print("🎉 Multi-agent system is ready!")
            return True
        print("⚠️ Multi-agent system needs setup")
        print("  💡 Run this script to set up the environment")
        return False

    except Exception as e:
        print(f"❌ Error checking readiness: {e}")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Simple Multi-Agent Environment Setup")
    parser.add_argument("--check", action="store_true", help="Check readiness without setup")
    parser.add_argument("--setup", action="store_true", help="Force setup even if already configured")

    args = parser.parse_args()

    if args.check:
        return 0 if test_multi_agent_readiness() else 1
    if args.setup:
        return 0 if setup_multi_agent_environment() else 1
    # Default: check first, then setup if needed
    if not test_multi_agent_readiness():
        print()
        print("🔧 Setting up environment...")
        return 0 if setup_multi_agent_environment() else 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
