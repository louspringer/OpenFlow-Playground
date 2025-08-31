#!/usr/bin/env python3
"""
Code Generation Orchestrator
Focused on orchestrating the code generation workflow between models and code.
"""

import logging
from typing import Dict, Any, List

from .model_manager import ModelManager
from .vocabulary_aligner import VocabularyAligner
from ..generators.code_generator import CodeGenerator
from ..cleaners.duplication_cleaner import DuplicationCleaner
from ..profiling.profiler import Profiler
from ..logging_config import log_data_transformation

logger = logging.getLogger(__name__)


class CodeGenerationOrchestrator:
    """Orchestrates the code generation workflow between models and code."""

    def __init__(self):
        """Initialize the code generation orchestrator."""
        self.model_manager = ModelManager()
        self.vocabulary_aligner = VocabularyAligner()
        self.code_generator = CodeGenerator()
        self.duplication_cleaner = DuplicationCleaner()
        self.profiler = Profiler()

        logger.info("✅ Code generation orchestrator initialized")

    def generate_code_from_extracted_model(
        self, extracted_model: Dict[str, Any], target_language: str = "python"
    ) -> str:
        """
        Generate code from an extracted model using ontological vocabulary alignment.

        Args:
            extracted_model: The extracted model from reverse engineering
            target_language: Target programming language

        Returns:
            Generated code as string
        """
        try:
            # Start profiling
            self.profiler.start_profiling("generate_code_from_extracted_model")

            # REAL profiling: track function entry
            logger.info(
                f"🚀 ENTERING generate_code_from_extracted_model with {target_language}"
            )
            logger.info(f"📊 Input model keys: {list(extracted_model.keys())}")

            logger.info(f"🎯 Generating {target_language} code from extracted model...")

            # Step 1: Align vocabulary between domains
            logger.info("🔄 Step 1: Vocabulary alignment")
            aligned_model = self.vocabulary_aligner.align_vocabulary(extracted_model)

            # Log vocabulary alignment results
            log_data_transformation(
                logger,
                "vocabulary_alignment",
                extracted_model.get("components", []),
                aligned_model.get("components", {}),
                {"target_language": target_language},
            )

            # Step 2: Generate code using aligned model
            logger.info("🔄 Step 2: Code generation")
            generated_code = self.code_generator.generate(
                aligned_model, target_language
            )

            # Log code generation results
            log_data_transformation(
                logger,
                "code_generation",
                aligned_model,
                generated_code,
                {
                    "code_length": len(generated_code),
                    "target_language": target_language,
                },
            )

            # Step 3: Clean up any duplications
            logger.info("🔄 Step 3: Duplication cleaning")
            cleaned_code = self.duplication_cleaner.clean_code(generated_code)

            # Log duplication cleaning results
            log_data_transformation(
                logger,
                "duplication_cleaning",
                generated_code,
                cleaned_code,
                {
                    "original_length": len(generated_code),
                    "cleaned_length": len(cleaned_code),
                    "target_language": target_language,
                },
            )

            # Stop profiling
            self.profiler.stop_profiling()

            logger.info("✅ Generated python code successfully")
            return cleaned_code

        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            self.profiler.stop_profiling()
            raise

    def get_generation_metrics(self) -> Dict[str, Any]:
        """Get metrics about code generation performance."""
        try:
            return {
                "profiler_status": "operational",  # Simplified for now
                "vocabulary_alignment_status": "operational",
                "code_generation_status": "operational",
                "duplication_cleaning_status": "operational",
            }
        except Exception as e:
            logger.error(f"❌ Failed to get generation metrics: {e}")
            return {"error": str(e)}
