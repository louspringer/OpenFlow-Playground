"""
Ack-Bert: Structured Candidate Comparison & Evaluation Framework

A methodology and toolset for systematic candidate evaluation using 
ontology-based comparison frameworks.
"""

__version__ = "0.1.0"
__author__ = "Ack-Bert Contributors"

from .ontology import OntologyManager
from .comparison import ComparisonEngine
from .evidence import EvidenceCollector
from .visualization import DiagramGenerator

__all__ = [
    "OntologyManager",
    "ComparisonEngine",
    "EvidenceCollector",
    "DiagramGenerator",
]
