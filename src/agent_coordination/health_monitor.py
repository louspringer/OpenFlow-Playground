#!/usr/bin/env python3
"""
Agent Health Monitor
Monitors health of individual agents and overall system health
"""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class HealthIndicator:
    """Individual health indicator"""

    name: str
    status: HealthStatus
    value: Any
    threshold: Optional[Any] = None
    last_updated: datetime = None
    description: str = ""

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.utcnow()


@dataclass
class AgentHealth:
    """Health status of an individual agent"""

    agent_id: str
    overall_status: HealthStatus
    indicators: Dict[str, HealthIndicator]
    last_heartbeat: datetime
    response_time_ms: Optional[float] = None
    error_count: int = 0
    last_error: Optional[str] = None


class AgentHealthMonitor:
    """
    Monitors health of agents and overall system
    Provides health indicators for multi-perspective validation
    """

    def __init__(self, heartbeat_timeout_seconds: int = 60):
        self.heartbeat_timeout = heartbeat_timeout_seconds
        self.agent_health: Dict[str, AgentHealth] = {}
        self.system_health_indicators: Dict[str, HealthIndicator] = {}
        self.logger = logging.getLogger(__name__)

        # Initialize system health indicators
        self._initialize_system_indicators()

    def _initialize_system_indicators(self):
        """Initialize system-level health indicators"""
        self.system_health_indicators = {
            "total_agents": HealthIndicator(name="total_agents", status=HealthStatus.UNKNOWN, value=0, description="Total number of registered agents"),
            "healthy_agents": HealthIndicator(name="healthy_agents", status=HealthStatus.UNKNOWN, value=0, description="Number of healthy agents"),
            "degraded_agents": HealthIndicator(name="degraded_agents", status=HealthStatus.UNKNOWN, value=0, description="Number of degraded agents"),
            "critical_agents": HealthIndicator(name="critical_agents", status=HealthStatus.UNKNOWN, value=0, description="Number of critical agents"),
            "system_uptime": HealthIndicator(name="system_uptime", status=HealthStatus.UNKNOWN, value=0.0, description="System uptime percentage"),
        }

    def register_agent(self, agent_id: str, capabilities: List[str] = None) -> bool:
        """Register a new agent for health monitoring"""
        if agent_id in self.agent_health:
            self.logger.warning(f"Agent {agent_id} already registered")
            return False

        if capabilities is None:
            capabilities = []

        # Initialize agent health
        agent_health = AgentHealth(
            agent_id=agent_id,
            overall_status=HealthStatus.UNKNOWN,
            indicators={
                "heartbeat": HealthIndicator(name="heartbeat", status=HealthStatus.UNKNOWN, value=False, description="Agent heartbeat status"),
                "response_time": HealthIndicator(name="response_time", status=HealthStatus.UNKNOWN, value=None, description="Agent response time in milliseconds"),
                "error_rate": HealthIndicator(name="error_rate", status=HealthStatus.UNKNOWN, value=0.0, description="Agent error rate"),
                "capabilities": HealthIndicator(name="capabilities", status=HealthStatus.HEALTHY, value=capabilities, description="Agent capabilities"),
            },
            last_heartbeat=datetime.utcnow(),
        )

        self.agent_health[agent_id] = agent_health
        self._update_system_indicators()

        self.logger.info(f"Registered agent {agent_id} with capabilities: {capabilities}")
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from health monitoring"""
        if agent_id not in self.agent_health:
            self.logger.warning(f"Agent {agent_id} not registered")
            return False

        del self.agent_health[agent_id]
        self._update_system_indicators()

        self.logger.info(f"Unregistered agent {agent_id}")
        return True

    def update_heartbeat(self, agent_id: str, response_time_ms: Optional[float] = None) -> bool:
        """Update agent heartbeat"""
        if agent_id not in self.agent_health:
            self.logger.warning(f"Agent {agent_id} not registered")
            return False

        agent_health = self.agent_health[agent_id]
        agent_health.last_heartbeat = datetime.utcnow()

        if response_time_ms is not None:
            agent_health.response_time_ms = response_time_ms
            agent_health.indicators["response_time"].value = response_time_ms
            agent_health.indicators["response_time"].last_updated = datetime.utcnow()

        # Update heartbeat indicator
        agent_health.indicators["heartbeat"].value = True
        agent_health.indicators["heartbeat"].status = HealthStatus.HEALTHY
        agent_health.indicators["heartbeat"].last_updated = datetime.utcnow()

        # Update overall agent health
        self._update_agent_health(agent_id)
        self._update_system_indicators()

        return True

    def report_error(self, agent_id: str, error_message: str) -> bool:
        """Report an error for an agent"""
        if agent_id not in self.agent_health:
            self.logger.warning(f"Agent {agent_id} not registered")
            return False

        agent_health = self.agent_health[agent_id]
        agent_health.error_count += 1
        agent_health.last_error = error_message

        # Update error rate indicator
        error_rate = agent_health.error_count / max(1, self._get_agent_uptime_minutes(agent_id))
        agent_health.indicators["error_rate"].value = error_rate
        agent_health.indicators["error_rate"].last_updated = datetime.utcnow()

        # Update overall agent health
        self._update_agent_health(agent_id)
        self._update_system_indicators()

        self.logger.warning(f"Agent {agent_id} error: {error_message}")
        return True

    def get_agent_health(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get health status of a specific agent"""
        if agent_id not in self.agent_health:
            return None

        agent_health = self.agent_health[agent_id]
        return {
            "agent_id": agent_id,
            "overall_status": agent_health.overall_status.value,
            "last_heartbeat": agent_health.last_heartbeat.isoformat(),
            "response_time_ms": agent_health.response_time_ms,
            "error_count": agent_health.error_count,
            "last_error": agent_health.last_error,
            "indicators": {
                name: {"status": indicator.status.value, "value": indicator.value, "last_updated": indicator.last_updated.isoformat(), "description": indicator.description}
                for name, indicator in agent_health.indicators.items()
            },
        }

    def get_all_agent_health(self) -> Dict[str, str]:
        """Get health status of all agents (simplified for compatibility)"""
        return {agent_id: agent_health.overall_status.value for agent_id, agent_health in self.agent_health.items()}

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        return {
            "overall_health": self._calculate_system_health().value,
            "total_agents": len(self.agent_health),
            "healthy_agents": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.HEALTHY),
            "degraded_agents": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.DEGRADED),
            "critical_agents": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.CRITICAL),
            "system_uptime": self._calculate_system_uptime(),
            "indicators": {
                name: {"status": indicator.status.value, "value": indicator.value, "last_updated": indicator.last_updated.isoformat(), "description": indicator.description}
                for name, indicator in self.system_health_indicators.items()
            },
        }

    def check_agent_health(self, agent_id: str) -> HealthStatus:
        """Check if an agent is healthy"""
        if agent_id not in self.agent_health:
            return HealthStatus.UNKNOWN

        agent_health = self.agent_health[agent_id]

        # Check heartbeat timeout
        time_since_heartbeat = datetime.utcnow() - agent_health.last_heartbeat
        if time_since_heartbeat.total_seconds() > self.heartbeat_timeout:
            return HealthStatus.CRITICAL

        return agent_health.overall_status

    def get_unhealthy_agents(self) -> List[str]:
        """Get list of unhealthy agents"""
        unhealthy = []
        for agent_id, agent_health in self.agent_health.items():
            if agent_health.overall_status in [HealthStatus.DEGRADED, HealthStatus.CRITICAL]:
                unhealthy.append(agent_id)
        return unhealthy

    def _update_agent_health(self, agent_id: str):
        """Update overall health status of an agent"""
        agent_health = self.agent_health[agent_id]

        # Check heartbeat
        time_since_heartbeat = datetime.utcnow() - agent_health.last_heartbeat
        if time_since_heartbeat.total_seconds() > self.heartbeat_timeout:
            agent_health.overall_status = HealthStatus.CRITICAL
            agent_health.indicators["heartbeat"].status = HealthStatus.CRITICAL
            agent_health.indicators["heartbeat"].value = False
            return

        # Check error rate
        error_rate = agent_health.indicators["error_rate"].value
        if error_rate > 0.1:  # 10% error rate threshold
            agent_health.overall_status = HealthStatus.CRITICAL
        elif error_rate > 0.05:  # 5% error rate threshold
            agent_health.overall_status = HealthStatus.DEGRADED
        else:
            agent_health.overall_status = HealthStatus.HEALTHY

        # Check response time
        if agent_health.response_time_ms is not None:
            if agent_health.response_time_ms > 5000:  # 5 second threshold
                if agent_health.overall_status == HealthStatus.HEALTHY:
                    agent_health.overall_status = HealthStatus.DEGRADED
            elif agent_health.response_time_ms > 10000:  # 10 second threshold
                agent_health.overall_status = HealthStatus.CRITICAL

    def _update_system_indicators(self):
        """Update system-level health indicators"""
        total_agents = len(self.agent_health)
        healthy_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.HEALTHY)
        degraded_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.DEGRADED)
        critical_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.CRITICAL)

        self.system_health_indicators["total_agents"].value = total_agents
        self.system_health_indicators["healthy_agents"].value = healthy_agents
        self.system_health_indicators["degraded_agents"].value = degraded_agents
        self.system_health_indicators["critical_agents"].value = critical_agents

        # Update system uptime
        uptime = self._calculate_system_uptime()
        self.system_health_indicators["system_uptime"].value = uptime

        # Update indicator statuses
        if critical_agents > 0:
            self.system_health_indicators["critical_agents"].status = HealthStatus.CRITICAL
        elif degraded_agents > total_agents * 0.3:  # 30% degraded threshold
            self.system_health_indicators["degraded_agents"].status = HealthStatus.DEGRADED
        else:
            self.system_health_indicators["healthy_agents"].status = HealthStatus.HEALTHY

    def _calculate_system_health(self) -> HealthStatus:
        """Calculate overall system health"""
        if not self.agent_health:
            return HealthStatus.UNKNOWN

        critical_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.CRITICAL)
        degraded_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.DEGRADED)
        total_agents = len(self.agent_health)

        if critical_agents > 0:
            return HealthStatus.CRITICAL
        elif degraded_agents > total_agents * 0.3:  # 30% degraded threshold
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY

    def _calculate_system_uptime(self) -> float:
        """Calculate system uptime percentage"""
        if not self.agent_health:
            return 0.0

        healthy_agents = sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.HEALTHY)
        total_agents = len(self.agent_health)

        return (healthy_agents / total_agents) * 100.0 if total_agents > 0 else 0.0

    def _get_agent_uptime_minutes(self, agent_id: str) -> float:
        """Get agent uptime in minutes (simplified)"""
        if agent_id not in self.agent_health:
            return 0.0

        # Simplified uptime calculation
        return 60.0  # Assume 1 hour for simplicity

    def cleanup_stale_agents(self, stale_timeout_minutes: int = 30):
        """Clean up agents that haven't sent heartbeats in a while"""
        current_time = datetime.utcnow()
        stale_agents = []

        for agent_id, agent_health in self.agent_health.items():
            time_since_heartbeat = current_time - agent_health.last_heartbeat
            if time_since_heartbeat.total_seconds() > (stale_timeout_minutes * 60):
                stale_agents.append(agent_id)

        for agent_id in stale_agents:
            self.logger.warning(f"Removing stale agent: {agent_id}")
            del self.agent_health[agent_id]

        if stale_agents:
            self._update_system_indicators()
            self.logger.info(f"Cleaned up {len(stale_agents)} stale agents")

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        return {
            "system_health": self.get_system_health(),
            "agent_count": len(self.agent_health),
            "unhealthy_agents": self.get_unhealthy_agents(),
            "health_distribution": {
                "healthy": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.HEALTHY),
                "degraded": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.DEGRADED),
                "critical": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.CRITICAL),
                "unknown": sum(1 for ah in self.agent_health.values() if ah.overall_status == HealthStatus.UNKNOWN),
            },
        }
