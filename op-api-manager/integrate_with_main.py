#!/usr/bin/env python3
"""
Integration script for OP API Manager with main project.

This script provides a bridge between the standalone OP API Manager package
and the main multi-agent system, allowing seamless integration.
"""

import sys
from pathlib import Path
from typing import Any, Optional

# Add the op-api-manager src to the path
current_dir = Path(__file__).parent
op_manager_src = current_dir / "src"
sys.path.insert(0, str(op_manager_src))

try:
    from op_api_manager import CacheConfig, OnePasswordAPIKeyManager
    from op_api_manager.models import APIKeyStatus, ProviderType

    OP_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  OP API Manager not available: {e}")
    OP_MANAGER_AVAILABLE = False


class OPManagerIntegration:
    """
    Integration bridge between OP API Manager and main project.

    This class provides a clean interface for the main project to use
    the OP API Manager functionality without tight coupling.
    """

    def __init__(self, cache_file: Optional[str] = None):
        """
        Initialize the integration.

        Args:
            cache_file: Optional custom cache file location
        """
        if not OP_MANAGER_AVAILABLE:
            raise RuntimeError("OP API Manager package not available")

        # Configure cache
        cache_config = CacheConfig()
        if cache_file:
            cache_config.cache_file = cache_file

        # Initialize manager
        self.manager = OnePasswordAPIKeyManager(cache_config)

    def get_working_api_keys(self) -> list[dict[str, Any]]:
        """
        Get all working API keys for use in the main project.

        Returns:
            List of working API key dictionaries
        """
        try:
            result = self.manager.discover_api_keys()
            working_keys = [
                key for key in result.api_keys if key.status == APIKeyStatus.WORKING
            ]

            # Convert to simple dictionaries for main project
            return [
                {
                    "id": key.id,
                    "title": key.title,
                    "provider": key.provider.value,
                    "category": key.category,
                    "guid": str(key.guid),
                    "url": key.url,
                    "notes": key.notes,
                    "tags": key.tags,
                }
                for key in working_keys
            ]
        except Exception as e:
            print(f"❌ Error getting working API keys: {e}")
            return []

    def get_api_keys_by_provider(self, provider: str) -> list[dict[str, Any]]:
        """
        Get API keys for a specific provider.

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')

        Returns:
            List of API key dictionaries for the provider
        """
        try:
            provider_enum = ProviderType(provider)
            keys = self.manager.get_api_keys_by_provider(provider_enum)

            return [
                {
                    "id": key.id,
                    "title": key.title,
                    "provider": key.provider.value,
                    "category": key.category,
                    "guid": str(key.guid),
                    "url": key.url,
                    "notes": key.notes,
                    "tags": key.tags,
                }
                for key in keys
            ]
        except Exception as e:
            print(f"❌ Error getting API keys for provider {provider}: {e}")
            return []

    def get_credential_pairs(self) -> list[dict[str, Any]]:
        """
        Get credential pairs for use in the main project.

        Returns:
            List of credential pair dictionaries
        """
        try:
            result = self.manager.discover_api_keys()

            return [
                {
                    "pair_type": pair.pair_type,
                    "description": pair.description,
                    "is_complete": pair.is_complete,
                    "primary": {
                        "id": pair.primary.id,
                        "title": pair.primary.title,
                        "provider": pair.primary.provider.value,
                        "guid": str(pair.primary.guid),
                    },
                    "secondary": (
                        {
                            "id": pair.secondary.id,
                            "title": pair.secondary.title,
                            "provider": pair.secondary.provider.value,
                            "guid": str(pair.secondary.guid),
                        }
                        if pair.secondary
                        else None
                    ),
                }
                for pair in result.credential_pairs
            ]
        except Exception as e:
            print(f"❌ Error getting credential pairs: {e}")
            return []

    def get_discovery_summary(self) -> dict[str, Any]:
        """
        Get a summary of the current discovery state.

        Returns:
            Dictionary with discovery summary information
        """
        try:
            result = self.manager.discover_api_keys()
            cache_status = self.manager.get_cache_status()

            return {
                "total_items": result.total_items,
                "api_keys_found": len(result.api_keys),
                "credential_pairs": len(result.credential_pairs),
                "providers": {k.value: v for k, v in result.providers.items()},
                "status_summary": {
                    k.value: v for k, v in result.status_summary.items()
                },
                "discovery_timestamp": result.discovery_timestamp,
                "cache_status": cache_status,
            }
        except Exception as e:
            print(f"❌ Error getting discovery summary: {e}")
            return {}

    def refresh_discovery(self) -> bool:
        """
        Force refresh the discovery cache.

        Returns:
            True if refresh was successful
        """
        try:
            self.manager.refresh_cache()
            return True
        except Exception as e:
            print(f"❌ Error refreshing discovery: {e}")
            return False


def main():
    """Main function for testing the integration."""
    print("🔗 OP API Manager Integration Test")
    print("==================================")

    if not OP_MANAGER_AVAILABLE:
        print("❌ OP API Manager not available")
        print("💡 Make sure the package is installed: make install")
        return 1

    try:
        # Initialize integration
        integration = OPManagerIntegration()

        # Test discovery summary
        print("\n📊 Discovery Summary:")
        summary = integration.get_discovery_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")

        # Test working API keys
        print("\n🔑 Working API Keys:")
        working_keys = integration.get_working_api_keys()
        if working_keys:
            for key in working_keys:
                print(f"  • {key['provider']}: {key['title']} (ID: {key['id'][:8]}...)")
        else:
            print("  No working API keys found")

        # Test provider-specific keys
        print("\n🌐 Provider Breakdown:")
        for provider in ["openai", "anthropic", "google", "aws"]:
            keys = integration.get_api_keys_by_provider(provider)
            if keys:
                print(f"  {provider}: {len(keys)} keys")
                for key in keys[:2]:  # Show first 2
                    print(f"    • {key['title']}")
            else:
                print(f"  {provider}: 0 keys")

        # Test credential pairs
        print("\n🔗 Credential Pairs:")
        pairs = integration.get_credential_pairs()
        if pairs:
            for pair in pairs:
                print(f"  • {pair['pair_type']}: {pair['description']}")
                print(f"    Primary: {pair['primary']['title']}")
                if pair["secondary"]:
                    print(f"    Secondary: {pair['secondary']['title']}")
        else:
            print("  No credential pairs found")

        print("\n✅ Integration test completed successfully!")
        return 0

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
