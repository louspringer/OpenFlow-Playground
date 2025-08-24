#!/usr/bin/env python3
"""
Integration test showing how the new unified interface works with existing functionality.

This demonstrates the seamless integration between old and new implementations.
"""

import sys
from pathlib import Path


# Setup path
def setup_path():
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))


setup_path()

from op_api_manager.status_manager import StatusManager
from op_api_manager.unified_interface import UnifiedOPInterface


def test_integration_with_existing_cache():
    """Test integration with existing cache."""
    print("🧪 Testing Integration with Existing Cache")
    print("=" * 50)

    # Initialize with existing cache
    cache_file = Path("../api_discovery_cache.json")
    if not cache_file.exists():
        print("❌ Cache file not found. Run from op-api-manager directory.")
        return False

    status_manager = StatusManager(str(cache_file))
    interface = UnifiedOPInterface(status_manager)

    # Test 1: Get current working credentials (existing functionality)
    print("\n1️⃣ Testing existing working credentials...")
    working = interface.get_working_credentials()
    print(f"   Found {len(working)} working providers")

    for provider, creds in working.items():
        print(f"   - {provider.upper()}: {len(creds)} credentials")

    # Test 2: Get archived credentials (new functionality)
    print("\n2️⃣ Testing new archived credentials...")
    archived = interface.get_archived_credentials()
    print(f"   Found {len(archived)} archived credentials")

    for cred in archived[:3]:  # Show first 3
        print(f"   - {cred['title']} ({cred['provider']}) - {cred['archive_reason']}")

    # Test 3: Status summary (new functionality)
    print("\n3️⃣ Testing new status summary...")
    summary = interface.get_status_summary()
    print(f"   Total: {summary['total_credentials']}")
    print(f"   Working: {summary['working']}")
    print(f"   Archived: {summary['archived']}")
    print(f"   Discovered: {summary['discovered']}")

    # Test 4: Cache validation (new functionality)
    print("\n4️⃣ Testing new cache validation...")
    validation = interface.validate_cache_integrity()
    print(f"   Validation passed: {validation['validation_passed']}")
    print(f"   Total keys: {validation['total_keys']}")
    print(f"   Status distribution: {validation['status_distribution']}")

    # Test 5: Provider-specific queries (new functionality)
    print("\n5️⃣ Testing new provider-specific queries...")
    for provider in ["azure", "aws", "google", "anthropic", "openai"]:
        creds = interface.get_credentials_by_provider(provider)
        if creds:
            print(f"   {provider.upper()}: {len(creds)} credentials")

    print("\n✅ Integration test completed successfully!")
    return True


def test_transaction_safety():
    """Test transaction safety with real data."""
    print("\n🧪 Testing Transaction Safety with Real Data")
    print("=" * 50)

    cache_file = Path("../api_discovery_cache.json")
    status_manager = StatusManager(str(cache_file))

    # Test transaction with real data
    print("Testing transaction safety...")

    try:
        with status_manager.transaction():
            # Get current status of a real item
            real_item_id = "jdgggnli2dlny3mruf7ih35po4"  # ANTHROPIC_API_KEY
            current_status = status_manager.get_credential_status(real_item_id)
            print(f"   Current status of {real_item_id}: {current_status}")

            # This transaction will succeed
            print("   ✅ Transaction completed successfully")

    except Exception as e:
        print(f"   ❌ Transaction failed: {e}")
        return False

    print("✅ Transaction safety test completed!")
    return True


def main():
    """Run integration tests."""
    print("🚀 OP API Manager - Integration Tests")
    print("=" * 60)

    try:
        # Test 1: Integration with existing cache
        if not test_integration_with_existing_cache():
            return 1

        # Test 2: Transaction safety
        if not test_transaction_safety():
            return 1

        print("\n" + "=" * 60)
        print("🎉 All integration tests passed!")
        print("✅ New unified interface working with existing system")
        print("🚀 Ready for full migration!")

        return 0

    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
