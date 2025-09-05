#!/usr/bin/env python3
"""
Comprehensive Pydantic Validation Tests for Ghostbusters

This module tests pydantic model validation, serialization, and error handling
for all Ghostbusters components.
"""

import json
from typing import Any, Dict, List

import pytest
from pydantic import ValidationError

from src.ghostbusters.agents.base_expert import DelusionResult
from src.ghostbusters.ghostbusters_orchestrator import GhostbustersState
from src.ghostbusters.recovery import RecoveryResult
from src.ghostbusters.validators import ValidationResult


class TestDelusionResultValidation:
    """Test DelusionResult pydantic model validation"""

    def test_valid_delusion_result(self):
        """Test creating a valid DelusionResult"""
        result = DelusionResult(
            delusions=[
                {
                    "type": "syntax_error",
                    "file": "test.py",
                    "line": 10,
                    "description": "Missing colon",
                    "confidence": 0.9,
                    "severity": "high",
                }
            ],
            confidence=0.8,
            recommendations=["Fix syntax error"],
            agent_name="TestAgent",
        )
        
        assert result.delusions[0]["type"] == "syntax_error"
        assert result.confidence == 0.8
        assert result.agent_name == "TestAgent"

    def test_confidence_validation_range(self):
        """Test confidence field validation (0.0-1.0 range)"""
        # Valid confidence values
        result1 = DelusionResult(
            delusions=[], confidence=0.0, recommendations=[], agent_name="Test"
        )
        assert result1.confidence == 0.0

        result2 = DelusionResult(
            delusions=[], confidence=1.0, recommendations=[], agent_name="Test"
        )
        assert result2.confidence == 1.0

        result3 = DelusionResult(
            delusions=[], confidence=0.5, recommendations=[], agent_name="Test"
        )
        assert result3.confidence == 0.5

    def test_confidence_validation_out_of_range(self):
        """Test confidence field validation with out-of-range values"""
        # Test negative confidence (should be rejected by field constraint)
        with pytest.raises(ValidationError):
            DelusionResult(
                delusions=[], confidence=-0.5, recommendations=[], agent_name="Test"
            )

        # Test confidence > 1.0 (should be rejected by field constraint)
        with pytest.raises(ValidationError):
            DelusionResult(
                delusions=[], confidence=1.5, recommendations=[], agent_name="Test"
            )

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with pytest.raises(ValidationError) as exc_info:
            DelusionResult()
        
        errors = exc_info.value.errors()
        error_fields = [error["loc"][0] for error in errors]
        assert "agent_name" in error_fields

    def test_default_values(self):
        """Test default values for optional fields"""
        result = DelusionResult(agent_name="Test", confidence=0.0)
        assert result.delusions == []
        assert result.recommendations == []
        assert result.confidence == 0.0


class TestValidationResultValidation:
    """Test ValidationResult pydantic model validation"""

    def test_valid_validation_result(self):
        """Test creating a valid ValidationResult"""
        result = ValidationResult(
            is_valid=True,
            confidence=0.9,
            issues=["Issue 1", "Issue 2"],
            recommendations=["Fix issue 1", "Fix issue 2"],
            validator_name="TestValidator",
        )
        
        assert result.is_valid is True
        assert result.confidence == 0.9
        assert len(result.issues) == 2
        assert len(result.recommendations) == 2

    def test_confidence_validation(self):
        """Test confidence field validation"""
        # Valid confidence
        result = ValidationResult(
            is_valid=True, confidence=0.7, validator_name="Test"
        )
        assert result.confidence == 0.7

        # Out of range confidence (should be rejected by field constraint)
        with pytest.raises(ValidationError):
            ValidationResult(
                is_valid=True, confidence=1.2, validator_name="Test"
            )

    def test_default_values(self):
        """Test default values for optional fields"""
        result = ValidationResult(is_valid=True, validator_name="Test", confidence=0.0)
        assert result.confidence == 0.0
        assert result.issues == []
        assert result.recommendations == []
        assert result.validator_name == "Test"


class TestRecoveryResultValidation:
    """Test RecoveryResult pydantic model validation"""

    def test_valid_recovery_result(self):
        """Test creating a valid RecoveryResult"""
        result = RecoveryResult(
            success=True,
            message="Recovery completed successfully",
            confidence=0.8,
            changes_made=["Fixed syntax error", "Added import"],
            engine_name="SyntaxRecoveryEngine",
            files_fixed=["test.py"],
            errors=[],
            warnings=["Minor warning"],
            metadata={"engine_type": "syntax"},
        )
        
        assert result.success is True
        assert result.confidence == 0.8
        assert len(result.changes_made) == 2
        assert result.engine_name == "SyntaxRecoveryEngine"

    def test_confidence_validation(self):
        """Test confidence field validation"""
        result = RecoveryResult(
            success=True, confidence=0.5, engine_name="Test"
        )
        assert result.confidence == 0.5

        # Test out of range (should be rejected by field constraint)
        with pytest.raises(ValidationError):
            RecoveryResult(
                success=True, confidence=1.5, engine_name="Test"
            )

    def test_default_values(self):
        """Test default values for optional fields"""
        result = RecoveryResult(success=True, engine_name="Test")
        assert result.message == "Recovery completed"
        assert result.confidence == 0.8
        assert result.changes_made == []
        assert result.files_fixed == []
        assert result.errors == []
        assert result.warnings == []
        assert result.metadata == {}


class TestGhostbustersStateValidation:
    """Test GhostbustersState pydantic model validation"""

    def test_valid_ghostbusters_state(self):
        """Test creating a valid GhostbustersState"""
        state = GhostbustersState(
            project_path="/test/project",
            delusions_detected=[
                {"agent": "security", "delusions": []},
                {"agent": "code_quality", "delusions": []},
            ],
            recovery_actions=[
                {"id": "action1", "engine": "syntax", "priority": "high"},
            ],
            confidence_score=0.8,
            validation_results={"security": "valid"},
            recovery_results={"action1": "success"},
            current_phase="detection",
            errors=[],
            warnings=["Warning 1"],
            metadata={"timestamp": "2024-01-01"},
        )
        
        assert state.project_path == "/test/project"
        assert len(state.delusions_detected) == 2
        assert state.confidence_score == 0.8
        assert state.current_phase == "detection"

    def test_confidence_score_validation(self):
        """Test confidence_score field validation"""
        state = GhostbustersState(project_path="/test")
        assert state.confidence_score == 0.0

        state = GhostbustersState(project_path="/test", confidence_score=0.5)
        assert state.confidence_score == 0.5

        # Test out of range (should be rejected by field constraint)
        with pytest.raises(ValidationError):
            GhostbustersState(project_path="/test", confidence_score=1.2)

    def test_default_values(self):
        """Test default values for optional fields"""
        state = GhostbustersState(project_path="/test")
        assert state.delusions_detected == []
        assert state.recovery_actions == []
        assert state.confidence_score == 0.0
        assert state.validation_results == {}
        assert state.recovery_results == {}
        assert state.current_phase == "detection"
        assert state.errors == []
        assert state.warnings == []
        assert state.metadata == {}


class TestPydanticSerialization:
    """Test pydantic model serialization and deserialization"""

    def test_delusion_result_serialization(self):
        """Test DelusionResult serialization to dict and JSON"""
        result = DelusionResult(
            delusions=[{"type": "test", "file": "test.py", "line": 1}],
            confidence=0.8,
            recommendations=["Fix test"],
            agent_name="TestAgent",
        )
        
        # Test to_dict
        result_dict = result.model_dump()
        assert isinstance(result_dict, dict)
        assert result_dict["confidence"] == 0.8
        assert result_dict["agent_name"] == "TestAgent"
        
        # Test to JSON
        result_json = result.model_dump_json()
        assert isinstance(result_json, str)
        parsed = json.loads(result_json)
        assert parsed["confidence"] == 0.8

    def test_validation_result_serialization(self):
        """Test ValidationResult serialization"""
        result = ValidationResult(
            is_valid=True,
            confidence=0.9,
            issues=["Issue 1"],
            recommendations=["Fix 1"],
            validator_name="TestValidator",
        )
        
        result_dict = result.model_dump()
        assert result_dict["is_valid"] is True
        assert result_dict["confidence"] == 0.9

    def test_recovery_result_serialization(self):
        """Test RecoveryResult serialization"""
        result = RecoveryResult(
            success=True,
            confidence=0.7,
            engine_name="TestEngine",
            changes_made=["Change 1"],
        )
        
        result_dict = result.model_dump()
        assert result_dict["success"] is True
        assert result_dict["confidence"] == 0.7

    def test_ghostbusters_state_serialization(self):
        """Test GhostbustersState serialization"""
        state = GhostbustersState(
            project_path="/test",
            confidence_score=0.8,
            current_phase="detection",
        )
        
        state_dict = state.model_dump()
        assert state_dict["project_path"] == "/test"
        assert state_dict["confidence_score"] == 0.8
        assert state_dict["current_phase"] == "detection"


class TestPydanticDeserialization:
    """Test pydantic model deserialization from dict and JSON"""

    def test_delusion_result_deserialization(self):
        """Test DelusionResult deserialization from dict"""
        data = {
            "delusions": [{"type": "test", "file": "test.py", "line": 1}],
            "confidence": 0.8,
            "recommendations": ["Fix test"],
            "agent_name": "TestAgent",
        }
        
        result = DelusionResult.model_validate(data)
        assert result.confidence == 0.8
        assert result.agent_name == "TestAgent"

    def test_validation_result_deserialization(self):
        """Test ValidationResult deserialization from dict"""
        data = {
            "is_valid": True,
            "confidence": 0.9,
            "issues": ["Issue 1"],
            "recommendations": ["Fix 1"],
            "validator_name": "TestValidator",
        }
        
        result = ValidationResult.model_validate(data)
        assert result.is_valid is True
        assert result.confidence == 0.9

    def test_recovery_result_deserialization(self):
        """Test RecoveryResult deserialization from dict"""
        data = {
            "success": True,
            "confidence": 0.7,
            "engine_name": "TestEngine",
            "changes_made": ["Change 1"],
        }
        
        result = RecoveryResult.model_validate(data)
        assert result.success is True
        assert result.confidence == 0.7

    def test_ghostbusters_state_deserialization(self):
        """Test GhostbustersState deserialization from dict"""
        data = {
            "project_path": "/test",
            "confidence_score": 0.8,
            "current_phase": "detection",
            "delusions_detected": [],
            "recovery_actions": [],
            "validation_results": {},
            "recovery_results": {},
            "errors": [],
            "warnings": [],
            "metadata": {},
        }
        
        state = GhostbustersState.model_validate(data)
        assert state.project_path == "/test"
        assert state.confidence_score == 0.8
        assert state.current_phase == "detection"


class TestPydanticErrorHandling:
    """Test pydantic validation error handling"""

    def test_invalid_confidence_type(self):
        """Test validation error for invalid confidence type"""
        with pytest.raises(ValidationError) as exc_info:
            DelusionResult(
                delusions=[],
                confidence="invalid",  # Should be float
                recommendations=[],
                agent_name="Test",
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "float_parsing" for error in errors)

    def test_missing_required_field(self):
        """Test validation error for missing required field"""
        with pytest.raises(ValidationError) as exc_info:
            ValidationResult(is_valid=True)  # Missing validator_name
        
        errors = exc_info.value.errors()
        error_fields = [error["loc"][0] for error in errors]
        assert "validator_name" in error_fields

    def test_invalid_field_type(self):
        """Test validation error for invalid field type"""
        with pytest.raises(ValidationError) as exc_info:
            RecoveryResult(
                success="invalid",  # Should be bool
                engine_name="Test",
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "bool_parsing" for error in errors)


class TestPydanticModelEquality:
    """Test pydantic model equality and comparison"""

    def test_delusion_result_equality(self):
        """Test DelusionResult equality"""
        result1 = DelusionResult(
            delusions=[], confidence=0.8, recommendations=[], agent_name="Test"
        )
        result2 = DelusionResult(
            delusions=[], confidence=0.8, recommendations=[], agent_name="Test"
        )
        
        assert result1 == result2

    def test_validation_result_equality(self):
        """Test ValidationResult equality"""
        result1 = ValidationResult(
            is_valid=True, confidence=0.9, validator_name="Test"
        )
        result2 = ValidationResult(
            is_valid=True, confidence=0.9, validator_name="Test"
        )
        
        assert result1 == result2

    def test_recovery_result_equality(self):
        """Test RecoveryResult equality"""
        result1 = RecoveryResult(
            success=True, confidence=0.7, engine_name="Test"
        )
        result2 = RecoveryResult(
            success=True, confidence=0.7, engine_name="Test"
        )
        
        assert result1 == result2

    def test_ghostbusters_state_equality(self):
        """Test GhostbustersState equality"""
        state1 = GhostbustersState(
            project_path="/test", confidence_score=0.8
        )
        state2 = GhostbustersState(
            project_path="/test", confidence_score=0.8
        )
        
        assert state1 == state2


class TestPydanticFieldValidation:
    """Test specific field validation rules"""

    def test_confidence_field_validator(self):
        """Test confidence field validator across all models"""
        # Test DelusionResult confidence validator (field constraint prevents negative values)
        with pytest.raises(ValidationError):
            DelusionResult(
                delusions=[], confidence=-0.1, recommendations=[], agent_name="Test"
            )

        # Test ValidationResult confidence validator (field constraint prevents > 1.0)
        with pytest.raises(ValidationError):
            ValidationResult(
                is_valid=True, confidence=1.1, validator_name="Test"
            )

        # Test RecoveryResult confidence validator (field constraint prevents > 1.0)
        with pytest.raises(ValidationError):
            RecoveryResult(
                success=True, confidence=2.0, engine_name="Test"
            )

    def test_list_field_defaults(self):
        """Test that list fields have proper defaults"""
        # Test DelusionResult
        result = DelusionResult(agent_name="Test", confidence=0.0)
        assert result.delusions == []
        assert result.recommendations == []

        # Test ValidationResult
        result = ValidationResult(is_valid=True, validator_name="Test", confidence=0.0)
        assert result.issues == []
        assert result.recommendations == []

        # Test RecoveryResult
        result = RecoveryResult(success=True, engine_name="Test")
        assert result.changes_made == []
        assert result.files_fixed == []
        assert result.errors == []
        assert result.warnings == []

        # Test GhostbustersState
        state = GhostbustersState(project_path="/test")
        assert state.delusions_detected == []
        assert state.recovery_actions == []
        assert state.errors == []
        assert state.warnings == []

    def test_dict_field_defaults(self):
        """Test that dict fields have proper defaults"""
        # Test GhostbustersState
        state = GhostbustersState(project_path="/test")
        assert state.validation_results == {}
        assert state.recovery_results == {}
        assert state.metadata == {}

        # Test RecoveryResult
        result = RecoveryResult(success=True, engine_name="Test")
        assert result.metadata == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
