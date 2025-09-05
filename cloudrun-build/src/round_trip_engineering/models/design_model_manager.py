#!/usr/bin/env python3
"""
Design Model Manager
Manages design models (creation, loading, saving, validation)
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from .model_persistence import ModelPersistence
from .component_manager import ComponentManager


logger = logging.getLogger(__name__)


@dataclass
class ModelComponent:
    """A component in our design model"""

    name: str
    type: str  # 'function', 'class', 'module', 'domain'
    description: str
    requirements: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DesignModel:
    """A complete design model that can be converted to/from code"""

    name: str
    description: str
    components: List[ModelComponent] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DesignModelManager(BaseReflectiveModule):
    """Manages design models (creation, loading, saving, validation)"""

    def __init__(self) -> None:
        super().__init__()
        self.design_models: Dict[str, DesignModel] = {}
        self.persistence = ModelPersistence()
        self.component_manager = ComponentManager()

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "model_management": [
                "create_model_from_design",
                "load_model",
                "save_model",
                "validate_model",
            ],
            "component_processing": [
                "add_component",
                "remove_component",
                "update_component",
            ],
        }

    def create_model_from_design(self, design_spec: Dict[str, Any]) -> DesignModel:
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

        self.design_models[design_model.name] = design_model
        logger.info(f"✅ Created model with {len(components)} components")

        return design_model

    def add_component(self, model_name: str, component: ModelComponent) -> bool:
        """Add a component to an existing model"""
        if model_name not in self.design_models:
            logger.error(f"Model {model_name} not found")
            return False

        model = self.design_models[model_name]
        return self.component_manager.add_component(model.components, component)

    def remove_component(self, model_name: str, component_name: str) -> bool:
        """Remove a component from an existing model"""
        if model_name not in self.design_models:
            logger.error(f"Model {model_name} not found")
            return False

        model = self.design_models[model_name]
        return self.component_manager.remove_component(model.components, component_name)

    def update_component(self, model_name: str, component_name: str, updates: Dict[str, Any]) -> bool:
        """Update a component in an existing model"""
        if model_name not in self.design_models:
            logger.error(f"Model {model_name} not found")
            return False

        model = self.design_models[model_name]
        return self.component_manager.update_component(model.components, component_name, updates)

    def get_model(self, model_name: str) -> Optional[DesignModel]:
        """Get a design model by name"""
        return self.design_models.get(model_name)

    def list_models(self) -> List[str]:
        """List all available model names"""
        return list(self.design_models.keys())

    def save_model(self, model_name: str, file_path: Optional[str] = None) -> bool:
        """Save a design model to file"""
        if model_name not in self.design_models:
            logger.error(f"Model {model_name} not found")
            return False

        model = self.design_models[model_name]

        # Convert model to dictionary
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

        return self.persistence.save_model(model_dict, model_name, file_path)

    def load_model(self, file_path: str) -> Optional[DesignModel]:
        """Load a design model from file"""
        model_dict = self.persistence.load_model(file_path)
        if not model_dict:
            return None

        try:
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

            self.design_models[model.name] = model
            logger.info(f"✅ Loaded model {model.name} from {file_path}")
            return model

        except Exception as e:
            logger.error(f"❌ Failed to reconstruct model from {file_path}: {e}")
            return None
