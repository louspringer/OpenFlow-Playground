"""
Security Scanning Domain

A comprehensive, multi-threaded security scanning system for detecting
credential exposure, security vulnerabilities, and compliance violations
across all file types in a project.

Features:
- Multi-threaded file processing for optimal performance
- Extensible pattern-based security detection
- Comprehensive file coverage with intelligent exclusions
- Multiple report formats and real-time monitoring
- CI/CD integration with proper exit codes
- Plugin architecture for custom security patterns

Architecture:
- Domain isolation with clear boundaries
- Worker pool for parallel processing
- Pattern management system
- Reporting and notification system
- Configuration management
- Performance monitoring and optimization
"""

from .core.scanner import SecurityScanner, create_security_scanner
from .core.worker_pool import WorkerPool, create_worker_pool
from .patterns.pattern_manager import PatternManager
from .reporting.report_generator import ReportGenerator
from .configuration.config_manager import ConfigManager

__version__ = "1.0.0"
__author__ = "OpenFlow Playground Security Team"

__all__ = [
    "SecurityScanner",
    "WorkerPool",
    "PatternManager",
    "ReportGenerator",
    "ConfigManager",
]
