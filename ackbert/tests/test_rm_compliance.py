"""Tests for RM compliance in Ack-Bert framework."""

import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from ackbert.rm_base import AckBertReflectiveModule
from ackbert.ontology import OntologyManager
from ackbert.comparison import ComparisonEngine


class TestAckBertReflectiveModule:
    """Test cases for AckBertReflectiveModule base class."""

    def test_rm_module_initialization(self):
        """Test RM module initialization."""
        module = AckBertReflectiveModule("TestModule")

        assert module.module_name == "TestModule"
        assert module._error_count == 0
        assert module._success_count == 0
        assert module._is_operational is True

    def test_rm_operation_logging(self):
        """Test RM operation logging."""
        module = AckBertReflectiveModule("TestModule")

        # Log successful operation
        module.log_operation(True, "test_operation", "Test details")
        assert module._success_count == 1
        assert module._error_count == 0

        # Log failed operation
        module.log_operation(False, "test_operation", "Test error")
        assert module._success_count == 1
        assert module._error_count == 1

    def test_rm_health_status(self):
        """Test RM health status reporting."""
        module = AckBertReflectiveModule("TestModule")

        health = module.get_health_status()
        assert "module_name" in health
        assert "status" in health
        assert "metrics" in health
        assert "capabilities" in health
        assert health["module_name"] == "TestModule"

    def test_rm_self_validation(self):
        """Test RM self-validation."""
        module = AckBertReflectiveModule("TestModule")

        # Should pass validation initially
        assert module.validate_self() is True

        # Should fail with invalid state
        module._error_count = -1
        assert module.validate_self() is False

    def test_rm_operational_metrics(self):
        """Test RM operational metrics."""
        module = AckBertReflectiveModule("TestModule")

        # Log some operations
        module.log_operation(True, "op1")
        module.log_operation(False, "op2")
        module.log_operation(True, "op3")

        metrics = module.get_operational_metrics()
        assert metrics["total_operations"] == 3
        assert metrics["success_count"] == 2
        assert metrics["error_count"] == 1
        assert metrics["success_rate"] == 2 / 3
        assert metrics["error_rate"] == 1 / 3

    def test_rm_health_check(self):
        """Test RM health check."""
        module = AckBertReflectiveModule("TestModule")

        # Should be healthy initially
        assert module.is_healthy() is True

        # Should still be healthy with some errors
        module.log_operation(False, "test_error")
        assert module.is_healthy() is True

        # Should be unhealthy with too many errors
        for _ in range(10):
            module.log_operation(False, "test_error")
        assert module.is_healthy() is False

    def test_rm_metrics_reset(self):
        """Test RM metrics reset."""
        module = AckBertReflectiveModule("TestModule")

        # Log some operations
        module.log_operation(True, "op1")
        module.log_operation(False, "op2")

        # Reset metrics
        module.reset_metrics()

        assert module._error_count == 0
        assert module._success_count == 0
        assert module._operation_count == 0


class TestOntologyManagerRMCompliance:
    """Test RM compliance in OntologyManager."""

    def _create_test_ontology(self) -> Path:
        """Create a test ontology file."""
        ontology_content = """@prefix ab: <http://example.org/ackbert#> .
@prefix cand: <http://example.org/candidate#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ab:Candidate a owl:Class ; rdfs:label "Candidate" .
ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .
ab:EvidenceStrength a owl:Class ; rdfs:label "Evidence Strength Level" .

ab:Level1 a ab:EvidenceStrength ; ab:level 1 ; ab:label "Self-asserted" .

jd:TestReq a ab:JDRequirement ; rdfs:label "Test Requirement" .

cand:TestCandidate a ab:Candidate ;
    rdfs:label "Test Candidate" ;
    ab:hasEvidenceStrength ab:Level1 ;
    ab:showsStrength jd:TestReq .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            return Path(f.name)

    def test_ontology_manager_rm_initialization(self):
        """Test OntologyManager RM initialization."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)

            # Check RM compliance
            assert hasattr(ontology, "module_name")
            assert ontology.module_name == "OntologyManager"
            assert ontology.is_healthy() is True

            # Check that initialization was logged
            metrics = ontology.get_operational_metrics()
            assert metrics["success_count"] >= 1  # At least initialization logged

        finally:
            ontology_path.unlink()

    def test_ontology_manager_rm_operation_logging(self):
        """Test OntologyManager RM operation logging."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)

            # Get candidates (should log operation)
            candidates = ontology.get_candidates()

            # Check that operation was logged
            metrics = ontology.get_operational_metrics()
            assert metrics["success_count"] >= 2  # Initialization + get_candidates

        finally:
            ontology_path.unlink()

    def test_ontology_manager_rm_health_status(self):
        """Test OntologyManager RM health status."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)

            health = ontology.get_health_status()
            assert health["module_name"] == "OntologyManager"
            assert "status" in health
            assert "metrics" in health
            assert "capabilities" in health

        finally:
            ontology_path.unlink()


class TestComparisonEngineRMCompliance:
    """Test RM compliance in ComparisonEngine."""

    def _create_test_ontology(self) -> Path:
        """Create a test ontology file."""
        ontology_content = """@prefix ab: <http://example.org/ackbert#> .
@prefix cand: <http://example.org/candidate#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ab:Candidate a owl:Class ; rdfs:label "Candidate" .
ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .
ab:EvidenceStrength a owl:Class ; rdfs:label "Evidence Strength Level" .

ab:Level1 a ab:EvidenceStrength ; ab:level 1 ; ab:label "Self-asserted" .

jd:TestReq a ab:JDRequirement ; rdfs:label "Test Requirement" .

cand:TestCandidate a ab:Candidate ;
    rdfs:label "Test Candidate" ;
    ab:hasEvidenceStrength ab:Level1 ;
    ab:showsStrength jd:TestReq .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            return Path(f.name)

    def test_comparison_engine_rm_initialization(self):
        """Test ComparisonEngine RM initialization."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            # Check RM compliance
            assert hasattr(engine, "module_name")
            assert engine.module_name == "ComparisonEngine"
            assert engine.is_healthy() is True

            # Check that initialization was logged
            metrics = engine.get_operational_metrics()
            assert metrics["success_count"] >= 1  # At least initialization logged

        finally:
            ontology_path.unlink()

    def test_comparison_engine_rm_operation_logging(self):
        """Test ComparisonEngine RM operation logging."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            # Generate comparison matrix (should log operation)
            matrix = engine.generate_comparison_matrix()

            # Check that operation was logged
            metrics = engine.get_operational_metrics()
            assert metrics["success_count"] >= 2  # Initialization + generate_comparison_matrix

        finally:
            ontology_path.unlink()

    def test_comparison_engine_rm_health_status(self):
        """Test ComparisonEngine RM health status."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            health = engine.get_health_status()
            assert health["module_name"] == "ComparisonEngine"
            assert "status" in health
            assert "metrics" in health
            assert "capabilities" in health

        finally:
            ontology_path.unlink()


class TestRMIntegration:
    """Test RM integration across Ack-Bert components."""

    def test_rm_diagnostic_info(self):
        """Test RM diagnostic information gathering."""
        module = AckBertReflectiveModule("TestModule")

        # Log some operations
        module.log_operation(True, "test_op1")
        module.log_operation(False, "test_op2")

        diagnostic = module.get_diagnostic_info()

        assert "module_name" in diagnostic
        assert "health_status" in diagnostic
        assert "operational_metrics" in diagnostic
        assert "capabilities" in diagnostic
        assert "is_healthy" in diagnostic
        assert "validation_passed" in diagnostic

        assert diagnostic["module_name"] == "TestModule"
        assert diagnostic["is_healthy"] is True
        assert diagnostic["validation_passed"] is True

    def test_rm_capabilities(self):
        """Test RM capabilities reporting."""
        module = AckBertReflectiveModule("TestModule")

        capabilities = module.get_capabilities()
        assert len(capabilities) > 0

        capability = capabilities[0]
        assert "name" in capability
        assert "description" in capability
        assert "available" in capability
        assert "version" in capability
