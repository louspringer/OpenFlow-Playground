"""
Data Models for Gmail-to-Calendar System
========================================

Defines the core data structures and contracts for the system.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json


class SourceType(Enum):
    """Source types for event creation"""

    GMAIL = "gmail"
    ICS = "ics"
    MANUAL = "manual"


class EventStatus(Enum):
    """Event status for tracking"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CONFLICT = "conflict"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass
class EventCandidate:
    """
    Represents a potential calendar event extracted from various sources.

    This is the core data structure that flows through the orchestration pipeline.
    """

    summary: str
    start_iso: str
    end_iso: str
    location: Optional[str] = None
    description: Optional[str] = None
    attendees: List[str] = field(default_factory=list)
    source: SourceType = SourceType.MANUAL
    idempotency_key: Optional[str] = None
    confidence: float = 1.0
    missing: List[str] = field(default_factory=list)
    source_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "summary": self.summary,
            "start_iso": self.start_iso,
            "end_iso": self.end_iso,
            "location": self.location,
            "description": self.description,
            "attendees": self.attendees,
            "source": self.source.value,
            "idempotency_key": self.idempotency_key,
            "confidence": self.confidence,
            "missing": self.missing,
            "source_metadata": self.source_metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventCandidate":
        """Create from dictionary"""
        return cls(
            summary=data["summary"],
            start_iso=data["start_iso"],
            end_iso=data["end_iso"],
            location=data.get("location"),
            description=data.get("description"),
            attendees=data.get("attendees", []),
            source=SourceType(data.get("source", "manual")),
            idempotency_key=data.get("idempotency_key"),
            confidence=data.get("confidence", 1.0),
            missing=data.get("missing", []),
            source_metadata=data.get("source_metadata", {}),
        )


@dataclass
class IdempotencyKey:
    """
    Generates and manages idempotency keys for preventing duplicate events.
    """

    source_system: str
    identifier: str

    def __str__(self) -> str:
        return f"{self.source_system}:{self.identifier}"

    @classmethod
    def from_gmail_message(cls, message_id: str) -> "IdempotencyKey":
        """Create from Gmail message ID"""
        return cls(source_system="gmail", identifier=message_id)

    @classmethod
    def from_ics_uid(cls, uid: str) -> "IdempotencyKey":
        """Create from ICS UID"""
        return cls(source_system="ics", identifier=uid)

    @classmethod
    def from_event_hash(cls, summary: str, start_iso: str, primary_attendee: str) -> "IdempotencyKey":
        """Create from event hash for manual events"""
        import hashlib

        content = f"{summary}|{start_iso}|{primary_attendee}"
        hash_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        return cls(source_system="manual", identifier=hash_id)


@dataclass
class ConflictInfo:
    """Information about calendar conflicts"""

    has_conflict: bool
    conflicting_events: List[Dict[str, Any]] = field(default_factory=list)
    suggested_times: List[Dict[str, str]] = field(default_factory=list)
    conflict_reason: Optional[str] = None


@dataclass
class ConfirmationRequest:
    """Request for user confirmation"""

    event_candidate: EventCandidate
    conflict_info: Optional[ConflictInfo] = None
    confirmation_message: str = ""
    requires_confirmation: bool = True


@dataclass
class EventResult:
    """Result of event creation/update"""

    success: bool
    event_id: Optional[str] = None
    event_link: Optional[str] = None
    error_message: Optional[str] = None
    idempotency_key: Optional[str] = None
    was_duplicate: bool = False


@dataclass
class AuditLog:
    """Audit log entry for tracking actions"""

    timestamp: datetime
    user_id: str
    action: str
    event_id: Optional[str]
    idempotency_key: Optional[str]
    source_message_id: Optional[str]
    success: bool
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "action": self.action,
            "event_id": self.event_id,
            "idempotency_key": self.idempotency_key,
            "source_message_id": self.source_message_id,
            "success": self.success,
            "details": self.details,
        }


# JSON Schema for validation
EVENT_CANDIDATE_SCHEMA = {
    "type": "object",
    "required": ["summary", "start_iso", "end_iso"],
    "properties": {
        "summary": {"type": "string", "maxLength": 180},
        "location": {"type": "string"},
        "description": {"type": "string"},
        "start_iso": {"type": "string", "format": "date-time"},
        "end_iso": {"type": "string", "format": "date-time"},
        "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
        "source": {"type": "string", "enum": ["gmail", "ics", "manual"]},
        "idempotency_key": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "missing": {"type": "array", "items": {"type": "string"}},
        "source_metadata": {"type": "object"},
    },
}
