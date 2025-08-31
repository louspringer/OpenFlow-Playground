"""
Method Generator Module

This module handles method generation from model methods.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MethodGenerator:
    """Generates method code from model methods."""

    def __init__(self):
        """Initialize the method generator."""
        logger.info("✅ Method generator initialized")

    def generate_method(
        self, method_info: Dict[str, Any], extracted_model: Dict[str, Any]
    ) -> str:
        """
        Generate method code from method info.

        Args:
            method_info: Method information from model
            extracted_model: Full extracted model for context

        Returns:
            Generated method code as string
        """
        try:
            # Extract method information
            name = method_info.get("name", "unknown_method")
            docstring = method_info.get("docstring", "")
            decorators = method_info.get("decorators", [])
            return_type = method_info.get("return_type", "Any")
            is_async = method_info.get("is_async", False)

            # Handle both enhanced parser format (arguments) and legacy format (parameters)
            parameters = method_info.get("parameters", [])
            if not parameters and "arguments" in method_info:
                # Convert enhanced parser format to method generator format
                enhanced_args = method_info.get("arguments", [])
                parameters = []
                for arg in enhanced_args:
                    # Skip 'self' parameter as it's added automatically by the method generator
                    if arg.get("name") == "self":
                        continue
                    param = {
                        "name": arg.get("name", "param"),
                        "type": arg.get("type", "Any"),
                        "default": arg.get("default"),
                    }
                    parameters.append(param)

            # Ensure return_type is a string
            if hasattr(return_type, "__str__"):
                return_type = str(return_type)
            else:
                return_type = "Any"

            # Build method signature
            method_sig = self._build_method_signature(
                name, parameters, return_type, is_async
            )

            # Add decorators
            decorator_code = ""
            for decorator in decorators:
                decorator_code += f"    @{decorator}\n"

            # Build method code
            code = f"""{decorator_code}    {method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # TODO: Implement method logic
        pass

"""

            logger.debug(f"✅ Generated method: {name}")
            return code

        except Exception as e:
            logger.error(f"❌ Failed to generate method {name}: {e}")
            return f"    # Error generating method {name}: {e}\n"

    def _build_method_signature(
        self,
        name: str,
        parameters: List[Dict[str, Any]],
        return_type: str,
        is_async: bool,
    ) -> str:
        """Build the method signature string."""
        # Build parameter string
        param_str = self._build_parameter_string(parameters)

        # Build method signature
        if is_async:
            if param_str:
                method_sig = f"async def {name}(self, {param_str}) -> {return_type}:"
            else:
                method_sig = f"async def {name}(self) -> {return_type}:"
        else:
            if param_str:
                method_sig = f"def {name}(self, {param_str}) -> {return_type}:"
            else:
                method_sig = f"def {name}(self) -> {return_type}:"

        return method_sig

    def _build_parameter_string(self, parameters: List[Dict[str, Any]]) -> str:
        """Build the parameter string for method signature."""
        if not parameters:
            return ""

        param_parts = []
        for param in parameters:
            param_name = param.get("name", "param")
            param_type = param.get("type", "Any")
            default_value = param.get("default")

            if default_value is not None:
                param_parts.append(f"{param_name}: {param_type} = {default_value}")
            else:
                param_parts.append(f"{param_name}: {param_type}")

        return ", ".join(param_parts)
