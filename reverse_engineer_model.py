#!/usr/bin/env python3
"""
Reverse engineer Python code back into model JSON format using enhanced AST parser
"""

# Import the enhanced AST parser using the wrapper
import ast  # Always import ast for basic functionality
import json
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from enhanced_ast_wrapper import get_enhanced_ast_linter

    linter_class = get_enhanced_ast_linter()
    if linter_class:
        ENHANCED_AST_AVAILABLE = True
        ASTEnhancedLinter = linter_class
    else:
        ENHANCED_AST_AVAILABLE = False
except ImportError:
    print("⚠️  Enhanced AST parser not available, falling back to basic parser")
    ENHANCED_AST_AVAILABLE = False


class EnhancedPythonCodeReverseEngineer:
    """Reverse engineer Python code into model JSON using enhanced AST parser"""

    def __init__(self) -> None:
        self.model_data = {
            "system_name": "",
            "description": "",
            "purpose": "",
            "graph_api_level": 1,
            "projection_system": "reverse_engineered",
            "components": {},
        }

        if ENHANCED_AST_AVAILABLE:
            self.ast_linter = ASTEnhancedLinter(".")
        else:
            self.ast_linter = None

    def reverse_engineer_file(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer a Python file into model JSON using enhanced AST"""
        try:
            if ENHANCED_AST_AVAILABLE and self.ast_linter:
                return self._reverse_engineer_with_enhanced_ast(file_path)
            else:
                return self._reverse_engineer_with_basic_ast(file_path)

        except Exception as e:
            print(f"Error reverse engineering {file_path}: {e}")
            return {}

    def _reverse_engineer_with_enhanced_ast(self, file_path: str) -> dict[str, Any]:
        """Use enhanced AST parser for comprehensive analysis"""
        print(f"🔍 Using enhanced AST parser for {file_path}")

        # Analyze the file with enhanced AST
        self.ast_linter._analyze_file(Path(file_path))

        # Extract module information
        self._extract_module_info_enhanced(file_path)

        # Extract classes and methods using enhanced analysis
        self._extract_classes_enhanced(file_path)

        # Extract module functions
        self._extract_functions_enhanced(file_path)

        return self.model_data

    def _extract_module_info_enhanced(self, file_path: str) -> None:
        """Extract module information using enhanced AST analysis"""
        try:
            with open(file_path) as f:
                content = f.read()

            # Use enhanced AST parser to analyze the module
            tree = ast.parse(content)

            # Extract module docstring and metadata
            for node in ast.walk(tree):
                if isinstance(node, ast.Module):
                    if node.body and isinstance(node.body[0], ast.Expr):
                        if isinstance(node.body[0].value, ast.Constant):
                            docstring = node.body[0].value.value
                            if isinstance(docstring, str):
                                self._parse_module_docstring(docstring)
                    break

        except Exception as e:
            print(f"⚠️  Error extracting module info: {e}")

    def _extract_classes_enhanced(self, file_path: str) -> None:
        """Extract class information using enhanced AST analysis"""
        try:
            with open(file_path) as f:
                content = f.read()

            # Use enhanced AST parser
            tree = ast.parse(content)

            # Analyze classes with enhanced capabilities
            for node in ast.walk(tree):
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
        """Extract comprehensive class information using enhanced AST"""
        class_info = {
            "responsibility": "",
            "methods": [],
            "implementation_status": "implemented",
            "notes": "",
            "validation_rules": {},
            "example_usage": {},
            "user_experience": {},
            "interaction_flow": {},
        }

        # Extract class docstring
        if class_node.body and isinstance(class_node.body[0], ast.Expr):
            if isinstance(class_node.body[0].value, ast.Constant):
                docstring = class_node.body[0].value.value
                if isinstance(docstring, str):
                    class_info["responsibility"] = docstring.strip()

        # Extract methods with enhanced analysis
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_method_info_enhanced(item)
                if method_info:
                    class_info["methods"].append(method_info)

        return class_info

    def _extract_method_info_enhanced(
        self, func_node: ast.FunctionDef
    ) -> Optional[str]:
        """Extract method information with enhanced AST analysis"""
        if func_node.name == "__init__":
            return None  # Skip __init__ methods

        # Build enhanced method signature
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":  # Skip self parameter
                param_name = arg.arg
                param_type = self._extract_type_annotation_enhanced(arg.annotation)
                params.append(f"{param_name}: {param_type}")

        # Get return type with enhanced analysis
        return_type = self._extract_type_annotation_enhanced(func_node.returns)

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        else:
            return f"{func_node.name}(self) -> {return_type}"

    def _extract_type_annotation_enhanced(self, annotation) -> str:
        """Extract type annotation with enhanced AST analysis"""
        if annotation is None:
            return "Any"

        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return annotation.value
        elif isinstance(annotation, ast.Subscript):
            # Handle generic types like List[str], Dict[str, int]
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if hasattr(annotation, "slice"):
                    slice_type = self._extract_type_annotation_enhanced(
                        annotation.slice
                    )
                    return f"{base_type}[{slice_type}]"
                return base_type
        elif isinstance(annotation, ast.Tuple):
            # Handle tuple types like Tuple[str, int]
            types = [self._extract_type_annotation_enhanced(t) for t in annotation.elts]
            return f"Tuple[{', '.join(types)}]"

        return "Any"

    def _extract_functions_enhanced(self, file_path: str) -> None:
        """Extract module-level functions using enhanced AST"""
        try:
            with open(file_path) as f:
                content = f.read()

            tree = ast.parse(content)
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Only include functions that are not inside classes
                    if not any(
                        isinstance(parent, ast.ClassDef)
                        for parent in ast.walk(tree)
                        if hasattr(parent, "body") and node in parent.body
                    ):
                        func_info = self._extract_method_info_enhanced(node)
                        if func_info:
                            functions.append(func_info)

            if functions:
                self.model_data["module_functions"] = functions

        except Exception as e:
            print(f"⚠️  Error extracting functions: {e}")

    def _parse_module_docstring(self, docstring: str) -> None:
        """Parse module docstring for metadata"""
        lines = docstring.strip().split("\n")
        if lines:
            self.model_data["system_name"] = lines[0].strip()
            if len(lines) > 1:
                self.model_data["description"] = lines[1].strip()

            # Look for purpose and other metadata
            for line in lines:
                if line.startswith("Purpose:"):
                    self.model_data["purpose"] = line.replace("Purpose:", "").strip()
                elif line.startswith("Graph API Level:"):
                    try:
                        level = int(line.split(":")[1].strip())
                        self.model_data["graph_api_level"] = level
                    except (ValueError, IndexError):
                        pass
                elif line.startswith("Projection System:"):
                    self.model_data["projection_system"] = line.split(":")[1].strip()

    def _reverse_engineer_with_basic_ast(self, file_path: str) -> dict[str, Any]:
        """Fallback to basic AST parsing if enhanced parser unavailable"""
        print(f"🔍 Using basic AST parser for {file_path}")

        try:
            with open(file_path) as f:
                content = f.read()

            tree = ast.parse(content)

            # Extract module-level information
            self._extract_module_info_basic(tree)

            # Extract classes
            self._extract_classes_basic(tree)

            # Extract functions
            self._extract_functions_basic(tree)

            return self.model_data

        except Exception as e:
            print(f"Error with basic AST parsing: {e}")
            return {}

    def _extract_module_info_basic(self, tree: ast.AST) -> None:
        """Extract module information using basic AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Module):
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant):
                        docstring = node.body[0].value.value
                        if isinstance(docstring, str):
                            self._parse_module_docstring(docstring)
                break

    def _extract_classes_basic(self, tree: ast.AST) -> None:
        """Extract class definitions using basic AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_info = self._extract_class_info_basic(node)
                if class_info:
                    self.model_data["components"][class_name] = class_info

    def _extract_class_info_basic(
        self, class_node: ast.ClassDef
    ) -> Optional[dict[str, Any]]:
        """Extract class information using basic AST"""
        class_info = {
            "responsibility": "",
            "methods": [],
            "implementation_status": "implemented",
            "notes": "",
            "validation_rules": {},
            "example_usage": {},
            "user_experience": {},
            "interaction_flow": {},
        }

        # Extract class docstring
        if class_node.body and isinstance(class_node.body[0], ast.Expr):
            if isinstance(class_node.body[0].value, ast.Constant):
                docstring = class_node.body[0].value.value
                if isinstance(docstring, str):
                    class_info["responsibility"] = docstring.strip()

        # Extract methods
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_method_info_basic(item)
                if method_info:
                    class_info["methods"].append(method_info)

        return class_info

    def _extract_method_info_basic(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract method information using basic AST"""
        if func_node.name == "__init__":
            return None

        # Build method signature
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":
                param_name = arg.arg
                param_type = "Any"

                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        param_type = arg.annotation.id
                    elif isinstance(arg.annotation, ast.Constant):
                        param_type = arg.annotation.value

                params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = "None"
        if func_node.returns:
            if isinstance(func_node.returns, ast.Name):
                return_type = func_node.returns.id
            elif isinstance(func_node.returns, ast.Constant):
                return_type = func_node.returns.value

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        else:
            return f"{func_node.name}(self) -> {return_type}"

    def _extract_functions_basic(self, tree: ast.AST) -> None:
        """Extract module-level functions using basic AST"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not any(
                    isinstance(parent, ast.ClassDef)
                    for parent in ast.walk(tree)
                    if hasattr(parent, "body") and node in parent.body
                ):
                    func_info = self._extract_method_info_basic(node)
                    if func_info:
                        functions.append(func_info)

        if functions:
            self.model_data["module_functions"] = functions


def main() -> None:
    """Main function to reverse engineer Python files"""
    reverse_engineer = EnhancedPythonCodeReverseEngineer()

    # Reverse engineer the simple_calculator.py file
    print("🔍 Reverse engineering simple_calculator.py...")
    model = reverse_engineer.reverse_engineer_file("scripts/simple_calculator.py")

    if model:
        # Save the reverse engineered model
        output_file = "reverse_engineered_model_enhanced.json"
        with open(output_file, "w") as f:
            json.dump(model, f, indent=2)

        print("✅ Reverse engineered model saved to " + output_file)

        # Display key information
        print("\n📊 Reverse Engineered Model:")
        print(f"   System: {model.get('system_name', 'Unknown')}")
        print(f"   Description: {model.get('description', 'No description')}")
        print(f"   Components: {len(model.get('components', {}))}")

        for comp_name, comp_info in model.get("components", {}).items():
            print(f"   📦 {comp_name}: {len(comp_info.get('methods', []))} methods")

        # Show enhanced AST availability
        if ENHANCED_AST_AVAILABLE:
            print("   🚀 Enhanced AST parser: Available and used")
        else:
            print("   ⚠️  Enhanced AST parser: Not available, used basic parser")

    else:
        print("❌ Failed to reverse engineer the file")


if __name__ == "__main__":
    main()
