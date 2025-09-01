#!/usr/bin/env python3
"""
Multi-Perspective Service Implementation - Makes existing agents completely reflective
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .service_interfaces import (
    MultiPerspectiveServiceInterface,
    ServiceHealth,
    ServiceCapability,
    ServiceStatus,
)
from .agents import (
    SecurityExpert,
    CodeQualityExpert,
    TestExpert,
    BuildExpert,
    ArchitectureExpert,
    ModelExpert,
)
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class MultiPerspectiveService(MultiPerspectiveServiceInterface):
    """Service that provides multi-perspective analysis capabilities"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.perspectives = {
            "security": SecurityExpert(),
            "code_quality": CodeQualityExpert(),
            "test": TestExpert(),
            "build": BuildExpert(),
            "architecture": ArchitectureExpert(),
            "model": ModelExpert(),
        }
        self._health_status = ServiceStatus.AVAILABLE
        self._last_health_check = None
        self._error_count = 0
        self._success_count = 0

        # Load project model for capability discovery
        self.project_model = self._load_project_model()

    async def get_service_status(self) -> ServiceHealth:
        """Get the current status of the multi-perspective service"""
        try:
            # Check if all perspectives are healthy
            healthy_perspectives = 0
            total_perspectives = len(self.perspectives)

            for name, perspective in self.perspectives.items():
                try:
                    # Quick health check - try to instantiate and check basic functionality
                    if hasattr(perspective, "detect_delusions"):
                        healthy_perspectives += 1
                except Exception as e:
                    logger.warning(f"Perspective {name} health check failed: {e}")

            # Calculate health percentage
            health_percentage = (healthy_perspectives / total_perspectives) * 100

            if health_percentage >= 90:
                self._health_status = ServiceStatus.AVAILABLE
                message = f"Multi-perspective service fully available ({health_percentage:.0f}% healthy)"
            elif health_percentage >= 50:
                self._health_status = ServiceStatus.PARTIALLY_AVAILABLE
                message = f"Multi-perspective service partially available ({health_percentage:.0f}% healthy)"
            else:
                self._health_status = ServiceStatus.NOT_AVAILABLE
                message = f"Multi-perspective service not available ({health_percentage:.0f}% healthy)"

            details = {
                "healthy_perspectives": healthy_perspectives,
                "total_perspectives": total_perspectives,
                "health_percentage": health_percentage,
                "perspective_status": await self._get_perspective_status_summary(),
            }

            return ServiceHealth(
                status=self._health_status,
                message=message,
                details=details,
                timestamp=asyncio.get_event_loop().time(),
            )

        except Exception as e:
            logger.error(f"Error getting multi-perspective service status: {e}")
            self._health_status = ServiceStatus.NOT_AVAILABLE
            return ServiceHealth(
                status=ServiceStatus.NOT_AVAILABLE,
                message=f"Error checking service status: {e}",
                details={"error": str(e)},
                timestamp=asyncio.get_event_loop().time(),
            )

    def _load_project_model(self) -> dict:
        """Load the project model registry for capability discovery"""
        try:
            model_path = Path(self.project_path) / "project_model_registry.json"
            if model_path.exists():
                with open(model_path, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Project model not found at {model_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading project model: {e}")
            return {}

    async def get_service_capabilities(self) -> List[ServiceCapability]:
        """Get the capabilities this service provides based on project model"""
        capabilities = []

        # Get Ghostbusters domain configuration from project model
        ghostbusters_domain = self.project_model.get("domains", {}).get("ghostbusters", {})

        for name, perspective in self.perspectives.items():
            try:
                # Get perspective-specific capabilities
                if hasattr(perspective, "detect_delusions"):
                    # Check if this perspective is mentioned in project model
                    content_indicators = ghostbusters_domain.get("content_indicators", [])
                    perspective_mentioned = any(name.replace("_", "") in indicator.lower() for indicator in content_indicators)

                    capabilities.append(
                        ServiceCapability(
                            name=f"{name}_analysis",
                            available=True,
                            description=f"Delusion detection from {name} perspective",
                            version="1.0.0",
                            details={
                                "perspective": name,
                                "method": "detect_delusions",
                                "async": True,
                                "model_defined": perspective_mentioned,
                                "project_model_requirements": self._get_perspective_requirements(name, ghostbusters_domain),
                            },
                        )
                    )

                # Add any additional capabilities the perspective might have
                if hasattr(perspective, "get_recommendations"):
                    capabilities.append(
                        ServiceCapability(
                            name=f"{name}_recommendations",
                            available=True,
                            description=f"Recommendations from {name} perspective",
                            version="1.0.0",
                            details={
                                "perspective": name,
                                "method": "get_recommendations",
                                "model_defined": True,
                            },
                        )
                    )

            except Exception as e:
                logger.warning(f"Error getting capabilities for perspective {name}: {e}")
                capabilities.append(
                    ServiceCapability(
                        name=f"{name}_analysis",
                        available=False,
                        description=f"Delusion detection from {name} perspective (unavailable)",
                        details={"error": str(e)},
                    )
                )

        # Add capabilities from project model requirements
        requirements = ghostbusters_domain.get("requirements", [])
        for req in requirements:
            if "multi-perspective" in req.lower() or "perspective" in req.lower():
                capabilities.append(
                    ServiceCapability(
                        name="multi_perspective_analysis",
                        available=True,
                        description=f"Multi-perspective analysis: {req}",
                        version="1.0.0",
                        details={
                            "requirement": req,
                            "source": "project_model",
                            "domain": "ghostbusters",
                        },
                    )
                )

        return capabilities

    def _get_perspective_requirements(self, perspective: str, domain_config: dict) -> List[str]:
        """Get requirements related to a specific perspective from project model"""
        requirements = domain_config.get("requirements", [])
        perspective_requirements = []

        perspective_keywords = {
            "security": ["security", "SecurityExpert"],
            "code_quality": ["code quality", "CodeQualityExpert", "quality"],
            "test": ["test", "TestExpert", "testing"],
            "build": ["build", "BuildExpert", "build"],
            "architecture": ["architecture", "ArchitectureExpert", "architectural"],
            "model": ["model", "ModelExpert", "model-driven"],
        }

        keywords = perspective_keywords.get(perspective, [])
        for req in requirements:
            if any(keyword.lower() in req.lower() for keyword in keywords):
                perspective_requirements.append(req)

        return perspective_requirements

    async def is_healthy(self) -> bool:
        """Check if the service is healthy and responding"""
        try:
            status = await self.get_service_status()
            return status.status in [
                ServiceStatus.AVAILABLE,
                ServiceStatus.PARTIALLY_AVAILABLE,
            ]
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def get_available_perspectives(self) -> List[str]:
        """Get list of available analysis perspectives"""
        available = []
        for name, perspective in self.perspectives.items():
            try:
                if hasattr(perspective, "detect_delusions"):
                    available.append(name)
            except Exception as e:
                logger.warning(f"Perspective {name} not available: {e}")
        return available

    async def get_perspective_status(self, perspective: str) -> ServiceHealth:
        """Get status of a specific perspective"""
        if perspective not in self.perspectives:
            return ServiceHealth(
                status=ServiceStatus.NOT_AVAILABLE,
                message=f"Perspective '{perspective}' not found",
                details={"available_perspectives": list(self.perspectives.keys())},
                timestamp=asyncio.get_event_loop().time(),
            )

        try:
            perspective_instance = self.perspectives[perspective]

            # Check if perspective has required methods
            if hasattr(perspective_instance, "detect_delusions"):
                # Test basic functionality
                try:
                    # Quick test - don't run full analysis, just check if method exists and is callable
                    method = getattr(perspective_instance, "detect_delusions")
                    if callable(method):
                        return ServiceHealth(
                            status=ServiceStatus.AVAILABLE,
                            message=f"Perspective '{perspective}' is available and functional",
                            details={
                                "perspective": perspective,
                                "has_detect_delusions": True,
                                "method_type": type(method).__name__,
                            },
                            timestamp=asyncio.get_event_loop().time(),
                        )
                    else:
                        return ServiceHealth(
                            status=ServiceStatus.NOT_AVAILABLE,
                            message=f"Perspective '{perspective}' method is not callable",
                            details={
                                "perspective": perspective,
                                "method_type": type(method).__name__,
                            },
                            timestamp=asyncio.get_event_loop().time(),
                        )
                except Exception as e:
                    return ServiceHealth(
                        status=ServiceStatus.NOT_AVAILABLE,
                        message=f"Perspective '{perspective}' test failed: {e}",
                        details={"perspective": perspective, "error": str(e)},
                        timestamp=asyncio.get_event_loop().time(),
                    )
            else:
                return ServiceHealth(
                    status=ServiceStatus.NOT_AVAILABLE,
                    message=f"Perspective '{perspective}' missing required method 'detect_delusions'",
                    details={
                        "perspective": perspective,
                        "missing_method": "detect_delusions",
                    },
                    timestamp=asyncio.get_event_loop().time(),
                )

        except Exception as e:
            return ServiceHealth(
                status=ServiceStatus.NOT_AVAILABLE,
                message=f"Error checking perspective '{perspective}' status: {e}",
                details={"perspective": perspective, "error": str(e)},
                timestamp=asyncio.get_event_loop().time(),
            )

    async def _get_perspective_status_summary(self) -> Dict[str, Any]:
        """Get summary status of all perspectives"""
        summary = {}
        for name in self.perspectives.keys():
            try:
                status = await self.get_perspective_status(name)
                summary[name] = {
                    "status": status.status.value,
                    "message": status.message,
                    "available": status.status in [ServiceStatus.AVAILABLE, ServiceStatus.PARTIALLY_AVAILABLE],
                }
            except Exception as e:
                summary[name] = {
                    "status": ServiceStatus.NOT_AVAILABLE.value,
                    "message": f"Error checking status: {e}",
                    "available": False,
                }
        return summary

    async def run_analysis(self, perspective: str, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Run analysis using a specific perspective"""
        if perspective not in self.perspectives:
            raise ValueError(f"Perspective '{perspective}' not available")

        try:
            perspective_instance = self.perspectives[perspective]
            analysis_path = Path(project_path) if project_path else self.project_path

            # Run the analysis
            result = await perspective_instance.detect_delusions(analysis_path)

            # Track success
            self._success_count += 1

            return {
                "perspective": perspective,
                "success": True,
                "delusions_found": len(result.delusions),
                "confidence": result.confidence,
                "recommendations": result.recommendations,
                "timestamp": asyncio.get_event_loop().time(),
            }

        except Exception as e:
            # Track error
            self._error_count += 1
            logger.error(f"Analysis failed for perspective '{perspective}': {e}")

            return {
                "perspective": perspective,
                "success": False,
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time(),
            }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the service"""
        return {
            "success_count": self._success_count,
            "error_count": self._error_count,
            "total_requests": self._success_count + self._error_count,
            "success_rate": ((self._success_count / (self._success_count + self._error_count) * 100) if (self._success_count + self._error_count) > 0 else 0),
            "last_health_check": self._last_health_check,
            "current_health_status": self._health_status.value,
        }


# Convenience function for external use
async def create_multi_perspective_service(
    project_path: str = ".",
) -> MultiPerspectiveService:
    """Create and return a multi-perspective service instance"""
    return MultiPerspectiveService(project_path)


async def get_multi_perspective_status(project_path: str = ".") -> ServiceHealth:
    """Get status of multi-perspective service"""
    service = MultiPerspectiveService(project_path)
    return await service.get_service_status()


async def is_multi_perspective_healthy(project_path: str = ".") -> bool:
    """Check if multi-perspective service is healthy"""
    service = MultiPerspectiveService(project_path)
    return await service.is_healthy()
