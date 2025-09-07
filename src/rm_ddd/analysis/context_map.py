"""
Context Map Analyzer

Analyzes relationships between bounded contexts and generates context maps.
"""

import ast
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RelationshipType(Enum):
    """Types of relationships between bounded contexts"""

    UPSTREAM_DOWNSTREAM = "upstream_downstream"
    PARTNER = "partner"
    SHARED_KERNEL = "shared_kernel"
    CUSTOMER_SUPPLIER = "customer_supplier"
    CONFORMIST = "conformist"
    ANTICORRUPTION_LAYER = "anticorruption_layer"
    OPEN_HOST_SERVICE = "open_host_service"
    PUBLISHED_LANGUAGE = "published_language"
    SEPARATE_WAYS = "separate_ways"
    BIG_BALL_OF_MUD = "big_ball_of_mud"


@dataclass
class ContextRelationship:
    """Relationship between two bounded contexts"""

    upstream_context: str
    downstream_context: str
    relationship_type: RelationshipType
    confidence: float  # 0.0 to 1.0
    evidence: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    data_flow: List[str] = field(default_factory=list)

    def add_evidence(self, evidence: str):
        """Add evidence for this relationship"""
        if evidence not in self.evidence:
            self.evidence.append(evidence)

    def add_interface(self, interface: str):
        """Add interface between contexts"""
        if interface not in self.interfaces:
            self.interfaces.append(interface)

    def add_data_flow(self, data_flow: str):
        """Add data flow between contexts"""
        if data_flow not in self.data_flow:
            self.data_flow.append(data_flow)


@dataclass
class ContextMap:
    """Context map showing relationships between bounded contexts"""

    contexts: List[str] = field(default_factory=list)
    relationships: List[ContextRelationship] = field(default_factory=list)
    shared_kernels: List[str] = field(default_factory=list)
    anticorruption_layers: List[str] = field(default_factory=list)
    open_host_services: List[str] = field(default_factory=list)
    published_languages: List[str] = field(default_factory=list)

    def add_context(self, context: str):
        """Add context to map"""
        if context not in self.contexts:
            self.contexts.append(context)

    def add_relationship(self, relationship: ContextRelationship):
        """Add relationship to map"""
        self.relationships.append(relationship)

    def get_relationships_for_context(self, context: str) -> List[ContextRelationship]:
        """Get all relationships for a specific context"""
        return [rel for rel in self.relationships if rel.upstream_context == context or rel.downstream_context == context]

    def get_upstream_contexts(self, context: str) -> List[str]:
        """Get upstream contexts for a given context"""
        return [rel.upstream_context for rel in self.relationships if rel.downstream_context == context]

    def get_downstream_contexts(self, context: str) -> List[str]:
        """Get downstream contexts for a given context"""
        return [rel.downstream_context for rel in self.relationships if rel.upstream_context == context]


class ContextMapAnalyzer:
    """Analyzes code to generate context maps"""

    def __init__(self):
        self.relationship_indicators = {
            RelationshipType.UPSTREAM_DOWNSTREAM: ["import", "from", "depends", "requires", "uses", "calls"],
            RelationshipType.CUSTOMER_SUPPLIER: ["api", "interface", "contract", "service", "client"],
            RelationshipType.CONFORMIST: ["adapter", "wrapper", "converter", "mapper", "transformer"],
            RelationshipType.ANTICORRUPTION_LAYER: ["facade", "gateway", "bridge", "translator", "anti-corruption"],
            RelationshipType.OPEN_HOST_SERVICE: ["public", "open", "host", "service", "endpoint"],
            RelationshipType.PUBLISHED_LANGUAGE: ["schema", "protocol", "standard", "format", "specification"],
            RelationshipType.SHARED_KERNEL: ["shared", "common", "kernel", "core", "base"],
            RelationshipType.PARTNER: ["collaborate", "coordinate", "sync", "integrate", "partner"],
        }

        self.interface_patterns = ["api", "interface", "service", "client", "adapter", "facade", "gateway", "bridge", "mapper", "converter", "translator"]

        self.data_flow_patterns = ["event", "message", "command", "query", "request", "response", "data", "payload", "entity", "dto", "model", "schema"]

    def analyze_file(self, tree: ast.AST, file_path: str, context_name: str) -> List[ContextRelationship]:
        """Analyze file for context relationships"""
        relationships = []

        # Analyze imports for dependencies
        import_relationships = self._analyze_imports(tree, context_name)
        relationships.extend(import_relationships)

        # Analyze class definitions for interfaces
        interface_relationships = self._analyze_interfaces(tree, context_name)
        relationships.extend(interface_relationships)

        # Analyze function calls for service relationships
        service_relationships = self._analyze_service_calls(tree, context_name)
        relationships.extend(service_relationships)

        # Analyze data flow patterns
        data_flow_relationships = self._analyze_data_flow(tree, context_name)
        relationships.extend(data_flow_relationships)

        return relationships

    def _analyze_imports(self, tree: ast.AST, context_name: str) -> List[ContextRelationship]:
        """Analyze imports for context dependencies"""
        relationships = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target_context = self._extract_context_from_module(alias.name)
                    if target_context and target_context != context_name:
                        relationship = ContextRelationship(upstream_context=target_context, downstream_context=context_name, relationship_type=RelationshipType.UPSTREAM_DOWNSTREAM, confidence=0.8)
                        relationship.add_evidence(f"Import from {alias.name}")
                        relationships.append(relationship)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    target_context = self._extract_context_from_module(node.module)
                    if target_context and target_context != context_name:
                        relationship = ContextRelationship(upstream_context=target_context, downstream_context=context_name, relationship_type=RelationshipType.UPSTREAM_DOWNSTREAM, confidence=0.9)
                        relationship.add_evidence(f"Import from {node.module}")
                        relationships.append(relationship)

        return relationships

    def _analyze_interfaces(self, tree: ast.AST, context_name: str) -> List[ContextRelationship]:
        """Analyze class definitions for interface relationships"""
        relationships = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Check for interface patterns
                if self._is_interface_class(class_name):
                    # Look for usage patterns to determine relationship type
                    relationship_type = self._determine_interface_relationship_type(class_name)

                    # Find target context (this is simplified - in reality would need more analysis)
                    target_context = self._infer_target_context_from_interface(class_name)

                    if target_context and target_context != context_name:
                        relationship = ContextRelationship(upstream_context=target_context, downstream_context=context_name, relationship_type=relationship_type, confidence=0.7)
                        relationship.add_interface(class_name)
                        relationship.add_evidence(f"Interface class: {class_name}")
                        relationships.append(relationship)

        return relationships

    def _analyze_service_calls(self, tree: ast.AST, context_name: str) -> List[ContextRelationship]:
        """Analyze function calls for service relationships"""
        relationships = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Analyze service calls
                if isinstance(node.func, ast.Attribute):
                    service_name = node.func.attr
                    if self._is_service_call(service_name):
                        target_context = self._infer_context_from_service_call(service_name)

                        if target_context and target_context != context_name:
                            relationship = ContextRelationship(upstream_context=target_context, downstream_context=context_name, relationship_type=RelationshipType.CUSTOMER_SUPPLIER, confidence=0.6)
                            relationship.add_evidence(f"Service call: {service_name}")
                            relationships.append(relationship)

        return relationships

    def _analyze_data_flow(self, tree: ast.AST, context_name: str) -> List[ContextRelationship]:
        """Analyze data flow patterns"""
        relationships = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Check for data transfer objects
                if self._is_data_transfer_object(class_name):
                    target_context = self._infer_context_from_data_object(class_name)

                    if target_context and target_context != context_name:
                        relationship = ContextRelationship(upstream_context=target_context, downstream_context=context_name, relationship_type=RelationshipType.CONFORMIST, confidence=0.5)
                        relationship.add_data_flow(class_name)
                        relationship.add_evidence(f"Data flow: {class_name}")
                        relationships.append(relationship)

        return relationships

    def _extract_context_from_module(self, module_name: str) -> Optional[str]:
        """Extract context name from module name"""
        # Simple heuristic - in reality would need more sophisticated analysis
        parts = module_name.split(".")

        # Look for domain indicators
        for part in parts:
            if any(keyword in part.lower() for keyword in ["domain", "service", "api", "client"]):
                return part.lower()

        # Use first part as context
        return parts[0].lower() if parts else None

    def _is_interface_class(self, class_name: str) -> bool:
        """Check if class is an interface"""
        interface_indicators = ["interface", "api", "client", "adapter", "facade"]
        return any(indicator in class_name.lower() for indicator in interface_indicators)

    def _determine_interface_relationship_type(self, class_name: str) -> RelationshipType:
        """Determine relationship type from interface class name"""
        class_name_lower = class_name.lower()

        if "adapter" in class_name_lower or "facade" in class_name_lower:
            return RelationshipType.ANTICORRUPTION_LAYER
        elif "api" in class_name_lower or "client" in class_name_lower:
            return RelationshipType.CUSTOMER_SUPPLIER
        elif "interface" in class_name_lower:
            return RelationshipType.UPSTREAM_DOWNSTREAM
        else:
            return RelationshipType.CONFORMIST

    def _infer_target_context_from_interface(self, class_name: str) -> Optional[str]:
        """Infer target context from interface class name"""
        # Simple heuristic - in reality would need more sophisticated analysis
        parts = class_name.split("_")

        for part in parts:
            if any(keyword in part.lower() for keyword in ["user", "order", "product", "payment"]):
                return part.lower()

        return None

    def _is_service_call(self, service_name: str) -> bool:
        """Check if function call is a service call"""
        service_indicators = ["get", "post", "put", "delete", "call", "invoke", "send"]
        return any(indicator in service_name.lower() for indicator in service_indicators)

    def _infer_context_from_service_call(self, service_name: str) -> Optional[str]:
        """Infer context from service call name"""
        # Simple heuristic - in reality would need more sophisticated analysis
        if "user" in service_name.lower():
            return "user"
        elif "order" in service_name.lower():
            return "order"
        elif "product" in service_name.lower():
            return "product"
        elif "payment" in service_name.lower():
            return "payment"

        return None

    def _is_data_transfer_object(self, class_name: str) -> bool:
        """Check if class is a data transfer object"""
        dto_indicators = ["dto", "model", "entity", "data", "payload", "request", "response"]
        return any(indicator in class_name.lower() for indicator in dto_indicators)

    def _infer_context_from_data_object(self, class_name: str) -> Optional[str]:
        """Infer context from data object name"""
        # Simple heuristic - in reality would need more sophisticated analysis
        if "user" in class_name.lower():
            return "user"
        elif "order" in class_name.lower():
            return "order"
        elif "product" in class_name.lower():
            return "product"
        elif "payment" in class_name.lower():
            return "payment"

        return None

    def build_context_map(self, context_analyses: Dict[str, List[ContextRelationship]]) -> ContextMap:
        """Build context map from multiple context analyses"""
        context_map = ContextMap()

        # Add all contexts
        for context_name in context_analyses.keys():
            context_map.add_context(context_name)

        # Add all relationships
        for context_name, relationships in context_analyses.items():
            for relationship in relationships:
                context_map.add_relationship(relationship)

        # Identify shared kernels
        context_map.shared_kernels = self._identify_shared_kernels(context_map)

        # Identify anti-corruption layers
        context_map.anticorruption_layers = self._identify_anticorruption_layers(context_map)

        # Identify open host services
        context_map.open_host_services = self._identify_open_host_services(context_map)

        # Identify published languages
        context_map.published_languages = self._identify_published_languages(context_map)

        return context_map

    def _identify_shared_kernels(self, context_map: ContextMap) -> List[str]:
        """Identify shared kernels in context map"""
        shared_kernels = []

        # Look for contexts that are shared between multiple other contexts
        context_usage = {}
        for relationship in context_map.relationships:
            upstream = relationship.upstream_context
            if upstream not in context_usage:
                context_usage[upstream] = set()
            context_usage[upstream].add(relationship.downstream_context)

        # Contexts used by multiple other contexts are potential shared kernels
        for context, users in context_usage.items():
            if len(users) > 1:
                shared_kernels.append(context)

        return shared_kernels

    def _identify_anticorruption_layers(self, context_map: ContextMap) -> List[str]:
        """Identify anti-corruption layers in context map"""
        acl_contexts = []

        for relationship in context_map.relationships:
            if relationship.relationship_type == RelationshipType.ANTICORRUPTION_LAYER:
                acl_contexts.append(relationship.downstream_context)

        return list(set(acl_contexts))

    def _identify_open_host_services(self, context_map: ContextMap) -> List[str]:
        """Identify open host services in context map"""
        ohs_contexts = []

        for relationship in context_map.relationships:
            if relationship.relationship_type == RelationshipType.OPEN_HOST_SERVICE:
                ohs_contexts.append(relationship.upstream_context)

        return list(set(ohs_contexts))

    def _identify_published_languages(self, context_map: ContextMap) -> List[str]:
        """Identify published languages in context map"""
        pl_contexts = []

        for relationship in context_map.relationships:
            if relationship.relationship_type == RelationshipType.PUBLISHED_LANGUAGE:
                pl_contexts.append(relationship.upstream_context)

        return list(set(pl_contexts))

    def generate_context_map_report(self, context_map: ContextMap) -> Dict[str, Any]:
        """Generate comprehensive context map report"""
        return {
            "contexts": context_map.contexts,
            "relationships": [
                {
                    "upstream": rel.upstream_context,
                    "downstream": rel.downstream_context,
                    "type": rel.relationship_type.value,
                    "confidence": rel.confidence,
                    "evidence": rel.evidence,
                    "interfaces": rel.interfaces,
                    "data_flow": rel.data_flow,
                }
                for rel in context_map.relationships
            ],
            "shared_kernels": context_map.shared_kernels,
            "anticorruption_layers": context_map.anticorruption_layers,
            "open_host_services": context_map.open_host_services,
            "published_languages": context_map.published_languages,
            "recommendations": self._generate_context_map_recommendations(context_map),
        }

    def _generate_context_map_recommendations(self, context_map: ContextMap) -> List[str]:
        """Generate recommendations for context map improvements"""
        recommendations = []

        # Check for circular dependencies
        circular_deps = self._find_circular_dependencies(context_map)
        if circular_deps:
            recommendations.append("Resolve circular dependencies between contexts")

        # Check for missing anti-corruption layers
        if not context_map.anticorruption_layers:
            recommendations.append("Consider adding anti-corruption layers for external integrations")

        # Check for shared kernel usage
        if len(context_map.shared_kernels) > 2:
            recommendations.append("Review shared kernel usage - consider reducing coupling")

        # Check for relationship confidence
        low_confidence_rels = [rel for rel in context_map.relationships if rel.confidence < 0.5]
        if low_confidence_rels:
            recommendations.append("Investigate low-confidence relationships")

        return recommendations

    def _find_circular_dependencies(self, context_map: ContextMap) -> List[List[str]]:
        """Find circular dependencies in context map"""
        # Simple cycle detection - in reality would need more sophisticated algorithm
        circular_deps = []

        for context in context_map.contexts:
            visited = set()
            path = []

            if self._has_cycle(context, context_map, visited, path):
                circular_deps.append(path)

        return circular_deps

    def _has_cycle(self, context: str, context_map: ContextMap, visited: set, path: List[str]) -> bool:
        """Check if context has circular dependency"""
        if context in visited:
            return context in path

        visited.add(context)
        path.append(context)

        # Check downstream contexts
        downstream_contexts = context_map.get_downstream_contexts(context)
        for downstream in downstream_contexts:
            if self._has_cycle(downstream, context_map, visited, path):
                return True

        path.pop()
        return False
