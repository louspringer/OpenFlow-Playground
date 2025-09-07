"""
DDD Pattern Detector

Detects Domain-Driven Design patterns in Python code.
"""

import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class DDDPatternType(Enum):
    """Types of DDD patterns"""

    ENTITY = "entity"
    VALUE_OBJECT = "value_object"
    AGGREGATE_ROOT = "aggregate_root"
    REPOSITORY = "repository"
    DOMAIN_SERVICE = "domain_service"
    DOMAIN_EVENT = "domain_event"
    FACTORY = "factory"
    SPECIFICATION = "specification"
    SAGA = "saga"
    ANTI_CORRUPTION_LAYER = "anti_corruption_layer"


@dataclass
class DDDPattern:
    """Represents a detected DDD pattern"""

    pattern_type: DDDPatternType
    class_name: str
    file_path: str
    line_number: int
    confidence: float  # 0.0 to 1.0
    details: Dict[str, Any] = field(default_factory=dict)
    indicators: List[str] = field(default_factory=list)

    def add_indicator(self, indicator: str):
        """Add detection indicator"""
        self.indicators.append(indicator)

    def add_detail(self, key: str, value: Any):
        """Add pattern detail"""
        self.details[key] = value


class DDDDetector:
    """Detects DDD patterns in Python AST"""

    def __init__(self):
        self.pattern_detectors = {
            DDDPatternType.ENTITY: self._detect_entity,
            DDDPatternType.VALUE_OBJECT: self._detect_value_object,
            DDDPatternType.AGGREGATE_ROOT: self._detect_aggregate_root,
            DDDPatternType.REPOSITORY: self._detect_repository,
            DDDPatternType.DOMAIN_SERVICE: self._detect_domain_service,
            DDDPatternType.DOMAIN_EVENT: self._detect_domain_event,
            DDDPatternType.FACTORY: self._detect_factory,
            DDDPatternType.SPECIFICATION: self._detect_specification,
            DDDPatternType.SAGA: self._detect_saga,
            DDDPatternType.ANTI_CORRUPTION_LAYER: self._detect_anti_corruption_layer,
        }

    def detect_patterns(self, tree: ast.AST, file_path: str) -> List[DDDPattern]:
        """Detect all DDD patterns in AST"""
        patterns = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for pattern_type, detector in self.pattern_detectors.items():
                    pattern = detector(node, file_path)
                    if pattern:
                        patterns.append(pattern)

        return patterns

    def _detect_entity(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect entity pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for identity field
        has_id = False
        for base in node.bases:
            if isinstance(base, ast.Name) and "Entity" in base.id:
                has_id = True
                confidence += 0.4
                indicators.append("Inherits from Entity base class")

        # Check for ID field in class (including in methods)
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id.lower() in ["id", "entity_id", "identifier"]:
                        has_id = True
                        confidence += 0.3
                        indicators.append(f"Has identity field: {target.id}")
            elif isinstance(item, ast.FunctionDef):
                # Check inside methods for ID assignments
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and target.attr.lower() in ["id", "entity_id", "identifier"]:
                                has_id = True
                                confidence += 0.3
                                indicators.append(f"Has identity field: {target.attr}")
                                break

        # Check for business methods
        business_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                business_methods.append(item.name)

        if business_methods:
            confidence += 0.2
            indicators.append(f"Has business methods: {', '.join(business_methods)}")
            details["business_methods"] = business_methods

        # Check for domain-specific naming
        if any(keyword in node.name.lower() for keyword in ["user", "customer", "order", "product", "account"]):
            confidence += 0.1
            indicators.append("Domain-specific naming")

        if confidence >= 0.3:
            return DDDPattern(pattern_type=DDDPatternType.ENTITY, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators)

        return None

    def _detect_value_object(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect value object pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for immutability indicators
        has_frozen = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "frozen":
                has_frozen = True
                confidence += 0.4
                indicators.append("Uses @frozen decorator")
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                # Check for frozen=True in dataclass call
                for keyword in decorator.keywords:
                    if keyword.arg == "frozen" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        has_frozen = True
                        confidence += 0.4
                        indicators.append("Uses @dataclass(frozen=True)")
                        break

        # Check for dataclass
        is_dataclass = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                is_dataclass = True
                confidence += 0.2
                indicators.append("Uses @dataclass decorator")
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                is_dataclass = True
                confidence += 0.2
                indicators.append("Uses @dataclass decorator")

        # Check for equality methods
        has_eq = False
        has_hash = False
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name == "__eq__":
                    has_eq = True
                    confidence += 0.2
                    indicators.append("Implements __eq__ method")
                elif item.name == "__hash__":
                    has_hash = True
                    confidence += 0.2
                    indicators.append("Implements __hash__ method")

        # Check for value object naming patterns
        if any(keyword in node.name.lower() for keyword in ["money", "email", "address", "date", "time", "value"]):
            confidence += 0.1
            indicators.append("Value object naming pattern")

        if confidence >= 0.3:
            return DDDPattern(
                pattern_type=DDDPatternType.VALUE_OBJECT, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None

    def _detect_aggregate_root(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect aggregate root pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for aggregate root inheritance
        for base in node.bases:
            if isinstance(base, ast.Name) and "Aggregate" in base.id:
                confidence += 0.5
                indicators.append("Inherits from AggregateRoot base class")

        # Check for domain events (including in methods)
        has_events = False
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and "event" in target.id.lower():
                        has_events = True
                        confidence += 0.2
                        indicators.append("Has domain events")
            elif isinstance(item, ast.FunctionDef):
                # Check inside methods for domain events
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and ("event" in target.attr.lower() or "domain" in target.attr.lower()):
                                has_events = True
                                confidence += 0.2
                                indicators.append("Has domain events")
                                break

        # Check for business invariants
        invariant_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if "invariant" in item.name.lower() or "validate" in item.name.lower():
                    invariant_methods.append(item.name)

        if invariant_methods:
            confidence += 0.2
            indicators.append(f"Has invariant methods: {', '.join(invariant_methods)}")
            details["invariant_methods"] = invariant_methods

        # Check for command handling
        command_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if any(keyword in item.name.lower() for keyword in ["handle", "process", "execute"]):
                    command_methods.append(item.name)

        if command_methods:
            confidence += 0.1
            indicators.append(f"Has command methods: {', '.join(command_methods)}")
            details["command_methods"] = command_methods

        if confidence >= 0.3:
            return DDDPattern(
                pattern_type=DDDPatternType.AGGREGATE_ROOT, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None

    def _detect_repository(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect repository pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for repository naming
        if "repository" in node.name.lower() or "repo" in node.name.lower():
            confidence += 0.3
            indicators.append("Repository naming pattern")

        # Check for repository methods
        repository_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_name = item.name.lower()
                if any(keyword in method_name for keyword in ["get", "find", "save", "delete", "add", "remove"]):
                    repository_methods.append(item.name)

        if repository_methods:
            confidence += 0.4
            indicators.append(f"Has repository methods: {', '.join(repository_methods)}")
            details["repository_methods"] = repository_methods

        # Check for abstract base class
        for base in node.bases:
            if isinstance(base, ast.Name) and "Repository" in base.id:
                confidence += 0.3
                indicators.append("Inherits from Repository base class")

        if confidence >= 0.4:
            return DDDPattern(pattern_type=DDDPatternType.REPOSITORY, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators)

        return None

    def _detect_domain_service(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect domain service pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for service naming
        if "service" in node.name.lower():
            confidence += 0.3
            indicators.append("Service naming pattern")

        # Check for stateless methods
        has_stateless = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "stateless":
                has_stateless = True
                confidence += 0.3
                indicators.append("Marked as stateless")

        # Check for domain-specific methods
        domain_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith("_") and not item.name.startswith("get_"):
                    domain_methods.append(item.name)

        if domain_methods:
            confidence += 0.2
            indicators.append(f"Has domain methods: {', '.join(domain_methods)}")
            details["domain_methods"] = domain_methods

        # Check for domain service inheritance
        for base in node.bases:
            if isinstance(base, ast.Name) and "Service" in base.id:
                confidence += 0.2
                indicators.append("Inherits from Service base class")

        if confidence >= 0.4:
            return DDDPattern(
                pattern_type=DDDPatternType.DOMAIN_SERVICE, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None

    def _detect_domain_event(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect domain event pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for event naming
        if any(keyword in node.name.lower() for keyword in ["event", "occurred", "happened"]):
            confidence += 0.3
            indicators.append("Event naming pattern")

        # Check for event fields
        event_fields = []
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        event_fields.append(target.id)

        if event_fields:
            confidence += 0.2
            indicators.append(f"Has event fields: {', '.join(event_fields)}")
            details["event_fields"] = event_fields

        # Check for event inheritance
        for base in node.bases:
            if isinstance(base, ast.Name) and "Event" in base.id:
                confidence += 0.4
                indicators.append("Inherits from Event base class")

        # Check for timestamp field
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and "time" in target.id.lower():
                        confidence += 0.1
                        indicators.append("Has timestamp field")

        if confidence >= 0.4:
            return DDDPattern(
                pattern_type=DDDPatternType.DOMAIN_EVENT, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None

    def _detect_factory(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect factory pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for factory naming
        if "factory" in node.name.lower() or "builder" in node.name.lower():
            confidence += 0.3
            indicators.append("Factory naming pattern")

        # Check for create methods
        create_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name.lower().startswith("create") or item.name.lower().startswith("build"):
                    create_methods.append(item.name)

        if create_methods:
            confidence += 0.4
            indicators.append(f"Has create methods: {', '.join(create_methods)}")
            details["create_methods"] = create_methods

        # Check for static methods
        static_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == "staticmethod":
                        static_methods.append(item.name)

        if static_methods:
            confidence += 0.2
            indicators.append(f"Has static methods: {', '.join(static_methods)}")
            details["static_methods"] = static_methods

        if confidence >= 0.4:
            return DDDPattern(pattern_type=DDDPatternType.FACTORY, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators)

        return None

    def _detect_specification(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect specification pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for specification naming
        if "spec" in node.name.lower() or "specification" in node.name.lower():
            confidence += 0.3
            indicators.append("Specification naming pattern")

        # Check for is_satisfied method
        has_satisfied = False
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if "satisfied" in item.name.lower() or "matches" in item.name.lower():
                    has_satisfied = True
                    confidence += 0.4
                    indicators.append("Has satisfaction method")

        # Check for boolean return methods
        boolean_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Check return type annotation
                if item.returns and isinstance(item.returns, ast.Name) and item.returns.id == "bool":
                    boolean_methods.append(item.name)

        if boolean_methods:
            confidence += 0.2
            indicators.append(f"Has boolean methods: {', '.join(boolean_methods)}")
            details["boolean_methods"] = boolean_methods

        if confidence >= 0.4:
            return DDDPattern(
                pattern_type=DDDPatternType.SPECIFICATION, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None

    def _detect_saga(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect saga pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for saga naming
        if "saga" in node.name.lower() or "workflow" in node.name.lower():
            confidence += 0.3
            indicators.append("Saga naming pattern")

        # Check for compensation methods
        compensation_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if "compensate" in item.name.lower() or "rollback" in item.name.lower():
                    compensation_methods.append(item.name)

        if compensation_methods:
            confidence += 0.4
            indicators.append(f"Has compensation methods: {', '.join(compensation_methods)}")
            details["compensation_methods"] = compensation_methods

        # Check for step methods
        step_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if "step" in item.name.lower() or "execute" in item.name.lower():
                    step_methods.append(item.name)

        if step_methods:
            confidence += 0.2
            indicators.append(f"Has step methods: {', '.join(step_methods)}")
            details["step_methods"] = step_methods

        if confidence >= 0.4:
            return DDDPattern(pattern_type=DDDPatternType.SAGA, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators)

        return None

    def _detect_anti_corruption_layer(self, node: ast.ClassDef, file_path: str) -> Optional[DDDPattern]:
        """Detect anti-corruption layer pattern"""
        indicators = []
        confidence = 0.0
        details = {}

        # Check for adapter naming
        if any(keyword in node.name.lower() for keyword in ["adapter", "translator", "mapper", "converter"]):
            confidence += 0.3
            indicators.append("Adapter naming pattern")

        # Check for translation methods
        translation_methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if any(keyword in item.name.lower() for keyword in ["translate", "convert", "map", "adapt"]):
                    translation_methods.append(item.name)

        if translation_methods:
            confidence += 0.4
            indicators.append(f"Has translation methods: {', '.join(translation_methods)}")
            details["translation_methods"] = translation_methods

        # Check for external system references
        external_refs = []
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        if any(keyword in target.id.lower() for keyword in ["external", "legacy", "third_party"]):
                            external_refs.append(target.id)

        if external_refs:
            confidence += 0.2
            indicators.append(f"References external systems: {', '.join(external_refs)}")
            details["external_references"] = external_refs

        if confidence >= 0.4:
            return DDDPattern(
                pattern_type=DDDPatternType.ANTI_CORRUPTION_LAYER, class_name=node.name, file_path=file_path, line_number=node.lineno, confidence=confidence, details=details, indicators=indicators
            )

        return None
