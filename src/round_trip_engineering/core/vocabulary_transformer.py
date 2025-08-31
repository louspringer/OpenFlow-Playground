#!/usr/bin/env python3
"""
Vocabulary Transformer
Focused on applying transformations to resolve vocabulary mismatches.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class VocabularyTransformer:
    """Applies transformations to resolve vocabulary mismatches."""

    def __init__(self):
        """Initialize the vocabulary transformer."""
        logger.info("✅ Vocabulary transformer initialized")

    def apply_vocabulary_transformations(
        self, model: Dict[str, Any], mismatches: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply vocabulary transformations to resolve mismatches."""
        aligned_model = model.copy()

        for mismatch in mismatches:
            field = mismatch["field"]
            transformation = mismatch["transformation"]

            logger.info(f"🔄 Applying transformation: {transformation}")

            if transformation == "convert_list_to_dict_by_name":
                if field == "components":
                    aligned_model["components"] = self._convert_components_list_to_dict(
                        aligned_model["components"]
                    )

            elif transformation == "ensure_component_structure":
                if field.startswith("components."):
                    component_name = field.split(".")[1]
                    if component_name in aligned_model["components"]:
                        aligned_model["components"][component_name] = (
                            self._ensure_component_structure(
                                aligned_model["components"][component_name]
                            )
                        )

            elif transformation == "enhance_workflow_metrics":
                if field == "workflow_analysis":
                    aligned_model["workflow_analysis"] = self._enhance_workflow_metrics(
                        aligned_model["workflow_analysis"]
                    )

            elif transformation == "convert_list_to_dict_by_id":
                if field == "relationships":
                    aligned_model["relationships"] = (
                        self._convert_relationships_list_to_dict(
                            aligned_model["relationships"]
                        )
                    )

            elif transformation == "ensure_class_structure":
                if field.startswith("enhanced_ast_data.classes["):
                    # Extract class index from field path
                    try:
                        class_index = int(field.split("[")[1].split("]")[0])
                        if (
                            "enhanced_ast_data" in aligned_model
                            and "classes" in aligned_model["enhanced_ast_data"]
                        ):
                            classes = aligned_model["enhanced_ast_data"]["classes"]
                            if isinstance(classes, list) and 0 <= class_index < len(
                                classes
                            ):
                                classes[class_index] = self._ensure_class_structure(
                                    classes[class_index]
                                )
                    except (ValueError, IndexError):
                        logger.warning(
                            f"⚠️ Could not parse class index from field: {field}"
                        )

        return aligned_model

    def _convert_components_list_to_dict(
        self, components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert components list to name-keyed dictionary."""
        if not isinstance(components, list):
            return components

        components_dict = {}
        for component in components:
            if isinstance(component, dict) and "name" in component:
                name = component["name"]
                components_dict[name] = component
            else:
                # Generate a name for components without names
                generated_name = f"Component_{len(components_dict)}"
                if isinstance(component, dict):
                    component["name"] = generated_name
                else:
                    component = {"name": generated_name, "content": component}
                components_dict[generated_name] = component

        logger.info(f"✅ Converted {len(components)} components to dict format")
        return components_dict

    def _ensure_component_structure(self, component: Any) -> Dict[str, Any]:
        """Ensure component has proper structure."""
        if isinstance(component, dict):
            if "name" not in component:
                component["name"] = "UnnamedComponent"
            if "type" not in component:
                component["type"] = "unknown"
            return component
        else:
            return {
                "name": "GeneratedComponent",
                "type": "unknown",
                "content": component,
            }

    def _enhance_workflow_metrics(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance workflow with complexity metrics."""
        if not isinstance(workflow, dict):
            workflow = {}

        # Add complexity metrics if missing
        if "complexity" not in workflow:
            workflow["complexity"] = 1000  # Default complexity

        if "nodes" not in workflow:
            workflow["nodes"] = []

        if "edges" not in workflow:
            workflow["edges"] = []

        # Calculate complexity based on nodes and edges
        node_count = len(workflow.get("nodes", []))
        edge_count = len(workflow.get("edges", []))

        if node_count > 0:
            workflow["complexity"] = max(
                workflow["complexity"], node_count * 10 + edge_count * 5
            )

        return workflow

    def _convert_relationships_list_to_dict(
        self, relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert relationships list to ID-keyed dictionary."""
        if not isinstance(relationships, list):
            return relationships

        relationships_dict = {}
        for i, relationship in enumerate(relationships):
            if isinstance(relationship, dict) and "id" in relationship:
                rel_id = relationship["id"]
                relationships_dict[rel_id] = relationship
            else:
                # Generate an ID for relationships without IDs
                generated_id = f"rel_{i}"
                if isinstance(relationship, dict):
                    relationship["id"] = generated_id
                else:
                    relationship = {"id": generated_id, "content": relationship}
                relationships_dict[generated_id] = relationship

        logger.info(f"✅ Converted {len(relationships)} relationships to dict format")
        return relationships_dict

    def _ensure_class_structure(self, cls: Any) -> Dict[str, Any]:
        """Ensure class has proper structure."""
        if isinstance(cls, dict):
            if "name" not in cls:
                cls["name"] = "UnnamedClass"
            if "methods" not in cls:
                cls["methods"] = []
            if "bases" not in cls:
                cls["bases"] = []
            return cls
        else:
            return {
                "name": "GeneratedClass",
                "methods": [],
                "bases": [],
                "content": cls,
            }

    def get_transformation_status(self) -> Dict[str, Any]:
        """Get the current status of vocabulary transformation operations."""
        try:
            return {
                "transformer_status": "operational",
                "transformation_capabilities": [
                    "components_list_to_dict",
                    "component_structure_ensuring",
                    "workflow_metrics_enhancement",
                    "relationships_list_to_dict",
                    "class_structure_ensuring",
                ],
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get transformation status: {e}")
            return {"error": str(e)}
