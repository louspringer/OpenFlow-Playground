#!/usr/bin/env python3
"""
Step Model - Defines the workflow steps and their relationships

This follows a model-first approach:
1. Define what each step does
2. Define inputs/outputs for each step
3. Define step relationships and flow
4. Then implement the actual workflow
"""

from dataclasses import dataclass, field
from enum import Enum


class StepType(Enum):
    """Types of workflow steps"""

    INITIALIZE = "initialize"
    PLAN = "plan"
    DO = "do"
    CHECK = "check"
    ACT = "act"
    SYNTHESIZE = "synthesize"
    COMPLETE = "complete"


class StepStatus(Enum):
    """Status of a workflow step"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepInput:
    """Input requirements for a step"""

    required: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class StepOutput:
    """Output produced by a step"""

    required: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class StepDefinition:
    """Definition of a workflow step"""

    step_type: StepType
    name: str
    description: str
    inputs: StepInput
    outputs: StepOutput
    dependencies: list[str] = field(default_factory=list)
    timeout_seconds: int = 300
    retry_count: int = 3
    parallel_executable: bool = False


@dataclass
class WorkflowModel:
    """Complete workflow model"""

    name: str
    description: str
    steps: dict[str, StepDefinition]
    step_order: list[str]
    parallel_groups: list[list[str]] = field(default_factory=list)
    error_handling: dict[str, str] = field(default_factory=dict)
    success_criteria: list[str] = field(default_factory=list)


class StepModelBuilder:
    """Builder for creating step models"""

    @staticmethod
    def build_code_quality_workflow() -> WorkflowModel:
        """Build the code quality automation workflow model"""

        steps = {
            "initialize": StepDefinition(
                step_type=StepType.INITIALIZE,
                name="Initialize Workflow",
                description="Initialize the workflow and start a new iteration",
                inputs=StepInput(
                    required=["target_directory", "max_iterations"],
                    optional=["storage_dir"],
                    description="Basic workflow configuration",
                ),
                outputs=StepOutput(
                    required=["iteration_number", "workflow_state"],
                    optional=["agent_sessions"],
                    description="Initialized workflow state",
                ),
                dependencies=[],
                timeout_seconds=60,
                retry_count=1,
                parallel_executable=False,
            ),
            "plan": StepDefinition(
                step_type=StepType.PLAN,
                name="Plan Phase",
                description="Generate current quality report and plan actions",
                inputs=StepInput(
                    required=["iteration_number", "target_directory"],
                    optional=["previous_quality_report"],
                    description="Current iteration context and target directory",
                ),
                outputs=StepOutput(
                    required=["quality_report", "action_plan"],
                    optional=["quality_metrics", "trends"],
                    description="Quality analysis and action plan",
                ),
                dependencies=["initialize"],
                timeout_seconds=120,
                retry_count=2,
                parallel_executable=False,
            ),
            "do": StepDefinition(
                step_type=StepType.DO,
                name="Execute Phase",
                description="Apply automated fixes and improvements",
                inputs=StepInput(
                    required=["action_plan", "target_directory"],
                    optional=["quality_report"],
                    description="Action plan and target directory",
                ),
                outputs=StepOutput(
                    required=[
                        "subproject_results",
                        "formatting_results",
                        "linting_results",
                    ],
                    optional=["fix_summary", "improvement_metrics"],
                    description="Results of automated fixes",
                ),
                dependencies=["plan"],
                timeout_seconds=600,  # 10 minutes for file operations
                retry_count=2,
                parallel_executable=True,  # Can run subproject, formatting, linting in parallel
            ),
            "check": StepDefinition(
                step_type=StepType.CHECK,
                name="Validation Phase",
                description="Run pre-commit validation and quality checks",
                inputs=StepInput(
                    required=["target_directory", "fix_results"],
                    optional=["quality_report"],
                    description="Target directory and results from fixes",
                ),
                outputs=StepOutput(
                    required=["pre_commit_results", "validation_summary"],
                    optional=["quality_improvement", "remaining_issues"],
                    description="Validation results and quality status",
                ),
                dependencies=["do"],
                timeout_seconds=180,
                retry_count=2,
                parallel_executable=False,
            ),
            "act": StepDefinition(
                step_type=StepType.ACT,
                name="Multi-Agent Analysis",
                description="Run collaborative multi-agent analysis with context sharing",
                inputs=StepInput(
                    required=["quality_report", "validation_results", "agent_sessions"],
                    optional=["previous_findings", "cross_agent_context"],
                    description="Quality context and agent session state",
                ),
                outputs=StepOutput(
                    required=["agent_findings", "cross_agent_insights"],
                    optional=["collaborative_patterns", "synthesis_inputs"],
                    description="Agent analysis results and collaborative insights",
                ),
                dependencies=["check"],
                timeout_seconds=300,  # 5 minutes for LLM calls
                retry_count=3,
                parallel_executable=True,  # Agents can run in parallel
            ),
            "synthesize": StepDefinition(
                step_type=StepType.SYNTHESIZE,
                name="Synthesis Phase",
                description="Synthesize results and plan next iteration",
                inputs=StepInput(
                    required=[
                        "agent_findings",
                        "cross_agent_insights",
                        "quality_report",
                    ],
                    optional=["previous_synthesis", "learning_context"],
                    description="All analysis results and context",
                ),
                outputs=StepOutput(
                    required=["synthesis", "next_iteration_plan", "should_continue"],
                    optional=["learning_outcomes", "recommendations"],
                    description="Synthesized results and iteration planning",
                ),
                dependencies=["act"],
                timeout_seconds=120,
                retry_count=2,
                parallel_executable=False,
            ),
            "complete": StepDefinition(
                step_type=StepType.COMPLETE,
                name="Complete Workflow",
                description="Finalize workflow and generate summary",
                inputs=StepInput(
                    required=["synthesis", "iteration_history"],
                    optional=["final_quality_report"],
                    description="Final synthesis and iteration history",
                ),
                outputs=StepOutput(
                    required=["workflow_summary", "final_status"],
                    optional=["recommendations", "next_actions"],
                    description="Final workflow summary and recommendations",
                ),
                dependencies=["synthesize"],
                timeout_seconds=60,
                retry_count=1,
                parallel_executable=False,
            ),
        }

        # Define step order
        step_order = [
            "initialize",
            "plan",
            "do",
            "check",
            "act",
            "synthesize",
            "complete",
        ]

        # Define parallel execution groups
        parallel_groups = [
            ["do"]  # The "do" step itself can run its sub-operations in parallel
        ]

        # Define error handling
        error_handling = {
            "initialize": "retry_once_then_fail",
            "plan": "retry_twice_then_continue_with_defaults",
            "do": "retry_twice_then_continue_with_partial_results",
            "check": "retry_twice_then_continue_with_warning",
            "act": "retry_three_times_then_continue_with_fallback",
            "synthesize": "retry_twice_then_continue_with_basic_synthesis",
            "complete": "retry_once_then_continue",
        }

        # Define success criteria
        success_criteria = [
            "All required steps completed successfully",
            "Quality issues reduced or addressed",
            "Multi-agent analysis provided actionable insights",
            "Workflow reached completion state",
        ]

        return WorkflowModel(
            name="Code Quality Automation Workflow",
            description="PDCA-based workflow for automated code quality improvement with multi-agent analysis",
            steps=steps,
            step_order=step_order,
            parallel_groups=parallel_groups,
            error_handling=error_handling,
            success_criteria=success_criteria,
        )

    @staticmethod
    def validate_workflow_model(model: WorkflowModel) -> list[str]:
        """Validate a workflow model for consistency"""
        errors = []

        # Check that all steps in step_order exist in steps
        for step_name in model.step_order:
            if step_name not in model.steps:
                errors.append(
                    f"Step '{step_name}' in step_order but not defined in steps"
                )

        # Check that all steps have dependencies that exist
        for step_name, step in model.steps.items():
            for dep in step.dependencies:
                if dep not in model.steps:
                    errors.append(
                        f"Step '{step_name}' depends on undefined step '{dep}'"
                    )

        # Check for circular dependencies
        for step_name, step in model.steps.items():
            if step_name in step.dependencies:
                errors.append(f"Step '{step_name}' has circular dependency on itself")

        # Check that parallel groups only contain valid steps
        for group in model.parallel_groups:
            for step_name in group:
                if step_name not in model.steps:
                    errors.append(
                        f"Parallel group contains undefined step '{step_name}'"
                    )

        return errors

    @staticmethod
    def generate_workflow_diagram() -> str:
        """Generate a Mermaid diagram for the workflow"""
        mermaid_lines = [
            "graph TD",
            "    A[Initialize] --> B[Plan]",
            "    B --> C[Do]",
            "    C --> D[Check]",
            "    D --> E[Act]",
            "    E --> F[Synthesize]",
            "    F --> G{Continue?}",
            "    G -->|Yes| B",
            "    G -->|No| H[Complete]",
            "",
            "    %% Parallel execution within Do phase",
            "    C --> C1[Subproject Scrubbing]",
            "    C --> C2[Formatting]",
            "    C --> C3[Linting]",
            "    C1 --> C4[Do Complete]",
            "    C2 --> C4",
            "    C3 --> C4",
            "    C4 --> D",
            "",
            "    %% Parallel execution within Act phase",
            "    E --> E1[Security Expert]",
            "    E --> E2[Quality Expert]",
            "    E --> E3[DevOps Expert]",
            "    E1 --> E4[Act Complete]",
            "    E2 --> E4",
            "    E3 --> E4",
            "    E4 --> F",
            "",
            "    style A fill:#e1f5fe",
            "    style H fill:#c8e6c9",
            "    style G fill:#fff3e0",
            "    style C1 fill:#f3e5f5",
            "    style C2 fill:#f3e5f5",
            "    style C3 fill:#f3e5f5",
            "    style E1 fill:#e8f5e8",
            "    style E2 fill:#e8f5e8",
            "    style E3 fill:#e8f5e8",
        ]

        return "\n".join(mermaid_lines)


# Pre-built workflow models
CODE_QUALITY_WORKFLOW = StepModelBuilder.build_code_quality_workflow()


def validate_and_show_workflow():
    """Validate the workflow model and show details"""
    print("🔍 Validating Code Quality Workflow Model")
    print("=" * 50)

    # Validate the model
    errors = StepModelBuilder.validate_workflow_model(CODE_QUALITY_WORKFLOW)

    if errors:
        print("❌ Workflow model validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ Workflow model validation passed!")

    # Show workflow details
    print(f"\n📋 Workflow: {CODE_QUALITY_WORKFLOW.name}")
    print(f"Description: {CODE_QUALITY_WORKFLOW.description}")
    print(f"Total steps: {len(CODE_QUALITY_WORKFLOW.steps)}")

    print("\n🔄 Step Flow:")
    for i, step_name in enumerate(CODE_QUALITY_WORKFLOW.step_order):
        step = CODE_QUALITY_WORKFLOW.steps[step_name]
        print(f"  {i+1}. {step.name} ({step.step_type.value})")
        print(
            f"     Dependencies: {', '.join(step.dependencies) if step.dependencies else 'None'}"
        )
        print(f"     Parallel: {'Yes' if step.parallel_executable else 'No'}")
        print(f"     Timeout: {step.timeout_seconds}s")

    print("\n⚡ Parallel Execution Groups:")
    for i, group in enumerate(CODE_QUALITY_WORKFLOW.parallel_groups):
        print(f"  Group {i+1}: {', '.join(group)}")

    print("\n🎯 Success Criteria:")
    for i, criterion in enumerate(CODE_QUALITY_WORKFLOW.success_criteria):
        print(f"  {i+1}. {criterion}")

    return True


if __name__ == "__main__":
    # Validate and show the workflow model
    validate_and_show_workflow()

    # Generate workflow diagram
    print("\n📊 Workflow Diagram (Mermaid):")
    print("```mermaid")
    print(StepModelBuilder.generate_workflow_diagram(CODE_QUALITY_WORKFLOW))
    print("```")
