"""
PDCA Context and Task Definitions

Defines context and task structures for PDCA cycle execution.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(Enum):
    """Task type categories."""

    DEVELOPMENT = "development"
    BUG_FIX = "bug_fix"
    FEATURE = "feature"
    REFACTOR = "refactor"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"


@dataclass
class PDCATask:
    """Represents a development task for PDCA cycle execution."""

    name: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    requirements: List[str]
    constraints: Dict[str, Any]
    success_criteria: List[str]
    estimated_duration: Optional[float] = None
    assigned_domain: Optional[str] = None
    dependencies: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        """Initialize default values."""
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()


@dataclass
class PDCAPhaseResult:
    """Result of a single PDCA phase execution."""

    phase: str
    success: bool
    duration: float
    outputs: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]
    timestamp: datetime

    def __post_init__(self):
        """Initialize default values."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class ModelRegistryQuery:
    """Query for project model registry intelligence."""

    domain: str
    requirement_type: str
    context: Dict[str, Any]
    confidence_threshold: float = 0.8
    max_results: int = 10


@dataclass
class ValidationResult:
    """Result of validation checks."""

    check_name: str
    passed: bool
    score: float
    details: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime

    def __post_init__(self):
        """Initialize default values."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
