#!/usr/bin/env python3
"""
Clean, Focused Test Generator - RM Compliant

This module generates unit tests using the TypeExtractor and follows RM principles:
- Single responsibility: Generate tests from type models
- Self-monitoring: Track generation success/failure
- Interface constraints: Clear, simple API
- Health monitoring: Report system status
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.reflective_modules.registry import ReflectiveModule
from src.ast_analysis.core.type_extractor import TypeExtractor
from src.model_driven_testing.rm_enhancer import rm_enhance
from src.model_driven_testing.test_health import TestGenerationHealth


class TestGenerator(ReflectiveModule):
    """Clean, focused test generator following RM principles"""

    __test__ = False  # Tell pytest: DO NOT COLLECT THIS CLASS!

    def __init__(self, test_output_dir: str = "tests/generated"):
        super().__init__()
        self.test_output_dir = Path(test_output_dir)
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        self.type_extractor = TypeExtractor()
        self.health_monitor = TestGenerationHealth()

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def create_for_testing(cls, test_output_dir: str = "tests/generated"):
        """Factory method for pytest compatibility - no constructor issues"""
        return cls(test_output_dir)

    @rm_enhance
    def generate_tests_from_file(self, file_path: str) -> List[Path]:
        """Generate tests for a single file"""
        try:
            self.logger.info(f"🎯 Generating tests for {file_path}")

            # Extract type information
            type_data = self.type_extractor.extract_types_from_file(file_path)
            if not type_data:
                self.logger.warning(f"⚠️ No type data extracted from {file_path}")
                return []

            # Generate tests for classes and functions
            generated_files = []

            # Generate class tests
            for class_info in type_data.get("classes", []):
                if self._can_test_class(class_info):
                    test_file = self._generate_class_tests(class_info, file_path)
                    if test_file:
                        generated_files.append(test_file)

            # Generate function tests
            for func_info in type_data.get("functions", []):
                if self._can_test_function(func_info):
                    test_file = self._generate_function_tests(func_info, file_path)
                    if test_file:
                        generated_files.append(test_file)

            self.logger.info(f"✅ Generated {len(generated_files)} test files")
            self.health_monitor.record_success(len(generated_files))
            return generated_files

        except Exception as e:
            self.logger.error(f"❌ Error generating tests: {e}")
            self.health_monitor.record_failure()
            return []

    def _can_test_class(self, class_info) -> bool:
        """Check if a class can be tested"""
        # Handle both object and dict formats
        if hasattr(class_info, "base_classes"):
            base_classes = getattr(class_info, "base_classes", [])
            class_name = getattr(class_info, "name", "unknown")
            methods = getattr(class_info, "methods", [])
        else:
            base_classes = class_info.get("base_classes", [])
            class_name = class_info.get("name", "unknown")
            methods = class_info.get("methods", [])

        # Skip abstract classes
        if "ABC" in base_classes:
            self.logger.info(f"⏭️ Skipping abstract class: {class_name}")
            return False

        # Skip classes without proper constructors
        has_constructor = any(m.get("name") == "__init__" if isinstance(m, dict) else m.name == "__init__" for m in methods)

        if not has_constructor:
            self.logger.info(f"⏭️ Skipping class without constructor: {class_name}")
            return False

        return True

    def _can_test_function(self, func_info) -> bool:
        """Check if a function can be tested"""
        # Handle both object and dict formats
        if hasattr(func_info, "name"):
            func_name = func_info.name
            parameters = getattr(func_info, "parameters", [])
        else:
            func_name = func_info.get("name", "unknown")
            parameters = func_info.get("parameters", [])

        # Skip class methods
        if any(p.get("name") == "self" if isinstance(p, dict) else p.name == "self" for p in parameters):
            self.logger.info(f"⏭️ Skipping class method: {func_name}")
            return False

        # Skip private functions
        if func_name.startswith("_"):
            self.logger.info(f"⏭️ Skipping private function: {func_name}")
            return False

        # RM Intelligence: Skip known nested functions that can't be imported
        nested_functions = ["show_rm_status"]  # Functions defined inside other functions
        if func_name in nested_functions:
            self.logger.info(f"⏭️ Skipping nested function: {func_name} - not importable")
            return False

        return True

    def _generate_class_tests(self, class_info, source_file: str) -> Optional[Path]:
        """Generate tests for a class"""
        try:
            # Handle both object and dict formats
            if hasattr(class_info, "name"):
                class_name = class_info.name
            else:
                class_name = class_info.get("name", "unknown")

            test_file = self.test_output_dir / f"test_{class_name.lower()}_class_generated.py"

            # Simple test content
            test_content = f'''#!/usr/bin/env python3
"""Generated tests for {class_name}"""

import pytest
from {source_file.replace("/", ".").replace(".py", "")} import {class_name}


class Test{class_name}:
    """Generated tests for {class_name}"""
    
    def test_{class_name.lower()}_initialization(self):
        """Test that {class_name} initializes correctly"""
        instance = {class_name}()
        assert instance is not None
        assert isinstance(instance, {class_name})
'''

            test_file.write_text(test_content)
            self.logger.info(f"✅ Generated class tests: {test_file}")
            return test_file

        except Exception as e:
            self.logger.error(f"❌ Error generating class tests: {e}")
            return None

    def _generate_function_tests(self, func_info, source_file: str) -> Optional[Path]:
        """Generate tests for a function"""
        try:
            # Handle both object and dict formats
            if hasattr(func_info, "name"):
                func_name = func_info.name
            else:
                func_name = func_info.get("name", "unknown")

            test_file = self.test_output_dir / f"test_{func_name.lower()}_function_generated.py"

            # Simple test content
            test_content = f'''#!/usr/bin/env python3
"""Generated tests for {func_name}"""

import pytest
from {source_file.replace("/", ".").replace(".py", "")} import {func_name}


class Test{func_name.title()}:
    """Generated tests for {func_name}"""
    
    def test_{func_name.lower()}_function_exists(self):
        """Test that {func_name} function exists"""
        assert {func_name} is not None
        assert callable({func_name})
'''

            test_file.write_text(test_content)
            self.logger.info(f"✅ Generated function tests: {test_file}")
            return test_file

        except Exception as e:
            self.logger.error(f"❌ Error generating function tests: {e}")
            return None

    def get_rm_health(self) -> dict:
        """RM Compliance: Report system health"""
        return {
            "status": "healthy",
            "module": "TestGenerator",
            "health_indicators": self.health_monitor.get_health_indicators(),
            "test_output_dir": str(self.test_output_dir),
            "type_extractor_available": self.type_extractor is not None,
        }

    def get_rm_capabilities(self) -> List[str]:
        """RM Compliance: Report system capabilities"""
        return ["generate_tests_from_file", "type_extraction", "class_test_generation", "function_test_generation", "health_monitoring"]

    def get_health_indicators(self) -> Dict[str, Any]:
        """RM Compliance: Get health indicators"""
        return self.health_monitor.get_health_indicators()

    def get_module_capabilities(self) -> List[str]:
        """RM Compliance: Get module capabilities"""
        return self.get_rm_capabilities()

    def get_module_status(self) -> str:
        """RM Compliance: Get module status"""
        return self.health_monitor.get_health_indicators()["status"]

    def is_healthy(self) -> bool:
        """RM Compliance: Check if module is healthy"""
        return self.health_monitor.get_health_indicators()["status"] == "healthy"
