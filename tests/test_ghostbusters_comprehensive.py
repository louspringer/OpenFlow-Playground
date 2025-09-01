#!/usr/bin/env python3
"""
Tests for Ghostbusters Component - Simplified Version
"""

from pathlib import Path

import pytest

from src.ghostbusters import (
    GhostbustersOrchestrator,
)


class TestGhostbustersBasic:
    """Test basic Ghostbusters functionality"""

    @pytest.fixture
    def project_path(self) -> Path:
        """Get project path for testing"""
        return Path()

    def test_ghostbusters_orchestrator_import(self, project_path: Path) -> None:
        """Test that GhostbustersOrchestrator can be imported and instantiated"""
        orchestrator = GhostbustersOrchestrator()
        assert orchestrator is not None
        assert hasattr(orchestrator, "project_path")

    def test_ghostbusters_orchestrator_basic_functionality(self, project_path: Path) -> None:
        """Test basic GhostbustersOrchestrator functionality"""
        orchestrator = GhostbustersOrchestrator()

        # Test that the orchestrator has the expected attributes
        assert hasattr(orchestrator, "project_path")
        assert hasattr(orchestrator, "agents")
        assert hasattr(orchestrator, "validators")
        assert hasattr(orchestrator, "recovery_engines")
        assert hasattr(orchestrator, "workflow")
        assert hasattr(orchestrator, "compiled_workflow")

        # Test that project_path is initialized
        assert orchestrator.project_path == Path()

    def test_ghostbusters_rules_exist(self) -> None:
        """Test that Ghostbusters rules file exists"""
        rules_file = Path(".cursor/rules/ghostbusters.mdc")
        assert rules_file.exists(), "Ghostbusters rules file should exist"

        # Check that the file has content
        content = rules_file.read_text()
        assert len(content) > 0, "Ghostbusters rules file should have content"
        assert "Ghostbusters Component" in content, "Rules file should contain component description"


if __name__ == "__main__":
    pytest.main([__file__])
