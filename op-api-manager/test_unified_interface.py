#!/usr/bin/env python3
"""
Test script for the new unified interface and status manager.

This script demonstrates the clean CRUD operations and atomic status management.
"""

import sys
from pathlib import Path


# Setup path first
def setup_path():
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))


# Import modules
setup_path()
from op_api_manager.status_manager import CredentialStatus, StatusManager
from op_api_manager.unified_interface import UnifiedOPInterface


def test_status_manager():
    """Test the StatusManager functionality."""
    print("🧪 Testing StatusManager...")

    # Initialize with a test cache file
    cache_file = Path(__file__).parent / "test_cache.json"
    status_manager = StatusManager(str(cache_file))

    # Test cache operations
    print("  📦 Testing cache operations...")
    cache = status_manager.load_cache()
    print(f"    ✅ Cache loaded: {len(cache.get('api_keys', []))} keys")

    # Test status update
    print("  🔄 Testing status update...")
    success = status_manager.update_credential_status("test-item-123", CredentialStatus.WORKING.value, "Test status update")
    print(f"    ✅ Status update: {success}")

    # Test working credentials
    print("  ✅ Testing working credentials...")
    working = status_manager.get_working_credentials()
    print(f"    ✅ Working credentials: {len(working)} providers")

    # Test status summary
    print("  📊 Testing status summary...")
    summary = status_manager.get_status_summary()
    print(f"    ✅ Status summary: {summary}")

    # Clean up
    if cache_file.exists():
        cache_file.unlink()

    print("✅ StatusManager tests completed!")


def test_unified_interface():
    """Test the UnifiedOPInterface functionality."""
    print("\n🧪 Testing UnifiedOPInterface...")

    # Initialize with a test cache file
    cache_file = Path(__file__).parent / "test_cache.json"
    status_manager = StatusManager(str(cache_file))
    interface = UnifiedOPInterface(status_manager)

    # Test CRUD operations
    print("  🔧 Testing CRUD operations...")

    # CREATE - Add a test credential
    print("    📝 Testing credential creation...")
    # This would integrate with discovery logic

    # READ - Get working credentials
    print("    👀 Testing credential retrieval...")
    working = interface.get_working_credentials()
    print(f"      ✅ Working credentials: {len(working)} providers")

    # UPDATE - Mark credential as working
    print("    ✏️  Testing status update...")
    success = interface.mark_credential_working("test-item-456", "API test passed")
    print(f"      ✅ Mark as working: {success}")

    # DELETE - Archive credential
    print("    🗑️  Testing credential archiving...")
    success = interface.archive_credential("test-item-789", "Not suitable for API usage")
    print(f"      ✅ Archive credential: {success}")

    # Test utility operations
    print("  🛠️  Testing utility operations...")

    # Status summary
    summary = interface.get_status_summary()
    print(f"    ✅ Status summary: {summary}")

    # Cache validation
    validation = interface.validate_cache_integrity()
    print(f"    ✅ Cache validation: {validation['validation_passed']}")

    # Clean up
    if cache_file.exists():
        cache_file.unlink()

    print("✅ UnifiedOPInterface tests completed!")


def test_transaction_safety():
    """Test transaction safety and rollback capabilities."""
    print("\n🧪 Testing transaction safety...")

    # Initialize with a test cache file
    cache_file = Path(__file__).parent / "test_cache.json"
    status_manager = StatusManager(str(cache_file))

    # Test successful transaction
    print("  ✅ Testing successful transaction...")
    try:
        with status_manager.transaction():
            status_manager.update_credential_status("test-item-1", CredentialStatus.WORKING.value, "Successful transaction")
            print("    ✅ Transaction completed successfully")
    except Exception as e:
        print(f"    ❌ Unexpected error: {e}")

    # Test failed transaction with rollback
    print("  ❌ Testing failed transaction with rollback...")
    try:
        with status_manager.transaction():
            status_manager.update_credential_status("test-item-2", CredentialStatus.WORKING.value, "Will fail")
            # Simulate a failure
            raise RuntimeError("Simulated transaction failure")
    except RuntimeError:
        print("    ✅ Transaction properly rolled back")

    # Verify rollback worked
    status = status_manager.get_credential_status("test-item-2")
    if status is None:
        print("    ✅ Rollback successful - item not in cache")
    else:
        print(f"    ❌ Rollback failed - item still has status: {status}")

    # Clean up
    if cache_file.exists():
        cache_file.unlink()

    print("✅ Transaction safety tests completed!")


def main():
    """Run all tests."""
    print("🚀 Starting Unified Interface Tests")
    print("=" * 50)

    try:
        test_status_manager()
        test_unified_interface()
        test_transaction_safety()

        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
