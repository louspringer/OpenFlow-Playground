"""
Class Generator Module

This module orchestrates class generation using focused, single-responsibility modules.
"""

import logging
from typing import Dict, Any, List

from .method_generator import MethodGenerator
from .class_structure_generator import ClassStructureGenerator
from .method_validator import MethodValidator
from .method_processor import MethodCompleter
from .operational_methods_generator import OperationalMethodsGenerator

logger = logging.getLogger(__name__)


class ClassGenerator:
    """Orchestrates class generation using focused modules."""

    def __init__(self):
        """Initialize the class generator with focused modules."""
        self.method_generator = MethodGenerator()
        self.class_structure_generator = ClassStructureGenerator()
        self.method_validator = MethodValidator()
        self.method_completer = MethodCompleter()
        self.operational_methods_generator = OperationalMethodsGenerator()
        logger.info("✅ Class generator initialized with focused modules")

    def generate_class(
        self,
        class_name: str,
        class_info: Dict[str, Any],
        extracted_model: Dict[str, Any],
    ) -> str:
        """
        Generate class code by orchestrating focused modules.

        Args:
            class_name: Name of the class
            class_info: Class information from model
            extracted_model: Full extracted model for context

        Returns:
            Generated class code as string
        """
        try:
            logger.info(f"🔍 Generating class: {class_name}")

            # Check if we have enhanced AST data
            enhanced_ast = class_info.get("enhanced_ast", {})

            if enhanced_ast and enhanced_ast.get("source_code"):
                # Use enhanced AST data for code preservation
                logger.info(f"✅ Using enhanced AST data for {class_name} (preserving {len(enhanced_ast['source_code'])} chars)")
                return self._generate_from_enhanced_ast(class_name, enhanced_ast, extracted_model)
            else:
                # Fallback to basic generation
                logger.info(f"⚠️ No enhanced AST data for {class_name}, using basic generation")
                return self._generate_basic_class(class_name, class_info, extracted_model)

        except Exception as e:
            logger.error(f"❌ Failed to generate class {class_name}: {e}")
            return f"# Error generating class {class_name}: {e}\n"

    def _generate_from_enhanced_ast(
        self,
        class_name: str,
        enhanced_ast: Dict[str, Any],
        extracted_model: Dict[str, Any],
    ) -> str:
        """Generate class code from enhanced AST data using focused modules."""
        try:
            # Use ClassStructureGenerator for class structure
            class_def = self.class_structure_generator.generate_class_structure(class_name, enhanced_ast)

            # Process methods using focused modules
            methods = enhanced_ast.get("methods", [])
            method_code = ""
            valid_methods = 0
            invalid_methods = 0
            generated_methods = 0

            for i, method in enumerate(methods):
                method_name = method.get("name", "")
                method_source = method.get("source_code", "")

                logger.info(f"🔍 Processing method {i + 1}/{len(methods)}: {method_name}")
                logger.info(f"  - Method source length: {len(method_source) if method_source else 0} chars")

                if method_source and method_source.strip():
                    # Use MethodValidator to check if method is valid
                    if self.method_validator.is_valid_method_source(method_source):
                        # Method is valid, use as-is with proper spacing
                        method_code += f"\n{method_source}\n"
                        valid_methods += 1
                        logger.info(f"  ✅ Using preserved method source")
                    else:
                        # Method is invalid, try to complete it
                        logger.info(f"  🔧 Method validation failed, attempting completion")
                        completed_method = self.method_completer.complete_method_source(method_source)
                        if completed_method != method_source:
                            method_code += f"\n{completed_method}\n"
                            logger.info(f"  ✅ Method completed successfully")
                        else:
                            # Completion failed, fall back to generated method
                            logger.info(f"  ⚠️ Method completion failed, using generated method")
                            generated_method = self.method_generator.generate_method(method, extracted_model)
                            method_code += f"\n{generated_method}\n"
                            generated_methods += 1
                        invalid_methods += 1
                else:
                    logger.info(f"  ⚠️ No method source available, using generated method")
                    generated_method = self.method_generator.generate_method(method, extracted_model)
                    method_code += f"\n{generated_method}\n"
                    generated_methods += 1

            logger.info(f"📊 Method processing summary for {class_name}:")
            logger.info(f"  - Valid preserved methods: {valid_methods}")
            logger.info(f"  - Invalid methods (completed): {invalid_methods}")
            logger.info(f"  - Total generated methods: {generated_methods}")

            # Use OperationalMethodsGenerator for ReflectiveModule methods
            operational_methods = self.operational_methods_generator.generate_operational_methods(class_name)

            # Combine everything with proper spacing
            code = f"{class_def}{method_code}{operational_methods}"

            logger.info(f"✅ Generated class {class_name} from enhanced AST with {len(methods)} methods")
            return code

        except Exception as e:
            logger.error(f"❌ Failed to generate from enhanced AST for {class_name}: {e}")
            # Fallback to basic generation
            return self._generate_basic_class(class_name, {"name": class_name}, extracted_model)

    def _generate_basic_class(
        self,
        class_name: str,
        class_info: Dict[str, Any],
        extracted_model: Dict[str, Any],
    ) -> str:
        """Generate basic class code when enhanced AST data is not available."""
        try:
            # Extract class information
            responsibility = class_info.get("responsibility", "")
            methods = class_info.get("methods", [])
            bases = class_info.get("bases", [])
            decorators = class_info.get("class_decorators", [])

            # Use ClassStructureGenerator for basic class structure
            enhanced_ast = {"bases": bases, "docstring": responsibility}
            class_def = self.class_structure_generator.generate_class_structure(class_name, enhanced_ast)

            # Add decorators
            decorator_code = ""
            for decorator in decorators:
                decorator_code += f"@{decorator}\n"

            # Build class code
            code = f"""{decorator_code}{class_def}"""

            # Add methods
            for i, method in enumerate(methods):
                code += self.method_generator.generate_method(method, extracted_model)
                # Add single blank line between methods (not extra)
                if i < len(methods) - 1:
                    code += "\n"

            # Use OperationalMethodsGenerator for ReflectiveModule methods
            operational_methods = self.operational_methods_generator.generate_operational_methods(class_name)
            code += operational_methods

            logger.info(f"✅ Generated basic class {class_name} with {len(methods)} methods")
            return code

        except Exception as e:
            logger.error(f"❌ Failed to generate basic class {class_name}: {e}")
            # Return minimal fallback
            return f'class {class_name}(ReflectiveModule):\n    """Generated class {class_name}"""\n'
