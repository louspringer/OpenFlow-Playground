#!/usr/bin/env python3
"""
Vocabulary Analyzer
Focused on analyzing vocabulary mismatches between domains.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class VocabularyAnalyzer:
    """Analyzes vocabulary mismatches between domains."""

    def __init__(self):
        """Initialize the vocabulary analyzer."""
        logger.info("✅ Vocabulary analyzer initialized")

    def analyze_vocabulary_mismatches(self, model: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze vocabulary mismatches between domains."""
        mismatches = []

        # Check components field alignment
        if "components" in model:
            components = model["components"]

            # Check if components is in the expected format for code generation
            if isinstance(components, list):
                mismatches.append(
                    {
                        "field": "components",
                        "current_type": "list",
                        "expected_type": "dict",
                        "description": "Components should be dict for code generation",
                        "transformation": "convert_list_to_dict_by_name",
                    }
                )
            elif isinstance(components, dict):
                # Validate dict structure
                for name, component in components.items():
                    if not isinstance(component, dict) or "name" not in component:
                        mismatches.append(
                            {
                                "field": f"components.{name}",
                                "current_type": type(component).__name__,
                                "expected_type": "dict_with_name",
                                "description": f"Component {name} should have 'name' field",
                                "transformation": "ensure_component_structure",
                            }
                        )

        # Check workflow field enhancement
        if "workflow_analysis" in model:
            workflow = model["workflow_analysis"]
            if not isinstance(workflow, dict) or "complexity" not in workflow:
                mismatches.append(
                    {
                        "field": "workflow_analysis",
                        "current_type": "basic_workflow",
                        "expected_type": "enhanced_workflow",
                        "description": "Workflow should include complexity metrics",
                        "transformation": "enhance_workflow_metrics",
                    }
                )

        # Check relationships field alignment
        if "relationships" in model:
            relationships = model["relationships"]
            if isinstance(relationships, list):
                mismatches.append(
                    {
                        "field": "relationships",
                        "current_type": "list",
                        "expected_type": "dict",
                        "description": "Relationships should be dict for code generation",
                        "transformation": "convert_list_to_dict_by_id",
                    }
                )

        # Check enhanced AST data structure
        if "enhanced_ast_data" in model:
            ast_data = model["enhanced_ast_data"]
            if isinstance(ast_data, dict) and "classes" in ast_data:
                classes = ast_data["classes"]
                if isinstance(classes, list):
                    for i, cls in enumerate(classes):
                        if not isinstance(cls, dict) or "name" not in cls:
                            mismatches.append(
                                {
                                    "field": f"enhanced_ast_data.classes[{i}]",
                                    "current_type": type(cls).__name__,
                                    "expected_type": "dict_with_name",
                                    "description": f"Class {i} should have 'name' field",
                                    "transformation": "ensure_class_structure",
                                }
                            )

        logger.info(f"🔍 Found {len(mismatches)} vocabulary mismatches")
        return mismatches

    def get_mismatch_summary(self, mismatches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get a summary of vocabulary mismatches."""
        try:
            if not mismatches:
                return {
                    "total_mismatches": 0,
                    "status": "no_mismatches",
                    "message": "Vocabulary is already aligned",
                }

            # Group mismatches by transformation type
            transformation_counts = {}
            field_types = {}

            for mismatch in mismatches:
                transformation = mismatch.get("transformation", "unknown")
                field = mismatch.get("field", "unknown")
                current_type = mismatch.get("current_type", "unknown")

                transformation_counts[transformation] = transformation_counts.get(transformation, 0) + 1
                field_types[field] = current_type

            return {
                "total_mismatches": len(mismatches),
                "status": "mismatches_found",
                "transformation_counts": transformation_counts,
                "field_types": field_types,
                "priority": "high" if len(mismatches) > 5 else "medium",
            }

        except Exception as e:
            logger.error(f"❌ Failed to generate mismatch summary: {e}")
            return {"error": str(e)}

    def get_analysis_status(self) -> Dict[str, Any]:
        """Get the current status of vocabulary analysis operations."""
        try:
            return {
                "analyzer_status": "operational",
                "analysis_capabilities": [
                    "components_alignment",
                    "workflow_enhancement",
                    "relationships_alignment",
                    "enhanced_ast_validation",
                ],
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get analysis status: {e}")
            return {"error": str(e)}
