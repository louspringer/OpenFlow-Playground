#!/usr/bin/env python3
"""
Control Flow Pattern Recognition System

Addresses UC-2 important risk use case for recognizing complex control flow patterns.
This system enhances AST parsing for boolean expressions, nested structures, and pattern recognition.
"""

import ast
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import ast2json


class ControlFlowAnalyzer:
    """Analyzes and recognizes complex control flow patterns in Python code."""

    def __init__(self):
        self.patterns = {}
        self.complexity_metrics = {}
        self.control_flow_graph = {}

    def analyze_control_flow(self, source_file: str) -> Dict[str, Any]:
        """
        Analyze control flow patterns in a Python file.

        Args:
            source_file: Path to source Python file

        Returns:
            Control flow analysis results with pattern recognition
        """
        try:
            # Parse source file
            with open(source_file, "r") as f:
                source_content = f.read()

            # Generate AST from source
            source_ast = ast.parse(source_content)

            # Extract control flow patterns
            patterns = self._extract_control_flow_patterns(source_ast)

            # Analyze complexity
            complexity = self._analyze_control_complexity(source_ast)

            # Generate control flow graph
            flow_graph = self._generate_control_flow_graph(source_ast)

            # Pattern recognition
            recognized_patterns = self._recognize_patterns(patterns)

            analysis_result = {
                "source_file": source_file,
                "patterns": patterns,
                "complexity": complexity,
                "flow_graph": flow_graph,
                "recognized_patterns": recognized_patterns,
                "analysis_success": True,
            }

            return analysis_result

        except Exception as e:
            return {
                "source_file": source_file,
                "error": str(e),
                "analysis_success": False,
            }

    def _extract_control_flow_patterns(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Extract control flow patterns from AST."""
        patterns = {
            "if_statements": [],
            "for_loops": [],
            "while_loops": [],
            "try_blocks": [],
            "boolean_expressions": [],
            "nested_structures": [],
            "early_returns": [],
            "break_continue": [],
        }

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.If):
                pattern = self._analyze_if_statement(node)
                patterns["if_statements"].append(pattern)

            elif isinstance(node, ast.For):
                pattern = self._analyze_for_loop(node)
                patterns["for_loops"].append(pattern)

            elif isinstance(node, ast.While):
                pattern = self._analyze_while_loop(node)
                patterns["while_loops"].append(pattern)

            elif isinstance(node, ast.Try):
                pattern = self._analyze_try_block(node)
                patterns["try_blocks"].append(pattern)

            elif isinstance(node, ast.BoolOp):
                pattern = self._analyze_boolean_expression(node)
                patterns["boolean_expressions"].append(pattern)

            elif isinstance(node, ast.Return):
                if self._is_early_return(node, ast_tree):
                    patterns["early_returns"].append(
                        {
                            "lineno": getattr(node, "lineno", 0),
                            "value": (self._get_node_value(node.value) if node.value else None),
                        }
                    )

            elif isinstance(node, (ast.Break, ast.Continue)):
                patterns["break_continue"].append({"type": type(node).__name__, "lineno": getattr(node, "lineno", 0)})

        # Analyze nested structures
        patterns["nested_structures"] = self._analyze_nested_structures(ast_tree)

        return patterns

    def _analyze_control_complexity(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Analyze overall control flow complexity."""
        complexity = {
            "total_statements": 0,
            "control_flow_statements": 0,
            "max_nesting_level": 0,
            "cyclomatic_complexity": 1,  # Start with 1 for base path
            "boolean_complexity": 0,
        }

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.stmt):
                complexity["total_statements"] += 1

            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity["control_flow_statements"] += 1
                complexity["cyclomatic_complexity"] += 1

            if isinstance(node, ast.BoolOp):
                complexity["boolean_complexity"] += self._calculate_boolean_complexity(node)

            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                nesting = self._calculate_nesting_level(node)
                complexity["max_nesting_level"] = max(complexity["max_nesting_level"], nesting)

        return complexity

    def _analyze_if_statement(self, node: ast.If) -> Dict[str, Any]:
        """Analyze if statement structure and complexity."""
        pattern = {
            "lineno": getattr(node, "lineno", 0),
            "test_complexity": self._analyze_condition_complexity(node.test),
            "body_complexity": self._analyze_body_complexity(node.body),
            "orelse_complexity": self._analyze_body_complexity(node.orelse),
            "nested_level": self._calculate_nesting_level(node),
            "has_elif": len(node.orelse) > 0 and isinstance(node.orelse[0], ast.If),
        }

        # Check for complex boolean conditions
        if isinstance(node.test, ast.BoolOp):
            pattern["boolean_operators"] = self._extract_boolean_operators(node.test)

        return pattern

    def _analyze_for_loop(self, node: ast.For) -> Dict[str, Any]:
        """Analyze for loop structure and complexity."""
        pattern = {
            "lineno": getattr(node, "lineno", 0),
            "target": self._get_node_value(node.target),
            "iter": self._get_node_value(node.iter),
            "body_complexity": self._analyze_body_complexity(node.body),
            "orelse_complexity": self._analyze_body_complexity(node.orelse),
            "nested_level": self._calculate_nesting_level(node),
            "has_break_continue": self._has_break_continue(node.body),
        }

        return pattern

    def _analyze_while_loop(self, node: ast.While) -> Dict[str, Any]:
        """Analyze while loop structure and complexity."""
        pattern = {
            "lineno": getattr(node, "lineno", 0),
            "test_complexity": self._analyze_condition_complexity(node.test),
            "body_complexity": self._analyze_body_complexity(node.body),
            "orelse_complexity": self._analyze_body_complexity(node.orelse),
            "nested_level": self._calculate_nesting_level(node),
            "has_break_continue": self._has_break_continue(node.body),
        }

        return pattern

    def _analyze_try_block(self, node: ast.Try) -> Dict[str, Any]:
        """Analyze try block structure and complexity."""
        pattern = {
            "lineno": getattr(node, "lineno", 0),
            "body_complexity": self._analyze_body_complexity(node.body),
            "handlers": len(node.handlers),
            "except_types": [self._get_node_value(handler.type) for handler in node.handlers if handler.type],
            "orelse_complexity": self._analyze_body_complexity(node.orelse),
            "finalbody_complexity": self._analyze_body_complexity(node.finalbody),
            "nested_level": self._calculate_nesting_level(node),
        }

        return pattern

    def _analyze_boolean_expression(self, node: ast.BoolOp) -> Dict[str, Any]:
        """Analyze boolean expression complexity."""
        pattern = {
            "lineno": getattr(node, "lineno", 0),
            "operator": type(node.op).__name__,
            "values": [self._get_node_value(val) for val in node.values],
            "complexity": self._calculate_boolean_complexity(node),
            "nested_booleans": self._count_nested_booleans(node),
        }

        return pattern

    def _analyze_condition_complexity(self, node: ast.expr) -> int:
        """Calculate complexity of a condition expression."""
        if not node:
            return 0

        complexity = 1

        # Count boolean operators
        if isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1

        # Count comparison operators
        if isinstance(node, ast.Compare):
            complexity += len(node.ops)

        # Count function calls
        if isinstance(node, ast.Call):
            complexity += 2

        # Count attribute access
        if isinstance(node, ast.Attribute):
            complexity += 1

        return complexity

    def _analyze_body_complexity(self, body: List[ast.stmt]) -> int:
        """Calculate complexity of a statement body."""
        if not body:
            return 0

        complexity = len(body)

        # Add complexity for control flow statements
        for stmt in body:
            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 2
            elif isinstance(stmt, ast.FunctionDef):
                complexity += 3
            elif isinstance(stmt, ast.ClassDef):
                complexity += 4

        return complexity

    def _calculate_nesting_level(self, node: ast.AST) -> int:
        """Calculate nesting level of a node."""
        level = 0
        current = node

        while hasattr(current, "parent"):
            if isinstance(current.parent, (ast.If, ast.For, ast.While, ast.Try)):
                level += 1
            current = current.parent

        return level

    def _extract_boolean_operators(self, node: ast.BoolOp) -> List[str]:
        """Extract boolean operators from a boolean expression."""
        operators = []

        def extract_ops(n):
            if isinstance(n, ast.BoolOp):
                operators.append(type(n.op).__name__)
                for val in n.values:
                    extract_ops(val)

        extract_ops(node)
        return operators

    def _calculate_boolean_complexity(self, node: ast.BoolOp) -> int:
        """Calculate complexity of a boolean expression."""
        complexity = len(node.values) - 1  # Number of operators

        for val in node.values:
            if isinstance(val, ast.BoolOp):
                complexity += self._calculate_boolean_complexity(val)
            elif isinstance(val, ast.Compare):
                complexity += len(val.ops)
            elif isinstance(val, ast.Call):
                complexity += 2

        return complexity

    def _count_nested_booleans(self, node: ast.BoolOp) -> int:
        """Count nested boolean expressions."""
        count = 0

        for val in node.values:
            if isinstance(val, ast.BoolOp):
                count += 1 + self._count_nested_booleans(val)

        return count

    def _has_break_continue(self, body: List[ast.stmt]) -> bool:
        """Check if body contains break or continue statements."""
        for stmt in body:
            if isinstance(stmt, (ast.Break, ast.Continue)):
                return True
            elif isinstance(stmt, (ast.If, ast.For, ast.While)):
                if self._has_break_continue(stmt.body) or self._has_break_continue(stmt.orelse):
                    return True
        return False

    def _is_early_return(self, node: ast.Return, ast_tree: ast.AST) -> bool:
        """Check if return statement is an early return."""
        # Simple heuristic: return in first half of function
        function = self._find_parent_function(node, ast_tree)
        if not function:
            return False

        function_lines = len(function.body)
        return_lines = [stmt.lineno for stmt in function.body if isinstance(stmt, ast.Return)]

        if not return_lines:
            return False

        # Consider early return if it's in the first third of the function
        return min(return_lines) < function_lines / 3

    def _find_parent_function(self, node: ast.AST, ast_tree: ast.AST) -> Optional[ast.FunctionDef]:
        """Find the parent function of a node."""
        for n in ast.walk(ast_tree):
            if isinstance(n, ast.FunctionDef):
                if node in ast.walk(n):
                    return n
        return None

    def _get_node_value(self, node: ast.expr) -> str:
        """Get string representation of a node."""
        if not node:
            return "None"

        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Attribute):
            return f"{self._get_node_value(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            func = self._get_node_value(node.func)
            args = [self._get_node_value(arg) for arg in node.args]
            return f"{func}({', '.join(args)})"
        else:
            return type(node).__name__

    def _analyze_nested_structures(self, ast_tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze nested control flow structures."""
        nested = []

        def analyze_nesting(node, level=0):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                nested.append(
                    {
                        "type": type(node).__name__,
                        "level": level,
                        "lineno": getattr(node, "lineno", 0),
                        "complexity": self._analyze_body_complexity(node.body),
                    }
                )

                # Analyze nested structures
                for child in node.body:
                    analyze_nesting(child, level + 1)

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                analyze_nesting(node)

        return nested

    def _generate_control_flow_graph(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Generate control flow graph representation."""
        graph = {"nodes": [], "edges": [], "entry_points": [], "exit_points": []}

        # Extract imports
        imports = []
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "import",
                            "module": alias.name,
                            "asname": alias.asname,
                            "lineno": getattr(node, "lineno", 0),
                        }
                    )
            elif isinstance(node, ast.ImportFrom):
                imports.append(
                    {
                        "type": "import_from",
                        "module": node.module,
                        "names": [alias.name for alias in node.names],
                        "lineno": getattr(node, "lineno", 0),
                    }
                )

        graph["imports"] = imports

        # Extract function definitions as entry points
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                graph["entry_points"].append({"name": node.name, "lineno": node.lineno, "type": "function"})

                # Add function body as nodes with detailed analysis
                for stmt in node.body:
                    node_info = {
                        "id": f"{node.name}_{stmt.lineno}",
                        "type": type(stmt).__name__,
                        "lineno": getattr(stmt, "lineno", 0),
                        "function": node.name,
                    }

                    # Analyze what this statement actually does
                    if isinstance(stmt, ast.Expr):
                        # Check if this expression contains a function call
                        call_info = self._extract_call_info(stmt.value)
                        if call_info:
                            node_info.update(call_info)

                    graph["nodes"].append(node_info)

        # Extract control flow statements (if __name__ == "__main__":, etc.)
        control_flow = []
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.If):
                # Check if this is the main guard
                if (
                    isinstance(node.test, ast.Compare)
                    and isinstance(node.test.left, ast.Name)
                    and node.test.left.id == "__name__"
                    and isinstance(node.test.ops[0], ast.Eq)
                    and isinstance(node.test.comparators[0], ast.Constant)
                    and node.test.comparators[0].value == "__main__"
                ):
                    control_flow.append(
                        {
                            "type": "main_guard",
                            "lineno": getattr(node, "lineno", 0),
                            "body_statements": len(node.body),
                            "has_else": len(node.orelse) > 0,
                        }
                    )

                    # Add main block statements to nodes
                    for stmt in node.body:
                        node_info = {
                            "id": f"main_{stmt.lineno}",
                            "type": type(stmt).__name__,
                            "lineno": getattr(stmt, "lineno", 0),
                            "function": "main",
                        }

                        # Analyze what this statement actually does
                        if isinstance(stmt, ast.Expr):
                            call_info = self._extract_call_info(stmt.value)
                            if call_info:
                                node_info.update(call_info)

                        graph["nodes"].append(node_info)
                else:
                    # Regular if statement
                    control_flow.append(
                        {
                            "type": "If",
                            "lineno": getattr(node, "lineno", 0),
                            "body_statements": len(node.body),
                            "has_else": len(node.orelse) > 0,
                        }
                    )
            elif isinstance(node, ast.For):
                control_flow.append(
                    {
                        "type": "For",
                        "lineno": getattr(node, "lineno", 0),
                        "body_statements": len(node.body),
                        "has_else": len(node.orelse) > 0,
                    }
                )
            elif isinstance(node, ast.While):
                control_flow.append(
                    {
                        "type": "While",
                        "lineno": getattr(node, "lineno", 0),
                        "body_statements": len(node.body),
                        "has_else": len(node.orelse) > 0,
                    }
                )
            elif isinstance(node, ast.Try):
                control_flow.append(
                    {
                        "type": "Try",
                        "lineno": getattr(node, "lineno", 0),
                        "body_statements": len(node.body),
                        "handlers": len(node.handlers),
                        "has_else": len(node.orelse) > 0,
                        "has_finally": len(node.finalbody) > 0,
                    }
                )

        graph["control_flow"] = control_flow

        return graph

    def _extract_call_info(self, expr: ast.expr) -> Optional[Dict[str, Any]]:
        """Extract function call information from an expression."""
        if isinstance(expr, ast.Call):
            # This is a direct function call
            func_name = self._get_function_name(expr.func)
            return {
                "call_type": "function_call",
                "function_called": func_name,
                "args_count": len(expr.args),
                "keywords_count": len(expr.keywords),
            }
        elif isinstance(expr, ast.Attribute):
            # This might be a method call like obj.method()
            if isinstance(expr.value, ast.Name):
                return {
                    "call_type": "method_call",
                    "object": expr.value.id,
                    "method": expr.attr,
                }
        elif isinstance(expr, ast.BinOp):
            # Check if binary operation involves function calls
            left_call = self._extract_call_info(expr.left) if hasattr(expr, "left") else None
            right_call = self._extract_call_info(expr.right) if hasattr(expr, "right") else None

            if left_call or right_call:
                return {
                    "call_type": "binary_operation",
                    "left_call": left_call,
                    "right_call": right_call,
                    "operator": type(expr.op).__name__,
                }

        return None

    def _get_function_name(self, func: ast.expr) -> str:
        """Get the name of a function being called."""
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            # Handle cases like module.function
            if isinstance(func.value, ast.Name):
                return f"{func.value.id}.{func.attr}"
            else:
                return func.attr
        else:
            return str(func)

    def _recognize_patterns(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize common control flow patterns."""
        recognized = {
            "guard_clauses": [],
            "early_returns": [],
            "nested_conditionals": [],
            "complex_loops": [],
            "exception_handling": [],
            "boolean_chains": [],
        }

        # Recognize guard clauses (early returns with simple conditions)
        for if_stmt in patterns["if_statements"]:
            if if_stmt["test_complexity"] <= 2 and if_stmt["body_complexity"] <= 1:
                recognized["guard_clauses"].append(if_stmt)

        # Recognize early returns
        recognized["early_returns"] = patterns["early_returns"]

        # Recognize nested conditionals
        for if_stmt in patterns["if_statements"]:
            if if_stmt["nested_level"] > 2:
                recognized["nested_conditionals"].append(if_stmt)

        # Recognize complex loops
        for loop in patterns["for_loops"] + patterns["while_loops"]:
            if loop["body_complexity"] > 5 or loop["nested_level"] > 2:
                recognized["complex_loops"].append(loop)

        # Recognize exception handling patterns
        for try_block in patterns["try_blocks"]:
            if try_block["handlers"] > 2 or try_block["nested_level"] > 1:
                recognized["exception_handling"].append(try_block)

        # Recognize boolean chains
        for bool_expr in patterns["boolean_expressions"]:
            if bool_expr["complexity"] > 3 or bool_expr["nested_booleans"] > 1:
                recognized["boolean_chains"].append(bool_expr)

        return recognized


def test_control_flow_analyzer():
    """Test the control flow analyzer."""
    analyzer = ControlFlowAnalyzer()

    # Test with a complex file
    test_file = "src/enhanced_activity_generator.py"

    # Run analysis
    result = analyzer.analyze_control_flow(test_file)

    if result["analysis_success"]:
        print("Control Flow Analysis Results:")
        print("=" * 50)

        print(f"\nPatterns Found:")
        for pattern_type, patterns in result["patterns"].items():
            print(f"  {pattern_type}: {len(patterns)}")

        print(f"\nComplexity Metrics:")
        print(f"  Total If Statements: {len(result['patterns']['if_statements'])}")
        print(f"  Total Loops: {len(result['patterns']['for_loops']) + len(result['patterns']['while_loops'])}")
        print(f"  Total Try Blocks: {len(result['patterns']['try_blocks'])}")
        print(f"  Boolean Expressions: {len(result['patterns']['boolean_expressions'])}")

        print(f"\nRecognized Patterns:")
        for pattern_type, patterns in result["recognized_patterns"].items():
            print(f"  {pattern_type}: {len(patterns)}")

        # Print detailed boolean expressions
        if result["patterns"]["boolean_expressions"]:
            print(f"\nDetailed Boolean Expressions:")
            for i, bool_expr in enumerate(result["patterns"]["boolean_expressions"][:3]):  # Show first 3
                print(f"  {i + 1}. Line {bool_expr['lineno']}: {bool_expr['operator']} (complexity: {bool_expr['complexity']})")

    else:
        print(f"Analysis failed: {result['error']}")

    return result


if __name__ == "__main__":
    test_control_flow_analyzer()
