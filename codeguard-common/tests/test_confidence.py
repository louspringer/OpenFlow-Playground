"""
Tests for the confidence scoring module.
"""

import pytest
from clewcrew_common.confidence import ConfidenceCalculator, ConfidenceScore


class TestConfidenceScore:
    """Test the ConfidenceScore model."""

    def test_confidence_score_creation(self):
        """Test creating a confidence score."""
        score = ConfidenceScore(
            value=0.8, factors=["test_factor"], metadata={"test": "data"}
        )
        assert score.value == 0.8
        assert score.factors == ["test_factor"]
        assert score.metadata == {"test": "data"}

    def test_confidence_score_validation(self):
        """Test confidence score validation."""
        # Should normalize values outside range
        score = ConfidenceScore(value=1.5)
        assert score.value == 1.0

        score = ConfidenceScore(value=-0.5)
        assert score.value == 0.0

        # Should accept valid values
        score = ConfidenceScore(value=0.5)
        assert score.value == 0.5


class TestConfidenceCalculator:
    """Test the ConfidenceCalculator class."""

    def test_calculate_agent_confidence_no_delusions(self):
        """Test agent confidence calculation with no delusions."""
        confidence = ConfidenceCalculator.calculate_agent_confidence([])
        assert confidence.value == 0.9
        assert "no_delusions_found" in confidence.factors

    def test_calculate_agent_confidence_with_delusions(self):
        """Test agent confidence calculation with delusions."""
        delusions = [
            {"confidence": 0.8, "severity": "high"},
            {"confidence": 0.6, "severity": "medium"},
        ]

        confidence = ConfidenceCalculator.calculate_agent_confidence(delusions)
        assert 0.0 <= confidence.value <= 1.0
        assert "high_severity_penalty" in confidence.factors
        assert "medium_severity" in confidence.factors

    def test_calculate_recovery_confidence_no_changes(self):
        """Test recovery confidence calculation with no changes."""
        confidence = ConfidenceCalculator.calculate_recovery_confidence([])
        assert confidence.value == 0.5
        assert "no_changes_made" in confidence.factors

    def test_calculate_recovery_confidence_with_changes(self):
        """Test recovery confidence calculation with changes."""
        changes = ["fix1", "fix2", "fix3"]
        confidence = ConfidenceCalculator.calculate_recovery_confidence(changes)
        assert confidence.value > 0.5
        assert "changes_successful" in confidence.factors
        assert "multiple_changes" in confidence.factors

    def test_calculate_validation_confidence_no_issues(self):
        """Test validation confidence calculation with no issues."""
        confidence = ConfidenceCalculator.calculate_validation_confidence([])
        assert confidence.value == 0.9
        assert "no_issues_found" in confidence.factors

    def test_calculate_validation_confidence_with_issues(self):
        """Test validation confidence calculation with issues."""
        issues = ["issue1", "issue2"]
        confidence = ConfidenceCalculator.calculate_validation_confidence(issues)
        assert confidence.value < 0.9
        assert "issues_found" in confidence.factors
        assert "multiple_issues" in confidence.factors

    def test_calculate_workflow_confidence(self):
        """Test workflow confidence calculation."""
        confidence = ConfidenceCalculator.calculate_workflow_confidence(
            steps_completed=3, total_steps=5, step_confidence_scores=[0.8, 0.9, 0.7]
        )
        assert 0.0 <= confidence.value <= 1.0
        assert "workflow_partially_completed" in confidence.factors

    def test_normalize_confidence(self):
        """Test confidence normalization."""
        assert ConfidenceCalculator.normalize_confidence(1.5) == 1.0
        assert ConfidenceCalculator.normalize_confidence(-0.5) == 0.0
        assert ConfidenceCalculator.normalize_confidence(0.5) == 0.5

    def test_combine_confidence_scores(self):
        """Test combining confidence scores."""
        scores = [
            ConfidenceScore(value=0.8, factors=["factor1"]),
            ConfidenceScore(value=0.6, factors=["factor2"]),
        ]

        combined = ConfidenceCalculator.combine_confidence_scores(scores)
        assert 0.0 <= combined.value <= 1.0
        assert "factor1" in combined.factors
        assert "factor2" in combined.factors
        assert combined.metadata["score_count"] == 2

    def test_combine_confidence_scores_with_weights(self):
        """Test combining confidence scores with weights."""
        scores = [
            ConfidenceScore(value=0.8, factors=["factor1"]),
            ConfidenceScore(value=0.6, factors=["factor2"]),
        ]
        weights = [0.7, 0.3]

        combined = ConfidenceCalculator.combine_confidence_scores(scores, weights)
        assert 0.0 <= combined.value <= 1.0
        assert combined.metadata["weights"] == weights

    def test_combine_confidence_scores_mismatched_weights(self):
        """Test combining confidence scores with mismatched weights."""
        scores = [
            ConfidenceScore(value=0.8, factors=["factor1"]),
            ConfidenceScore(value=0.6, factors=["factor2"]),
        ]
        weights = [0.7]  # Mismatched

        with pytest.raises(
            ValueError, match="Number of weights must match number of scores"
        ):
            ConfidenceCalculator.combine_confidence_scores(scores, weights)

    def test_combine_confidence_scores_empty(self):
        """Test combining empty confidence scores."""
        combined = ConfidenceCalculator.combine_confidence_scores([])
        assert combined.value == 0.0
        assert "no_scores_provided" in combined.factors


if __name__ == "__main__":
    pytest.main([__file__])
