#!/usr/bin/env python3
"""
Reflective Modules Package

This package provides the foundation for Reflective Module (RM) architecture,
enabling components to be self-monitoring, interface-constrained, and
architecturally bounded to prevent spaghetti code.
"""

from .base import ReflectiveModule
from .health import ModuleHealth, ModuleCapability, ModuleStatus
from .registry import ReflectiveModuleRegistry

__all__ = [
    "ReflectiveModule",
    "ModuleHealth",
    "ModuleCapability",
    "ModuleStatus",
    "ReflectiveModuleRegistry",
]

# Version information
__version__ = "1.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Reflective Module architecture foundation"
