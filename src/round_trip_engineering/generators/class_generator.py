"""
Class Generator Module

This module handles class generation from model components.
"""

import logging
from typing import Dict, Any, List

from .method_generator import MethodGenerator

logger = logging.getLogger(__name__)


class ClassGenerator:
    """Generates class code from model components."""

    def __init__(self):
        """Initialize the class generator."""
        self.method_generator = MethodGenerator()
        logger.info("✅ Class generator initialized")

    def generate_class(
        self,
        class_name: str,
        class_info: Dict[str, Any],
        extracted_model: Dict[str, Any],
    ) -> str:
        """
        Generate class code from class info.

        Args:
            class_name: Name of the class
            class_info: Class information from model
            extracted_model: Full extracted model for context

        Returns:
            Generated class code as string
        """
        try:
            logger.info(f"🔍 Generating class: {class_name}")

            # Extract class information
            responsibility = class_info.get("responsibility", "")
            methods = class_info.get("methods", [])
            bases = class_info.get("bases", [])
            decorators = class_info.get("class_decorators", [])

            # Build class definition
            class_def = f"class {class_name}"
            if bases:
                class_def += f"({', '.join(bases)})"
            class_def += ":"

            # Add decorators
            decorator_code = ""
            for decorator in decorators:
                decorator_code += f"@{decorator}\n"

            # Build class code
            code = f"""{decorator_code}{class_def}
    \"\"\"
    {responsibility}
    \"\"\"
"""

            # Add methods
            for i, method in enumerate(methods):
                code += self.method_generator.generate_method(method, extracted_model)
                # Add single blank line between methods (not extra)
                if i < len(methods) - 1:
                    code += "\n"

            logger.info(f"✅ Generated class {class_name} with {len(methods)} methods")
            return code

        except Exception as e:
            logger.error(f"❌ Failed to generate class {class_name}: {e}")
            return f"# Error generating class {class_name}: {e}\n"
