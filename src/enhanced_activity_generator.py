#!/usr/bin/env python3
"""
Enhanced Activity Diagram Generator

Integrates the StarUML Python extension's mature AST parser with our workflow analysis
to generate professional-quality UML activity diagrams from Python code.

This combines:
- StarUML extension's proven AST parsing (ast2json.py)
- Enhanced workflow analysis for activity diagrams
- Multiple SVG generation methods (PlantUML JAR, server, Graphviz)
- Professional UML compliance
"""

import ast
import subprocess
import tempfile
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys

# Add the StarUML extension to our path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "external", "staruml-python")
)


class EnhancedActivityGenerator:
    """Generate UML activity diagrams from Python code using StarUML extension's AST parser."""

    def __init__(self):
        self.plantuml_jar = self._find_plantuml_jar()
        self.java_available = self._check_java()
        self.ast_parser_path = os.path.join(
            os.path.dirname(__file__), "..", "external", "staruml-python", "ast2json.py"
        )

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

    def analyze_python_file_enhanced(self, file_path: str) -> Dict[str, Any]:
        """Analyze Python file using StarUML extension's AST parser."""
        try:
            # Use the StarUML extension's AST parser
            result = subprocess.run(
                [sys.executable, self.ast_parser_path, file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the JSON output
            ast_data = json.loads(result.stdout)

            # Extract workflow information from the AST
            workflow_analyzer = EnhancedWorkflowAnalyzer()
            return workflow_analyzer.analyze_workflow_from_ast(ast_data, file_path)

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
            "skinparam activityDiamondBackgroundColor lightyellow",
            "skinparam activityStartColor lightgreen",
            "skinparam activityEndColor lightcoral",
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
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".puml", delete=False
            ) as f:
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

    def _generate_svg_plantuml_server(
        self, plantuml_code: str, output_path: str
    ) -> bool:
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

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".dot", delete=False
            ) as f:
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
                dot_lines.append(
                    f'  {node_id} [shape=oval, fillcolor=lightgreen, label="Start"];'
                )
            elif line.startswith("stop"):
                node_counter += 1
                node_id = f"stop_{node_counter}"
                nodes[node_id] = "Stop"
                dot_lines.append(
                    f'  {node_id} [shape=oval, fillcolor=lightcoral, label="Stop"];'
                )

        # Add edges (simplified)
        for i in range(1, node_counter):
            dot_lines.append(f"  node_{i} -> node_{i + 1};")

        dot_lines.append("}")
        return "\n".join(dot_lines)

    def generate_activity_diagram(
        self, python_file: str, output_dir: str = "generated_activity_models"
    ) -> Dict[str, Any]:
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

            # Analyze Python file using enhanced StarUML extension parser
            workflow_data = self.analyze_python_file_enhanced(python_file)
            if not workflow_data.get("success", False):
                result["errors"].append(
                    f"Analysis failed: {workflow_data.get('error', 'Unknown error')}"
                )
                return result

            # Generate PlantUML code
            plantuml_code = self.generate_plantuml_activity(workflow_data)

            # Save PlantUML code
            base_name = Path(python_file).stem
            plantuml_file = os.path.join(
                output_dir, f"{base_name}_enhanced_activity.puml"
            )
            with open(plantuml_file, "w") as f:
                f.write(plantuml_code)
            result["output_files"].append(plantuml_file)

            # Generate SVG
            svg_file = os.path.join(output_dir, f"{base_name}_enhanced_activity.svg")
            if self.generate_svg(plantuml_code, svg_file):
                result["output_files"].append(svg_file)
                result["success"] = True
            else:
                result["errors"].append("SVG generation failed with all methods")

            return result

        except Exception as e:
            result["errors"].append(f"Unexpected error: {str(e)}")
            return result


class EnhancedWorkflowAnalyzer:
    """Analyze Python AST (from StarUML extension) to extract workflow information."""

    def analyze_workflow_from_ast(
        self, ast_data: Dict[str, Any], file_path: str
    ) -> Dict[str, Any]:
        """Analyze AST data and extract workflow nodes and edges."""
        try:
            # Extract workflow information from the AST
            nodes = []
            edges = []

            # Process the AST data to extract workflow
            self._extract_workflow_from_ast(ast_data, nodes, edges)

            return {
                "success": True,
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "nodes": nodes,
                "edges": edges,
                "workflow_analysis_successful": True,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "file_path": file_path}

    def _extract_workflow_from_ast(
        self, ast_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Recursively extract workflow information from AST data."""
        if not isinstance(ast_data, dict):
            return

        # Look for key AST node types
        for node_type, node_data in ast_data.items():
            if node_type == "Module":
                self._extract_workflow_from_ast(node_data, nodes, edges)
            elif node_type == "FunctionDef":
                self._process_function_def(node_data, nodes, edges)
            elif node_type == "If":
                self._process_if_statement(node_data, nodes, edges)
            elif node_type == "While":
                self._process_while_loop(node_data, nodes, edges)
            elif node_type == "For":
                self._process_for_loop(node_data, nodes, edges)
            elif node_type == "Expr":
                self._process_expression(node_data, nodes, edges)
            elif isinstance(node_data, dict):
                self._extract_workflow_from_ast(node_data, nodes, edges)
            elif isinstance(node_data, list):
                for item in node_data:
                    self._extract_workflow_from_ast(item, nodes, edges)

    def _process_function_def(
        self, func_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Process function definition."""
        if "name" in func_data:
            func_name = func_data["name"]

            # Add function start node
            start_node = {
                "id": f"func_start_{func_name}",
                "type": "start",
                "label": f"Function: {func_name}",
            }
            nodes.append(start_node)

            # Process function body
            if "body" in func_data:
                self._extract_workflow_from_ast(func_data["body"], nodes, edges)

            # Add function end node
            end_node = {
                "id": f"func_end_{func_name}",
                "type": "end",
                "label": f"End: {func_name}",
            }
            nodes.append(end_node)

            # Connect last activity node to end, or start to end if no activities
            if nodes and len(nodes) > 1:
                # Find the last non-end node
                last_activity = None
                for node in reversed(nodes[:-1]):  # Exclude the end node we just added
                    if node["type"] != "end":
                        last_activity = node
                        break

                if last_activity:
                    edges.append(
                        {"from": last_activity["id"], "to": end_node["id"], "label": ""}
                    )
                else:
                    # No activities, connect start to end
                    edges.append(
                        {"from": start_node["id"], "to": end_node["id"], "label": ""}
                    )

    def _process_if_statement(
        self, if_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Process if statement."""
        if "test" in if_data:
            # Simplify the test expression for readability
            test_str = self._simplify_expression(if_data["test"])

            # Add decision node
            decision_node = {
                "id": f"decision_{len(nodes)}",
                "type": "decision",
                "label": test_str,
            }
            nodes.append(decision_node)

            # Process if body
            if "body" in if_data:
                self._extract_workflow_from_ast(if_data["body"], nodes, edges)

            # Process else body
            if "orelse" in if_data:
                self._extract_workflow_from_ast(if_data["orelse"], nodes, edges)

    def _process_while_loop(
        self, while_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Process while loop."""
        if "test" in while_data:
            test_str = self._simplify_expression(while_data["test"])

            # Add loop node
            loop_node = {
                "id": f"loop_{len(nodes)}",
                "type": "loop",
                "label": f"While: {test_str}",
            }
            nodes.append(loop_node)

            # Process loop body
            if "body" in while_data:
                self._extract_workflow_from_ast(while_data["body"], nodes, edges)

    def _process_for_loop(
        self, for_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Process for loop."""
        target_str = self._simplify_expression(for_data.get("target", "item"))
        iter_str = self._simplify_expression(for_data.get("iter", "collection"))

        # Add loop node
        loop_node = {
            "id": f"loop_{len(nodes)}",
            "type": "loop",
            "label": f"For: {target_str} in {iter_str}",
        }
        nodes.append(loop_node)

        # Process loop body
        if "body" in for_data:
            self._extract_workflow_from_ast(for_data["body"], nodes, edges)

    def _process_expression(
        self, expr_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]
    ):
        """Process expression."""
        if "value" in expr_data:
            value_data = expr_data["value"]

            if isinstance(value_data, dict):
                if "Call" in value_data:
                    # Function call
                    func_name = self._extract_function_name(value_data["Call"])
                    activity_node = {
                        "id": f"activity_{len(nodes)}",
                        "type": "activity",
                        "label": f"Call: {func_name}()",
                    }
                    nodes.append(activity_node)
                elif "Assign" in value_data:
                    # Assignment
                    target = value_data["Assign"].get("targets", ["var"])
                    var_name = self._simplify_expression(target[0]) if target else "var"
                    activity_node = {
                        "id": f"activity_{len(nodes)}",
                        "type": "activity",
                        "label": f"Assign: {var_name}",
                    }
                    nodes.append(activity_node)

    def _simplify_expression(self, expr_data: Any) -> str:
        """Simplify complex expressions for readable labels."""
        if isinstance(expr_data, dict):
            if "Name" in expr_data:
                return expr_data["Name"].get("id", "var")
            elif "Constant" in expr_data:
                return str(expr_data["Constant"].get("value", ""))
            elif "Compare" in expr_data:
                # Simplify comparison expressions
                left = self._simplify_expression(expr_data["Compare"].get("left", ""))
                right = self._simplify_expression(
                    expr_data["Compare"].get("comparators", [""])[0]
                )
                return f"{left} == {right}"
            else:
                return str(expr_data)[:50]  # Truncate long expressions
        else:
            return str(expr_data)[:50]

    def _extract_function_name(self, call_data: Dict[str, Any]) -> str:
        """Extract function name from call data."""
        if "func" in call_data:
            func_data = call_data["func"]
            if isinstance(func_data, dict):
                if "Name" in func_data:
                    return func_data["Name"].get("id", "function")
                elif "Attribute" in func_data:
                    return func_data["Attribute"].get("attr", "function")
        return "function"


def main():
    """Test the enhanced activity generator."""
    generator = EnhancedActivityGenerator()

    # Test with a simple Python file
    test_file = "src/lightweight_activity_generator.py"

    if os.path.exists(test_file):
        print(f"Generating enhanced activity diagram for: {test_file}")
        result = generator.generate_activity_diagram(test_file)

        if result["success"]:
            print("✅ Enhanced activity diagram generated successfully!")
            print("Output files:")
            for file_path in result["output_files"]:
                print(f"  - {file_path}")
        else:
            print("❌ Failed to generate enhanced activity diagram:")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"Test file not found: {test_file}")


if __name__ == "__main__":
    main()
