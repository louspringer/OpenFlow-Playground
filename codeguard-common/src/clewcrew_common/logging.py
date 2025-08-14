"""
Logging Framework

Unified logging and monitoring for Ghostbusters components.
This module provides consistent logging across all components.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Optional


class ClewcrewLogger:
    """Unified logger for Ghostbusters components"""

    def __init__(self, component_name: str, log_level: str = "INFO"):
        """Initialize the logger for a component"""
        self.component_name = component_name
        self.logger = logging.getLogger(f"ghostbusters.{component_name}")

        # Set log level
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)

        # Add handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, context: Optional[dict[str, Any]] = None):
        """Log info message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.info(message)

    def warning(
        self,
        message: str,
        severity: str = "medium",
        context: Optional[dict[str, Any]] = None,
    ):
        """Log warning message with severity and optional context"""
        if context:
            message = f"{message} | Severity: {severity} | Context: {context}"
        else:
            message = f"{message} | Severity: {severity}"
        self.logger.warning(message)

    def error(self, message: str, context: Optional[dict[str, Any]] = None):
        """Log error message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.error(message)

    def debug(self, message: str, context: Optional[dict[str, Any]] = None):
        """Log debug message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.debug(message)

    def critical(self, message: str, context: Optional[dict[str, Any]] = None):
        """Log critical message with optional context"""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.critical(message)


class LoggingConfig:
    """Configuration for Ghostbusters logging"""

    def __init__(self):
        self.default_level = "INFO"
        self.log_to_file = False
        self.log_file_path = None
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"

    def configure_file_logging(self, log_file_path: str):
        """Configure logging to file"""
        self.log_to_file = True
        self.log_file_path = Path(log_file_path)

        # Ensure log directory exists
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

    def get_logger(self, component_name: str) -> ClewcrewLogger:
        """Get a configured logger for a component"""
        return ClewcrewLogger(component_name, self.default_level)


# Global logging configuration
logging_config = LoggingConfig()


def get_logger(component_name: str) -> ClewcrewLogger:
    """Get a logger for a component"""
    return logging_config.get_logger(component_name)
