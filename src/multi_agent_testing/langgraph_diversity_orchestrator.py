#!/usr/bin/env python3
"""LangGraph diversity orchestrator"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class Agent:
    """Represents an agent in the diversity system"""

    name: str
    role: str
    expertise: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {"name": self.name, "role": self.role, "expertise": self.expertise}


class AnalysisType(Enum):
    """Types of diversity analysis"""

    BLIND_SPOT_DETECTION = "blind_spot_detection"
    AGREEMENT_ANALYSIS = "agreement_analysis"
    MODEL_DIVERSITY = "model_diversity"
    ROLE_DIVERSITY = "role_diversity"


@dataclass
class BlindSpotFinding:
    """Represents a blind spot found in diversity analysis"""

    question: str
    confidence: str
    blind_spots: str
    recommendation: str
    category: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "question": self.question,
            "confidence": self.confidence,
            "blind_spots": self.blind_spots,
            "recommendation": self.recommendation,
            "category": self.category,
        }


@dataclass
class DiversityAnalysis:
    """Represents a diversity analysis result"""

    agent_name: str
    findings: list[BlindSpotFinding]
    total_findings: int
    confidence_score: float
    diversity_score: float

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_name": self.agent_name,
            "findings": [f.to_dict() for f in self.findings],
            "total_findings": self.total_findings,
            "confidence_score": self.confidence_score,
            "diversity_score": self.diversity_score,
        }


class LangGraphDiversityOrchestrator:
    """LangGraph-based diversity orchestrator"""

    def __init__(self):
        """Initialize the orchestrator"""
        self.analyses: list[DiversityAnalysis] = []
        self.blind_spots: list[BlindSpotFinding] = []
        self.agents = [
            Agent(
                "Security Expert", "Security", "Security vulnerabilities and threats"
            ),
            Agent("DevOps Engineer", "Operations", "Infrastructure and deployment"),
            Agent("Code Quality Expert", "Quality", "Code quality and maintainability"),
            Agent(
                "User Experience Advocate", "UX", "User experience and accessibility"
            ),
            Agent("Performance Engineer", "Performance", "Performance and scalability"),
        ]

    def create_llm_client(self, agent):
        """Create LLM client for an agent"""
        # Check for required API key
        if not os.getenv("OPENAI_API_KEY"):
            msg = "OPENAI_API_KEY environment variable is required"
            raise ValueError(msg)

        # Mock implementation for testing
        return {"agent": agent.name, "client_type": "openai"}

    def calculate_diversity_metrics(
        self, analyses: list[DiversityAnalysis]
    ) -> dict[str, Any]:
        """Calculate diversity metrics from analyses"""
        total_findings = sum(a.total_findings for a in analyses)

        # Count unique findings
        all_findings = []
        for analysis in analyses:
            all_findings.extend([f.blind_spots for f in analysis.findings])
        unique_findings = len(set(all_findings))

        # Calculate overall diversity score
        if analyses:
            diversity_score = sum(a.diversity_score for a in analyses) / len(analyses)
        else:
            diversity_score = 0.0

        # Calculate agent coverage
        agent_coverage = (
            len({a.agent_name for a in analyses}) / len(self.agents)
            if self.agents
            else 0.0
        )

        # Calculate category coverage
        all_categories = set()
        for analysis in analyses:
            for finding in analysis.findings:
                all_categories.add(finding.category)
        category_coverage = len(all_categories) / 5.0  # Assuming 5 main categories

        return {
            "total_findings": total_findings,
            "unique_findings": unique_findings,
            "diversity_score": diversity_score,
            "agent_coverage": agent_coverage,
            "category_coverage": category_coverage,
        }

    def detect_blind_spots(
        self,
        model_responses: dict[str, list[str]],
        role_responses: dict[str, list[str]],
    ) -> list[BlindSpotFinding]:
        """Detect blind spots in model and role diversity"""
        blind_spots = []

        # Check for model convergence (all models giving similar responses)
        if len(model_responses) > 1:
            response_sets = [set(responses) for responses in model_responses.values()]
            common_responses = set.intersection(*response_sets)
            if len(common_responses) > 0.8 * len(list(model_responses.values())[0]):
                blind_spots.append(
                    BlindSpotFinding(
                        question="Are models too similar?",
                        confidence="Medium",
                        blind_spots="High model convergence - models may be too similar",
                        recommendation="Add more diverse model types or training data",
                        category="model_diversity",
                    )
                )

        # Check for role convergence
        if len(role_responses) > 1:
            role_sets = [set(responses) for responses in role_responses.values()]
            common_role_responses = set.intersection(*role_sets)
            if len(common_role_responses) > 0.7 * len(list(role_responses.values())[0]):
                blind_spots.append(
                    BlindSpotFinding(
                        question="Are roles distinct enough?",
                        confidence="High",
                        blind_spots="High role convergence - roles may not be distinct enough",
                        recommendation="Implement more distinct role definitions and training",
                        category="role_diversity",
                    )
                )

        # Check for missing edge cases
        edge_case_indicators = [
            "edge case",
            "corner case",
            "exception",
            "error",
            "failure",
        ]
        edge_case_coverage = 0
        total_responses = sum(len(responses) for responses in model_responses.values())

        for responses in model_responses.values():
            for response in responses:
                if any(
                    indicator in response.lower() for indicator in edge_case_indicators
                ):
                    edge_case_coverage += 1

        if edge_case_coverage / total_responses < 0.1:
            blind_spots.append(
                BlindSpotFinding(
                    question="Are edge cases covered?",
                    confidence="Medium",
                    blind_spots="Low edge case coverage in analysis",
                    recommendation="Add adversarial testing and edge case scenarios",
                    category="edge_case_coverage",
                )
            )

        return blind_spots

    def analyze_diversity(
        self,
        analysis_type: AnalysisType,
        model_responses: dict[str, list[str]],
        role_responses: dict[str, list[str]],
    ) -> DiversityAnalysis:
        """Perform diversity analysis of specified type"""

        # Detect blind spots
        blind_spots = self.detect_blind_spots(model_responses, role_responses)

        # Calculate diversity score (based on response variety)
        all_responses = []
        for responses in model_responses.values():
            all_responses.extend(responses)
        for responses in role_responses.values():
            all_responses.extend(responses)

        unique_responses = len(set(all_responses))
        total_responses = len(all_responses)
        diversity_score = (
            unique_responses / total_responses if total_responses > 0 else 0
        )

        # Calculate agreement rate (how often responses agree)
        if len(all_responses) > 1:
            agreement_count = 0
            for i, response1 in enumerate(all_responses):
                for response2 in all_responses[i + 1 :]:
                    if response1 == response2:
                        agreement_count += 1
            total_comparisons = len(all_responses) * (len(all_responses) - 1) / 2
            agreement_rate = (
                agreement_count / total_comparisons if total_comparisons > 0 else 0
            )
        else:
            agreement_rate = 1.0

        # Generate recommendations
        recommendations = []
        if diversity_score < 0.7:
            recommendations.append(
                "Increase response diversity through varied prompts and models"
            )
        if agreement_rate > 0.8:
            recommendations.append(
                "Reduce over-agreement by increasing model and role diversity"
            )
        if blind_spots:
            recommendations.append(
                "Address blind spots through targeted mitigation strategies"
            )

        # Create analysis result
        analysis = DiversityAnalysis(
            agent_name="Diversity Analyzer",
            findings=blind_spots,
            total_findings=len(blind_spots),
            confidence_score=0.8,
            diversity_score=diversity_score,
        )

        # Store results
        self.analyses.append(analysis)
        self.blind_spots.extend(blind_spots)

        return analysis

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get summary of all analyses performed"""
        if not self.analyses:
            return {"message": "No analyses performed yet"}

        total_blind_spots = len(self.blind_spots)
        critical_blind_spots = len(
            [bs for bs in self.blind_spots if bs.confidence == "High"]
        )
        high_blind_spots = len(
            [bs for bs in self.blind_spots if bs.confidence == "Medium"]
        )

        avg_diversity_score = sum(a.diversity_score for a in self.analyses) / len(
            self.analyses
        )

        return {
            "total_analyses": len(self.analyses),
            "total_blind_spots": total_blind_spots,
            "critical_blind_spots": critical_blind_spots,
            "high_blind_spots": high_blind_spots,
            "average_diversity_score": avg_diversity_score,
            "recommendations": [
                "Address high-confidence blind spots first",
                f"Improve diversity score from {avg_diversity_score:.2f} to >0.8",
                "Implement targeted mitigation strategies",
            ],
        }
