#!/usr/bin/env python3
"""
Ghostbusters Service Interfaces - Clean external interfaces for service status
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


class ServiceStatus(Enum):
    """Service status enumeration"""

    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    NOT_AVAILABLE = "not_available"
    UNKNOWN = "unknown"


@dataclass
class ServiceHealth:
    """Service health information"""

    status: ServiceStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None


@dataclass
class ServiceCapability:
    """Service capability information"""

    name: str
    available: bool
    description: str
    version: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ServiceInterface(ABC):
    """Base interface for all Ghostbusters services"""

    @abstractmethod
    async def get_service_status(self) -> ServiceHealth:
        """Get the current status of this service"""
        pass

    @abstractmethod
    async def get_service_capabilities(self) -> List[ServiceCapability]:
        """Get the capabilities this service provides"""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if the service is healthy and responding"""
        pass


class MultiPerspectiveServiceInterface(ServiceInterface):
    """Interface for multi-perspective analysis services"""

    @abstractmethod
    async def get_available_perspectives(self) -> List[str]:
        """Get list of available analysis perspectives"""
        pass

    @abstractmethod
    async def get_perspective_status(self, perspective: str) -> ServiceHealth:
        """Get status of a specific perspective"""
        pass


class MultiAgentServiceInterface(ServiceInterface):
    """Interface for multi-agent system services"""

    @abstractmethod
    async def get_available_agents(self) -> List[str]:
        """Get list of available AI agents"""
        pass

    @abstractmethod
    async def get_agent_status(self, agent: str) -> ServiceHealth:
        """Get status of a specific agent"""
        pass

    @abstractmethod
    async def get_llm_provider_status(self) -> Dict[str, ServiceHealth]:
        """Get status of LLM providers (OpenAI, Anthropic, etc.)"""
        pass


class RecoveryServiceInterface(ServiceInterface):
    """Interface for recovery engine services"""

    @abstractmethod
    async def get_available_recovery_engines(self) -> List[str]:
        """Get list of available recovery engines"""
        pass

    @abstractmethod
    async def get_recovery_engine_status(self, engine: str) -> ServiceHealth:
        """Get status of a specific recovery engine"""
        pass


class ValidationServiceInterface(ServiceInterface):
    """Interface for validation services"""

    @abstractmethod
    async def get_available_validators(self) -> List[str]:
        """Get list of available validators"""
        pass

    @abstractmethod
    async def get_validator_status(self, validator: str) -> ServiceHealth:
        """Get status of a specific validator"""
        pass


class GhostbustersServiceRegistry:
    """Registry for all Ghostbusters services with their interfaces"""

    def __init__(self):
        self.services: Dict[str, ServiceInterface] = {}

    def register_service(self, name: str, service: ServiceInterface) -> None:
        """Register a service with the registry"""
        self.services[name] = service

    def get_service(self, name: str) -> Optional[ServiceInterface]:
        """Get a service by name"""
        return self.services.get(name)

    async def get_all_service_status(self) -> Dict[str, ServiceHealth]:
        """Get status of all registered services"""
        statuses = {}
        for name, service in self.services.items():
            try:
                statuses[name] = await service.get_service_status()
            except Exception as e:
                statuses[name] = ServiceHealth(
                    status=ServiceStatus.NOT_AVAILABLE,
                    message=f"Error getting status: {e}",
                    details={"error": str(e)},
                )
        return statuses

    async def get_service_capabilities_summary(
        self,
    ) -> Dict[str, List[ServiceCapability]]:
        """Get capabilities summary from all services"""
        capabilities = {}
        for name, service in self.services.items():
            try:
                capabilities[name] = await service.get_service_capabilities()
            except Exception as e:
                capabilities[name] = []
        return capabilities


# Convenience functions for external use
async def get_ghostbusters_service_status() -> Dict[str, Any]:
    """Get comprehensive status of all Ghostbusters services"""
    # This would be implemented by the actual service registry
    # For now, return a placeholder
    return {
        "status": "Service registry not initialized",
        "services": {},
        "timestamp": None,
    }


async def is_ghostbusters_healthy() -> bool:
    """Check if Ghostbusters services are healthy"""
    # This would check the actual service registry
    # For now, return False to indicate services need to be set up
    return False


def get_ghostbusters_status_message() -> str:
    """Get a human-readable status message"""
    # This would query the actual service registry
    # For now, return a placeholder
    return "Status: Ghostbusters services not initialized - run service setup for details"
