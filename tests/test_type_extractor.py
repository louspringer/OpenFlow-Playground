#!/usr/bin/env python3
"""
Unit Tests for TypeExtractor - Demonstrating Error-Free Test Generation

This test demonstrates how knowing requirements, interfaces, and return values
enables generation of perfect unit tests.
"""

import ast
import pytest
from pathlib import Path
from unittest.mock import mock_open, patch

from src.ast_analysis.core.type_extractor import (
    TypeExtractor,
    TypeAnnotation,
    FunctionSignature,
    ClassInterface,
    PydanticModel,
)


class TestTypeExtractor:
    """Test suite for TypeExtractor class"""

    def test_initialization(self):
        """Test TypeExtractor initializes correctly with RM compliance"""
        extractor = TypeExtractor()

        # RM Compliance: Health monitoring attributes exist
        assert hasattr(extractor, "_extraction_count")
        assert hasattr(extractor, "_success_count")
        assert hasattr(extractor, "_error_count")
        assert hasattr(extractor, "_type_annotations_found")

        # Initial state
        assert extractor._extraction_count == 0
        assert extractor._success_count == 0
        assert extractor._error_count == 0
        assert extractor._type_annotations_found == 0

    def test_extract_types_from_file_success(self):
        """Test successful type extraction from a Python file"""
        extractor = TypeExtractor()

        # Mock Python file content with known structure
        mock_content = """
from typing import List, Optional
from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    count: int
    items: List[str]
    optional_field: Optional[bool] = None

def test_function(param1: str, param2: int) -> bool:
    return True

async def async_function() -> str:
    return "test"
"""

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = extractor.extract_types_from_file(Path("test.py"))

        # Verify structure matches known interface
        assert "functions" in result
        assert "classes" in result
        assert "pydantic_models" in result
        assert "type_annotations" in result
        assert "mypy_compliance" in result
        assert "validation_errors" in result

        # Verify Pydantic model extraction
        assert len(result["pydantic_models"]) == 1
        model = result["pydantic_models"][0]
        assert model.name == "TestModel"
        assert len(model.fields) == 4

        # Verify function extraction
        assert len(result["functions"]) == 2
        function_names = [f.name for f in result["functions"]]
        assert "test_function" in function_names
        assert "async_function" in function_names

        # Verify health tracking
        assert extractor._extraction_count == 1
        assert extractor._success_count == 1
        assert extractor._error_count == 0

    def test_extract_types_from_file_error_handling(self):
        """Test error handling when file parsing fails"""
        extractor = TypeExtractor()

        # Mock file open to raise exception
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            result = extractor.extract_types_from_file(Path("nonexistent.py"))

        # Verify error structure matches known interface
        assert "functions" in result
        assert "classes" in result
        assert "pydantic_models" in result
        assert "type_annotations" in result
        assert "mypy_compliance" in result
        assert "validation_errors" in result

        # Verify error state
        assert result["functions"] == []
        assert result["classes"] == []
        assert result["pydantic_models"] == []
        assert result["type_annotations"] == []
        assert result["mypy_compliance"]["score"] == 0.0
        assert len(result["validation_errors"]) == 1

        # Verify health tracking
        assert extractor._extraction_count == 1
        assert extractor._success_count == 0
        assert extractor._error_count == 1

    def test_extract_function_signatures(self):
        """Test function signature extraction with known AST structure"""
        extractor = TypeExtractor()

        # Create AST tree with known function structure
        source = """
def simple_function():
    pass

def typed_function(param1: str, param2: int = 42) -> bool:
    return True

@decorator
async def async_function() -> str:
    return "async"
"""

        ast_tree = ast.parse(source)
        signatures = extractor._extract_function_signatures(ast_tree)

        # Verify we get expected number of functions
        assert len(signatures) == 3

        # Verify simple function
        simple_func = next(f for f in signatures if f.name == "simple_function")
        assert simple_func.name == "simple_function"
        assert simple_func.is_async is False
        assert len(simple_func.parameters) == 0
        assert simple_func.return_type is None

        # Verify typed function
        typed_func = next(f for f in signatures if f.name == "typed_function")
        assert typed_func.name == "typed_function"
        assert typed_func.is_async is False
        assert len(typed_func.parameters) == 2
        assert typed_func.return_type is not None
        assert typed_func.return_type.type_hint == "bool"

        # Verify async function
        async_func = next(f for f in signatures if f.name == "async_function")
        assert async_func.name == "async_function"
        assert async_func.is_async is True
        assert len(async_func.parameters) == 0
        assert async_func.return_type is not None
        assert async_func.return_type.type_hint == "str"
        assert "decorator" in async_func.decorators

    def test_extract_class_interfaces(self):
        """Test class interface extraction with known AST structure"""
        extractor = TypeExtractor()

        # Create AST tree with known class structure
        source = """
class BaseClass:
    pass

class TestClass(BaseClass):
    class_var: str = "default"
    
    def __init__(self, name: str):
        self.name = name
    
    def method1(self) -> str:
        return self.name
    
    @property
    def property1(self) -> int:
        return 42
"""

        ast_tree = ast.parse(source)
        interfaces = extractor._extract_class_interfaces(ast_tree)

        # Verify we get expected number of classes
        assert len(interfaces) == 2

        # Verify TestClass
        test_class = next(c for c in interfaces if c.name == "TestClass")
        assert test_class.name == "TestClass"
        assert "BaseClass" in test_class.base_classes
        assert len(test_class.methods) >= 1  # At least __init__
        assert len(test_class.class_variables) >= 1  # At least class_var

    def test_extract_pydantic_models(self):
        """Test Pydantic model extraction with known structure"""
        extractor = TypeExtractor()

        # Create AST tree with Pydantic model
        source = """
from pydantic import BaseModel, Field
from typing import Optional, List

class UserModel(BaseModel):
    id: int
    name: str = Field(..., description="User name")
    email: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        validate_assignment = True
"""

        ast_tree = ast.parse(source)
        models = extractor._extract_pydantic_models(ast_tree)

        # Verify Pydantic model detection
        assert len(models) == 1
        model = models[0]
        assert model.name == "UserModel"
        assert len(model.fields) == 4

        # Verify field types
        field_names = [f.name for f in model.fields]
        assert "id" in field_names
        assert "name" in field_names
        assert "email" in field_names
        assert "tags" in field_names

    def test_extract_type_annotations(self):
        """Test type annotation extraction with known structure"""
        extractor = TypeExtractor()

        # Create AST tree with type annotations
        source = """
from typing import List, Dict, Optional

# Type annotations
name: str = "test"
count: int = 42
items: List[str] = []
config: Dict[str, Any] = {}
optional_value: Optional[bool] = None
"""

        ast_tree = ast.parse(source)
        annotations = extractor._extract_type_annotations(ast_tree)

        # Verify type annotations
        assert len(annotations) == 5

        # Verify specific annotations
        annotation_names = [a.name for a in annotations]
        assert "name" in annotation_names
        assert "count" in annotation_names
        assert "items" in annotation_names
        assert "config" in annotation_names
        assert "optional_value" in annotation_names

    def test_analyze_mypy_compliance(self):
        """Test Mypy compliance analysis with known code structure"""
        extractor = TypeExtractor()

        # Create AST tree with mixed typing
        source = """
def untyped_function(param):
    return param

def typed_function(param: str) -> str:
    return param

def partial_function(param: str):
    return param
"""

        ast_tree = ast.parse(source)
        compliance = extractor._analyze_mypy_compliance(ast_tree)

        # Verify compliance structure
        assert "score" in compliance
        assert "total_functions" in compliance
        assert "typed_functions" in compliance
        assert "total_parameters" in compliance
        assert "typed_parameters" in compliance
        assert "issues" in compliance

        # Verify specific values
        assert compliance["total_functions"] == 3
        assert compliance["typed_functions"] == 1  # Only typed_function has return type
        assert compliance["total_parameters"] == 3
        assert compliance["typed_parameters"] == 2  # typed_function and partial_function have typed params

        # Verify issues
        assert len(compliance["issues"]) > 0
        assert any("missing return type annotation" in issue for issue in compliance["issues"])

    def test_health_status_reporting(self):
        """Test health status reporting with known metrics"""
        extractor = TypeExtractor()

        # Simulate some extractions
        extractor._extraction_count = 10
        extractor._success_count = 8
        extractor._error_count = 2
        extractor._type_annotations_found = 25

        health = extractor.get_health_status()

        # Verify health structure
        assert "status" in health
        assert "total_extractions" in health
        assert "success_count" in health
        assert "error_count" in health
        assert "success_rate" in health
        assert "error_rate" in health
        assert "type_annotations_found" in health
        assert "average_annotations_per_file" in health

        # Verify calculated values
        assert health["total_extractions"] == 10
        assert health["success_count"] == 8
        assert health["error_count"] == 2
        assert health["success_rate"] == 0.8
        assert health["error_rate"] == 0.2
        assert health["type_annotations_found"] == 25
        assert health["average_annotations_per_file"] == 2.5

        # Verify status classification
        assert health["status"] == "DEGRADED"  # 20% error rate

    def test_health_status_healthy(self):
        """Test health status when system is healthy"""
        extractor = TypeExtractor()

        # Simulate healthy state
        extractor._extraction_count = 10
        extractor._success_count = 10
        extractor._error_count = 0
        extractor._type_annotations_found = 30

        health = extractor.get_health_status()

        assert health["status"] == "HEALTHY"
        assert health["success_rate"] == 1.0
        assert health["error_rate"] == 0.0

    def test_health_status_unhealthy(self):
        """Test health status when system is unhealthy"""
        extractor = TypeExtractor()

        # Simulate unhealthy state
        extractor._extraction_count = 10
        extractor._success_count = 3
        extractor._error_count = 7
        extractor._type_annotations_found = 5

        health = extractor.get_health_status()

        assert health["status"] == "UNHEALTHY"
        assert health["success_rate"] == 0.3
        assert health["error_rate"] == 0.7

    def test_type_annotation_validation(self):
        """Test TypeAnnotation dataclass validation"""
        # Valid annotation
        valid_annotation = TypeAnnotation(name="test_param", type_hint="str", line_number=10)
        assert valid_annotation.validate() is True
        assert len(valid_annotation.validation_errors) == 0

        # Invalid annotation - missing name
        invalid_annotation = TypeAnnotation(name="", type_hint="str", line_number=10)
        assert invalid_annotation.validate() is False
        assert len(invalid_annotation.validation_errors) > 0

    def test_function_signature_validation(self):
        """Test FunctionSignature dataclass validation"""
        # Valid signature
        valid_signature = FunctionSignature(name="test_function", line_number=20)
        assert valid_signature.validate() is True
        assert len(valid_signature.validation_errors) == 0

        # Invalid signature - missing name
        invalid_signature = FunctionSignature(name="", line_number=20)
        assert invalid_signature.validate() is False
        assert len(invalid_signature.validation_errors) > 0

    def test_class_interface_validation(self):
        """Test ClassInterface dataclass validation"""
        # Valid interface
        valid_interface = ClassInterface(name="TestClass", line_number=30)
        assert valid_interface.validate() is True
        assert len(valid_interface.validation_errors) == 0

        # Invalid interface - missing name
        invalid_interface = ClassInterface(name="", line_number=30)
        assert invalid_interface.validate() is False
        assert len(invalid_interface.validation_errors) > 0

    def test_pydantic_model_validation(self):
        """Test PydanticModel dataclass validation"""
        # Valid model
        valid_model = PydanticModel(name="UserModel", line_number=40)
        assert valid_model.validate() is True
        assert len(valid_model.validation_errors) == 0

        # Invalid model - missing name
        invalid_model = PydanticModel(name="", line_number=40)
        assert invalid_model.validate() is False
        assert len(invalid_model.validation_errors) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
