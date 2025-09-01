#!/usr/bin/env python3
"""
Round-Trip Engineering Package

This package provides round-trip engineering capabilities between models and code.
It includes vocabulary alignment, code generation, and duplication cleaning.
"""

from .core.round_trip_system import RoundTripSystem
from .enhanced_reverse_engineer import EnhancedReverseEngineer
from .round_trip_model_system import RoundTripModelSystem

__all__ = ["RoundTripSystem", "EnhancedReverseEngineer", "RoundTripModelSystem"]

# Version information
__version__ = "2.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Round-trip engineering with ontological vocabulary alignment"
