"""
OP API Manager - Intelligent API key discovery and management for 1Password.

A Python package for discovering, organizing, and managing API keys stored in 1Password.
Provides intelligent credential pairing, GUID assignment, and comprehensive CLI tools.
"""

__version__ = "0.1.0"
__author__ = "OpenFlow Team"
__email__ = "team@openflow.dev"

from .cli import main
from .core import OnePasswordAPIKeyManager
from .models import (
    APIKeyItem,
    APIKeyStatus,
    CacheConfig,
    CredentialPair,
    DiscoveryResult,
    ProviderType,
)

__all__ = [
    "OnePasswordAPIKeyManager",
    "APIKeyItem",
    "CredentialPair",
    "ProviderType",
    "APIKeyStatus",
    "DiscoveryResult",
    "CacheConfig",
    "main",
]
