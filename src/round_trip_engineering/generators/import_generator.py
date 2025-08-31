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

            # Collect all needed imports
            needed_imports = self._analyze_import_needs(extracted_model)

            # Generate import statements
            import_code = self._generate_import_statements(needed_imports)

            if import_code:
                import_code += "\n"  # Add spacing after imports

            logger.info(f"✅ Generated {len(needed_imports)} import categories")
            return import_code

        except Exception as e:
            logger.error(f"❌ Import generation failed: {e}")
            return ""

    def _analyze_import_needs(
        self, extracted_model: Dict[str, Any]
    ) -> Dict[str, Set[str]]:
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
                if any(
                    op_method in method_name.lower()
                    for op_method in operational_methods
                ):
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
            import_lines.append(
                f"from dataclasses import {', '.join(dataclass_imports)}"
            )

        if needed_imports["pydantic"]:
            pydantic_imports = sorted(needed_imports["pydantic"])
            import_lines.append(f"from pydantic import {', '.join(pydantic_imports)}")

        if needed_imports["enum"]:
            enum_imports = sorted(needed_imports["enum"])
            import_lines.append(f"from enum import {', '.join(enum_imports)}")

        # Add Reflective Module imports
        if needed_imports["reflective_modules"]:
            reflective_imports = sorted(needed_imports["reflective_modules"])
            import_lines.append(
                f"from src.reflective_modules import {', '.join(reflective_imports)}"
            )

        # Add standard imports
        if needed_imports["standard"]:
            for std_import in sorted(needed_imports["standard"]):
                import_lines.append(f"import {std_import}")

        return "\n".join(import_lines)
