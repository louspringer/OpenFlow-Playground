"""
RM-DDD Core Module

Core Reflective Module functionality with domain awareness extensions.
"""

from .base import ReflectiveModuleBase, DomainReflectiveModule
from .health import ModuleHealth, ModuleStatus, ModuleCapability, DomainHealth, HealthMonitor
from .registry import get_global_registry, ModuleRegistry

__all__ = [
    "ReflectiveModuleBase",
    "DomainReflectiveModule",
    "ModuleHealth",
    "ModuleStatus",
    "ModuleCapability",
    "DomainHealth",
    "HealthMonitor",
    "get_global_registry",
    "ModuleRegistry",
]
