#!/usr/bin/env python3
"""
Agent Communication Protocols
Implements robust communication protocols for multi-hackathon agent coordination
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages in agent communication protocol"""

    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    HEALTH_CHECK = "health_check"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    ERROR_REPORT = "error_report"
    HEARTBEAT = "heartbeat"


class MessagePriority(Enum):
    """Message priority levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AgentMessage:
    """Standardized message format for agent communication"""

    message_id: str
    message_type: MessageType
    priority: MessagePriority
    sender_id: str
    recipient_id: Optional[str]  # None for broadcast
    timestamp: datetime
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        data = asdict(self)
        data["message_type"] = self.message_type.value
        data["priority"] = self.priority.value
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create message from dictionary"""
        data["message_type"] = MessageType(data["message_type"])
        data["priority"] = MessagePriority(data["priority"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

    def is_expired(self) -> bool:
        """Check if message has expired based on timeout"""
        elapsed = (datetime.utcnow() - self.timestamp).total_seconds()
        return elapsed > self.timeout_seconds


@dataclass
class TaskRequest:
    """Task request payload"""

    task_id: str
    task_type: str
    description: str
    requirements: Dict[str, Any]
    deadline: Optional[datetime] = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class TaskResponse:
    """Task response payload"""

    task_id: str
    status: str  # "accepted", "rejected", "completed", "failed"
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    estimated_completion: Optional[datetime] = None


@dataclass
class StatusUpdate:
    """Status update payload"""

    agent_id: str
    status: str  # "idle", "busy", "error", "maintenance"
    current_tasks: List[str]
    health_indicators: Dict[str, Any]
    capabilities: List[str]


class CommunicationProtocol:
    """
    Robust communication protocol for agent coordination
    Implements message queuing, retry logic, and error handling
    """

    def __init__(self, agent_id: str, message_queue_size: int = 1000):
        self.agent_id = agent_id
        self.message_queue_size = message_queue_size
        self.incoming_queue: List[AgentMessage] = []
        self.outgoing_queue: List[AgentMessage] = []
        self.pending_responses: Dict[str, AgentMessage] = {}
        self.message_history: List[AgentMessage] = []
        self.logger = logging.getLogger(f"{__name__}.{agent_id}")

    def send_message(
        self,
        message_type: MessageType,
        recipient_id: Optional[str],
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.MEDIUM,
        correlation_id: Optional[str] = None,
        timeout_seconds: int = 30,
    ) -> str:
        """Send a message to another agent"""
        message_id = f"{self.agent_id}_{int(time.time() * 1000)}"

        message = AgentMessage(
            message_id=message_id,
            message_type=message_type,
            priority=priority,
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            timestamp=datetime.utcnow(),
            payload=payload,
            correlation_id=correlation_id,
            timeout_seconds=timeout_seconds,
        )

        self.outgoing_queue.append(message)
        self.logger.info(f"Sent {message_type.value} message {message_id} to {recipient_id or 'broadcast'}")

        return message_id

    def receive_message(self) -> Optional[AgentMessage]:
        """Receive the next message from the incoming queue"""
        if not self.incoming_queue:
            return None

        message = self.incoming_queue.pop(0)
        self.message_history.append(message)

        # Clean up old messages to prevent memory leaks
        if len(self.message_history) > self.message_queue_size:
            self.message_history = self.message_history[-self.message_queue_size :]

        return message

    def queue_incoming_message(self, message: AgentMessage):
        """Queue an incoming message (called by message router)"""
        # Prioritize messages by priority
        if message.priority == MessagePriority.CRITICAL:
            self.incoming_queue.insert(0, message)
        elif message.priority == MessagePriority.HIGH:
            # Insert after critical messages
            insert_index = 0
            for i, existing in enumerate(self.incoming_queue):
                if existing.priority != MessagePriority.CRITICAL:
                    insert_index = i
                    break
            self.incoming_queue.insert(insert_index, message)
        else:
            self.incoming_queue.append(message)

        self.logger.info(f"Queued incoming {message.message_type.value} message from {message.sender_id}")

    def send_task_request(self, recipient_id: str, task_request: TaskRequest, priority: MessagePriority = MessagePriority.MEDIUM) -> str:
        """Send a task request to another agent"""
        return self.send_message(message_type=MessageType.TASK_REQUEST, recipient_id=recipient_id, payload=asdict(task_request), priority=priority)

    def send_task_response(self, recipient_id: str, task_response: TaskResponse, correlation_id: str, priority: MessagePriority = MessagePriority.MEDIUM) -> str:
        """Send a task response back to the requesting agent"""
        return self.send_message(message_type=MessageType.TASK_RESPONSE, recipient_id=recipient_id, payload=asdict(task_response), correlation_id=correlation_id, priority=priority)

    def send_status_update(self, recipient_id: Optional[str], status_update: StatusUpdate, priority: MessagePriority = MessagePriority.LOW) -> str:
        """Send a status update (can be broadcast)"""
        return self.send_message(message_type=MessageType.STATUS_UPDATE, recipient_id=recipient_id, payload=asdict(status_update), priority=priority)

    def send_health_check(self, recipient_id: str, priority: MessagePriority = MessagePriority.MEDIUM) -> str:
        """Send a health check request"""
        return self.send_message(message_type=MessageType.HEALTH_CHECK, recipient_id=recipient_id, payload={}, priority=priority)

    def send_heartbeat(self, recipient_id: Optional[str], priority: MessagePriority = MessagePriority.LOW) -> str:
        """Send a heartbeat message"""
        return self.send_message(message_type=MessageType.HEARTBEAT, recipient_id=recipient_id, payload={"timestamp": datetime.utcnow().isoformat()}, priority=priority)

    def process_retries(self):
        """Process message retries for failed deliveries"""
        current_time = datetime.utcnow()
        retry_messages = []

        for message_id, message in list(self.pending_responses.items()):
            if message.is_expired():
                if message.retry_count < message.max_retries:
                    message.retry_count += 1
                    message.timestamp = current_time
                    retry_messages.append(message)
                    self.logger.warning(f"Retrying message {message_id} (attempt {message.retry_count})")
                else:
                    self.logger.error(f"Message {message_id} failed after {message.max_retries} retries")
                    del self.pending_responses[message_id]

        # Re-queue retry messages
        for message in retry_messages:
            self.outgoing_queue.append(message)

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status for monitoring"""
        return {
            "incoming_queue_size": len(self.incoming_queue),
            "outgoing_queue_size": len(self.outgoing_queue),
            "pending_responses": len(self.pending_responses),
            "message_history_size": len(self.message_history),
            "queue_capacity": self.message_queue_size,
        }

    def clear_expired_messages(self):
        """Clean up expired messages from queues"""
        current_time = datetime.utcnow()

        # Clean incoming queue
        self.incoming_queue = [msg for msg in self.incoming_queue if not msg.is_expired()]

        # Clean outgoing queue
        self.outgoing_queue = [msg for msg in self.outgoing_queue if not msg.is_expired()]

        # Clean pending responses
        expired_responses = [msg_id for msg_id, msg in self.pending_responses.items() if msg.is_expired()]
        for msg_id in expired_responses:
            del self.pending_responses[msg_id]

        self.logger.info(f"Cleaned up expired messages, removed {len(expired_responses)} expired responses")
