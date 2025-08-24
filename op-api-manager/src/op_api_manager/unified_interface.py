"""
Unified Interface for OP API Manager.

This module provides a clean, consistent interface for all CRUD operations
on API credentials, using the StatusManager for atomic operations.
"""

from typing import Any, Optional

from .models import DiscoveryResult
from .status_manager import CredentialStatus, StatusManager


class UnifiedOPInterface:
    """
    Unified interface for OP API Manager operations.

    This class provides clean CRUD operations with proper error handling
    and atomic operations through the StatusManager.
    """

    def __init__(self, status_manager: StatusManager):
        """
        Initialize the unified interface.

        Args:
            status_manager: The status manager instance
        """
        self.status_manager = status_manager

    # CREATE Operations
    def discover_credentials(self, force_refresh: bool = False) -> DiscoveryResult:
        """
        Discover all potential API credentials.

        Args:
            force_refresh: Force refresh even if cache is valid

        Returns:
            DiscoveryResult containing all discovered items
        """
        # This would integrate with the existing discovery logic
        # For now, return a placeholder
        return DiscoveryResult(
            total_items=0, api_keys=[], credential_pairs=[], discovery_timestamp=""
        )

    # READ Operations
    def get_working_credentials(
        self, force_test: bool = False
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Get all working credentials organized by provider.

        Args:
            force_test: If True, test all APIs fresh

        Returns:
            Dictionary mapping provider names to working credentials
        """
        if force_test:
            # This would trigger the testing workflow
            # For now, return cached results
            pass

        return self.status_manager.get_working_credentials()

    def get_credentials_by_provider(self, provider: str) -> list[dict[str, Any]]:
        """
        Get credentials for a specific provider.

        Args:
            provider: The provider name

        Returns:
            List of credentials for the provider
        """
        working_creds = self.status_manager.get_working_credentials()
        return working_creds.get(provider.lower(), [])

    def get_archived_credentials(self) -> list[dict[str, Any]]:
        """
        Get all archived credentials.

        Returns:
            List of archived credentials
        """
        return self.status_manager.get_archived_credentials()

    def get_credential_status(self, item_id: str) -> Optional[str]:
        """
        Get the current status of a specific credential.

        Args:
            item_id: The 1Password item ID

        Returns:
            The current status or None if not found
        """
        return self.status_manager.get_credential_status(item_id)

    # UPDATE Operations
    def update_credential_status(
        self, item_id: str, status: str, reason: str = None
    ) -> bool:
        """
        Update the status of a credential.

        Args:
            item_id: The 1Password item ID
            status: The new status to set
            reason: Optional reason for the status change

        Returns:
            True if successful, False otherwise
        """
        return self.status_manager.update_credential_status(item_id, status, reason)

    def mark_credential_working(
        self, item_id: str, reason: str = "API test passed"
    ) -> bool:
        """
        Mark a credential as working.

        Args:
            item_id: The 1Password item ID
            reason: Reason for marking as working

        Returns:
            True if successful, False otherwise
        """
        return self.status_manager.update_credential_status(
            item_id, CredentialStatus.WORKING.value, reason
        )

    def mark_credential_error(
        self, item_id: str, reason: str = "API test failed"
    ) -> bool:
        """
        Mark a credential as having an error.

        Args:
            item_id: The 1Password item ID
            reason: Reason for the error

        Returns:
            True if successful, False otherwise
        """
        return self.status_manager.update_credential_status(
            item_id, CredentialStatus.ERROR.value, reason
        )

    # DELETE Operations
    def archive_credential(
        self, item_id: str, reason: str = "Not suitable for API usage"
    ) -> bool:
        """
        Archive a credential in both cache and 1Password.

        Args:
            item_id: The 1Password item ID
            reason: Reason for archiving

        Returns:
            True if successful, False otherwise
        """
        return self.status_manager.archive_credential(item_id, reason)

    # Utility Operations
    def get_status_summary(self) -> dict[str, Any]:
        """
        Get a summary of all credential statuses.

        Returns:
            Dictionary with status counts and summary information
        """
        return self.status_manager.get_status_summary()

    def refresh_cache(self) -> bool:
        """
        Refresh the cache from disk.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Force reload of cache
            self.status_manager._cache = None
            self.status_manager.load_cache()
            return True
        except Exception as e:
            print(f"❌ Failed to refresh cache: {e}")
            return False

    def validate_cache_integrity(self) -> dict[str, Any]:
        """
        Validate the integrity of the cache.

        Returns:
            Dictionary with validation results
        """
        cache = self.status_manager.load_cache()
        validation_results = {
            "cache_loaded": cache is not None,
            "total_keys": len(cache.get("api_keys", [])),
            "status_distribution": {},
            "orphaned_entries": [],
            "validation_passed": True,
        }

        # Check status distribution
        for key in cache.get("api_keys", []):
            status = key.get("status", "unknown")
            if status not in validation_results["status_distribution"]:
                validation_results["status_distribution"][status] = 0
            validation_results["status_distribution"][status] += 1

            # Check for required fields
            required_fields = ["id", "title", "status"]
            missing_fields = [field for field in required_fields if not key.get(field)]
            if missing_fields:
                validation_results["orphaned_entries"].append(
                    {"id": key.get("id"), "missing_fields": missing_fields}
                )
                validation_results["validation_passed"] = False

        return validation_results
