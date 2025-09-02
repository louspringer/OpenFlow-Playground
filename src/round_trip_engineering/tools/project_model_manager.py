#!/usr/bin/env python3
"""
Project Model Manager Reflective Module
Specialized manager for project_model_registry.json operations.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from .interface import IModelCrud
from .model_schemas import ProjectModel, DomainInfo, CategoryInfo


class ProjectModelManager(BaseReflectiveModule, IModelCrud):
    """Project Model Manager for project_model_registry.json operations."""

    def __init__(
        self,
        model_file: str = "project_model_registry.json",
        backup_dir: str = "backups",
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.model_file = Path(model_file)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

        # RM Compliance: Track operational metrics
        self._operation_count = 0
        self._error_count = 0
        self._last_operation_time = None

        # Project model specific validation
        self._required_sections = ["domains", "requirements_traceability", "backlog"]

        self.logger.info(f"✅ ProjectModelManager initialized for {self.model_file}")

    async def get_module_capabilities(self) -> List[Any]:
        """Return module capabilities."""
        try:
            from src.reflective_modules.health import ModuleCapability
        except ImportError:
            return [
                {
                    "name": "project_model_crud",
                    "description": "Project model registry CRUD operations",
                    "available": True,
                    "methods": ["add_item", "update_section", "remove_item"],
                },
                {
                    "name": "project_model_validation",
                    "description": "Project model schema validation",
                    "available": True,
                    "methods": ["validate", "validate_schema"],
                },
                {
                    "name": "project_model_backup",
                    "description": "Project model backup and restore",
                    "available": True,
                    "methods": ["create_backup", "restore_backup", "list_backups"],
                },
            ]

        return [
            ModuleCapability(
                name="project_model_crud",
                description="Project model registry CRUD operations",
                available=True,
                version="1.0.0",
                dependencies=["json", "pathlib"],
            ),
            ModuleCapability(
                name="project_model_validation",
                description="Project model schema validation",
                available=True,
                version="1.0.0",
                dependencies=["json"],
            ),
            ModuleCapability(
                name="project_model_backup",
                description="Project model backup and restore",
                available=True,
                version="1.0.0",
                dependencies=["json", "pathlib"],
            ),
        ]

    def add_item(
        self,
        item_id: str,
        description: str,
        title: Optional[str] = None,
        priority: str = "medium",
        collection: str = "backlog",
        **kwargs,
    ) -> bool:
        """Add a new item to project model registry."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Handle different collection types
            if collection == "domains":
                # Domains is a dict, add as new domain
                if collection not in model_data:
                    model_data[collection] = {}

                # Create domain info using schema defaults
                domain_data = {
                    "patterns": kwargs.get("patterns", [f"src/{item_id}/*.py"]),
                    "content_indicators": kwargs.get("content_indicators", [item_id]),
                    "linter": kwargs.get("linter", "flake8"),
                    "validator": kwargs.get("validator", "pytest"),
                    "formatter": kwargs.get("formatter", "black"),
                    "requirements": kwargs.get("requirements", [description]),
                    "tools": kwargs.get("tools", []),
                    "capabilities": kwargs.get("capabilities", []),
                    "workflows": kwargs.get("workflows", {}),
                    "tool_rules": kwargs.get("tool_rules", {}),
                    "exclusions": kwargs.get("exclusions", ["*.pyc", "__pycache__"]),
                    "description": description,
                }

                # Validate domain data against schema
                try:
                    domain_info = DomainInfo(**domain_data)
                    model_data[collection][item_id] = domain_info.model_dump()
                    self.logger.info(f"✅ Domain '{item_id}' created with schema validation")
                except Exception as e:
                    self.logger.warning(f"⚠️ Domain schema validation failed, using raw data: {e}")
                    model_data[collection][item_id] = domain_data

            elif collection in ["backlog", "requirements_traceability"]:
                # These are lists
                if collection not in model_data:
                    model_data[collection] = []

                if collection == "backlog":
                    new_item = {
                        "id": item_id,
                        "title": title or item_id,
                        "description": description,
                        "priority": priority,
                        "status": "pending",
                        "created_at": int(time.time()),
                        **kwargs,
                    }
                else:  # requirements_traceability
                    new_item = {
                        "requirement": description,
                        "domain": kwargs.get("domain", "general"),
                        "implementation": kwargs.get("implementation", ""),
                        "test": kwargs.get("test", ""),
                        **kwargs,
                    }
                model_data[collection].append(new_item)

            else:
                # Default: treat as list
                if collection not in model_data:
                    model_data[collection] = []

                new_item = {
                    "id": item_id,
                    "description": description,
                    "title": title,
                    "priority": priority,
                    "created_at": int(time.time()),
                    **kwargs,
                }
                model_data[collection].append(new_item)

            # Validate
            self.validate()

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Item added to {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add item: {e}")
            raise

    def update_section(self, section_name: str, updates: Dict[str, Any]) -> bool:
        """Update a section in project model registry."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Update section
            if section_name not in model_data:
                model_data[section_name] = {}
            model_data[section_name].update(updates)

            # Validate
            self.validate()

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Section updated: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to update section: {e}")
            raise

    def remove_item(self, item_id: str, collection: str = "backlog") -> bool:
        """Remove an item from project model registry."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Find and remove item
            if collection in model_data:
                if collection == "requirements_traceability":
                    # Remove by requirement description
                    model_data[collection] = [item for item in model_data[collection] if item.get("requirement") != item_id]
                else:
                    # Remove by id
                    model_data[collection] = [item for item in model_data[collection] if item.get("id") != item_id]

            # Validate
            self.validate()

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Item removed from {collection}: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove item: {e}")
            raise

    def add_section(self, section_name: str, section_config: Dict[str, Any]) -> bool:
        """Add a new section to project model registry."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Add new section
            model_data[section_name] = section_config

            # Validate
            self.validate()

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Section added: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add section: {e}")
            raise

    def remove_section(self, section_name: str) -> bool:
        """Remove a section from project model registry."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Remove section
            if section_name in model_data:
                del model_data[section_name]

            # Validate
            self.validate()

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Section removed: {section_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove section: {e}")
            raise

    def create_backup(self) -> str:
        """Create a backup of the project model registry."""
        try:
            timestamp = int(time.time())
            backup_file = self.backup_dir / f"project_model_registry_backup_{timestamp}.json"

            if self.model_file.exists():
                with open(self.model_file, "r") as f:
                    content = f.read()

                with open(backup_file, "w") as f:
                    f.write(content)

                self._track_success()
                self.logger.info(f"✅ Backup created: {backup_file}")
                return str(backup_file)
            else:
                raise FileNotFoundError(f"Project model file not found: {self.model_file}")

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Backup creation failed: {e}")
            raise

    def list_backups(self) -> List[str]:
        """List available project model backups."""
        try:
            backup_files = list(self.backup_dir.glob("project_model_registry_backup_*.json"))
            return sorted([str(f) for f in backup_files])

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to list backups: {e}")
            raise

    def restore_backup(self, backup_file: str) -> bool:
        """Restore from a project model backup."""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_file}")

            with open(backup_path, "r") as f:
                content = f.read()

            # Validate backup content
            json.loads(content)  # Ensure it's valid JSON

            # Restore
            with open(self.model_file, "w") as f:
                f.write(content)

            self._track_success()
            self.logger.info(f"✅ Backup restored: {backup_file}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Backup restore failed: {e}")
            raise

    def validate(self) -> bool:
        """Validate the project model registry structure using Pydantic schemas."""
        try:
            if not self.model_file.exists():
                raise FileNotFoundError(f"Project model file not found: {self.model_file}")

            with open(self.model_file, "r") as f:
                content = f.read()

            model_data = json.loads(content)

            # Validate using Pydantic schema
            try:
                project_model = ProjectModel(**model_data)
                self.logger.info("✅ Project model schema validation passed")
            except Exception as schema_error:
                self.logger.error(f"❌ Schema validation failed: {schema_error}")
                # Fall back to basic validation for backward compatibility
                self._basic_validation(model_data)

            # Check required sections
            for section in self._required_sections:
                if section not in model_data:
                    self.logger.warning(f"⚠️ Missing required section: {section}")

            self._track_success()
            self.logger.info("✅ Project model validation passed")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Project model validation failed: {e}")
            raise

    def _basic_validation(self, model_data: Dict[str, Any]) -> None:
        """Basic validation fallback for backward compatibility."""
        if not isinstance(model_data, dict):
            raise ValueError("Project model must be a JSON object")

        # Validate domains structure if present
        if "domains" in model_data and isinstance(model_data["domains"], dict):
            for domain_name, domain_info in model_data["domains"].items():
                if not isinstance(domain_info, dict):
                    raise ValueError(f"Domain '{domain_name}' must be a dictionary")

                # Validate domain info structure
                try:
                    DomainInfo(**domain_info)
                except Exception as e:
                    self.logger.warning(f"⚠️ Domain '{domain_name}' schema validation failed: {e}")

        # Validate domain_architecture structure if present
        if "domain_architecture" in model_data and isinstance(model_data["domain_architecture"], dict):
            for category_name, category_info in model_data["domain_architecture"].items():
                if not isinstance(category_info, dict):
                    raise ValueError(f"Category '{category_name}' must be a dictionary")

                # Validate category info structure
                try:
                    CategoryInfo(**category_info)
                except Exception as e:
                    self.logger.warning(f"⚠️ Category '{category_name}' schema validation failed: {e}")

    def load_model(self) -> Dict[str, Any]:
        """Load the current project model registry."""
        try:
            if not self.model_file.exists():
                raise FileNotFoundError(f"Project model file not found: {self.model_file}")

            with open(self.model_file, "r") as f:
                content = f.read()

            model_data = json.loads(content)
            self._track_success()
            self.logger.info("✅ Project model loaded successfully")
            return model_data

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Project model loading failed: {e}")
            raise

    def get_project_stats(self) -> Dict[str, Any]:
        """Get project model statistics."""
        try:
            model_data = self.load_model()

            stats = {
                "total_domains": len(model_data.get("domains", {})),
                "total_requirements": len(model_data.get("requirements_traceability", [])),
                "total_backlog_items": len(model_data.get("backlog", [])),
                "pending_backlog_items": len([item for item in model_data.get("backlog", []) if item.get("status") == "pending"]),
                "high_priority_items": len([item for item in model_data.get("backlog", []) if item.get("priority") == "high"]),
            }

            return stats

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to get project stats: {e}")
            raise
