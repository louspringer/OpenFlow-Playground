#!/usr/bin/env python3
"""
Agent Coordinator
Main coordinator for multi-hackathon agent coordination
Implements robust communication protocols and multi-perspective validation
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set
from datetime import datetime

from .communication_protocols import CommunicationProtocol, MessageType, MessagePriority, AgentMessage, TaskRequest, TaskResponse, StatusUpdate
from .multi_perspective_validator import MultiPerspectiveValidator, StakeholderType
from .health_monitor import AgentHealthMonitor, HealthStatus

logger = logging.getLogger(__name__)


@dataclass
class AgentInfo:
    """Information about a registered agent"""

    agent_id: str
    capabilities: List[str]
    communication_protocol: CommunicationProtocol
    last_seen: datetime
    status: str = "idle"
    current_tasks: Set[str] = None

    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = set()


@dataclass
class CoordinationTask:
    """Task for agent coordination"""

    task_id: str
    task_type: str
    description: str
    requirements: Dict[str, Any]
    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, assigned, in_progress, completed, failed
    created_at: datetime = None
    deadline: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class AgentCoordinator:
    """
    Main coordinator for multi-hackathon agent coordination
    Implements robust communication protocols and multi-perspective validation
    """

    def __init__(self, coordinator_id: str = "main_coordinator"):
        self.coordinator_id = coordinator_id
        self.logger = logging.getLogger(f"{__name__}.{coordinator_id}")

        # Core components
        self.communication_protocol = CommunicationProtocol(coordinator_id)
        self.health_monitor = AgentHealthMonitor()
        self.multi_perspective_validator = MultiPerspectiveValidator(self.health_monitor)

        # Agent management
        self.registered_agents: Dict[str, AgentInfo] = {}
        self.active_tasks: Dict[str, CoordinationTask] = {}
        self.task_queue: List[CoordinationTask] = []

        # Coordination state
        self.is_running = False
        self.coordination_loop_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = {"tasks_completed": 0, "tasks_failed": 0, "agents_registered": 0, "coordination_cycles": 0, "validation_requests": 0}

        self.logger.info(f"Agent Coordinator {coordinator_id} initialized")

    async def start(self):
        """Start the agent coordinator"""
        if self.is_running:
            self.logger.warning("Coordinator already running")
            return

        self.is_running = True
        self.coordination_loop_task = asyncio.create_task(self._coordination_loop())

        self.logger.info("Agent Coordinator started")

    async def stop(self):
        """Stop the agent coordinator"""
        if not self.is_running:
            self.logger.warning("Coordinator not running")
            return

        self.is_running = False

        if self.coordination_loop_task:
            self.coordination_loop_task.cancel()
            try:
                await self.coordination_loop_task
            except asyncio.CancelledError:
                pass

        self.logger.info("Agent Coordinator stopped")

    async def register_agent(self, agent_id: str, capabilities: List[str], communication_protocol: CommunicationProtocol) -> bool:
        """Register a new agent with the coordinator"""
        if agent_id in self.registered_agents:
            self.logger.warning(f"Agent {agent_id} already registered")
            return False

        # Register with health monitor
        self.health_monitor.register_agent(agent_id, capabilities)

        # Create agent info
        agent_info = AgentInfo(agent_id=agent_id, capabilities=capabilities, communication_protocol=communication_protocol, last_seen=datetime.utcnow())

        self.registered_agents[agent_id] = agent_info
        self.stats["agents_registered"] += 1

        self.logger.info(f"Registered agent {agent_id} with capabilities: {capabilities}")
        return True

    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordinator"""
        if agent_id not in self.registered_agents:
            self.logger.warning(f"Agent {agent_id} not registered")
            return False

        # Unregister from health monitor
        self.health_monitor.unregister_agent(agent_id)

        # Cancel any assigned tasks
        for task in self.active_tasks.values():
            if task.assigned_agent == agent_id and task.status in ["assigned", "in_progress"]:
                task.status = "failed"
                task.error_message = f"Agent {agent_id} unregistered"
                self.stats["tasks_failed"] += 1

        del self.registered_agents[agent_id]

        self.logger.info(f"Unregistered agent {agent_id}")
        return True

    async def submit_task(self, task_type: str, description: str, requirements: Dict[str, Any], deadline: Optional[datetime] = None) -> str:
        """Submit a new task for coordination"""
        task_id = f"task_{int(time.time() * 1000)}"

        task = CoordinationTask(task_id=task_id, task_type=task_type, description=description, requirements=requirements, deadline=deadline)

        # Use multi-perspective validation for task submission
        validation_result = self.multi_perspective_validator.validate_agent_decision(
            decision_context=f"Task submission: {task_type}",
            initial_confidence=0.7,  # Assume medium confidence for new tasks
            decision_data={
                "task_type": task_type,
                "requirements": requirements,
                "deadline": deadline.isoformat() if deadline else None,
                "service_impact": requirements.get("service_impact", "low"),
                "resource_usage": requirements.get("resource_usage", 0.1),
                "code_quality": requirements.get("code_quality", 0.9),
                "test_coverage": requirements.get("test_coverage", 0.8),
                "metrics": requirements.get("metrics", {}),
                "validation": requirements.get("validation", {}),
                "metadata": requirements.get("metadata", {}),
            },
        )

        self.stats["validation_requests"] += 1

        if not validation_result.consensus_reached or validation_result.overall_confidence < 0.5:
            self.logger.warning(f"Task {task_id} rejected by multi-perspective validation: consensus={validation_result.consensus_reached}, confidence={validation_result.overall_confidence}")
            self.logger.warning(f"Final recommendation: {validation_result.final_recommendation}")
            return None

        self.active_tasks[task_id] = task
        self.task_queue.append(task)

        self.logger.info(f"Submitted task {task_id}: {task_type}")
        return task_id

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id not in self.active_tasks:
            return None

        task = self.active_tasks[task_id]
        return {
            "task_id": task_id,
            "task_type": task.task_type,
            "description": task.description,
            "status": task.status,
            "assigned_agent": task.assigned_agent,
            "created_at": task.created_at.isoformat(),
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "result": task.result,
            "error_message": task.error_message,
        }

    async def get_coordinator_status(self) -> Dict[str, Any]:
        """Get overall coordinator status"""
        return {
            "coordinator_id": self.coordinator_id,
            "is_running": self.is_running,
            "registered_agents": len(self.registered_agents),
            "active_tasks": len(self.active_tasks),
            "queued_tasks": len(self.task_queue),
            "system_health": self.health_monitor.get_system_health(),
            "stats": self.stats,
            "agent_list": list(self.registered_agents.keys()),
        }

    async def _coordination_loop(self):
        """Main coordination loop"""
        self.logger.info("Starting coordination loop")

        while self.is_running:
            try:
                await self._coordination_cycle()
                self.stats["coordination_cycles"] += 1
                await asyncio.sleep(1)  # 1 second cycle
            except Exception as e:
                self.logger.error(f"Error in coordination loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    async def _coordination_cycle(self):
        """Single coordination cycle"""
        # Process incoming messages
        await self._process_incoming_messages()

        # Assign queued tasks
        await self._assign_queued_tasks()

        # Check task status
        await self._check_task_status()

        # Update agent health
        await self._update_agent_health()

        # Clean up completed tasks
        await self._cleanup_completed_tasks()

        # Process communication retries
        self.communication_protocol.process_retries()

    async def _process_incoming_messages(self):
        """Process incoming messages from agents"""
        while True:
            message = self.communication_protocol.receive_message()
            if not message:
                break

            try:
                await self._handle_message(message)
            except Exception as e:
                self.logger.error(f"Error handling message {message.message_id}: {e}")

    async def _handle_message(self, message: AgentMessage):
        """Handle a specific message"""
        if message.message_type == MessageType.TASK_RESPONSE:
            await self._handle_task_response(message)
        elif message.message_type == MessageType.STATUS_UPDATE:
            await self._handle_status_update(message)
        elif message.message_type == MessageType.HEALTH_CHECK:
            await self._handle_health_check(message)
        elif message.message_type == MessageType.HEARTBEAT:
            await self._handle_heartbeat(message)
        elif message.message_type == MessageType.ERROR_REPORT:
            await self._handle_error_report(message)
        else:
            self.logger.warning(f"Unknown message type: {message.message_type}")

    async def _handle_task_response(self, message: AgentMessage):
        """Handle task response from agent"""
        task_response = TaskResponse(**message.payload)
        task_id = task_response.task_id

        if task_id not in self.active_tasks:
            self.logger.warning(f"Received response for unknown task: {task_id}")
            return

        task = self.active_tasks[task_id]

        if task_response.status == "completed":
            task.status = "completed"
            task.result = task_response.result
            self.stats["tasks_completed"] += 1
            self.logger.info(f"Task {task_id} completed by {message.sender_id}")
        elif task_response.status == "failed":
            task.status = "failed"
            task.error_message = task_response.error_message
            self.stats["tasks_failed"] += 1
            self.logger.error(f"Task {task_id} failed: {task_response.error_message}")
        else:
            self.logger.warning(f"Unknown task response status: {task_response.status}")

    async def _handle_status_update(self, message: AgentMessage):
        """Handle status update from agent"""
        status_update = StatusUpdate(**message.payload)
        agent_id = status_update.agent_id

        if agent_id in self.registered_agents:
            agent_info = self.registered_agents[agent_id]
            agent_info.status = status_update.status
            agent_info.current_tasks = set(status_update.current_tasks)
            agent_info.last_seen = datetime.utcnow()

            # Update health monitor
            self.health_monitor.update_heartbeat(agent_id)

    async def _handle_health_check(self, message: AgentMessage):
        """Handle health check request"""
        # Send health check response
        response_payload = {"coordinator_health": "healthy" if self.is_running else "stopped", "system_health": self.health_monitor.get_system_health(), "timestamp": datetime.utcnow().isoformat()}

        self.communication_protocol.send_message(message_type=MessageType.HEALTH_CHECK, recipient_id=message.sender_id, payload=response_payload, correlation_id=message.message_id)

    async def _handle_heartbeat(self, message: AgentMessage):
        """Handle heartbeat from agent"""
        agent_id = message.sender_id
        if agent_id in self.registered_agents:
            agent_info = self.registered_agents[agent_id]
            agent_info.last_seen = datetime.utcnow()

            # Update health monitor
            self.health_monitor.update_heartbeat(agent_id)

    async def _handle_error_report(self, message: AgentMessage):
        """Handle error report from agent"""
        agent_id = message.sender_id
        error_message = message.payload.get("error_message", "Unknown error")

        if agent_id in self.registered_agents:
            self.health_monitor.report_error(agent_id, error_message)

    async def _assign_queued_tasks(self):
        """Assign queued tasks to available agents"""
        if not self.task_queue:
            return

        available_agents = [agent_id for agent_id, agent_info in self.registered_agents.items() if agent_info.status == "idle" and len(agent_info.current_tasks) == 0]

        if not available_agents:
            return

        # Assign tasks to available agents
        tasks_to_assign = []
        for task in self.task_queue[:]:
            if task.status != "pending":
                continue

            # Find best agent for this task
            best_agent = self._find_best_agent_for_task(task, available_agents)
            if best_agent:
                task.assigned_agent = best_agent
                task.status = "assigned"
                tasks_to_assign.append(task)
                self.task_queue.remove(task)
                available_agents.remove(best_agent)

        # Send task assignments
        for task in tasks_to_assign:
            await self._send_task_assignment(task)

    def _find_best_agent_for_task(self, task: CoordinationTask, available_agents: List[str]) -> Optional[str]:
        """Find the best agent for a specific task"""
        if not available_agents:
            return None

        # Simple capability matching for now
        required_capabilities = task.requirements.get("capabilities", [])

        for agent_id in available_agents:
            agent_info = self.registered_agents[agent_id]
            if all(cap in agent_info.capabilities for cap in required_capabilities):
                return agent_id

        # If no perfect match, return first available agent
        return available_agents[0]

    async def _send_task_assignment(self, task: CoordinationTask):
        """Send task assignment to agent"""
        if not task.assigned_agent:
            return

        task_request = TaskRequest(task_id=task.task_id, task_type=task.task_type, description=task.description, requirements=task.requirements, deadline=task.deadline)

        self.communication_protocol.send_task_request(recipient_id=task.assigned_agent, task_request=task_request, priority=MessagePriority.HIGH)

        self.logger.info(f"Assigned task {task.task_id} to agent {task.assigned_agent}")

    async def _check_task_status(self):
        """Check status of active tasks"""
        current_time = datetime.utcnow()

        for task in self.active_tasks.values():
            if task.status in ["assigned", "in_progress"]:
                # Check for timeout
                if task.deadline and current_time > task.deadline:
                    task.status = "failed"
                    task.error_message = "Task deadline exceeded"
                    self.stats["tasks_failed"] += 1
                    self.logger.warning(f"Task {task.task_id} timed out")

    async def _update_agent_health(self):
        """Update agent health status"""
        current_time = datetime.utcnow()

        for agent_id, agent_info in self.registered_agents.items():
            # Check if agent is responsive
            time_since_seen = current_time - agent_info.last_seen
            if time_since_seen.total_seconds() > 60:  # 1 minute timeout
                agent_info.status = "unresponsive"
                self.health_monitor.report_error(agent_id, "Agent unresponsive")

    async def _cleanup_completed_tasks(self):
        """Clean up completed and failed tasks"""
        completed_tasks = [task_id for task_id, task in self.active_tasks.items() if task.status in ["completed", "failed"]]

        for task_id in completed_tasks:
            del self.active_tasks[task_id]

        if completed_tasks:
            self.logger.info(f"Cleaned up {len(completed_tasks)} completed tasks")
