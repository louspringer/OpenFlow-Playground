#!/usr/bin/env python3
"""
Reflective Module Base Interface

This module defines the base interface that all Reflective Modules must implement
to ensure architectural boundaries and operational visibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .health import ModuleHealth, ModuleCapability


class ReflectiveModule(ABC):
    """
    Base interface for all Reflective Modules.

    Reflective Modules are components that:
    1. Must expose their own status through defined interfaces
    2. Cannot be probed internally - only through operational interfaces
    3. Must be completely self-aware and self-reporting
    4. Must have clear architectural boundaries that prevent spaghetti code
    5. Must be testable in isolation without reaching into implementation guts
    """

    @abstractmethod
    async def get_module_status(self) -> ModuleHealth:
        """
        Get current module status.

        Returns:
            ModuleHealth: Comprehensive health status including capabilities,
                        health indicators, and operational metrics.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass

    @abstractmethod
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """
        Get module capabilities.

        Returns:
            List[ModuleCapability]: List of all capabilities this module provides,
                                  including availability status and dependencies.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """
        Check if module is healthy.

        Returns:
            bool: True if module is healthy and operational, False otherwise.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass

    @abstractmethod
    async def get_health_indicators(self) -> Dict[str, Any]:
        """
        Get detailed health indicators.

        Returns:
            Dict[str, Any]: Dictionary of health indicators including performance
                           metrics, error counts, and operational statistics.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass

    async def get_module_info(self) -> Dict[str, Any]:
        """
        Get comprehensive module information.

        This method provides a complete overview of the module including
        status, capabilities, health indicators, and metadata.

        Returns:
            Dict[str, Any]: Complete module information dictionary.
        """
        status = await self.get_module_status()
        capabilities = await self.get_module_capabilities()
        health_indicators = await self.get_health_indicators()

        return {
            "module_name": self.__class__.__name__,
            "module_type": "ReflectiveModule",
            "status": status.to_dict(),
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "available": cap.available,
                    "version": cap.version,
                    "dependencies": cap.dependencies,
                }
                for cap in capabilities
            ],
            "health_indicators": health_indicators,
            "compliance": {
                "reflective_module": True,
                "interface_constrained": True,
                "self_monitoring": True,
                "architecturally_bounded": True,
            },
        }

    async def validate_rm_compliance(self) -> Dict[str, bool]:
        """
        Validate that this module complies with Reflective Module principles.

        Returns:
            Dict[str, bool]: Dictionary indicating compliance with each RM principle.
        """
        try:
            # Test all required methods
            await self.get_module_status()
            await self.get_module_capabilities()
            await self.is_healthy()
            await self.get_health_indicators()

            return {
                "interface_implementation": True,
                "status_reporting": True,
                "capability_disclosure": True,
                "health_monitoring": True,
                "operational_visibility": True,
            }
        except Exception as e:
            return {
                "interface_implementation": False,
                "status_reporting": False,
                "capability_disclosure": False,
                "health_monitoring": False,
                "operational_visibility": False,
                "error": str(e),
            }


class ReflectiveModuleMixin:
    """
    Mixin class to provide common Reflective Module functionality.

    This mixin can be used to add RM capabilities to existing classes
    without requiring a complete rewrite.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the RM mixin"""
        super().__init__(*args, **kwargs)
        self._rm_initialized = True
        self._rm_start_time = None
        self._rm_error_count = 0
        self._rm_warning_count = 0

    async def _get_basic_health_indicators(self) -> Dict[str, Any]:
        """
        Get basic health indicators for the module.

        Returns:
            Dict[str, Any]: Basic health indicators including uptime and error counts.
        """
        import time

        if not hasattr(self, "_rm_start_time"):
            self._rm_start_time = time.time()

        uptime = time.time() - self._rm_start_time if self._rm_start_time else 0

        return {
            "uptime": uptime,
            "error_count": getattr(self, "_rm_error_count", 0),
            "warning_count": getattr(self, "_rm_warning_count", 0),
            "initialized": getattr(self, "_rm_initialized", False),
        }

    def _increment_error_count(self) -> None:
        """Increment the error count for health monitoring"""
        self._rm_error_count += 1

    def _increment_warning_count(self) -> None:
        """Increment the warning count for health monitoring"""
        self._rm_warning_count += 1
