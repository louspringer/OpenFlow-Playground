"""
Data models for OP API Manager.

This module contains Pydantic models for representing API keys, credentials,
and discovery results.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ProviderType(str, Enum):
    """Supported API providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AWS = "aws"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    AI21 = "ai21"
    AZURE = "azure"
    UNKNOWN = "unknown"


class APIKeyStatus(str, Enum):
    """Status of an API key."""

    DISCOVERED = "discovered"
    TESTED = "tested"
    WORKING = "working"
    FAILED = "failed"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


class APIKeyItem(BaseModel):
    """Represents a discovered API key item from 1Password."""

    id: str = Field(..., description="1Password item ID")
    title: str = Field(..., description="Item title")
    category: str = Field(..., description="1Password category")
    guid: UUID = Field(default_factory=uuid4, description="Unique identifier")
    provider: Optional[ProviderType] = Field(None, description="Detected provider type")
    status: APIKeyStatus = Field(
        default=APIKeyStatus.DISCOVERED, description="Current status"
    )
    url: Optional[str] = Field(None, description="Associated URL")
    notes: Optional[str] = Field(None, description="Item notes")
    tags: List[str] = Field(default_factory=list, description="Item tags")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @field_validator("provider", mode="before")
    @classmethod
    def detect_provider(cls, v, info):
        """Auto-detect provider from title and other fields."""
        if isinstance(v, ProviderType):
            return v

        # Get title from the data if available
        title = ""
        if hasattr(info, "data") and info.data and "title" in info.data:
            title = info.data["title"].lower()

        # Provider detection logic
        if any(keyword in title for keyword in ["openai", "gpt", "chatgpt"]):
            return ProviderType.OPENAI
        elif any(keyword in title for keyword in ["claude", "anthropic"]):
            return ProviderType.ANTHROPIC
        elif any(keyword in title for keyword in ["google", "gemini"]):
            return ProviderType.GOOGLE
        elif any(keyword in title for keyword in ["aws", "amazon", "bedrock"]):
            return ProviderType.AWS
        elif any(keyword in title for keyword in ["huggingface", "hf"]):
            return ProviderType.HUGGINGFACE
        elif any(keyword in title for keyword in ["cohere"]):
            return ProviderType.COHERE
        elif any(keyword in title for keyword in ["ai21"]):
            return ProviderType.AI21
        elif any(keyword in title for keyword in ["azure"]):
            return ProviderType.AZURE
        else:
            return ProviderType.UNKNOWN

    @property
    def detected_provider(self) -> ProviderType:
        """Get the detected provider, computing it from title if not set."""
        if self.provider is not None:
            return self.provider

        # Compute provider from title
        title_lower = self.title.lower()
        if any(keyword in title_lower for keyword in ["openai", "gpt", "chatgpt"]):
            return ProviderType.OPENAI
        elif any(keyword in title_lower for keyword in ["claude", "anthropic"]):
            return ProviderType.ANTHROPIC
        elif any(keyword in title_lower for keyword in ["google", "gemini"]):
            return ProviderType.GOOGLE
        elif any(keyword in title_lower for keyword in ["aws", "amazon", "bedrock"]):
            return ProviderType.AWS
        elif any(keyword in title_lower for keyword in ["huggingface", "hf"]):
            return ProviderType.HUGGINGFACE
        elif any(keyword in title_lower for keyword in ["cohere"]):
            return ProviderType.COHERE
        elif any(keyword in title_lower for keyword in ["ai21"]):
            return ProviderType.AI21
        elif any(keyword in title_lower for keyword in ["azure"]):
            return ProviderType.AZURE
        else:
            return ProviderType.UNKNOWN


class CredentialPair(BaseModel):
    """Represents a pair of related credentials (e.g., AWS Access Key + Secret)."""

    primary: APIKeyItem = Field(..., description="Primary credential")
    secondary: Optional[APIKeyItem] = Field(None, description="Secondary credential")
    pair_type: str = Field(..., description="Type of credential pair")
    description: Optional[str] = Field(None, description="Description of the pair")

    @property
    def is_complete(self) -> bool:
        """Check if the credential pair is complete."""
        return self.secondary is not None


class DiscoveryResult(BaseModel):
    """Result of an API key discovery operation."""

    total_items: int = Field(..., description="Total items discovered")
    api_keys: List[APIKeyItem] = Field(..., description="Discovered API keys")
    credential_pairs: List[CredentialPair] = Field(
        ..., description="Organized credential pairs"
    )
    providers: Optional[Dict[ProviderType, int]] = Field(
        None, description="Count by provider"
    )
    status_summary: Optional[Dict[APIKeyStatus, int]] = Field(
        None, description="Count by status"
    )
    discovery_timestamp: str = Field(..., description="When discovery was performed")
    cache_file: Optional[str] = Field(None, description="Cache file location")

    @field_validator("providers", "status_summary", mode="before")
    @classmethod
    def compute_summaries(cls, v, info):
        """Compute summary statistics."""
        if v is not None:
            return v

        if not hasattr(info, "data") or "api_keys" not in info.data:
            return {}

        api_keys = info.data["api_keys"]

        if info.field_name == "providers":
            # Compute provider summary
            providers = {}
            for key in api_keys:
                providers[key.provider] = providers.get(key.provider, 0) + 1
            return providers

        if info.field_name == "status_summary":
            # Compute status summary
            status_summary = {}
            for key in api_keys:
                status_summary[key.status] = status_summary.get(key.status, 0) + 1
            return status_summary

        return {}

    def model_post_init(self, __context):
        """Post-initialization hook to compute summaries if not provided."""
        if self.providers is None:
            # Compute provider summary
            providers = {}
            for key in self.api_keys:
                detected_provider = key.detected_provider
                providers[detected_provider] = providers.get(detected_provider, 0) + 1
            self.providers = providers

        if self.status_summary is None:
            # Compute status summary
            status_summary = {}
            for key in self.api_keys:
                status_summary[key.status] = status_summary.get(key.status, 0) + 1
            self.status_summary = status_summary


class CacheConfig(BaseModel):
    """Configuration for caching operations."""

    enabled: bool = Field(default=True, description="Enable caching")
    cache_file: str = Field(
        default="api_discovery_cache.json", description="Cache file path"
    )
    max_age_hours: int = Field(default=24, description="Maximum cache age in hours")
    auto_refresh: bool = Field(default=False, description="Auto-refresh expired cache")
