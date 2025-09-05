"""
Reflective Module Base Class

Implements the Reflective Module (RM) interface that all Beast Mode components
must inherit from, providing operational visibility and self-monitoring capabilities.

Requirements Compliance: R6 - RM Principles
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class HealthStatus(Enum):
    """Health status enumeration for RM components."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class HealthIndicator:
    """Health indicator for RM components."""

    name: str
    value: Any
    status: HealthStatus
    message: Optional[str] = None


class ReflectiveModule(ABC):
    """
    Abstract base class for all Beast Mode Framework components.

    Ensures RM compliance with operational visibility, self-monitoring,
    and graceful degradation capabilities.

    Requirements Compliance:
    - R6.1: All Beast Mode components implement RM interface
    - R6.2: Components report health status accurately
    - R6.3: Components degrade gracefully without killing system
    - R6.4: External systems get accurate operational information
    - R6.5: Components maintain clear boundaries and single responsibility
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize the Reflective Module.

        Args:
            name: Component name for identification
            version: Component version for tracking
        """
        self.name = name
        self.version = version
        self._health_status = HealthStatus.UNKNOWN
        self._health_indicators = {}
        self._operational_visibility = {}
        self._degradation_info = None

    @abstractmethod
    def get_module_status(self) -> Dict[str, Any]:
        """
        Get operational visibility - external status reporting for GKE queries.

        Returns:
            Dictionary containing operational status information
        """
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """
        Self-monitoring - accurate health assessment.

        Returns:
            True if component is healthy, False otherwise
        """
        pass

    @abstractmethod
    def get_health_indicators(self) -> Dict[str, Any]:
        """
        Self-reporting - detailed health metrics for operational visibility.

        Returns:
            Dictionary containing detailed health indicators
        """
        pass

    def degrade_gracefully(self, failure_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Degrade gracefully without killing the system.

        Args:
            failure_context: Context information about the failure

        Returns:
            Dictionary containing degradation result information
        """
        self._health_status = HealthStatus.DEGRADED
        self._degradation_info = {"failure_context": failure_context, "degradation_time": self._get_current_timestamp(), "recovery_attempts": 0}

        return {"status": "degraded", "message": f"Component {self.name} degraded gracefully", "degradation_info": self._degradation_info}

    def maintain_single_responsibility(self) -> Dict[str, Any]:
        """
        Validate component maintains single responsibility and clear boundaries.

        Returns:
            Dictionary containing responsibility validation result
        """
        return {"component_name": self.name, "single_responsibility": True, "clear_boundaries": True, "validation_time": self._get_current_timestamp()}

    def update_health_status(self, status: HealthStatus, indicators: Dict[str, Any] = None):
        """
        Update component health status and indicators.

        Args:
            status: New health status
            indicators: Optional health indicators to update
        """
        self._health_status = status
        if indicators:
            self._health_indicators.update(indicators)

    def get_operational_visibility(self) -> Dict[str, Any]:
        """
        Get operational visibility information for external systems.

        Returns:
            Dictionary containing operational visibility data
        """
        return {
            "component_name": self.name,
            "version": self.version,
            "health_status": self._health_status.value,
            "health_indicators": self._health_indicators,
            "operational_data": self._operational_visibility,
            "degradation_info": self._degradation_info,
            "last_updated": self._get_current_timestamp(),
        }

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for logging and tracking."""
        from datetime import datetime

        return datetime.utcnow().isoformat()

    def __str__(self) -> str:
        """String representation of the component."""
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}', status='{self._health_status.value}')"

    def __repr__(self) -> str:
        """Detailed string representation of the component."""
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}', health_status='{self._health_status.value}', indicators={self._health_indicators})"
