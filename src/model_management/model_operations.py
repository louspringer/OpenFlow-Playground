#!/usr/bin/env python3
"""
Model registry operations for model CRUD system.
Single responsibility: Model registry operations (register, unregister, list, get-info).
"""

import json
import sys
from pathlib import Path

# Add project root to path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.round_trip_engineering.tools import get_model_registry


class ModelOperations:
    """Handles model registry operations."""

    def __init__(self):
        self.registry = get_model_registry()

    def read_model_registry(self) -> str:
        """Read the project model registry and return as JSON string."""
        try:
            import json
            from pathlib import Path

            # Read the project model registry directly
            model_file = Path(__file__).parent.parent.parent / "project_model_registry.json"
            if not model_file.exists():
                return "❌ project_model_registry.json not found"

            with open(model_file, "r") as f:
                data = json.load(f)

            return json.dumps(data, indent=2)

        except Exception as e:
            return f"❌ Error reading model: {e}"

    def register_model(self, model_name: str, implementation: str, config: str = None) -> tuple[bool, str]:
        """Register a new model."""
        try:
            # Parse configuration if provided
            config_dict = {}
            if config:
                try:
                    config_dict = json.loads(config)
                except json.JSONDecodeError:
                    return False, "Invalid --config JSON"

            # Register model with config
            success = self.registry.register_model(model_name, implementation, **config_dict)
            if success:
                return True, f"✅ Model registered: {model_name} ({implementation})"
            else:
                return False, f"❌ Failed to register model: {model_name}"

        except Exception as e:
            return False, f"❌ Error registering model: {e}"

    def unregister_model(self, model_name: str) -> tuple[bool, str]:
        """Unregister a model."""
        try:
            success = self.registry.unregister_model(model_name)
            if success:
                return True, f"✅ Model unregistered: {model_name}"
            else:
                return False, f"❌ Failed to unregister model: {model_name}"

        except Exception as e:
            return False, f"❌ Error unregistering model: {e}"

    def list_models(self) -> tuple[bool, str]:
        """List all registered models."""
        try:
            models = self.registry.list_models()
            output = ["📋 Registered models:"]

            for model_name in models:
                info = self.registry.get_model_info(model_name)
                output.append(f"  - {model_name}")
                if info.get("config"):
                    output.append(f"    Config: {list(info['config'].keys())}")

            return True, "\n".join(output)

        except Exception as e:
            return False, f"❌ Error listing models: {e}"

    def get_model_info(self, model_name: str) -> tuple[bool, str]:
        """Get information about a specific model."""
        try:
            info = self.registry.get_model_info(model_name)
            output = [
                f"📋 Model info for '{model_name}':",
                f"  Implementation: {info.get('implementation', 'N/A')}",
                f"  Config: {info.get('config', {})}",
                f"  Instance: {'Initialized' if info.get('instance') else 'Lazy (not initialized)'}",
            ]
            return True, "\n".join(output)

        except Exception as e:
            return False, f"❌ Error getting model info: {e}"


def create_model_registry_operations() -> ModelOperations:
    """Factory function to create model registry operations instance."""
    return ModelOperations()
