"""
Code Quality System

Comprehensive code quality automation that integrates with the multi-agent testing framework,
enforces quality gates, and provides round-trip code generation validation.
"""

from .quality_metrics import QualityMetrics, QualityScore
from .quality_gates import QualityGate, QualityGateManager
from .quality_enforcer import QualityEnforcer
from .integrations import PreCommitIntegration, CICDIntegration

__all__ = [
    "QualityMetrics",
    "QualityScore", 
    "QualityGate",
    "QualityGateManager",
    "QualityEnforcer",
    "PreCommitIntegration",
    "CICDIntegration",
]

__version__ = "0.1.0"
