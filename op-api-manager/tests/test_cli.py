"""
Tests for the CLI module.
"""

from unittest.mock import Mock, patch

from click.testing import CliRunner
from op_api_manager.cli import main


class TestCLI:
    """Test CLI functionality."""

    def test_help_command(self):
        """Test help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "OP API Manager" in result.output

    def test_version_command(self):
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "op-api-manager" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_discover_command(self, mock_manager_class):
        """Test discover command."""
        # Mock the manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        # Mock discovery result
        mock_result = Mock()
        mock_result.total_items = 100
        mock_result.api_keys = []
        mock_result.credential_pairs = []
        mock_result.discovery_timestamp = "2025-01-20T10:30:00"
        mock_result.providers = {}
        mock_result.status_summary = {}

        mock_manager.discover_api_keys.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(main, ["discover"])

        assert result.exit_code == 0
        assert "API Key Discovery Results" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_summary_command(self, mock_manager_class):
        """Test summary command."""
        # Mock the manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        # Mock discovery result
        mock_result = Mock()
        mock_result.api_keys = []
        mock_result.providers = {}
        mock_result.status_summary = {}

        mock_manager.discover_api_keys.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(main, ["summary"])

        assert result.exit_code == 0
        assert "API Key Summary" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_cache_command(self, mock_manager_class):
        """Test cache command."""
        # Mock the manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        # Mock cache status
        mock_cache_status = {
            "status": "valid",
            "age_hours": 2.5,
            "max_age_hours": 24,
            "last_discovery": "2025-01-20T08:00:00",
        }

        mock_manager.get_cache_status.return_value = mock_cache_status

        runner = CliRunner()
        result = runner.invoke(main, ["cache"])

        assert result.exit_code == 0
        assert "Cache Status" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_providers_command(self, mock_manager_class):
        """Test providers command."""
        # Mock the manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        # Mock discovery result
        mock_result = Mock()
        mock_result.providers = {"openai": 5, "anthropic": 3}

        mock_manager.discover_api_keys.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(main, ["providers"])

        assert result.exit_code == 0
        assert "Provider Breakdown" in result.output

    @patch("op_api_manager.cli.OnePasswordAPIKeyManager")
    def test_refresh_command(self, mock_manager_class):
        """Test refresh command."""
        # Mock the manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        # Mock discovery result
        mock_result = Mock()
        mock_result.total_items = 100
        mock_result.api_keys = []
        mock_result.credential_pairs = []
        mock_result.discovery_timestamp = "2025-01-20T10:30:00"
        mock_result.providers = {}
        mock_result.status_summary = {}

        mock_manager.refresh_cache.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(main, ["refresh"])

        assert result.exit_code == 0
        assert "Cache refreshed successfully" in result.output
