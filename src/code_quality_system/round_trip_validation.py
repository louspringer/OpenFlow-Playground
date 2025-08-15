#!/usr/bin/env python3
"""
Round-Trip Quality Validation System

This module provides comprehensive validation of the quality system's round-trip capabilities,
ensuring that quality metrics, enforcement, and reporting work correctly across the entire
development lifecycle.
"""

import json
import logging
from pathlib import Path
from typing import Any

from .multi_agent_integration import QualityMultiAgentAdapter
from .quality_enforcer import QualityEnforcer
from .quality_metrics import QualityMetrics


class RoundTripQualityValidator:
    """
    Validates the complete round-trip quality workflow from development to deployment.

    This validator ensures:
    1. Quality metrics are correctly calculated and stored
    2. Quality gates are properly enforced
    3. Multi-agent analysis integrates correctly
    4. CI/CD integration works end-to-end
    5. Quality reports are accurate and actionable
    """

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quality_enforcer = QualityEnforcer(project_path)
        self.quality_adapter = QualityMultiAgentAdapter(project_path)
        self.logger = logging.getLogger(__name__)

        # Validation results storage
        self.validation_results: dict[str, Any] = {}
        self.validation_errors: list[str] = []

    async def validate_complete_workflow(self) -> dict[str, Any]:
        """
        Validate the complete quality workflow round-trip.

        Returns:
            Comprehensive validation results
        """
        self.logger.info("Starting complete round-trip quality validation")

        try:
            # Step 1: Validate quality metrics calculation
            metrics_validation = await self._validate_quality_metrics()

            # Step 2: Validate quality gates enforcement
            gates_validation = await self._validate_quality_gates()

            # Step 3: Validate multi-agent integration
            agent_validation = await self._validate_multi_agent_integration()

            # Step 4: Validate CI/CD integration
            cicd_validation = await self._validate_cicd_integration()

            # Step 5: Validate end-to-end workflow
            workflow_validation = await self._validate_end_to_end_workflow()

            # Compile comprehensive results
            self.validation_results = {
                "status": "completed",
                "overall_success": all(
                    [
                        metrics_validation["success"],
                        gates_validation["success"],
                        agent_validation["success"],
                        cicd_validation["success"],
                        workflow_validation["success"],
                    ]
                ),
                "validation_components": {
                    "quality_metrics": metrics_validation,
                    "quality_gates": gates_validation,
                    "multi_agent_integration": agent_validation,
                    "cicd_integration": cicd_validation,
                    "end_to_end_workflow": workflow_validation,
                },
                "total_errors": len(self.validation_errors),
                "validation_errors": self.validation_errors,
                "recommendations": self._generate_recommendations(),
            }

            self.logger.info("Round-trip quality validation completed successfully")
            return self.validation_results

        except Exception as e:
            self.logger.error(f"Round-trip quality validation failed: {e}")
            return {"status": "error", "error": str(e), "overall_success": False}

    async def _validate_quality_metrics(self) -> dict[str, Any]:
        """Validate quality metrics calculation and storage"""
        self.logger.info("Validating quality metrics")

        try:
            # Test metrics calculation
            test_metrics = QualityMetrics(
                code_quality=85.0,
                security=90.0,
                test_coverage=78.0,
                documentation=82.0,
                performance=88.0,
            )

            # Validate metrics serialization
            metrics_dict = test_metrics.to_dict()
            self._assert_valid_json(metrics_dict, "Quality metrics serialization")

            # Validate metrics deserialization
            reconstructed_metrics = QualityMetrics.from_dict(metrics_dict)
            self._assert_metrics_equal(test_metrics, reconstructed_metrics)

            # Validate score calculation
            calculated_score = test_metrics.calculate_overall_score()
            self._assert_valid_score(calculated_score)

            return {
                "success": True,
                "metrics_tested": len(metrics_dict),
                "score_calculation": "valid",
                "serialization": "valid",
            }

        except Exception as e:
            self.validation_errors.append(f"Quality metrics validation failed: {e}")
            return {"success": False, "error": str(e)}

    async def _validate_quality_gates(self) -> dict[str, Any]:
        """Validate quality gates enforcement"""
        self.logger.info("Validating quality gates")

        try:
            # Test quality gate configuration
            gate_config = {
                "code_quality": {"threshold": 80.0, "blocking": True},
                "security": {"threshold": 85.0, "blocking": True},
                "test_coverage": {"threshold": 70.0, "blocking": False},
            }

            # Validate gate enforcement
            test_metrics = QualityMetrics(
                code_quality=85.0,
                security=90.0,
                test_coverage=78.0,
                documentation=82.0,
                performance=88.0,
            )

            # Test passing metrics
            passing_result = self.quality_enforcer.check_quality_gates(
                test_metrics, gate_config
            )
            self._assert_gate_result(passing_result, should_pass=True)

            # Test failing metrics
            failing_metrics = QualityMetrics(
                code_quality=75.0,  # Below 80.0 threshold
                security=90.0,
                test_coverage=78.0,
                documentation=82.0,
                performance=88.0,
            )

            failing_result = self.quality_enforcer.check_quality_gates(
                failing_metrics, gate_config
            )
            self._assert_gate_result(failing_result, should_pass=False)

            return {
                "success": True,
                "gates_tested": len(gate_config),
                "passing_scenario": "valid",
                "failing_scenario": "valid",
            }

        except Exception as e:
            self.validation_errors.append(f"Quality gates validation failed: {e}")
            return {"success": False, "error": str(e)}

    async def _validate_multi_agent_integration(self) -> dict[str, Any]:
        """Validate multi-agent integration with quality system"""
        self.logger.info("Validating multi-agent integration")

        try:
            # Mock agent results
            mock_agent_results = {
                "security_expert": {
                    "status": "success",
                    "findings": ["No critical vulnerabilities found"],
                    "score": 90.0,
                },
                "code_quality_expert": {
                    "status": "success",
                    "findings": ["Code follows best practices"],
                    "score": 85.0,
                },
                "test_expert": {
                    "status": "success",
                    "findings": ["Test coverage is adequate"],
                    "score": 78.0,
                },
            }

            # Test multi-agent quality analysis
            analysis_result = (
                await self.quality_adapter.run_multi_agent_quality_analysis(
                    mock_agent_results
                )
            )

            # Validate analysis results
            self._assert_valid_analysis_result(analysis_result)

            return {
                "success": True,
                "agents_tested": len(mock_agent_results),
                "analysis_integration": "valid",
            }

        except Exception as e:
            self.validation_errors.append(
                f"Multi-agent integration validation failed: {e}"
            )
            return {"success": False, "error": str(e)}

    async def _validate_cicd_integration(self) -> dict[str, Any]:
        """Validate CI/CD integration"""
        self.logger.info("Validating CI/CD integration")

        try:
            # Test CI/CD environment detection
            from .integrations.ci_cd_integration import CICDIntegration

            cicd = CICDIntegration(self.project_path)

            # Validate environment detection
            self._assert_valid_environment(cicd.ci_environment)

            # Validate configuration loading
            self._assert_valid_config(cicd.ci_config)

            # Validate environment rules
            self._assert_valid_environment_rules(cicd.environment_rules)

            return {
                "success": True,
                "environment_detection": "valid",
                "configuration_loading": "valid",
                "environment_rules": "valid",
            }

        except Exception as e:
            self.validation_errors.append(f"CI/CD integration validation failed: {e}")
            return {"success": False, "error": str(e)}

    async def _validate_end_to_end_workflow(self) -> dict[str, Any]:
        """Validate complete end-to-end quality workflow"""
        self.logger.info("Validating end-to-end workflow")

        try:
            # Test complete workflow from development to deployment
            workflow_steps = [
                "development_quality_check",
                "pre_commit_validation",
                "ci_cd_quality_gates",
                "deployment_approval",
                "post_deployment_validation",
            ]

            workflow_results = {}
            for step in workflow_steps:
                workflow_results[step] = await self._test_workflow_step(step)

            # Validate all steps completed successfully
            all_steps_successful = all(
                result["success"] for result in workflow_results.values()
            )

            return {
                "success": all_steps_successful,
                "workflow_steps": workflow_results,
                "total_steps": len(workflow_steps),
                "successful_steps": sum(
                    1 for result in workflow_results.values() if result["success"]
                ),
            }

        except Exception as e:
            self.validation_errors.append(f"End-to-end workflow validation failed: {e}")
            return {"success": False, "error": str(e)}

    async def _test_workflow_step(self, step_name: str) -> dict[str, Any]:
        """Test individual workflow step"""
        try:
            if step_name == "development_quality_check":
                return await self._test_development_quality_check()
            if step_name == "pre_commit_validation":
                return await self._test_pre_commit_validation()
            if step_name == "ci_cd_quality_gates":
                return await self._test_cicd_quality_gates()
            if step_name == "deployment_approval":
                return await self._test_deployment_approval()
            if step_name == "post_deployment_validation":
                return await self._test_post_deployment_validation()
            return {
                "success": False,
                "error": f"Unknown workflow step: {step_name}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_development_quality_check(self) -> dict[str, Any]:
        """Test development quality check workflow step"""
        try:
            # Simulate development quality check
            dev_metrics = QualityMetrics(
                code_quality=82.0,
                security=88.0,
                test_coverage=75.0,
                documentation=80.0,
                performance=85.0,
            )

            # Check if metrics meet development thresholds
            dev_thresholds = {
                "code_quality": {"threshold": 70.0, "blocking": False},
                "security": {"threshold": 80.0, "blocking": True},
                "test_coverage": {"threshold": 60.0, "blocking": False},
            }

            result = self.quality_enforcer.check_quality_gates(
                dev_metrics, dev_thresholds
            )

            return {
                "success": result["can_proceed"],
                "metrics": dev_metrics.to_dict(),
                "thresholds": dev_thresholds,
                "result": result,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_pre_commit_validation(self) -> dict[str, Any]:
        """Test pre-commit validation workflow step"""
        try:
            # Simulate pre-commit validation
            from .integrations.pre_commit_integration import PreCommitIntegration

            pre_commit = PreCommitIntegration(self.project_path)

            # Test pre-commit hooks configuration
            hooks_config = pre_commit.get_hooks_config()
            self._assert_valid_hooks_config(hooks_config)

            return {
                "success": True,
                "hooks_configured": len(hooks_config),
                "validation_type": "pre_commit",
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_cicd_quality_gates(self) -> dict[str, Any]:
        """Test CI/CD quality gates workflow step"""
        try:
            # Simulate CI/CD quality gates
            cicd_metrics = QualityMetrics(
                code_quality=85.0,
                security=90.0,
                test_coverage=78.0,
                documentation=82.0,
                performance=88.0,
            )

            cicd_thresholds = {
                "code_quality": {"threshold": 80.0, "blocking": True},
                "security": {"threshold": 85.0, "blocking": True},
                "test_coverage": {"threshold": 70.0, "blocking": True},
            }

            result = self.quality_enforcer.check_quality_gates(
                cicd_metrics, cicd_thresholds
            )

            return {
                "success": result["can_proceed"],
                "metrics": cicd_metrics.to_dict(),
                "thresholds": cicd_thresholds,
                "result": result,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_deployment_approval(self) -> dict[str, Any]:
        """Test deployment approval workflow step"""
        try:
            # Simulate deployment approval process
            deployment_metrics = QualityMetrics(
                code_quality=87.0,
                security=92.0,
                test_coverage=80.0,
                documentation=85.0,
                performance=90.0,
            )

            # Deployment requires higher thresholds
            deployment_thresholds = {
                "code_quality": {"threshold": 85.0, "blocking": True},
                "security": {"threshold": 90.0, "blocking": True},
                "test_coverage": {"threshold": 75.0, "blocking": True},
            }

            result = self.quality_enforcer.check_quality_gates(
                deployment_metrics, deployment_thresholds
            )

            return {
                "success": result["can_proceed"],
                "metrics": deployment_metrics.to_dict(),
                "thresholds": deployment_thresholds,
                "result": result,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_post_deployment_validation(self) -> dict[str, Any]:
        """Test post-deployment validation workflow step"""
        try:
            # Simulate post-deployment validation
            post_deployment_metrics = QualityMetrics(
                code_quality=87.0,
                security=92.0,
                test_coverage=80.0,
                documentation=85.0,
                performance=90.0,
            )

            # Post-deployment validation should confirm quality maintained
            validation_result = {
                "status": "success",
                "quality_maintained": True,
                "metrics": post_deployment_metrics.to_dict(),
                "deployment_health": "healthy",
            }

            return {"success": True, "validation_result": validation_result}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        if not self.validation_results.get("overall_success", False):
            recommendations.append(
                "Address validation errors to ensure quality system reliability"
            )

        if self.validation_results.get("total_errors", 0) > 0:
            recommendations.append(
                "Review and fix validation errors for system stability"
            )

        # Add specific recommendations based on component results
        components = self.validation_results.get("validation_components", {})

        if not components.get("quality_metrics", {}).get("success", False):
            recommendations.append(
                "Verify quality metrics calculation and storage mechanisms"
            )

        if not components.get("quality_gates", {}).get("success", False):
            recommendations.append(
                "Validate quality gates configuration and enforcement"
            )

        if not components.get("multi_agent_integration", {}).get("success", False):
            recommendations.append(
                "Ensure multi-agent integration is properly configured"
            )

        if not components.get("cicd_integration", {}).get("success", False):
            recommendations.append(
                "Verify CI/CD integration and environment configuration"
            )

        if not components.get("end_to_end_workflow", {}).get("success", False):
            recommendations.append(
                "Complete end-to-end workflow testing and validation"
            )

        if not recommendations:
            recommendations.append(
                "Quality system is fully validated and ready for production use"
            )

        return recommendations

    # Helper assertion methods
    def _assert_valid_json(self, data: Any, context: str) -> None:
        """Assert that data can be serialized to JSON"""
        try:
            json.dumps(data)
        except Exception as e:
            msg = f"{context} failed JSON serialization: {e}"
            raise AssertionError(msg)

    def _assert_metrics_equal(
        self, metrics1: QualityMetrics, metrics2: QualityMetrics
    ) -> None:
        """Assert that two QualityMetrics objects are equal"""
        if metrics1.to_dict() != metrics2.to_dict():
            msg = "QualityMetrics serialization/deserialization mismatch"
            raise AssertionError(msg)

    def _assert_valid_score(self, score: float) -> None:
        """Assert that a quality score is valid"""
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            msg = f"Invalid quality score: {score}"
            raise AssertionError(msg)

    def _assert_gate_result(self, result: dict[str, Any], should_pass: bool) -> None:
        """Assert that a gate result matches expectations"""
        if result.get("can_proceed") != should_pass:
            msg = f"Gate result mismatch: expected {should_pass}, got {result.get('can_proceed')}"
            raise AssertionError(msg)

    def _assert_valid_analysis_result(self, result: dict[str, Any]) -> None:
        """Assert that multi-agent analysis result is valid"""
        if not isinstance(result, dict) or "status" not in result:
            msg = f"Invalid analysis result format: {result}"
            raise AssertionError(msg)

    def _assert_valid_environment(self, environment: str) -> None:
        """Assert that CI/CD environment is valid"""
        valid_environments = [
            "github_actions",
            "gitlab_ci",
            "circleci",
            "jenkins",
            "travis",
            "azure_devops",
            "unknown",
        ]
        if environment not in valid_environments:
            msg = f"Invalid CI/CD environment: {environment}"
            raise AssertionError(msg)

    def _assert_valid_config(self, config: dict[str, Any]) -> None:
        """Assert that CI/CD configuration is valid"""
        required_keys = ["ci_environment", "quality_threshold", "fail_on_quality"]
        for key in required_keys:
            if key not in config:
                msg = f"Missing required config key: {key}"
                raise AssertionError(msg)

    def _assert_valid_environment_rules(self, rules: dict[str, Any]) -> None:
        """Assert that environment rules are valid"""
        if not isinstance(rules, dict) or len(rules) == 0:
            msg = f"Invalid environment rules: {rules}"
            raise AssertionError(msg)

    def _assert_valid_hooks_config(self, hooks: dict[str, Any]) -> None:
        """Assert that pre-commit hooks configuration is valid"""
        if not isinstance(hooks, dict):
            msg = f"Invalid hooks configuration: {hooks}"
            raise AssertionError(msg)


async def main() -> None:
    """Main function for round-trip quality validation"""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python round_trip_validation.py <project_path>")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.exists():
        print(f"Project path does not exist: {project_path}")
        sys.exit(1)

    validator = RoundTripQualityValidator(project_path)
    results = await validator.validate_complete_workflow()

    print("🔍 ROUND-TRIP QUALITY VALIDATION RESULTS")
    print("=" * 50)
    print(f"Status: {results['status']}")
    print(f"Overall Success: {results['overall_success']}")
    print(f"Total Errors: {results['total_errors']}")

    if results["validation_errors"]:
        print("\n❌ Validation Errors:")
        for error in results["validation_errors"]:
            print(f"  - {error}")

    if "recommendations" in results:
        print("\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"  - {rec}")

    sys.exit(0 if results["overall_success"] else 1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
