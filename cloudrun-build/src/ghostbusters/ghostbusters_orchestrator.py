#!/usr/bin/env python3
"""
Ghostbusters Orchestrator - Multi-Agent Delusion Detection and Recovery System

LOGGING SYSTEM FOR FUTURE DEBUGGING:
====================================

This system uses comprehensive logging to track execution flow and detect corruption:

1. [MAIN] - Main workflow entry point and initialization
2. [WORKFLOW] - Individual workflow phase execution
3. [DETECTION] - Agent execution and result processing
4. [VALIDATION] - Validator execution and result processing
5. [RECOVERY] - Recovery engine execution and result processing

CORRUPTION DETECTION:
- Each agent should run exactly once per workflow
- Data structures should maintain consistent format
- State transitions should follow expected sequence
- Confidence scores should be reasonable (0.0-1.0)

COMMON ISSUES TO WATCH FOR:
- Agents running multiple times (check agent_counts)
- Data structure mismatches (check delusions_detected format)
- Infinite loops in workflow phases
- State corruption between phases

If you see corruption, check:
1. Agent execution counts
2. Data structure consistency
3. Workflow phase transitions
4. State object integrity
"""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# LangGraph imports
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, ConfigDict, Field

# Local imports
from .agents import (
    ArchitectureExpert,
    BuildExpert,
    CodeQualityExpert,
    MCPExpert,
    ModelExpert,
    SecurityExpert,
    TestIssueExpert,
)
from .recovery import (
    ImportResolver,
    IndentationFixer,
    SyntaxRecoveryEngine,
    TypeAnnotationFixer,
)
from .validators import (
    ArchitectureValidator,
    BuildValidator,
    CodeQualityValidator,
    ModelValidator,
    SecurityValidator,
    TestIssueValidator,
)


class GhostbustersState(BaseModel):
    """State for Ghostbusters workflow"""

    project_path: str
    delusions_detected: list[dict[str, Any]] = Field(default_factory=list)
    recovery_actions: list[dict[str, Any]] = Field(default_factory=list)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    validation_results: dict[str, Any] = Field(default_factory=dict)
    recovery_results: dict[str, Any] = Field(default_factory=dict)
    current_phase: str = Field(default="detection")
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GhostbustersOrchestrator:
    """Multi-agent orchestrator for delusion detection and recovery"""

    def __init__(self, project_path: str = ".") -> None:
        self.project_path = Path(project_path)
        self.logger = logging.getLogger(__name__)

        # Initialize agents
        self.agents = {
            "security": SecurityExpert(),
            "code_quality": CodeQualityExpert(),
            "test": TestIssueExpert(),
            "build": BuildExpert(),
            "architecture": ArchitectureExpert(),
            "model": ModelExpert(),
            "mcp": MCPExpert(),
        }

        # Initialize validators
        self.validators = {
            "security": SecurityValidator(),
            "code_quality": CodeQualityValidator(),
            "test": TestIssueValidator(),
            "build": BuildValidator(),
            "architecture": ArchitectureValidator(),
            "model": ModelValidator(),
        }

        # Initialize recovery engines
        self.recovery_engines = {
            "syntax": SyntaxRecoveryEngine(),
            "indentation": IndentationFixer(),
            "imports": ImportResolver(),
            "types": TypeAnnotationFixer(),
        }

        # Create LangGraph workflow
        self.workflow = self._create_workflow()
        # Compile the workflow so it can be invoked
        self.compiled_workflow = self.workflow.compile()

    def _create_workflow(self) -> StateGraph:
        """Create LangGraph workflow for Ghostbusters"""

        # Define the state graph
        workflow = StateGraph(GhostbustersState)

        # Add nodes - full workflow
        workflow.add_node("detect_delusions", self._detect_delusions_node)
        workflow.add_node("validate_findings", self._validate_findings_node)
        workflow.add_node("plan_recovery", self._plan_recovery_node)
        workflow.add_node("execute_recovery", self._execute_recovery_node)
        workflow.add_node("validate_recovery", self._validate_recovery_node)
        workflow.add_node("generate_report", self._generate_report_node)

        # Define edges - full workflow path
        workflow.set_entry_point("detect_delusions")
        workflow.add_edge("detect_delusions", "validate_findings")
        workflow.add_edge("validate_findings", "plan_recovery")
        workflow.add_edge("plan_recovery", "execute_recovery")
        workflow.add_edge("execute_recovery", "validate_recovery")
        workflow.add_edge("validate_recovery", "generate_report")
        workflow.add_edge("generate_report", END)

        return workflow

    async def _detect_delusions_node(
        self,
        state: GhostbustersState,
    ) -> GhostbustersState:
        """Detect delusions using agents"""
        self.logger.info("🔍 [WORKFLOW_NODE] Detecting delusions...")
        self.logger.info("🔍 [WORKFLOW_NODE] Input state type: %s", type(state).__name__)

        # Convert dict to GhostbustersState if needed
        if isinstance(state, dict):
            self.logger.info("🔍 [WORKFLOW_NODE] Converting dict to GhostbustersState")
            state = GhostbustersState(**state)

        delusions_detected = []
        for name, agent in self.agents.items():
            try:
                result = await agent.detect_delusions(self.project_path)
                # BRUTAL FIX: Extract delusions from DelusionResult
                if result and hasattr(result, "delusions"):
                    delusions_detected.append(
                        {"agent": name, "delusions": result.delusions},
                    )
                self.logger.info("✅ %s detection completed", name)
            except Exception as e:
                self.logger.error("❌ %s detection failed: %s", name, e)
                state.errors.append(f"{name} detection error: {e}")

        state.delusions_detected = delusions_detected
        state.current_phase = "detection_complete"

        self.logger.info(
            "🔍 [WORKFLOW_NODE] Detection complete, returning state type: %s",
            type(state).__name__,
        )
        return state

    async def _validate_findings_node(
        self,
        state: GhostbustersState,
    ) -> GhostbustersState:
        """Validate findings using validators - FIXED ITERATION BUG"""
        self.logger.info("🔍 [WORKFLOW_NODE] Validating findings...")
        self.logger.info("🔍 [WORKFLOW_NODE] Input state type: %s", type(state).__name__)

        # Convert dict to GhostbustersState if needed
        if isinstance(state, dict):
            self.logger.info("🔍 [WORKFLOW_NODE] Converting dict to GhostbustersState")
            state = GhostbustersState(**state)

        validation_results = {}
        for name, validator in self.validators.items():
            try:
                # FIXED: Don't iterate over ValidationResult, just store it
                result = await validator.validate_findings(state.delusions_detected)
                validation_results[name] = result
                self.logger.info("✅ %s validation completed", name)
            except Exception as e:
                self.logger.error("❌ %s validation failed: %s", name, e)
                state.errors.append(f"{name} validation error: {e}")

        state.validation_results = validation_results
        state.current_phase = "validation_complete"

        self.logger.info(
            "🔍 [WORKFLOW_NODE] Validation complete, returning state type: %s",
            type(state).__name__,
        )
        return state

    async def _plan_recovery_node(self, state: GhostbustersState) -> GhostbustersState:
        """Plan recovery actions based on findings"""
        self.logger.info("📋 Planning recovery actions...")

        recovery_actions = []

        # Analyze delusions and plan recovery
        for agent_result in state.delusions_detected:
            delusions = agent_result.get("delusions", [])
            for delusion_item in delusions:
                action = await self._plan_recovery_action(delusion_item)
                if action:
                    recovery_actions.append(action)

        state.recovery_actions = recovery_actions
        state.current_phase = "planning_complete"

        return state

    async def _execute_recovery_node(
        self,
        state: GhostbustersState,
    ) -> GhostbustersState:
        """Execute recovery actions"""
        self.logger.info("🔧 Executing recovery actions...")

        recovery_results = {}

        # Limit recovery actions to prevent infinite loops
        max_recovery_actions = 10
        actions_to_execute = state.recovery_actions[:max_recovery_actions]

        for action in actions_to_execute:
            engine_name = action["engine"]
            if engine_name in self.recovery_engines:
                try:
                    engine = self.recovery_engines[engine_name]
                    result = await engine.execute_recovery(action)
                    recovery_results[action["id"]] = result
                    self.logger.info("✅ Recovery action %s completed", action["id"])
                except Exception as e:
                    self.logger.error(
                        "❌ Recovery action %s failed: %s",
                        action["id"],
                        e,
                    )
                    state.errors.append(f"Recovery error: {e}")

        if len(state.recovery_actions) > max_recovery_actions:
            self.logger.warning(
                "⚠️ Limited recovery actions to %s to prevent infinite loops",
                max_recovery_actions,
            )

        state.recovery_results = recovery_results
        state.current_phase = "recovery_complete"

        return state

    async def _validate_recovery_node(
        self,
        state: GhostbustersState,
    ) -> GhostbustersState:
        """Validate recovery results"""
        self.logger.info("🔍 Validating recovery results...")

        # Re-run validation to check if issues are resolved
        post_recovery_validation = {}
        for name, validator in self.validators.items():
            try:
                result = await validator.validate_findings(state.delusions_detected)
                post_recovery_validation[name] = result
            except Exception as e:
                self.logger.error("❌ Post-recovery validation failed: %s", e)

        # Calculate confidence improvement
        pre_confidence = self._calculate_confidence(state.validation_results)
        post_confidence = self._calculate_confidence(post_recovery_validation)
        confidence_improvement = post_confidence - pre_confidence

        state.confidence_score = post_confidence
        state.metadata["confidence_improvement"] = confidence_improvement
        state.current_phase = "validation_complete"

        return state

    async def _generate_report_node(
        self,
        state: GhostbustersState,
    ) -> GhostbustersState:
        """Generate comprehensive report"""
        print("📊 [REPORT_NODE_DEBUG] _generate_report_node called!")
        self.logger.info("📊 [REPORT_NODE] Generating Ghostbusters report...")
        self.logger.info(
            "📊 [REPORT_NODE] Validation results: %s",
            list(state.validation_results.keys()),
        )

        # Calculate confidence based on validation and recovery results
        self.logger.info("📊 [REPORT_NODE] Calling _calculate_confidence...")
        confidence = self._calculate_confidence(state.validation_results)
        self.logger.info("📊 [REPORT_NODE] Base confidence from validation: %s", confidence)

        # Adjust confidence based on recovery success
        recovery_success_rate = state.metadata.get("recovery_success_rate", 0.0)
        self.logger.info("📊 [REPORT_NODE] Recovery success rate: %s", recovery_success_rate)

        # Add debug output
        print(f"📊 [REPORT_NODE_DEBUG] Base confidence: {confidence}")
        print(f"📊 [REPORT_NODE_DEBUG] Recovery success rate: {recovery_success_rate}")

        confidence = (confidence + recovery_success_rate) / 2
        self.logger.info(
            "📊 [REPORT_NODE] Final adjusted confidence: (%s + %s) / 2 = %s",
            confidence * 2 - recovery_success_rate,
            recovery_success_rate,
            confidence,
        )

        print(f"📊 [REPORT_NODE_DEBUG] Final adjusted confidence: {confidence}")

        state.confidence_score = confidence
        state.current_phase = "complete"

        # Create report
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_path": str(self.project_path),
            "confidence_score": confidence,
            "delusions_detected": len(state.delusions_detected),
            "recovery_actions": len(state.recovery_actions),
            "errors": state.errors,
            "warnings": state.warnings,
            "current_phase": state.current_phase,
        }

        state.metadata["report"] = report
        self.logger.info("📊 [REPORT_NODE] Ghostbusters completed with confidence: %s", confidence)
        return state

    def _calculate_confidence(self, validation_results: dict[str, Any]) -> float:
        """Calculate confidence score from validation results"""
        self.logger.info("🔍 [CONFIDENCE] Calculating confidence from validation results")
        self.logger.info(
            "🔍 [CONFIDENCE] Validation results keys: %s",
            list(validation_results.keys()),
        )

        if not validation_results:
            self.logger.info("🔍 [CONFIDENCE] No validation results, returning 0.0")
            return 0.0

        total_confidence = 0.0
        count = 0

        for validator_name, result in validation_results.items():
            self.logger.info("🔍 [CONFIDENCE] Processing validator: %s", validator_name)
            self.logger.info("🔍 [CONFIDENCE] Result type: %s", type(result).__name__)
            self.logger.info(
                "🔍 [CONFIDENCE] Result attributes: %s",
                [attr for attr in dir(result) if not attr.startswith("_")],
            )

            if hasattr(result, "confidence"):
                confidence = result.confidence
                self.logger.info("🔍 [CONFIDENCE] %s confidence: %s", validator_name, confidence)
                print(f"🔍 [CONFIDENCE_DEBUG] {validator_name}: {confidence}")
                total_confidence += confidence
                count += 1
            else:
                self.logger.warning("⚠️ [CONFIDENCE] %s has no confidence attribute", validator_name)
                print(f"⚠️ [CONFIDENCE_DEBUG] {validator_name}: NO CONFIDENCE ATTRIBUTE")
                print(f"⚠️ [CONFIDENCE_DEBUG] {validator_name} result type: {type(result)}")
                print(f"⚠️ [CONFIDENCE_DEBUG] {validator_name} result: {result}")

        final_confidence = total_confidence / count if count > 0 else 0.0
        self.logger.info(
            "🔍 [CONFIDENCE] Final calculation: %s / %s = %s",
            total_confidence,
            count,
            final_confidence,
        )

        # Add print statements to ensure we see this
        print(f"🔍 [CONFIDENCE_DEBUG] Total confidence: {total_confidence}")
        print(f"🔍 [CONFIDENCE_DEBUG] Count: {count}")
        print(f"🔍 [CONFIDENCE_DEBUG] Final confidence: {final_confidence}")

        return final_confidence

    async def run_ghostbusters(self) -> GhostbustersState:
        """Run the complete Ghostbusters workflow"""
        self.logger.info("🚀 [MAIN] Starting Ghostbusters workflow...")
        self.logger.info("🚀 [MAIN] Project path: %s", self.project_path)
        self.logger.info("🚀 [MAIN] Agents: %s", list(self.agents.keys()))
        self.logger.info("🚀 [MAIN] Validators: %s", list(self.validators.keys()))
        self.logger.info("🚀 [MAIN] Recovery engines: %s", list(self.recovery_engines.keys()))

        # Initialize state
        self.logger.info("🚀 [MAIN] Initializing GhostbustersState...")
        state = GhostbustersState(
            project_path=str(self.project_path),
            delusions_detected=[],
            recovery_actions=[],
            confidence_score=0.0,
            validation_results={},
            recovery_results={},
            current_phase="detection",
            errors=[],
            warnings=[],
            metadata={},
        )

        self.logger.info("🚀 [MAIN] State initialized with type: %s", type(state).__name__)
        self.logger.info(
            "🚀 [MAIN] State attributes: %s",
            [attr for attr in dir(state) if not attr.startswith("_")],
        )
        self.logger.info("🚀 [MAIN] State current_phase: %s", state.current_phase)

        try:
            # Use the actual LangGraph workflow
            self.logger.info("🚀 [WORKFLOW] Executing LangGraph workflow...")
            self.logger.info("🚀 [WORKFLOW] Workflow nodes: %s", list(self.workflow.nodes.keys()))

            # Execute the compiled workflow asynchronously
            self.logger.info(
                "🚀 [WORKFLOW] About to execute workflow with state type: %s",
                type(state).__name__,
            )
            final_state = await self.compiled_workflow.ainvoke(state)
            self.logger.info("🚀 [WORKFLOW] Workflow execution completed")
            self.logger.info("🚀 [WORKFLOW] Final state type: %s", type(final_state).__name__)

            # Update our state with the workflow results
            state = final_state

        except Exception as e:
            self.logger.error("❌ [MAIN] Ghostbusters workflow failed: %s", e)
            self.logger.error("❌ [MAIN] Exception type: %s", type(e).__name__)
            state.errors.append(str(e))
            state.confidence_score = 0.0

        # Final summary logging
        self.logger.info("🚀 [MAIN] Workflow completed successfully")
        self.logger.info("🚀 [MAIN] Final state summary:")

        # Handle both dict and GhostbustersState
        if isinstance(state, dict):
            self.logger.info("🚀 [MAIN]   - Current phase: %s", state.get("current_phase", "unknown"))
            self.logger.info(
                "🚀 [MAIN]   - Delusions detected: %d",
                len(state.get("delusions_detected", [])),
            )
            self.logger.info(
                "🚀 [MAIN]   - Validation results: %d",
                len(state.get("validation_results", {})),
            )
            self.logger.info(
                "🚀 [MAIN]   - Recovery actions: %d",
                len(state.get("recovery_actions", [])),
            )
            self.logger.info(
                "🚀 [MAIN]   - Recovery results: %d",
                len(state.get("recovery_results", {})),
            )
            self.logger.info("🚀 [MAIN]   - Errors: %d", len(state.get("errors", [])))
            self.logger.info("🚀 [MAIN]   - Warnings: %d", len(state.get("warnings", [])))
            self.logger.info("🚀 [MAIN]   - Metadata items: %d", len(state.get("metadata", {})))
            self.logger.info(
                "🚀 [MAIN]   - Confidence score: %s",
                state.get("confidence_score", "unknown"),
            )
        else:
            self.logger.info("🚀 [MAIN]   - Current phase: %s", state.current_phase)
            self.logger.info("🚀 [MAIN]   - Delusions detected: %d", len(state.delusions_detected))
            self.logger.info("🚀 [MAIN]   - Validation results: %d", len(state.validation_results))
            self.logger.info("🚀 [MAIN]   - Recovery actions: %d", len(state.recovery_actions))
            self.logger.info("🚀 [MAIN]   - Recovery results: %d", len(state.recovery_results))
            self.logger.info("🚀 [MAIN]   - Errors: %d", len(state.errors))
            self.logger.info("🚀 [MAIN]   - Warnings: %d", len(state.warnings))
            self.logger.info("🚀 [MAIN]   - Metadata items: %d", len(state.metadata))
            self.logger.info("🚀 [MAIN]   - Confidence score: %s", state.confidence_score)

        return state

    async def _detect_delusions(self, state: GhostbustersState) -> GhostbustersState:
        """Detect delusions using all agents - FIXED DATA STRUCTURE"""
        self.logger.info("🔍 [DETECTION] Starting _detect_delusions method")
        self.logger.info("🔍 [DETECTION] Agents available: %s", list(self.agents.keys()))

        delusions_detected = []
        for agent_count, (agent_name, agent) in enumerate(self.agents.items(), 1):
            self.logger.info(
                "🔍 [DETECTION] Processing agent %d/%d: %s",
                agent_count,
                len(self.agents),
                agent_name,
            )

            try:
                self.logger.info(
                    "🔍 [DETECTION] Calling %s.detect_delusions(%s)",
                    agent_name,
                    self.project_path,
                )

                result = await agent.detect_delusions(self.project_path)

                self.logger.info(
                    "🔍 [DETECTION] %s returned result type: %s",
                    agent_name,
                    type(result).__name__,
                )

                # Use the same data structure as the workflow node
                if result and hasattr(result, "delusions"):
                    delusion_count = len(result.delusions)
                    self.logger.info(
                        "🔍 [DETECTION] %s found %d delusions",
                        agent_name,
                        delusion_count,
                    )

                    # Log first few delusions for debugging
                    if delusion_count > 0:
                        sample_delusions = result.delusions[:3]
                        self.logger.info(
                            "🔍 [DETECTION] %s sample delusions: %s",
                            agent_name,
                            [d.get("type", "Unknown") for d in sample_delusions],
                        )

                    delusions_detected.append(
                        {"agent": agent_name, "delusions": result.delusions},
                    )

                    # Store metadata
                    state.metadata[f"{agent_name}_confidence"] = result.confidence
                    state.metadata[f"{agent_name}_recommendations"] = result.recommendations

                    self.logger.info(
                        "🔍 [DETECTION] %s confidence: %s, recommendations: %d",
                        agent_name,
                        result.confidence,
                        len(result.recommendations),
                    )
                else:
                    self.logger.warning(
                        "⚠️ [DETECTION] %s returned invalid result: %s",
                        agent_name,
                        result,
                    )

                self.logger.info("✅ [DETECTION] %s detection completed", agent_name)

            except Exception as e:
                self.logger.error("❌ [DETECTION] %s detection failed: %s", agent_name, e)
                self.logger.error("❌ [DETECTION] Exception type: %s", type(e).__name__)
                state.errors.append(f"{agent_name} detection error: {e}")

        self.logger.info(
            "🔍 [DETECTION] Completed all agents. Total delusion groups: %d",
            len(delusions_detected),
        )

        # Log the final data structure for debugging
        for i, group in enumerate(delusions_detected):
            agent = group.get("agent", "Unknown")
            delusions = group.get("delusions", [])
            self.logger.info("🔍 [DETECTION] Group %d: %s has %d delusions", i, agent, len(delusions))

        state.delusions_detected = delusions_detected
        state.current_phase = "detection_complete"

        self.logger.info(
            "🔍 [DETECTION] Final state.delusions_detected length: %d",
            len(state.delusions_detected),
        )
        self.logger.info("🔍 [DETECTION] Final state.current_phase: %s", state.current_phase)

        return state

    async def _validate_findings(self, state: GhostbustersState) -> GhostbustersState:
        """Validate findings using validators"""
        validation_results = {}

        for validator_name, validator in self.validators.items():
            try:
                result = await validator.validate_findings(state.delusions_detected)
                validation_results[validator_name] = result
            except Exception as e:
                self.logger.error("Validator %s failed: %s", validator_name, e)
                state.errors.append(f"Validator {validator_name} failed: {e}")

        state.validation_results = validation_results
        state.current_phase = "planning"
        return state

    async def _plan_recovery(self, state: GhostbustersState) -> GhostbustersState:
        """Plan recovery actions for detected delusions"""
        recovery_actions = []

        for delusion in state.delusions_detected:
            action = await self._plan_recovery_action(delusion)
            if action:
                recovery_actions.append(action)

        state.recovery_actions = recovery_actions
        state.current_phase = "execution"
        return state

    async def _execute_recovery(self, state: GhostbustersState) -> GhostbustersState:
        """Execute recovery actions"""
        recovery_results = {}

        # Limit recovery actions to prevent infinite loops
        max_recovery_actions = 10
        actions_to_execute = state.recovery_actions[:max_recovery_actions]

        for action in actions_to_execute:
            engine_name = action.get("engine")
            if engine_name in self.recovery_engines:
                try:
                    engine = self.recovery_engines[engine_name]
                    result = await engine.execute_recovery(action)
                    recovery_results[action.get("id", "unknown")] = result
                except Exception as e:
                    self.logger.error("Recovery engine %s failed: %s", engine_name, e)
                    state.errors.append(f"Recovery engine {engine_name} failed: {e}")

        if len(state.recovery_actions) > max_recovery_actions:
            self.logger.warning(
                "Limited recovery actions to %s to prevent infinite loops",
                max_recovery_actions,
            )

        state.recovery_results = recovery_results
        state.current_phase = "validation"
        return state

    async def _validate_recovery(self, state: GhostbustersState) -> GhostbustersState:
        """Validate recovery results"""
        # Re-run detection to see if issues were fixed
        post_recovery_state = await self._detect_delusions(state)
        remaining_delusions = len(post_recovery_state.delusions_detected)
        original_delusions = len(state.delusions_detected)

        if original_delusions > 0:
            success_rate = (original_delusions - remaining_delusions) / original_delusions
        else:
            success_rate = 1.0

        state.metadata["recovery_success_rate"] = success_rate
        state.metadata["remaining_delusions"] = remaining_delusions
        state.current_phase = "reporting"
        return state

    async def _generate_report(self, state: GhostbustersState) -> GhostbustersState:
        """Generate final report and calculate confidence"""
        self.logger.info("📊 [REPORT] Generating final report...")
        self.logger.info("📊 [REPORT] Validation results: %s", list(state.validation_results.keys()))

        # Calculate confidence based on validation and recovery results
        self.logger.info("📊 [REPORT] Calling _calculate_confidence...")
        confidence = self._calculate_confidence(state.validation_results)
        self.logger.info("📊 [REPORT] Base confidence from validation: %s", confidence)

        # Adjust confidence based on recovery success
        recovery_success_rate = state.metadata.get("recovery_success_rate", 0.0)
        self.logger.info("📊 [REPORT] Recovery success rate: %s", recovery_success_rate)

        # Add debug output
        print(f"📊 [REPORT_DEBUG] Base confidence: {confidence}")
        print(f"📊 [REPORT_DEBUG] Recovery success rate: {recovery_success_rate}")

        confidence = (confidence + recovery_success_rate) / 2
        self.logger.info(
            "📊 [REPORT] Final adjusted confidence: (%s + %s) / 2 = %s",
            confidence * 2 - recovery_success_rate,
            recovery_success_rate,
            confidence,
        )

        print(f"📊 [REPORT_DEBUG] Final adjusted confidence: {confidence}")

        state.confidence_score = confidence
        state.current_phase = "complete"

        self.logger.info("📊 [REPORT] Ghostbusters completed with confidence: %s", confidence)
        return state

    async def _plan_recovery_action(
        self,
        delusion: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Plan a recovery action for a delusion"""
        delusion_type = delusion.get("type", "")

        # Map delusion types to recovery engines
        engine_mapping = {
            "syntax_error": "syntax",
            "indentation_error": "indentation",
            "import_error": "imports",
            "type_error": "types",
            "subprocess_vulnerability": "security",
        }

        engine_name = engine_mapping.get(delusion_type)
        if engine_name and engine_name in self.recovery_engines:
            return {
                "id": f"recovery_{len(self.recovery_actions) if hasattr(self, 'recovery_actions') else 0}",
                "engine": engine_name,
                "delusion": delusion,
                "priority": delusion.get("priority", "medium"),
            }

        return None


async def run_ghostbusters(project_path: str = ".") -> GhostbustersState:
    """Convenience function to run Ghostbusters"""
    orchestrator = GhostbustersOrchestrator(project_path)
    return await orchestrator.run_ghostbusters()


if __name__ == "__main__":

    async def main() -> None:
        print("🚀 [MAIN_FUNCTION] Starting Ghostbusters main function...")

        state = await run_ghostbusters()

        # Handle both dict and GhostbustersState
        if isinstance(state, dict):
            confidence = state.get("confidence_score", "unknown")
            delusions_detected = state.get("delusions_detected", [])
            errors = state.get("errors", [])
            current_phase = state.get("current_phase", "unknown")
            metadata = state.get("metadata", {})
        else:
            confidence = state.confidence_score
            delusions_detected = state.delusions_detected
            errors = state.errors
            current_phase = state.current_phase
            metadata = state.metadata

        print(f"\n🎯 [MAIN_FUNCTION] Ghostbusters completed with confidence: {confidence}")
        print(f"🎯 [MAIN_FUNCTION] Final state type: {type(state).__name__}")

        # Show what was actually found with corruption detection
        if delusions_detected:
            print(f"\n🚨 [MAIN_FUNCTION] Found {len(delusions_detected)} delusion groups:")

            # Detect corruption: check for duplicate agents
            agent_counts = {}
            for group in delusions_detected:
                agent = group.get("agent", "Unknown")
                agent_counts[agent] = agent_counts.get(agent, 0) + 1

            # Show corruption warnings
            corrupted_agents = [agent for agent, count in agent_counts.items() if count > 1]
            if corrupted_agents:
                print("⚠️ [MAIN_FUNCTION] CORRUPTION DETECTED: These agents ran multiple times:")
                for agent in corrupted_agents:
                    print(f"    {agent}: {agent_counts[agent]} times")
            else:
                print("✅ [MAIN_FUNCTION] No corruption detected - each agent ran once")

            # Show results
            for group in delusions_detected:
                agent = group.get("agent", "Unknown")
                delusions = group.get("delusions", [])
                print(f"  [MAIN_FUNCTION] {agent}: {len(delusions)} delusions")
                for d in delusions[:3]:  # Show first 3
                    print(f"    - {d.get('type', 'Unknown')}: {d.get('description', 'No description')}")
                if len(delusions) > 3:
                    print(f"    ... and {len(delusions) - 3} more")
        else:
            print("\n✅ [MAIN_FUNCTION] No delusions detected")

        if errors:
            print(f"\n❌ [MAIN_FUNCTION] Errors: {len(errors)}")
            for error in errors[:3]:
                print(f"  - {error}")
        else:
            print("\n✅ [MAIN_FUNCTION] No errors")

        # Show workflow execution summary
        print(f"\n📊 [MAIN_FUNCTION] Workflow Phase: {current_phase}")
        if metadata:
            print(f"\n📊 [MAIN_FUNCTION] Metadata: {len(metadata)} items")
            for key, value in list(metadata.items())[:3]:
                print(f"    {key}: {value}")

        print("\n🎯 [MAIN_FUNCTION] Main function completed successfully")

    asyncio.run(main())
