#!/usr/bin/env python3
"""
Demo Design Specifications

Contains design specification creation methods for the demo orchestrator.
Extracted to maintain the 200-line limit for the main orchestrator.
"""

from typing import Dict, Any, List


class DemoDesignSpecs:
    """Design specification creation utilities for demos."""

    @staticmethod
    def create_basic_design_spec() -> Dict[str, Any]:
        """Create a basic design specification for demo purposes."""
        return {
            "name": "BasicDemoClass",
            "description": "A basic demo class for round-trip engineering",
            "components": [
                {
                    "name": "BasicDemoClass",
                    "type": "class",
                    "description": "A basic demo class for testing",
                    "requirements": ["Must be simple and easy to understand", "Should demonstrate basic functionality"],
                    "dependencies": ["typing", "pathlib"],
                    "metadata": {
                        "methods": [
                            {"name": "__init__", "parameters": [], "return_type": "None", "description": "Initialize the demo class"},
                            {"name": "demo_method", "parameters": [{"name": "value", "type": "str"}], "return_type": "str", "description": "A simple demo method"},
                        ],
                        "attributes": [{"name": "demo_value", "type": "str", "description": "A demo attribute"}],
                    },
                }
            ],
            "relationships": [],
            "constraints": ["Must be simple and easy to understand", "Should demonstrate basic Python class structure"],
        }

    @staticmethod
    def create_advanced_design_spec() -> Dict[str, Any]:
        """Create an advanced design specification for demo purposes."""
        return {
            "name": "AdvancedDemoSystem",
            "description": "An advanced demo system with multiple components",
            "components": [
                {
                    "name": "DataProcessor",
                    "type": "class",
                    "description": "Processes data with advanced algorithms",
                    "metadata": {
                        "methods": [
                            {"name": "__init__", "parameters": [{"name": "config", "type": "Dict[str, Any]"}], "return_type": "None", "description": "Initialize with configuration"},
                            {"name": "process_data", "parameters": [{"name": "data", "type": "List[Any]"}], "return_type": "Dict[str, Any]", "description": "Process input data"},
                            {"name": "validate_input", "parameters": [{"name": "input_data", "type": "Any"}], "return_type": "bool", "description": "Validate input data"},
                        ],
                        "attributes": [
                            {"name": "config", "type": "Dict[str, Any]", "description": "Configuration data"},
                            {"name": "processed_count", "type": "int", "description": "Count of processed items"},
                        ],
                    },
                },
                {
                    "name": "ResultFormatter",
                    "type": "class",
                    "description": "Formats results for output",
                    "metadata": {"methods": [{"name": "validate", "parameters": [{"name": "data", "type": "Any"}], "return_type": "bool", "description": "Validate data"}]},
                },
            ],
            "relationships": [{"from": "DataProcessor", "to": "ResultFormatter", "type": "uses", "description": "Uses formatter for data output"}],
            "constraints": ["Must handle complex data structures", "Should demonstrate error handling", "Must be performant for large datasets"],
        }

    @staticmethod
    def create_performance_design_spec(iterations: int = 5) -> Dict[str, Any]:
        """Create a performance-focused design specification."""
        return {
            "name": "PerformanceTestClass_5",
            "description": "A performance-focused demo system",
            "components": [
                {
                    "name": "PerformanceProcessor",
                    "type": "class",
                    "metadata": {
                        "methods": [
                            {"name": "process_large_dataset", "parameters": [{"name": "data", "type": "List[Any]"}], "return_type": "List[Any]", "description": "Process large datasets efficiently"},
                            {"name": "optimize_memory", "parameters": [], "return_type": "None", "description": "Optimize memory usage"},
                        ]
                    },
                }
            ],
            "constraints": ["Must process 10,000+ items in under 1 second", "Memory usage must not exceed 100MB", "Should use efficient algorithms"],
        }
