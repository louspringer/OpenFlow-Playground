"""
Tests for the models module.
"""

from uuid import UUID

from op_api_manager.models import (
    APIKeyItem,
    APIKeyStatus,
    CacheConfig,
    CredentialPair,
    DiscoveryResult,
    ProviderType,
)


class TestProviderType:
    """Test ProviderType enum."""

    def test_provider_types(self):
        """Test that all expected provider types exist."""
        expected_providers = [
            "openai",
            "anthropic",
            "google",
            "aws",
            "huggingface",
            "cohere",
            "ai21",
            "azure",
            "unknown",
        ]

        for provider in expected_providers:
            assert ProviderType(provider) in ProviderType

    def test_provider_detection(self):
        """Test provider detection logic."""
        # Test OpenAI detection
        item = APIKeyItem(
            id="test-id", title="OpenAI API Key", category="login", provider="openai"
        )
        assert item.provider == ProviderType.OPENAI

        # Test Anthropic detection
        item = APIKeyItem(
            id="test-id", title="Claude API Key", category="login", provider="anthropic"
        )
        assert item.provider == ProviderType.ANTHROPIC


class TestAPIKeyStatus:
    """Test APIKeyStatus enum."""

    def test_status_types(self):
        """Test that all expected status types exist."""
        expected_statuses = [
            "discovered",
            "tested",
            "working",
            "failed",
            "expired",
            "unknown",
        ]

        for status in expected_statuses:
            assert APIKeyStatus(status) in APIKeyStatus


class TestAPIKeyItem:
    """Test APIKeyItem model."""

    def test_create_api_key_item(self):
        """Test creating an APIKeyItem."""
        item = APIKeyItem(
            id="test-id",
            title="Test API Key",
            category="login",
            provider=ProviderType.OPENAI,
        )

        assert item.id == "test-id"
        assert item.title == "Test API Key"
        assert item.category == "login"
        assert item.provider == ProviderType.OPENAI
        assert item.status == APIKeyStatus.DISCOVERED
        assert isinstance(item.guid, UUID)

    def test_provider_auto_detection(self):
        """Test automatic provider detection from title."""
        # OpenAI detection
        item = APIKeyItem(id="test-id", title="OpenAI GPT API Key", category="login")
        assert item.detected_provider == ProviderType.OPENAI

        # AWS detection
        item = APIKeyItem(id="test-id", title="AWS Access Key ID", category="login")
        assert item.detected_provider == ProviderType.AWS

        # Unknown provider
        item = APIKeyItem(id="test-id", title="Some Random Item", category="login")
        assert item.detected_provider == ProviderType.UNKNOWN


class TestCredentialPair:
    """Test CredentialPair model."""

    def test_create_credential_pair(self):
        """Test creating a CredentialPair."""
        primary = APIKeyItem(
            id="primary-id",
            title="Primary Key",
            category="login",
            provider=ProviderType.AWS,
        )

        secondary = APIKeyItem(
            id="secondary-id",
            title="Secondary Key",
            category="login",
            provider=ProviderType.AWS,
        )

        pair = CredentialPair(
            primary=primary,
            secondary=secondary,
            pair_type="aws_access_secret",
            description="AWS credentials",
        )

        assert pair.primary == primary
        assert pair.secondary == secondary
        assert pair.pair_type == "aws_access_secret"
        assert pair.description == "AWS credentials"
        assert pair.is_complete is True

    def test_incomplete_pair(self):
        """Test creating an incomplete credential pair."""
        primary = APIKeyItem(
            id="primary-id",
            title="Primary Key",
            category="login",
            provider=ProviderType.OPENAI,
        )

        pair = CredentialPair(
            primary=primary,
            secondary=None,
            pair_type="single",
            description="Single credential",
        )

        assert pair.primary == primary
        assert pair.secondary is None
        assert pair.is_complete is False


class TestDiscoveryResult:
    """Test DiscoveryResult model."""

    def test_create_discovery_result(self):
        """Test creating a DiscoveryResult."""
        api_keys = [
            APIKeyItem(
                id="key1", title="Key 1", category="login", provider=ProviderType.OPENAI
            ),
            APIKeyItem(
                id="key2",
                title="Key 2",
                category="login",
                provider=ProviderType.ANTHROPIC,
            ),
        ]

        credential_pairs = [
            CredentialPair(
                primary=api_keys[0],
                secondary=None,
                pair_type="single",
                description="Single credential",
            )
        ]

        result = DiscoveryResult(
            total_items=100,
            api_keys=api_keys,
            credential_pairs=credential_pairs,
            discovery_timestamp="2025-01-20T10:30:00",
        )

        assert result.total_items == 100
        assert len(result.api_keys) == 2
        assert len(result.credential_pairs) == 1
        assert result.discovery_timestamp == "2025-01-20T10:30:00"

        # Test computed summaries
        assert result.providers[ProviderType.OPENAI] == 1
        assert result.providers[ProviderType.ANTHROPIC] == 1
        assert result.status_summary[APIKeyStatus.DISCOVERED] == 2


class TestCacheConfig:
    """Test CacheConfig model."""

    def test_default_cache_config(self):
        """Test default cache configuration."""
        config = CacheConfig()

        assert config.enabled is True
        assert config.cache_file == "api_discovery_cache.json"
        assert config.max_age_hours == 24
        assert config.auto_refresh is False

    def test_custom_cache_config(self):
        """Test custom cache configuration."""
        config = CacheConfig(
            enabled=False,
            cache_file="custom_cache.json",
            max_age_hours=12,
            auto_refresh=True,
        )

        assert config.enabled is False
        assert config.cache_file == "custom_cache.json"
        assert config.max_age_hours == 12
        assert config.auto_refresh is True
