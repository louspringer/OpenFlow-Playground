"""
Tool Health Manager

Implements systematic tool health diagnostics and repair capabilities
with systematic fix generation and prevention patterns.

Requirements Compliance: R3 - Tool Fixing
- R3.1: Systematic tool health diagnostics and repair
- R3.2: Integration with existing tool ecosystem
- R3.3: Systematic fix generation with validation
- R3.4: Prevention pattern generation and application
- R3.5: Tool health monitoring and alerting
"""

import logging
import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

from ..base.reflective_module import ReflectiveModule, HealthStatus
from ..base.data_models import ToolRepairResult, ToolHealthAssessment, MakefileDiagnosisResult
from .diagnostics import ToolDiagnosticsEngine
from .repair import ToolRepairEngine
from .prevention import ToolPreventionEngine


@dataclass
class ToolHealthStatus:
    """Health status of a tool."""

    tool_name: str
    is_healthy: bool
    health_score: float
    issues: List[str]
    recommendations: List[str]
    last_checked: datetime


class ToolHealthManager(ReflectiveModule):
    """
    Manages tool health with systematic diagnostics and repair.

    Provides comprehensive tool health monitoring, systematic repair,
    and prevention pattern generation for the entire tool ecosystem.
    """

    def __init__(self, project_root: str = "."):
        """
        Initialize the Tool Health Manager.

        Args:
            project_root: Root directory of the project
        """
        super().__init__("ToolHealthManager", "1.0.0")
        self.project_root = Path(project_root)
        self.diagnostics = ToolDiagnosticsEngine()
        self.repair = ToolRepairEngine()
        self.prevention = ToolPreventionEngine()
        self.tool_registry = self._load_tool_registry()
        self.health_status_cache = {}
        self._setup_logging()

    def diagnose_tool_health(self, tool_name: str) -> ToolHealthAssessment:
        """
        Perform comprehensive tool health diagnosis.

        Args:
            tool_name: Name of the tool to diagnose

        Returns:
            Comprehensive tool health assessment
        """
        self.logger.info(f"Diagnosing tool health for: {tool_name}")
        start_time = datetime.utcnow()

        try:
            # Get tool configuration
            tool_config = self.tool_registry.get(tool_name, {})
            if not tool_config:
                raise ValueError(f"Tool not found in registry: {tool_name}")

            # Perform systematic diagnostics
            diagnostics_result = self.diagnostics.perform_diagnostics(tool_name, tool_config)

            # Assess overall health
            health_score = self._calculate_health_score(diagnostics_result)
            is_healthy = health_score >= 0.8

            # Generate recommendations
            recommendations = self._generate_recommendations(diagnostics_result, health_score)

            # Create assessment
            assessment = ToolHealthAssessment(
                tool_name=tool_name,
                status=HealthStatus.HEALTHY if is_healthy else HealthStatus.DEGRADED,
                installation_integrity=diagnostics_result.get("installation_integrity", {}),
                dependency_check=diagnostics_result.get("dependency_check", {}),
                configuration_check=diagnostics_result.get("configuration_check", {}),
                version_compatibility=diagnostics_result.get("version_compatibility", {}),
                overall_health_score=health_score,
                recommendations=recommendations,
                timestamp=datetime.utcnow(),
            )

            # Cache health status
            self.health_status_cache[tool_name] = ToolHealthStatus(
                tool_name=tool_name, is_healthy=is_healthy, health_score=health_score, issues=diagnostics_result.get("issues", []), recommendations=recommendations, last_checked=datetime.utcnow()
            )

            self.logger.info(f"Tool health diagnosis completed for {tool_name}: {health_score:.2f}")
            return assessment

        except Exception as e:
            self.logger.error(f"Tool health diagnosis failed for {tool_name}: {str(e)}")
            self.update_health_status(HealthStatus.DEGRADED, {"error": str(e)})
            raise

    def repair_tool(self, tool_name: str, repair_strategy: str = "systematic") -> ToolRepairResult:
        """
        Repair a tool using systematic approach.

        Args:
            tool_name: Name of the tool to repair
            repair_strategy: Repair strategy ("systematic", "quick", "comprehensive")

        Returns:
            Tool repair result with validation
        """
        self.logger.info(f"Repairing tool: {tool_name} with strategy: {repair_strategy}")
        start_time = datetime.utcnow()

        try:
            # Get current health status
            if tool_name not in self.health_status_cache:
                self.diagnose_tool_health(tool_name)

            health_status = self.health_status_cache[tool_name]
            if health_status.is_healthy:
                return ToolRepairResult(
                    tool_name=tool_name,
                    root_cause_identified="no_repair_needed",
                    systematic_fix_applied={},
                    fix_validation={"valid": True, "reason": "tool_already_healthy"},
                    prevention_pattern={},
                    repair_time=0.0,
                    success=True,
                    timestamp=datetime.utcnow(),
                )

            # Identify root cause
            root_cause = self._identify_root_cause(tool_name, health_status)

            # Generate systematic fix
            systematic_fix = self.repair.generate_systematic_fix(tool_name, root_cause, health_status.issues)

            # Apply fix
            fix_result = self.repair.apply_fix(tool_name, systematic_fix)

            # Validate fix
            fix_validation = self._validate_fix(tool_name, systematic_fix, fix_result)

            # Generate prevention pattern
            prevention_pattern = self.prevention.generate_prevention_pattern(tool_name, root_cause, systematic_fix)

            # Calculate repair time
            repair_time = (datetime.utcnow() - start_time).total_seconds()

            # Create repair result
            repair_result = ToolRepairResult(
                tool_name=tool_name,
                root_cause_identified=root_cause,
                systematic_fix_applied=systematic_fix,
                fix_validation=fix_validation,
                prevention_pattern=prevention_pattern,
                repair_time=repair_time,
                success=fix_validation.get("valid", False),
                timestamp=datetime.utcnow(),
            )

            # Update health status cache
            if repair_result.success:
                self.health_status_cache[tool_name].is_healthy = True
                self.health_status_cache[tool_name].health_score = 1.0

            self.logger.info(f"Tool repair completed for {tool_name}: {repair_result.success}")
            return repair_result

        except Exception as e:
            self.logger.error(f"Tool repair failed for {tool_name}: {str(e)}")
            self.update_health_status(HealthStatus.DEGRADED, {"error": str(e)})
            raise

    def diagnose_makefile_health(self) -> MakefileDiagnosisResult:
        """
        Diagnose Makefile health and identify issues.

        Returns:
            Makefile diagnosis result
        """
        self.logger.info("Diagnosing Makefile health")
        start_time = datetime.utcnow()

        try:
            makefile_path = self.project_root / "Makefile"
            if not makefile_path.exists():
                return MakefileDiagnosisResult(
                    missing_files=["Makefile"],
                    broken_targets=[],
                    dependency_issues=[],
                    root_cause="makefile_missing",
                    diagnosis_time=(datetime.utcnow() - start_time).total_seconds(),
                    timestamp=datetime.utcnow(),
                )

            # Check Makefile syntax
            syntax_check = self._check_makefile_syntax(makefile_path)

            # Check targets
            targets_check = self._check_makefile_targets(makefile_path)

            # Check dependencies
            dependencies_check = self._check_makefile_dependencies(makefile_path)

            # Identify root cause
            root_cause = self._identify_makefile_root_cause(syntax_check, targets_check, dependencies_check)

            diagnosis_time = (datetime.utcnow() - start_time).total_seconds()

            return MakefileDiagnosisResult(
                missing_files=syntax_check.get("missing_files", []),
                broken_targets=targets_check.get("broken_targets", []),
                dependency_issues=dependencies_check.get("dependency_issues", []),
                root_cause=root_cause,
                diagnosis_time=diagnosis_time,
                timestamp=datetime.utcnow(),
            )

        except Exception as e:
            self.logger.error(f"Makefile diagnosis failed: {str(e)}")
            return MakefileDiagnosisResult(
                missing_files=[], broken_targets=[], dependency_issues=[], root_cause="diagnosis_failed", diagnosis_time=(datetime.utcnow() - start_time).total_seconds(), timestamp=datetime.utcnow()
            )

    def get_all_tools_health(self) -> Dict[str, ToolHealthStatus]:
        """
        Get health status of all tools in the registry.

        Returns:
            Dictionary of tool health statuses
        """
        all_health = {}

        for tool_name in self.tool_registry.keys():
            try:
                if tool_name not in self.health_status_cache:
                    self.diagnose_tool_health(tool_name)
                all_health[tool_name] = self.health_status_cache[tool_name]
            except Exception as e:
                self.logger.error(f"Failed to get health for {tool_name}: {str(e)}")
                all_health[tool_name] = ToolHealthStatus(
                    tool_name=tool_name,
                    is_healthy=False,
                    health_score=0.0,
                    issues=[f"Health check failed: {str(e)}"],
                    recommendations=["Investigate tool configuration"],
                    last_checked=datetime.utcnow(),
                )

        return all_health

    def _load_tool_registry(self) -> Dict[str, Any]:
        """Load tool registry from project model."""
        try:
            model_registry_path = self.project_root / "project_model_registry.json"
            if model_registry_path.exists():
                with open(model_registry_path, "r") as f:
                    model_registry = json.load(f)

                # Extract tools from domains
                tools = {}
                for domain_name, domain_config in model_registry.get("domains", {}).items():
                    if "linter" in domain_config:
                        tools[domain_config["linter"]] = {"domain": domain_name, "type": "linter", "config": domain_config}
                    if "validator" in domain_config:
                        tools[domain_config["validator"]] = {"domain": domain_name, "type": "validator", "config": domain_config}
                    if "formatter" in domain_config:
                        tools[domain_config["formatter"]] = {"domain": domain_name, "type": "formatter", "config": domain_config}

                return tools
            else:
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load tool registry: {str(e)}")
            return {}

    def _calculate_health_score(self, diagnostics_result: Dict[str, Any]) -> float:
        """Calculate overall health score from diagnostics result."""
        scores = []

        # Installation integrity score
        installation_score = diagnostics_result.get("installation_integrity", {}).get("score", 0.0)
        scores.append(installation_score)

        # Dependency check score
        dependency_score = diagnostics_result.get("dependency_check", {}).get("score", 0.0)
        scores.append(dependency_score)

        # Configuration check score
        config_score = diagnostics_result.get("configuration_check", {}).get("score", 0.0)
        scores.append(config_score)

        # Version compatibility score
        version_score = diagnostics_result.get("version_compatibility", {}).get("score", 0.0)
        scores.append(version_score)

        # Return weighted average
        if scores:
            return sum(scores) / len(scores)
        else:
            return 0.0

    def _generate_recommendations(self, diagnostics_result: Dict[str, Any], health_score: float) -> List[str]:
        """Generate recommendations based on diagnostics result."""
        recommendations = []

        if health_score < 0.5:
            recommendations.append("Tool requires immediate attention - critical issues detected")
        elif health_score < 0.8:
            recommendations.append("Tool has minor issues - consider repair")
        else:
            recommendations.append("Tool is healthy - maintain current configuration")

        # Add specific recommendations based on diagnostics
        issues = diagnostics_result.get("issues", [])
        for issue in issues:
            if "installation" in issue.lower():
                recommendations.append("Check tool installation and dependencies")
            elif "configuration" in issue.lower():
                recommendations.append("Review and update tool configuration")
            elif "version" in issue.lower():
                recommendations.append("Update tool to compatible version")

        return recommendations

    def _identify_root_cause(self, tool_name: str, health_status: ToolHealthStatus) -> str:
        """Identify root cause of tool health issues."""
        if not health_status.issues:
            return "unknown"

        # Analyze issues to identify root cause
        issues = health_status.issues

        if any("installation" in issue.lower() for issue in issues):
            return "installation_issue"
        elif any("configuration" in issue.lower() for issue in issues):
            return "configuration_issue"
        elif any("dependency" in issue.lower() for issue in issues):
            return "dependency_issue"
        elif any("version" in issue.lower() for issue in issues):
            return "version_compatibility_issue"
        else:
            return "general_health_issue"

    def _validate_fix(self, tool_name: str, systematic_fix: Dict[str, Any], fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the applied fix resolved the issues."""
        # Re-run diagnostics to validate fix
        try:
            tool_config = self.tool_registry.get(tool_name, {})
            diagnostics_result = self.diagnostics.perform_diagnostics(tool_name, tool_config)
            health_score = self._calculate_health_score(diagnostics_result)

            return {
                "valid": health_score >= 0.8,
                "health_score_after_fix": health_score,
                "issues_resolved": len(diagnostics_result.get("issues", [])) == 0,
                "validation_timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {"valid": False, "error": str(e), "validation_timestamp": datetime.utcnow().isoformat()}

    def _check_makefile_syntax(self, makefile_path: Path) -> Dict[str, Any]:
        """Check Makefile syntax."""
        try:
            result = subprocess.run(["make", "-n", "-f", str(makefile_path)], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return {"valid": True, "missing_files": []}
            else:
                return {"valid": False, "missing_files": [str(makefile_path)]}
        except Exception as e:
            return {"valid": False, "missing_files": [str(makefile_path)], "error": str(e)}

    def _check_makefile_targets(self, makefile_path: Path) -> Dict[str, Any]:
        """Check Makefile targets."""
        try:
            with open(makefile_path, "r") as f:
                content = f.read()

            # Simple target validation (in real system, would use make parser)
            targets = []
            for line in content.split("\n"):
                if ":" in line and not line.startswith("\t") and not line.startswith(" "):
                    target = line.split(":")[0].strip()
                    if target and not target.startswith("#"):
                        targets.append(target)

            # Check if common targets exist
            common_targets = ["test", "lint", "format", "clean", "install"]
            missing_targets = [target for target in common_targets if target not in targets]

            return {"targets_found": targets, "broken_targets": missing_targets}
        except Exception as e:
            return {"targets_found": [], "broken_targets": [], "error": str(e)}

    def _check_makefile_dependencies(self, makefile_path: Path) -> Dict[str, Any]:
        """Check Makefile dependencies."""
        try:
            with open(makefile_path, "r") as f:
                content = f.read()

            # Simple dependency validation
            dependency_issues = []

            # Check for circular dependencies (simplified)
            if "target1: target2" in content and "target2: target1" in content:
                dependency_issues.append("circular_dependency_detected")

            return {"dependency_issues": dependency_issues}
        except Exception as e:
            return {"dependency_issues": [f"dependency_check_failed: {str(e)}"]}

    def _identify_makefile_root_cause(self, syntax_check: Dict[str, Any], targets_check: Dict[str, Any], dependencies_check: Dict[str, Any]) -> str:
        """Identify root cause of Makefile issues."""
        if not syntax_check.get("valid", False):
            return "syntax_error"
        elif targets_check.get("broken_targets"):
            return "missing_targets"
        elif dependencies_check.get("dependency_issues"):
            return "dependency_issues"
        else:
            return "unknown"

    def _setup_logging(self):
        """Setup logging for tool health management."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)

    # ReflectiveModule interface implementation
    def get_module_status(self) -> Dict[str, Any]:
        """Get operational visibility for external systems."""
        return {
            "manager_name": self.name,
            "version": self.version,
            "tools_registered": len(self.tool_registry),
            "tools_health_cached": len(self.health_status_cache),
            "diagnostics_engine_status": "active",
            "repair_engine_status": "active",
            "prevention_engine_status": "active",
            "health_status": self._health_status.value,
            "operational_data": self._operational_visibility,
        }

    def is_healthy(self) -> bool:
        """Check if tool health manager is healthy."""
        return self._health_status == HealthStatus.HEALTHY and self.diagnostics is not None and self.repair is not None and self.prevention is not None

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        return {
            "diagnostics_engine_healthy": self.diagnostics is not None,
            "repair_engine_healthy": self.repair is not None,
            "prevention_engine_healthy": self.prevention is not None,
            "tool_registry_loaded": len(self.tool_registry) > 0,
            "health_cache_size": len(self.health_status_cache),
            "last_health_check": datetime.utcnow().isoformat(),
        }
