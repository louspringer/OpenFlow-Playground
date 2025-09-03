#!/usr/bin/env python3
"""
Ack-Bert Reflective Module Base
Provides RM compliance for Ack-Bert framework components.
"""

import logging
import time
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

# Import ReflectiveModule interface
try:
    from src.reflective_modules.base import ReflectiveModule
    from src.reflective_modules.health import (
        ModuleHealth,
        ModuleCapability,
        ModuleStatus,
    )

    REFLECTIVE_MODULE_AVAILABLE = True
except ImportError:
    # Fallback if ReflectiveModule not available
    REFLECTIVE_MODULE_AVAILABLE = False
    ReflectiveModule = ABC
    ModuleHealth = Dict[str, Any]
    ModuleCapability = Dict[str, Any]
    ModuleStatus = type(
        "ModuleStatus",
        (),
        {
            "AVAILABLE": "AVAILABLE",
            "PARTIALLY_AVAILABLE": "PARTIALLY_AVAILABLE",
            "NOT_AVAILABLE": "NOT_AVAILABLE",
        },
    )()

logger = logging.getLogger(__name__)


class AckBertReflectiveModule(ReflectiveModule):
    """Base class providing RM compliance for Ack-Bert components."""

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        self.logger = logging.getLogger(f"{__name__}.{module_name}")

        # RM Compliance: Track operational metrics
        self._error_count = 0
        self._success_count = 0
        self._last_operation_time = time.time()
        self._is_operational = True
        self._operation_count = 0

        # RM Compliance: Health indicators
        self._health_indicators = {"error_rate": 0.0, "success_rate": 0.0, "uptime": 0.0, "last_operation": None, "operational_status": "HEALTHY"}

        self.logger.info(f"✅ {module_name} RM module initialized")

    def log_operation(self, success: bool, operation: str, details: Optional[str] = None) -> None:
        """RM Compliance: Log operations for self-monitoring."""
        self._operation_count += 1
        self._last_operation_time = time.time()

        if success:
            self._success_count += 1
            self.logger.debug(f"✅ {operation} succeeded")
        else:
            self._error_count += 1
            self.logger.warning(f"❌ {operation} failed: {details}")

        # Update health indicators
        self._update_health_indicators()

    def _update_health_indicators(self) -> None:
        """RM Compliance: Update health indicators."""
        total_operations = self._error_count + self._success_count
        if total_operations > 0:
            self._health_indicators["error_rate"] = self._error_count / total_operations
            self._health_indicators["success_rate"] = self._success_count / total_operations

        self._health_indicators["uptime"] = time.time() - self._last_operation_time
        self._health_indicators["last_operation"] = self._last_operation_time

        if self._error_count > self._success_count and self._error_count > 5:
            self._health_indicators["operational_status"] = "DEGRADED"
        elif self._error_count == 0:
            self._health_indicators["operational_status"] = "HEALTHY"
        else:
            self._health_indicators["operational_status"] = "WARNING"

    def get_health_status(self) -> ModuleHealth:
        """RM Compliance: Return current health status."""
        return {
            "module_name": self.module_name,
            "status": self._health_indicators["operational_status"],
            "metrics": self._health_indicators,
            "capabilities": self.get_capabilities(),
            "last_updated": time.time(),
        }

    def get_capabilities(self) -> List[ModuleCapability]:
        """RM Compliance: Return module capabilities."""
        return [{"name": f"{self.module_name}_operations", "description": f"Core operations for {self.module_name}", "available": self._is_operational, "version": "1.0.0"}]

    def validate_self(self) -> bool:
        """RM Compliance: Self-validation."""
        try:
            # Basic validation checks
            if self._error_count < 0 or self._success_count < 0:
                self.logger.error("Invalid operation counts")
                return False

            if self._last_operation_time > time.time():
                self.logger.error("Invalid last operation time")
                return False

            self.logger.debug(f"✅ {self.module_name} self-validation passed")
            return True

        except Exception as e:
            self.logger.error(f"❌ {self.module_name} self-validation failed: {e}")
            return False

    def get_operational_metrics(self) -> Dict[str, Any]:
        """RM Compliance: Return operational metrics."""
        return {
            "module_name": self.module_name,
            "total_operations": self._operation_count,
            "success_count": self._success_count,
            "error_count": self._error_count,
            "success_rate": self._health_indicators["success_rate"],
            "error_rate": self._health_indicators["error_rate"],
            "uptime": self._health_indicators["uptime"],
            "last_operation": self._last_operation_time,
            "operational_status": self._health_indicators["operational_status"],
        }

    def reset_metrics(self) -> None:
        """RM Compliance: Reset operational metrics."""
        self._error_count = 0
        self._success_count = 0
        self._operation_count = 0
        self._last_operation_time = time.time()
        self._update_health_indicators()
        self.logger.info(f"✅ {self.module_name} metrics reset")

    def is_healthy(self) -> bool:
        """RM Compliance: Check if module is healthy."""
        return self._is_operational and self._health_indicators["operational_status"] in ["HEALTHY", "WARNING"] and self.validate_self()

    def get_diagnostic_info(self) -> Dict[str, Any]:
        """RM Compliance: Get diagnostic information."""
        return {
            "module_name": self.module_name,
            "health_status": self.get_health_status(),
            "operational_metrics": self.get_operational_metrics(),
            "capabilities": self.get_capabilities(),
            "is_healthy": self.is_healthy(),
            "validation_passed": self.validate_self(),
        }
