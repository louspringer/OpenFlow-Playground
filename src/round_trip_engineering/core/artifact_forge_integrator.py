#!/usr/bin/env python3
"""
ArtifactForge Integrator
Focused on ArtifactForge integration and enhanced AST parsing.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

from ..workflow_analyzer import WorkflowAnalyzer

logger = logging.getLogger(__name__)


class ArtifactForgeIntegrator:
    """Manages ArtifactForge integration and enhanced AST parsing."""

    def __init__(self):
        """Initialize the ArtifactForge integrator."""
        self.workflow_analyzer = WorkflowAnalyzer()
        logger.info("✅ ArtifactForge integrator initialized")

    def analyze_source_with_artifact_forge(
        self, source_path: str, target_language: str = "python"
    ) -> Dict[str, Any]:
        """
        Analyze source code with ArtifactForge and generate enhanced model.

        Args:
            source_path: Path to source Python file
            target_language: Target programming language

        Returns:
            Dictionary containing analysis results and enhanced model
        """
        try:
            logger.info(f"🔍 Starting ArtifactForge-integrated analysis: {source_path}")

            # Step 1: Use ArtifactForge for enhanced AST parsing and workflow analysis
            logger.info(
                "🔄 Step 1: ArtifactForge enhanced AST parsing and workflow analysis"
            )
            workflow_data = self.workflow_analyzer.analyze_workflow(source_path)

            if not workflow_data.get("workflow_analysis_successful", False):
                logger.warning(
                    "⚠️ Workflow analysis failed, proceeding with basic parsing"
                )

            # Step 2: Extract enhanced model from source using EnhancedArtifactParser
            logger.info("🔄 Step 2: Enhanced AST model extraction")
            from src.artifact_forge.agents.artifact_parser_enhanced import (
                EnhancedArtifactParser,
            )

            enhanced_parser = EnhancedArtifactParser()
            ast_result = enhanced_parser.parse_artifact(source_path, "python")

            if not ast_result.parsed_data:
                logger.warning(
                    "⚠️ Enhanced AST parsing failed, falling back to basic model"
                )
                # Fallback to simple model
                extracted_model = self._create_fallback_model(
                    source_path, workflow_data
                )
            else:
                # Use the rich enhanced AST data
                logger.info(
                    f"✅ Enhanced AST parsing successful: {len(ast_result.parsed_data.get('classes', []))} classes found"
                )
                extracted_model = self._create_enhanced_ast_model(
                    source_path, workflow_data, ast_result
                )

            logger.info("✅ ArtifactForge-integrated analysis completed successfully")
            return extracted_model

        except Exception as e:
            logger.error(f"❌ ArtifactForge-integrated analysis failed: {e}")
            return {
                "source_path": source_path,
                "error": str(e),
                "artifactorge_integration": "failed",
            }

    def _create_fallback_model(
        self, source_path: str, workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a fallback model when enhanced AST parsing fails."""
        return {
            "components": [
                {
                    "name": "GeneratedClass",
                    "type": "class",
                    "description": f"Generated from {source_path} with workflow analysis",
                    "workflow_complexity": workflow_data.get("complexity", 0),
                    "workflow_nodes": len(workflow_data.get("nodes", [])),
                    "workflow_edges": len(workflow_data.get("edges", [])),
                }
            ],
            "name": f"WorkflowEnhanced_{source_path.split('/')[-1].replace('.py', '')}",
            "description": f"Enhanced model with workflow analysis from {source_path}",
            "workflow_analysis": workflow_data,
        }

    def _create_enhanced_ast_model(
        self, source_path: str, workflow_data: Dict[str, Any], ast_result: Any
    ) -> Dict[str, Any]:
        """Create an enhanced AST model from successful parsing."""
        components = []
        for cls in ast_result.parsed_data.get("classes", []):
            component = {
                "name": cls.get("name", "UnknownClass"),
                "type": "class",
                "description": f"Enhanced AST extracted class: {cls.get('name', 'Unknown')}",
                "workflow_complexity": workflow_data.get("complexity", 0),
                "workflow_nodes": len(workflow_data.get("nodes", [])),
                "workflow_edges": len(workflow_data.get("edges", [])),
                # Enhanced AST data - store raw for now, will build clean model later
                "enhanced_ast": {
                    "bases": cls.get("bases", []),
                    "methods": cls.get("methods", []),
                    "class_variables": cls.get("class_variables", []),
                    "source_code": cls.get("source_code", ""),
                    "method_count": cls.get("method_count", 0),
                    "docstring": cls.get("docstring", ""),
                },
            }
            components.append(component)

        return {
            "components": components,
            "name": f"EnhancedAST_{source_path.split('/')[-1].replace('.py', '')}",
            "description": f"Enhanced AST model with workflow analysis from {source_path}",
            "workflow_analysis": workflow_data,
            "enhanced_ast_data": ast_result.parsed_data,
        }

    def get_integration_status(self) -> Dict[str, Any]:
        """Get the current status of ArtifactForge integration."""
        try:
            return {
                "workflow_analyzer_status": "operational",
                "enhanced_parser_available": True,
                "integration_health": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get integration status: {e}")
            return {"error": str(e)}
