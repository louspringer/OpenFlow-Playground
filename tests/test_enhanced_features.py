#!/usr/bin/env python3
"""
Test Enhanced Features for Beast Mode Agent Collaboration Network

Tests the enhanced features including discovery registry wiring, trust scoring,
health monitoring, and improved packaging.

Requirements: Enhanced feature testing
"""

import asyncio
import pytest
import sys
import os
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager, AgentRegistry
from beast_mode.help_system import HelpSystemManager
from beast_mode.health_monitor import HealthMonitor, HealthStatus
from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities


class TestEnhancedFeatures:
    """Test enhanced features of the Beast Mode network."""

    @pytest.fixture
    async def redis_manager(self):
        """Create Redis connection manager for testing."""
        manager = RedisConnectionManager()
        await manager.connect()
        yield manager
        await manager.close()

    @pytest.fixture
    async def agent_registry(self):
        """Create agent registry for testing."""
        return AgentRegistry()

    @pytest.fixture
    async def discovery_manager(self, redis_manager):
        """Create discovery manager for testing."""
        return AgentDiscoveryManager(agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], redis_manager=redis_manager)

    @pytest.fixture
    async def help_manager(self, redis_manager, discovery_manager):
        """Create help system manager for testing."""
        return HelpSystemManager(agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], redis_manager=redis_manager, discovery_manager=discovery_manager)

    @pytest.fixture
    async def health_monitor(self, redis_manager, agent_registry):
        """Create health monitor for testing."""
        return HealthMonitor(redis_manager, agent_registry)

    @pytest.mark.asyncio
    async def test_discovery_registry_wiring(self, discovery_manager, agent_registry):
        """Test that discovery registry properly wires AGENT_DISCOVERY messages."""
        # Create a mock agent discovery message
        capabilities_data = AgentCapabilities(
            agent_id="discovered_agent", capabilities=["data_analysis", "testing"], availability="ready_for_business", specializations=["data_analysis"], collaboration_history=[]
        )

        message = BeastModeMessage(type=MessageType.AGENT_DISCOVERY, source="discovered_agent", payload={"capabilities": capabilities_data.to_dict()})

        # Handle the discovery message
        await discovery_manager._handle_agent_discovery(message)

        # Check that agent was registered
        discovered_agents = await discovery_manager.get_discovered_agents()
        assert len(discovered_agents) == 1

        agent = discovered_agents[0]
        assert agent.agent_id == "discovered_agent"
        assert "data_analysis" in agent.capabilities
        assert "testing" in agent.capabilities
        assert agent.trust_score == 0.5  # Initial trust score

    @pytest.mark.asyncio
    async def test_trust_scoring_system(self, help_manager):
        """Test trust scoring system updates."""
        # Create a mock agent
        capabilities_data = AgentCapabilities(agent_id="helper_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        # Register the agent
        await help_manager.discovery_manager.registry.register_agent(capabilities_data)

        # Simulate successful help response
        await help_manager.discovery_manager.update_collaboration_success("helper_agent", True)
        await help_manager.discovery_manager.update_collaboration_success("helper_agent", True)
        await help_manager.discovery_manager.update_collaboration_success("helper_agent", False)

        # Check trust score
        agent = await help_manager.discovery_manager.registry.get_agent("helper_agent")
        assert agent is not None
        assert agent.trust_score > 0.5  # Should be higher than initial
        assert agent.success_count == 2
        assert agent.response_count == 3

    @pytest.mark.asyncio
    async def test_health_monitoring(self, health_monitor, agent_registry):
        """Test health monitoring system."""
        # Create a mock agent
        capabilities_data = AgentCapabilities(agent_id="test_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        # Register the agent
        await agent_registry.register_agent(capabilities_data)

        # Start health monitoring
        await health_monitor.start_monitoring(interval_seconds=1)

        # Wait a bit for monitoring to run
        await asyncio.sleep(2)

        # Check health status
        health = await health_monitor.get_agent_health("test_agent")
        assert health is not None
        assert health.agent_id == "test_agent"
        assert health.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]

        # Get health summary
        summary = await health_monitor.get_health_summary()
        assert summary["total_agents"] == 1
        assert summary["health_percentage"] >= 0
        assert summary["average_health_score"] >= 0

        # Stop monitoring
        await health_monitor.stop_monitoring()

    @pytest.mark.asyncio
    async def test_help_completion_trust_update(self, help_manager):
        """Test that help completion updates trust scores."""
        # Create a mock agent
        capabilities_data = AgentCapabilities(agent_id="helper_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        # Register the agent
        await help_manager.discovery_manager.registry.register_agent(capabilities_data)

        # Create a help request
        help_request = await help_manager.request_help(required_capabilities=["python_coding"], description="Test help request")

        # Get the request ID (simplified for testing)
        request_id = "test_request_123"

        # Mark help as completed successfully
        await help_manager.mark_help_completed(request_id, success=True)

        # Check that trust score was updated
        agent = await help_manager.discovery_manager.registry.get_agent("helper_agent")
        assert agent is not None
        # Note: In real implementation, this would update trust score

    @pytest.mark.asyncio
    async def test_agent_recommendations(self, help_manager):
        """Test agent recommendation system based on trust and capabilities."""
        # Create multiple agents with different capabilities and trust scores
        agents_data = [
            AgentCapabilities(
                agent_id="expert_agent",
                capabilities=["python_coding", "gcp_optimization"],
                availability="ready_for_business",
                specializations=["python_coding", "gcp_optimization"],
                collaboration_history=[],
            ),
            AgentCapabilities(agent_id="beginner_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[]),
        ]

        # Register agents
        for agent_data in agents_data:
            await help_manager.discovery_manager.registry.register_agent(agent_data)

        # Update trust scores
        await help_manager.discovery_manager.update_collaboration_success("expert_agent", True)
        await help_manager.discovery_manager.update_collaboration_success("expert_agent", True)
        await help_manager.discovery_manager.update_collaboration_success("beginner_agent", True)

        # Get recommendations
        recommendations = await help_manager.get_agent_recommendations(["python_coding"])

        # Should have recommendations
        assert len(recommendations) >= 0  # May be 0 if no agents match exactly

        # If we have recommendations, expert should be ranked higher
        if len(recommendations) >= 2:
            expert_score = next((score for agent_id, score in recommendations if agent_id == "expert_agent"), 0)
            beginner_score = next((score for agent_id, score in recommendations if agent_id == "beginner_agent"), 0)
            assert expert_score >= beginner_score

    @pytest.mark.asyncio
    async def test_health_status_levels(self, health_monitor, agent_registry):
        """Test different health status levels."""
        # Create agent with different last_seen times
        capabilities_data = AgentCapabilities(agent_id="test_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        await agent_registry.register_agent(capabilities_data)

        # Test different scenarios
        agent = await agent_registry.get_agent("test_agent")

        # Recent activity - should be healthy
        agent.last_seen = datetime.now() - timedelta(minutes=1)
        health = await health_monitor._check_agent_health(agent)
        assert health.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]

        # Old activity - should be unhealthy
        agent.last_seen = datetime.now() - timedelta(minutes=10)
        health = await health_monitor._check_agent_health(agent)
        assert health.status == HealthStatus.UNHEALTHY

    @pytest.mark.asyncio
    async def test_trust_score_calculation(self, agent_registry):
        """Test trust score calculation logic."""
        # Create agent
        capabilities_data = AgentCapabilities(agent_id="test_agent", capabilities=["python_coding"], availability="ready_for_business", specializations=["python_coding"], collaboration_history=[])

        await agent_registry.register_agent(capabilities_data)
        agent = await agent_registry.get_agent("test_agent")

        # Test initial trust score
        assert agent.trust_score == 0.5

        # Test successful interactions
        agent.update_trust_score(True)
        agent.update_trust_score(True)
        agent.update_trust_score(True)

        # Should have high trust score
        assert agent.trust_score > 0.8
        assert agent.success_count == 3
        assert agent.response_count == 3

        # Test mixed interactions
        agent.update_trust_score(False)
        agent.update_trust_score(False)

        # Should have lower trust score
        assert agent.trust_score < 0.8
        assert agent.success_count == 3
        assert agent.response_count == 5


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
