#!/usr/bin/env python3
"""
Enhanced Reverse Engineer - Fixed Version

Purpose: Extract complete method implementations for true round-trip functionality
"""

import ast
import json
import os
from typing import Any, Dict, List, Optional


class EnhancedReverseEngineer:
    """Enhanced reverse engineer with method body extraction"""

    def __init__(self):
        self.model_data = {}
        self.cached_nodes = None

    def reverse_engineer_file(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer a Python file into a comprehensive model"""
        try:
            print(f"🔍 Reverse engineering: {file_path}")

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)
            self.cached_nodes = list(ast.walk(tree))

            # Extract comprehensive model
            self._extract_module_docstring(tree, content)
            self._extract_file_metadata(tree, content)
            self._extract_imports(tree)
            self._extract_module_assignments(tree)
            self._extract_classes(tree)
            self._extract_module_functions(tree)
            self._extract_file_structure(tree, content)

            return self.model_data

        except Exception as e:
            print(f"❌ Error reverse engineering {file_path}: {e}")
            return {}

    def _extract_method_info_enhanced(
        self, func_node: ast.FunctionDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive method information including body content"""
        try:
            # Detect test methods
            is_test_method = (
                func_node.name.startswith("test_") or "test" in func_node.name.lower()
            )
            return_type = (
                "None"
                if is_test_method
                else self._extract_type_annotation(func_node.returns)
            )

            method_info = {
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

            # Extract method body content for round-trip functionality
            if func_node.body:
                method_body = []
                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(
                        stmt.value, ast.Constant
                    ):
                        # Skip docstring lines
                        continue
                    # Convert AST node back to source code
                    try:
                        import astor

                        body_line = astor.to_source(stmt).strip()
                        if body_line:
                            method_body.append(body_line)
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_line = ast.unparse(stmt).strip()
                            if body_line:
                                method_body.append(body_line)
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"
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

    def _extract_async_method_info_enhanced(
        self, func_node: ast.AsyncFunctionDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive async method information including body content"""
        try:
            # Detect test methods
            is_test_method = (
                func_node.name.startswith("test_") or "test" in func_node.name.lower()
            )
            return_type = (
                "None"
                if is_test_method
                else self._extract_type_annotation(func_node.returns)
            )

            method_info = {
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

            # Extract method body content for round-trip functionality
            if func_node.body:
                method_body = []
                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(
                        stmt.value, ast.Constant
                    ):
                        # Skip docstring lines
                        continue
                    # Convert AST node back to source code
                    try:
                        import astor

                        body_line = astor.to_source(stmt).strip()
                        if body_line:
                            method_body.append(body_line)
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_line = ast.unparse(stmt).strip()
                            if body_line:
                                method_body.append(body_line)
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"
                else:
                    method_info["implementation_status"] = "skeleton"

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(
                f"🚨 ERROR in _extract_async_method_info_enhanced: {type(e).__name__}: {e}"
            )
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
        else:
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
        else:
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

    def _extract_type_annotation(self, annotation) -> str:
        """Extract type annotation with enhanced analysis"""
        if annotation is None:
            return "Any"
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return annotation.value
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if hasattr(annotation, "slice"):
                    slice_value = annotation.slice
                    if isinstance(slice_value, ast.Name):
                        return f"{base_type}[{slice_value.id}]"
                    elif isinstance(slice_value, ast.Tuple):
                        slice_types = []
                        for elt in slice_value.elts:
                            if isinstance(elt, ast.Name):
                                slice_types.append(elt.id)
                            elif isinstance(elt, ast.Constant):
                                slice_types.append(str(elt.value))
                        return f"{base_type}[{', '.join(slice_types)}]"
        return "Any"

    def _extract_module_docstring(self, tree: ast.AST, content: str) -> None:
        """Extract module docstring"""
        try:
            for node in self.cached_nodes:
                if isinstance(node, ast.Module):
                    if node.body and isinstance(node.body[0], ast.Expr):
                        if isinstance(node.body[0].value, ast.Constant):
                            docstring = node.body[0].value.value
                            if isinstance(docstring, str):
                                self.model_data["module_docstring"] = docstring
                                break
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_docstring: {e}")

    def _extract_file_metadata(self, tree: ast.AST, content: str) -> None:
        """Extract file metadata"""
        try:
            lines = content.split("\n")
            self.model_data["file_metadata"] = {
                "executable": content.startswith("#!/"),
                "is_test_file": any("test" in line.lower() for line in lines),
                "has_main_block": "__main__" in content,
                "file_type": "module",
                "line_count": len(lines),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_metadata: {e}")

    def _extract_imports(self, tree: ast.AST) -> None:
        """Extract imports"""
        try:
            imports = []
            for node in self.cached_nodes:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = [alias.name for alias in node.names]
                    imports.append(f"from {module} import {', '.join(names)}")
            self.model_data["imports"] = imports
        except Exception as e:
            print(f"🚨 ERROR in _extract_imports: {e}")

    def _extract_module_assignments(self, tree: ast.AST) -> None:
        """Extract module assignments"""
        try:
            self.model_data["module_assignments"] = {}
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_assignments: {e}")

    def _extract_classes(self, tree: ast.AST) -> None:
        """Extract class information"""
        try:
            components = {}
            for node in self.cached_nodes:
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "responsibility": "",
                        "methods": [],
                        "bases": [
                            base.id for base in node.bases if isinstance(base, ast.Name)
                        ],
                        "class_decorators": [],
                        "implementation_status": "implemented",
                    }

                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._extract_method_info_enhanced(item)
                            if method_info:
                                class_info["methods"].append(method_info)
                        elif isinstance(item, ast.AsyncFunctionDef):
                            method_info = self._extract_async_method_info_enhanced(item)
                            if method_info:
                                class_info["methods"].append(method_info)

                    components[node.name] = class_info

            self.model_data["components"] = components
        except Exception as e:
            print(f"🚨 ERROR in _extract_classes: {e}")

    def _extract_module_functions(self, tree: ast.AST) -> None:
        """Extract module functions"""
        try:
            self.model_data["module_functions"] = []
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_functions: {e}")

    def _extract_file_structure(self, tree: ast.AST, content: str) -> None:
        """Extract file structure information"""
        try:
            lines = content.split("\n")
            code_lines = len(
                [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ]
            )
            comment_lines = len(
                [line for line in lines if line.strip().startswith("#")]
            )
            blank_lines = len([line for line in lines if not line.strip()])

            self.model_data["file_structure"] = {
                "total_lines": len(lines),
                "code_lines": code_lines,
                "comment_lines": comment_lines,
                "blank_lines": blank_lines,
                "total_nodes": len(self.cached_nodes),
                "class_nodes": len(
                    [n for n in self.cached_nodes if isinstance(n, ast.ClassDef)]
                ),
                "function_nodes": len(
                    [
                        n
                        for n in self.cached_nodes
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ]
                ),
                "import_nodes": len(
                    [
                        n
                        for n in self.cached_nodes
                        if isinstance(n, (ast.Import, ast.ImportFrom))
                    ]
                ),
                "expression_nodes": len(
                    [n for n in self.cached_nodes if isinstance(n, ast.Expr)]
                ),
                "assignment_nodes": len(
                    [n for n in self.cached_nodes if isinstance(n, ast.Assign)]
                ),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_structure: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_reverse_engineer_fixed.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Reverse engineer the file
    engineer = EnhancedReverseEngineer()
    model = engineer.reverse_engineer_file(file_path)

    # Save the model
    output_file = "enhanced_reverse_engineered_model_fixed.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ Model saved to: {output_file}")
    print(f"📦 Components: {len(model.get('components', {}))}")
    print(f"📏 Total Lines: {model.get('file_structure', {}).get('total_lines', 0)}")


if __name__ == "__main__":
    import sys

    main()
