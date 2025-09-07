#!/usr/bin/env python3
"""
Agent Discovery System for Beast Mode Agent Collaboration Network

Implements agent presence announcement, capability broadcasting, discovery response handling,
and agent registry for tracking discovered agents.

Requirements: 2.1, 2.2, 2.3, 2.4
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Callable, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities, MessageSerializer
from beast_mode.redis_foundation import RedisConnectionManager

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredAgent:
    """Represents a discovered agent with its capabilities and status."""

    agent_id: str
    capabilities: List[str]
    specializations: List[str]
    availability: str
    last_seen: datetime
    collaboration_history: List[str] = field(default_factory=list)
    trust_score: float = 0.5  # Initial trust score
    response_count: int = 0
    success_count: int = 0

    def update_trust_score(self, success: bool):
        """Update trust score based on collaboration success."""
        self.response_count += 1
        if success:
            self.success_count += 1

        # Simple trust calculation: success rate with some decay
        if self.response_count > 0:
            success_rate = self.success_count / self.response_count
            # Apply slight decay to older interactions
            time_decay = 0.95 ** (self.response_count - 1)
            self.trust_score = min(1.0, success_rate * time_decay)

    def is_available(self) -> bool:
        """Check if agent is currently available."""
        return self.availability in ["ready_for_business", "busy"] and datetime.now() - self.last_seen < timedelta(minutes=5)

    def matches_capabilities(self, required_capabilities: List[str]) -> bool:
        """Check if agent has all required capabilities."""
        return all(cap in self.capabilities for cap in required_capabilities)

    def get_capability_match_score(self, required_capabilities: List[str]) -> float:
        """Calculate how well this agent matches required capabilities."""
        if not required_capabilities:
            return 0.0

        matches = sum(1 for cap in required_capabilities if cap in self.capabilities)
        return matches / len(required_capabilities)


class AgentRegistry:
    """Manages discovered agents and their capabilities."""

    def __init__(self):
        self.agents: Dict[str, DiscoveredAgent] = {}
        self.capability_index: Dict[str, Set[str]] = {}  # capability -> set of agent_ids
        self._lock = asyncio.Lock()

    async def register_agent(self, capabilities: AgentCapabilities) -> None:
        """Register or update an agent's capabilities."""
        async with self._lock:
            agent_id = capabilities.agent_id

            # Create or update agent
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.capabilities = capabilities.capabilities
                agent.specializations = capabilities.specializations
                agent.availability = capabilities.availability
                agent.last_seen = datetime.now()
            else:
                agent = DiscoveredAgent(
                    agent_id=agent_id,
                    capabilities=capabilities.capabilities,
                    specializations=capabilities.specializations,
                    availability=capabilities.availability,
                    last_seen=datetime.now(),
                    collaboration_history=capabilities.collaboration_history,
                )
                self.agents[agent_id] = agent

            # Update capability index
            self._update_capability_index(agent_id, capabilities.capabilities)

            logger.info(f"Registered agent '{agent_id}' with capabilities: {capabilities.capabilities}")

    def _update_capability_index(self, agent_id: str, capabilities: List[str]) -> None:
        """Update the capability index for efficient searching."""
        # Remove agent from all capabilities first
        for cap_set in self.capability_index.values():
            cap_set.discard(agent_id)

        # Add agent to relevant capabilities
        for capability in capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = set()
            self.capability_index[capability].add(agent_id)

    async def find_agents_by_capabilities(self, required_capabilities: List[str]) -> List[DiscoveredAgent]:
        """Find agents that have the required capabilities."""
        if not required_capabilities:
            return list(self.agents.values())

        # Find agents that have all required capabilities
        candidate_agents = set()
        for capability in required_capabilities:
            if capability in self.capability_index:
                if not candidate_agents:
                    candidate_agents = self.capability_index[capability].copy()
                else:
                    candidate_agents &= self.capability_index[capability]
            else:
                return []  # No agents have this capability

        # Return agents sorted by trust score and capability match
        agents = [self.agents[agent_id] for agent_id in candidate_agents]
        agents.sort(key=lambda a: (a.trust_score, a.get_capability_match_score(required_capabilities)), reverse=True)

        return agents

    async def get_agent(self, agent_id: str) -> Optional[DiscoveredAgent]:
        """Get a specific agent by ID."""
        return self.agents.get(agent_id)

    async def get_available_agents(self) -> List[DiscoveredAgent]:
        """Get all currently available agents."""
        return [agent for agent in self.agents.values() if agent.is_available()]

    async def update_agent_trust(self, agent_id: str, success: bool) -> None:
        """Update an agent's trust score based on collaboration success."""
        if agent_id in self.agents:
            self.agents[agent_id].update_trust_score(success)

    async def cleanup_stale_agents(self, max_age_minutes: int = 30) -> None:
        """Remove agents that haven't been seen recently."""
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        stale_agents = [agent_id for agent_id, agent in self.agents.items() if agent.last_seen < cutoff_time]

        for agent_id in stale_agents:
            agent = self.agents.pop(agent_id)
            # Remove from capability index
            for cap_set in self.capability_index.values():
                cap_set.discard(agent_id)
            logger.info(f"Removed stale agent: {agent_id}")


class AgentDiscoveryManager:
    """Manages agent discovery protocol and interactions."""

    def __init__(self, agent_id: str, capabilities: List[str], redis_manager: RedisConnectionManager):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.redis_manager = redis_manager
        self.registry = AgentRegistry()
        self.discovery_handlers: Dict[MessageType, Callable[[BeastModeMessage], Any]] = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup message handlers for discovery protocol."""
        self.discovery_handlers = {
            MessageType.AGENT_DISCOVERY: self._handle_agent_discovery,
            MessageType.AGENT_RESPONSE: self._handle_agent_response,
            MessageType.HELP_WANTED: self._handle_help_wanted,
            MessageType.HELP_RESPONSE: self._handle_help_response,
        }

    async def announce_presence(self) -> None:
        """Announce this agent's presence and capabilities."""
        capabilities_data = AgentCapabilities(
            agent_id=self.agent_id,
            capabilities=self.capabilities,
            availability="ready_for_business",
            specializations=self.capabilities,  # Use capabilities as specializations for now
            collaboration_history=[],
        )

        message = BeastModeMessage(type=MessageType.AGENT_DISCOVERY, source=self.agent_id, payload={"capabilities": capabilities_data.to_dict()})

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.info(f"Agent '{self.agent_id}' announced presence with capabilities: {self.capabilities}")

    async def _handle_agent_discovery(self, message: BeastModeMessage) -> None:
        """Handle agent discovery messages from other agents."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            capabilities_data = AgentCapabilities(**message.payload["capabilities"])
            await self.registry.register_agent(capabilities_data)

            # Respond with our own capabilities
            await self._send_discovery_response(message.source)

        except Exception as e:
            logger.error(f"Error handling agent discovery from {message.source}: {e}")

    async def _handle_agent_response(self, message: BeastModeMessage) -> None:
        """Handle agent response messages."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            capabilities_data = AgentCapabilities(**message.payload["capabilities"])
            await self.registry.register_agent(capabilities_data)

        except Exception as e:
            logger.error(f"Error handling agent response from {message.source}: {e}")

    async def _handle_help_wanted(self, message: BeastModeMessage) -> None:
        """Handle help wanted messages and check if we can help."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            required_capabilities = message.payload.get("required_capabilities", [])
            if self._can_help_with(required_capabilities):
                await self._send_help_response(message.source, required_capabilities)

        except Exception as e:
            logger.error(f"Error handling help wanted from {message.source}: {e}")

    async def _handle_help_response(self, message: BeastModeMessage) -> None:
        """Handle help response messages."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            # Log that we received help response
            logger.info(f"Received help response from {message.source}")

        except Exception as e:
            logger.error(f"Error handling help response from {message.source}: {e}")

    def _can_help_with(self, required_capabilities: List[str]) -> bool:
        """Check if this agent can help with the required capabilities."""
        return all(cap in self.capabilities for cap in required_capabilities)

    async def _send_discovery_response(self, target_agent: str) -> None:
        """Send discovery response to a specific agent."""
        capabilities_data = AgentCapabilities(agent_id=self.agent_id, capabilities=self.capabilities, availability="ready_for_business", specializations=self.capabilities, collaboration_history=[])

        message = BeastModeMessage(type=MessageType.AGENT_RESPONSE, source=self.agent_id, target=target_agent, payload={"capabilities": capabilities_data.to_dict()})

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.debug(f"Sent discovery response to {target_agent}")

    async def _send_help_response(self, target_agent: str, required_capabilities: List[str]) -> None:
        """Send help response to a specific agent."""
        message = BeastModeMessage(
            type=MessageType.HELP_RESPONSE,
            source=self.agent_id,
            target=target_agent,
            payload={"offered_capabilities": required_capabilities, "message": f"I can help with: {', '.join(required_capabilities)}"},
        )

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.info(f"Offered help to {target_agent} for capabilities: {required_capabilities}")

    async def request_help(self, required_capabilities: List[str], description: str = "") -> List[DiscoveredAgent]:
        """Request help from agents with specific capabilities."""
        message = BeastModeMessage(
            type=MessageType.HELP_WANTED, source=self.agent_id, payload={"required_capabilities": required_capabilities, "description": description, "timestamp": datetime.now().isoformat()}
        )

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.info(f"Requested help for capabilities: {required_capabilities}")

        # Return agents that can help
        return await self.registry.find_agents_by_capabilities(required_capabilities)

    async def get_discovered_agents(self) -> List[DiscoveredAgent]:
        """Get all discovered agents."""
        return list(self.registry.agents.values())

    async def get_agents_by_capability(self, capability: str) -> List[DiscoveredAgent]:
        """Get agents that have a specific capability."""
        return await self.registry.find_agents_by_capabilities([capability])

    async def update_collaboration_success(self, agent_id: str, success: bool) -> None:
        """Update collaboration success for an agent."""
        await self.registry.update_agent_trust(agent_id, success)

    async def cleanup_stale_agents(self) -> None:
        """Clean up stale agents from registry."""
        await self.registry.cleanup_stale_agents()

    def get_handlers(self) -> Dict[MessageType, Callable[[BeastModeMessage], Any]]:
        """Get discovery message handlers for registration with bus client."""
        return self.discovery_handlers
