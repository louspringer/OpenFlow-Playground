"""
RM-DDD Registry

Global registry for Reflective Module discovery, registration, and health monitoring.
"""

from __future__ import annotations
import asyncio
import time
import uuid
from typing import Dict, Iterable, List, Optional, Any
from contextlib import asynccontextmanager

from .types import ModuleHealth, ModuleStatus


class ModuleRegistry:
    """Global registry for RM-DDD modules"""

    def __init__(self) -> None:
        self._by_id: Dict[str, Any] = {}
        self._by_name: Dict[str, str] = {}  # name -> id
        self._by_domain: Dict[str, List[str]] = {}  # domain -> list of ids
        self._lock = asyncio.Lock()
        self._health_cache: Dict[str, ModuleHealth] = {}
        self._last_health_check: Dict[str, float] = {}

    async def register(self, module: Any) -> str:
        """Register a module with the registry"""
        async with self._lock:
            # Generate ID if not provided
            if not hasattr(module, "module_id") or not module.module_id:
                module.module_id = f"{module.__class__.__name__}_{uuid.uuid4().hex[:8]}"

            module_id = module.module_id
            self._by_id[module_id] = module
            self._by_name[module.__class__.__name__] = module_id

            # Track by domain if it's a domain module
            if hasattr(module, "domain_context"):
                domain = module.domain_context
                if domain not in self._by_domain:
                    self._by_domain[domain] = []
                self._by_domain[domain].append(module_id)

            return module_id

    async def unregister(self, module_id: str) -> bool:
        """Unregister a module from the registry"""
        async with self._lock:
            if module_id not in self._by_id:
                return False

            module = self._by_id[module_id]
            del self._by_id[module_id]

            # Remove from name mapping
            for name, mid in list(self._by_name.items()):
                if mid == module_id:
                    del self._by_name[name]
                    break

            # Remove from domain mapping
            if hasattr(module, "domain_context"):
                domain = module.domain_context
                if domain in self._by_domain and module_id in self._by_domain[domain]:
                    self._by_domain[domain].remove(module_id)
                    if not self._by_domain[domain]:
                        del self._by_domain[domain]

            # Clear health cache
            if module_id in self._health_cache:
                del self._health_cache[module_id]
            if module_id in self._last_health_check:
                del self._last_health_check[module_id]

            return True

    async def get(self, module_id: str) -> Optional[Any]:
        """Get module by ID"""
        return self._by_id.get(module_id)

    async def by_name(self, name: str) -> Optional[Any]:
        """Get module by class name"""
        module_id = self._by_name.get(name)
        return self._by_id.get(module_id) if module_id else None

    async def by_domain(self, domain: str) -> List[Any]:
        """Get all modules in a domain"""
        module_ids = self._by_domain.get(domain, [])
        return [self._by_id[mid] for mid in module_ids if mid in self._by_id]

    async def list_all(self) -> List[Any]:
        """Get all registered modules"""
        return list(self._by_id.values())

    async def health(self, only: Optional[Iterable[str]] = None, use_cache: bool = True) -> Dict[str, ModuleHealth]:
        """Get health status for modules"""
        ids = only or list(self._by_id.keys())
        results: Dict[str, ModuleHealth] = {}
        current_time = time.time()

        for module_id in ids:
            if module_id not in self._by_id:
                continue

            # Use cache if available and recent (within 30 seconds)
            if use_cache and module_id in self._health_cache and module_id in self._last_health_check and current_time - self._last_health_check[module_id] < 30:
                results[module_id] = self._health_cache[module_id]
                continue

            # Get fresh health status
            try:
                module = self._by_id[module_id]
                health = await module.get_module_status()
                results[module_id] = health

                # Update cache
                self._health_cache[module_id] = health
                self._last_health_check[module_id] = current_time
            except Exception as e:
                # Create error health status
                error_health = ModuleHealth(status=ModuleStatus.ERROR, message=f"Health check failed: {str(e)}")
                results[module_id] = error_health
                self._health_cache[module_id] = error_health
                self._last_health_check[module_id] = current_time

        return results

    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        all_health = await self.health()

        total_modules = len(all_health)
        healthy_modules = sum(1 for h in all_health.values() if h.status == ModuleStatus.AVAILABLE)
        degraded_modules = sum(1 for h in all_health.values() if h.status == ModuleStatus.DEGRADED)
        error_modules = sum(1 for h in all_health.values() if h.status == ModuleStatus.ERROR)

        overall_status = ModuleStatus.AVAILABLE
        if error_modules > 0:
            overall_status = ModuleStatus.ERROR
        elif degraded_modules > 0:
            overall_status = ModuleStatus.DEGRADED

        return {
            "overall_status": overall_status,
            "total_modules": total_modules,
            "healthy_modules": healthy_modules,
            "degraded_modules": degraded_modules,
            "error_modules": error_modules,
            "health_percentage": (healthy_modules / total_modules * 100) if total_modules > 0 else 100,
            "module_details": all_health,
        }

    async def get_capabilities(self) -> Dict[str, List[str]]:
        """Get all capabilities by module"""
        capabilities = {}
        for module_id, module in self._by_id.items():
            try:
                module_capabilities = await module.get_module_capabilities()
                capabilities[module_id] = [cap.name for cap in module_capabilities]
            except Exception:
                capabilities[module_id] = []
        return capabilities

    async def find_by_capability(self, capability_name: str) -> List[Any]:
        """Find modules that provide a specific capability"""
        matching_modules = []
        for module_id, module in self._by_id.items():
            try:
                capabilities = await module.get_module_capabilities()
                if any(cap.name == capability_name for cap in capabilities):
                    matching_modules.append(module)
            except Exception:
                continue
        return matching_modules


# Global registry instance
_registry = ModuleRegistry()


def get_global_registry() -> ModuleRegistry:
    """Get the global module registry"""
    return _registry
