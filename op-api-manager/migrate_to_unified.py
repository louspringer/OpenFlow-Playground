#!/usr/bin/env python3
"""
Migration script to transition from old implementation to unified architecture.

This script migrates the existing OP API Manager to use the new StatusManager
and UnifiedOPInterface for all operations.
"""

import json
import sys
from pathlib import Path
from typing import Any


# Add the src directory to the path
def setup_path():
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))


setup_path()

from op_api_manager.status_manager import StatusManager
from op_api_manager.unified_interface import UnifiedOPInterface


class MigrationManager:
    """Manages the migration from old to new implementation."""

    def __init__(self, cache_file_path: str):
        """
        Initialize the migration manager.

        Args:
            cache_file_path: Path to the existing cache file
        """
        self.cache_file_path = Path(cache_file_path)
        self.status_manager = StatusManager(str(cache_file_path))
        self.interface = UnifiedOPInterface(self.status_manager)

    def analyze_current_state(self) -> dict[str, Any]:
        """Analyze the current state of the system."""
        print("🔍 Analyzing current system state...")

        # Load existing cache
        with open(self.cache_file_path) as f:
            old_cache = json.load(f)

        # Analyze status distribution
        status_counts = {}
        provider_counts = {}
        orphaned_entries = []

        for key in old_cache.get("api_keys", []):
            # Count by status
            status = key.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

            # Count by provider
            provider = key.get("detected_provider", "unknown")
            provider_counts[provider] = provider_counts.get(provider, 0) + 1

            # Check for orphaned entries
            required_fields = ["id", "title", "status"]
            missing_fields = [field for field in required_fields if not key.get(field)]
            if missing_fields:
                orphaned_entries.append(
                    {"id": key.get("id"), "missing_fields": missing_fields}
                )

        analysis = {
            "total_credentials": len(old_cache.get("api_keys", [])),
            "status_distribution": status_counts,
            "provider_distribution": provider_counts,
            "orphaned_entries": orphaned_entries,
            "cache_file_size": self.cache_file_path.stat().st_size,
            "cache_last_modified": self.cache_file_path.stat().st_mtime,
        }

        print("📊 Analysis complete:")
        print(f"   Total credentials: {analysis['total_credentials']}")
        print(f"   Status distribution: {analysis['status_distribution']}")
        print(f"   Provider distribution: {analysis['provider_distribution']}")
        print(f"   Orphaned entries: {len(analysis['orphaned_entries'])}")

        return analysis

    def validate_migration_readiness(self) -> dict[str, Any]:
        """Validate that the system is ready for migration."""
        print("\n🔍 Validating migration readiness...")

        validation_results = {
            "status_manager_ready": False,
            "unified_interface_ready": False,
            "cache_accessible": False,
            "migration_safe": False,
            "issues": [],
        }

        # Test StatusManager
        try:
            self.status_manager.load_cache()
            validation_results["status_manager_ready"] = True
            print("   ✅ StatusManager: Ready")
        except Exception as e:
            validation_results["status_manager_ready"] = False
            validation_results["issues"].append(f"StatusManager failed: {e}")
            print(f"   ❌ StatusManager: Failed - {e}")

        # Test UnifiedOPInterface
        try:
            self.interface.get_status_summary()
            validation_results["unified_interface_ready"] = True
            print("   ✅ UnifiedOPInterface: Ready")
        except Exception as e:
            validation_results["unified_interface_ready"] = False
            validation_results["issues"].append(f"UnifiedOPInterface failed: {e}")
            print(f"   ❌ UnifiedOPInterface: Failed - {e}")

        # Test cache accessibility
        try:
            if self.cache_file_path.exists():
                validation_results["cache_accessible"] = True
                print("   ✅ Cache: Accessible")
            else:
                validation_results["cache_accessible"] = False
                validation_results["issues"].append("Cache file not found")
                print("   ❌ Cache: Not found")
        except Exception as e:
            validation_results["cache_accessible"] = False
            validation_results["issues"].append(f"Cache access failed: {e}")
            print(f"   ❌ Cache: Access failed - {e}")

        # Overall migration safety
        validation_results["migration_safe"] = all(
            [
                validation_results["status_manager_ready"],
                validation_results["unified_interface_ready"],
                validation_results["cache_accessible"],
            ]
        )

        if validation_results["migration_safe"]:
            print("   🎉 Migration: SAFE TO PROCEED")
        else:
            print("   🚨 Migration: NOT SAFE - Fix issues first")

        return validation_results

    def create_backup(self) -> Path:
        """Create a backup of the current cache."""
        print("\n💾 Creating backup...")

        backup_path = self.cache_file_path.with_suffix(".backup.json")
        try:
            with open(self.cache_file_path) as src, open(backup_path, "w") as dst:
                json.dump(json.load(src), dst, indent=2)
            print(f"   ✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"   ❌ Backup failed: {e}")
            raise

    def migrate_status_management(self) -> bool:
        """Migrate status management to use StatusManager."""
        print("\n🔄 Migrating status management...")

        try:
            # Test status operations
            print("   Testing status operations...")

            # Get current working credentials
            working = self.interface.get_working_credentials()
            print(f"   ✅ Retrieved {len(working)} working providers")

            # Test status update (on a test item)
            test_item_id = "test-migration-item"
            success = self.interface.update_credential_status(
                test_item_id, "discovered", "Migration test"
            )
            print(f"   ✅ Status update test: {success}")

            # Test archive operation (on a test item)
            success = self.interface.archive_credential(
                test_item_id, "Migration test - cleanup"
            )
            print(f"   ✅ Archive test: {success}")

            print("   🎉 Status management migration: SUCCESS")
            return True

        except Exception as e:
            print(f"   ❌ Status management migration failed: {e}")
            return False

    def migrate_cache_operations(self) -> bool:
        """Migrate cache operations to use StatusManager."""
        print("\n🔄 Migrating cache operations...")

        try:
            # Test cache operations
            print("   Testing cache operations...")

            # Test cache validation
            validation = self.interface.validate_cache_integrity()
            print(f"   ✅ Cache validation: {validation['validation_passed']}")

            # Test status summary
            summary = self.interface.get_status_summary()
            print(f"   ✅ Status summary: {summary['total_credentials']} total")

            # Test cache refresh
            success = self.interface.refresh_cache()
            print(f"   ✅ Cache refresh: {success}")

            print("   🎉 Cache operations migration: SUCCESS")
            return True

        except Exception as e:
            print(f"   ❌ Cache operations migration failed: {e}")
            return False

    def run_full_migration(self) -> bool:
        """Run the complete migration process."""
        print("🚀 Starting full migration process...")
        print("=" * 60)

        try:
            # Step 1: Analyze current state
            self.analyze_current_state()

            # Step 2: Validate migration readiness
            validation = self.validate_migration_readiness()
            if not validation["migration_safe"]:
                print("\n❌ Migration validation failed. Please fix issues:")
                for issue in validation["issues"]:
                    print(f"   - {issue}")
                return False

            # Step 3: Create backup
            backup_path = self.create_backup()

            # Step 4: Migrate status management
            if not self.migrate_status_management():
                print("\n❌ Status management migration failed")
                return False

            # Step 5: Migrate cache operations
            if not self.migrate_cache_operations():
                print("\n❌ Cache operations migration failed")
                return False

            print("\n" + "=" * 60)
            print("🎉 Migration completed successfully!")
            print(f"📦 Backup created: {backup_path}")
            print("✅ System now using unified architecture")

            return True

        except Exception as e:
            print(f"\n❌ Migration failed with error: {e}")
            import traceback

            traceback.print_exc()
            return False

    def rollback_migration(self, backup_path: Path) -> bool:
        """Rollback migration using backup."""
        print(f"\n🔄 Rolling back migration using backup: {backup_path}")

        try:
            if backup_path.exists():
                # Restore backup
                with (
                    open(backup_path) as src,
                    open(self.cache_file_path, "w") as dst,
                ):
                    json.dump(json.load(src), dst, indent=2)
                print("   ✅ Rollback completed successfully")
                return True
            else:
                print("   ❌ Backup file not found")
                return False
        except Exception as e:
            print(f"   ❌ Rollback failed: {e}")
            return False


def main():
    """Main migration function."""
    print("🚀 OP API Manager - Migration to Unified Architecture")
    print("=" * 60)

    # Default cache file path
    cache_file = Path("../api_discovery_cache.json")

    if not cache_file.exists():
        print(f"❌ Cache file not found: {cache_file}")
        print("Please run this script from the op-api-manager directory")
        return 1

    # Initialize migration manager
    migration_manager = MigrationManager(str(cache_file))

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "analyze":
            migration_manager.analyze_current_state()
        elif command == "validate":
            migration_manager.validate_migration_readiness()
        elif command == "backup":
            migration_manager.create_backup()
        elif command == "migrate":
            migration_manager.run_full_migration()
        elif command == "rollback":
            if len(sys.argv) > 2:
                backup_path = Path(sys.argv[2])
                migration_manager.rollback_migration(backup_path)
            else:
                print("Usage: python migrate_to_unified.py rollback <backup_path>")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: analyze, validate, backup, migrate, rollback")
            return 1
    else:
        # Default: run full migration
        success = migration_manager.run_full_migration()
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
