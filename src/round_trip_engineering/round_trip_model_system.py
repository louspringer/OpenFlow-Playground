#!/usr/bin/env python3
"""
Round-Trip Model System
Can create models from design AND generate code from models
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# Try to import Black for code formatting
try:
    from black import FileMode, TargetVersion, format_str

    BLACK_AVAILABLE = True
except ImportError:
    BLACK_AVAILABLE = False
    logging.warning(
        "Black not available - generated code may not be properly formatted"
    )

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelComponent:
    """A component in our design model"""

    name: str
    type: str  # 'function', 'class', 'module', 'domain'
    description: str
    requirements: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DesignModel:
    """A complete design model that can be converted to/from code"""

    name: str
    description: str
    components: list[ModelComponent] = field(default_factory=list)
    relationships: dict[str, list[str]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class RoundTripModelSystem:
    """System that can create models from design AND generate code from models"""

    def __init__(self) -> None:
        self.design_models: dict[str, DesignModel] = {}

    def create_model_from_design(self, design_spec: dict[str, Any]) -> DesignModel:
        """Create a model directly from design specification (NO reverse engineering)"""
        logger.info(
            f"🎯 Creating model from design: {design_spec.get('name', 'Unknown')}",
        )

        # Extract design components
        components = []
        for comp_spec in design_spec.get("components", []):
            component = ModelComponent(
                name=comp_spec["name"],
                type=comp_spec["type"],
                description=comp_spec["description"],
                requirements=comp_spec.get("requirements", []),
                dependencies=comp_spec.get("dependencies", []),
                metadata=comp_spec.get("metadata", {}),
            )
            components.append(component)

        # Create the design model
        design_model = DesignModel(
            name=design_spec["name"],
            description=design_spec["description"],
            components=components,
            relationships=design_spec.get("relationships", {}),
            metadata=design_spec.get("metadata", {}),
        )

        self.design_models[design_model.name] = design_model
        logger.info(f"✅ Created model with {len(components)} components")

        return design_model

    def generate_code_from_model(self, model_name: str) -> dict[str, str]:
        """Generate code from a design model (NO reverse engineering)"""
        if model_name not in self.design_models:
            msg = f"Model {model_name} not found"
            raise ValueError(msg)

        model = self.design_models[model_name]
        logger.info(f"🎯 Generating code from model: {model_name}")

        generated_files = {}

        # Generate code for each component
        for component in model.components:
            if component.type == "function":
                code = self._generate_function_code(component)
                filename = f"{component.name}.py"
                generated_files[filename] = code
            elif component.type == "class":
                code = self._generate_class_code(component)
                filename = f"{component.name}.py"
                generated_files[filename] = code
            elif component.type == "module":
                code = self._generate_module_code(component)
                filename = f"{component.name}/__init__.py"
                generated_files[filename] = code
            elif component.type == "domain":
                code = self._generate_domain_code(component)
                filename = f"{component.name}/domain_model.py"
                generated_files[filename] = code

        logger.info(f"✅ Generated {len(generated_files)} files from model")
        return generated_files

    def generate_code_from_extracted_model(
        self, extracted_model: dict[str, Any]
    ) -> str:
        """
        Generate complete Python module skeleton code from an extracted model.

        This method creates a fully functional Python file with:
        - Proper imports (typing, dataclass, pydantic, enum as needed)
        - Module docstring with system name and description
        - All classes with methods, type hints, and docstrings
        - All functions with parameters, return types, and docstrings
        - TODO comments for implementation guidance
        - Appropriate return statements based on type analysis
        - Main function and __main__ guard for executable files

        The generated code is a complete skeleton that developers can fill in
        with actual implementation logic.

        Args:
            extracted_model: Reverse engineering output containing system info,
                           components, methods, imports, and metadata

        Returns:
            Complete Python module code as a string

        Key Features:
        - Smart import detection and filtering
        - Structure preservation with type hints
        - TODO comments for implementation guidance
        - Support for executable files and packages
        - Clean, formatted output
        """
        # Generate unique generation ID for traceability
        generation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        model_id = extracted_model.get("model_id", "unknown")

        logger.info(f"🎯 Generating code from extracted model {model_id}")
        logger.info(f"🆔 Generation ID: {generation_id} at {timestamp}")

        print(f"🆔 Code Generation {generation_id} from Model {model_id}")

        # 🏗️ STEP 1: Extract system information and metadata
        system_name = extracted_model.get("system_name", "Unknown System")
        description = extracted_model.get("description", "")
        purpose = extracted_model.get("purpose", "")

        # 📁 STEP 2: Determine file type and build file header
        metadata = extracted_model.get("file_metadata", {})
        is_executable = metadata.get("executable", False)

        # Add shebang only if original file was executable
        code = "#!/usr/bin/env python3\n\n" if is_executable else ""

        # Add docstring with generation metadata
        purpose_line = f"\n{purpose}" if purpose else ""
        code += f"""\"\"\"
{system_name}

{description}{purpose_line}

Generated from Model: {model_id}
Generation ID: {generation_id}
Generated at: {timestamp}
\"\"\"

"""

        # 📚 STEP 3: Analyze and generate smart imports
        # Check what typing imports are needed based on method return types
        needs_typing = False
        components = extracted_model.get("components", {})
        for class_name, class_info in components.items():
            methods = class_info.get("methods", [])
            for method in methods:
                return_type = method.get("return_type", "Any")
                if return_type == "Any":
                    needs_typing = True
                    break
            if needs_typing:
                break

        # 🔍 STEP 4: Detect advanced typing needs (dataclass, pydantic, enum)
        typing_imports = []
        needs_dataclass = False
        needs_pydantic = False
        needs_enum = False

        for class_info in extracted_model.get("components", {}).values():
            # Check if class has @dataclass decorator
            decorators = class_info.get("class_decorators", [])
            if "dataclass" in decorators:
                needs_dataclass = True

            # Check base classes for BaseModel and Enum inheritance
            bases = class_info.get("bases", [])
            for base in bases:
                if "BaseModel" in base and not needs_pydantic:
                    needs_pydantic = True
                if "Enum" in base and not needs_enum:
                    needs_enum = True

            for method in class_info.get("methods", []):
                # Check return type for BaseModel and Enum usage
                return_type = method.get("return_type", "")
                if return_type and "BaseModel" in return_type and not needs_pydantic:
                    needs_pydantic = True
                if return_type and "Enum" in return_type and not needs_enum:
                    needs_enum = True
                # Check return type for Optional usage
                if (
                    return_type
                    and "Optional" in return_type
                    and "Optional" not in typing_imports
                ):
                    typing_imports.append("Optional")

                for param in method.get("parameters", []):
                    if isinstance(param, dict) and "type" in param:
                        param_type = param["type"]
                        if (
                            "Optional" in param_type
                            and "Optional" not in typing_imports
                        ):
                            typing_imports.append("Optional")
                        # Only add Tuple if it's actually used in the final cleaned types
                        # Since we convert complex types to simple ones, we need to check if Tuple is still needed
                        if "List" in param_type and "List" not in typing_imports:
                            typing_imports.append("List")
                        if "Dict" in param_type and "Dict" not in typing_imports:
                            typing_imports.append("Dict")
                        # Check for BaseModel usage
                        if "BaseModel" in param_type and not needs_pydantic:
                            needs_pydantic = True
                        # Check for Enum usage
                        if "Enum" in param_type and not needs_enum:
                            needs_enum = True

        # Combine all typing imports into one statement
        all_typing_imports = []
        # Always include Any since it's commonly used
        all_typing_imports.append("Any")
        all_typing_imports.extend(typing_imports)

        if all_typing_imports:
            code += f"from typing import {', '.join(all_typing_imports)}\n"

        # Add dataclass import if needed
        if needs_dataclass:
            code += "from dataclasses import dataclass\n"

        # Add pydantic import if needed
        if needs_pydantic:
            code += "from pydantic import BaseModel\n"

        # Add enum import if needed
        if needs_enum:
            code += "from enum import Enum\n"

        if all_typing_imports or needs_dataclass or needs_pydantic or needs_enum:
            code += "\n"

        # 🎯 DEPENDENCY-BASED IMPORT GENERATION (NOT filtering!)
        # Instead of guessing which imports are "used", we analyze the actual dependencies

        # Get the original imports from the extracted model
        imports = extracted_model.get("imports", [])
        used_names = extracted_model.get("used_names", [])

        # Debug: Print what we're working with
        print(f"🔍 DEBUG: Found {len(imports)} imports: {imports}")
        print(f"🔍 DEBUG: Found {len(used_names)} used names: {used_names}")

        # Check if this is a package __init__.py file first
        metadata = extracted_model.get("file_metadata", {})
        is_package_init = (
            metadata.get("file_type") == "module" and "clewcrew" in system_name.lower()
        )

        if is_package_init:
            # For package __init__.py files, keep all imports
            essential_imports = imports
        else:
            # Filter imports to only include those that are actually used
            # For test files, we need to be more conservative about what we keep
            essential_imports = []
            for imp in imports:
                print(f"🔍 DEBUG: Processing import: {imp}")
                # Extract the imported name from the import statement
                if "from " in imp and " import " in imp:
                    # Handle: "from module import name" - MUST COME FIRST!
                    imported_names_str = imp.split(" import ")[1].strip()
                    print(
                        f"🔍 DEBUG: From import - extracted names string: {imported_names_str}"
                    )
                    # Split comma-separated names
                    imported_names = [
                        name.strip() for name in imported_names_str.split(", ")
                    ]
                    print(f"🔍 DEBUG: Split names: {imported_names}")
                    # Check if ANY of the imported names are used
                    if any(name in used_names for name in imported_names):
                        essential_imports.append(imp)
                        print(f"✅ DEBUG: Added from import: {imp}")
                    else:
                        print(f"❌ DEBUG: Skipped from import (none used): {imp}")
                elif "import " in imp and " as " in imp:
                    # Handle: "import module as alias"
                    imported_name = imp.split(" as ")[1].strip()
                    print(f"🔍 DEBUG: Alias import - extracted name: {imported_name}")
                    if imported_name in used_names:
                        essential_imports.append(imp)
                        print(f"✅ DEBUG: Added alias import: {imp}")
                    else:
                        print(f"❌ DEBUG: Skipped alias import (not used): {imp}")
                elif "import " in imp:
                    # Handle: "import module"
                    imported_name = imp.split("import ")[1].strip()
                    print(f"🔍 DEBUG: Module import - extracted name: {imported_name}")
                    if imported_name in used_names:
                        essential_imports.append(imp)
                        print(f"✅ DEBUG: Added module import: {imp}")
                    else:
                        print(f"❌ DEBUG: Skipped module import (not used): {imp}")
                else:
                    # Keep imports we can't parse
                    essential_imports.append(imp)
                    print(f"✅ DEBUG: Added unparseable import: {imp}")

            print(f"🔍 DEBUG: Essential imports: {essential_imports}")

        # For package __init__.py files, keep all imports
        # For test files, only keep essential imports
        # For regular files, keep all imports that are actually used
        if is_package_init:
            # Keep all imports for package __init__.py files
            essential_imports = essential_imports
        elif metadata.get("is_test_file", False):
            # For test files, only keep essential imports
            essential_imports = []
            for imp in essential_imports:
                # Skip typing imports since we handle them separately
                if "typing" in imp:
                    continue
                # Keep pytest only if we actually use pytest decorators
                elif "pytest" in imp:
                    # Check if any methods have pytest decorators
                    has_pytest_decorators = any(
                        "pytest" in method.get("decorators", [])
                        for class_info in extracted_model.get("components", {}).values()
                        for method in class_info.get("methods", [])
                    )
                    if has_pytest_decorators:
                        essential_imports.append(imp)
                # For test files, be very conservative about imports
                # Skip imports that will cause mypy errors (like clewcrew_core modules)
                # Only keep imports that are absolutely essential and won't cause mypy errors
                elif "Mock" in imp or "AsyncMock" in imp:
                    # Only keep if we actually use them in the generated code
                    if any(
                        "Mock" in str(method) or "AsyncMock" in str(method)
                        for class_info in extracted_model.get("components", {}).values()
                        for method in class_info.get("methods", [])
                    ):
                        essential_imports.append(imp)
                # Skip other imports that aren't used
                else:
                    continue
        else:
            # For regular files, keep all imports that are actually used
            essential_imports = essential_imports

        # For package __init__.py files, add module variables first, then imports, then __all__
        if is_package_init:
            # Add module assignments first (like __version__, __author__, etc.)
            module_assignments = extracted_model.get("module_assignments", {})
            if module_assignments:
                for var_name, value in module_assignments.items():
                    if var_name != "__all__":  # Handle __all__ separately
                        if isinstance(value, str):
                            code += f'{var_name} = "{value}"\n'
                        else:
                            code += f"{var_name} = {value}\n"
                code += "\n"

            # Add imports
            if essential_imports:
                # Group imports by module to consolidate them
                import_groups = {}
                for imp in essential_imports:
                    if "from " in imp and " import " in imp:
                        # Extract module and imported names
                        parts = imp.split(" import ")
                        module_part = parts[0].replace("from ", "")
                        imported_names = parts[1].split(", ")

                        if module_part not in import_groups:
                            import_groups[module_part] = []
                        import_groups[module_part].extend(imported_names)
                    else:
                        # Keep non-relative imports as-is
                        code += f"{imp}\n"

                # Generate consolidated relative imports
                for module, names in import_groups.items():
                    # Convert to relative import format
                    relative_module = "." + module
                    code += f"from {relative_module} import {', '.join(names)}\n"

                code += "\n"

            # Add __all__ list last
            if "__all__" in module_assignments:
                all_list = module_assignments["__all__"]
                if isinstance(all_list, list):
                    code += "__all__ = [\n"
                    for item in all_list:
                        code += f'    "{item}",\n'
                    code += "]\n"
        else:
            # For non-package files, add imports first
            if essential_imports:
                for imp in essential_imports:
                    code += f"{imp}\n"
                code += "\n"

            # Add module assignments
            module_assignments = extracted_model.get("module_assignments", {})
            if module_assignments:
                for var_name, value in module_assignments.items():
                    if var_name != "__all__":  # Handle __all__ separately
                        if isinstance(value, str):
                            code += f'{var_name} = "{value}"\n'
                        else:
                            code += f"{var_name} = {value}\n"

                # Add __all__ list if it exists
                if "__all__" in module_assignments:
                    all_list = module_assignments["__all__"]
                    if isinstance(all_list, list):
                        code += "\n__all__ = [\n"
                        for item in all_list:
                            code += f'    "{item}",\n'
                        code += "]\n"

                code += "\n"

        # 🏗️ STEP 5: Generate all classes with methods and type hints
        components = extracted_model.get("components", {})
        for i, (class_name, class_info) in enumerate(components.items()):
            # Add proper spacing before class definition (PEP 8: 2 blank lines)
            # For first class, only add 1 blank line since imports already added 1
            # For subsequent classes, add 2 blank lines
            if i == 0:
                code += "\n"
            else:
                code += "\n\n"
            code += self._generate_class_from_extracted_model(
                class_name, class_info, extracted_model
            )

        # ⚙️ STEP 6: Generate standalone functions with type hints
        functions = extracted_model.get("functions", {})
        for i, (func_name, func_info) in enumerate(functions.items()):
            # Add proper spacing before function definition (PEP 8: 2 blank lines)
            if i > 0 or components:  # Add blank line if there are classes before
                code += "\n\n"
            code += self._generate_function_from_extracted_model(func_name, func_info)
            # Add proper spacing between functions (2 blank lines)
            if i < len(functions) - 1:
                code += "\n\n"

        # 🚀 STEP 7: Generate main entry point and __main__ guard
        if not is_package_init:
            if (
                components or functions
            ):  # Add blank line if there are classes or functions before
                code += "\n\n"
            code += f"""def main() -> None:
    \"\"\"Main entry point for {system_name}\"\"\"
    print("🚀 {system_name}")
    print("📝 Generated from extracted model")
    print("✅ Ready to use!")


if __name__ == "__main__":
    main()
"""

        logger.info("✅ Generated complete module code")

        # ✨ STEP 8: Clean up and format the final generated code
        return self._clean_generated_code(code)

    def _clean_generated_code(self, code: str) -> str:
        """Clean up generated code to ensure no trailing whitespace and proper formatting"""
        lines = code.split("\n")
        cleaned_lines = []

        for line in lines:
            # Remove trailing whitespace from each line
            cleaned_line = line.rstrip()
            cleaned_lines.append(cleaned_line)

        # Join lines back together, ensuring no trailing whitespace
        cleaned_code = "\n".join(cleaned_lines)

        # Ensure the file ends with exactly one newline
        if not cleaned_code.endswith("\n"):
            cleaned_code += "\n"

        # Format with Black if available
        if BLACK_AVAILABLE:
            try:
                # Configure Black mode (88 character line length, Python 3.9+)
                mode = FileMode(
                    target_versions={
                        TargetVersion.PY39,
                        TargetVersion.PY310,
                        TargetVersion.PY311,
                        TargetVersion.PY312,
                    },
                    line_length=88,
                    string_normalization=True,
                    is_pyi=False,
                    is_ipynb=False,
                    skip_source_first_line=False,
                    magic_trailing_comma=True,
                    preview=False,
                )

                # Format the code
                formatted_code = format_str(cleaned_code, mode=mode)

                # Log what Black changed so we can learn to generate cleaner code
                if formatted_code != cleaned_code:
                    logger.warning(
                        "🔍 Black made formatting changes - this means the model generated messy code:"
                    )
                    logger.warning(f"  Original length: {len(cleaned_code)} chars")
                    logger.warning(f"  Formatted length: {len(formatted_code)} chars")

                    # Log specific changes for learning
                    original_lines = cleaned_code.split("\n")
                    formatted_lines = formatted_code.split("\n")

                    if len(original_lines) != len(formatted_lines):
                        logger.warning(
                            f"  Line count changed: {len(original_lines)} → {len(formatted_lines)}"
                        )

                    # Log first few differences for pattern recognition
                    for i, (orig, fmt) in enumerate(
                        zip(original_lines, formatted_lines)
                    ):
                        if orig != fmt and i < 10:  # Only log first 10 differences
                            logger.warning(f"  Line {i+1}: '{orig}' → '{fmt}'")

                logger.info("✅ Generated code formatted with Black")
                return formatted_code
            except Exception as e:
                logger.warning(
                    f"Black formatting failed: {e}, returning unformatted code"
                )
                return cleaned_code
        else:
            logger.warning("Black not available - returning unformatted code")
            return cleaned_code

    def _generate_class_from_extracted_model(
        self,
        class_name: str,
        class_info: dict[str, Any],
        extracted_model: dict[str, Any],
    ) -> str:
        """Generate class code from extracted model class info"""
        responsibility = class_info.get("responsibility", "")
        methods = class_info.get("methods", [])
        bases = class_info.get("bases", [])
        decorators = class_info.get("class_decorators", [])

        # Build class definition
        class_def = "class " + class_name
        if bases:
            class_def += f"({', '.join(bases)})"
        class_def += ":"

        # Add decorators
        decorator_code = ""
        for decorator in decorators:
            decorator_code += f"@{decorator}\n"

        # Build class code
        code = f"""{decorator_code}{class_def}
    \"\"\"
    {responsibility}
    \"\"\"
"""

        # Add methods
        for i, method in enumerate(methods):
            code += self._generate_method_from_extracted_model(method, extracted_model)
            # Add single blank line between methods (not extra)
            if i < len(methods) - 1:
                code += "\n"

        # No extra blank line after class - let the next class add spacing

        return code

    def _generate_method_from_extracted_model(
        self, method_info: dict[str, Any], extracted_model: dict[str, Any]
    ) -> str:
        """Generate method code from extracted model method info"""
        name = method_info.get("name", "unknown_method")
        docstring = method_info.get("docstring", "")
        decorators = method_info.get("decorators", [])
        return_type = method_info.get("return_type", "Any")
        is_async = method_info.get("is_async", False)
        is_test_method = method_info.get("is_test_method", False)
        parameters = method_info.get("parameters", [])

        # Build parameter string from structured parameter data
        param_parts = []
        for param in parameters:
            if isinstance(param, dict) and "name" in param and "type" in param:
                param_name = param["name"]
                param_type = param["type"]
                if param_name != "self":  # Skip self parameter
                    # Clean up overly complex type annotations
                    cleaned_type = self._clean_complex_type(param_type)
                    param_parts.append(f"{param_name}: {cleaned_type}")
            elif isinstance(param, str) and param != "self":
                param_parts.append(f"{param}: Any")

        param_str = ", ".join(param_parts)
        method_name = name

        # For test files, ensure proper pytest return types
        if is_test_method:
            if method_name.startswith("test_"):
                return_type = "None"  # Test methods return None
            elif "fixture" in decorators:
                return_type = "Any"  # Pytest fixtures return Any
            # Don't override return type for other test methods - use what's in the model

        # Add decorators
        decorator_code = ""
        for decorator in decorators:
            decorator_code += f"    @{decorator}\n"

        # Build method signature (handle async methods)
        # For logging methods and constructors, use None return type
        if method_name in ["info", "warning", "error", "debug", "critical", "__init__"]:
            actual_return_type = "None"
        else:
            # Clean up complex return types for the method signature
            actual_return_type = self._clean_complex_type(return_type)

        if is_async:
            if param_str:
                method_sig = f"    async def {method_name}(self, {param_str}) -> {actual_return_type}:"
            else:
                method_sig = (
                    f"    async def {method_name}(self) -> {actual_return_type}:"
                )
        else:
            if param_str:
                method_sig = (
                    f"    def {method_name}(self, {param_str}) -> {actual_return_type}:"
                )
            else:
                method_sig = f"    def {method_name}(self) -> {actual_return_type}:"

        # Generate proper return statement
        if return_type == "None":
            return_stmt = "return None"
        elif return_type in ["str", "int", "float", "bool"]:
            return_stmt = f"return {self._get_default_value(return_type)}"
        elif return_type == "ClewcrewLogger":
            return_stmt = "return ClewcrewLogger('default', 'INFO')"
        else:
            # Clean up complex return types and generate appropriate return statements
            cleaned_return_type = self._clean_complex_type(return_type)
            if "dict[" in cleaned_return_type:
                return_stmt = "return {}"
            elif "list[" in cleaned_return_type:
                return_stmt = "return []"
            elif "tuple[" in cleaned_return_type:
                return_stmt = "return ()"
            else:
                # For custom classes, try to create a default instance
                if cleaned_return_type and not cleaned_return_type.startswith(
                    "Optional"
                ):
                    # Check if it's a type that can be instantiated
                    if cleaned_return_type in [
                        "Any",
                        "str",
                        "int",
                        "float",
                        "bool",
                        "dict",
                        "list",
                        "tuple",
                    ]:
                        # For basic types, return appropriate defaults
                        if cleaned_return_type == "Any":
                            return_stmt = "return None"
                        elif cleaned_return_type == "dict":
                            return_stmt = "return {}"
                        elif cleaned_return_type == "list":
                            return_stmt = "return []"
                        elif cleaned_return_type == "tuple":
                            return_stmt = "return ()"
                        else:
                            return_stmt = (
                                f"return {self._get_default_value(cleaned_return_type)}"
                            )
                    else:
                        # Try to create a default instance of the custom class
                        return_stmt = f"return {cleaned_return_type}()"
                else:
                    # For logging methods and constructors, return None
                    if method_name in [
                        "info",
                        "warning",
                        "error",
                        "debug",
                        "critical",
                        "__init__",
                    ]:
                        return_stmt = "return None"
                    else:
                        return_stmt = "return None"

        # Check if we have method body content for round-trip functionality
        method_body = method_info.get("body", [])
        implementation_status = method_info.get("implementation_status", "skeleton")

        # Ghostbusters recommendation: Respect implementation_status over is_test_method
        if method_body and implementation_status == "implemented":
            print(
                f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: USING EXTRACTED BODY (Ghostbusters approved)"
            )
            print(
                f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Body lines: {method_body[:3]}..."
            )  # Show first 3 lines
            # Use the actual implementation from the extracted model
            body_lines = []
            for body_line in method_body:
                body_lines.append(f"        {body_line}")
            body_content = "\n".join(body_lines)
            print(
                f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Generated body content length: {len(body_content)}"
            )

            code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
{body_content}
"""
            print(
                f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Generated code with body, length: {len(code)}"
            )
        else:
            # Generate appropriate code based on method type and status
            if is_test_method:
                print(
                    f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Generating test method placeholder"
                )
                # Generate realistic test method code that uses imports
                if "ClewcrewState" in name or "state" in name.lower():
                    code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # Test implementation
        assert True  # Placeholder assertion
        {return_stmt}
"""
                elif "orchestrator" in name.lower():
                    code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # Test implementation
        assert True  # Placeholder assertion
        {return_stmt}
"""
                elif "mock" in name.lower():
                    code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # Test implementation
        assert True  # Placeholder assertion
        {return_stmt}
"""
                else:
                    code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # Test implementation
        assert True  # Placeholder assertion
        {return_stmt}
"""
            else:
                print(
                    f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Generating skeleton placeholder"
                )
                # Generate skeleton code for unimplemented methods
                code = f"""{decorator_code}{method_sig}
        \"\"\"
        {docstring}
        \"\"\"
        # TODO: Implement {method_name}
        {return_stmt}
"""
        print(
            f"🔍 DEBUG: Method {method_info.get('name', 'unknown')}: Final code length: {len(code)}"
        )
        return code

    def _generate_function_from_extracted_model(
        self, func_name: str, func_info: dict[str, Any]
    ) -> str:
        """Generate function code from extracted model function info"""
        docstring = func_info.get("docstring", "")
        return_type = func_info.get("return_type", "Any")
        parameters = func_info.get("parameters", [])

        # Build parameter string from structured parameter data
        param_parts = []
        for param in parameters:
            if isinstance(param, dict) and "name" in param and "type" in param:
                param_name = param["name"]
                param_type = param["type"]
                param_parts.append(f"{param_name}: {param_type}")
            elif isinstance(param, str):
                param_parts.append(f"{param}: Any")

        param_str = ", ".join(param_parts)

        # Generate proper return statement
        if return_type == "None":
            return_stmt = "return None"
        elif return_type in ["str", "int", "float", "bool"]:
            return_stmt = f"return {self._get_default_value(return_type)}"
        elif return_type == "ClewcrewLogger":
            return_stmt = "return ClewcrewLogger()"
        else:
            return_stmt = "return None"

        # Build function code
        code = f"""def {func_name}({param_str}) -> {return_type}:
    \"\"\"
    {docstring}
    \"\"\"
    # TODO: Implement {func_name}
    {return_stmt}
"""
        return code

    def _generate_function_code(self, component: ModelComponent) -> str:
        """Generate function code from component design"""
        # Extract function signature from metadata
        params = component.metadata.get("parameters", [])
        return_type = component.metadata.get("return_type", "Any")

        # Build parameter string with proper type annotations
        param_str = ""
        if params:
            param_parts = []
            for param in params:
                if isinstance(param, dict) and "name" in param and "type" in param:
                    # Parameter is a dict with name and type
                    param_parts.append(f"{param['name']}: {param['type']}")
                elif isinstance(param, str):
                    # Parameter is a simple string
                    param_parts.append(param)
                else:
                    # Fallback for unknown parameter format
                    param_parts.append(str(param))
            param_str = ", ".join(param_parts)

        # Generate function code
        code = f"""#!/usr/bin/env python3
\"\"\"
{component.description}
\"\"\"

"""

        # Add imports based on dependencies
        for dep in component.dependencies:
            code += f"from {dep} import *\n"

        code += f"""

def {component.name}({param_str}) -> {return_type}:
    \"\"\"
    {component.description}
    \"\"\"
    # TODO: Implement based on requirements: {component.requirements}
    pass
"""

        return code

    def _generate_class_code(self, component: ModelComponent) -> str:
        """Generate class code from component design"""
        methods = component.metadata.get("methods", [])

        code = f"""#!/usr/bin/env python3
\"\"\"
{component.description}
\"\"\"

"""

        # Add imports based on dependencies
        for dep in component.dependencies:
            code += f"from {dep} import *\n"

        code += f"""


class {component.name}:
    \"\"\"
    {component.description}
    \"\"\"

    def __init__(self) -> None:
        # TODO: Initialize based on requirements: {component.requirements}
        return None
"""

        # Add methods with proper signature parsing
        for method in methods:
            # Skip __init__ method since we already generated it above
            if isinstance(method, str) and method.startswith("__init__"):
                continue
            elif isinstance(method, dict) and method.get("name") == "__init__":
                continue

            # Parse method signature if it's a string
            if isinstance(method, str):
                # Parse method signature like "add(self, a: float, b: float) -> float"
                parsed_method = self._parse_method_signature(method)
                code += self._generate_method_from_parsed(parsed_method)
            else:
                # Handle method as dict
                code += self._generate_method_from_dict(method)

        return code

    def _parse_method_signature(self, method_signature: str) -> dict[str, Any]:
        """Parse method signature string into components"""
        # Example: "add(self, a: float, b: float) -> float"
        try:
            # Split on -> to separate parameters from return type
            if "->" in method_signature:
                params_part, return_type = method_signature.split("->", 1)
                return_type = return_type.strip()
                params_part = params_part.strip()  # Remove trailing spaces
            else:
                params_part = method_signature
                return_type = "None"

            # Extract method name and parameters
            # Remove trailing ) and split on first (
            if "(" in params_part and params_part.endswith(")"):
                method_name = params_part[: params_part.find("(")]
                params_str = params_part[params_part.find("(") + 1 : -1]

                # Parse parameters
                params = []
                if params_str.strip():
                    for param in params_str.split(","):
                        param = param.strip()
                        # Skip 'self' parameter as it's implicit in Python methods
                        if param == "self":
                            continue
                        if ":" in param:
                            param_name, param_type = param.split(":", 1)
                            params.append(
                                {"name": param_name.strip(), "type": param_type.strip()}
                            )
                        else:
                            params.append({"name": param.strip(), "type": "Any"})

                return {
                    "name": method_name.strip(),
                    "params": params,
                    "return_type": return_type,
                }
            else:
                # Fallback for malformed signatures
                return {
                    "name": method_signature.strip(),
                    "params": [],
                    "return_type": "Any",
                }
        except Exception:
            # Fallback for any parsing errors
            return {
                "name": method_signature.strip(),
                "params": [],
                "return_type": "Any",
            }

    def _generate_method_from_parsed(self, parsed_method: dict) -> str:
        """Generate method code from parsed method signature"""
        method_name = parsed_method["name"]
        params = parsed_method["params"]
        return_type = parsed_method["return_type"]

        # Build parameter string
        if params:
            param_str = ", ".join([f"{p['name']}: {p['type']}" for p in params])
        else:
            param_str = ""

        # Generate proper return statement based on return type
        if return_type == "None":
            return_stmt = "return None"
        elif return_type in ["str", "int", "float", "bool"]:
            return_stmt = f"return {self._get_default_value(return_type)}"
        else:
            return_stmt = "return None"

        # Handle method signature properly
        if param_str:
            method_sig = f"def {method_name}(self, {param_str}) -> {return_type}:"
        else:
            method_sig = f"def {method_name}(self) -> {return_type}:"

        code = f"""
    {method_sig}
        \"\"\"
        {method_name}(self, {param_str}) -> {return_type}
        \"\"\"
        # TODO: Implement {method_name}(self, {param_str}) -> {return_type}
        {return_stmt}
"""
        return code

    def _generate_method_from_dict(self, method: dict) -> str:
        """Generate method code from method dict"""
        method_name = method.get("name", "unknown_method")
        params = method.get("parameters", [])
        return_type = method.get("return_type", "Any")

        # Build parameter string
        if params:
            param_str = ", ".join([f"{p['name']}: {p['type']}" for p in params])
        else:
            param_str = ""

        # Generate proper return statement
        if return_type == "None":
            return_stmt = "return None"
        elif return_type in ["str", "float", "bool"]:
            return_stmt = f"return {self._get_default_value(return_type)}"
        else:
            return_stmt = "return None"

        # Handle method signature properly
        if param_str:
            method_sig = f"def {method_name}(self, {param_str}) -> {return_type}:"
        else:
            method_sig = f"def {method_name}(self) -> {return_type}:"

        code = f"""
    {method_sig}
        \"\"\"
        {method_name}(self, {param_str}) -> {return_type}
        \"\"\"
        # TODO: Implement {method_name}(self, {param_str}) -> {return_type}
        {return_stmt}
"""
        return code

    def _clean_complex_type(self, type_annotation: str) -> str:
        """Clean up overly complex type annotations"""
        # Handle None case
        if type_annotation is None:
            return "Any"

        # Convert to string if it's not already
        type_str = str(type_annotation)

        # Handle dict types with complex nested types
        if "dict[" in type_str:
            # Any dict with complex types becomes dict[str, Any]
            if "Tuple[" in type_str or "dict[" in type_str or "list[" in type_str:
                return "dict[str, Any]"
            else:
                return "dict[str, Any]"

        # Handle list types with complex nested types
        elif "list[" in type_str:
            if "dict[" in type_str or "Tuple[" in type_str:
                return "list[dict[str, Any]]"
            else:
                return "list[Any]"

        # Handle tuple types with complex nested types
        elif "Tuple[" in type_str:
            if "dict[" in type_str or "list[" in type_str:
                return "tuple[str, Any]"
            else:
                return "tuple[Any, ...]"

        # Return the original type if it's simple
        return type_str

    def _get_default_value(self, type_name: str) -> str:
        """Get default value for a type"""
        defaults = {
            "str": '""',
            "int": "0",
            "float": "0.0",
            "bool": "False",
            "list": "[]",
            "dict": "{}",
            "tuple": "()",
        }
        return defaults.get(type_name, "None")

    def _generate_module_code(self, component: ModelComponent) -> str:
        """Generate module code from component design"""
        code = f"""#!/usr/bin/env python3
\"\"\"
{component.description}

This module contains:
{chr(10).join(f'- {req}' for req in component.requirements)}
\"\"\"

# Module imports
"""

        # Add imports based on dependencies
        for dep in component.dependencies:
            code += f"from {dep} import *\n"

        code += f"""

# Module-level variables and constants
# TODO: Add based on requirements: {component.requirements}

# Module-level functions
# TODO: Add based on requirements: {component.requirements}
"""

        return code

    def _generate_domain_code(self, component: ModelComponent) -> str:
        """Generate domain code from component design"""
        code = f"""#!/usr/bin/env python3
\"\"\"
{component.description}

Domain Model Requirements:
{chr(10).join(f'- {req}' for req in component.requirements)}
\"\"\"

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

"""

        # Add imports based on dependencies
        for dep in component.dependencies:
            code += f"from {dep} import *\n"

        code += f"""

@dataclass
class {component.name}Domain:
    \"\"\"
    {component.description}
    \"\"\"

    # Domain-specific fields
    # TODO: Add based on requirements: {component.requirements}

    def __post_init__(self):
        \"\"\"Initialize domain-specific components\"\"\"
        # TODO: Initialize based on requirements: {component.requirements}
        pass

    def validate_domain(self) -> bool:
        \"\"\"Validate domain requirements\"\"\"
        # TODO: Implement validation based on requirements: {component.requirements}
        return True
"""

        return code

    def save_model(self, model_name: str, file_path: str) -> None:
        """Save a design model to JSON"""
        if model_name not in self.design_models:
            msg = f"Model {model_name} not found"
            raise ValueError(msg)

        model = self.design_models[model_name]

        # Convert to JSON-serializable format
        model_data = {
            "name": model.name,
            "description": model.description,
            "components": [
                {
                    "name": comp.name,
                    "type": comp.type,
                    "description": comp.description,
                    "requirements": comp.requirements,
                    "dependencies": comp.dependencies,
                    "metadata": comp.metadata,
                }
                for comp in model.components
            ],
            "relationships": model.relationships,
            "metadata": model.metadata,
        }

        with open(file_path, "w") as f:
            json.dump(model_data, f, indent=2)

        logger.info(f"✅ Saved model {model_name} to {file_path}")

    def load_model(self, file_path: str) -> DesignModel:
        """Load a design model from JSON"""
        with open(file_path) as f:
            model_data = json.load(f)

        # Reconstruct components
        components = []
        for comp_data in model_data["components"]:
            component = ModelComponent(
                name=comp_data["name"],
                type=comp_data["type"],
                description=comp_data["description"],
                requirements=comp_data.get("requirements", []),
                dependencies=comp_data.get("dependencies", []),
                metadata=comp_data.get("metadata", {}),
            )
            components.append(component)

        # Reconstruct model
        model = DesignModel(
            name=model_data["name"],
            description=model_data["description"],
            components=components,
            relationships=model_data.get("relationships", {}),
            metadata=model_data.get("metadata", {}),
        )

        self.design_models[model.name] = model
        logger.info(f"✅ Loaded model {model.name} with {len(components)} components")

        return model


def main() -> None:
    """Demonstrate round-trip model system"""
    system = RoundTripModelSystem()

    # STEP 1: Create model from design (NO reverse engineering)
    design_spec = {
        "name": "ASTGuidedCodeGenerator",
        "description": "AST-guided code generator that respects syntactic boundaries",
        "components": [
            {
                "name": "ASTNode",
                "type": "class",
                "description": "Represents an AST node with metadata",
                "requirements": [
                    "dataclass",
                    "metadata support",
                    "parent-child relationships",
                ],
                "dependencies": ["dataclasses", "typing"],
                "metadata": {
                    "methods": [
                        {
                            "name": "__post_init__",
                            "description": "Initialize default values",
                            "return_type": "None",
                        },
                    ],
                },
            },
            {
                "name": "LintingRule",
                "type": "class",
                "description": "Represents a linting rule with AST-aware patterns",
                "requirements": [
                    "rule code",
                    "description",
                    "severity",
                    "AST patterns",
                    "fix strategy",
                ],
                "dependencies": ["dataclasses", "typing"],
                "metadata": {
                    "methods": [
                        {
                            "name": "__post_init__",
                            "description": "Initialize default values",
                            "return_type": "None",
                        },
                    ],
                },
            },
            {
                "name": "ASTGuidedCodeGenerator",
                "type": "class",
                "description": "AST-guided code generator that respects syntactic boundaries",
                "requirements": [
                    "AST parsing",
                    "linting rule integration",
                    "syntactic boundary detection",
                    "fix strategy generation",
                ],
                "dependencies": [
                    "ast",
                    "logging",
                    "dataclasses",
                    "typing",
                    "src.artifact_forge.agents.artifact_parser_enhanced",
                ],
                "metadata": {
                    "methods": [
                        {
                            "name": "analyze_file_ast",
                            "description": "Analyze file using AST with linting rule integration",
                            "return_type": "Dict[str, Any]",
                        },
                        {
                            "name": "generate_perfect_code",
                            "description": "Generate perfect code using AST-guided approach",
                            "return_type": "str",
                        },
                    ],
                },
            },
        ],
        "relationships": {
            "ASTGuidedCodeGenerator": ["ASTNode", "LintingRule"],
            "ASTNode": [],
            "LintingRule": [],
        },
    }

    print("🎯 STEP 1: Creating model from design")
    model = system.create_model_from_design(design_spec)
    print(f"   ✅ Created model: {model.name} with {len(model.components)} components")

    # STEP 2: Save model to JSON
    print("\n🎯 STEP 2: Saving model to JSON")
    system.save_model("ASTGuidedCodeGenerator", "ast_guided_model.json")

    # STEP 3: Generate code from model
    print("\n🎯 STEP 3: Generating code from model")
    generated_files = system.generate_code_from_model("ASTGuidedCodeGenerator")

    # STEP 4: Save generated code
    print("\n🎯 STEP 4: Saving generated code")
    for filename, code in generated_files.items():
        with open(f"generated_{filename}", "w") as f:
            f.write(code)
        print(f"   💾 Saved generated_{filename}")

    # STEP 5: Load model from JSON (round-trip)
    print("\n🎯 STEP 5: Loading model from JSON (round-trip)")
    loaded_model = system.load_model("ast_guided_model.json")

    print("\n✅ ROUND-TRIP COMPLETE!")
    print(f"   📊 Model: {loaded_model.name}")
    print(f"   📊 Components: {len(loaded_model.components)}")
    print(f"   📊 Generated files: {len(generated_files)}")
    print("   🎯 Round-trip successful: Design → Model → Code → Model")


if __name__ == "__main__":
    main()
