#!/usr/bin/env python3
"""
AST-Enhanced Linter Implementation

This module implements the actual AST-enhanced linting functionality
based on the domain model defined in ast_enhanced_linter_model.py.

The linter uses AST parsing for semantic analysis and provides:
1. Comprehensive code quality analysis
2. Intelligent issue detection
3. AST-based auto-fixing
4. Quality metrics and reporting
"""

import ast
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Import our domain model
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


@dataclass
class LintingIssue:
    """Represents a linting issue found in the code"""

    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    suggestion: str
    auto_fixable: bool
    context: str
    rule_name: str
    ast_node: Optional[ast.AST] = None


@dataclass
class FileAnalysis:
    """Analysis results for a single file"""

    file_path: Path
    file_type: str
    total_issues: int
    critical_issues: int
    warnings: int
    suggestions: int
    one_liner_score: float
    ast_analysis_result: Optional[ASTAnalysisResult] = None
    issues: list[LintingIssue] = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []


class ASTEnhancedLinter:
    """
    AST-Enhanced Linter Implementation

    This linter uses AST parsing for semantic analysis and provides
    comprehensive code quality analysis with intelligent auto-fixing.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.model = create_ast_enhanced_linter_model()
        self.file_analyses: dict[str, FileAnalysis] = {}

        # File type detection patterns
        self.file_patterns = {
            "python": [".py"],
            "shell": [".sh", ".bash", ".zsh"],
            "yaml": [".yaml", ".yml"],
            "markdown": [".md", ".markdown"],
            "json": [".json"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
        }

    def scan_codebase(
        self, target_path: str = None, file_types: list[str] = None
    ) -> dict[str, FileAnalysis]:
        """
        Scan the codebase for linting issues using AST-enhanced analysis

        Args:
            target_path: Path to scan (defaults to workspace_path)
            file_types: List of file types to scan (defaults to all supported types)

        Returns:
            Dictionary mapping file paths to analysis results
        """
        scan_path = Path(target_path) if target_path else self.workspace_path
        file_types = file_types or list(self.file_patterns.keys())

        print(f"🔍 Scanning codebase at: {scan_path}")
        print(f"📁 Target file types: {', '.join(file_types)}")

        # Find all files to analyze
        files_to_analyze = []
        for file_type in file_types:
            if file_type in self.file_patterns:
                for extension in self.file_patterns[file_type]:
                    files_to_analyze.extend(scan_path.rglob(f"*{extension}"))

        # Filter out common directories to ignore
        ignored_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            ".venv",
            "venv",
        }
        files_to_analyze = [
            f
            for f in files_to_analyze
            if not any(ignored_dir in f.parts for ignored_dir in ignored_dirs)
        ]

        print(f"📊 Found {len(files_to_analyze)} files to analyze")

        # Analyze each file
        for file_path in files_to_analyze:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")

        return self.file_analyses

    def _analyze_file(self, file_path: Path):
        """Analyze a single file for linting issues"""
        file_type = self._detect_file_type(file_path)

        if file_type == "python":
            self._analyze_python_file_with_ast(file_path)
        else:
            self._analyze_file_with_patterns(file_path, file_type)

    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the type of file based on extension"""
        suffix = file_path.suffix.lower()

        for file_type, extensions in self.file_patterns.items():
            if suffix in extensions:
                return file_type

        return "generic"

    def _analyze_python_file_with_ast(self, file_path: Path):
        """Analyze Python file using AST for comprehensive analysis"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            start_time = time.time()

            # Parse AST
            try:
                tree = ast.parse(content)
                syntax_valid = True
                syntax_errors = []
            except SyntaxError as e:
                syntax_valid = False
                syntax_errors = [e]
                tree = None

            # Create AST analysis result
            ast_result = ASTAnalysisResult(
                file_path=file_path,
                syntax_valid=syntax_valid,
                syntax_errors=syntax_errors,
                issues=[],
                metrics=[],
                ast_tree=tree,
                analysis_time=time.time() - start_time,
            )

            # Apply all analysis rules
            issues = []
            metrics = []

            if tree is not None:
                # Analyze imports
                issues.extend(self._analyze_imports_with_ast(tree, lines))

                # Analyze functions and classes
                issues.extend(self._analyze_functions_and_classes_with_ast(tree, lines))

                # Analyze complexity
                issues.extend(self._analyze_complexity_with_ast(tree, lines))

                # Analyze code smells
                issues.extend(self._analyze_code_smells_with_ast(tree, lines))

                # Calculate metrics
                metrics.extend(self._calculate_quality_metrics(tree, lines))

            # Add syntax errors if any
            for error in syntax_errors:
                issues.append(
                    LintingIssue(
                        file_path=str(file_path),
                        line_number=error.lineno or 1,
                        issue_type=IssueType.SYNTAX_ERROR.value,
                        severity=IssueSeverity.CRITICAL.value,
                        description=f"Syntax error: {error.msg}",
                        suggestion="Fix the syntax error in the code",
                        auto_fixable=False,
                        context=(
                            lines[error.lineno - 1]
                            if error.lineno and error.lineno <= len(lines)
                            else "Unknown"
                        ),
                        rule_name="Syntax Validation",
                    )
                )

            # Update AST result
            ast_result.issues = issues
            ast_result.metrics = metrics

            # Create file analysis
            file_analysis = FileAnalysis(
                file_path=file_path,
                file_type="python",
                total_issues=len(issues),
                critical_issues=len(
                    [i for i in issues if i.severity == IssueSeverity.CRITICAL.value]
                ),
                warnings=len(
                    [i for i in issues if i.severity == IssueSeverity.WARNING.value]
                ),
                suggestions=len(
                    [i for i in issues if i.severity == IssueSeverity.SUGGESTION.value]
                ),
                one_liner_score=self._calculate_one_liner_score(lines),
                ast_analysis_result=ast_result,
                issues=issues,
            )

            self.file_analyses[str(file_path)] = file_analysis

        except Exception as e:
            print(f"⚠️  Error analyzing Python file {file_path}: {e}")

    def _analyze_imports_with_ast(
        self, tree: ast.AST, lines: list[str]
    ) -> list[LintingIssue]:
        """Analyze imports using AST for semantic understanding"""
        issues = []

        # Get import analysis rules
        import_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.IMPORT_ANALYSIS
        )

        for node in ast.walk(tree):
            for rule in import_rules:
                if isinstance(node, tuple(rule.ast_node_types)):
                    # Check if rule conditions are met
                    if all(condition(node) for condition in rule.conditions):
                        # Find line number
                        line_number = getattr(node, "lineno", 1)

                        issues.append(
                            LintingIssue(
                                file_path="",  # Will be set by caller
                                line_number=line_number,
                                issue_type=rule.issue_type.value,
                                severity=rule.severity.value,
                                description=rule.description,
                                suggestion=rule.suggestion,
                                auto_fixable=rule.auto_fix
                                in [
                                    AutoFixCapability.CAN_FIX,
                                    AutoFixCapability.CAN_PARTIALLY_FIX,
                                ],
                                context=(
                                    lines[line_number - 1]
                                    if line_number <= len(lines)
                                    else "Unknown"
                                ),
                                rule_name=rule.name,
                                ast_node=node,
                            )
                        )

        return issues

    def _analyze_functions_and_classes_with_ast(
        self, tree: ast.AST, lines: list[str]
    ) -> list[LintingIssue]:
        """Analyze functions and classes using AST"""
        issues = []

        # Get function and class analysis rules
        function_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.FUNCTION_ANALYSIS
        )
        class_rules = self.model.get_rules_for_strategy(AnalysisStrategy.CLASS_ANALYSIS)

        for node in ast.walk(tree):
            # Check function rules
            if isinstance(node, ast.FunctionDef):
                for rule in function_rules:
                    if isinstance(node, tuple(rule.ast_node_types)):
                        if all(condition(node) for condition in rule.conditions):
                            line_number = getattr(node, "lineno", 1)

                            issues.append(
                                LintingIssue(
                                    file_path="",
                                    line_number=line_number,
                                    issue_type=rule.issue_type.value,
                                    severity=rule.severity.value,
                                    description=rule.description,
                                    suggestion=rule.suggestion,
                                    auto_fixable=rule.auto_fix
                                    in [
                                        AutoFixCapability.CAN_FIX,
                                        AutoFixCapability.CAN_PARTIALLY_FIX,
                                    ],
                                    context=(
                                        lines[line_number - 1]
                                        if line_number <= len(lines)
                                        else "Unknown"
                                    ),
                                    rule_name=rule.name,
                                    ast_node=node,
                                )
                            )

            # Check class rules
            elif isinstance(node, ast.ClassDef):
                for rule in class_rules:
                    if isinstance(node, tuple(rule.ast_node_types)):
                        if all(condition(node) for condition in rule.conditions):
                            line_number = getattr(node, "lineno", 1)

                            issues.append(
                                LintingIssue(
                                    file_path="",
                                    line_number=line_number,
                                    issue_type=rule.issue_type.value,
                                    severity=rule.severity.value,
                                    description=rule.description,
                                    suggestion=rule.suggestion,
                                    auto_fixable=rule.auto_fix
                                    in [
                                        AutoFixCapability.CAN_FIX,
                                        AutoFixCapability.CAN_PARTIALLY_FIX,
                                    ],
                                    context=(
                                        lines[line_number - 1]
                                        if line_number <= len(lines)
                                        else "Unknown"
                                    ),
                                    rule_name=rule.name,
                                    ast_node=node,
                                )
                            )

        return issues

    def _analyze_complexity_with_ast(
        self, tree: ast.AST, lines: list[str]
    ) -> list[LintingIssue]:
        """Analyze code complexity using AST"""
        issues = []

        # Get complexity analysis rules
        complexity_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.COMPLEXITY_ANALYSIS
        )

        for node in ast.walk(tree):
            for rule in complexity_rules:
                if isinstance(node, tuple(rule.ast_node_types)):
                    if all(condition(node) for condition in rule.conditions):
                        line_number = getattr(node, "lineno", 1)

                        issues.append(
                            LintingIssue(
                                file_path="",
                                line_number=line_number,
                                issue_type=rule.issue_type.value,
                                severity=rule.severity.value,
                                description=rule.description,
                                suggestion=rule.suggestion,
                                auto_fixable=rule.auto_fix
                                in [
                                    AutoFixCapability.CAN_FIX,
                                    AutoFixCapability.CAN_PARTIALLY_FIX,
                                ],
                                context=(
                                    lines[line_number - 1]
                                    if line_number <= len(lines)
                                    else "Unknown"
                                ),
                                rule_name=rule.name,
                                ast_node=node,
                            )
                        )

        return issues

    def _analyze_code_smells_with_ast(
        self, tree: ast.AST, lines: list[str]
    ) -> list[LintingIssue]:
        """Analyze code smells using AST"""
        issues = []

        # Get code smell detection rules
        code_smell_rules = self.model.get_rules_for_strategy(
            AnalysisStrategy.CODE_SMELL_DETECTION
        )

        for node in ast.walk(tree):
            for rule in code_smell_rules:
                if isinstance(node, tuple(rule.ast_node_types)):
                    if all(condition(node) for condition in rule.conditions):
                        line_number = getattr(node, "lineno", 1)

                        issues.append(
                            LintingIssue(
                                file_path="",
                                line_number=line_number,
                                issue_type=rule.issue_type.value,
                                severity=rule.severity.value,
                                description=rule.description,
                                suggestion=rule.suggestion,
                                auto_fixable=rule.auto_fix
                                in [
                                    AutoFixCapability.CAN_FIX,
                                    AutoFixCapability.CAN_PARTIALLY_FIX,
                                ],
                                context=(
                                    lines[line_number - 1]
                                    if line_number <= len(lines)
                                    else "Unknown"
                                ),
                                rule_name=rule.name,
                                ast_node=node,
                            )
                        )

        return issues

    def _calculate_quality_metrics(
        self, tree: ast.AST, lines: list[str]
    ) -> list[CodeQualityMetric]:
        """Calculate quality metrics from AST analysis"""
        metrics = []

        # Function count
        function_count = len(
            [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        )
        metrics.append(
            CodeQualityMetric(
                name="function_count",
                value=float(function_count),
                unit="functions",
                description="Total number of functions in the file",
            )
        )

        # Class count
        class_count = len(
            [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        )
        metrics.append(
            CodeQualityMetric(
                name="class_count",
                value=float(class_count),
                unit="classes",
                description="Total number of classes in the file",
            )
        )

        # Import count
        import_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))
            ]
        )
        metrics.append(
            CodeQualityMetric(
                name="import_count",
                value=float(import_count),
                unit="imports",
                threshold=self.model.quality_thresholds.get("import_count", 10.0),
                is_good=import_count
                <= self.model.quality_thresholds.get("import_count", 10.0),
                description="Total number of import statements",
            )
        )

        # Line count
        line_count = len(lines)
        metrics.append(
            CodeQualityMetric(
                name="line_count",
                value=float(line_count),
                unit="lines",
                description="Total number of lines in the file",
            )
        )

        return metrics

    def _analyze_file_with_patterns(self, file_path: Path, file_type: str):
        """Analyze non-Python files using pattern-based analysis"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            # Basic pattern-based analysis for non-Python files
            issues = []

            # Check for one-liners
            for i, line in enumerate(lines, 1):
                if self._is_one_liner(line, file_type):
                    issues.append(
                        LintingIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type=IssueType.ONE_LINER_DETECTED.value,
                            severity=IssueSeverity.WARNING.value,
                            description="One-liner detected",
                            suggestion="Break into multiple lines for readability",
                            auto_fixable=True,
                            context=line,
                            rule_name="Pattern Analysis",
                        )
                    )

                # Check line length
                max_length = self.model.quality_thresholds.get("line_length", 88)
                if len(line) > max_length:
                    issues.append(
                        LintingIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type=IssueType.LINE_TOO_LONG.value,
                            severity=IssueSeverity.WARNING.value,
                            description=f"Line too long ({len(line)} characters)",
                            suggestion=f"Break line to be under {max_length} characters",
                            auto_fixable=True,
                            context=line,
                            rule_name="Pattern Analysis",
                        )
                    )

            # Create file analysis
            file_analysis = FileAnalysis(
                file_path=file_path,
                file_type=file_type,
                total_issues=len(issues),
                critical_issues=0,
                warnings=len(issues),
                suggestions=0,
                one_liner_score=self._calculate_one_liner_score(lines),
                issues=issues,
            )

            self.file_analyses[str(file_path)] = file_analysis

        except Exception as e:
            print(f"⚠️  Error analyzing {file_type} file {file_path}: {e}")

    def _is_one_liner(self, line: str, file_type: str) -> bool:
        """Check if a line is a one-liner that should be broken up"""
        # Remove comments and whitespace
        clean_line = line.split("#")[0].strip()

        if not clean_line:
            return False

        # Check for common one-liner patterns
        one_liner_patterns = {
            "shell": [
                r'^[^#]*\b(bash|sh|zsh)\s+-c\s+["\'`].*[`"\']\s*$',
                r'^[^#]*\bgit\s+(commit|push|pull|checkout|branch)\s+-m\s+["\'`].*[`"\']\s*$',
                r'^[^#]*\bpython\s+-c\s+["\'`].*[`"\']\s*$',
                r'^[^#]*\bdocker\s+run\s+.*["\'`].*[`"\']\s*$',
                r'^[^#]*\bkubectl\s+.*["\'`].*[`"\']\s*$',
                r'^[^#]*\bgcloud\s+.*["\'`].*[`"\']\s*$',
            ],
            "python": [
                r"^[^#]*\bimport\s+.*,\s+.*\s*$",  # Multiple imports on one line
                r"^[^#]*\bfrom\s+.*\s+import\s+\*\s*$",  # Wildcard imports
            ],
            "yaml": [
                r"^[^#]*\b.*:\s*\{.*\}.*$",  # Complex inline objects
                r"^[^#]*\b.*:\s*\[.*\].*$",  # Complex inline arrays
            ],
        }

        import re

        patterns = one_liner_patterns.get(file_type, [])

        return any(re.match(pattern, clean_line) for pattern in patterns)

    def _calculate_one_liner_score(self, lines: list[str]) -> float:
        """Calculate a score indicating how much the file uses one-liners"""
        if not lines:
            return 0.0

        one_liner_count = 0
        for line in lines:
            if self._is_one_liner(line, "generic"):
                one_liner_count += 1

        return one_liner_count / len(lines)

    def auto_fix_issues(self, target_path: str = None) -> dict[str, int]:
        """
        Automatically fix issues that can be resolved

        Args:
            target_path: Path to fix (defaults to workspace_path)

        Returns:
            Dictionary mapping file paths to number of fixes applied
        """
        fix_path = Path(target_path) if target_path else self.workspace_path
        fixes_applied = {}

        print(f"🔧 Auto-fixing issues in: {fix_path}")

        for file_path, analysis in self.file_analyses.items():
            if not Path(file_path).is_relative_to(fix_path):
                continue

            if analysis.file_type == "python" and analysis.ast_analysis_result:
                # Use AST-based fixing for Python files
                fixes = self._fix_python_file_with_ast(file_path, analysis)
                if fixes > 0:
                    fixes_applied[file_path] = fixes
            else:
                # Use pattern-based fixing for other files
                fixes = self._fix_file_with_patterns(file_path, analysis)
                if fixes > 0:
                    fixes_applied[file_path] = fixes

        return fixes_applied

    def _fix_python_file_with_ast(self, file_path: str, analysis: FileAnalysis) -> int:
        """Fix Python file issues using AST transformations"""
        if (
            not analysis.ast_analysis_result
            or not analysis.ast_analysis_result.ast_tree
        ):
            return 0

        fixes_applied = 0

        # Get auto-fixable issues
        auto_fixable_issues = [issue for issue in analysis.issues if issue.auto_fixable]

        if not auto_fixable_issues:
            return 0

        try:
            # Apply transformations based on transformation rules
            for issue in auto_fixable_issues:
                transformation_rule = self._find_transformation_rule(issue.issue_type)
                if transformation_rule and issue.ast_node:
                    # Apply transformation
                    transformed_tree = transformation_rule.ast_transformer(
                        analysis.ast_analysis_result.ast_tree
                    )

                    # Validate transformation
                    if transformation_rule.validation(
                        analysis.ast_analysis_result.ast_tree, transformed_tree
                    ):
                        # Update the AST tree
                        analysis.ast_analysis_result.ast_tree = transformed_tree
                        fixes_applied += 1
                    else:
                        # Rollback if validation fails
                        if transformation_rule.rollback:
                            analysis.ast_analysis_result.ast_tree = (
                                transformation_rule.rollback(transformed_tree)
                            )

            # Write back the fixed code if any fixes were applied
            if fixes_applied > 0:
                self._write_ast_to_file(
                    file_path, analysis.ast_analysis_result.ast_tree
                )

        except Exception as e:
            print(f"⚠️  Error applying AST fixes to {file_path}: {e}")

        return fixes_applied

    def _fix_file_with_patterns(self, file_path: str, analysis: FileAnalysis) -> int:
        """Fix non-Python file issues using pattern-based transformations"""
        fixes_applied = 0

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            modified = False

            # Fix one-liners
            for i, line in enumerate(lines):
                if self._is_one_liner(line, analysis.file_type):
                    fixed_line = self._fix_one_liner(line, analysis.file_type)
                    if fixed_line != line:
                        lines[i] = fixed_line
                        modified = True
                        fixes_applied += 1

            # Fix long lines
            max_length = self.model.quality_thresholds.get("line_length", 88)
            for i, line in enumerate(lines):
                if len(line) > max_length:
                    fixed_lines = self._fix_long_line(
                        line, max_length, analysis.file_type
                    )
                    if len(fixed_lines) > 1:
                        # Replace the long line with multiple shorter lines
                        lines[i : i + 1] = fixed_lines
                        modified = True
                        fixes_applied += 1

            # Write back if modified
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")

        except Exception as e:
            print(f"⚠️  Error applying pattern fixes to {file_path}: {e}")

        return fixes_applied

    def _find_transformation_rule(
        self, issue_type: str
    ) -> Optional[TransformationRule]:
        """Find transformation rule for a specific issue type"""
        for rule in self.model.transformation_rules:
            if rule.issue_type.value == issue_type:
                return rule
        return None

    def _fix_one_liner(self, line: str, file_type: str) -> str:
        """Fix a one-liner by breaking it into multiple lines"""
        if file_type == "shell":
            # Break shell commands at logical points
            if " && " in line:
                return line.replace(" && ", " \\\n    && ")
            if " | " in line:
                return line.replace(" | ", " \\\n    | ")
            if "; " in line:
                return line.replace("; ", " \\\n    ; ")

        elif file_type == "python":
            # Break Python imports
            if "import " in line and "," in line:
                parts = line.split(",")
                result = [parts[0]]
                for part in parts[1:]:
                    result.append("import " + part.strip())
                return "\n".join(result)

        return line

    def _fix_long_line(self, line: str, max_length: int, file_type: str) -> list[str]:
        """Fix a long line by breaking it into multiple lines"""
        if len(line) <= max_length:
            return [line]

        if file_type == "shell":
            # Break shell commands
            if " && " in line:
                return line.split(" && ")
            if " | " in line:
                return line.split(" | ")
            if "; " in line:
                return line.split("; ")

        # Generic line breaking
        words = line.split()
        result = []
        current_line = ""

        for word in words:
            if len(current_line + word) + 1 <= max_length:
                current_line += word + " "
            else:
                if current_line:
                    result.append(current_line.strip())
                current_line = word + " "

        if current_line:
            result.append(current_line.strip())

        return result if result else [line]

    def _write_ast_to_file(self, file_path: str, tree: ast.AST):
        """Write AST tree back to file"""
        try:
            import astor  # For AST to code conversion

            code = astor.to_source(tree)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

        except ImportError:
            print("⚠️  astor not available, cannot write AST back to file")
        except Exception as e:
            print(f"⚠️  Error writing AST to file {file_path}: {e}")

    def generate_report(self, output_format: str = "markdown") -> str:
        """Generate a comprehensive report of all findings"""
        if output_format == "markdown":
            return self._generate_markdown_report()
        if output_format == "json":
            return self._generate_json_report()
        return self._generate_text_report()

    def _generate_markdown_report(self) -> str:
        """Generate markdown report"""
        report_lines = [
            "# AST-Enhanced Linter Report",
            "",
            f"**Workspace:** {self.workspace_path}",
            f"**Files Analyzed:** {len(self.file_analyses)}",
            "",
            "## Summary",
            "",
        ]

        # Calculate totals
        total_issues = sum(
            analysis.total_issues for analysis in self.file_analyses.values()
        )
        total_critical = sum(
            analysis.critical_issues for analysis in self.file_analyses.values()
        )
        total_warnings = sum(
            analysis.warnings for analysis in self.file_analyses.values()
        )
        total_suggestions = sum(
            analysis.suggestions for analysis in self.file_analyses.values()
        )

        report_lines.extend(
            [
                f"- **Total Issues:** {total_issues}",
                f"- **Critical:** {total_critical}",
                f"- **Warnings:** {total_warnings}",
                f"- **Suggestions:** {total_suggestions}",
                "",
            ]
        )

        # File-by-file analysis
        report_lines.append("## File Analysis")
        report_lines.append("")

        for file_path, analysis in sorted(self.file_analyses.items()):
            report_lines.extend(
                [
                    f"### {file_path}",
                    f"- **Type:** {analysis.file_type}",
                    f"- **Issues:** {analysis.total_issues} (Critical: {analysis.critical_issues}, Warnings: {analysis.warnings}, Suggestions: {analysis.suggestions})",
                    f"- **One-liner Score:** {analysis.one_liner_score:.2%}",
                    "",
                ]
            )

            # Show AST metrics if available
            if analysis.ast_analysis_result and analysis.ast_analysis_result.metrics:
                report_lines.append("#### Quality Metrics:")
                for metric in analysis.ast_analysis_result.metrics:
                    status = "✅" if metric.is_good else "⚠️"
                    threshold_info = (
                        f" (threshold: {metric.threshold})" if metric.threshold else ""
                    )
                    report_lines.append(
                        f"- {status} **{metric.name}:** {metric.value} {metric.unit}{threshold_info}"
                    )
                report_lines.append("")

            # Show sample issues
            if analysis.issues:
                report_lines.append("#### Sample Issues:")
                for issue in analysis.issues[:5]:  # Show first 5 issues
                    severity_icon = {
                        IssueSeverity.CRITICAL.value: "🚨",
                        IssueSeverity.WARNING.value: "⚠️",
                        IssueSeverity.SUGGESTION.value: "💡",
                        IssueSeverity.INFO.value: "ℹ️",
                    }.get(issue.severity, "❓")

                    report_lines.append(
                        f"- {severity_icon} **{issue.issue_type}** (line {issue.line_number}): {issue.description}"
                    )
                    report_lines.append(f"  - Suggestion: {issue.suggestion}")
                    if issue.auto_fixable:
                        report_lines.append(f"  - Auto-fixable: ✅")
                    report_lines.append("")

        return "\n".join(report_lines)

    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        import json

        report_data = {
            "workspace": str(self.workspace_path),
            "files_analyzed": len(self.file_analyses),
            "summary": {
                "total_issues": sum(
                    analysis.total_issues for analysis in self.file_analyses.values()
                ),
                "critical_issues": sum(
                    analysis.critical_issues for analysis in self.file_analyses.values()
                ),
                "warnings": sum(
                    analysis.warnings for analysis in self.file_analyses.values()
                ),
                "suggestions": sum(
                    analysis.suggestions for analysis in self.file_analyses.values()
                ),
            },
            "files": {},
        }

        for file_path, analysis in self.file_analyses.items():
            report_data["files"][file_path] = {
                "file_type": analysis.file_type,
                "total_issues": analysis.total_issues,
                "critical_issues": analysis.critical_issues,
                "warnings": analysis.warnings,
                "suggestions": analysis.suggestions,
                "one_liner_score": analysis.one_liner_score,
                "issues": [
                    {
                        "line_number": issue.line_number,
                        "issue_type": issue.issue_type,
                        "severity": issue.severity,
                        "description": issue.description,
                        "suggestion": issue.suggestion,
                        "auto_fixable": issue.auto_fixable,
                        "context": issue.context,
                        "rule_name": issue.rule_name,
                    }
                    for issue in analysis.issues
                ],
            }

            # Add AST metrics if available
            if analysis.ast_analysis_result and analysis.ast_analysis_result.metrics:
                report_data["files"][file_path]["metrics"] = [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "threshold": metric.threshold,
                        "is_good": metric.is_good,
                        "description": metric.description,
                    }
                    for metric in analysis.ast_analysis_result.metrics
                ]

        return json.dumps(report_data, indent=2)

    def _generate_text_report(self) -> str:
        """Generate plain text report"""
        report_lines = [
            "AST-Enhanced Linter Report",
            "=" * 50,
            "",
            f"Workspace: {self.workspace_path}",
            f"Files Analyzed: {len(self.file_analyses)}",
            "",
            "Summary:",
            "",
        ]

        # Calculate totals
        total_issues = sum(
            analysis.total_issues for analysis in self.file_analyses.values()
        )
        total_critical = sum(
            analysis.critical_issues for analysis in self.file_analyses.values()
        )
        total_warnings = sum(
            analysis.warnings for analysis in self.file_analyses.values()
        )
        total_suggestions = sum(
            analysis.suggestions for analysis in self.file_analyses.values()
        )

        report_lines.extend(
            [
                f"  Total Issues: {total_issues}",
                f"  Critical: {total_critical}",
                f"  Warnings: {total_warnings}",
                f"  Suggestions: {total_suggestions}",
                "",
            ]
        )

        # File-by-file analysis
        for file_path, analysis in sorted(self.file_analyses.items()):
            report_lines.extend(
                [
                    f"{file_path}:",
                    f"  Type: {analysis.file_type}",
                    f"  Issues: {analysis.total_issues} (Critical: {analysis.critical_issues}, Warnings: {analysis.warnings}, Suggestions: {analysis.suggestions})",
                    f"  One-liner Score: {analysis.one_liner_score:.2%}",
                    "",
                ]
            )

        return "\n".join(report_lines)


def main():
    """Main entry point for the AST-enhanced linter"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AST-Enhanced Linter for Code Quality Analysis"
    )
    parser.add_argument("--scan", default=".", help="Path to scan for code analysis")
    parser.add_argument(
        "--fix", action="store_true", help="Automatically fix issues where possible"
    )
    parser.add_argument(
        "--output",
        choices=["markdown", "json", "text"],
        default="markdown",
        help="Output format for report",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Create linter
    linter = ASTEnhancedLinter(args.scan)

    # Scan codebase
    print("🔍 Starting AST-enhanced code analysis...")
    linter.scan_codebase(args.scan)

    # Auto-fix if requested
    if args.fix:
        print("🔧 Applying auto-fixes...")
        fixes = linter.auto_fix_issues(args.scan)
        if fixes:
            print(f"✅ Applied {sum(fixes.values())} fixes across {len(fixes)} files")
        else:
            print("ℹ️  No auto-fixes were applied")

    # Generate report
    report = linter.generate_report(args.output)

    if args.output == "json":
        print(report)
    else:
        print(report)

    # Summary
    total_issues = sum(
        analysis.total_issues for analysis in linter.file_analyses.values()
    )
    print(
        f"\n📊 Analysis complete: {total_issues} issues found across {len(linter.file_analyses)} files"
    )


if __name__ == "__main__":
    main()
