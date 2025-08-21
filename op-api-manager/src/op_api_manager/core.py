"""
Core functionality for OP API Manager.

This module contains the main OnePasswordAPIKeyManager class that handles
API key discovery, organization, and management.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    APIKeyItem,
    APIKeyStatus,
    CacheConfig,
    CredentialPair,
    DiscoveryResult,
    ProviderType,
)


class OnePasswordAPIKeyManager:
    """
    Intelligent API key discovery and management for 1Password.

    This class provides functionality to discover API keys stored in 1Password,
    organize them into logical groups, assign unique GUIDs, and manage caching
    for efficient operations.
    """

    def __init__(self, cache_config: Optional[CacheConfig] = None):
        """
        Initialize the OP API Key Manager.

        Args:
            cache_config: Configuration for caching operations
        """
        self.cache_config = cache_config or CacheConfig()
        self._cache: Optional[Dict[str, Any]] = None
        self._last_discovery: Optional[datetime] = None

    def discover_api_keys(self, force_refresh: bool = False) -> DiscoveryResult:
        """
        Discover all potential API keys from 1Password.

        Args:
            force_refresh: Force refresh even if cache is valid

        Returns:
            DiscoveryResult containing all discovered items
        """
        # Check cache first
        if not force_refresh and self._is_cache_valid():
            return self._load_from_cache()

        # Perform discovery
        items = self._discover_items()
        api_keys = self._filter_api_keys(items)
        credential_pairs = self._organize_credentials(api_keys)

        # Create result
        result = DiscoveryResult(
            total_items=len(items),
            api_keys=api_keys,
            credential_pairs=credential_pairs,
            discovery_timestamp=datetime.now().isoformat(),
            cache_file=self.cache_config.cache_file,
        )

        # Cache the result
        self._cache_result(result)

        return result

    def get_api_keys_by_provider(self, provider: ProviderType) -> List[APIKeyItem]:
        """
        Get all API keys for a specific provider.

        Args:
            provider: The provider to filter by

        Returns:
            List of API keys for the provider
        """
        result = self.discover_api_keys()
        return [key for key in result.api_keys if key.provider == provider]

    def get_working_api_keys(self) -> List[APIKeyItem]:
        """
        Get all API keys marked as working.

        Returns:
            List of working API keys
        """
        result = self.discover_api_keys()
        return [key for key in result.api_keys if key.status == APIKeyStatus.WORKING]

    def refresh_cache(self) -> DiscoveryResult:
        """
        Force refresh the cache by re-discovering API keys.

        Returns:
            Fresh discovery result
        """
        return self.discover_api_keys(force_refresh=True)

    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get the current cache status.

        Returns:
            Dictionary with cache information
        """
        if not self._cache:
            return {"status": "no_cache", "age_hours": None}

        if not self._last_discovery:
            return {"status": "unknown", "age_hours": None}

        age = datetime.now() - self._last_discovery
        age_hours = age.total_seconds() / 3600

        return {
            "status": "valid"
            if age_hours < self.cache_config.max_age_hours
            else "expired",
            "age_hours": round(age_hours, 2),
            "max_age_hours": self.cache_config.max_age_hours,
            "last_discovery": self._last_discovery.isoformat(),
        }

    def _discover_items(self) -> List[Dict[str, Any]]:
        """
        Discover all items from 1Password.

        Returns:
            List of item dictionaries
        """
        try:
            # List all items
            result = subprocess.run(
                ["op", "item", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )

            items = json.loads(result.stdout)
            return items

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to list 1Password items: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse 1Password output: {e}") from e

    def _filter_api_keys(self, items: List[Dict[str, Any]]) -> List[APIKeyItem]:
        """
        Filter items to identify potential API keys.

        Args:
            items: List of 1Password items

        Returns:
            List of API key items
        """
        api_keys = []

        for item in items:
            if self._is_api_key_item(item):
                try:
                    # Get detailed item information
                    item_detail = self._get_item_detail(item["id"])

                    # Create API key item
                    api_key = APIKeyItem(
                        id=item["id"],
                        title=item.get("title", "Unknown"),
                        category=item.get("category", "Unknown"),
                        url=item_detail.get("urls", [{}])[0].get("href")
                        if item_detail.get("urls")
                        else None,
                        notes=item_detail.get("notes"),
                        tags=item_detail.get("tags", []),
                        created_at=item_detail.get("created_at"),
                        updated_at=item_detail.get("updated_at"),
                        metadata=item_detail,
                    )

                    api_keys.append(api_key)

                except Exception as e:
                    # Log error but continue with other items
                    print(
                        f"Warning: Failed to process item {item.get('id', 'unknown')}: {e}"
                    )
                    continue

        return api_keys

    def _is_api_key_item(self, item: Dict[str, Any]) -> bool:
        """
        Determine if an item is likely an API key.

        Args:
            item: 1Password item dictionary

        Returns:
            True if the item appears to be an API key
        """
        title = item.get("title", "").lower()
        category = item.get("category", "").lower()

        # Look for specific API key indicators in title
        api_key_indicators = [
            "api key",
            "api token",
            "api secret",
            "api credential",
            "openai",
            "gpt",
            "chatgpt",
            "claude",
            "anthropic",
            "google",
            "gemini",
            "aws",
            "amazon",
            "bedrock",
            "huggingface",
            "hf",
            "cohere",
            "ai21",
            "azure",
            "access key",
            "secret key",
        ]

        # Check if title contains specific API key indicators
        if any(indicator in title for indicator in api_key_indicators):
            return True

        # Check for generic API indicators (but be more specific)
        if "api" in title and any(word in title for word in ["key", "token", "secret"]):
            return True

        # Check if category suggests API keys (but be more specific)
        if category == "api credential":
            return True

        # Check tags for API key indicators
        tags = item.get("tags", [])
        if any(
            indicator in tag.lower() for tag in tags for indicator in api_key_indicators
        ):
            return True

        return False

    def _get_item_detail(self, item_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific item.

        Args:
            item_id: 1Password item ID

        Returns:
            Detailed item information
        """
        try:
            result = subprocess.run(
                ["op", "item", "get", item_id, "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )

            return json.loads(result.stdout)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get item {item_id}: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse item {item_id}: {e}") from e

    def _organize_credentials(self, api_keys: List[APIKeyItem]) -> List[CredentialPair]:
        """
        Organize credentials into logical pairs.

        Args:
            api_keys: List of discovered API keys

        Returns:
            List of credential pairs
        """
        pairs = []
        processed_ids = set()

        for primary in api_keys:
            if primary.id in processed_ids:
                continue

            # Look for related credentials
            secondary = self._find_related_credential(primary, api_keys)

            if secondary:
                pair = CredentialPair(
                    primary=primary,
                    secondary=secondary,
                    pair_type=self._determine_pair_type(primary, secondary),
                    description=f"Auto-paired credentials for {primary.detected_provider.value}",
                )
                pairs.append(pair)
                processed_ids.add(primary.id)
                processed_ids.add(secondary.id)
            else:
                # Single credential
                pair = CredentialPair(
                    primary=primary,
                    secondary=None,
                    pair_type="single",
                    description=f"Single credential for {primary.detected_provider.value}",
                )
                pairs.append(pair)
                processed_ids.add(primary.id)

        return pairs

    def _find_related_credential(
        self, primary: APIKeyItem, all_keys: List[APIKeyItem]
    ) -> Optional[APIKeyItem]:
        """
        Find a related credential for pairing.

        Args:
            primary: Primary credential to find a pair for
            all_keys: All available API keys

        Returns:
            Related credential if found, None otherwise
        """
        if primary.detected_provider == ProviderType.AWS:
            return self._find_aws_pair(primary, all_keys)
        elif primary.detected_provider == ProviderType.GOOGLE:
            return self._find_google_pair(primary, all_keys)

        return None

    def _find_aws_pair(
        self, primary: APIKeyItem, all_keys: List[APIKeyItem]
    ) -> Optional[APIKeyItem]:
        """
        Find AWS credential pair (Access Key ID + Secret Access Key).

        Args:
            primary: Primary AWS credential
            all_keys: All available API keys

        Returns:
            Paired AWS credential if found
        """
        title = primary.title.lower()

        # Determine if primary is access key or secret
        is_access_key = "access key" in title or "access_key" in title
        is_secret = "secret" in title or "secret key" in title or "secret_key" in title

        if is_access_key:
            # Look for secret
            for key in all_keys:
                if (
                    key.id != primary.id
                    and key.provider == ProviderType.AWS
                    and (
                        "secret" in key.title.lower()
                        or "secret key" in key.title.lower()
                    )
                ):
                    return key
        elif is_secret:
            # Look for access key
            for key in all_keys:
                if (
                    key.id != primary.id
                    and key.provider == ProviderType.AWS
                    and (
                        "access key" in key.title.lower()
                        or "access_key" in key.title.lower()
                    )
                ):
                    return key

        return None

    def _find_google_pair(
        self, primary: APIKeyItem, all_keys: List[APIKeyItem]
    ) -> Optional[APIKeyItem]:
        """
        Find Google credential pair.

        Args:
            primary: Primary Google credential
            all_keys: All available API keys

        Returns:
            Paired Google credential if found
        """
        # Google credentials are often single items
        # but we can look for related items with similar naming

        for key in all_keys:
            if (
                key.id != primary.id
                and key.provider == ProviderType.GOOGLE
                and self._are_google_credentials_related(primary, key)
            ):
                return key

        return None

    def _are_google_credentials_related(
        self, cred1: APIKeyItem, cred2: APIKeyItem
    ) -> bool:
        """
        Determine if two Google credentials are related.

        Args:
            cred1: First Google credential
            cred2: Second Google credential

        Returns:
            True if credentials appear to be related
        """
        title1 = cred1.title.lower()
        title2 = cred2.title.lower()

        # Check for common patterns
        if "service account" in title1 and "service account" in title2:
            return True
        if "api key" in title1 and "api key" in title2:
            return True

        return False

    def _determine_pair_type(
        self, primary: APIKeyItem, secondary: Optional[APIKeyItem]
    ) -> str:
        """
        Determine the type of credential pair.

        Args:
            primary: Primary credential
            secondary: Secondary credential (if any)

        Returns:
            Pair type description
        """
        if not secondary:
            return "single"

        if primary.provider == ProviderType.AWS:
            return "aws_access_secret"
        elif primary.provider == ProviderType.GOOGLE:
            return "google_credentials"
        else:
            return "generic_pair"

    def _is_cache_valid(self) -> bool:
        """
        Check if the current cache is valid.

        Returns:
            True if cache is valid and not expired
        """
        if not self.cache_config.enabled:
            return False

        if not self._last_discovery:
            return False

        age = datetime.now() - self._last_discovery
        return age.total_seconds() < (self.cache_config.max_age_hours * 3600)

    def _load_from_cache(self) -> DiscoveryResult:
        """
        Load discovery result from cache.

        Returns:
            Cached discovery result
        """
        if not self._cache:
            raise RuntimeError("No cached data available")

        return DiscoveryResult(**self._cache)

    def _cache_result(self, result: DiscoveryResult) -> None:
        """
        Cache the discovery result.

        Args:
            result: Discovery result to cache
        """
        if not self.cache_config.enabled:
            return

        self._cache = result.dict()
        self._last_discovery = datetime.now()

        # Save to file
        cache_path = Path(self.cache_config.cache_file)
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        with open(cache_path, "w") as f:
            json.dump(self._cache, f, indent=2, default=str)
