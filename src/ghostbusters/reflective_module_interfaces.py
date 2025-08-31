"""
Reflective Module Interfaces

This module defines the interfaces and base classes for Reflective Modules.
Reflective Modules are self-monitoring, isolated, testable units that enforce
architectural boundaries by exposing operational interfaces and disallowing
internal probing.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List


class ModuleStatus(Enum):
    """Operational status of a module."""

    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    FAILED = "failed"
    STARTING = "starting"
    STOPPING = "stopping"
    UNKNOWN = "unknown"


class ModuleHealth(Enum):
    """Health status of a module."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ServiceCapability(Enum):
    """Capabilities that a service can provide."""

    CORE_FUNCTIONALITY = "core_functionality"
    MONITORING = "monitoring"
    RECOVERY = "recovery"
    VALIDATION = "validation"
    ANALYSIS = "analysis"
    REPORTING = "reporting"
    INTEGRATION = "integration"
    EXTENSION = "extension"


class ReflectiveModule(ABC):
    """
    Base class for Reflective Modules.

    Reflective Modules are self-monitoring, isolated, testable units that
    enforce architectural boundaries by exposing operational interfaces and
    disallowing internal probing.
    """

    @abstractmethod
    def get_module_status(self) -> ModuleStatus:
        """
        Get the current operational status of this module.

        Returns:
            ModuleStatus: Current operational status
        """
        pass

    @abstractmethod
    def get_module_health(self) -> ModuleHealth:
        """
        Get the current health status of this module.

        Returns:
            ModuleHealth: Current health status
        """
        pass

    @abstractmethod
    def get_module_capabilities(self) -> List[ServiceCapability]:
        """
        Get the capabilities this module provides.

        Returns:
            List[ServiceCapability]: List of available capabilities
        """
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """
        Check if this module is currently healthy.

        Returns:
            bool: True if healthy, False otherwise
        """
        pass

    @abstractmethod
    def get_graceful_degradation_info(self) -> Dict[str, Any]:
        """
        Get information about any graceful degradation in progress.

        Returns:
            Dict[str, Any]: Degradation information or empty dict if none
        """
        pass


class RecoveryReflectiveModule(ReflectiveModule):
    """
    Base class for recovery engines that implement Reflective Module interfaces.
    """

    def get_module_status(self) -> ModuleStatus:
        """Get recovery engine status."""
        return ModuleStatus.OPERATIONAL

    def get_module_health(self) -> ModuleHealth:
        """Get recovery engine health."""
        return ModuleHealth.HEALTHY

    def get_module_capabilities(self) -> List[ServiceCapability]:
        """Get recovery engine capabilities."""
        return [ServiceCapability.RECOVERY, ServiceCapability.MONITORING]

    def is_healthy(self) -> bool:
        """Check if recovery engine is healthy."""
        return self.get_module_health() == ModuleHealth.HEALTHY

    def get_graceful_degradation_info(self) -> Dict[str, Any]:
        """Get recovery engine degradation info."""
        return {}


class ValidationReflectiveModule(ReflectiveModule):
    """
    Base class for validators that implement Reflective Module interfaces.
    """

    def get_module_status(self) -> ModuleStatus:
        """Get validator status."""
        return ModuleStatus.OPERATIONAL

    def get_module_health(self) -> ModuleHealth:
        """Get validator health."""
        return ModuleHealth.HEALTHY

    def get_module_capabilities(self) -> List[ServiceCapability]:
        """Get validator capabilities."""
        return [ServiceCapability.VALIDATION, ServiceCapability.MONITORING]

    def is_healthy(self) -> bool:
        """Check if validator is healthy."""
        return self.get_module_health() == ModuleHealth.HEALTHY

    def get_graceful_degradation_info(self) -> Dict[str, Any]:
        """Get validator degradation info."""
        return {}
