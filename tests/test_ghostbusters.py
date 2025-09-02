#!/usr/bin/env python3
"""
Test Ghostbusters Module

This module tests the Ghostbusters orchestrator functionality.
"""

import asyncio
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.ghostbusters.agents import (
    ArchitectureExpert,
    BuildExpert,
    CodeQualityExpert,
    ModelExpert,
    SecurityExpert,
    TestIssueExpert,
)
from src.ghostbusters.ghostbusters_orchestrator import (
    GhostbustersOrchestrator,
    run_ghostbusters,
)
from src.ghostbusters.recovery import (
    ImportResolver,
    IndentationFixer,
    SyntaxRecoveryEngine,
    TypeAnnotationFixer,
)
from src.ghostbusters.validators import (
    ArchitectureValidator,
    BuildValidator,
    CodeQualityValidator,
    ModelValidator,
    SecurityValidator,
    TestIssueValidator,
)


class TestGhostbustersOrchestrator:
    """Test the Ghostbusters Orchestrator class"""

    def test_init(self):
        """Test orchestrator initialization"""
        orchestrator = GhostbustersOrchestrator()
        assert orchestrator.project_path == Path()
        assert "security" in orchestrator.agents
        assert "code_quality" in orchestrator.agents
        assert "test" in orchestrator.agents
        assert "build" in orchestrator.agents
        assert "architecture" in orchestrator.agents
        assert "model" in orchestrator.agents

    def test_agents_initialization(self):
        """Test that agents are properly initialized"""
        orchestrator = GhostbustersOrchestrator()

        # Check that agents are instances of the correct classes
        assert isinstance(orchestrator.agents["security"], SecurityExpert)
        assert isinstance(orchestrator.agents["code_quality"], CodeQualityExpert)
        assert isinstance(orchestrator.agents["test"], TestIssueExpert)
        assert isinstance(orchestrator.agents["build"], BuildExpert)
        assert isinstance(orchestrator.agents["architecture"], ArchitectureExpert)
        assert isinstance(orchestrator.agents["model"], ModelExpert)

    def test_validators_initialization(self):
        """Test that validators are properly initialized"""
        orchestrator = GhostbustersOrchestrator()

        # Check that validators are instances of the correct classes
        assert isinstance(orchestrator.validators["security"], SecurityValidator)
        assert isinstance(orchestrator.validators["code_quality"], CodeQualityValidator)
        assert isinstance(orchestrator.validators["test"], TestIssueValidator)
        assert isinstance(orchestrator.validators["build"], BuildValidator)
        assert isinstance(orchestrator.validators["architecture"], ArchitectureValidator)
        assert isinstance(orchestrator.validators["model"], ModelValidator)

    def test_recovery_engines_initialization(self):
        """Test that recovery engines are properly initialized"""
        orchestrator = GhostbustersOrchestrator()

        # Check that recovery engines are instances of the correct classes
        assert isinstance(orchestrator.recovery_engines["syntax"], SyntaxRecoveryEngine)
        assert isinstance(orchestrator.recovery_engines["indentation"], IndentationFixer)
        assert isinstance(orchestrator.recovery_engines["imports"], ImportResolver)
        assert isinstance(orchestrator.recovery_engines["types"], TypeAnnotationFixer)

    def test_workflow_creation(self):
        """Test that the workflow is properly created"""
        orchestrator = GhostbustersOrchestrator()

        # Check that workflow has the expected nodes
        workflow_nodes = list(orchestrator.workflow.nodes.keys())
        expected_nodes = [
            "detect_delusions",
            "validate_findings",
            "plan_recovery",
            "execute_recovery",
            "validate_recovery",
            "generate_report",
        ]

        for node in expected_nodes:
            assert node in workflow_nodes, f"Expected node {node} not found in workflow"


class TestRunGhostbusters:
    """Test the run_ghostbusters function"""

    @pytest.mark.asyncio
    async def test_run_ghostbusters_default(self):
        """Test running ghostbusters with default path"""
        with patch("src.ghostbusters.ghostbusters_orchestrator.GhostbustersOrchestrator") as mock_orchestrator:
            mock_instance = Mock()
            # Create a mock state object
            mock_state = Mock(
                project_path=".",
                confidence_score=0.95,
                delusions_detected=[],
                current_phase="analysis_complete",
            )
            # Make run_ghostbusters return an awaitable that returns the mock state
            mock_instance.run_ghostbusters.return_value = asyncio.Future()
            mock_instance.run_ghostbusters.return_value.set_result(mock_state)
            mock_orchestrator.return_value = mock_instance

            result = await run_ghostbusters()

            assert result.project_path == "."
            assert result.confidence_score == 0.95
            assert result.current_phase == "analysis_complete"

    @pytest.mark.asyncio
    async def test_run_ghostbusters_custom_path(self):
        """Test running ghostbusters with custom path"""
        with patch("src.ghostbusters.ghostbusters_orchestrator.GhostbustersOrchestrator") as mock_orchestrator:
            mock_instance = Mock()
            # Create a mock state object
            mock_state = Mock(
                project_path="custom_path",
                confidence_score=0.88,
                delusions_detected=[],
                current_phase="analysis_complete",
            )
            # Make run_ghostbusters return an awaitable that returns the mock state
            mock_instance.run_ghostbusters.return_value = asyncio.Future()
            mock_instance.run_ghostbusters.return_value.set_result(mock_state)
            mock_orchestrator.return_value = mock_instance

            result = await run_ghostbusters("custom_path")

            assert result.project_path == "custom_path"
            assert result.confidence_score == 0.88
            assert result.current_phase == "analysis_complete"


if __name__ == "__main__":
    pytest.main([__file__])
