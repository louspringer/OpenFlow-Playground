#!/usr/bin/env python3
"""
Type Handler & Utilities
Handles type annotations, parsing, and utility functions for code generation.
"""

import re
import logging
from typing import Any, Dict, List, Optional

from .base_reflective_module import BaseReflectiveModule


class TypeHandler(BaseReflectiveModule):
    """Handles type annotations and utility functions for code generation"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "type_handling": [
                "parse_method_signature",
                "clean_complex_type",
                "get_default_value",
                "normalize_type_annotation",
            ],
            "method_parsing": [
                "parse_method_signature",
                "generate_method_from_parsed",
                "generate_method_from_dict",
            ],
            "utilities": [
                "extract_type_info",
                "validate_type_annotation",
            ],
        }

    def parse_method_signature(self, method_signature: str) -> Dict[str, Any]:
        """Parse a method signature string into structured data"""
        self.logger.debug(f"Parsing method signature: {method_signature}")

        # Basic pattern matching for method signatures
        # Example: "def method_name(self, param1: str, param2: int = 10) -> bool:"
        
        # Extract method name
        name_match = re.search(r'def\s+(\w+)', method_signature)
        method_name = name_match.group(1) if name_match else "unknown_method"

        # Extract parameters
        params_match = re.search(r'\((.*?)\)', method_signature)
        params_str = params_match.group(1) if params_match else ""
        
        parameters = []
        if params_str:
            # Split by comma, but be careful about nested parentheses
            param_parts = self._split_parameters(params_str)
            for param in param_parts:
                param_info = self._parse_parameter(param.strip())
                if param_info:
                    parameters.append(param_info)

        # Extract return type
        return_match = re.search(r'->\s*([^:]+)', method_signature)
        return_type = return_match.group(1).strip() if return_match else "Any"

        return {
            "name": method_name,
            "parameters": parameters,
            "return_type": return_type,
            "signature": method_signature,
        }

    def _split_parameters(self, params_str: str) -> List[str]:
        """Split parameter string by comma, respecting nested parentheses"""
        params = []
        current_param = ""
        paren_count = 0
        
        for char in params_str:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                if current_param.strip():
                    params.append(current_param.strip())
                current_param = ""
                continue
            
            current_param += char
        
        if current_param.strip():
            params.append(current_param.strip())
        
        return params

    def _parse_parameter(self, param_str: str) -> Optional[Dict[str, Any]]:
        """Parse a single parameter string into structured data"""
        if not param_str:
            return None

        # Handle self parameter
        if param_str == "self":
            return {
                "name": "self",
                "type": "Any",
                "default": None,
                "is_self": True,
            }

        # Parse parameter with type annotation and default value
        # Format: name: type = default
        param_pattern = r'(\w+)(?:\s*:\s*([^=]+))?(?:\s*=\s*(.+))?'
        match = re.match(param_pattern, param_str)
        
        if match:
            name = match.group(1)
            param_type = match.group(2).strip() if match.group(2) else "Any"
            default_value = match.group(3).strip() if match.group(3) else None
            
            return {
                "name": name,
                "type": param_type,
                "default": default_value,
                "is_self": False,
            }
        
        # Simple parameter without type annotation
        return {
            "name": param_str,
            "type": "Any",
            "default": None,
            "is_self": False,
        }

    def generate_method_from_parsed(self, parsed_method: Dict[str, Any]) -> str:
        """Generate method code from parsed method data"""
        method_name = parsed_method.get("name", "generated_method")
        parameters = parsed_method.get("parameters", [])
        return_type = parsed_method.get("return_type", "Any")

        code_lines = []
        
        # Method signature
        param_str = ", ".join([f"{p['name']}: {p['type']}" for p in parameters])
        code_lines.append(f"def {method_name}({param_str}) -> {return_type}:")
        
        # Method docstring
        code_lines.append(f'    """Generated method {method_name}"""')
        
        # Method body
        code_lines.append("    pass")
        
        return "\n".join(code_lines)

    def generate_method_from_dict(self, method: Dict[str, Any]) -> str:
        """Generate method code from method dictionary"""
        method_name = method.get("name", "generated_method")
        arguments = method.get("arguments", [])
        return_type = method.get("return_type", "Any")
        docstring = method.get("docstring", f"Generated method {method_name}")

        code_lines = []
        
        # Method signature
        if arguments:
            param_str = ", ".join([f"{arg['name']}: {arg.get('type', 'Any')}" for arg in arguments])
            code_lines.append(f"def {method_name}({param_str}) -> {return_type}:")
        else:
            code_lines.append(f"def {method_name}(self) -> {return_type}:")
        
        # Method docstring
        code_lines.append(f'    """{docstring}"""')
        
        # Method body
        code_lines.append("    pass")
        
        return "\n".join(code_lines)

    def clean_complex_type(self, type_annotation: str) -> str:
        """Clean and normalize complex type annotations"""
        if not type_annotation:
            return "Any"

        # Remove extra whitespace
        cleaned = type_annotation.strip()
        
        # Handle common complex types
        # Union types: Union[str, int] -> str | int
        cleaned = re.sub(r'Union\[([^\]]+)\]', r'\1', cleaned)
        
        # Optional types: Optional[str] -> str | None
        cleaned = re.sub(r'Optional\[([^\]]+)\]', r'\1 | None', cleaned)
        
        # List types: List[str] -> list[str]
        cleaned = re.sub(r'List\[([^\]]+)\]', r'list[\1]', cleaned)
        
        # Dict types: Dict[str, int] -> dict[str, int]
        cleaned = re.sub(r'Dict\[([^\]]+)\]', r'dict[\1]', cleaned)
        
        # Tuple types: Tuple[str, int] -> tuple[str, int]
        cleaned = re.sub(r'Tuple\[([^\]]+)\]', r'tuple[\1]', cleaned)
        
        # Set types: Set[str] -> set[str]
        cleaned = re.sub(r'Set\[([^\]]+)\]', r'set[\1]', cleaned)
        
        return cleaned

    def get_default_value(self, type_name: str) -> str:
        """Get appropriate default value for a given type"""
        type_name = type_name.lower().strip()
        
        # Handle basic types
        if type_name in ["str", "string"]:
            return '""'
        elif type_name in ["int", "integer"]:
            return "0"
        elif type_name in ["float", "number"]:
            return "0.0"
        elif type_name in ["bool", "boolean"]:
            return "False"
        elif type_name in ["list", "array"]:
            return "[]"
        elif type_name in ["dict", "dictionary"]:
            return "{}"
        elif type_name in ["set"]:
            return "set()"
        elif type_name in ["tuple"]:
            return "()"
        elif type_name in ["bytes"]:
            return 'b""'
        elif type_name in ["none", "null"]:
            return "None"
        else:
            return "None"

    def normalize_type_annotation(self, type_annotation: str) -> str:
        """Normalize type annotation to standard format"""
        if not type_annotation:
            return "Any"
        
        # Clean the type annotation
        normalized = self.clean_complex_type(type_annotation)
        
        # Handle common aliases
        type_mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "dictionary": "dict",
            "null": "None",
        }
        
        for alias, standard in type_mapping.items():
            normalized = re.sub(rf'\b{alias}\b', standard, normalized, flags=re.IGNORECASE)
        
        return normalized

    def extract_type_info(self, type_annotation: str) -> Dict[str, Any]:
        """Extract detailed information about a type annotation"""
        normalized = self.normalize_type_annotation(type_annotation)
        
        return {
            "original": type_annotation,
            "normalized": normalized,
            "is_optional": "None" in normalized or "|" in normalized,
            "is_collection": any(t in normalized for t in ["list", "dict", "set", "tuple"]),
            "is_union": "|" in normalized,
            "default_value": self.get_default_value(normalized),
        }

    def validate_type_annotation(self, type_annotation: str) -> bool:
        """Validate if a type annotation is syntactically correct"""
        if not type_annotation:
            return False
        
        # Basic validation - check for common patterns
        valid_patterns = [
            r'^[A-Za-z_][A-Za-z0-9_]*$',  # Simple type names
            r'^[A-Za-z_][A-Za-z0-9_]*\[.*\]$',  # Generic types
            r'^[A-Za-z_][A-Za-z0-9_]* \| [A-Za-z_][A-Za-z0-9_]*$',  # Union types
        ]
        
        for pattern in valid_patterns:
            if re.match(pattern, type_annotation):
                return True
        
        return False
