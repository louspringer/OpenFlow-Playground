#!/usr/bin/env python3
"""
Multi-Perspective Validator for Agent Coordination
Implements stakeholder-driven risk reduction for complex agent decisions
Based on Kiro's Beast Mode Framework multi-perspective validation
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .health_monitor import AgentHealthMonitor

logger = logging.getLogger(__name__)


class StakeholderType(Enum):
    """Stakeholder types for multi-perspective validation"""

    BEAST_MODE_SYSTEM = "beast_mode_system"
    GKE_CONSUMER = "gke_consumer"
    DEVOPS_SRE = "devops_sre"
    DEVELOPMENT_TEAM = "development_team"
    EVALUATOR_JUDGE = "evaluator_judge"
    AGENT_COORDINATOR = "agent_coordinator"


@dataclass
class StakeholderPerspective:
    """Individual stakeholder perspective on a decision"""

    stakeholder_type: StakeholderType
    confidence_score: float  # 0.0-1.0
    assessment: str
    concerns: List[str]
    recommendations: List[str]
    approval_status: bool
    risk_factors: List[str]


@dataclass
class MultiPerspectiveAnalysis:
    """Complete multi-perspective analysis result"""

    decision_context: str
    overall_confidence: float
    stakeholder_perspectives: Dict[StakeholderType, StakeholderPerspective]
    consensus_reached: bool
    final_recommendation: str
    risk_factors: List[str]
    mitigation_strategies: List[str]


class MultiPerspectiveValidator:
    """
    Multi-perspective validator for agent coordination decisions
    Implements stakeholder-driven risk reduction for complex decisions
    """

    def __init__(self, health_monitor: AgentHealthMonitor):
        self.health_monitor = health_monitor
        self.validation_count = 0
        self.total_validations = 0
        self.logger = logging.getLogger(__name__)

        # Decision confidence thresholds
        self.confidence_thresholds = {
            "high_confidence": 0.8,  # 80%+ → Use registry + domain tools
            "medium_confidence": 0.5,  # 50-80% → Registry + basic multi-perspective
            "low_confidence": 0.5,  # <50% → Full Ghostbusters multi-perspective
        }

        # Stakeholder priority weights
        self.stakeholder_weights = {
            StakeholderType.BEAST_MODE_SYSTEM: 0.25,  # System stability
            StakeholderType.GKE_CONSUMER: 0.20,  # Service delivery
            StakeholderType.DEVOPS_SRE: 0.20,  # Infrastructure
            StakeholderType.DEVELOPMENT_TEAM: 0.15,  # Development velocity
            StakeholderType.EVALUATOR_JUDGE: 0.10,  # External validation
            StakeholderType.AGENT_COORDINATOR: 0.10,  # Coordination efficiency
        }

    def validate_agent_decision(self, decision_context: str, initial_confidence: float, decision_data: Dict[str, Any]) -> MultiPerspectiveAnalysis:
        """
        Validate an agent decision using multi-perspective analysis
        """
        self.validation_count += 1
        self.total_validations += 1

        self.logger.info(f"Starting multi-perspective validation for: {decision_context}")

        # Determine validation depth based on confidence
        if initial_confidence >= self.confidence_thresholds["high_confidence"]:
            return self._quick_validation(decision_context, initial_confidence, decision_data)
        elif initial_confidence >= self.confidence_thresholds["medium_confidence"]:
            return self._standard_validation(decision_context, initial_confidence, decision_data)
        else:
            return self._full_validation(decision_context, initial_confidence, decision_data)

    def _quick_validation(self, decision_context: str, initial_confidence: float, decision_data: Dict[str, Any]) -> MultiPerspectiveAnalysis:
        """Quick validation for high-confidence decisions"""
        self.logger.info("Using quick validation (high confidence)")

        # Get perspectives from key stakeholders only
        key_stakeholders = [StakeholderType.BEAST_MODE_SYSTEM, StakeholderType.AGENT_COORDINATOR]

        perspectives = {}
        for stakeholder in key_stakeholders:
            perspectives[stakeholder] = self._get_stakeholder_perspective(stakeholder, decision_context, decision_data, quick_mode=True)

        return self._synthesize_analysis(decision_context, perspectives, initial_confidence)

    def _standard_validation(self, decision_context: str, initial_confidence: float, decision_data: Dict[str, Any]) -> MultiPerspectiveAnalysis:
        """Standard validation for medium-confidence decisions"""
        self.logger.info("Using standard validation (medium confidence)")

        # Get perspectives from core stakeholders
        core_stakeholders = [StakeholderType.BEAST_MODE_SYSTEM, StakeholderType.GKE_CONSUMER, StakeholderType.DEVOPS_SRE, StakeholderType.AGENT_COORDINATOR]

        perspectives = {}
        for stakeholder in core_stakeholders:
            perspectives[stakeholder] = self._get_stakeholder_perspective(stakeholder, decision_context, decision_data, quick_mode=False)

        return self._synthesize_analysis(decision_context, perspectives, initial_confidence)

    def _full_validation(self, decision_context: str, initial_confidence: float, decision_data: Dict[str, Any]) -> MultiPerspectiveAnalysis:
        """Full validation for low-confidence decisions"""
        self.logger.info("Using full validation (low confidence)")

        # Get perspectives from all stakeholders
        perspectives = {}
        for stakeholder in StakeholderType:
            perspectives[stakeholder] = self._get_stakeholder_perspective(stakeholder, decision_context, decision_data, quick_mode=False)

        return self._synthesize_analysis(decision_context, perspectives, initial_confidence)

    def _get_stakeholder_perspective(self, stakeholder: StakeholderType, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool = False) -> StakeholderPerspective:
        """Get perspective from a specific stakeholder"""

        if stakeholder == StakeholderType.BEAST_MODE_SYSTEM:
            return self._beast_mode_perspective(decision_context, decision_data, quick_mode)
        elif stakeholder == StakeholderType.GKE_CONSUMER:
            return self._gke_consumer_perspective(decision_context, decision_data, quick_mode)
        elif stakeholder == StakeholderType.DEVOPS_SRE:
            return self._devops_sre_perspective(decision_context, decision_data, quick_mode)
        elif stakeholder == StakeholderType.DEVELOPMENT_TEAM:
            return self._development_team_perspective(decision_context, decision_data, quick_mode)
        elif stakeholder == StakeholderType.EVALUATOR_JUDGE:
            return self._evaluator_judge_perspective(decision_context, decision_data, quick_mode)
        elif stakeholder == StakeholderType.AGENT_COORDINATOR:
            return self._agent_coordinator_perspective(decision_context, decision_data, quick_mode)
        else:
            raise ValueError(f"Unknown stakeholder type: {stakeholder}")

    def _beast_mode_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """Beast Mode System perspective - focuses on system stability and proven methodology"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check system health
        health_status = self.health_monitor.get_system_health()
        if health_status.get("overall_health", "unknown") not in ["healthy", "unknown"]:
            concerns.append("System health is degraded")
            risk_factors.append("System instability")
            recommendations.append("Address system health issues before proceeding")

        # Check if decision follows proven patterns
        if "proven_pattern" not in decision_data.get("metadata", {}) and decision_data.get("metadata", {}).get("proven_pattern") is not True:
            concerns.append("Decision doesn't follow proven patterns")
            risk_factors.append("Unproven approach")
            recommendations.append("Use proven Beast Mode patterns")

        # Calculate confidence based on system stability
        confidence = 0.8 if health_status.get("overall_health") == "healthy" else 0.3
        if concerns:
            confidence *= 0.7

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.BEAST_MODE_SYSTEM,
            confidence_score=confidence,
            assessment="System stability and proven methodology focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.6,
            risk_factors=risk_factors,
        )

    def _gke_consumer_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """GKE Consumer perspective - focuses on service delivery and reliability"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check service availability
        if "service_impact" in decision_data:
            impact = decision_data["service_impact"]
            if impact == "high":
                concerns.append("High service impact")
                risk_factors.append("Service disruption")
                recommendations.append("Minimize service impact")

        # Check response time requirements
        if "response_time" in decision_data:
            response_time = decision_data["response_time"]
            if response_time > 30:  # seconds
                concerns.append("Slow response time")
                recommendations.append("Optimize for faster response")

        confidence = 0.7
        if concerns:
            confidence *= 0.6

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.GKE_CONSUMER,
            confidence_score=confidence,
            assessment="Service delivery and reliability focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.5,
            risk_factors=risk_factors,
        )

    def _devops_sre_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """DevOps SRE perspective - focuses on infrastructure stability and monitoring"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check resource usage
        if "resource_usage" in decision_data:
            usage = decision_data["resource_usage"]
            if usage > 0.8:  # 80% threshold
                concerns.append("High resource usage")
                risk_factors.append("Resource exhaustion")
                recommendations.append("Optimize resource usage")

        # Check monitoring capabilities
        if "monitoring" not in decision_data.get("capabilities", []):
            concerns.append("Limited monitoring capabilities")
            risk_factors.append("Reduced observability")
            recommendations.append("Implement comprehensive monitoring")

        confidence = 0.75
        if concerns:
            confidence *= 0.7

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.DEVOPS_SRE,
            confidence_score=confidence,
            assessment="Infrastructure stability and monitoring focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.6,
            risk_factors=risk_factors,
        )

    def _development_team_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """Development Team perspective - focuses on code quality and maintainability"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check code quality impact
        if "code_quality" in decision_data:
            quality = decision_data["code_quality"]
            if quality < 0.8:  # 80% quality threshold
                concerns.append("Code quality degradation")
                risk_factors.append("Technical debt")
                recommendations.append("Maintain code quality standards")

        # Check testing coverage
        if "test_coverage" in decision_data:
            coverage = decision_data["test_coverage"]
            if coverage < 0.8:  # 80% coverage threshold
                concerns.append("Insufficient test coverage")
                risk_factors.append("Regression risk")
                recommendations.append("Increase test coverage")

        confidence = 0.8
        if concerns:
            confidence *= 0.6

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.DEVELOPMENT_TEAM,
            confidence_score=confidence,
            assessment="Code quality and maintainability focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.7,
            risk_factors=risk_factors,
        )

    def _evaluator_judge_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """Evaluator Judge perspective - focuses on measurable outcomes and proof of concept"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check for measurable outcomes
        if "metrics" not in decision_data:
            concerns.append("No measurable outcomes defined")
            risk_factors.append("Unmeasurable results")
            recommendations.append("Define clear success metrics")

        # Check for proof of concept
        if "proof_of_concept" not in decision_data.get("validation", {}):
            concerns.append("No proof of concept")
            risk_factors.append("Unproven approach")
            recommendations.append("Provide proof of concept")

        confidence = 0.6
        if concerns:
            confidence *= 0.5

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.EVALUATOR_JUDGE,
            confidence_score=confidence,
            assessment="Measurable outcomes and proof of concept focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.5,
            risk_factors=risk_factors,
        )

    def _agent_coordinator_perspective(self, decision_context: str, decision_data: Dict[str, Any], quick_mode: bool) -> StakeholderPerspective:
        """Agent Coordinator perspective - focuses on coordination efficiency and communication"""
        concerns = []
        recommendations = []
        risk_factors = []

        # Check communication overhead
        if "communication_complexity" in decision_data:
            complexity = decision_data["communication_complexity"]
            if complexity > 0.7:  # 70% complexity threshold
                concerns.append("High communication complexity")
                risk_factors.append("Coordination overhead")
                recommendations.append("Simplify communication protocols")

        # Check agent availability
        agent_health = self.health_monitor.get_all_agent_health()
        unhealthy_agents = [aid for aid, health in agent_health.items() if health != "healthy"]
        if unhealthy_agents:
            concerns.append(f"Unhealthy agents: {unhealthy_agents}")
            risk_factors.append("Agent unavailability")
            recommendations.append("Address agent health issues")

        confidence = 0.8
        if concerns:
            confidence *= 0.6

        return StakeholderPerspective(
            stakeholder_type=StakeholderType.AGENT_COORDINATOR,
            confidence_score=confidence,
            assessment="Coordination efficiency and communication focus",
            concerns=concerns,
            recommendations=recommendations,
            approval_status=confidence > 0.6,
            risk_factors=risk_factors,
        )

    def _synthesize_analysis(self, decision_context: str, perspectives: Dict[StakeholderType, StakeholderPerspective], initial_confidence: float) -> MultiPerspectiveAnalysis:
        """Synthesize all perspectives into final analysis"""

        # Calculate weighted overall confidence
        total_weight = 0
        weighted_confidence = 0

        for stakeholder, perspective in perspectives.items():
            weight = self.stakeholder_weights.get(stakeholder, 0.1)
            weighted_confidence += perspective.confidence_score * weight
            total_weight += weight

        overall_confidence = weighted_confidence / total_weight if total_weight > 0 else 0

        # Check consensus
        approvals = sum(1 for p in perspectives.values() if p.approval_status)
        total_stakeholders = len(perspectives)
        consensus_reached = approvals >= (total_stakeholders * 0.5)  # 50% approval threshold

        # Collect all concerns and recommendations
        all_concerns = []
        all_recommendations = []
        all_risk_factors = []

        for perspective in perspectives.values():
            all_concerns.extend(perspective.concerns)
            all_recommendations.extend(perspective.recommendations)
            all_risk_factors.extend(perspective.risk_factors)

        # Generate final recommendation
        if consensus_reached and overall_confidence > 0.7:
            final_recommendation = "APPROVE - High confidence with stakeholder consensus"
        elif consensus_reached and overall_confidence > 0.5:
            final_recommendation = "APPROVE WITH CONDITIONS - Address key concerns before proceeding"
        else:
            final_recommendation = "REJECT - Insufficient confidence or stakeholder consensus"

        # Generate mitigation strategies
        mitigation_strategies = []
        if all_risk_factors:
            mitigation_strategies.append("Implement risk mitigation measures")
        if all_concerns:
            mitigation_strategies.append("Address stakeholder concerns")
        if not consensus_reached:
            mitigation_strategies.append("Improve stakeholder alignment")

        self.logger.info(f"Multi-perspective analysis complete: {final_recommendation}")

        return MultiPerspectiveAnalysis(
            decision_context=decision_context,
            overall_confidence=overall_confidence,
            stakeholder_perspectives=perspectives,
            consensus_reached=consensus_reached,
            final_recommendation=final_recommendation,
            risk_factors=list(set(all_risk_factors)),
            mitigation_strategies=mitigation_strategies,
        )

    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics for monitoring"""
        return {
            "total_validations": self.total_validations,
            "current_validations": self.validation_count,
            "confidence_thresholds": self.confidence_thresholds,
            "stakeholder_weights": {k.value: v for k, v in self.stakeholder_weights.items()},
        }
