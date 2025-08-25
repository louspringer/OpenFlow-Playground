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

            # Generate unique generation ID for traceability
            generation_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            model_id = extracted_model.get("model_id", "unknown")

            logger.info(f"🎯 Generating code from extracted model {model_id}")
            logger.info(f"🆔 Generation ID: {generation_id} at {timestamp}")

            # Extract system information and metadata
            system_name = extracted_model.get("system_name", "Unknown System")
            description = extracted_model.get("description", "")
            purpose = extracted_model.get("purpose", "")

            # Build file header
            metadata = extracted_model.get("file_metadata", {})
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
            code += self.import_generator.generate_imports(extracted_model)

            # Generate components (classes, functions, etc.)
            components = extracted_model.get("components", {})
            if isinstance(components, dict):
                for class_name, class_info in components.items():
                    code += self.class_generator.generate_class(
                        class_name, class_info, extracted_model
                    )
                    code += "\n\n"  # Add spacing between classes

            # Generate main function if executable
            if is_executable:
                code += self._generate_main_function()

            logger.info(f"✅ Generated {target_language} code successfully")
            return code

        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            raise

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
