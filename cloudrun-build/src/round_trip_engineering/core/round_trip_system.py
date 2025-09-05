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
from .model_manager import ModelManager

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
        self.model_manager = ModelManager()

        # Expose components for backward compatibility with tests
        self.vocabulary_aligner = self.code_generation_orchestrator.vocabulary_aligner
        self.code_generator = self.code_generation_orchestrator.code_generator
        self.duplication_cleaner = self.code_generation_orchestrator.duplication_cleaner
        self.profiler = self.code_generation_orchestrator.profiler

        logger.info("✅ Round-trip system initialized with focused modules")

    def create_model_from_design(self, design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a model from design specification.

        Args:
            design_spec: Design specification dictionary

        Returns:
            Dictionary containing model creation results
        """
        try:
            logger.info(f"🎯 Creating model from design: {design_spec.get('name', 'Unknown')}")
            model = self.model_manager.create_model_from_design(design_spec)
            
            result = {
                "success": True,
                "model_name": model["name"],
                "component_count": len(model["components"]),
                "message": f"✅ Created model with {len(model['components'])} components",
            }
            
            logger.info(f"✅ Successfully created model: {model['name']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to create model from design: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Failed to create model: {e}",
            }

    def generate_code_from_model(self, model_name: str) -> Dict[str, Any]:
        """
        Generate code from a model.

        Args:
            model_name: Name of the model to generate code from

        Returns:
            Dictionary containing code generation results
        """
        try:
            logger.info(f"🎯 Generating code from model: {model_name}")
            
            # Get the model from the model manager
            if model_name not in self.model_manager.design_models:
                raise ValueError(f"Model '{model_name}' not found")
            
            model = self.model_manager.design_models[model_name]
            
            # Generate code using the code generation orchestrator
            generated_code = self.code_generation_orchestrator.generate_code_from_extracted_model(model)
            
            result = {
                "success": True,
                "model_name": model_name,
                "generated_code": generated_code,
                "message": f"✅ Generated code from model: {model_name}",
            }
            
            logger.info(f"✅ Successfully generated code from model: {model_name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to generate code from model: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Failed to generate code: {e}",
            }

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

    def print_profiling_summary(self) -> None:
        """Print profiling summary using the profiler component."""
        try:
            self.profiler.print_summary()
        except Exception as e:
            logger.error(f"❌ Failed to print profiling summary: {e}")

    def get_profiling_stats(self) -> Dict[str, Any]:
        """Get profiling statistics from the profiler component."""
        try:
            return self.profiler.get_stats()
        except Exception as e:
            logger.error(f"❌ Failed to get profiling stats: {e}")
            return {"error": str(e)}
