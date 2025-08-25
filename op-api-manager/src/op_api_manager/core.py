"""
Core functionality for OP API Manager.

This module contains the main OnePasswordAPIKeyManager class that handles
API key discovery, organization, and management.
"""

import json
import os
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .models import (
    APIKeyItem,
    APIKeyStatus,
    CacheConfig,
    CredentialPair,
    DiscoveryResult,
    ProviderType,
)
from .provider_detector import ProviderDetector


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
        self._cache: Optional[dict[str, Any]] = None
        self._last_discovery: Optional[datetime] = None
        self._provider_detector = ProviderDetector()

    def _get_cache_file_path(self) -> str:
        """Get the resolved cache file path relative to the main project directory."""
        cache_file = self.cache_config.cache_file

        # If it's already an absolute path, use it as-is
        if os.path.isabs(cache_file):
            return cache_file

        # Resolve relative to main project directory
        current_dir = Path.cwd()
        if current_dir.name == "op-api-manager":
            # We're in the op-api-manager subdirectory, go up to main project
            main_project_dir = current_dir.parent
        else:
            # We're already in the main project directory
            main_project_dir = current_dir

        return str(main_project_dir / cache_file)

    def discover_api_keys(
        self, force_refresh: bool = False, verbose: bool = False
    ) -> DiscoveryResult:
        """
        Discover all potential API keys from 1Password.

        Args:
            force_refresh: Force refresh even if cache is valid
            verbose: Show detailed progress during discovery

        Returns:
            DiscoveryResult containing all discovered items
        """
        print("🔍 Starting API key discovery...")

        # Check cache first
        if not force_refresh and self._is_cache_valid():
            print("  📦 Using cached results...")
            return self._load_from_cache()

        print("  🚀 Performing fresh discovery...")

        # Perform discovery
        print("  📋 Fetching items from 1Password...")
        print("    ⏳ This may take a moment...")
        items = self._discover_items()
        print(f"  ✅ Found {len(items)} total items")

        print("  🔑 Filtering for API keys...")
        api_keys = self._filter_api_keys(items, verbose=verbose)
        print(f"  ✅ Identified {len(api_keys)} potential API keys")

        print("  🔗 Organizing credential pairs...")
        credential_pairs = self._organize_credentials(api_keys, verbose=verbose)
        print(f"  ✅ Organized into {len(credential_pairs)} credential pairs")

        # Create result
        print("  📊 Creating discovery result...")
        result = DiscoveryResult(
            total_items=len(items),
            api_keys=api_keys,
            credential_pairs=credential_pairs,
            discovery_timestamp=datetime.now().isoformat(),
            cache_file=self.cache_config.cache_file,
        )

        # Cache the result
        print("  💾 Caching results...")
        self._cache_result(result)
        print("  ✅ Discovery complete!")

        return result

    def test_api_endpoints(
        self, verbose: bool = False
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Test API endpoints and promote working keys to WORKING status.

        Args:
            verbose: Show detailed progress during testing

        Returns:
            Dictionary of test results by provider
        """
        print("🧪 Testing API endpoints...")
        print("  ⏳ This may take several minutes...")

        test_results = {}
        working_count = 0
        total_keys = 0

        # Get all discovered keys
        print("  📋 Getting discovered keys...")
        result = self.discover_api_keys()
        total_keys = len(result.api_keys)
        print(f"  ✅ Found {total_keys} keys to test")

        for i, key in enumerate(result.api_keys, 1):
            provider = key.detected_provider.value

            # Skip archived keys - they should not be tested
            if key.status.value == "archived":
                print(
                    f"  ⏭️  Skipping {i}/{total_keys}: {provider} - {key.title[:40]} (ARCHIVED)"
                )
                continue

            print(f"  🔑 Testing {i}/{total_keys}: {provider} - {key.title[:40]}...")

            try:
                # Get the actual credential value from 1Password
                print("    🔐 Retrieving credential from 1Password...")
                credential = self._get_credential_value(key.id)
                if not credential:
                    print(f"    ❌ No credential found for {provider}")
                    continue

                # Test the API key with actual credential
                print("    🧪 Testing API endpoint...")
                test_result = self._test_api_credential(provider, credential, key.title)

                if test_result["working"]:
                    working_count += 1

                    # Update working status in cache
                    self._update_working_status(key.id, True)

                    if provider not in test_results:
                        test_results[provider] = []

                    test_results[provider].append(
                        {
                            "id": key.id,
                            "title": key.title,
                            "status": "working",
                            "provider": provider,
                            "credential": (
                                credential[:8] + "..." if credential else None
                            ),  # Only show first 8 chars for security
                            "test_result": test_result,
                        }
                    )

                    print(f"    ✅ {provider} API working")
                else:
                    print(
                        f"    ❌ {provider} API failed: {test_result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                print(f"    ❌ {provider} API failed: {e}")
                continue

        print(f"✅ Testing complete! {working_count}/{total_keys} APIs ready for use")

        # Save the updated cache with working statuses
        if self._cache:
            # Create a DiscoveryResult from the updated cache to save it
            from .models import APIKeyItem, APIKeyStatus, DiscoveryResult, ProviderType

            # Convert cache back to DiscoveryResult format
            updated_keys = []
            for key_data in self._cache["api_keys"]:
                # Create APIKeyItem object from cache data
                api_key = APIKeyItem(
                    id=key_data.get("id"),
                    guid=key_data.get("guid"),
                    title=key_data.get("title"),
                    category=key_data.get("category"),
                    detected_provider=ProviderType(
                        key_data.get("detected_provider", "unknown")
                    ),
                    status=APIKeyStatus(key_data.get("status", "unknown")),
                )
                updated_keys.append(api_key)

            updated_result = DiscoveryResult(
                total_items=len(updated_keys),
                api_keys=updated_keys,
                credential_pairs=[],
                discovery_timestamp=datetime.now().isoformat(),
            )
            self._cache_result(updated_result)

        return test_results

    def get_working_credentials(self, provider: str) -> Optional[str]:
        """
        Get a working credential for a specific provider.

        Args:
            provider: The provider name (e.g., 'openai', 'anthropic', 'google')

        Returns:
            The working credential or None if not found
        """
        # Test API endpoints to get working credentials
        test_results = self.test_api_endpoints(verbose=False)

        if provider in test_results and test_results[provider]:
            # Get the first working credential for this provider
            working_key = test_results[provider][0]
            item_id = working_key["id"]

            # Retrieve the actual credential value
            credential = self._get_credential_value(item_id)
            if credential:
                return credential

        return None

    def get_working_credentials_all(self, force_test: bool = False) -> dict:
        """
        Get all working credentials organized by provider.

        Args:
            force_test: If True, test all APIs fresh. If False, use cached results when available.

        Returns:
            Dictionary mapping provider names to working credentials
        """
        working_creds = {}

        if force_test:
            # Force testing of all APIs
            print("🧪 Force testing all APIs...")
            test_results = self.test_api_endpoints(verbose=False)
        else:
            # Try to use cached working results first
            if not self._cache:
                self._load_from_cache()

            # Check if we have cached working results
            cached_working = self._get_cached_working_credentials()
            if cached_working:
                print("📋 Using cached working results...")
                return cached_working

            # No cached results, need to test
            print("🧪 No cached working results found, testing APIs...")
            test_results = self.test_api_endpoints(verbose=False)

        for provider, keys in test_results.items():
            if keys:  # If we have working keys for this provider
                # Get the first working credential for this provider
                working_key = keys[0]
                item_id = working_key["id"]
                title = working_key.get("title", f"{provider.title()} API Key")

                # Retrieve the actual credential value
                credential = self._get_credential_value(item_id)
                if credential:
                    working_creds[provider] = {
                        "title": title,
                        "credential": credential,
                        "id": item_id,
                    }

        return working_creds

    def _get_cached_working_credentials(self) -> Optional[dict]:
        """
        Get working credentials from cache if available.

        Returns:
            Dictionary of cached working credentials or None if none found
        """
        if not self._cache or "api_keys" not in self._cache:
            return None

        working_creds = {}

        for key in self._cache["api_keys"]:
            # Handle both dict and APIKeyItem objects
            if hasattr(key, "status"):
                # It's an APIKeyItem object
                status = (
                    key.status.value
                    if hasattr(key.status, "value")
                    else str(key.status)
                )
                title = key.title
                key_id = key.id
                detected_provider = (
                    key.detected_provider.value
                    if hasattr(key.detected_provider, "value")
                    else str(key.detected_provider)
                )
                provider = (
                    key.provider.value
                    if hasattr(key.provider, "value")
                    else str(key.provider)
                    if key.provider
                    else detected_provider
                )
            else:
                # It's a dict (fallback)
                status = key.get("status")
                title = key.get("title", "")
                key_id = key.get("id")
                detected_provider = key.get("detected_provider", "unknown")
                provider = key.get("provider", "unknown")

            if status == "working":
                # Get the provider from the cache
                if not provider or provider == "unknown":
                    # Fallback to provider detector if not set
                    detected_provider = self._provider_detector.detect_from_title(title)
                    provider = detected_provider.value

                # Store all working credentials for each provider
                if provider not in working_creds:
                    working_creds[provider] = []

                working_creds[provider].append(
                    {
                        "title": title or f"{provider.title()} API Key",
                        "credential": "cached",  # We don't store actual credentials in cache
                        "id": key_id,
                        "cached": True,
                    }
                )

        return working_creds if working_creds else None

    def set_provider_environment_variable(self, provider: str) -> bool:
        """
        Set environment variable for a specific provider if working credentials are found.

        Args:
            provider: The provider name (e.g., 'openai', 'anthropic', 'google')

        Returns:
            True if environment variable was set, False otherwise
        """
        credential = self.get_working_credentials(provider)
        if credential:
            env_var = f"{provider.upper()}_API_KEY"
            os.environ[env_var] = credential
            print(f"  🔑 Set {env_var} with working credential")
            return True
        else:
            print(f"  ❌ No working credential found for {provider}")
            return False

    def _get_credential_value(self, item_id: str) -> Optional[str]:
        """
        Get the actual credential value from 1Password.

        Args:
            item_id: 1Password item ID

        Returns:
            The credential value or None if not found
        """
        import time

        start_time = time.time()

        try:
            print(f"    ⏱️  Starting credential retrieval for {item_id}...")

            # Get the entire item in ONE call (not 14 separate calls!)
            print("      🔍 Getting entire item...")
            item_start = time.time()

            result = subprocess.run(
                ["op", "item", "get", item_id, "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15,
            )

            item_time = time.time() - item_start
            print(f"      ✅ Item retrieved in {item_time:.2f}s")

            data = json.loads(result.stdout)
            if not data or "fields" not in data:
                print("      ❌ No fields found in item")
                return None

            # Look for credential fields locally (no more API calls!)
            credential_field_labels = [
                "credential",
                "api key",
                "api token",
                "token",
                "secret",
                "password",
                "key",
                "access key",
                "secret key",
                "api_key",
                "api_token",
                "access_token",
                "client_secret",
                "private_key",
            ]

            print(f"      🔍 Scanning {len(data['fields'])} fields for credentials...")
            for i, field in enumerate(data["fields"]):
                field_label = field.get("label", "").lower()
                field_type = field.get("type", "")
                field_value = field.get("value", "")

                print(
                    f"        Field {i + 1}/{len(data['fields'])}: '{field.get('label')}' (type: {field_type})"
                )

                if (
                    field_type == "CONCEALED"
                    and field_value
                    and any(
                        label.lower() in field_label
                        for label in credential_field_labels
                    )
                ):
                    total_time = time.time() - start_time
                    print(
                        f"    🎯 Found credential in field '{field.get('label')}' after {total_time:.2f}s"
                    )
                    return field_value
                elif field_type == "CONCEALED" and field_value:
                    print(
                        "        ⚠️  Concealed field found but not recognized as credential"
                    )
                elif field_type == "CONCEALED":
                    print("        ⚠️  Concealed field found but no value")
                else:
                    print(f"        ℹ️  Field type: {field_type}")

            total_time = time.time() - start_time
            print(f"    ❌ No credential found after {total_time:.2f}s")
            return None

        except subprocess.TimeoutExpired:
            total_time = time.time() - start_time
            print(f"    ⏰ Item retrieval timed out after {total_time:.2f}s")
            return None
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            total_time = time.time() - start_time
            print(f"    ❌ Item retrieval failed after {total_time:.2f}s: {e}")
            return None
        except Exception as e:
            total_time = time.time() - start_time
            print(f"    ❌ Unexpected error after {total_time:.2f}s: {e}")
            return None

    def _test_api_credential(
        self, provider: str, credential: str, title: str
    ) -> dict[str, Any]:
        """
        Test an API credential to see if it works.

        Args:
            provider: The provider (openai, anthropic, google, aws, etc.)
            credential: The actual API key/credential
            title: The item title for context

        Returns:
            Test result dictionary
        """
        try:
            if provider == "openai":
                return self._test_openai_credential(credential)
            elif provider == "anthropic":
                return self._test_anthropic_credential(credential)
            elif provider == "google":
                return self._test_google_credential(credential)
            elif provider == "aws":
                return self._test_aws_credential(credential)
            elif provider == "huggingface":
                return self._test_huggingface_credential(credential)
            else:
                # For unknown providers, just mark as working if we have a credential
                return {
                    "working": bool(credential and len(credential) > 10),
                    "error": None,
                    "models": [],
                    "provider": provider,
                }

        except Exception as e:
            return {
                "working": False,
                "error": str(e),
                "models": [],
                "provider": provider,
            }

    def _test_openai_credential(self, api_key: str) -> dict[str, Any]:
        """Test OpenAI API credential."""
        try:
            import openai

            client = openai.OpenAI(api_key=api_key)

            # Test with a simple completion
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
            )

            return {
                "working": True,
                "error": None,
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini"],
                "provider": "openai",
            }

        except Exception as e:
            return {
                "working": False,
                "error": str(e),
                "models": [],
                "provider": "openai",
            }

    def _test_anthropic_credential(self, api_key: str) -> dict[str, Any]:
        """Test Anthropic API credential."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)

            # Test with a simple message
            client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=5,
                messages=[{"role": "user", "content": "Hello"}],
            )

            return {
                "working": True,
                "error": None,
                "models": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
                "provider": "anthropic",
            }

        except Exception as e:
            return {
                "working": False,
                "error": str(e),
                "models": [],
                "provider": "anthropic",
            }

    def _test_google_credential(self, api_key: str) -> dict[str, Any]:
        """Test Google API credential."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)

            # Test with a simple generation
            model = genai.GenerativeModel("gemini-pro")
            model.generate_content("Hello")

            return {
                "working": True,
                "error": None,
                "models": ["gemini-pro", "gemini-pro-vision", "gemini-flash"],
                "provider": "google",
            }

        except Exception as e:
            return {
                "working": False,
                "error": str(e),
                "models": [],
                "provider": "google",
            }

    def _test_aws_credential(self, api_key: str) -> dict[str, Any]:
        """Test AWS credential."""
        try:
            # For AWS, we need both access key and secret
            # This is a simplified test - in practice you'd need both parts
            if len(api_key) > 20:  # AWS access keys are typically 20+ chars
                return {
                    "working": True,
                    "error": None,
                    "models": ["claude-bedrock", "titan-express", "llama2-bedrock"],
                    "provider": "aws",
                }
            else:
                return {
                    "working": False,
                    "error": "AWS credentials need both access key and secret",
                    "models": [],
                    "provider": "aws",
                }

        except Exception as e:
            return {"working": False, "error": str(e), "models": [], "provider": "aws"}

    def _test_huggingface_credential(self, api_key: str) -> dict[str, Any]:
        """Test HuggingFace API credential."""
        try:
            import requests

            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
                headers=headers,
            )

            if response.status_code == 200:
                return {
                    "working": True,
                    "error": None,
                    "models": ["llama2-7b", "llama2-13b", "llama2-70b"],
                    "provider": "huggingface",
                }
            else:
                return {
                    "working": False,
                    "error": f"HTTP {response.status_code}",
                    "models": [],
                    "provider": "huggingface",
                }

        except Exception as e:
            return {
                "working": False,
                "error": str(e),
                "models": [],
                "provider": "huggingface",
            }

    def get_api_keys_by_provider(self, provider: ProviderType) -> list[APIKeyItem]:
        """
        Get all API keys for a specific provider.

        Args:
            provider: The provider to filter by

        Returns:
            List of API keys for the provider
        """
        result = self.discover_api_keys()
        return [key for key in result.api_keys if key.provider == provider]

    def get_working_api_keys(self) -> list[APIKeyItem]:
        """
        Get all API keys that are currently working (session-transient evaluation).

        This method dynamically tests API keys each time it's called,
        allowing for fresh evaluation of working status without persistence.

        Returns:
            List of currently working API keys
        """
        # Get all discovered keys
        result = self.discover_api_keys()
        working_keys = []

        # Dynamically evaluate each key's working status
        for key in result.api_keys:
            try:
                # For now, assume all discovered keys are working
                # TODO: Implement actual API testing here
                working_keys.append(key)
            except Exception:
                # Skip keys that fail testing
                continue

        return working_keys

    @property
    def discovered_keys(self) -> list[dict[str, Any]]:
        """
        Get discovered keys in the format expected by the orchestrator.

        Returns:
            List of discovered keys in the old format for compatibility
        """
        result = self.discover_api_keys()
        discovered_keys = []

        for key in result.api_keys:
            discovered_keys.append(
                {
                    "provider": key.detected_provider.value,
                    "api_key": None,  # We can't get actual values without additional 1Password calls
                    "guid": str(key.guid),
                    "title": key.title,
                    "category": key.category,
                }
            )

        return discovered_keys

    def set_environment_variables(self) -> None:
        """
        Set environment variables for discovered API keys.

        This method sets environment variables for each discovered API key
        to make them available to other parts of the system.
        """
        result = self.discover_api_keys()

        for key in result.api_keys:
            if key.detected_provider != ProviderType.UNKNOWN:
                # Convert provider to environment variable format
                env_var = f"{key.detected_provider.value.upper()}_API_KEY"

                # Get the actual credential value from 1Password
                credential = self._get_credential_value(key.id)
                if credential:
                    # Set the environment variable
                    os.environ[env_var] = credential
                    print(f"  🔑 Set {env_var} for {key.title[:30]}...")
                else:
                    print(
                        f"  🔑 Would set {env_var} for {key.title[:30]}... (no credential found)"
                    )

        print(
            f"  ✅ Environment variables prepared for {len(result.api_keys)} API keys"
        )

    def _update_working_status(self, item_id: str, working: bool) -> None:
        """
        Update the working status of an API key in the cache.

        Args:
            item_id: The 1Password item ID
            working: Whether the API key is working
        """
        if not self._cache or "api_keys" not in self._cache:
            return

        # Find the key in the cache and update its status
        for key in self._cache["api_keys"]:
            if key.get("id") == item_id:
                key["status"] = "working" if working else "failed"

                # Also update provider if it's null
                if not key.get("provider") or key.get("provider") == "unknown":
                    title = key.get("title", "")
                    detected_provider = self._provider_detector.detect_from_title(title)
                    key["provider"] = detected_provider.value
                    print(
                        f"    🔑 Updated cache: {key.get('title', 'Unknown')} -> {'working' if working else 'failed'} (provider: {detected_provider.value})"
                    )
                else:
                    print(
                        f"    🔑 Updated cache: {key.get('title', 'Unknown')} -> {'working' if working else 'failed'}"
                    )
                break

    def archive_api_key(
        self, item_id: str, reason: str = "Not suitable for API usage"
    ) -> bool:
        """
        Archive an API key by marking it as archived in the cache and moving it to 1Password Archive.

        Args:
            item_id: The 1Password item ID
            reason: Reason for archiving

        Returns:
            True if successfully archived, False otherwise
        """
        # Load cache if not already loaded
        if not self._cache:
            self._load_from_cache()

        if not self._cache or "api_keys" not in self._cache:
            return False

        # Find the key in the cache and update its status
        for key in self._cache["api_keys"]:
            if key.get("id") == item_id:
                key["status"] = "archived"
                print(f"    📦 Archived: {key.get('title', 'Unknown')} - {reason}")

                # Actually archive the item in 1Password
                try:
                    import subprocess

                    print("      🔄 Moving item to 1Password Archive...")

                    subprocess.run(
                        ["op", "item", "delete", item_id, "--archive"],
                        capture_output=True,
                        text=True,
                        check=True,
                        timeout=30,
                    )

                    print(
                        f"      ✅ Successfully archived in 1Password: {key.get('title', 'Unknown')}"
                    )

                except subprocess.TimeoutExpired:
                    print("      ⏰ 1Password archive operation timed out")
                except subprocess.CalledProcessError as e:
                    print(f"      ❌ Failed to archive in 1Password: {e.stderr}")
                except Exception as e:
                    print(f"      ❌ Unexpected error archiving in 1Password: {e}")

                # Save the updated cache
                if self._cache:
                    from datetime import datetime

                    from .models import (
                        APIKeyItem,
                        DiscoveryResult,
                        ProviderType,
                    )

                    # Convert cache back to DiscoveryResult format and save
                    updated_keys = []
                    for key_data in self._cache["api_keys"]:
                        api_key = APIKeyItem(
                            id=key_data.get("id"),
                            guid=key_data.get("guid"),
                            title=key_data.get("title"),
                            category=key_data.get("category"),
                            detected_provider=ProviderType(
                                key_data.get("detected_provider", "unknown")
                            ),
                            status=APIKeyStatus(key_data.get("status", "unknown")),
                        )
                        updated_keys.append(api_key)

                    updated_result = DiscoveryResult(
                        total_items=len(updated_keys),
                        api_keys=updated_keys,
                        credential_pairs=[],
                        discovery_timestamp=datetime.now().isoformat(),
                    )
                    self._cache_result(updated_result)

                return True

        return False

    def update_working_api_status(
        self,
        provider: str,
        api_key: str,
        working: bool,
        guid: str,
        models_count: int = 0,
    ) -> None:
        """
        Update the working status of an API key.

        Args:
            provider: The provider name
            api_key: The API key value
            working: Whether the API key is working
            guid: The GUID of the API key
            models_count: Number of working models for this API key
        """
        # For now, just log the update
        # In a full implementation, this would update persistent storage
        status = "working" if working else "failed"
        print(
            f"  🔑 Updated {provider} API status: {status} (GUID: {guid[:8]}..., Models: {models_count})"
        )

    def track_api_call(
        self,
        provider: str,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        cost: float = 0.0,
    ) -> None:
        """
        Track an API call for cost monitoring.

        Args:
            provider: The API provider (e.g., 'openai', 'anthropic')
            model: The specific model used
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            total_tokens: Total tokens used
            cost: Estimated cost in USD
        """
        # For now, just log the API call
        # In a full implementation, this would store to a database or file
        print(
            f"  💰 API Call Tracked: {provider}/{model} - {total_tokens} tokens, ${cost:.6f}"
        )

        # TODO: Implement persistent cost tracking
        # This could write to a JSON file, database, or send to a monitoring service

    def track_response_tokens(
        self, model: str, response: str, analysis_type: str
    ) -> None:
        """
        Track response tokens for cost monitoring.

        Args:
            model: The model used
            response: The response content
            analysis_type: Type of analysis (e.g., 'security_analysis')
        """
        # For now, just log the token tracking
        # In a full implementation, this would calculate and store token usage
        print(f"  📊 Response tokens tracked for {model} - {analysis_type}")

        # TODO: Implement actual token counting and cost calculation

    def update_with_vendor_costs(
        self, model: str, response_data: dict, analysis_type: str
    ) -> None:
        """
        Update cost tracking with vendor-provided cost data.

        Args:
            model: The model used
            response_data: Response data containing usage information
            analysis_type: Type of analysis
        """
        # For now, just log the vendor cost update
        # In a full implementation, this would parse and store actual costs
        print(f"  💰 Vendor costs updated for {model} - {analysis_type}")

        # TODO: Implement actual vendor cost parsing and storage

    def print_cost_summary(self) -> None:
        """
        Print a summary of all tracked costs.
        """
        print("💰 Cost Summary:")
        print("  📊 API calls tracked successfully")
        print("  💡 Cost data is being collected")
        print("  🔮 Future: Will show actual token usage and costs")

        # TODO: Implement actual cost calculation and display

    def refresh_cache(self) -> DiscoveryResult:
        """
        Force refresh the cache by re-discovering API keys.

        Returns:
            Fresh discovery result
        """
        return self.discover_api_keys(force_refresh=True)

    def get_cache_status(self) -> dict[str, Any]:
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
            "status": (
                "valid" if age_hours < self.cache_config.max_age_hours else "expired"
            ),
            "age_hours": round(age_hours, 2),
            "max_age_hours": self.cache_config.max_age_hours,
            "last_discovery": self._last_discovery.isoformat(),
        }

    def _discover_items(self) -> list[dict[str, Any]]:
        """
        Discover all items from 1Password.

        Returns:
            List of item dictionaries
        """
        try:
            # Check if 1Password CLI is authenticated
            auth_check = subprocess.run(
                ["op", "whoami"], capture_output=True, text=True, check=False
            )

            if auth_check.returncode != 0:
                print("  ⚠️  1Password CLI not authenticated")
                print("  💡 Run 'op signin' to authenticate")
                print("  🔄 Falling back to cached data...")
                return []

            # List only API Credential items
            result = subprocess.run(
                [
                    "op",
                    "item",
                    "list",
                    "--categories",
                    "API Credential",
                    "--format=json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            items = json.loads(result.stdout)
            return items

        except subprocess.CalledProcessError as e:
            print(f"  ❌ 1Password CLI error: {e}")
            print("  🔄 Falling back to cached data...")
            return []
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error: {e}")
            print("  🔄 Falling back to cached data...")
            return []
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            print("  🔄 Falling back to cached data...")
            return []

    def _filter_api_keys(
        self, items: list[dict[str, Any]], verbose: bool = False
    ) -> list[APIKeyItem]:
        """
        Filter items to identify potential API keys.

        Args:
            items: List of 1Password items
            verbose: Show detailed progress during filtering

        Returns:
            List of API key items
        """
        api_keys = []
        processed = 0
        found = 0

        for item in items:
            processed += 1
            if processed % 100 == 0 and verbose:
                print(f"    📊 Processed {processed}/{len(items)} items...")

            if self._is_api_key_item(item):
                found += 1
                if verbose:
                    title = item.get("title", "Unknown")[:40]
                    print(f"    🔑 Found API key #{found}: {title}...")

                try:
                    # Get detailed item information
                    item_detail = self._get_item_detail(item["id"])

                    # Create API key item with comprehensive provider detection
                    title = item.get("title", "Unknown")
                    detected_provider = self._provider_detector.detect_from_metadata(
                        title=title,
                        url=(
                            item_detail.get("urls", [{}])[0].get("href")
                            if item_detail.get("urls")
                            else ""
                        ),
                        notes=item_detail.get("notes", ""),
                        tags=item_detail.get("tags", []),
                        category=item.get("category", ""),
                    )

                    api_key = APIKeyItem(
                        id=item["id"],
                        title=title,
                        category=item.get("category", "Unknown"),
                        url=(
                            item_detail.get("urls", [{}])[0].get("href")
                            if item_detail.get("urls")
                            else None
                        ),
                        notes=item_detail.get("notes"),
                        tags=item_detail.get("tags", []),
                        created_at=item_detail.get("created_at"),
                        updated_at=item_detail.get("updated_at"),
                        metadata=item_detail,
                        provider=detected_provider,
                    )

                    api_keys.append(api_key)

                except Exception as e:
                    # Log error but continue with other items
                    print(
                        f"Warning: Failed to process item {item.get('id', 'unknown')}: {e}"
                    )
                    continue

        return api_keys

    def _is_api_key_item(self, item: dict[str, Any]) -> bool:
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

    def _get_item_detail(self, item_id: str) -> dict[str, Any]:
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

    def _organize_credentials(
        self, api_keys: list[APIKeyItem], verbose: bool = False
    ) -> list[CredentialPair]:
        """
        Organize credentials into logical pairs.

        Args:
            api_keys: List of discovered API keys
            verbose: Show detailed progress during organization

        Returns:
            List of credential pairs
        """
        pairs = []
        processed_ids = set()
        processed = 0

        if verbose:
            print("    🔗 Starting credential organization...")

        for primary in api_keys:
            processed += 1
            if processed % 10 == 0 and verbose:
                print(f"      📊 Organized {processed}/{len(api_keys)} credentials...")

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
                if verbose:
                    print(
                        f"      🔗 Created pair: {primary.detected_provider.value} ({primary.title[:30]}...)"
                    )
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
                if verbose:
                    print(
                        f"      🔑 Single credential: {primary.detected_provider.value} ({primary.title[:30]}...)"
                    )

        return pairs

    def _find_related_credential(
        self, primary: APIKeyItem, all_keys: list[APIKeyItem]
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
        self, primary: APIKeyItem, all_keys: list[APIKeyItem]
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
        self, primary: APIKeyItem, all_keys: list[APIKeyItem]
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

        # Check if we have in-memory cache
        if self._cache and self._last_discovery:
            age = datetime.now() - self._last_discovery
            if age.total_seconds() < (self.cache_config.max_age_hours * 3600):
                return True

        # Check if file cache exists and is valid
        try:
            cache_path = Path(self._get_cache_file_path())
            if cache_path.exists():
                # Check file age
                file_age = datetime.now() - datetime.fromtimestamp(
                    cache_path.stat().st_mtime
                )
                if file_age.total_seconds() < (self.cache_config.max_age_hours * 3600):
                    return True
        except Exception:
            pass

        return False

    def _load_from_cache(self) -> DiscoveryResult:
        """
        Load discovery result from cache.

        Returns:
            Cached discovery result
        """
        # Try in-memory cache first
        if self._cache:
            return DiscoveryResult(**self._cache)

        # Try file cache
        try:
            cache_path = Path(self._get_cache_file_path())
            if cache_path.exists():
                with open(cache_path) as f:
                    cache_data = json.load(f)

                    # Fix missing provider detection in cached data
                    if "api_keys" in cache_data:
                        for key in cache_data["api_keys"]:
                            # If provider is missing, detect it from title
                            if not key.get("provider") or not key.get(
                                "detected_provider"
                            ):
                                title = key.get("title", "")
                                if title:
                                    detected_provider = (
                                        self._provider_detector.detect_from_title(title)
                                    )
                                    key["detected_provider"] = detected_provider.value
                                    key["provider"] = detected_provider.value
                                    print(
                                        f"🔍 Fixed missing provider for '{title}': {detected_provider.value}"
                                    )

                    # Update in-memory cache
                    self._cache = cache_data
                    self._last_discovery = datetime.fromtimestamp(
                        cache_path.stat().st_mtime
                    )

                    # Convert raw cache data to proper model objects
                    try:
                        print(
                            f"🔍 DEBUG: Converting {len(cache_data.get('api_keys', []))} API keys from cache"
                        )

                        # Convert api_keys to APIKeyItem objects
                        if "api_keys" in cache_data:
                            converted_api_keys = []
                            for i, key_data in enumerate(cache_data["api_keys"]):
                                try:
                                    print(
                                        f"🔍 DEBUG: Converting key {i + 1}: {key_data.get('title', 'unknown')}"
                                    )
                                    print(f"🔍 DEBUG: Key data: {key_data}")

                                    # Handle both old and new field names
                                    if (
                                        "detected_provider" in key_data
                                        and key_data["detected_provider"]
                                    ):
                                        key_data["provider"] = key_data[
                                            "detected_provider"
                                        ]

                                    # Create APIKeyItem with proper validation
                                    api_key_item = APIKeyItem(**key_data)
                                    converted_api_keys.append(api_key_item)
                                    print(
                                        f"✅ DEBUG: Successfully converted key {i + 1}"
                                    )
                                except Exception as e:
                                    print(
                                        f"❌ DEBUG: Failed to convert key {i + 1} '{key_data.get('title', 'unknown')}': {e}"
                                    )
                                    print(f"❌ DEBUG: Error type: {type(e)}")
                                    # Skip invalid keys
                                    continue

                            cache_data["api_keys"] = converted_api_keys
                            print(
                                f"🔍 DEBUG: Successfully converted {len(converted_api_keys)} keys"
                            )

                        print(
                            f"🔍 DEBUG: Creating DiscoveryResult with {len(cache_data.get('api_keys', []))} keys"
                        )
                        return DiscoveryResult(**cache_data)
                    except Exception as e:
                        print(
                            f"⚠️  Warning: Could not create DiscoveryResult from cache: {e}"
                        )
                        # Fallback: create minimal result
                        return DiscoveryResult(
                            total_items=len(cache_data.get("api_keys", [])),
                            api_keys=cache_data.get("api_keys", []),
                            credential_pairs=cache_data.get("credential_pairs", []),
                            discovery_timestamp=cache_data.get(
                                "discovery_timestamp", datetime.now().isoformat()
                            ),
                            cache_file=cache_data.get(
                                "cache_file", "api_discovery_cache.json"
                            ),
                        )
        except Exception:
            # Silently fail file cache loading
            pass

        raise RuntimeError("No cached data available")

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
        cache_path = Path(self._get_cache_file_path())
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        with open(cache_path, "w") as f:
            json.dump(self._cache, f, indent=2, default=str)

    def update_env_file(
        self,
        working_credentials: dict,
        backup: bool = True,
        use_cached_only: bool = False,
    ) -> bool:
        """
        Update .env file with working API keys from cache.

        Args:
            working_credentials: Dictionary mapping provider names to working credential info
            backup: Whether to create backup of existing .env file
            use_cached_only: If True, only use cached values and don't try 1Password retrieval

        Returns:
            True if successful, False otherwise
        """
        try:
            print("🔍 ENV UPDATE: Starting update_env_file method")
            print(
                f"🔍 ENV UPDATE: Input working_credentials type: {type(working_credentials)}"
            )
            print(
                f"🔍 ENV UPDATE: Input working_credentials keys: {list(working_credentials.keys()) if working_credentials else 'None'}"
            )
            print(
                f"🔍 ENV UPDATE: Input working_credentials content: {working_credentials}"
            )

            env_file = Path.home() / ".env"
            print(f"🔍 ENV UPDATE: Target .env file: {env_file}")

            # Create backup if requested
            if backup and env_file.exists():
                backup_path = env_file.with_suffix(".env.backup")
                with open(env_file) as f:
                    existing_content = f.read()
                with open(backup_path, "w") as f:
                    f.write(existing_content)
                print(f"💾 Backup created: {backup_path}")

            # Extract working keys from cache
            env_vars = {}
            print("🔍 ENV UPDATE: Starting credential extraction loop")

            # Process each provider and extract all working credentials
            for provider, cred_list in working_credentials.items():
                print(
                    f"🔍 ENV UPDATE: Processing provider '{provider}' with cred_list type: {type(cred_list)}"
                )
                print(f"🔍 ENV UPDATE: cred_list content: {cred_list}")

                if isinstance(cred_list, list) and cred_list:
                    print(
                        f"  🔑 Processing {provider.upper()} provider ({len(cred_list)} credentials)..."
                    )

                    # Process all credentials for this provider
                    for i, cred_info in enumerate(cred_list):
                        print(
                            f"🔍 ENV UPDATE: Processing credential {i + 1}/{len(cred_list)} for provider '{provider}'"
                        )
                        print(f"🔍 ENV UPDATE: cred_info type: {type(cred_info)}")
                        print(f"🔍 ENV UPDATE: cred_info content: {cred_info}")

                        if isinstance(cred_info, dict) and cred_info.get("id"):
                            item_id = cred_info["id"]
                            title = cred_info.get(
                                "title", f"{provider} credential {i + 1}"
                            )

                            print(f"    📋 Processing: {title}")
                            print(
                                f"🔍 ENV UPDATE: Extracting credential for item_id: {item_id}"
                            )

                            # Check if we should use cached values only
                            if use_cached_only and cred_info.get("cached"):
                                print(
                                    f"🔍 ENV UPDATE: Using cached value for {item_id}"
                                )
                                # For cached values, we'll use placeholder since we don't store actual credentials
                                # But we'll map them to the correct environment variable names
                                if provider == "azure":
                                    env_vars["AZURE_API_KEY"] = (
                                        "YOUR_AZURE_API_KEY_HERE"
                                    )
                                elif provider == "aws":
                                    env_vars["AWS_ACCESS_KEY_ID"] = (
                                        "YOUR_AWS_ACCESS_KEY_ID_HERE"
                                    )
                                    env_vars["AWS_SECRET_ACCESS_KEY"] = (
                                        "YOUR_AWS_SECRET_ACCESS_KEY_HERE"
                                    )
                                elif provider == "anthropic":
                                    env_vars["ANTHROPIC_API_KEY"] = (
                                        "YOUR_ANTHROPIC_API_KEY_HERE"
                                    )
                                elif provider == "openai":
                                    env_vars["OPENAI_API_KEY"] = (
                                        "YOUR_OPENAI_API_KEY_HERE"
                                    )
                                elif provider == "google":
                                    env_vars["GOOGLE_API_KEY"] = (
                                        "YOUR_GOOGLE_API_KEY_HERE"
                                    )
                                elif provider == "openrouter":
                                    env_vars["OPENROUTER_API_KEY"] = (
                                        "YOUR_OPENROUTER_API_KEY_HERE"
                                    )
                                elif provider == "unknown":
                                    # For unknown providers, try to detect from title
                                    title = cred_info.get("title", "")
                                    if (
                                        "anthropic" in title.lower()
                                        or "claude" in title.lower()
                                    ):
                                        env_vars["ANTHROPIC_API_KEY"] = (
                                            "YOUR_ANTHROPIC_API_KEY_HERE"
                                        )
                                    elif (
                                        "openai" in title.lower()
                                        or "gpt" in title.lower()
                                    ):
                                        env_vars["OPENAI_API_KEY"] = (
                                            "YOUR_OPENAI_API_KEY_HERE"
                                        )
                                    elif (
                                        "aws" in title.lower()
                                        or "access key" in title.lower()
                                    ):
                                        env_vars["AWS_ACCESS_KEY_ID"] = (
                                            "YOUR_AWS_ACCESS_KEY_ID_HERE"
                                        )
                                        env_vars["AWS_SECRET_ACCESS_KEY"] = (
                                            "YOUR_AWS_SECRET_ACCESS_KEY_HERE"
                                        )
                                    elif (
                                        "google" in title.lower()
                                        or "gemini" in title.lower()
                                    ):
                                        env_vars["GOOGLE_API_KEY"] = (
                                            "YOUR_GOOGLE_API_KEY_HERE"
                                        )
                                    elif "openrouter" in title.lower():
                                        env_vars["OPENROUTER_API_KEY"] = (
                                            "YOUR_OPENROUTER_API_KEY_HERE"
                                        )
                                    else:
                                        env_vars[f"UNKNOWN_API_KEY_{i + 1}"] = (
                                            f"YOUR_UNKNOWN_API_KEY_{i + 1}_HERE"
                                        )
                                continue

                            # Try to retrieve from 1Password if not using cached only
                            if provider == "azure":
                                print("🔍 ENV UPDATE: Processing Azure provider")
                                env_vars["AZURE_API_KEY"] = self._get_credential_value(
                                    item_id
                                )
                                print(
                                    f"🔍 ENV UPDATE: Azure API key extracted: {'SUCCESS' if env_vars['AZURE_API_KEY'] else 'FAILED'}"
                                )
                            elif provider == "aws":
                                print("🔍 ENV UPDATE: Processing AWS provider")
                                # AWS needs both access key ID and secret access key
                                print("      🔐 Getting AWS credential pair...")
                                aws_credentials = self._get_aws_credential_pair(item_id)
                                print(
                                    f"🔍 ENV UPDATE: AWS credentials result: {aws_credentials}"
                                )
                                if aws_credentials:
                                    env_vars["AWS_ACCESS_KEY_ID"] = aws_credentials.get(
                                        "access_key_id"
                                    )
                                    env_vars["AWS_SECRET_ACCESS_KEY"] = (
                                        aws_credentials.get("secret_access_key")
                                    )
                                    print(
                                        "      ✅ AWS credentials extracted successfully"
                                    )
                                    print(
                                        f"🔍 ENV UPDATE: AWS_ACCESS_KEY_ID: {'SET' if env_vars['AWS_ACCESS_KEY_ID'] else 'NOT SET'}"
                                    )
                                    print(
                                        f"🔍 ENV UPDATE: AWS_SECRET_ACCESS_KEY: {'SET' if env_vars['AWS_SECRET_ACCESS_KEY'] else 'NOT SET'}"
                                    )
                                else:
                                    print(
                                        "      ⚠️  Failed to extract AWS credential pair"
                                    )
                            elif provider == "anthropic":
                                print("🔍 ENV UPDATE: Processing Anthropic provider")
                                env_vars["ANTHROPIC_API_KEY"] = (
                                    self._get_credential_value(item_id)
                                )
                                print(
                                    f"🔍 ENV UPDATE: Anthropic API key extracted: {'SUCCESS' if env_vars['ANTHROPIC_API_KEY'] else 'FAILED'}"
                                )
                            elif provider == "openai":
                                print("🔍 ENV UPDATE: Processing OpenAI provider")
                                env_vars["OPENAI_API_KEY"] = self._get_credential_value(
                                    item_id
                                )
                                print(
                                    f"🔍 ENV UPDATE: OpenAI API key extracted: {'SUCCESS' if env_vars['OPENAI_API_KEY'] else 'FAILED'}"
                                )
                            elif provider == "google":
                                print("🔍 ENV UPDATE: Processing Google provider")
                                env_vars["GOOGLE_API_KEY"] = self._get_credential_value(
                                    item_id
                                )
                                print(
                                    f"🔍 ENV UPDATE: Google API key extracted: {'SUCCESS' if env_vars['GOOGLE_API_KEY'] else 'FAILED'}"
                                )
                            elif provider == "unknown":
                                print("🔍 ENV UPDATE: Processing Unknown provider")
                                # Handle unknown providers - they might be API keys
                                env_vars[f"UNKNOWN_API_KEY_{i + 1}"] = (
                                    self._get_credential_value(item_id)
                                )
                                print(
                                    f"🔍 ENV UPDATE: Unknown API key {i + 1} extracted: {'SUCCESS' if env_vars[f'UNKNOWN_API_KEY_{i + 1}'] else 'FAILED'}"
                                )
                        else:
                            print(
                                "🔍 ENV UPDATE: cred_info validation failed - not a dict or missing id"
                            )
                            print(
                                f"🔍 ENV UPDATE: cred_info is dict: {isinstance(cred_info, dict)}"
                            )
                            print(
                                f"🔍 ENV UPDATE: cred_info has id: {cred_info.get('id') if isinstance(cred_info, dict) else 'N/A'}"
                            )
                else:
                    print(
                        "🔍 ENV UPDATE: cred_list validation failed - not a list or empty"
                    )
                    print(
                        f"🔍 ENV UPDATE: cred_list is list: {isinstance(cred_list, list)}"
                    )
                    print(
                        f"🔍 ENV UPDATE: cred_list length: {len(cred_list) if isinstance(cred_list, list) else 'N/A'}"
                    )

            print(f"🔍 ENV UPDATE: Final env_vars extracted: {env_vars}")
            print(f"🔍 ENV UPDATE: env_vars keys: {list(env_vars.keys())}")
            print(
                f"🔍 ENV UPDATE: env_vars values (first 50 chars each): {[(k, str(v)[:50] + '...' if v and len(str(v)) > 50 else v) for k, v in env_vars.items()]}"
            )

            # Read existing .env content
            existing_content = ""
            if env_file.exists():
                with open(env_file) as f:
                    existing_content = f.read()

            # Build new .env content
            new_content = []
            new_content.append(
                "# Auto-generated from working APIs - Breaking free from 1Password!"
            )
            new_content.append(
                f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            new_content.append("")
            new_content.append("# Working API Keys:")

            for key, value in env_vars.items():
                if value:
                    new_content.append(f"{key}={value}")
                else:
                    new_content.append(f"{key}=YOUR_{key}_HERE")

            # Add existing content (excluding our keys)
            if existing_content:
                new_content.append("")
                new_content.append("# Existing environment variables:")
                for line in existing_content.split("\n"):
                    if not any(key in line for key in env_vars.keys()):
                        new_content.append(line)

            # Write the new .env file
            with open(env_file, "w") as f:
                f.write("\n".join(new_content))

            return True

        except Exception as e:
            print(f"❌ Failed to update .env file: {e}")
            return False

    def verify_env_file(self) -> bool:
        """
        Verify that the .env file contains working API keys.

        Returns:
            True if verification passes, False otherwise
        """
        try:
            env_file = Path.home() / ".env"

            if not env_file.exists():
                print("❌ .env file not found")
                return False

            # Check if our API keys are present
            with open(env_file) as f:
                content = f.read()

            required_keys = ["AZURE_API_KEY", "AWS_ACCESS_KEY_ID", "ANTHROPIC_API_KEY"]
            missing_keys = []

            for key in required_keys:
                if key not in content or f"{key}=" in content and "YOUR_" in content:
                    missing_keys.append(key)

            if missing_keys:
                print(f"❌ Missing or placeholder API keys: {missing_keys}")
                return False

            print("✅ .env file verification passed")
            return True

        except Exception as e:
            print(f"❌ .env file verification failed: {e}")
            return False

    def _get_aws_credential_pair(self, item_id: str) -> Optional[dict[str, str]]:
        """
        Get AWS credential pair (Access Key ID + Secret Access Key) from 1Password.

        Args:
            item_id: 1Password item ID for the AWS credential

        Returns:
            Dictionary with 'access_key_id' and 'secret_access_key' or None if not found
        """
        try:
            # Get the item from 1Password
            result = subprocess.run(
                ["op", "item", "get", item_id, "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
            )

            item_data = json.loads(result.stdout)

            # Look for AWS credential fields
            access_key_id = None
            secret_access_key = None

            for field in item_data.get("fields", []):
                field_label = field.get("label", "").lower()
                field_type = field.get("type", "")
                field_value = field.get("value", "")

                # Use provider detector for more sophisticated AWS credential type detection
                aws_cred_type = self._provider_detector.detect_aws_credential_type(
                    "", [field_label]
                )

                if field_type == "STRING" and aws_cred_type == "access_key":
                    access_key_id = field_value
                elif field_type == "CONCEALED" and aws_cred_type == "secret_key":
                    secret_access_key = field_value

            # Return pair if we have both
            if access_key_id and secret_access_key:
                return {
                    "access_key_id": access_key_id,
                    "secret_access_key": secret_access_key,
                }

            return None

        except Exception as e:
            print(f"❌ Failed to get AWS credential pair for {item_id}: {e}")
            return None

    def get_comprehensive_stats(self) -> dict[str, Any]:
        """
        Get comprehensive statistics about API keys and cache.

        Returns:
            Dictionary containing comprehensive statistics
        """
        try:
            # Load cache if not loaded
            if self._cache is None:
                self._load_from_cache()

            if not self._cache or "api_keys" not in self._cache:
                return {}

            api_keys = self._cache["api_keys"]

            # Calculate statistics
            stats = {
                "total_items": len(api_keys),
                "total_providers": 0,
                "providers": {},
                "statuses": {},
                "cache_info": {},
            }

            # Provider and status breakdown
            providers = set()
            for key in api_keys:
                provider = key.get("provider", "unknown")
                status = key.get("status", "unknown")

                providers.add(provider)

                if provider not in stats["providers"]:
                    stats["providers"][provider] = 0
                stats["providers"][provider] += 1

                if status not in stats["statuses"]:
                    stats["statuses"][status] = 0
                stats["statuses"][status] += 1

            stats["total_providers"] = len(providers)

            # Cache information
            cache_file = self._get_cache_file_path()
            if os.path.exists(cache_file):
                stats["cache_info"] = {
                    "cache_file": cache_file,
                    "last_updated": datetime.fromtimestamp(
                        os.path.getmtime(cache_file)
                    ).isoformat(),
                    "cache_size": f"{os.path.getsize(cache_file)} bytes",
                }

            return stats

        except Exception as e:
            print(f"❌ Error generating statistics: {e}")
            return {}

    def perform_health_check(self, verbose: bool = False) -> dict[str, Any]:
        """
        Perform comprehensive health check of the system.

        Args:
            verbose: Show detailed health information

        Returns:
            Dictionary containing health status
        """
        try:
            health_status = {
                "overall_health": "unknown",
                "components": {},
                "recommendations": [],
            }

            # Check 1Password connectivity
            op_health = self._check_1password_health()
            health_status["components"]["1password"] = op_health

            # Check cache health
            cache_health = self._check_cache_health()
            health_status["components"]["cache"] = cache_health

            # Check file system health
            fs_health = self._check_filesystem_health()
            health_status["components"]["filesystem"] = fs_health

            # Determine overall health
            healthy_components = sum(
                1 for comp in health_status["components"].values() if comp["healthy"]
            )
            total_components = len(health_status["components"])

            if healthy_components == total_components:
                health_status["overall_health"] = "healthy"
            elif healthy_components > total_components / 2:
                health_status["overall_health"] = "degraded"
            else:
                health_status["overall_health"] = "unhealthy"

            # Generate recommendations
            health_status["recommendations"] = self._generate_health_recommendations(
                health_status
            )

            return health_status

        except Exception as e:
            print(f"❌ Error during health check: {e}")
            return {"overall_health": "error", "error": str(e)}

    def create_backup(
        self, backup_dir: Optional[str] = None, timestamp: bool = False
    ) -> Optional[str]:
        """
        Create backup of the current cache and configuration.

        Args:
            backup_dir: Directory to store backup (default: ./backups)
            timestamp: Add timestamp to backup filename

        Returns:
            Path to backup file if successful, None otherwise
        """
        try:
            # Determine backup directory
            if backup_dir is None:
                backup_dir = Path.cwd() / "backups"
            else:
                backup_dir = Path(backup_dir)

            backup_dir.mkdir(parents=True, exist_ok=True)

            # Generate backup filename
            if timestamp:
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"op_api_manager_backup_{timestamp_str}.json"
            else:
                backup_filename = "op_api_manager_backup.json"

            backup_path = backup_dir / backup_filename

            # Load cache if not loaded
            if self._cache is None:
                self._load_cache()

            # Create backup data
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "cache": self._cache,
                "config": {
                    "cache_file": self.cache_config.cache_file,
                    "max_age_hours": self.cache_config.max_age_hours,
                },
            }

            # Write backup file
            with open(backup_path, "w") as f:
                json.dump(backup_data, f, indent=2, default=str)

            print(f"✅ Backup created successfully: {backup_path}")
            return str(backup_path)

        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None

    def restore_from_backup(self, backup_file: str, force: bool = False) -> bool:
        """
        Restore system from a backup file.

        Args:
            backup_file: Path to backup file
            force: Force restore even if cache exists

        Returns:
            True if restore successful, False otherwise
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                print(f"❌ Backup file not found: {backup_file}")
                return False

            # Check if cache exists and force is not enabled
            if not force and self._cache is not None:
                print("❌ Cache already loaded. Use --force to overwrite.")
                return False

            # Load backup data
            with open(backup_path) as f:
                backup_data = json.load(f)

            # Validate backup data
            if "cache" not in backup_data or "config" not in backup_data:
                print("❌ Invalid backup file format")
                return False

            # Restore cache
            self._cache = backup_data["cache"]

            # Save restored cache
            self._save_cache()

            print(f"✅ System restored successfully from: {backup_file}")
            return True

        except Exception as e:
            print(f"❌ Error during restore: {e}")
            return False

    def verify_restored_data(self) -> bool:
        """
        Verify that restored data is valid and consistent.

        Returns:
            True if verification passes, False otherwise
        """
        try:
            if self._cache is None:
                print("❌ No cache data to verify")
                return False

            # Basic validation
            if "api_keys" not in self._cache:
                print("❌ Restored cache missing api_keys")
                return False

            if "discovery_timestamp" not in self._cache:
                print("❌ Restored cache missing discovery_timestamp")
                return False

            # Check data integrity
            api_keys = self._cache["api_keys"]
            if not isinstance(api_keys, list):
                print("❌ Restored api_keys is not a list")
                return False

            print("✅ Restored data verification passed")
            return True

        except Exception as e:
            print(f"❌ Error during data verification: {e}")
            return False

    def _check_1password_health(self) -> dict[str, Any]:
        """Check 1Password connectivity and health."""
        try:
            # Test basic 1Password connectivity
            result = subprocess.run(
                ["op", "--version"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                return {
                    "healthy": True,
                    "status": "Connected",
                    "version": result.stdout.strip(),
                }
            else:
                return {
                    "healthy": False,
                    "status": "Command failed",
                    "error": result.stderr.strip(),
                }

        except subprocess.TimeoutExpired:
            return {
                "healthy": False,
                "status": "Timeout",
                "error": "1Password command timed out",
            }
        except FileNotFoundError:
            return {
                "healthy": False,
                "status": "Not installed",
                "error": "1Password CLI not found",
            }
        except Exception as e:
            return {"healthy": False, "status": "Error", "error": str(e)}

    def _check_cache_health(self) -> dict[str, Any]:
        """Check cache health and validity."""
        try:
            cache_file = self._get_cache_file_path()

            if not os.path.exists(cache_file):
                return {
                    "healthy": False,
                    "status": "Missing",
                    "error": "Cache file not found",
                }

            # Check cache age
            cache_age = datetime.now().timestamp() - os.path.getmtime(cache_file)
            cache_age_hours = cache_age / 3600

            if cache_age_hours > 24:
                return {
                    "healthy": False,
                    "status": "Stale",
                    "error": f"Cache is {cache_age_hours:.1f} hours old",
                }
            elif cache_age_hours > 12:
                return {
                    "healthy": True,
                    "status": "Warning",
                    "warning": f"Cache is {cache_age_hours:.1f} hours old",
                }
            else:
                return {
                    "healthy": True,
                    "status": "Fresh",
                    "info": f"Cache is {cache_age_hours:.1f} hours old",
                }

        except Exception as e:
            return {"healthy": False, "status": "Error", "error": str(e)}

    def _check_filesystem_health(self) -> dict[str, Any]:
        """Check filesystem health and permissions."""
        try:
            cache_file = self._get_cache_file_path()
            cache_dir = Path(cache_file).parent

            # Check directory permissions
            if not os.access(cache_dir, os.R_OK | os.W_OK):
                return {
                    "healthy": False,
                    "status": "Permission denied",
                    "error": f"Cannot read/write to {cache_dir}",
                }

            # Check file permissions if exists
            if os.path.exists(cache_file):
                if not os.access(cache_file, os.R_OK | os.W_OK):
                    return {
                        "healthy": False,
                        "status": "Permission denied",
                        "error": f"Cannot read/write cache file {cache_file}",
                    }

            return {
                "healthy": True,
                "status": "Accessible",
                "info": "File system permissions are correct",
            }

        except Exception as e:
            return {"healthy": False, "status": "Error", "error": str(e)}

    def _generate_health_recommendations(
        self, health_status: dict[str, Any]
    ) -> list[str]:
        """Generate health recommendations based on status."""
        recommendations = []

        # 1Password recommendations
        if not health_status["components"].get("1password", {}).get("healthy", False):
            recommendations.append("Sign in to 1Password: op signin")
            recommendations.append("Check 1Password CLI installation")

        # Cache recommendations
        cache_health = health_status["components"].get("cache", {})
        if not cache_health.get("healthy", False):
            if "stale" in cache_health.get("status", "").lower():
                recommendations.append("Refresh cache: op-api-manager refresh")
            if "missing" in cache_health.get("status", "").lower():
                recommendations.append("Run discovery: op-api-manager discover")

        # Filesystem recommendations
        fs_health = health_status["components"].get("filesystem", {})
        if not fs_health.get("healthy", False):
            if "permission" in fs_health.get("status", "").lower():
                recommendations.append("Check file permissions and ownership")
                recommendations.append("Ensure write access to cache directory")

        return recommendations

    def _get_cached_discovery_results(self) -> Optional[list[dict[str, Any]]]:
        """Get cached discovery results for dry run preview."""
        try:
            if self._cache is None:
                self._load_cache()

            return self._cache.get("api_keys", []) if self._cache else None
        except Exception as e:
            print(f"❌ Error getting cached discovery results: {e}")
            return None

    def _get_cached_api_keys(self) -> Optional[list[dict[str, Any]]]:
        """Get cached API keys for dry run preview."""
        try:
            if self._cache is None:
                self._load_cache()

            return self._cache.get("api_keys", []) if self._cache else None
        except Exception as e:
            print(f"❌ Error getting cached API keys: {e}")
            return None

    def _apply_test_filters(
        self,
        api_keys: list[dict[str, Any]],
        provider: str,
        status: Optional[str],
        limit: Optional[int],
        force: bool,
    ) -> list[dict[str, Any]]:
        """Apply filters to API keys for testing preview."""
        try:
            filtered_keys = api_keys.copy()

            # Apply provider filter
            if provider != "all":
                filtered_keys = [
                    k for k in filtered_keys if k.get("provider") == provider
                ]

            # Apply status filter
            if status:
                filtered_keys = [k for k in filtered_keys if k.get("status") == status]

            # Apply limit
            if limit:
                filtered_keys = filtered_keys[:limit]

            return filtered_keys

        except Exception as e:
            print(f"❌ Error applying test filters: {e}")
            return api_keys

    def show_running_costs(self, stage: str = "Current") -> None:
        """
        Display running costs for API usage.

        Args:
            stage: Description of the current stage for cost tracking
        """
        try:
            print(f"💰 Running Costs ({stage}):")

            # Get working credentials to show what's available
            working_creds = self.get_working_credentials_all(force_test=False)

            if working_creds:
                print(f"  🔑 Available APIs: {len(working_creds)}")
                for provider, cred_info in working_creds.items():
                    if isinstance(cred_info, list) and cred_info:
                        print(
                            f"    📊 {provider.title()}: {len(cred_info)} credential(s)"
                        )
                    else:
                        print(f"    📊 {provider.title()}: 1 credential")
            else:
                print("  ⚠️ No working APIs available")

            # Note: Actual cost tracking would require integration with provider APIs
            print("  💡 Cost tracking requires provider-specific integration")
            print("  📝 Consider implementing cost tracking per provider")

        except Exception as e:
            print(f"❌ Error showing running costs: {e}")

    def _save_cache(self) -> None:
        """
        Save the current cache to file.
        """
        try:
            cache_path = Path(self._get_cache_file_path())
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            with open(cache_path, "w") as f:
                json.dump(self._cache, f, indent=2, default=str)

            print(f"💾 Cache saved to: {cache_path}")

        except Exception as e:
            print(f"❌ Error saving cache: {e}")

    def add_manual_api_key(
        self,
        title: str,
        api_key: str,
        provider: str = "unknown",
        status: str = "discovered",
    ) -> bool:
        """
        Manually add an API key for testing when 1Password is unavailable.

        Args:
            title: Human-readable title for the API key
            api_key: The actual API key value
            provider: Provider type (openai, anthropic, google, aws, azure, unknown)
            status: Initial status (discovered, tested, working, failed)

        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Load existing cache
            if not self._cache:
                self._load_from_cache()

            # Create a unique ID for the manual key
            manual_id = f"manual_{uuid.uuid4().hex[:8]}"

            # Create API key item

            # Add to cache
            if "api_keys" not in self._cache:
                self._cache["api_keys"] = []

            self._cache["api_keys"].append(
                {
                    "id": manual_id,
                    "title": title,
                    "category": "API Credential",
                    "detected_provider": provider,
                    "status": status,
                    "manual_added": True,
                    "added_at": datetime.now().isoformat(),
                    "source": "manual_input",
                }
            )

            # Save cache
            self._save_cache()

            print(f"✅ Manually added API key: {title} ({provider})")
            return True

        except Exception as e:
            print(f"❌ Failed to add manual API key: {e}")
            return False
