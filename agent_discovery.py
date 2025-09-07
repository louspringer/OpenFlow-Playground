import asyncio
import logging
from typing import Dict, List, Optional, Set, Callable, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from message_models import BeastModeMessage, MessageType, AgentCapabilities, MessageSerializer
from redis_foundation import RedisConnectionManager

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredAgent:
    agent_id: str
    capabilities: List[str]
    specializations: List[str]
    availability: str
    last_seen: datetime
    collaboration_history: List[str] = field(default_factory=list)
    trust_score: float = 0.5
    response_count: int = 0
    success_count: int = 0

    def update_trust_score(self, success: bool):
        self.response_count += 1
        if success:
            self.success_count += 1
        if self.response_count > 0:
            success_rate = self.success_count / self.response_count
            time_decay = 0.95 ** (self.response_count - 1)
            self.trust_score = min(1.0, success_rate * time_decay)

    def is_available(self) -> bool:
        return self.availability in ["ready_for_business", "busy"] and datetime.now() - self.last_seen < timedelta(minutes=5)

    def matches_capabilities(self, required_capabilities: List[str]) -> bool:
        return all(cap in self.capabilities for cap in required_capabilities)

    def get_capability_match_score(self, required_capabilities: List[str]) -> float:
        if not required_capabilities:
            return 0.0
        matches = sum(1 for cap in required_capabilities if cap in self.capabilities)
        return matches / len(required_capabilities)


class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, DiscoveredAgent] = {}
        self.capability_index: Dict[str, Set[str]] = {}
        self._lock = asyncio.Lock()

    async def register_agent(self, capabilities: AgentCapabilities) -> None:
        async with self._lock:
            agent_id = capabilities.agent_id

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

            self._update_capability_index(agent_id, capabilities.capabilities)
            logger.info(f"Registered agent '{agent_id}' with capabilities: {capabilities.capabilities}")

    def _update_capability_index(self, agent_id: str, capabilities: List[str]) -> None:
        for cap_set in self.capability_index.values():
            cap_set.discard(agent_id)
        for capability in capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = set()
            self.capability_index[capability].add(agent_id)

    async def find_agents_by_capabilities(self, required_capabilities: List[str]) -> List[DiscoveredAgent]:
        if not required_capabilities:
            return list(self.agents.values())

        candidate_agents = set()
        for capability in required_capabilities:
            if capability in self.capability_index:
                if not candidate_agents:
                    candidate_agents = self.capability_index[capability].copy()
                else:
                    candidate_agents &= self.capability_index[capability]
            else:
                return []

        agents = [self.agents[agent_id] for agent_id in candidate_agents]
        agents.sort(key=lambda a: (a.trust_score, a.get_capability_match_score(required_capabilities)), reverse=True)
        return agents

    async def get_agent(self, agent_id: str) -> Optional[DiscoveredAgent]:
        return self.agents.get(agent_id)

    async def get_available_agents(self) -> List[DiscoveredAgent]:
        return [agent for agent in self.agents.values() if agent.is_available()]

    async def update_agent_trust(self, agent_id: str, success: bool) -> None:
        if agent_id in self.agents:
            self.agents[agent_id].update_trust_score(success)


class AgentDiscoveryManager:
    def __init__(self, agent_id: str, capabilities: List[str], redis_manager: RedisConnectionManager):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.redis_manager = redis_manager
        self.registry = AgentRegistry()

    async def announce_presence(self) -> None:
        capabilities_data = AgentCapabilities(agent_id=self.agent_id, capabilities=self.capabilities, availability="ready_for_business", specializations=self.capabilities, collaboration_history=[])

        message = BeastModeMessage(type=MessageType.AGENT_DISCOVERY, source=self.agent_id, payload={"capabilities": capabilities_data.to_dict()})

        await self.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))
        logger.info(f"Agent '{self.agent_id}' announced presence with capabilities: {self.capabilities}")

    async def get_discovered_agents(self) -> List[DiscoveredAgent]:
        return list(self.registry.agents.values())
