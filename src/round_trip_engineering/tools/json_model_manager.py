#!/usr/bin/env python3
"""
JSON Model Manager - Reflective Module for managing project model registry updates
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.round_trip_engineering.generators.base_reflective_module import (
    BaseReflectiveModule,
)

logger = logging.getLogger(__name__)


class JSONModelManager(BaseReflectiveModule):
    """Reflective Module for managing JSON model registry updates."""

    def __init__(self):
        super().__init__()
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.model_file = self.project_root / "project_model_registry.json"
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities."""
        return {
            "json_operations": [
                "add_requirement",
                "add_backlog_item",
                "update_domain",
                "validate_json",
                "create_backup",
                "restore_backup",
            ],
            "supported_files": ["project_model_registry.json"],
            "backup_strategy": "timestamped_backups",
        }

    def create_backup(self) -> str:
        """Create a timestamped backup of the model registry."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"project_model_registry_{timestamp}.json"

            with open(self.model_file, "r") as f:
                content = f.read()

            with open(backup_file, "w") as f:
                f.write(content)

            logger.info(f"✅ Backup created: {backup_file}")
            return str(backup_file)

        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            raise

    def load_model(self) -> Dict[str, Any]:
        """Load the current model registry."""
        try:
            with open(self.model_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise

    def save_model(self, model: Dict[str, Any]) -> None:
        """Save the updated model registry."""
        try:
            with open(self.model_file, "w") as f:
                json.dump(model, f, indent=2)
            logger.info("✅ Model saved successfully")
        except Exception as e:
            logger.error(f"❌ Failed to save model: {e}")
            raise

    def validate_json(self, model: Dict[str, Any]) -> bool:
        """Validate JSON structure."""
        try:
            # Basic validation - ensure it's a dict and can be serialized
            json.dumps(model)
            return True
        except Exception as e:
            logger.error(f"❌ JSON validation failed: {e}")
            return False

    def add_requirement(self, domain: str, requirement: str) -> bool:
        """Add a requirement to a domain."""
        try:
            # Create backup first
            self.create_backup()

            # Load current model
            model = self.load_model()

            # Add requirement to domain
            if domain in model.get("domains", {}):
                if "requirements" not in model["domains"][domain]:
                    model["domains"][domain]["requirements"] = []

                model["domains"][domain]["requirements"].append(requirement)

                # Validate and save
                if self.validate_json(model):
                    self.save_model(model)
                    logger.info(f"✅ Requirement added to {domain}: {requirement}")
                    return True
                else:
                    logger.error("❌ JSON validation failed after update")
                    return False
            else:
                logger.error(f"❌ Domain {domain} not found")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to add requirement: {e}")
            return False

    def add_backlog_item(self, item: Dict[str, Any]) -> bool:
        """Add a backlog item."""
        try:
            # Create backup first
            self.create_backup()

            # Load current model
            model = self.load_model()

            # Ensure backlog array exists
            if "backlog" not in model:
                model["backlog"] = []

            # Add backlog item
            model["backlog"].append(item)

            # Validate and save
            if self.validate_json(model):
                self.save_model(model)
                logger.info(f"✅ Backlog item added: {item.get('title', 'Unknown')}")
                return True
            else:
                logger.error("❌ JSON validation failed after update")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to add backlog item: {e}")
            return False

    def update_domain(self, domain: str, updates: Dict[str, Any]) -> bool:
        """Update a domain with new information."""
        try:
            # Create backup first
            self.create_backup()

            # Load current model
            model = self.load_model()

            # Update domain
            if domain in model.get("domains", {}):
                model["domains"][domain].update(updates)

                # Validate and save
                if self.validate_json(model):
                    self.save_model(model)
                    logger.info(f"✅ Domain {domain} updated successfully")
                    return True
                else:
                    logger.error("❌ JSON validation failed after update")
                    return False
            else:
                logger.error(f"❌ Domain {domain} not found")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to update domain: {e}")
            return False


def main():
    """CLI interface for JSON Model Manager."""
    import argparse

    parser = argparse.ArgumentParser(description="JSON Model Manager CLI")
    parser.add_argument(
        "--add-requirement",
        nargs=2,
        metavar=("DOMAIN", "REQUIREMENT"),
        help="Add requirement to domain",
    )
    parser.add_argument(
        "--add-backlog",
        nargs=2,
        metavar=("TITLE", "DESCRIPTION"),
        help="Add backlog item",
    )
    parser.add_argument("--backup", action="store_true", help="Create backup")

    args = parser.parse_args()

    manager = JSONModelManager()

    if args.backup:
        backup_file = manager.create_backup()
        print(f"Backup created: {backup_file}")

    if args.add_requirement:
        domain, requirement = args.add_requirement
        success = manager.add_requirement(domain, requirement)
        print(f"Requirement addition: {'✅ Success' if success else '❌ Failed'}")

    if args.add_backlog:
        title, description = args.add_backlog
        backlog_item = {
            "id": f"backlog_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "description": description,
            "priority": "medium",
            "status": "pending",
            "created_at": datetime.now().isoformat() + "Z",
            "updated_at": datetime.now().isoformat() + "Z",
        }
        success = manager.add_backlog_item(backlog_item)
        print(f"Backlog addition: {'✅ Success' if success else '❌ Failed'}")


if __name__ == "__main__":
    main()
