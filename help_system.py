import asyncio
import logging
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from message_models import BeastModeMessage, MessageType, MessageSerializer
from agent_discovery import AgentDiscoveryManager, DiscoveredAgent

logger = logging.getLogger(__name__)


class HelpRequestStatus(str, Enum):
    PENDING = "pending"
    RESPONDED = "responded"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class HelpRequest:
    request_id: str
    requester_id: str
    required_capabilities: List[str]
    description: str
    status: HelpRequestStatus
    created_at: datetime
    responses: List[str] = field(default_factory=list)
    selected_responder: Optional[str] = None
    completed_at: Optional[datetime] = None
    success: Optional[bool] = None
    timeout_minutes: int = 30

    def is_expired(self) -> bool:
        return datetime.now() - self.created_at > timedelta(minutes=self.timeout_minutes)

    def add_response(self, agent_id: str) -> None:
        if agent_id not in self.responses:
            self.responses.append(agent_id)

    def select_responder(self, agent_id: str) -> None:
        self.selected_responder = agent_id
        self.status = HelpRequestStatus.IN_PROGRESS

    def mark_completed(self, success: bool) -> None:
        self.status = HelpRequestStatus.COMPLETED
        self.completed_at = datetime.now()
        self.success = success


class HelpSystemManager:
    def __init__(self, agent_id: str, discovery_manager: AgentDiscoveryManager):
        self.agent_id = agent_id
        self.discovery_manager = discovery_manager
        self.active_requests: Dict[str, HelpRequest] = {}
        self.completed_requests: List[HelpRequest] = []

    async def request_help(self, required_capabilities: List[str], description: str = "", timeout_minutes: int = 30) -> str:
        request_id = f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        help_request = HelpRequest(
            request_id=request_id,
            requester_id=self.agent_id,
            required_capabilities=required_capabilities,
            description=description,
            status=HelpRequestStatus.PENDING,
            created_at=datetime.now(),
            timeout_minutes=timeout_minutes,
        )

        self.active_requests[request_id] = help_request

        message = BeastModeMessage(
            type=MessageType.HELP_WANTED,
            source=self.agent_id,
            payload={"request_id": request_id, "required_capabilities": required_capabilities, "description": description, "timeout_minutes": timeout_minutes, "timestamp": datetime.now().isoformat()},
        )

        await self.discovery_manager.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))

        logger.info(f"Requested help (ID: {request_id}) for capabilities: {required_capabilities}")
        return request_id

    async def get_help_requests(self) -> List[HelpRequest]:
        return list(self.active_requests.values()) + self.completed_requests

    async def get_available_helpers(self, required_capabilities: List[str]) -> List[DiscoveredAgent]:
        return await self.discovery_manager.registry.find_agents_by_capabilities(required_capabilities)
