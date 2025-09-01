#!/usr/bin/env python3
"""
Lightweight Activity Diagram Generator

A headless activity diagram generator that combines:
- AST parsing for Python code analysis
- PlantUML syntax generation for activity diagrams
- Graphviz for SVG output

This provides the same functionality as StarUML's CLI but without GUI requirements.
"""

import ast
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json


class LightweightActivityGenerator:
    """Generate UML activity diagrams from Python code without GUI requirements."""

    def __init__(self):
        self.plantuml_jar = self._find_plantuml_jar()
        self.java_available = self._check_java()

    def _find_plantuml_jar(self) -> Optional[str]:
        """Find PlantUML JAR file in common locations."""
        common_paths = [
            "/usr/share/plantuml/plantuml.jar",
            "/opt/plantuml/plantuml.jar",
            "plantuml.jar",  # Current directory
            os.path.expanduser("~/.local/share/plantuml/plantuml.jar"),
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

    def _check_java(self) -> bool:
        """Check if Java is available."""
        try:
            subprocess.run(["java", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze Python file and extract workflow information."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            analyzer = PythonWorkflowAnalyzer()
            return analyzer.analyze_workflow(tree, file_path)

        except Exception as e:
            return {"success": False, "error": str(e), "file_path": file_path}

    def generate_plantuml_activity(self, workflow_data: Dict[str, Any]) -> str:
        """Generate PlantUML activity diagram syntax."""
        if not workflow_data.get("success", False):
            return f"// Error analyzing file: {workflow_data.get('error', 'Unknown error')}"

        nodes = workflow_data.get("nodes", [])
        edges = workflow_data.get("edges", [])

        plantuml_lines = [
            "@startuml",
            "!theme plain",
            "skinparam backgroundColor transparent",
            "skinparam activityFontSize 12",
            "skinparam activityFontName Arial",
            "",
            "title Activity Diagram - " + workflow_data.get("file_name", "Unknown"),
            "",
        ]

        # Generate nodes
        for node in nodes:
            node_id = node["id"]
            node_type = node["type"]
            label = node.get("label", "Unknown")

            if node_type == "start":
                plantuml_lines.append(f"start")
            elif node_type == "end":
                plantuml_lines.append(f"stop")
            elif node_type == "decision":
                plantuml_lines.append(f"if ({label}) then (yes)")
                plantuml_lines.append(f"else (no)")
                plantuml_lines.append(f"endif")
            elif node_type == "activity":
                plantuml_lines.append(f":{label};")
            elif node_type == "loop":
                plantuml_lines.append(f"while ({label}) is (continue)")
                plantuml_lines.append(f"endwhile (exit)")

        plantuml_lines.append("")

        # Generate edges (flow control)
        for edge in edges:
            from_node = edge["from"]
            to_node = edge["to"]
            label = edge.get("label", "")

            if label:
                plantuml_lines.append(f"{from_node} --> {to_node} : {label}")
            else:
                plantuml_lines.append(f"{from_node} --> {to_node}")

        plantuml_lines.append("@enduml")
        return "\n".join(plantuml_lines)

    def generate_svg(self, plantuml_code: str, output_path: str) -> bool:
        """Generate SVG from PlantUML code using multiple methods."""

        # Method 1: Try PlantUML JAR + Java
        if self.plantuml_jar and self.java_available:
            if self._generate_svg_plantuml_jar(plantuml_code, output_path):
                return True

        # Method 2: Try PlantUML server (if available)
        if self._generate_svg_plantuml_server(plantuml_code, output_path):
            return True

        # Method 3: Try Graphviz directly (fallback)
        if self._generate_svg_graphviz(plantuml_code, output_path):
            return True

        return False

    def _generate_svg_plantuml_jar(self, plantuml_code: str, output_path: str) -> bool:
        """Generate SVG using PlantUML JAR file."""
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".puml", delete=False) as f:
                f.write(plantuml_code)
                temp_file = f.name

            # Run PlantUML JAR
            result = subprocess.run(
                [
                    "java",
                    "-jar",
                    self.plantuml_jar,
                    "-tsvg",
                    temp_file,
                    "-o",
                    os.path.dirname(output_path),
                ],
                capture_output=True,
                text=True,
            )

            os.unlink(temp_file)

            if result.returncode == 0:
                # PlantUML generates with .puml.svg extension
                expected_output = temp_file.replace(".puml", ".puml.svg")
                if os.path.exists(expected_output):
                    os.rename(expected_output, output_path)
                    return True

            return False

        except Exception:
            return False

    def _generate_svg_plantuml_server(self, plantuml_code: str, output_path: str) -> bool:
        """Generate SVG using PlantUML server."""
        try:
            import requests

            # Try local PlantUML server
            response = requests.post(
                "http://localhost:8080/plantuml/svg/",
                data=plantuml_code,
                headers={"Content-Type": "text/plain"},
                timeout=10,
            )

            if response.status_code == 200:
                with open(output_path, "w") as f:
                    f.write(response.text)
                return True

            return False

        except Exception:
            return False

    def _generate_svg_graphviz(self, plantuml_code: str, output_path: str) -> bool:
        """Generate SVG using Graphviz directly (simplified approach)."""
        try:
            # Convert PlantUML to DOT format (simplified)
            dot_code = self._plantuml_to_dot(plantuml_code)

            with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
                f.write(dot_code)
                temp_file = f.name

            # Use Graphviz to generate SVG
            result = subprocess.run(
                ["dot", "-Tsvg", temp_file, "-o", output_path],
                capture_output=True,
                text=True,
            )

            os.unlink(temp_file)
            return result.returncode == 0

        except Exception:
            return False

    def _plantuml_to_dot(self, plantuml_code: str) -> str:
        """Convert PlantUML activity syntax to Graphviz DOT format."""
        # This is a simplified conversion - in practice, you'd want a more robust parser
        dot_lines = [
            "digraph G {",
            "  rankdir=TB;",
            "  node [shape=box, style=filled, fillcolor=lightblue];",
            "  edge [fontsize=10];",
            "",
        ]

        # Simple node extraction (this is a basic implementation)
        lines = plantuml_code.split("\n")
        node_counter = 0
        nodes = {}

        for line in lines:
            line = line.strip()
            if line.startswith(":") and line.endswith(";"):
                node_counter += 1
                node_id = f"node_{node_counter}"
                label = line[1:-1]  # Remove : and ;
                nodes[node_id] = label
                dot_lines.append(f'  {node_id} [label="{label}"];')
            elif line.startswith("start"):
                node_counter += 1
                node_id = f"start_{node_counter}"
                nodes[node_id] = "Start"
                dot_lines.append(f'  {node_id} [shape=oval, fillcolor=lightgreen, label="Start"];')
            elif line.startswith("stop"):
                node_counter += 1
                node_id = f"stop_{node_counter}"
                nodes[node_id] = "Stop"
                dot_lines.append(f'  {node_id} [shape=oval, fillcolor=lightcoral, label="Stop"];')

        # Add edges (simplified)
        for i in range(1, node_counter):
            dot_lines.append(f"  node_{i} -> node_{i + 1};")

        dot_lines.append("}")
        return "\n".join(dot_lines)

    def generate_activity_diagram(self, python_file: str, output_dir: str = "generated_activity_models") -> Dict[str, Any]:
        """Main method to generate activity diagram from Python file."""
        result = {
            "success": False,
            "input_file": python_file,
            "output_files": [],
            "errors": [],
        }

        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Analyze Python file
            workflow_data = self.analyze_python_file(python_file)
            if not workflow_data.get("success", False):
                result["errors"].append(f"Analysis failed: {workflow_data.get('error', 'Unknown error')}")
                return result

            # Generate PlantUML code
            plantuml_code = self.generate_plantuml_activity(workflow_data)

            # Save PlantUML code
            base_name = Path(python_file).stem
            plantuml_file = os.path.join(output_dir, f"{base_name}_activity.puml")
            with open(plantuml_file, "w") as f:
                f.write(plantuml_code)
            result["output_files"].append(plantuml_file)

            # Generate SVG
            svg_file = os.path.join(output_dir, f"{base_name}_activity.svg")
            if self.generate_svg(plantuml_code, svg_file):
                result["output_files"].append(svg_file)
                result["success"] = True
            else:
                result["errors"].append("SVG generation failed with all methods")

            return result

        except Exception as e:
            result["errors"].append(f"Unexpected error: {str(e)}")
            return result


class PythonWorkflowAnalyzer:
    """Analyze Python AST to extract workflow information."""

    def analyze_workflow(self, tree: ast.AST, file_path: str) -> Dict[str, Any]:
        """Analyze AST and extract workflow nodes and edges."""
        analyzer = WorkflowVisitor()
        analyzer.visit(tree)

        return {
            "success": True,
            "file_path": file_path,
            "file_name": Path(file_path).name,
            "nodes": analyzer.nodes,
            "edges": analyzer.edges,
            "workflow_analysis_successful": True,
        }


class WorkflowVisitor(ast.NodeVisitor):
    """AST visitor to extract workflow information."""

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_counter = 0
        self.last_node = None

    def _add_node(self, node_type: str, label: str) -> str:
        """Add a node and return its ID."""
        self.node_counter += 1
        node_id = f"node_{self.node_counter}"

        self.nodes.append({"id": node_id, "type": node_type, "label": label})

        # Add edge from last node if exists
        if self.last_node:
            self.edges.append({"from": self.last_node, "to": node_id, "label": ""})

        self.last_node = node_id
        return node_id

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions."""
        # Add function start
        start_id = self._add_node("start", f"Function: {node.name}")

        # Visit function body
        self.generic_visit(node)

        # Add function end
        end_id = self._add_node("end", f"End: {node.name}")

        # Connect last node to end
        if self.last_node and self.last_node != end_id:
            self.edges.append({"from": self.last_node, "to": end_id, "label": ""})

    def visit_If(self, node: ast.If):
        """Visit if statements."""
        # Add decision node
        test_str = ast.unparse(node.test) if hasattr(ast, "unparse") else str(node.test)
        decision_id = self._add_node("decision", test_str)

        # Store current last_node
        current_last = self.last_node

        # Visit if body
        self.last_node = decision_id
        for item in node.body:
            self.visit(item)

        # Visit else body if exists
        if node.orelse:
            self.last_node = decision_id
            for item in node.orelse:
                self.visit(item)

        # Reset last_node for continuation
        self.last_node = current_last

    def visit_While(self, node: ast.While):
        """Visit while loops."""
        # Add loop start
        test_str = ast.unparse(node.test) if hasattr(ast, "unparse") else str(node.test)
        loop_id = self._add_node("loop", f"While: {test_str}")

        # Store current last_node
        current_last = self.last_node

        # Visit loop body
        self.last_node = loop_id
        for item in node.body:
            self.visit(item)

        # Reset last_node for continuation
        self.last_node = current_last

    def visit_For(self, node: ast.For):
        """Visit for loops."""
        # Add loop start
        target_str = ast.unparse(node.target) if hasattr(ast, "unparse") else str(node.target)
        iter_str = ast.unparse(node.iter) if hasattr(ast, "unparse") else str(node.iter)
        loop_id = self._add_node("loop", f"For: {target_str} in {iter_str}")

        # Store current last_node
        current_last = self.last_node

        # Visit loop body
        self.last_node = loop_id
        for item in node.body:
            self.visit(item)

        # Reset last_node for continuation
        self.last_node = current_last

    def visit_Expr(self, node: ast.Expr):
        """Visit expressions (function calls, assignments, etc.)."""
        if isinstance(node.value, ast.Call):
            # Function call
            if hasattr(node.value.func, "id"):
                func_name = node.value.func.id
                self._add_node("activity", f"Call: {func_name}()")
            else:
                self._add_node("activity", "Function Call")
        elif isinstance(node.value, ast.Assign):
            # Assignment
            if hasattr(node.value.targets[0], "id"):
                var_name = node.value.targets[0].id
                self._add_node("activity", f"Assign: {var_name}")
            else:
                self._add_node("activity", "Assignment")
        else:
            # Other expressions
            self._add_node("activity", "Expression")


def main():
    """Test the lightweight activity generator."""
    generator = LightweightActivityGenerator()

    # Test with a simple Python file
    test_file = "src/round_trip_engineering/simple_workflow_analyzer.py"

    if os.path.exists(test_file):
        print(f"Generating activity diagram for: {test_file}")
        result = generator.generate_activity_diagram(test_file)

        if result["success"]:
            print("✅ Activity diagram generated successfully!")
            print("Output files:")
            for file_path in result["output_files"]:
                print(f"  - {file_path}")
        else:
            print("❌ Failed to generate activity diagram:")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"Test file not found: {test_file}")


if __name__ == "__main__":
    main()
