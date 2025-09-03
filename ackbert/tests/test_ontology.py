"""Tests for ontology management functionality."""

import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from ackbert.ontology import OntologyManager, EvidenceStrength, JDRequirement, Candidate


class TestOntologyManager:
    """Test cases for OntologyManager class."""

    def test_load_ontology_success(self):
        """Test successful ontology loading."""
        # Create a minimal valid ontology
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
            temp_path = Path(f.name)

        try:
            ontology = OntologyManager(temp_path)
            assert ontology is not None
            assert ontology.graph is not None
        finally:
            temp_path.unlink()

    def test_load_ontology_file_not_found(self):
        """Test ontology loading with non-existent file."""
        with pytest.raises(FileNotFoundError):
            OntologyManager("non_existent_file.ttl")

    def test_get_candidates(self):
        """Test candidate extraction from ontology."""
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
            temp_path = Path(f.name)

        try:
            ontology = OntologyManager(temp_path)
            candidates = ontology.get_candidates()

            assert len(candidates) == 1
            assert candidates[0].name == "Test Candidate"
            assert candidates[0].evidence_strength.level == 1
            assert "Test Requirement" in candidates[0].strengths
        finally:
            temp_path.unlink()

    def test_get_requirements(self):
        """Test requirement extraction from ontology."""
        ontology_content = """@prefix ab: <http://example.org/ackbert#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .

jd:TestReq a ab:JDRequirement ; rdfs:label "Test Requirement" .
jd:AnotherReq a ab:JDRequirement ; rdfs:label "Another Requirement" .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            temp_path = Path(f.name)

        try:
            ontology = OntologyManager(temp_path)
            requirements = ontology.get_requirements()

            assert len(requirements) == 2
            req_names = [req.name for req in requirements]
            assert "Test Requirement" in req_names
            assert "Another Requirement" in req_names
        finally:
            temp_path.unlink()

    def test_validate_ontology_success(self):
        """Test successful ontology validation."""
        ontology_content = """@prefix ab: <http://example.org/ackbert#> .
@prefix cand: <http://example.org/candidate#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ab:Candidate a owl:Class ; rdfs:label "Candidate" .
ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .
ab:EvidenceStrength a owl:Class ; rdfs:label "Evidence Strength Level" .
ab:Artifact a owl:Class ; rdfs:label "Artifact" .

ab:Level1 a ab:EvidenceStrength ; ab:level 1 ; ab:label "Self-asserted" .

jd:TestReq a ab:JDRequirement ; rdfs:label "Test Requirement" .

cand:TestCandidate a ab:Candidate ;
    rdfs:label "Test Candidate" ;
    ab:hasEvidenceStrength ab:Level1 ;
    ab:showsStrength jd:TestReq .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            temp_path = Path(f.name)

        try:
            ontology = OntologyManager(temp_path)
            issues = ontology.validate_ontology()

            assert len(issues) == 0
        finally:
            temp_path.unlink()

    def test_validate_ontology_missing_evidence_strength(self):
        """Test ontology validation with missing evidence strength."""
        ontology_content = """@prefix ab: <http://example.org/ackbert#> .
@prefix cand: <http://example.org/candidate#> .
@prefix jd: <http://example.org/jd#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ab:Candidate a owl:Class ; rdfs:label "Candidate" .
ab:JDRequirement a owl:Class ; rdfs:label "Job Description Requirement" .

jd:TestReq a ab:JDRequirement ; rdfs:label "Test Requirement" .

cand:TestCandidate a ab:Candidate ;
    rdfs:label "Test Candidate" ;
    ab:showsStrength jd:TestReq .
"""

        with NamedTemporaryFile(mode="w", suffix=".ttl", delete=False) as f:
            f.write(ontology_content)
            temp_path = Path(f.name)

        try:
            ontology = OntologyManager(temp_path)
            issues = ontology.validate_ontology()

            assert len(issues) > 0
            assert any("missing evidence strength" in issue.lower() for issue in issues)
        finally:
            temp_path.unlink()


class TestEvidenceStrength:
    """Test cases for EvidenceStrength class."""

    def test_evidence_strength_creation(self):
        """Test EvidenceStrength object creation."""
        strength = EvidenceStrength(level=2, label="Test Level", description="Test description")

        assert strength.level == 2
        assert strength.label == "Test Level"
        assert strength.description == "Test description"

    def test_evidence_strength_level_validation(self):
        """Test EvidenceStrength level validation."""
        with pytest.raises(ValueError):
            EvidenceStrength(level=0, label="Invalid", description="Test")

        with pytest.raises(ValueError):
            EvidenceStrength(level=4, label="Invalid", description="Test")

    def test_evidence_strength_class_methods(self):
        """Test EvidenceStrength class methods."""
        level_1 = EvidenceStrength.level_1()
        assert level_1.level == 1
        assert "Self-asserted" in level_1.label

        level_2 = EvidenceStrength.level_2()
        assert level_2.level == 2
        assert "Partial demo" in level_2.label

        level_3 = EvidenceStrength.level_3()
        assert level_3.level == 3
        assert "Third-party" in level_3.label


class TestJDRequirement:
    """Test cases for JDRequirement class."""

    def test_jd_requirement_creation(self):
        """Test JDRequirement object creation."""
        req = JDRequirement(name="Test Requirement", description="Test description", weight=0.8)

        assert req.name == "Test Requirement"
        assert req.description == "Test description"
        assert req.weight == 0.8

    def test_jd_requirement_default_weight(self):
        """Test JDRequirement with default weight."""
        req = JDRequirement(name="Test Requirement")
        assert req.weight == 1.0

    def test_jd_requirement_weight_validation(self):
        """Test JDRequirement weight validation."""
        with pytest.raises(ValueError):
            JDRequirement(name="Test", weight=-0.1)

        with pytest.raises(ValueError):
            JDRequirement(name="Test", weight=1.1)


class TestCandidate:
    """Test cases for Candidate class."""

    def test_candidate_creation(self):
        """Test Candidate object creation."""
        evidence_strength = EvidenceStrength.level_2()
        candidate = Candidate(name="Test Candidate", evidence_strength=evidence_strength, strengths=["Requirement 1", "Requirement 2"], gaps=["Requirement 3"], comment="Test comment")

        assert candidate.name == "Test Candidate"
        assert candidate.evidence_strength.level == 2
        assert len(candidate.strengths) == 2
        assert len(candidate.gaps) == 1
        assert candidate.comment == "Test comment"

    def test_candidate_default_values(self):
        """Test Candidate with default values."""
        evidence_strength = EvidenceStrength.level_1()
        candidate = Candidate(name="Test Candidate", evidence_strength=evidence_strength)

        assert candidate.strengths == []
        assert candidate.gaps == []
        assert candidate.comment is None
