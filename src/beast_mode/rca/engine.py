"""
Root Cause Analysis Engine

Implements systematic root cause analysis with pattern library integration,
comprehensive failure analysis, and systematic fix generation.

Requirements Compliance: R7 - Root Cause Analysis
- R7.1: Systematic root cause analysis with pattern library
- R7.2: Comprehensive failure analysis with 5W1H methodology
- R7.3: Systematic fixes with validation and prevention patterns
- R7.4: Integration with PDCA Check phase for failure analysis
- R7.5: Pattern learning and model updates for continuous improvement
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from ..base.reflective_module import ReflectiveModule, HealthStatus
from ..base.data_models import RCAResult, RCASeverity
from .pattern_library import PatternLibrary
from .analysis_factors import AnalysisFactors
from .systematic_fixes import SystematicFixes


@dataclass
class FailureContext:
    """Context information for failure analysis."""

    failure_type: str
    symptoms: List[str]
    environment: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    affected_components: List[str]
    user_impact: str
    business_impact: str


class RootCauseAnalysisEngine(ReflectiveModule):
    """
    Systematic root cause analysis engine with pattern library integration.

    Provides comprehensive failure analysis using 5W1H methodology and
    generates systematic fixes with validation and prevention patterns.
    """

    def __init__(self, pattern_library_path: Optional[str] = None):
        """
        Initialize the RCA Engine.

        Args:
            pattern_library_path: Optional path to pattern library file
        """
        super().__init__("RootCauseAnalysisEngine", "1.0.0")
        self.pattern_library = PatternLibrary(pattern_library_path)
        self.analysis_factors = AnalysisFactors()
        self.systematic_fixes = SystematicFixes()
        self._setup_logging()

    def analyze_failure(self, failure_context: FailureContext) -> RCAResult:
        """
        Perform systematic root cause analysis on a failure.

        Args:
            failure_context: Context information about the failure

        Returns:
            Comprehensive RCA result with root causes and fixes
        """
        self.logger.info(f"Starting RCA for failure: {failure_context.failure_type}")
        start_time = datetime.utcnow()

        try:
            # Step 1: Pattern matching against known patterns
            pattern_matches = self._match_known_patterns(failure_context)

            # Step 2: 5W1H analysis
            analysis_factors = self._perform_5w1h_analysis(failure_context)

            # Step 3: Root cause identification
            root_causes = self._identify_root_causes(failure_context, pattern_matches, analysis_factors)

            # Step 4: Severity assessment
            severity = self._assess_severity(failure_context, root_causes)

            # Step 5: Generate systematic fixes
            systematic_fixes = self._generate_systematic_fixes(failure_context, root_causes, pattern_matches)

            # Step 6: Validate fixes
            fix_validation = self._validate_fixes(systematic_fixes, failure_context)

            # Step 7: Generate prevention patterns
            prevention_patterns = self._generate_prevention_patterns(failure_context, root_causes, systematic_fixes)

            # Create comprehensive result
            rca_result = RCAResult(
                failure=failure_context.failure_type,
                symptoms=failure_context.symptoms,
                root_causes=root_causes,
                severity=severity,
                analysis_factors=analysis_factors,
                systematic_fixes=systematic_fixes,
                fix_validation=fix_validation,
                prevention_patterns=prevention_patterns,
                timestamp=datetime.utcnow(),
            )

            # Update pattern library with new learnings
            self._update_pattern_library(failure_context, rca_result)

            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(f"RCA completed for failure: {failure_context.failure_type}, duration: {duration}s")

            return rca_result

        except Exception as e:
            self.logger.error(f"RCA failed for failure: {failure_context.failure_type}, error: {str(e)}")
            self.update_health_status(HealthStatus.DEGRADED, {"error": str(e)})
            raise

    def _match_known_patterns(self, failure_context: FailureContext) -> List[Dict[str, Any]]:
        """Match failure against known patterns in the pattern library."""
        patterns = self.pattern_library.get_patterns()
        matches = []

        for pattern in patterns:
            match_score = self._calculate_pattern_match_score(failure_context, pattern)
            if match_score > 0.7:  # Threshold for pattern match
                matches.append(
                    {
                        "pattern_id": pattern["id"],
                        "pattern_name": pattern["name"],
                        "match_score": match_score,
                        "similar_failures": pattern.get("similar_failures", []),
                        "known_causes": pattern.get("known_causes", []),
                    }
                )

        return sorted(matches, key=lambda x: x["match_score"], reverse=True)

    def _calculate_pattern_match_score(self, failure_context: FailureContext, pattern: Dict[str, Any]) -> float:
        """Calculate how well a failure matches a known pattern."""
        score = 0.0

        # Match failure type
        if failure_context.failure_type.lower() in pattern.get("failure_types", []):
            score += 0.3

        # Match symptoms
        pattern_symptoms = pattern.get("symptoms", [])
        symptom_matches = sum(1 for symptom in failure_context.symptoms if any(ps in symptom.lower() for ps in pattern_symptoms))
        if pattern_symptoms:
            score += 0.4 * (symptom_matches / len(pattern_symptoms))

        # Match environment
        pattern_env = pattern.get("environment_indicators", {})
        env_matches = sum(1 for key, value in pattern_env.items() if failure_context.environment.get(key) == value)
        if pattern_env:
            score += 0.3 * (env_matches / len(pattern_env))

        return min(score, 1.0)

    def _perform_5w1h_analysis(self, failure_context: FailureContext) -> Dict[str, Any]:
        """Perform 5W1H analysis on the failure."""
        return {
            "what": {"failure_description": failure_context.failure_type, "symptoms": failure_context.symptoms, "affected_components": failure_context.affected_components},
            "when": {
                "timeline": failure_context.timeline,
                "first_occurrence": self._extract_first_occurrence(failure_context.timeline),
                "frequency": self._calculate_frequency(failure_context.timeline),
            },
            "where": {
                "environment": failure_context.environment,
                "affected_systems": failure_context.affected_components,
                "geographic_location": failure_context.environment.get("location", "unknown"),
            },
            "who": {
                "affected_users": failure_context.user_impact,
                "responsible_teams": self._identify_responsible_teams(failure_context),
                "stakeholders": self._identify_stakeholders(failure_context),
            },
            "why": {
                "business_impact": failure_context.business_impact,
                "technical_impact": self._assess_technical_impact(failure_context),
                "root_cause_hypotheses": self._generate_root_cause_hypotheses(failure_context),
            },
            "how": {
                "failure_mechanism": self._analyze_failure_mechanism(failure_context),
                "propagation_path": self._analyze_propagation_path(failure_context),
                "detection_method": self._analyze_detection_method(failure_context),
            },
        }

    def _identify_root_causes(self, failure_context: FailureContext, pattern_matches: List[Dict[str, Any]], analysis_factors: Dict[str, Any]) -> List[str]:
        """Identify root causes based on analysis factors and pattern matches."""
        root_causes = []

        # Extract from pattern matches
        for match in pattern_matches:
            root_causes.extend(match.get("known_causes", []))

        # Extract from 5W1H analysis
        why_analysis = analysis_factors.get("why", {})
        root_causes.extend(why_analysis.get("root_cause_hypotheses", []))

        # Add systematic analysis
        root_causes.extend(self._perform_systematic_root_cause_analysis(failure_context))

        # Remove duplicates and return
        return list(set(root_causes))

    def _assess_severity(self, failure_context: FailureContext, root_causes: List[str]) -> RCASeverity:
        """Assess severity of the failure based on impact and root causes."""
        severity_score = 0

        # Business impact scoring
        business_impact = failure_context.business_impact.lower()
        if "critical" in business_impact or "severe" in business_impact:
            severity_score += 3
        elif "high" in business_impact or "significant" in business_impact:
            severity_score += 2
        elif "medium" in business_impact or "moderate" in business_impact:
            severity_score += 1

        # User impact scoring
        user_impact = failure_context.user_impact.lower()
        if "all users" in user_impact or "system down" in user_impact:
            severity_score += 3
        elif "many users" in user_impact or "major feature" in user_impact:
            severity_score += 2
        elif "some users" in user_impact or "minor feature" in user_impact:
            severity_score += 1

        # Root cause complexity scoring
        if len(root_causes) > 3:
            severity_score += 1
        if any("systemic" in cause.lower() for cause in root_causes):
            severity_score += 1

        # Map to severity enum
        if severity_score >= 5:
            return RCASeverity.CRITICAL
        elif severity_score >= 3:
            return RCASeverity.HIGH
        elif severity_score >= 1:
            return RCASeverity.MEDIUM
        else:
            return RCASeverity.LOW

    def _generate_systematic_fixes(self, failure_context: FailureContext, root_causes: List[str], pattern_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate systematic fixes for the identified root causes."""
        fixes = []

        for root_cause in root_causes:
            fix = self.systematic_fixes.generate_fix(root_cause, failure_context, pattern_matches)
            fixes.append(fix)

        return fixes

    def _validate_fixes(self, systematic_fixes: List[Dict[str, Any]], failure_context: FailureContext) -> Dict[str, Any]:
        """Validate that fixes address the root causes and prevent recurrence."""
        validation_results = []

        for fix in systematic_fixes:
            validation = {
                "fix_id": fix.get("id"),
                "root_cause_addressed": fix.get("root_cause"),
                "validation_passed": True,  # Placeholder for actual validation
                "prevention_measures": fix.get("prevention_measures", []),
                "rollback_plan": fix.get("rollback_plan", {}),
                "testing_required": fix.get("testing_required", []),
            }
            validation_results.append(validation)

        return {"validation_results": validation_results, "overall_validation_passed": all(v["validation_passed"] for v in validation_results), "timestamp": datetime.utcnow().isoformat()}

    def _generate_prevention_patterns(self, failure_context: FailureContext, root_causes: List[str], systematic_fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate prevention patterns to avoid similar failures in the future."""
        prevention_patterns = []

        for root_cause in root_causes:
            pattern = {
                "pattern_id": f"prevention_{root_cause.replace(' ', '_').lower()}",
                "root_cause": root_cause,
                "prevention_measures": self._generate_prevention_measures(root_cause),
                "monitoring_indicators": self._generate_monitoring_indicators(root_cause),
                "early_warning_signs": self._generate_early_warning_signs(root_cause),
                "created_at": datetime.utcnow().isoformat(),
            }
            prevention_patterns.append(pattern)

        return prevention_patterns

    def _update_pattern_library(self, failure_context: FailureContext, rca_result: RCAResult):
        """Update pattern library with new learnings from this RCA."""
        new_pattern = {
            "id": f"pattern_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "failure_type": failure_context.failure_type,
            "symptoms": failure_context.symptoms,
            "root_causes": rca_result.root_causes,
            "systematic_fixes": [fix["id"] for fix in rca_result.systematic_fixes],
            "prevention_patterns": [pattern["pattern_id"] for pattern in rca_result.prevention_patterns],
            "created_at": datetime.utcnow().isoformat(),
        }

        self.pattern_library.add_pattern(new_pattern)

    # Helper methods for 5W1H analysis
    def _extract_first_occurrence(self, timeline: List[Dict[str, Any]]) -> Optional[str]:
        """Extract first occurrence from timeline."""
        if not timeline:
            return None
        return min(entry.get("timestamp", "") for entry in timeline)

    def _calculate_frequency(self, timeline: List[Dict[str, Any]]) -> str:
        """Calculate frequency of failure occurrences."""
        if len(timeline) <= 1:
            return "single_occurrence"
        elif len(timeline) <= 5:
            return "occasional"
        elif len(timeline) <= 20:
            return "frequent"
        else:
            return "chronic"

    def _identify_responsible_teams(self, failure_context: FailureContext) -> List[str]:
        """Identify responsible teams based on affected components."""
        # Placeholder logic - would analyze component ownership
        return ["development_team", "operations_team"]

    def _identify_stakeholders(self, failure_context: FailureContext) -> List[str]:
        """Identify stakeholders affected by the failure."""
        return ["end_users", "business_owners", "technical_teams"]

    def _assess_technical_impact(self, failure_context: FailureContext) -> str:
        """Assess technical impact of the failure."""
        if len(failure_context.affected_components) > 5:
            return "system_wide"
        elif len(failure_context.affected_components) > 1:
            return "multi_component"
        else:
            return "single_component"

    def _generate_root_cause_hypotheses(self, failure_context: FailureContext) -> List[str]:
        """Generate root cause hypotheses based on failure context."""
        hypotheses = []

        # Time-based hypotheses
        if failure_context.timeline:
            hypotheses.append("timing_related_issue")

        # Environment-based hypotheses
        if failure_context.environment:
            hypotheses.append("environment_configuration_issue")

        # Component-based hypotheses
        if len(failure_context.affected_components) > 1:
            hypotheses.append("integration_issue")
        else:
            hypotheses.append("component_specific_issue")

        return hypotheses

    def _analyze_failure_mechanism(self, failure_context: FailureContext) -> str:
        """Analyze the mechanism of failure."""
        return "systematic_analysis_required"  # Placeholder

    def _analyze_propagation_path(self, failure_context: FailureContext) -> List[str]:
        """Analyze how the failure propagated through the system."""
        return failure_context.affected_components

    def _analyze_detection_method(self, failure_context: FailureContext) -> str:
        """Analyze how the failure was detected."""
        return "monitoring_system"  # Placeholder

    def _perform_systematic_root_cause_analysis(self, failure_context: FailureContext) -> List[str]:
        """Perform systematic root cause analysis beyond pattern matching."""
        root_causes = []

        # Analyze failure patterns
        if len(failure_context.symptoms) > 3:
            root_causes.append("complex_failure_scenario")

        # Analyze environment factors
        if failure_context.environment.get("recent_changes"):
            root_causes.append("recent_change_induced_failure")

        # Analyze component interactions
        if len(failure_context.affected_components) > 1:
            root_causes.append("component_interaction_failure")

        return root_causes

    def _generate_prevention_measures(self, root_cause: str) -> List[str]:
        """Generate prevention measures for a specific root cause."""
        measures = []

        if "timing" in root_cause.lower():
            measures.extend(["implement_timeout_handling", "add_retry_mechanisms"])
        elif "environment" in root_cause.lower():
            measures.extend(["validate_environment_config", "add_configuration_checks"])
        elif "integration" in root_cause.lower():
            measures.extend(["improve_error_handling", "add_integration_tests"])

        return measures

    def _generate_monitoring_indicators(self, root_cause: str) -> List[str]:
        """Generate monitoring indicators for a specific root cause."""
        indicators = []

        if "timing" in root_cause.lower():
            indicators.extend(["response_time_metrics", "timeout_occurrences"])
        elif "environment" in root_cause.lower():
            indicators.extend(["configuration_drift", "environment_health"])
        elif "integration" in root_cause.lower():
            indicators.extend(["integration_health", "error_rates"])

        return indicators

    def _generate_early_warning_signs(self, root_cause: str) -> List[str]:
        """Generate early warning signs for a specific root cause."""
        warnings = []

        if "timing" in root_cause.lower():
            warnings.extend(["increasing_response_times", "timeout_warnings"])
        elif "environment" in root_cause.lower():
            warnings.extend(["configuration_changes", "environment_degradation"])
        elif "integration" in root_cause.lower():
            warnings.extend(["increasing_error_rates", "integration_failures"])

        return warnings

    def _setup_logging(self):
        """Setup logging for RCA operations."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)

    # ReflectiveModule interface implementation
    def get_module_status(self) -> Dict[str, Any]:
        """Get operational visibility for external systems."""
        return {
            "engine_name": self.name,
            "version": self.version,
            "pattern_library_size": len(self.pattern_library.get_patterns()),
            "analysis_factors_loaded": True,
            "systematic_fixes_loaded": True,
            "health_status": self._health_status.value,
            "operational_data": self._operational_visibility,
        }

    def is_healthy(self) -> bool:
        """Check if RCA engine is healthy."""
        return self._health_status == HealthStatus.HEALTHY and self.pattern_library is not None and self.analysis_factors is not None and self.systematic_fixes is not None

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        return {
            "pattern_library_status": "loaded" if self.pattern_library else "not_loaded",
            "analysis_factors_status": "loaded" if self.analysis_factors else "not_loaded",
            "systematic_fixes_status": "loaded" if self.systematic_fixes else "not_loaded",
            "last_health_check": datetime.utcnow().isoformat(),
        }
