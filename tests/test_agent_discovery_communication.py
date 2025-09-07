#!/usr/bin/env python3
"""
Tests for Agent Discovery and Communication (Tasks 4-6)

Tests agent discovery protocol, help wanted system, and message type handling.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from beast_mode.agent_discovery import AgentRegistry, DiscoveredAgent, AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager, HelpRequest, HelpRequestStatus, CollaborationMetrics
from beast_mode.message_handlers import MessageRouter, MessageCompatibilityLayer, MessageHandlerManager
from beast_mode.message_models import BeastModeMessage, MessageType, AgentCapabilities


class TestAgentRegistry:
    """Test agent registry functionality."""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    @pytest.fixture
    def sample_capabilities(self):
        return AgentCapabilities(
            agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], availability="ready_for_business", specializations=["cost_analysis"], collaboration_history=[]
        )

    @pytest.mark.asyncio
    async def test_register_agent(self, registry, sample_capabilities):
        """Test agent registration."""
        await registry.register_agent(sample_capabilities)

        assert "test_agent" in registry.agents
        agent = registry.agents["test_agent"]
        assert agent.agent_id == "test_agent"
        assert agent.capabilities == ["python_coding", "gcp_optimization"]
        assert agent.availability == "ready_for_business"

    @pytest.mark.asyncio
    async def test_find_agents_by_capabilities(self, registry, sample_capabilities):
        """Test finding agents by capabilities."""
        await registry.register_agent(sample_capabilities)

        # Find agents with matching capabilities
        agents = await registry.find_agents_by_capabilities(["python_coding"])
        assert len(agents) == 1
        assert agents[0].agent_id == "test_agent"

        # Find agents with non-matching capabilities
        agents = await registry.find_agents_by_capabilities(["java_coding"])
        assert len(agents) == 0

    @pytest.mark.asyncio
    async def test_update_agent_trust(self, registry, sample_capabilities):
        """Test updating agent trust score."""
        await registry.register_agent(sample_capabilities)

        agent = registry.agents["test_agent"]
        initial_trust = agent.trust_score

        # Update trust with success
        await registry.update_agent_trust("test_agent", True)
        assert agent.trust_score > initial_trust

        # Update trust with failure
        await registry.update_agent_trust("test_agent", False)
        assert agent.trust_score < 1.0


class TestDiscoveredAgent:
    """Test DiscoveredAgent functionality."""

    def test_agent_creation(self):
        """Test agent creation."""
        agent = DiscoveredAgent(agent_id="test_agent", capabilities=["python_coding"], specializations=["gcp_optimization"], availability="ready_for_business", last_seen=datetime.now())

        assert agent.agent_id == "test_agent"
        assert agent.capabilities == ["python_coding"]
        assert agent.trust_score == 0.5

    def test_is_available(self):
        """Test availability checking."""
        agent = DiscoveredAgent(agent_id="test_agent", capabilities=["python_coding"], specializations=[], availability="ready_for_business", last_seen=datetime.now())

        assert agent.is_available() is True

        # Test with old timestamp
        agent.last_seen = datetime.now() - timedelta(minutes=10)
        assert agent.is_available() is False

    def test_matches_capabilities(self):
        """Test capability matching."""
        agent = DiscoveredAgent(agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], specializations=[], availability="ready_for_business", last_seen=datetime.now())

        assert agent.matches_capabilities(["python_coding"]) is True
        assert agent.matches_capabilities(["python_coding", "gcp_optimization"]) is True
        assert agent.matches_capabilities(["java_coding"]) is False

    def test_get_capability_match_score(self):
        """Test capability match scoring."""
        agent = DiscoveredAgent(agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], specializations=[], availability="ready_for_business", last_seen=datetime.now())

        score = agent.get_capability_match_score(["python_coding"])
        assert score == 1.0

        score = agent.get_capability_match_score(["python_coding", "gcp_optimization"])
        assert score == 1.0

        score = agent.get_capability_match_score(["python_coding", "java_coding"])
        assert score == 0.5


class TestHelpRequest:
    """Test HelpRequest functionality."""

    def test_help_request_creation(self):
        """Test help request creation."""
        request = HelpRequest(
            request_id="test_request",
            requester_id="test_agent",
            required_capabilities=["python_coding"],
            description="Need help with Python",
            status=HelpRequestStatus.PENDING,
            created_at=datetime.now(),
        )

        assert request.request_id == "test_request"
        assert request.status == HelpRequestStatus.PENDING
        assert request.is_expired() is False

    def test_help_request_expiration(self):
        """Test help request expiration."""
        request = HelpRequest(
            request_id="test_request",
            requester_id="test_agent",
            required_capabilities=["python_coding"],
            description="Need help with Python",
            status=HelpRequestStatus.PENDING,
            created_at=datetime.now() - timedelta(minutes=35),
            timeout_minutes=30,
        )

        assert request.is_expired() is True

    def test_add_response(self):
        """Test adding responses."""
        request = HelpRequest(
            request_id="test_request",
            requester_id="test_agent",
            required_capabilities=["python_coding"],
            description="Need help with Python",
            status=HelpRequestStatus.PENDING,
            created_at=datetime.now(),
        )

        request.add_response("helper_agent")
        assert "helper_agent" in request.responses

        # Adding same agent again should not duplicate
        request.add_response("helper_agent")
        assert request.responses.count("helper_agent") == 1


class TestCollaborationMetrics:
    """Test CollaborationMetrics functionality."""

    def test_metrics_creation(self):
        """Test metrics creation."""
        metrics = CollaborationMetrics()
        assert metrics.total_requests == 0
        assert metrics.get_success_rate() == 0.0

    def test_record_collaboration(self):
        """Test recording collaboration."""
        metrics = CollaborationMetrics()

        metrics.record_collaboration("agent1", ["python_coding"], True, 5.0)
        assert metrics.total_requests == 1
        assert metrics.successful_collaborations == 1
        assert metrics.get_success_rate() == 1.0

        metrics.record_collaboration("agent1", ["python_coding"], False, 3.0)
        assert metrics.total_requests == 2
        assert metrics.successful_collaborations == 1
        assert metrics.get_success_rate() == 0.5


class TestMessageCompatibilityLayer:
    """Test message compatibility layer."""

    def test_convert_legacy_message(self):
        """Test converting legacy message format."""
        compatibility = MessageCompatibilityLayer()

        # Test simple message conversion
        legacy_data = {"message": "Hello world", "source": "test_agent"}

        message = compatibility.convert_legacy_message(legacy_data)
        assert message.type == MessageType.SIMPLE_MESSAGE
        assert message.source == "test_agent"
        assert message.payload["message"] == "Hello world"

    def test_validate_message(self):
        """Test message validation."""
        compatibility = MessageCompatibilityLayer()

        # Valid message
        valid_message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="test_agent", payload={"message": "Hello"})
        assert compatibility.validate_message(valid_message) is True

        # Invalid message (missing required fields)
        invalid_message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="", payload={"message": "Hello"})  # Empty source
        assert compatibility.validate_message(invalid_message) is False


class TestMessageTypeHandlers:
    """Test message type handlers."""

    def test_simple_message_handler(self):
        """Test simple message handler."""
        from beast_mode.message_handlers import SimpleMessageHandler

        handler = SimpleMessageHandler("test_agent")

        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="other_agent", payload={"message": "Hello"})

        # Test handler can handle the message
        assert handler.can_handle(message) is True

    def test_prompt_request_handler(self):
        """Test prompt request handler."""
        from beast_mode.message_handlers import PromptRequestHandler

        handler = PromptRequestHandler("test_agent")

        message = BeastModeMessage(type=MessageType.PROMPT_REQUEST, source="other_agent", payload={"prompt_type": "cost_analysis", "prompt_data": {"query": "What are the costs?"}})

        assert handler.can_handle(message) is True


class TestIntegration:
    """Integration tests for Tasks 4-6."""

    @pytest.mark.asyncio
    async def test_agent_discovery_flow(self):
        """Test complete agent discovery flow."""
        # Mock Redis manager
        redis_manager = AsyncMock()
        redis_manager.publish = AsyncMock()

        # Create discovery managers for two agents
        agent1 = AgentDiscoveryManager("agent1", ["python_coding"], redis_manager)
        agent2 = AgentDiscoveryManager("agent2", ["gcp_optimization"], redis_manager)

        # Agent1 announces presence
        await agent1.announce_presence()

        # Verify announcement was published
        assert redis_manager.publish.called

        # Simulate agent2 receiving the announcement
        capabilities_data = AgentCapabilities(agent_id="agent1", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        discovery_message = BeastModeMessage(type=MessageType.AGENT_DISCOVERY, source="agent1", payload={"capabilities": capabilities_data.model_dump()})

        await agent2._handle_agent_discovery(discovery_message)

        # Verify agent1 was registered in agent2's registry
        discovered_agents = await agent2.get_discovered_agents()
        assert len(discovered_agents) == 1
        assert discovered_agents[0].agent_id == "agent1"

    @pytest.mark.asyncio
    async def test_help_request_flow(self):
        """Test complete help request flow."""
        # Mock Redis manager
        redis_manager = AsyncMock()
        redis_manager.publish = AsyncMock()

        # Create discovery and help managers
        discovery_manager = AgentDiscoveryManager("agent1", ["python_coding"], redis_manager)
        help_manager = HelpSystemManager("agent1", discovery_manager)

        # Request help
        request_id = await help_manager.request_help(["gcp_optimization"], "Need GCP help")

        # Verify help request was published
        assert redis_manager.publish.called
        assert request_id is not None

        # Simulate receiving help response
        help_response = BeastModeMessage(
            type=MessageType.HELP_RESPONSE, source="agent2", target="agent1", payload={"request_id": request_id, "offered_capabilities": ["gcp_optimization"], "message": "I can help with GCP"}
        )

        await help_manager._handle_help_response(help_response)

        # Verify help request was updated
        requests = await help_manager.get_help_requests(HelpRequestStatus.PENDING)
        assert len(requests) == 1
        assert "agent2" in requests[0].responses

    @pytest.mark.asyncio
    async def test_message_routing(self):
        """Test message routing functionality."""
        # Mock managers
        redis_manager = AsyncMock()
        discovery_manager = AgentDiscoveryManager("test_agent", ["python_coding"], redis_manager)
        help_manager = HelpSystemManager("test_agent", discovery_manager)

        # Create message router
        router = MessageRouter("test_agent", discovery_manager, help_manager)

        # Test routing simple message
        simple_message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="other_agent", payload={"message": "Hello"})

        result = await router.route_message(simple_message)
        assert result.success is True

        # Test routing message not for this agent
        targeted_message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="other_agent", target="different_agent", payload={"message": "Hello"})

        result = await router.route_message(targeted_message)
        assert result.success is True
        assert result.should_continue is False


if __name__ == "__main__":
    pytest.main([__file__])
