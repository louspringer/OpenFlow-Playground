#!/usr/bin/env python3
"""
Base Reflective Module
Provides common ReflectiveModule functionality to reduce duplication.
"""

import logging
import time
from typing import Any, Dict, List
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


class BaseReflectiveModule(ReflectiveModule):
    """Base class providing common ReflectiveModule functionality."""

    def __init__(self) -> None:
        # Initialize operational state tracking
        self._error_count = 0
        self._success_count = 0
        self._last_operation_time = time.time()
        self._is_operational = True

        logger.info(f"✅ {self.__class__.__name__} initialized")

    # Common operational state methods
    def _check_operational_state(self) -> bool:
        """Check if module is operational."""
        return self._is_operational

    def _get_error_count(self) -> int:
        """Get current error count."""
        return self._error_count

    def _get_success_count(self) -> int:
        """Get current success count."""
        return self._success_count

    def _calculate_success_rate(self) -> float:
        """Calculate current success rate."""
        total_operations = self._success_count + self._error_count
        return self._success_count / total_operations if total_operations > 0 else 1.0

    def _get_last_operation_time(self) -> float:
        """Get last operation timestamp."""
        return self._last_operation_time

    def _track_success(self) -> None:
        """Track successful operation."""
        self._success_count += 1
        self._last_operation_time = time.time()

    def _track_error(self) -> None:
        """Track error operation."""
        self._error_count += 1
        self._last_operation_time = time.time()

    # Common ReflectiveModule interface implementation
    async def get_module_status(self) -> ModuleHealth:
        """Get current module status."""
        try:
            # Calculate success rate
            total_operations = self._success_count + self._error_count
            success_rate = self._calculate_success_rate()

            # Determine status based on operational state
            if self._is_operational and self._error_count == 0 and success_rate > 0.95:
                status = ModuleStatus.AVAILABLE
                message = "Module is fully operational"
            elif self._is_operational and success_rate > 0.8:
                status = ModuleStatus.PARTIALLY_AVAILABLE
                message = f"Module operational with {success_rate:.1%} success rate"
            else:
                status = ModuleStatus.NOT_AVAILABLE
                message = f"Module has {self._error_count} errors, {success_rate:.1%} success rate"

            return ModuleHealth(
                status=status,
                message=message,
                capabilities=await self.get_module_capabilities(),
                health_indicators={
                    "error_count": self._error_count,
                    "success_count": self._success_count,
                    "success_rate": success_rate,
                    "last_operation": self._last_operation_time,
                    "total_operations": total_operations,
                },
                timestamp=time.time(),
            )

        except Exception as e:
            return ModuleHealth(
                status=ModuleStatus.NOT_AVAILABLE,
                message=f"Module status check failed: {e}",
                capabilities=[],
                health_indicators={"error": str(e)},
                timestamp=time.time(),
            )

    async def is_healthy(self) -> bool:
        """Check if module is healthy."""
        try:
            status = await self.get_module_status()
            return status.status == ModuleStatus.AVAILABLE
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        try:
            status = await self.get_module_status()
            return status.health_indicators
        except Exception as e:
            logger.error(f"❌ Failed to get health indicators: {e}")
            return {"error": str(e), "status": "unhealthy"}

    # Abstract method that must be implemented by subclasses
    @abstractmethod
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get module capabilities."""
        pass
