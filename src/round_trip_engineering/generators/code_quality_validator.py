#!/usr/bin/env python3
"""
Code Quality & Validation
Handles code quality validation, formatting, and assurance for generated code.
"""

import logging
import re
from typing import Any, Dict, List, Tuple

from .base_reflective_module import BaseReflectiveModule


class CodeQualityValidator(BaseReflectiveModule):
    """Handles code quality validation and assurance for generated code"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "code_validation": [
                "validate_python_syntax",
                "check_code_quality",
                "identify_issues",
                "validate_generated_code",
            ],
            "code_formatting": [
                "format_code_structure",
                "ensure_consistent_style",
                "apply_black_formatting",
            ],
            "quality_metrics": [
                "calculate_complexity",
                "measure_maintainability",
                "assess_readability",
            ],
        }

    def validate_python_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Validate Python syntax and return issues found"""
        issues = []

        try:
            # Basic syntax validation
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
        except Exception as e:
            issues.append(f"Compilation error: {e}")

        # Check for common issues
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            # Check for unmatched parentheses/brackets
            if line.count("(") != line.count(")"):
                issues.append(f"Line {i}: Unmatched parentheses")
            if line.count("[") != line.count("]"):
                issues.append(f"Line {i}: Unmatched brackets")
            if line.count("{") != line.count("}"):
                issues.append(f"Line {i}: Unmatched braces")

            # Check for common syntax issues
            if line.strip().endswith(":"):
                # Check if next non-empty line is properly indented
                next_indented = False
                for j in range(i, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        if lines[j].startswith("    ") or lines[j].startswith("\t"):
                            next_indented = True
                        break

                if not next_indented and line.strip() not in [
                    "class:",
                    "def:",
                    "if:",
                    "for:",
                    "while:",
                    "try:",
                    "except:",
                    "finally:",
                    "else:",
                    "elif:",
                ]:
                    issues.append(f"Line {i}: Missing indented block after colon")

        return len(issues) == 0, issues

    def check_code_quality(self, code: str) -> Dict[str, Any]:
        """Check code quality and return metrics"""
        lines = code.split("\n")

        # Count various elements
        total_lines = len(lines)
        empty_lines = len([line for line in lines if line.strip() == ""])
        comment_lines = len([line for line in lines if line.strip().startswith("#")])
        docstring_lines = len(
            [line for line in lines if '"""' in line or "'''" in line]
        )

        # Count code elements
        class_definitions = len(
            [line for line in lines if line.strip().startswith("class ")]
        )
        function_definitions = len(
            [line for line in lines if line.strip().startswith("def ")]
        )
        import_statements = len(
            [line for line in lines if line.strip().startswith(("import ", "from "))]
        )

        # Calculate metrics
        code_lines = total_lines - empty_lines - comment_lines
        code_density = code_lines / total_lines if total_lines > 0 else 0

        # Calculate complexity metrics
        complexity_score = self._calculate_complexity_score(code)
        maintainability_score = self._calculate_maintainability_score(code)
        readability_score = self._calculate_readability_score(code)

        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "empty_lines": empty_lines,
            "comment_lines": comment_lines,
            "docstring_lines": docstring_lines,
            "class_definitions": class_definitions,
            "function_definitions": function_definitions,
            "import_statements": import_statements,
            "code_density": code_density,
            "complexity_score": complexity_score,
            "maintainability_score": maintainability_score,
            "readability_score": readability_score,
        }

    def _calculate_complexity_score(self, code: str) -> float:
        """Calculate cyclomatic complexity score"""
        complexity = 1  # Base complexity

        # Count control flow statements
        complexity += len(re.findall(r"\bif\b", code))
        complexity += len(re.findall(r"\bfor\b", code))
        complexity += len(re.findall(r"\bwhile\b", code))
        complexity += len(re.findall(r"\btry\b", code))
        complexity += len(re.findall(r"\bexcept\b", code))
        complexity += len(re.findall(r"\band\b", code))
        complexity += len(re.findall(r"\bor\b", code))

        return complexity

    def _calculate_maintainability_score(self, code: str) -> float:
        """Calculate maintainability index score"""
        lines = code.split("\n")
        total_lines = len(lines)

        if total_lines == 0:
            return 100.0

        # Count various maintainability factors
        long_lines = len([line for line in lines if len(line) > 80])
        complex_functions = len(re.findall(r"def\s+\w+\([^)]*\):", code))
        nested_structures = len(re.findall(r"^\s+", code, re.MULTILINE))

        # Calculate score (higher is better)
        score = 100.0
        score -= (long_lines / total_lines) * 20
        score -= (complex_functions / total_lines) * 15
        score -= (nested_structures / total_lines) * 10

        return max(0.0, min(100.0, score))

    def _calculate_readability_score(self, code: str) -> float:
        """Calculate readability score"""
        lines = code.split("\n")
        total_lines = len(lines)

        if total_lines == 0:
            return 100.0

        # Count readability factors
        short_lines = len([line for line in lines if len(line) <= 80])
        well_commented = len([line for line in lines if line.strip().startswith("#")])
        clear_names = len(re.findall(r"[a-z_][a-z0-9_]*", code))

        # Calculate score
        score = 100.0
        score += (short_lines / total_lines) * 20
        score += (well_commented / total_lines) * 15
        score += (clear_names / total_lines) * 10

        return max(0.0, min(100.0, score))

    def identify_issues(self, code: str) -> List[Dict[str, Any]]:
        """Identify potential issues in the code"""
        issues = []

        # Check syntax
        is_valid, syntax_issues = self.validate_python_syntax(code)
        if not is_valid:
            for issue in syntax_issues:
                issues.append(
                    {
                        "type": "syntax_error",
                        "severity": "high",
                        "message": issue,
                        "line": None,
                    }
                )

        # Check code quality
        quality_metrics = self.check_code_quality(code)

        # Identify potential issues based on metrics
        if quality_metrics["code_density"] < 0.5:
            issues.append(
                {
                    "type": "low_code_density",
                    "severity": "medium",
                    "message": f"Code density is low ({quality_metrics['code_density']:.2f})",
                    "line": None,
                }
            )

        if quality_metrics["complexity_score"] > 10:
            issues.append(
                {
                    "type": "high_complexity",
                    "severity": "medium",
                    "message": f"Code complexity is high ({quality_metrics['complexity_score']})",
                    "line": None,
                }
            )

        if quality_metrics["maintainability_score"] < 50:
            issues.append(
                {
                    "type": "low_maintainability",
                    "severity": "medium",
                    "message": f"Maintainability score is low ({quality_metrics['maintainability_score']:.1f})",
                    "line": None,
                }
            )

        return issues

    def validate_generated_code(self, code: str) -> Dict[str, Any]:
        """Comprehensive validation of generated code"""
        validation_result = {
            "is_valid": True,
            "issues": [],
            "metrics": {},
            "recommendations": [],
        }

        # Syntax validation
        is_syntax_valid, syntax_issues = self.validate_python_syntax(code)
        if not is_syntax_valid:
            validation_result["is_valid"] = False
            validation_result["issues"].extend(syntax_issues)

        # Quality assessment
        quality_metrics = self.check_code_quality(code)
        validation_result["metrics"] = quality_metrics

        # Issue identification
        issues = self.identify_issues(code)
        validation_result["issues"].extend(issues)

        # Generate recommendations
        if quality_metrics["complexity_score"] > 8:
            validation_result["recommendations"].append(
                "Consider breaking down complex functions into smaller, focused functions"
            )

        if quality_metrics["maintainability_score"] < 60:
            validation_result["recommendations"].append(
                "Improve code structure and reduce nesting for better maintainability"
            )

        if quality_metrics["readability_score"] < 70:
            validation_result["recommendations"].append(
                "Add more comments and improve variable naming for better readability"
            )

        return validation_result

    def format_code_structure(self, code: str) -> str:
        """Format code structure for better readability"""
        lines = code.split("\n")
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            # Handle indentation changes
            if stripped.startswith("class ") or stripped.startswith("def "):
                # Reset indentation for top-level definitions
                indent_level = 0
            elif stripped.endswith(":"):
                # Increase indentation after colons
                formatted_lines.append("    " * indent_level + stripped)
                indent_level += 1
                continue
            elif stripped.startswith("return ") or stripped.startswith("pass"):
                # Decrease indentation for return/pass statements
                indent_level = max(0, indent_level - 1)

            # Apply current indentation
            if stripped:
                formatted_lines.append("    " * indent_level + stripped)
            else:
                formatted_lines.append("")

        return "\n".join(formatted_lines)

    def ensure_consistent_style(self, code: str) -> str:
        """Ensure consistent code style throughout"""
        # Normalize line endings
        code = code.replace("\r\n", "\n").replace("\r", "\n")

        # Ensure consistent indentation (4 spaces)
        lines = code.split("\n")
        normalized_lines = []

        for line in lines:
            if line.strip():  # Skip empty lines
                # Convert tabs to spaces
                line = line.expandtabs(4)

                # Ensure proper indentation
                stripped = line.strip()
                if stripped:
                    # Count leading spaces
                    leading_spaces = len(line) - len(line.lstrip())
                    # Normalize to 4-space increments
                    normalized_indent = (leading_spaces // 4) * 4
                    normalized_lines.append(" " * normalized_indent + stripped)
                else:
                    normalized_lines.append("")
            else:
                normalized_lines.append("")

        return "\n".join(normalized_lines)

    def apply_black_formatting(self, code: str) -> str:
        """Apply Black code formatting if available"""
        try:
            from black import FileMode, format_str

            # Format the code using Black
            formatted_code = format_str(code, mode=FileMode())
            self.logger.info("✅ Applied Black formatting")
            return formatted_code
        except ImportError:
            self.logger.warning("Black not available, using basic formatting")
            # Fall back to basic formatting
            return self.ensure_consistent_style(code)
