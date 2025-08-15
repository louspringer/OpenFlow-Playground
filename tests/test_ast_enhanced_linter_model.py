#!/usr/bin/env python3
"""
Test-Driven Development Suite for AST-Enhanced Linter Model

This test suite validates the domain model and ensures it behaves correctly
before implementing the actual linter functionality.

Test Strategy:
1. Test model creation and initialization
2. Test analysis rule configuration
3. Test transformation rule setup
4. Test quality threshold validation
5. Test AST analysis capabilities
6. Test auto-fix capabilities
"""

import ast

# Import the model we're testing
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from ast_enhanced_linter_model import (
    AnalysisStrategy,
    ASTAnalysisResult,
    ASTAnalysisRule,
    ASTEnhancedLinterModel,
    AutoFixCapability,
    CodeQualityMetric,
    IssueSeverity,
    IssueType,
    TransformationRule,
    create_ast_enhanced_linter_model,
)


class TestASTEnhancedLinterModel:
    """Test suite for the AST-Enhanced Linter Model"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.model = create_ast_enhanced_linter_model()

    def test_model_creation(self):
        """Test that the model can be created successfully"""
        assert self.model is not None
        assert isinstance(self.model, ASTEnhancedLinterModel)

    def test_analysis_rules_initialization(self):
        """Test that analysis rules are properly initialized"""
        assert len(self.model.analysis_rules) > 0

        # Check that we have rules for each strategy
        strategies = [rule.strategy for rule in self.model.analysis_rules]
        assert AnalysisStrategy.SYNTAX_VALIDATION in strategies
        assert AnalysisStrategy.IMPORT_ANALYSIS in strategies
        assert AnalysisStrategy.FUNCTION_ANALYSIS in strategies
        assert AnalysisStrategy.COMPLEXITY_ANALYSIS in strategies
        assert AnalysisStrategy.CODE_SMELL_DETECTION in strategies

    def test_transformation_rules_initialization(self):
        """Test that transformation rules are properly initialized"""
        assert len(self.model.transformation_rules) > 0

        # Check that we have transformation rules for key issue types
        issue_types = [rule.issue_type for rule in self.model.transformation_rules]
        assert IssueType.MULTIPLE_IMPORTS in issue_types
        assert IssueType.UNUSED_IMPORT in issue_types
        assert IssueType.DEEPLY_NESTED_CALL in issue_types

    def test_quality_thresholds_initialization(self):
        """Test that quality thresholds are properly initialized"""
        assert len(self.model.quality_thresholds) > 0

        # Check key thresholds
        assert "function_length" in self.model.quality_thresholds
        assert "class_length" in self.model.quality_thresholds
        assert "nesting_depth" in self.model.quality_thresholds
        assert "cyclomatic_complexity" in self.model.quality_thresholds

        # Check threshold values are reasonable
        assert self.model.quality_thresholds["function_length"] == 20.0
        assert self.model.quality_thresholds["line_length"] == 88.0

    def test_get_rules_for_strategy(self):
        """Test getting rules for a specific analysis strategy"""
        import_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.IMPORT_ANALYSIS
        )
        assert len(import_rules) > 0

        # All returned rules should be for import analysis
        for rule in import_rules:
            assert rule.strategy == AnalysisStrategy.IMPORT_ANALYSIS

    def test_get_rules_for_issue_type(self):
        """Test getting rules for a specific issue type"""
        multiple_imports_rules = self.model.get_rules_for_issue_type(
            IssueType.MULTIPLE_IMPORTS
        )
        assert len(multiple_imports_rules) > 0

        # All returned rules should be for multiple imports
        for rule in multiple_imports_rules:
            assert rule.issue_type == IssueType.MULTIPLE_IMPORTS

    def test_get_auto_fixable_rules(self):
        """Test getting rules that can be auto-fixed"""
        auto_fixable_rules = self.model.get_auto_fixable_rules()
        assert len(auto_fixable_rules) > 0

        # All returned rules should be auto-fixable
        for rule in auto_fixable_rules:
            assert rule.auto_fix in [
                AutoFixCapability.CAN_FIX,
                AutoFixCapability.CAN_PARTIALLY_FIX,
            ]

    def test_import_analysis_rules(self):
        """Test that import analysis rules are properly configured"""
        import_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.IMPORT_ANALYSIS
        )

        # Check for multiple imports rule
        multiple_imports_rule = next(
            (
                rule
                for rule in import_rules
                if rule.issue_type == IssueType.MULTIPLE_IMPORTS
            ),
            None,
        )
        assert multiple_imports_rule is not None
        assert multiple_imports_rule.auto_fix == AutoFixCapability.CAN_FIX
        assert multiple_imports_rule.severity == IssueSeverity.WARNING

        # Check for unused import rule
        unused_import_rule = next(
            (
                rule
                for rule in import_rules
                if rule.issue_type == IssueType.UNUSED_IMPORT
            ),
            None,
        )
        assert unused_import_rule is not None
        assert unused_import_rule.auto_fix == AutoFixCapability.CAN_FIX

    def test_function_analysis_rules(self):
        """Test that function analysis rules are properly configured"""
        function_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.FUNCTION_ANALYSIS
        )

        # Check for missing docstring rule
        missing_docstring_rule = next(
            (
                rule
                for rule in function_rules
                if rule.issue_type == IssueType.MISSING_DOCSTRING
            ),
            None,
        )
        assert missing_docstring_rule is not None
        assert missing_docstring_rule.auto_fix == AutoFixCapability.CANNOT_FIX
        assert missing_docstring_rule.severity == IssueSeverity.SUGGESTION

        # Check for function too long rule
        function_too_long_rule = next(
            (
                rule
                for rule in function_rules
                if rule.issue_type == IssueType.FUNCTION_TOO_LONG
            ),
            None,
        )
        assert function_too_long_rule is not None
        assert function_too_long_rule.threshold == 20.0

    def test_complexity_analysis_rules(self):
        """Test that complexity analysis rules are properly configured"""
        complexity_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.COMPLEXITY_ANALYSIS
        )

        # Check for deeply nested call rule
        deeply_nested_rule = next(
            (
                rule
                for rule in complexity_rules
                if rule.issue_type == IssueType.DEEPLY_NESTED_CALL
            ),
            None,
        )
        assert deeply_nested_rule is not None
        assert deeply_nested_rule.threshold == 3.0
        assert deeply_nested_rule.auto_fix == AutoFixCapability.CAN_PARTIALLY_FIX

    def test_code_smell_detection_rules(self):
        """Test that code smell detection rules are properly configured"""
        code_smell_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.CODE_SMELL_DETECTION
        )

        # Check for magic numbers rule
        magic_numbers_rule = next(
            (
                rule
                for rule in code_smell_rules
                if rule.issue_type == IssueType.MAGIC_NUMBERS
            ),
            None,
        )
        assert magic_numbers_rule is not None
        assert magic_numbers_rule.auto_fix == AutoFixCapability.CANNOT_FIX

    def test_condition_methods(self):
        """Test that condition methods work correctly"""
        # Test multiple imports condition
        mock_import_node = Mock()
        mock_import_node.names = ["os", "sys", "json"]
        assert self.model._has_multiple_imports(mock_import_node) is True

        mock_single_import_node = Mock()
        mock_single_import_node.names = ["os"]
        assert self.model._has_multiple_imports(mock_single_import_node) is False

    def test_wildcard_import_detection(self):
        """Test wildcard import detection"""
        mock_wildcard_node = Mock()
        mock_wildcard_node.names = [Mock()]
        mock_wildcard_node.names[0].name = "*"
        assert self.model._is_wildcard_import(mock_wildcard_node) is True

        mock_specific_node = Mock()
        mock_specific_node.names = [Mock()]
        mock_specific_node.names[0].name = "os"
        assert self.model._is_wildcard_import(mock_specific_node) is False

    def test_function_length_analysis(self):
        """Test function length analysis"""
        mock_function_node = Mock()
        mock_function_node.body = [Mock()] * 25  # 25 lines

        assert self.model._is_function_too_long(mock_function_node) is True

        mock_short_function_node = Mock()
        mock_short_function_node.body = [Mock()] * 15  # 15 lines

        assert self.model._is_function_too_long(mock_short_function_node) is False

    def test_magic_number_detection(self):
        """Test magic number detection"""
        # Test magic numbers
        for magic_num in [42, 100, 1000, -5]:
            mock_num_node = Mock()
            mock_num_node.n = magic_num
            assert self.model._is_magic_number(mock_num_node) is True

        # Test non-magic numbers
        for non_magic_num in [0, 1, -1]:
            mock_num_node = Mock()
            mock_num_node.n = non_magic_num
            assert self.model._is_magic_number(mock_num_node) is False

    def test_hardcoded_string_detection(self):
        """Test hardcoded string detection"""
        # Test long strings (potential hardcoded values)
        mock_long_string_node = Mock()
        mock_long_string_node.s = "This is a very long string that might be hardcoded"
        assert self.model._is_hardcoded_string(mock_long_string_node) is True

        # Test short strings (likely not hardcoded)
        mock_short_string_node = Mock()
        mock_short_string_node.s = "short"
        assert self.model._is_hardcoded_string(mock_short_string_node) is False

    def test_transformation_rule_validation(self):
        """Test that transformation rules have proper validation methods"""
        for rule in self.model.transformation_rules:
            assert hasattr(rule, "validation")
            assert callable(rule.validation)
            assert hasattr(rule, "ast_transformer")
            assert callable(rule.ast_transformer)

    def test_rollback_capabilities(self):
        """Test that transformation rules have rollback capabilities"""
        for rule in self.model.transformation_rules:
            if rule.rollback is not None:
                assert callable(rule.rollback)

    def test_quality_threshold_consistency(self):
        """Test that quality thresholds are consistent and reasonable"""
        thresholds = self.model.quality_thresholds

        # Function length should be reasonable
        assert 10 <= thresholds["function_length"] <= 50

        # Class length should be reasonable
        assert 100 <= thresholds["class_length"] <= 500

        # Nesting depth should be reasonable
        assert 2 <= thresholds["nesting_depth"] <= 5

        # Line length should match common standards
        assert thresholds["line_length"] in [79, 88, 100, 120]

    def test_ast_node_type_consistency(self):
        """Test that AST node types in rules are valid"""
        for rule in self.model.analysis_rules:
            for node_type in rule.ast_node_types:
                # Check that the node type is a valid AST node type
                assert issubclass(node_type, ast.AST)

    def test_rule_severity_consistency(self):
        """Test that rule severities are appropriate for their issue types"""
        for rule in self.model.analysis_rules:
            # Syntax errors should be critical
            if rule.issue_type == IssueType.SYNTAX_ERROR:
                assert rule.severity == IssueSeverity.CRITICAL

            # Import issues should be warnings or suggestions
            if rule.issue_type in [IssueType.MULTIPLE_IMPORTS, IssueType.UNUSED_IMPORT]:
                assert rule.severity in [
                    IssueSeverity.WARNING,
                    IssueSeverity.SUGGESTION,
                ]

            # Code smell issues should be suggestions
            if rule.issue_type in [
                IssueType.MAGIC_NUMBERS,
                IssueType.HARDCODED_STRINGS,
            ]:
                assert rule.severity == IssueSeverity.SUGGESTION


class TestASTAnalysisResult:
    """Test suite for AST Analysis Result data structure"""

    def test_ast_analysis_result_creation(self):
        """Test creating an AST analysis result"""
        file_path = Path("test_file.py")
        result = ASTAnalysisResult(
            file_path=file_path,
            syntax_valid=True,
            syntax_errors=[],
            issues=[],
            metrics=[],
            ast_tree=None,
            analysis_time=0.1,
        )

        assert result.file_path == file_path
        assert result.syntax_valid is True
        assert len(result.syntax_errors) == 0
        assert len(result.issues) == 0
        assert len(result.metrics) == 0
        assert result.analysis_time == 0.1


class TestCodeQualityMetric:
    """Test suite for Code Quality Metric data structure"""

    def test_code_quality_metric_creation(self):
        """Test creating a code quality metric"""
        metric = CodeQualityMetric(
            name="function_length",
            value=15.0,
            unit="lines",
            threshold=20.0,
            is_good=True,
            description="Function length in lines",
        )

        assert metric.name == "function_length"
        assert metric.value == 15.0
        assert metric.unit == "lines"
        assert metric.threshold == 20.0
        assert metric.is_good is True
        assert metric.description == "Function length in lines"

    def test_code_quality_metric_threshold_validation(self):
        """Test that metrics can validate against thresholds"""
        metric = CodeQualityMetric(
            name="function_length",
            value=25.0,
            unit="lines",
            threshold=20.0,
            is_good=False,
            description="Function exceeds threshold",
        )

        assert metric.value > metric.threshold
        assert metric.is_good is False


class TestTransformationRule:
    """Test suite for Transformation Rule data structure"""

    def test_transformation_rule_creation(self):
        """Test creating a transformation rule"""

        def mock_transformer(tree):
            return tree

        def mock_validator(original, transformed):
            return True

        rule = TransformationRule(
            name="Test Transformation",
            issue_type=IssueType.MULTIPLE_IMPORTS,
            description="Test transformation rule",
            ast_transformer=mock_transformer,
            validation=mock_validator,
            rollback=None,
        )

        assert rule.name == "Test Transformation"
        assert rule.issue_type == IssueType.MULTIPLE_IMPORTS
        assert callable(rule.ast_transformer)
        assert callable(rule.validation)
        assert rule.rollback is None


class TestModelIntegration:
    """Test suite for model integration and real-world scenarios"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.model = create_ast_enhanced_linter_model()

    def test_model_with_real_python_code(self):
        """Test the model with actual Python code"""
        python_code = """
import os, sys, json

def long_function_with_many_lines():
    # This function is intentionally long to test our analysis
    line1 = "This is line 1"
    line2 = "This is line 2"
    line3 = "This is line 3"
    line4 = "This is line 4"
    line5 = "This is line 5"
    line6 = "This is line 6"
    line7 = "This is line 7"
    line8 = "This is line 8"
    line9 = "This is line 9"
    line10 = "This is line 10"
    line11 = "This is line 11"
    line12 = "This is line 12"
    line13 = "This is line 13"
    line14 = "This is line 14"
    line15 = "This is line 15"
    line16 = "This is line 16"
    line17 = "This is line 17"
    line18 = "This is line 18"
    line19 = "This is line 19"
    line20 = "This is line 20"
    line21 = "This is line 21"
    return line1 + line2 + line3

class TestClass:
    def __init__(self):
        self.value = 42  # Magic number!
        self.config = "hardcoded configuration string that is very long"

    def method_without_docstring(self):
        pass
"""

        # Parse the code
        try:
            ast.parse(python_code)

            # Test that we can identify various issues
            import_rules = self.model.get_rules_for_strategy(
                AnalysisStrategy.IMPORT_ANALYSIS
            )
            function_rules = self.model.get_rules_for_strategy(
                AnalysisStrategy.FUNCTION_ANALYSIS
            )
            code_smell_rules = self.model.get_rules_for_strategy(
                AnalysisStrategy.CODE_SMELL_DETECTION
            )

            # We should have rules for the issues in our test code
            assert len(import_rules) > 0
            assert len(function_rules) > 0
            assert len(code_smell_rules) > 0

        except SyntaxError:
            pytest.fail("Test Python code should be syntactically valid")

    def test_model_extensibility(self):
        """Test that the model can be extended with new rules"""
        # Create a custom rule
        custom_rule = ASTAnalysisRule(
            name="Custom Test Rule",
            strategy=AnalysisStrategy.PATTERN_ANALYSIS,
            issue_type=IssueType.ONE_LINER_DETECTED,
            severity=IssueSeverity.WARNING,
            auto_fix=AutoFixCapability.CAN_FIX,
            description="Custom test rule for extensibility",
            suggestion="This is a test rule",
            ast_node_types=[ast.Expr],
            conditions=[lambda node: True],
            fix_strategy=lambda node: None,
        )

        # Add the custom rule
        self.model.analysis_rules.append(custom_rule)

        # Verify it was added
        assert custom_rule in self.model.analysis_rules

        # Verify we can retrieve it
        pattern_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.PATTERN_ANALYSIS
        )
        assert custom_rule in pattern_rules


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
