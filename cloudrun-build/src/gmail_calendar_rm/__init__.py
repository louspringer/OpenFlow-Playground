"""
Gmail-to-Calendar RM Integration Layer
=====================================

Provides RM-compliant integration for the Gmail-to-Calendar system
within the OpenFlow-Playground project architecture.

This layer wraps the core gmail-calendar-system package with:
- RM compliance interfaces
- Project model registry integration
- Health monitoring and audit trails
- Project-specific tooling and workflows
"""

__version__ = "1.0.0"
__author__ = "OpenFlow-Playground"

from .rm_integration import RMGmailCalendarSystem
from .model_registry import ModelRegistryIntegration
from .health_monitoring import HealthMonitor
from .audit_system import AuditSystem

__all__ = [
    "RMGmailCalendarSystem",
    "ModelRegistryIntegration",
    "HealthMonitor",
    "AuditSystem",
]
