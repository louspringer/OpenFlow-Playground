#!/usr/bin/env python3
"""
Security Scanning Package

A comprehensive security scanning system that integrates with GitGuardian API
and provides actionable security insights for the quality system.
"""

from .op_integration import (
    CredentialManager,
    OnePasswordIntegration,
)
from .quality_integration import (
    SecurityQualityGate,
    SecurityQualityIntegrator,
    SecurityQualityMetrics,
)
from .security_scanner import (
    GitGuardianSecurityScanner,
    SecurityIssue,
    SecurityScanManager,
    SecurityScanResult,
)

__all__ = [
    "SecurityIssue",
    "SecurityScanResult",
    "GitGuardianSecurityScanner",
    "SecurityScanManager",
    "SecurityQualityMetrics",
    "SecurityQualityIntegrator",
    "SecurityQualityGate",
    "CredentialManager",
    "OnePasswordIntegration",
]

__version__ = "1.0.0"
