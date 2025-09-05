#!/usr/bin/env python3
"""
AST Extractor - Reflective Module

Focused AST extraction module that handles all AST parsing and data extraction.
This module is self-monitoring, self-cleaning, and test-aware for RM compliance.
"""

import ast
import logging
import time
from typing import Any, Dict, List, Optional

# Setup logger for RM compliance
logger = logging.getLogger(__name__)


class ASTExtractor:
    """
    AST Extractor - RM Compliant Version.

    Only does what we actually need:
    - Parse Python files into AST
    - Extract module information
    - Extract classes and functions
    - Extract imports and metadata
    - Test-aware
    """

    def __init__(self):
        """Initialize the AST extractor."""
        self._test_environment = self._detect_test_environment()
        self._extraction_stats = {"files_processed": 0, "errors": 0, "total_nodes": 0}

        logger.info("✅ AST Extractor initialized with RM compliance")

    def _detect_test_environment(self) -> bool:
        """RM compliance: self-aware of testing environment."""
        import sys
        import os

        return "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ or "unittest" in sys.modules

    def parse_file(self, file_path: str) -> Optional[ast.AST]:
        """Parse a Python file into an AST."""
        start_time = time.time()

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            node_count = len(list(ast.walk(tree)))

            # Update stats
            self._extraction_stats["files_processed"] += 1
            self._extraction_stats["total_nodes"] += node_count

            parse_time = time.time() - start_time
            logger.info(f"✅ Parsed {file_path}: {node_count} nodes in {parse_time:.3f}s")

            return tree

        except FileNotFoundError:
            logger.error(f"❌ File not found: {file_path}")
            self._extraction_stats["errors"] += 1
            return None
        except SyntaxError as e:
            logger.error(f"❌ Syntax error in {file_path}: {e}")
            self._extraction_stats["errors"] += 1
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error parsing {file_path}: {e}")
            self._extraction_stats["errors"] += 1
            return None

    def extract_module_docstring(self, tree: ast.AST, content: str) -> str:
        """Extract module docstring."""
        try:
            if tree.body and isinstance(tree.body[0], ast.Expr):
                if isinstance(tree.body[0].value, ast.Constant):
                    docstring = tree.body[0].value.value
                    if isinstance(docstring, str):
                        return docstring.strip()
            return ""
        except Exception as e:
            logger.warning(f"Failed to extract module docstring: {e}")
            return ""

    def extract_file_metadata(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Extract file metadata."""
        try:
            lines = content.split("\n")
            return {
                "total_lines": len(lines),
                "non_empty_lines": len([line for line in lines if line.strip()]),
                "comment_lines": len([line for line in lines if line.strip().startswith("#")]),
                "import_lines": len([line for line in lines if line.strip().startswith(("import ", "from "))]),
            }
        except Exception as e:
            logger.warning(f"Failed to extract file metadata: {e}")
            return {}

    def extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract imports from AST."""
        imports = []

        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({"type": "import", "module": alias.name, "alias": alias.asname, "line_number": getattr(node, "lineno", 0)})
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append({"type": "from_import", "module": node.module or "", "name": alias.name, "alias": alias.asname, "line_number": getattr(node, "lineno", 0)})
        except Exception as e:
            logger.warning(f"Failed to extract imports: {e}")

        return imports

    def extract_classes(self, tree: ast.AST, source_lines: List[str]) -> List[Dict[str, Any]]:
        """Extract class information from AST."""
        classes = []

        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "line_number": getattr(node, "lineno", 0),
                        "docstring": "",
                        "bases": [self._extract_type_annotation(base) for base in node.bases],
                        "decorators": [self._extract_decorator_name(dec) for dec in node.decorator_list],
                        "methods": [],
                    }

                    # Extract class docstring
                    if node.body and isinstance(node.body[0], ast.Expr):
                        if isinstance(node.body[0].value, ast.Constant):
                            docstring = node.body[0].value.value
                            if isinstance(docstring, str):
                                class_info["docstring"] = docstring.strip()

                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._extract_method_info(item, source_lines)
                            if method_info:
                                class_info["methods"].append(method_info)

                    classes.append(class_info)
        except Exception as e:
            logger.warning(f"Failed to extract classes: {e}")

        return classes

    def extract_module_functions(self, tree: ast.AST, source_lines: List[str]) -> List[Dict[str, Any]]:
        """Extract module-level functions from AST."""
        functions = []

        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not self._is_nested_function(node, tree):
                    function_info = self._extract_method_info(node, source_lines)
                    if function_info:
                        functions.append(function_info)
        except Exception as e:
            logger.warning(f"Failed to extract module functions: {e}")

        return functions

    def _extract_method_info(self, func_node: ast.FunctionDef, source_lines: List[str]) -> Optional[Dict[str, Any]]:
        """Extract method/function information with enhanced analysis."""
        try:
            is_test_method = func_node.name.startswith("test_")
            return_type = "None" if is_test_method else self._extract_type_annotation(func_node.returns)

            method_info = {
                "name": func_node.name,
                "signature": self._build_method_signature(func_node),
                "docstring": "",
                "decorators": [self._extract_decorator_name(dec) for dec in func_node.decorator_list],
                "line_number": getattr(func_node, "lineno", 0),
                "return_type": return_type,
                "parameters": self._extract_parameters(func_node.args),
                "is_test_method": is_test_method,
                "is_async": False,
                "activity_model": {},  # Activity modeling for methods
                "control_flow": {},  # Control flow analysis
                "behavior_patterns": [],  # Behavior pattern detection
            }

            # Extract method docstring
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Constant):
                    docstring = func_node.body[0].value.value
                    if isinstance(docstring, str):
                        method_info["docstring"] = docstring.strip()

            # Extract method body content for round-trip functionality
            if func_node.body:
                method_body = []
                activity_sequence = []  # Track activity sequence
                control_flow_map = {}  # Track control flow

                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        # Skip docstring lines
                        continue

                    # Analyze statement for activity modeling
                    stmt_analysis = self._analyze_statement_activity(stmt)
                    if stmt_analysis:
                        activity_sequence.append(stmt_analysis)

                    # Track control flow
                    control_info = self._analyze_control_flow(stmt)
                    if control_info:
                        control_flow_map[stmt.lineno] = control_info

                    # Convert AST node back to source code
                    try:
                        import astor

                        body_source = astor.to_source(stmt)
                        body_lines = body_source.strip().split("\n")
                        for line in body_lines:
                            if line.strip():
                                method_body.append(line.rstrip())
                    except ImportError:
                        try:
                            body_source = ast.unparse(stmt)
                            body_lines = body_source.strip().split("\n")
                            for line in body_lines:
                                if line.strip():
                                    method_body.append(line.rstrip())
                        except AttributeError:
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                # Add body content to method info
                method_info["body_content"] = method_body
                method_info["activity_model"] = {
                    "sequence": activity_sequence,
                    "complexity_score": self._calculate_complexity_score(activity_sequence),
                    "activity_categories": self._categorize_activities(activity_sequence),
                }
                method_info["control_flow"] = {
                    "map": control_flow_map,
                    "max_nesting": self._calculate_nesting_depth(control_flow_map),
                    "has_conditionals": any(cf.get("type") == "conditional" for cf in control_flow_map.values()),
                    "has_loops": any(cf.get("type") == "loop" for cf in control_flow_map.values()),
                    "has_exceptions": any(cf.get("type") == "exception" for cf in control_flow_map.values()),
                }

                # Detect behavior patterns
                method_info["behavior_patterns"] = self._detect_behavior_patterns(activity_sequence, control_flow_map)

                method_info["implementation_status"] = "implemented"
            else:
                method_info["body_content"] = []
                method_info["implementation_status"] = "skeleton"

            return method_info
        except Exception as e:
            logger.warning(f"Failed to extract method info for {func_node.name}: {e}")
            return None

    def _extract_parameters(self, args: ast.arguments) -> List[Dict[str, Any]]:
        """Extract parameter information."""
        parameters = []

        try:
            for arg in args.args:
                param_info = {"name": arg.arg, "type": self._extract_type_annotation(arg.annotation), "default": None}
                parameters.append(param_info)
        except Exception as e:
            logger.warning(f"Failed to extract parameters: {e}")

        return parameters

    def _extract_type_annotation(self, annotation) -> str:
        """Extract type annotation."""
        if annotation is None:
            return "Any"

        try:
            if isinstance(annotation, ast.Name):
                return annotation.id
            elif isinstance(annotation, ast.Constant):
                return str(annotation.value)
            else:
                return "Any"
        except Exception as e:
            logger.warning(f"Failed to extract type annotation: {e}")
            return "Any"

    def _extract_decorator_name(self, decorator) -> str:
        """Extract decorator name."""
        try:
            if isinstance(decorator, ast.Name):
                return decorator.id
            elif isinstance(decorator, ast.Attribute):
                return decorator.attr
            else:
                return "unknown_decorator"
        except Exception as e:
            logger.warning(f"Failed to extract decorator name: {e}")
            return "unknown_decorator"

    def _is_nested_function(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is nested inside a class or other function."""
        try:
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node != func_node:
                    for child in ast.walk(node):
                        if child == func_node:
                            return True
            return False
        except Exception as e:
            logger.warning(f"Failed to check if function is nested: {e}")
            return False

    def _build_method_signature(self, func_node: ast.FunctionDef) -> str:
        """Build complete method signature string."""
        params = []
        for arg in func_node.args.args:
            param_type = self._extract_type_annotation(arg.annotation)
            params.append(f"{arg.arg}: {param_type}")

        return_type = self._extract_type_annotation(func_node.returns)
        return f"def {func_node.name}({', '.join(params)}) -> {return_type}:"

    def _analyze_statement_activity(self, stmt: ast.stmt) -> Optional[Dict[str, Any]]:
        """Analyze a statement for activity modeling."""
        try:
            activity = {"type": "unknown", "line_number": getattr(stmt, "lineno", 0), "complexity": 1, "nested_structures": self._has_nested_structures(stmt)}

            if isinstance(stmt, ast.Assign):
                activity["type"] = "assignment"
                activity["targets"] = [self._extract_target_name(target) for target in stmt.targets]
            elif isinstance(stmt, ast.Expr):
                if isinstance(stmt.value, ast.Call):
                    activity["type"] = "function_call"
                    activity["function"] = self._extract_function_name(stmt.value)
                else:
                    activity["type"] = "expression"
            elif isinstance(stmt, ast.Return):
                activity["type"] = "return"
            elif isinstance(stmt, ast.If):
                activity["type"] = "conditional"
                activity["complexity"] = 2
            elif isinstance(stmt, (ast.For, ast.While)):
                activity["type"] = "loop"
                activity["complexity"] = 3
            elif isinstance(stmt, ast.Try):
                activity["type"] = "exception_handling"
                activity["complexity"] = 3
            elif isinstance(stmt, ast.With):
                activity["type"] = "context_manager"
                activity["complexity"] = 2

            return activity
        except Exception as e:
            logger.warning(f"Failed to analyze statement activity: {e}")
            return None

    def _analyze_control_flow(self, stmt: ast.stmt) -> Optional[Dict[str, Any]]:
        """Analyze control flow for a statement."""
        try:
            control_info = {"type": "statement", "line_number": getattr(stmt, "lineno", 0), "nesting_level": self._calculate_statement_nesting(stmt)}

            if isinstance(stmt, ast.If):
                control_info["type"] = "conditional"
            elif isinstance(stmt, (ast.For, ast.While)):
                control_info["type"] = "loop"
            elif isinstance(stmt, ast.Try):
                control_info["type"] = "exception"
            elif isinstance(stmt, ast.With):
                control_info["type"] = "context"

            return control_info
        except Exception as e:
            logger.warning(f"Failed to analyze control flow: {e}")
            return None

    def _detect_behavior_patterns(self, activity_sequence: List, control_flow: Dict) -> List[str]:
        """Detect common behavior patterns in method execution."""
        patterns = []

        try:
            # Pattern: Data processing
            if any(act.get("type") == "assignment" for act in activity_sequence):
                if any(act.get("type") == "loop" for act in activity_sequence):
                    patterns.append("data_processing")

            # Pattern: Validation
            if any(act.get("type") == "conditional" for act in activity_sequence):
                if any(act.get("type") == "return" for act in activity_sequence):
                    patterns.append("validation")

            # Pattern: Error handling
            if any(cf.get("type") == "exception" for cf in control_flow.values()):
                patterns.append("error_handling")

            # Pattern: Resource management
            if any(act.get("type") == "context_manager" for act in activity_sequence):
                patterns.append("resource_management")

            # Pattern: API interaction
            if any(act.get("type") == "function_call" for act in activity_sequence):
                patterns.append("api_interaction")

        except Exception as e:
            logger.warning(f"Failed to detect behavior patterns: {e}")

        return patterns

    def _categorize_activities(self, activity_sequence: List) -> Dict[str, int]:
        """Categorize activities by type."""
        categories = {}
        for activity in activity_sequence:
            activity_type = activity.get("type", "unknown")
            categories[activity_type] = categories.get(activity_type, 0) + 1
        return categories

    def _calculate_complexity_score(self, activity_sequence: List) -> int:
        """Calculate complexity score based on activities."""
        try:
            base_complexity = len(activity_sequence)
            nested_complexity = sum(act.get("complexity", 1) for act in activity_sequence)
            return base_complexity + nested_complexity
        except Exception as e:
            logger.warning(f"Failed to calculate complexity score: {e}")
            return 1

    def _calculate_nesting_depth(self, control_flow: Dict) -> int:
        """Calculate maximum nesting depth."""
        try:
            return max((cf.get("nesting_level", 0) for cf in control_flow.values()), default=0)
        except Exception as e:
            logger.warning(f"Failed to calculate nesting depth: {e}")
            return 0

    def _has_nested_structures(self, stmt: ast.stmt) -> bool:
        """Check if statement has nested control structures."""
        try:
            for child in ast.walk(stmt):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                    return True
            return False
        except Exception as e:
            logger.warning(f"Failed to check nested structures: {e}")
            return False

    def _calculate_statement_nesting(self, stmt: ast.stmt) -> int:
        """Calculate nesting level of a statement."""
        try:
            level = 0
            current = stmt
            while hasattr(current, "parent"):
                current = current.parent
                if isinstance(current, (ast.If, ast.For, ast.While, ast.Try)):
                    level += 1
            return level
        except Exception as e:
            logger.warning(f"Failed to calculate statement nesting: {e}")
            return 0

    def _extract_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from call node."""
        try:
            if isinstance(call_node.func, ast.Name):
                return call_node.func.id
            elif isinstance(call_node.func, ast.Attribute):
                return call_node.func.attr
            else:
                return "unknown_function"
        except Exception as e:
            logger.warning(f"Failed to extract function name: {e}")
            return "unknown_function"

    def _extract_target_name(self, target) -> str:
        """Extract target name from assignment target."""
        try:
            if isinstance(target, ast.Name):
                return target.id
            elif isinstance(target, ast.Attribute):
                return target.attr
            else:
                return "unknown_target"
        except Exception as e:
            logger.warning(f"Failed to extract target name: {e}")
            return "unknown_target"

    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get extraction statistics."""
        return self._extraction_stats.copy()

    def reset_stats(self) -> None:
        """Reset extraction statistics."""
        self._extraction_stats = {"files_processed": 0, "errors": 0, "total_nodes": 0}
        logger.info("✅ Extraction stats reset")

    def is_healthy(self) -> bool:
        """Check if this module is currently healthy."""
        error_rate = self._extraction_stats["errors"] / max(1, self._extraction_stats["files_processed"])
        return error_rate < 0.1  # Less than 10% error rate

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        total_files = self._extraction_stats["files_processed"]
        error_rate = self._extraction_stats["errors"] / max(1, total_files)

        return {
            "files_processed": total_files,
            "errors": self._extraction_stats["errors"],
            "total_nodes": self._extraction_stats["total_nodes"],
            "error_rate": error_rate,
            "is_healthy": self.is_healthy(),
        }


def main() -> None:
    """Main function for executable module."""
    extractor = ASTExtractor()

    # Test extraction
    test_file = "src/round_trip_engineering/ast_extractor.py"
    tree = extractor.parse_file(test_file)

    if tree:
        print(f"✅ Successfully parsed {test_file}")

        # Extract information
        docstring = extractor.extract_module_docstring(tree, "")
        imports = extractor.extract_imports(tree)
        classes = extractor.extract_classes(tree, [])
        functions = extractor.extract_module_functions(tree, [])

        print(f"📊 Extracted: {len(imports)} imports, {len(classes)} classes, {len(functions)} functions")

        # Get stats
        stats = extractor.get_extraction_stats()
        print(f"📈 Stats: {stats}")
    else:
        print(f"❌ Failed to parse {test_file}")


if __name__ == "__main__":
    main()
