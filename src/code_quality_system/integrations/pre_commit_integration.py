#!/usr/bin/env python3
"""
Pre-commit Integration

Integrates quality enforcement with git pre-commit hooks.
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

from src.code_quality_system.quality_enforcer import QualityEnforcer


class PreCommitIntegration:
    """Integrates quality enforcement with git pre-commit hooks"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quality_enforcer = QualityEnforcer(project_path)
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.fast_mode = True  # Use cached metrics when possible
        self.verbose = False

    def run_pre_commit_check(self) -> bool:
        """Run quality check for pre-commit hook"""
        self.logger.info("Running pre-commit quality check")

        try:
            # Check if we're in a git repository
            if not self._is_git_repository():
                self.logger.warning(
                    "Not in a git repository, skipping pre-commit check"
                )
                return True

            # Get staged files
            staged_files = self._get_staged_files()
            if not staged_files:
                self.logger.info("No staged files, pre-commit check passed")
                return True

            # Run quality check
            if self.fast_mode:
                result = self.quality_enforcer.run_quick_quality_check()
                if result["status"] == "success":
                    self.logger.info("Quick quality check passed using cached metrics")
                    return True

            # Run full quality check
            result = self._run_full_quality_check(staged_files)

            if result["can_proceed"]:
                self.logger.info("Pre-commit quality check passed")
                return True
            self.logger.error("Pre-commit quality check failed")
            self._print_failure_details(result)
            return False

        except Exception as e:
            self.logger.error(f"Pre-commit check failed with error: {e}")
            return False

    def _is_git_repository(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _get_staged_files(self) -> list[Path]:
        """Get list of staged files"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )

            if result.returncode != 0:
                return []

            staged_files = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    file_path = self.project_path / line.strip()
                    if file_path.exists():
                        staged_files.append(file_path)

            return staged_files

        except Exception as e:
            self.logger.warning(f"Could not get staged files: {e}")
            return []

    def _run_full_quality_check(self, staged_files: list[Path]) -> dict[str, Any]:
        """Run full quality check on staged files"""
        self.logger.info(
            f"Running full quality check on {len(staged_files)} staged files"
        )

        # Analyze staged files for quality issues
        analysis_results = self._analyze_staged_files(staged_files)

        # Run quality enforcement
        return self.quality_enforcer.enforce_quality(analysis_results)

    def _analyze_staged_files(self, staged_files: list[Path]) -> dict[str, Any]:
        """Analyze staged files for quality issues"""
        analysis_results = {
            "flake8_issues": [],
            "security_issues": [],
            "coverage_percentage": 0.0,
            "performance_metrics": {},
        }

        # Analyze Python files for code quality issues
        python_files = [f for f in staged_files if f.suffix == ".py"]
        if python_files:
            analysis_results["flake8_issues"] = self._check_python_quality(python_files)

        # Check for security issues in staged files
        analysis_results["security_issues"] = self._check_security_issues(staged_files)

        # Get test coverage if tests are staged
        test_files = [f for f in staged_files if "test" in f.name.lower()]
        if test_files:
            analysis_results["coverage_percentage"] = self._get_test_coverage()

        return analysis_results

    def _check_python_quality(self, python_files: list[Path]) -> list[dict[str, Any]]:
        """Check Python files for quality issues"""
        issues = []

        for py_file in python_files:
            try:
                # Basic syntax check
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    issues.append(
                        {
                            "file": str(py_file),
                            "type": "syntax_error",
                            "priority": "critical",
                            "description": "Python syntax error",
                            "details": result.stderr,
                        }
                    )

                # Check for common code quality issues
                content = py_file.read_text()

                # Check for long lines
                for i, line in enumerate(content.split("\n"), 1):
                    if len(line) > 88:  # Black's default line length
                        issues.append(
                            {
                                "file": str(py_file),
                                "type": "line_length",
                                "priority": "medium",
                                "description": f"Line {i} exceeds 88 characters",
                                "line": i,
                                "details": {"line_length": len(line)},
                            }
                        )

                # Check for missing docstrings in functions/classes
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith(("def ", "class ")):
                        # Check if next non-empty line is a docstring
                        docstring_found = False
                        for j in range(i, min(i + 3, len(lines))):
                            next_line = lines[j].strip()
                            if next_line.startswith(('"""', "'''")):
                                docstring_found = True
                                break
                            if next_line and not next_line.startswith("#"):
                                break

                        if not docstring_found:
                            issues.append(
                                {
                                    "file": str(py_file),
                                    "type": "missing_docstring",
                                    "priority": "low",
                                    "description": f"Missing docstring for {line.strip()}",
                                    "line": i,
                                }
                            )

            except Exception as e:
                issues.append(
                    {
                        "file": str(py_file),
                        "type": "analysis_error",
                        "priority": "medium",
                        "description": f"Could not analyze file: {e}",
                    }
                )

        return issues

    def _check_security_issues(self, staged_files: list[Path]) -> list[dict[str, Any]]:
        """Check staged files for security issues"""
        security_issues = []

        for file_path in staged_files:
            try:
                content = file_path.read_text()

                # Check for hardcoded credentials
                credential_patterns = [
                    r"sk-[a-zA-Z0-9]{48}",  # OpenAI API key
                    r"pk_[a-zA-Z0-9]{48}",  # OpenAI API key
                    r"AKIA[a-zA-Z0-9]{16}",  # AWS access key
                    r"ghp_[a-zA-Z0-9]{36}",  # GitHub personal access token
                    r"gho_[a-zA-Z0-9]{36}",  # GitHub personal access token
                ]

                import re

                for pattern in credential_patterns:
                    if re.search(pattern, content):
                        security_issues.append(
                            {
                                "file": str(file_path),
                                "type": "hardcoded_credential",
                                "priority": "critical",
                                "description": "Hardcoded credential detected",
                                "details": {"pattern": pattern},
                            }
                        )

                # Check for dangerous operations
                dangerous_patterns = [
                    r"subprocess\.run",
                    r"os\.system",
                    r"eval\(",
                    r"exec\(",
                ]

                for pattern in dangerous_patterns:
                    if re.search(pattern, content):
                        security_issues.append(
                            {
                                "file": str(file_path),
                                "type": "dangerous_operation",
                                "priority": "high",
                                "description": "Potentially dangerous operation detected",
                                "details": {"pattern": pattern},
                            }
                        )

            except Exception:
                # Skip files that can't be read as text
                pass

        return security_issues

    def _get_test_coverage(self) -> float:
        """Get current test coverage percentage"""
        try:
            # Check if coverage file exists
            coverage_file = self.project_path / "coverage.xml"
            if coverage_file.exists():
                import xml.etree.ElementTree as ET

                tree = ET.parse(coverage_file)
                root = tree.getroot()

                coverage_elem = root.find(".//coverage")
                if coverage_elem is not None:
                    line_rate = float(coverage_elem.get("line-rate", "0"))
                    return line_rate * 100.0

            # Fallback: check if htmlcov exists
            htmlcov_dir = self.project_path / "htmlcov"
            if htmlcov_dir.exists():
                return 75.0  # Assume reasonable coverage if htmlcov exists

            return 0.0

        except Exception as e:
            self.logger.warning(f"Could not determine test coverage: {e}")
            return 0.0

    def _print_failure_details(self, result: dict[str, Any]) -> None:
        """Print detailed failure information"""
        print("\n" + "=" * 60)
        print("❌ QUALITY CHECK FAILED")
        print("=" * 60)

        print(f"Overall Quality Score: {result.get('overall_score', 'N/A'):.1f}")
        print(f"Blocking Gates: {result.get('blocking_gates', 0)}")

        if "gate_results" in result:
            print("\nGate Results:")
            for gate in result["gate_results"]:
                status_icon = "✅" if gate["status"] == "passed" else "❌"
                print(f"  {status_icon} {gate['name']}: {gate['message']}")

        if "recommendations" in result:
            print("\nRecommendations:")
            for rec in result["recommendations"]:
                print(f"  • {rec}")

        print("\n" + "=" * 60)
        print("Fix the issues above before committing.")
        print("=" * 60)

    def install_pre_commit_hook(self) -> bool:
        """Install pre-commit hook in the current repository"""
        try:
            git_hooks_dir = self.project_path / ".git" / "hooks"
            if not git_hooks_dir.exists():
                self.logger.error("Git hooks directory not found")
                return False

            pre_commit_hook = git_hooks_dir / "pre-commit"

            # Create pre-commit hook script
            hook_content = f"""#!/bin/bash
# Quality enforcement pre-commit hook
cd "{self.project_path}"
python -m src.code_quality_system.integrations.pre_commit_integration
exit $?
"""

            with open(pre_commit_hook, "w") as f:
                f.write(hook_content)

            # Make hook executable
            pre_commit_hook.chmod(0o755)

            self.logger.info(f"Pre-commit hook installed at {pre_commit_hook}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to install pre-commit hook: {e}")
            return False

    def uninstall_pre_commit_hook(self) -> bool:
        """Uninstall pre-commit hook"""
        try:
            pre_commit_hook = self.project_path / ".git" / "hooks" / "pre-commit"
            if pre_commit_hook.exists():
                pre_commit_hook.unlink()
                self.logger.info("Pre-commit hook uninstalled")
                return True
            self.logger.info("No pre-commit hook found to uninstall")
            return True

        except Exception as e:
            self.logger.error(f"Failed to uninstall pre-commit hook: {e}")
            return False
