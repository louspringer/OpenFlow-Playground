#!/usr/bin/env python3
"""
Security Best Practices Module

This module provides security best practices implementation using established tools
instead of custom security scanners. It follows industry standards and OWASP guidelines.
"""

from .domain_model import (
    SecurityBestPractices,
    SecurityCategory,
    SecurityFinding,
    SecurityScanResult,
    SecuritySeverity,
    SecurityTool,
    SecurityToolType,
    SecurityWorkflow,
)

__version__ = "1.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Security best practices using established tools instead of custom scanners"

__all__ = [
    "SecurityBestPractices",
    "SecurityTool",
    "SecurityFinding",
    "SecurityScanResult",
    "SecurityWorkflow",
    "SecurityToolType",
    "SecuritySeverity",
    "SecurityCategory",
]

# Core principle
CORE_PRINCIPLE = "Use established tools, not custom scanners"

# Available security tools
SECURITY_TOOLS = [
    "Bandit",  # Python security scanning
    "Semgrep",  # Pattern-based security scanning
    "Safety",  # Dependency vulnerability scanning
    "Detect-Secrets",  # Secret detection
    "Gitleaks",  # Comprehensive secret detection
    "Trivy",  # Infrastructure and dependency scanning
]

# Security best practices
SECURITY_BEST_PRACTICES = [
    "NEVER build custom security scanners",
    "ALWAYS use established, battle-tested tools",
    "Follow OWASP Top 10 guidelines",
    "Use CWE references for issue classification",
    "Implement proper severity levels",
    "Use comprehensive security scanning workflow",
    "Integrate multiple security tools for coverage",
    "Provide clear tool installation instructions",
    "Support both Python packages and external binaries",
    "Maintain security tool configurations",
]


# Quick access to main class
def create_security_best_practices():
    """Create a new SecurityBestPractices instance"""
    return SecurityBestPractices()


def get_security_tools():
    """Get list of available security tools"""
    return SECURITY_TOOLS.copy()


def get_best_practices():
    """Get list of security best practices"""
    return SECURITY_BEST_PRACTICES.copy()


def get_core_principle():
    """Get the core security principle"""
    return CORE_PRINCIPLE
