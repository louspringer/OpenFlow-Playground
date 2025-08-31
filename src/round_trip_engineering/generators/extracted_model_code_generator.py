#!/usr/bin/env python3
"""
Extracted Model Code Generator
Generates complete Python module skeleton code from extracted models.
"""

import logging
import re
from typing import Any, Dict

from .base_reflective_module import BaseReflectiveModule


class ExtractedModelCodeGenerator(BaseReflectiveModule):
    """Generates Python code from extracted models (reverse engineering output)"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "code_generation": [
                "generate_module_from_extracted_model",
                "generate_class_from_extracted_model",
                "generate_method_from_extracted_model",
                "generate_function_from_extracted_model",
            ],
            "code_cleaning": [
                "clean_generated_code",
                "ensure_clean_generation",
            ],
            "formatting": [
                "record_formatting_patterns",
            ],
        }

    def generate_module_from_extracted_model(
        self, extracted_model: Dict[str, Any]
    ) -> str:
        """Generate complete Python module skeleton code from an extracted model"""
        self.logger.info(
            f"🎯 Generating module from extracted model: {extracted_model.get('name', 'Unknown')}"
        )

        # Extract basic information
        module_name = extracted_model.get("name", "generated_module")
        classes = extracted_model.get("classes", [])
        functions = extracted_model.get("functions", [])
        imports = extracted_model.get("imports", [])

        # Generate module code
        code_lines = []
        
        # Add module docstring
        code_lines.append('"""')
        code_lines.append(f"Generated module: {module_name}")
        code_lines.append("Generated from extracted model")
        code_lines.append('"""')
        code_lines.append("")

        # Add imports
        if imports:
            for import_stmt in imports:
                code_lines.append(import_stmt)
            code_lines.append("")

        # Generate classes
        for class_data in classes:
            class_code = self.generate_class_from_extracted_model(class_data)
            code_lines.extend(class_code.split("\n"))
            code_lines.append("")

        # Generate functions
        for func_data in functions:
            func_code = self.generate_function_from_extracted_model(func_data)
            code_lines.extend(func_code.split("\n"))
            code_lines.append("")

        # Clean up empty lines
        code = "\n".join(code_lines).strip()
        code = self.ensure_clean_generation(code)

        self.logger.info(f"✅ Generated module with {len(classes)} classes and {len(functions)} functions")
        return code

    def generate_class_from_extracted_model(self, class_data: Dict[str, Any]) -> str:
        """Generate a class from extracted class data"""
        class_name = class_data.get("name", "GeneratedClass")
        methods = class_data.get("methods", [])
        bases = class_data.get("bases", [])
        docstring = class_data.get("docstring", f"Generated class {class_name}")

        code_lines = []
        
        # Class definition
        if bases:
            base_classes = ", ".join(bases)
            code_lines.append(f"class {class_name}({base_classes}):")
        else:
            code_lines.append(f"class {class_name}:")

        # Class docstring
        code_lines.append(f'    """{docstring}"""')
        code_lines.append("")

        # Generate methods
        for method_data in methods:
            method_code = self.generate_method_from_extracted_model(method_data)
            # Indent method code
            indented_method = "\n".join(f"    {line}" for line in method_code.split("\n"))
            code_lines.append(indented_method)
            code_lines.append("")

        return "\n".join(code_lines)

    def generate_method_from_extracted_model(self, method_data: Dict[str, Any]) -> str:
        """Generate a method from extracted method data"""
        method_name = method_data.get("name", "generated_method")
        parameters = method_data.get("parameters", [])
        return_type = method_data.get("return_type", "Any")
        docstring = method_data.get("docstring", f"Generated method {method_name}")
        body = method_data.get("body", "pass")

        code_lines = []
        
        # Method signature
        if parameters:
            param_str = ", ".join(parameters)
            code_lines.append(f"def {method_name}({param_str}) -> {return_type}:")
        else:
            code_lines.append(f"def {method_name}(self) -> {return_type}:")

        # Method docstring
        code_lines.append(f'        """{docstring}"""')
        
        # Method body
        if body and body != "pass":
            code_lines.append(f"        {body}")
        else:
            code_lines.append("        pass")

        return "\n".join(code_lines)

    def generate_function_from_extracted_model(self, func_data: Dict[str, Any]) -> str:
        """Generate a function from extracted function data"""
        func_name = func_data.get("name", "generated_function")
        parameters = func_data.get("parameters", [])
        return_type = func_data.get("return_type", "Any")
        docstring = func_data.get("docstring", f"Generated function {func_name}")
        body = func_data.get("body", "pass")

        code_lines = []
        
        # Function signature
        if parameters:
            param_str = ", ".join(parameters)
            code_lines.append(f"def {func_name}({param_str}) -> {return_type}:")
        else:
            code_lines.append(f"def {func_name}() -> {return_type}:")

        # Function docstring
        code_lines.append(f'    """{docstring}"""')
        
        # Function body
        if body and body != "pass":
            code_lines.append(f"    {body}")
        else:
            code_lines.append("    pass")

        return "\n".join(code_lines)

    def clean_generated_code(self, code: str) -> str:
        """Clean up generated code by removing redundant patterns"""
        # Remove multiple consecutive empty lines
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        
        # Remove trailing whitespace
        code = re.sub(r'[ \t]+\n', '\n', code)
        
        # Ensure proper spacing around class/function definitions
        code = re.sub(r'(\n)(class|def)', r'\1\n\2', code)
        
        return code.strip()

    def ensure_clean_generation(self, code: str) -> str:
        """Ensure the generated code is clean and properly formatted"""
        # Apply basic cleaning
        code = self.clean_generated_code(code)
        
        # Ensure proper line endings
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove any completely empty lines at the end
        code = code.rstrip('\n')
        
        return code

    def record_formatting_patterns(self, code: str) -> Dict[str, Any]:
        """Record formatting patterns in the generated code for analysis"""
        patterns = {
            "total_lines": len(code.split('\n')),
            "empty_lines": len([line for line in code.split('\n') if line.strip() == '']),
            "class_definitions": len(re.findall(r'^class\s+\w+', code, re.MULTILINE)),
            "function_definitions": len(re.findall(r'^def\s+\w+', code, re.MULTILINE)),
            "docstrings": len(re.findall(r'""".*?"""', code, re.DOTALL)),
            "imports": len(re.findall(r'^import\s+|^from\s+', code, re.MULTILINE)),
        }
        
        return patterns
