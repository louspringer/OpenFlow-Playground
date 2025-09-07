"""
Bounded Context Analyzer

Analyzes code for bounded context patterns and boundaries.
"""

import ast
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field


@dataclass
class ContextAnalysis:
    """Analysis of a bounded context"""

    context_name: str
    file_path: str
    confidence: float  # 0.0 to 1.0
    entities: List[str] = field(default_factory=list)
    value_objects: List[str] = field(default_factory=list)
    aggregates: List[str] = field(default_factory=list)
    repositories: List[str] = field(default_factory=list)
    domain_services: List[str] = field(default_factory=list)
    domain_events: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    boundaries: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)

    def add_entity(self, entity: str):
        """Add entity to context"""
        if entity not in self.entities:
            self.entities.append(entity)

    def add_value_object(self, vo: str):
        """Add value object to context"""
        if vo not in self.value_objects:
            self.value_objects.append(vo)

    def add_aggregate(self, aggregate: str):
        """Add aggregate to context"""
        if aggregate not in self.aggregates:
            self.aggregates.append(aggregate)

    def add_repository(self, repository: str):
        """Add repository to context"""
        if repository not in self.repositories:
            self.repositories.append(repository)

    def add_domain_service(self, service: str):
        """Add domain service to context"""
        if service not in self.domain_services:
            self.domain_services.append(service)

    def add_domain_event(self, event: str):
        """Add domain event to context"""
        if event not in self.domain_events:
            self.domain_events.append(event)

    def add_dependency(self, dependency: str):
        """Add context dependency"""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def add_boundary(self, boundary: str):
        """Add boundary indicator"""
        if boundary not in self.boundaries:
            self.boundaries.append(boundary)

    def add_indicator(self, indicator: str):
        """Add analysis indicator"""
        if indicator not in self.indicators:
            self.indicators.append(indicator)


class BoundedContextAnalyzer:
    """Analyzes code for bounded context patterns"""

    def __init__(self):
        self.context_indicators = {
            "domain_keywords": [
                "user",
                "customer",
                "order",
                "product",
                "payment",
                "inventory",
                "shipping",
                "billing",
                "account",
                "profile",
                "notification",
                "authentication",
                "authorization",
                "session",
                "cart",
                "wishlist",
            ],
            "context_patterns": ["management", "service", "domain", "business", "core", "application", "infrastructure", "presentation"],
            "boundary_indicators": ["interface", "adapter", "gateway", "facade", "proxy", "mapper", "converter", "translator", "bridge"],
        }

    def analyze_file(self, tree: ast.AST, file_path: str) -> Optional[ContextAnalysis]:
        """Analyze file for bounded context patterns"""

        # Extract context name from file path
        context_name = self._extract_context_name(file_path)
        if not context_name:
            return None

        analysis = ContextAnalysis(context_name=context_name, file_path=file_path, confidence=0.0)

        # Analyze all classes in the file
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        for class_node in classes:
            self._analyze_class(class_node, analysis)

        # Analyze imports for dependencies
        self._analyze_imports(tree, analysis)

        # Calculate confidence based on findings
        analysis.confidence = self._calculate_confidence(analysis)

        return analysis if analysis.confidence > 0.3 else None

    def _extract_context_name(self, file_path: str) -> Optional[str]:
        """Extract context name from file path"""
        import os

        # Get directory structure
        path_parts = file_path.split(os.sep)

        # Look for domain indicators in path
        for part in path_parts:
            if any(keyword in part.lower() for keyword in self.context_indicators["domain_keywords"]):
                return part.lower()

        # Look for context patterns
        for part in path_parts:
            if any(pattern in part.lower() for pattern in self.context_indicators["context_patterns"]):
                return part.lower()

        # Use parent directory name as fallback
        if len(path_parts) >= 2:
            return path_parts[-2].lower()

        return None

    def _analyze_class(self, class_node: ast.ClassDef, analysis: ContextAnalysis):
        """Analyze class for context patterns"""
        class_name = class_node.name

        # Check for domain entity patterns
        if self._is_entity(class_node):
            analysis.add_entity(class_name)
            analysis.add_indicator("Contains domain entities")

        # Check for value object patterns
        if self._is_value_object(class_node):
            analysis.add_value_object(class_name)
            analysis.add_indicator("Contains value objects")

        # Check for aggregate patterns
        if self._is_aggregate(class_node):
            analysis.add_aggregate(class_name)
            analysis.add_indicator("Contains aggregates")

        # Check for repository patterns
        if self._is_repository(class_node):
            analysis.add_repository(class_name)
            analysis.add_indicator("Contains repositories")

        # Check for domain service patterns
        if self._is_domain_service(class_node):
            analysis.add_domain_service(class_name)
            analysis.add_indicator("Contains domain services")

        # Check for domain event patterns
        if self._is_domain_event(class_node):
            analysis.add_domain_event(class_name)
            analysis.add_indicator("Contains domain events")

        # Check for boundary patterns
        if self._is_boundary(class_node):
            analysis.add_boundary(class_name)
            analysis.add_indicator("Contains boundary objects")

    def _is_entity(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a domain entity"""
        # Check for entity inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "Entity" in base.id:
                return True

        # Check for entity naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["entity", "model", "domain"]):
            return True

        # Check for ID field
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id.lower() in ["id", "entity_id"]:
                        return True

        return False

    def _is_value_object(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a value object"""
        # Check for value object inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "ValueObject" in base.id:
                return True

        # Check for dataclass with frozen
        has_dataclass = False
        has_frozen = False

        for decorator in class_node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == "dataclass":
                    has_dataclass = True
                elif decorator.id == "frozen":
                    has_frozen = True

        if has_dataclass and has_frozen:
            return True

        # Check for value object naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["value", "money", "email", "address"]):
            return True

        return False

    def _is_aggregate(self, class_node: ast.ClassDef) -> bool:
        """Check if class is an aggregate root"""
        # Check for aggregate inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "Aggregate" in base.id:
                return True

        # Check for aggregate naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["aggregate", "root", "manager"]):
            return True

        # Check for domain events
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and "event" in target.id.lower():
                        return True

        return False

    def _is_repository(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a repository"""
        # Check for repository inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "Repository" in base.id:
                return True

        # Check for repository naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["repository", "repo", "store", "dao"]):
            return True

        # Check for repository methods
        repository_methods = ["get", "find", "save", "delete", "add", "remove"]
        method_names = [item.name for item in class_node.body if isinstance(item, ast.FunctionDef)]

        if any(method in method_names for method in repository_methods):
            return True

        return False

    def _is_domain_service(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a domain service"""
        # Check for service inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "Service" in base.id:
                return True

        # Check for service naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["service", "manager", "handler"]):
            return True

        # Check for stateless decorator
        for decorator in class_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "stateless":
                return True

        return False

    def _is_domain_event(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a domain event"""
        # Check for event inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "Event" in base.id:
                return True

        # Check for event naming patterns
        if any(keyword in class_node.name.lower() for keyword in ["event", "occurred", "happened"]):
            return True

        # Check for timestamp field
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and "time" in target.id.lower():
                        return True

        return False

    def _is_boundary(self, class_node: ast.ClassDef) -> bool:
        """Check if class is a boundary object"""
        # Check for boundary inheritance
        for base in class_node.bases:
            if isinstance(base, ast.Name) and any(keyword in base.id for keyword in ["Interface", "Adapter", "Gateway"]):
                return True

        # Check for boundary naming patterns
        if any(keyword in class_node.name.lower() for keyword in self.context_indicators["boundary_indicators"]):
            return True

        return False

    def _analyze_imports(self, tree: ast.AST, analysis: ContextAnalysis):
        """Analyze imports for context dependencies"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    if self._is_external_dependency(module_name):
                        analysis.add_dependency(module_name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    if self._is_external_dependency(node.module):
                        analysis.add_dependency(node.module)

    def _is_external_dependency(self, module_name: str) -> bool:
        """Check if module is an external dependency"""
        # Standard library modules (not external)
        stdlib_modules = {"os", "sys", "json", "datetime", "typing", "dataclasses", "abc", "enum", "pathlib", "collections", "itertools"}

        if module_name in stdlib_modules:
            return False

        # Check for common external packages
        external_indicators = ["django", "flask", "fastapi", "sqlalchemy", "pandas", "numpy", "requests", "boto3", "redis", "celery"]

        return any(indicator in module_name for indicator in external_indicators)

    def _calculate_confidence(self, analysis: ContextAnalysis) -> float:
        """Calculate confidence score for context analysis"""
        confidence = 0.0

        # Base confidence from context name
        if analysis.context_name:
            confidence += 0.2

        # Add confidence for each domain pattern found
        if analysis.entities:
            confidence += 0.2
        if analysis.value_objects:
            confidence += 0.1
        if analysis.aggregates:
            confidence += 0.2
        if analysis.repositories:
            confidence += 0.1
        if analysis.domain_services:
            confidence += 0.1
        if analysis.domain_events:
            confidence += 0.1
        if analysis.boundaries:
            confidence += 0.1

        # Bonus for having multiple patterns
        pattern_count = sum([len(analysis.entities), len(analysis.value_objects), len(analysis.aggregates), len(analysis.repositories), len(analysis.domain_services), len(analysis.domain_events)])

        if pattern_count > 3:
            confidence += 0.1

        return min(1.0, confidence)
