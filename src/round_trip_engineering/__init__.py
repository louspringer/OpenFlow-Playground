#!/usr/bin/env python3
"""
Round-Trip Engineering Package

This package provides round-trip engineering capabilities between models and code.
It includes vocabulary alignment, code generation, and duplication cleaning.
"""

from .core.round_trip_system import RoundTripSystem

__all__ = ["RoundTripSystem"]

# Version information
__version__ = "2.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Round-trip engineering with ontological vocabulary alignment"
