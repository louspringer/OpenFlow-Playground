"""
Evidence collection and management for Ack-Bert framework.

Handles evidence gathering, strength assessment, and validation.
"""

from typing import Dict, List, Optional, Set, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class EvidenceSource(str, Enum):
    """Evidence source types."""

    RESUME = "resume"
    PORTFOLIO = "portfolio"
    PUBLIC_REPOSITORY = "public_repository"
    PUBLICATION = "publication"
    DEMO = "demo"
    REFERENCE = "reference"
    INTERVIEW = "interview"


class EvidenceStrength(BaseModel):
    """Evidence strength model."""

    level: int = Field(ge=1, le=3, description="Evidence strength level (1-3)")
    label: str = Field(description="Human-readable label")
    description: str = Field(description="Detailed description")

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


@dataclass
class EvidenceItem:
    """Individual evidence item."""

    source: EvidenceSource
    content: str
    strength: EvidenceStrength
    requirements_covered: Set[str]
    url: Optional[str] = None
    date: Optional[str] = None
    validated: bool = False


class EvidenceCollector:
    """Collects and manages evidence for candidates."""

    def __init__(self):
        self.evidence_items: Dict[str, List[EvidenceItem]] = {}
        self.requirements_map: Dict[str, Set[str]] = {}

    def add_candidate(self, candidate_name: str) -> None:
        """Add a new candidate to track."""
        if candidate_name not in self.evidence_items:
            self.evidence_items[candidate_name] = []

    def add_evidence(
        self, candidate_name: str, source: EvidenceSource, content: str, requirements_covered: Set[str], strength: EvidenceStrength, url: Optional[str] = None, date: Optional[str] = None
    ) -> None:
        """Add evidence item for a candidate."""
        if candidate_name not in self.evidence_items:
            self.add_candidate(candidate_name)

        evidence = EvidenceItem(source=source, content=content, strength=strength, requirements_covered=requirements_covered, url=url, date=date)

        self.evidence_items[candidate_name].append(evidence)

        # Update requirements mapping
        if candidate_name not in self.requirements_map:
            self.requirements_map[candidate_name] = set()
        self.requirements_map[candidate_name].update(requirements_covered)

    def get_candidate_evidence(self, candidate_name: str) -> List[EvidenceItem]:
        """Get all evidence for a candidate."""
        return self.evidence_items.get(candidate_name, [])

    def get_evidence_summary(self, candidate_name: str) -> Dict:
        """Get evidence summary for a candidate."""
        evidence = self.get_candidate_evidence(candidate_name)

        if not evidence:
            return {"total_items": 0, "strength_distribution": {}, "sources": {}, "requirements_covered": [], "overall_strength": EvidenceStrength.level_1()}

        # Calculate strength distribution
        strength_dist = {}
        sources = {}
        all_requirements = set()

        for item in evidence:
            level = item.strength.level
            strength_dist[level] = strength_dist.get(level, 0) + 1

            source = item.source.value
            sources[source] = sources.get(source, 0) + 1

            all_requirements.update(item.requirements_covered)

        # Determine overall strength (highest level with evidence)
        max_level = max(strength_dist.keys()) if strength_dist else 1
        overall_strength = EvidenceStrength.level_1()
        if max_level == 2:
            overall_strength = EvidenceStrength.level_2()
        elif max_level == 3:
            overall_strength = EvidenceStrength.level_3()

        return {"total_items": len(evidence), "strength_distribution": strength_dist, "sources": sources, "requirements_covered": list(all_requirements), "overall_strength": overall_strength}

    def identify_gaps(self, candidate_name: str, all_requirements: Set[str]) -> Set[str]:
        """Identify requirements not covered by evidence."""
        covered = self.requirements_map.get(candidate_name, set())
        return all_requirements - covered

    def validate_evidence(self, candidate_name: str) -> List[str]:
        """Validate evidence for a candidate and return issues."""
        issues = []
        evidence = self.get_candidate_evidence(candidate_name)

        if not evidence:
            issues.append("No evidence found for candidate")
            return issues

        # Check for minimum evidence requirements
        level_3_count = sum(1 for item in evidence if item.strength.level == 3)
        if level_3_count == 0:
            issues.append("No Level 3 (public/validated) evidence found")

        # Check for diverse sources
        sources = set(item.source for item in evidence)
        if len(sources) < 2:
            issues.append("Limited evidence sources (less than 2)")

        # Check for recent evidence
        # TODO: Implement date-based validation when dates are available

        return issues

    def export_to_dict(self) -> Dict:
        """Export all evidence to dictionary format."""
        result = {}

        for candidate_name, evidence_list in self.evidence_items.items():
            result[candidate_name] = {
                "evidence": [
                    {
                        "source": item.source.value,
                        "content": item.content,
                        "strength": {"level": item.strength.level, "label": item.strength.label, "description": item.strength.description},
                        "requirements_covered": list(item.requirements_covered),
                        "url": item.url,
                        "date": item.date,
                        "validated": item.validated,
                    }
                    for item in evidence_list
                ],
                "summary": self.get_evidence_summary(candidate_name),
            }

        return result

    def load_from_resume(self, candidate_name: str, resume_path: Union[str, Path]) -> None:
        """Load evidence from resume file (placeholder implementation)."""
        # TODO: Implement resume parsing
        # This would extract claims and map them to requirements
        pass

    def load_from_portfolio(self, candidate_name: str, portfolio_url: str) -> None:
        """Load evidence from portfolio URL (placeholder implementation)."""
        # TODO: Implement portfolio scraping
        # This would extract projects and map them to requirements
        pass

    def load_from_repository(self, candidate_name: str, repo_url: str) -> None:
        """Load evidence from public repository (placeholder implementation)."""
        # TODO: Implement repository analysis
        # This would analyze code, commits, issues, etc.
        pass

    def generate_evidence_report(self, candidate_name: str) -> Dict:
        """Generate comprehensive evidence report for a candidate."""
        evidence = self.get_candidate_evidence(candidate_name)
        summary = self.get_evidence_summary(candidate_name)
        issues = self.validate_evidence(candidate_name)

        return {
            "candidate": candidate_name,
            "summary": summary,
            "evidence_items": [
                {
                    "source": item.source.value,
                    "content": item.content[:200] + "..." if len(item.content) > 200 else item.content,
                    "strength": item.strength.label,
                    "requirements": list(item.requirements_covered),
                    "url": item.url,
                }
                for item in evidence
            ],
            "validation_issues": issues,
            "recommendations": self._generate_evidence_recommendations(candidate_name, issues),
        }

    def _generate_evidence_recommendations(self, candidate_name: str, issues: List[str]) -> List[str]:
        """Generate recommendations based on evidence issues."""
        recommendations = []

        if "No Level 3 evidence found" in issues:
            recommendations.append("Request public repositories, publications, or demos")

        if "Limited evidence sources" in issues:
            recommendations.append("Gather evidence from multiple sources (resume, portfolio, references)")

        if "No evidence found" in issues:
            recommendations.append("Request candidate to provide evidence materials")

        return recommendations
