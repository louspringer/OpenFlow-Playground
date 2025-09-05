"""
Beast Mode Framework Data Models

Data structures for the Beast Mode Framework, supporting all 8 requirements
with comprehensive type safety and validation.

Requirements Compliance: All R1-R8 data structures
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from datetime import datetime


class PDCAPhase(Enum):
    """PDCA cycle phases."""

    PLAN = "plan"
    DO = "do"
    CHECK = "check"
    ACT = "act"


class RCASeverity(Enum):
    """Root cause analysis severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolStatus(Enum):
    """Tool health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class PDCAResult:
    """Result of a complete PDCA cycle execution."""

    task: str
    phase: PDCAPhase
    plan_result: Dict[str, Any]
    do_result: Dict[str, Any]
    check_result: Dict[str, Any]
    act_result: Dict[str, Any]
    success: bool
    metrics: Dict[str, Any]
    timestamp: datetime
    model_updates: List[Dict[str, Any]]


@dataclass
class RCAResult:
    """Result of root cause analysis."""

    failure: str
    symptoms: List[str]
    root_causes: List[str]
    severity: RCASeverity
    analysis_factors: Dict[str, Any]
    systematic_fixes: List[Dict[str, Any]]
    fix_validation: Dict[str, Any]
    prevention_patterns: List[Dict[str, Any]]
    timestamp: datetime


@dataclass
class ToolRepairResult:
    """Result of systematic tool repair."""

    tool_name: str
    root_cause_identified: str
    systematic_fix_applied: Dict[str, Any]
    fix_validation: Dict[str, Any]
    prevention_pattern: Dict[str, Any]
    repair_time: float
    success: bool
    timestamp: datetime


@dataclass
class ModelDrivenDecisionResult:
    """Result of model-driven decision making."""

    decision_context: Dict[str, Any]
    registry_consultation: Dict[str, Any]
    domain_intelligence_used: Dict[str, Any]
    decision_reasoning: Dict[str, Any]
    registry_updates: List[Dict[str, Any]]
    confidence_score: float
    timestamp: datetime


@dataclass
class GKEServiceDeliveryResult:
    """Result of GKE service delivery."""

    service_type: str
    gke_request: Dict[str, Any]
    beast_mode_response: Dict[str, Any]
    improvement_metrics: Dict[str, Any]
    adhoc_comparison: Dict[str, Any]
    delivery_time: float
    success: bool
    timestamp: datetime


@dataclass
class ReflectiveModuleStatus:
    """Status of a Reflective Module component."""

    is_healthy: bool
    health_indicators: Dict[str, Any]
    operational_visibility: Dict[str, Any]
    graceful_degradation_status: Optional[Dict[str, Any]]
    single_responsibility_validation: Dict[str, Any]
    last_updated: datetime


@dataclass
class SuperiorityMetrics:
    """Metrics proving Beast Mode superiority over ad-hoc approaches."""

    problem_resolution_speed: Dict[str, Any]
    tool_health_performance: Dict[str, Any]
    decision_success_rates: Dict[str, Any]
    gke_velocity_improvement: Dict[str, Any]
    overall_superiority_proof: Dict[str, Any]
    measurement_timestamp: datetime


@dataclass
class MakefileDiagnosisResult:
    """Result of Makefile health diagnosis."""

    missing_files: List[str]
    broken_targets: List[str]
    dependency_issues: List[str]
    root_cause: str
    diagnosis_time: float
    timestamp: datetime


@dataclass
class ToolHealthAssessment:
    """Assessment of tool health status."""

    tool_name: str
    status: ToolStatus
    installation_integrity: Dict[str, Any]
    dependency_check: Dict[str, Any]
    configuration_check: Dict[str, Any]
    version_compatibility: Dict[str, Any]
    overall_health_score: float
    recommendations: List[str]
    timestamp: datetime


@dataclass
class ServiceUsageMetrics:
    """Metrics for service usage and performance."""

    service_name: str
    usage_count: int
    success_rate: float
    average_response_time: float
    error_count: int
    improvement_over_adhoc: float
    measurement_period: str
    timestamp: datetime


@dataclass
class PatternLearningResult:
    """Result of pattern learning and model updates."""

    pattern_type: str
    pattern_data: Dict[str, Any]
    learning_source: str
    model_updates: List[Dict[str, Any]]
    prevention_measures: List[Dict[str, Any]]
    confidence_score: float
    timestamp: datetime


@dataclass
class ComparativeAnalysisResult:
    """Result of comparative analysis between approaches."""

    comparison_type: str
    beast_mode_metrics: Dict[str, Any]
    adhoc_metrics: Dict[str, Any]
    improvement_percentage: float
    statistical_significance: float
    sample_size: int
    analysis_timestamp: datetime
