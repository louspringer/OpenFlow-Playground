#!/usr/bin/env python3
"""
Reflective Module Health Monitoring

This module provides dataclasses and utilities for monitoring the health
and capabilities of Reflective Modules.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ModuleStatus(Enum):
    """Status enumeration for Reflective Modules"""

    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    NOT_AVAILABLE = "not_available"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass
class ModuleCapability:
    """Represents a capability of a Reflective Module"""

    name: str
    description: str
    available: bool
    version: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    last_verified: Optional[datetime] = None

    def __post_init__(self):
        """Validate capability data"""
        if not self.name:
            raise ValueError("Capability name cannot be empty")
        if not self.description:
            raise ValueError("Capability description cannot be empty")


@dataclass
class ModuleHealth:
    """Comprehensive health status for a Reflective Module"""

    status: ModuleStatus
    message: str
    capabilities: List[ModuleCapability]
    health_indicators: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    module_version: Optional[str] = None
    uptime: Optional[float] = None
    error_count: int = 0
    warning_count: int = 0

    def __post_init__(self):
        """Validate health data"""
        if not self.message:
            raise ValueError("Health message cannot be empty")
        if not isinstance(self.capabilities, list):
            raise ValueError("Capabilities must be a list")

    @property
    def is_healthy(self) -> bool:
        """Check if module is considered healthy"""
        return self.status in [ModuleStatus.AVAILABLE, ModuleStatus.PARTIALLY_AVAILABLE]

    @property
    def available_capabilities(self) -> List[ModuleCapability]:
        """Get list of available capabilities"""
        return [cap for cap in self.capabilities if cap.available]

    @property
    def unavailable_capabilities(self) -> List[ModuleCapability]:
        """Get list of unavailable capabilities"""
        return [cap for cap in self.capabilities if not cap.available]

    def add_health_indicator(self, key: str, value: Any) -> None:
        """Add or update a health indicator"""
        self.health_indicators[key] = value

    def get_health_indicator(self, key: str, default: Any = None) -> Any:
        """Get a health indicator value"""
        return self.health_indicators.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert health status to dictionary"""
        return {
            "status": self.status.value,
            "message": self.message,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "available": cap.available,
                    "version": cap.version,
                    "dependencies": cap.dependencies,
                }
                for cap in self.capabilities
            ],
            "health_indicators": self.health_indicators,
            "timestamp": self.timestamp.isoformat(),
            "module_version": self.module_version,
            "uptime": self.uptime,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_healthy": self.is_healthy,
        }


class HealthMonitor:
    """Utility class for monitoring module health"""

    @staticmethod
    def create_healthy_status(message: str, capabilities: List[ModuleCapability], **kwargs) -> ModuleHealth:
        """Create a healthy status for a module"""
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE,
            message=message,
            capabilities=capabilities,
            **kwargs,
        )

    @staticmethod
    def create_degraded_status(
        message: str,
        capabilities: List[ModuleCapability],
        unavailable_capabilities: List[str],
        **kwargs,
    ) -> ModuleHealth:
        """Create a degraded status for a module"""
        # Mark unavailable capabilities
        for cap in capabilities:
            if cap.name in unavailable_capabilities:
                cap.available = False

        return ModuleHealth(
            status=ModuleStatus.PARTIALLY_AVAILABLE,
            message=message,
            capabilities=capabilities,
            **kwargs,
        )

    @staticmethod
    def create_error_status(message: str, capabilities: List[ModuleCapability], error_details: str, **kwargs) -> ModuleHealth:
        """Create an error status for a module"""
        return ModuleHealth(
            status=ModuleStatus.ERROR,
            message=message,
            capabilities=capabilities,
            error_count=1,
            health_indicators={"error_details": error_details},
            **kwargs,
        )
