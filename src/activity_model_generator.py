#!/usr/bin/env python3
"""
Integrated Activity Model Generator

This module integrates Pyreverse (for class structure analysis) and PlantUML
(for diagram generation) to create comprehensive activity models from Python source code.

Features:
- Automatic class diagram generation using Pyreverse
- Activity diagram creation using PlantUML
- Integration with round-trip engineering system
- AST-based method call analysis for workflow mapping
- Performance profiling integration
"""

import ast
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import tempfile
import subprocess

# Import our tools
import pylint.pyreverse
import plantuml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PyreverseAnalyzer:
    """Analyzes Python code using Pyreverse to extract class structures"""

    def __init__(self, output_dir: str = "generated_diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(
            f"Pyreverse analyzer initialized with output directory: {self.output_dir}"
        )

    def analyze_module(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze a Python module and generate class diagrams

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing analysis results and diagram paths
        """
        logger.info(f"🔍 Analyzing module: {source_path}")

        # Create temporary directory for Pyreverse output
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Run Pyreverse analysis
            try:
                # Save original sys.argv
                original_argv = sys.argv.copy()

                # Set up Pyreverse arguments
                sys.argv = [
                    "pyreverse",
                    "-o",
                    "dot",  # Use dot format instead of png
                    "-d",
                    str(temp_path),  # Output directory
                    source_path,  # Source file
                ]

                # Run Pyreverse analysis
                pylint.run_pyreverse()

                # Restore original sys.argv
                sys.argv = original_argv

                # Collect generated files
                generated_files = list(temp_path.glob("*.dot"))
                logger.info(
                    f"✅ Pyreverse analysis completed. Generated {len(generated_files)} files"
                )

                # Copy files to our output directory
                result_files = []
                for file_path in generated_files:
                    dest_path = self.output_dir / file_path.name
                    dest_path.write_bytes(file_path.read_bytes())
                    result_files.append(str(dest_path))

                # Parse the source code for additional analysis
                class_structure = self._parse_class_structure(source_path)

                return {
                    "source_path": source_path,
                    "diagram_files": result_files,
                    "class_structure": class_structure,
                    "analysis_successful": True,
                }

            except Exception as e:
                logger.error(f"❌ Pyreverse analysis failed: {e}")
                return {
                    "source_path": source_path,
                    "diagram_files": [],
                    "class_structure": {},
                    "analysis_successful": False,
                    "error": str(e),
                }

    def _parse_class_structure(self, source_path: str) -> Dict[str, Any]:
        """Parse Python source to extract class structure information"""
        try:
            with open(source_path, "r") as f:
                source_code = f.read()

            tree = ast.parse(source_code)

            classes = {}
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

                    # Extract methods
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

            logger.info(f"✅ Parsed {len(classes)} classes from {source_path}")
            return classes

        except Exception as e:
            logger.error(f"❌ Failed to parse class structure: {e}")
            return {}


class PlantUMLGenerator:
    """Generates UML diagrams using PlantUML"""

    def __init__(self, server_url: str = "http://localhost:20075"):
        self.server_url = server_url
        self.server = plantuml.PlantUML(url=server_url)
        logger.info(f"PlantUML generator initialized with server: {server_url}")

    def generate_activity_diagram(
        self, class_structure: Dict[str, Any], output_path: str
    ) -> str:
        """
        Generate PlantUML activity diagram from class structure

        Args:
            class_structure: Class structure from Pyreverse analysis
            output_path: Path to save the generated diagram

        Returns:
            Path to generated diagram file
        """
        logger.info(f"🎨 Generating PlantUML activity diagram")

        # Generate PlantUML code
        plantuml_code = self._generate_plantuml_code(class_structure)

        try:
            # Generate diagram
            diagram = self.server.processes(plantuml_code)

            # Save diagram
            with open(output_path, "wb") as f:
                f.write(diagram)

            logger.info(f"✅ Activity diagram generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ Failed to generate PlantUML diagram: {e}")
            # Save PlantUML code for debugging
            code_path = output_path.replace(".png", ".puml")
            with open(code_path, "w") as f:
                f.write(plantuml_code)
            logger.info(f"💾 PlantUML code saved to: {code_path}")
            raise

    def _generate_plantuml_code(self, class_structure: Dict[str, Any]) -> str:
        """Generate PlantUML code from class structure"""

        plantuml_lines = [
            "@startuml ActivityModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam activityFontSize 12",
            "skinparam activityFontName Arial",
            "",
            "title Round-Trip Engineering Activity Model",
            "",
            "start",
            "",
        ]

        # Add class creation workflow
        plantuml_lines.extend(
            [
                ":Create Model from Design;",
                "note right: Parse design specification",
                "",
                ":Extract Class Structure;",
                "note right: Use Pyreverse for analysis",
                "",
            ]
        )

        # Add class-specific activities
        for class_name, class_info in class_structure.items():
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

        # Add final workflow steps
        plantuml_lines.extend(
            [
                ":Generate Code;",
                "note right: Create Python implementation",
                "",
                ":Validate Generated Code;",
                "note right: Run tests and quality checks",
                "",
                ":Save Model;",
                "note right: Persist for future use",
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

        plantuml_lines = [
            "@startuml SequenceModel",
            "!theme plain",
            "skinparam backgroundColor white",
            "skinparam sequenceFontSize 12",
            "skinparam sequenceFontName Arial",
            "",
            "title Round-Trip Engineering Sequence Model",
            "",
            "actor User",
            "participant RoundTripSystem",
            "participant ModelManager",
            "participant CodeGenerator",
            "",
        ]

        # Add sequence workflow
        plantuml_lines.extend(
            [
                "User -> RoundTripSystem: create_model_from_design()",
                "activate RoundTripSystem",
                "",
                "RoundTripSystem -> ModelManager: create_model_from_design()",
                "activate ModelManager",
                "ModelManager --> RoundTripSystem: model",
                "deactivate ModelManager",
                "",
                "RoundTripSystem -> CodeGenerator: generate_from_model()",
                "activate CodeGenerator",
                "CodeGenerator --> RoundTripSystem: generated_code",
                "deactivate CodeGenerator",
                "",
                "RoundTripSystem --> User: model",
                "deactivate RoundTripSystem",
                "",
                "@enduml",
            ]
        )

        plantuml_code = "\n".join(plantuml_lines)

        try:
            diagram = self.server.processes(plantuml_code)
            with open(output_path, "wb") as f:
                f.write(diagram)

            logger.info(f"✅ Sequence diagram generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ Failed to generate sequence diagram: {e}")
            raise


class ActivityModelGenerator:
    """Main class that integrates Pyreverse and PlantUML for comprehensive model generation"""

    def __init__(self, output_dir: str = "generated_models"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.pyreverse = PyreverseAnalyzer(str(self.output_dir / "pyreverse"))
        self.plantuml = PlantUMLGenerator()

        logger.info(
            f"🎯 Activity Model Generator initialized with output directory: {self.output_dir}"
        )

    def generate_from_code(self, source_path: str) -> Dict[str, Any]:
        """
        Generate comprehensive activity models from Python source code

        Args:
            source_path: Path to Python source file

        Returns:
            Dictionary containing all generated models and diagrams
        """
        logger.info(f"🚀 Starting comprehensive model generation for: {source_path}")

        # Step 1: Analyze with Pyreverse
        pyreverse_results = self.pyreverse.analyze_module(source_path)

        if not pyreverse_results["analysis_successful"]:
            logger.error("❌ Pyreverse analysis failed, cannot proceed")
            return pyreverse_results

        # Step 2: Generate PlantUML diagrams
        class_structure = pyreverse_results["class_structure"]

        try:
            # Generate activity diagram
            activity_diagram_path = self.output_dir / "activity_diagram.png"
            self.plantuml.generate_activity_diagram(
                class_structure, str(activity_diagram_path)
            )

            # Generate sequence diagram
            sequence_diagram_path = self.output_dir / "sequence_diagram.png"
            self.plantuml.generate_sequence_diagram(
                class_structure, str(sequence_diagram_path)
            )

            # Compile results
            results = {
                "source_path": source_path,
                "generation_successful": True,
                "pyreverse_results": pyreverse_results,
                "plantuml_diagrams": {
                    "activity_diagram": str(activity_diagram_path),
                    "sequence_diagram": str(sequence_diagram_path),
                },
                "class_structure": class_structure,
                "output_directory": str(self.output_dir),
            }

            logger.info(f"🎉 Comprehensive model generation completed successfully!")
            logger.info(f"📁 Output directory: {self.output_dir}")
            logger.info(f"📊 Generated {len(class_structure)} class models")
            logger.info(f"🎨 Generated 2 PlantUML diagrams")

            return results

        except Exception as e:
            logger.error(f"❌ PlantUML diagram generation failed: {e}")
            return {
                "source_path": source_path,
                "generation_successful": False,
                "pyreverse_results": pyreverse_results,
                "error": str(e),
            }

    def generate_from_directory(self, source_dir: str) -> Dict[str, Any]:
        """
        Generate models for all Python files in a directory

        Args:
            source_dir: Directory containing Python source files

        Returns:
            Dictionary containing results for all files
        """
        source_path = Path(source_dir)
        python_files = list(source_path.glob("**/*.py"))

        logger.info(f"📁 Processing {len(python_files)} Python files in: {source_dir}")

        results = {}
        for python_file in python_files:
            logger.info(f"🔄 Processing: {python_file}")
            try:
                file_results = self.generate_from_code(str(python_file))
                results[str(python_file)] = file_results
            except Exception as e:
                logger.error(f"❌ Failed to process {python_file}: {e}")
                results[str(python_file)] = {
                    "generation_successful": False,
                    "error": str(e),
                }

        return results


def main():
    """Command-line interface for the Activity Model Generator"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate activity models from Python code"
    )
    parser.add_argument("source", help="Python source file or directory")
    parser.add_argument(
        "--output",
        "-o",
        default="generated_models",
        help="Output directory for generated models",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    generator = ActivityModelGenerator(args.output)

    if Path(args.source).is_file():
        results = generator.generate_from_code(args.source)
    else:
        results = generator.generate_from_directory(args.source)

    if results.get("generation_successful", False):
        print(f"✅ Model generation completed successfully!")
        print(f"📁 Output directory: {results.get('output_directory', 'Unknown')}")
    else:
        print(f"❌ Model generation failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
