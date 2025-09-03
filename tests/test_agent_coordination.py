#!/usr/bin/env python3
"""
Tests for Agent Coordination Framework
"""

import asyncio
import pytest
import pytest_asyncio
from datetime import datetime, timedelta

from src.agent_coordination import (
    AgentCoordinator,
    CommunicationProtocol,
    MessageType,
    MessagePriority,
    TaskRequest,
    TaskResponse,
    StatusUpdate,
    MultiPerspectiveValidator,
    StakeholderType,
    AgentHealthMonitor,
)


class TestAgentCoordination:
    """Test cases for agent coordination framework"""

    @pytest_asyncio.fixture
    async def coordinator(self):
        """Create a test coordinator"""
        coordinator = AgentCoordinator("test_coordinator")
        await coordinator.start()
        yield coordinator
        await coordinator.stop()

    @pytest.fixture
    def mock_agent_protocol(self):
        """Create a mock agent communication protocol"""
        return CommunicationProtocol("test_agent")

    @pytest.mark.asyncio
    async def test_coordinator_initialization(self, coordinator):
        """Test coordinator initialization"""
        assert coordinator.coordinator_id == "test_coordinator"
        assert coordinator.is_running is True
        assert len(coordinator.registered_agents) == 0
        assert len(coordinator.active_tasks) == 0

    @pytest.mark.asyncio
    async def test_agent_registration(self, coordinator, mock_agent_protocol):
        """Test agent registration"""
        capabilities = ["task_processing", "data_analysis"]

        result = await coordinator.register_agent(agent_id="test_agent", capabilities=capabilities, communication_protocol=mock_agent_protocol)

        assert result is True
        assert "test_agent" in coordinator.registered_agents
        assert coordinator.registered_agents["test_agent"].capabilities == capabilities
        assert coordinator.stats["agents_registered"] == 1

    @pytest.mark.asyncio
    async def test_task_submission(self, coordinator):
        """Test task submission"""
        requirements = {
            "capabilities": ["task_processing"],
            "service_impact": "low",
            "resource_usage": 0.1,
            "code_quality": 0.9,
            "test_coverage": 0.8,
            "metrics": {"success_rate": 0.95},
            "validation": {"proof_of_concept": True},
            "metadata": {"proven_pattern": True},
        }

        task_id = await coordinator.submit_task(task_type="test_task", description="Test task description", requirements=requirements)

        assert task_id is not None
        assert task_id in coordinator.active_tasks
        assert coordinator.active_tasks[task_id].task_type == "test_task"
        assert coordinator.stats["validation_requests"] == 1

    @pytest.mark.asyncio
    async def test_multi_perspective_validation(self):
        """Test multi-perspective validation"""
        health_monitor = AgentHealthMonitor()
        validator = MultiPerspectiveValidator(health_monitor)

        decision_data = {
            "service_impact": "low",
            "resource_usage": 0.1,
            "code_quality": 0.9,
            "test_coverage": 0.8,
            "metrics": {"success_rate": 0.95},
            "validation": {"proof_of_concept": True},
            "metadata": {"proven_pattern": True},
        }

        result = validator.validate_agent_decision(decision_context="Test decision", initial_confidence=0.7, decision_data=decision_data)

        assert result.decision_context == "Test decision"
        assert result.overall_confidence > 0.0
        assert len(result.stakeholder_perspectives) > 0
        assert result.final_recommendation is not None

    @pytest.mark.asyncio
    async def test_health_monitoring(self):
        """Test health monitoring"""
        health_monitor = AgentHealthMonitor()

        # Register an agent
        health_monitor.register_agent("test_agent", ["capability1"])

        # Update heartbeat
        health_monitor.update_heartbeat("test_agent", response_time_ms=100.0)

        # Get agent health
        agent_health = health_monitor.get_agent_health("test_agent")
        assert agent_health is not None
        assert agent_health["overall_status"] == "healthy"

        # Get system health
        system_health = health_monitor.get_system_health()
        assert system_health["overall_health"] == "healthy"
        assert system_health["total_agents"] == 1
        assert system_health["healthy_agents"] == 1

    @pytest.mark.asyncio
    async def test_communication_protocol(self, mock_agent_protocol):
        """Test communication protocol"""
        # Send a message
        message_id = mock_agent_protocol.send_message(
            message_type=MessageType.HEARTBEAT, recipient_id="coordinator", payload={"timestamp": datetime.utcnow().isoformat()}, priority=MessagePriority.LOW
        )

        assert message_id is not None
        assert len(mock_agent_protocol.outgoing_queue) == 1

        # Send task request
        task_request = TaskRequest(task_id="test_task", task_type="test", description="Test task", requirements={})

        message_id = mock_agent_protocol.send_task_request(recipient_id="coordinator", task_request=task_request)

        assert message_id is not None
        assert len(mock_agent_protocol.outgoing_queue) == 2

    @pytest.mark.asyncio
    async def test_coordinator_status(self, coordinator):
        """Test coordinator status reporting"""
        status = await coordinator.get_coordinator_status()

        assert status["coordinator_id"] == "test_coordinator"
        assert status["is_running"] is True
        assert status["registered_agents"] == 0
        assert status["active_tasks"] == 0
        assert status["queued_tasks"] == 0
        assert "system_health" in status
        assert "stats" in status

    @pytest.mark.asyncio
    async def test_agent_unregistration(self, coordinator, mock_agent_protocol):
        """Test agent unregistration"""
        # Register agent first
        await coordinator.register_agent(agent_id="test_agent", capabilities=["test"], communication_protocol=mock_agent_protocol)

        assert "test_agent" in coordinator.registered_agents

        # Unregister agent
        result = await coordinator.unregister_agent("test_agent")

        assert result is True
        assert "test_agent" not in coordinator.registered_agents


if __name__ == "__main__":
    pytest.main([__file__])
