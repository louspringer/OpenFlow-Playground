#!/usr/bin/env python3
"""
Test Ghostbusters Module

This module tests the Ghostbusters orchestrator functionality.
"""

from unittest.mock import Mock, patch

import pytest

from src.ghostbusters import GhostbustersOrchestrator, run_ghostbusters


class TestGhostbustersOrchestrator:
    """Test the Ghostbusters Orchestrator class"""

    def test_init(self):
        """Test orchestrator initialization"""
        orchestrator = GhostbustersOrchestrator()
        assert orchestrator.config == {}
        assert orchestrator.agents == {}
        assert orchestrator.investigation_results == {}
        assert orchestrator.quality_metrics == {}

    def test_add_agent(self):
        """Test adding an agent"""
        orchestrator = GhostbustersOrchestrator()
        result = orchestrator.add_agent("test_agent", {"type": "test"})
        assert result is True
        assert "test_agent" in orchestrator.agents
        assert orchestrator.agents["test_agent"]["type"] == "test"

    def test_investigate_quality_issues_file(self):
        """Test investigating quality issues for a file"""
        orchestrator = GhostbustersOrchestrator()

        # Mock file path
        with patch("pathlib.Path") as mock_path:
            mock_path.return_value.is_file.return_value = True
            mock_path.return_value.suffix = ".py"
            mock_path.return_value.read_text.return_value = "print('Hello World')"

            result = orchestrator.investigate_quality_issues("test_file.py")

            assert result["target_path"] == "test_file.py"
            assert "timestamp" in result
            assert result["issues_found"] == []
            assert result["quality_score"] == 100.0

    def test_investigate_quality_issues_directory(self):
        """Test investigating quality issues for a directory"""
        orchestrator = GhostbustersOrchestrator()

        # Mock directory path
        with patch("pathlib.Path") as mock_path:
            mock_path.return_value.is_file.return_value = False
            mock_path.return_value.is_dir.return_value = True
            mock_path.return_value.rglob.return_value = []

            result = orchestrator.investigate_quality_issues("test_dir")

            assert result["target_path"] == "test_dir"
            assert "timestamp" in result
            assert result["issues_found"] == []
            assert result["quality_score"] == 100.0

    def test_get_investigation_summary(self):
        """Test getting investigation summary"""
        orchestrator = GhostbustersOrchestrator()
        orchestrator.add_agent("test_agent", {"type": "test"})

        summary = orchestrator.get_investigation_summary()

        assert summary["total_investigations"] == 0
        assert summary["recent_investigations"] == []
        assert summary["overall_quality_trend"] == "no_data"
        assert summary["agent_status"]["test_agent"] == "active"


class TestRunGhostbusters:
    """Test the run_ghostbusters function"""

    def test_run_ghostbusters_default(self):
        """Test running ghostbusters with default path"""
        with patch("src.ghostbusters.GhostbustersOrchestrator") as mock_orchestrator:
            mock_instance = Mock()
            mock_instance.investigate_quality_issues.return_value = {
                "target_path": ".",
                "quality_score": 95.0,
            }
            mock_orchestrator.return_value = mock_instance

            result = run_ghostbusters()

            assert result["target_path"] == "."
            assert result["quality_score"] == 95.0
            mock_instance.add_agent.assert_called()

    def test_run_ghostbusters_custom_path(self):
        """Test running ghostbusters with custom path"""
        with patch("src.ghostbusters.GhostbustersOrchestrator") as mock_orchestrator:
            mock_instance = Mock()
            mock_instance.investigate_quality_issues.return_value = {
                "target_path": "custom_path",
                "quality_score": 88.0,
            }
            mock_orchestrator.return_value = mock_instance

            result = run_ghostbusters("custom_path")

            assert result["target_path"] == "custom_path"
            assert result["quality_score"] == 88.0


if __name__ == "__main__":
    pytest.main([__file__])
