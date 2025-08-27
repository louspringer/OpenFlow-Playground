#!/usr/bin/env python3
"""
Workflow Analyzer for Round-Trip Engineering

This module analyzes Python code to extract actual workflow patterns and generate
UML-compliant activity diagrams using Mermaid syntax.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass

# Import ArtifactForge for AST parsing
from src.artifact_forge.agents.artifact_parser_enhanced import EnhancedArtifactParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WorkflowNode:
    """Represents a node in the workflow"""

    name: str
    node_type: str  # 'start', 'end', 'activity', 'decision', 'merge', 'fork', 'join'
    line_number: int
    content: str
    conditions: List[str] = None
    branches: List[str] = None


@dataclass
class WorkflowEdge:
    """Represents an edge/connection in the workflow"""

    from_node: str
    to_node: str
    label: str = ""
    condition: str = ""


class WorkflowAnalyzer:
    """Analyzes Python code to extract workflow patterns and generate activity diagrams"""

    def __init__(self):
        self.parser = EnhancedArtifactParser()
        logger.info("🔍 Workflow analyzer initialized with ArtifactForge integration")

    def analyze_workflow(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze Python code to extract workflow patterns

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing workflow analysis
        """
        logger.info(f"🔍 Analyzing workflow for: {source_path}")

        try:
            # Use ArtifactForge for basic parsing
            artifact = self.parser.parse_artifact(source_path, "python")

            # Extract workflow patterns from the parsed data
            workflow_data = self._extract_workflow_patterns(source_path, artifact)

            logger.info(
                f"✅ Workflow analysis completed: {len(workflow_data.get('nodes', []))} nodes"
            )
            return workflow_data

        except Exception as e:
            logger.error(f"❌ Workflow analysis failed: {e}")
            return {
                "source_path": source_path,
                "workflow_analysis_successful": False,
                "error": str(e),
            }

    def _extract_workflow_patterns(self, source_path: str, artifact) -> Dict[str, Any]:
        """Extract workflow patterns from ArtifactForge parsed data"""

        # Get the actual Python source for detailed analysis
        with open(source_path, "r") as f:
            source_code = f.read()

        # Parse with AST for workflow analysis
        tree = ast.parse(source_code)

        # Extract workflow nodes and edges
        nodes = []
        edges = []

        # Start node
        nodes.append(
            WorkflowNode(
                name="Start",
                node_type="start",
                line_number=1,
                content="Module Entry Point",
            )
        )

        # Analyze classes and methods for workflow
        for class_info in artifact.parsed_data.get("classes", []):
            class_name = class_info["name"]

            # Add class processing node
            nodes.append(
                WorkflowNode(
                    name=f"Process {class_name}",
                    node_type="activity",
                    line_number=class_info["line_number"],
                    content=f"Process class: {class_name}",
                )
            )

            # Connect start to class processing
            edges.append(
                WorkflowEdge(
                    from_node="Start",
                    to_node=f"Process {class_name}",
                    label="Initialize",
                )
            )

            # Analyze methods for workflow patterns
            method_nodes = self._analyze_method_workflow(
                source_code, class_name, class_info
            )
            nodes.extend(method_nodes)

            # Connect class processing to first method
            if method_nodes:
                edges.append(
                    WorkflowEdge(
                        from_node=f"Process {class_name}",
                        to_node=method_nodes[0].name,
                        label="Execute Methods",
                    )
                )

        # Analyze standalone functions
        for func_info in artifact.parsed_data.get("functions", []):
            func_name = func_info["name"]

            # Add function execution node
            nodes.append(
                WorkflowNode(
                    name=f"Execute {func_name}",
                    node_type="activity",
                    line_number=func_info["line_number"],
                    content=f"Execute function: {func_name}",
                )
            )

            # Connect start to function execution
            edges.append(
                WorkflowEdge(
                    from_node="Start",
                    to_node=f"Execute {func_name}",
                    label="Call Function",
                )
            )

        # End node
        nodes.append(
            WorkflowNode(
                name="End",
                node_type="end",
                line_number=len(source_code.splitlines()),
                content="Module Complete",
            )
        )

        # Connect all final nodes to end
        for node in nodes:
            if node.node_type in ["activity", "decision", "merge"]:
                # Check if this node has no outgoing edges
                has_outgoing = any(edge.from_node == node.name for edge in edges)
                if not has_outgoing:
                    edges.append(
                        WorkflowEdge(
                            from_node=node.name, to_node="End", label="Complete"
                        )
                    )

        return {
            "source_path": source_path,
            "workflow_analysis_successful": True,
            "nodes": [self._node_to_dict(node) for node in nodes],
            "edges": [self._edge_to_dict(edge) for edge in edges],
            "complexity": len(nodes) + len(edges),
        }

    def _analyze_method_workflow(
        self, source_code: str, class_name: str, class_info: Dict
    ) -> List[WorkflowNode]:
        """Analyze individual methods for workflow patterns"""
        nodes = []

        # Find the class definition in source
        class_pattern = rf"class\s+{class_name}\s*[\(:]"
        class_match = re.search(class_pattern, source_code)

        if class_match:
            class_start = class_match.start()

            # Find method definitions within the class
            method_pattern = rf"def\s+(\w+)\s*\("
            method_matches = re.finditer(method_pattern, source_code[class_start:])

            for match in method_matches:
                method_name = match.group(1)
                method_start = class_start + match.start()

                # Extract method content
                method_content = self._extract_method_content(source_code, method_start)

                # Analyze method for control flow
                method_nodes = self._analyze_method_control_flow(
                    method_name, method_content
                )
                nodes.extend(method_nodes)

        return nodes

    def _extract_method_content(self, source_code: str, method_start: int) -> str:
        """Extract the content of a method from source code"""
        # Find the indentation level of the method
        lines = source_code[method_start:].split("\n")
        if not lines:
            return ""

        # Get the indentation of the method definition
        method_line = lines[0]
        indent_level = len(method_line) - len(method_line.lstrip())

        # Find where the method ends (next line with same or less indentation)
        method_lines = [lines[0]]
        for line in lines[1:]:
            if line.strip() == "":
                method_lines.append(line)
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level and line.strip():
                break

            method_lines.append(line)

        return "\n".join(method_lines)

    def _analyze_method_control_flow(
        self, method_name: str, method_content: str
    ) -> List[WorkflowNode]:
        """Analyze method content for control flow patterns"""
        nodes = []

        # Add method entry node
        nodes.append(
            WorkflowNode(
                name=f"{method_name}_entry",
                node_type="activity",
                line_number=0,
                content=f"Enter {method_name}",
            )
        )

        # Look for control flow patterns
        lines = method_content.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()

            # Decision points (if/elif/else)
            if line.startswith("if "):
                condition = line[3:].rstrip(":")
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_if_{i}",
                        node_type="decision",
                        line_number=i,
                        content=f"if {condition}",
                        conditions=[condition],
                    )
                )

            elif line.startswith("elif "):
                condition = line[6:].rstrip(":")
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_elif_{i}",
                        node_type="decision",
                        line_number=i,
                        content=f"elif {condition}",
                        conditions=[condition],
                    )
                )

            elif line.startswith("else:"):
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_else_{i}",
                        node_type="decision",
                        line_number=i,
                        content="else",
                        conditions=["default"],
                    )
                )

            # Loops
            elif line.startswith("for "):
                loop_var = line[4:].split(" in ")[0].strip()
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_for_{i}",
                        node_type="activity",
                        line_number=i,
                        content=f"for {loop_var} in collection",
                    )
                )

            elif line.startswith("while "):
                condition = line[6:].rstrip(":")
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_while_{i}",
                        node_type="decision",
                        line_number=i,
                        content=f"while {condition}",
                        conditions=[condition],
                    )
                )

            # Try/except blocks
            elif line.startswith("try:"):
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_try_{i}",
                        node_type="activity",
                        line_number=i,
                        content="try block",
                    )
                )

            elif line.startswith("except "):
                exception = line[7:].rstrip(":")
                nodes.append(
                    WorkflowNode(
                        name=f"{method_name}_except_{i}",
                        node_type="activity",
                        line_number=i,
                        content=f"except {exception}",
                    )
                )

        # Add method exit node
        nodes.append(
            WorkflowNode(
                name=f"{method_name}_exit",
                node_type="activity",
                line_number=len(lines),
                content=f"Exit {method_name}",
            )
        )

        return nodes

    def _node_to_dict(self, node: WorkflowNode) -> Dict[str, Any]:
        """Convert WorkflowNode to dictionary"""
        return {
            "name": node.name,
            "type": node.node_type,
            "line_number": node.line_number,
            "content": node.content,
            "conditions": node.conditions or [],
            "branches": node.branches or [],
        }

    def _edge_to_dict(self, edge: WorkflowEdge) -> Dict[str, Any]:
        """Convert WorkflowEdge to dictionary"""
        return {
            "from": edge.from_node,
            "to": edge.to_node,
            "label": edge.label,
            "condition": edge.condition,
        }

    def generate_mermaid_activity_diagram(self, workflow_data: Dict[str, Any]) -> str:
        """Generate Mermaid activity diagram syntax from workflow data"""

        if not workflow_data.get("workflow_analysis_successful", False):
            return "# Workflow analysis failed"

        nodes = workflow_data.get("nodes", [])
        edges = workflow_data.get("edges", [])

        mermaid_lines = [
            "flowchart TD",
            "    %% Workflow Analysis Generated from Python Code",
            "",
        ]

        # Generate nodes
        for node in nodes:
            node_name = node["name"].replace(" ", "_").replace("-", "_")
            # Clean and escape node content for Mermaid
            node_content = self._clean_mermaid_text(node["content"])

            if node["type"] == "start":
                mermaid_lines.append(f"    {node_name}([{node_content}])")
            elif node["type"] == "end":
                mermaid_lines.append(f"    {node_name}([{node_content}])")
            elif node["type"] == "decision":
                mermaid_lines.append(f"    {node_name}{{{node_content}}}")
            elif node["type"] == "activity":
                mermaid_lines.append(f"    {node_name}[{node_content}]")
            else:
                mermaid_lines.append(f"    {node_name}[{node_content}]")

        mermaid_lines.append("")

        # Generate edges
        for edge in edges:
            from_node = edge["from"].replace(" ", "_").replace("-", "_")
            to_node = edge["to"].replace(" ", "_").replace("-", "_")
            label = self._clean_mermaid_text(edge["label"])
            condition = self._clean_mermaid_text(edge["condition"])

            if condition:
                mermaid_lines.append(f"    {from_node} -->|{condition}| {to_node}")
            elif label:
                mermaid_lines.append(f"    {from_node} -->|{label}| {to_node}")
            else:
                mermaid_lines.append(f"    {from_node} --> {to_node}")

        return "\n".join(mermaid_lines)

    def _clean_mermaid_text(self, text: str) -> str:
        """Clean and escape text for Mermaid syntax"""
        if not text:
            return ""

        # Remove quotes and special characters that break Mermaid
        cleaned = text.replace('"', "").replace("'", "")
        cleaned = cleaned.replace("{", "(").replace("}", ")")
        cleaned = cleaned.replace("[", "(").replace("]", ")")
        cleaned = cleaned.replace("|", "-")
        cleaned = cleaned.replace("-->", "->")

        # Limit length to prevent diagram overflow
        if len(cleaned) > 50:
            cleaned = cleaned[:47] + "..."

        return cleaned

    def save_mermaid_diagram(
        self, workflow_data: Dict[str, Any], output_path: str
    ) -> str:
        """Save Mermaid activity diagram to file"""

        mermaid_syntax = self.generate_mermaid_activity_diagram(workflow_data)

        # Save Mermaid syntax
        mermaid_path = output_path.replace(".svg", ".mmd")
        with open(mermaid_path, "w") as f:
            f.write(mermaid_syntax)

        logger.info(f"💾 Mermaid syntax saved to: {mermaid_path}")

        # For now, return the Mermaid syntax
        # In production, you'd use a Mermaid renderer to generate SVG
        return mermaid_path
