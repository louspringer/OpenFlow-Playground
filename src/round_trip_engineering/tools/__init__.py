"""
Tools for Round-Trip Engineering
Project Singleton Registry for Model CRUD Operations
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .interface import IModelCrud

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Project singleton registry for model instances with self-bootstrapping."""

    _instance = None
    _models: Dict[str, Dict[str, Any]] = {}
    _registry_file: Path = Path("model_registry.json")
    _initialized = False

    def __new__(cls):
        """Singleton pattern - ensure only one instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the singleton registry."""
        if not self._initialized:
            self._bootstrap_registry()
            self._initialized = True

    def _bootstrap_registry(self) -> None:
        """Bootstrap the registry - manage its own model directly."""
        logger.info("🚀 Bootstrapping Model Registry...")

        # Create registry directory if it doesn't exist
        self._registry_file.parent.mkdir(exist_ok=True)

        if not self._registry_file.exists():
            logger.info("📝 Creating default registry configuration")
            self._create_default_registry()
        else:
            logger.info(f"📖 Loading existing registry from {self._registry_file}")
            self._load_registry()

        # Ensure the registry has at least one model manager for itself
        if "registry_manager" not in self._models:
            logger.info("🔧 Adding registry manager for self-management")
            self._add_registry_manager()

    def _create_default_registry(self) -> None:
        """Create default registry with essential models."""
        default_registry = {
            "models": {
                "project": {
                    "implementation": "project_model_manager",
                    "config": {
                        "model_file": "project_model_registry.json",
                        "backup_dir": "backups",
                    },
                },
                "registry_manager": {
                    "implementation": "json_model_manager",
                    "config": {
                        "model_file": "model_registry.json",
                        "backup_dir": "backups",
                    },
                },
            }
        }

        self._models = default_registry["models"]
        self._save_registry()
        logger.info("✅ Created default registry configuration")

    def _load_registry(self) -> None:
        """Load registry from file."""
        try:
            with open(self._registry_file, "r") as f:
                registry_data = json.load(f)

            if not isinstance(registry_data, dict) or "models" not in registry_data:
                raise ValueError("Invalid registry format")

            # Migrate old format to new format and ensure ALL details are preserved
            models = registry_data["models"]
            for model_name, model_info in models.items():
                # Handle old format with separate auth_config and model_config
                if "auth_config" in model_info and "model_config" in model_info:
                    # Combine auth and model config - ALL details must be preserved
                    config = {**model_info["auth_config"], **model_info["model_config"]}
                    model_info["config"] = config
                    # Remove old fields
                    model_info.pop("auth_config", None)
                    model_info.pop("model_config", None)

                # Ensure instance is None for lazy initialization (not serialized)
                model_info["instance"] = None

            self._models = models
            logger.info(f"✅ Loaded {len(self._models)} models from registry")

        except Exception as e:
            logger.error(f"❌ Failed to load registry: {e}")
            logger.info("🔄 Falling back to default registry")
            self._create_default_registry()

    def _add_registry_manager(self) -> None:
        """Add a manager for the registry's own model."""
        self._models["registry_manager"] = {
            "implementation": "json_model_manager",
            "config": {"model_file": str(self._registry_file), "backup_dir": "backups"},
            "instance": None,
        }
        self._save_registry()

    def _get_registry_manager(self) -> IModelCrud:
        """Get the manager for the registry's own model (self-bootstrapping)."""
        if "registry_manager" not in self._models:
            self._add_registry_manager()

        model_info = self._models["registry_manager"]

        # Lazy initialization
        if model_info["instance"] is None:
            implementation_name = model_info["implementation"]
            config = model_info["config"]
            model_info["instance"] = self._create_implementation(implementation_name, config)

        return model_info["instance"]

    def register_model(self, model_name: str, implementation: str, **config) -> bool:
        """Register a model with ALL necessary details for instantiation."""
        if model_name in self._models:
            raise ValueError(f"Model '{model_name}' already registered")

        # Generate default configuration based on implementation
        default_config = self._get_default_config(implementation, model_name, **config)

        # Store ALL details needed for instantiation
        self._models[model_name] = {
            "implementation": implementation,  # Right type
            "config": default_config,  # Right auth, right config, ALL details
            "instance": None,  # Lazy initialization
        }

        # Persist changes directly (registry manages its own model)
        self._save_registry()

        logger.info(f"✅ Registered model '{model_name}' with implementation '{implementation}'")
        return True

    def _get_default_config(self, implementation: str, model_name: str, **overrides) -> Dict[str, Any]:
        """Get default configuration for implementation (opaque to users)."""
        config = {}

        if implementation == "json_model_manager":
            config = {"model_file": f"{model_name}.json", "backup_dir": "backups"}
        elif implementation == "neo4j_model_manager":
            # No defaults - must be configured externally with env var references
            config = {}
        elif implementation == "ontology_model_manager":
            config = {
                "ontology_file": f"{model_name}.ttl",
                "format": "turtle",
                "namespace": f"http://example.org/{model_name}#",
            }
        elif implementation == "project_model_manager":
            config = {"model_file": f"{model_name}.json", "backup_dir": "backups"}

        # Apply any overrides
        config.update(overrides)
        return config

    def get_model(self, model_name: str) -> IModelCrud:
        """Get a model instance by name using ALL stored details."""
        if model_name not in self._models:
            raise ValueError(f"Model '{model_name}' not registered")

        model_info = self._models[model_name]

        # Lazy initialization using ALL stored details
        if model_info["instance"] is None:
            implementation_name = model_info["implementation"]  # Right type
            config = model_info["config"]  # Right auth, right config, ALL details

            # Factory method - implementation details completely hidden
            model_info["instance"] = self._create_implementation(implementation_name, config)

        return model_info["instance"]

    def _resolve_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve environment variable references in configuration."""
        import os

        resolved_config = {}

        for key, value in config.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Extract environment variable name
                env_var_name = value[2:-1]  # Remove ${ and }
                env_value = os.getenv(env_var_name)
                if env_value is None:
                    raise ValueError(f"Environment variable '{env_var_name}' not set")
                resolved_config[key] = env_value
            else:
                resolved_config[key] = value

        return resolved_config

    def _create_implementation(self, implementation_name: str, config: Dict[str, Any]) -> IModelCrud:
        """Create implementation instance with environment variable resolution."""
        try:
            # Resolve environment variables in config
            resolved_config = self._resolve_env_vars(config)

            # Implementation mapping - completely hidden from users
            implementation_map = {
                "json_model_manager": self._create_json_manager,
                "neo4j_model_manager": self._create_neo4j_manager,
                "ontology_model_manager": self._create_ontology_manager,
                "project_model_manager": self._create_project_manager,
            }

            if implementation_name not in implementation_map:
                raise ValueError(f"Unknown implementation: {implementation_name}")

            return implementation_map[implementation_name](resolved_config)

        except Exception as e:
            logger.error(f"❌ Failed to create implementation '{implementation_name}': {e}")
            raise

    def _create_json_manager(self, config: Dict[str, Any]) -> IModelCrud:
        """Create JSON manager (implementation detail)."""
        from .model_crud_manager import ModelCrudManager

        return ModelCrudManager(**config)

    def _create_neo4j_manager(self, config: Dict[str, Any]) -> IModelCrud:
        """Create Neo4j manager (implementation detail)."""
        from .neo4j_model_manager import Neo4jModelManager

        return Neo4jModelManager(**config)

    def _create_ontology_manager(self, config: Dict[str, Any]) -> IModelCrud:
        """Create Ontology manager (implementation detail)."""
        from .ontology_model_manager import OntologyModelManager

        return OntologyModelManager(**config)

    def _create_project_manager(self, config: Dict[str, Any]) -> IModelCrud:
        """Create Project manager (implementation detail)."""
        from .project_model_manager import ProjectModelManager

        return ProjectModelManager(**config)

    def list_models(self) -> List[str]:
        """List all registered model names."""
        return list(self._models.keys())

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get model information without exposing implementation details."""
        if model_name not in self._models:
            raise ValueError(f"Model '{model_name}' not registered")

        model_info = self._models[model_name].copy()
        # Hide implementation details from users
        model_info.pop("instance", None)
        model_info.pop("implementation", None)  # Don't expose implementation name
        return model_info

    def unregister_model(self, model_name: str) -> bool:
        """Unregister a model."""
        if model_name not in self._models:
            return False

        # Clean up instance if it exists
        if "instance" in self._models[model_name]:
            del self._models[model_name]["instance"]

        del self._models[model_name]

        # Persist changes directly (registry manages its own model)
        self._save_registry()

        logger.info(f"✅ Unregistered model '{model_name}'")
        return True

    def _save_registry(self) -> None:
        """Save registry to file (direct file I/O for bootstrapping)."""
        registry_data = {"models": self._models}

        # Remove instance references before saving
        for model_info in registry_data["models"].values():
            model_info.pop("instance", None)

        with open(self._registry_file, "w") as f:
            json.dump(registry_data, f, indent=2)


# Global singleton instance
_model_registry = None


def get_model_registry() -> ModelRegistry:
    """Get the global singleton registry instance."""
    global _model_registry
    if _model_registry is None:
        _model_registry = ModelRegistry()
    return _model_registry


# Export only the interface and registry accessor - no implementation details
__all__ = ["IModelCrud", "get_model_registry"]
__version__ = "2.0.0"
__author__ = "OpenFlow Playground Team"
