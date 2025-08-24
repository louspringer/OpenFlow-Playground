#!/usr/bin/env python3
"""
🔧 Multi-Agent Environment Setup Script

This script uses the new op-api-manager to properly set up the environment
for multi-agent systems, replacing the old 1Password patching approach.
"""

import os
import sys
from pathlib import Path

# Add op-api-manager to path
op_api_manager_path = Path(__file__).parent.parent.parent / "op-api-manager" / "src"
if op_api_manager_path.exists():
    sys.path.insert(0, str(op_api_manager_path))

try:
    from op_api_manager.core import OnePasswordAPIKeyManager
    from op_api_manager.models import CacheConfig

    print("✅ Successfully imported op-api-manager")
except ImportError as e:
    print(f"❌ Failed to import op-api-manager: {e}")
    print("  🔧 Please ensure op-api-manager is properly installed")
    sys.exit(1)


def setup_multi_agent_environment():
    """Set up the environment for multi-agent systems using op-api-manager."""
    try:
        print("🚀 Setting up multi-agent environment...")
        print()

        # Initialize API key manager
        print("🔑 Initializing API key manager...")
        cache_config = CacheConfig()
        api_manager = OnePasswordAPIKeyManager(cache_config)

        if not api_manager:
            print("❌ Failed to initialize API key manager")
            return False

        # Check if we have working credentials in cache
        print("📦 Checking for working credentials in cache...")
        working_credentials = api_manager.get_working_credentials_all(force_test=False)

        if working_credentials:
            total_apis = sum(len(apis) for apis in working_credentials.values())
            print(f"  ✅ Found {total_apis} working APIs in cache")

            # Display what we found
            for provider, api_list in working_credentials.items():
                print(f"    🔑 {provider.upper()}: {len(api_list)} working APIs")

        else:
            print("  🔄 No working credentials in cache, testing APIs...")

            # Test API endpoints to discover working ones
            print("  🧪 Testing API endpoints...")
            test_results = api_manager.test_api_endpoints(verbose=True)

            if test_results:
                total_apis = sum(len(apis) for apis in test_results.values())
                print(f"  ✅ API testing completed, found {total_apis} working APIs")

                # Display what we found
                for provider, api_list in test_results.items():
                    print(f"    🔑 {provider.upper()}: {len(api_list)} working APIs")
            else:
                print("  ⚠️ No working APIs found during testing")

        # Set environment variables for multi-agent systems
        print()
        print("🔧 Setting environment variables for multi-agent systems...")
        api_manager.set_environment_variables()

        # Verify environment variables are set
        print("  🔍 Verifying environment variables...")
        required_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "HUGGINGFACE_API_KEY",
            "COHERE_API_KEY",
            "AI21_API_KEY",
            "OPENROUTER_API_KEY",
        ]

        set_vars = []
        missing_vars = []

        for var in required_vars:
            if os.getenv(var):
                set_vars.append(var)
            else:
                missing_vars.append(var)

        print(f"  ✅ Set: {len(set_vars)} environment variables")
        if set_vars:
            for var in set_vars:
                value = os.getenv(var)
                preview = value[:8] + "..." if len(value) > 8 else value
                print(f"    🔑 {var}: {preview}")

        if missing_vars:
            print(f"  ⚠️ Missing: {len(missing_vars)} environment variables")
            for var in missing_vars:
                print(f"    ❌ {var}")

        # Update .env file if we have working credentials
        print()
        print("💾 Updating .env file...")
        if working_credentials or test_results:
            credentials_to_use = (
                working_credentials if working_credentials else test_results
            )
            success = api_manager.update_env_file(credentials_to_use, backup=True)

            if success:
                print("  ✅ .env file updated successfully")

                # Verify the .env file
                if api_manager.verify_env_file():
                    print("  ✅ .env file verification passed")
                else:
                    print("  ⚠️ .env file verification failed")
            else:
                print("  ❌ Failed to update .env file")
        else:
            print("  ⚠️ No working credentials to persist")

        # Display final status
        print()
        print("🎯 Multi-Agent Environment Setup Complete!")
        print()

        if set_vars:
            print("✅ Ready for multi-agent operations with:")
            for var in set_vars:
                print(f"  🔑 {var}")
        else:
            print("⚠️ No API keys configured - multi-agent operations may fail")
            print("  💡 Run 'op-api-manager discover --force' to find API keys")
            print("  💡 Run 'op-api-manager test --force' to test discovered keys")

        return True

    except Exception as e:
        print(f"❌ Error setting up multi-agent environment: {e}")
        return False


def check_multi_agent_readiness():
    """Check if the multi-agent system is ready to run."""
    try:
        print("🔍 Checking multi-agent system readiness...")
        print()

        # Check environment variables
        print("🔑 Environment Variables:")
        required_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
        ]

        ready = True
        for var in required_vars:
            if os.getenv(var):
                value = os.getenv(var)
                preview = value[:8] + "..." if len(value) > 8 else value
                print(f"  ✅ {var}: {preview}")
            else:
                print(f"  ❌ {var}: Not set")
                ready = False

        print()

        # Check op-api-manager availability
        print("🔧 op-api-manager Status:")
        try:
            from op_api_manager.core import OnePasswordAPIKeyManager

            print("  ✅ op-api-manager available")
        except ImportError:
            print("  ❌ op-api-manager not available")
            ready = False

        # Check cache status
        print("📦 Cache Status:")
        try:
            cache_config = CacheConfig()
            api_manager = OnePasswordAPIKeyManager(cache_config)
            cache_status = api_manager.get_cache_status()
            print(f"  ✅ Cache available: {cache_status.get('cache_file', 'Unknown')}")
        except Exception as e:
            print(f"  ❌ Cache error: {e}")
            ready = False

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

    parser = argparse.ArgumentParser(description="Multi-Agent Environment Setup")
    parser.add_argument(
        "--check", action="store_true", help="Check readiness without setup"
    )
    parser.add_argument(
        "--setup", action="store_true", help="Force setup even if already configured"
    )

    args = parser.parse_args()

    if args.check:
        return 0 if check_multi_agent_readiness() else 1
    if args.setup:
        return 0 if setup_multi_agent_environment() else 1
    # Default: check first, then setup if needed
    if not check_multi_agent_readiness():
        print()
        print("🔧 Setting up environment...")
        return 0 if setup_multi_agent_environment() else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
