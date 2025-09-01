#!/usr/bin/env python3
"""
Model Persistence
Handles saving and loading of design models
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class ModelPersistence(BaseReflectiveModule):
    """Handles saving and loading of design models"""

    def __init__(self) -> None:
        super().__init__()
        self.models_directory = Path("design_models")

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "persistence": ["save_model", "load_model", "export_model", "import_model"],
            "file_management": [
                "create_models_directory",
                "list_model_files",
                "validate_model_file",
            ],
        }

    def create_models_directory(self) -> Path:
        """Create models directory if it doesn't exist"""
        self.models_directory.mkdir(exist_ok=True)
        logger.info(f"✅ Models directory ready: {self.models_directory}")
        return self.models_directory

    def save_model(
        self,
        model_data: Dict[str, Any],
        model_name: str,
        file_path: Optional[str] = None,
    ) -> bool:
        """Save a design model to file"""
        try:
            if file_path is None:
                # Create models directory if it doesn't exist
                self.create_models_directory()
                file_path = self.models_directory / f"{model_name}.json"

            # Convert model to dictionary format
            model_dict = self._model_to_dict(model_data)

            with open(file_path, "w") as f:
                json.dump(model_dict, f, indent=2)

            logger.info(f"✅ Model {model_name} saved to {file_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save model {model_name}: {e}")
            return False

    def load_model(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load a design model from file"""
        try:
            with open(file_path, "r") as f:
                model_dict = json.load(f)

            # Validate the loaded model
            if not self._validate_model_dict(model_dict):
                raise ValueError("Invalid model file format")

            logger.info(f"✅ Model loaded from {file_path}")
            return model_dict

        except Exception as e:
            logger.error(f"❌ Failed to load model from {file_path}: {e}")
            return None

    def export_model(self, model_data: Dict[str, Any], model_name: str, format: str = "json") -> Optional[str]:
        """Export model in specified format"""
        try:
            if format.lower() == "json":
                return json.dumps(model_data, indent=2)
            elif format.lower() == "yaml":
                import yaml

                return yaml.dump(model_data, default_flow_style=False)
            else:
                logger.error(f"Unsupported export format: {format}")
                return None

        except Exception as e:
            logger.error(f"❌ Failed to export model {model_name}: {e}")
            return None

    def import_model(self, model_content: str, format: str = "json") -> Optional[Dict[str, Any]]:
        """Import model from content string"""
        try:
            if format.lower() == "json":
                return json.loads(model_content)
            elif format.lower() == "yaml":
                import yaml

                return yaml.safe_load(model_content)
            else:
                logger.error(f"Unsupported import format: {format}")
                return None

        except Exception as e:
            logger.error(f"❌ Failed to import model: {e}")
            return None

    def list_model_files(self) -> List[Path]:
        """List all model files in the models directory"""
        try:
            if not self.models_directory.exists():
                return []

            model_files = list(self.models_directory.glob("*.json"))
            logger.info(f"✅ Found {len(model_files)} model files")
            return model_files

        except Exception as e:
            logger.error(f"❌ Failed to list model files: {e}")
            return []

    def validate_model_file(self, file_path: str) -> bool:
        """Validate that a model file is properly formatted"""
        try:
            with open(file_path, "r") as f:
                model_dict = json.load(f)

            return self._validate_model_dict(model_dict)

        except Exception as e:
            logger.error(f"❌ Model file validation failed for {file_path}: {e}")
            return False

    def _model_to_dict(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert model data to dictionary format for saving"""
        # This is a simplified conversion - in practice, you'd handle more complex types
        return model_data.copy()

    def _validate_model_dict(self, model_dict: Dict[str, Any]) -> bool:
        """Validate that a model dictionary has the required structure"""
        required_keys = ["name", "type"]

        # Check top-level structure
        if not all(key in model_dict for key in required_keys):
            logger.error(f"Missing required keys: {required_keys}")
            return False

        # Check if it's a module or class
        if model_dict["type"] == "module":
            if "classes" not in model_dict and "functions" not in model_dict:
                logger.error("Module must contain classes or functions")
                return False

        return True

    def get_models_directory(self) -> Path:
        """Get the models directory path"""
        return self.models_directory

    def set_models_directory(self, path: str) -> bool:
        """Set a new models directory path"""
        try:
            new_path = Path(path)
            if new_path.exists() and not new_path.is_dir():
                raise ValueError(f"Path exists but is not a directory: {path}")

            self.models_directory = new_path
            logger.info(f"✅ Models directory set to: {self.models_directory}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to set models directory: {e}")
            return False
