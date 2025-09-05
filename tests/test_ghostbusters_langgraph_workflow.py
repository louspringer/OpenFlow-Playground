#!/usr/bin/env python3
"""
LangGraph Workflow Tests for Ghostbusters with Pydantic State

This module tests the LangGraph workflow integration with pydantic state models.
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.ghostbusters.ghostbusters_orchestrator import (
    GhostbustersOrchestrator,
    GhostbustersState,
    run_ghostbusters,
)


class TestLangGraphWorkflowIntegration:
    """Test LangGraph workflow integration with pydantic state"""

    @pytest.fixture
    def orchestrator(self):
        """Create a GhostbustersOrchestrator instance for testing"""
        return GhostbustersOrchestrator()

    @pytest.fixture
    def initial_state(self):
        """Create an initial GhostbustersState for testing"""
        return GhostbustersState(
            project_path="/test/project",
            delusions_detected=[],
            recovery_actions=[],
            confidence_score=0.0,
            validation_results={},
            recovery_results={},
            current_phase="detection",
            errors=[],
            warnings=[],
            metadata={},
        )

    def test_workflow_creation(self, orchestrator):
        """Test that the LangGraph workflow is created correctly"""
        assert orchestrator.workflow is not None
        assert orchestrator.compiled_workflow is not None
        
        # Check that workflow has the expected nodes
        expected_nodes = [
            "detect_delusions",
            "validate_findings", 
            "plan_recovery",
            "execute_recovery",
            "validate_recovery",
            "generate_report",
        ]
        
        for node in expected_nodes:
            assert node in orchestrator.workflow.nodes

    def test_workflow_state_type(self, orchestrator):
        """Test that the workflow uses GhostbustersState as the state type"""
        # The workflow should be configured to use GhostbustersState
        assert orchestrator.workflow.state_schema == GhostbustersState

    @pytest.mark.asyncio
    async def test_detect_delusions_node(self, orchestrator, initial_state):
        """Test the detect_delusions workflow node"""
        # Mock the agents to return predictable results
        mock_result = Mock()
        mock_result.delusions = [
            {
                "type": "syntax_error",
                "file": "test.py",
                "line": 10,
                "description": "Missing colon",
                "confidence": 0.9,
                "severity": "high",
            }
        ]
        mock_result.confidence = 0.8
        mock_result.recommendations = ["Fix syntax error"]

        with patch.object(orchestrator.agents["security"], "detect_delusions", return_value=mock_result):
            result_state = await orchestrator._detect_delusions_node(initial_state)
            
            assert isinstance(result_state, GhostbustersState)
            assert result_state.current_phase == "detection_complete"
            assert len(result_state.delusions_detected) > 0

    @pytest.mark.asyncio
    async def test_validate_findings_node(self, orchestrator, initial_state):
        """Test the validate_findings workflow node"""
        # Set up initial state with delusions
        initial_state.delusions_detected = [
            {"agent": "security", "delusions": []},
            {"agent": "code_quality", "delusions": []},
        ]

        # Mock the validators to return predictable results
        mock_validation_result = Mock()
        mock_validation_result.is_valid = True
        mock_validation_result.confidence = 0.9
        mock_validation_result.issues = []
        mock_validation_result.recommendations = []
        mock_validation_result.validator_name = "TestValidator"

        with patch.object(orchestrator.validators["security"], "validate_findings", return_value=mock_validation_result):
            result_state = await orchestrator._validate_findings_node(initial_state)
            
            assert isinstance(result_state, GhostbustersState)
            assert result_state.current_phase == "validation_complete"
            assert len(result_state.validation_results) > 0

    @pytest.mark.asyncio
    async def test_plan_recovery_node(self, orchestrator, initial_state):
        """Test the plan_recovery workflow node"""
        # Set up initial state with delusions
        initial_state.delusions_detected = [
            {
                "agent": "security",
                "delusions": [
                    {
                        "type": "syntax_error",
                        "file": "test.py",
                        "line": 10,
                        "description": "Missing colon",
                        "confidence": 0.9,
                        "severity": "high",
                    }
                ],
            }
        ]

        result_state = await orchestrator._plan_recovery_node(initial_state)
        
        assert isinstance(result_state, GhostbustersState)
        assert result_state.current_phase == "planning_complete"
        # Recovery actions should be planned based on delusions

    @pytest.mark.asyncio
    async def test_execute_recovery_node(self, orchestrator, initial_state):
        """Test the execute_recovery workflow node"""
        # Set up initial state with recovery actions
        initial_state.recovery_actions = [
            {
                "id": "recovery_1",
                "engine": "syntax",
                "delusion": {"type": "syntax_error"},
                "priority": "high",
            }
        ]

        # Mock the recovery engines
        mock_recovery_result = Mock()
        mock_recovery_result.success = True
        mock_recovery_result.confidence = 0.8
        mock_recovery_result.changes_made = ["Fixed syntax error"]
        mock_recovery_result.engine_name = "SyntaxRecoveryEngine"

        with patch.object(orchestrator.recovery_engines["syntax"], "execute_recovery", return_value=mock_recovery_result):
            result_state = await orchestrator._execute_recovery_node(initial_state)
            
            assert isinstance(result_state, GhostbustersState)
            assert result_state.current_phase == "recovery_complete"
            assert len(result_state.recovery_results) > 0

    @pytest.mark.asyncio
    async def test_validate_recovery_node(self, orchestrator, initial_state):
        """Test the validate_recovery workflow node"""
        # Set up initial state with validation results
        initial_state.validation_results = {
            "security": Mock(confidence=0.8),
            "code_quality": Mock(confidence=0.9),
        }

        # Mock the validators for post-recovery validation
        mock_validation_result = Mock()
        mock_validation_result.confidence = 0.95

        with patch.object(orchestrator.validators["security"], "validate_findings", return_value=mock_validation_result):
            result_state = await orchestrator._validate_recovery_node(initial_state)
            
            assert isinstance(result_state, GhostbustersState)
            assert result_state.current_phase == "validation_complete"
            assert "confidence_improvement" in result_state.metadata

    @pytest.mark.asyncio
    async def test_generate_report_node(self, orchestrator, initial_state):
        """Test the generate_report workflow node"""
        # Set up initial state with validation results
        initial_state.validation_results = {
            "security": Mock(confidence=0.8),
            "code_quality": Mock(confidence=0.9),
        }
        initial_state.metadata["recovery_success_rate"] = 0.7

        result_state = await orchestrator._generate_report_node(initial_state)
        
        assert isinstance(result_state, GhostbustersState)
        assert result_state.current_phase == "complete"
        assert "report" in result_state.metadata
        assert result_state.confidence_score > 0

    @pytest.mark.asyncio
    async def test_state_transitions(self, orchestrator, initial_state):
        """Test that state transitions work correctly through the workflow"""
        # Mock all the agents, validators, and recovery engines
        mock_delusion_result = Mock()
        mock_delusion_result.delusions = []
        mock_delusion_result.confidence = 0.8
        mock_delusion_result.recommendations = []

        mock_validation_result = Mock()
        mock_validation_result.is_valid = True
        mock_validation_result.confidence = 0.9
        mock_validation_result.issues = []
        mock_validation_result.recommendations = []
        mock_validation_result.validator_name = "TestValidator"

        mock_recovery_result = Mock()
        mock_recovery_result.success = True
        mock_recovery_result.confidence = 0.8
        mock_recovery_result.changes_made = []
        mock_recovery_result.engine_name = "TestEngine"

        # Mock all the components
        with patch.object(orchestrator.agents["security"], "detect_delusions", return_value=mock_delusion_result), \
             patch.object(orchestrator.validators["security"], "validate_findings", return_value=mock_validation_result), \
             patch.object(orchestrator.recovery_engines["syntax"], "execute_recovery", return_value=mock_recovery_result):
            
            # Test each node in sequence
            state = initial_state
            
            # Detection phase
            state = await orchestrator._detect_delusions_node(state)
            assert state.current_phase == "detection_complete"
            
            # Validation phase
            state = await orchestrator._validate_findings_node(state)
            assert state.current_phase == "validation_complete"
            
            # Planning phase
            state = await orchestrator._plan_recovery_node(state)
            assert state.current_phase == "planning_complete"
            
            # Execution phase
            state = await orchestrator._execute_recovery_node(state)
            assert state.current_phase == "recovery_complete"
            
            # Post-recovery validation
            state = await orchestrator._validate_recovery_node(state)
            assert state.current_phase == "validation_complete"
            
            # Report generation
            state = await orchestrator._generate_report_node(state)
            assert state.current_phase == "complete"

    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, orchestrator, initial_state):
        """Test that the workflow handles errors gracefully"""
        # Mock an agent to raise an exception
        with patch.object(orchestrator.agents["security"], "detect_delusions", side_effect=Exception("Test error")):
            result_state = await orchestrator._detect_delusions_node(initial_state)
            
            assert isinstance(result_state, GhostbustersState)
            assert len(result_state.errors) > 0
            assert "security detection error" in result_state.errors[0]

    @pytest.mark.asyncio
    async def test_state_serialization_in_workflow(self, orchestrator, initial_state):
        """Test that state can be serialized and deserialized during workflow execution"""
        # Mock the agents
        mock_result = Mock()
        mock_result.delusions = []
        mock_result.confidence = 0.8
        mock_result.recommendations = []

        with patch.object(orchestrator.agents["security"], "detect_delusions", return_value=mock_result):
            # Execute a workflow node
            result_state = await orchestrator._detect_delusions_node(initial_state)
            
            # Test serialization
            state_dict = result_state.model_dump()
            assert isinstance(state_dict, dict)
            assert "project_path" in state_dict
            assert "current_phase" in state_dict
            
            # Test deserialization
            deserialized_state = GhostbustersState.model_validate(state_dict)
            assert isinstance(deserialized_state, GhostbustersState)
            assert deserialized_state.project_path == result_state.project_path
            assert deserialized_state.current_phase == result_state.current_phase

    @pytest.mark.asyncio
    async def test_full_workflow_execution(self, orchestrator):
        """Test the complete workflow execution"""
        # Mock all components to return predictable results
        mock_delusion_result = Mock()
        mock_delusion_result.delusions = []
        mock_delusion_result.confidence = 0.8
        mock_delusion_result.recommendations = []

        mock_validation_result = Mock()
        mock_validation_result.is_valid = True
        mock_validation_result.confidence = 0.9
        mock_validation_result.issues = []
        mock_validation_result.recommendations = []
        mock_validation_result.validator_name = "TestValidator"

        mock_recovery_result = Mock()
        mock_recovery_result.success = True
        mock_recovery_result.confidence = 0.8
        mock_recovery_result.changes_made = []
        mock_recovery_result.engine_name = "TestEngine"

        # Mock all the components
        with patch.object(orchestrator.agents["security"], "detect_delusions", return_value=mock_delusion_result), \
             patch.object(orchestrator.validators["security"], "validate_findings", return_value=mock_validation_result), \
             patch.object(orchestrator.recovery_engines["syntax"], "execute_recovery", return_value=mock_recovery_result):
            
            # Run the complete workflow
            final_state = await orchestrator.run_ghostbusters()
            
            # The workflow might return a dict or GhostbustersState
            if isinstance(final_state, dict):
                assert final_state.get("current_phase") == "complete"
                assert final_state.get("confidence_score", 0) >= 0.0
            else:
                assert isinstance(final_state, GhostbustersState)
                assert final_state.current_phase == "complete"
                assert final_state.confidence_score >= 0.0

    def test_confidence_calculation(self, orchestrator):
        """Test the confidence calculation method"""
        # Test with empty validation results
        confidence = orchestrator._calculate_confidence({})
        assert confidence == 0.0
        
        # Test with validation results
        validation_results = {
            "security": Mock(confidence=0.8),
            "code_quality": Mock(confidence=0.9),
        }
        
        confidence = orchestrator._calculate_confidence(validation_results)
        assert abs(confidence - 0.85) < 0.001  # Average of 0.8 and 0.9 (with floating point tolerance)

    def test_plan_recovery_action(self, orchestrator):
        """Test the recovery action planning method"""
        # Test with a syntax error delusion
        delusion = {
            "type": "syntax_error",
            "file": "test.py",
            "line": 10,
            "description": "Missing colon",
            "confidence": 0.9,
            "severity": "high",
        }
        
        action = asyncio.run(orchestrator._plan_recovery_action(delusion))
        
        if action:  # Action might be None if no matching engine
            assert "id" in action
            assert "engine" in action
            assert "delusion" in action
            assert "priority" in action


class TestRunGhostbustersFunction:
    """Test the convenience function for running Ghostbusters"""

    @pytest.mark.asyncio
    async def test_run_ghostbusters_default_path(self):
        """Test running Ghostbusters with default path"""
        # Mock the orchestrator to avoid actual execution
        with patch("src.ghostbusters.ghostbusters_orchestrator.GhostbustersOrchestrator") as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.run_ghostbusters = AsyncMock(return_value=GhostbustersState(
                project_path=".",
                current_phase="complete",
                confidence_score=0.8,
            ))
            mock_orchestrator_class.return_value = mock_orchestrator
            
            result = await run_ghostbusters()
            
            assert isinstance(result, GhostbustersState)
            assert result.current_phase == "complete"
            assert result.confidence_score == 0.8

    @pytest.mark.asyncio
    async def test_run_ghostbusters_custom_path(self):
        """Test running Ghostbusters with custom path"""
        custom_path = "/custom/project/path"
        
        with patch("src.ghostbusters.ghostbusters_orchestrator.GhostbustersOrchestrator") as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.run_ghostbusters = AsyncMock(return_value=GhostbustersState(
                project_path=custom_path,
                current_phase="complete",
                confidence_score=0.8,
            ))
            mock_orchestrator_class.return_value = mock_orchestrator
            
            result = await run_ghostbusters(custom_path)
            
            assert isinstance(result, GhostbustersState)
            assert result.project_path == custom_path
            mock_orchestrator_class.assert_called_once_with(custom_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
