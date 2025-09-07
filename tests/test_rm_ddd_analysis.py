"""
Tests for RM-DDD Analysis System

Comprehensive tests for all analysis components.
"""

import pytest
import ast
from unittest.mock import Mock, patch
from src.rm_ddd.analysis import (
    CodebaseAnalyzer,
    AnalysisResult,
    DDDDetector,
    DDDPattern,
    RMComplianceAnalyzer,
    ComplianceReport,
    BoundedContextAnalyzer,
    ContextAnalysis,
    UbiquitousLanguageAnalyzer,
    LanguageAnalysis,
    ComplexityAnalyzer,
    ComplexityReport,
    ContextMapAnalyzer,
    ContextMap,
    ContextRelationship,
    RelationshipType,
)


class TestDDDDetector:
    """Test DDD pattern detection"""

    def test_entity_detection(self):
        """Test entity pattern detection"""
        detector = DDDDetector()

        # Test entity class with ID field
        entity_code = """
class User:
    def __init__(self, user_id: str):
        self.id = user_id
        self.name = ""
"""
        tree = ast.parse(entity_code)
        patterns = detector.detect_patterns(tree, "test.py")

        assert len(patterns) > 0
        entity_patterns = [p for p in patterns if p.pattern_type.value == "entity"]
        assert len(entity_patterns) > 0
        assert entity_patterns[0].class_name == "User"

    def test_value_object_detection(self):
        """Test value object pattern detection"""
        detector = DDDDetector()

        # Test value object class with dataclass and frozen
        vo_code = """
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str
"""
        tree = ast.parse(vo_code)
        patterns = detector.detect_patterns(tree, "test.py")

        assert len(patterns) > 0
        vo_patterns = [p for p in patterns if p.pattern_type.value == "value_object"]
        assert len(vo_patterns) > 0
        assert vo_patterns[0].class_name == "Money"

    def test_aggregate_detection(self):
        """Test aggregate pattern detection"""
        detector = DDDDetector()

        # Test aggregate class with domain events and business methods
        aggregate_code = """
class Order:
    def __init__(self, order_id: str):
        self.id = order_id
        self.items = []
        self.status = "pending"
        self._domain_events = []
    
    def add_item(self, item):
        self.items.append(item)
        self._domain_events.append("OrderItemAdded")
    
    def validate_invariants(self):
        return len(self.items) > 0
    
    def handle_command(self, command):
        pass
"""
        tree = ast.parse(aggregate_code)
        patterns = detector.detect_patterns(tree, "test.py")

        assert len(patterns) > 0
        aggregate_patterns = [p for p in patterns if p.pattern_type.value == "aggregate_root"]
        assert len(aggregate_patterns) > 0
        assert aggregate_patterns[0].class_name == "Order"


class TestRMComplianceAnalyzer:
    """Test RM compliance analysis"""

    def test_rm_compliance_detection(self):
        """Test RM compliance detection"""
        analyzer = RMComplianceAnalyzer()

        # Test RM-compliant class
        rm_code = """
from src.rm_ddd.core.base import ReflectiveModuleBase

class MyModule(ReflectiveModuleBase):
    def __init__(self):
        super().__init__()
        self.module_id = "my_module"
    
    async def get_module_status(self):
        return ModuleHealth(status="available")
    
    async def is_healthy(self):
        return True
    
    async def get_health_indicators(self):
        return {"uptime": 100}
"""
        tree = ast.parse(rm_code)
        report = analyzer.analyze_file(tree, "test.py")

        assert report is not None
        assert report.compliance_percentage > 0

    def test_non_compliant_detection(self):
        """Test non-compliant class detection"""
        analyzer = RMComplianceAnalyzer()

        # Test non-compliant class
        non_rm_code = """
class RegularClass:
    def some_method(self):
        return "hello"
"""
        tree = ast.parse(non_rm_code)
        report = analyzer.analyze_file(tree, "test.py")

        assert report is not None
        assert report.compliance_percentage == 0


class TestBoundedContextAnalyzer:
    """Test bounded context analysis"""

    def test_context_detection(self):
        """Test bounded context detection"""
        analyzer = BoundedContextAnalyzer()

        # Test domain-focused code
        domain_code = """
class UserService:
    def create_user(self, user_data):
        pass
    
    def get_user(self, user_id):
        pass

class UserRepository:
    def save(self, user):
        pass
"""
        tree = ast.parse(domain_code)
        analysis = analyzer.analyze_file(tree, "user_domain.py")

        assert analysis is not None
        assert analysis.context_name is not None
        assert analysis.confidence > 0

    def test_context_confidence_calculation(self):
        """Test context confidence calculation"""
        analyzer = BoundedContextAnalyzer()

        # Test high-confidence context
        high_confidence_code = """
class UserEntity:
    def __init__(self, user_id):
        self.user_id = user_id

class UserValueObject:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        pass
"""
        tree = ast.parse(high_confidence_code)
        analysis = analyzer.analyze_file(tree, "user_domain.py")

        assert analysis is not None
        assert analysis.confidence > 0.5


class TestUbiquitousLanguageAnalyzer:
    """Test ubiquitous language analysis"""

    def test_domain_term_detection(self):
        """Test domain term detection"""
        analyzer = UbiquitousLanguageAnalyzer()

        # Test code with domain terms
        domain_code = """
class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.orders = []
    
    def place_order(self, order):
        self.orders.append(order)
"""
        tree = ast.parse(domain_code)
        analysis = analyzer.analyze_file(tree, "test.py")

        assert analysis is not None
        assert len(analysis.domain_terms) > 0
        assert "customer" in analysis.domain_terms

    def test_consistency_analysis(self):
        """Test language consistency analysis"""
        analyzer = UbiquitousLanguageAnalyzer()

        # Test code with inconsistent terminology
        inconsistent_code = """
class User:
    def __init__(self, user_id):
        self.user_id = user_id

class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
"""
        tree = ast.parse(inconsistent_code)
        analysis = analyzer.analyze_file(tree, "test.py")

        assert analysis is not None
        assert len(analysis.inconsistent_terms) > 0


class TestComplexityAnalyzer:
    """Test complexity analysis"""

    def test_function_complexity(self):
        """Test function complexity analysis"""
        analyzer = ComplexityAnalyzer()

        # Test complex function
        complex_code = """
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        return a + b + c + d + e
                    else:
                        return a + b + c + d
                else:
                    return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0
"""
        tree = ast.parse(complex_code)
        report = analyzer.analyze_file(tree, "test.py")

        assert report is not None
        assert len(report.complex_functions) > 0
        assert report.complex_functions[0]["name"] == "complex_function"

    def test_class_complexity(self):
        """Test class complexity analysis"""
        analyzer = ComplexityAnalyzer()

        # Test complex class
        complex_code = """
class ComplexClass:
    def method1(self):
        if True:
            if True:
                if True:
                    pass
    
    def method2(self):
        if True:
            if True:
                if True:
                    if True:
                        pass
    
    def method3(self):
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            pass
"""
        tree = ast.parse(complex_code)
        report = analyzer.analyze_file(tree, "test.py")

        assert report is not None
        assert len(report.complex_classes) > 0
        assert report.complex_classes[0]["name"] == "ComplexClass"


class TestContextMapAnalyzer:
    """Test context map analysis"""

    def test_relationship_detection(self):
        """Test context relationship detection"""
        analyzer = ContextMapAnalyzer()

        # Test code with imports
        import_code = """
from user_domain import UserService
from order_domain import OrderService

class PaymentService:
    def __init__(self):
        self.user_service = UserService()
        self.order_service = OrderService()
"""
        tree = ast.parse(import_code)
        relationships = analyzer.analyze_file(tree, "payment_domain.py", "payment")

        assert len(relationships) > 0
        assert any(rel.upstream_context == "user_domain" for rel in relationships)
        assert any(rel.upstream_context == "order_domain" for rel in relationships)

    def test_context_map_building(self):
        """Test context map building"""
        analyzer = ContextMapAnalyzer()

        # Mock context analyses
        context_analyses = {
            "user": [ContextRelationship(upstream_context="auth", downstream_context="user", relationship_type=RelationshipType.UPSTREAM_DOWNSTREAM, confidence=0.8)],
            "order": [ContextRelationship(upstream_context="user", downstream_context="order", relationship_type=RelationshipType.CUSTOMER_SUPPLIER, confidence=0.9)],
        }

        context_map = analyzer.build_context_map(context_analyses)

        assert len(context_map.contexts) == 2
        assert len(context_map.relationships) == 2
        assert "user" in context_map.contexts
        assert "order" in context_map.contexts


class TestCodebaseAnalyzer:
    """Test main codebase analyzer"""

    @pytest.mark.asyncio
    async def test_analyze_codebase(self):
        """Test codebase analysis"""
        analyzer = CodebaseAnalyzer()

        # Mock file system
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True

            with patch("pathlib.Path.rglob") as mock_rglob:
                mock_rglob.return_value = ["/test/test.py"]

                with patch(
                    "builtins.open",
                    mock_open_file_content(
                        """
class User:
    def __init__(self, user_id):
        self.id = user_id

class UserService:
    async def get_module_status(self):
        return "available"
    
    async def is_healthy(self):
        return True
    
    async def get_health_indicators(self):
        return {"users": 100}
"""
                    ),
                ):
                    result = await analyzer.analyze_codebase("/test")

                    assert result is not None
                    assert result.total_files == 1
                    assert result.analyzed_files == 1
                    assert result.overall_score > 0

    @pytest.mark.asyncio
    async def test_analyzer_health(self):
        """Test analyzer health status"""
        analyzer = CodebaseAnalyzer()

        health = await analyzer.get_module_status()
        assert health.status.value in ["available", "degraded", "unavailable"]
        assert health.message is not None
        assert len(health.capabilities) > 0

    @pytest.mark.asyncio
    async def test_analyzer_health_indicators(self):
        """Test analyzer health indicators"""
        analyzer = CodebaseAnalyzer()

        indicators = await analyzer.get_health_indicators()
        assert "cached_analyses" in indicators
        assert "domain_context" in indicators
        assert "analyzer_type" in indicators


def mock_open_file_content(content: str):
    """Mock file content for testing"""

    def mock_open(filename, mode="r", encoding="utf-8"):
        return Mock(read=Mock(return_value=content))

    return mock_open


class TestAnalysisResult:
    """Test analysis result functionality"""

    def test_analysis_result_creation(self):
        """Test analysis result creation"""
        result = AnalysisResult()

        assert result.timestamp is not None
        assert result.total_files == 0
        assert result.analyzed_files == 0
        assert len(result.ddd_patterns) == 0
        assert len(result.recommendations) == 0
        assert result.overall_score == 0.0

    def test_add_recommendation(self):
        """Test adding recommendations"""
        result = AnalysisResult()

        result.add_recommendation("Test recommendation")

        assert len(result.recommendations) == 1
        assert result.recommendations[0] == "Test recommendation"

    def test_calculate_overall_score(self):
        """Test overall score calculation"""
        result = AnalysisResult()

        # Add some mock data
        result.ddd_patterns = [DDDPattern("entity", "User", "test.py", 0.8, {}), DDDPattern("value_object", "Money", "test.py", 0.9, {})]

        result.rm_compliance = ComplianceReport(compliance_percentage=80.0)
        result.language_analysis = LanguageAnalysis(consistency_score=0.8)
        result.complexity_analysis = ComplexityReport(overall_complexity=0.3)

        score = result.calculate_overall_score()

        assert score > 0
        assert score <= 100


if __name__ == "__main__":
    pytest.main([__file__])
