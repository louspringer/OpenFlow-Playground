#!/usr/bin/env python3
"""
Model CRUD Interface
Abstract interface for model CRUD operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IModelCrud(ABC):
    """Abstract interface for model CRUD operations."""

    @abstractmethod
    def add_item(
        self,
        item_id: str,
        description: str,
        title: Optional[str] = None,
        priority: str = "medium",
        collection: str = "items",
        **kwargs,
    ) -> bool:
        """Add a new item to a collection."""
        pass

    @abstractmethod
    def update_section(self, section_name: str, updates: Dict[str, Any]) -> bool:
        """Update a section configuration."""
        pass

    @abstractmethod
    def remove_item(self, item_id: str, collection: str = "items") -> bool:
        """Remove an item from a collection."""
        pass

    @abstractmethod
    def add_section(self, section_name: str, section_config: Dict[str, Any]) -> bool:
        """Add a new section."""
        pass

    @abstractmethod
    def remove_section(self, section_name: str) -> bool:
        """Remove a section."""
        pass

    @abstractmethod
    def create_backup(self) -> str:
        """Create a backup of the current model."""
        pass

    @abstractmethod
    def list_backups(self) -> List[str]:
        """List available backups."""
        pass

    @abstractmethod
    def restore_backup(self, backup_file: str) -> bool:
        """Restore from a backup."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate the current model."""
        pass

    @abstractmethod
    def load_model(self) -> Dict[str, Any]:
        """Load the current model."""
        pass
