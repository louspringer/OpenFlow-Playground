#!/usr/bin/env python3
"""
Extracted Model Processor
Processes extracted models from reverse engineering for code generation
"""

import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from .type_normalizer import TypeNormalizer
from .data_cleaner import DataCleaner


logger = logging.getLogger(__name__)


class ExtractedModelProcessor(BaseReflectiveModule):
    """Processes extracted models from reverse engineering for code generation"""

    def __init__(self) -> None:
        super().__init__()
        self.processed_models: Dict[str, Dict[str, Any]] = {}
        self.type_normalizer = TypeNormalizer()
        self.data_cleaner = DataCleaner()

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "model_processing": [
                "process_extracted_model",
                "validate_extracted_model",
                "clean_extracted_model",
            ],
            "code_generation": [
                "generate_code_from_extracted_model",
                "generate_class_from_extracted_model",
                "generate_method_from_extracted_model",
            ],
        }

    def process_extracted_model(
        self, extracted_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process an extracted model for code generation"""
        logger.info("🎯 Processing extracted model for code generation")

        # Validate the model structure
        if not self.data_cleaner.validate_model_structure(extracted_model):
            raise ValueError("Invalid extracted model structure")

        # Clean and normalize the model
        cleaned_model = self.data_cleaner.clean_extracted_model(extracted_model)

        # Process classes
        if "classes" in cleaned_model:
            for class_name, class_data in cleaned_model["classes"].items():
                cleaned_model["classes"][class_name] = self._process_class_data(
                    class_data
                )

        # Process functions
        if "functions" in cleaned_model:
            for func_name, func_data in cleaned_model["functions"].items():
                cleaned_model["functions"][func_name] = self._process_function_data(
                    func_data
                )

        # Store processed model
        model_id = extracted_model.get("name", "unnamed_model")
        self.processed_models[model_id] = cleaned_model

        logger.info(f"✅ Processed extracted model: {model_id}")
        return cleaned_model

    def _validate_extracted_model_structure(self, model: Dict[str, Any]) -> bool:
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

    def _process_class_data(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process class data for code generation"""
        processed = class_data.copy()

        # Process methods
        for method_name, method_data in processed["methods"].items():
            if isinstance(method_data, dict):
                processed["methods"][method_name] = self._process_method_data(
                    method_data
                )

        # Process attributes
        processed["attributes"] = self._process_attributes(
            processed.get("attributes", [])
        )

        return processed

    def _process_method_data(self, method_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method data for code generation"""
        processed = method_data.copy()

        # Process parameters
        processed["parameters"] = self._process_parameters(
            processed.get("parameters", [])
        )

        # Process return type
        processed["return_type"] = self._normalize_type(
            processed.get("return_type", "Any")
        )

        return processed

    def _process_function_data(self, func_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process function data for code generation"""
        processed = func_data.copy()

        # Process parameters
        processed["parameters"] = self._process_parameters(
            processed.get("parameters", [])
        )

        # Process return type
        processed["return_type"] = self._normalize_type(
            processed.get("return_type", "Any")
        )

        return processed

    def _process_parameters(
        self, parameters: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process method/function parameters"""
        return self.type_normalizer.normalize_parameter_types(parameters)

    def _process_attributes(
        self, attributes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process class attributes"""
        processed = []

        for attr in attributes:
            if isinstance(attr, dict):
                processed_attr = attr.copy()

                # Ensure required fields
                if "name" not in processed_attr:
                    processed_attr["name"] = "attribute"
                if "type" not in processed_attr:
                    processed_attr["type"] = "Any"
                if "default" not in processed_attr:
                    processed_attr["default"] = None

                # Normalize type
                processed_attr["type"] = self._normalize_type(processed_attr["type"])

                processed.append(processed_attr)
            else:
                # Handle string attributes
                processed.append({"name": str(attr), "type": "Any", "default": None})

        return processed

    def _normalize_type(self, type_annotation: str) -> str:
        """Normalize type annotations"""
        return self.type_normalizer.normalize_type(type_annotation)

    def get_processed_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get a processed model by ID"""
        return self.processed_models.get(model_id)

    def list_processed_models(self) -> List[str]:
        """List all processed model IDs"""
        return list(self.processed_models.keys())

    def clear_processed_models(self) -> None:
        """Clear all processed models"""
        self.processed_models.clear()
        logger.info("✅ Cleared all processed models")
