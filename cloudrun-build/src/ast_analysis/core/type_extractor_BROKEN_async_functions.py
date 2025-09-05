#!/usr/bin/env python3
"""
Type Extractor - RM-compliant type analysis and validation

This module extracts type information from Python code to enable:
- Mypy compliance validation
- Pydantic model discovery
- Interface contract extraction
- Type-driven code generation
"""

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)


@dataclass
class TypeAnnotation:
    """RM Compliance: Structured type annotation information"""

    name: str
    type_hint: str
    line_number: int
    is_optional: bool = False
    is_union: bool = False
    is_generic: bool = False
    base_types: List[str] = field(default_factory=list)
    validation_errors: List[str] = field(default_factory=list)

    def validate(self) -> bool:
        """RM Compliance: Self-validation"""
        if not self.name or not self.type_hint:
            self.validation_errors.append("Missing required fields")
            return False
        return True


@dataclass
class FunctionSignature:
    """RM Compliance: Function signature with type information"""

    name: str
    parameters: List[TypeAnnotation] = field(default_factory=list)
    return_type: Optional[TypeAnnotation] = None
    decorators: List[str] = field(default_factory=list)
    line_number: int = 0
    is_async: bool = False
    validation_errors: List[str] = field(default_factory=list)

    def validate(self) -> bool:
        """RM Compliance: Self-validation"""
        if not self.name:
            self.validation_errors.append("Missing function name")
            return False
        return True


@dataclass
class ClassInterface:
    """RM Compliance: Class interface with type contracts"""

    name: str
    base_classes: List[str] = field(default_factory=list)
    methods: List[FunctionSignature] = field(default_factory=list)
    properties: List[TypeAnnotation] = field(default_factory=list)
    class_variables: List[TypeAnnotation] = field(default_factory=list)
    line_number: int = 0
    validation_errors: List[str] = field(default_factory=list)

    def validate(self) -> bool:
        """RM Compliance: Self-validation"""
        if not self.name:
            self.validation_errors.append("Missing class name")
            return False
        return True


@dataclass
class PydanticModel:
    """RM Compliance: Pydantic model information"""

    name: str
    fields: List[TypeAnnotation] = field(default_factory=list)
    validators: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    line_number: int = 0
    validation_errors: List[str] = field(default_factory=list)

    def validate(self) -> bool:
        """RM Compliance: Self-validation"""
        if not self.name:
            self.validation_errors.append("Missing model name")
            return False
        return True


class TypeExtractor:
    """RM Compliance: Type extraction with self-monitoring"""

    def __init__(self):
        # RM Compliance: Health monitoring
        self._extraction_count = 0
        self._success_count = 0
        self._error_count = 0
        self._type_annotations_found = 0

        logger.info("✅ TypeExtractor initialized with RM compliance")

    def extract_types_from_file(self, file_path: Path) -> Dict[str, Any]:
        """RM Compliance: Extract all type information from file"""
        self._extraction_count += 1

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            ast_tree = ast.parse(content)

            result = {
                "functions": self._extract_function_signatures(ast_tree),
                "classes": self._extract_class_interfaces(ast_tree),
                "pydantic_models": self._extract_pydantic_models(ast_tree),
                "type_annotations": self._extract_type_annotations(ast_tree),
                "mypy_compliance": self._analyze_mypy_compliance(ast_tree),
                "validation_errors": [],
            }

            # RM Compliance: Success tracking
            self._success_count += 1
            self._type_annotations_found += len(result["type_annotations"])

            logger.info(f"✅ Extracted types from {file_path}: {len(result['type_annotations'])} annotations")
            return result

        except Exception as e:
            error_msg = f"Error extracting types from {file_path}: {e}"
            logger.error(error_msg)
            self._error_count += 1

            return {"functions": [], "classes": [], "pydantic_models": [], "type_annotations": [], "mypy_compliance": {"score": 0.0, "issues": [error_msg]}, "validation_errors": [error_msg]}

    def _extract_function_signatures(self, ast_tree: ast.AST) -> List[FunctionSignature]:
        """Extract function signatures with type information"""
        signatures = []

        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                signature = FunctionSignature(name=node.name, line_number=node.lineno, is_async=isinstance(node, ast.AsyncFunctionDef))

                # Extract parameters with types
                for arg in node.args.args:
                    param_type = self._extract_type_annotation(arg.annotation)
                    signature.parameters.append(TypeAnnotation(name=arg.arg, type_hint=param_type or "Any", line_number=arg.lineno if hasattr(arg, "lineno") else 0))

                # Extract return type
                if node.returns:
                    signature.return_type = TypeAnnotation(
                        name="return", type_hint=self._extract_type_annotation(node.returns), line_number=node.returns.lineno if hasattr(node.returns, "lineno") else 0
                    )

                # Extract decorators
                signature.decorators = [self._extract_decorator_name(d) for d in node.decorator_list]

                if signature.validate():
                    signatures.append(signature)
                else:
                    logger.warning(f"Invalid function signature for {node.name}: {signature.validation_errors}")

        return signatures

    def _extract_class_interfaces(self, ast_tree: ast.AST) -> List[ClassInterface]:
        """Extract class interfaces with type contracts"""
        interfaces = []

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ClassDef):
                interface = ClassInterface(name=node.name, line_number=node.lineno)

                # Extract base classes
                for base in node.bases:
                    interface.base_classes.append(self._extract_type_annotation(base))

                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_sig = self._extract_function_signatures(ast_tree)
                        # Find the method signature for this class
                        for sig in method_sig:
                            if sig.name == item.name:
                                interface.methods.append(sig)
                                break

                # Extract class variables and properties
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                var_type = self._extract_type_annotation(item.value)
                                interface.class_variables.append(TypeAnnotation(name=target.id, type_hint=var_type or "Any", line_number=target.lineno if hasattr(target, "lineno") else 0))
                    elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        # Handle typed class variables like: class_var: str = "default"
                        var_type = self._extract_type_annotation(item.annotation)
                        interface.class_variables.append(TypeAnnotation(name=item.target.id, type_hint=var_type or "Any", line_number=item.target.lineno if hasattr(item.target, "lineno") else 0))

                if interface.validate():
                    interfaces.append(interface)
                else:
                    logger.warning(f"Invalid class interface for {node.name}: {interface.validation_errors}")

        return interfaces

    def _extract_pydantic_models(self, ast_tree: ast.AST) -> List[PydanticModel]:
        """Extract Pydantic model information"""
        models = []

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ClassDef):
                # Check if this is a Pydantic model
                if self._is_pydantic_model(node):
                    model = PydanticModel(name=node.name, line_number=node.lineno)

                    # Extract fields from class body
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            field_type = self._extract_type_annotation(item.annotation)
                            model.fields.append(TypeAnnotation(name=item.target.id, type_hint=field_type or "Any", line_number=item.target.lineno if hasattr(item.target, "lineno") else 0))

                    if model.validate():
                        models.append(model)
                    else:
                        logger.warning(f"Invalid Pydantic model for {node.name}: {model.validation_errors}")

        return models

    def _extract_type_annotations(self, ast_tree: ast.AST) -> List[TypeAnnotation]:
        """Extract all type annotations from AST"""
        annotations = []

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                annotation = TypeAnnotation(name=node.target.id, type_hint=self._extract_type_annotation(node.annotation), line_number=node.target.lineno if hasattr(node.target, "lineno") else 0)

                if annotation.validate():
                    annotations.append(annotation)

        return annotations

    def _analyze_mypy_compliance(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Analyze mypy compliance of the code"""
        total_functions = 0
        typed_functions = 0
        total_parameters = 0
        typed_parameters = 0

        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_functions += 1
                if node.returns:
                    typed_functions += 1

                for arg in node.args.args:
                    total_parameters += 1
                    if arg.annotation:
                        typed_parameters += 1

        compliance_score = 0.0
        if total_functions > 0:
            function_score = typed_functions / total_functions
            parameter_score = typed_parameters / total_parameters if total_parameters > 0 else 1.0
            compliance_score = (function_score + parameter_score) / 2

        return {
            "score": compliance_score,
            "total_functions": total_functions,
            "typed_functions": typed_functions,
            "total_parameters": total_parameters,
            "typed_parameters": typed_parameters,
            "issues": self._identify_mypy_issues(ast_tree),
        }

    def _identify_mypy_issues(self, ast_tree: ast.AST) -> List[str]:
        """Identify potential mypy issues"""
        issues = []

        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.returns:
                    issues.append(f"Function '{node.name}' missing return type annotation")

                for arg in node.args.args:
                    if not arg.annotation:
                        issues.append(f"Parameter '{arg.arg}' in '{node.name}' missing type annotation")

        return issues

    def _is_pydantic_model(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a Pydantic model"""
        # Check base classes for Pydantic types
        for base in class_node.bases:
            base_name = self._extract_type_annotation(base)
            if "BaseModel" in base_name or "Pydantic" in base_name:
                return True

        # Check decorators
        for decorator in class_node.decorator_list:
            decorator_name = self._extract_decorator_name(decorator)
            if "pydantic" in decorator_name.lower():
                return True

        return False

    def _extract_type_annotation(self, node: Optional[ast.expr]) -> str:
        """Extract type annotation as string"""
        if node is None:
            return "Any"

        try:
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Constant):
                return str(node.value)
            elif isinstance(node, ast.Subscript):
                value = self._extract_type_annotation(node.value)
                slice_val = self._extract_type_annotation(node.slice)
                return f"{value}[{slice_val}]"
            elif isinstance(node, ast.Tuple):
                elements = [self._extract_type_annotation(el) for el in node.elts]
                return f"Tuple[{', '.join(elements)}]"
            elif isinstance(node, ast.Attribute):
                value = self._extract_type_annotation(node.value)
                return f"{value}.{node.attr}"
            else:
                return ast.unparse(node) if hasattr(ast, "unparse") else str(node)
        except Exception:
            return "Any"

    def _extract_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name as string"""
        try:
            if isinstance(decorator, ast.Name):
                return decorator.id
            elif isinstance(decorator, ast.Attribute):
                value = self._extract_decorator_name(decorator.value)
                return f"{value}.{decorator.attr}"
            elif isinstance(decorator, ast.Call):
                return self._extract_decorator_name(decorator.func)
            else:
                return ast.unparse(decorator) if hasattr(ast, "unparse") else str(decorator)
        except Exception:
            return "unknown"

    def get_health_status(self) -> Dict[str, Any]:
        """RM Compliance: Health monitoring and reporting"""
        total_extractions = self._extraction_count
        success_rate = self._success_count / total_extractions if total_extractions > 0 else 0
        error_rate = self._error_count / total_extractions if total_extractions > 0 else 0

        health_status = "HEALTHY"
        if error_rate >= 0.2:  # 20% error rate should be DEGRADED
            health_status = "DEGRADED"
        if error_rate >= 0.6:
            health_status = "UNHEALTHY"

        return {
            "status": health_status,
            "total_extractions": total_extractions,
            "success_count": self._success_count,
            "error_count": self._error_count,
            "success_rate": success_rate,
            "error_rate": error_rate,
            "type_annotations_found": self._type_annotations_found,
            "average_annotations_per_file": self._type_annotations_found / total_extractions if total_extractions > 0 else 0,
        }
