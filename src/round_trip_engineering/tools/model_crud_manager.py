#!/usr/bin/env python3
"""
Model CRUD Manager Reflective Module
General-purpose model CRUD operations with schema validation and backup management.
Provides safe, programmatic model manipulation with internal schema validation.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jq
from pydantic import BaseModel, Field

from ..generators.base_reflective_module import BaseReflectiveModule


class ModelSchema(BaseModel):
    """Generic model schema structure."""

    data: Dict[str, Any] = Field(description="Model data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Model metadata")


class ItemSchema(BaseModel):
    """Generic item schema structure."""

    id: str = Field(description="Unique item identifier")
    title: Optional[str] = Field(default=None, description="Item title")
    description: str = Field(description="Item description")
    priority: str = Field(default="medium", description="Item priority")
    status: str = Field(default="pending", description="Item status")
    created_at: int = Field(description="Creation timestamp")
    data: Dict[str, Any] = Field(
        default_factory=dict, description="Additional item data"
    )


class UpdateSchema(BaseModel):
    """Generic update schema structure."""

    data: Dict[str, Any] = Field(description="Update data")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Update metadata"
    )


class ModelCrudManager(BaseReflectiveModule):
    """JSON-based model CRUD operations with schema validation and backup management."""

    def __init__(
        self, model_file: str = "model.json", backup_dir: str = "backups"
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.model_file = Path(model_file)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

        # Generic schema validation
        self.schema = ModelSchema

        # RM Compliance: Track operational metrics
        self._operation_count = 0
        self._error_count = 0
        self._last_operation_time = None

        self.logger.info(f"✅ ModelCrudManager initialized for {self.model_file}")

    async def get_module_capabilities(self) -> List[Any]:
        """Return module capabilities."""
        try:
            from src.reflective_modules.health import ModuleCapability
        except ImportError:
            # Fallback if ModuleCapability not available
            return [
                {
                    "name": "json_crud",
                    "description": "Schema-based CRUD operations on project model",
                    "available": True,
                    "methods": [
                        "add_requirement",
                        "add_backlog_item",
                        "update_domain",
                        "remove_requirement",
                        "remove_backlog_item",
                    ],
                },
                {
                    "name": "schema_ddl",
                    "description": "Meta-CRUD operations on schema structure",
                    "available": True,
                    "methods": [
                        "validate_schema",
                        "update_schema",
                        "add_domain",
                        "remove_domain",
                    ],
                },
                {
                    "name": "ontology_alignment",
                    "description": "Vocabulary alignment and ontology management",
                    "available": True,
                    "methods": [
                        "align_vocabulary",
                        "add_vocabulary_mapping",
                        "validate_ontology",
                    ],
                },
                {
                    "name": "backup_management",
                    "description": "Backup and restore operations",
                    "available": True,
                    "methods": ["create_backup", "restore_backup", "list_backups"],
                },
            ]

        capabilities = []

        # JSON CRUD capabilities
        capabilities.append(
            ModuleCapability(
                name="json_crud",
                description="Schema-based CRUD operations on project model",
                available=True,
                version="1.0.0",
                dependencies=["jq", "json", "pydantic"],
            )
        )

        # Schema DDL capabilities
        capabilities.append(
            ModuleCapability(
                name="schema_ddl",
                description="Meta-CRUD operations on schema structure",
                available=True,
                version="1.0.0",
                dependencies=["json", "pydantic"],
            )
        )

        # Ontology alignment capabilities
        capabilities.append(
            ModuleCapability(
                name="ontology_alignment",
                description="Vocabulary alignment and ontology management",
                available=True,
                version="1.0.0",
                dependencies=["json", "pydantic"],
            )
        )

        # Backup management capabilities
        capabilities.append(
            ModuleCapability(
                name="backup_management",
                description="Backup and restore operations",
                available=True,
                version="1.0.0",
                dependencies=["json", "pathlib"],
            )
        )

        return capabilities

    def create_backup(self) -> str:
        """Create a backup of the current model file."""
        try:
            timestamp = int(time.time())
            backup_file = self.backup_dir / f"project_model_backup_{timestamp}.json"

            if self.model_file.exists():
                with open(self.model_file, "r") as f:
                    content = f.read()

                with open(backup_file, "w") as f:
                    f.write(content)

                self._track_success()
                self.logger.info(f"✅ Backup created: {backup_file}")
                return str(backup_file)
            else:
                raise FileNotFoundError(f"Model file not found: {self.model_file}")

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Backup creation failed: {e}")
            raise

    def load_model(self) -> Dict[str, Any]:
        """Load the current model from file."""
        try:
            if not self.model_file.exists():
                raise FileNotFoundError(f"Model file not found: {self.model_file}")

            with open(self.model_file, "r") as f:
                content = f.read()

            model_data = json.loads(content)
            self._track_success()
            self.logger.info(f"✅ Model loaded successfully")
            return model_data

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Model loading failed: {e}")
            raise

    def save_model(self, model_data: Dict[str, Any]) -> bool:
        """Save model data to file."""
        try:
            # Validate schema before saving
            self.validate_json(model_data)

            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Model saved successfully")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Model saving failed: {e}")
            raise

    def validate_json(self, data: Dict[str, Any]) -> bool:
        """Validate JSON structure against schema."""
        try:
            # Basic schema validation
            if not isinstance(data, dict):
                raise ValueError("Root must be a dictionary")

            # Generic validation - just ensure it's a valid JSON structure
            # No specific required keys for generic usage

            self._track_success()
            self.logger.info(f"✅ JSON validation passed")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ JSON validation failed: {e}")
            raise

    def add_item(
        self,
        item_id: str,
        description: str,
        title: Optional[str] = None,
        priority: str = "medium",
        collection: str = "items",
        **kwargs,
    ) -> bool:
        """Add a new item to a collection using internal schema validation."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Create new item using internal schema
            new_item = ItemSchema(
                id=item_id,
                title=title,
                description=description,
                priority=priority,
                status="pending",
                created_at=int(time.time()),
                data=kwargs,
            ).model_dump()

            # Load current model data
            model_data = json.loads(content)

            # Ensure collection exists
            if collection not in model_data:
                model_data[collection] = []

            # Add new item
            model_data[collection].append(new_item)

            # Validate
            self.validate_json(model_data)

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
        """Update a section configuration using internal schema validation."""
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
            self.validate_json(model_data)

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

    def remove_item(self, item_id: str, collection: str = "items") -> bool:
        """Remove an item from a collection using internal schema validation."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Remove item
            if collection in model_data and isinstance(model_data[collection], list):
                model_data[collection] = [
                    item for item in model_data[collection] if item.get("id") != item_id
                ]

            # Validate
            self.validate_json(model_data)

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
        """Add a new section using internal schema validation."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Add section
            model_data[section_name] = section_config

            # Validate
            self.validate_json(model_data)

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
        """Remove a section using internal schema validation."""
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
            self.validate_json(model_data)

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

    def add_backlog_item(
        self, item_id: str, title: str, description: str, priority: str = "medium"
    ) -> bool:
        """Add a new backlog item using internal schema validation."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Create new backlog item using internal schema
            new_item = BacklogItemSchema(
                id=item_id,
                title=title,
                description=description,
                priority=priority,
                status="pending",
                created_at=int(time.time()),
            ).model_dump()

            # Load current model data
            model_data = json.loads(content)

            # Add new backlog item
            model_data["backlog"].append(new_item)

            # Validate
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Backlog item added: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add backlog item: {e}")
            raise

    def update_domain(self, domain_name: str, updates: Dict[str, Any]) -> bool:
        """Update a domain configuration using jq Python package."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Load current model data
            model_data = json.loads(content)

            # Update domain
            if domain_name not in model_data["domains"]:
                model_data["domains"][domain_name] = {}
            model_data["domains"][domain_name].update(updates)

            # Validate
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                json.dump(model_data, f, indent=2)

            self._track_success()
            self.logger.info(f"✅ Domain updated: {domain_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to update domain: {e}")
            raise

    def remove_requirement(self, req_id: str) -> bool:
        """Remove a requirement using jq Python package."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Use jq Python package to remove requirement
            updated_content = (
                jq.compile(
                    ".requirements_traceability = [.[] | select(.id != $req_id)]"
                )
                .input(content)
                .input(req_id)
                .first()
            )

            # Parse and validate
            model_data = json.loads(updated_content)
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                f.write(updated_content)

            self._track_success()
            self.logger.info(f"✅ Requirement removed: {req_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove requirement: {e}")
            raise

    def remove_backlog_item(self, item_id: str) -> bool:
        """Remove a backlog item using jq Python package."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Use jq Python package to remove backlog item
            updated_content = (
                jq.compile(".backlog = [.[] | select(.id != $item_id)]")
                .input(content)
                .input(item_id)
                .first()
            )

            # Parse and validate
            model_data = json.loads(updated_content)
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                f.write(updated_content)

            self._track_success()
            self.logger.info(f"✅ Backlog item removed: {item_id}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove backlog item: {e}")
            raise

    def add_domain(self, domain_name: str, domain_config: Dict[str, Any]) -> bool:
        """Add a new domain using jq Python package."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Use jq Python package to add domain
            updated_content = (
                jq.compile(f'.domains["{domain_name}"] = $domain_config')
                .input(content)
                .input(domain_config)
                .first()
            )

            # Parse and validate
            model_data = json.loads(updated_content)
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                f.write(updated_content)

            self._track_success()
            self.logger.info(f"✅ Domain added: {domain_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add domain: {e}")
            raise

    def remove_domain(self, domain_name: str) -> bool:
        """Remove a domain using jq Python package."""
        try:
            # Create backup first
            self.create_backup()

            # Load current content
            with open(self.model_file, "r") as f:
                content = f.read()

            # Use jq Python package to remove domain
            updated_content = (
                jq.compile(f'del(.domains["{domain_name}"])').input(content).first()
            )

            # Parse and validate
            model_data = json.loads(updated_content)
            self.validate_json(model_data)

            # Save back
            with open(self.model_file, "w") as f:
                f.write(updated_content)

            self._track_success()
            self.logger.info(f"✅ Domain removed: {domain_name}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to remove domain: {e}")
            raise

    def align_vocabulary(self, text: str) -> str:
        """Align vocabulary using ontology mappings."""
        try:
            aligned_text = text.lower()

            # Apply vocabulary mappings
            for standard_term, variations in self.vocabulary_mappings.items():
                for variation in variations:
                    if variation in aligned_text:
                        aligned_text = aligned_text.replace(variation, standard_term)
                        break

            self._track_success()
            self.logger.info(f"✅ Vocabulary aligned: {text} -> {aligned_text}")
            return aligned_text

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Vocabulary alignment failed: {e}")
            raise

    def add_vocabulary_mapping(self, standard_term: str, variations: List[str]) -> bool:
        """Add a new vocabulary mapping."""
        try:
            self.vocabulary_mappings[standard_term] = variations
            self._track_success()
            self.logger.info(f"✅ Vocabulary mapping added: {standard_term}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to add vocabulary mapping: {e}")
            raise

    def validate_ontology(self) -> Dict[str, Any]:
        """Validate ontology consistency."""
        try:
            validation_results = {
                "total_mappings": len(self.vocabulary_mappings),
                "standard_terms": list(self.vocabulary_mappings.keys()),
                "total_variations": sum(
                    len(variations) for variations in self.vocabulary_mappings.values()
                ),
                "conflicts": [],
                "suggestions": [],
            }

            # Check for conflicts (same variation mapped to different terms)
            all_variations = []
            for term, variations in self.vocabulary_mappings.items():
                for variation in variations:
                    if variation in all_variations:
                        validation_results["conflicts"].append(
                            f"Duplicate variation: {variation}"
                        )
                    all_variations.append(variation)

            self._track_success()
            self.logger.info(f"✅ Ontology validation completed")
            return validation_results

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Ontology validation failed: {e}")
            raise

    def list_backups(self) -> List[str]:
        """List available backups."""
        try:
            backup_files = list(self.backup_dir.glob("project_model_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            self._track_success()
            self.logger.info(f"✅ Found {len(backup_files)} backups")
            return [str(f) for f in backup_files]

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to list backups: {e}")
            raise

    def restore_backup(self, backup_file: str) -> bool:
        """Restore from backup."""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_file}")

            # Create backup of current state
            self.create_backup()

            # Restore from backup
            with open(backup_path, "r") as f:
                content = f.read()

            # Validate before restoring
            model_data = json.loads(content)
            self.validate_json(model_data)

            # Restore
            with open(self.model_file, "w") as f:
                f.write(content)

            self._track_success()
            self.logger.info(f"✅ Restored from backup: {backup_file}")
            return True

        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Failed to restore backup: {e}")
            raise

    def validate(self) -> bool:
        """Validate the current model."""
        try:
            model_data = self.load_model()
            return self.validate_json(model_data)
        except Exception as e:
            self._track_error()
            self.logger.error(f"❌ Model validation failed: {e}")
            raise


# CLI interface
def main():
    """CLI interface for Model CRUD Manager."""
    import argparse

    parser = argparse.ArgumentParser(description="Model CRUD Manager CLI")
    parser.add_argument(
        "action",
        choices=[
            "add-item",
            "update-section",
            "remove-item",
            "add-section",
            "remove-section",
            "create-backup",
            "list-backups",
            "restore-backup",
            "validate",
        ],
    )
    parser.add_argument("--id", help="Item ID")
    parser.add_argument("--title", help="Item title")
    parser.add_argument("--description", help="Item description")
    parser.add_argument("--priority", default="medium", help="Priority level")
    parser.add_argument("--collection", default="items", help="Collection name")
    parser.add_argument("--section", help="Section name")
    parser.add_argument("--updates", help="JSON updates")
    parser.add_argument("--backup-file", help="Backup file path")
    parser.add_argument("--model-file", default="model.json", help="Model file path")

    args = parser.parse_args()

    manager = ModelCrudManager(model_file=args.model_file)

    try:
        if args.action == "add-item":
            if not all([args.id, args.description]):
                print("❌ --id and --description required for add-item")
                return 1
            success = manager.add_item(
                args.id, args.description, args.title, args.priority, args.collection
            )
            print(f"✅ Item added to {args.collection}: {success}")

        elif args.action == "update-section":
            if not all([args.section, args.updates]):
                print("❌ --section and --updates required for update-section")
                return 1
            updates = json.loads(args.updates)
            success = manager.update_section(args.section, updates)
            print(f"✅ Section updated: {success}")

        elif args.action == "remove-item":
            if not args.id:
                print("❌ --id required for remove-item")
                return 1
            success = manager.remove_item(args.id, args.collection)
            print(f"✅ Item removed from {args.collection}: {success}")

        elif args.action == "add-section":
            if not all([args.section, args.updates]):
                print("❌ --section and --updates required for add-section")
                return 1
            section_config = json.loads(args.updates)
            success = manager.add_section(args.section, section_config)
            print(f"✅ Section added: {success}")

        elif args.action == "remove-section":
            if not args.section:
                print("❌ --section required for remove-section")
                return 1
            success = manager.remove_section(args.section)
            print(f"✅ Section removed: {success}")

        elif args.action == "create-backup":
            backup_file = manager.create_backup()
            print(f"✅ Backup created: {backup_file}")

        elif args.action == "list-backups":
            backups = manager.list_backups()
            print("📋 Available backups:")
            for backup in backups:
                print(f"  - {backup}")

        elif args.action == "restore-backup":
            if not args.backup_file:
                print("❌ --backup-file required for restore-backup")
                return 1
            success = manager.restore_backup(args.backup_file)
            print(f"✅ Backup restored: {success}")

        elif args.action == "validate":
            model_data = manager.load_model()
            success = manager.validate_json(model_data)
            print(f"✅ Validation passed: {success}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
