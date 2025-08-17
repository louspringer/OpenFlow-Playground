#!/usr/bin/env python3
"""
Abstract Factory System for Model-Driven Development

Purpose: Eliminate context confusion by providing the right tool for the right job
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import Any

# Add root to path for accessing root-level tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ReverseEngineeringTool(ABC):
    """Abstract base for reverse engineering tools"""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this tool can handle the given file"""

    @abstractmethod
    def reverse_engineer(self, file_path: str) -> dict[str, Any]:
        """Extract model from source code"""


class CodeGenerationTool(ABC):
    """Abstract base for code generation tools"""

    @abstractmethod
    def can_handle(self, model: dict[str, Any]) -> bool:
        """Check if this tool can handle the given model"""

    @abstractmethod
    def generate_code(self, model: dict[str, Any]) -> str:
        """Generate code from model"""


class LintingTool(ABC):
    """Abstract base for linting tools"""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this tool can handle the given file"""

    @abstractmethod
    def lint(self, file_path: str) -> list[dict[str, Any]]:
        """Lint the given file"""


class ParsingTool(ABC):
    """Abstract base for parsing tools"""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this tool can handle the given file"""

    @abstractmethod
    def parse(self, file_path: str) -> Any:
        """Parse the given file"""


# Concrete Implementations


class EnhancedReverseEngineer(ReverseEngineeringTool):
    """Enhanced reverse engineer for Python files"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(".py")

    def reverse_engineer(self, file_path: str) -> dict[str, Any]:
        """Use the root enhanced_reverse_engineer.py"""
        try:
            from enhanced_reverse_engineer import (
                EnhancedReverseEngineer as RootEngineer,
            )

            engineer = RootEngineer()
            return engineer.reverse_engineer(file_path)
        except ImportError as e:
            raise ImportError(f"Enhanced reverse engineer not available: {e}")


class RoundTripCodeGenerator(CodeGenerationTool):
    """Round-trip code generator for extracted models"""

    def can_handle(self, model: dict[str, Any]) -> bool:
        # Check if this is an extracted model (not a design spec)
        return (
            "components" in model
            and "module_functions" in model
            and "file_structure" in model
        )

    def generate_code(self, model: dict[str, Any]) -> str:
        """Use the root round_trip_model_system.py with generate_code_from_extracted_model"""
        try:
            from .round_trip_engineering import RoundTripModelSystem

            system = RoundTripModelSystem()
            return system.generate_code_from_extracted_model(model)
        except ImportError as e:
            raise ImportError(f"Round-trip model system not available: {e}")


class DesignSpecCodeGenerator(CodeGenerationTool):
    """Design spec code generator for new class structures"""

    def can_handle(self, model: dict[str, Any]) -> bool:
        # Check if this is a design spec (not an extracted model)
        return (
            "system_name" in model
            and "components" in model
            and "file_structure" not in model
        )

    def generate_code(self, model: dict[str, Any]) -> str:
        """Use the src round_trip_model_system.py for design specs"""
        try:
            from src.round_trip_model_system import RoundTripModelSystem

            system = RoundTripModelSystem()
            # Convert model to design spec format if needed
            return system.generate_code_from_model(model["system_name"])
        except ImportError as e:
            raise ImportError(f"Design spec generator not available: {e}")


class PythonLinter(LintingTool):
    """Python linting tool"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(".py")

    def lint(self, file_path: str) -> list[dict[str, Any]]:
        """Use flake8 for Python linting"""
        try:
            import subprocess

            result = subprocess.run(
                ["flake8", file_path, "--format=json"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return []
            # Parse flake8 JSON output
            import json

            return json.loads(result.stdout)
        except Exception as e:
            return [{"error": f"Linting failed: {e}"}]


class YAMLLinter(LintingTool):
    """YAML linting tool"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith((".yml", ".yaml"))

    def lint(self, file_path: str) -> list[dict[str, Any]]:
        """Use yamllint for YAML files"""
        try:
            import subprocess

            result = subprocess.run(
                ["yamllint", file_path, "--format=json"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return []
            # Parse yamllint output
            return [{"error": result.stderr}]
        except Exception as e:
            return [{"error": f"YAML linting failed: {e}"}]


class MDCLinter(LintingTool):
    """MDC file linting tool (special YAML format)"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(".mdc")

    def lint(self, file_path: str) -> list[dict[str, Any]]:
        """Use specialized MDC parser for .mdc files"""
        try:
            # MDC files have special comma-separated globs format
            # Use specialized validation
            from src.mdc_parser import MDCParser

            parser = MDCParser()
            yaml_data, markdown_content = parser.parse_mdc(file_path)
            # Basic validation - check if it parses without errors
            return []
        except Exception as e:
            return [{"error": f"MDC parsing failed: {e}"}]


class PythonParser(ParsingTool):
    """Python AST parser"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(".py")

    def parse(self, file_path: str) -> Any:
        """Use Python AST parser"""
        try:
            import ast

            with open(file_path) as f:
                content = f.read()
            return ast.parse(content)
        except Exception as e:
            raise SyntaxError(f"Python parsing failed: {e}")


class YAMLParser(ParsingTool):
    """YAML parser"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith((".yml", ".yaml"))

    def parse(self, file_path: str) -> Any:
        """Use ruamel.yaml for YAML files"""
        try:
            from ruamel.yaml import YAML

            yaml = YAML()
            with open(file_path) as f:
                return yaml.load(f)
        except Exception as e:
            raise SyntaxError(f"YAML parsing failed: {e}")


class MDCParser(ParsingTool):
    """MDC file parser (special YAML format)"""

    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(".mdc")

    def parse(self, file_path: str) -> Any:
        """Use specialized MDC parser"""
        try:
            from src.mdc_parser import MDCParser

            parser = MDCParser()
            yaml_data, markdown_content = parser.parse_mdc(file_path)
            return {"yaml": yaml_data, "markdown": markdown_content}
        except Exception as e:
            raise SyntaxError(f"MDC parsing failed: {e}")


# Abstract Factory


class ModelDrivenFactory:
    """Abstract factory for model-driven development tools"""

    def __init__(self):
        # Initialize all available tools
        self.reverse_engineering_tools = [
            EnhancedReverseEngineer(),
        ]

        self.code_generation_tools = [
            RoundTripCodeGenerator(),
            DesignSpecCodeGenerator(),
        ]

        self.linting_tools = [
            PythonLinter(),
            YAMLLinter(),
            MDCLinter(),
        ]

        self.parsing_tools = [
            PythonParser(),
            YAMLParser(),
            MDCParser(),
        ]

    def get_reverse_engineering_tool(self, file_path: str) -> ReverseEngineeringTool:
        """Get the appropriate reverse engineering tool for the file"""
        for tool in self.reverse_engineering_tools:
            if tool.can_handle(file_path):
                return tool
        raise ValueError("No reverse engineering tool available for " + file_path)

    def get_code_generation_tool(self, model: dict[str, Any]) -> CodeGenerationTool:
        """Get the appropriate code generation tool for the model"""
        for tool in self.code_generation_tools:
            if tool.can_handle(model):
                return tool
        raise ValueError("No code generation tool available for this model type")

    def get_linting_tool(self, file_path: str) -> LintingTool:
        """Get the appropriate linting tool for the file"""
        for tool in self.linting_tools:
            if tool.can_handle(file_path):
                return tool
        raise ValueError("No linting tool available for " + file_path)

    def get_parsing_tool(self, file_path: str) -> ParsingTool:
        """Get the appropriate parsing tool for the file"""
        for tool in self.parsing_tools:
            if tool.can_handle(file_path):
                return tool
        raise ValueError("No parsing tool available for " + file_path)


# Convenience Functions


def reverse_engineer_file(file_path: str) -> dict[str, Any]:
    """Convenience function to reverse engineer any file"""
    factory = ModelDrivenFactory()
    tool = factory.get_reverse_engineering_tool(file_path)
    return tool.reverse_engineer(file_path)


def generate_code_from_model(model: dict[str, Any]) -> str:
    """Convenience function to generate code from any model"""
    factory = ModelDrivenFactory()
    tool = factory.get_code_generation_tool(model)
    return tool.generate_code(model)


def lint_file(file_path: str) -> list[dict[str, Any]]:
    """Convenience function to lint any file"""
    factory = ModelDrivenFactory()
    tool = factory.get_linting_tool(file_path)
    return tool.lint(file_path)


def parse_file(file_path: str) -> Any:
    """Convenience function to parse any file"""
    factory = ModelDrivenFactory()
    tool = factory.get_parsing_tool(file_path)
    return tool.parse(file_path)


# Main function for testing
def main():
    """Test the abstract factory system"""
    print("🏭 Testing Abstract Factory System")
    print("=" * 50)

    factory = ModelDrivenFactory()

    # Test reverse engineering
    print("\n🔍 Testing Reverse Engineering Tools:")
    test_file = "scripts/simple_calculator.py"
    if os.path.exists(test_file):
        try:
            tool = factory.get_reverse_engineering_tool(test_file)
            print("✅ Found tool: " + tool.__class__.__name__)
            model = tool.reverse_engineer(test_file)
            print(f"✅ Model extracted: {len(model.get('components', {}))} components")
        except Exception as e:
            print(f"❌ Reverse engineering failed: {e}")

    # Test code generation
    print("\n🔧 Testing Code Generation Tools:")
    try:
        # Create a simple test model
        test_model = {
            "components": {"TestClass": {"methods": []}},
            "module_functions": [],
            "file_structure": {"total_lines": 10},
        }
        tool = factory.get_code_generation_tool(test_model)
        print("✅ Found tool: " + tool.__class__.__name__)
    except Exception as e:
        print(f"❌ Code generation tool selection failed: {e}")

    print("\n🎯 Abstract Factory System Ready!")


if __name__ == "__main__":
    main()
