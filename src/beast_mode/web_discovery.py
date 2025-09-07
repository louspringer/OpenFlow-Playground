#!/usr/bin/env python3
"""
Web-Enhanced Discovery System for Beast Mode Agent Collaboration Network

Implements web-based service discovery using mDNS/Zeroconf for local network discovery
and HTTP-based discovery for remote agents.

Requirements: Web-based discovery, mDNS integration, HTTP discovery
"""

import asyncio
import logging
import json
import aiohttp
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from urllib.parse import urljoin

try:
    from zeroconf import ServiceInfo, Zeroconf, ServiceListener

    ZEROCONF_AVAILABLE = True
except ImportError:
    ZEROCONF_AVAILABLE = False
    ServiceInfo = None
    Zeroconf = None
    ServiceListener = None

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities
from beast_mode.redis_foundation import RedisConnectionManager

logger = logging.getLogger(__name__)


@dataclass
class WebDiscoveredAgent:
    """Represents an agent discovered via web protocols."""

    agent_id: str
    service_name: str
    service_type: str
    host: str
    port: int
    capabilities: List[str]
    specializations: List[str]
    availability: str
    last_seen: datetime
    discovery_method: str  # 'mdns', 'http', 'redis'
    http_endpoint: Optional[str] = None
    trust_score: float = 0.5

    def get_discovery_url(self) -> str:
        """Get the discovery URL for this agent."""
        if self.http_endpoint:
            return self.http_endpoint
        return f"http://{self.host}:{self.port}"


class WebDiscoveryListener(ServiceListener):
    """Listener for mDNS service discovery."""

    def __init__(self, discovery_manager):
        self.discovery_manager = discovery_manager
        self.discovered_services: Set[str] = set()

    def add_service(self, zeroconf, type, name):
        """Called when a new service is discovered."""
        info = zeroconf.get_service_info(type, name)
        if info and name not in self.discovered_services:
            self.discovered_services.add(name)
            asyncio.create_task(self._handle_service_discovery(info, name))

    def remove_service(self, zeroconf, type, name):
        """Called when a service is removed."""
        if name in self.discovered_services:
            self.discovered_services.remove(name)
            asyncio.create_task(self._handle_service_removal(name))

    def update_service(self, zeroconf, type, name):
        """Called when a service is updated."""
        info = zeroconf.get_service_info(type, name)
        if info:
            asyncio.create_task(self._handle_service_update(info, name))

    async def _handle_service_discovery(self, info, name):
        """Handle discovery of a new service."""
        try:
            # Extract agent information from service properties
            properties = {}
            for key, value in info.properties.items():
                properties[key.decode("utf-8")] = value.decode("utf-8")

            agent_id = properties.get("agent_id", name)
            capabilities = json.loads(properties.get("capabilities", "[]"))
            specializations = json.loads(properties.get("specializations", "[]"))

            # Create discovered agent
            discovered_agent = WebDiscoveredAgent(
                agent_id=agent_id,
                service_name=name,
                service_type=info.type,
                host=info.parsed_addresses()[0] if info.parsed_addresses() else "localhost",
                port=info.port,
                capabilities=capabilities,
                specializations=specializations,
                availability=properties.get("availability", "unknown"),
                last_seen=datetime.now(),
                discovery_method="mdns",
                http_endpoint=properties.get("http_endpoint"),
            )

            # Register with discovery manager
            await self.discovery_manager.register_web_agent(discovered_agent)
            logger.info(f"Discovered agent via mDNS: {agent_id} at {discovered_agent.get_discovery_url()}")

        except Exception as e:
            logger.error(f"Error handling service discovery for {name}: {e}")

    async def _handle_service_removal(self, name):
        """Handle removal of a service."""
        await self.discovery_manager.unregister_web_agent(name)
        logger.info(f"Service removed: {name}")

    async def _handle_service_update(self, info, name):
        """Handle update of a service."""
        # Similar to discovery but for updates
        await self._handle_service_discovery(info, name)


class WebDiscoveryManager:
    """Manages web-based agent discovery using mDNS and HTTP."""

    def __init__(self, agent_id: str, capabilities: List[str], redis_manager: RedisConnectionManager):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.redis_manager = redis_manager
        self.discovered_agents: Dict[str, WebDiscoveredAgent] = {}
        self.zeroconf = None
        self.listener = None
        self.http_server = None
        self.discovery_running = False

        # Service configuration
        self.service_type = "_beastmode._tcp.local."
        self.service_name = f"{agent_id}._beastmode._tcp.local."
        self.http_port = 8080

    async def start_discovery(self):
        """Start web-based discovery services."""
        logger.info("Starting web-based discovery...")

        # Start mDNS discovery
        if ZEROCONF_AVAILABLE:
            await self._start_mdns_discovery()
        else:
            logger.warning("Zeroconf not available, mDNS discovery disabled")

        # Start HTTP discovery server
        await self._start_http_discovery()

        # Announce our own service
        await self._announce_service()

        self.discovery_running = True
        logger.info("Web-based discovery started")

    async def stop_discovery(self):
        """Stop web-based discovery services."""
        logger.info("Stopping web-based discovery...")

        self.discovery_running = False

        # Stop mDNS
        if self.zeroconf:
            self.zeroconf.close()

        # Stop HTTP server
        if self.http_server:
            self.http_server.close()
            await self.http_server.wait_closed()

        logger.info("Web-based discovery stopped")

    async def _start_mdns_discovery(self):
        """Start mDNS service discovery."""
        if not ZEROCONF_AVAILABLE:
            return

        self.zeroconf = Zeroconf()
        self.listener = WebDiscoveryListener(self)

        # Browse for Beast Mode services
        self.zeroconf.add_service_listener(self.service_type, self.listener)
        logger.info(f"Started mDNS discovery for {self.service_type}")

    async def _start_http_discovery(self):
        """Start HTTP-based discovery server."""
        from aiohttp import web

        async def discovery_handler(request):
            """Handle discovery requests."""
            return web.json_response(
                {"agent_id": self.agent_id, "capabilities": self.capabilities, "availability": "ready_for_business", "timestamp": datetime.now().isoformat(), "discovery_method": "http"}
            )

        async def health_handler(request):
            """Handle health check requests."""
            return web.json_response({"status": "healthy", "agent_id": self.agent_id, "timestamp": datetime.now().isoformat()})

        async def capabilities_handler(request):
            """Handle capabilities requests."""
            return web.json_response({"agent_id": self.agent_id, "capabilities": self.capabilities, "specializations": self.capabilities, "availability": "ready_for_business"})

        # Create web application
        app = web.Application()
        app.router.add_get("/discovery", discovery_handler)
        app.router.add_get("/health", health_handler)
        app.router.add_get("/capabilities", capabilities_handler)

        # Start server
        self.http_server = web.AppRunner(app)
        await self.http_server.setup()
        site = web.TCPSite(self.http_server, "0.0.0.0", self.http_port)
        await site.start()

        logger.info(f"Started HTTP discovery server on port {self.http_port}")

    async def _announce_service(self):
        """Announce our service via mDNS."""
        if not ZEROCONF_AVAILABLE:
            return

        try:
            # Create service info
            properties = {
                "agent_id": self.agent_id,
                "capabilities": json.dumps(self.capabilities),
                "specializations": json.dumps(self.capabilities),
                "availability": "ready_for_business",
                "http_endpoint": f"http://localhost:{self.http_port}",
            }

            service_info = ServiceInfo(self.service_type, self.service_name, addresses=[b"\x7f\x00\x00\x01"], port=self.http_port, properties=properties)  # 127.0.0.1

            # Register service
            self.zeroconf.register_service(service_info)
            logger.info(f"Announced service: {self.service_name}")

        except Exception as e:
            logger.error(f"Error announcing service: {e}")

    async def register_web_agent(self, agent: WebDiscoveredAgent):
        """Register a web-discovered agent."""
        self.discovered_agents[agent.agent_id] = agent

        # Also register with Redis for compatibility
        capabilities_data = AgentCapabilities(
            agent_id=agent.agent_id, capabilities=agent.capabilities, availability=agent.availability, specializations=agent.specializations, collaboration_history=[]
        )

        # Send discovery message to Redis
        message = BeastModeMessage(type=MessageType.AGENT_DISCOVERY, source=agent.agent_id, payload={"capabilities": capabilities_data.to_dict()})

        await self.redis_manager.publish("beast_mode_network", message.to_json())
        logger.info(f"Registered web agent: {agent.agent_id}")

    async def unregister_web_agent(self, agent_id: str):
        """Unregister a web-discovered agent."""
        if agent_id in self.discovered_agents:
            del self.discovered_agents[agent_id]
            logger.info(f"Unregistered web agent: {agent_id}")

    async def discover_agents_http(self, discovery_urls: List[str]) -> List[WebDiscoveredAgent]:
        """Discover agents via HTTP requests."""
        discovered_agents = []

        async with aiohttp.ClientSession() as session:
            for url in discovery_urls:
                try:
                    async with session.get(f"{url}/discovery", timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()

                            agent = WebDiscoveredAgent(
                                agent_id=data["agent_id"],
                                service_name=data["agent_id"],
                                service_type="http",
                                host=url.split("://")[1].split(":")[0],
                                port=int(url.split(":")[-1]) if ":" in url else 80,
                                capabilities=data.get("capabilities", []),
                                specializations=data.get("capabilities", []),
                                availability=data.get("availability", "unknown"),
                                last_seen=datetime.now(),
                                discovery_method="http",
                                http_endpoint=url,
                            )

                            discovered_agents.append(agent)
                            await self.register_web_agent(agent)

                except Exception as e:
                    logger.error(f"Error discovering agent at {url}: {e}")

        return discovered_agents

    async def get_discovered_agents(self) -> List[WebDiscoveredAgent]:
        """Get all discovered agents."""
        return list(self.discovered_agents.values())

    async def find_agents_by_capabilities(self, required_capabilities: List[str]) -> List[WebDiscoveredAgent]:
        """Find agents with specific capabilities."""
        matching_agents = []

        for agent in self.discovered_agents.values():
            if all(cap in agent.capabilities for cap in required_capabilities):
                matching_agents.append(agent)

        # Sort by trust score
        matching_agents.sort(key=lambda a: a.trust_score, reverse=True)
        return matching_agents

    async def health_check_agents(self) -> Dict[str, bool]:
        """Perform health checks on discovered agents."""
        health_status = {}

        async with aiohttp.ClientSession() as session:
            for agent in self.discovered_agents.values():
                if agent.http_endpoint:
                    try:
                        async with session.get(f"{agent.http_endpoint}/health", timeout=3) as response:
                            health_status[agent.agent_id] = response.status == 200
                    except:
                        health_status[agent.agent_id] = False
                else:
                    health_status[agent.agent_id] = True  # Assume healthy if no HTTP endpoint

        return health_status

    async def get_discovery_summary(self) -> Dict[str, Any]:
        """Get summary of discovery status."""
        total_agents = len(self.discovered_agents)
        http_agents = len([a for a in self.discovered_agents.values() if a.discovery_method == "http"])
        mdns_agents = len([a for a in self.discovered_agents.values() if a.discovery_method == "mdns"])

        health_status = await self.health_check_agents()
        healthy_agents = sum(1 for status in health_status.values() if status)

        return {
            "total_agents": total_agents,
            "http_agents": http_agents,
            "mdns_agents": mdns_agents,
            "healthy_agents": healthy_agents,
            "health_percentage": (healthy_agents / total_agents * 100) if total_agents > 0 else 0,
            "discovery_running": self.discovery_running,
            "zeroconf_available": ZEROCONF_AVAILABLE,
        }
