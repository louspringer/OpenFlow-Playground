#!/usr/bin/env python3
"""
Test individual API keys to find better candidates.
"""

import sys

from op_api_manager.core import CacheConfig, OnePasswordAPIKeyManager


def test_individual_key(item_id: str):
    """Test a specific API key."""
    print(f"🧪 Testing API key: {item_id}")

    # Initialize manager
    manager = OnePasswordAPIKeyManager(CacheConfig())

    # Get the credential
    print("  🔐 Retrieving credential...")
    credential = manager._get_credential_value(item_id)

    if credential:
        print(f"  ✅ Got credential: {credential[:8]}...")

        # Try to determine what type of credential this might be
        if credential.startswith("sk-"):
            print("  🎯 Looks like OpenAI API key")
        elif credential.startswith("sk-ant-"):
            print("  🎯 Looks like Anthropic API key")
        elif len(credential) == 20 and credential.isupper():
            print("  🎯 Looks like AWS Access Key ID")
        elif len(credential) == 40:
            print("  🎯 Looks like AWS Secret Access Key or GitHub token")
        elif credential.startswith("ey"):
            print("  🎯 Looks like JWT token")
        elif len(credential) == 32:
            print("  🎯 Looks like Azure API key (32 chars)")
        elif len(credential) == 64:
            print("  🎯 Looks like Azure API key (64 chars)")
        else:
            print(f"  ❓ Unknown format, length: {len(credential)}")

    else:
        print("  ❌ No credential found")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_individual_key.py <item_id>")
        sys.exit(1)

    test_individual_key(sys.argv[1])
