#!/usr/bin/env python3
"""
Represents an AST node with metadata

This class provides:
- dataclass
- metadata support
- parent-child relationships
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dataclasses import *
from typing import *


@dataclass
class ASTNode:
    """
    Represents an AST node with metadata
    """

    # Class attributes
    # TODO: Add based on requirements: ['dataclass', 'metadata support', 'parent-child relationships']

    # Class methods
    # TODO: Add based on requirements: ['dataclass', 'metadata support', 'parent-child relationships']

    def __post_init__(self) -> None:
        """Initialize default values after object creation"""
        pass

    def __str__(self) -> str:
        """String representation of the object"""
        return f"ASTNode({self.__dict__})

    def __repr__(self) -> str:
        """Detailed string representation for debugging"""
        return f"ASTNode({self.__dict__})
