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

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message identifier")
    type: MessageType = Field(..., description="Standardized message type")
    source: str = Field(..., description="Sending agent identifier")
    target: Optional[str] = Field(None, description="Target agent (None for broadcast)")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message content and metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message creation time")
    priority: int = Field(default=5, ge=1, le=10, description="Message priority (1-10)")

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

    agent_id: str = Field(..., description="Unique agent identifier")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    availability: str = Field(default="offline", description="Current availability status")
    specializations: List[str] = Field(default_factory=list, description="Agent specializations")
    collaboration_history: List[str] = Field(default_factory=list, description="Previous collaborations")


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
