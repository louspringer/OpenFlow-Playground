"""
Core Message Data Models for Beast Mode Agent Collaboration Network

Task 2: Implement core message data models
- Create BeastModeMessage model with validation
- Implement MessageType enum with all standard types
- Add AgentCapabilities model for agent metadata
- Write serialization/deserialization utilities
- Create unit tests for message validation
- Requirements: 6.1, 6.2
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import json
import uuid


class MessageType(str, Enum):
    """Standardized message types for agent communication."""

    # Basic communication
    SIMPLE_MESSAGE = "simple_message"  # Basic text communication
    PROMPT_REQUEST = "prompt_request"  # Request for processing
    PROMPT_RESPONSE = "prompt_response"  # Response to request

    # Agent discovery and capabilities
    AGENT_DISCOVERY = "agent_discovery"  # Presence announcement
    AGENT_RESPONSE = "agent_response"  # Discovery response

    # Collaboration and help
    HELP_WANTED = "help_wanted"  # Request for assistance
    HELP_RESPONSE = "help_response"  # Offer to help

    # Spore sharing
    SPORE_DELIVERY = "spore_delivery"  # Spore sharing
    SPORE_REQUEST = "spore_request"  # Request for specific spore

    # Technical and system
    TECHNICAL_EXCHANGE = "technical_exchange"  # Setup/debugging info
    SYSTEM_HEALTH = "system_health"  # Health monitoring
    HEALTH_CHECK = "health_check"  # Health check ping
    HEALTH_RESPONSE = "health_response"  # Health check response
    HEALTH_REPORT = "health_report"  # Health status report

    # Processor responses
    PROCESSOR_RESPONSE = "processor_response"  # Automated responses


@dataclass
class BeastModeMessage:
    """
    Core message model for Beast Mode Agent Collaboration Network.

    All messages in the network use this standardized format with validation
    and serialization capabilities.
    """

    type: MessageType
    source: str
    target: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 5
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"id": self.id, "type": self.type.value, "source": self.source, "target": self.target, "payload": self.payload, "timestamp": self.timestamp.isoformat(), "priority": self.priority}

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize message from JSON string."""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except Exception as e:
            raise ValueError(f"Invalid BeastModeMessage format: {e}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary."""
        # Convert timestamp string back to datetime
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        # Convert type string back to enum
        if "type" in data and isinstance(data["type"], str):
            data["type"] = MessageType(data["type"])

        return cls(**data)


@dataclass
class AgentCapabilities:
    """Agent capabilities and metadata for discovery."""

    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    availability: str = "offline"
    specializations: List[str] = field(default_factory=list)
    collaboration_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "availability": self.availability,
            "specializations": self.specializations,
            "collaboration_history": self.collaboration_history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary."""
        return cls(**data)


class MessageSerializer:
    """Utility class for message serialization and deserialization."""

    @staticmethod
    def serialize(message: BeastModeMessage) -> str:
        """Serialize a message to JSON string."""
        return message.to_json()

    @staticmethod
    def deserialize(json_str: str) -> BeastModeMessage:
        """Deserialize a JSON string to a message."""
        return BeastModeMessage.from_json(json_str)
