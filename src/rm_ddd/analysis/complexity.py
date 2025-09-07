"""
Complexity Analyzer

Analyzes code complexity and provides complexity metrics.
"""

import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ComplexityMetrics:
    """Complexity metrics for a code element"""

    cyclomatic_complexity: int = 0
    cognitive_complexity: int = 0
    lines_of_code: int = 0
    number_of_parameters: int = 0
    nesting_depth: int = 0
    number_of_branches: int = 0
    number_of_loops: int = 0


@dataclass
class ComplexityReport:
    """Complexity analysis report"""

    overall_complexity: float = 0.0
    max_complexity: int = 0
    complex_functions: List[Dict[str, Any]] = field(default_factory=list)
    complex_classes: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def merge(self, other: "ComplexityReport"):
        """Merge another complexity report"""
        self.overall_complexity = max(self.overall_complexity, other.overall_complexity)
        self.max_complexity = max(self.max_complexity, other.max_complexity)
        self.complex_functions.extend(other.complex_functions)
        self.complex_classes.extend(other.complex_classes)
        self.recommendations.extend(other.recommendations)


class ComplexityAnalyzer:
    """Analyzes code complexity"""

    def __init__(self):
        self.complexity_thresholds = {"cyclomatic": 10, "cognitive": 15, "lines_of_code": 50, "parameters": 5, "nesting": 4}

    def analyze_file(self, tree: ast.AST, file_path: str) -> Optional[ComplexityReport]:
        """Analyze file complexity"""
        report = ComplexityReport()

        # Analyze all functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics = self._analyze_function(node)
                if metrics:
                    self._evaluate_complexity(node.name, metrics, report, "function")

            elif isinstance(node, ast.ClassDef):
                metrics = self._analyze_class(node)
                if metrics:
                    self._evaluate_complexity(node.name, metrics, report, "class")

        # Calculate overall complexity
        if report.complex_functions or report.complex_classes:
            total_complexity = sum(func.get("complexity", 0) for func in report.complex_functions) + sum(cls.get("complexity", 0) for cls in report.complex_classes)
            report.overall_complexity = total_complexity / (len(report.complex_functions) + len(report.complex_classes))

        return report if report.complex_functions or report.complex_classes else None

    def _analyze_function(self, node: ast.FunctionDef) -> Optional[ComplexityMetrics]:
        """Analyze function complexity"""
        metrics = ComplexityMetrics()

        # Count parameters
        metrics.number_of_parameters = len(node.args.args)

        # Count lines of code
        metrics.lines_of_code = node.end_lineno - node.lineno if node.end_lineno else 1

        # Calculate cyclomatic complexity
        metrics.cyclomatic_complexity = self._calculate_cyclomatic_complexity(node)

        # Calculate cognitive complexity
        metrics.cognitive_complexity = self._calculate_cognitive_complexity(node)

        # Calculate nesting depth
        metrics.nesting_depth = self._calculate_nesting_depth(node)

        # Count branches and loops
        metrics.number_of_branches = self._count_branches(node)
        metrics.number_of_loops = self._count_loops(node)

        return metrics

    def _analyze_class(self, node: ast.ClassDef) -> Optional[ComplexityMetrics]:
        """Analyze class complexity"""
        metrics = ComplexityMetrics()

        # Count methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        metrics.number_of_parameters = len(methods)

        # Count lines of code
        metrics.lines_of_code = node.end_lineno - node.lineno if node.end_lineno else 1

        # Calculate complexity for all methods
        total_cyclomatic = 0
        total_cognitive = 0
        max_nesting = 0

        for method in methods:
            method_metrics = self._analyze_function(method)
            if method_metrics:
                total_cyclomatic += method_metrics.cyclomatic_complexity
                total_cognitive += method_metrics.cognitive_complexity
                max_nesting = max(max_nesting, method_metrics.nesting_depth)

        metrics.cyclomatic_complexity = total_cyclomatic
        metrics.cognitive_complexity = total_cognitive
        metrics.nesting_depth = max_nesting

        return metrics

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _calculate_cognitive_complexity(self, node: ast.AST) -> int:
        """Calculate cognitive complexity"""
        complexity = 0
        nesting_level = 0

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1 + nesting_level
                nesting_level += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1 + nesting_level
                nesting_level += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.Compare):
                complexity += len(child.ops) - 1

        return complexity

    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(child, ast.ExceptHandler):
                current_depth += 1
                max_depth = max(max_depth, current_depth)

        return max_depth

    def _count_branches(self, node: ast.AST) -> int:
        """Count number of branches"""
        branches = 0

        for child in ast.walk(node):
            if isinstance(child, ast.If):
                branches += 1
            elif isinstance(child, ast.ExceptHandler):
                branches += 1
            elif isinstance(child, ast.BoolOp):
                branches += len(child.values) - 1

        return branches

    def _count_loops(self, node: ast.AST) -> int:
        """Count number of loops"""
        loops = 0

        for child in ast.walk(node):
            if isinstance(child, (ast.While, ast.For, ast.AsyncFor)):
                loops += 1

        return loops

    def _evaluate_complexity(self, name: str, metrics: ComplexityMetrics, report: ComplexityReport, element_type: str):
        """Evaluate complexity and add to report if complex"""
        is_complex = False
        complexity_score = 0

        # Check thresholds
        if metrics.cyclomatic_complexity > self.complexity_thresholds["cyclomatic"]:
            is_complex = True
            complexity_score += metrics.cyclomatic_complexity

        if metrics.cognitive_complexity > self.complexity_thresholds["cognitive"]:
            is_complex = True
            complexity_score += metrics.cognitive_complexity

        if metrics.lines_of_code > self.complexity_thresholds["lines_of_code"]:
            is_complex = True
            complexity_score += metrics.lines_of_code

        if metrics.number_of_parameters > self.complexity_thresholds["parameters"]:
            is_complex = True
            complexity_score += metrics.number_of_parameters

        if metrics.nesting_depth > self.complexity_thresholds["nesting"]:
            is_complex = True
            complexity_score += metrics.nesting_depth

        if is_complex:
            complexity_info = {
                "name": name,
                "type": element_type,
                "complexity": complexity_score,
                "metrics": {
                    "cyclomatic_complexity": metrics.cyclomatic_complexity,
                    "cognitive_complexity": metrics.cognitive_complexity,
                    "lines_of_code": metrics.lines_of_code,
                    "number_of_parameters": metrics.number_of_parameters,
                    "nesting_depth": metrics.nesting_depth,
                    "number_of_branches": metrics.number_of_branches,
                    "number_of_loops": metrics.number_of_loops,
                },
            }

            if element_type == "function":
                report.complex_functions.append(complexity_info)
            else:
                report.complex_classes.append(complexity_info)

            # Update max complexity
            report.max_complexity = max(report.max_complexity, complexity_score)

            # Add recommendation
            report.recommendations.append(f"Consider refactoring {element_type} '{name}' - complexity score: {complexity_score}")
