#!/usr/bin/env python3
"""
Enhanced Module Modeling System - Phase 3 of Mass Reverse Engineering

Purpose: Create comprehensive models for each detected module by combining individual file models
Graph API Level: 3
Projection System: enhanced_module_modeling
"""

import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enhanced_reverse_engineer import EnhancedReverseEngineer
from scripts.module_detection_system import ModuleDetector


@dataclass
class EnhancedModuleModel:
    """Comprehensive model for a logical module"""

    module_name: str
    module_type: str
    confidence_score: float
    files: list[str]
    file_count: int

    # Aggregated metrics
    total_lines: int
    total_classes: int
    total_functions: int
    total_imports: int

    # Module-level information
    module_docstring: str
    module_purpose: str
    graph_api_level: str
    projection_system: str

    # Aggregated content
    all_classes: list[dict[str, Any]]
    all_functions: list[dict[str, Any]]
    all_imports: list[str]
    dependencies: set[str]

    # Cross-file relationships
    class_dependencies: dict[str, list[str]]
    function_dependencies: dict[str, list[str]]

    # Module structure
    module_structure: dict[str, Any]

    # Metadata
    creation_timestamp: str
    version: str = "1.0.0"


class EnhancedModuleModeler:
    """Create comprehensive models for detected modules"""

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.module_detector = ModuleDetector(workspace_path)
        self.reverse_engineer = EnhancedReverseEngineer()
        self.module_models: dict[str, EnhancedModuleModel] = {}

    def load_module_detection_results(
        self, summary_path: str = "module_detection_summary.json"
    ) -> dict[str, Any]:
        """Load previously generated module detection results"""
        print("📂 Loading module detection results...")

        try:
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)

            print(f"✅ Loaded {summary['total_modules']} modules from {summary_path}")
            return summary
        except FileNotFoundError:
            print(f"⚠️ Module detection summary not found: {summary_path}")
            print("🔍 Running module detection first...")
            return self._run_module_detection()

    def _run_module_detection(self) -> dict[str, Any]:
        """Run module detection if summary doesn't exist"""
        print("🧩 Running module detection...")

        # Discover Python files
        self.module_detector.discover_python_files()

        # Detect modules
        self.module_detector.detect_modules()

        # Generate and save summary
        summary_path = self.module_detector.save_module_summary()

        # Load the generated summary
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)

        return summary

    def create_enhanced_module_models(
        self, summary: dict[str, Any]
    ) -> dict[str, EnhancedModuleModel]:
        """Create enhanced models for all detected modules"""
        print("🚀 Creating enhanced module models...")

        modules_data = summary.get("modules", {})
        total_modules = len(modules_data)

        for i, (module_name, module_data) in enumerate(modules_data.items(), 1):
            print(f"📦 Processing module {i}/{total_modules}: {module_name}")

            try:
                module_model = self._create_single_module_model(
                    module_name, module_data
                )
                self.module_models[module_name] = module_model
                print(f"   ✅ Created model for {module_name}")

            except Exception as e:
                print(f"   ❌ Failed to create model for {module_name}: {e}")
                continue

        print(
            f"🎯 Enhanced module modeling complete! Created {len(self.module_models)} models"
        )
        return self.module_models

    def _create_single_module_model(
        self, module_name: str, module_data: dict[str, Any]
    ) -> EnhancedModuleModel:
        """Create enhanced model for a single module"""

        # Get file paths for this module
        file_paths = [Path(f) for f in module_data["files"]]

        # Reverse engineer each file in the module
        file_models = []
        all_classes = []
        all_functions = []
        all_imports = set()
        dependencies = set()

        for file_path in file_paths:
            try:
                # Reverse engineer the file
                file_model = self.reverse_engineer.reverse_engineer(file_path)

                if file_model["status"] == "success":
                    file_models.append(file_model)

                    # Aggregate classes
                    for class_info in file_model.get("classes", []):
                        class_info["source_file"] = str(file_path)
                        all_classes.append(class_info)

                    # Aggregate functions
                    for func_info in file_model.get("functions", []):
                        func_info["source_file"] = str(file_path)
                        all_functions.append(func_info)

                    # Aggregate imports
                    all_imports.update(file_model.get("imports", []))

                    # Aggregate dependencies
                    dependencies.update(file_model.get("dependencies", []))

            except Exception as e:
                print(f"   ⚠️ Error processing {file_path}: {e}")
                continue

        # Analyze cross-file relationships
        class_dependencies = self._analyze_class_dependencies(all_classes, file_models)
        function_dependencies = self._analyze_function_dependencies(
            all_functions, file_models
        )

        # Create module-level docstring and metadata
        module_docstring = self._create_module_docstring(
            module_name, module_data, file_models
        )
        module_purpose = self._extract_module_purpose(module_data, file_models)
        graph_api_level = self._determine_graph_api_level(module_data, file_models)
        projection_system = self._determine_projection_system(module_name, module_data)

        # Create module structure
        module_structure = self._create_module_structure(module_data, file_models)

        # Create the enhanced module model
        module_model = EnhancedModuleModel(
            module_name=module_name,
            module_type=module_data["module_type"],
            confidence_score=module_data["confidence_score"],
            files=module_data["files"],
            file_count=module_data["file_count"],
            total_lines=module_data["total_lines"],
            total_classes=module_data["total_classes"],
            total_functions=module_data["total_functions"],
            total_imports=module_data["total_imports"],
            module_docstring=module_docstring,
            module_purpose=module_purpose,
            graph_api_level=graph_api_level,
            projection_system=projection_system,
            all_classes=all_classes,
            all_functions=all_functions,
            all_imports=list(all_imports),
            dependencies=dependencies,
            class_dependencies=class_dependencies,
            function_dependencies=function_dependencies,
            module_structure=module_structure,
            creation_timestamp=self._get_timestamp(),
        )

        return module_model

    def _analyze_class_dependencies(
        self, classes: list[dict[str, Any]], file_models: list[dict[str, Any]]
    ) -> dict[str, list[str]]:
        """Analyze dependencies between classes in the module"""
        class_dependencies = defaultdict(list)

        for class_info in classes:
            class_name = class_info.get("name", "")
            if not class_name:
                continue

            # Find classes that this class depends on
            dependencies = []

            # Check for inheritance
            bases = class_info.get("bases", [])
            for base in bases:
                if base and base != "object":
                    dependencies.append(base)

            # Check for type hints in methods
            methods = class_info.get("methods", [])
            for method in methods:
                method_deps = self._extract_type_dependencies(method)
                dependencies.extend(method_deps)

            class_dependencies[class_name] = list(set(dependencies))

        return dict(class_dependencies)

    def _analyze_function_dependencies(
        self, functions: list[dict[str, Any]], file_models: list[dict[str, Any]]
    ) -> dict[str, list[str]]:
        """Analyze dependencies between functions in the module"""
        function_dependencies = defaultdict(list)

        for func_info in functions:
            func_name = func_info.get("name", "")
            if not func_name:
                continue

            # Extract type dependencies from function signature and body
            dependencies = self._extract_type_dependencies(func_info)
            function_dependencies[func_name] = dependencies

        return dict(function_dependencies)

    def _extract_type_dependencies(self, item: dict[str, Any]) -> list[str]:
        """Extract type dependencies from a function or method"""
        dependencies = []

        # Check return type
        return_type = item.get("return_type", "")
        if return_type and return_type not in ["None", "Any"]:
            dependencies.append(return_type)

        # Check parameters
        parameters = item.get("parameters", [])
        for param in parameters:
            param_type = param.get("type", "")
            if param_type and param_type not in ["Any"]:
                dependencies.append(param_type)

        return list(set(dependencies))

    def _create_module_docstring(
        self,
        module_name: str,
        module_data: dict[str, Any],
        file_models: list[dict[str, Any]],
    ) -> str:
        """Create a comprehensive module-level docstring"""

        docstring_parts = [
            '"""',
            f"{module_name}",
            "",
            f"Purpose: {self._extract_module_purpose(module_data, file_models)}",
            f"Graph API Level: {self._determine_graph_api_level(module_data, file_models)}",
            f"Projection System: {self._determine_projection_system(module_name, module_data)}",
            "",
            f'Module Type: {module_data["module_type"]}',
            f'Files: {module_data["file_count"]}',
            f'Total Lines: {module_data["total_lines"]}',
            f'Classes: {module_data["total_classes"]}',
            f'Functions: {module_data["total_functions"]}',
            f'Imports: {module_data["total_imports"]}',
            "",
            "This module was automatically detected and modeled by the Enhanced Module Modeling System.",
            '"""',
        ]

        return "\n".join(docstring_parts)

    def _extract_module_purpose(
        self, module_data: dict[str, Any], file_models: list[dict[str, Any]]
    ) -> str:
        """Extract the purpose of the module from its content"""

        # Try to find purpose from file models
        for file_model in file_models:
            module_docstring = file_model.get("module_docstring", "")
            if module_docstring:
                # Look for purpose indicators
                purpose_patterns = [
                    r"Purpose:\s*(.+)",
                    r"purpose[:\s]+(.+)",
                    r"for\s+(.+)",
                    r"to\s+(.+)",
                ]

                for pattern in purpose_patterns:
                    match = re.search(pattern, module_docstring, re.IGNORECASE)
                    if match:
                        return match.group(1).strip()

        # Fallback based on module name and type
        module_name = module_data.get("name", "")
        module_type = module_data.get("module_type", "")

        if "test" in module_name.lower():
            return "Testing and validation"
        elif "script" in module_name.lower():
            return "Utility scripts and tools"
        elif "core" in module_name.lower():
            return "Core functionality and business logic"
        elif "model" in module_name.lower():
            return "Data models and schemas"
        elif "service" in module_name.lower():
            return "Service layer and API endpoints"
        else:
            return "General functionality"

    def _determine_graph_api_level(
        self, module_data: dict[str, Any], file_models: list[dict[str, Any]]
    ) -> str:
        """Determine the Graph API level for this module"""

        # Check file models for explicit Graph API level
        for file_model in file_models:
            module_docstring = file_model.get("module_docstring", "")
            if module_docstring:
                match = re.search(r"Graph API Level:\s*(\d+)", module_docstring)
                if match:
                    return match.group(1)

        # Determine based on module characteristics
        total_lines = module_data.get("total_lines", 0)
        total_classes = module_data.get("total_classes", 0)
        total_functions = module_data.get("total_functions", 0)

        if total_lines > 1000 or total_classes > 10:
            return "3"  # Complex module
        elif total_lines > 500 or total_classes > 5:
            return "2"  # Medium complexity
        else:
            return "1"  # Simple module

    def _determine_projection_system(
        self, module_name: str, module_data: dict[str, Any]
    ) -> str:
        """Determine the projection system for this module"""

        # Check for known projection systems
        if "test" in module_name.lower():
            return "test_system"
        elif "model" in module_name.lower():
            return "model_system"
        elif "core" in module_name.lower():
            return "core_system"
        elif "service" in module_name.lower():
            return "service_system"
        elif "script" in module_name.lower():
            return "script_system"
        else:
            return "general_system"

    def _create_module_structure(
        self, module_data: dict[str, Any], file_models: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Create a comprehensive module structure"""

        structure = {
            "module_info": {
                "name": module_data.get("name", ""),
                "type": module_data.get("module_type", ""),
                "confidence": module_data.get("confidence_score", 0.0),
                "file_count": module_data.get("file_count", 0),
            },
            "metrics": {
                "total_lines": module_data.get("total_lines", 0),
                "total_classes": module_data.get("total_classes", 0),
                "total_functions": module_data.get("total_functions", 0),
                "total_imports": module_data.get("total_imports", 0),
            },
            "files": [],
            "aggregated_content": {"classes": [], "functions": [], "imports": []},
        }

        # Add file information
        for file_path in module_data.get("files", []):
            file_info = {
                "path": file_path,
                "name": Path(file_path).name,
                "stem": Path(file_path).stem,
            }
            structure["files"].append(file_info)

        # Add aggregated content from file models
        for file_model in file_models:
            if file_model["status"] == "success":
                # Add classes
                for class_info in file_model.get("classes", []):
                    class_info["source_file"] = file_model.get("file_path", "")
                    structure["aggregated_content"]["classes"].append(class_info)

                # Add functions
                for func_info in file_model.get("functions", []):
                    func_info["source_file"] = file_model.get("file_path", "")
                    structure["aggregated_content"]["functions"].append(func_info)

                # Add imports
                structure["aggregated_content"]["imports"].extend(
                    file_model.get("imports", [])
                )

        return structure

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime

        return datetime.now().isoformat()

    def save_enhanced_module_models(
        self, output_dir: str = "enhanced_module_models"
    ) -> str:
        """Save all enhanced module models to JSON files"""
        print(f"💾 Saving enhanced module models to {output_dir}...")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save individual module models
        for module_name, module_model in self.module_models.items():
            # Convert dataclass to dict and handle sets
            model_dict = asdict(module_model)

            # Convert sets to lists for JSON serialization
            def convert_sets(obj):
                if isinstance(obj, dict):
                    return {k: convert_sets(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_sets(item) for item in obj]
                elif isinstance(obj, set):
                    return list(obj)
                else:
                    return obj

            model_dict = convert_sets(model_dict)

            # Save to individual file
            safe_name = re.sub(r"[^\w\-_]", "_", module_name)
            model_file = output_path / f"{safe_name}_enhanced_model.json"

            with open(model_file, "w", encoding="utf-8") as f:
                json.dump(model_dict, f, indent=2, ensure_ascii=False)

        # Save summary index
        summary = {
            "workspace_path": str(self.workspace_path),
            "total_modules": len(self.module_models),
            "modules": list(self.module_models.keys()),
            "creation_timestamp": self._get_timestamp(),
            "version": "1.0.0",
        }

        summary_file = output_path / "enhanced_module_models_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(
            f"✅ Saved {len(self.module_models)} enhanced module models to {output_dir}"
        )
        return str(output_path)

    def generate_enhanced_summary(self) -> dict[str, Any]:
        """Generate comprehensive summary of all enhanced module models"""
        summary = {
            "workspace_path": str(self.workspace_path),
            "total_modules": len(self.module_models),
            "modules": {},
            "statistics": {
                "total_lines": sum(m.total_lines for m in self.module_models.values()),
                "total_classes": sum(
                    m.total_classes for m in self.module_models.values()
                ),
                "total_functions": sum(
                    m.total_functions for m in self.module_models.values()
                ),
                "total_imports": sum(
                    m.total_imports for m in self.module_models.values()
                ),
            },
            "module_types": defaultdict(int),
            "projection_systems": defaultdict(int),
            "graph_api_levels": defaultdict(int),
        }

        # Add module details
        for module_name, module_model in self.module_models.items():
            summary["modules"][module_name] = {
                "name": module_model.module_name,
                "type": module_model.module_type,
                "confidence": module_model.confidence_score,
                "files": module_model.files,
                "file_count": module_model.file_count,
                "total_lines": module_model.total_lines,
                "total_classes": module_model.total_classes,
                "total_functions": module_model.total_functions,
                "total_imports": module_model.total_imports,
                "purpose": module_model.module_purpose,
                "graph_api_level": module_model.graph_api_level,
                "projection_system": module_model.projection_system,
                "dependencies": list(module_model.dependencies),
            }

            # Count module types and systems
            summary["module_types"][module_model.module_type] += 1
            summary["projection_systems"][module_model.projection_system] += 1
            summary["graph_api_levels"][module_model.graph_api_level] += 1

        return summary


def main() -> None:
    """Main entry point for enhanced module modeling"""
    print("🚀 Enhanced Module Modeling System - Phase 3")
    print("=" * 60)

    # Initialize modeler
    modeler = EnhancedModuleModeler(".")

    # Load or run module detection
    summary = modeler.load_module_detection_results()

    # Create enhanced module models
    module_models = modeler.create_enhanced_module_models(summary)

    # Save enhanced models
    output_dir = modeler.save_enhanced_module_models()

    # Generate enhanced summary
    enhanced_summary = modeler.generate_enhanced_summary()

    # Display results
    print("\n📊 Enhanced Module Modeling Results:")
    print("-" * 40)

    print(f"📦 Total Modules: {enhanced_summary['total_modules']}")
    print(f"📝 Total Lines: {enhanced_summary['statistics']['total_lines']:,}")
    print(f"🏗️ Total Classes: {enhanced_summary['statistics']['total_classes']}")
    print(f"⚙️ Total Functions: {enhanced_summary['statistics']['total_functions']}")
    print(f"📚 Total Imports: {enhanced_summary['statistics']['total_imports']}")

    print(f"\n🔍 Module Types:")
    for module_type, count in enhanced_summary["module_types"].items():
        print(f"   {module_type}: {count}")

    print(f"\n🎯 Projection Systems:")
    for system, count in enhanced_summary["projection_systems"].items():
        print(f"   {system}: {count}")

    print(f"\n📈 Graph API Levels:")
    for level, count in enhanced_summary["graph_api_levels"].items():
        print(f"   {level}: {count}")

    print(f"\n🎯 Phase 3 Complete! Enhanced models saved to: {output_dir}")
    print(f"📁 Summary: {output_dir}/enhanced_module_models_summary.json")


if __name__ == "__main__":
    main()
