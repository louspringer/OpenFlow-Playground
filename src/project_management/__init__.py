#!/usr/bin/env python3
"""
Project Management Domain

This domain provides comprehensive project management capabilities including:
- RM compliance checking and tracking
- Project model management
- Domain coordination and oversight
- Workflow orchestration
"""

from .rm_compliance_checker import RMComplianceChecker, create_rm_compliance_checker

__all__ = [
    "RMComplianceChecker",
    "create_rm_compliance_checker",
]

__version__ = "1.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Project management and RM compliance domain"
