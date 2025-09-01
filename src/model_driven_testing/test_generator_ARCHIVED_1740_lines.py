#!/usr/bin/env python3
"""
Reflective Module (RM) Compliant Test Generation System

This system generates unit tests directly from implementation models to ensure
test coverage and maintainability. It is now RM compliant with:
- Self-monitoring of generation quality
- Self-correction of broken tests
- Interface constraints for test generation
- Health monitoring and reporting
"""

import ast
import json
import logging
import os
import time
import functools
import inspect
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

# RM Compliance imports
from src.reflective_modules.registry import ReflectiveModuleRegistry
from src.reflective_modules.base import ReflectiveModule

# AST Analysis Domain - Use centralized AST parsing
from src.ast_analysis.api.ast_api import ASTAnalysisAPI
from src.ast_analysis.core.type_extractor import TypeExtractor

# Configure logging for RM compliance with detailed profiling
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("logs/test_generation.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)


class RMEnhancer:
    """RM Compliance: Automatically infers and adds logging/profiling to Python implementations"""

    @staticmethod
    def should_enhance_method(method_name: str, class_name: str = None) -> bool:
        """RM Inference: Determine if method should be enhanced based on context"""
        # Always enhance core RM methods
        if method_name.startswith("get_rm_") or method_name.startswith("_rm_"):
            return True

        # Enhance methods that suggest complexity
        complexity_indicators = ["generate", "extract", "parse", "analyze", "validate", "transform"]
        if any(indicator in method_name.lower() for indicator in complexity_indicators):
            return True

        # Enhance methods in test generation domain
        if class_name and "test" in class_name.lower():
            return True

        return False

    @staticmethod
    def create_profiling_decorator(method_name: str, class_name: str = None) -> callable:
        """RM Inference: Create context-aware profiling decorator"""
        if not RMEnhancer.should_enhance_method(method_name, class_name):
            return lambda func: func  # No-op decorator

        def profile_method(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                context = f"{class_name}.{method_name}" if class_name else method_name

                logger.debug(f"🚀 RM-Enhanced: Starting {context}")
                logger.debug(f"   Args: {args[1:] if args else 'None'}")
                logger.debug(f"   Kwargs: {kwargs}")

                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time

                    # RM Inference: Log based on execution time
                    if execution_time > 1.0:
                        logger.warning(f"🐌 RM-Performance: {context} took {execution_time:.4f}s (slow)")
                    elif execution_time > 0.1:
                        logger.info(f"📊 RM-Performance: {context} took {execution_time:.4f}s")
                    else:
                        logger.debug(f"⚡ RM-Performance: {context} took {execution_time:.4f}s (fast)")

                    return result

                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"❌ RM-Error: {context} failed after {execution_time:.4f}s")
                    logger.error(f"   Exception: {type(e).__name__}: {e}")
                    raise
                finally:
                    execution_time = time.time() - start_time
                    logger.debug(f"📊 RM-Complete: {context} total time: {execution_time:.4f}s")

            return wrapper

        return profile_method


# RM Compliance: Auto-enhancement decorator
def rm_enhance(func):
    """RM Inference: Automatically enhance methods with logging/profiling based on context"""
    # Infer method name and class name from the function
    method_name = func.__name__
    class_name = func.__qualname__.split(".")[0] if "." in func.__qualname__ else None

    # RM Inference: Automatically determine enhancement level
    return RMEnhancer.create_profiling_decorator(method_name, class_name)(func)


# RM Compliance: Environment variable for controlled generation
AUTO_GENERATION_DISABLED = os.getenv("DISABLE_TEST_GENERATION", "false").lower() == "true"

# RM Compliance: Health thresholds
MAX_GENERATION_FAILURES = 3
MAX_BROKEN_TESTS = 5
GENERATION_QUALITY_THRESHOLD = 0.8  # 80% of generated tests must be valid


class TestGenerationHealth:
    """RM Compliance: Health monitoring for test generation system"""

    def __init__(self):
        self.generation_failures = 0
        self.broken_tests = 0
        self.total_generated = 0
        self.valid_tests = 0
        self.health_status = "healthy"
        self.last_health_check = None

    def record_generation_failure(self):
        """Record a test generation failure"""
        self.generation_failures += 1
        self._update_health_status()

    def record_broken_test(self):
        """Record a broken generated test"""
        self.broken_tests += 1
        self._update_health_status()

    def record_successful_test(self):
        """Record a successfully generated test"""
        self.total_generated += 1
        self.valid_tests += 1

    def record_invalid_test(self):
        """Record an invalid generated test"""
        self.total_generated += 1

    def _update_health_status(self):
        """Update overall health status based on thresholds"""
        if self.generation_failures >= MAX_GENERATION_FAILURES:
            self.health_status = "critical"
        elif self.broken_tests >= MAX_BROKEN_TESTS:
            self.health_status = "degraded"
        elif self.total_generated > 0:
            quality_ratio = self.valid_tests / self.total_generated
            if quality_ratio < GENERATION_QUALITY_THRESHOLD:
                self.health_status = "degraded"
            else:
                self.health_status = "healthy"

    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        quality_ratio = self.valid_tests / self.total_generated if self.total_generated > 0 else 0.0

        return {
            "status": self.health_status,
            "generation_failures": self.generation_failures,
            "broken_tests": self.broken_tests,
            "total_generated": self.total_generated,
            "valid_tests": self.valid_tests,
            "quality_ratio": quality_ratio,
            "thresholds": {"max_generation_failures": MAX_GENERATION_FAILURES, "max_broken_tests": MAX_BROKEN_TESTS, "quality_threshold": GENERATION_QUALITY_THRESHOLD},
        }


class ArtifactModel:
    """RM Compliance: Enhanced artifact model with validation"""

    def __init__(self, name: str, source_file: Path, artifact_type: str = "class"):
        self.name = name
        self.source_file = source_file
        self.artifact_type = artifact_type
        self.file_path = source_file  # For backward compatibility
        self.validation_errors = []
        self.is_valid = True

    def validate(self) -> bool:
        """RM Compliance: Validate artifact model"""
        self.validation_errors = []

        # Check required attributes
        if not self.name:
            self.validation_errors.append("Missing artifact name")

        if not self.source_file:
            self.validation_errors.append("Missing source file")

        if not self.artifact_type:
            self.validation_errors.append("Missing artifact type")

        # Check file existence
        if self.source_file and not self.source_file.exists():
            self.validation_errors.append(f"Source file does not exist: {self.source_file}")

        # Check file extension
        if self.source_file and self.source_file.suffix != ".py":
            self.validation_errors.append(f"Source file must be Python file: {self.source_file}")

        self.is_valid = len(self.validation_errors) == 0
        return self.is_valid

    def get_validation_report(self) -> Dict[str, Any]:
        """Get validation report for RM compliance"""
        return {"is_valid": self.is_valid, "errors": self.validation_errors, "name": self.name, "source_file": str(self.source_file), "artifact_type": self.artifact_type}


class ClassArtifactModel(ArtifactModel):
    """RM Compliance: Enhanced class artifact model"""

    def __init__(self, name: str, source_file: Path):
        super().__init__(name, source_file, "class")
        self.attributes: List[str] = []
        self.methods: List[Dict[str, Any]] = []
        self.dependencies: List[str] = []
        self.inheritance: List[str] = []

    def validate(self) -> bool:
        """RM Compliance: Validate class artifact model"""
        base_valid = super().validate()

        # Class-specific validation
        if not self.name[0].isupper():
            self.validation_errors.append("Class name should start with uppercase")

        if not self.name.replace("_", "").isalnum():
            self.validation_errors.append("Class name should be alphanumeric with underscores")

        self.is_valid = base_valid and len(self.validation_errors) == 0
        return self.is_valid


class FunctionArtifactModel(ArtifactModel):
    """RM Compliance: Enhanced function artifact model"""

    def __init__(self, name: str, source_file: Path):
        super().__init__(name, source_file, "function")
        self.parameters: List[str] = []
        self.decorators: List[str] = []
        self.return_type: Optional[str] = None

    def validate(self) -> bool:
        """RM Compliance: Validate function artifact model"""
        base_valid = super().validate()

        # Function-specific validation
        if not self.name[0].islower() and not self.name.startswith("_"):
            self.validation_errors.append("Function name should start with lowercase or underscore")

        self.is_valid = base_valid and len(self.validation_errors) == 0
        return self.is_valid


class ModuleArtifactModel(ArtifactModel):
    """RM Compliance: Enhanced module artifact model"""

    def __init__(self, name: str, source_file: Path):
        super().__init__(name, source_file, "module")
        self.classes: List[str] = []
        self.functions: List[str] = []
        self.imports: List[str] = []
        self.constants: List[str] = []

    def validate(self) -> bool:
        """RM Compliance: Validate module artifact model"""
        base_valid = super().validate()

        # Module-specific validation
        if not self.name.replace("_", "").isalnum():
            self.validation_errors.append("Module name should be alphanumeric with underscores")

        self.is_valid = base_valid and len(self.validation_errors) == 0
        return self.is_valid


class ArtifactModelExtractor(ABC):
    """RM Compliance: Enhanced artifact model extractor with validation"""

    def __init__(self, source_file: Path):
        self.source_file = source_file
        self.ast_tree = None
        self.extraction_errors = []
        self.is_extraction_valid = True

        try:
            with open(source_file, "r") as f:
                source_code = f.read()
            self.ast_tree = ast.parse(source_code)
        except Exception as e:
            self.extraction_errors.append(f"Failed to parse {source_file}: {e}")
            self.is_extraction_valid = False

    def validate_extraction(self) -> bool:
        """RM Compliance: Validate that extraction was successful"""
        if not self.ast_tree:
            self.extraction_errors.append("No AST tree generated")
            self.is_extraction_valid = False

        if not self.source_file.exists():
            self.extraction_errors.append(f"Source file does not exist: {self.source_file}")
            self.is_extraction_valid = False

        self.is_extraction_valid = len(self.extraction_errors) == 0
        return self.is_extraction_valid

    def get_extraction_report(self) -> Dict[str, Any]:
        """Get extraction report for RM compliance"""
        return {"is_valid": self.is_extraction_valid, "errors": self.extraction_errors, "source_file": str(self.source_file), "has_ast_tree": self.ast_tree is not None}

    @abstractmethod
    def extract_models(self) -> List[ArtifactModel]:
        """Extract artifact models from source code"""
        pass


class ClassModelExtractor(ArtifactModelExtractor):
    """RM Compliance: Enhanced class model extractor"""

    def extract_models(self) -> List[ArtifactModel]:
        """Extract all class models from the source file"""
        if not self.validate_extraction():
            logger.warning(f"Extraction validation failed for {self.source_file}")
            return []

        models = []

        try:
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
                                    "args": [arg.arg for arg in item.args.args[1:]],  # Skip self
                                    "decorators": [d.id for d in item.decorator_list if isinstance(d, ast.Name)],
                                }
                            )

                    # Extract dependencies and inheritance
                    class_model.dependencies = self._extract_class_dependencies(node)
                    class_model.inheritance = self._extract_inheritance(node)

                    # RM Compliance: Validate before adding
                    if class_model.validate():
                        models.append(class_model)
                    else:
                        logger.warning(f"Invalid class model for {node.name}: {class_model.validation_errors}")

        except Exception as e:
            logger.error(f"Error extracting class models from {self.source_file}: {e}")

        return models

    def _extract_init_attributes(self, init_method: ast.FunctionDef) -> List[str]:
        """Extract attributes assigned in __init__ method"""
        attributes = []

        try:
            for item in init_method.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                            attributes.append(target.attr)
                        elif isinstance(target, ast.Name):
                            attributes.append(target.id)
        except Exception as e:
            logger.warning(f"Error extracting init attributes: {e}")

        return attributes

    def _extract_class_dependencies(self, class_node: ast.ClassDef) -> List[str]:
        """Extract class dependencies from assignments"""
        dependencies = []

        try:
            for item in class_node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                            # Look for class instantiations
                            if isinstance(item.value, ast.Call):
                                if isinstance(item.value.func, ast.Name):
                                    dependencies.append(item.value.func.id)
                                elif isinstance(item.value.func, ast.Attribute):
                                    dependencies.append(item.value.func.attr)
        except Exception as e:
            logger.warning(f"Error extracting class dependencies: {e}")

        return dependencies

    def _extract_inheritance(self, class_node: ast.ClassDef) -> List[str]:
        """Extract inheritance information"""
        inheritance = []

        try:
            for base in class_node.bases:
                if isinstance(base, ast.Name):
                    inheritance.append(base.id)
                elif isinstance(base, ast.Attribute):
                    inheritance.append(base.attr)
        except Exception as e:
            logger.warning(f"Error extracting inheritance: {e}")

        return inheritance


class FunctionModelExtractor(ArtifactModelExtractor):
    """RM Compliance: Enhanced function model extractor"""

    def extract_models(self) -> List[ArtifactModel]:
        """Extract all function models from the source file"""
        if not self.validate_extraction():
            logger.warning(f"Extraction validation failed for {self.source_file}")
            return []

        models = []

        try:
            # First pass: collect all class names to identify methods
            class_names = set()
            for node in ast.walk(self.ast_tree):
                if isinstance(node, ast.ClassDef):
                    class_names.add(node.name)

            # Second pass: extract only standalone functions (not methods)
            for node in ast.walk(self.ast_tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if this function is inside a class by looking at its name pattern
                    # Methods typically start with underscore or are clearly part of a class
                    if not self._is_method(node) and not self._is_likely_method(node, class_names):
                        function_model = FunctionArtifactModel(node.name, self.source_file)

                        # Extract parameters
                        function_model.parameters = [arg.arg for arg in node.args.args]

                        # Extract decorators
                        function_model.decorators = [d.id for d in node.decorator_list if isinstance(d, ast.Name)]

                        # Extract return type annotation
                        if node.returns:
                            function_model.return_type = ast.unparse(node.returns)

                        # RM Compliance: Validate before adding
                        if function_model.validate():
                            models.append(function_model)
                        else:
                            logger.warning(f"Invalid function model for {node.name}: {function_model.validation_errors}")

        except Exception as e:
            logger.error(f"Error extracting function models from {self.source_file}: {e}")

        return models

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method using AST domain"""
        try:
            # Use AST domain for proper method detection
            # This is a fallback - the main extraction should use AST domain
            if node.name.startswith("_"):
                return True
            return False
        except Exception:
            return False

    def _is_likely_method(self, node: ast.FunctionDef, class_names: Set[str]) -> bool:
        """Check if function is likely a method based on context"""
        try:
            # Check if function name suggests it's a method
            if node.name.startswith("_"):
                return True

            # Check if function has 'self' as first parameter
            if node.args.args and node.args.args[0].arg == "self":
                return True

            return False
        except Exception:
            return False


class ModuleModelExtractor(ArtifactModelExtractor):
    """RM Compliance: Enhanced module model extractor"""

    def extract_models(self) -> List[ArtifactModel]:
        """Extract module-level information"""
        if not self.validate_extraction():
            logger.warning(f"Extraction validation failed for {self.source_file}")
            return []

        try:
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

            # RM Compliance: Validate before adding
            if module_model.validate():
                return [module_model]
            else:
                logger.warning(f"Invalid module model: {module_model.validation_errors}")
                return []

        except Exception as e:
            logger.error(f"Error extracting module model from {self.source_file}: {e}")
            return []

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method using AST domain"""
        try:
            # Use AST domain for proper method detection
            # This is a fallback - the main extraction should use AST domain
            if node.name.startswith("_"):
                return True
            return False
        except Exception:
            return False


class TestModelGenerator(ABC):
    """RM Compliance: Enhanced test model generator with validation"""

    def __init__(self, artifact_model: ArtifactModel):
        self.artifact_model = artifact_model
        self.generation_errors = []
        self.is_generation_valid = True

    def validate_generation(self) -> bool:
        """RM Compliance: Validate test model generation"""
        if not self.artifact_model.is_valid:
            self.generation_errors.append("Artifact model is invalid")
            self.is_generation_valid = False

        self.is_generation_valid = len(self.generation_errors) == 0
        return self.is_generation_valid

    def get_generation_report(self) -> Dict[str, Any]:
        """Get generation report for RM compliance"""
        return {"is_valid": self.is_generation_valid, "errors": self.generation_errors, "artifact_model": self.artifact_model.get_validation_report()}

    @abstractmethod
    def generate_test_model(self) -> Dict[str, Any]:
        """Generate a complete test model"""
        pass


class ClassTestModelGenerator(TestModelGenerator):
    """RM Compliance: Enhanced class test model generator"""

    def generate_test_model(self) -> Dict[str, Any]:
        """Generates test models for Python classes"""
        if not self.validate_generation():
            logger.warning(f"Generation validation failed for {self.artifact_model.name}")
            return {}

        try:
            return {
                "test_class_name": f"Test{self.artifact_model.name}",
                "artifact_name": self.artifact_model.name,
                "test_methods": self._generate_test_methods(),
                "fixtures": self._generate_fixtures(),
                "test_data": self._generate_test_data(),
            }
        except Exception as e:
            logger.error(f"Error generating test model for {self.artifact_model.name}: {e}")
            return {}

    def _generate_test_methods(self) -> List[Dict[str, Any]]:
        """Generate test method definitions"""
        methods = []

        try:
            # Always include initialization test
            methods.append({"name": f"test_{self.artifact_model.name.lower()}_initialization", "type": "initialization", "description": f"Test that {self.artifact_model.name} initializes correctly"})

            # Generate attribute tests
            for attr in self.artifact_model.attributes:
                methods.append({"name": f"test_{attr}_attribute_exists", "type": "attribute", "description": f"Test that {attr} attribute exists and is properly initialized"})

            # Generate method tests
            for method in self.artifact_model.methods:
                if method["is_public"]:
                    methods.append({"name": f"test_{method['name']}_method_exists", "type": "method", "description": f"Test that {method['name']} method exists and is callable"})

        except Exception as e:
            logger.warning(f"Error generating test methods: {e}")

        return methods

    def _generate_fixtures(self) -> List[Dict[str, Any]]:
        """Generate pytest fixtures"""
        fixtures = []

        try:
            fixtures.append({"name": self.artifact_model.name.lower(), "type": "instance", "description": f"Get a fresh {self.artifact_model.name} instance"})
        except Exception as e:
            logger.warning(f"Error generating fixtures: {e}")

        return fixtures

    def _generate_test_data(self) -> Dict[str, Any]:
        """Generate test data requirements"""
        return {"setup_required": True, "teardown_required": False, "mock_dependencies": len(self.artifact_model.dependencies) > 0}


class FunctionTestModelGenerator(TestModelGenerator):
    """RM Compliance: Enhanced function test model generator"""

    def generate_test_model(self) -> Dict[str, Any]:
        """Generates test models for Python functions"""
        if not self.validate_generation():
            logger.warning(f"Generation validation failed for {self.artifact_model.name}")
            return {}

        try:
            return {
                "test_class_name": f"Test{self.artifact_model.name.capitalize()}",
                "artifact_name": self.artifact_model.name,
                "test_methods": self._generate_test_methods(),
                "fixtures": self._generate_fixtures(),
                "test_data": self._generate_test_data(),
            }
        except Exception as e:
            logger.error(f"Error generating test model for {self.artifact_model.name}: {e}")
            return {}

    def _generate_test_methods(self) -> List[Dict[str, Any]]:
        """Generate test method definitions"""
        methods = []

        try:
            methods.append({"name": f"test_{self.artifact_model.name}_function_exists", "type": "existence", "description": f"Test that {self.artifact_model.name} function exists and is callable"})

            if self.artifact_model.parameters:
                methods.append({"name": f"test_{self.artifact_model.name}_parameters", "type": "parameters", "description": f"Test that {self.artifact_model.name} has correct parameters"})

        except Exception as e:
            logger.warning(f"Error generating test methods: {e}")

        return methods

    def _generate_fixtures(self) -> List[Dict[str, Any]]:
        """Generate pytest fixtures"""
        return []

    def _generate_test_data(self) -> Dict[str, Any]:
        """Generate test data requirements"""
        return {"setup_required": False, "teardown_required": False, "mock_dependencies": False}


class TestCodeGenerator(ABC):
    """RM Compliance: Enhanced test code generator with validation"""

    def __init__(self, test_model: Dict[str, Any]):
        self.test_model = test_model
        self.generation_errors = []
        self.is_generation_valid = True

    def validate_test_model(self) -> bool:
        """RM Compliance: Validate test model before code generation"""
        required_fields = ["test_class_name", "test_methods"]

        for field in required_fields:
            if field not in self.test_model:
                self.generation_errors.append(f"Missing required field: {field}")

        if not self.test_model.get("test_methods"):
            self.generation_errors.append("No test methods defined")

        self.is_generation_valid = len(self.generation_errors) == 0
        return self.is_generation_valid

    def get_validation_report(self) -> Dict[str, Any]:
        """Get validation report for RM compliance"""
        return {"is_valid": self.is_generation_valid, "errors": self.generation_errors, "test_model_keys": list(self.test_model.keys())}

    @abstractmethod
    def generate_test_code(self) -> str:
        """Generate complete test code"""
        pass


class PytestCodeGenerator(TestCodeGenerator):
    """RM Compliance: Enhanced pytest code generator with validation"""

    def __init__(self, test_model: Dict[str, Any], artifact_type: str = "class", artifact_model: Optional[ArtifactModel] = None):
        super().__init__(test_model)
        self.artifact_type = artifact_type
        self.artifact_model = artifact_model

    def generate_test_code(self) -> str:
        """Generate complete pytest test code"""
        if not self.validate_test_model():
            logger.error(f"Test model validation failed: {self.generation_errors}")
            return "# Test generation failed due to validation errors\n"

        try:
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

        except Exception as e:
            logger.error(f"Error generating test code: {e}")
            return f"# Test generation failed: {e}\n"

    def _get_import_path(self) -> str:
        """Get the import path for the class"""
        # First try to use source file path if available
        if hasattr(self, "source_file_path") and self.source_file_path:
            file_path = self.source_file_path
            if file_path.suffix == ".py":
                # Convert src/ghostbusters/ghostbusters_orchestrator.py to src.ghostbusters.ghostbusters_orchestrator
                return str(file_path.with_suffix("")).replace("/", ".").replace("\\", ".")

        # Fallback to artifact model
        if self.artifact_model and hasattr(self.artifact_model, "file_path"):
            # Convert file path to import path
            file_path = self.artifact_model.file_path
            if file_path.suffix == ".py":
                # Convert src/ghostbusters/ghostbusters_orchestrator.py to src.ghostbusters.ghostbusters_orchestrator
                return str(file_path.with_suffix("")).replace("/", ".").replace("\\", ".")

        # If we can't determine the path, raise an error instead of using a hardcoded fallback
        raise ValueError(f"Cannot determine import path for artifact model: {self.artifact_model}")

    def _get_class_name(self) -> str:
        """Get the class/function/module name from the test model"""
        # Use the artifact model name if available
        if self.artifact_model and hasattr(self.artifact_model, "name"):
            return self.artifact_model.name

        # For functions, use the artifact_name which preserves the original case
        if self.artifact_type == "function":
            return self.test_model.get("artifact_name", "unknown")

        # Fallback to extracting from test class name (remove "Test" prefix)
        return self.test_model["test_class_name"].replace("Test", "")

    def _get_artifact_name(self) -> str:
        """Get the actual artifact name for testing"""
        if self.artifact_model and hasattr(self.artifact_model, "name"):
            return self.artifact_model.name
        return self._get_class_name()

    def _generate_fixture(self, fixture: Dict[str, Any]) -> List[str]:
        """Generate a pytest fixture"""
        if fixture["type"] == "instance":
            # Check if we have defaults for Pydantic models
            defaults = fixture.get("defaults", {})
            if defaults:
                # Generate with defaults
                default_args = ", ".join([f"{k}={repr(v)}" for k, v in defaults.items()])
                return [
                    "    @pytest.fixture",
                    f"    def {fixture['name']}(self):",
                    f'        """{fixture["description"]}"""',
                    f"        return {self._get_artifact_name()}({default_args})",
                ]
            else:
                # Generate without defaults
                return [
                    "    @pytest.fixture",
                    f"    def {fixture['name']}(self):",
                    f'        """{fixture["description"]}"""',
                    f"        return {self._get_artifact_name()}()",
                ]
        return []

    def _generate_test_method(self, method: Dict[str, Any]) -> List[str]:
        """Generate a test method"""
        fixture_params = self._get_fixture_params(method)
        param_string = f", {fixture_params}" if fixture_params else ""

        lines = [
            f"    def {method['name']}(self{param_string}):",
            f'        """{method["description"]}"""',
        ]

        # Use artifact_type from __init__
        artifact_type = getattr(self, "artifact_type", "class")

        if artifact_type == "class":
            if method["type"] == "initialization":
                lines.extend(
                    [
                        f"        assert {self._get_fixture_name()} is not None",
                        f"        assert isinstance({self._get_fixture_name()}, {self._get_artifact_name()})",
                    ]
                )
            elif method["type"] == "attribute":
                target_name = method.get("target_name", method["name"].replace("_attribute_exists", ""))
                lines.extend(
                    [
                        f"        assert hasattr({self._get_fixture_name()}, '{target_name}')",
                        "# Add specific attribute validation here",
                    ]
                )
            elif method["type"] == "method":
                target_name = method.get("target_name", method["name"].replace("_method_exists", ""))
                lines.extend(
                    [
                        f"        assert hasattr({self._get_fixture_name()}, '{target_name}')",
                        f"        assert callable(getattr({self._get_fixture_name()}, '{target_name}'))",
                    ]
                )
            elif method["type"] == "abstract_method":
                target_name = method.get("target_name", method["name"].replace("_method_exists", ""))
                lines.extend(
                    [
                        f"        assert hasattr({self._get_artifact_name()}, '{target_name}')",
                        f"        # Abstract method - cannot be called directly",
                    ]
                )
        elif artifact_type == "function":
            if method["type"] == "existence":
                lines.extend(
                    [
                        f"        assert {self._get_artifact_name()} is not None",
                        f"        assert callable({self._get_artifact_name()})",
                    ]
                )
            elif method["type"] == "parameters":
                lines.extend(
                    [
                        f"        # Test parameter validation for {self._get_artifact_name()}",
                        "# Add parameter-specific tests here",
                    ]
                )

        return lines

    def _get_fixture_params(self, method: Dict[str, Any]) -> str:
        """Get fixture parameters for test method"""
        fixtures = self.test_model.get("fixtures", [])
        fixture_names = [f["name"] for f in fixtures if f["type"] == "instance"]
        return ", ".join(fixture_names) if fixture_names else ""

    def _get_fixture_name(self) -> str:
        """Get the name of the instance fixture"""
        fixtures = self.test_model.get("fixtures", [])
        instance_fixtures = [f["name"] for f in fixtures if f["type"] == "instance"]
        return instance_fixtures[0] if instance_fixtures else "instance"


class PythonUnitTestGenerator(ReflectiveModule):
    """RM Compliance: Reflective Module for Python unit test generation"""

    def __init__(self, project_root: Path = None):
        super().__init__()

        # RM Compliance: Initialize health monitoring
        self.health_monitor = TestGenerationHealth()

        # RM Compliance: Register with reflective module registry
        ReflectiveModuleRegistry().register_module(self)

        # Project configuration
        self.project_root = project_root or Path.cwd()
        self.test_output_dir = self.project_root / "tests" / "generated"

        # Ensure output directory exists
        self.test_output_dir.mkdir(parents=True, exist_ok=True)

        # RM Compliance: Initialize extractors with validation
        self.extractors = {
            "class": ClassModelExtractor,
            "function": FunctionModelExtractor,
            "module": ModuleModelExtractor,
        }

        # RM Compliance: Initialize TypeExtractor for explicit model generation
        self.type_extractor = TypeExtractor()

        # RM Compliance: Initialize test generators with validation
        self.test_generators = {
            "class": ClassTestModelGenerator,
            "function": FunctionTestModelGenerator,
        }

        # RM Compliance: Track generation metrics
        self.generation_metrics = {"total_files_processed": 0, "successful_generations": 0, "failed_generations": 0, "broken_tests_detected": 0, "tests_fixed": 0}

    @rm_enhance
    def get_rm_health(self) -> Dict[str, Any]:
        """RM Compliance: Get comprehensive health status"""
        health_report = self.health_monitor.get_health_report()

        return {
            "module_type": "test_generation",
            "health_status": health_report["status"],
            "generation_metrics": self.generation_metrics,
            "health_details": health_report,
            "rm_compliance": {"self_monitoring": True, "self_correction": True, "interface_constraints": True, "health_monitoring": True},
        }

    def get_rm_capabilities(self) -> List[str]:
        """RM Compliance: Get module capabilities"""
        return ["test_generation", "artifact_extraction", "test_validation", "self_monitoring", "self_correction"]

    def get_rm_interface(self) -> Dict[str, Any]:
        """RM Compliance: Get module interface"""
        return {
            "public_methods": ["generate_tests_for_file", "generate_tests_from_project_model", "validate_generated_tests", "fix_broken_tests"],
            "configuration": {"project_root": str(self.project_root), "test_output_dir": str(self.test_output_dir), "supported_artifact_types": list(self.extractors.keys())},
        }

    async def get_module_status(self):
        """RM Compliance: Get current module status"""
        from src.reflective_modules.health import ModuleHealth

        return ModuleHealth(status="healthy" if self.health_monitor.health_status == "healthy" else "degraded", capabilities=self.get_rm_capabilities(), health_indicators=self.get_rm_health())

    async def get_module_capabilities(self):
        """RM Compliance: Get module capabilities"""
        from src.reflective_modules.health import ModuleCapability

        return [ModuleCapability(name=cap, available=True, dependencies=[]) for cap in self.get_rm_capabilities()]

    async def is_healthy(self) -> bool:
        """RM Compliance: Check if module is healthy"""
        return self.health_monitor.health_status == "healthy"

    async def get_health_indicators(self) -> Dict[str, Any]:
        """RM Compliance: Get detailed health indicators"""
        return self.get_rm_health()

    def generate_tests_for_file(self, source_file: Path, artifact_types: Optional[List[str]] = None) -> List[Path]:
        """RM Compliance: Generate tests for a specific file with validation"""
        if not source_file.exists():
            logger.error(f"Source file does not exist: {source_file}")
            self.health_monitor.record_generation_failure()
            return []

        if artifact_types is None:
            artifact_types = ["class", "function", "module"]

        generated_files = []
        self.generation_metrics["total_files_processed"] += 1

        try:
            for artifact_type in artifact_types:
                if artifact_type in self.extractors:
                    extractor_class = self.extractors[artifact_type]
                    extractor = extractor_class(source_file)

                    # RM Compliance: Validate extraction
                    if not extractor.validate_extraction():
                        logger.warning(f"Extraction validation failed for {artifact_type} in {source_file}")
                        self.health_monitor.record_generation_failure()
                        continue

                    try:
                        models = extractor.extract_models()
                        for model in models:
                            # RM Compliance: Validate artifact model
                            if not model.validate():
                                logger.warning(f"Artifact model validation failed: {model.validation_errors}")
                                continue

                            test_file = self._generate_test_for_model(model)
                            if test_file:
                                generated_files.append(test_file)
                                self.generation_metrics["successful_generations"] += 1

                                # RM Compliance: Validate generated test
                                if self._validate_generated_test(test_file):
                                    self.health_monitor.record_successful_test()
                                else:
                                    self.health_monitor.record_broken_test()
                                    self.generation_metrics["broken_tests_detected"] += 1

                    except Exception as e:
                        logger.error(f"Failed to extract {artifact_type} models from {source_file}: {e}")
                        self.health_monitor.record_generation_failure()
                        self.generation_metrics["failed_generations"] += 1

        except Exception as e:
            logger.error(f"Error generating tests for {source_file}: {e}")
            self.health_monitor.record_generation_failure()
            self.generation_metrics["failed_generations"] += 1

        return generated_files

    def _generate_test_for_model(self, model: ArtifactModel) -> Optional[Path]:
        """RM Compliance: Generate test for a specific artifact model with validation"""
        try:
            # Validate that the model has valid data before generating tests
            if not model.name or not model.artifact_type:
                logger.warning(f"Skipping invalid model: {model}")
                return None

            # Check if the source file actually exists and contains the artifact
            if not model.source_file or not model.source_file.exists():
                logger.warning(f"Skipping model with non-existent source file: {model.name}")
                return None

            # Generate test model
            if model.artifact_type in self.test_generators:
                generator_class = self.test_generators[model.artifact_type]
                test_generator = generator_class(model)

                # RM Compliance: Validate test model generation
                if not test_generator.validate_generation():
                    logger.warning(f"Test model generation validation failed: {test_generator.generation_errors}")
                    return None

                test_model = test_generator.generate_test_model()

                # Generate test code
                code_generator = PytestCodeGenerator(test_model, model.artifact_type, model)

                # RM Compliance: Validate test model before code generation
                if not code_generator.validate_test_model():
                    logger.warning(f"Test model validation failed: {code_generator.generation_errors}")
                    return None

                test_code = code_generator.generate_test_code()

                # Write test file
                test_file = self.test_output_dir / f"test_{model.name.lower()}_{model.artifact_type}_generated.py"
                test_file.write_text(test_code)

                return test_file

        except Exception as e:
            logger.error(f"Failed to generate test for {model.name}: {e}")
            self.health_monitor.record_generation_failure()

        return None

    def _validate_generated_test(self, test_file: Path) -> bool:
        """RM Compliance: Validate generated test file"""
        try:
            # Check if file exists and has content
            if not test_file.exists() or test_file.stat().st_size == 0:
                return False

            # Check Python syntax
            with open(test_file, "r") as f:
                source_code = f.read()

            ast.parse(source_code)

            # Check for basic test structure
            if "import pytest" not in source_code:
                return False

            if "class Test" not in source_code:
                return False

            if "def test_" not in source_code:
                return False

            return True

        except Exception as e:
            logger.warning(f"Test validation failed for {test_file}: {e}")
            return False

    def fix_broken_tests(self) -> int:
        """RM Compliance: Self-correction - fix broken generated tests"""
        fixed_count = 0

        try:
            for test_file in self.test_output_dir.glob("test_*_generated.py"):
                if not self._validate_generated_test(test_file):
                    logger.info(f"Attempting to fix broken test: {test_file}")

                    # Try to regenerate the test by finding the source file
                    source_file = self._find_source_file_for_test(test_file)
                    if source_file:
                        # Delete broken test and regenerate
                        test_file.unlink()
                        fixed_files = self.generate_tests_for_file(source_file)
                        if fixed_files:
                            fixed_count += 1
                            self.generation_metrics["tests_fixed"] += 1

        except Exception as e:
            logger.error(f"Error fixing broken tests: {e}")

        return fixed_count

    def _find_source_file_for_test(self, test_file: Path) -> Optional[Path]:
        """Find the source file that corresponds to a generated test"""
        try:
            # Extract artifact info from test filename
            # test_ghostbustersorchestrator_class_generated.py -> ghostbustersorchestrator
            test_name = test_file.stem.replace("test_", "").replace("_generated", "")

            # Look for source files in common locations
            search_paths = [self.project_root / "src", self.project_root / "scripts", self.project_root]

            for search_path in search_paths:
                if search_path.exists():
                    for source_file in search_path.rglob("*.py"):
                        if test_name.lower() in source_file.stem.lower():
                            return source_file

        except Exception as e:
            logger.warning(f"Error finding source file for {test_file}: {e}")

        return None

    def validate_generated_tests(self) -> Dict[str, Any]:
        """RM Compliance: Comprehensive validation of all generated tests"""
        validation_results = {"total_tests": 0, "valid_tests": 0, "broken_tests": 0, "fixable_tests": 0, "unfixable_tests": 0, "validation_errors": []}

        try:
            for test_file in self.test_output_dir.glob("test_*_generated.py"):
                validation_results["total_tests"] += 1

                if self._validate_generated_test(test_file):
                    validation_results["valid_tests"] += 1
                else:
                    validation_results["broken_tests"] += 1

                    # Check if test can be fixed
                    source_file = self._find_source_file_for_test(test_file)
                    if source_file:
                        validation_results["fixable_tests"] += 1
                    else:
                        validation_results["unfixable_tests"] += 1

        except Exception as e:
            validation_results["validation_errors"].append(str(e))

        return validation_results

    def generate_tests_from_project_model(self) -> List[Path]:
        """RM Compliance: Generate tests for all artifacts defined in project model with validation"""
        # Safety check: prevent automatic generation in CI/CD or testing environments
        if AUTO_GENERATION_DISABLED:
            logger.info("Test generation disabled by DISABLE_TEST_GENERATION environment variable")
            return []

        generated_files = []

        try:
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
                                        test_files = self.generate_tests_for_file(source_file)
                                        generated_files.extend(test_files)
                                    except Exception as e:
                                        logger.error(f"Failed to generate tests for {source_file}: {e}")
                                        self.health_monitor.record_generation_failure()

        except Exception as e:
            logger.error(f"Error generating tests from project model: {e}")
            self.health_monitor.record_generation_failure()

        return generated_files

    def cleanup_broken_tests(self) -> int:
        """RM Compliance: Clean up tests that cannot be fixed"""
        cleaned_count = 0

        try:
            for test_file in self.test_output_dir.glob("test_*_generated.py"):
                if not self._validate_generated_test(test_file):
                    source_file = self._find_source_file_for_test(test_file)
                    if not source_file:  # Cannot be fixed
                        logger.info(f"Cleaning up unfixable test: {test_file}")
                        test_file.unlink()
                        cleaned_count += 1

        except Exception as e:
            logger.error(f"Error cleaning up broken tests: {e}")

        return cleaned_count

    @rm_enhance
    def generate_tests_from_type_extractor(self, file_path: Path) -> List[Path]:
        """RM Compliance: Generate tests using explicit models from TypeExtractor"""
        logger.info(f"🎯 Generating tests using TypeExtractor for {file_path}")

        try:
            # Extract explicit type information using TypeExtractor
            type_data = self.type_extractor.extract_types_from_file(str(file_path))

            if not type_data:
                logger.warning(f"⚠️ No type data extracted from {file_path}")
                return []

            # Clean up any existing generated tests first
            self._cleanup_generated_tests()

            # Generate tests from explicit models
            generated_files = []

            # Generate tests for classes
            for class_info in type_data.get("classes", []):
                class_tests = self._generate_class_tests_from_type_model(class_info, file_path)
                if class_tests:
                    generated_files.append(class_tests)

            # Generate tests for functions (only standalone functions, not class methods)
            for func_info in type_data.get("functions", []):
                # Skip functions that are actually class methods
                if not self._is_class_method(func_info, type_data.get("classes", [])):
                    func_tests = self._generate_function_tests_from_type_model(func_info, file_path)
                    if func_tests:
                        generated_files.append(func_tests)

            logger.info(f"✅ Generated {len(generated_files)} test files using TypeExtractor")
            return generated_files

        except Exception as e:
            logger.error(f"❌ Error generating tests with TypeExtractor: {e}")
            return []

    def _generate_class_tests_from_type_model(self, class_info: Any, source_file: Path) -> Optional[Path]:
        """Generate tests for a class using explicit type model"""
        try:
            class_name = class_info.name
            base_classes = getattr(class_info, "base_classes", [])
            methods = getattr(class_info, "methods", [])
            class_variables = getattr(class_info, "class_variables", [])

            # RM Intelligence: Check if this is an abstract base class
            # Check both immediate base classes and MRO for ABC inheritance
            is_abstract = "ABC" in base_classes

            # Also check if any base class name contains "ABC" (for cases like LanguageParser)
            if not is_abstract:
                for base in base_classes:
                    if "ABC" in base or "abstract" in base.lower():
                        is_abstract = True
                        break

            # RM Intelligence: Check if this class can be instantiated
            # Skip classes that inherit from abstract base classes without proper constructors
            if is_abstract:
                logger.info(f"⏭️ Skipping abstract class: {class_name} - use Ghostbusters for validation instead")
                return None

            # RM Intelligence: Check if this class has a proper constructor
            # Skip classes that only have the default object.__init__
            has_proper_constructor = False
            for method in methods:
                if method.name == "__init__":
                    # Check if it's not just the default object.__init__
                    if hasattr(method, "parameters") and len(method.parameters) > 0:
                        has_proper_constructor = True
                        break

            if not has_proper_constructor:
                logger.info(f"⏭️ Skipping class without proper constructor: {class_name} - can't be instantiated")
                return None

            # Create test model from explicit data
            test_model = {
                "test_class_name": f"Test{class_name}",
                "artifact_name": class_name,
                "test_methods": self._create_test_methods_from_type_model(class_name, methods, class_variables, base_classes),
                "fixtures": self._create_fixtures_from_type_model(class_name, base_classes),
                "test_data": {"setup_required": True, "teardown_required": False, "mock_dependencies": False},
            }

            # Generate test code with source file context
            generator = PytestCodeGenerator(test_model, "class", None)
            generator.source_file_path = Path(source_file)  # Convert to Path object
            test_code = generator.generate_test_code()

            # Write test file
            test_file = self.test_output_dir / f"test_{class_name.lower()}_class_generated.py"
            test_file.write_text(test_code)

            return test_file

        except Exception as e:
            logger.error(f"❌ Error generating class tests: {e}")
            return None

    def _generate_function_tests_from_type_model(self, func_info: Any, source_file: Path) -> Optional[Path]:
        """Generate tests for a function using explicit type model"""
        try:
            func_name = func_info.name
            parameters = getattr(func_info, "parameters", [])
            return_type = getattr(func_info, "return_type", None)
            decorators = getattr(func_info, "decorators", [])

            # RM Intelligence: Check if this is actually a standalone function
            # Skip methods that have 'self' parameter or are private methods
            if any(p.name == "self" for p in parameters) or func_name.startswith("_"):
                logger.info(f"⏭️ Skipping class method: {func_name} - not a standalone function")
                return None

            # RM Intelligence: Skip functions that are likely nested or not importable
            # These functions can't be tested as standalone functions
            if func_name in ["show_rm_status"]:  # Known nested functions
                logger.info(f"⏭️ Skipping nested function: {func_name} - not importable")
                return None

            # Create test model from explicit data
            test_model = {
                "test_class_name": f"Test{func_name.title().replace('_', '')}",
                "artifact_name": func_name,
                "test_methods": self._create_function_test_methods_from_type_model(func_name, parameters, return_type, decorators),
                "fixtures": [],
                "test_data": {"setup_required": False, "teardown_required": False, "mock_dependencies": False},
            }

            # Generate test code with source file context
            generator = PytestCodeGenerator(test_model, "function", None)
            generator.source_file_path = Path(source_file)  # Convert to Path object
            test_code = generator.generate_test_code()

            # Write test code
            test_file = self.test_output_dir / f"test_{func_name.lower()}_function_generated.py"
            test_file.write_text(test_code)

            return test_file

        except Exception as e:
            logger.error(f"❌ Error generating function tests: {e}")
            return None

    def _create_test_methods_from_type_model(self, class_name: str, methods: List[Dict], class_variables: List[Dict], base_classes: List[str]) -> List[Dict[str, Any]]:
        """Create test methods from explicit type model"""
        test_methods = []

        # Test class initialization
        if "ABC" not in base_classes:  # Don't test abstract classes
            test_methods.append({"name": f"test_{class_name.lower()}_initialization", "type": "initialization", "description": f"Test that {class_name} initializes correctly"})

        # Test class variables
        for var in class_variables:
            test_methods.append(
                {
                    "name": f"test_{var.name}_attribute_exists",
                    "type": "attribute",
                    "description": f"Test that {var.name} attribute exists and has correct type",
                    "target_name": var.name,  # Store the actual attribute name
                }
            )

        # Test methods
        for method in methods:
            if method.name != "__init__":
                # Check if this is an abstract method
                is_abstract = hasattr(method, "decorators") and "abstractmethod" in method.decorators

                test_methods.append(
                    {
                        "name": f"test_{method.name}_method_exists",
                        "type": "abstract_method" if is_abstract else "method",
                        "description": f"Test that {method.name} method exists and is {'abstract' if is_abstract else 'callable'}",
                        "target_name": method.name,  # Store the actual method name
                        "is_abstract": is_abstract,
                    }
                )

        return test_methods

    def _create_function_test_methods_from_type_model(self, func_name: str, parameters: List[Dict], return_type: Dict, decorators: List[str]) -> List[Dict[str, Any]]:
        """Create test methods for functions from explicit type model"""
        test_methods = []

        # Test function exists
        test_methods.append({"name": f"test_{func_name}_function_exists", "type": "existence", "description": f"Test that {func_name} function exists and is callable"})

        # Test parameters if function has them
        if parameters and len(parameters) > 1:  # Skip self parameter
            test_methods.append({"name": f"test_{func_name}_parameters", "type": "parameters", "description": f"Test that {func_name} has correct parameters"})

        return test_methods

    def _create_fixtures_from_type_model(self, class_name: str, base_classes: List[str]) -> List[Dict[str, Any]]:
        """Create fixtures from explicit type model"""
        fixtures = []

        # Skip abstract classes entirely - they can't be tested directly
        if "ABC" not in base_classes:
            fixtures.append({"name": class_name.lower(), "type": "instance", "description": f"Get a fresh {class_name} instance", "defaults": self._get_pydantic_defaults(class_name)})

        return fixtures

    @rm_enhance
    def _get_pydantic_defaults(self, class_name: str) -> Dict[str, Any]:
        """Get sensible defaults for Pydantic models and dataclasses"""
        logger.debug(f"🔍 Starting _get_pydantic_defaults for class: {class_name}")
        defaults = {}

        try:
            # Try to import the class from the module where it's defined
            import importlib
            import inspect

            # Try common module paths
            module_paths = ["src.ghostbusters.agents.base_expert", "src.ast_analysis.core.type_extractor", "src.ast_analysis.core.ast_parser", "src.ast_analysis.api.ast_api"]

            logger.debug(f"🔍 Searching for {class_name} in {len(module_paths)} module paths")

            class_obj = None
            for module_path in module_paths:
                try:
                    logger.debug(f"🔍 Trying module: {module_path}")
                    module = importlib.import_module(module_path)
                    class_obj = getattr(module, class_name, None)
                    if class_obj:
                        logger.info(f"✅ Found {class_name} in {module_path}")
                        break
                    else:
                        logger.debug(f"🔍 {class_name} not found in {module_path}")
                except ImportError as e:
                    logger.debug(f"🔍 Import error for {module_path}: {e}")
                    continue

            if class_obj:
                print(f"🔍 Analyzing {class_name}:")
                print(f"  - Has model_fields: {hasattr(class_obj, 'model_fields')}")
                print(f"  - Has __dataclass_fields__: {hasattr(class_obj, '__dataclass_fields__')}")
                print(f"  - Has __init__: {hasattr(class_obj, '__init__')}")

                # Check if it's a Pydantic model
                if hasattr(class_obj, "model_fields"):
                    print(f"  - Processing as Pydantic model")
                    for field_name, field_info in class_obj.model_fields.items():
                        if field_info.is_required:
                            defaults[field_name] = self._get_default_value(field_info.annotation, field_name)

                # Check if it's a dataclass
                elif hasattr(class_obj, "__dataclass_fields__"):
                    print(f"  - Processing as dataclass")
                    print(f"  - Fields: {list(class_obj.__dataclass_fields__.keys())}")
                    import dataclasses

                    for field_name, field_info in class_obj.__dataclass_fields__.items():
                        print(f"    - {field_name}: default={field_info.default}, type={field_info.type}")
                        if field_info.default == dataclasses.MISSING:  # Required field
                            print(f"      -> Required field, adding default")
                            try:
                                default_value = self._get_default_value(field_info.type, field_name)
                                print(f"      -> Setting {field_name} = {default_value}")
                                defaults[field_name] = default_value
                            except Exception as e:
                                print(f"      -> ERROR getting default for {field_name}: {e}")
                                defaults[field_name] = f"test_{field_name}"

                # Check if it has __init__ with required parameters
                elif hasattr(class_obj, "__init__"):
                    print(f"  - Processing as __init__ class")
                    sig = inspect.signature(class_obj.__init__)
                    for param_name, param in sig.parameters.items():
                        if param_name != "self" and param.default == inspect._empty:
                            defaults[param_name] = self._get_default_value(param.annotation, param_name)

        except Exception as e:
            # If we can't determine defaults, that's okay
            pass

        return defaults

    def _get_default_value(self, annotation: Any, field_name: str) -> Any:
        """Get sensible default value based on type annotation"""
        print(f"    🔍 Getting default for {field_name}: {annotation}")

        # Handle None annotation
        if annotation is None or annotation == inspect._empty:
            print(f"      -> None/empty annotation, using test_{field_name}")
            return f"test_{field_name}"

        # Handle string types
        if annotation == str:
            print(f"      -> String type, using test_{field_name}")
            return f"test_{field_name}"

        # Handle numeric types
        elif annotation == float:
            print(f"      -> Float type, using 0.5")
            return 0.5
        elif annotation == int:
            print(f"      -> Int type, using 1")
            return 1
        elif annotation == bool:
            print(f"      -> Bool type, using False")
            return False

        # Handle list types
        elif hasattr(annotation, "__origin__") and annotation.__origin__ == list:
            print(f"      -> List type, using []")
            return []

        # Handle dict types
        elif hasattr(annotation, "__origin__") and annotation.__origin__ == dict:
            print(f"      -> Dict type, using {{}}")
            return {}

        # Handle Union types (including Optional)
        elif hasattr(annotation, "__origin__") and annotation.__origin__ == type(Union):
            print(f"      -> Union type, processing...")
            # For Optional types, use None
            if type(None) in annotation.__args__:
                return None
            # For other unions, use first non-None type
            for arg in annotation.__args__:
                if arg != type(None):
                    return self._get_default_value(arg, field_name)
            return None

        # Default fallback
        else:
            print(f"      -> Unknown type, using test_{field_name}")
            return f"test_{field_name}"

        print(f"      -> ERROR: Method should not reach here!")
        return f"test_{field_name}"  # Safety fallback

    def _cleanup_generated_tests(self):
        """Clean up existing generated tests without requiring approval"""
        try:
            for test_file in self.test_output_dir.glob("test_*_generated.py"):
                test_file.unlink()
                logger.info(f"🧹 Cleaned up existing test: {test_file.name}")
        except Exception as e:
            logger.warning(f"⚠️ Error during cleanup: {e}")

    def _is_class_method(self, func_info: Any, classes: List[Any]) -> bool:
        """Check if a function is actually a class method"""
        # Check decorators - if it has classmethod, field_validator, or abstractmethod, it's a class method
        decorators = getattr(func_info, "decorators", [])
        if any(decorator in ["classmethod", "field_validator", "abstractmethod"] for decorator in decorators):
            return True

        # Also check if this function name appears in any class's methods
        func_name = func_info.name
        for class_info in classes:
            for method in getattr(class_info, "methods", []):
                if method.name == func_name:
                    return True

        return False


if __name__ == "__main__":
    # Example usage - only run when explicitly executed
    logger.info("Test generator main function - use for development only")
    logger.info("To generate tests, import and use PythonUnitTestGenerator class directly")

    # RM Compliance: Demonstrate health monitoring
    generator = PythonUnitTestGenerator()
    health = generator.get_rm_health()
    logger.info(f"Generator health: {health['health_status']}")

    # Uncomment the following lines only when you want to generate tests
    # project_root = Path()
    # test_generator = PythonUnitTestGenerator(project_root)
    #
    # # Generate tests for specific file
    # source_file = Path("src/ghostbusters/ghostbusters_orchestrator.py")
    # if source_file.exists():
    #     test_files = test_generator.generate_tests_for_file(source_file, ["class"])
    #     logger.info(f"Generated {len(test_files)} test files")
    # else:
    #     logger.info(f"Source file not found: {source_file}")
    #
    # # Generate tests from project model
    # generated_files = test_generator.generate_tests_from_project_model()
    # logger.info(f"Generated {len(generated_files)} total test files")
