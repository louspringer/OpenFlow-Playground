"""Tests for comparison engine functionality."""

import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from ackbert.ontology import OntologyManager, EvidenceStrength, JDRequirement, Candidate
from ackbert.comparison import ComparisonEngine, ComparisonMatrix, RiskLevel, RecommendationType


class TestComparisonMatrix:
    """Test cases for ComparisonMatrix class."""

    def test_comparison_matrix_creation(self):
        """Test ComparisonMatrix object creation."""
        candidates = [
            Candidate(name="Candidate 1", evidence_strength=EvidenceStrength.level_2(), strengths=["Requirement 1"], gaps=["Requirement 2"]),
            Candidate(name="Candidate 2", evidence_strength=EvidenceStrength.level_1(), strengths=["Requirement 2"], gaps=["Requirement 1"]),
        ]

        requirements = [JDRequirement(name="Requirement 1"), JDRequirement(name="Requirement 2")]

        matrix = ComparisonMatrix(candidates, requirements)

        assert len(matrix.candidates) == 2
        assert len(matrix.requirements) == 2
        assert "Candidate 1" in matrix.matrix
        assert "Candidate 2" in matrix.matrix

    def test_comparison_matrix_mapping(self):
        """Test comparison matrix requirement mapping."""
        candidates = [Candidate(name="Test Candidate", evidence_strength=EvidenceStrength.level_2(), strengths=["Strength Req"], gaps=["Gap Req"])]

        requirements = [JDRequirement(name="Strength Req"), JDRequirement(name="Gap Req"), JDRequirement(name="Unknown Req")]

        matrix = ComparisonMatrix(candidates, requirements)

        assert matrix.matrix["Test Candidate"]["Strength Req"] == "✓ Strength"
        assert matrix.matrix["Test Candidate"]["Gap Req"] == "✗ Gap"
        assert matrix.matrix["Test Candidate"]["Unknown Req"] == "? Unknown"

    def test_comparison_matrix_summary(self):
        """Test comparison matrix summary generation."""
        candidates = [Candidate(name="Test Candidate", evidence_strength=EvidenceStrength.level_2(), strengths=["Req 1", "Req 2"], gaps=["Req 3"])]

        requirements = [JDRequirement(name="Req 1"), JDRequirement(name="Req 2"), JDRequirement(name="Req 3"), JDRequirement(name="Req 4")]

        matrix = ComparisonMatrix(candidates, requirements)
        summary = matrix.get_summary()

        assert summary["Test Candidate"]["strengths"] == 2
        assert summary["Test Candidate"]["gaps"] == 1
        assert summary["Test Candidate"]["unknown"] == 1


class TestComparisonEngine:
    """Test cases for ComparisonEngine class."""

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
ab:Level2 a ab:EvidenceStrength ; ab:level 2 ; ab:label "Partial demo" .
ab:Level3 a ab:EvidenceStrength ; ab:level 3 ; ab:label "Public validation" .

jd:LLMTraining a ab:JDRequirement ; rdfs:label "LLM Training" .
jd:Governance a ab:JDRequirement ; rdfs:label "Governance" .
jd:PostTraining a ab:JDRequirement ; rdfs:label "Post Training" .

cand:StrongCandidate a ab:Candidate ;
    rdfs:label "Strong Candidate" ;
    ab:hasEvidenceStrength ab:Level3 ;
    ab:showsStrength jd:LLMTraining, jd:Governance ;
    ab:lacksArtifact jd:PostTraining .

cand:WeakCandidate a ab:Candidate ;
    rdfs:label "Weak Candidate" ;
    ab:hasEvidenceStrength ab:Level1 ;
    ab:showsStrength jd:Governance ;
    ab:lacksArtifact jd:LLMTraining, jd:PostTraining .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            return Path(f.name)

    def test_comparison_engine_initialization(self):
        """Test ComparisonEngine initialization."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            assert engine.ontology is not None
            assert len(engine.candidates) == 2
            assert len(engine.requirements) == 3
        finally:
            ontology_path.unlink()

    def test_generate_comparison_matrix(self):
        """Test comparison matrix generation."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)
            matrix = engine.generate_comparison_matrix()

            assert matrix is not None
            assert "Strong Candidate" in matrix.matrix
            assert "Weak Candidate" in matrix.matrix
        finally:
            ontology_path.unlink()

    def test_assess_risks(self):
        """Test risk assessment generation."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)
            risks = engine.assess_risks()

            assert len(risks) == 2

            # Strong candidate should have lower risk
            strong_risk = next(r for r in risks if r.candidate_name == "Strong Candidate")
            weak_risk = next(r for r in risks if r.candidate_name == "Weak Candidate")

            # Risk levels should be different (strong < weak)
            risk_order = {RiskLevel.LOW: 1, RiskLevel.MEDIUM: 2, RiskLevel.HIGH: 3}
            assert risk_order[strong_risk.level] <= risk_order[weak_risk.level]
        finally:
            ontology_path.unlink()

    def test_synthesize_recommendations(self):
        """Test recommendation synthesis."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)
            recommendations = engine.synthesize_recommendations()

            assert len(recommendations) == 2

            # Strong candidate should get better recommendation
            strong_rec = next(r for r in recommendations if r.candidate_name == "Strong Candidate")
            weak_rec = next(r for r in recommendations if r.candidate_name == "Weak Candidate")

            # Strong candidate should get advance or keep_warm, weak should get reject or request_more_info
            assert strong_rec.type in [RecommendationType.ADVANCE, RecommendationType.KEEP_WARM]
            assert weak_rec.type in [RecommendationType.REJECT, RecommendationType.REQUEST_MORE_INFO]
        finally:
            ontology_path.unlink()

    def test_generate_report(self):
        """Test comprehensive report generation."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)
            report = engine.generate_report()

            assert "summary" in report
            assert "comparison_matrix" in report
            assert "risk_assessments" in report
            assert "recommendations" in report

            assert report["summary"]["total_candidates"] == 2
            assert report["summary"]["total_requirements"] == 3
        finally:
            ontology_path.unlink()

    def test_calculate_risk_level(self):
        """Test risk level calculation logic."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            # Test high risk candidate
            high_risk_candidate = Candidate(name="High Risk", evidence_strength=EvidenceStrength.level_1(), strengths=["One Strength"], gaps=["Gap 1", "Gap 2", "Gap 3"])

            risk_level = engine._calculate_risk_level(high_risk_candidate)
            assert risk_level == RiskLevel.HIGH

            # Test low risk candidate
            low_risk_candidate = Candidate(name="Low Risk", evidence_strength=EvidenceStrength.level_3(), strengths=["Strength 1", "Strength 2", "Strength 3"], gaps=["One Gap"])

            risk_level = engine._calculate_risk_level(low_risk_candidate)
            assert risk_level == RiskLevel.LOW
        finally:
            ontology_path.unlink()

    def test_determine_recommendation_type(self):
        """Test recommendation type determination."""
        ontology_path = self._create_test_ontology()

        try:
            ontology = OntologyManager(ontology_path)
            engine = ComparisonEngine(ontology)

            # Test advance recommendation
            advance_candidate = Candidate(name="Advance", evidence_strength=EvidenceStrength.level_3(), strengths=["S1", "S2", "S3"], gaps=[])

            from ackbert.comparison import RiskAssessment

            low_risk = RiskAssessment("Advance", RiskLevel.LOW, "Low risk", [])

            rec_type = engine._determine_recommendation_type(advance_candidate, low_risk)
            assert rec_type == RecommendationType.ADVANCE

            # Test reject recommendation
            reject_candidate = Candidate(name="Reject", evidence_strength=EvidenceStrength.level_1(), strengths=["S1"], gaps=["G1", "G2", "G3", "G4"])

            high_risk = RiskAssessment("Reject", RiskLevel.HIGH, "High risk", [])

            rec_type = engine._determine_recommendation_type(reject_candidate, high_risk)
            assert rec_type == RecommendationType.REJECT
        finally:
            ontology_path.unlink()
