#!/usr/bin/env python3
"""
Simple Workflow Analyzer for Demonstration

This module creates a simplified workflow analysis that generates
clean, working Mermaid syntax for UML activity diagrams.
"""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleWorkflowAnalyzer:
    """Simplified workflow analyzer that generates clean Mermaid syntax"""

    def __init__(self):
        logger.info("🔍 Simple workflow analyzer initialized")

    def analyze_simple_workflow(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze Python code and generate a simplified workflow

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing simplified workflow analysis
        """
        logger.info(f"🔍 Analyzing simple workflow for: {source_path}")

        try:
            with open(source_path, "r") as f:
                source_code = f.read()

            # Parse with AST
            tree = ast.parse(source_code)

            # Extract simplified workflow
            workflow_data = self._extract_simple_workflow(
                source_path, source_code, tree
            )

            logger.info(
                f"✅ Simple workflow analysis completed: {len(workflow_data.get('nodes', []))} nodes"
            )
            return workflow_data

        except Exception as e:
            logger.error(f"❌ Simple workflow analysis failed: {e}")
            return {
                "source_path": source_path,
                "workflow_analysis_successful": False,
                "error": str(e),
            }

    def _extract_simple_workflow(
        self, source_path: str, source_code: str, tree: ast.AST
    ) -> Dict[str, Any]:
        """Extract a simplified workflow from Python code"""

        nodes = []
        edges = []

        # Start node
        nodes.append({"id": "start", "type": "start", "label": "Start"})

        # Find classes
        class_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_count += 1
                class_name = node.name

                # Add class processing node
                nodes.append(
                    {
                        "id": f"class_{class_name}",
                        "type": "activity",
                        "label": f"Process {class_name}",
                    }
                )

                # Connect start to class
                edges.append(
                    {
                        "from": "start",
                        "to": f"class_{class_name}",
                        "label": "Initialize",
                    }
                )

                # Add method nodes (simplified)
                method_count = 0
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_count += 1
                        if method_count <= 3:  # Limit to first 3 methods
                            method_id = f"method_{class_name}_{item.name}"
                            nodes.append(
                                {
                                    "id": method_id,
                                    "type": "activity",
                                    "label": f"{item.name}()",
                                }
                            )

                            # Connect class to method
                            edges.append(
                                {
                                    "from": f"class_{class_name}",
                                    "to": method_id,
                                    "label": "Execute",
                                }
                            )

                # Add decision point if methods found
                if method_count > 0:
                    decision_id = f"decision_{class_name}"
                    nodes.append(
                        {
                            "id": decision_id,
                            "type": "decision",
                            "label": "Methods Complete?",
                        }
                    )

                    # Connect last method to decision
                    if method_count <= 3:
                        # Find the last method
                        last_method = None
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                last_method = f"method_{class_name}_{item.name}"

                        if last_method:
                            edges.append(
                                {
                                    "from": last_method,
                                    "to": decision_id,
                                    "label": "Complete",
                                }
                            )
                    else:
                        edges.append(
                            {
                                "from": f"class_{class_name}",
                                "to": decision_id,
                                "label": "Process",
                            }
                        )

        # Find standalone functions (simplified approach)
        function_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if this function is at module level (not in a class)
                # We'll assume it's standalone if we can't determine otherwise
                function_count += 1
                if function_count <= 2:  # Limit to first 2 functions
                    func_id = f"function_{node.name}"
                    nodes.append(
                        {
                            "id": func_id,
                            "type": "activity",
                            "label": f"Function: {node.name}()",
                        }
                    )

                    # Connect start to function
                    edges.append({"from": "start", "to": func_id, "label": "Call"})

        # End node
        nodes.append({"id": "end", "type": "end", "label": "End"})

        # Connect all final nodes to end
        for workflow_node in nodes:
            if workflow_node["type"] in ["activity", "decision"]:
                # Check if this node has no outgoing edges
                has_outgoing = any(
                    edge["from"] == workflow_node["id"] for edge in edges
                )
                if not has_outgoing:
                    edges.append(
                        {"from": workflow_node["id"], "to": "end", "label": "Complete"}
                    )

        return {
            "source_path": source_path,
            "workflow_analysis_successful": True,
            "nodes": nodes,
            "edges": edges,
            "complexity": len(nodes) + len(edges),
        }

    def _clean_mermaid_text(self, text: str) -> str:
        """
        Cleans text for Mermaid diagram labels to avoid special characters.
        """
        # Replace common Mermaid special characters with underscores
        text = text.replace("|", "_")
        text = text.replace(">", "_")
        text = text.replace("<", "_")
        text = text.replace("(", "_")
        text = text.replace(")", "_")
        text = text.replace("[", "_")
        text = text.replace("]", "_")
        text = text.replace("{", "_")
        text = text.replace("}", "_")
        text = text.replace("*", "_")
        text = text.replace("&", "_")
        text = text.replace("#", "_")
        text = text.replace("@", "_")
        text = text.replace("!", "_")
        text = text.replace("?", "_")
        text = text.replace("+", "_")
        text = text.replace("-", "_")
        text = text.replace("=", "_")
        text = text.replace(".", "_")
        text = text.replace(",", "_")
        text = text.replace(";", "_")
        text = text.replace(":", "_")
        text = text.replace(" ", "_")
        text = text.replace("\t", "_")
        text = text.replace("\n", "_")
        text = text.replace("\r", "_")
        text = text.replace('"', "_")
        text = text.replace("'", "_")
        text = text.replace("`", "_")
        text = text.replace("~", "_")
        text = text.replace("^", "_")
        text = text.replace("\\", "_")
        text = text.replace("/", "_")
        text = text.replace("|", "_")  # Double replacement for robustness
        return text

    def generate_clean_mermaid(self, workflow_data: Dict[str, Any]) -> str:
        """Generate clean, working Mermaid syntax"""

        if not workflow_data.get("workflow_analysis_successful", False):
            return "# Workflow analysis failed"

        nodes = workflow_data.get("nodes", [])
        edges = workflow_data.get("edges", [])

        mermaid_lines = ["flowchart TD", "    %% Simple Workflow Analysis", ""]

        # Create clean ID mapping
        id_mapping = {}
        clean_id_counter = 0

        # Generate nodes with clean IDs
        for node in nodes:
            # Create a very simple, clean ID
            clean_id_counter += 1
            clean_id = f"n{clean_id_counter}"
            id_mapping[node["id"]] = clean_id

            node_type = node["type"]
            label = self._clean_mermaid_text(node["label"])

            if node_type == "start":
                mermaid_lines.append(f"    {clean_id}([{label}])")
            elif node_type == "end":
                mermaid_lines.append(f"    {clean_id}([{label}])")
            elif node_type == "decision":
                mermaid_lines.append(f"    {clean_id}{{{label}}}")
            elif node_type == "activity":
                mermaid_lines.append(f"    {clean_id}[{label}]")

        mermaid_lines.append("")

        # Generate edges using clean IDs
        for edge in edges:
            from_node = id_mapping.get(edge["from"], edge["from"])
            to_node = id_mapping.get(edge["to"], edge["to"])
            label = self._clean_mermaid_text(edge["label"])

            if label:
                mermaid_lines.append(f"    {from_node} -->|{label}| {to_node}")
            else:
                mermaid_lines.append(f"    {from_node} --> {to_node}")

        return "\n".join(mermaid_lines)

    def save_clean_mermaid(
        self, workflow_data: Dict[str, Any], output_path: str
    ) -> str:
        """Save clean Mermaid syntax to file"""

        mermaid_syntax = self.generate_clean_mermaid(workflow_data)

        # Save Mermaid syntax
        mermaid_path = output_path.replace(".svg", ".mmd")
        with open(mermaid_path, "w") as f:
            f.write(mermaid_syntax)

        logger.info(f"💾 Clean Mermaid syntax saved to: {mermaid_path}")
        return mermaid_path
