#!/usr/bin/env python3
"""
Test a specific API key instead of all 70 keys.
"""

import time

from op_api_manager.core import CacheConfig, OnePasswordAPIKeyManager


def test_specific_openai_key():
    """Test just the specific OpenAI API key."""
    print("🎯 Testing specific OpenAI API key...")

    # Initialize manager
    manager = OnePasswordAPIKeyManager(CacheConfig())

    # The specific OpenAI key ID from 1Password
    openai_key_id = "67kb4niwnxxyibbi46koc2z34e"

    print(f"🔑 Testing OpenAI key: {openai_key_id}")

    start_time = time.time()

    # Get the credential
    print("  🔐 Retrieving credential...")
    credential = manager._get_credential_value(openai_key_id)

    if credential:
        print(f"  ✅ Got credential: {credential[:8]}...")

        # Test the API
        print("  🧪 Testing OpenAI API...")
        test_result = manager._test_openai_credential(credential)

        if test_result["working"]:
            print("  🎉 OpenAI API is working!")
            print(f"  📊 Available models: {test_result['models']}")

            # Set environment variable
            print("  🔑 Setting environment variable...")
            manager.set_provider_environment_variable("openai")

        else:
            print(f"  ❌ OpenAI API failed: {test_result['error']}")
    else:
        print("  ❌ No credential found")

    total_time = time.time() - start_time
    print(f"⏱️  Total time: {total_time:.2f} seconds")


if __name__ == "__main__":
    test_specific_openai_key()
