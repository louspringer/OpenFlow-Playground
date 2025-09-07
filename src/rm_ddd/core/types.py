"""
RM-DDD Core Types

Core data types and enums for the RM-DDD system.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class ModuleStatus(str, Enum):
    """Module status enumeration"""

    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    STARTING = "starting"
    ERROR = "error"


@dataclass(frozen=True)
class ModuleCapability:
    """Describes a module capability"""

    name: str
    description: str = ""
    enabled: bool = True
    version: str = "1"
    dependencies: List[str] = field(default_factory=list)
    performance_metrics: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ModuleHealth:
    """Comprehensive module health information"""

    status: ModuleStatus
    message: str = ""
    capabilities: List[ModuleCapability] = field(default_factory=list)
    indicators: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class DomainHealth:
    """Domain-specific health information"""

    domain_context: str
    boundary_integrity: bool
    invariant_compliance: bool
    language_consistency: float
    complexity_score: float
    last_validated: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class DomainBoundaries:
    """Defines domain boundaries for a component"""

    context: str
    bounded_context_rules: List[str]
    anti_corruption_layers: List[str] = field(default_factory=list)
    shared_kernels: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AggregateBoundaries:
    """Defines aggregate consistency boundaries"""

    aggregate_root: str
    internal_entities: List[str]
    consistency_rules: List[str]
    invariants: List[str]


@dataclass
class ValidationResult:
    """Result of validation operation"""

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        """Add validation warning"""
        self.warnings.append(warning)
