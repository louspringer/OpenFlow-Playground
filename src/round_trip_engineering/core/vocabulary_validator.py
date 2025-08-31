#!/usr/bin/env python3
"""
Vocabulary Validator
Focused on validating vocabulary alignment and providing fallback mechanisms.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class VocabularyValidator:
    """Validates vocabulary alignment and provides fallback mechanisms."""

    def __init__(self):
        """Initialize the vocabulary validator."""
        logger.info("✅ Vocabulary validator initialized")

    def validate_vocabulary_alignment(
        self, original_model: Dict[str, Any], aligned_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate that vocabulary alignment was successful."""
        validation_result = {"valid": True, "issues": [], "improvements": []}

        # Check components structure
        if "components" in aligned_model:
            components = aligned_model["components"]
            if isinstance(components, dict):
                validation_result["improvements"].append(
                    "Components successfully converted to dict format"
                )

                # Check component structure
                for name, component in components.items():
                    if not isinstance(component, dict) or "name" not in component:
                        validation_result["valid"] = False
                        validation_result["issues"].append(
                            f"Component {name} missing required structure"
                        )
            else:
                validation_result["valid"] = False
                validation_result["issues"].append(
                    "Components not in expected dict format"
                )

        # Check workflow enhancement
        if "workflow_analysis" in aligned_model:
            workflow = aligned_model["workflow_analysis"]
            if isinstance(workflow, dict) and "complexity" in workflow:
                validation_result["improvements"].append(
                    "Workflow enhanced with complexity metrics"
                )
            else:
                validation_result["issues"].append("Workflow not properly enhanced")

        # Check relationships structure
        if "relationships" in aligned_model:
            relationships = aligned_model["relationships"]
            if isinstance(relationships, dict):
                validation_result["improvements"].append(
                    "Relationships successfully converted to dict format"
                )
            else:
                validation_result["issues"].append(
                    "Relationships not in expected dict format"
                )

        # Check enhanced AST data structure
        if "enhanced_ast_data" in aligned_model:
            ast_data = aligned_model["enhanced_ast_data"]
            if isinstance(ast_data, dict) and "classes" in ast_data:
                classes = ast_data["classes"]
                if isinstance(classes, list):
                    for i, cls in enumerate(classes):
                        if isinstance(cls, dict) and "name" in cls:
                            validation_result["improvements"].append(
                                f"Class {i} has proper structure"
                            )
                        else:
                            validation_result["valid"] = False
                            validation_result["issues"].append(
                                f"Class {i} missing required structure"
                            )

        logger.info(
            f"✅ Vocabulary alignment validation completed: {len(validation_result['improvements'])} improvements, {len(validation_result['issues'])} issues"
        )
        return validation_result

    def basic_vocabulary_alignment(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """Basic vocabulary alignment as fallback."""
        logger.info("🔄 Using basic vocabulary alignment fallback...")

        aligned_model = model.copy()

        # Basic components conversion
        if "components" in aligned_model:
            components = aligned_model["components"]
            if isinstance(components, list):
                aligned_model["components"] = (
                    self._basic_convert_components_list_to_dict(components)
                )

        # Basic workflow enhancement
        if "workflow_analysis" in aligned_model:
            workflow = aligned_model["workflow_analysis"]
            if isinstance(workflow, dict):
                if "complexity" not in workflow:
                    workflow["complexity"] = 1000
                if "nodes" not in workflow:
                    workflow["nodes"] = []
                if "edges" not in workflow:
                    workflow["edges"] = []

        return aligned_model

    def _basic_convert_components_list_to_dict(
        self, components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Basic conversion of components list to name-keyed dictionary."""
        if not isinstance(components, list):
            return components

        components_dict = {}
        for i, component in enumerate(components):
            if isinstance(component, dict) and "name" in component:
                name = component["name"]
                components_dict[name] = component
            else:
                # Generate a name for components without names
                generated_name = f"Component_{i}"
                if isinstance(component, dict):
                    component["name"] = generated_name
                else:
                    component = {"name": generated_name, "content": component}
                components_dict[generated_name] = component

        logger.info(f"✅ Basic conversion: {len(components)} components to dict format")
        return components_dict

    def get_validation_summary(
        self, validation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get a summary of vocabulary validation results."""
        try:
            return {
                "validation_successful": validation_result.get("valid", False),
                "total_improvements": len(validation_result.get("improvements", [])),
                "total_issues": len(validation_result.get("issues", [])),
                "alignment_quality": (
                    "excellent"
                    if validation_result.get("valid", False)
                    and len(validation_result.get("issues", [])) == 0
                    else (
                        "good"
                        if validation_result.get("valid", False)
                        else "needs_attention"
                    )
                ),
                "status": (
                    "validated"
                    if validation_result.get("valid", False)
                    else "validation_failed"
                ),
            }
        except Exception as e:
            logger.error(f"❌ Failed to generate validation summary: {e}")
            return {"error": str(e)}

    def get_validation_status(self) -> Dict[str, Any]:
        """Get the current status of vocabulary validation operations."""
        try:
            return {
                "validator_status": "operational",
                "validation_capabilities": [
                    "components_structure_validation",
                    "workflow_enhancement_validation",
                    "relationships_structure_validation",
                    "enhanced_ast_validation",
                    "fallback_alignment",
                ],
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get validation status: {e}")
            return {"error": str(e)}
