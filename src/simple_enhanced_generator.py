#!/usr/bin/env python3
"""
Simple Enhanced Activity Diagram Generator

A simplified version that generates clean, logical activity diagrams
using the StarUML extension's AST parser.
"""

import subprocess
import tempfile
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add the StarUML extension to our path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "external", "staruml-python")
)


class SimpleEnhancedGenerator:
    """Generate clean activity diagrams from Python code."""

    def __init__(self):
        self.ast_parser_path = os.path.join(
            os.path.dirname(__file__), "..", "external", "staruml-python", "ast2json.py"
        )

    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
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
            return self._extract_simple_workflow(ast_data, file_path)

        except Exception as e:
            return {"success": False, "error": str(e), "file_path": file_path}

    def _extract_simple_workflow(
        self, ast_data: Dict[str, Any], file_path: str
    ) -> Dict[str, Any]:
        """Extract a simple, clean workflow from AST data."""
        try:
            functions = []

            # Find all function definitions
            self._find_functions(ast_data, functions)

            # Create a simple workflow
            workflow = {
                "success": True,
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "functions": functions,
            }

            return workflow

        except Exception as e:
            return {"success": False, "error": str(e), "file_path": file_path}

    def _find_functions(self, ast_data: Any, functions: List[Dict]):
        """Recursively find function definitions."""
        if isinstance(ast_data, dict):
            for key, value in ast_data.items():
                if key == "FunctionDef":
                    if isinstance(value, dict) and "name" in value:
                        func_name = value["name"]
                        functions.append({"name": func_name, "type": "function"})
                elif isinstance(value, (dict, list)):
                    self._find_functions(value, functions)
        elif isinstance(ast_data, list):
            for item in ast_data:
                self._find_functions(item, functions)

    def generate_plantuml_activity(self, workflow_data: Dict[str, Any]) -> str:
        """Generate simple PlantUML activity diagram."""
        if not workflow_data.get("success", False):
            return f"// Error analyzing file: {workflow_data.get('error', 'Unknown error')}"

        functions = workflow_data.get("functions", [])

        if not functions:
            return "// No functions found in file"

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

        # Generate a simple sequential workflow
        plantuml_lines.append("start")

        for i, func in enumerate(functions):
            func_name = func["name"]
            plantuml_lines.append(f":{func_name}();")

            # Add decision for main function
            if func_name == "main":
                plantuml_lines.append("if (success?) then (yes)")
                plantuml_lines.append("  :Generate activity diagram;")
                plantuml_lines.append("else (no)")
                plantuml_lines.append("  :Handle error;")
                plantuml_lines.append("endif")

        plantuml_lines.append("stop")
        plantuml_lines.append("@enduml")

        return "\n".join(plantuml_lines)

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

            # Analyze Python file
            workflow_data = self.analyze_python_file(python_file)
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
                output_dir, f"{base_name}_simple_enhanced.puml"
            )
            with open(plantuml_file, "w") as f:
                f.write(plantuml_code)
            result["output_files"].append(plantuml_file)

            # Try to generate SVG using Graphviz
            svg_file = os.path.join(output_dir, f"{base_name}_simple_enhanced.svg")
            if self._generate_svg_graphviz(plantuml_code, svg_file):
                result["output_files"].append(svg_file)
                result["success"] = True
            else:
                result["errors"].append("SVG generation failed")

            return result

        except Exception as e:
            result["errors"].append(f"Unexpected error: {str(e)}")
            return result

    def _generate_svg_graphviz(self, plantuml_code: str, output_path: str) -> bool:
        """Generate SVG using Graphviz directly."""
        try:
            # Convert PlantUML to DOT format
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
        dot_lines = [
            "digraph G {",
            "  rankdir=TB;",
            "  node [shape=box, style=filled, fillcolor=lightblue];",
            "  edge [fontsize=10];",
            "",
        ]

        # Parse PlantUML lines
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
            elif line.startswith("if ("):
                node_counter += 1
                node_id = f"decision_{node_counter}"
                # Extract condition from if statement
                condition = line[3 : line.find(")")] if ")" in line else "condition"
                nodes[node_id] = condition
                dot_lines.append(
                    f'  {node_id} [shape=diamond, fillcolor=lightyellow, label="{condition}"];'
                )

        # Add edges (simplified sequential flow)
        for i in range(1, node_counter):
            dot_lines.append(f"  node_{i} -> node_{i + 1};")

        dot_lines.append("}")
        return "\n".join(dot_lines)


def main():
    """Test the simple enhanced generator."""
    generator = SimpleEnhancedGenerator()

    # Test with a simple Python file
    test_file = "src/lightweight_activity_generator.py"

    if os.path.exists(test_file):
        print(f"Generating simple enhanced activity diagram for: {test_file}")
        result = generator.generate_activity_diagram(test_file)

        if result["success"]:
            print("✅ Simple enhanced activity diagram generated successfully!")
            print("Output files:")
            for file_path in result["output_files"]:
                print(f"  - {file_path}")
        else:
            print("❌ Failed to generate simple enhanced activity diagram:")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"Test file not found: {test_file}")


if __name__ == "__main__":
    main()
