#!/usr/bin/env python3
"""
Help Wanted System for Beast Mode Agent Collaboration Network

Implements help request broadcasting, capability matching, help response generation,
and collaboration tracking with success metrics.

Requirements: 4.1, 4.2, 4.3, 4.4
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, MessageSerializer
from beast_mode.agent_discovery import AgentDiscoveryManager, DiscoveredAgent

logger = logging.getLogger(__name__)


class HelpRequestStatus(str, Enum):
    """Status of a help request."""

    PENDING = "pending"
    RESPONDED = "responded"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class HelpRequest:
    """Represents a help request with tracking information."""

    request_id: str
    requester_id: str
    required_capabilities: List[str]
    description: str
    status: HelpRequestStatus
    created_at: datetime
    responses: List[str] = field(default_factory=list)  # Agent IDs that responded
    selected_responder: Optional[str] = None
    completed_at: Optional[datetime] = None
    success: Optional[bool] = None
    timeout_minutes: int = 30

    def is_expired(self) -> bool:
        """Check if the help request has expired."""
        return datetime.now() - self.created_at > timedelta(minutes=self.timeout_minutes)

    def add_response(self, agent_id: str) -> None:
        """Add a response from an agent."""
        if agent_id not in self.responses:
            self.responses.append(agent_id)

    def select_responder(self, agent_id: str) -> None:
        """Select a responder for this help request."""
        self.selected_responder = agent_id
        self.status = HelpRequestStatus.IN_PROGRESS

    def mark_completed(self, success: bool) -> None:
        """Mark the help request as completed."""
        self.status = HelpRequestStatus.COMPLETED
        self.completed_at = datetime.now()
        self.success = success


@dataclass
class CollaborationMetrics:
    """Tracks collaboration success metrics."""

    total_requests: int = 0
    successful_collaborations: int = 0
    failed_collaborations: int = 0
    average_response_time: float = 0.0
    agent_success_rates: Dict[str, float] = field(default_factory=dict)
    capability_success_rates: Dict[str, float] = field(default_factory=dict)

    def record_collaboration(self, agent_id: str, capabilities: List[str], success: bool, response_time: float) -> None:
        """Record a collaboration result."""
        self.total_requests += 1
        if success:
            self.successful_collaborations += 1
        else:
            self.failed_collaborations += 1

        # Update average response time
        if self.total_requests == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (self.average_response_time * (self.total_requests - 1) + response_time) / self.total_requests

        # Update agent success rate
        if agent_id not in self.agent_success_rates:
            self.agent_success_rates[agent_id] = 0.0

        current_rate = self.agent_success_rates[agent_id]
        total_agent_requests = sum(1 for req in [agent_id] if req in self.agent_success_rates)
        new_rate = (current_rate * total_agent_requests + (1.0 if success else 0.0)) / (total_agent_requests + 1)
        self.agent_success_rates[agent_id] = new_rate

        # Update capability success rates
        for capability in capabilities:
            if capability not in self.capability_success_rates:
                self.capability_success_rates[capability] = 0.0

            current_cap_rate = self.capability_success_rates[capability]
            total_cap_requests = sum(1 for cap in capabilities if cap in self.capability_success_rates)
            new_cap_rate = (current_cap_rate * total_cap_requests + (1.0 if success else 0.0)) / (total_cap_requests + 1)
            self.capability_success_rates[capability] = new_cap_rate

    def get_success_rate(self) -> float:
        """Get overall success rate."""
        if self.total_requests == 0:
            return 0.0
        return self.successful_collaborations / self.total_requests

    def get_agent_success_rate(self, agent_id: str) -> float:
        """Get success rate for a specific agent."""
        return self.agent_success_rates.get(agent_id, 0.0)

    def get_capability_success_rate(self, capability: str) -> float:
        """Get success rate for a specific capability."""
        return self.capability_success_rates.get(capability, 0.0)


class HelpSystemManager:
    """Manages the help wanted system and collaboration tracking."""

    def __init__(self, agent_id: str, discovery_manager: AgentDiscoveryManager):
        self.agent_id = agent_id
        self.discovery_manager = discovery_manager
        self.active_requests: Dict[str, HelpRequest] = {}
        self.completed_requests: List[HelpRequest] = []
        self.metrics = CollaborationMetrics()
        self.help_handlers: Dict[MessageType, Callable[[BeastModeMessage], Any]] = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup message handlers for help system."""
        self.help_handlers = {
            MessageType.HELP_WANTED: self._handle_help_wanted,
            MessageType.HELP_RESPONSE: self._handle_help_response,
        }

    async def request_help(self, required_capabilities: List[str], description: str = "", timeout_minutes: int = 30) -> str:
        """Request help from other agents."""
        request_id = f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        # Create help request
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

        # Broadcast help request
        message = BeastModeMessage(
            type=MessageType.HELP_WANTED,
            source=self.agent_id,
            payload={"request_id": request_id, "required_capabilities": required_capabilities, "description": description, "timeout_minutes": timeout_minutes, "timestamp": datetime.now().isoformat()},
        )

        await self.discovery_manager.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))

        logger.info(f"Requested help (ID: {request_id}) for capabilities: {required_capabilities}")
        return request_id

    async def _handle_help_wanted(self, message: BeastModeMessage) -> None:
        """Handle help wanted messages from other agents."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            required_capabilities = message.payload.get("required_capabilities", [])
            request_id = message.payload.get("request_id", "")
            description = message.payload.get("description", "")

            # Check if we can help
            if self._can_help_with(required_capabilities):
                await self._send_help_response(message.source, request_id, required_capabilities, description)
                logger.info(f"Responded to help request from {message.source} for capabilities: {required_capabilities}")
            else:
                logger.debug(f"Cannot help with capabilities: {required_capabilities}")

        except Exception as e:
            logger.error(f"Error handling help wanted from {message.source}: {e}")

    async def _handle_help_response(self, message: BeastModeMessage) -> None:
        """Handle help response messages with trust scoring."""
        if message.source == self.agent_id:
            return  # Ignore our own messages

        try:
            request_id = message.payload.get("request_id", "")
            offered_capabilities = message.payload.get("offered_capabilities", [])

            # Find the corresponding help request
            if request_id in self.active_requests:
                help_request = self.active_requests[request_id]
                help_request.add_response(message.source)

                # If this is the first response, select this agent
                if help_request.status == HelpRequestStatus.PENDING and not help_request.selected_responder:
                    help_request.select_responder(message.source)
                    logger.info(f"Selected {message.source} as responder for request {request_id}")

                # Update trust score for responding agent
                await self.discovery_manager.update_collaboration_success(message.source, True)
                logger.debug(f"Updated trust score for {message.source} (help response)")

        except Exception as e:
            logger.error(f"Error handling help response from {message.source}: {e}")
            # Update trust score negatively for errors
            await self.discovery_manager.update_collaboration_success(message.source, False)

    def _can_help_with(self, required_capabilities: List[str]) -> bool:
        """Check if this agent can help with the required capabilities."""
        agent_capabilities = self.discovery_manager.capabilities
        return all(cap in agent_capabilities for cap in required_capabilities)

    async def _send_help_response(self, target_agent: str, request_id: str, required_capabilities: List[str], description: str) -> None:
        """Send help response to a specific agent."""
        message = BeastModeMessage(
            type=MessageType.HELP_RESPONSE,
            source=self.agent_id,
            target=target_agent,
            payload={
                "request_id": request_id,
                "offered_capabilities": required_capabilities,
                "message": f"I can help with: {', '.join(required_capabilities)}",
                "description": f"Response to: {description}",
                "timestamp": datetime.now().isoformat(),
            },
        )

        await self.discovery_manager.redis_manager.publish("beast_mode_network", MessageSerializer.serialize(message))

    async def complete_help_request(self, request_id: str, success: bool) -> None:
        """Mark a help request as completed."""
        if request_id in self.active_requests:
            help_request = self.active_requests.pop(request_id)
            help_request.mark_completed(success)
            self.completed_requests.append(help_request)

            # Update metrics
            if help_request.selected_responder:
                response_time = (help_request.completed_at - help_request.created_at).total_seconds() / 60.0
                self.metrics.record_collaboration(help_request.selected_responder, help_request.required_capabilities, success, response_time)

                # Update trust score in discovery manager
                await self.discovery_manager.update_collaboration_success(help_request.selected_responder, success)

            logger.info(f"Completed help request {request_id} with success: {success}")

    async def get_help_requests(self, status: Optional[HelpRequestStatus] = None) -> List[HelpRequest]:
        """Get help requests, optionally filtered by status."""
        if status is None:
            return list(self.active_requests.values()) + self.completed_requests
        elif status == HelpRequestStatus.PENDING:
            return [req for req in self.active_requests.values() if req.status == status]
        else:
            return [req for req in self.completed_requests if req.status == status]

    async def get_available_helpers(self, required_capabilities: List[str]) -> List[DiscoveredAgent]:
        """Get agents that can help with specific capabilities."""
        return await self.discovery_manager.registry.find_agents_by_capabilities(required_capabilities)

    async def get_collaboration_metrics(self) -> CollaborationMetrics:
        """Get collaboration success metrics."""
        return self.metrics

    async def cleanup_expired_requests(self) -> None:
        """Clean up expired help requests."""
        expired_requests = [req_id for req_id, req in self.active_requests.items() if req.is_expired()]

        for req_id in expired_requests:
            help_request = self.active_requests.pop(req_id)
            help_request.status = HelpRequestStatus.TIMEOUT
            self.completed_requests.append(help_request)
            logger.info(f"Expired help request: {req_id}")

    def get_handlers(self) -> Dict[MessageType, Callable[[BeastModeMessage], Any]]:
        """Get help system message handlers for registration with bus client."""
        return self.help_handlers

    async def get_agent_recommendations(self, required_capabilities: List[str]) -> List[Tuple[str, float]]:
        """Get agent recommendations based on capabilities and success rates."""
        available_agents = await self.get_available_helpers(required_capabilities)

        recommendations = []
        for agent in available_agents:
            # Calculate recommendation score based on capability match and success rate
            capability_score = agent.get_capability_match_score(required_capabilities)
            success_rate = self.metrics.get_agent_success_rate(agent.agent_id)
            trust_score = agent.trust_score

            # Weighted score: 40% capability match, 30% success rate, 30% trust score
            recommendation_score = capability_score * 0.4 + success_rate * 0.3 + trust_score * 0.3

            recommendations.append((agent.agent_id, recommendation_score))

        # Sort by recommendation score (highest first)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations

    async def mark_help_completed(self, request_id: str, success: bool = True) -> None:
        """Mark a help request as completed and update trust scores."""
        if request_id in self.active_requests:
            help_request = self.active_requests[request_id]
            help_request.mark_completed()

            # Update trust score for the responder
            if help_request.selected_responder:
                await self.discovery_manager.update_collaboration_success(help_request.selected_responder, success)
                logger.info(f"Updated trust score for {help_request.selected_responder} (help completion: {success})")

            # Remove from active requests
            del self.active_requests[request_id]

    async def get_trust_scores(self) -> Dict[str, float]:
        """Get trust scores for all discovered agents."""
        discovered_agents = await self.discovery_manager.get_discovered_agents()
        return {agent.agent_id: agent.trust_score for agent in discovered_agents}
