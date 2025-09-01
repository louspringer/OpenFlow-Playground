#!/usr/bin/env python3
"""
Enhanced Reverse Engineer V2 - With Pattern Detection

Purpose: Extract complete method implementations with pattern detection and transformation
"""

import ast
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

# PatternDetector import removed - not implemented


class EnhancedReverseEngineerV2:
    """Enhanced reverse engineer with pattern detection and transformation"""

    def __init__(self) -> None:
        self.model_data: dict[str, Any] = {}
        self.cached_nodes: list[ast.AST] | None = None
        # self.pattern_detector = PatternDetector()  # Not implemented

    def reverse_engineer_file(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer a Python file into a comprehensive model with pattern detection"""
        try:
            print(f"🔍 Reverse engineering with pattern detection: {file_path}")

            # Generate unique model ID with timestamp
            model_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            print(f"🆔 Generated Model ID: {model_id} at {timestamp}")

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                source_lines = content.split("\n")

            # Parse AST
            tree = ast.parse(content)
            self.cached_nodes = list(ast.walk(tree))

            # Add model metadata
            self.model_data["model_id"] = model_id
            self.model_data["model_timestamp"] = timestamp
            self.model_data["source_file"] = file_path
            self.model_data["source_lines"] = source_lines

            # Extract comprehensive model
            self._extract_module_docstring(tree, content)
            self._extract_file_metadata(tree, content)
            self._extract_imports(tree)
            self._extract_used_names(tree)
            self._extract_module_assignments(tree)
            self._extract_classes(tree, source_lines)
            self._extract_module_functions(tree, source_lines)
            self._extract_file_structure(tree, content)

            print(f"🆔 Model {model_id} completed with {len(self.cached_nodes)} AST nodes")
            return self.model_data

        except Exception as e:
            print(f"❌ Error reverse engineering {file_path}: {e}")
            return {}

    def _extract_method_info_enhanced(self, func_node: ast.FunctionDef, source_lines: list[str]) -> dict[str, Any] | None:
        """Extract comprehensive method information with pattern detection"""
        try:
            # Detect test methods - only methods that start with "test_" are actual test methods
            is_test_method = func_node.name.startswith("test_")
            return_type = "None" if is_test_method else self._extract_type_annotation(func_node.returns)

            method_info: dict[str, Any] = {
                "name": func_node.name,
                "signature": self._build_method_signature(func_node),
                "docstring": "",
                "decorators": [],
                "line_number": getattr(func_node, "lineno", 0),
                "return_type": return_type,
                "parameters": self._extract_parameters(func_node.args),
                "is_test_method": is_test_method,
            }

            # Extract method docstring
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Constant):
                    docstring = func_node.body[0].value.value
                    if isinstance(docstring, str):
                        method_info["docstring"] = docstring.strip()

            # Extract method body content with pattern detection
            if func_node.body:
                method_body = []
                detected_patterns = []

                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        # Skip docstring lines
                        continue

                    # Detect patterns in this statement
                    patterns = self.pattern_detector.detect_patterns_in_node(stmt, source_lines)
                    detected_patterns.extend(patterns)

                    # Convert AST node back to source code with proper line structure
                    try:
                        import astor

                        body_source = astor.to_source(stmt)
                        # Split into lines and preserve structure
                        body_lines = body_source.strip().split("\n")
                        for line in body_lines:
                            if line.strip():  # Skip empty lines
                                method_body.append(line.rstrip())
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_source = ast.unparse(stmt)
                            # Split into lines and preserve structure
                            body_lines = body_source.strip().split("\n")
                            for line in body_lines:
                                if line.strip():  # Skip empty lines
                                    method_body.append(line.rstrip())
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"

                    # Add pattern information to the method
                    if detected_patterns:
                        method_info["detected_patterns"] = [
                            {
                                "pattern_type": p.pattern_type,
                                "description": p.description,
                                "best_practice": p.best_practice,
                                "line_number": p.line_number,
                                "confidence": p.confidence,
                                "transformed_code": p.transformed_code,
                            }
                            for p in detected_patterns
                        ]
                        method_info["pattern_summary"] = self.pattern_detector.get_pattern_summary(detected_patterns)

                        # Add best practice recommendations
                        method_info["best_practice_recommendations"] = [f"Line {p.line_number}: {p.best_practice}" for p in detected_patterns]
                else:
                    method_info["implementation_status"] = "skeleton"

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_method_info_enhanced: {type(e).__name__}: {e}")
            return None

    def _extract_async_method_info_enhanced(self, func_node: ast.AsyncFunctionDef, source_lines: list[str]) -> dict[str, Any] | None:
        """Extract comprehensive async method information with pattern detection"""
        try:
            # Detect test methods - only methods that start with "test_" are actual test methods
            is_test_method = func_node.name.startswith("test_")
            return_type = "None" if is_test_method else self._extract_type_annotation(func_node.returns)

            method_info: dict[str, Any] = {
                "name": func_node.name,
                "signature": self._build_async_method_signature(func_node),
                "docstring": "",
                "decorators": [],
                "line_number": getattr(func_node, "lineno", 0),
                "return_type": return_type,
                "parameters": self._extract_parameters(func_node.args),
                "is_async": True,
                "is_test_method": is_test_method,
            }

            # Extract method docstring
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Constant):
                    docstring = func_node.body[0].value.value
                    if isinstance(docstring, str):
                        method_info["docstring"] = docstring.strip()

            # Extract method body content with pattern detection
            if func_node.body:
                method_body = []
                detected_patterns = []

                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        # Skip docstring lines
                        continue

                    # Detect patterns in this statement
                    patterns = self.pattern_detector.detect_patterns_in_node(stmt, source_lines)
                    detected_patterns.extend(patterns)

                    # Convert AST node back to source code with proper line structure
                    try:
                        import astor

                        body_source = astor.to_source(stmt)
                        # Split into lines and preserve structure
                        body_lines = body_source.strip().split("\n")
                        for line in body_lines:
                            if line.strip():  # Skip empty lines
                                method_body.append(line.rstrip())
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_source = ast.unparse(stmt)
                            # Split into lines and preserve structure
                            body_lines = body_source.strip().split("\n")
                            for line in body_lines:
                                if line.strip():  # Skip empty lines
                                    method_body.append(line.rstrip())
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"

                    # Add pattern information to the method
                    if detected_patterns:
                        method_info["detected_patterns"] = [
                            {
                                "pattern_type": p.pattern_type,
                                "description": p.description,
                                "best_practice": p.best_practice,
                                "line_number": p.line_number,
                                "confidence": p.confidence,
                                "transformed_code": p.transformed_code,
                            }
                            for p in detected_patterns
                        ]
                        method_info["pattern_summary"] = self.pattern_detector.get_pattern_summary(detected_patterns)

                        # Add best practice recommendations
                        method_info["best_practice_recommendations"] = [f"Line {p.line_number}: {p.best_practice}" for p in detected_patterns]
                else:
                    method_info["implementation_status"] = "skeleton"

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_async_method_info_enhanced: {type(e).__name__}: {e}")
            return None

    def _build_method_signature(self, func_node: ast.FunctionDef) -> str:
        """Build complete method signature string"""
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":  # Skip self parameter
                param_name = arg.arg
                param_type = self._extract_type_annotation(arg.annotation)
                params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = self._extract_type_annotation(func_node.returns)

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        return f"{func_node.name}(self) -> {return_type}"

    def _build_async_method_signature(self, func_node: ast.AsyncFunctionDef) -> str:
        """Build complete async method signature string"""
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":  # Skip self parameter
                param_name = arg.arg
                param_type = self._extract_type_annotation(arg.annotation)
                params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = self._extract_type_annotation(func_node.returns)

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        return f"{func_node.name}(self) -> {return_type}"

    def _extract_parameters(self, args: ast.arguments) -> list[dict[str, Any]]:
        """Extract detailed parameter information"""
        parameters = []
        for arg in args.args:
            if arg.arg != "self":
                param_info = {
                    "name": arg.arg,
                    "type": self._extract_type_annotation(arg.annotation),
                    "default": None,
                }
                parameters.append(param_info)
        return parameters

    def _extract_type_annotation(self, annotation: ast.expr | None) -> str:
        """Extract type annotation with enhanced analysis"""
        if annotation is None:
            return "Any"
        if isinstance(annotation, ast.Name):
            return annotation.id
        if isinstance(annotation, ast.Constant):
            return annotation.value
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if hasattr(annotation, "slice"):
                    slice_value = annotation.slice
                    if isinstance(slice_value, ast.Name):
                        return f"{base_type}[{slice_value.id}]"
                    if isinstance(slice_value, ast.Tuple):
                        slice_types = []
                        for elt in slice_value.elts:
                            if isinstance(elt, ast.Name):
                                slice_types.append(elt.id)
                            elif isinstance(elt, ast.Constant):
                                slice_types.append(str(elt.value))
                        return f"{base_type}[{', '.join(slice_types)}]"
        return "Any"

    def _extract_module_docstring(self, tree: ast.Module, content: str) -> None:
        """Extract module docstring"""
        try:
            if tree.body and isinstance(tree.body[0], ast.Expr):
                if isinstance(tree.body[0].value, ast.Constant):
                    docstring = tree.body[0].value.value
                    if isinstance(docstring, str):
                        self.model_data["module_docstring"] = docstring.strip()
                        return
            self.model_data["module_docstring"] = ""
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_docstring: {e}")
            self.model_data["module_docstring"] = ""

    def _extract_file_metadata(self, tree: ast.Module, content: str) -> None:
        """Extract file metadata"""
        try:
            lines = content.split("\n")
            has_main = any("if __name__ == '__main__'" in line for line in lines)
            is_test_file = any("test_" in line for line in lines)

            self.model_data["file_metadata"] = {
                "executable": has_main,
                "is_test_file": is_test_file,
                "has_main_block": has_main,
                "file_type": "module",
                "line_count": len(lines),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_metadata: {e}")

    def _extract_imports(self, tree: ast.Module) -> None:
        """Extract import statements"""
        try:
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = ", ".join(alias.name for alias in node.names)
                    imports.append(f"from {module} import {names}")

            self.model_data["imports"] = imports
        except Exception as e:
            print(f"🚨 ERROR in _extract_imports: {e}")

    def _extract_used_names(self, tree: ast.Module) -> None:
        """Extract used names from the AST"""
        try:
            used_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)
                    if isinstance(node.attr, str):
                        used_names.add(node.attr)

            self.model_data["used_names"] = list(used_names)
        except Exception as e:
            print(f"🚨 ERROR in _extract_used_names: {e}")

    def _extract_module_assignments(self, tree: ast.Module) -> None:
        """Extract module-level assignments"""
        try:
            assignments = []
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assignments.append(target.id)

            self.model_data["module_assignments"] = assignments
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_assignments: {e}")

    def _extract_classes(self, tree: ast.AST, source_lines: list[str]) -> None:
        """Extract class information with pattern detection"""
        try:
            components = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "description": "",
                        "status": "implemented",
                        "methods": [],
                        "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                        "class_decorators": [],
                        "implementation_status": "implemented",
                    }

                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._extract_method_info_enhanced(item, source_lines)
                            if method_info:
                                class_info["methods"].append(method_info)
                        elif isinstance(item, ast.AsyncFunctionDef):
                            method_info = self._extract_async_method_info_enhanced(item, source_lines)
                            if method_info:
                                class_info["methods"].append(method_info)

                    components[node.name] = class_info

            self.model_data["components"] = components
        except Exception as e:
            print(f"🚨 ERROR in _extract_classes: {e}")

    def _extract_module_functions(self, tree: ast.AST, source_lines: list[str]) -> None:
        """Extract module functions with pattern detection"""
        try:
            module_functions = []
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    method_info = self._extract_method_info_enhanced(node, source_lines)
                    if method_info:
                        module_functions.append(method_info)
                elif isinstance(node, ast.AsyncFunctionDef):
                    method_info = self._extract_async_method_info_enhanced(node, source_lines)
                    if method_info:
                        module_functions.append(method_info)

            self.model_data["module_functions"] = module_functions
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_functions: {e}")

    def _extract_file_structure(self, tree: ast.Module, content: str) -> None:
        """Extract file structure information"""
        try:
            lines = content.split("\n")
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
            comment_lines = len([line for line in lines if line.strip().startswith("#")])
            blank_lines = len([line for line in lines if not line.strip()])

            self.model_data["file_structure"] = {
                "total_lines": len(lines),
                "code_lines": code_lines,
                "comment_lines": comment_lines,
                "blank_lines": blank_lines,
                "total_nodes": len(self.cached_nodes),
                "class_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.ClassDef)]),
                "function_nodes": len([n for n in self.cached_nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
                "import_nodes": len([n for n in self.cached_nodes if isinstance(n, (ast.Import, ast.ImportFrom))]),
                "expression_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.Expr)]),
                "assignment_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.Assign)]),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_structure: {e}")


def main() -> None:
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_reverse_engineer_v2.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Reverse engineer the file with pattern detection
    engineer = EnhancedReverseEngineerV2()
    model = engineer.reverse_engineer_file(file_path)

    # Save the model
    output_file = "enhanced_reverse_engineered_model_with_patterns.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ Model with pattern detection saved to: {output_file}")
    print(f"📦 Components: {len(model.get('components', {}))}")
    print(f"📏 Total Lines: {model.get('file_structure', {}).get('total_lines', 0)}")

    # Show pattern summary
    total_patterns = 0
    for component in model.get("components", {}).values():
        for method in component.get("methods", []):
            if "detected_patterns" in method:
                total_patterns += len(method["detected_patterns"])

    for func in model.get("module_functions", []):
        if "detected_patterns" in func:
            total_patterns += len(func["detected_patterns"])

    print(f"🔍 Total patterns detected: {total_patterns}")


if __name__ == "__main__":
    import sys

    main()
