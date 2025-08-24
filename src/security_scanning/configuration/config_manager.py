"""
Configuration Manager for Security Scanning

This module provides configuration management for the security scanning
domain, including pattern definitions, exclusion rules, and settings.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Configuration manager for security scanning operations

    Features:
    - Default security patterns
    - Configurable exclusions
    - Performance settings
    - Output formatting options
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager

        Args:
            config_file: Path to configuration file (optional)
        """
        self.config_file = config_file
        self.config = self._load_default_config()

        # Load custom config if provided
        if config_file:
            self._load_custom_config(config_file)

        logger.debug("Configuration manager initialized")

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "scanning": {
                "max_file_size": 10 * 1024 * 1024,  # 10MB
                "max_workers": None,  # Auto-detect
                "enable_monitoring": True,
                "show_progress": True,
                "timeout": 300,  # 5 minutes
            },
            "patterns": {
                "enable_credential_detection": True,
                "enable_vulnerability_detection": True,
                "enable_compliance_detection": True,
                "false_positive_threshold": 0.8,
            },
            "reporting": {
                "output_formats": ["json", "console"],
                "include_context": True,
                "include_metadata": True,
                "severity_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            },
            "exclusions": {
                "file_patterns": [],
                "directory_patterns": [],
                "size_thresholds": [],
            },
            "performance": {
                "batch_size": 100,
                "memory_limit": 500 * 1024 * 1024,  # 500MB
                "cpu_threshold": 0.9,  # 90%
            },
        }

    def _load_custom_config(self, config_file: str):
        """Load custom configuration from file"""
        try:
            # TODO: Implement custom config loading
            logger.info(
                f"Custom configuration loading not yet implemented: {config_file}"
            )
        except Exception as e:
            logger.warning(f"Failed to load custom config {config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key

        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """
        Set configuration value by key

        Args:
            key: Configuration key (dot notation supported)
            value: Value to set
        """
        keys = key.split(".")
        config = self.config

        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def get_scanning_config(self) -> Dict[str, Any]:
        """Get scanning configuration"""
        return self.config.get("scanning", {})

    def get_patterns_config(self) -> Dict[str, Any]:
        """Get patterns configuration"""
        return self.config.get("patterns", {})

    def get_reporting_config(self) -> Dict[str, Any]:
        """Get reporting configuration"""
        return self.config.get("reporting", {})

    def get_exclusions_config(self) -> Dict[str, Any]:
        """Get exclusions configuration"""
        return self.config.get("exclusions", {})

    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance configuration"""
        return self.config.get("performance", {})

    def update_config(self, updates: Dict[str, Any]):
        """
        Update configuration with new values

        Args:
            updates: Dictionary of configuration updates
        """
        for key, value in updates.items():
            self.set(key, value)

        logger.info("Configuration updated")

    def validate_config(self) -> List[str]:
        """
        Validate configuration for errors

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Validate scanning config
        scanning = self.get_scanning_config()
        if scanning.get("max_file_size", 0) <= 0:
            errors.append("max_file_size must be positive")

        if scanning.get("timeout", 0) <= 0:
            errors.append("timeout must be positive")

        # Validate patterns config
        patterns = self.get_patterns_config()
        threshold = patterns.get("false_positive_threshold", 0)
        if not 0 <= threshold <= 1:
            errors.append("false_positive_threshold must be between 0 and 1")

        # Validate performance config
        performance = self.get_performance_config()
        if performance.get("memory_limit", 0) <= 0:
            errors.append("memory_limit must be positive")

        if performance.get("cpu_threshold", 0) <= 0:
            errors.append("cpu_threshold must be positive")

        return errors

    def get_effective_config(self) -> Dict[str, Any]:
        """
        Get effective configuration with all defaults applied

        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass
