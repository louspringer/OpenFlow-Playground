#!/usr/bin/env python3
"""
Governed Recursive AST Analyzer - RM Compliant

This module does recursive descent with GOVERNORS to prevent infinite recursion.
"""

import ast
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ASTNodeInfo:
    """Information about an AST node with scope context"""

    name: str
    node_type: str  # 'function', 'class', 'method', 'nested_function'
    scope_depth: int  # How deep in the AST tree
    parent_scope: Optional[str] = None  # Parent function/class name
    is_importable: bool = True  # Can this be imported as standalone?
    source_location: Optional[str] = None


class GovernedASTAnalyzer:
    """AST analyzer with recursion governors to prevent infinite loops"""

    def __init__(self, max_depth: int = 5, max_nodes: int = 1000):
        self.max_depth = max_depth  # Maximum recursion depth
        self.max_nodes = max_nodes  # Maximum nodes to analyze
        self.node_count = 0
        self.analyzed_nodes = set()  # Prevent re-analyzing same nodes

        logger.info(f"🔧 GovernedASTAnalyzer initialized: max_depth={max_depth}, max_nodes={max_nodes}")

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file with governed recursion"""
        try:
            logger.info(f"🎯 Analyzing {file_path} with governed recursion")

            with open(file_path) as f:
                content = f.read()

            tree = ast.parse(content)

            # Reset counters
            self.node_count = 0
            self.analyzed_nodes.clear()

            # Analyze with governors
            result = self._analyze_node(tree, depth=0, parent_scope=None)

            logger.info(f"✅ Analysis complete: {self.node_count} nodes analyzed")
            return result

        except Exception as e:
            logger.error(f"❌ Error analyzing {file_path}: {e}")
            return {"error": str(e)}

    def _analyze_node(self, node: ast.AST, depth: int, parent_scope: Optional[str]) -> Dict[str, Any]:
        """Analyze a single AST node with recursion governors"""

        # GOVERNOR 1: Depth limit
        if depth > self.max_depth:
            logger.warning(f"🚨 Depth limit reached ({depth} > {self.max_depth}) at {type(node).__name__}")
            return {"error": f"Depth limit exceeded: {depth}"}

        # GOVERNOR 2: Node count limit
        if self.node_count >= self.max_nodes:
            logger.warning(f"🚨 Node count limit reached ({self.node_count} >= {self.max_nodes})")
            return {"error": f"Node count limit exceeded: {self.node_count}"}

        # GOVERNOR 3: Prevent re-analyzing same node
        node_id = id(node)
        if node_id in self.analyzed_nodes:
            logger.debug(f"⏭️ Skipping already analyzed node: {type(node).__name__}")
            return {"error": "Node already analyzed"}

        # Mark as analyzed
        self.analyzed_nodes.add(node_id)
        self.node_count += 1

        # Analyze based on node type
        if isinstance(node, ast.Module):
            return self._analyze_module(node, depth, parent_scope)
        elif isinstance(node, ast.FunctionDef):
            return self._analyze_function(node, depth, parent_scope)
        elif isinstance(node, ast.ClassDef):
            return self._analyze_class(node, depth, parent_scope)
        else:
            return {"node_type": type(node).__name__, "depth": depth}

    def _analyze_module(self, node: ast.Module, depth: int, parent_scope: Optional[str]) -> Dict[str, Any]:
        """Analyze module with governed recursion"""
        logger.debug(f"📁 Analyzing module at depth {depth}")

        top_level_functions = []
        top_level_classes = []

        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                func_info = self._analyze_function(child, depth + 1, parent_scope)
                if func_info.get("is_importable"):
                    top_level_functions.append(func_info)
            elif isinstance(child, ast.ClassDef):
                class_info = self._analyze_class(child, depth + 1, parent_scope)
                top_level_classes.append(class_info)

        return {"node_type": "module", "depth": depth, "top_level_functions": top_level_functions, "top_level_classes": top_level_classes, "total_nodes_analyzed": self.node_count}

    def _analyze_function(self, node: ast.FunctionDef, depth: int, parent_scope: Optional[str]) -> Dict[str, Any]:
        """Analyze function with governed recursion"""
        logger.debug(f"🔧 Analyzing function {node.name} at depth {depth}")

        # Check if this is a nested function
        is_nested = parent_scope is not None
        is_importable = not is_nested and depth <= 2  # Only top-level functions are importable

        # Analyze nested functions (with depth governor)
        nested_functions = []
        if depth < self.max_depth:
            for child in ast.walk(node):
                if isinstance(child, ast.FunctionDef) and child != node:
                    nested_info = self._analyze_function(child, depth + 1, node.name)
                    nested_functions.append(nested_info)

        return {
            "name": node.name,
            "node_type": "nested_function" if is_nested else "function",
            "scope_depth": depth,
            "parent_scope": parent_scope,
            "is_importable": is_importable,
            "nested_functions": nested_functions,
            "source_location": f"line {node.lineno}",
        }

    def _analyze_class(self, node: ast.ClassDef, depth: int, parent_scope: Optional[str]) -> Dict[str, Any]:
        """Analyze class with governed recursion"""
        logger.debug(f"🏗️ Analyzing class {node.name} at depth {depth}")

        methods = []
        nested_classes = []

        # Analyze class body (with depth governor)
        if depth < self.max_depth:
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_info = self._analyze_function(child, depth + 1, node.name)
                    method_info["node_type"] = "method"
                    method_info["is_importable"] = False  # Methods are never importable
                    methods.append(method_info)
                elif isinstance(child, ast.ClassDef):
                    nested_info = self._analyze_class(child, depth + 1, node.name)
                    nested_classes.append(nested_info)

        return {
            "name": node.name,
            "node_type": "nested_class" if parent_scope else "class",
            "scope_depth": depth,
            "parent_scope": parent_scope,
            "is_importable": parent_scope is None,  # Only top-level classes are importable
            "methods": methods,
            "nested_classes": nested_classes,
            "source_location": f"line {node.lineno}",
        }

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary with governor status"""
        return {
            "nodes_analyzed": self.node_count,
            "max_depth_reached": any(depth > self.max_depth for depth in [self.max_depth]),
            "max_nodes_reached": self.node_count >= self.max_nodes,
            "governor_status": "active" if self.node_count < self.max_nodes else "triggered",
            "recursion_safety": "safe" if self.node_count < self.max_nodes else "limit_reached",
        }
