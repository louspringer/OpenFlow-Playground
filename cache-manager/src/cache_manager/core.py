"""
Cache Manager Core

This module provides the core cache management functionality,
separate from API key concerns.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .models import (
    CacheConfig,
    CacheFormat,
    CacheHealth,
    CacheMetadata,
    CacheOperation,
    CacheStats,
    CacheStatus,
)


class CacheManager:
    """
    Core cache management functionality.

    This class handles all cache operations including:
    - Loading and saving cache data
    - Cache validation and repair
    - Performance monitoring
    - Health checks
    """

    def __init__(self, config: Optional[CacheConfig] = None):
        """Initialize the cache manager."""
        self.config = config or CacheConfig()
        self._cache_data: dict[str, Any] = {}
        self._metadata: dict[str, CacheMetadata] = {}
        self._stats = CacheStats()
        self._last_operation = datetime.now()

        # Ensure cache directory exists
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)

    def load_cache(self, cache_key: str, cache_file: Optional[Path] = None) -> Any:
        """
        Load data from cache.

        Args:
            cache_key: Key to load
            cache_file: Optional specific cache file path

        Returns:
            Cached data or None if not found/expired
        """
        start_time = time.time()

        try:
            # Check in-memory cache first
            if cache_key in self._cache_data:
                self._stats.hit_count += 1
                self._update_metadata(cache_key, "load")
                return self._cache_data[cache_key]

            self._stats.miss_count += 1

            # Load from file
            file_path = cache_file or self._get_cache_file_path(cache_key)
            if not file_path.exists():
                return None

            # Load based on format
            data = self._load_from_file(file_path)
            if data is None:
                return None

            # Validate cache entry
            if not self._validate_cache_entry(cache_key, data):
                return None

            # Store in memory
            self._cache_data[cache_key] = data
            self._update_metadata(cache_key, "load")

            # Update stats
            duration_ms = (time.time() - start_time) * 1000
            self._stats.avg_load_time_ms = (self._stats.avg_load_time_ms + duration_ms) / 2

            return data

        except Exception as e:
            self._record_operation(cache_key, "load", False, str(e))
            return None

    def save_cache(self, cache_key: str, data: Any, cache_file: Optional[Path] = None) -> bool:
        """
        Save data to cache.

        Args:
            cache_key: Key to save
            data: Data to cache
            cache_file: Optional specific cache file path

        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()

        try:
            # Store in memory
            self._cache_data[cache_key] = data

            # Save to file
            file_path = cache_file or self._get_cache_file_path(cache_key)
            success = self._save_to_file(file_path, data)

            if success:
                self._update_metadata(cache_key, "save")
                self._stats.total_entries = len(self._cache_data)

                # Update stats
                duration_ms = (time.time() - start_time) * 1000
                self._stats.avg_save_time_ms = (self._stats.avg_save_time_ms + duration_ms) / 2

                self._record_operation(cache_key, "save", True)
                return True
            self._record_operation(cache_key, "save", False, "File save failed")
            return False

        except Exception as e:
            self._record_operation(cache_key, "save", False, str(e))
            return False

    def validate_cache(self, cache_key: str) -> CacheHealth:
        """
        Validate cache integrity and health.

        Args:
            cache_key: Key to validate

        Returns:
            Cache health status
        """
        issues = []
        recommendations = []

        # Check if cache exists
        if cache_key not in self._cache_data:
            issues.append(f"Cache key '{cache_key}' not found in memory")
            recommendations.append("Load cache data first")
            return CacheHealth(
                status=CacheStatus.MISSING,
                issues=issues,
                recommendations=recommendations,
            )

        # Check file existence
        file_path = self._get_cache_file_path(cache_key)
        if not file_path.exists():
            issues.append(f"Cache file not found: {file_path}")
            recommendations.append("Check file permissions and path")
            return CacheHealth(
                status=CacheStatus.MISSING,
                issues=issues,
                recommendations=recommendations,
            )

        # Check file integrity
        try:
            with open(file_path) as f:
                if self.config.format == CacheFormat.JSON:
                    json.load(f)
                elif self.config.format == CacheFormat.YAML:
                    yaml.safe_load(f)
        except Exception as e:
            issues.append(f"Cache file corrupted: {e}")
            recommendations.append("Repair or regenerate cache")
            return CacheHealth(
                status=CacheStatus.CORRUPTED,
                issues=issues,
                recommendations=recommendations,
            )

        # Check expiration
        metadata = self._metadata.get(cache_key)
        if metadata and metadata.expires_at:
            if datetime.now() > metadata.expires_at:
                issues.append("Cache entry expired")
                recommendations.append("Refresh cache data")
                return CacheHealth(
                    status=CacheStatus.EXPIRED,
                    issues=issues,
                    recommendations=recommendations,
                )

        # Check performance
        performance_score = 1.0
        if self._stats.avg_load_time_ms > 1000:  # > 1 second
            performance_score = 0.5
            issues.append("Cache load performance degraded")
            recommendations.append("Consider cache optimization")

        # Check integrity
        integrity_score = 1.0
        if self._stats.corruption_count > 0:
            integrity_score = 0.3
            issues.append("Cache corruption detected")
            recommendations.append("Investigate corruption source")

        return CacheHealth(
            status=CacheStatus.VALID,
            issues=issues,
            recommendations=recommendations,
            performance_score=performance_score,
            integrity_score=integrity_score,
            maintenance_needed=len(issues) > 0,
        )

    def repair_cache(self, cache_key: str) -> bool:
        """
        Attempt to repair corrupted cache.

        Args:
            cache_key: Key to repair

        Returns:
            True if repair successful, False otherwise
        """
        try:
            # Remove corrupted entry from memory
            if cache_key in self._cache_data:
                del self._cache_data[cache_key]

            # Try to reload from file
            file_path = self._get_cache_file_path(cache_key)
            if file_path.exists():
                # Create backup
                backup_path = file_path.with_suffix(".backup")
                file_path.rename(backup_path)

                # Try to repair
                try:
                    with open(backup_path) as f:
                        if self.config.format == CacheFormat.JSON:
                            data = json.load(f)
                        elif self.config.format == CacheFormat.YAML:
                            data = yaml.safe_load(f)
                        else:
                            return False

                    # Save repaired data
                    success = self._save_to_file(file_path, data)
                    if success:
                        self._cache_data[cache_key] = data
                        self._record_operation(cache_key, "repair", True)
                        return True

                except Exception:
                    # Restore backup if repair failed
                    backup_path.rename(file_path)
                    return False

            return False

        except Exception as e:
            self._record_operation(cache_key, "repair", False, str(e))
            return False

    def get_stats(self) -> CacheStats:
        """Get cache performance statistics."""
        # Update hit rate
        total_requests = self._stats.hit_count + self._stats.miss_count
        if total_requests > 0:
            self._stats.hit_rate = self._stats.hit_count / total_requests

        # Update total size
        total_size = 0
        for key, data in self._cache_data.items():
            try:
                total_size += len(str(data).encode("utf-8"))
            except Exception:
                pass
        self._stats.total_size_bytes = total_size

        return self._stats

    def clear_cache(self, cache_key: Optional[str] = None) -> bool:
        """
        Clear cache data.

        Args:
            cache_key: Specific key to clear, or None to clear all

        Returns:
            True if successful, False otherwise
        """
        try:
            if cache_key:
                # Clear specific key
                if cache_key in self._cache_data:
                    del self._cache_data[cache_key]
                if cache_key in self._metadata:
                    del self._metadata[cache_key]

                # Remove file
                file_path = self._get_cache_file_path(cache_key)
                if file_path.exists():
                    file_path.unlink()
            else:
                # Clear all
                self._cache_data.clear()
                self._metadata.clear()

                # Remove all cache files
                for cache_file in self.config.cache_dir.glob("*.cache"):
                    cache_file.unlink()

            self._record_operation(cache_key or "all", "clear", True)
            return True

        except Exception as e:
            self._record_operation(cache_key or "all", "clear", False, str(e))
            return False

    def _get_cache_file_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        filename = f"{cache_key}.cache"
        if self.config.format == CacheFormat.JSON:
            filename += ".json"
        elif self.config.format == CacheFormat.YAML:
            filename += ".yaml"
        return self.config.cache_dir / filename

    def _load_from_file(self, file_path: Path) -> Optional[Any]:
        """Load data from file based on format."""
        try:
            with open(file_path) as f:
                if self.config.format == CacheFormat.JSON:
                    return json.load(f)
                if self.config.format == CacheFormat.YAML:
                    return yaml.safe_load(f)
                return None
        except Exception:
            return None

    def _save_to_file(self, file_path: Path, data: Any) -> bool:
        """Save data to file based on format."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w") as f:
                if self.config.format == CacheFormat.JSON:
                    json.dump(data, f, indent=2, default=str)
                elif self.config.format == CacheFormat.YAML:
                    yaml.dump(data, f, default_flow_style=False)
                else:
                    return False

            return True
        except Exception:
            return False

    def _validate_cache_entry(self, cache_key: str, data: Any) -> bool:
        """Validate a cache entry."""
        # Check expiration
        metadata = self._metadata.get(cache_key)
        if metadata and metadata.expires_at:
            if datetime.now() > metadata.expires_at:
                return False

        # Check size limits
        data_size = len(str(data).encode("utf-8"))
        return not data_size > self.config.max_size_mb * 1024 * 1024

    def _update_metadata(self, cache_key: str, operation: str):
        """Update cache metadata."""
        if cache_key not in self._metadata:
            self._metadata[cache_key] = CacheMetadata(key=cache_key, value=self._cache_data[cache_key])

        metadata = self._metadata[cache_key]
        metadata.updated_at = datetime.now()
        metadata.size_bytes = len(str(self._cache_data[cache_key]).encode("utf-8"))

        # Set expiration
        if self.config.ttl_hours > 0:
            metadata.expires_at = datetime.now() + timedelta(hours=self.config.ttl_hours)

    def _record_operation(
        self,
        cache_key: str,
        operation: str,
        success: bool,
        error_message: Optional[str] = None,
    ):
        """Record a cache operation."""
        # Record operation for statistics
        if not success:
            self._stats.corruption_count += 1

        self._last_operation = datetime.now()
