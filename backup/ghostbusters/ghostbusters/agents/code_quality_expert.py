"""Code quality expert agent for detecting code quality issues."""

from pathlib import Path
from typing import Any

from .base_expert import BaseExpert, DelusionResult


class CodeQualityExpert(BaseExpert):
    """Expert agent for detecting code quality issues."""

    def __init__(self) -> None:
        """Initialize the code quality expert."""
        super().__init__("CodeQualityExpert")

    async def detect_delusions(self, project_path: Path) -> DelusionResult:
        """Analyze existing code quality tool output and recommend systemic fixes."""
        delusions = []
        recommendations = []

        # Check if we have existing linting output to analyze
        linting_issues = await self._analyze_existing_lint_output(project_path)

        if linting_issues:
            # Analyze patterns and recommend systemic fixes
            systemic_issues = await self._identify_systemic_problems(linting_issues)
            delusions.extend(systemic_issues)

            # Generate smart recommendations based on patterns
            recommendations.extend(
                await self._generate_systemic_recommendations(linting_issues)
            )
        else:
            # No existing linting output - recommend setting up quality tools
            delusions.append(
                self._create_delusion(
                    "missing_quality_tools",
                    str(project_path),
                    1,
                    "No code quality tools configured or no output available",
                    0.8,
                    "medium",
                )
            )
            recommendations.append(
                self._create_recommendation(
                    "Set up automated code quality pipeline with pre-commit hooks",
                    "high",
                ),
            )

        confidence = self._calculate_confidence(delusions)

        return DelusionResult(
            delusions=delusions,
            confidence=confidence,
            recommendations=recommendations,
            agent_name=self.name,
        )

    async def _analyze_existing_lint_output(
        self, project_path: Path
    ) -> list[dict[str, Any]]:
        """Analyze existing linting tool output without running tools."""
        linting_issues = []

        # Look for existing flake8 output files
        flake8_output = project_path / ".flake8_output.txt"
        if flake8_output.exists():
            try:
                content = flake8_output.read_text()
                for line in content.strip().split("\n"):
                    if line.strip() and ":" in line:
                        parts = line.split(":", 3)
                        if len(parts) >= 4:
                            linting_issues.append(
                                {
                                    "file": parts[0],
                                    "line": int(parts[1]),
                                    "code": parts[2].strip(),
                                    "message": parts[3].strip(),
                                    "tool": "flake8",
                                }
                            )
            except Exception:
                pass

        # Look for existing mypy output
        mypy_output = project_path / ".mypy_output.txt"
        if mypy_output.exists():
            try:
                content = mypy_output.read_text()
                for line in content.strip().split("\n"):
                    if line.strip() and ":" in line:
                        parts = line.split(":", 3)
                        if len(parts) >= 4:
                            linting_issues.append(
                                {
                                    "file": parts[0],
                                    "line": int(parts[1]),
                                    "code": parts[2].strip(),
                                    "message": parts[3].strip(),
                                    "tool": "mypy",
                                }
                            )
            except Exception:
                pass

        # Look for existing black output
        black_output = project_path / ".black_output.txt"
        if black_output.exists():
            try:
                content = black_output.read_text()
                if "would reformat" in content:
                    linting_issues.append(
                        {
                            "file": "multiple",
                            "line": 0,
                            "code": "BLACK001",
                            "message": "Code formatting issues detected by Black",
                            "tool": "black",
                        }
                    )
            except Exception:
                pass

        return linting_issues

    async def _identify_systemic_problems(
        self, linting_issues: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Identify systemic patterns in linting issues."""
        systemic_issues = []

        if not linting_issues:
            return systemic_issues

        # Analyze patterns
        error_codes = [issue["code"] for issue in linting_issues if "code" in issue]
        files_affected = {issue["file"] for issue in linting_issues if "file" in issue}

        # Pattern 1: Widespread import issues
        import_errors = [
            code for code in error_codes if code in ["E402", "E302", "E305"]
        ]
        if (
            len(import_errors) > len(linting_issues) * 0.3
        ):  # More than 30% are import issues
            systemic_issues.append(
                self._create_delusion(
                    "systemic_import_issues",
                    "project-wide",
                    1,
                    f"Widespread import organization issues: {
                        len(import_errors)
                    } import-related errors across {len(files_affected)} files",
                    0.9,
                    "high",
                )
            )

        # Pattern 2: Widespread formatting issues
        formatting_errors = [
            code for code in error_codes if code in ["W291", "W292", "E501"]
        ]
        if (
            len(formatting_errors) > len(linting_issues) * 0.4
        ):  # More than 40% are formatting issues
            systemic_issues.append(
                self._create_delusion(
                    "systemic_formatting_issues",
                    "project-wide",
                    1,
                    f"Widespread code formatting issues: {
                        len(formatting_errors)
                    } formatting errors across {len(files_affected)} files",
                    0.85,
                    "medium",
                )
            )

        # Pattern 3: Missing type hints across many files
        type_errors = [code for code in error_codes if code in ["F821", "F822", "F823"]]
        if (
            len(type_errors) > len(linting_issues) * 0.2
        ):  # More than 20% are type issues
            systemic_issues.append(
                self._create_delusion(
                    "systemic_type_issues",
                    "project-wide",
                    1,
                    f"Widespread type annotation issues: {
                        len(type_errors)
                    } type-related errors across {len(files_affected)} files",
                    0.8,
                    "medium",
                )
            )

        # Pattern 4: Many files affected (indicates systemic issue)
        if (
            len(files_affected) > len(linting_issues) * 0.1
        ):  # Issues spread across many files
            systemic_issues.append(
                self._create_delusion(
                    "widespread_quality_issues",
                    "project-wide",
                    1,
                    f"Quality issues spread across {
                        len(files_affected)
                    } files, indicating systemic process problems",
                    0.9,
                    "high",
                )
            )

        return systemic_issues

    async def _generate_systemic_recommendations(
        self, linting_issues: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Generate smart recommendations based on systemic patterns."""
        recommendations = []

        if not linting_issues:
            return recommendations

        error_codes = [issue["code"] for issue in linting_issues if "code" in issue]
        files_affected = {issue["file"] for issue in linting_issues if "file" in issue}

        # Recommendation 1: Import organization
        import_errors = [
            code for code in error_codes if code in ["E402", "E302", "E305"]
        ]
        if import_errors:
            recommendations.append(
                self._create_recommendation(
                    f"Implement import sorting with isort: {
                        len(import_errors)
                    } import organization issues detected",
                    "high",
                ),
            )
            recommendations.append(
                self._create_recommendation(
                    "Add pre-commit hook for import sorting to prevent future issues",
                    "medium",
                ),
            )

        # Recommendation 2: Code formatting
        formatting_errors = [
            code for code in error_codes if code in ["W291", "W292", "E501"]
        ]
        if formatting_errors:
            recommendations.append(
                self._create_recommendation(
                    f"Implement automated formatting with Black: {
                        len(formatting_errors)
                    } formatting issues detected",
                    "high",
                ),
            )
            recommendations.append(
                self._create_recommendation(
                    "Add pre-commit hook for Black formatting to prevent future issues",
                    "medium",
                ),
            )

        # Recommendation 3: Type annotations
        type_errors = [code for code in error_codes if code in ["F821", "F822", "F823"]]
        if type_errors:
            recommendations.append(
                self._create_recommendation(
                    f"Implement gradual type annotation strategy: {
                        len(type_errors)
                    } type-related issues detected",
                    "high",
                ),
            )
            recommendations.append(
                self._create_recommendation(
                    "Add mypy to CI/CD pipeline for type checking",
                    "medium",
                ),
            )

        # Recommendation 4: Process improvement
        if len(files_affected) > 10:
            recommendations.append(
                self._create_recommendation(
                    "Implement comprehensive pre-commit hooks for all quality tools",
                    "high",
                ),
            )
            recommendations.append(
                self._create_recommendation(
                    "Add quality gates to CI/CD pipeline to prevent regressions",
                    "high",
                ),
            )

        # Recommendation 5: Team training
        if len(linting_issues) > 100:
            recommendations.append(
                self._create_recommendation(
                    "Provide team training on code quality standards and tool usage",
                    "medium",
                ),
            )

        return recommendations
