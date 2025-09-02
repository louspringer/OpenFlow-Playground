#!/usr/bin/env python3
"""
Test suite for RM Compliance Checker

Tests the RM Compliance Checker Reflective Module functionality.
"""

import asyncio
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.project_management.rm_compliance_checker import RMComplianceChecker, RMComplianceLevel, DomainRMCompliance, RMImplementation, create_rm_compliance_checker


class TestRMComplianceChecker:
    """Test cases for RM Compliance Checker."""

    @pytest.fixture
    async def compliance_checker(self):
        """Create a test RM Compliance Checker."""
        checker = RMComplianceChecker(project_root=".")
        return checker

    @pytest.mark.asyncio
    async def test_module_status(self, compliance_checker):
        """Test getting module status."""
        status = await compliance_checker.get_module_status()

        assert status is not None
        assert hasattr(status, "status")
        assert hasattr(status, "capabilities")
        assert hasattr(status, "health_indicators")

    @pytest.mark.asyncio
    async def test_module_capabilities(self, compliance_checker):
        """Test getting module capabilities."""
        capabilities = await compliance_checker.get_module_capabilities()

        assert len(capabilities) > 0
        capability_names = [cap.name for cap in capabilities]
        assert "rm_compliance_assessment" in capability_names
        assert "rm_implementation_tracking" in capability_names
        assert "rm_compliance_reporting" in capability_names

    @pytest.mark.asyncio
    async def test_is_healthy(self, compliance_checker):
        """Test health check."""
        is_healthy = await compliance_checker.is_healthy()
        assert isinstance(is_healthy, bool)

    @pytest.mark.asyncio
    async def test_health_indicators(self, compliance_checker):
        """Test getting health indicators."""
        indicators = await compliance_checker.get_health_indicators()

        assert isinstance(indicators, dict)
        assert "total_domains_assessed" in indicators
        assert "overall_compliance_percentage" in indicators

    @pytest.mark.asyncio
    async def test_assess_domain_rm_compliance(self, compliance_checker):
        """Test assessing domain RM compliance."""
        # Test with a known domain
        compliance = await compliance_checker.assess_domain_rm_compliance("reflective_modules")

        assert isinstance(compliance, DomainRMCompliance)
        assert compliance.domain_name == "reflective_modules"
        assert compliance.compliance_level in [RMComplianceLevel.FULL, RMComplianceLevel.PARTIAL, RMComplianceLevel.NONE, RMComplianceLevel.UNKNOWN]

    @pytest.mark.asyncio
    async def test_assess_all_domains(self, compliance_checker):
        """Test assessing all domains."""
        results = await compliance_checker.assess_all_domains()

        assert isinstance(results, dict)
        assert len(results) > 0

        # Check that we have some known domains
        expected_domains = ["reflective_modules", "ghostbusters", "round_trip_engineering"]
        for domain in expected_domains:
            if domain in results:
                assert isinstance(results[domain], DomainRMCompliance)

    @pytest.mark.asyncio
    async def test_generate_compliance_report(self, compliance_checker):
        """Test generating compliance report."""
        report = await compliance_checker.generate_compliance_report()

        assert isinstance(report, dict)
        assert "summary" in report
        assert "compliance_groups" in report
        assert "domain_details" in report

        summary = report["summary"]
        assert "total_domains" in summary
        assert "fully_compliant" in summary
        assert "overall_compliance_percentage" in summary

    @pytest.mark.asyncio
    async def test_create_rm_compliance_checker(self):
        """Test creating RM compliance checker."""
        checker = await create_rm_compliance_checker(".")

        assert isinstance(checker, RMComplianceChecker)
        assert checker.project_root == Path(".")

    def test_rm_compliance_level_enum(self):
        """Test RM compliance level enum."""
        assert RMComplianceLevel.FULL.value == "full"
        assert RMComplianceLevel.PARTIAL.value == "partial"
        assert RMComplianceLevel.NONE.value == "none"
        assert RMComplianceLevel.UNKNOWN.value == "unknown"

    def test_rm_implementation_dataclass(self):
        """Test RM implementation dataclass."""
        impl = RMImplementation(file_path="test.py", class_name="TestClass", interface_type="ReflectiveModule", methods_implemented=["get_module_status"], is_abstract=False)

        assert impl.file_path == "test.py"
        assert impl.class_name == "TestClass"
        assert impl.interface_type == "ReflectiveModule"
        assert "get_module_status" in impl.methods_implemented
        assert impl.is_abstract is False

    def test_domain_rm_compliance_dataclass(self):
        """Test domain RM compliance dataclass."""
        compliance = DomainRMCompliance(
            domain_name="test_domain", compliance_level=RMComplianceLevel.FULL, implementation_count=5, requirements_count=10, rm_requirements_count=3, compliance_score=0.8
        )

        assert compliance.domain_name == "test_domain"
        assert compliance.compliance_level == RMComplianceLevel.FULL
        assert compliance.implementation_count == 5
        assert compliance.compliance_score == 0.8

    @pytest.mark.asyncio
    async def test_determine_compliance_level(self, compliance_checker):
        """Test compliance level determination."""
        # Test full compliance
        full_impls = [
            RMImplementation("test1.py", "Class1", "ReflectiveModule"),
            RMImplementation("test2.py", "Class2", "ReflectiveModule"),
            RMImplementation("test3.py", "Class3", "ReflectiveModule"),
        ]
        level = compliance_checker._determine_compliance_level(full_impls, 3)
        assert level == RMComplianceLevel.FULL

        # Test partial compliance
        partial_impls = [RMImplementation("test1.py", "Class1", "ReflectiveModule")]
        level = compliance_checker._determine_compliance_level(partial_impls, 1)
        assert level == RMComplianceLevel.PARTIAL

        # Test no compliance
        level = compliance_checker._determine_compliance_level([], 0)
        assert level == RMComplianceLevel.NONE

    def test_calculate_compliance_score(self, compliance_checker):
        """Test compliance score calculation."""
        # Test with implementations and requirements
        impls = [
            RMImplementation("test1.py", "Class1", "ReflectiveModule"),
            RMImplementation("test2.py", "Class2", "ReflectiveModule"),
        ]
        score = compliance_checker._calculate_compliance_score(impls, 2)
        assert 0.0 <= score <= 1.0

        # Test with no requirements
        score = compliance_checker._calculate_compliance_score(impls, 0)
        assert score == 0.0


class TestRMComplianceCheckerIntegration:
    """Integration tests for RM Compliance Checker."""

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test the complete RM compliance checking workflow."""
        checker = RMComplianceChecker(".")

        # Step 1: Check module health
        is_healthy = await checker.is_healthy()
        assert isinstance(is_healthy, bool)

        # Step 2: Get capabilities
        capabilities = await checker.get_module_capabilities()
        assert len(capabilities) > 0

        # Step 3: Assess a specific domain
        compliance = await checker.assess_domain_rm_compliance("reflective_modules")
        assert isinstance(compliance, DomainRMCompliance)

        # Step 4: Generate report
        report = await checker.generate_compliance_report()
        assert "summary" in report

        # Step 5: Verify cache is populated
        assert len(checker.domains_cache) > 0


if __name__ == "__main__":
    pytest.main([__file__])
