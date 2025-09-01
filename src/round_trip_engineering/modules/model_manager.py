#!/usr/bin/env python3
"""
Model Manager Module

Handles design models, model creation, and model operations.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


@dataclass
class ModelComponent:
    """A component in our design model"""

    name: str
    type: str  # 'function', 'class', 'module', 'domain'
    description: str
    requirements: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DesignModel:
    """A complete design model that can be converted to/from code"""

    name: str
    description: str
    components: list[ModelComponent] = field(default_factory=list)
    relationships: dict[str, list[str]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelManager:
    """Manages design models and model operations"""

    def __init__(self) -> None:
        self.design_models: dict[str, DesignModel] = {}

    def create_model_from_design(self, design_spec: dict[str, Any]) -> DesignModel:
        """Create a model directly from design specification (NO reverse engineering)"""
        logger.info(f"🎯 Creating model from design: {design_spec.get('name', 'Unknown')}")

        # Extract design components
        components = []
        for comp_spec in design_spec.get("components", []):
            component = ModelComponent(
                name=comp_spec["name"],
                type=comp_spec["type"],
                description=comp_spec["description"],
                requirements=comp_spec.get("requirements", []),
                dependencies=comp_spec.get("dependencies", []),
                metadata=comp_spec.get("metadata", {}),
            )
            components.append(component)

        # Create the design model
        design_model = DesignModel(
            name=design_spec["name"],
            description=design_spec["description"],
            components=components,
            relationships=design_spec.get("relationships", {}),
            metadata=design_spec.get("metadata", {}),
        )

        # Store the model
        self.design_models[design_model.name] = design_model
        logger.info(f"✅ Created model: {design_model.name} with {len(components)} components")

        return design_model

    def save_model(self, model_name: str, filename: str) -> None:
        """Save a model to JSON file"""
        if model_name not in self.design_models:
            raise ValueError(f"Model '{model_name}' not found")

        model = self.design_models[model_name]

        # Convert model to dict for JSON serialization
        model_dict = {
            "name": model.name,
            "description": model.description,
            "components": [
                {
                    "name": comp.name,
                    "type": comp.type,
                    "description": comp.description,
                    "requirements": comp.requirements,
                    "dependencies": comp.dependencies,
                    "metadata": comp.metadata,
                }
                for comp in model.components
            ],
            "relationships": model.relationships,
            "metadata": model.metadata,
        }

        with open(filename, "w") as f:
            json.dump(model_dict, f, indent=2)

        logger.info(f"💾 Saved model '{model_name}' to {filename}")

    def load_model(self, filename: str) -> DesignModel:
        """Load a model from JSON file"""
        with open(filename, "r") as f:
            model_dict = json.load(f)

        # Reconstruct components
        components = []
        for comp_dict in model_dict.get("components", []):
            component = ModelComponent(
                name=comp_dict["name"],
                type=comp_dict["type"],
                description=comp_dict["description"],
                requirements=comp_dict.get("requirements", []),
                dependencies=comp_dict.get("dependencies", []),
                metadata=comp_dict.get("metadata", {}),
            )
            components.append(component)

        # Create the model
        model = DesignModel(
            name=model_dict["name"],
            description=model_dict["description"],
            components=components,
            relationships=model_dict.get("relationships", {}),
            metadata=model_dict.get("metadata", {}),
        )

        # Store the model
        self.design_models[model.name] = model
        logger.info(f"📂 Loaded model '{model.name}' from {filename}")

        return model

    def get_model(self, model_name: str) -> DesignModel:
        """Get a model by name"""
        if model_name not in self.design_models:
            raise ValueError(f"Model '{model_name}' not found")
        return self.design_models[model_name]

    def list_models(self) -> list[str]:
        """List all available model names"""
        return list(self.design_models.keys())
