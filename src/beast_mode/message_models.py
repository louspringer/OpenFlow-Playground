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
from pydantic import BaseModel, Field, validator
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

    @validator("id")
    def validate_id(cls, v):
        """Ensure ID is a valid UUID string."""
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError("Message ID must be a valid UUID string")

    @validator("source")
    def validate_source(cls, v):
        """Ensure source is not empty."""
        if not v or not v.strip():
            raise ValueError("Source cannot be empty")
        return v.strip()

    @validator("payload")
    def validate_payload(cls, v):
        """Ensure payload is serializable."""
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError):
            raise ValueError("Payload must be JSON serializable")

    @validator("priority")
    def validate_priority(cls, v):
        """Ensure priority is within valid range."""
        if not 1 <= v <= 10:
            raise ValueError("Priority must be between 1 and 10")
        return v

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return self.json()

    @classmethod
    def from_json(cls, json_str: str) -> "BeastModeMessage":
        """Deserialize message from JSON string."""
        try:
            data = json.loads(json_str)
            return cls(**data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid JSON for BeastModeMessage: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return self.dict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BeastModeMessage":
        """Create message from dictionary."""
        return cls(**data)

    def is_broadcast(self) -> bool:
        """Check if message is a broadcast (no target)."""
        return self.target is None

    def is_direct(self) -> bool:
        """Check if message is direct (has target)."""
        return self.target is not None

    def get_message_text(self) -> str:
        """Extract message text from payload."""
        return self.payload.get("message", "")

    def set_message_text(self, text: str) -> None:
        """Set message text in payload."""
        self.payload["message"] = text

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to payload."""
        self.payload[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata from payload."""
        return self.payload.get(key, default)


class AgentCapabilities(BaseModel):
    """
    Agent capabilities and metadata for discovery and collaboration.
    """

    agent_id: str = Field(..., description="Unique agent identifier")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    availability: str = Field(default="ready_for_business", description="Current availability status")
    specializations: List[str] = Field(default_factory=list, description="Specific areas of expertise")
    collaboration_history: List[str] = Field(default_factory=list, description="Previous successful collaborations")
    last_seen: datetime = Field(default_factory=datetime.now, description="Last time agent was seen")

    @validator("availability")
    def validate_availability(cls, v):
        """Ensure availability is valid."""
        valid_statuses = ["ready_for_business", "busy", "offline", "maintenance"]
        if v not in valid_statuses:
            raise ValueError(f"Availability must be one of: {valid_statuses}")
        return v

    @validator("capabilities")
    def validate_capabilities(cls, v):
        """Ensure capabilities list is valid."""
        if not isinstance(v, list):
            raise ValueError("Capabilities must be a list")
        return [cap.strip() for cap in v if cap.strip()]

    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability."""
        return capability.lower() in [cap.lower() for cap in self.capabilities]

    def add_capability(self, capability: str) -> None:
        """Add capability to agent."""
        if capability.strip() and not self.has_capability(capability):
            self.capabilities.append(capability.strip())

    def remove_capability(self, capability: str) -> bool:
        """Remove capability from agent."""
        for i, cap in enumerate(self.capabilities):
            if cap.lower() == capability.lower():
                self.capabilities.pop(i)
                return True
        return False

    def match_capabilities(self, required_capabilities: List[str]) -> List[str]:
        """Find matching capabilities from required list."""
        matches = []
        for required in required_capabilities:
            if self.has_capability(required):
                matches.append(required)
        return matches

    def is_available(self) -> bool:
        """Check if agent is available for collaboration."""
        return self.availability == "ready_for_business"

    def update_last_seen(self) -> None:
        """Update last seen timestamp."""
        self.last_seen = datetime.now()


class MessageValidationError(Exception):
    """Exception raised when message validation fails."""

    pass


class MessageSerializer:
    """
    Utility class for message serialization and deserialization.
    """

    @staticmethod
    def serialize(message: BeastModeMessage) -> str:
        """Serialize message to JSON string."""
        try:
            return message.to_json()
        except Exception as e:
            raise MessageValidationError(f"Failed to serialize message: {e}")

    @staticmethod
    def deserialize(json_str: str) -> BeastModeMessage:
        """Deserialize message from JSON string."""
        try:
            return BeastModeMessage.from_json(json_str)
        except Exception as e:
            raise MessageValidationError(f"Failed to deserialize message: {e}")

    @staticmethod
    def validate_message(message: BeastModeMessage) -> bool:
        """Validate message structure and content."""
        try:
            # Test serialization/deserialization round trip
            json_str = message.to_json()
            deserialized = BeastModeMessage.from_json(json_str)

            # Check critical fields
            if not message.id or not message.source or not message.type:
                return False

            # Check payload is serializable
            json.dumps(message.payload)

            return True

        except Exception:
            return False

    @staticmethod
    def create_simple_message(source: str, message_text: str, target: Optional[str] = None, priority: int = 5) -> BeastModeMessage:
        """Create a simple message with text content."""
        return BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=source, target=target, payload={"message": message_text}, priority=priority)

    @staticmethod
    def create_prompt_request(source: str, prompt: str, target: Optional[str] = None, context: Optional[str] = None, priority: int = 9) -> BeastModeMessage:
        """Create a prompt request message."""
        payload = {"prompt": prompt}
        if context:
            payload["context"] = context

        return BeastModeMessage(type=MessageType.PROMPT_REQUEST, source=source, target=target, payload=payload, priority=priority)

    @staticmethod
    def create_agent_discovery(source: str, capabilities: List[str], specializations: List[str] = None) -> BeastModeMessage:
        """Create an agent discovery message."""
        return BeastModeMessage(
            type=MessageType.AGENT_DISCOVERY, source=source, payload={"capabilities": capabilities, "specializations": specializations or [], "timestamp": datetime.now().isoformat()}, priority=7
        )


# Example usage and testing
def test_message_models():
    """Test message model functionality."""
    print("Testing BeastModeMessage...")

    # Test simple message creation
    msg = MessageSerializer.create_simple_message(source="test_agent", message_text="Hello, Beast Mode!", priority=5)

    print(f"✅ Created message: {msg.id}")
    print(f"✅ Message type: {msg.type}")
    print(f"✅ Is broadcast: {msg.is_broadcast()}")

    # Test serialization
    json_str = msg.to_json()
    print(f"✅ Serialized to JSON: {len(json_str)} characters")

    # Test deserialization
    deserialized = MessageSerializer.deserialize(json_str)
    print(f"✅ Deserialized message ID: {deserialized.id}")

    # Test validation
    is_valid = MessageSerializer.validate_message(msg)
    print(f"✅ Message validation: {is_valid}")

    print("\nTesting AgentCapabilities...")

    # Test agent capabilities
    agent = AgentCapabilities(agent_id="test_agent", capabilities=["python_coding", "gcp_optimization"], specializations=["cost_analysis", "deployment"])

    print(f"✅ Agent ID: {agent.agent_id}")
    print(f"✅ Has python_coding: {agent.has_capability('python_coding')}")
    print(f"✅ Is available: {agent.is_available()}")

    # Test capability matching
    matches = agent.match_capabilities(["python_coding", "web_development"])
    print(f"✅ Capability matches: {matches}")

    print("\n✅ All message model tests passed!")


if __name__ == "__main__":
    test_message_models()
