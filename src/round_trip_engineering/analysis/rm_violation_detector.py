#!/usr/bin/env python3
"""
RM Violation Detector - Analyzes code for Reflective Module compliance.
"""

import ast
import logging
from typing import Dict, List, Any, Optional, Union, Literal
from dataclasses import dataclass, asdict
from enum import Enum
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class ViolationSeverity(str, Enum):
    """Severity levels for RM violations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RMViolation:
    """Represents a single RM violation."""

    violation_type: str
    severity: ViolationSeverity
    description: str
    line_number: Optional[int] = None
    suggestion: str = ""
    requires_human_judgment: bool = False
    confidence: float = 0.0


@dataclass
class RefactoringSuggestion:
    """Represents a refactoring suggestion."""

    original_file: str
    new_files: List[str]
    description: str
    confidence: float
    requires_human_judgment: bool = False
    reasoning: str = ""


# Pydantic models for clear type safety
class ViolationData(BaseModel):
    """Pydantic model for violation data."""

    violation_type: str = Field(..., description="Type of violation")
    severity: ViolationSeverity = Field(..., description="Severity level")
    description: str = Field(..., description="Description of violation")
    line_number: Optional[int] = Field(None, description="Line number where violation occurs")
    suggestion: str = Field("", description="Suggested fix")
    requires_human_judgment: bool = Field(False, description="Whether human judgment is required")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence level (0.0-1.0)")


class SuggestionData(BaseModel):
    """Pydantic model for suggestion data."""

    original_file: str = Field(..., description="Original file path")
    new_files: List[str] = Field(..., description="List of new files to create")
    description: str = Field(..., description="Description of refactoring")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence level (0.0-1.0)")
    requires_human_judgment: bool = Field(False, description="Whether human judgment is required")
    reasoning: str = Field("", description="Reasoning for suggestion")


class ErrorData(BaseModel):
    """Pydantic model for error data."""

    file: str = Field(..., description="File that caused error")
    error: str = Field(..., description="Error message")
    severity: Literal["critical", "high", "medium", "low"] = Field("critical", description="Error severity")


class AnalysisResult(BaseModel):
    """Pydantic model for a single analysis result."""

    type: Literal["violation", "suggestion", "error"] = Field(..., description="Type of result")
    data: Union[ViolationData, SuggestionData, ErrorData] = Field(..., description="Result data")


class RMViolationDetector:
    """Detects RM violations and suggests refactoring."""

    def __init__(self):
        self.violations: List[RMViolation] = []
        self.suggestions: List[RefactoringSuggestion] = []

    def analyze_file(self, file_path: str) -> List[AnalysisResult]:
        """
        Analyze a file for RM violations.

        Args:
            file_path: Path to the file to analyze

        Returns:
            List of AnalysisResult objects with clear type safety.

        Example:
            results = detector.analyze_file("my_file.py")
            for result in results:
                if result.type == "violation":
                    print(f"Violation: {result.data.description}")
                elif result.type == "suggestion":
                    print(f"Suggestion: {result.data.description}")
                elif result.type == "error":
                    print(f"Error: {result.data.error}")
        """
        try:
            with open(file_path, "r") as f:
                content = f.read()

            tree = ast.parse(content)
            self.violations.clear()
            self.suggestions.clear()

            # Analyze the AST
            self._analyze_ast(tree, file_path)

            # Generate suggestions
            self._generate_suggestions(file_path)

            # Return as list of AnalysisResult objects
            results: List[AnalysisResult] = []

            # Add violations
            for violation in self.violations:
                violation_data = ViolationData(
                    violation_type=violation.violation_type,
                    severity=violation.severity,
                    description=violation.description,
                    line_number=violation.line_number,
                    suggestion=violation.suggestion,
                    requires_human_judgment=violation.requires_human_judgment,
                    confidence=violation.confidence,
                )
                results.append(AnalysisResult(type="violation", data=violation_data))

            # Add suggestions
            for suggestion in self.suggestions:
                suggestion_data = SuggestionData(
                    original_file=suggestion.original_file,
                    new_files=suggestion.new_files,
                    description=suggestion.description,
                    confidence=suggestion.confidence,
                    requires_human_judgment=suggestion.requires_human_judgment,
                    reasoning=suggestion.reasoning,
                )
                results.append(AnalysisResult(type="suggestion", data=suggestion_data))

            return results

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            error_data = ErrorData(file=file_path, error=str(e), severity="critical")
            return [AnalysisResult(type="error", data=error_data)]

    def _analyze_ast(self, tree: ast.AST, file_path: str) -> None:
        """Analyze AST for RM violations."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, file_path)
            elif isinstance(node, ast.FunctionDef):
                self._analyze_function(node, file_path)

    def _analyze_class(self, node: ast.ClassDef, file_path: str) -> None:
        """Analyze a class for RM violations."""
        # Count methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]

        # Check method count violation
        if len(methods) > 10:
            self.violations.append(
                RMViolation(
                    violation_type="method_count",
                    severity=ViolationSeverity.HIGH,
                    description=f"Class '{node.name}' has {len(methods)} methods (max 10)",
                    line_number=node.lineno,
                    suggestion="Consider splitting into smaller classes",
                    requires_human_judgment=True,
                    confidence=0.8,
                )
            )

        # Check for multiple responsibilities
        method_names = [m.name for m in methods]
        if self._has_multiple_responsibilities(method_names):
            self.violations.append(
                RMViolation(
                    violation_type="multiple_responsibilities",
                    severity=ViolationSeverity.CRITICAL,
                    description=f"Class '{node.name}' appears to have multiple responsibilities",
                    line_number=node.lineno,
                    suggestion="Split into focused classes with single responsibilities",
                    requires_human_judgment=True,
                    confidence=0.9,
                )
            )

    def _analyze_function(self, node: ast.FunctionDef, file_path: str) -> None:
        """Analyze a function for RM violations."""
        # Check function length
        if hasattr(node, "end_lineno") and node.end_lineno:
            length = node.end_lineno - node.lineno
            if length > 50:
                self.violations.append(
                    RMViolation(
                        violation_type="function_length",
                        severity=ViolationSeverity.MEDIUM,
                        description=f"Function '{node.name}' is {length} lines long (max 50)",
                        line_number=node.lineno,
                        suggestion="Consider breaking into smaller functions",
                        requires_human_judgment=False,
                        confidence=0.7,
                    )
                )

    def _has_multiple_responsibilities(self, method_names: List[str]) -> bool:
        """Check if method names suggest multiple responsibilities."""
        # Simple heuristic - look for different "domains" in method names
        domains = {
            "ui": ["render", "display", "show", "gui", "ui", "widget"],
            "data": ["process", "parse", "load", "save", "data"],
            "analysis": ["analyze", "compute", "calculate", "statistics"],
            "network": ["fetch", "request", "api", "http", "network"],
        }

        found_domains = set()
        for name in method_names:
            name_lower = name.lower()
            for domain, keywords in domains.items():
                if any(keyword in name_lower for keyword in keywords):
                    found_domains.add(domain)

        return len(found_domains) > 2

    def _generate_suggestions(self, file_path: str) -> None:
        """Generate refactoring suggestions."""
        if not self.violations:
            return

        # Group violations by class
        class_violations: Dict[str, List[RMViolation]] = {}
        for violation in self.violations:
            if violation.line_number:
                # This is a simplified approach - in reality you'd need to map line numbers to classes
                class_violations.setdefault("main_class", []).append(violation)

        # Generate suggestions for each class
        for class_name, violations in class_violations.items():
            if any(v.severity in [ViolationSeverity.HIGH, ViolationSeverity.CRITICAL] for v in violations):
                self.suggestions.append(
                    RefactoringSuggestion(
                        original_file=file_path,
                        new_files=[f"{file_path.replace('.py', '')}_refactored.py"],
                        description=f"Refactor {class_name} to address RM violations",
                        confidence=0.8,
                        requires_human_judgment=True,
                        reasoning="Multiple high-severity violations detected",
                    )
                )
