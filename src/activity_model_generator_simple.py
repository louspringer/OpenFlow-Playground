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
    """Generates UML diagrams using Node.js PlantUML wrapper"""

    def __init__(self, server_url: str = "http://localhost:20075"):
        self.server_url = server_url
        try:
            self.client = NodePlantUMLWrapper()
            logger.info(
                f"Node.js PlantUML generator initialized with server: {server_url}"
            )
        except Exception as e:
            logger.warning(f"⚠️  Node.js PlantUML client not available: {e}")
            self.client = None

    def generate_activity_diagram(
        self, class_structure: Dict[str, Any], output_path: str
    ) -> str:
        """
        Generate PlantUML activity diagram from class structure

        Args:
            class_structure: Class structure from analysis
            output_path: Path to save the generated diagram

        Returns:
            Path to generated diagram file
        """
        logger.info(f"🎨 Generating PlantUML activity diagram")

        # Generate PlantUML code
        plantuml_code = self._generate_plantuml_code(class_structure)

        # Save PlantUML code
        code_path = output_path.replace(".png", ".puml")
        with open(code_path, "w") as f:
            f.write(plantuml_code)
        logger.info(f"💾 PlantUML code saved to: {code_path}")

        # Try to generate diagram if client is available
        if self.client:
            try:
                result = self.client.generate_diagram(plantuml_code, output_path)
                if result:
                    logger.info(f"✅ Activity diagram generated: {output_path}")
                    return output_path
                else:
                    logger.warning(f"⚠️  Node.js PlantUML diagram generation failed")
                    logger.info(f"💾 PlantUML code available at: {code_path}")
                    return code_path
            except Exception as e:
                logger.warning(f"⚠️  Node.js PlantUML diagram generation failed: {e}")
                logger.info(f"💾 PlantUML code available at: {code_path}")
                return code_path
        else:
            logger.info(f"💾 PlantUML code saved (client not available): {code_path}")
            return code_path

    def _generate_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate PlantUML code from class structure"""

        classes = class_structure.get("classes", {})
        functions = class_structure.get("functions", [])

        plantuml_lines = [
            "@startuml ActivityModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam activityFontSize 12",
            "skinparam activityFontName Arial",
            "",
            "title Python Module Activity Model",
            "",
            "start",
            "",
        ]

        # Add class creation workflow
        plantuml_lines.extend(
            [
                ":Parse Python Source;",
                "note right: AST analysis and structure extraction",
                "",
                f":Extract {len(classes)} Classes;",
                "note right: Class structure analysis",
                "",
            ]
        )

        # Add class-specific activities
        for class_name, class_info in classes.items():
            plantuml_lines.extend(
                [
                    f":Process Class: {class_name};",
                    f"note right: {len(class_info.get('methods', []))} methods, {len(class_info.get('attributes', []))} attributes",
                ]
            )

            # Add method processing
            for method in class_info.get("methods", []):
                plantuml_lines.append(f"  :Generate Method: {method['name']};")

            plantuml_lines.append("")

        # Add function processing
        if functions:
            plantuml_lines.extend(
                [
                    f":Process {len(functions)} Functions;",
                    "note right: Standalone function analysis",
                ]
            )

            for func in functions:
                plantuml_lines.append(f"  :Generate Function: {func['name']};")

            plantuml_lines.append("")

        # Add final workflow steps
        plantuml_lines.extend(
            [
                ":Generate Activity Models;",
                "note right: Create UML activity diagrams",
                "",
                ":Save Results;",
                "note right: Persist models and diagrams",
                "",
                "stop",
                "@enduml",
            ]
        )

        return "\n".join(plantuml_lines)

    def generate_sequence_diagram(
        self, class_structure: Dict[str, Any], output_path: str
    ) -> str:
        """Generate PlantUML sequence diagram from class structure"""
        logger.info(f"🎬 Generating PlantUML sequence diagram")

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

        plantuml_code = "\n".join(plantuml_lines)

        # Save PlantUML code
        code_path = output_path.replace(".png", ".puml")
        with open(code_path, "w") as f:
            f.write(plantuml_code)
        logger.info(f"💾 Sequence diagram PlantUML code saved to: {code_path}")

        # Try to generate diagram if client is available
        if self.client:
            try:
                result = self.client.generate_diagram(plantuml_code, output_path)
                if result:
                    logger.info(f"✅ Sequence diagram generated: {output_path}")
                    return output_path
                else:
                    logger.warning(
                        f"⚠️  Node.js PlantUML sequence diagram generation failed"
                    )
                    return code_path
            except Exception as e:
                logger.warning(
                    f"⚠️  Node.js PlantUML sequence diagram generation failed: {e}"
                )
                return code_path
        else:
            return code_path


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
            # Generate activity diagram
            activity_diagram_path = self.output_dir / "activity_diagram.svg"
            self.plantuml.generate_activity_diagram(
                class_structure, str(activity_diagram_path)
            )

            # Generate sequence diagram
            sequence_diagram_path = self.output_dir / "sequence_diagram.svg"
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
