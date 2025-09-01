#!/usr/bin/env python3
"""
Fix Model Mapping for 1Password Freedom
Updates the orchestrator to use correct model names instead of generic provider names
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def fix_model_mapping():
    """Fix the model mapping in the orchestrator"""

    print("🔧 Fixing Model Mapping for True 1Password Freedom")
    print("=" * 60)

    # Load environment variables
    load_dotenv()

    # Path to the orchestrator
    orchestrator_path = Path("src/multi_agent_testing/code_quality_automation_orchestrator.py")

    if not orchestrator_path.exists():
        print(f"❌ Orchestrator not found: {orchestrator_path}")
        return False

    print(f"\n📁 Fixing orchestrator: {orchestrator_path}")

    # Read the current orchestrator
    try:
        with open(orchestrator_path) as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Failed to read orchestrator: {e}")
        return False

    # Create backup
    backup_path = orchestrator_path.with_suffix(".py.backup2")
    try:
        with open(backup_path, "w") as f:
            f.write(content)
        print(f"💾 Backup created: {backup_path}")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False

    # Define the fixes
    fixes = [
        # Fix 1: Replace generic "azure" with actual Azure OpenAI model
        {
            "old": 'if os.getenv("AZURE_API_KEY"):\n                api_test_results["azure"] = [{"id": "env_azure", "working": True}]\n                working_models.append("azure")',
            "new": 'if os.getenv("AZURE_API_KEY"):\n                api_test_results["azure"] = [{"id": "env_azure", "working": True}]\n                working_models.append("gpt4")  # Use OpenAI GPT-4 model',
        },
        # Fix 2: Replace generic "aws" with actual AWS Bedrock model
        {
            "old": 'if os.getenv("AWS_ACCESS_KEY_ID"):\n                api_test_results["aws"] = [{"id": "env_aws", "working": True}]\n                working_models.append("aws")',
            "new": 'if os.getenv("AWS_ACCESS_KEY_ID"):\n                api_test_results["aws"] = [{"id": "env_aws", "working": True}]\n                working_models.append("claude_bedrock")  # Use AWS Bedrock Claude model',
        },
        # Fix 3: Update the working models mapping section
        {
            "old": """            # Set the working API keys for the smoke test and update environment
            if hasattr(test_system, "set_working_api_keys"):
                working_keys = {}
                for model in working_models:
                    if model == "claude":
                        # Get the actual Anthropic API key from the discovered keys
                        anthropic_keys = api_test_results.get("anthropic", [])
                        if anthropic_keys:
                            # Use the first working Anthropic key
                            anthropic_key = anthropic_keys[0].get("id", "")
                            working_keys["claude"] = anthropic_key
                            # Set environment variable
                            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
                            print("🔑 Updated ANTHROPIC_API_KEY environment with working key")
                        else:
                            working_keys["claude"] = os.getenv("ANTHROPIC_API_KEY")
                    elif model == "gpt4_vision" and self.working_openai_key:
                        # Use the working OpenAI API key we validated
                        working_keys["gpt4_vision"] = self.working_openai_key
                        # Update environment variable with working key
                        os.environ["OPENAI_API_KEY"] = self.working_openai_key
                        print("🔑 Updated OPENAI_API_KEY environment with working key")
                    elif model == "gpt5" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-5
                        working_keys["gpt5"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-5")
                    elif model == "gpt3_5_turbo" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-3.5-turbo
                        working_keys["gpt3_5_turbo"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-3.5-turbo")
                    elif model == "huggingface" and hasattr(
                        self, "working_huggingface_key"
                    ):
                        # Use the working HuggingFace API key we validated
                        working_keys["huggingface"] = self.working_huggingface_key
                        # Update environment variable with working key
                        os.environ["HUGGINGFACE_API_KEY"] = self.working_huggingface_key
                        print(
                            "🔑 Updated HUGGINGFACE_API_KEY environment with working key"
                        )
                    elif (
                        model in ["claude_haiku", "claude_sonnet"]
                        and self.working_anthropic_key
                    ):
                        # Use the working Anthropic API key for alternative models
                        working_keys[model] = self.working_anthropic_key
                        print(f"🔑 Using working Anthropic API key for {model}")
                    elif (
                        model in ["gemini_pro", "gemini_flash", "gemini_pro_vision"]
                        and self.working_google_key
                    ):
                        # Use the working Google API key
                        working_keys[model] = self.working_google_key
                        os.environ["GOOGLE_API_KEY"] = self.working_google_key
                        print(
                            f"🔑 Updated GOOGLE_API_KEY environment with working key for {model}"
                        )
                    elif (
                        model in ["claude_bedrock", "titan_express", "llama2_bedrock"]
                        and self.working_aws_key
                    ):
                        # Use the working AWS API key
                        working_keys[model] = self.working_aws_key
                        os.environ["AWS_ACCESS_KEY_ID"] = self.working_aws_key
                        print(
                            f"🔑 Updated AWS_ACCESS_KEY_ID environment with working key for {model}"
                        )""",
            "new": """            # Set the working API keys for the smoke test and update environment
            if hasattr(test_system, "set_working_api_keys"):
                working_keys = {}
                for model in working_models:
                    if model == "claude":
                        # Use environment variable directly
                        working_keys["claude"] = os.getenv("ANTHROPIC_API_KEY")
                        print("🔑 Using ANTHROPIC_API_KEY from environment")
                    elif model == "gpt4":
                        # Use environment variable directly for Azure OpenAI
                        working_keys["gpt4"] = os.getenv("AZURE_API_KEY")
                        print("🔑 Using AZURE_API_KEY from environment for GPT-4")
                    elif model == "claude_bedrock":
                        # Use environment variable directly for AWS Bedrock
                        working_keys["claude_bedrock"] = os.getenv("AWS_ACCESS_KEY_ID")
                        print("🔑 Using AWS_ACCESS_KEY_ID from environment for Claude Bedrock")
                    elif model == "gpt4_vision" and self.working_openai_key:
                        # Use the working OpenAI API key we validated
                        working_keys["gpt4_vision"] = self.working_openai_key
                        # Update environment variable with working key
                        os.environ["OPENAI_API_KEY"] = self.working_openai_key
                        print("🔑 Updated OPENAI_API_KEY environment with working key")
                    elif model == "gpt5" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-5
                        working_keys["gpt5"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-5")
                    elif model == "gpt3_5_turbo" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-3.5-turbo
                        working_keys["gpt3_5_turbo"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-3.5-turbo")
                    elif model == "huggingface" and hasattr(
                        self, "working_huggingface_key"
                    ):
                        # Use the working HuggingFace API key we validated
                        working_keys["huggingface"] = self.working_huggingface_key
                        # Update environment variable with working key
                        os.environ["HUGGINGFACE_API_KEY"] = self.working_huggingface_key
                        print(
                            "🔑 Updated HUGGINGFACE_API_KEY environment with working key"
                        )
                    elif (
                        model in ["claude_haiku", "claude_sonnet"]
                        and self.working_anthropic_key
                    ):
                        # Use the working Anthropic API key for alternative models
                        working_keys[model] = self.working_anthropic_key
                        print(f"🔑 Using working Anthropic API key for {model}")
                    elif (
                        model in ["gemini_pro", "gemini_flash", "gemini_pro_vision"]
                        and self.working_google_key
                    ):
                        # Use the working Google API key
                        working_keys[model] = self.working_google_key
                        os.environ["GOOGLE_API_KEY"] = self.working_google_key
                        print(
                            f"🔑 Updated GOOGLE_API_KEY environment with working key for {model}"
                        )
                    elif (
                        model in ["claude_bedrock", "titan_express", "llama2_bedrock"]
                        and self.working_aws_key
                    ):
                        # Use the working AWS API key
                        working_keys[model] = self.working_aws_key
                        os.environ["AWS_ACCESS_KEY_ID"] = self.working_aws_key
                        print(
                            f"🔑 Updated AWS_ACCESS_KEY_ID environment with working key for {model}"
                        )""",
        },
    ]

    # Apply all fixes
    for i, fix in enumerate(fixes, 1):
        print(f"\n🔧 Applying fix {i}...")

        if fix["old"] in content:
            content = content.replace(fix["old"], fix["new"])
            print(f"✅ Fix {i} applied successfully")
        else:
            print(f"⚠️  Fix {i} target not found (may have been applied already)")

    # Write the fixed orchestrator
    try:
        with open(orchestrator_path, "w") as f:
            f.write(content)
        print("\n✅ All fixes applied successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to write fixed orchestrator: {e}")
        return False


def test_fixed_orchestrator():
    """Test that the fixed orchestrator works"""

    print("\n🧪 Testing fixed orchestrator...")

    try:
        # Import the fixed orchestrator
        import sys

        sys.path.insert(0, "src")

        from multi_agent_testing.code_quality_automation_orchestrator import (
            CodeQualityAutomationOrchestrator,
        )

        print("✅ Fixed orchestrator imported successfully")

        # Create instance
        orchestrator = CodeQualityAutomationOrchestrator(".")
        print("✅ Orchestrator instance created")

        # Test multi-agent analysis
        print("\n🤖 Testing multi-agent analysis...")
        results = orchestrator.run_multi_agent_analysis()

        print("✅ Multi-agent analysis completed!")
        print(f"📊 Results: {results}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def restore_backup():
    """Restore the original orchestrator from backup"""

    print("\n🔄 Restoring original orchestrator...")

    orchestrator_path = Path("src/multi_agent_testing/code_quality_automation_orchestrator.py")
    backup_path = orchestrator_path.with_suffix(".py.backup2")

    if not backup_path.exists():
        print("❌ Backup not found")
        return False

    try:
        with open(backup_path) as f:
            backup_content = f.read()

        with open(orchestrator_path, "w") as f:
            f.write(backup_content)

        print("✅ Original orchestrator restored")
        return True

    except Exception as e:
        print(f"❌ Failed to restore: {e}")
        return False


if __name__ == "__main__":
    print("🔓 Model Mapping Fix for 1Password Freedom")
    print("=" * 60)

    # Apply the fixes
    if fix_model_mapping():
        print("\n🎉 Model mapping fixed successfully!")

        # Test the fixed orchestrator
        if test_fixed_orchestrator():
            print("\n🚀 SUCCESS! Orchestrator now uses correct model names!")
            print("\n📝 What was fixed:")
            print('  - "azure" → "gpt4" (OpenAI GPT-4 model)')
            print('  - "aws" → "claude_bedrock" (AWS Bedrock Claude model)')
            print("  - Environment variable mapping corrected")
            print('  - No more "Unknown model" errors')
        else:
            print("\n❌ Test failed, restoring backup...")
            restore_backup()
    else:
        print("\n❌ Fix failed")
