"""
Code Generator Module

This module handles the actual code generation from models.
It coordinates class, method, and function generation.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid

from .class_generator import ClassGenerator
from .method_generator import MethodGenerator
from .import_generator import ImportGenerator

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Main code generator that coordinates all generation operations."""

    def __init__(self):
        """Initialize the code generator with sub-generators."""
        self.class_generator = ClassGenerator()
        self.method_generator = MethodGenerator()
        self.import_generator = ImportGenerator()
        logger.info("✅ Code generator initialized")

    def generate(
        self, extracted_model: Dict[str, Any], target_language: str = "python"
    ) -> str:
        """
        Generate code from an extracted model.

        Args:
            extracted_model: The extracted model from reverse engineering
            target_language: Target programming language

        Returns:
            Generated code as string
        """
        try:
            logger.info(f"🔍 Generating {target_language} code from extracted model...")

            # STEP 1: Build complete in-memory model first (BEST PRACTICE)
            complete_model = self._build_complete_model(extracted_model)
            logger.info(
                f"✅ Built complete in-memory model with {len(complete_model.get('components', {}))} components"
            )

            # STEP 2: Validate the complete model
            self._validate_complete_model(complete_model)
            logger.info("✅ Complete model validation passed")

            # STEP 3: Generate code from the complete model
            code = self._generate_from_complete_model(complete_model, target_language)
            logger.info(
                f"✅ Generated {target_language} code successfully from complete model"
            )

            return code

        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            raise

    def _build_complete_model(self, extracted_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a complete in-memory model from the extracted model.

        This implements the best practice of building the complete model first
        before generating any code.
        """
        logger.info("🏗️  Building complete in-memory model...")

        # Start with the extracted model
        complete_model = extracted_model.copy()

        # Ensure we have all required fields
        complete_model.setdefault("system_name", "Unknown System")
        complete_model.setdefault("description", "")
        complete_model.setdefault("purpose", "")
        complete_model.setdefault("model_id", "unknown")
        complete_model.setdefault("file_metadata", {"executable": False})

        # Build complete component structure
        components = complete_model.get("components", {})
        if isinstance(components, dict):
            for class_name, class_info in components.items():
                # Ensure each class has complete structure
                complete_model["components"][class_name] = self._build_complete_class(
                    class_info
                )

        logger.info(
            f"✅ Complete model built with {len(complete_model.get('components', {}))} components"
        )
        return complete_model

    def _build_complete_class(self, class_info: Dict[str, Any]) -> Dict[str, Any]:
        """Build a complete class structure with all required fields."""
        complete_class = class_info.copy()

        # Ensure required fields exist
        complete_class.setdefault("name", "UnknownClass")
        complete_class.setdefault("type", "class")
        complete_class.setdefault("description", "")
        complete_class.setdefault("responsibility", "")
        complete_class.setdefault("methods", [])
        complete_class.setdefault("bases", [])
        complete_class.setdefault("class_decorators", [])

        # Build complete method structures
        methods = complete_class.get("methods", [])
        complete_methods = []
        for method in methods:
            complete_methods.append(self._build_complete_method(method))

        complete_class["methods"] = complete_methods

        return complete_class

    def _build_complete_method(self, method_info: Dict[str, Any]) -> Dict[str, Any]:
        """Build a complete method structure with all required fields."""
        complete_method = method_info.copy()

        # Ensure required fields exist
        complete_method.setdefault("name", "unknown_method")
        complete_method.setdefault("docstring", "")
        complete_method.setdefault("return_type", "Any")
        complete_method.setdefault("parameters", [])
        complete_method.setdefault("decorators", [])

        return complete_method

    def _validate_complete_model(self, complete_model: Dict[str, Any]) -> None:
        """Validate that the complete model has all required structure."""
        logger.info("🔍 Validating complete model structure...")

        # Validate required top-level fields
        required_fields = ["system_name", "components"]
        for field in required_fields:
            if field not in complete_model:
                raise ValueError(f"Missing required field: {field}")

        # Validate components structure
        components = complete_model.get("components", {})
        if not isinstance(components, dict):
            raise ValueError("Components must be a dictionary")

        # Validate each component
        for class_name, class_info in components.items():
            if not isinstance(class_info, dict):
                raise ValueError(f"Component {class_name} must be a dictionary")

            # Validate class structure
            required_class_fields = ["name", "type", "methods"]
            for field in required_class_fields:
                if field not in class_info:
                    raise ValueError(
                        f"Component {class_name} missing required field: {field}"
                    )

        logger.info("✅ Complete model validation passed")

    def _generate_from_complete_model(
        self, complete_model: Dict[str, Any], target_language: str
    ) -> str:
        """Generate code from the complete, validated model."""
        logger.info(f"🎯 Generating {target_language} code from complete model...")

        # Generate unique generation ID for traceability
        generation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        model_id = complete_model.get("model_id", "unknown")

        logger.info(f"🎯 Generating code from complete model {model_id}")
        logger.info(f"🆔 Generation ID: {generation_id} at {timestamp}")

        # Extract system information and metadata
        system_name = complete_model.get("system_name", "Unknown System")
        description = complete_model.get("description", "")
        purpose = complete_model.get("purpose", "")

        # Build file header
        metadata = complete_model.get("file_metadata", {})
        is_executable = metadata.get("executable", False)

        # Start building code
        code = self._build_file_header(
            system_name,
            description,
            purpose,
            model_id,
            generation_id,
            timestamp,
            is_executable,
        )

        # Generate imports
        code += self.import_generator.generate_imports(complete_model)

        # Generate components (classes, functions, etc.)
        components = complete_model.get("components", {})
        if isinstance(components, dict):
            for class_name, class_info in components.items():
                code += self.class_generator.generate_class(
                    class_name, class_info, complete_model
                )
                code += "\n\n"  # Add spacing between classes

        # Generate main function if executable
        if is_executable:
            code += self._generate_main_function()

        return code

    def generate_from_model(self, model: Any) -> Dict[str, str]:
        """
        Generate code from a stored model.

        Args:
            model: Stored model object

        Returns:
            Dictionary mapping filenames to generated code
        """
        try:
            # Convert model to extracted model format
            extracted_model = {
                "system_name": model.get("name", "Unknown System"),
                "description": model.get("description", ""),
                "components": model.get("components", {}),
                "model_id": model.get("model_id", "unknown"),
                "file_metadata": {"executable": False},
            }

            # Generate code
            code = self.generate(extracted_model)

            # Return as single file
            filename = f"{model.get('name', 'generated')}.py"
            return {filename: code}

        except Exception as e:
            logger.error(f"❌ Failed to generate code from model: {e}")
            raise

    def _build_file_header(
        self,
        system_name: str,
        description: str,
        purpose: str,
        model_id: str,
        generation_id: str,
        timestamp: str,
        is_executable: bool,
    ) -> str:
        """Build the file header with docstring and metadata."""
        code = "#!/usr/bin/env python3\n\n" if is_executable else ""

        # Add docstring with generation metadata
        purpose_line = f"\n{purpose}" if purpose else ""
        code += f"""\"\"\"
{system_name}

{description}{purpose_line}

Generated from Model: {model_id}
Generation ID: {generation_id}
Generated at: {timestamp}
\"\"\"

"""
        return code

    def _generate_main_function(self) -> str:
        """Generate a main function for executable files."""
        return """def main() -> None:
    \"\"\"Main function for executable module.\"\"\"
    print("Generated module executed successfully!")


if __name__ == "__main__":
    main()
"""
