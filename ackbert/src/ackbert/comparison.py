"""
Comparison engine for Ack-Bert framework.

Handles candidate comparison, matrix generation, and recommendation synthesis.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field

from .ontology import OntologyManager, Candidate, JDRequirement
from .rm_base import AckBertReflectiveModule


class RiskLevel(str, Enum):
    """Risk level enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecommendationType(str, Enum):
    """Recommendation type enumeration."""

    ADVANCE = "advance"
    KEEP_WARM = "keep_warm"
    REJECT = "reject"
    REQUEST_MORE_INFO = "request_more_info"


@dataclass
class RiskAssessment:
    """Risk assessment for a candidate."""

    candidate_name: str
    level: RiskLevel
    description: str
    mitigation_strategies: List[str]


@dataclass
class Recommendation:
    """Hiring recommendation."""

    candidate_name: str
    type: RecommendationType
    action: str
    reasoning: str
    next_steps: List[str]


class ComparisonMatrix:
    """Comparison matrix for candidates."""

    def __init__(self, candidates: List[Candidate], requirements: List[JDRequirement]):
        self.candidates = candidates
        self.requirements = requirements
        self.matrix = self._build_matrix()

    def _build_matrix(self) -> Dict[str, Dict[str, str]]:
        """Build comparison matrix."""
        matrix = {}

        for candidate in self.candidates:
            matrix[candidate.name] = {}

            # Map requirements to candidate strengths/gaps
            for req in self.requirements:
                if req.name in candidate.strengths:
                    matrix[candidate.name][req.name] = "✓ Strength"
                elif req.name in candidate.gaps:
                    matrix[candidate.name][req.name] = "✗ Gap"
                else:
                    matrix[candidate.name][req.name] = "? Unknown"

        return matrix

    def to_dict(self) -> Dict:
        """Convert matrix to dictionary."""
        return {"requirements": [req.name for req in self.requirements], "candidates": self.matrix}

    def get_summary(self) -> Dict[str, Dict[str, int]]:
        """Get summary statistics."""
        summary = {}

        for candidate_name, req_scores in self.matrix.items():
            summary[candidate_name] = {
                "strengths": sum(1 for score in req_scores.values() if "✓" in score),
                "gaps": sum(1 for score in req_scores.values() if "✗" in score),
                "unknown": sum(1 for score in req_scores.values() if "?" in score),
            }

        return summary


class ComparisonEngine(AckBertReflectiveModule):
    """Main comparison engine for Ack-Bert framework with RM compliance."""

    def __init__(self, ontology_manager: OntologyManager):
        super().__init__("ComparisonEngine")
        self.ontology = ontology_manager

        try:
            self.candidates = ontology_manager.get_candidates()
            self.requirements = ontology_manager.get_requirements()
            self.log_operation(True, "comparison_engine_initialization", f"Initialized with {len(self.candidates)} candidates and {len(self.requirements)} requirements")
        except Exception as e:
            self.log_operation(False, "comparison_engine_initialization", str(e))
            raise

    def generate_comparison_matrix(self) -> ComparisonMatrix:
        """Generate comparison matrix for all candidates."""
        try:
            matrix = ComparisonMatrix(self.candidates, self.requirements)
            self.log_operation(True, "generate_comparison_matrix", f"Generated matrix for {len(self.candidates)} candidates")
            return matrix
        except Exception as e:
            self.log_operation(False, "generate_comparison_matrix", str(e))
            raise

    def assess_risks(self) -> List[RiskAssessment]:
        """Assess risks for each candidate."""
        risks = []

        for candidate in self.candidates:
            risk_level = self._calculate_risk_level(candidate)
            description = self._generate_risk_description(candidate, risk_level)
            mitigation = self._generate_mitigation_strategies(candidate, risk_level)

            risks.append(RiskAssessment(candidate_name=candidate.name, level=risk_level, description=description, mitigation_strategies=mitigation))

        return risks

    def synthesize_recommendations(self) -> List[Recommendation]:
        """Synthesize hiring recommendations."""
        recommendations = []
        risks = self.assess_risks()

        for candidate in self.candidates:
            candidate_risk = next(r for r in risks if r.candidate_name == candidate.name)
            rec_type = self._determine_recommendation_type(candidate, candidate_risk)
            action = self._generate_action(candidate, rec_type)
            reasoning = self._generate_reasoning(candidate, candidate_risk)
            next_steps = self._generate_next_steps(candidate, rec_type)

            recommendations.append(Recommendation(candidate_name=candidate.name, type=rec_type, action=action, reasoning=reasoning, next_steps=next_steps))

        return recommendations

    def _calculate_risk_level(self, candidate: Candidate) -> RiskLevel:
        """Calculate risk level for candidate."""
        gap_count = len(candidate.gaps)
        strength_count = len(candidate.strengths)
        evidence_level = candidate.evidence_strength.level

        # High risk: many gaps, low evidence, few strengths
        if gap_count >= 3 or evidence_level == 1 or strength_count <= 1:
            return RiskLevel.HIGH

        # Medium risk: some gaps or medium evidence
        if gap_count >= 2 or evidence_level == 2 or strength_count <= 2:
            return RiskLevel.MEDIUM

        # Low risk: few gaps, high evidence, many strengths
        return RiskLevel.LOW

    def _generate_risk_description(self, candidate: Candidate, risk_level: RiskLevel) -> str:
        """Generate risk description."""
        if risk_level == RiskLevel.HIGH:
            return f"High risk due to {len(candidate.gaps)} knowledge gaps and evidence level {candidate.evidence_strength.level}"
        elif risk_level == RiskLevel.MEDIUM:
            return f"Medium risk with {len(candidate.gaps)} gaps and {len(candidate.strengths)} strengths"
        else:
            return f"Low risk with strong evidence (level {candidate.evidence_strength.level}) and {len(candidate.strengths)} strengths"

    def _generate_mitigation_strategies(self, candidate: Candidate, risk_level: RiskLevel) -> List[str]:
        """Generate mitigation strategies."""
        strategies = []

        if candidate.gaps:
            strategies.append(f"Address gaps in: {', '.join(candidate.gaps)}")

        if candidate.evidence_strength.level < 3:
            strategies.append("Request additional evidence or demonstrations")

        if risk_level == RiskLevel.HIGH:
            strategies.append("Consider technical screening or trial project")

        return strategies

    def _determine_recommendation_type(self, candidate: Candidate, risk: RiskAssessment) -> RecommendationType:
        """Determine recommendation type based on candidate and risk."""
        if risk.level == RiskLevel.LOW and len(candidate.strengths) >= 3:
            return RecommendationType.ADVANCE
        elif risk.level == RiskLevel.MEDIUM and len(candidate.strengths) >= 2:
            return RecommendationType.KEEP_WARM
        elif risk.level == RiskLevel.HIGH and len(candidate.gaps) > len(candidate.strengths):
            return RecommendationType.REJECT
        else:
            return RecommendationType.REQUEST_MORE_INFO

    def _generate_action(self, candidate: Candidate, rec_type: RecommendationType) -> str:
        """Generate action based on recommendation type."""
        actions = {
            RecommendationType.ADVANCE: f"Advance {candidate.name} to technical screen",
            RecommendationType.KEEP_WARM: f"Keep {candidate.name} warm for future opportunities",
            RecommendationType.REJECT: f"Reject {candidate.name} at this time",
            RecommendationType.REQUEST_MORE_INFO: f"Request additional information from {candidate.name}",
        }
        return actions[rec_type]

    def _generate_reasoning(self, candidate: Candidate, risk: RiskAssessment) -> str:
        """Generate reasoning for recommendation."""
        reasoning_parts = []

        if candidate.strengths:
            reasoning_parts.append(f"Strengths: {', '.join(candidate.strengths)}")

        if candidate.gaps:
            reasoning_parts.append(f"Gaps: {', '.join(candidate.gaps)}")

        reasoning_parts.append(f"Evidence level: {candidate.evidence_strength.label}")

        if candidate.comment:
            reasoning_parts.append(f"Note: {candidate.comment}")

        return "; ".join(reasoning_parts)

    def _generate_next_steps(self, candidate: Candidate, rec_type: RecommendationType) -> List[str]:
        """Generate next steps based on recommendation type."""
        if rec_type == RecommendationType.ADVANCE:
            return ["Schedule technical interview", "Prepare questions focusing on gaps", "Request portfolio/demo materials"]
        elif rec_type == RecommendationType.KEEP_WARM:
            return ["Add to talent pipeline", "Monitor for new evidence", "Consider for future roles"]
        elif rec_type == RecommendationType.REQUEST_MORE_INFO:
            return ["Request specific artifacts", "Ask for demonstrations", "Clarify experience details"]
        else:  # REJECT
            return ["Send polite rejection", "Provide feedback if requested", "Archive candidate data"]

    def generate_report(self) -> Dict:
        """Generate comprehensive comparison report."""
        matrix = self.generate_comparison_matrix()
        risks = self.assess_risks()
        recommendations = self.synthesize_recommendations()

        return {
            "summary": {"total_candidates": len(self.candidates), "total_requirements": len(self.requirements), "comparison_date": "2025-01-09"},  # TODO: Use actual date
            "comparison_matrix": matrix.to_dict(),
            "matrix_summary": matrix.get_summary(),
            "risk_assessments": [{"candidate": risk.candidate_name, "level": risk.level.value, "description": risk.description, "mitigation": risk.mitigation_strategies} for risk in risks],
            "recommendations": [{"candidate": rec.candidate_name, "type": rec.type.value, "action": rec.action, "reasoning": rec.reasoning, "next_steps": rec.next_steps} for rec in recommendations],
        }
