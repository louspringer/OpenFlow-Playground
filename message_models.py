from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import uuid


class MessageType(str, Enum):
    SIMPLE_MESSAGE = "simple_message"
    PROMPT_REQUEST = "prompt_request"
    PROMPT_RESPONSE = "prompt_response"
    AGENT_DISCOVERY = "agent_discovery"
    AGENT_RESPONSE = "agent_response"
    HELP_WANTED = "help_wanted"
    HELP_RESPONSE = "help_response"
    SPORE_DELIVERY = "spore_delivery"
    SPORE_REQUEST = "spore_request"
    TECHNICAL_EXCHANGE = "technical_exchange"
    SYSTEM_HEALTH = "system_health"
    PROCESSOR_RESPONSE = "processor_response"


@dataclass
class BeastModeMessage:
    type: MessageType
    source: str
    target: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 5
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type.value, "source": self.source, "target": self.target, "payload": self.payload, "timestamp": self.timestamp.isoformat(), "priority": self.priority}

    @classmethod
    def from_json(cls, json_str: str):
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except Exception as e:
            raise ValueError(f"Invalid BeastModeMessage format: {e}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        if "type" in data and isinstance(data["type"], str):
            data["type"] = MessageType(data["type"])
        return cls(**data)


@dataclass
class AgentCapabilities:
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    availability: str = "offline"
    specializations: List[str] = field(default_factory=list)
    collaboration_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "availability": self.availability,
            "specializations": self.specializations,
            "collaboration_history": self.collaboration_history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)


class MessageSerializer:
    @staticmethod
    def serialize(message: BeastModeMessage) -> str:
        return message.to_json()

    @staticmethod
    def deserialize(json_str: str) -> BeastModeMessage:
        return BeastModeMessage.from_json(json_str)
