"""
Model Manager Module

This module handles model creation, storage, loading, and management operations.
It provides a clean interface for model CRUD operations.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages model operations and persistence."""

    def __init__(self):
        """Initialize the model manager."""
        self.design_models: Dict[str, Any] = {}
        logger.info("✅ Model manager initialized")

    def create_model_from_design(self, design_spec: Dict[str, Any]) -> Any:
        """
        Create a model from design specification.

        Args:
            design_spec: Design specification dictionary

        Returns:
            Created model object
        """
        try:
            # Create a simple model representation
            model = {
                "name": design_spec.get("name", "Unknown Model"),
                "description": design_spec.get("description", ""),
                "components": design_spec.get("components", []),
                "relationships": design_spec.get("relationships", {}),
                "metadata": design_spec.get("metadata", {}),
                "created_at": datetime.now().isoformat(),
                "model_id": f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            }

            # Store the model
            self.design_models[model["name"]] = model

            logger.info(f"✅ Created model: {model['name']} with {len(model['components'])} components")
            return model

        except Exception as e:
            logger.error(f"❌ Failed to create model from design: {e}")
            raise

    def save_model(self, model_name: str, file_path: str) -> None:
        """
        Save a model to file.

        Args:
            model_name: Name of the model to save
            file_path: Path to save the model
        """
        try:
            model = self.design_models.get(model_name)
            if not model:
                raise ValueError(f"Model {model_name} not found")

            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            # Save to JSON
            with open(file_path, "w") as f:
                json.dump(model, f, indent=2)

            logger.info(f"✅ Saved model {model_name} to {file_path}")

        except Exception as e:
            logger.error(f"❌ Failed to save model {model_name}: {e}")
            raise

    def load_model(self, file_path: str) -> Any:
        """
        Load a model from file.

        Args:
            file_path: Path to the model file

        Returns:
            Loaded model object
        """
        try:
            with open(file_path, "r") as f:
                model_data = json.load(f)

            # Reconstruct model
            model = {
                "name": model_data["name"],
                "description": model_data["description"],
                "components": model_data.get("components", []),
                "relationships": model_data.get("relationships", {}),
                "metadata": model_data.get("metadata", {}),
                "created_at": model_data.get("created_at", ""),
                "model_id": model_data.get("model_id", "unknown"),
            }

            # Store in memory
            self.design_models[model["name"]] = model

            logger.info(f"✅ Loaded model {model['name']} with {len(model['components'])} components")
            return model

        except Exception as e:
            logger.error(f"❌ Failed to load model from {file_path}: {e}")
            raise

    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Get a model by name.

        Args:
            model_name: Name of the model

        Returns:
            Model object or None if not found
        """
        return self.design_models.get(model_name)

    def list_models(self) -> List[str]:
        """
        List all available models.

        Returns:
            List of model names
        """
        return list(self.design_models.keys())

    def delete_model(self, model_name: str) -> bool:
        """
        Delete a model.

        Args:
            model_name: Name of the model to delete

        Returns:
            True if deleted, False if not found
        """
        if model_name in self.design_models:
            del self.design_models[model_name]
            logger.info(f"✅ Deleted model: {model_name}")
            return True
        else:
            logger.warning(f"⚠️ Model {model_name} not found for deletion")
            return False
