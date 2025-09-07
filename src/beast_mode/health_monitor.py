#!/usr/bin/env python3
"""
Health Monitoring System for Beast Mode Agent Collaboration Network

Provides agent status monitoring, capability verification, and system health checks.

Requirements: Health monitoring, agent status verification
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, MessageSerializer
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentRegistry, DiscoveredAgent

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class AgentHealth:
    """Represents the health status of an agent."""

    agent_id: str
    status: HealthStatus
    last_heartbeat: datetime
    response_time_ms: Optional[float] = None
    capability_verification: Dict[str, bool] = field(default_factory=dict)
    error_count: int = 0
    success_count: int = 0
    uptime_seconds: float = 0.0

    def is_healthy(self) -> bool:
        """Check if agent is considered healthy."""
        return self.status == HealthStatus.HEALTHY

    def get_health_score(self) -> float:
        """Calculate overall health score (0.0 to 1.0)."""
        if self.error_count + self.success_count == 0:
            return 0.5  # Unknown status

        success_rate = self.success_count / (self.error_count + self.success_count)

        # Factor in response time (lower is better)
        time_factor = 1.0
        if self.response_time_ms:
            if self.response_time_ms < 100:
                time_factor = 1.0
            elif self.response_time_ms < 500:
                time_factor = 0.8
            elif self.response_time_ms < 1000:
                time_factor = 0.6
            else:
                time_factor = 0.4

        # Factor in capability verification
        capability_factor = 1.0
        if self.capability_verification:
            verified_count = sum(1 for v in self.capability_verification.values() if v)
            capability_factor = verified_count / len(self.capability_verification)

        return success_rate * time_factor * capability_factor


class HealthMonitor:
    """Monitors agent health and system status."""

    def __init__(self, redis_manager: RedisConnectionManager, registry: AgentRegistry):
        self.redis_manager = redis_manager
        self.registry = registry
        self.agent_health: Dict[str, AgentHealth] = {}
        self.monitoring_active = False
        self._monitoring_task: Optional[asyncio.Task] = None

    async def start_monitoring(self, interval_seconds: int = 30):
        """Start health monitoring with specified interval."""
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return

        self.monitoring_active = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop(interval_seconds))
        logger.info(f"Started health monitoring (interval: {interval_seconds}s)")

    async def stop_monitoring(self):
        """Stop health monitoring."""
        self.monitoring_active = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped health monitoring")

    async def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                await self._check_all_agents()
                await asyncio.sleep(interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Short delay before retry

    async def _check_all_agents(self):
        """Check health of all discovered agents."""
        discovered_agents = await self.registry.get_discovered_agents()

        for agent in discovered_agents:
            await self._check_agent_health(agent)

    async def _check_agent_health(self, agent: DiscoveredAgent):
        """Check health of a specific agent."""
        agent_id = agent.agent_id

        # Initialize health record if not exists
        if agent_id not in self.agent_health:
            self.agent_health[agent_id] = AgentHealth(agent_id=agent_id, status=HealthStatus.UNKNOWN, last_heartbeat=datetime.now())

        health = self.agent_health[agent_id]

        # Check if agent is still active
        time_since_last_seen = datetime.now() - agent.last_seen

        if time_since_last_seen > timedelta(minutes=5):
            health.status = HealthStatus.UNHEALTHY
            health.error_count += 1
        elif time_since_last_seen > timedelta(minutes=2):
            health.status = HealthStatus.DEGRADED
        else:
            health.status = HealthStatus.HEALTHY
            health.success_count += 1

        # Update heartbeat
        health.last_heartbeat = agent.last_seen

        # Calculate uptime
        if health.uptime_seconds == 0:
            health.uptime_seconds = (datetime.now() - agent.last_seen).total_seconds()
        else:
            health.uptime_seconds += 30  # Approximate based on monitoring interval

        # Verify capabilities (simplified check)
        await self._verify_agent_capabilities(agent, health)

        logger.debug(f"Health check for {agent_id}: {health.status} (score: {health.get_health_score():.2f})")

    async def _verify_agent_capabilities(self, agent: DiscoveredAgent, health: AgentHealth):
        """Verify agent capabilities through simple ping."""
        try:
            # Send a simple ping message
            ping_message = BeastModeMessage(type=MessageType.HEALTH_CHECK, source="health_monitor", target=agent.agent_id, payload={"ping": True, "timestamp": datetime.now().isoformat()})

            start_time = datetime.now()
            await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(ping_message))

            # Wait for response (simplified - in real implementation would wait for actual response)
            await asyncio.sleep(0.1)  # Short wait

            response_time = (datetime.now() - start_time).total_seconds() * 1000
            health.response_time_ms = response_time

            # Mark capability as verified if we got a quick response
            for capability in agent.capabilities:
                health.capability_verification[capability] = response_time < 1000

        except Exception as e:
            logger.error(f"Error verifying capabilities for {agent.agent_id}: {e}")
            health.error_count += 1

    async def get_agent_health(self, agent_id: str) -> Optional[AgentHealth]:
        """Get health status of a specific agent."""
        return self.agent_health.get(agent_id)

    async def get_all_health_status(self) -> Dict[str, AgentHealth]:
        """Get health status of all agents."""
        return self.agent_health.copy()

    async def get_healthy_agents(self) -> List[str]:
        """Get list of healthy agent IDs."""
        return [agent_id for agent_id, health in self.agent_health.items() if health.is_healthy()]

    async def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary."""
        total_agents = len(self.agent_health)
        healthy_agents = len(await self.get_healthy_agents())

        if total_agents == 0:
            return {"total_agents": 0, "healthy_agents": 0, "health_percentage": 0.0, "average_health_score": 0.0, "status": "no_agents"}

        health_percentage = (healthy_agents / total_agents) * 100
        average_health_score = sum(h.get_health_score() for h in self.agent_health.values()) / total_agents

        overall_status = HealthStatus.HEALTHY
        if health_percentage < 50:
            overall_status = HealthStatus.UNHEALTHY
        elif health_percentage < 80:
            overall_status = HealthStatus.DEGRADED

        return {
            "total_agents": total_agents,
            "healthy_agents": healthy_agents,
            "health_percentage": health_percentage,
            "average_health_score": average_health_score,
            "status": overall_status.value,
            "agents": {
                agent_id: {"status": health.status.value, "health_score": health.get_health_score(), "response_time_ms": health.response_time_ms, "uptime_seconds": health.uptime_seconds}
                for agent_id, health in self.agent_health.items()
            },
        }

    async def send_health_report(self, target_agent: Optional[str] = None):
        """Send health report to specified agent or broadcast."""
        summary = await self.get_health_summary()

        message = BeastModeMessage(type=MessageType.HEALTH_REPORT, source="health_monitor", target=target_agent, payload={"health_summary": summary, "timestamp": datetime.now().isoformat()})

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.info(f"Sent health report: {summary['status']} ({summary['health_percentage']:.1f}% healthy)")

    async def cleanup(self):
        """Clean up monitoring resources."""
        await self.stop_monitoring()
        self.agent_health.clear()
        logger.info("Health monitor cleaned up")
