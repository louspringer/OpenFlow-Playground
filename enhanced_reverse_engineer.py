#!/usr/bin/env python3
"""
Enhanced Reverse Engineering using Enhanced AST Parser
"""

import ast
import json
from typing import Any, Optional

# Import the enhanced AST parser using the wrapper
try:
    from enhanced_ast_wrapper import get_enhanced_ast_linter

    linter_class = get_enhanced_ast_linter()
    if linter_class:
        ENHANCED_AST_AVAILABLE = True
        ASTEnhancedLinter = linter_class
        print("🚀 Enhanced AST parser available!")
    else:
        ENHANCED_AST_AVAILABLE = False
        print("⚠️  Enhanced AST parser not available, using basic parser")
except ImportError:
    print("⚠️  Enhanced AST parser not available, using basic parser")
    ENHANCED_AST_AVAILABLE = False


class EnhancedReverseEngineer:
    """Enhanced Python code reverse engineer using AST analysis"""

    def __init__(self) -> None:
        self.model_data: dict[str, Any] = {}
        self.ast_linter = None
        self._cached_nodes = None  # Cache for AST nodes

        # Try to initialize enhanced AST linter
        try:
            from enhanced_ast_wrapper import get_enhanced_ast_linter

            self.ast_linter = get_enhanced_ast_linter()
            print("✅ Enhanced AST linter initialized")
        except Exception as e:
            print(f"⚠️  Enhanced AST linter not available: {e}")

    def _cache_tree_nodes(self, tree: ast.AST) -> None:
        """Cache AST nodes to avoid multiple ast.walk() calls"""
        if self._cached_nodes is None:
            try:
                # Debug: see what ast.walk returns
                walk_result = ast.walk(tree)
                print(f"🔍 Debug: ast.walk(tree) type: {type(walk_result)}")

                # Convert to list and check
                nodes_list = list(walk_result)
                print(f"🔍 Debug: list(ast.walk(tree)) type: {type(nodes_list)}")
                print(f"🔍 Debug: list(ast.walk(tree)) length: {len(nodes_list)}")
                print(
                    f"🔍 Debug: First few nodes: {[type(n).__name__ for n in nodes_list[:5]]}"
                )

                # Cache the nodes
                self._cached_nodes = nodes_list
                print(f"✅ Successfully cached {len(nodes_list)} AST nodes")

            except Exception as e:
                print(f"🚨 ERROR in _cache_tree_nodes: {type(e).__name__}: {e}")
                print(f"🚨 Tree type: {type(tree)}")
                print(f"🚨 Tree content: {tree}")
                # Don't cache on error
                self._cached_nodes = []

    def _get_cached_nodes(self) -> list[ast.AST]:
        """Get cached AST nodes or empty list if not available"""
        if self._cached_nodes is None:
            print("⚠️  No cached nodes available, returning empty list")
            return []
        try:
            print(f"🔍 Returning {len(self._cached_nodes)} cached nodes")
            return self._cached_nodes
        except Exception as e:
            print(f"🚨 ERROR in _get_cached_nodes: {type(e).__name__}: {e}")
            print(f"🚨 _cached_nodes type: {type(self._cached_nodes)}")
            print(f"🚨 _cached_nodes content: {self._cached_nodes}")
            return []

    def reverse_engineer(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer Python file to enhanced model"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST once and cache nodes
            tree = ast.parse(content)
            self._cache_tree_nodes(tree)

            # Initialize model data
            self.model_data = {
                "system_name": "",
                "description": "",
                "purpose": "",
                "graph_api_level": 1,
                "projection_system": "default",
                "components": {},
                "module_functions": [],
                "imports": [],
                "module_docstring": "",
                "file_structure": {},
            }

            # Extract all information using cached nodes
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

    def _extract_module_docstring(self, tree: ast.AST, content: str) -> None:
        """Extract comprehensive module docstring"""
        try:
            print(f"🔍 _extract_module_docstring: content type: {type(content)}")
            print(
                f"🔍 _extract_module_docstring: content length: {len(content) if isinstance(content, str) else 'Not a string'}"
            )

            # Use cached nodes instead of calling ast.walk again
            all_nodes = self._get_cached_nodes()

            for node in all_nodes:
                if isinstance(node, ast.Module):
                    if node.body and isinstance(node.body[0], ast.Expr):
                        if isinstance(node.body[0].value, ast.Constant):
                            docstring = node.body[0].value.value
                            print(
                                f"🔍 _extract_module_docstring: docstring type: {type(docstring)}"
                            )
                            print(
                                f"🔍 _extract_module_docstring: docstring content: {repr(docstring)}"
                            )

                            if isinstance(docstring, str):
                                self.model_data["module_docstring"] = docstring
                                self._parse_module_docstring(docstring)
                                break
                            print(f"⚠️  Docstring is not a string: {type(docstring)}")
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_docstring: {type(e).__name__}: {e}")
            print(f"🚨 Content type: {type(content)}")
            print(f"🚨 Content content: {content}")
            print(f"🚨 Tree type: {type(tree)}")

    def _parse_module_docstring(self, docstring: str) -> None:
        """Parse module docstring for metadata"""
        try:
            print(f"🔍 _parse_module_docstring: docstring type: {type(docstring)}")
            print(f"🔍 _parse_module_docstring: docstring content: {repr(docstring)}")

            lines = docstring.strip().split("\n")
            print(f"🔍 _parse_module_docstring: lines type: {type(lines)}")
            print(f"🔍 _parse_module_docstring: lines content: {lines}")

            if lines:
                self.model_data["system_name"] = lines[0].strip()
                if len(lines) > 1:
                    # Skip empty lines to find the first non-empty description
                    description_line = 1
                    while (
                        description_line < len(lines)
                        and not lines[description_line].strip()
                    ):
                        description_line += 1
                    if description_line < len(lines):
                        self.model_data["description"] = lines[description_line].strip()

                # Look for purpose and other metadata
                # For package __init__.py files, the purpose is often in the docstring
                if len(lines) > 2:
                    # Look for additional description lines (skip empty lines)
                    for i in range(2, len(lines)):
                        line = lines[i].strip()
                        if (
                            line
                            and not line.startswith("Purpose:")
                            and not line.startswith("Graph API Level:")
                            and not line.startswith("Projection System:")
                        ):
                            # Skip if this is the same as the description
                            if line != self.model_data.get("description", ""):
                                self.model_data["purpose"] = line
                                break

                for line in lines:
                    if line.startswith("Purpose:"):
                        self.model_data["purpose"] = line.replace(
                            "Purpose:", ""
                        ).strip()
                    elif line.startswith("Graph API Level:"):
                        try:
                            level = int(line.split(":")[1].strip())
                            self.model_data["graph_api_level"] = level
                        except (ValueError, IndexError):
                            pass
                    elif line.startswith("Projection System:"):
                        self.model_data["projection_system"] = line.split(":")[
                            1
                        ].strip()

            print("✅ Successfully parsed module docstring")

        except Exception as e:
            print(f"🚨 ERROR in _parse_module_docstring: {type(e).__name__}: {e}")
            print(f"🚨 Docstring type: {type(docstring)}")
            print(f"🚨 Docstring content: {docstring}")
            print(
                f"🚨 Lines type: {type(lines) if 'lines' in locals() else 'Not defined'}"
            )
            print(
                f"🚨 Lines content: {lines if 'lines' in locals() else 'Not defined'}"
            )

    def _extract_file_metadata(self, tree: ast.AST, content: str) -> None:
        """Extract file-level metadata like executable status, test status, etc."""
        try:
            # Check if file has shebang (executable)
            source_lines = content.split("\n")
            has_shebang = (
                source_lines[0].strip().startswith("#!") if source_lines else False
            )

            # Check if file contains test code
            all_nodes = self._get_cached_nodes()
            is_test_file = False
            has_main_block = False

            for node in all_nodes:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    if "test" in node.name.lower():
                        is_test_file = True
                        break

            # Check for main block
            for node in all_nodes:
                if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                    if (
                        isinstance(node.test.left, ast.Name)
                        and node.test.left.id == "__name__"
                    ):
                        has_main_block = True
                        break

            # Determine file type
            file_type = "module"
            if is_test_file:
                file_type = "test"
            elif has_main_block:
                file_type = "script"
            elif has_shebang:
                file_type = "executable"

            self.model_data["file_metadata"] = {
                "executable": has_shebang,
                "is_test_file": is_test_file,
                "has_main_block": has_main_block,
                "file_type": file_type,
                "line_count": len(source_lines),
            }

            print(f"✅ Extracted file metadata: {self.model_data['file_metadata']}")

        except Exception as e:
            print(f"🚨 ERROR in _extract_file_metadata: {type(e).__name__}: {e}")
            self.model_data["file_metadata"] = {
                "executable": False,
                "is_test_file": False,
                "has_main_block": False,
                "file_type": "unknown",
                "line_count": 0,
            }

    def _extract_imports(self, tree: ast.AST) -> None:
        """Extract import statements with enhanced analysis and usage detection"""
        imports = []
        used_names = set()

        try:
            # Use cached nodes instead of calling ast.walk again
            all_nodes = self._get_cached_nodes()

            # First pass: collect all import statements
            import_nodes = []
            for node in all_nodes:
                if isinstance(node, ast.Import):
                    import_nodes.append(("import", node, None))
                elif isinstance(node, ast.ImportFrom):
                    import_nodes.append(("from", node, node.module))

            # Second pass: analyze usage to determine which imports are needed
            for node in all_nodes:
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Handle attribute access like 'pytest.fixture'
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)

            # Third pass: build imports list with usage analysis
            for import_type, node, module in import_nodes:
                if import_type == "import":
                    for alias in node.names:
                        if alias.asname:
                            imports.append(f"import {alias.name} as {alias.asname}")
                        else:
                            imports.append(f"import {alias.name}")
                elif import_type == "from":
                    for alias in node.names:
                        if alias.asname:
                            imports.append(
                                f"from {module} import {alias.name} as {alias.asname}"
                            )
                        else:
                            imports.append(f"from {module} import {alias.name}")

            # Store both raw imports and usage analysis
            self.model_data["imports"] = imports
            self.model_data["used_names"] = list(used_names)
        except Exception as e:
            print(f"🚨 ERROR in _extract_imports: {type(e).__name__}: {e}")
            print(
                f"🚨 Node type: {type(node) if 'node' in locals() else 'Not defined'}"
            )
            print(
                f"🚨 Node names type: {type(node.names) if 'node' in locals() and hasattr(node, 'names') else 'Not defined'}"
            )
            print(
                f"🚨 Node names content: {node.names if 'node' in locals() and hasattr(node, 'names') else 'Not defined'}"
            )
            print(f"⚠️  Error extracting imports: {e}")

    def _extract_module_assignments(self, tree: ast.AST) -> None:
        """Extract module-level assignments like __version__, __author__, etc."""
        try:
            all_nodes = self._get_cached_nodes()
            module_assignments = {}

            for node in all_nodes:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            if var_name.startswith("__") and var_name.endswith("__"):
                                # This is a module-level special variable
                                if isinstance(node.value, ast.Constant):
                                    module_assignments[var_name] = node.value.value
                                elif isinstance(node.value, ast.List):
                                    # Extract list contents
                                    list_contents = []
                                    for elt in node.value.elts:
                                        if isinstance(elt, ast.Constant):
                                            list_contents.append(elt.value)
                                        else:
                                            list_contents.append(str(elt))
                                    module_assignments[var_name] = list_contents
                                else:
                                    # For complex values, store the string representation
                                    module_assignments[var_name] = str(node.value)

            self.model_data["module_assignments"] = module_assignments
            print(f"✅ Extracted module assignments: {module_assignments}")

        except Exception as e:
            print(f"🚨 ERROR in _extract_module_assignments: {type(e).__name__}: {e}")
            self.model_data["module_assignments"] = {}

    def _extract_classes(self, tree: ast.AST) -> None:
        """Extract class definitions with enhanced analysis"""
        try:
            # Use cached nodes instead of calling ast.walk again
            all_nodes = self._get_cached_nodes()

            for node in all_nodes:
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    class_info = self._extract_class_info_enhanced(node)
                    if class_info:
                        self.model_data["components"][class_name] = class_info
        except Exception as e:
            print(f"⚠️  Error extracting classes: {e}")

    def _extract_class_info_enhanced(
        self, class_node: ast.ClassDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive class information"""
        try:
            print(
                f"🔍 _extract_class_info_enhanced: class_node.body type: {type(class_node.body)}"
            )
            print(
                f"🔍 _extract_class_info_enhanced: class_node.body content: {class_node.body}"
            )

            class_info = {
                "responsibility": "",
                "methods": [],
                "implementation_status": "implemented",
                "notes": "",
                "validation_rules": {},
                "example_usage": {},
                "user_experience": {},
                "interaction_flow": {},
                "class_decorators": [],
                "bases": [],
                "line_number": getattr(class_node, "lineno", 0),
            }

            # Extract class docstring
            if class_node.body and isinstance(class_node.body[0], ast.Expr):
                if isinstance(class_node.body[0].value, ast.Constant):
                    docstring = class_node.body[0].value.value
                    if isinstance(docstring, str):
                        class_info["responsibility"] = docstring.strip()

            # Extract base classes
            for base in class_node.bases:
                if isinstance(base, ast.Name):
                    class_info["bases"].append(base.id)

            # Extract decorators
            for decorator in class_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    class_info["class_decorators"].append(decorator.id)

            # Extract methods with enhanced analysis (including async methods)
            for item in class_node.body:
                if isinstance(item, ast.FunctionDef):
                    method_info = self._extract_method_info_enhanced(item)
                    if method_info:
                        class_info["methods"].append(method_info)
                elif isinstance(item, ast.AsyncFunctionDef):
                    method_info = self._extract_async_method_info_enhanced(item)
                    if method_info:
                        class_info["methods"].append(method_info)

            print(f"✅ Successfully extracted class info for {class_node.name}")
            return class_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_class_info_enhanced: {type(e).__name__}: {e}")
            print(f"🚨 Class node type: {type(class_node)}")
            print(
                f"🚨 Class node body type: {type(class_node.body) if hasattr(class_node, 'body') else 'No body attribute'}"
            )
            print(
                f"🚨 Class node body content: {class_node.body if hasattr(class_node, 'body') else 'No body attribute'}"
            )
            return None

    def _extract_method_info_enhanced(
        self, func_node: ast.FunctionDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive method information"""
        try:
            print(
                f"🔍 _extract_method_info_enhanced: func_node.body type: {type(func_node.body)}"
            )
            print(
                f"🔍 _extract_method_info_enhanced: func_node.body content: {func_node.body}"
            )

            # Include __init__ methods for complete round-trip functionality
            # if func_node.name == "__init__":
            #     return None  # Skip __init__ methods

            # Detect test methods and set appropriate return type
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

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_method_info_enhanced: {type(e).__name__}: {e}")
            print(f"🚨 Func node type: {type(func_node)}")
            print(
                f"🚨 Func node name: {func_node.name if hasattr(func_node, 'name') else 'No name'}"
            )
            print(
                f"🚨 Func node body type: {type(func_node.body) if hasattr(func_node, 'body') else 'No body attribute'}"
            )
            print(
                f"🚨 Func node body content: {func_node.body if hasattr(func_node, 'body') else 'No body attribute'}"
            )
            return None

    def _extract_async_method_info_enhanced(
        self, func_node: ast.AsyncFunctionDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive async method information"""
        try:
            print(
                f"🔍 _extract_async_method_info_enhanced: func_node.body type: {type(func_node.body)}"
            )
            print(
                f"🔍 _extract_async_method_info_enhanced: func_node.body content: {func_node.body}"
            )

            # Include __init__ methods for complete round-trip functionality
            # if func_node.name == "__init__":
            #     return None  # Skip __init__ methods

            # Detect test methods and set appropriate return type
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

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(
                f"🚨 ERROR in _extract_async_method_info_enhanced: {type(e).__name__}: {e}"
            )
            print(f"🚨 Func node type: {type(func_node)}")
            print(
                f"🚨 Func node name: {func_node.name if hasattr(func_node, 'name') else 'No name'}"
            )
            print(
                f"🚨 Func node body type: {type(func_node.body) if hasattr(func_node, 'body') else 'No body attribute'}"
            )
            print(
                f"🚨 Func node body content: {func_node.body if hasattr(func_node, 'body') else 'No body attribute'}"
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
        return f"{func_node.name}(self) -> {return_type}"

    def _extract_parameters(self, args: ast.arguments) -> list[dict[str, Any]]:
        """Extract detailed parameter information"""
        parameters = []

        try:
            print(f"🔍 _extract_parameters: args type: {type(args)}")
            print(f"🔍 _extract_parameters: args.args type: {type(args.args)}")
            print(f"🔍 _extract_parameters: args.args content: {args.args}")

            for arg in args.args:
                if arg.arg != "self":
                    param_info = {
                        "name": arg.arg,
                        "type": self._extract_type_annotation(arg.annotation),
                        "default": None,
                    }
                    parameters.append(param_info)

            print(f"✅ Successfully extracted {len(parameters)} parameters")
            return parameters

        except Exception as e:
            print(f"🚨 ERROR in _extract_parameters: {type(e).__name__}: {e}")
            print(f"🚨 Args type: {type(args)}")
            print(
                f"🚨 Args args type: {type(args.args) if hasattr(args, 'args') else 'No args attribute'}"
            )
            print(
                f"🚨 Args args content: {args.args if hasattr(args, 'args') else 'No args attribute'}"
            )
            return []

    def _extract_type_annotation(self, annotation) -> str:
        """Extract type annotation with enhanced analysis"""
        if annotation is None:
            return "Any"

        if isinstance(annotation, ast.Name):
            return annotation.id
        if isinstance(annotation, ast.Constant):
            return annotation.value
        if isinstance(annotation, ast.Subscript):
            # Handle generic types like List[str], Dict[str, int]
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if hasattr(annotation, "slice"):
                    slice_type = self._extract_type_annotation(annotation.slice)
                    return f"{base_type}[{slice_type}]"
                return base_type
        elif isinstance(annotation, ast.Tuple):
            # Handle tuple types like tuple[str, int]
            types = [self._extract_type_annotation(t) for t in annotation.elts]
            return f"tuple[{', '.join(types)}]"

        return "Any"

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

        # Build async method signature string (just the method name and parameters)
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        return f"{func_node.name}(self) -> {return_type}"

    def _extract_module_functions(self, tree: ast.AST) -> None:
        """Extract module-level functions (not inside classes)"""
        functions = []
        try:
            # Use cached nodes instead of calling ast.walk again
            all_nodes = self._get_cached_nodes()

            for node in all_nodes:
                if isinstance(node, ast.FunctionDef):
                    # Check if function is at module level (not inside a class)
                    if not self._is_inside_class(node):
                        func_info = self._extract_function_info_enhanced(node)
                        if func_info:
                            functions.append(func_info)

            self.model_data["module_functions"] = functions
        except Exception as e:
            print(f"⚠️  Error extracting module functions: {e}")

    def _is_inside_class(self, func_node: ast.FunctionDef) -> bool:
        """Check if a function is inside a class"""
        try:
            # Use cached nodes instead of calling ast.walk again
            all_nodes = self._get_cached_nodes()

            for node in all_nodes:
                if isinstance(node, ast.ClassDef):
                    print(f"🔍 _is_inside_class: node.body type: {type(node.body)}")
                    print(f"🔍 _is_inside_class: node.body content: {node.body}")

                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item == func_node:
                            return True
            return False
        except Exception as e:
            print(f"🚨 ERROR in _is_inside_class: {type(e).__name__}: {e}")
            print(f"🚨 Func node type: {type(func_node)}")
            print(
                f"🚨 Func node name: {func_node.name if hasattr(func_node, 'name') else 'No name'}"
            )
            return False

    def _extract_function_info_enhanced(
        self, func_node: ast.FunctionDef
    ) -> Optional[dict[str, Any]]:
        """Extract comprehensive function information"""
        func_info = {
            "name": func_node.name,
            "signature": self._build_function_signature(func_node),
            "docstring": "",
            "decorators": [],
            "line_number": getattr(func_node, "lineno", 0),
            "return_type": self._extract_type_annotation(func_node.returns),
            "parameters": self._extract_parameters(func_node.args),
        }

        # Extract function docstring
        if func_node.body and isinstance(func_node.body[0], ast.Expr):
            if isinstance(func_node.body[0].value, ast.Constant):
                docstring = func_node.body[0].value.value
                if isinstance(docstring, str):
                    func_info["docstring"] = docstring.strip()

        # Extract decorators
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Name):
                func_info["decorators"].append(decorator.id)

        return func_info

    def _build_function_signature(self, func_node: ast.FunctionDef) -> str:
        """Build complete function signature string"""
        params = []
        for arg in func_node.args.args:
            param_name = arg.arg
            param_type = self._extract_type_annotation(arg.annotation)
            params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = self._extract_type_annotation(func_node.returns)

        # Build function signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}({param_str}) -> {return_type}"
        return f"{func_node.name}() -> {return_type}"

    def _extract_file_structure(self, tree: ast.AST, content: str) -> None:
        """Extract overall file structure information"""
        try:
            lines = content.split("\n")

            # Get cached nodes with error logging
            all_nodes = self._get_cached_nodes()
            print(f"🔍 _extract_file_structure: Got {len(all_nodes)} cached nodes")
            print(f"🔍 _extract_file_structure: all_nodes type: {type(all_nodes)}")
            print(f"🔍 _extract_file_structure: all_nodes content: {all_nodes}")

            self.model_data["file_structure"] = {
                "total_lines": len(lines),
                "code_lines": len(
                    [
                        line
                        for line in lines
                        if line.strip() and not line.strip().startswith("#")
                    ]
                ),
                "comment_lines": len(
                    [line for line in lines if line.strip().startswith("#")]
                ),
                "blank_lines": len([line for line in lines if not line.strip()]),
                "total_nodes": len(all_nodes),
                "class_nodes": len(
                    [node for node in all_nodes if isinstance(node, ast.ClassDef)]
                ),
                "function_nodes": len(
                    [node for node in all_nodes if isinstance(node, ast.FunctionDef)]
                ),
                "import_nodes": len(
                    [
                        node
                        for node in all_nodes
                        if isinstance(node, (ast.Import, ast.ImportFrom))
                    ]
                ),
                "expression_nodes": len(
                    [node for node in all_nodes if isinstance(node, ast.Expr)]
                ),
                "assignment_nodes": len(
                    [node for node in all_nodes if isinstance(node, ast.Assign)]
                ),
                "return_nodes": len(
                    [node for node in all_nodes if isinstance(node, ast.Return)]
                ),
            }

            print(
                f"✅ Successfully extracted file structure with {len(all_nodes)} nodes"
            )

        except Exception as e:
            print(f"🚨 ERROR in _extract_file_structure: {type(e).__name__}: {e}")
            print(
                f"🔍 _extract_file_structure: all_nodes type: {type(all_nodes) if 'all_nodes' in locals() else 'Not defined'}"
            )
            print(
                f"🔍 _extract_file_structure: all_nodes content: {all_nodes if 'all_nodes' in locals() else 'Not defined'}"
            )
            print(f"⚠️  Error extracting file structure: {e}")

    def _clean_model_data(self) -> None:
        """Clean model data to ensure no whitespace issues"""
        try:
            # Clean string fields
            for key in ["system_name", "description", "purpose", "projection_system"]:
                if key in self.model_data and isinstance(self.model_data[key], str):
                    self.model_data[key] = self.model_data[key].strip()

            # Clean module docstring
            if "module_docstring" in self.model_data and isinstance(
                self.model_data["module_docstring"], str
            ):
                self.model_data["module_docstring"] = self.model_data[
                    "module_docstring"
                ].strip()

            # Clean imports list
            if "imports" in self.model_data and isinstance(
                self.model_data["imports"], list
            ):
                self.model_data["imports"] = [
                    imp.strip() for imp in self.model_data["imports"] if imp.strip()
                ]

            # Clean used_names list
            if "used_names" in self.model_data and isinstance(
                self.model_data["used_names"], list
            ):
                self.model_data["used_names"] = [
                    name.strip()
                    for name in self.model_data["used_names"]
                    if name.strip()
                ]

            print("✅ Model data cleaned successfully")

        except Exception as e:
            print(f"🚨 ERROR in _clean_model_data: {type(e).__name__}: {e}")


def main() -> None:
    """Main function to test enhanced reverse engineering"""
    import sys

    reverse_engineer = EnhancedReverseEngineer()

    # Get file path from command line argument or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"🔍 Enhanced Reverse Engineering Test for: {file_path}")
    else:
        file_path = "scripts/simple_calculator.py"
        print("🔍 Enhanced Reverse Engineering Test (using default file)")

    print("=" * 50)

    model = reverse_engineer.reverse_engineer(file_path)

    if model:
        # Clean the model data before saving
        reverse_engineer._clean_model_data()

        # Save the enhanced reverse engineered model
        output_file = "enhanced_reverse_engineered_model.json"
        with open(output_file, "w") as f:
            json.dump(model, f, indent=2)

        print("✅ Enhanced reverse engineered model saved to " + output_file)

        # Display comprehensive information
        print("\n📊 Enhanced Reverse Engineered Model:")
        print(f"   System: {model.get('system_name', 'Unknown')}")
        print(f"   Description: {model.get('description', 'No description')}")
        print(f"   Purpose: {model.get('purpose', 'No purpose')}")
        print(f"   Graph API Level: {model.get('graph_api_level', 'Unknown')}")
        print(f"   Projection System: {model.get('projection_system', 'Unknown')}")
        print(f"   Components: {len(model.get('components', {}))}")
        print(f"   Module Functions: {len(model.get('module_functions', []))}")
        print(f"   Imports: {len(model.get('imports', []))}")

        # Show components
        for comp_name, comp_info in model.get("components", {}).items():
            print(f"   📦 {comp_name}: {len(comp_info.get('methods', []))} methods")

        # Show module functions
        for func in model.get("module_functions", []):
            print(
                f"   ⚙️  {func.get('name', 'Unknown')}: {func.get('signature', 'No signature')}"
            )

        # Show file structure
        structure = model.get("file_structure", {})
        print(f"   📏 Total Lines: {structure.get('total_lines', 0)}")
        print(f"   🏗️  Classes: {structure.get('classes_count', 0)}")
        print(f"   ⚙️  Functions: {structure.get('functions_count', 0)}")
        print(f"   📦 Imports: {structure.get('imports_count', 0)}")

        # Show enhanced AST availability
        if ENHANCED_AST_AVAILABLE:
            print("   🚀 Enhanced AST parser: Available and used")
        else:
            print("   ⚠️  Enhanced AST parser: Not available, used basic parser")

    else:
        print("❌ Failed to reverse engineer the file")

    print("\n" + "=" * 50)
    print("🔍 Enhanced Reverse Engineering Complete")


if __name__ == "__main__":
    main()
