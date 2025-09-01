"""
Cache Management Models

This module defines the data models for cache management operations,
separate from API key concerns.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class CacheStatus(str, Enum):
    """Status of cache operations."""

    VALID = "valid"
    CORRUPTED = "corrupted"
    EXPIRED = "expired"
    MISSING = "missing"
    STALE = "stale"


class CacheFormat(str, Enum):
    """Supported cache formats."""

    JSON = "json"
    YAML = "yaml"
    BINARY = "binary"
    SQLITE = "sqlite"


class CacheMetadata(BaseModel):
    """Metadata about a cache entry."""

    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cached value")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    size_bytes: int = Field(0, description="Size in bytes")
    checksum: Optional[str] = Field(None, description="Data integrity checksum")
    version: str = Field("1.0", description="Cache format version")


class CacheConfig(BaseModel):
    """Configuration for cache operations."""

    enabled: bool = Field(default=True, description="Enable caching")
    cache_dir: Path = Field(default=Path.cwd(), description="Cache directory")
    max_size_mb: int = Field(default=100, description="Maximum cache size in MB")
    ttl_hours: int = Field(default=24, description="Time to live in hours")
    format: CacheFormat = Field(default=CacheFormat.JSON, description="Cache format")
    compression: bool = Field(default=False, description="Enable compression")
    encryption: bool = Field(default=False, description="Enable encryption")
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    max_backups: int = Field(default=5, description="Maximum number of backups")


class CacheStats(BaseModel):
    """Statistics about cache performance."""

    total_entries: int = Field(0, description="Total cache entries")
    total_size_bytes: int = Field(0, description="Total cache size in bytes")
    hit_count: int = Field(0, description="Cache hit count")
    miss_count: int = Field(0, description="Cache miss count")
    hit_rate: float = Field(0.0, description="Cache hit rate (0.0 to 1.0)")
    avg_load_time_ms: float = Field(0.0, description="Average load time in milliseconds")
    avg_save_time_ms: float = Field(0.0, description="Average save time in milliseconds")
    last_cleanup: Optional[datetime] = Field(None, description="Last cleanup timestamp")
    corruption_count: int = Field(0, description="Number of corruption events")


class CacheOperation(BaseModel):
    """Result of a cache operation."""

    success: bool = Field(..., description="Whether operation succeeded")
    operation: str = Field(..., description="Type of operation performed")
    cache_key: str = Field(..., description="Cache key involved")
    timestamp: datetime = Field(default_factory=datetime.now, description="Operation timestamp")
    duration_ms: float = Field(0.0, description="Operation duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CacheHealth(BaseModel):
    """Health status of the cache system."""

    status: CacheStatus = Field(..., description="Overall cache health")
    last_check: datetime = Field(default_factory=datetime.now, description="Last health check")
    issues: list[str] = Field(default_factory=list, description="List of identified issues")
    recommendations: list[str] = Field(default_factory=list, description="Recommendations for improvement")
    performance_score: float = Field(0.0, description="Performance score (0.0 to 1.0)")
    integrity_score: float = Field(0.0, description="Data integrity score (0.0 to 1.0)")
    maintenance_needed: bool = Field(False, description="Whether maintenance is needed")
