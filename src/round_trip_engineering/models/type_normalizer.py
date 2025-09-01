#!/usr/bin/env python3
"""
Type Normalizer
Handles normalization of type annotations and parameter types
"""

import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class TypeNormalizer(BaseReflectiveModule):
    """Handles normalization of type annotations and parameter types"""

    def __init__(self) -> None:
        super().__init__()

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "type_normalization": [
                "normalize_type",
                "normalize_parameter_types",
                "validate_type_annotation",
            ],
            "type_analysis": ["analyze_type_patterns", "suggest_type_improvements"],
        }

    def normalize_type(self, type_annotation: str) -> str:
        """Normalize type annotations"""
        if not type_annotation:
            return "Any"

        # Remove common prefixes/suffixes
        type_str = str(type_annotation).strip()

        # Handle common type patterns
        if type_str.lower() in ["none", "null"]:
            return "None"
        elif type_str.lower() in ["str", "string"]:
            return "str"
        elif type_str.lower() in ["int", "integer"]:
            return "int"
        elif type_str.lower() in ["float", "number"]:
            return "float"
        elif type_str.lower() in ["bool", "boolean"]:
            return "bool"
        elif type_str.lower() in ["list", "array"]:
            return "List[Any]"
        elif type_str.lower() in ["dict", "dictionary", "object"]:
            return "Dict[str, Any]"
        elif type_str.lower() in ["any", "unknown"]:
            return "Any"

        return type_str

    def normalize_parameter_types(self, parameters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize types for a list of parameters"""
        normalized = []

        for param in parameters:
            if isinstance(param, dict):
                normalized_param = param.copy()

                # Ensure required fields
                if "name" not in normalized_param:
                    normalized_param["name"] = "param"
                if "type" not in normalized_param:
                    normalized_param["type"] = "Any"
                if "default" not in normalized_param:
                    normalized_param["default"] = None

                # Normalize type
                normalized_param["type"] = self.normalize_type(normalized_param["type"])

                normalized.append(normalized_param)
            else:
                # Handle string parameters
                normalized.append({"name": str(param), "type": "Any", "default": None})

        return normalized

    def validate_type_annotation(self, type_annotation: str) -> Dict[str, Any]:
        """Validate a type annotation"""
        validation_result = {
            "is_valid": True,
            "normalized_type": "",
            "warnings": [],
            "suggestions": [],
        }

        try:
            normalized = self.normalize_type(type_annotation)
            validation_result["normalized_type"] = normalized

            # Check for potential issues
            if type_annotation.lower() in ["unknown", "undefined"]:
                validation_result["warnings"].append("Vague type annotation")
                validation_result["suggestions"].append("Consider using a more specific type")

            if len(type_annotation) > 50:
                validation_result["warnings"].append("Very long type annotation")
                validation_result["suggestions"].append("Consider breaking into multiple types")

            # Check for common patterns that could be improved
            if "Any" in normalized and normalized != "Any":
                validation_result["suggestions"].append("Consider using more specific types instead of Any")

        except Exception as e:
            validation_result["is_valid"] = False
            validation_result["warnings"].append(f"Type validation failed: {e}")

        return validation_result

    def analyze_type_patterns(self, type_annotations: List[str]) -> Dict[str, Any]:
        """Analyze patterns in type annotations"""
        analysis = {
            "total_types": len(type_annotations),
            "type_frequency": {},
            "common_patterns": [],
            "improvement_opportunities": [],
        }

        # Count type frequencies
        for type_ann in type_annotations:
            normalized = self.normalize_type(type_ann)
            analysis["type_frequency"][normalized] = analysis["type_frequency"].get(normalized, 0) + 1

        # Identify common patterns
        for type_name, count in analysis["type_frequency"].items():
            if count > 1:
                analysis["common_patterns"].append({"type": type_name, "frequency": count})

        # Identify improvement opportunities
        if analysis["type_frequency"].get("Any", 0) > len(type_annotations) * 0.3:
            analysis["improvement_opportunities"].append("High usage of Any types - consider more specific types")

        if analysis["type_frequency"].get("str", 0) > len(type_annotations) * 0.5:
            analysis["improvement_opportunities"].append("High usage of str types - consider more specific string types")

        return analysis

    def suggest_type_improvements(self, type_annotation: str, context: str = "") -> List[str]:
        """Suggest improvements for a type annotation"""
        suggestions = []

        normalized = self.normalize_type(type_annotation)

        # Context-specific suggestions
        if context and "id" in context.lower():
            if normalized == "Any":
                suggestions.append("Consider using 'str' for ID fields")
            elif normalized == "str":
                suggestions.append("Consider using 'UUID' for unique identifiers")

        if context and "count" in context.lower():
            if normalized == "Any":
                suggestions.append("Consider using 'int' for count fields")

        if context and "name" in context.lower():
            if normalized == "Any":
                suggestions.append("Consider using 'str' for name fields")

        # General suggestions
        if normalized == "Any":
            suggestions.append("Consider using a more specific type")

        if "List[Any]" in normalized:
            suggestions.append("Consider using more specific list types")

        if "Dict[str, Any]" in normalized:
            suggestions.append("Consider using more specific dictionary types")

        return suggestions

    def get_type_hierarchy(self) -> Dict[str, List[str]]:
        """Get a hierarchy of type relationships"""
        return {
            "basic_types": ["str", "int", "float", "bool", "None"],
            "container_types": ["List", "Dict", "Tuple", "Set"],
            "complex_types": ["Any", "Union", "Optional", "Generic"],
            "custom_types": ["CustomClass", "Enum", "Protocol"],
        }

    def is_basic_type(self, type_annotation: str) -> bool:
        """Check if a type is a basic Python type"""
        basic_types = {"str", "int", "float", "bool", "None", "Any"}
        normalized = self.normalize_type(type_annotation)
        return normalized in basic_types

    def is_container_type(self, type_annotation: str) -> bool:
        """Check if a type is a container type"""
        container_types = {"List", "Dict", "Tuple", "Set"}
        normalized = self.normalize_type(type_annotation)
        return any(ct in normalized for ct in container_types)
