#!/usr/bin/env python3
"""
LangGraph Orchestrator - Real LangGraph Integration with Multi-Agent Collaboration

This orchestrator uses LangGraph's StateGraph for proper workflow orchestration
and integrates with the AgentSessionManager for context-aware collaboration.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from .agent_session_manager import AgentFinding, AgentSessionManager, AgentType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("langgraph_orchestrator.log"),
    ],
)
logger = logging.getLogger(__name__)


class WorkflowStage(Enum):
    """Stages of the LangGraph workflow"""

    INITIALIZE = "initialize"
    PLAN = "plan"
    DO = "do"
    CHECK = "check"
    ACT = "act"
    SYNTHESIZE = "synthesize"
    COMPLETE = "complete"


class OrchestratorState(TypedDict, total=False):
    """State for the LangGraph workflow - using TypedDict for proper LangGraph integration"""

    # Workflow state
    current_stage: str  # WorkflowStage enum value
    iteration_number: int
    max_iterations: int

    # Quality analysis state
    quality_report: Optional[dict[str, Any]]
    subproject_results: Optional[dict[str, Any]]
    formatting_results: Optional[dict[str, Any]]
    linting_results: Optional[dict[str, Any]]
    pre_commit_results: Optional[dict[str, Any]]

    # Multi-agent state
    agent_findings: dict[str, list[dict[str, Any]]]
    cross_agent_insights: list[dict[str, Any]]
    synthesis: Optional[dict[str, Any]]

    # Context and learning
    iteration_context: Optional[dict[str, Any]]
    learning_outcomes: list[str]

    # Workflow control
    should_continue: bool
    error_message: Optional[str]
    next_actions: list[str]

    # Messages for LangChain integration
    messages: Annotated[list, add_messages]


class LangGraphOrchestrator:
    """LangGraph-based workflow orchestrator with proper state management"""

    def __init__(
        self, target_directory: str = ".", storage_dir: str = "agent_sessions"
    ):
        self.target_directory = Path(target_directory).resolve()
        self.agent_session_manager = AgentSessionManager(storage_dir)
        self.workflow = self._create_workflow()

        # Initialize API key manager
        self.api_manager = None
        self.working_models = []
        self._initialize_api_keys()

    def _initialize_api_keys(self) -> None:
        """Initialize API keys and test endpoints"""
        try:
            import sys

            scripts_path = str(Path.cwd() / "scripts")
            sys.path.insert(0, scripts_path)
            from op_api_manager import OnePasswordAPIKeyManager

            self.api_manager = OnePasswordAPIKeyManager()

            # Try to get working API keys (will fail gracefully if 1Password not signed in)
            try:
                working_keys = self.api_manager.get_working_api_keys()
                if working_keys:
                    # Extract provider types from working keys
                    providers = set()
                    for key_info in working_keys:
                        if hasattr(key_info, "detected_provider"):
                            providers.add(key_info.detected_provider.value)

                    if "anthropic" in providers:
                        self.working_models.append("claude")
                        print("✅ Using Anthropic Claude for multi-agent analysis")

                    if "openai" in providers:
                        self.working_models.append("gpt4_vision")
                        print("✅ Using OpenAI GPT-4 for multi-agent analysis")

                    if self.working_models:
                        print(
                            f"🚀 Multi-LLM setup: {len(self.working_models)} models available"
                        )
                    else:
                        print("⚠️ No working API endpoints found")
                else:
                    print("⚠️ No working API endpoints found")
            except Exception as e:
                print(f"⚠️ API key discovery failed (1Password not signed in): {e}")
                print("⚠️ Multi-LLM analysis will use fallback methods")

        except Exception as e:
            print(f"⚠️ Error initializing API keys: {e}")

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        logger.info("🔧 Creating LangGraph workflow...")

        # Create the workflow graph
        workflow = StateGraph(OrchestratorState)
        logger.info("✅ Created StateGraph")

        # Add workflow nodes
        workflow.add_node("initialize", self._initialize_phase)
        workflow.add_node("plan", self._plan_phase)
        workflow.add_node("do", self._do_phase)
        workflow.add_node("check", self._check_phase)
        workflow.add_node("act", self._act_phase)
        workflow.add_node("synthesize", self._synthesize_phase)
        workflow.add_node("complete", self._complete_phase)
        logger.info("✅ Added all workflow nodes")

        # Set the entrypoint
        workflow.set_entry_point("initialize")
        logger.info("✅ Set entry point to 'initialize'")

        # Add conditional edges
        workflow.add_conditional_edges(
            "initialize",
            self._should_continue_to_plan,
            {True: "plan", False: "complete"},
        )
        logger.info("✅ Added initialize → plan/complete conditional edge")

        workflow.add_conditional_edges(
            "plan", self._should_continue_to_do, {True: "do", False: "complete"}
        )
        logger.info("✅ Added plan → do/complete conditional edge")

        workflow.add_edge("do", "check")
        workflow.add_edge("check", "act")
        logger.info("✅ Added do → check → act edges")

        workflow.add_conditional_edges(
            "act",
            self._should_continue_to_synthesize,
            {True: "synthesize", False: "complete"},
        )
        logger.info("✅ Added act → synthesize/complete conditional edge")

        # Fix the recursion issue: synthesize should go to complete, not back to plan
        workflow.add_edge("synthesize", "complete")
        logger.info("✅ Added synthesize → complete edge (no more recursion)")

        workflow.add_edge("complete", END)
        logger.info("✅ Added complete → END edge")

        logger.info("🔧 Compiling workflow...")
        compiled_workflow = workflow.compile()
        logger.info("✅ Workflow compiled successfully")

        return compiled_workflow

    def _should_continue_to_plan(self, state: OrchestratorState) -> bool:
        """Determine if we should continue to plan phase"""
        iteration_number = state.get("iteration_number", 0)
        max_iterations = state.get("max_iterations", 5)
        logger.info(
            f"🔍 _should_continue_to_plan: iteration={iteration_number}, max_iterations={max_iterations}"
        )

        # Check if we have an error
        if state.get("error_message"):
            logger.info(
                f"❌ Error detected: {state.get('error_message')}, going to complete"
            )
            return False

        # Check if we should continue
        if not state.get("should_continue", True):
            logger.info("❌ Should not continue, going to complete")
            return False

        # Check if we've reached max iterations (but allow at least one full cycle)
        if iteration_number >= max_iterations and iteration_number > 0:
            logger.info("❌ Max iterations reached, going to complete")
            return False

        logger.info("✅ Continuing to plan phase")
        return True

    def _should_continue_to_do(self, state: OrchestratorState) -> bool:
        """Determine if we should continue to do phase"""
        quality_report = state.get("quality_report")
        logger.info(f"🔍 _should_continue_to_do: quality_report={bool(quality_report)}")

        # Check if we have a quality report
        if not quality_report:
            logger.info("❌ No quality report, going to complete")
            return False

        # Check if we have issues to address
        total_issues = quality_report.get("total_issues", 0)
        logger.info(f"📊 Total issues found: {total_issues}")

        if total_issues > 0:
            logger.info("✅ Issues found, continuing to do phase")
            return True
        logger.info("✅ No issues found, going to complete")
        return False

    def _should_continue_to_synthesize(self, state: OrchestratorState) -> bool:
        """Determine if we should continue to synthesis phase"""
        logger.info(
            "🔍 _should_continue_to_synthesize: always continue after act phase"
        )
        # Always continue to synthesis after act phase
        return True

    def _should_continue_to_next_iteration(self, state: OrchestratorState) -> bool:
        """Determine if we should continue to the next iteration"""
        iteration_number = state.get("iteration_number", 0)
        max_iterations = state.get("max_iterations", 5)
        logger.info(
            f"🔍 _should_continue_to_next_iteration: iteration={iteration_number}, max_iterations={max_iterations}"
        )

        # Check if we've reached max iterations
        if iteration_number >= max_iterations:
            logger.info("❌ Max iterations reached, stopping")
            return False

        # Check if we have quality issues to address
        quality_report = state.get("quality_report")
        if quality_report and quality_report.get("total_issues", 0) > 0:
            logger.info("✅ Quality issues found, continuing to next iteration")
            return True

        # Check if we have agent findings to process
        agent_findings = state.get("agent_findings", {})
        total_findings = sum(len(findings) for findings in agent_findings.values())
        if total_findings > 0:
            logger.info(
                f"✅ Agent findings found: {total_findings}, continuing to next iteration"
            )
            return True

        # If no issues and no findings, we're done
        logger.info("✅ No issues and no findings, stopping")
        return False

    async def _initialize_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Initialize the workflow and start a new iteration"""
        logger.info("🚀 Starting initialize phase...")

        try:
            # Start new iteration
            iteration_number = self.agent_session_manager.start_new_iteration()
            logger.info(f"✅ Started iteration {iteration_number}")

            # Return state updates as dict
            updates = {
                "iteration_number": iteration_number,
                "current_stage": WorkflowStage.INITIALIZE.value,
                "should_continue": True,
                "error_message": None,
                "max_iterations": 5,
                "agent_findings": {},
                "cross_agent_insights": [],
                "learning_outcomes": [],
                "next_actions": [],
                "messages": [],
            }

            logger.info(
                f"📊 State updated: iteration={iteration_number}, stage={WorkflowStage.INITIALIZE.value}"
            )
            return updates

        except Exception as e:
            logger.error(f"❌ Initialize phase failed: {e}")
            return {
                "error_message": f"Initialize failed: {e}",
                "should_continue": False,
            }

    async def _plan_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Plan phase: generate quality report and plan actions"""
        logger.info("📋 Starting plan phase...")

        try:
            # Generate quality report
            quality_report = await self._generate_quality_report()

            logger.info(
                f"✅ Plan phase completed: {quality_report.get('total_issues', 0)} issues found"
            )
            return {
                "current_stage": WorkflowStage.PLAN.value,
                "quality_report": quality_report,
            }

        except Exception as e:
            logger.error(f"❌ Plan phase failed: {e}")
            return {"error_message": f"Plan failed: {e}", "should_continue": False}

    async def _do_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Do phase: Apply automated fixes"""
        iteration_number = state.get("iteration_number", 0)
        logger.info(f"🔧 Starting do phase for iteration {iteration_number}")

        try:
            # Run subproject scrubbing
            subproject_result = await self._run_subproject_scrubbing()

            # Run formatting
            formatting_result = await self._run_formatting()

            # Run linting
            linting_result = await self._run_linting()

            logger.info("✅ Do phase completed successfully")
            return {
                "current_stage": WorkflowStage.DO.value,
                "subproject_results": subproject_result,
                "formatting_results": formatting_result,
                "linting_results": linting_result,
            }

        except Exception as e:
            logger.error(f"❌ Do phase failed: {e}")
            return {
                "error_message": f"Execution phase failed: {str(e)}",
                "should_continue": False,
            }

    async def _check_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Check phase: Run pre-commit validation"""
        print(f"🔍 Validation phase for iteration {state.get('iteration_number', 0)}")

        try:
            # Run pre-commit checks
            pre_commit_result = await self._run_pre_commit_check()

            # Add validation message
            messages = state.get("messages", [])
            messages.append(
                HumanMessage(
                    content=f"Pre-commit validation: {pre_commit_result.get('success', False)}"
                )
            )

            print(
                f"✅ Validation complete: pre-commit {'passed' if pre_commit_result.get('success') else 'failed'}"
            )

            return {
                "current_stage": WorkflowStage.CHECK.value,
                "pre_commit_results": pre_commit_result,
                "messages": messages,
            }

        except Exception as e:
            print(f"❌ Validation phase failed: {e}")
            return {
                "current_stage": WorkflowStage.CHECK.value,
                "error_message": f"Validation phase failed: {str(e)}",
                "should_continue": False,
            }

    async def _act_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Act phase: Run multi-agent analysis"""
        print(
            f"🤖 Multi-agent analysis phase for iteration {state.get('iteration_number', 0)}"
        )

        try:
            # Run multi-agent analysis
            agent_results = await self._run_multi_agent_analysis()

            # Add analysis message
            total_findings = sum(len(findings) for findings in agent_results.values())
            messages = state.get("messages", [])
            messages.append(
                HumanMessage(
                    content=f"Multi-agent analysis complete: {total_findings} findings across {len(agent_results)} agents"
                )
            )

            print(f"✅ Multi-agent analysis complete: {total_findings} findings")

            return {
                "current_stage": WorkflowStage.ACT.value,
                "agent_findings": agent_results,
                "messages": messages,
            }

        except Exception as e:
            print(f"❌ Multi-agent analysis failed: {e}")
            return {
                "current_stage": WorkflowStage.ACT.value,
                "error_message": f"Multi-agent analysis failed: {str(e)}",
                "should_continue": False,
            }

    async def _synthesize_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Synthesize phase: Analyze results and plan next iteration"""
        print(f"🧠 Synthesis phase for iteration {state.get('iteration_number', 0)}")

        try:
            # Synthesize iteration results
            synthesis = self.agent_session_manager.synthesize_iteration_results()

            # Extract learning outcomes
            learning_outcomes = synthesis.get("learning_outcomes", [])

            # Determine if we should continue
            iteration_number = state.get("iteration_number", 0)
            max_iterations = state.get("max_iterations", 5)
            quality_report = state.get("quality_report")
            pre_commit_results = state.get("pre_commit_results", {})

            should_continue = (
                iteration_number < max_iterations
                and quality_report
                and quality_report.get("total_issues", 0) > 0
                and not pre_commit_results.get("success", False)
            )

            # Add synthesis message
            messages = state.get("messages", [])
            messages.append(
                AIMessage(
                    content=f"Synthesis complete: {len(synthesis.get('recommendations', []))} recommendations, continue={should_continue}"
                )
            )

            print(
                f"✅ Synthesis complete: {len(synthesis.get('recommendations', []))} recommendations"
            )

            return {
                "current_stage": WorkflowStage.SYNTHESIZE.value,
                "synthesis": synthesis,
                "learning_outcomes": learning_outcomes,
                "should_continue": should_continue,
                "messages": messages,
            }

        except Exception as e:
            print(f"❌ Synthesis phase failed: {e}")
            return {
                "current_stage": WorkflowStage.SYNTHESIZE.value,
                "error_message": f"Synthesis phase failed: {str(e)}",
                "should_continue": False,
            }

    async def _complete_phase(self, state: OrchestratorState) -> dict[str, Any]:
        """Complete the workflow and finalize results"""
        logger.info("🏁 Starting complete phase...")

        try:
            # Finalize the iteration
            iteration_number = state.get("iteration_number", 0)
            if hasattr(self.agent_session_manager, "finalize_iteration"):
                self.agent_session_manager.finalize_iteration(iteration_number)
                logger.info(f"✅ Finalized iteration {iteration_number}")

            # Generate final synthesis if not already done
            synthesis = state.get("synthesis")
            if not synthesis:
                synthesis = self.agent_session_manager.synthesize_iteration_results()
                logger.info("✅ Generated final synthesis")

            logger.info(f"🏁 Workflow completed after {iteration_number} iterations")
            return {
                "current_stage": WorkflowStage.COMPLETE.value,
                "should_continue": False,
                "synthesis": synthesis,
            }

        except Exception as e:
            logger.error(f"❌ Complete phase failed: {e}")
            return {
                "error_message": f"Complete failed: {e}",
                "current_stage": WorkflowStage.COMPLETE.value,
                "should_continue": False,
            }

    async def _generate_quality_report(self) -> dict[str, Any]:
        """Generate current quality report using existing tools"""
        print("  📋 Generating quality report...")

        try:
            # Import the existing orchestrator to use its quality reporting
            from .code_quality_automation_orchestrator import (
                CodeQualityAutomationOrchestrator,
            )

            # Create a temporary orchestrator to generate the report
            temp_orchestrator = CodeQualityAutomationOrchestrator(
                str(self.target_directory)
            )
            quality_report = temp_orchestrator.generate_quality_report()

            # Convert to dictionary format
            report_dict = quality_report.to_dict()
            print(
                f"  ✅ Quality report generated: {report_dict.get('total_issues', 0)} issues found"
            )

            return report_dict

        except Exception as e:
            print(f"  ❌ Quality report generation failed: {e}")
            # Return a basic report structure
            return {
                "timestamp": datetime.now().isoformat(),
                "total_files_analyzed": 0,
                "files_with_issues": 0,
                "total_issues": 0,
                "issues_by_severity": {},
                "issues_by_type": {},
                "automated_fixes_applied": 0,
                "manual_fixes_required": 0,
                "recommendations": [],
                "next_actions": [],
            }

    async def _run_subproject_scrubbing(self) -> dict[str, Any]:
        """Run subproject scrubbing using existing tools"""
        print("  🔧 Running subproject scrubbing...")

        try:
            from .code_quality_automation_orchestrator import (
                CodeQualityAutomationOrchestrator,
            )

            temp_orchestrator = CodeQualityAutomationOrchestrator(
                str(self.target_directory)
            )
            result = temp_orchestrator.run_subproject_scrubbing()

            print(
                f"  ✅ Subproject scrubbing: {'success' if result.get('success') else 'failed'}"
            )
            return result

        except Exception as e:
            print(f"  ❌ Subproject scrubbing failed: {e}")
            return {"success": False, "error": str(e)}

    async def _run_formatting(self) -> dict[str, Any]:
        """Run code formatting using existing tools"""
        print("  🎨 Running code formatting...")

        try:
            from .code_quality_automation_orchestrator import (
                CodeQualityAutomationOrchestrator,
            )

            temp_orchestrator = CodeQualityAutomationOrchestrator(
                str(self.target_directory)
            )
            result = temp_orchestrator.run_black_formatting()

            print(
                f"  ✅ Code formatting: {'success' if result.get('success') else 'failed'}"
            )
            return result

        except Exception as e:
            print(f"  ❌ Code formatting failed: {e}")
            return {"success": False, "error": str(e)}

    async def _run_linting(self) -> dict[str, Any]:
        """Run code linting using existing tools"""
        print("  🔍 Running code linting...")

        try:
            from .code_quality_automation_orchestrator import (
                CodeQualityAutomationOrchestrator,
            )

            temp_orchestrator = CodeQualityAutomationOrchestrator(
                str(self.target_directory)
            )
            result = temp_orchestrator.run_ruff_linting()

            print(
                f"  ✅ Code linting: {'success' if result.get('success') else 'failed'}"
            )
            return result

        except Exception as e:
            print(f"  ❌ Code linting failed: {e}")
            return {"success": False, "error": str(e)}

    async def _run_pre_commit_check(self) -> dict[str, Any]:
        """Run pre-commit checks using existing tools"""
        print("  ✅ Running pre-commit checks...")

        try:
            from .code_quality_automation_orchestrator import (
                CodeQualityAutomationOrchestrator,
            )

            temp_orchestrator = CodeQualityAutomationOrchestrator(
                str(self.target_directory)
            )
            result = temp_orchestrator.run_pre_commit_check()

            print(
                f"  ✅ Pre-commit checks: {'passed' if result.get('success') else 'failed'}"
            )
            return result

        except Exception as e:
            print(f"  ❌ Pre-commit checks failed: {e}")
            return {"success": False, "error": str(e)}

    async def _run_multi_agent_analysis(self) -> dict[str, list[dict[str, Any]]]:
        """Run multi-agent analysis with proper context sharing"""
        print("🤖 Running collaborative multi-agent analysis...")

        agent_results = {}

        # Run agents in parallel with cross-context sharing
        tasks = []
        for agent_type in AgentType:
            task = self._run_agent_with_context(agent_type)
            tasks.append(task)

        # Wait for all agents to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for i, result in enumerate(results):
            agent_type = list(AgentType)[i]
            if isinstance(result, Exception):
                print(f"❌ {agent_type.value} failed: {result}")
                agent_results[agent_type.value] = []
            else:
                agent_results[agent_type.value] = result

        return agent_results

    async def _run_agent_with_context(
        self, agent_type: AgentType
    ) -> list[dict[str, Any]]:
        """Run a single agent with cross-agent context"""
        print(f"  🔍 Running {agent_type.value}...")

        try:
            # Get cross-agent context for this agent
            cross_context = self.agent_session_manager.get_cross_agent_context(
                agent_type
            )

            # Update agent context with cross-agent information
            self.agent_session_manager.update_agent_context(
                agent_type,
                {
                    "cross_agent_context": cross_context,
                    "iteration_number": self.agent_session_manager.current_iteration,
                },
            )

            # Run the agent analysis (this would integrate with MultiDimensionalSmokeTest)
            findings = await self._run_agent_analysis(agent_type, cross_context)

            # Store findings in agent session manager
            for finding_data in findings:
                finding = AgentFinding(
                    agent_type=agent_type,
                    finding_id=finding_data.get("finding_id", ""),
                    category=finding_data.get("category", "unknown"),
                    severity=finding_data.get("severity", "medium"),
                    description=finding_data.get("description", ""),
                    recommendations=finding_data.get("recommendations", []),
                    confidence=finding_data.get("confidence", 0.5),
                    timestamp=datetime.now().isoformat(),
                    metadata=finding_data.get("metadata", {}),
                    cross_references=finding_data.get("cross_references", []),
                )

                self.agent_session_manager.add_agent_finding(agent_type, finding)

            print(f"  ✅ {agent_type.value} completed: {len(findings)} findings")
            return findings

        except Exception as e:
            print(f"  ❌ {agent_type.value} failed: {e}")
            return []

    async def _run_agent_analysis(
        self, agent_type: AgentType, cross_context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Run analysis for a specific agent type using real tools"""
        print(f"    🤖 Running {agent_type.value} analysis...")

        try:
            # Import the real multi-dimensional smoke test
            from .multi_dimensional_smoke_test import MultiDimensionalSmokeTest

            # Initialize the test system
            test_system = MultiDimensionalSmokeTest()

            # Prepare the configuration based on agent type
            if agent_type == AgentType.SECURITY:
                config = {
                    "role": "security_expert",
                    "prompt_structure": "direct_questions",
                    "response_format": "json",
                    "model": (
                        self.working_models[0] if self.working_models else "claude"
                    ),
                    "temperature": 0.7,
                }
                scenario = "security_audit"

            elif agent_type == AgentType.QUALITY:
                config = {
                    "role": "code_quality_expert",
                    "prompt_structure": "direct_questions",
                    "response_format": "json",
                    "model": (
                        self.working_models[0] if self.working_models else "claude"
                    ),
                    "temperature": 0.7,
                }
                scenario = "code_quality_assessment"

            elif agent_type == AgentType.DEVOPS:
                config = {
                    "role": "devops_expert",
                    "prompt_structure": "direct_questions",
                    "response_format": "json",
                    "model": (
                        self.working_models[0] if self.working_models else "claude"
                    ),
                    "temperature": 0.7,
                }
                scenario = "devops_pipeline_review"

            else:
                print(f"    ⚠️ Unknown agent type: {agent_type}")
                return []

            # Add cross-agent context to the configuration
            config["cross_agent_context"] = cross_context
            config["iteration_context"] = {
                "iteration_number": self.agent_session_manager.current_iteration,
                "previous_findings": len(
                    self.agent_session_manager.get_agent_previous_findings(
                        agent_type, self.agent_session_manager.current_iteration
                    )
                ),
            }

            # Run the analysis
            result = test_system.run_test(config, scenario)

            # Convert the result to our finding format
            findings = self._convert_result_to_findings(
                result, agent_type, cross_context
            )

            print(
                f"    ✅ {agent_type.value} analysis complete: {len(findings)} findings"
            )
            return findings

        except Exception as e:
            print(f"    ❌ {agent_type.value} analysis failed: {e}")
            return []

    def _convert_result_to_findings(
        self, result: Any, agent_type: AgentType, cross_context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Convert analysis result to our finding format"""
        findings = []

        try:
            # Handle different result formats
            if isinstance(result, dict):
                # If result is already a dictionary, try to extract findings
                if "delusions" in result:
                    delusions = result["delusions"]
                    if isinstance(delusions, list):
                        for i, delusion in enumerate(delusions):
                            finding = {
                                "finding_id": f"{agent_type.value}_{i+1:03d}",
                                "category": delusion.get("category", "unknown"),
                                "severity": self._determine_severity(delusion),
                                "description": delusion.get(
                                    "description", str(delusion)
                                ),
                                "recommendations": delusion.get("recommendations", []),
                                "confidence": delusion.get("confidence", 0.8),
                                "metadata": {
                                    "cross_context_used": bool(cross_context),
                                    "agent_type": agent_type.value,
                                    "result_type": "delusion",
                                },
                                "cross_references": [],
                            }
                            findings.append(finding)

                elif "findings" in result:
                    # Handle findings format
                    for i, finding_data in enumerate(result["findings"]):
                        finding = {
                            "finding_id": f"{agent_type.value}_{i+1:03d}",
                            "category": finding_data.get("category", "unknown"),
                            "severity": self._determine_severity(finding_data),
                            "description": finding_data.get(
                                "description", str(finding_data)
                            ),
                            "recommendations": finding_data.get("recommendations", []),
                            "confidence": finding_data.get("confidence", 0.8),
                            "metadata": {
                                "cross_context_used": bool(cross_context),
                                "agent_type": agent_type.value,
                                "result_type": "finding",
                            },
                            "cross_references": [],
                        }
                        findings.append(finding)

                else:
                    # Generic result handling
                    finding = {
                        "finding_id": f"{agent_type.value}_001",
                        "category": "analysis",
                        "severity": "medium",
                        "description": f"Analysis result from {agent_type.value}: {str(result)[:200]}...",
                        "recommendations": [
                            "Review analysis results for actionable insights"
                        ],
                        "confidence": 0.7,
                        "metadata": {
                            "cross_context_used": bool(cross_context),
                            "agent_type": agent_type.value,
                            "result_type": "generic",
                        },
                        "cross_references": [],
                    }
                    findings.append(finding)

            elif isinstance(result, str):
                # Handle string results
                finding = {
                    "finding_id": f"{agent_type.value}_001",
                    "category": "analysis",
                    "severity": "medium",
                    "description": f"Analysis result from {agent_type.value}: {result[:200]}...",
                    "recommendations": [
                        "Review analysis results for actionable insights"
                    ],
                    "confidence": 0.7,
                    "metadata": {
                        "cross_context_used": bool(cross_context),
                        "agent_type": agent_type.value,
                        "result_type": "string",
                    },
                    "cross_references": [],
                }
                findings.append(finding)

            else:
                # Handle other result types
                finding = {
                    "finding_id": f"{agent_type.value}_001",
                    "category": "analysis",
                    "severity": "medium",
                    "description": f"Analysis result from {agent_type.value}: {type(result).__name__}",
                    "recommendations": [
                        "Review analysis results for actionable insights"
                    ],
                    "confidence": 0.7,
                    "metadata": {
                        "cross_context_used": bool(cross_context),
                        "agent_type": agent_type.value,
                        "result_type": type(result).__name__,
                    },
                    "cross_references": [],
                }
                findings.append(finding)

        except Exception as e:
            print(f"    ⚠️ Error converting result to findings: {e}")
            # Return a basic finding
            finding = {
                "finding_id": f"{agent_type.value}_error",
                "category": "error",
                "severity": "high",
                "description": f"Error in {agent_type.value} analysis: {str(e)}",
                "recommendations": ["Check agent configuration and try again"],
                "confidence": 0.5,
                "metadata": {
                    "cross_context_used": bool(cross_context),
                    "agent_type": agent_type.value,
                    "result_type": "error",
                },
                "cross_references": [],
            }
            findings.append(finding)

        return findings

    def _determine_severity(self, finding_data: Any) -> str:
        """Determine severity based on finding data"""
        try:
            if isinstance(finding_data, dict):
                # Check for explicit severity
                if "severity" in finding_data:
                    return finding_data["severity"]

                # Check for confidence-based severity
                confidence = finding_data.get("confidence", 0.5)
                if confidence > 0.9:
                    return "critical"
                if confidence > 0.8:
                    return "high"
                if confidence > 0.6:
                    return "medium"
                return "low"

                # Check for category-based severity
                category = finding_data.get("category", "").lower()
                if "security" in category or "critical" in category:
                    return "high"
                if "quality" in category or "medium" in category:
                    return "medium"
                return "low"

            return "medium"  # Default severity

        except Exception:
            return "medium"  # Fallback severity

    async def run_workflow(self) -> dict[str, Any]:
        """Run the complete LangGraph workflow"""
        logger.info("🚀 Starting LangGraph workflow execution...")

        try:
            # Initialize the workflow state as dict (required for TypedDict)
            initial_state: OrchestratorState = {
                "current_stage": WorkflowStage.INITIALIZE.value,
                "iteration_number": 0,
                "max_iterations": 5,
                "should_continue": True,
                "error_message": None,
                "agent_findings": {},
                "cross_agent_insights": [],
                "learning_outcomes": [],
                "next_actions": [],
                "messages": [],
            }
            logger.info(
                f"📊 Initial state: iteration={initial_state['iteration_number']}, max_iterations={initial_state['max_iterations']}"
            )

            # Run the workflow
            logger.info("🔄 Executing workflow...")
            final_state_dict = await self.workflow.ainvoke(initial_state)
            logger.info(
                f"✅ Workflow execution completed. Final state type: {type(final_state_dict)}"
            )

            # LangGraph returns dictionaries, so we always expect dict format
            final_state = final_state_dict
            logger.info("✅ Final state is dictionary (as expected from LangGraph)")

            # Extract results from dictionary format
            results = {
                "workflow_success": final_state.get("current_stage")
                == WorkflowStage.COMPLETE.value,
                "iterations_completed": final_state.get("iteration_number", 0),
                "final_stage": final_state.get("current_stage", "unknown"),
                "total_agent_findings": sum(
                    len(findings)
                    for findings in final_state.get("agent_findings", {}).values()
                ),
                "synthesis": final_state.get("synthesis"),
                "learning_outcomes": final_state.get("learning_outcomes", []),
                "error_message": final_state.get("error_message"),
                "quality_report": final_state.get("quality_report"),
            }

            logger.info(
                f"📋 Workflow results: success={results['workflow_success']}, iterations={results['iterations_completed']}"
            )
            return results

        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")

            # Return error results
            return {
                "workflow_success": False,
                "iterations_completed": 0,
                "final_stage": "error",
                "total_agent_findings": 0,
                "synthesis": None,
                "learning_outcomes": [],
                "error_message": str(e),
                "quality_report": None,
            }

    def get_workflow_summary(self) -> dict[str, Any]:
        """Get a summary of the workflow state"""
        return {
            "current_iteration": self.agent_session_manager.current_iteration,
            "total_iterations": len(self.agent_session_manager.iteration_contexts),
            "learning_summary": self.agent_session_manager.get_learning_summary(),
            "workflow_available": True,
        }
