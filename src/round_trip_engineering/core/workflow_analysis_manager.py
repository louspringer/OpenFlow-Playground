#!/usr/bin/env python3
"""
Workflow Analysis Manager
Focused on managing workflow analysis operations.
"""

import logging
from typing import Dict, Any, List

from ..workflow_analyzer import WorkflowAnalyzer

logger = logging.getLogger(__name__)


class WorkflowAnalysisManager:
    """Manages workflow analysis operations."""

    def __init__(self):
        """Initialize the workflow analysis manager."""
        self.workflow_analyzer = WorkflowAnalyzer()
        logger.info("✅ Workflow analysis manager initialized")

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
            workflow_data = self.workflow_analyzer.analyze_workflow(source_path)

            logger.info(
                f"✅ Workflow analysis completed: {len(workflow_data.get('nodes', []))} nodes"
            )
            return workflow_data

        except Exception as e:
            logger.error(f"❌ Workflow analysis failed: {e}")
            return {
                "source_path": source_path,
                "workflow_analysis_successful": False,
                "error": str(e),
            }

    def analyze_workflow_complexity(
        self, workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze the complexity of a workflow.

        Args:
            workflow_data: Workflow analysis data

        Returns:
            Complexity analysis results
        """
        try:
            nodes = workflow_data.get("nodes", [])
            edges = workflow_data.get("edges", [])

            complexity_metrics = {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "complexity_score": len(nodes)
                * len(edges)
                / 100,  # Simple complexity formula
                "density": len(edges) / max(len(nodes), 1),
                "analysis_timestamp": workflow_data.get("timestamp", "unknown"),
            }

            logger.info(
                f"✅ Workflow complexity analysis completed: {complexity_metrics['complexity_score']:.2f}"
            )
            return complexity_metrics

        except Exception as e:
            logger.error(f"❌ Workflow complexity analysis failed: {e}")
            return {"error": str(e)}

    def get_workflow_summary(self, source_path: str) -> Dict[str, Any]:
        """
        Get a summary of workflow analysis for a source file.

        Args:
            source_path: Path to source Python file

        Returns:
            Workflow summary
        """
        try:
            workflow_data = self.get_workflow_analysis(source_path)
            complexity_metrics = self.analyze_workflow_complexity(workflow_data)

            summary = {
                "source_path": source_path,
                "workflow_analysis_successful": workflow_data.get(
                    "workflow_analysis_successful", False
                ),
                "complexity_metrics": complexity_metrics,
                "nodes": workflow_data.get("nodes", []),
                "edges": workflow_data.get("edges", []),
                "timestamp": workflow_data.get("timestamp", "unknown"),
            }

            if "error" in workflow_data:
                summary["error"] = workflow_data["error"]

            logger.info(f"✅ Workflow summary generated for: {source_path}")
            return summary

        except Exception as e:
            logger.error(f"❌ Failed to generate workflow summary: {e}")
            return {
                "source_path": source_path,
                "error": str(e),
                "workflow_analysis_successful": False,
            }

    def get_analysis_status(self) -> Dict[str, Any]:
        """Get the current status of workflow analysis operations."""
        try:
            return {
                "workflow_analyzer_status": "operational",
                "analysis_capabilities": [
                    "workflow_analysis",
                    "complexity_analysis",
                    "summary_generation",
                ],
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get analysis status: {e}")
            return {"error": str(e)}
