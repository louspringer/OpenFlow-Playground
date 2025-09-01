#!/usr/bin/env python3
"""
Tests for JSON Model Manager
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.round_trip_engineering.tools.project_model_manager import ProjectModelManager as JSONModelManager


class TestJSONModelManager:
    """Test JSON Model Manager functionality."""

    @pytest.fixture
    def temp_manager(self):
        """Create a temporary manager for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary project structure
            temp_project = Path(temp_dir) / "test_project"
            temp_project.mkdir()

            # Create a temporary model file
            model_file = temp_project / "project_model_registry.json"
            test_model = {
                "domains": {"test_domain": {"requirements": ["existing requirement"]}},
                "backlog": [],
            }

            with open(model_file, "w") as f:
                json.dump(test_model, f)

            # Mock the project root
            with patch.object(JSONModelManager, "__init__", return_value=None):
                manager = JSONModelManager()
                manager.project_root = temp_project
                manager.model_file = model_file
                manager.backup_dir = temp_project / "backups"
                manager.backup_dir.mkdir(exist_ok=True)
                yield manager

    def test_module_capabilities(self, temp_manager):
        """Test that module capabilities are properly defined."""
        capabilities = temp_manager.get_module_capabilities()

        assert "json_operations" in capabilities
        assert "supported_files" in capabilities
        assert "backup_strategy" in capabilities

        expected_operations = [
            "add_requirement",
            "add_backlog_item",
            "update_domain",
            "validate_json",
            "create_backup",
            "restore_backup",
        ]

        for operation in expected_operations:
            assert operation in capabilities["json_operations"]

    def test_create_backup(self, temp_manager):
        """Test backup creation."""
        backup_file = temp_manager.create_backup()

        assert Path(backup_file).exists()
        assert "project_model_registry_" in backup_file
        assert backup_file.endswith(".json")

    def test_load_model(self, temp_manager):
        """Test model loading."""
        model = temp_manager.load_model()

        assert "domains" in model
        assert "test_domain" in model["domains"]
        assert "existing requirement" in model["domains"]["test_domain"]["requirements"]

    def test_validate_json(self, temp_manager):
        """Test JSON validation."""
        valid_model = {"test": "data"}
        invalid_model = {"test": temp_manager}  # Contains non-serializable object

        assert temp_manager.validate_json(valid_model) is True
        assert temp_manager.validate_json(invalid_model) is False

    def test_add_requirement(self, temp_manager):
        """Test adding a requirement to a domain."""
        success = temp_manager.add_requirement("test_domain", "new requirement")

        assert success is True

        # Verify the requirement was added
        model = temp_manager.load_model()
        requirements = model["domains"]["test_domain"]["requirements"]
        assert "new requirement" in requirements
        assert len(requirements) == 2  # existing + new

    def test_add_requirement_nonexistent_domain(self, temp_manager):
        """Test adding a requirement to a non-existent domain."""
        success = temp_manager.add_requirement("nonexistent_domain", "new requirement")

        assert success is False

    def test_add_backlog_item(self, temp_manager):
        """Test adding a backlog item."""
        backlog_item = {
            "id": "test_item",
            "title": "Test Item",
            "description": "Test description",
            "priority": "medium",
            "status": "pending",
        }

        success = temp_manager.add_backlog_item(backlog_item)

        assert success is True

        # Verify the backlog item was added
        model = temp_manager.load_model()
        assert len(model["backlog"]) == 1
        assert model["backlog"][0]["title"] == "Test Item"

    def test_update_domain(self, temp_manager):
        """Test updating a domain."""
        updates = {"new_field": "new_value", "requirements": ["updated requirement"]}

        success = temp_manager.update_domain("test_domain", updates)

        assert success is True

        # Verify the domain was updated
        model = temp_manager.load_model()
        domain = model["domains"]["test_domain"]
        assert domain["new_field"] == "new_value"
        assert domain["requirements"] == ["updated requirement"]

    def test_update_nonexistent_domain(self, temp_manager):
        """Test updating a non-existent domain."""
        updates = {"new_field": "new_value"}

        success = temp_manager.update_domain("nonexistent_domain", updates)

        assert success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
