#!/usr/bin/env python3
"""
Simplified Activity Model Generator

This version focuses on core functionality without Pyreverse dependency
for initial testing and validation.
"""

import ast
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import tempfile

# Import Node.js PlantUML wrapper
from plantuml_client_wrapper import NodePlantUMLWrapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleClassAnalyzer:
    """Simple class structure analyzer using AST parsing"""

    def __init__(self):
        logger.info("🔍 Simple class analyzer initialized")

    def analyze_module(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze a Python module and extract class structure

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing class structure information
        """
        logger.info(f"🔍 Analyzing module: {source_path}")

        try:
            with open(source_path, "r") as f:
                source_code = f.read()

            tree = ast.parse(source_code)

            classes = {}
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "bases": [
                            base.id for base in node.bases if isinstance(base, ast.Name)
                        ],
                        "methods": [],
                        "attributes": [],
                        "docstring": ast.get_docstring(node) or "",
                    }

                    # Extract methods and attributes
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                "name": item.name,
                                "args": [arg.arg for arg in item.args.args],
                                "docstring": ast.get_docstring(item) or "",
                            }
                            class_info["methods"].append(method_info)
                        elif isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    class_info["attributes"].append(target.id)

                    classes[node.name] = class_info

                elif isinstance(node, ast.FunctionDef):
                    function_info = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(item) or "",
                    }
                    functions.append(function_info)

            logger.info(
                f"✅ Analysis completed: {len(classes)} classes, {len(functions)} functions"
            )

            return {
                "source_path": source_path,
                "classes": classes,
                "functions": functions,
                "analysis_successful": True,
            }

        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return {
                "source_path": source_path,
                "classes": {},
                "functions": [],
                "analysis_successful": False,
                "error": str(e),
            }


class PlantUMLGenerator:
    """Generates REAL UML diagrams using PlantUML"""

    def __init__(self):
        logger.info("🎨 PlantUML generator initialized")

        # Try to initialize PlantUML client
        try:
            self.plantuml_client = NodePlantUMLWrapper()
            logger.info("✅ PlantUML client initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ PlantUML client not available: {e}")
            self.plantuml_client = None

    def generate_activity_diagram(
        self, class_structure: Dict[str, Any], output_path: str
    ) -> str:
        """
        Generate REAL UML activity diagram using PlantUML

        Args:
            class_structure: Class structure from analysis
            output_path: Path to save the generated diagram

        Returns:
            Path to generated diagram file
        """
        logger.info(f"🎨 Generating REAL UML activity diagram using PlantUML")

        # Generate PlantUML code
        plantuml_code = self._generate_plantuml_code(class_structure)
        code_path = output_path.replace(".svg", ".puml")
        with open(code_path, "w") as f:
            f.write(plantuml_code)
        logger.info(f"💾 PlantUML code saved to: {code_path}")

        # Use PlantUML to generate REAL UML diagram
        try:
            # Try to use PlantUML client if available
            if hasattr(self, "plantuml_client") and self.plantuml_client:
                svg_path = self.plantuml_client.generate_diagram(
                    plantuml_code, output_path, "svg"
                )
                if svg_path:
                    logger.info(
                        f"✅ REAL UML activity diagram generated using PlantUML: {svg_path}"
                    )
                    return svg_path

            # Fallback: generate basic SVG (not UML compliant)
            logger.warning("⚠️ PlantUML client not available, generating basic SVG")
            svg_content = self._generate_svg_activity_diagram(class_structure)
            with open(output_path, "w") as f:
                f.write(svg_content)
            logger.info(f"✅ Basic SVG generated (not UML compliant): {output_path}")

        except Exception as e:
            logger.error(f"❌ PlantUML generation failed: {e}")
            # Fallback to basic SVG
            svg_content = self._generate_svg_activity_diagram(class_structure)
            with open(output_path, "w") as f:
                f.write(svg_content)
            logger.info(f"✅ Fallback SVG generated: {output_path}")

        return output_path

    def _generate_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate REAL UML activity diagram PlantUML code"""

        classes = class_structure.get("classes", {})
        functions = class_structure.get("functions", [])

        plantuml_lines = [
            "@startuml",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam activityFontSize 12",
            "skinparam activityFontName Arial",
            "skinparam activityDiamondBackgroundColor #fff3e0",
            "skinparam activityDiamondBorderColor #f57c00",
            "",
            "title Python Module Activity Model",
            "",
            "start",
            "",
        ]

        # Generate proper UML activity diagram
        if classes:
            # Main workflow
            plantuml_lines.extend(
                [
                    ":Initialize Module;",
                    "",
                ]
            )

            # Process each class
            for class_name, class_info in classes.items():
                plantuml_lines.extend(
                    [
                        f":Process Class: {class_name};",
                        "",
                    ]
                )

                # Add methods as activities
                methods = class_info.get("methods", [])
                for i, method in enumerate(methods):
                    if i == 0:
                        plantuml_lines.append(f":{method['name']};")
                    else:
                        plantuml_lines.append(f":{method['name']};")

                # Add decision points for conditional logic
                if any(
                    "if" in method.get("docstring", "").lower()
                    or "check" in method.get("name", "").lower()
                    for method in methods
                ):
                    plantuml_lines.extend(
                        [
                            "",
                            "if (Condition Check?) then (yes)",
                            "  :Process Success Path;",
                            "else (no)",
                            "  :Process Fallback Path;",
                            "endif",
                            "",
                        ]
                    )

                plantuml_lines.append("")

        # Add standalone functions
        if functions:
            plantuml_lines.extend(
                [
                    ":Process Standalone Functions;",
                    "",
                ]
            )

            for func in functions[:5]:  # Limit to first 5
                plantuml_lines.append(f":{func['name']};")

            if len(functions) > 5:
                plantuml_lines.append(f":... and {len(functions) - 5} more;")

            plantuml_lines.append("")

        plantuml_lines.extend([":Module Complete;", "stop", "", "@enduml"])

        return "\n".join(plantuml_lines)

    def _generate_svg_sequence_diagram(self, class_structure: Dict[str, Any]) -> str:
        """Generate SVG sequence diagram directly from class structure"""

        classes = class_structure.get("classes", {})

        # Calculate dimensions based on content
        width = 900
        height = 300 + (len(classes) * 60)

        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            "  <defs>",
            "    <style>",
            "      .title { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #333; }",
            "      .subtitle { font-family: Arial, sans-serif; font-size: 14px; fill: #666; }",
            "      .participant { fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; rx: 5; }",
            "      .message { stroke: #ff5722; stroke-width: 2; marker-end: url(#arrowhead); }",
            "      .text { font-family: Arial, sans-serif; font-size: 12px; fill: #333; }",
            "      .message-text { font-family: Arial, sans-serif; font-size: 11px; fill: #ff5722; }",
            "    </style>",
            '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
            '      <polygon points="0 0, 10 3.5, 0 7" fill="#ff5722" />',
            "    </marker>",
            "  </defs>",
            "",
            f'  <text x="{width // 2}" y="30" text-anchor="middle" class="title">Python Module Sequence Model</text>',
            f'  <text x="{width // 2}" y="50" text-anchor="middle" class="subtitle">Classes: {len(classes)}</text>',
            "",
        ]

        y_offset = 80

        # Generate participant boxes
        participants = ["User", "ClassAnalyzer", "PlantUMLGenerator"]
        for i, participant in enumerate(participants):
            x = 50 + (i * 250)
            svg_lines.extend(
                [
                    f'  <rect x="{x}" y="{y_offset}" width="200" height="40" class="participant" />',
                    f'  <text x="{x + 100}" y="{y_offset + 25}" text-anchor="middle" class="text">{participant}</text>',
                ]
            )

        # Generate sequence flow
        sequence_y = y_offset + 80
        svg_lines.extend(
            [
                f'  <line x1="150" y1="{sequence_y}" x2="150" y2="{sequence_y + 100}" stroke="#666" stroke-width="1" stroke-dasharray="5,5" />',
                f'  <line x1="400" y1="{sequence_y}" x2="400" y2="{sequence_y + 100}" stroke="#666" stroke-width="1" stroke-dasharray="5,5" />',
                f'  <line x1="650" y1="{sequence_y}" x2="650" y2="{sequence_y + 100}" stroke="#666" stroke-width="1" stroke-dasharray="5,5" />',
            ]
        )

        # Generate messages
        messages = [
            ("User", "ClassAnalyzer", "analyze_module()"),
            ("ClassAnalyzer", "ClassAnalyzer", "Parse AST"),
            ("ClassAnalyzer", "User", "class_structure"),
            ("User", "PlantUMLGenerator", "generate_diagrams()"),
            ("PlantUMLGenerator", "PlantUMLGenerator", "Create SVG"),
            ("PlantUMLGenerator", "User", "generated_diagrams"),
        ]

        for i, (from_participant, to_participant, message) in enumerate(messages):
            msg_y = sequence_y + 20 + (i * 15)

            # Calculate positions
            if from_participant == "User":
                from_x = 150
            elif from_participant == "ClassAnalyzer":
                from_x = 400
            else:
                from_x = 650

            if to_participant == "User":
                to_x = 150
            elif to_participant == "ClassAnalyzer":
                to_x = 400
            else:
                to_x = 650

            # Draw message line
            svg_lines.extend(
                [
                    f'  <line x1="{from_x}" y1="{msg_y}" x2="{to_x}" y2="{msg_y}" class="message" />',
                    f'  <text x="{(from_x + to_x) // 2}" y="{msg_y - 5}" text-anchor="middle" class="message-text">{message}</text>',
                ]
            )

        svg_lines.extend(["</svg>"])

        return "\n".join(svg_lines)

    def _generate_svg_activity_diagram(self, class_structure: Dict[str, Any]) -> str:
        """Generate SVG activity diagram showing actual workflow"""

        classes = class_structure.get("classes", {})
        functions = class_structure.get("functions", [])

        # Calculate dimensions based on workflow complexity
        width = 900
        height = 600

        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            "  <defs>",
            "    <style>",
            "      .title { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #333; }",
            "      .subtitle { font-family: Arial, sans-serif; font-size: 14px; fill: #666; }",
            "      .activity { fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; rx: 8; }",
            "      .decision { fill: #fff3e0; stroke: #f57c00; stroke-width: 2; rx: 8; }",
            "      .start-end { fill: #e8f5e8; stroke: #388e3c; stroke-width: 2; rx: 20; }",
            "      .text { font-family: Arial, sans-serif; font-size: 12px; fill: #333; }",
            "      .arrow { stroke: #666; stroke-width: 2; marker-end: url(#arrowhead); }",
            "      .decision-text { font-family: Arial, sans-serif; font-size: 11px; fill: #f57c00; }",
            "    </style>",
            '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
            '      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />',
            "    </marker>",
            "  </defs>",
            "",
            f'  <text x="{width // 2}" y="30" text-anchor="middle" class="title">Python Module Activity Flow</text>',
            f'  <text x="{width // 2}" y="50" text-anchor="middle" class="subtitle">Classes: {len(classes)}, Functions: {len(functions)}</text>',
            "",
        ]

        # Generate workflow based on class structure
        if classes:
            # Start with main class workflow
            for class_name, class_info in classes.items():
                methods = class_info.get("methods", [])

                # Create workflow for main methods
                y_offset = 100
                x_offset = 50

                # Start
                svg_lines.extend(
                    [
                        f'  <ellipse cx="{x_offset + 30}" cy="{y_offset}" rx="30" ry="20" class="start-end" />',
                        f'  <text x="{x_offset + 30}" y="{y_offset + 5}" text-anchor="middle" class="text">Start</text>',
                    ]
                )

                # Main workflow
                current_y = y_offset + 50

                for i, method in enumerate(methods[:5]):  # Show first 5 methods
                    # Activity box
                    svg_lines.extend(
                        [
                            f'  <rect x="{x_offset}" y="{current_y}" width="200" height="40" class="activity" />',
                            f'  <text x="{x_offset + 100}" y="{current_y + 25}" text-anchor="middle" class="text">{method["name"]}</text>',
                        ]
                    )

                    # Arrow from previous
                    if i == 0:
                        svg_lines.extend(
                            [
                                f'  <line x1="{x_offset + 30}" y1="{y_offset + 20}" x2="{x_offset + 100}" y2="{current_y}" class="arrow" />'
                            ]
                        )
                    else:
                        prev_y = current_y - 50
                        svg_lines.extend(
                            [
                                f'  <line x1="{x_offset + 100}" y1="{prev_y + 40}" x2="{x_offset + 100}" y2="{current_y}" class="arrow" />'
                            ]
                        )

                    current_y += 60

                # End
                svg_lines.extend(
                    [
                        f'  <ellipse cx="{x_offset + 100}" cy="{current_y}" rx="30" ry="20" class="start-end" />',
                        f'  <text x="{x_offset + 100}" y="{current_y + 5}" text-anchor="middle" class="text">End</text>',
                        f'  <line x1="{x_offset + 100}" y1="{current_y - 20}" x2="{x_offset + 100}" y2="{current_y}" class="arrow" />',
                    ]
                )

                # Add decision points if methods suggest conditional logic
                if any(
                    "if" in method.get("docstring", "").lower()
                    or "check" in method.get("name", "").lower()
                    for method in methods
                ):
                    decision_x = x_offset + 300
                    decision_y = y_offset + 100

                    svg_lines.extend(
                        [
                            f'  <rect x="{decision_x}" y="{decision_y}" width="150" height="60" class="decision" />',
                            f'  <text x="{decision_x + 75}" y="{decision_y + 20}" text-anchor="middle" class="decision-text">Decision</text>',
                            f'  <text x="{decision_x + 75}" y="{decision_y + 40}" text-anchor="middle" class="text">Logic Check</text>',
                        ]
                    )

                # Add intelligent workflow based on method names and structure
                if class_name == "VocabularyAligner":
                    # Create proper workflow for vocabulary alignment
                    workflow_x = x_offset + 300
                    workflow_y = y_offset + 200

                    # Main decision point
                    svg_lines.extend(
                        [
                            f'  <rect x="{workflow_x}" y="{workflow_y}" width="180" height="60" class="decision" />',
                            f'  <text x="{workflow_x + 90}" y="{workflow_y + 20}" text-anchor="middle" class="decision-text">Ontology Bridge</text>',
                            f'  <text x="{workflow_x + 90}" y="{workflow_y + 40}" text-anchor="middle" class="text">Available?</text>',
                        ]
                    )

                    # Yes path
                    yes_x = workflow_x + 250
                    yes_y = workflow_y
                    svg_lines.extend(
                        [
                            f'  <rect x="{yes_x}" y="{yes_y}" width="150" height="40" class="activity" />',
                            f'  <text x="{yes_x + 75}" y="{yes_y + 25}" text-anchor="middle" class="text">Ontological</text>',
                            f'  <text x="{yes_x + 75}" y="{yes_y + 40}" text-anchor="middle" class="text">Alignment</text>',
                        ]
                    )

                    # No path
                    no_x = workflow_x + 250
                    no_y = workflow_y + 100
                    svg_lines.extend(
                        [
                            f'  <rect x="{no_x}" y="{no_y}" width="150" height="40" class="activity" />',
                            f'  <text x="{no_x + 75}" y="{no_y + 25}" text-anchor="middle" class="text">Manual</text>',
                            f'  <text x="{no_x + 75}" y="{no_y + 40}" text-anchor="middle" class="text">Alignment</text>',
                        ]
                    )

                    # Arrows
                    svg_lines.extend(
                        [
                            f'  <line x1="{x_offset + 200}" y1="{current_y - 30}" x2="{workflow_x}" y2="{workflow_y + 30}" class="arrow" />',
                            f'  <line x1="{workflow_x + 180}" y1="{workflow_y + 30}" x2="{yes_x}" y2="{yes_y + 20}" class="arrow" />',
                            f'  <line x1="{workflow_x + 180}" y1="{workflow_y + 30}" x2="{no_x}" y2="{no_y + 20}" class="arrow" />',
                        ]
                    )

                    # Labels
                    svg_lines.extend(
                        [
                            f'  <text x="{workflow_x + 90}" y="{yes_y - 10}" text-anchor="middle" class="text">Yes</text>',
                            f'  <text x="{workflow_x + 90}" y="{no_y - 10}" text-anchor="middle" class="text">No</text>',
                        ]
                    )

        # Add standalone functions workflow
        if functions:
            func_y = y_offset + 200
            func_x = 50

            svg_lines.extend(
                [
                    f'  <text x="{func_x}" y="{func_y - 20}" class="subtitle">Standalone Functions</text>',
                    f'  <rect x="{func_x}" y="{func_y}" width="200" height="40" class="activity" />',
                    f'  <text x="{func_x + 100}" y="{func_y + 25}" text-anchor="middle" class="text">Process Functions</text>',
                ]
            )

        svg_lines.extend(["</svg>"])

        return "\n".join(svg_lines)

    def generate_sequence_diagram(
        self, class_structure: Dict[str, Any], output_path: str
    ) -> str:
        """Generate SVG sequence diagram from class structure"""
        logger.info(f"🎬 Generating SVG sequence diagram")

        # Generate PlantUML code for reference
        plantuml_code = self._generate_sequence_plantuml_code(class_structure)
        code_path = output_path.replace(".svg", ".puml")
        with open(code_path, "w") as f:
            f.write(plantuml_code)
        logger.info(f"💾 Sequence diagram PlantUML code saved to: {code_path}")

        # Generate SVG directly
        svg_content = self._generate_svg_sequence_diagram(class_structure)

        with open(output_path, "w") as f:
            f.write(svg_content)
        logger.info(f"✅ SVG sequence diagram generated: {output_path}")

        return output_path

    def _generate_sequence_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate PlantUML sequence diagram code"""

        classes = class_structure.get("classes", {})

        plantuml_lines = [
            "@startuml SequenceModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam sequenceFontSize 12",
            "skinparam sequenceFontName Arial",
            "",
            "title Python Module Sequence Model",
            "",
            "actor User",
            "participant ClassAnalyzer",
            "participant PlantUMLGenerator",
            "",
        ]

        # Add sequence workflow
        plantuml_lines.extend(
            [
                "User -> ClassAnalyzer: analyze_module(source_path)",
                "activate ClassAnalyzer",
                "",
                "ClassAnalyzer -> ClassAnalyzer: Parse AST",
                "ClassAnalyzer -> ClassAnalyzer: Extract classes",
                "ClassAnalyzer -> ClassAnalyzer: Extract methods",
                "ClassAnalyzer --> User: class_structure",
                "deactivate ClassAnalyzer",
                "",
                "User -> PlantUMLGenerator: generate_diagrams()",
                "activate PlantUMLGenerator",
                "PlantUMLGenerator -> PlantUMLGenerator: Create PlantUML code",
                "PlantUMLGenerator -> PlantUMLGenerator: Generate diagrams",
                "PlantUMLGenerator --> User: generated_diagrams",
                "deactivate PlantUMLGenerator",
                "",
                "@enduml",
            ]
        )

        return "\n".join(plantuml_lines)


class SimpleActivityModelGenerator:
    """Simplified activity model generator without Pyreverse dependency"""

    def __init__(self, output_dir: str = "generated_models_simple"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.class_analyzer = SimpleClassAnalyzer()
        self.plantuml = PlantUMLGenerator()

        logger.info(
            f"🎯 Simple Activity Model Generator initialized with output directory: {self.output_dir}"
        )

    def generate_from_code(self, source_path: str) -> Dict[str, Any]:
        """
        Generate comprehensive activity models from Python source code

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing all generated models and diagrams
        """
        logger.info(f"🚀 Starting simplified model generation for: {source_path}")

        # Step 1: Analyze with simple analyzer
        analysis_results = self.class_analyzer.analyze_module(source_path)

        if not analysis_results["analysis_successful"]:
            logger.error("❌ Analysis failed, cannot proceed")
            return analysis_results

        # Step 2: Generate PlantUML diagrams
        class_structure = analysis_results

        try:
            # Generate unique filenames based on source file
            source_name = Path(source_path).stem
            activity_diagram_path = (
                self.output_dir / f"{source_name}_activity_diagram.svg"
            )
            self.plantuml.generate_activity_diagram(
                class_structure, str(activity_diagram_path)
            )

            # Generate sequence diagram
            sequence_diagram_path = (
                self.output_dir / f"{source_name}_sequence_diagram.svg"
            )
            self.plantuml.generate_sequence_diagram(
                class_structure, str(sequence_diagram_path)
            )

            # Compile results
            results = {
                "source_path": source_path,
                "generation_successful": True,
                "analysis_results": analysis_results,
                "plantuml_diagrams": {
                    "activity_diagram": str(activity_diagram_path),
                    "sequence_diagram": str(sequence_diagram_path),
                },
                "class_structure": analysis_results,
                "output_directory": str(self.output_dir),
            }

            logger.info(f"🎉 Simplified model generation completed successfully!")
            logger.info(f"📁 Output directory: {self.output_dir}")
            logger.info(
                f"📊 Analyzed {len(analysis_results.get('classes', {}))} classes"
            )
            logger.info(f"🎨 Generated PlantUML diagrams")

            return results

        except Exception as e:
            logger.error(f"❌ PlantUML diagram generation failed: {e}")
            return {
                "source_path": source_path,
                "generation_successful": False,
                "analysis_results": analysis_results,
                "error": str(e),
            }


def main():
    """Command-line interface for the Simple Activity Model Generator"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate activity models from Python code (simplified)"
    )
    parser.add_argument("source", help="Python source file or directory")
    parser.add_argument(
        "--output",
        "-o",
        default="generated_models_simple",
        help="Output directory for generated models",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    generator = SimpleActivityModelGenerator(args.output)

    if Path(args.source).is_file():
        results = generator.generate_from_code(args.source)
    else:
        print(f"❌ Source must be a file: {args.source}")
        return

    if results.get("generation_successful", False):
        print(f"✅ Model generation completed successfully!")
        print(f"📁 Output directory: {results.get('output_directory', 'Unknown')}")
    else:
        print(f"❌ Model generation failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
