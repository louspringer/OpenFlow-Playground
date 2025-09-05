#!/usr/bin/env python3
"""
Interface Specifications Package

This package provides comprehensive interface specifications for all public APIs,
enabling interface-based test generation and validation instead of implementation probing.
"""

from .interface_spec import InterfaceSpec, FunctionSpec, ParameterSpec, TypeSpec
from .contract_spec import ContractSpec, ValidationRule, ExceptionSpec

__all__ = [
    "InterfaceSpec",
    "FunctionSpec",
    "ParameterSpec",
    "TypeSpec",
    "ContractSpec",
    "ValidationRule",
    "ExceptionSpec",
]

# Version information
__version__ = "1.0.0"
__author__ = "OpenFlow-Playground Team"
__description__ = "Comprehensive interface specifications for API modeling"
