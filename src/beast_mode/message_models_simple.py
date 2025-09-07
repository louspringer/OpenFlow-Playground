"""
Core Message Data Models for Beast Mode Agent Collaboration Network

Task 2: Implement core message data models
- Create BeastModeMessage Pydantic model with validation
- Implement MessageType enum with all standard types
- Add AgentCapabilities model for agent metadata
- Write serialization/deserialization utilities
- Create unit tests for message validation
- Requirements: 6.1, 6.2
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
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

    # Processor responses
    PROCESSOR_RESPONSE = "processor_response"  # Automated responses


class BeastModeMessage(BaseModel):
    """
    Core message model for Beast Mode Agent Collaboration Network.

    All messages in the network use this standardized format with validation
    and serialization capabilities.
    """

    id: str
    type: MessageType
    source: str
    target: Optional[str] = None
    payload: Dict[str, Any] = {}
    timestamp: datetime
    priority: int = 5

    def __init__(self, **data):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        if "timestamp" not in data:
            data["timestamp"] = datetime.now()
        if "payload" not in data:
            data["payload"] = {}
        super().__init__(**data)

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize message from JSON string."""
        try:
            return cls.model_validate_json(json_str)
        except Exception as e:
            raise ValueError(f"Invalid BeastModeMessage format: {e}")


class AgentCapabilities(BaseModel):
    """Agent capabilities and metadata for discovery."""

    agent_id: str
    capabilities: List[str] = []
    availability: str = "offline"
    specializations: List[str] = []
    collaboration_history: List[str] = []


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
