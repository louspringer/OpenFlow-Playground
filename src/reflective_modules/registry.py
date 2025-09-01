#!/usr/bin/env python3
"""
Reflective Module Registry

This module provides a registry system for discovering and managing
Reflective Modules across the system.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Type
from .base import ReflectiveModule
from .health import ModuleHealth, ModuleCapability, ModuleStatus

logger = logging.getLogger(__name__)


class ReflectiveModuleRegistry:
    """
    Registry for discovering and managing Reflective Modules.

    This registry provides:
    1. Module discovery and registration
    2. Health monitoring across all modules
    3. Capability discovery and orchestration
    4. System-wide health status
    """

    def __init__(self):
        """Initialize the RM registry"""
        self._modules: Dict[str, ReflectiveModule] = {}
        self._module_metadata: Dict[str, Dict[str, Any]] = {}
        self._capability_index: Dict[str, List[str]] = {}
        self._health_cache: Dict[str, ModuleHealth] = {}
        self._last_health_check: Optional[float] = None
        self._health_check_interval: float = 30.0  # seconds

    def register_module(
        self,
        module: ReflectiveModule,
        module_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a Reflective Module with the registry.

        Args:
            module: The ReflectiveModule instance to register
            module_id: Optional custom ID for the module
            metadata: Optional metadata about the module

        Returns:
            str: The module ID used for registration

        Raises:
            ValueError: If module is not a valid ReflectiveModule
            KeyError: If module_id already exists
        """
        if not isinstance(module, ReflectiveModule):
            raise ValueError("Module must implement ReflectiveModule interface")

        # Generate module ID if not provided
        if module_id is None:
            module_id = f"{module.__class__.__name__}_{id(module)}"

        # Check for duplicate registration
        if module_id in self._modules:
            raise KeyError(f"Module ID '{module_id}' already registered")

        # Register the module
        self._modules[module_id] = module
        self._module_metadata[module_id] = metadata or {}

        # Index capabilities
        self._index_module_capabilities(module_id, module)

        logger.info(f"Registered Reflective Module: {module_id} ({module.__class__.__name__})")
        return module_id

    def unregister_module(self, module_id: str) -> bool:
        """
        Unregister a module from the registry.

        Args:
            module_id: The ID of the module to unregister

        Returns:
            bool: True if module was unregistered, False if not found
        """
        if module_id in self._modules:
            # Remove from all indexes
            module = self._modules[module_id]
            self._remove_module_capabilities(module_id, module)

            del self._modules[module_id]
            del self._module_metadata[module_id]

            if module_id in self._health_cache:
                del self._health_cache[module_id]

            logger.info(f"Unregistered Reflective Module: {module_id}")
            return True

        return False

    def get_module(self, module_id: str) -> Optional[ReflectiveModule]:
        """
        Get a registered module by ID.

        Args:
            module_id: The ID of the module to retrieve

        Returns:
            Optional[ReflectiveModule]: The module if found, None otherwise
        """
        return self._modules.get(module_id)

    def list_modules(self) -> List[str]:
        """
        Get list of all registered module IDs.

        Returns:
            List[str]: List of module IDs
        """
        return list(self._modules.keys())

    def get_module_metadata(self, module_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a registered module.

        Args:
            module_id: The ID of the module

        Returns:
            Optional[Dict[str, Any]]: Module metadata if found, None otherwise
        """
        return self._module_metadata.get(module_id)

    def find_modules_by_capability(self, capability_name: str) -> List[str]:
        """
        Find modules that provide a specific capability.

        Args:
            capability_name: Name of the capability to search for

        Returns:
            List[str]: List of module IDs that provide the capability
        """
        return self._capability_index.get(capability_name, [])

    def get_all_capabilities(self) -> Dict[str, List[str]]:
        """
        Get all capabilities and the modules that provide them.

        Returns:
            Dict[str, List[str]]: Mapping of capability names to module IDs
        """
        return self._capability_index.copy()

    async def get_module_health(self, module_id: str, force_check: bool = False) -> Optional[ModuleHealth]:
        """
        Get health status for a specific module.

        Args:
            module_id: The ID of the module
            force_check: Force a fresh health check

        Returns:
            Optional[ModuleHealth]: Module health status if found, None otherwise
        """
        if module_id not in self._modules:
            return None

        # Check cache unless forced
        if not force_check and module_id in self._health_cache:
            return self._health_cache[module_id]

        try:
            module = self._modules[module_id]
            health = await module.get_module_status()
            self._health_cache[module_id] = health
            return health
        except Exception as e:
            logger.error(f"Failed to get health for module {module_id}: {e}")
            return None

    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get comprehensive health status for all registered modules.

        Returns:
            Dict[str, Any]: System-wide health status including module health,
                           capability availability, and overall system status
        """
        system_health = {
            "total_modules": len(self._modules),
            "healthy_modules": 0,
            "degraded_modules": 0,
            "unhealthy_modules": 0,
            "module_health": {},
            "capability_availability": {},
            "overall_status": ModuleStatus.UNKNOWN.value,
        }

        # Check health of all modules
        for module_id in self._modules:
            health = await self.get_module_health(module_id, force_check=True)
            if health:
                system_health["module_health"][module_id] = health.to_dict()

                if health.is_healthy:
                    system_health["healthy_modules"] += 1
                elif health.status == ModuleStatus.PARTIALLY_AVAILABLE:
                    system_health["degraded_modules"] += 1
                else:
                    system_health["unhealthy_modules"] += 1

        # Determine overall system status
        total_modules = system_health["total_modules"]
        if total_modules == 0:
            system_health["overall_status"] = ModuleStatus.UNKNOWN.value
        elif system_health["unhealthy_modules"] == 0 and system_health["degraded_modules"] == 0:
            system_health["overall_status"] = ModuleStatus.AVAILABLE.value
        elif system_health["unhealthy_modules"] == 0:
            system_health["overall_status"] = ModuleStatus.PARTIALLY_AVAILABLE.value
        else:
            system_health["overall_status"] = ModuleStatus.ERROR.value

        # Check capability availability
        for capability_name, module_ids in self._capability_index.items():
            available_count = 0
            for module_id in module_ids:
                if module_id in self._modules:
                    health = await self.get_module_health(module_id)
                    if health and health.is_healthy:
                        available_count += 1

            system_health["capability_availability"][capability_name] = {
                "total_providers": len(module_ids),
                "available_providers": available_count,
                "fully_available": available_count == len(module_ids),
            }

        return system_health

    async def validate_all_modules(self) -> Dict[str, Dict[str, bool]]:
        """
        Validate RM compliance for all registered modules.

        Returns:
            Dict[str, Dict[str, bool]]: Compliance validation results for each module
        """
        validation_results = {}

        for module_id, module in self._modules.items():
            try:
                compliance = await module.validate_rm_compliance()
                validation_results[module_id] = compliance
            except Exception as e:
                validation_results[module_id] = {
                    "error": str(e),
                    "compliance_check_failed": True,
                }

        return validation_results

    def _index_module_capabilities(self, module_id: str, module: ReflectiveModule) -> None:
        """Index the capabilities of a module for discovery"""
        try:
            # Get capabilities synchronously for indexing
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context, schedule the capability check
                asyncio.create_task(self._async_index_capabilities(module_id, module))
            else:
                # If we're in a sync context, we can't get capabilities yet
                # They'll be indexed when first accessed
                pass
        except Exception as e:
            logger.warning(f"Could not index capabilities for {module_id}: {e}")

    async def _async_index_capabilities(self, module_id: str, module: ReflectiveModule) -> None:
        """Asynchronously index module capabilities"""
        try:
            capabilities = await module.get_module_capabilities()
            for capability in capabilities:
                if capability.name not in self._capability_index:
                    self._capability_index[capability.name] = []
                if module_id not in self._capability_index[capability.name]:
                    self._capability_index[capability.name].append(module_id)
        except Exception as e:
            logger.warning(f"Failed to index capabilities for {module_id}: {e}")

    def _remove_module_capabilities(self, module_id: str, module: ReflectiveModule) -> None:
        """Remove module capabilities from the index"""
        for capability_name, module_ids in list(self._capability_index.items()):
            if module_id in module_ids:
                module_ids.remove(module_id)
                if not module_ids:
                    del self._capability_index[capability_name]

    async def start_health_monitoring(self, interval: float = 30.0) -> None:
        """
        Start background health monitoring for all modules.

        Args:
            interval: Health check interval in seconds
        """
        self._health_check_interval = interval

        async def health_monitor():
            while True:
                try:
                    await self.get_system_health()
                    await asyncio.sleep(interval)
                except Exception as e:
                    logger.error(f"Health monitoring error: {e}")
                    await asyncio.sleep(interval)

        asyncio.create_task(health_monitor())
        logger.info(f"Started health monitoring with {interval}s interval")


# Global registry instance
_global_registry: Optional[ReflectiveModuleRegistry] = None


def get_global_registry() -> ReflectiveModuleRegistry:
    """Get the global RM registry instance"""
    global _global_registry
    if _global_registry is None:
        _global_registry = ReflectiveModuleRegistry()
    return _global_registry


def register_global_module(
    module: ReflectiveModule,
    module_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Register a module with the global registry"""
    return get_global_registry().register_module(module, module_id, metadata)


def get_global_module(module_id: str) -> Optional[ReflectiveModule]:
    """Get a module from the global registry"""
    return get_global_registry().get_module(module_id)
