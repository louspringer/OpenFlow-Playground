"""
PDCA Orchestrator

Implements systematic Plan-Do-Check-Act workflow for real development tasks,
using project model registry for intelligence-driven decisions.

Requirements Compliance: R2 - PDCA Execution
- R2.1: Execute complete Plan-Do-Check-Act cycle on real tasks
- R2.2: Use project model registry for planning
- R2.3: Implement systematically, not ad-hoc
- R2.4: Validate against model + perform RCA on failures
- R2.5: Update project model with lessons learned
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from ..base.reflective_module import ReflectiveModule, HealthStatus
from ..base.data_models import PDCAResult, PDCAPhase
from .phases import PlanPhase, DoPhase, CheckPhase, ActPhase
from .context import PDCATask


class PDCAOrchestrator(ReflectiveModule):
    """
    Orchestrates systematic PDCA cycles for real development tasks.

    Ensures model-driven decisions, systematic implementation, and continuous
    improvement through project registry integration.
    """

    def __init__(self, project_root: str = "."):
        """
        Initialize the PDCA Orchestrator.

        Args:
            project_root: Root directory of the project
        """
        super().__init__("PDCAOrchestrator", "1.0.0")
        self.project_root = Path(project_root)
        self.model_registry_path = self.project_root / "project_model_registry.json"
        self.model_registry = None
        self.phase_handlers = {PDCAPhase.PLAN: PlanPhase(self), PDCAPhase.DO: DoPhase(self), PDCAPhase.CHECK: CheckPhase(self), PDCAPhase.ACT: ActPhase(self)}
        self._load_model_registry()
        self._setup_logging()

    def execute_real_task_cycle(self, task: PDCATask) -> PDCAResult:
        """
        Execute complete PDCA cycle on actual development task.

        Args:
            task: Development task to execute PDCA cycle on

        Returns:
            Complete PDCA result with all phases
        """
        logging.info(f"Starting PDCA cycle for task: {task.name}")
        start_time = datetime.utcnow()

        try:
            # Plan Phase
            plan_result = self._execute_plan_phase(task)

            # Do Phase
            do_result = self._execute_do_phase(task, plan_result)

            # Check Phase
            check_result = self._execute_check_phase(task, plan_result, do_result)

            # Act Phase
            act_result = self._execute_act_phase(task, plan_result, do_result, check_result)

            # Create comprehensive result
            pdca_result = PDCAResult(
                task=task.name,
                phase=PDCAPhase.ACT,  # Final phase
                plan_result=plan_result,
                do_result=do_result,
                check_result=check_result,
                act_result=act_result,
                success=check_result.get("success", False),
                metrics=self._calculate_metrics(start_time, plan_result, do_result, check_result, act_result),
                timestamp=datetime.utcnow(),
                model_updates=act_result.get("model_updates", []),
            )

            logging.info(f"PDCA cycle completed for task: {task.name}, success: {pdca_result.success}")
            return pdca_result

        except Exception as e:
            logging.error(f"PDCA cycle failed for task: {task.name}, error: {str(e)}")
            self.update_health_status(HealthStatus.DEGRADED, {"error": str(e)})
            raise

    def _execute_plan_phase(self, task: PDCATask) -> Dict[str, Any]:
        """Execute Plan phase using model-driven intelligence."""
        return self.phase_handlers[PDCAPhase.PLAN].execute(task)

    def _execute_do_phase(self, task: PDCATask, plan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Do phase with systematic implementation."""
        return self.phase_handlers[PDCAPhase.DO].execute(task, plan_result)

    def _execute_check_phase(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Check phase with validation and RCA."""
        return self.phase_handlers[PDCAPhase.CHECK].execute(task, plan_result, do_result)

    def _execute_act_phase(self, task: PDCATask, plan_result: Dict[str, Any], do_result: Dict[str, Any], check_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Act phase with continuous improvement."""
        return self.phase_handlers[PDCAPhase.ACT].execute(task, plan_result, do_result, check_result)

    def _load_model_registry(self):
        """Load project model registry for intelligence-driven decisions."""
        try:
            if self.model_registry_path.exists():
                with open(self.model_registry_path, "r") as f:
                    self.model_registry = json.load(f)
                logging.info("Project model registry loaded successfully")
            else:
                logging.warning("Project model registry not found, using empty registry")
                self.model_registry = {"domains": {}, "requirements_traceability": []}
        except Exception as e:
            logging.error(f"Failed to load model registry: {str(e)}")
            self.model_registry = {"domains": {}, "requirements_traceability": []}

    def _setup_logging(self):
        """Setup logging for PDCA operations."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _calculate_metrics(self, start_time: datetime, plan_result: Dict[str, Any], do_result: Dict[str, Any], check_result: Dict[str, Any], act_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate PDCA cycle metrics."""
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()

        return {
            "total_duration": duration,
            "plan_duration": plan_result.get("duration", 0),
            "do_duration": do_result.get("duration", 0),
            "check_duration": check_result.get("duration", 0),
            "act_duration": act_result.get("duration", 0),
            "success_rate": 1.0 if check_result.get("success", False) else 0.0,
            "model_updates_count": len(act_result.get("model_updates", [])),
            "timestamp": end_time.isoformat(),
        }

    # ReflectiveModule interface implementation
    def get_module_status(self) -> Dict[str, Any]:
        """Get operational visibility for external systems."""
        return {
            "orchestrator_name": self.name,
            "version": self.version,
            "project_root": str(self.project_root),
            "model_registry_loaded": self.model_registry is not None,
            "phase_handlers_count": len(self.phase_handlers),
            "health_status": self._health_status.value,
            "operational_data": self._operational_visibility,
        }

    def is_healthy(self) -> bool:
        """Check if orchestrator is healthy."""
        return self._health_status == HealthStatus.HEALTHY and self.model_registry is not None and len(self.phase_handlers) == 4

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        return {
            "model_registry_status": "loaded" if self.model_registry else "not_loaded",
            "phase_handlers_status": "all_loaded" if len(self.phase_handlers) == 4 else "partial",
            "project_root_accessible": self.project_root.exists(),
            "last_health_check": datetime.utcnow().isoformat(),
        }
