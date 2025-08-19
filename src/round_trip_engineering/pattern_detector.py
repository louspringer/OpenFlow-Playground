#!/usr/bin/env python3
"""
Pattern Detection System for Round-Trip Engineering

Purpose: Detect coding patterns and transform them into best practices
"""

import ast
from dataclasses import dataclass
from typing import Any


@dataclass
class CodePattern:
    """Represents a detected code pattern"""

    pattern_type: str
    original_code: str
    transformed_code: str
    description: str
    best_practice: str
    line_number: int
    confidence: float


@dataclass
class PatternTransformation:
    """Represents a pattern transformation rule"""

    pattern_type: str
    detection_pattern: str
    transformation_rule: str
    best_practice: str
    examples: list[str]


class PatternDetector:
    """Detects coding patterns and suggests transformations"""

    def __init__(self):
        self.patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> dict[str, PatternTransformation]:
        """Initialize known coding patterns"""
        return {
            "exception_string_literal": PatternTransformation(
                pattern_type="exception_string_literal",
                detection_pattern="raise ExceptionType('message')",
                transformation_rule="Assign message to variable first",
                best_practice="Exception messages should be assigned to variables before raising",
                examples=[
                    "raise ValueError('No credential mappings found')",
                    "raise FileNotFoundError(f'Model file not found: {path}')",
                ],
            ),
            "exception_f_string": PatternTransformation(
                pattern_type="exception_f_string",
                detection_pattern="raise ExceptionType(f'message {variable}')",
                transformation_rule="Assign f-string to variable first",
                best_practice="F-string exception messages should be assigned to variables",
                examples=[
                    "raise FileNotFoundError(f'Model file not found: {self.model_file}')"
                ],
            ),
            "hardcoded_credentials": PatternTransformation(
                pattern_type="hardcoded_credentials",
                detection_pattern="password = 'secret' or username = 'admin'",
                transformation_rule="Use environment variables or secure parameter stores",
                best_practice="Never hardcode credentials in source code",
                examples=["password = 'my_secret_password'", "username = 'admin'"],
            ),
            "unused_imports": PatternTransformation(
                pattern_type="unused_imports",
                detection_pattern="import module but module not used",
                transformation_rule="Remove unused imports or add noqa directive",
                best_practice="Only import what you actually use",
                examples=["from typing import Dict, List, Any  # Only use Any"],
            ),
        }

    def detect_patterns_in_node(
        self, node: ast.AST, source_lines: list[str]
    ) -> list[CodePattern]:
        """Detect patterns in an AST node"""
        patterns = []

        if isinstance(node, ast.Raise):
            patterns.extend(self._detect_exception_patterns(node, source_lines))
        elif isinstance(node, ast.Assign):
            patterns.extend(self._detect_assignment_patterns(node, source_lines))
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            patterns.extend(self._detect_import_patterns(node, source_lines))

        return patterns

    def _detect_exception_patterns(
        self, node: ast.Raise, source_lines: list[str]
    ) -> list[CodePattern]:
        """Detect exception-related patterns"""
        patterns = []

        if node.exc and isinstance(node.exc, ast.Call):
            # Check for string literal exceptions
            if (
                node.exc.args
                and len(node.exc.args) == 1
                and isinstance(node.exc.args[0], ast.Constant)
                and isinstance(node.exc.args[0].value, str)
            ):
                # EM101: Exception must not use a string literal
                original_code = source_lines[node.lineno - 1].strip()
                transformed_code = self._transform_exception_string_literal(
                    original_code, node.exc.args[0].value
                )

                patterns.append(
                    CodePattern(
                        pattern_type="exception_string_literal",
                        original_code=original_code,
                        transformed_code=transformed_code,
                        description="Exception uses string literal directly",
                        best_practice="Assign message to variable first",
                        line_number=node.lineno,
                        confidence=0.95,
                    )
                )

            # Check for f-string exceptions
            elif (
                node.exc.args
                and len(node.exc.args) == 1
                and isinstance(node.exc.args[0], ast.JoinedStr)
            ):
                # EM102: Exception must not use an f-string literal
                original_code = source_lines[node.lineno - 1].strip()
                transformed_code = self._transform_exception_f_string(
                    original_code, node.exc.args[0]
                )

                patterns.append(
                    CodePattern(
                        pattern_type="exception_f_string",
                        original_code=original_code,
                        transformed_code=transformed_code,
                        description="Exception uses f-string directly",
                        best_practice="Assign f-string to variable first",
                        line_number=node.lineno,
                        confidence=0.95,
                    )
                )

        return patterns

    def _detect_assignment_patterns(
        self, node: ast.Assign, source_lines: list[str]
    ) -> list[CodePattern]:
        """Detect assignment-related patterns"""
        patterns = []

        # Check for hardcoded credentials
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.lower() in [
                "password",
                "username",
                "secret",
                "key",
                "token",
            ]:
                if (
                    node.value
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and len(node.value.value) > 5
                ):  # Likely not a placeholder
                    original_code = source_lines[node.lineno - 1].strip()
                    transformed_code = self._transform_hardcoded_credential(
                        original_code, target.id
                    )

                    patterns.append(
                        CodePattern(
                            pattern_type="hardcoded_credentials",
                            original_code=original_code,
                            transformed_code=transformed_code,
                            description=f"Hardcoded {target.id} detected",
                            best_practice="Use environment variables or secure parameter stores",
                            line_number=node.lineno,
                            confidence=0.90,
                        )
                    )

        return patterns

    def _detect_import_patterns(
        self, node: ast.Import, source_lines: list[str]
    ) -> list[CodePattern]:
        """Detect import-related patterns"""
        patterns = []

        # This would require analyzing the entire file to see if imports are used
        # For now, we'll just note the pattern
        original_code = source_lines[node.lineno - 1].strip()

        patterns.append(
            CodePattern(
                pattern_type="import_analysis_needed",
                original_code=original_code,
                transformed_code=original_code,  # No transformation yet
                description="Import statement - usage analysis needed",
                best_practice="Ensure imports are actually used",
                line_number=node.lineno,
                confidence=0.50,
            )
        )

        return patterns

    def _transform_exception_string_literal(
        self, original_code: str, message: str
    ) -> str:
        """Transform exception string literal to variable assignment"""
        # Extract the exception type and message
        if "raise" in original_code and "(" in original_code:
            parts = original_code.split("(")
            if len(parts) >= 2:
                exception_type = parts[0].replace("raise", "").strip()
                message_part = parts[1].rstrip(")")

                # Create the transformation
                var_name = "error_msg"
                transformed = f"    {var_name} = {message_part}\n    raise {exception_type}({var_name})"
                return transformed

        return original_code

    def _transform_exception_f_string(
        self, original_code: str, f_string_node: ast.JoinedStr
    ) -> str:
        """Transform exception f-string to variable assignment"""
        # Extract the exception type
        if "raise" in original_code and "(" in original_code:
            parts = original_code.split("(")
            if len(parts) >= 2:
                exception_type = parts[0].replace("raise", "").strip()

                # Create the transformation
                var_name = "error_msg"
                # We'd need to reconstruct the f-string from the AST
                # For now, use a placeholder
                transformed = f"    {var_name} = f'...'  # Extract f-string content\n    raise {exception_type}({var_name})"
                return transformed

        return original_code

    def _transform_hardcoded_credential(
        self, original_code: str, credential_type: str
    ) -> str:
        """Transform hardcoded credential to environment variable"""
        if "=" in original_code:
            parts = original_code.split("=")
            if len(parts) >= 2:
                var_name = parts[0].strip()
                env_var_name = f"{credential_type.upper()}"
                transformed = f"{var_name} = os.getenv('{env_var_name}', '')"
                return transformed

        return original_code

    def get_pattern_summary(self, patterns: list[CodePattern]) -> dict[str, Any]:
        """Get a summary of detected patterns"""
        if not patterns:
            return {"total_patterns": 0, "patterns_by_type": {}}

        patterns_by_type = {}
        for pattern in patterns:
            if pattern.pattern_type not in patterns_by_type:
                patterns_by_type[pattern.pattern_type] = []
            patterns_by_type[pattern.pattern_type].append(pattern)

        return {
            "total_patterns": len(patterns),
            "patterns_by_type": patterns_by_type,
            "confidence_avg": sum(p.confidence for p in patterns) / len(patterns),
            "lines_affected": list(set(p.line_number for p in patterns)),
        }


def main():
    """Test the pattern detector"""
    # Example usage
    detector = PatternDetector()

    # Test with a simple AST node
    test_code = """
def test_function():
    raise ValueError("No credential mappings found")
    raise FileNotFoundError(f"Model file not found: {self.model_file}")
    password = "my_secret_password"
"""

    tree = ast.parse(test_code)

    # Simulate source lines
    source_lines = test_code.split("\n")

    all_patterns = []
    for node in ast.walk(tree):
        patterns = detector.detect_patterns_in_node(node, source_lines)
        all_patterns.extend(patterns)

    summary = detector.get_pattern_summary(all_patterns)
    print("Pattern Detection Results:")
    print(f"Total patterns: {summary['total_patterns']}")
    print(f"Confidence average: {summary['confidence_avg']:.2f}")

    for pattern in all_patterns:
        print(f"\nLine {pattern.line_number}: {pattern.pattern_type}")
        print(f"  Original: {pattern.original_code}")
        print(f"  Transformed: {pattern.transformed_code}")
        print(f"  Best practice: {pattern.best_practice}")


if __name__ == "__main__":
    main()
