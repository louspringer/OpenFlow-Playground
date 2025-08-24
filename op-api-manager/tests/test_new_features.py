"""
Comprehensive tests for new CLI features.

This module tests all the new use cases discovered during CLI development:
- Filtering and limiting options
- Dry-run capabilities
- Export formats
- Enhanced verbose options
- Statistics and health monitoring
- Backup and restore functionality
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from op_api_manager.cli import main
from op_api_manager.core import OnePasswordAPIKeyManager
from op_api_manager.models import CacheConfig


class TestNewCLIFeatures:
    """Test all new CLI features and use cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.cache_config = CacheConfig()

        # Mock data for testing
        self.mock_discovery_result = {
            "total_items": 10,
            "api_keys": [
                {
                    "id": "1",
                    "provider": "openai",
                    "status": "working",
                    "title": "OpenAI Key 1",
                },
                {
                    "id": "2",
                    "provider": "anthropic",
                    "status": "working",
                    "title": "Anthropic Key 1",
                },
                {
                    "id": "3",
                    "provider": "aws",
                    "status": "failed",
                    "title": "AWS Key 1",
                },
                {
                    "id": "4",
                    "provider": "azure",
                    "status": "discovered",
                    "title": "Azure Key 1",
                },
            ],
        }

        self.mock_working_credentials = {
            "openai": [
                {"title": "OpenAI Key 1", "credential": "sk-1234567890abcdef"},
                {"title": "OpenAI Key 2", "credential": "sk-fedcba0987654321"},
            ],
            "anthropic": [
                {"title": "Anthropic Key 1", "credential": "sk-ant-1234567890abcdef"}
            ],
            "aws": [{"title": "AWS Key 1", "credential": "AKIA1234567890ABCDEF"}],
        }

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_discover_with_new_options(self, mock_manager_class):
        """Test discover command with all new options."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.discover_api_keys.return_value = Mock(**self.mock_discovery_result)

        # Test with provider filter
        result = self.runner.invoke(
            main, ["discover", "--provider", "openai", "--verbose"]
        )
        assert result.exit_code == 0
        assert "OpenAI Key 1" in result.output

        # Test with limit
        result = self.runner.invoke(main, ["discover", "--limit", "2", "--verbose"])
        assert result.exit_code == 0

        # Test with force
        result = self.runner.invoke(main, ["discover", "--force", "--verbose"])
        assert result.exit_code == 0

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_discover_dry_run(self, mock_manager_class):
        """Test discover command with dry-run option."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager._get_cached_discovery_results.return_value = [
            {
                "id": "1",
                "provider": "openai",
                "status": "working",
                "title": "OpenAI Key 1",
            }
        ]

        result = self.runner.invoke(
            main, ["discover", "--dry-run", "--provider", "openai"]
        )
        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        assert "Would process 1 cached items" in result.output
        assert "Would filter to 1 openai items" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_test_with_new_options(self, mock_manager_class):
        """Test test command with all new options."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager._get_cached_api_keys.return_value = [
            {
                "id": "1",
                "provider": "openai",
                "status": "working",
                "title": "OpenAI Key 1",
            }
        ]
        mock_manager._apply_test_filters.return_value = [
            {
                "id": "1",
                "provider": "openai",
                "status": "working",
                "title": "OpenAI Key 1",
            }
        ]
        mock_manager.test_api_endpoints.return_value = self.mock_working_credentials

        # Test with provider filter
        result = self.runner.invoke(main, ["test", "--provider", "openai", "--verbose"])
        assert result.exit_code == 0

        # Test with status filter
        result = self.runner.invoke(main, ["test", "--status", "working", "--verbose"])
        assert result.exit_code == 0

        # Test with limit
        result = self.runner.invoke(main, ["test", "--limit", "1", "--verbose"])
        assert result.exit_code == 0

        # Test with force
        result = self.runner.invoke(main, ["test", "--force", "--verbose"])
        assert result.exit_code == 0

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_test_dry_run(self, mock_manager_class):
        """Test test command with dry-run option."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager._get_cached_api_keys.return_value = [
            {
                "id": "1",
                "provider": "openai",
                "status": "working",
                "title": "OpenAI Key 1",
            }
        ]
        mock_manager._apply_test_filters.return_value = [
            {
                "id": "1",
                "provider": "openai",
                "status": "working",
                "title": "OpenAI Key 1",
            }
        ]

        result = self.runner.invoke(main, ["test", "--dry-run", "--provider", "openai"])
        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        assert "Would test 1 items" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_working_with_new_options(self, mock_manager_class):
        """Test working command with all new options."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_working_credentials_all.return_value = (
            self.mock_working_credentials
        )

        # Test with refresh
        result = self.runner.invoke(main, ["working", "--refresh", "--verbose"])
        assert result.exit_code == 0
        assert "Refresh mode enabled" in result.output

        # Test with provider filter
        result = self.runner.invoke(
            main, ["working", "--provider", "openai", "--verbose"]
        )
        assert result.exit_code == 0
        assert "Provider filter: openai" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_working_export_formats(self, mock_manager_class):
        """Test working command with different export formats."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_working_credentials_all.return_value = (
            self.mock_working_credentials
        )

        # Test JSON export
        result = self.runner.invoke(main, ["working", "--export", "json"])
        assert result.exit_code == 0

        # Test CSV export
        result = self.runner.invoke(main, ["working", "--export", "csv"])
        assert result.exit_code == 0

        # Test with output file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            result = self.runner.invoke(
                main, ["working", "--export", "json", "--output", output_file]
            )
            assert result.exit_code == 0
            assert "JSON exported to:" in result.output

            # Verify file was created
            assert Path(output_file).exists()

        finally:
            Path(output_file).unlink(missing_ok=True)

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_summary_with_new_options(self, mock_manager_class):
        """Test summary command with all new options."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.discover_api_keys.return_value = Mock(**self.mock_discovery_result)

        # Test with provider filter
        result = self.runner.invoke(main, ["summary", "--provider", "openai"])
        assert result.exit_code == 0
        assert "Provider filter: openai" in result.output

        # Test with status filter
        result = self.runner.invoke(main, ["summary", "--status", "working"])
        assert result.exit_code == 0
        assert "Status filter: working" in result.output

        # Test with limit
        result = self.runner.invoke(main, ["summary", "--limit", "2"])
        assert result.exit_code == 0
        assert "Display limit: 2 items" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_summary_export_formats(self, mock_manager_class):
        """Test summary command with different export formats."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.discover_api_keys.return_value = Mock(**self.mock_discovery_result)

        # Test JSON export
        result = self.runner.invoke(main, ["summary", "--export", "json"])
        assert result.exit_code == 0

        # Test CSV export
        result = self.runner.invoke(main, ["summary", "--export", "csv"])
        assert result.exit_code == 0

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_stats_command(self, mock_manager_class):
        """Test stats command."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_comprehensive_stats.return_value = {
            "total_items": 10,
            "total_providers": 4,
            "providers": {"openai": 3, "anthropic": 2, "aws": 3, "azure": 2},
            "statuses": {"working": 6, "failed": 2, "discovered": 2},
            "cache_info": {
                "cache_file": "/tmp/cache.json",
                "last_updated": "2024-01-01T00:00:00",
                "cache_size": "1024 bytes",
            },
        }

        result = self.runner.invoke(main, ["stats"])
        assert result.exit_code == 0
        assert "Total Items: 10" in result.output
        assert "Total Providers: 4" in result.output
        assert "openai: 3" in result.output
        assert "working: 6" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_health_check_command(self, mock_manager_class):
        """Test health-check command."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.perform_health_check.return_value = {
            "overall_health": "healthy",
            "components": {
                "1password": {
                    "healthy": True,
                    "status": "Connected",
                    "version": "2.0.0",
                },
                "cache": {
                    "healthy": True,
                    "status": "Fresh",
                    "info": "Cache is 2.0 hours old",
                },
                "filesystem": {
                    "healthy": True,
                    "status": "Accessible",
                    "info": "File system permissions are correct",
                },
            },
            "recommendations": [],
        }

        result = self.runner.invoke(main, ["health-check"])
        assert result.exit_code == 0
        assert "Overall Health: ✅ healthy" in result.output
        assert "1password: ✅ Connected" in result.output
        assert "cache: ✅ Fresh" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_health_check_degraded(self, mock_manager_class):
        """Test health-check command with degraded health."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.perform_health_check.return_value = {
            "overall_health": "degraded",
            "components": {
                "1password": {
                    "healthy": True,
                    "status": "Connected",
                    "version": "2.0.0",
                },
                "cache": {
                    "healthy": False,
                    "status": "Stale",
                    "error": "Cache is 25.0 hours old",
                },
                "filesystem": {
                    "healthy": True,
                    "status": "Accessible",
                    "info": "File system permissions are correct",
                },
            },
            "recommendations": ["Refresh cache: op-api-manager refresh"],
        }

        result = self.runner.invoke(main, ["health-check"])
        assert result.exit_code == 0
        assert "Overall Health: ⚠️ degraded" in result.output
        assert "cache: ❌ Stale" in result.output
        assert "Refresh cache: op-api-manager refresh" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_backup_command(self, mock_manager_class):
        """Test backup command."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.create_backup.return_value = "/tmp/backup.json"

        result = self.runner.invoke(main, ["backup"])
        assert result.exit_code == 0
        assert "Creating system backup" in result.output
        assert "Backup created successfully: /tmp/backup.json" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_backup_with_timestamp(self, mock_manager_class):
        """Test backup command with timestamp."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.create_backup.return_value = "/tmp/backup_20240101_120000.json"

        result = self.runner.invoke(main, ["backup", "--timestamp"])
        assert result.exit_code == 0
        assert (
            "Backup created successfully: /tmp/backup_20240101_120000.json"
            in result.output
        )

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_restore_command(self, mock_manager_class):
        """Test restore command."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.restore_from_backup.return_value = True
        mock_manager.verify_restored_data.return_value = True

        # Create a temporary backup file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            backup_file = f.name
            json.dump({"cache": {}, "config": {}}, f)

        try:
            result = self.runner.invoke(main, ["restore", backup_file, "--verify"])
            assert result.exit_code == 0
            assert "Restoring system from backup" in result.output
            assert "System restored successfully" in result.output
            assert "Data verification passed" in result.output

        finally:
            Path(backup_file).unlink(missing_ok=True)

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_restore_with_force(self, mock_manager_class):
        """Test restore command with force option."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.restore_from_backup.return_value = True

        # Create a temporary backup file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            backup_file = f.name
            json.dump({"cache": {}, "config": {}}, f)

        try:
            result = self.runner.invoke(main, ["restore", backup_file, "--force"])
            assert result.exit_code == 0
            assert "Force mode enabled" in result.output
            assert "System restored successfully" in result.output

        finally:
            Path(backup_file).unlink(missing_ok=True)

    def test_export_functions(self):
        """Test export utility functions."""
        from op_api_manager.cli import _export_csv, _export_json

        # Test JSON export
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            _export_json(self.mock_working_credentials, output_file, False)
            assert Path(output_file).exists()

            # Verify content
            with open(output_file) as f:
                data = json.load(f)
                assert "openai" in data
                assert "anthropic" in data
                assert "aws" in data

        finally:
            Path(output_file).unlink(missing_ok=True)

        # Test CSV export
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_file = f.name

        try:
            _export_csv(self.mock_working_credentials, output_file, False)
            assert Path(output_file).exists()

            # Verify content
            with open(output_file) as f:
                content = f.read()
                assert "Provider,Title,Credential" in content
                assert "openai" in content
                assert "anthropic" in content

        finally:
            Path(output_file).unlink(missing_ok=True)

    def test_display_functions(self):
        """Test display utility functions."""
        from op_api_manager.cli import _display_health_status, _display_statistics

        # Test statistics display
        stats_data = {
            "total_items": 10,
            "total_providers": 4,
            "providers": {"openai": 3, "anthropic": 2},
            "statuses": {"working": 6, "failed": 2},
            "cache_info": {
                "cache_file": "/tmp/cache.json",
                "last_updated": "2024-01-01T00:00:00",
                "cache_size": "1024 bytes",
            },
        }

        # This should not raise any exceptions
        _display_statistics(stats_data)

        # Test health status display
        health_status = {
            "overall_health": "healthy",
            "components": {
                "1password": {"healthy": True, "status": "Connected"},
                "cache": {"healthy": True, "status": "Fresh"},
            },
            "recommendations": [],
        }

        # This should not raise any exceptions
        _display_health_status(health_status)


class TestCoreManagerNewFeatures:
    """Test new features in the core manager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cache_config = CacheConfig()
        self.manager = OnePasswordAPIKeyManager(self.cache_config)

    @patch("op_api_manager.core.subprocess.run")
    def test_get_comprehensive_stats(self, mock_run):
        """Test comprehensive statistics generation."""
        # Mock cache data
        self.manager._cache = {
            "api_keys": [
                {"provider": "openai", "status": "working"},
                {"provider": "anthropic", "status": "working"},
                {"provider": "aws", "status": "failed"},
            ]
        }

        stats = self.manager.get_comprehensive_stats()

        assert stats["total_items"] == 3
        assert stats["total_providers"] == 3
        assert stats["providers"]["openai"] == 1
        assert stats["providers"]["anthropic"] == 1
        assert stats["providers"]["aws"] == 1
        assert stats["statuses"]["working"] == 2
        assert stats["statuses"]["failed"] == 1

    @patch("op_api_manager.core.subprocess.run")
    def test_perform_health_check(self, mock_run):
        """Test health check functionality."""
        # Mock 1Password version check
        mock_run.return_value = Mock(returncode=0, stdout="2.0.0")

        health_status = self.manager.perform_health_check()

        assert "overall_health" in health_status
        assert "components" in health_status
        assert "1password" in health_status["components"]
        assert health_status["components"]["1password"]["healthy"] is True

    @patch("op_api_manager.core.subprocess.run")
    def test_create_backup(self, mock_run):
        """Test backup creation."""
        # Mock cache data
        self.manager._cache = {
            "api_keys": [],
            "discovery_timestamp": "2024-01-01T00:00:00",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            backup_path = self.manager.create_backup(
                backup_dir=temp_dir, timestamp=False
            )

            assert backup_path is not None
            assert Path(backup_path).exists()

            # Verify backup content
            with open(backup_path) as f:
                backup_data = json.load(f)
                assert "timestamp" in backup_data
                assert "cache" in backup_data
                assert "config" in backup_data

    def test_restore_from_backup(self):
        """Test backup restoration."""
        # Create a temporary backup file
        backup_data = {
            "timestamp": "2024-01-01T00:00:00",
            "cache": {"api_keys": [], "discovery_timestamp": "2024-01-01T00:00:00"},
            "config": {"cache_file": "cache.json", "cache_ttl": 3600},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            backup_file = f.name
            json.dump(backup_data, f)

        try:
            success = self.manager.restore_from_backup(backup_file, force=True)
            assert success is True
            assert self.manager._cache is not None

        finally:
            Path(backup_file).unlink(missing_ok=True)

    def test_verify_restored_data(self):
        """Test restored data verification."""
        # Test with valid cache
        self.manager._cache = {
            "api_keys": [],
            "discovery_timestamp": "2024-01-01T00:00:00",
        }

        assert self.manager.verify_restored_data() is True

        # Test with invalid cache
        self.manager._cache = None
        assert self.manager.verify_restored_data() is False

        # Test with missing required fields
        self.manager._cache = {"api_keys": []}
        assert self.manager.verify_restored_data() is False

    def test_apply_test_filters(self):
        """Test test filter application."""
        api_keys = [
            {"id": "1", "provider": "openai", "status": "working"},
            {"id": "2", "provider": "anthropic", "status": "working"},
            {"id": "3", "provider": "aws", "status": "failed"},
        ]

        # Test provider filter
        filtered = self.manager._apply_test_filters(
            api_keys, "openai", None, None, False
        )
        assert len(filtered) == 1
        assert filtered[0]["provider"] == "openai"

        # Test status filter
        filtered = self.manager._apply_test_filters(
            api_keys, "all", "working", None, False
        )
        assert len(filtered) == 2
        assert all(k["status"] == "working" for k in filtered)

        # Test limit
        filtered = self.manager._apply_test_filters(api_keys, "all", None, 2, False)
        assert len(filtered) == 2


if __name__ == "__main__":
    pytest.main([__file__])
