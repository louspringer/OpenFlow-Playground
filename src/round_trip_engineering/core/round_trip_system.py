"""
Core Round-Trip Engineering System

This module orchestrates the round-trip engineering process between models and code.
It coordinates vocabulary alignment, code generation, and cleaning operations.
"""

import logging
import sys
from typing import Dict, Any, List
from pathlib import Path

# Add the ontology bridge to the path
ontology_bridge_path = Path(__file__).parent.parent.parent.parent / "scripts"
sys.path.insert(0, str(ontology_bridge_path))

try:
    from simple_ontology_bridge import SimpleOntologyBridge

    ONTOLOGY_BRIDGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Ontology bridge not available: {e}")
    ONTOLOGY_BRIDGE_AVAILABLE = False

from .code_generation_orchestrator import CodeGenerationOrchestrator
from .artifact_forge_integrator import ArtifactForgeIntegrator
from .workflow_analysis_manager import WorkflowAnalysisManager

logger = logging.getLogger(__name__)


class RoundTripSystem:
    """
    Main orchestrator for round-trip engineering system.

    Integrates ArtifactForge parsing, workflow analysis, and code generation
    to provide comprehensive round-trip engineering capabilities.
    """

    def __init__(self):
        """Initialize the round-trip system with focused modules."""
        self.code_generation_orchestrator = CodeGenerationOrchestrator()
        self.artifact_forge_integrator = ArtifactForgeIntegrator()
        self.workflow_analysis_manager = WorkflowAnalysisManager()

        logger.info("✅ Round-trip system initialized with focused modules")

    def generate_code_from_extracted_model(self, extracted_model: Dict[str, Any], target_language: str = "python") -> str:
        """
        Generate code from an extracted model using ontological vocabulary alignment.

        Args:
            extracted_model: The extracted model from reverse engineering
            target_language: Target programming language

        Returns:
            Generated code as string
        """
        try:
            logger.info(f"🎯 Generating {target_language} code from extracted model...")
            return self.code_generation_orchestrator.generate_code_from_extracted_model(extracted_model, target_language)
        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            raise

    def analyze_and_generate_code(self, source_path: str, target_language: str = "python") -> Dict[str, Any]:
        """
        Analyze source code with ArtifactForge and generate enhanced code.

        This method demonstrates the full ArtifactForge integration:
        1. Uses ArtifactForge for enhanced AST parsing and workflow analysis
        2. Extracts rich model data with full method implementations
        3. Generates improved code using the enhanced AST model

        Args:
            source_path: Path to source Python file
            target_language: Target programming language

        Returns:
            Dictionary containing analysis results and generated code
        """
        try:
            logger.info(f"🔍 Starting ArtifactForge-integrated analysis: {source_path}")

            # Step 1: Use ArtifactForge for enhanced AST parsing and workflow analysis
            logger.info("🔄 Step 1: ArtifactForge enhanced AST parsing and workflow analysis")
            extracted_model = self.artifact_forge_integrator.analyze_source_with_artifact_forge(source_path, target_language)

            # Step 2: Generate enhanced code using the enriched model
            logger.info("🔄 Step 2: Enhanced code generation from AST data")
            generated_code = self.generate_code_from_extracted_model(extracted_model, target_language)

            # Step 3: Compile results
            workflow_data = extracted_model.get("workflow_analysis", {})
            ast_result = extracted_model.get("enhanced_ast_data", {})

            results = {
                "source_path": source_path,
                "workflow_analysis": workflow_data,
                "extracted_model": extracted_model,
                "generated_code": generated_code,
                "enhancement_metrics": {
                    "workflow_nodes_analyzed": len(workflow_data.get("nodes", [])),
                    "workflow_complexity": workflow_data.get("complexity", 0),
                    "code_generation_successful": True,
                    "artifactorge_integration": "success",
                    "enhanced_ast_classes": (len(ast_result.get("classes", [])) if ast_result else 0),
                    "enhanced_ast_methods": (sum(len(cls.get("methods", [])) for cls in ast_result.get("classes", [])) if ast_result else 0),
                },
            }

            logger.info("✅ ArtifactForge-integrated analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"❌ ArtifactForge-integrated analysis failed: {e}")
            return {
                "source_path": source_path,
                "error": str(e),
                "artifactorge_integration": "failed",
            }

    def get_workflow_analysis(self, source_path: str) -> Dict[str, Any]:
        """
        Get workflow analysis for a source file using ArtifactForge integration.

        Args:
            source_path: Path to source Python file

        Returns:
            Workflow analysis results
        """
        try:
            logger.info(f"🔍 Getting workflow analysis for: {source_path}")
            return self.workflow_analysis_manager.get_workflow_analysis(source_path)
        except Exception as e:
            logger.error(f"❌ Workflow analysis failed: {e}")
            return {
                "source_path": source_path,
                "workflow_analysis_successful": False,
                "error": str(e),
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get the overall status of the round-trip system."""
        try:
            return {
                "code_generation_status": self.code_generation_orchestrator.get_generation_metrics(),
                "artifact_forge_status": self.artifact_forge_integrator.get_integration_status(),
                "workflow_analysis_status": self.workflow_analysis_manager.get_analysis_status(),
                "overall_status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get system status: {e}")
            return {"error": str(e)}
