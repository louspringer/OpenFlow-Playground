#!/usr/bin/env python3
"""
Python Unit Test Generator - Model-Driven Test Generation System

This system generates unit tests directly from implementation models to ensure
tests stay in sync with actual code structure and requirements. Uses abstract
factory pattern to handle different artifact types (classes, functions, modules).
"""

import ast
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Protocol


class ArtifactModel(Protocol):
    """Protocol for artifact models that can be tested"""

    @property
    def name(self) -> str:
        """Name of the artifact"""
        ...

    @property
    def artifact_type(self) -> str:
        """Type of artifact (class, function, module)"""
        ...

    @property
    def file_path(self) -> Path:
        """Path to the source file"""
        ...


class ClassArtifactModel:
    """Model of a Python class for test generation"""

    def __init__(self, name: str, file_path: Path):
        self._name = name
        self._file_path = file_path
        self.attributes: list[str] = []
        self.methods: list[dict[str, Any]] = []
        self.dependencies: list[str] = []
        self.inheritance: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def artifact_type(self) -> str:
        return "class"

    @property
    def file_path(self) -> Path:
        return self._file_path


class FunctionArtifactModel:
    """Model of a Python function for test generation"""

    def __init__(self, name: str, file_path: Path):
        self._name = name
        self._file_path = file_path
        self.parameters: list[str] = []
        self.return_type: str = ""
        self.decorators: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def artifact_type(self) -> str:
        return "function"

    @property
    def file_path(self) -> Path:
        return self._file_path


class ModuleArtifactModel:
    """Model of a Python module for test generation"""

    def __init__(self, name: str, file_path: Path):
        self._name = name
        self._file_path = file_path
        self.classes: list[str] = []
        self.functions: list[str] = []
        self.imports: list[str] = []
        self.constants: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def artifact_type(self) -> str:
        return "module"

    @property
    def file_path(self) -> Path:
        return self._file_path


class ArtifactModelExtractor(ABC):
    """Abstract base class for extracting artifact models from source code"""

    def __init__(self, source_file: Path):
        self.source_file = source_file
        self.ast_tree = None
        self._parse_source()

    def _parse_source(self):
        """Parse the source file into AST"""
        if self.source_file.exists():
            source_content = self.source_file.read_text()
            self.ast_tree = ast.parse(source_content)
        else:
            msg = f"Source file not found: {self.source_file}"
            raise FileNotFoundError(msg)

    @abstractmethod
    def extract_models(self) -> list[ArtifactModel]:
        """Extract all models from the source file"""


class ClassModelExtractor(ArtifactModelExtractor):
    """Extracts class models from Python source code"""

    def extract_models(self) -> list[ArtifactModel]:
        """Extract all class models from the source file"""
        if not self.ast_tree:
            return []

        models = []

        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                class_model = ClassArtifactModel(node.name, self.source_file)

                # Extract attributes from __init__
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                        class_model.attributes = self._extract_init_attributes(item)
                    elif isinstance(item, ast.FunctionDef):
                        class_model.methods.append(
                            {
                                "name": item.name,
                                "is_public": not item.name.startswith("_"),
                                "args": [
                                    arg.arg for arg in item.args.args[1:]
                                ],  # Skip self
                                "decorators": [
                                    d.id
                                    for d in item.decorator_list
                                    if isinstance(d, ast.Name)
                                ],
                            }
                        )

                # Extract dependencies and inheritance
                class_model.dependencies = self._extract_class_dependencies(node)
                class_model.inheritance = self._extract_inheritance(node)

                models.append(class_model)

        return models

    def _extract_init_attributes(self, init_method: ast.FunctionDef) -> list[str]:
        """Extract attributes assigned in __init__ method"""
        attributes = []

        for item in init_method.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        attributes.append(target.attr)
                    elif isinstance(target, ast.Name):
                        attributes.append(target.id)

        return attributes

    def _extract_class_dependencies(self, class_node: ast.ClassDef) -> list[str]:
        """Extract class dependencies from assignments"""
        dependencies = []

        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        # Look for class instantiations
                        if isinstance(item.value, ast.Call):
                            if isinstance(item.value.func, ast.Name):
                                dependencies.append(item.value.func.id)
                            elif isinstance(item.value.func, ast.Attribute):
                                dependencies.append(item.value.func.attr)

        return dependencies

    def _extract_inheritance(self, class_node: ast.ClassDef) -> list[str]:
        """Extract inheritance information"""
        inheritance = []

        for base in class_node.bases:
            if isinstance(base, ast.Name):
                inheritance.append(base.id)
            elif isinstance(base, ast.Attribute):
                inheritance.append(base.attr)

        return inheritance


class FunctionModelExtractor(ArtifactModelExtractor):
    """Extracts function models from Python source code"""

    def extract_models(self) -> list[ArtifactModel]:
        """Extract all function models from the source file"""
        if not self.ast_tree:
            return []

        models = []

        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef) and not self._is_method(node):
                function_model = FunctionArtifactModel(node.name, self.source_file)

                # Extract parameters
                function_model.parameters = [arg.arg for arg in node.args.args]

                # Extract decorators
                function_model.decorators = [
                    d.id for d in node.decorator_list if isinstance(d, ast.Name)
                ]

                # Extract return type annotation
                if node.returns:
                    function_model.return_type = ast.unparse(node.returns)

                models.append(function_model)

        return models

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (defined inside a class)"""
        parent = getattr(node, "parent", None)
        return parent and isinstance(parent, ast.ClassDef)


class ModuleModelExtractor(ArtifactModelExtractor):
    """Extracts module-level models from Python source code"""

    def extract_models(self) -> list[ArtifactModel]:
        """Extract module-level information"""
        if not self.ast_tree:
            return []

        module_model = ModuleArtifactModel(self.source_file.stem, self.source_file)

        # Extract classes, functions, imports, and constants
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                module_model.classes.append(node.name)
            elif isinstance(node, ast.FunctionDef) and not self._is_method(node):
                module_model.functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_model.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_model.imports.append(f"from {node.module}")
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        module_model.constants.append(target.id)

        return [module_model]

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (defined inside a class)"""
        parent = getattr(node, "parent", None)
        return parent and isinstance(parent, ast.ClassDef)


class TestModelGenerator(ABC):
    """Abstract base class for generating test models from artifact models"""

    def __init__(self, artifact_model: ArtifactModel):
        self.artifact_model = artifact_model

    @abstractmethod
    def generate_test_model(self) -> dict[str, Any]:
        """Generate a complete test model"""


class ClassTestModelGenerator(TestModelGenerator):
    """Generates test models for Python classes"""

    def generate_test_model(self) -> dict[str, Any]:
        """Generate a complete test model for a class"""
        return {
            "test_class_name": f"Test{self.artifact_model.name}",
            "artifact_type": "class",
            "test_methods": self._generate_test_methods(),
            "fixtures": self._generate_fixtures(),
            "assertions": self._generate_assertions(),
            "test_data": self._generate_test_data(),
        }

    def _generate_test_methods(self) -> list[dict[str, Any]]:
        """Generate test method definitions"""
        methods = []

        # Test initialization
        methods.append(
            {
                "name": f"test_{self.artifact_model.name.lower()}_initialization",
                "description": f"Test that {self.artifact_model.name} initializes correctly",
                "type": "initialization",
            }
        )

        # Test attributes
        for attr in self.artifact_model.attributes:
            methods.append(
                {
                    "name": f"test_{attr}_attribute_exists",
                    "description": f"Test that {attr} attribute exists and is properly initialized",
                    "type": "attribute",
                    "target": attr,
                }
            )

        # Test methods
        for method in self.artifact_model.methods:
            if method["is_public"]:
                methods.append(
                    {
                        "name": f"test_{method['name']}_method",
                        "description": f"Test that {method['name']} method works correctly",
                        "type": "method",
                        "target": method["name"],
                    }
                )

        return methods

    def _generate_fixtures(self) -> list[dict[str, Any]]:
        """Generate pytest fixtures"""
        fixtures = []

        # Main instance fixture
        fixtures.append(
            {
                "name": self.artifact_model.name.lower(),
                "type": "instance",
                "description": f"Get a fresh {self.artifact_model.name} instance",
            }
        )

        return fixtures

    def _generate_assertions(self) -> list[dict[str, Any]]:
        """Generate assertion patterns"""
        assertions = []

        # Attribute existence assertions
        for attr in self.artifact_model.attributes:
            assertions.append(
                {
                    "type": "attribute_exists",
                    "target": attr,
                    "pattern": f"assert hasattr(instance, '{attr}')",
                }
            )

        # Method existence assertions
        for method in self.artifact_model.methods:
            if method["is_public"]:
                assertions.append(
                    {
                        "type": "method_exists",
                        "target": method["name"],
                        "pattern": f"assert hasattr(instance, '{method['name']}')",
                    }
                )

        return assertions

    def _generate_test_data(self) -> dict[str, Any]:
        """Generate test data requirements"""
        return {
            "required_attributes": self.artifact_model.attributes,
            "required_methods": [
                m["name"] for m in self.artifact_model.methods if m["is_public"]
            ],
            "dependencies": self.artifact_model.dependencies,
            "inheritance": self.artifact_model.inheritance,
            "file_path": str(self.artifact_model.file_path),
        }


class FunctionTestModelGenerator(TestModelGenerator):
    """Generates test models for Python functions"""

    def generate_test_model(self) -> dict[str, Any]:
        """Generate a complete test model for a function"""
        return {
            "test_class_name": f"Test{self.artifact_model.name}",
            "artifact_type": "function",
            "test_methods": self._generate_test_methods(),
            "fixtures": self._generate_fixtures(),
            "assertions": self._generate_assertions(),
            "test_data": self._generate_test_data(),
        }

    def _generate_test_methods(self) -> list[dict[str, Any]]:
        """Generate test method definitions for functions"""
        methods = []

        # Test function import
        methods.append(
            {
                "name": f"test_{self.artifact_model.name.lower()}_import",
                "description": f"Test that {self.artifact_model.name} function can be imported",
                "type": "initialization",
            }
        )

        # Test function callability
        methods.append(
            {
                "name": f"test_{self.artifact_model.name.lower()}_callable",
                "description": f"Test that {self.artifact_model.name} function is callable",
                "type": "callable",
            }
        )

        return methods

    def _generate_fixtures(self) -> list[dict[str, Any]]:
        """Generate pytest fixtures for functions"""
        fixtures = []

        # Function fixture
        fixtures.append(
            {
                "name": self.artifact_model.name.lower(),
                "type": "function",
                "description": f"Get the {self.artifact_model.name} function",
            }
        )

        return fixtures

    def _generate_assertions(self) -> list[dict[str, Any]]:
        """Generate assertion patterns for functions"""
        assertions = []

        # Function import assertions
        assertions.append(
            {
                "type": "function_import",
                "target": self.artifact_model.name,
                "pattern": f"from {self.artifact_model.file_path.parent} import {self.artifact_model.name}",
            }
        )

        return assertions

    def _generate_test_data(self) -> dict[str, Any]:
        """Generate test data requirements for functions"""
        return {
            "function_name": self.artifact_model.name,
            "parameters": self.artifact_model.parameters,
            "return_type": self.artifact_model.return_type,
            "decorators": self.artifact_model.decorators,
            "file_path": str(self.artifact_model.file_path),
        }


class ModuleTestModelGenerator(TestModelGenerator):
    """Generates test models for Python modules"""

    def generate_test_model(self) -> dict[str, Any]:
        """Generate a complete test model for a module"""
        return {
            "test_class_name": f"Test{self.artifact_model.name}",
            "artifact_type": "module",
            "test_methods": self._generate_test_methods(),
            "fixtures": self._generate_fixtures(),
            "assertions": self._generate_assertions(),
            "test_data": self._generate_test_data(),
        }

    def _generate_test_methods(self) -> list[dict[str, Any]]:
        """Generate test method definitions for modules"""
        methods = []

        # Test module import
        methods.append(
            {
                "name": f"test_{self.artifact_model.name.lower()}_import",
                "description": f"Test that {self.artifact_model.name} module can be imported",
                "type": "initialization",
            }
        )

        # Test module contents
        if self.artifact_model.classes:
            methods.append(
                {
                    "name": f"test_{self.artifact_model.name.lower()}_classes",
                    "description": f"Test that {self.artifact_model.name} module has expected classes",
                    "type": "module_content",
                    "target": "classes",
                }
            )

        if self.artifact_model.functions:
            methods.append(
                {
                    "name": f"test_{self.artifact_model.name.lower()}_functions",
                    "description": f"Test that {self.artifact_model.name} module has expected functions",
                    "type": "module_content",
                    "target": "functions",
                }
            )

        return methods

    def _generate_fixtures(self) -> list[dict[str, Any]]:
        """Generate pytest fixtures for modules"""
        fixtures = []

        # Module fixture
        fixtures.append(
            {
                "name": self.artifact_model.name.lower(),
                "type": "module",
                "description": f"Get the {self.artifact_model.name} module",
            }
        )

        return fixtures

    def _generate_assertions(self) -> list[dict[str, Any]]:
        """Generate assertion patterns for modules"""
        assertions = []

        # Module import assertions
        assertions.append(
            {
                "type": "module_import",
                "target": self.artifact_model.name,
                "pattern": f"import {self.artifact_model.file_path.parent}",
            }
        )

        return assertions

    def _generate_test_data(self) -> dict[str, Any]:
        """Generate test data requirements for modules"""
        return {
            "module_name": self.artifact_model.name,
            "classes": self.artifact_model.classes,
            "functions": self.artifact_model.functions,
            "imports": self.artifact_model.imports,
            "constants": self.artifact_model.constants,
            "file_path": str(self.artifact_model.file_path),
        }


class TestCodeGenerator(ABC):
    """Abstract base class for generating actual test code from test models"""

    def __init__(self, test_model: dict[str, Any]):
        self.test_model = test_model

    @abstractmethod
    def generate_test_code(self) -> str:
        """Generate complete test code"""


class PytestCodeGenerator(TestCodeGenerator):
    """Generates pytest-compatible test code"""

    def __init__(self, test_model: dict[str, Any], artifact_type: str = "class"):
        self.test_model = test_model
        self.artifact_type = artifact_type

    def generate_test_code(self) -> str:
        """Generate complete pytest test code"""
        code_lines = [
            "#!/usr/bin/env python3",
            '"""',
            f"Generated tests for {self.test_model['test_class_name']}",
            '"""',
            "",
            "import pytest",
            "from pathlib import Path",
            "",
            f"from {self._get_import_path()} import {self._get_class_name()}",
            "",
            "",
            f"class {self.test_model['test_class_name']}:",
            f'    """Generated tests for {self._get_class_name()}"""',
            "",
        ]

        # Add fixtures
        for fixture in self.test_model.get("fixtures", []):
            code_lines.extend(self._generate_fixture(fixture))
            code_lines.append("")

        # Add test methods
        for method in self.test_model.get("test_methods", []):
            code_lines.extend(self._generate_test_method(method))
            code_lines.append("")

        return "\n".join(code_lines)

    def _get_import_path(self) -> str:
        """Get the import path for the class"""
        # Extract from the artifact model's file path
        artifact_model = getattr(self, "artifact_model", None)
        if artifact_model and hasattr(artifact_model, "file_path"):
            # Convert file path to import path
            file_path = artifact_model.file_path
            if file_path.suffix == ".py":
                # Convert src/ghostbusters/ghostbusters_orchestrator.py to src.ghostbusters.ghostbusters_orchestrator
                return (
                    str(file_path.with_suffix("")).replace("/", ".").replace("\\", ".")
                )
        # Fallback for backward compatibility
        return "src.ghostbusters.ghostbusters_orchestrator"

    def _get_class_name(self) -> str:
        """Get the class/function/module name from the test model"""
        # Extract from test class name (remove "Test" prefix)
        return self.test_model["test_class_name"].replace("Test", "")

    def _get_artifact_name(self) -> str:
        """Get the actual artifact name for testing"""
        artifact_model = getattr(self, "artifact_model", None)
        if artifact_model and hasattr(artifact_model, "name"):
            return artifact_model.name
        return self._get_class_name()

    def _generate_fixture(self, fixture: dict[str, Any]) -> list[str]:
        """Generate a pytest fixture"""
        if fixture["type"] == "instance":
            return [
                "    @pytest.fixture",
                f"    def {fixture['name']}(self):",
                f"        \"\"\"{fixture['description']}\"\"\"",
                f"        return {self._get_artifact_name()}()",
            ]
        return []

    def _generate_test_method(self, method: dict[str, Any]) -> list[str]:
        """Generate a test method"""
        lines = [
            f"    def {method['name']}(self, {self._get_fixture_params(method)}):",
            f"        \"\"\"{method['description']}\"\"\"",
        ]

        # Use artifact_type from __init__
        artifact_type = getattr(self, "artifact_type", "class")

        if artifact_type == "class":
            if method["type"] == "initialization":
                lines.extend(
                    [
                        f"        instance = {self._get_artifact_name()}()",
                        "        assert instance is not None",
                        f"        assert isinstance(instance, {self._get_artifact_name()})",
                    ]
                )
            elif method["type"] == "attribute":
                lines.extend(
                    [
                        f"        instance = {self._get_artifact_name()}()",
                        f"        assert hasattr(instance, '{method['target']}')",
                        "        # Add specific attribute validation here",
                    ]
                )
            elif method["type"] == "method":
                lines.extend(
                    [
                        f"        instance = {self._get_artifact_name()}()",
                        f"        assert hasattr(instance, '{method['target']}')",
                        f"        method_obj = getattr(instance, '{method['target']}')",
                        "        assert callable(method_obj)",
                    ]
                )
        elif artifact_type == "function":
            if method["type"] == "initialization":
                lines.extend(
                    [
                        "        # Test that function can be imported",
                        f"        from {self._get_import_path()} import {self._get_artifact_name()}",
                        f"        assert {self._get_artifact_name()} is not None",
                        f"        assert callable({self._get_artifact_name()})",
                    ]
                )
            elif method["type"] == "callable":
                lines.extend(
                    [
                        "        # Test that function is callable",
                        f"        from {self._get_import_path()} import {self._get_artifact_name()}",
                        f"        assert callable({self._get_artifact_name()})",
                    ]
                )
        elif artifact_type == "module":
            if method["type"] == "initialization":
                lines.extend(
                    [
                        "        # Test that module can be imported",
                        f"        import {self._get_import_path()}",
                        f"        module = {self._get_import_path()}",
                        "        assert module is not None",
                    ]
                )
            elif method["type"] == "module_content":
                lines.extend(
                    [
                        f"        # Test that module has expected {method['target']}",
                        f"        import {self._get_import_path()}",
                        f"        module = {self._get_import_path()}",
                        f"        assert hasattr(module, '{method['target']}')",
                    ]
                )

        return lines

    def _get_fixture_params(self, method: dict[str, Any]) -> str:
        """Get fixture parameters for a test method"""
        # For now, all methods use the instance fixture
        return "ghostbustersorchestrator"


class PythonUnitTestGenerator:
    """Main system for generating Python unit tests from implementation models"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_output_dir = project_root / "tests" / "generated"
        self.test_output_dir.mkdir(parents=True, exist_ok=True)

        # Register extractors for different artifact types
        self.extractors = {
            "class": ClassModelExtractor,
            "function": FunctionModelExtractor,
            "module": ModuleModelExtractor,
        }

        # Register test model generators
        self.test_generators = {
            "class": ClassTestModelGenerator,
            "function": FunctionTestModelGenerator,  # Functions can use class-style tests
            "module": ModuleTestModelGenerator,  # Modules can use class-style tests
        }

        # Register code generators
        self.code_generators = {"pytest": PytestCodeGenerator}

    def generate_tests_for_file(
        self, source_file: Path, artifact_types: list[str] = None
    ) -> list[Path]:
        """Generate tests for all artifacts in a source file"""
        if artifact_types is None:
            artifact_types = ["class", "function", "module"]

        generated_files = []

        for artifact_type in artifact_types:
            if artifact_type in self.extractors:
                extractor_class = self.extractors[artifact_type]
                extractor = extractor_class(source_file)

                try:
                    models = extractor.extract_models()
                    for model in models:
                        test_file = self._generate_test_for_model(model)
                        if test_file:
                            generated_files.append(test_file)
                except Exception as e:
                    print(
                        f"Failed to extract {artifact_type} models from {source_file}: {e}"
                    )

        return generated_files

    def _generate_test_for_model(self, model: ArtifactModel) -> Optional[Path]:
        """Generate test for a specific artifact model"""
        try:
            # Generate test model
            if model.artifact_type in self.test_generators:
                generator_class = self.test_generators[model.artifact_type]
                test_generator = generator_class(model)
                test_model = test_generator.generate_test_model()

                # Generate test code
                code_generator = PytestCodeGenerator(test_model, model.artifact_type)
                test_code = code_generator.generate_test_code()

                # Write test file
                test_file = (
                    self.test_output_dir
                    / f"test_{model.name.lower()}_{model.artifact_type}_generated.py"
                )
                test_file.write_text(test_code)

                return test_file
        except Exception as e:
            print(f"Failed to generate test for {model.name}: {e}")

        return None

    def generate_tests_from_project_model(self) -> list[Path]:
        """Generate tests for all artifacts defined in project model"""
        generated_files = []

        # Load project model
        project_model_file = self.project_root / "project_model_registry.json"
        if project_model_file.exists():
            with open(project_model_file) as f:
                project_model = json.load(f)

            # Generate tests for each domain
            for domain_name, domain_config in project_model.get("domains", {}).items():
                if "patterns" in domain_config:
                    for pattern in domain_config["patterns"]:
                        # Find source files matching pattern
                        source_files = list(self.project_root.glob(pattern))
                        for source_file in source_files:
                            if source_file.is_file() and source_file.suffix == ".py":
                                try:
                                    test_files = self.generate_tests_for_file(
                                        source_file
                                    )
                                    generated_files.extend(test_files)
                                except Exception as e:
                                    print(
                                        f"Failed to generate tests for {source_file}: {e}"
                                    )

        return generated_files


if __name__ == "__main__":
    # Example usage
    project_root = Path()
    test_generator = PythonUnitTestGenerator(project_root)

    # Generate tests for GhostbustersOrchestrator
    source_file = Path("src/ghostbusters/ghostbusters_orchestrator.py")
    test_files = test_generator.generate_tests_for_file(source_file, ["class"])
    print(f"Generated {len(test_files)} test files")

    # Generate tests from project model
    generated_files = test_generator.generate_tests_from_project_model()
    print(f"Generated {len(generated_files)} total test files")
