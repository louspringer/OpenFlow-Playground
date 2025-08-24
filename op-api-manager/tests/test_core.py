"""
Tests for the core module.
"""

from unittest.mock import Mock, patch

import pytest

from op_api_manager.core import OnePasswordAPIKeyManager
from op_api_manager.models import CacheConfig, ProviderType


class TestOnePasswordAPIKeyManager:
    """Test OnePasswordAPIKeyManager class."""

    def test_init_with_default_config(self):
        """Test initialization with default cache config."""
        manager = OnePasswordAPIKeyManager()
        assert isinstance(manager.cache_config, CacheConfig)
        assert manager.cache_config.enabled is True

    def test_init_with_custom_config(self):
        """Test initialization with custom cache config."""
        custom_config = CacheConfig(
            enabled=False, cache_file="custom.json", max_age_hours=12
        )
        manager = OnePasswordAPIKeyManager(custom_config)
        assert manager.cache_config == custom_config

    @patch("op_api_manager.core.subprocess.run")
    def test_discover_items_success(self, mock_run):
        """Test successful item discovery."""
        # Mock successful subprocess run
        mock_result = Mock()
        mock_result.stdout = '[{"id": "test1", "title": "Test Item"}]'
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        manager = OnePasswordAPIKeyManager()
        items = manager._discover_items()

        assert len(items) == 1
        assert items[0]["id"] == "test1"
        assert items[0]["title"] == "Test Item"

    @patch("op_api_manager.core.subprocess.run")
    def test_discover_items_failure(self, mock_run):
        """Test item discovery failure."""
        # Mock failed subprocess run
        mock_run.side_effect = Exception("Command failed")

        manager = OnePasswordAPIKeyManager()

        with pytest.raises(Exception, match="Command failed"):
            manager._discover_items()

    def test_is_api_key_item(self):
        """Test API key item detection."""
        manager = OnePasswordAPIKeyManager()

        # Test API key indicators
        api_key_item = {
            "title": "OpenAI API Key",
            "category": "login",
            "tags": ["api", "key"],
        }
        assert manager._is_api_key_item(api_key_item) is True

        # Test non-API key item
        regular_item = {
            "title": "Regular Password",
            "category": "login",
            "tags": ["password"],
        }
        assert manager._is_api_key_item(regular_item) is False

        # Test with API key in title
        api_title_item = {
            "title": "My API Token for Service",
            "category": "secure note",
            "tags": [],
        }
        assert manager._is_api_key_item(api_title_item) is True

    def test_determine_pair_type(self):
        """Test credential pair type determination."""
        manager = OnePasswordAPIKeyManager()

        # Test AWS pair
        primary = Mock()
        primary.provider = ProviderType.AWS
        secondary = Mock()

        pair_type = manager._determine_pair_type(primary, secondary)
        assert pair_type == "aws_access_secret"

        # Test Google pair
        primary.provider = ProviderType.GOOGLE
        pair_type = manager._determine_pair_type(primary, secondary)
        assert pair_type == "google_credentials"

        # Test single credential
        pair_type = manager._determine_pair_type(primary, None)
        assert pair_type == "single"

        # Test generic pair
        primary.provider = ProviderType.OPENAI
        pair_type = manager._determine_pair_type(primary, secondary)
        assert pair_type == "generic_pair"

    def test_cache_validation(self):
        """Test cache validation logic."""
        manager = OnePasswordAPIKeyManager()

        # Test no cache
        assert manager._is_cache_valid() is False

        # Test with cache but no discovery time
        manager._cache = {"test": "data"}
        assert manager._is_cache_valid() is False

        # Test with valid cache
        from datetime import datetime, timedelta

        manager._last_discovery = datetime.now()
        assert manager._is_cache_valid() is True

        # Test with expired cache
        manager._last_discovery = datetime.now() - timedelta(hours=25)
        assert manager._is_cache_valid() is False
