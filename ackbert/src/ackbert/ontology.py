"""
Ontology management for Ack-Bert framework.

Handles RDF/Turtle ontology loading, validation, and querying for
candidate comparison and evaluation workflows.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from urllib.parse import urljoin

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
from pydantic import BaseModel, Field

from .rm_base import AckBertReflectiveModule


class EvidenceStrength(BaseModel):
    """Evidence strength level model."""

    level: int = Field(ge=1, le=3, description="Evidence strength level (1-3)")
    label: str = Field(description="Human-readable label")
    description: Optional[str] = Field(None, description="Detailed description")

    @classmethod
    def level_1(cls) -> "EvidenceStrength":
        """Level 1: Self-asserted resume evidence."""
        return cls(level=1, label="Self-asserted resume evidence", description="Claims made in resume or application materials")

    @classmethod
    def level_2(cls) -> "EvidenceStrength":
        """Level 2: Partial demo / internal artifact."""
        return cls(level=2, label="Partial demo / internal artifact", description="Demonstrations or artifacts that show partial capability")

    @classmethod
    def level_3(cls) -> "EvidenceStrength":
        """Level 3: Third-party/public validation."""
        return cls(level=3, label="Third-party/public validation", description="Publicly available evidence or third-party validation")


class JDRequirement(BaseModel):
    """Job description requirement model."""

    name: str = Field(description="Requirement name")
    description: Optional[str] = Field(None, description="Requirement description")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Requirement weight")


class Candidate(BaseModel):
    """Candidate model."""

    name: str = Field(description="Candidate name")
    evidence_strength: EvidenceStrength = Field(description="Overall evidence strength")
    strengths: List[str] = Field(default_factory=list, description="Areas of strength")
    gaps: List[str] = Field(default_factory=list, description="Knowledge gaps")
    comment: Optional[str] = Field(None, description="Additional comments")


class OntologyManager(AckBertReflectiveModule):
    """Manages RDF ontology for Ack-Bert framework with RM compliance."""

    def __init__(self, ontology_path: Union[str, Path]):
        """Initialize ontology manager with RDF file."""
        super().__init__("OntologyManager")
        self.ontology_path = Path(ontology_path)
        self.graph = Graph()

        try:
            self._load_ontology()
            self._setup_namespaces()
            self.log_operation(True, "ontology_initialization", f"Loaded ontology from {ontology_path}")
        except Exception as e:
            self.log_operation(False, "ontology_initialization", str(e))
            raise

    def _load_ontology(self) -> None:
        """Load RDF ontology from file."""
        if not self.ontology_path.exists():
            raise FileNotFoundError(f"Ontology file not found: {self.ontology_path}")

        self.graph.parse(str(self.ontology_path), format="turtle")

    def _setup_namespaces(self) -> None:
        """Setup namespace bindings."""
        self.AB = Namespace("http://example.org/ackbert#")
        self.CAND = Namespace("http://example.org/candidate#")
        self.JD = Namespace("http://example.org/jd#")
        self.ART = Namespace("http://example.org/artifact#")

        self.graph.bind("ab", self.AB)
        self.graph.bind("cand", self.CAND)
        self.graph.bind("jd", self.JD)
        self.graph.bind("art", self.ART)

    def get_candidates(self) -> List[Candidate]:
        """Extract all candidates from ontology."""
        try:
            candidates = []

            for candidate_uri in self.graph.subjects(RDF.type, self.AB.Candidate):
                name = self._get_label(candidate_uri)
                evidence_strength = self._get_evidence_strength(candidate_uri)
                strengths = self._get_strengths(candidate_uri)
                gaps = self._get_gaps(candidate_uri)
                comment = self._get_comment(candidate_uri)

                candidates.append(Candidate(name=name, evidence_strength=evidence_strength, strengths=strengths, gaps=gaps, comment=comment))

            self.log_operation(True, "get_candidates", f"Extracted {len(candidates)} candidates")
            return candidates

        except Exception as e:
            self.log_operation(False, "get_candidates", str(e))
            raise

    def get_requirements(self) -> List[JDRequirement]:
        """Extract all job requirements from ontology."""
        requirements = []

        for req_uri in self.graph.subjects(RDF.type, self.AB.JDRequirement):
            name = self._get_label(req_uri)
            description = self._get_comment(req_uri)

            requirements.append(JDRequirement(name=name, description=description))

        return requirements

    def get_evidence_strengths(self) -> List[EvidenceStrength]:
        """Extract all evidence strength levels from ontology."""
        strengths = []

        for strength_uri in self.graph.subjects(RDF.type, self.AB.EvidenceStrength):
            level = self._get_level(strength_uri)
            label = self._get_label(strength_uri)
            description = self._get_comment(strength_uri)

            strengths.append(EvidenceStrength(level=level, label=label, description=description))

        return strengths

    def _get_label(self, uri: URIRef) -> str:
        """Get label for URI."""
        label = self.graph.value(uri, RDFS.label)
        return str(label) if label else str(uri).split("#")[-1]

    def _get_comment(self, uri: URIRef) -> Optional[str]:
        """Get comment for URI."""
        comment = self.graph.value(uri, RDFS.comment)
        return str(comment) if comment else None

    def _get_level(self, uri: URIRef) -> int:
        """Get level for evidence strength URI."""
        level = self.graph.value(uri, self.AB.level)
        return int(level) if level else 1

    def _get_evidence_strength(self, candidate_uri: URIRef) -> EvidenceStrength:
        """Get evidence strength for candidate."""
        strength_uri = self.graph.value(candidate_uri, self.AB.hasEvidenceStrength)
        if not strength_uri:
            return EvidenceStrength(level=1, label="Unknown")

        level = self._get_level(strength_uri)
        label = self._get_label(strength_uri)
        description = self._get_comment(strength_uri)

        return EvidenceStrength(level=level, label=label, description=description)

    def _get_strengths(self, candidate_uri: URIRef) -> List[str]:
        """Get strengths for candidate."""
        strengths = []
        for strength_uri in self.graph.objects(candidate_uri, self.AB.showsStrength):
            strengths.append(self._get_label(strength_uri))
        return strengths

    def _get_gaps(self, candidate_uri: URIRef) -> List[str]:
        """Get gaps for candidate."""
        gaps = []
        for gap_uri in self.graph.objects(candidate_uri, self.AB.lacksArtifact):
            gaps.append(self._get_label(gap_uri))
        return gaps

    def validate_ontology(self) -> List[str]:
        """Validate ontology structure and return any issues."""
        issues = []

        # Check for required classes
        required_classes = [self.AB.Candidate, self.AB.JDRequirement, self.AB.EvidenceStrength, self.AB.Artifact]

        for class_uri in required_classes:
            if not self.graph.subjects(RDF.type, class_uri):
                issues.append(f"No instances found for required class: {class_uri}")

        # Check for candidates with evidence strength
        for candidate_uri in self.graph.subjects(RDF.type, self.AB.Candidate):
            if not self.graph.value(candidate_uri, self.AB.hasEvidenceStrength):
                issues.append(f"Candidate {candidate_uri} missing evidence strength")

        return issues

    def export_candidates_to_dict(self) -> Dict[str, Dict]:
        """Export candidates to dictionary format."""
        candidates = {}

        for candidate in self.get_candidates():
            candidates[candidate.name] = {
                "evidence_strength": {"level": candidate.evidence_strength.level, "label": candidate.evidence_strength.label, "description": candidate.evidence_strength.description},
                "strengths": candidate.strengths,
                "gaps": candidate.gaps,
                "comment": candidate.comment,
            }

        return candidates

    def get_comparison_data(self) -> Dict:
        """Get structured data for comparison matrix generation."""
        return {
            "candidates": self.export_candidates_to_dict(),
            "requirements": {req.name: req.dict() for req in self.get_requirements()},
            "evidence_strengths": {str(es.level): es.dict() for es in self.get_evidence_strengths()},
        }
