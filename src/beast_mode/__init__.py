"""
Beast Mode Framework - Systematic Development Methodology

This module provides systematic development capabilities that enhance the OpenFlow-Playground
demo-focused architecture with measurable superiority over ad-hoc approaches.

Key Components:
- PDCA Orchestrator: Systematic Plan-Do-Check-Act workflow
- RCA Engine: Root cause analysis with pattern library
- Service Interface: External service delivery capabilities
- Tool Health Manager: Systematic tool diagnostics and repair
- Metrics Engine: Comparative analysis and superiority proof

Requirements Compliance:
- R1: Systematic Superiority through Makefile Health Manager
- R2: PDCA Execution on real development tasks
- R3: Tool Fixing with systematic repair engine
- R4: Model-Driven Decisions using project registry
- R5: Service Delivery to GKE hackathon
- R6: RM Principles in all components
- R7: Root Cause Analysis with pattern library
- R8: Measurable Superiority over ad-hoc approaches
"""

from .base.reflective_module import ReflectiveModule
from .pdca.orchestrator import PDCAOrchestrator
from .rca.engine import RootCauseAnalysisEngine
from .metrics.collection import MetricsCollectionEngine
from .service_interface.gke_interface import GKEServiceInterface
from .tool_health.manager import ToolHealthManager

__version__ = "1.0.0"
__author__ = "Beast Mode Framework Team"

__all__ = ["ReflectiveModule", "PDCAOrchestrator", "RootCauseAnalysisEngine", "MetricsCollectionEngine", "GKEServiceInterface", "ToolHealthManager"]
