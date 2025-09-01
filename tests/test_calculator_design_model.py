#!/usr/bin/env python3
"""
Test Calculator Design Model Usage

This test validates that the calculator design model can be used for round-trip engineering.
It tests the complete workflow from design model to generated code and back.
"""

import json
from pathlib import Path

import pytest


class TestCalculatorDesignModel:
    """Test the calculator design model and round-trip functionality"""

    @pytest.fixture
    def calculator_design_spec(self):
        """Load the calculator design specification"""
        design_spec_path = Path("calculator_design_spec.json")
        assert design_spec_path.exists(), "Calculator design spec not found"

        with open(design_spec_path) as f:
            return json.load(f)

    @pytest.fixture
    def simple_calculator_file(self):
        """Get the simple calculator file path"""
        calculator_path = Path("scripts/simple_calculator.py")
        assert calculator_path.exists(), "Simple calculator file not found"
        return calculator_path

    def test_design_spec_structure(self, calculator_design_spec):
        """Test that the design spec has the correct structure"""
        # Check top-level structure
        assert "name" in calculator_design_spec
        assert "description" in calculator_design_spec
        assert "components" in calculator_design_spec

        # Check name and description
        assert calculator_design_spec["name"] == "simple_calculator"
        assert "calculator system" in calculator_design_spec["description"].lower()

        # Check components
        components = calculator_design_spec["components"]
        assert len(components) == 3  # Calculator, CalculatorUI, main

        # Check component names
        component_names = [comp["name"] for comp in components]
        assert "Calculator" in component_names
        assert "CalculatorUI" in component_names
        assert "main" in component_names

    def test_calculator_component(self, calculator_design_spec):
        """Test the Calculator component specification"""
        calculator_comp = None
        for comp in calculator_design_spec["components"]:
            if comp["name"] == "Calculator":
                calculator_comp = comp
                break

        assert calculator_comp is not None, "Calculator component not found"

        # Check component structure
        assert calculator_comp["type"] == "class"
        assert "mathematical operations" in calculator_comp["description"].lower()

        # Check methods
        methods = calculator_comp["metadata"]["methods"]
        expected_methods = [
            "__init__(self) -> None",
            "add(self, a: float, b: float) -> float",
            "subtract(self, a: float, b: float) -> float",
            "multiply(self, a: float, b: float) -> float",
            "divide(self, a: float, b: float) -> float",
        ]

        for expected_method in expected_methods:
            assert expected_method in methods, f"Method {expected_method} not found"

    def test_calculator_ui_component(self, calculator_design_spec):
        """Test the CalculatorUI component specification"""
        ui_comp = None
        for comp in calculator_design_spec["components"]:
            if comp["name"] == "CalculatorUI":
                ui_comp = comp
                break

        assert ui_comp is not None, "CalculatorUI component not found"

        # Check component structure
        assert ui_comp["type"] == "class"
        assert "user interface" in ui_comp["description"].lower()

        # Check methods
        methods = ui_comp["metadata"]["methods"]
        for expected_method in [
            "__init__(self) -> None",
            "display_result(self, result: float) -> None",
            "get_user_input(self) -> str",
            "run_calculator(self) -> None",
        ]:
            assert expected_method in methods, f"Method {expected_method} not found"

    def test_main_function_component(self, calculator_design_spec):
        """Test the main function component specification"""
        main_comp = None
        for comp in calculator_design_spec["components"]:
            if comp["name"] == "main":
                main_comp = comp
                break

        assert main_comp is not None, "Main function component not found"

        # Check component structure
        assert main_comp["type"] == "function"
        assert "entry point" in main_comp["description"].lower()

        # Check signature
        signature = main_comp["metadata"]["signature"]
        assert signature == "main() -> None"

    def test_generated_code_structure(self, simple_calculator_file):
        """Test that the generated code has the correct structure"""
        with open(simple_calculator_file) as f:
            content = f.read()

        # Check that classes are defined
        assert "class Calculator:" in content
        assert "class CalculatorUI:" in content

        # Check that methods are defined
        assert "def __init__(self) -> None:" in content
        assert "def add(self, a: float, b: float) -> float:" in content
        assert "def subtract(self, a: float, b: float) -> float:" in content
        assert "def multiply(self, a: float, b: float) -> float:" in content
        assert "def divide(self, a: float, b: float) -> float:" in content

        # Check UI methods
        assert "def display_result(self, result: float) -> None:" in content
        assert "def get_user_input(self) -> str:" in content
        assert "def run_calculator(self) -> None:" in content

        # Check main function
        assert "def main() -> None:" in content

    def test_generated_code_parses(self, simple_calculator_file):
        """Test that the generated code can be parsed by Python"""
        import ast

        with open(simple_calculator_file) as f:
            content = f.read()

        # Should parse without syntax errors
        tree = ast.parse(content)
        assert tree is not None

        # Check for classes
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert len(classes) == 2  # Calculator and CalculatorUI

        # Check for functions
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        assert len(functions) >= 8  # 6 methods + main + any other functions

    def test_design_model_round_trip(self, calculator_design_spec, simple_calculator_file):
        """Test that the design model can be used for round-trip engineering"""
        # This test validates that the design model can be used to generate code
        # and that the generated code can be reverse engineered back to a model

        # Load the round-trip model system
        try:
            from src.round_trip_engineering import RoundTripModelSystem

            _ = RoundTripModelSystem()  # Test instantiation
        except ImportError:
            pytest.skip("RoundTripModelSystem not available")

        # Load the enhanced reverse engineer
        try:
            from enhanced_reverse_engineer_fixed_v2 import EnhancedReverseEngineer

            reverse_engineer = EnhancedReverseEngineer()
        except ImportError:
            pytest.skip("EnhancedReverseEngineer not available")

        # Step 1: Reverse engineer the generated code
        generated_model = reverse_engineer.reverse_engineer_file(str(simple_calculator_file))
        assert generated_model is not None

        # Step 2: Check that the reverse engineered model has the expected components
        components = generated_model.get("components", {})
        assert "Calculator" in components
        assert "CalculatorUI" in components

        # Step 3: Check that the methods are preserved
        calculator_methods = components["Calculator"].get("methods", [])
        method_names = [method["name"] for method in calculator_methods]

        expected_methods = ["__init__", "add", "subtract", "multiply", "divide"]
        for expected_method in expected_methods:
            assert expected_method in method_names, f"Method {expected_method} not found in reverse engineered model"

    def test_design_model_validation(self, calculator_design_spec):
        """Test that the design model follows proper validation rules"""
        # Check that all components have required fields
        for comp in calculator_design_spec["components"]:
            required_fields = [
                "name",
                "type",
                "description",
                "requirements",
                "metadata",
            ]
            for field in required_fields:
                assert field in comp, f"Component {comp['name']} missing required field: {field}"

            # Check metadata structure
            metadata = comp["metadata"]
            if comp["type"] == "class":
                assert "methods" in metadata
                assert isinstance(metadata["methods"], list)
            elif comp["type"] == "function":
                assert "signature" in metadata
                assert "return_type" in metadata

    def test_design_model_consistency(self, calculator_design_spec):
        """Test that the design model is internally consistent"""
        # Check that component names are unique
        component_names = [comp["name"] for comp in calculator_design_spec["components"]]
        assert len(component_names) == len(set(component_names)), "Duplicate component names found"

        # Check that dependencies are valid (if any)
        for comp in calculator_design_spec["components"]:
            dependencies = comp.get("dependencies", [])
            for dep in dependencies:
                assert dep in component_names, f"Dependency {dep} not found in components"


if __name__ == "__main__":
    pytest.main([__file__])
