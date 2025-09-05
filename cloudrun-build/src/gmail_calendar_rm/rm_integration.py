"""
RM Integration Layer for Gmail-to-Calendar System
================================================

Provides RM-compliant wrapper around the core gmail-calendar-system package
with project-specific integration, health monitoring, and audit capabilities.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

# Core system imports (when available)
try:
    from gmail_calendar_system import GmailCalendarOrchestrator
    from gmail_calendar_system.connectors import OAuthConfig
    from gmail_calendar_system.models import EventResult, AuditLog
except ImportError:
    # Fallback to local implementation during development
    from ..gmail_calendar_system.orchestrator import GmailCalendarOrchestrator
    from ..gmail_calendar_system.connectors import OAuthConfig
    from ..gmail_calendar_system.models import EventResult, AuditLog

from .health_monitoring import HealthMonitor
from .audit_system import AuditSystem
from .model_registry import ModelRegistryIntegration


class RMGmailCalendarSystem:
    """
    RM-compliant wrapper for the Gmail-to-Calendar system.

    Provides:
    - RM compliance interfaces
    - Project model registry integration
    - Health monitoring and status reporting
    - Comprehensive audit trails
    - Project-specific error handling
    """

    def __init__(self, gmail_config: OAuthConfig, calendar_config: OAuthConfig, default_timezone: str = "America/Denver", confidence_threshold: float = 0.85):
        self.logger = logging.getLogger(__name__)

        # Initialize core system
        self.orchestrator = GmailCalendarOrchestrator(gmail_config=gmail_config, calendar_config=calendar_config, default_timezone=default_timezone, confidence_threshold=confidence_threshold)

        # Initialize RM components
        self.health_monitor = HealthMonitor()
        self.audit_system = AuditSystem()
        self.model_registry = ModelRegistryIntegration()

        # RM compliance state
        self._is_healthy = True
        self._last_health_check = None
        self._operation_count = 0
        self._error_count = 0

        self.logger.info("✅ RM Gmail-to-Calendar System initialized")

    async def process_request(self, user_query: str, user_id: str = "rm_user") -> Dict[str, Any]:
        """
        Process a Gmail-to-Calendar request with RM compliance.

        Args:
            user_query: User's request
            user_id: User identifier for audit logging

        Returns:
            Result dictionary with RM-compliant response
        """
        start_time = datetime.now()
        self._operation_count += 1

        try:
            # Log operation start
            await self.audit_system.log_operation_start(operation="process_request", user_id=user_id, query=user_query)

            # Process with core system
            result = await self.orchestrator.process_request(user_query, user_id)

            # Log operation completion
            await self.audit_system.log_operation_completion(operation="process_request", user_id=user_id, result=result, duration=(datetime.now() - start_time).total_seconds())

            # Update health status
            if result.get("success"):
                self._is_healthy = True
            else:
                self._error_count += 1
                if self._error_count > 5:  # Threshold for health degradation
                    self._is_healthy = False

            # Return RM-compliant response
            return {
                "success": result.get("success", False),
                "data": result,
                "rm_metadata": {
                    "operation_id": self._operation_count,
                    "health_status": self._is_healthy,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "audit_trail": await self.audit_system.get_operation_trail(user_id),
                },
            }

        except Exception as e:
            self._error_count += 1
            self._is_healthy = False

            # Log error
            await self.audit_system.log_operation_error(operation="process_request", user_id=user_id, error=str(e), duration=(datetime.now() - start_time).total_seconds())

            self.logger.error(f"❌ RM operation failed: {e}")

            return {
                "success": False,
                "error": str(e),
                "rm_metadata": {
                    "operation_id": self._operation_count,
                    "health_status": self._is_healthy,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "error_count": self._error_count,
                },
            }

    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get RM-compliant health status.

        Returns:
            Health status dictionary
        """
        self._last_health_check = datetime.now()

        # Check core system health
        core_health = await self.health_monitor.check_core_system_health()

        # Check RM components health
        rm_health = await self.health_monitor.check_rm_components_health()

        # Overall health assessment
        overall_healthy = self._is_healthy and core_health.get("healthy", False) and rm_health.get("healthy", False)

        return {
            "healthy": overall_healthy,
            "timestamp": self._last_health_check.isoformat(),
            "core_system": core_health,
            "rm_components": rm_health,
            "metrics": {
                "operation_count": self._operation_count,
                "error_count": self._error_count,
                "error_rate": self._error_count / max(self._operation_count, 1),
                "last_health_check": self._last_health_check.isoformat(),
            },
        }

    async def get_capabilities(self) -> Dict[str, Any]:
        """
        Get RM-compliant capabilities.

        Returns:
            Capabilities dictionary
        """
        return {
            "name": "gmail-calendar-system",
            "version": "1.0.0",
            "description": "Gmail-to-Calendar system with RM compliance",
            "capabilities": ["gmail_reading", "calendar_writing", "ics_parsing", "time_normalization", "conflict_detection", "audit_trail", "health_monitoring"],
            "interfaces": {"mcp_tools": ["google-calendar", "gmail", "ics"], "cli": "gmail-calendar", "api": "GmailCalendarOrchestrator"},
            "rm_compliance": {"health_monitoring": True, "audit_trails": True, "model_registry_integration": True, "error_handling": True, "metrics_collection": True},
        }

    async def register_with_model_registry(self) -> bool:
        """
        Register with the project model registry.

        Returns:
            Registration success status
        """
        try:
            success = await self.model_registry.register_gmail_calendar_system()
            if success:
                self.logger.info("✅ Registered with model registry")
            else:
                self.logger.warning("⚠️ Model registry registration failed")
            return success
        except Exception as e:
            self.logger.error(f"❌ Model registry registration error: {e}")
            return False

    async def get_audit_trail(self, user_id: Optional[str] = None, operation: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get audit trail with optional filtering.

        Args:
            user_id: Filter by user ID
            operation: Filter by operation type
            limit: Maximum number of entries

        Returns:
            List of audit trail entries
        """
        return await self.audit_system.get_audit_trail(user_id=user_id, operation=operation, limit=limit)

    async def get_metrics(self) -> Dict[str, Any]:
        """
        Get RM-compliant metrics.

        Returns:
            Metrics dictionary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "operations": {
                "total": self._operation_count,
                "successful": self._operation_count - self._error_count,
                "failed": self._error_count,
                "success_rate": (self._operation_count - self._error_count) / max(self._operation_count, 1),
            },
            "health": {"current_status": self._is_healthy, "last_check": self._last_health_check.isoformat() if self._last_health_check else None},
            "system": {"uptime": "calculated_from_start_time", "memory_usage": "available_via_psutil", "cpu_usage": "available_via_psutil"},
        }
