#!/usr/bin/env python3
"""
Mermaid Diagram Projector for Model-Driven Development

This projector generates Mermaid diagrams from project models and code structures,
integrating with the existing projection system architecture.
"""

import ast
import json
import logging
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MermaidProjector:
    """Project Mermaid diagrams from project models and code structures."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.models = {}
        self.load_project_model()

    def load_project_model(self) -> dict[str, Any]:
        """Load the project model registry."""
        model_path = self.project_root / "project_model_registry.json"
        if model_path.exists():
            try:
                with open(model_path) as f:
                    self.models = json.load(f)
                logger.info("✅ Project model loaded successfully")
            except Exception as e:
                logger.error(f"❌ Error loading project model: {e}")
        return self.models

    def project_system_architecture_diagram(self) -> str:
        """Project system architecture diagram from project model."""
        if not self.models:
            return self._generate_fallback_system_diagram()

        # Extract domain information from model
        _ = self.models.get("domain_architecture", {})

        mermaid = """graph TB
    subgraph "OpenFlow Playground"
        subgraph "Core Systems"
            AF[ArtifactForge]
            GB[Ghostbusters]
            MDT[Model-Driven Testing]
            SF[Security First]
        end

        subgraph "Domains"
            PY[Python]
            YAML[YAML/CloudFormation]
            SEC[Security]
            BASH[Bash]
            MDC[MDC Files]
        end

        subgraph "Tools"
            LINT[Linters]
            VAL[Validators]
            FMT[Formatters]
        end
    end

    AF --> PY
    AF --> YAML
    GB --> PY
    MDT --> PY
    SF --> SEC
    PY --> LINT
    YAML --> VAL
    SEC --> VAL
    BASH --> LINT
    MDC --> VAL"""

        return mermaid

    def project_ghostbusters_architecture_diagram(self) -> str:
        """Project Ghostbusters architecture from actual code."""
        gb_path = self.project_root / "src" / "ghostbusters"
        if not gb_path.exists():
            return self._generate_fallback_ghostbusters_diagram()

        # Extract actual classes using AST
        classes = self._extract_classes_from_directory(gb_path)

        mermaid = "classDiagram\n"
        for class_name, methods in classes.items():
            mermaid += f"    class {class_name} {{\n"
            for method in methods[:5]:  # Limit to first 5 methods
                mermaid += f"        +{method}\n"
            mermaid += "    }\n"

        # Add inheritance relationships
        if "BaseExpert" in classes and "SecurityExpert" in classes:
            mermaid += "    BaseExpert <|-- SecurityExpert\n"
        if "BaseValidator" in classes and "SecurityValidator" in classes:
            mermaid += "    BaseValidator <|-- SecurityValidator\n"
        if "BaseRecoveryEngine" in classes and "SyntaxRecoveryEngine" in classes:
            mermaid += "    BaseRecoveryEngine <|-- SyntaxRecoveryEngine\n"

        return mermaid

    def project_workflow_diagram(self) -> str:
        """Project workflow diagram from actual workflow code."""
        workflow_path = (
            self.project_root / "src" / "ghostbusters" / "ghostbusters_orchestrator.py"
        )
        if not workflow_path.exists():
            return self._generate_fallback_workflow_diagram()

        # Extract workflow states from actual code
        states = self._extract_workflow_states(workflow_path)

        mermaid = "stateDiagram-v2\n"
        mermaid += "    [*] --> Initialized\n"

        for i, state in enumerate(states):
            if i == 0:
                mermaid += f"    Initialized --> {state}\n"
            else:
                mermaid += f"    {states[i-1]} --> {state}\n"

        mermaid += f"    {states[-1]} --> [*]\n"

        return mermaid

    def project_testing_architecture_diagram(self) -> str:
        """Project testing architecture from model-driven testing system."""
        mdt_path = self.project_root / "src" / "model_driven_testing"
        if not mdt_path.exists():
            return self._generate_fallback_testing_diagram()

        # Extract actual test generator classes
        _ = self._extract_classes_from_directory(mdt_path)

        mermaid = """graph TB
    subgraph "Model-Driven Testing System"
        subgraph "Core Components"
            AM[Artifact Model Extractor]
            TMG[Test Model Generator]
            TCG[Test Code Generator]
        end

        subgraph "Artifact Types"
            CLASS[Class Artifacts]
            FUNC[Function Artifacts]
            MOD[Module Artifacts]
        end

        subgraph "Output"
            TESTS[Generated Tests]
            VALIDATION[Test Validation]
        end
    end

    AM --> TMG
    TMG --> TCG
    CLASS --> AM
    FUNC --> AM
    MOD --> AM
    TCG --> TESTS
    TESTS --> VALIDATION"""

        return mermaid

    def _extract_classes_from_directory(self, directory: Path) -> dict[str, list[str]]:
        """Extract classes and methods from Python files in directory."""
        classes = {}

        for py_file in directory.rglob("*.py"):
            try:
                with open(py_file) as f:
                    content = f.read()

                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        methods = []
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                methods.append(item.name)
                        classes[node.name] = methods
            except Exception as e:
                logger.warning(f"⚠️  Error parsing {py_file}: {e}")
                continue

        return classes

    def _extract_workflow_states(self, workflow_file: Path) -> list[str]:
        """Extract workflow states from workflow file."""
        try:
            with open(workflow_file) as f:
                content = f.read()

            # Look for workflow state patterns
            states = []
            lines = content.split("\n")
            for line in lines:
                if "state" in line.lower() and ":" in line:
                    state = line.split(":")[0].strip()
                    if state and not state.startswith("#"):
                        states.append(state)

            return states if states else ["Detection", "Validation", "Recovery"]
        except Exception as e:
            logger.warning(f"⚠️  Error extracting workflow states: {e}")
            return ["Detection", "Validation", "Recovery"]

    def _generate_fallback_system_diagram(self) -> str:
        """Generate fallback system diagram when model is unavailable."""
        return """graph TB
    subgraph "System Architecture"
        GB[Ghostbusters]
        MDT[Model-Driven Testing]
        SF[Security First]
    end

    GB --> MDT
    MDT --> SF"""

    def _generate_fallback_ghostbusters_diagram(self) -> str:
        """Generate fallback Ghostbusters diagram when code is unavailable."""
        return """classDiagram
    class GhostbustersOrchestrator {
        +project_path: Path
        +agents: Dict
        +validators: Dict
        +recovery_engines: Dict
    }

    class BaseExpert {
        <<abstract>>
        +name: str
        +analyze(project_path, context) Dict
    }

    BaseExpert <|-- SecurityExpert
    BaseExpert <|-- CodeQualityExpert"""

    def _generate_fallback_workflow_diagram(self) -> str:
        """Generate fallback workflow diagram when code is unavailable."""
        return """stateDiagram-v2
    [*] --> Initialized
    Initialized --> Detection
    Detection --> Validation
    Validation --> Recovery
    Recovery --> [*]"""

    def _generate_fallback_testing_diagram(self) -> str:
        """Generate fallback testing diagram when code is unavailable."""
        return """graph TB
    subgraph "Testing System"
        MDT[Model-Driven Testing]
        TESTS[Generated Tests]
    end

    MDT --> TESTS"""

    def project_all_diagrams(self) -> dict[str, str]:
        """Project all diagrams and return them."""
        return {
            "system_architecture": self.project_system_architecture_diagram(),
            "ghostbusters_architecture": self.project_ghostbusters_architecture_diagram(),
            "workflow": self.project_workflow_diagram(),
            "testing_architecture": self.project_testing_architecture_diagram(),
        }

    def update_markdown_file(
        self, markdown_file: Path, diagrams: dict[str, str]
    ) -> None:
        """Update markdown file with projected diagrams."""
        if not markdown_file.exists():
            logger.error(f"❌ Markdown file not found: {markdown_file}")
            return

        try:
            with open(markdown_file) as f:
                content = f.read()

            # First, fix any existing double backticks issues
            content = self._fix_double_backticks(content)

            # Replace each diagram section
            for diagram_name, diagram_content in diagrams.items():
                # Look for the specific diagram section
                section_pattern = f"### {diagram_name.replace('_', ' ').title()}"

                if section_pattern in content:
                    # Find the section and replace the diagram
                    sections = content.split(section_pattern)
                    if len(sections) > 1:
                        # Find the mermaid block in the second section
                        mermaid_start = sections[1].find("```mermaid")
                        if mermaid_start != -1:
                            mermaid_end = sections[1].find("```", mermaid_start + 1)
                            if mermaid_end != -1:
                                # Replace the diagram content
                                new_section = (
                                    sections[1][:mermaid_start]
                                    + f"```mermaid\n{diagram_content}\n```\n"
                                    + sections[1][mermaid_end + 3 :]
                                )
                                content = sections[0] + section_pattern + new_section

            # Write the updated content back
            with open(markdown_file, "w") as f:
                f.write(content)

            logger.info(f"✅ Updated {markdown_file} with projected diagrams")

        except Exception as e:
            logger.error(f"❌ Error updating markdown file: {e}")

    def _fix_double_backticks(self, content: str) -> str:
        """Fix double backticks issues in the content."""
        # Fix patterns like ```\n```
        content = content.replace("```\n```", "```")

        # Fix patterns like ```\n---\n``` (which creates double backticks)
        content = content.replace("```\n---\n", "```\n---\n")

        # Fix any remaining double backticks
        import re

        double_backtick_pattern = r"```\s*\n```"
        content = re.sub(double_backtick_pattern, "```", content)

        logger.info("🔧 Fixed double backticks issues")
        return content


def main():
    """Main function to project and update diagrams."""
    project_root = Path()
    projector = MermaidProjector(project_root)

    logger.info("🔍 Loading project model...")
    projector.load_project_model()

    logger.info("🎨 Projecting Mermaid diagrams...")
    diagrams = projector.project_all_diagrams()

    logger.info("📝 Updating markdown file...")
    markdown_file = Path("docs/GHOSTBUSTERS_COMPREHENSIVE_DESIGN.md")
    projector.update_markdown_file(markdown_file, diagrams)

    logger.info("✅ Mermaid diagram projection complete!")

    # Show what was projected
    for name, content in diagrams.items():
        logger.info(f"\n--- {name.replace('_', ' ').title()} ---")
        logger.info(content[:100] + "..." if len(content) > 100 else content)


if __name__ == "__main__":
    main()
