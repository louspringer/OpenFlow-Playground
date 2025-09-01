#!/usr/bin/env python3
"""
Data Cleaner
Handles cleaning and normalization of extracted model data
"""

import logging
from typing import Any, Dict, List

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class DataCleaner(BaseReflectiveModule):
    """Handles cleaning and normalization of extracted model data"""

    def __init__(self) -> None:
        super().__init__()

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "data_cleaning": [
                "clean_extracted_model",
                "clean_class_data",
                "clean_method_data",
                "clean_function_data",
            ],
            "data_validation": [
                "validate_model_structure",
                "validate_class_data",
                "validate_method_data",
            ],
        }

    def clean_extracted_model(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize the extracted model"""
        cleaned = model.copy()

        # Ensure consistent structure
        if "classes" not in cleaned:
            cleaned["classes"] = {}
        if "functions" not in cleaned:
            cleaned["functions"] = []
        if "imports" not in cleaned:
            cleaned["imports"] = []
        if "metadata" not in cleaned:
            cleaned["metadata"] = {}

        # Clean class data
        for class_name, class_data in cleaned["classes"].items():
            if isinstance(class_data, dict):
                cleaned["classes"][class_name] = self.clean_class_data(class_data)

        # Clean function data
        for func_name, func_data in cleaned["functions"].items():
            if isinstance(func_data, dict):
                cleaned["functions"][func_name] = self.clean_function_data(func_data)

        return cleaned

    def clean_class_data(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean class data structure"""
        cleaned = class_data.copy()

        # Ensure required fields
        if "name" not in cleaned:
            cleaned["name"] = "UnknownClass"
        if "methods" not in cleaned:
            cleaned["methods"] = {}
        if "attributes" not in cleaned:
            cleaned["attributes"] = []
        if "bases" not in cleaned:
            cleaned["bases"] = []
        if "docstring" not in cleaned:
            cleaned["docstring"] = ""

        # Clean method data
        for method_name, method_data in cleaned["methods"].items():
            if isinstance(method_data, dict):
                cleaned["methods"][method_name] = self.clean_method_data(method_data)

        return cleaned

    def clean_method_data(self, method_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean method data structure"""
        cleaned = method_data.copy()

        # Ensure required fields
        if "name" not in cleaned:
            cleaned["name"] = "unknown_method"
        if "parameters" not in cleaned:
            cleaned["parameters"] = []
        if "return_type" not in cleaned:
            cleaned["return_type"] = "Any"
        if "docstring" not in cleaned:
            cleaned["docstring"] = ""
        if "source" not in cleaned:
            cleaned["source"] = ""

        # Normalize parameters
        if "arguments" in cleaned and "parameters" not in cleaned:
            cleaned["parameters"] = cleaned.pop("arguments")

        return cleaned

    def clean_function_data(self, func_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean function data structure"""
        cleaned = func_data.copy()

        # Ensure required fields
        if "name" not in cleaned:
            cleaned["name"] = "unknown_function"
        if "parameters" not in cleaned:
            cleaned["parameters"] = []
        if "return_type" not in cleaned:
            cleaned["return_type"] = "Any"
        if "docstring" not in cleaned:
            cleaned["docstring"] = ""
        if "source" not in cleaned:
            cleaned["source"] = ""

        # Normalize parameters
        if "arguments" in cleaned and "parameters" not in cleaned:
            cleaned["parameters"] = cleaned.pop("arguments")

        return cleaned

    def validate_model_structure(self, model: Dict[str, Any]) -> bool:
        """Validate that the extracted model has the required structure"""
        required_keys = ["name", "type"]

        # Check top-level structure
        if not all(key in model for key in required_keys):
            logger.error(f"Missing required keys: {required_keys}")
            return False

        # Check if it's a module or class
        if model["type"] == "module":
            if "classes" not in model and "functions" not in model:
                logger.error("Module must contain classes or functions")
                return False

        return True

    def validate_class_data(self, class_data: Dict[str, Any]) -> bool:
        """Validate class data structure"""
        try:
            required_attrs = ["name", "methods"]

            for attr in required_attrs:
                if not hasattr(class_data, attr):
                    logger.error(f"Class missing required attribute: {attr}")
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ Class validation failed: {e}")
            return False

    def validate_method_data(self, method_data: Dict[str, Any]) -> bool:
        """Validate method data structure"""
        try:
            required_attrs = ["name", "parameters", "return_type"]

            for attr in required_attrs:
                if not hasattr(method_data, attr):
                    logger.error(f"Method missing required attribute: {attr}")
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ Method validation failed: {e}")
            return False

    def get_cleaning_statistics(self, original_model: Dict[str, Any], cleaned_model: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about the cleaning process"""
        stats = {
            "original_size": len(str(original_model)),
            "cleaned_size": len(str(cleaned_model)),
            "size_reduction": 0,
            "fields_added": 0,
            "fields_modified": 0,
        }

        # Calculate size reduction
        if stats["original_size"] > 0:
            stats["size_reduction"] = (stats["original_size"] - stats["cleaned_size"]) / stats["original_size"] * 100

        # Count fields added/modified (simplified)
        original_keys = set(self._flatten_dict(original_model).keys())
        cleaned_keys = set(self._flatten_dict(cleaned_model).keys())

        stats["fields_added"] = len(cleaned_keys - original_keys)
        stats["fields_modified"] = len(original_keys.intersection(cleaned_keys))

        return stats

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        """Flatten a nested dictionary for key counting"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
