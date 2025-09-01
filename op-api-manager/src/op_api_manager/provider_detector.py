"""
Provider Detection and Configuration Registry for OP API Manager.

This module contains the ProviderDetector class that handles intelligent
detection of API providers and manages provider-specific configuration
including required environment variables and credential attributes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .models import ProviderType


class CredentialAttributeType(Enum):
    """Types of credential attributes that can be required."""

    STRING = "string"
    CONCEALED = "concealed"
    URL = "url"
    PROJECT_ID = "project_id"
    REGION = "region"
    ORGANIZATION = "organization"


@dataclass
class CredentialAttribute:
    """Represents a required credential attribute for a provider."""

    name: str
    header_name: str
    prefix: str
    description: str


@dataclass
class ProviderPattern:
    """Represents a provider detection pattern."""

    keywords: list[str]
    confidence: float
    service_type: str


@dataclass
class ProviderConfig:
    """Complete configuration for a provider including detection and credential requirements."""

    name: str
    patterns: list[ProviderPattern]
    endpoint: str
    credential_attributes: list[CredentialAttribute]
    env_vars: list[str]
    models: list[str]
    description: str = ""
    service_type: str = "direct_api"

    def get_env_vars(self) -> list[str]:
        """Get list of environment variable names for this provider."""
        return [attr.env_var for attr in self.credential_attributes]

    def get_required_attributes(self) -> list[CredentialAttribute]:
        """Get list of required credential attributes."""
        return [attr for attr in self.credential_attributes if attr.required]


class ProviderDetector:
    """
    Intelligent provider detection and configuration registry for API keys and credentials.

    This class centralizes all provider detection logic and provides
    consistent, extensible provider identification and configuration across the system.
    """

    def __init__(self):
        """Initialize the provider detector with predefined provider configurations."""
        self._provider_configs = self._build_provider_configs()
        self._patterns = [pattern for config in self._provider_configs.values() for pattern in config.patterns]

    def _build_provider_configs(self) -> dict[str, ProviderConfig]:
        """Build provider configurations with proper service modeling."""
        return {
            # Direct API providers
            "openai": ProviderConfig(
                name="OpenAI",
                patterns=[
                    ProviderPattern(
                        keywords=["openai", "gpt", "chatgpt"],
                        confidence=0.9,
                        service_type="direct_api",
                    )
                ],
                endpoint="https://api.openai.com/v1/chat/completions",
                credential_attributes=[CredentialAttribute("api_key", "Bearer", "sk-", "API key starting with sk-")],
                env_vars=["OPENAI_API_KEY"],
                models=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
            ),
            "anthropic": ProviderConfig(
                name="Anthropic",
                patterns=[
                    ProviderPattern(
                        keywords=["anthropic", "claude"],
                        confidence=0.9,
                        service_type="direct_api",
                    )
                ],
                endpoint="https://api.anthropic.com/v1/messages",
                credential_attributes=[
                    CredentialAttribute(
                        "api_key",
                        "x-api-key",
                        "sk-ant-",
                        "API key starting with sk-ant-",
                    )
                ],
                env_vars=["ANTHROPIC_API_KEY"],
                models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            ),
            "google": ProviderConfig(
                name="Google AI",
                patterns=[
                    ProviderPattern(
                        keywords=["google", "gemini", "palm"],
                        confidence=0.9,
                        service_type="direct_api",
                    )
                ],
                endpoint="https://generativelanguage.googleapis.com/v1beta/models",
                credential_attributes=[CredentialAttribute("api_key", "Authorization", "AIza", "API key starting with AIza")],
                env_vars=["GOOGLE_API_KEY"],
                models=["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            ),
            # Gateway/Proxy services
            "openrouter": ProviderConfig(
                name="OpenRouter",
                patterns=[
                    ProviderPattern(
                        keywords=["openrouter", "router", "gateway"],
                        confidence=0.8,
                        service_type="gateway_service",
                    )
                ],
                endpoint="https://openrouter.ai/api/v1/chat/completions",
                credential_attributes=[
                    CredentialAttribute(
                        "api_key",
                        "Authorization",
                        "Bearer",
                        "Bearer token for OpenRouter",
                    )
                ],
                env_vars=["OPENROUTER_API_KEY"],
                models=[
                    "openai/gpt-4o",
                    "anthropic/claude-3-sonnet",
                    "meta-llama/llama-3.1-70b",
                ],
                description="Gateway service that routes to multiple providers (OpenAI, Anthropic, Meta, etc.)",
            ),
            # Specialized providers
            "huggingface": ProviderConfig(
                name="Hugging Face",
                patterns=[
                    ProviderPattern(
                        keywords=["huggingface", "hugging_face", "hf_"],
                        confidence=0.9,
                        service_type="model_hosting",
                    )
                ],
                endpoint="https://api-inference.huggingface.co/models",
                credential_attributes=[
                    CredentialAttribute(
                        "api_key",
                        "Authorization",
                        "Bearer",
                        "Bearer token for HuggingFace",
                    )
                ],
                env_vars=["HUGGINGFACE_API_KEY"],
                models=["meta-llama/Llama-2-7b-chat-hf", "microsoft/DialoGPT-medium"],
                description="Model hosting platform with its own API format and models",
            ),
            "aws_bedrock": ProviderConfig(
                name="AWS Bedrock",
                patterns=[
                    ProviderPattern(
                        keywords=["bedrock", "aws", "amazon"],
                        confidence=0.8,
                        service_type="cloud_service",
                    )
                ],
                endpoint="bedrock-runtime",
                credential_attributes=[
                    CredentialAttribute(
                        "access_key_id",
                        "AWS_ACCESS_KEY_ID",
                        "AKIA",
                        "AWS Access Key ID",
                    ),
                    CredentialAttribute(
                        "secret_access_key",
                        "AWS_SECRET_ACCESS_KEY",
                        "",
                        "AWS Secret Access Key",
                    ),
                ],
                env_vars=["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
                models=["anthropic.claude-3-sonnet", "amazon.titan-text-express"],
                description="AWS managed service with different authentication and endpoint structure",
            ),
            "azure_openai": ProviderConfig(
                name="Azure OpenAI",
                patterns=[
                    ProviderPattern(
                        keywords=["azure", "openai", "gpt"],
                        confidence=0.8,
                        service_type="cloud_service",
                    )
                ],
                endpoint="https://{resource}.openai.azure.com/openai/deployments/{deployment}",
                credential_attributes=[
                    CredentialAttribute("api_key", "api-key", "", "Azure OpenAI API key"),
                    CredentialAttribute("endpoint", "AZURE_OPENAI_ENDPOINT", "", "Azure OpenAI endpoint"),
                ],
                env_vars=["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"],
                models=["gpt-4", "gpt-35-turbo"],
                description="Azure-hosted OpenAI models with different endpoint structure",
            ),
            "cohere": ProviderConfig(
                name="Cohere",
                patterns=[
                    ProviderPattern(
                        keywords=["cohere", "command"],
                        confidence=0.9,
                        service_type="direct_api",
                    )
                ],
                endpoint="https://api.cohere.ai/v1/chat",
                credential_attributes=[CredentialAttribute("api_key", "Authorization", "Bearer", "Bearer token for Cohere")],
                env_vars=["COHERE_API_KEY"],
                models=["command-r-plus", "command-r", "command"],
            ),
            "mistral": ProviderConfig(
                name="Mistral AI",
                patterns=[
                    ProviderPattern(
                        keywords=["mistral", "mixtral"],
                        confidence=0.9,
                        service_type="direct_api",
                    )
                ],
                endpoint="https://api.mistral.ai/v1/chat/completions",
                credential_attributes=[CredentialAttribute("api_key", "Authorization", "Bearer", "Bearer token for Mistral")],
                env_vars=["MISTRAL_API_KEY"],
                models=[
                    "mistral-large-latest",
                    "mixtral-8x7b-instruct",
                    "mistral-7b-instruct",
                ],
            ),
        }

    def get_provider_config(self, provider: ProviderType) -> Optional[ProviderConfig]:
        """
        Get configuration for a specific provider.

        Args:
            provider: Provider type to get configuration for

        Returns:
            ProviderConfig if found, None otherwise
        """
        return self._provider_configs.get(provider)

    def get_all_provider_configs(self) -> dict[ProviderType, ProviderConfig]:
        """
        Get all provider configurations.

        Returns:
            Dictionary of all provider configurations
        """
        return self._provider_configs.copy()

    def register_provider(self, config: ProviderConfig) -> None:
        """
        Register a new provider configuration.

        Args:
            config: Provider configuration to register
        """
        self._provider_configs[config.provider] = config
        # Update patterns list
        self._patterns = [config.detection_patterns for config in self._provider_configs.values()]

    def detect_from_title(self, title: str) -> ProviderType:
        """
        Detect provider from item title.

        Args:
            title: Item title to analyze

        Returns:
            Detected provider type
        """
        if not title:
            return ProviderType.UNKNOWN

        title_clean = title.lower().strip()

        # Check each pattern in priority order
        for pattern in self._patterns:
            if self._matches_pattern(title_clean, pattern):
                return pattern.provider

        return ProviderType.UNKNOWN

    def detect_from_metadata(
        self,
        title: str = "",
        url: str = "",
        notes: str = "",
        tags: list[str] = None,
        category: str = "",
    ) -> ProviderType:
        """
        Detect provider from comprehensive metadata.

        Args:
            title: Item title
            url: Associated URL
            notes: Item notes
            tags: Item tags
            category: Item category

        Returns:
            Detected provider type
        """
        # Combine all text for analysis
        all_text = (
            " ".join(
                [
                    title or "",
                    url or "",
                    notes or "",
                    " ".join(tags or []),
                    category or "",
                ]
            )
            .lower()
            .strip()
        )

        if not all_text:
            return ProviderType.UNKNOWN

        # Check each pattern in priority order
        for pattern in self._patterns:
            if self._matches_pattern(all_text, pattern):
                return pattern.provider

        return ProviderType.UNKNOWN

    def detect_from_api_key_format(self, api_key: str) -> ProviderType:
        """
        Detect provider from API key format/structure.

        Args:
            api_key: The actual API key string

        Returns:
            Detected provider type
        """
        if not api_key:
            return ProviderType.UNKNOWN

        # Check format-specific patterns
        for pattern in self._patterns:
            for regex_pattern in pattern.compiled_patterns:
                if regex_pattern.match(api_key):
                    return pattern.provider

        return ProviderType.UNKNOWN

    def get_provider_keywords(self, provider: ProviderType) -> list[str]:
        """
        Get keywords associated with a provider.

        Args:
            provider: Provider type

        Returns:
            List of keywords for the provider
        """
        config = self.get_provider_config(provider)
        if config:
            return [keyword for pattern in config.patterns for keyword in pattern.keywords]
        return []

    def get_provider_env_vars(self, provider: ProviderType) -> list[str]:
        """
        Get environment variable names required for a provider.

        Args:
            provider: Provider type

        Returns:
            List of environment variable names
        """
        config = self.get_provider_config(provider)
        if config:
            return config.get_env_vars()
        return []

    def get_provider_credential_attributes(self, provider: ProviderType) -> list[CredentialAttribute]:
        """
        Get credential attributes required for a provider.

        Args:
            provider: Provider type

        Returns:
            List of credential attributes
        """
        config = self.get_provider_config(provider)
        if config:
            return config.credential_attributes.copy()
        return []

    def get_confidence_score(self, title: str, provider: ProviderType) -> float:
        """
        Get confidence score for provider detection.

        Args:
            title: Item title
            provider: Provider to check against

        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not title:
            return 0.0

        title_clean = title.lower().strip()

        # Find the pattern for this provider
        config = self.get_provider_config(provider)
        if not config:
            return 0.0

        pattern = config.patterns[0]  # Use first pattern for now

        # Calculate score based on matches
        score = 0.0
        max_score = len(pattern.keywords) + len(pattern.patterns)

        # Check keyword matches
        for keyword in pattern.keywords:
            if keyword in title_clean:
                score += 1.0

        # Check pattern matches
        for regex_pattern in pattern.compiled_patterns:
            if regex_pattern.search(title_clean):
                score += 1.0

        return min(score / max_score, 1.0) if max_score > 0 else 0.0

    def _matches_pattern(self, text: str, pattern: ProviderPattern) -> bool:
        """
        Check if text matches a provider pattern.

        Args:
            text: Text to check
            pattern: Provider pattern to match against

        Returns:
            True if text matches the pattern
        """
        # Check keywords
        for keyword in pattern.keywords:
            if keyword in text:
                return True

        # Check regex patterns
        for regex_pattern in pattern.compiled_patterns:
            if regex_pattern.search(text):
                return True

        return False

    def detect_aws_credential_type(self, title: str, field_labels: list[str] = None) -> str:
        """
        Detect specific AWS credential type.

        Args:
            title: Item title
            field_labels: Field labels from the credential

        Returns:
            AWS credential type ('access_key', 'secret_key', 'session_token', 'unknown')
        """
        title_lower = title.lower()
        all_labels = " ".join(field_labels or []).lower()
        combined_text = f"{title_lower} {all_labels}"

        if any(term in combined_text for term in ["access key", "access_key", "akid"]):
            return "access_key"
        elif any(term in combined_text for term in ["secret", "secret key", "secret_key"]):
            return "secret_key"
        elif any(term in combined_text for term in ["session", "token", "session_token"]):
            return "session_token"
        else:
            return "unknown"

    def suggest_provider_from_partial_match(self, text: str, min_confidence: float = 0.3) -> list[ProviderType]:
        """
        Suggest possible providers based on partial matches.

        Args:
            text: Text to analyze
            min_confidence: Minimum confidence threshold

        Returns:
            List of suggested providers sorted by confidence
        """
        suggestions = []

        for provider in self._provider_configs.keys():
            confidence = self.get_confidence_score(text, provider)
            if confidence >= min_confidence:
                suggestions.append((provider, confidence))

        # Sort by confidence (highest first)
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [provider for provider, _ in suggestions]
