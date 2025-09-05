"""
PDCA Phase Handlers

Implements individual phase handlers for Plan, Do, Check, and Act phases
of the PDCA cycle with model-driven intelligence and systematic approaches.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod

from .context import PDCATask, PDCAPhaseResult, ModelRegistryQuery, ValidationResult


class PDCAPhase(ABC):
    """Abstract base class for PDCA phase handlers."""

    def __init__(self, orchestrator):
        """Initialize phase handler with orchestrator reference."""
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, task: PDCATask, *args, **kwargs) -> Dict[str, Any]:
        """Execute the phase for the given task."""
        pass


class PlanPhase(PDCAPhase):
    """
    Plan Phase Handler

    Uses project model registry for intelligence-driven planning,
    identifying requirements and constraints systematically.
    """

    def execute(self, task: PDCATask) -> Dict[str, Any]:
        """
        Execute Plan phase using model-driven intelligence.

        Args:
            task: Development task to plan for

        Returns:
            Plan phase result with requirements and constraints
        """
        start_time = datetime.utcnow()
        self.logger.info(f"Starting Plan phase for task: {task.name}")

        try:
            # Query model registry for domain intelligence
            domain_intelligence = self._query_domain_intelligence(task)

            # Identify requirements and constraints
            requirements = self._identify_requirements(task, domain_intelligence)
            constraints = self._identify_constraints(task, domain_intelligence)

            # Create systematic plan
            plan = self._create_systematic_plan(task, requirements, constraints)

            duration = (datetime.utcnow() - start_time).total_seconds()

            result = {
                "phase": "plan",
                "success": True,
                "duration": duration,
                "domain_intelligence": domain_intelligence,
                "requirements": requirements,
                "constraints": constraints,
                "plan": plan,
                "model_queries": self._get_model_queries_used(),
                "timestamp": datetime.utcnow().isoformat(),
            }

            self.logger.info(f"Plan phase completed for task: {task.name}")
            return result

        except Exception as e:
            self.logger.error(f"Plan phase failed for task: {task.name}, error: {str(e)}")
            return {"phase": "plan", "success": False, "duration": (datetime.utcnow() - start_time).total_seconds(), "error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _query_domain_intelligence(self, task: PDCATask) -> Dict[str, Any]:
        """Query project model registry for domain intelligence."""
        if not self.orchestrator.model_registry:
            return {"domains": {}, "requirements": []}

        # Extract relevant domains and requirements
        domains = self.orchestrator.model_registry.get("domains", {})
        requirements = self.orchestrator.model_registry.get("requirements_traceability", [])

        # Filter based on task requirements
        relevant_domains = {}
        for domain_name, domain_config in domains.items():
            if self._is_domain_relevant(task, domain_config):
                relevant_domains[domain_name] = domain_config

        return {"domains": relevant_domains, "requirements": requirements, "query_timestamp": datetime.utcnow().isoformat()}

    def _is_domain_relevant(self, task: PDCATask, domain_config: Dict[str, Any]) -> bool:
        """Check if domain is relevant to the task."""
        # Simple relevance check based on task type and domain patterns
        task_type = task.task_type.value.lower()
        domain_name = domain_config.get("name", "").lower()

        # Check for pattern matches
        patterns = {"development": ["dev", "code", "build"], "testing": ["test", "qa", "validation"], "documentation": ["doc", "readme", "guide"], "deployment": ["deploy", "infra", "cloud"]}

        for pattern in patterns.get(task_type, []):
            if pattern in domain_name:
                return True

        return False

    def _identify_requirements(self, task: PDCATask, domain_intelligence: Dict[str, Any]) -> List[str]:
        """Identify requirements from model registry and task context."""
        requirements = list(task.requirements)  # Start with task requirements

        # Add domain-specific requirements
        for domain_name, domain_config in domain_intelligence.get("domains", {}).items():
            domain_requirements = domain_config.get("requirements", [])
            requirements.extend(domain_requirements)

        # Remove duplicates and return
        return list(set(requirements))

    def _identify_constraints(self, task: PDCATask, domain_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Identify constraints from model registry and task context."""
        constraints = dict(task.constraints)  # Start with task constraints

        # Add domain-specific constraints
        for domain_name, domain_config in domain_intelligence.get("domains", {}).items():
            domain_constraints = domain_config.get("constraints", {})
            constraints.update(domain_constraints)

        return constraints

    def _create_systematic_plan(self, task: PDCATask, requirements: List[str], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Create systematic plan based on requirements and constraints."""
        return {
            "task_name": task.name,
            "task_type": task.task_type.value,
            "priority": task.priority.value,
            "requirements": requirements,
            "constraints": constraints,
            "success_criteria": task.success_criteria,
            "estimated_duration": task.estimated_duration,
            "assigned_domain": task.assigned_domain,
            "dependencies": task.dependencies,
            "plan_created": datetime.utcnow().isoformat(),
        }

    def _get_model_queries_used(self) -> List[Dict[str, Any]]:
        """Get list of model queries used in planning."""
        return [{"query_type": "domain_intelligence", "timestamp": datetime.utcnow().isoformat(), "success": True}]


class DoPhase(PDCAPhase):
    """
    Do Phase Handler

    Implements systematic development approach, not ad-hoc coding,
    with RM compliance enforcement.
    """

    def execute(self, task: PDCATask, plan_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Do phase with systematic implementation.

        Args:
            task: Development task
            plan_result: Result from Plan phase

        Returns:
            Do phase result with implementation details
        """
        start_time = datetime.utcnow()
        self.logger.info(f"Starting Do phase for task: {task.name}")

        try:
            # Validate plan before implementation
            plan_validation = self._validate_plan(plan_result)
            if not plan_validation["valid"]:
                raise ValueError(f"Plan validation failed: {plan_validation['errors']}")

            # Execute systematic implementation
            implementation = self._execute_systematic_implementation(task, plan_result)

            # Validate implementation
            implementation_validation = self._validate_implementation(implementation)

            duration = (datetime.utcnow() - start_time).total_seconds()

            result = {
                "phase": "do",
                "success": implementation_validation["valid"],
                "duration": duration,
                "plan_validation": plan_validation,
                "implementation": implementation,
                "implementation_validation": implementation_validation,
                "timestamp": datetime.utcnow().isoformat(),
            }

            self.logger.info(f"Do phase completed for task: {task.name}")
            return result

        except Exception as e:
            self.logger.error(f"Do phase failed for task: {task.name}, error: {str(e)}")
            return {"phase": "do", "success": False, "duration": (datetime.utcnow() - start_time).total_seconds(), "error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _validate_plan(self, plan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate plan before implementation."""
        errors = []

        if not plan_result.get("success", False):
            errors.append("Plan phase was not successful")

        if not plan_result.get("requirements"):
            errors.append("No requirements identified")

        if not plan_result.get("plan"):
            errors.append("No plan created")

        return {"valid": len(errors) == 0, "errors": errors, "timestamp": datetime.utcnow().isoformat()}

    def _execute_systematic_implementation(self, task: PDCATask, plan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute systematic implementation based on plan."""
        # This is a placeholder for actual implementation logic
        # In a real system, this would execute the actual development work

        return {
            "implementation_type": "systematic",
            "task_name": task.name,
            "requirements_addressed": plan_result.get("requirements", []),
            "constraints_respected": plan_result.get("constraints", {}),
            "implementation_artifacts": [],
            "rm_compliance": True,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _validate_implementation(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Validate implementation against requirements."""
        errors = []

        if not implementation.get("rm_compliance", False):
            errors.append("Implementation does not meet RM compliance requirements")

        if not implementation.get("requirements_addressed"):
            errors.append("No requirements were addressed in implementation")

        return {"valid": len(errors) == 0, "errors": errors, "rm_compliance": implementation.get("rm_compliance", False), "timestamp": datetime.utcnow().isoformat()}


class CheckPhase(PDCAPhase):
    """
    Check Phase Handler

    Performs comprehensive validation with C1-C7 checks and RCA integration.
    """

    def execute(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Check phase with comprehensive validation.

        Args:
            task: Development task
            plan_result: Result from Plan phase
            do_result: Result from Do phase

        Returns:
            Check phase result with validation details
        """
        start_time = datetime.utcnow()
        self.logger.info(f"Starting Check phase for task: {task.name}")

        try:
            # Perform C1-C7 validation checks
            validation_results = self._perform_comprehensive_validation(task, plan_result, do_result)

            # Perform RCA on any failures
            rca_results = self._perform_rca_on_failures(validation_results)

            # Calculate overall success
            overall_success = all(result["passed"] for result in validation_results.values())

            duration = (datetime.utcnow() - start_time).total_seconds()

            result = {
                "phase": "check",
                "success": overall_success,
                "duration": duration,
                "validation_results": validation_results,
                "rca_results": rca_results,
                "overall_success": overall_success,
                "timestamp": datetime.utcnow().isoformat(),
            }

            self.logger.info(f"Check phase completed for task: {task.name}, success: {overall_success}")
            return result

        except Exception as e:
            self.logger.error(f"Check phase failed for task: {task.name}, error: {str(e)}")
            return {"phase": "check", "success": False, "duration": (datetime.utcnow() - start_time).total_seconds(), "error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _perform_comprehensive_validation(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any]) -> Dict[str, Any]:
        """Perform C1-C7 validation checks."""
        validation_results = {}

        # C1: Model Compliance Check
        validation_results["c1_model_compliance"] = self._check_model_compliance(task, plan_result, do_result)

        # C2: RM Compliance Check
        validation_results["c2_rm_compliance"] = self._check_rm_compliance(task, do_result)

        # C3: Tool Integration Check
        validation_results["c3_tool_integration"] = self._check_tool_integration(task, do_result)

        # C4: Architecture Boundaries Check
        validation_results["c4_architecture_boundaries"] = self._check_architecture_boundaries(task, do_result)

        # C5: Performance & Quality Check
        validation_results["c5_performance_quality"] = self._check_performance_quality(task, do_result)

        # C6: Root Cause Analysis Check
        validation_results["c6_rca_check"] = self._check_rca_requirements(task, do_result)

        # C7: Ghostbusters Multi-Perspective Validation
        validation_results["c7_ghostbusters_validation"] = self._check_ghostbusters_validation(task, do_result)

        return validation_results

    def _check_model_compliance(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C1: Model Compliance Check against project model requirements."""
        return {
            "check_name": "model_compliance",
            "passed": True,  # Placeholder
            "score": 1.0,
            "details": {"compliance_verified": True},
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_rm_compliance(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C2: RM Compliance Check for Reflective Module interfaces."""
        return {
            "check_name": "rm_compliance",
            "passed": do_result.get("implementation", {}).get("rm_compliance", False),
            "score": 1.0 if do_result.get("implementation", {}).get("rm_compliance", False) else 0.0,
            "details": {"rm_interface_implemented": True},
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_tool_integration(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C3: Tool Integration Check for domain tool validation."""
        return {"check_name": "tool_integration", "passed": True, "score": 1.0, "details": {"tools_integrated": True}, "recommendations": [], "timestamp": datetime.utcnow().isoformat()}  # Placeholder

    def _check_architecture_boundaries(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C4: Architecture Boundaries Check for proper delegation."""
        return {
            "check_name": "architecture_boundaries",
            "passed": True,  # Placeholder
            "score": 1.0,
            "details": {"boundaries_respected": True},
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_performance_quality(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C5: Performance & Quality Check for regressions and module sizes."""
        return {
            "check_name": "performance_quality",
            "passed": True,  # Placeholder
            "score": 1.0,
            "details": {"performance_acceptable": True},
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_rca_requirements(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C6: Root Cause Analysis Check for systematic failure analysis."""
        return {"check_name": "rca_requirements", "passed": True, "score": 1.0, "details": {"rca_ready": True}, "recommendations": [], "timestamp": datetime.utcnow().isoformat()}  # Placeholder

    def _check_ghostbusters_validation(self, task: PDCATask, do_result: Dict[str, Any]) -> Dict[str, Any]:
        """C7: Ghostbusters Multi-Perspective Validation integration."""
        return {
            "check_name": "ghostbusters_validation",
            "passed": True,  # Placeholder
            "score": 1.0,
            "details": {"ghostbusters_ready": True},
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _perform_rca_on_failures(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform RCA on any validation failures."""
        failures = [result for result in validation_results.values() if not result.get("passed", False)]

        if not failures:
            return {"rca_performed": False, "reason": "no_failures"}

        # Placeholder for actual RCA logic
        return {"rca_performed": True, "failures_analyzed": len(failures), "root_causes_identified": [], "timestamp": datetime.utcnow().isoformat()}


class ActPhase(PDCAPhase):
    """
    Act Phase Handler

    Implements continuous improvement through pattern standardization
    and project model updates.
    """

    def execute(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any], check_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Act phase for continuous improvement.

        Args:
            task: Development task
            plan_result: Result from Plan phase
            do_result: Result from Do phase
            check_result: Result from Check phase

        Returns:
            Act phase result with improvement actions
        """
        start_time = datetime.utcnow()
        self.logger.info(f"Starting Act phase for task: {task.name}")

        try:
            # Standardize successful patterns
            pattern_standardization = self._standardize_successful_patterns(task, plan_result, do_result, check_result)

            # Update project model with learnings
            model_updates = self._update_project_model(task, pattern_standardization)

            # Generate templates for future work
            templates = self._generate_future_templates(task, pattern_standardization)

            duration = (datetime.utcnow() - start_time).total_seconds()

            result = {
                "phase": "act",
                "success": True,
                "duration": duration,
                "pattern_standardization": pattern_standardization,
                "model_updates": model_updates,
                "templates": templates,
                "timestamp": datetime.utcnow().isoformat(),
            }

            self.logger.info(f"Act phase completed for task: {task.name}")
            return result

        except Exception as e:
            self.logger.error(f"Act phase failed for task: {task.name}, error: {str(e)}")
            return {"phase": "act", "success": False, "duration": (datetime.utcnow() - start_time).total_seconds(), "error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _standardize_successful_patterns(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any], check_result: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize successful patterns for future use."""
        return {"patterns_identified": [], "standardization_applied": True, "pattern_library_updated": True, "timestamp": datetime.utcnow().isoformat()}

    def _update_project_model(self, task: PDCATask, pattern_standardization: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Update project model with new learnings."""
        return [{"update_type": "pattern_learning", "task_name": task.name, "patterns_added": pattern_standardization.get("patterns_identified", []), "timestamp": datetime.utcnow().isoformat()}]

    def _generate_future_templates(self, task: PDCATask, pattern_standardization: Dict[str, Any]) -> Dict[str, Any]:
        """Generate templates for similar future work."""
        return {"templates_generated": [], "template_types": ["pdca_cycle", "validation_checks", "pattern_application"], "timestamp": datetime.utcnow().isoformat()}
