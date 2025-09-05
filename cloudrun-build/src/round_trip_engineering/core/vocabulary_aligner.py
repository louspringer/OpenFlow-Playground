"""
Vocabulary Alignment Module

This module handles vocabulary alignment between different domains using ontological approaches.
It transforms data structures to ensure compatibility between reverse engineering and code generation.
"""

import logging
from typing import Dict, Any, Optional, Union, List, Set

from .vocabulary_mapping_manager import VocabularyMappingManager
from .vocabulary_analyzer import VocabularyAnalyzer
from .vocabulary_transformer import VocabularyTransformer
from .vocabulary_validator import VocabularyValidator

logger = logging.getLogger(__name__)


class VocabularyAligner:
    """Handles vocabulary alignment between different domains."""

    def __init__(self, ontology_bridge=None):
        """Initialize the vocabulary aligner with focused modules."""
        # Use the new focused modules
        self.vocabulary_mapping_manager = VocabularyMappingManager()
        self.vocabulary_analyzer = VocabularyAnalyzer()
        self.vocabulary_transformer = VocabularyTransformer()
        self.vocabulary_validator = VocabularyValidator()

        # Keep the old ontology bridge for backward compatibility
        self.ontology_bridge = ontology_bridge

        logger.info("✅ Vocabulary aligner initialized with focused modules")

    def align_vocabulary(self, extracted_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Align vocabulary between reverse engineering and code generation domains.

        Args:
            extracted_model: Model from reverse engineering domain

        Returns:
            Aligned model for code generation domain
        """
        try:
            logger.info("🔍 Starting ontological vocabulary alignment...")

            # Step 1: Analyze vocabulary mismatches
            mismatches = self.vocabulary_analyzer.analyze_vocabulary_mismatches(extracted_model)

            if mismatches:
                logger.info(f"⚠️ Found {len(mismatches)} vocabulary mismatches")
                for mismatch in mismatches:
                    logger.info(f"  - {mismatch['description']}")

                # Step 2: Apply vocabulary transformations
                aligned_model = self.vocabulary_transformer.apply_vocabulary_transformations(extracted_model, mismatches)

                # Step 3: Validate alignment
                validation_result = self.vocabulary_validator.validate_vocabulary_alignment(extracted_model, aligned_model)

                if validation_result["valid"]:
                    logger.info("✅ Ontological vocabulary alignment successful")
                else:
                    logger.warning("⚠️ Vocabulary alignment validation issues:")
                    for issue in validation_result.get("issues", []):
                        logger.warning(f"  - {issue}")
            else:
                logger.info("✅ No vocabulary mismatches found - model already aligned")
                aligned_model = extracted_model

            return aligned_model

        except Exception as e:
            logger.error(f"❌ Ontological vocabulary alignment failed: {e}")
            logger.info("🔄 Falling back to basic alignment...")
            return self.vocabulary_validator.basic_vocabulary_alignment(extracted_model)

    def get_alignment_status(self) -> Dict[str, Any]:
        """Get the overall status of vocabulary alignment operations."""
        try:
            return {
                "mapping_status": self.vocabulary_mapping_manager.get_mapping_status(),
                "analysis_status": self.vocabulary_analyzer.get_analysis_status(),
                "transformation_status": self.vocabulary_transformer.get_transformation_status(),
                "validation_status": self.vocabulary_validator.get_validation_status(),
                "overall_status": "healthy",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get alignment status: {e}")
            return {"error": str(e)}
