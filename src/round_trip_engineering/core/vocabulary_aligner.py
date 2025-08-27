"""
Vocabulary Alignment Module

This module handles vocabulary alignment between different domains using ontological approaches.
It transforms data structures to ensure compatibility between reverse engineering and code generation.
"""

import logging
from typing import Dict, Any, Optional, Union, List

logger = logging.getLogger(__name__)


class VocabularyAligner:
    """Handles vocabulary alignment between different domains."""

    def __init__(self, ontology_bridge=None):
        """Initialize the vocabulary aligner."""
        self.ontology_bridge = ontology_bridge
        logger.info("✅ Vocabulary aligner initialized")

    def align_vocabulary(self, extracted_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Align vocabulary between reverse engineering and code generation domains.

        Args:
            extracted_model: Model from reverse engineering domain

        Returns:
            Aligned model for code generation domain
        """
        try:
            # Use ontology bridge for vocabulary alignment if available
            if self.ontology_bridge and "components" in extracted_model:
                return self._align_vocabulary_ontologically(extracted_model)
            else:
                # Fallback to manual alignment
                return self._align_vocabulary_manually(extracted_model)

        except Exception as e:
            logger.error(f"❌ Vocabulary alignment failed: {e}")
            logger.info("🔄 Falling back to manual alignment...")
            return self._align_vocabulary_manually(extracted_model)

    def _align_vocabulary_ontologically(
        self, extracted_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Align vocabulary using ontological approach.

        Args:
            extracted_model: Model from reverse engineering domain

        Returns:
            Aligned model for code generation domain
        """
        try:
            logger.info("🔍 Using ontology bridge for vocabulary alignment...")

            # Analyze vocabulary alignment
            analysis = self.ontology_bridge.analyze_vocabulary_mismatch(
                extracted_model,
                {"expected": "dict_format"},  # Code generation expects dict
            )

            if not analysis["valid"]:
                logger.warning("⚠️ Vocabulary alignment issues detected:")
                for mismatch in analysis.get("vocabulary_mismatches", []):
                    logger.warning(f"  - {mismatch['description']}")

                # Apply recommended transformations
                for transform in analysis.get("recommended_transformations", []):
                    if transform["type"] == "list_to_dict":
                        logger.info(f"🔄 Applying {transform['description']}...")
                        extracted_model[
                            "components"
                        ] = self.ontology_bridge.resolve_vocabulary_mismatch(
                            extracted_model["components"], "dict"
                        )
                        break

            # Validate transformation integrity
            if "components" in extracted_model and isinstance(
                extracted_model["components"], dict
            ):
                validation = self.ontology_bridge.validate_transformation(
                    extracted_model.get(
                        "original_components", extracted_model["components"]
                    ),
                    extracted_model["components"],
                    "dict",
                )

                if not validation["valid"]:
                    logger.warning("⚠️ Transformation validation failed:")
                    for issue in validation.get("issues", []):
                        logger.warning(f"  - {issue}")
                else:
                    logger.info(
                        "✅ Vocabulary alignment and transformation validation successful"
                    )

            return extracted_model

        except Exception as e:
            logger.error(f"❌ Ontological vocabulary alignment failed: {e}")
            raise

    def _align_vocabulary_manually(
        self, extracted_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Manual fallback for vocabulary alignment when ontology bridge is unavailable.

        Args:
            extracted_model: Model from reverse engineering domain

        Returns:
            Aligned model for code generation domain
        """
        logger.info("🔄 Using manual vocabulary alignment...")

        # Handle components field alignment
        if "components" in extracted_model:
            components = extracted_model["components"]

            # Convert list to dict if needed
            if isinstance(components, list):
                logger.info("📝 Converting components from list to dict format...")
                components_dict = {}
                for component in components:
                    if isinstance(component, dict) and "name" in component:
                        components_dict[component["name"]] = component
                    else:
                        logger.warning(
                            f"⚠️ Skipping component without name: {component}"
                        )

                extracted_model["components"] = components_dict
                logger.info(f"✅ Converted {len(components)} components to dict format")

            # Keep dict format if that's what we already have (code generation expects dict)
            elif isinstance(components, dict):
                logger.info(
                    "📝 Components already in dict format - keeping for code generation"
                )
                # No conversion needed - code generation expects dict format
                logger.info(
                    f"✅ Components already in correct dict format with {len(components)} items"
                )

        return extracted_model
