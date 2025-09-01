#!/usr/bin/env python3
"""
Code Cleaner & Validation
Handles code cleaning, validation, and quality assurance for generated code.
"""

import re
import logging
from typing import Any, Dict, List, Tuple

from .base_reflective_module import BaseReflectiveModule


class CodeCleaner(BaseReflectiveModule):
    """Handles code cleaning, validation, and quality assurance"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "code_cleaning": [
                "clean_generated_code",
                "ensure_clean_generation",
                "remove_duplicate_code",
                "normalize_imports",
            ],
            "code_validation": [
                "validate_python_syntax",
                "check_code_quality",
                "identify_issues",
            ],
            "formatting": [
                "format_code_structure",
                "ensure_consistent_style",
            ],
        }

    def clean_generated_code(self, code: str) -> str:
        """Clean up generated code by removing redundant patterns and improving structure"""
        if not code:
            return code

        # Remove multiple consecutive empty lines
        code = re.sub(r"\n\s*\n\s*\n", "\n\n", code)

        # Remove trailing whitespace
        code = re.sub(r"[ \t]+\n", "\n", code)

        # Ensure proper spacing around class/function definitions
        code = re.sub(r"(\n)(class|def)", r"\1\n\2", code)

        # Remove empty lines at the beginning
        code = re.sub(r"^\s*\n+", "", code)

        # Remove empty lines at the end
        code = code.rstrip("\n")

        return code

    def ensure_clean_generation(self, code: str) -> str:
        """Ensure the generated code is clean and properly formatted"""
        # Apply basic cleaning
        code = self.clean_generated_code(code)

        # Ensure proper line endings
        code = code.replace("\r\n", "\n").replace("\r", "\n")

        # Normalize imports
        code = self.normalize_imports(code)

        # Format code structure
        code = self.format_code_structure(code)

        # Final cleanup
        code = code.strip()

        return code

    def remove_duplicate_code(self, code: str) -> str:
        """Remove duplicate code blocks and consolidate similar patterns"""
        lines = code.split("\n")
        cleaned_lines = []
        seen_blocks = set()

        i = 0
        while i < len(lines):
            line = lines[i]
            cleaned_lines.append(line)

            # Check for method/function definitions
            if line.strip().startswith("def ") or line.strip().startswith("class "):
                # Collect the entire block
                block_lines = [line]
                j = i + 1
                indent_level = len(line) - len(line.lstrip())

                while j < len(lines):
                    next_line = lines[j]
                    if next_line.strip() == "":
                        block_lines.append(next_line)
                        j += 1
                        continue

                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= indent_level and next_line.strip():
                        break

                    block_lines.append(next_line)
                    j += 1

                block_content = "\n".join(block_lines)
                block_hash = hash(block_content.strip())

                if block_hash not in seen_blocks:
                    seen_blocks.add(block_hash)
                    i = j - 1
                else:
                    # Remove duplicate block
                    cleaned_lines = cleaned_lines[: -len(block_lines)]

            i += 1

        return "\n".join(cleaned_lines)

    def normalize_imports(self, code: str) -> str:
        """Normalize and organize import statements"""
        lines = code.split("\n")
        import_lines = []
        other_lines = []

        # Separate imports from other code
        for line in lines:
            if line.strip().startswith(("import ", "from ")):
                import_lines.append(line.strip())
            else:
                other_lines.append(line)

        # Sort and deduplicate imports
        import_lines = sorted(list(set(import_lines)))

        # Group imports by type
        stdlib_imports = []
        third_party_imports = []
        local_imports = []

        for imp in import_lines:
            if imp.startswith("import ") or imp.startswith("from "):
                # Simple heuristic for categorization
                if any(
                    pkg in imp
                    for pkg in [
                        "os",
                        "sys",
                        "re",
                        "json",
                        "typing",
                        "datetime",
                        "pathlib",
                    ]
                ):
                    stdlib_imports.append(imp)
                elif any(pkg in imp for pkg in ["black", "flake8", "mypy", "pytest"]):
                    third_party_imports.append(imp)
                else:
                    local_imports.append(imp)

        # Combine imports with proper spacing
        all_imports = []
        if stdlib_imports:
            all_imports.extend(stdlib_imports)
            all_imports.append("")
        if third_party_imports:
            all_imports.extend(third_party_imports)
            all_imports.append("")
        if local_imports:
            all_imports.extend(local_imports)
            all_imports.append("")

        # Combine all lines
        result_lines = all_imports + other_lines
        return "\n".join(result_lines)

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
        docstring_lines = len([line for line in lines if '"""' in line or "'''" in line])

        # Count code elements
        class_definitions = len([line for line in lines if line.strip().startswith("class ")])
        function_definitions = len([line for line in lines if line.strip().startswith("def ")])
        import_statements = len([line for line in lines if line.strip().startswith(("import ", "from "))])

        # Calculate metrics
        code_lines = total_lines - empty_lines - comment_lines
        code_density = code_lines / total_lines if total_lines > 0 else 0

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
        }

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

        if quality_metrics["class_definitions"] > 10:
            issues.append(
                {
                    "type": "too_many_classes",
                    "severity": "medium",
                    "message": f"Too many classes ({quality_metrics['class_definitions']}) - consider splitting",
                    "line": None,
                }
            )

        if quality_metrics["function_definitions"] > 20:
            issues.append(
                {
                    "type": "too_many_functions",
                    "severity": "medium",
                    "message": f"Too many functions ({quality_metrics['function_definitions']}) - consider splitting",
                    "line": None,
                }
            )

        return issues

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
