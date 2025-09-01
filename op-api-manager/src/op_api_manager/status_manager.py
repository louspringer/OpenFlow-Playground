"""
Unified Status Management for OP API Manager.

This module provides atomic status management operations for API credentials,
ensuring consistency between cache and 1Password states.
"""

import json
import subprocess
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class CredentialStatus(Enum):
    """Credential status enumeration."""

    DISCOVERED = "discovered"
    WORKING = "working"
    ARCHIVED = "archived"
    ERROR = "error"


class StatusUpdate:
    """Represents a status update operation."""

    def __init__(
        self,
        item_id: str,
        old_status: str,
        new_status: str,
        reason: str = None,
        timestamp: datetime = None,
    ):
        self.item_id = item_id
        self.old_status = old_status
        self.new_status = new_status
        self.reason = reason
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "item_id": self.item_id,
            "old_status": self.old_status,
            "new_status": self.new_status,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
        }


class StatusManager:
    """
    Manages credential status operations atomically.

    This class ensures that status changes are applied consistently
    across both the local cache and 1Password, with proper validation
    and rollback capabilities.
    """

    def __init__(self, cache_file_path: str):
        """
        Initialize the status manager.

        Args:
            cache_file_path: Path to the cache file
        """
        self.cache_file_path = Path(cache_file_path)
        self._cache: Optional[dict[str, Any]] = None
        self._status_history: list[StatusUpdate] = []

    def load_cache(self) -> dict[str, Any]:
        """Load the current cache."""
        if self._cache is None:
            if self.cache_file_path.exists():
                with open(self.cache_file_path) as f:
                    self._cache = json.load(f)
            else:
                self._cache = {"api_keys": [], "status_history": []}
        return self._cache

    def save_cache(self) -> bool:
        """Save the current cache to disk."""
        try:
            if self._cache:
                # Add status history to cache
                if "status_history" not in self._cache:
                    self._cache["status_history"] = []

                # Add new status updates
                for update in self._status_history:
                    self._cache["status_history"].append(update.to_dict())

                # Clear processed history
                self._status_history.clear()

                # Save to disk
                self.cache_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.cache_file_path, "w") as f:
                    json.dump(self._cache, f, indent=2, default=str)
                return True
        except Exception as e:
            print(f"❌ Failed to save cache: {e}")
            return False
        return False

    def get_credential_status(self, item_id: str) -> Optional[str]:
        """Get the current status of a credential."""
        cache = self.load_cache()
        for key in cache.get("api_keys", []):
            if key.get("id") == item_id:
                return key.get("status")
        return None

    def update_credential_status(self, item_id: str, new_status: str, reason: str = None) -> bool:
        """
        Update the status of a credential.

        Args:
            item_id: The 1Password item ID
            new_status: The new status to set
            reason: Optional reason for the status change

        Returns:
            True if successful, False otherwise
        """
        cache = self.load_cache()
        old_status = None

        # Find and update the credential
        for key in cache.get("api_keys", []):
            if key.get("id") == item_id:
                old_status = key.get("status")
                key["status"] = new_status
                key["status_updated_at"] = datetime.now().isoformat()
                if reason:
                    key["status_reason"] = reason
                break

        if old_status is None:
            print(f"❌ Credential {item_id} not found in cache")
            return False

        # Record the status update
        status_update = StatusUpdate(item_id=item_id, old_status=old_status, new_status=new_status, reason=reason)
        self._status_history.append(status_update)

        print(f"✅ Status updated: {item_id} {old_status} → {new_status}")
        if reason:
            print(f"   Reason: {reason}")

        return True

    def archive_credential(self, item_id: str, reason: str = "Not suitable for API usage") -> bool:
        """
        Archive a credential in both cache and 1Password.

        Args:
            item_id: The 1Password item ID
            reason: Reason for archiving

        Returns:
            True if successful, False otherwise
        """
        try:
            # Update cache status first
            if not self.update_credential_status(item_id, CredentialStatus.ARCHIVED.value, reason):
                return False

            # Archive in 1Password
            print("🔄 Moving item to 1Password Archive...")
            subprocess.run(
                ["op", "item", "delete", item_id, "--archive"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )

            print(f"✅ Successfully archived in 1Password: {item_id}")

            # Save cache
            return self.save_cache()

        except subprocess.TimeoutExpired:
            print("⏰ 1Password archive operation timed out")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to archive in 1Password: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error archiving in 1Password: {e}")
            return False

    def get_working_credentials(self) -> dict[str, Any]:
        """Get all working credentials from cache."""
        cache = self.load_cache()
        working_creds = {}

        for key in cache.get("api_keys", []):
            if key.get("status") == CredentialStatus.WORKING.value:
                provider = key.get("detected_provider", "unknown")
                if provider not in working_creds:
                    working_creds[provider] = []

                working_creds[provider].append(
                    {
                        "id": key.get("id"),
                        "title": key.get("title"),
                        "status": key.get("status"),
                        "provider": provider,
                    }
                )

        return working_creds

    def get_archived_credentials(self) -> list[dict[str, Any]]:
        """Get all archived credentials from cache."""
        cache = self.load_cache()
        archived = []

        for key in cache.get("api_keys", []):
            if key.get("status") == CredentialStatus.ARCHIVED.value:
                archived.append(
                    {
                        "id": key.get("id"),
                        "title": key.get("title"),
                        "status": key.get("status"),
                        "provider": key.get("detected_provider", "unknown"),
                        "archived_at": key.get("status_updated_at"),
                        "archive_reason": key.get("status_reason"),
                    }
                )

        return archived

    @contextmanager
    def transaction(self):
        """
        Context manager for atomic operations.

        Provides rollback capability if operations fail.
        """
        # Backup current cache
        cache_backup = self._cache.copy() if self._cache else None

        try:
            yield self
            # If we get here, operation succeeded
            self.save_cache()
        except Exception as e:
            # Rollback on failure
            print(f"❌ Operation failed, rolling back: {e}")
            self._cache = cache_backup
            self._status_history.clear()
            raise

    def get_status_summary(self) -> dict[str, Any]:
        """Get a summary of all credential statuses."""
        cache = self.load_cache()
        summary = {
            "total_credentials": 0,
            "discovered": 0,
            "working": 0,
            "archived": 0,
            "error": 0,
        }

        for key in cache.get("api_keys", []):
            summary["total_credentials"] += 1
            status = key.get("status", "discovered")
            if status in summary:
                summary[status] += 1

        return summary
