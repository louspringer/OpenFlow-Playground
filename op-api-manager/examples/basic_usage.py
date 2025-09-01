#!/usr/bin/env python3
"""
Basic usage example for OP API Manager.

This script demonstrates how to use the OP API Manager
to discover and manage API keys from 1Password.
"""

import sys
from pathlib import Path

# Add the src directory to the path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from op_api_manager import CacheConfig, OnePasswordAPIKeyManager


def main():
    """Main example function."""
    print("🔍 OP API Manager - Basic Usage Example")
    print("=" * 50)

    # Create a custom cache configuration
    cache_config = CacheConfig(
        enabled=True,
        cache_file="example_cache.json",
        max_age_hours=12,
        auto_refresh=False,
    )

    # Initialize the manager
    print("📦 Initializing OP API Manager...")
    manager = OnePasswordAPIKeyManager(cache_config)

    try:
        # Discover API keys
        print("🔍 Discovering API keys from 1Password...")
        result = manager.discover_api_keys()

        # Display results
        print("\n✅ Discovery completed!")
        print(f"📊 Total items scanned: {result.total_items}")
        print(f"🔑 API keys found: {len(result.api_keys)}")
        print(f"🔗 Credential pairs: {len(result.credential_pairs)}")

        # Show provider breakdown
        if result.providers:
            print("\n🌐 Provider breakdown:")
            for provider, count in result.providers.items():
                print(f"  • {provider.value}: {count}")

        # Show status breakdown
        if result.status_summary:
            print("\n📈 Status breakdown:")
            for status, count in result.status_summary.items():
                print(f"  • {status.value}: {count}")

        # Show some credential pairs
        if result.credential_pairs:
            print("\n🔗 Credential pairs:")
            for i, pair in enumerate(result.credential_pairs[:3]):  # Show first 3
                print(f"  {i + 1}. {pair.pair_type}: {pair.primary.title}")
                if pair.secondary:
                    print(f"     Secondary: {pair.secondary.title}")
                print(f"     Description: {pair.description}")

        # Check cache status
        print("\n💾 Cache status:")
        cache_status = manager.get_cache_status()
        for key, value in cache_status.items():
            print(f"  • {key}: {value}")

        # Example: Get keys for specific provider
        print("\n🎯 Example: Getting OpenAI keys...")
        openai_keys = manager.get_api_keys_by_provider("openai")
        print(f"  Found {len(openai_keys)} OpenAI keys")

        for key in openai_keys:
            print(f"    • {key.title} (ID: {key.id[:8]}...)")

    except Exception as e:
        print(f"❌ Error during discovery: {e}")
        print("\n💡 Make sure you have:")
        print("  1. 1Password CLI installed and authenticated")
        print("  2. Access to your 1Password vault")
        print("  3. Some API keys stored in 1Password")
        return 1

    print("\n🎉 Example completed successfully!")
    print("💡 Try running 'op-api-manager --help' for more options")

    return 0


if __name__ == "__main__":
    exit(main())
