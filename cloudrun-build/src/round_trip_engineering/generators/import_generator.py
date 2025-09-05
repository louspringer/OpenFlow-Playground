"""
Import Generator Module

This module handles smart import detection and generation based on model analysis.
"""

import logging
from typing import Dict, Any, List, Set

logger = logging.getLogger(__name__)


class ImportGenerator:
    """Generates smart imports based on model analysis."""

    def __init__(self):
        """Initialize the import generator."""
        logger.info("✅ Import generator initialized")

    def generate_imports(self, extracted_model: Dict[str, Any]) -> str:
        """
        Generate imports based on model analysis.

        Args:
            extracted_model: The extracted model

        Returns:
            Generated import statements as string
        """
        try:
            logger.info("🔍 Analyzing imports for model...")

            # First, preserve original imports from the file
            original_imports = self._extract_original_imports(extracted_model)

            # Collect all needed imports
            needed_imports = self._analyze_import_needs(extracted_model)

            # Merge original imports with needed imports
            merged_imports = self._merge_imports(original_imports, needed_imports)

            # Generate import statements
            import_code = self._generate_import_statements(merged_imports)

            if import_code:
                import_code += "\n"  # Add spacing after imports

            logger.info(f"✅ Generated {len(merged_imports)} import categories")
            return import_code

        except Exception as e:
            logger.error(f"❌ Import generation failed: {e}")
            return ""

    def _extract_original_imports(self, extracted_model: Dict[str, Any]) -> Dict[str, Set[str]]:
        """Extract original imports from the source file."""
        original_imports = {
            "typing": set(),
            "dataclasses": set(),
            "pydantic": set(),
            "enum": set(),
            "standard": set(),
            "reflective_modules": set(),
        }

        # Get original source code if available
        enhanced_ast_data = extracted_model.get("enhanced_ast_data", {})
        if enhanced_ast_data:
            # Look for original imports in the AST data
            # This is a simplified approach - in practice, we'd parse the original file
            logger.info("🔍 Extracting original imports from enhanced AST data")

            # For now, add common imports that should be preserved
            original_imports["standard"].add("argparse")
            original_imports["standard"].add("json")
            original_imports["typing"].add("Dict")
            original_imports["typing"].add("Any")

            # Add ReflectiveModule imports if class inherits from ReflectiveModule
            components = extracted_model.get("components", {})
            enhanced_ast = extracted_model.get("enhanced_ast_data", {})

            # Check components (if dict format)
            if isinstance(components, dict):
                for class_info in components.values():
                    bases = class_info.get("bases", [])
                    if any("ReflectiveModule" in base for base in bases):
                        original_imports["reflective_modules"].add("ReflectiveModule")
                        original_imports["reflective_modules"].add("ModuleStatus")
                        original_imports["reflective_modules"].add("ModuleHealth")
                        original_imports["reflective_modules"].add("ModuleCapability")
                        original_imports["typing"].add("List")
                        original_imports["typing"].add("Dict")
                        original_imports["typing"].add("Any")
                        original_imports["standard"].add("time")
                        original_imports["standard"].add("logging")
                        break
            elif isinstance(components, list):
                # Handle list format components
                for class_info in components:
                    if isinstance(class_info, dict):
                        bases = class_info.get("bases", [])
                        if any("ReflectiveModule" in base for base in bases):
                            original_imports["reflective_modules"].add("ReflectiveModule")
                            original_imports["reflective_modules"].add("ModuleStatus")
                            original_imports["reflective_modules"].add("ModuleHealth")
                            original_imports["reflective_modules"].add("ModuleCapability")
                            original_imports["typing"].add("List")
                            original_imports["typing"].add("Dict")
                            original_imports["typing"].add("Any")
                            original_imports["standard"].add("time")
                            original_imports["standard"].add("logging")
                            break

            # Check enhanced_ast_data classes (if available)
            if isinstance(enhanced_ast, dict):
                classes = enhanced_ast.get("classes", [])
                for class_info in classes:
                    bases = class_info.get("bases", [])
                    if any("ReflectiveModule" in base for base in bases):
                        original_imports["reflective_modules"].add("ReflectiveModule")
                        original_imports["reflective_modules"].add("ModuleStatus")
                        original_imports["reflective_modules"].add("ModuleHealth")
                        original_imports["reflective_modules"].add("ModuleCapability")
                        original_imports["typing"].add("List")
                        original_imports["typing"].add("Dict")
                        original_imports["typing"].add("Any")
                        original_imports["standard"].add("time")
                        original_imports["standard"].add("logging")
                        break

            # Always add ReflectiveModule imports since ClassStructureGenerator adds it as base
            # when no other bases are present
            original_imports["reflective_modules"].add("ReflectiveModule")
            original_imports["reflective_modules"].add("ModuleStatus")
            original_imports["reflective_modules"].add("ModuleHealth")
            original_imports["reflective_modules"].add("ModuleCapability")
            original_imports["typing"].add("List")
            original_imports["typing"].add("Dict")
            original_imports["typing"].add("Any")
            original_imports["standard"].add("time")
            original_imports["standard"].add("logging")

        return original_imports

    def _merge_imports(self, original_imports: Dict[str, Set[str]], needed_imports: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """Merge original imports with needed imports."""
        merged = {}
        for category in original_imports:
            merged[category] = original_imports[category].union(needed_imports.get(category, set()))
        return merged

    def _analyze_import_needs(self, extracted_model: Dict[str, Any]) -> Dict[str, Set[str]]:
        """Analyze what imports are needed based on the model."""
        needed_imports = {
            "typing": set(),
            "dataclasses": set(),
            "pydantic": set(),
            "enum": set(),
            "standard": set(),
            "reflective_modules": set(),
        }

        components = extracted_model.get("components", {})
        if not isinstance(components, dict):
            return needed_imports

        for class_info in components.values():
            # Check class decorators
            decorators = class_info.get("class_decorators", [])
            if "dataclass" in decorators:
                needed_imports["dataclasses"].add("dataclass")

            # Check base classes
            bases = class_info.get("bases", [])
            for base in bases:
                if "BaseModel" in base:
                    needed_imports["pydantic"].add("BaseModel")
                if "Enum" in base:
                    needed_imports["enum"].add("Enum")
                if "ReflectiveModule" in base:
                    needed_imports["reflective_modules"].add("ReflectiveModule")
                    needed_imports["reflective_modules"].add("ModuleStatus")
                    needed_imports["reflective_modules"].add("ModuleHealth")
                    needed_imports["reflective_modules"].add("ModuleCapability")
                    needed_imports["typing"].add("List")
                    needed_imports["typing"].add("Dict")
                    needed_imports["typing"].add("Any")

            # Check methods for typing needs
            methods = class_info.get("methods", [])
            for method in methods:
                return_type = method.get("return_type", "")
                if return_type:
                    if "Optional" in return_type:
                        needed_imports["typing"].add("Optional")
                    if "List" in return_type:
                        needed_imports["typing"].add("List")
                    if "Dict" in return_type:
                        needed_imports["typing"].add("Dict")
                    if "Any" in return_type:
                        needed_imports["typing"].add("Any")
                    if "Union" in return_type:
                        needed_imports["typing"].add("Union")
                    if "BaseModel" in return_type:
                        needed_imports["pydantic"].add("BaseModel")

            # Check for Reflective Module interface needs
            # Look for methods that suggest operational monitoring
            operational_methods = [
                "get_status",
                "get_health",
                "get_capabilities",
                "is_healthy",
                "get_module_status",
                "get_module_health",
                "get_module_capabilities",
                "get_graceful_degradation_info",
            ]
            for method in methods:
                method_name = method.get("name", "")
                if any(op_method in method_name.lower() for op_method in operational_methods):
                    needed_imports["reflective_modules"].add("ReflectiveModule")
                    needed_imports["reflective_modules"].add("ModuleStatus")
                    needed_imports["reflective_modules"].add("ModuleHealth")
                    needed_imports["reflective_modules"].add("ModuleCapability")
                    needed_imports["typing"].add("List")
                    needed_imports["typing"].add("Dict")
                    needed_imports["typing"].add("Any")
                    break

        # Always include Pydantic for modern Python development
        if not needed_imports["pydantic"]:
            needed_imports["pydantic"].add("BaseModel")
            needed_imports["pydantic"].add("Field")
            needed_imports["pydantic"].add("validator")

        return needed_imports

    def _generate_import_statements(self, needed_imports: Dict[str, Set[str]]) -> str:
        """Generate actual import statements."""
        import_lines = []

        # Standard library imports
        if needed_imports["typing"]:
            typing_imports = sorted(needed_imports["typing"])
            import_lines.append(f"from typing import {', '.join(typing_imports)}")

        if needed_imports["dataclasses"]:
            dataclass_imports = sorted(needed_imports["dataclasses"])
            import_lines.append(f"from dataclasses import {', '.join(dataclass_imports)}")

        if needed_imports["pydantic"]:
            pydantic_imports = sorted(needed_imports["pydantic"])
            import_lines.append(f"from pydantic import {', '.join(pydantic_imports)}")

        if needed_imports["enum"]:
            enum_imports = sorted(needed_imports["enum"])
            import_lines.append(f"from enum import {', '.join(enum_imports)}")

        # Add Reflective Module imports
        if needed_imports["reflective_modules"]:
            reflective_imports = sorted(needed_imports["reflective_modules"])
            import_lines.append(f"from src.reflective_modules import {', '.join(reflective_imports)}")

        # Add standard imports
        if needed_imports["standard"]:
            for std_import in sorted(needed_imports["standard"]):
                import_lines.append(f"import {std_import}")

        return "\n".join(import_lines)
