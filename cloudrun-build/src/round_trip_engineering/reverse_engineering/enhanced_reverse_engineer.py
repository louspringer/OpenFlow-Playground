#!/usr/bin/env python3
"""
Enhanced Reverse Engineer
Performs enhanced reverse engineering with AST parsing and code preservation
"""

import ast
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule


logger = logging.getLogger(__name__)


class EnhancedReverseEngineer(BaseReflectiveModule):
    """Performs enhanced reverse engineering with AST parsing and code preservation"""

    def __init__(self) -> None:
        super().__init__()
        self.parsed_files: Dict[str, Dict[str, Any]] = {}

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "reverse_engineering": [
                "parse_python_file",
                "extract_ast_model",
                "preserve_code_structure",
            ],
            "ast_analysis": [
                "analyze_class_structure",
                "analyze_function_structure",
                "extract_method_signatures",
            ],
        }

    def parse_python_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a Python file and extract its structure"""
        logger.info(f"🎯 Parsing Python file: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Extract model
            extracted_model = self._extract_ast_model(tree, content, file_path)

            # Store parsed file
            self.parsed_files[file_path] = extracted_model

            logger.info(f"✅ Successfully parsed {file_path}")
            return extracted_model

        except Exception as e:
            logger.error(f"❌ Failed to parse {file_path}: {e}")
            raise

    def _extract_ast_model(self, tree: ast.AST, content: str, file_path: str) -> Dict[str, Any]:
        """Extract model from AST"""
        file_name = Path(file_path).stem

        model = {
            "name": file_name,
            "type": "module",
            "file_path": file_path,
            "classes": {},
            "functions": {},
            "imports": [],
            "metadata": {
                "total_lines": len(content.splitlines()),
                "ast_nodes": len(list(ast.walk(tree))),
            },
        }

        # Extract imports
        model["imports"] = self._extract_imports(tree)

        # Extract classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_data = self._extract_class_data(node, content)
                model["classes"][class_data["name"]] = class_data

        # Extract functions (not in classes)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not self._is_method(node, tree):
                func_data = self._extract_function_data(node, content)
                model["functions"][func_data["name"]] = func_data

        return model

    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements"""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno,
                        }
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(
                        {
                            "type": "from_import",
                            "module": module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno,
                        }
                    )

        return imports

    def _extract_class_data(self, node: ast.ClassDef, content: str) -> Dict[str, Any]:
        """Extract class data from AST node"""
        class_data = {
            "name": node.name,
            "bases": [self._get_base_name(base) for base in node.bases],
            "docstring": ast.get_docstring(node) or "",
            "methods": {},
            "attributes": [],
            "line_start": node.lineno,
            "line_end": node.end_lineno or node.lineno,
            "source": self._get_source_segment(content, node),
        }

        # Extract methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_data = self._extract_method_data(item, content)
                class_data["methods"][method_data["name"]] = method_data
            elif isinstance(item, ast.Assign):
                # Extract class attributes
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_data["attributes"].append(
                            {
                                "name": target.id,
                                "type": self._get_type_annotation(item.value),
                                "line": item.lineno,
                            }
                        )

        return class_data

    def _extract_method_data(self, node: ast.FunctionDef, content: str) -> Dict[str, Any]:
        """Extract method data from AST node"""
        method_data = {
            "name": node.name,
            "parameters": self._extract_parameters(node.args),
            "return_type": self._get_return_type(node),
            "docstring": ast.get_docstring(node) or "",
            "line_start": node.lineno,
            "line_end": node.end_lineno or node.lineno,
            "source": self._get_source_segment(content, node),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }

        return method_data

    def _extract_function_data(self, node: ast.FunctionDef, content: str) -> Dict[str, Any]:
        """Extract function data from AST node"""
        func_data = {
            "name": node.name,
            "parameters": self._extract_parameters(node.args),
            "return_type": self._get_return_type(node),
            "docstring": ast.get_docstring(node) or "",
            "line_start": node.lineno,
            "line_end": node.end_lineno or node.lineno,
            "source": self._get_source_segment(content, node),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }

        return func_data

    def _extract_parameters(self, args: ast.arguments) -> List[Dict[str, Any]]:
        """Extract parameter information from function arguments"""
        parameters = []

        # Handle positional arguments
        for arg in args.posonlyargs + args.args:
            param = {
                "name": arg.arg,
                "type": self._get_annotation_name(arg.annotation),
                "default": None,
            }
            parameters.append(param)

        # Handle keyword-only arguments
        for arg in args.kwonlyargs:
            param = {
                "name": arg.arg,
                "type": self._get_annotation_name(arg.annotation),
                "default": None,
            }
            parameters.append(param)

        # Handle defaults for positional arguments
        if args.defaults:
            for i, default in enumerate(args.defaults):
                if i < len(parameters):
                    parameters[i]["default"] = self._get_default_value(default)

        # Handle defaults for keyword-only arguments
        if args.kw_defaults:
            for i, default in enumerate(args.kw_defaults):
                if default is not None and i < len(parameters):
                    param_idx = len(args.posonlyargs) + len(args.args) + i
                    if param_idx < len(parameters):
                        parameters[param_idx]["default"] = self._get_default_value(default)

        return parameters

    def _get_annotation_name(self, annotation: Optional[ast.expr]) -> str:
        """Get the name of a type annotation"""
        if annotation is None:
            return "Any"

        try:
            # Try to unparse the annotation
            if hasattr(ast, "unparse"):
                return ast.unparse(annotation)
            else:
                # Fallback for older Python versions
                return str(annotation)
        except:
            return str(annotation)

    def _get_default_value(self, default: ast.expr) -> Any:
        """Get the default value of a parameter"""
        try:
            if hasattr(ast, "unparse"):
                return ast.unparse(default)
            else:
                # Fallback for older Python versions
                return str(default)
        except:
            return str(default)

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Get the return type of a function"""
        if node.returns is None:
            return "Any"

        return self._get_annotation_name(node.returns)

    def _get_base_name(self, base: ast.expr) -> str:
        """Get the name of a base class"""
        try:
            if hasattr(ast, "unparse"):
                return ast.unparse(base)
            else:
                return str(base)
        except:
            return str(base)

    def _get_type_annotation(self, value: ast.expr) -> str:
        """Get the type annotation for a value"""
        if isinstance(value, ast.Constant):
            return type(value.value).__name__
        elif isinstance(value, ast.List):
            return "List[Any]"
        elif isinstance(value, ast.Dict):
            return "Dict[str, Any]"
        elif isinstance(value, ast.Tuple):
            return "Tuple[Any, ...]"
        else:
            return "Any"

    def _get_source_segment(self, content: str, node: ast.AST) -> str:
        """Get the source code segment for an AST node"""
        try:
            if hasattr(ast, "get_source_segment"):
                return ast.get_source_segment(content, node) or ""
            else:
                # Fallback for older Python versions
                lines = content.splitlines()
                start_line = node.lineno - 1  # AST uses 1-indexed lines
                end_line = (node.end_lineno or node.lineno) - 1
                return "\n".join(lines[start_line : end_line + 1])
        except:
            return ""

    def _is_method(self, node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is a method (defined inside a class)"""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False

    def get_parsed_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get a parsed file by path"""
        return self.parsed_files.get(file_path)

    def list_parsed_files(self) -> List[str]:
        """List all parsed file paths"""
        return list(self.parsed_files.keys())

    def clear_parsed_files(self) -> None:
        """Clear all parsed files"""
        self.parsed_files.clear()
        logger.info("✅ Cleared all parsed files")
