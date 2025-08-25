"""
Core Round-Trip Engineering System

This module orchestrates the round-trip engineering process between models and code.
It coordinates vocabulary alignment, code generation, and cleaning operations.
"""

import logging
import sys
import cProfile
import pstats
from typing import Dict, Any
from pathlib import Path

# Add the ontology bridge to the path
ontology_bridge_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(ontology_bridge_path))

try:
    from simple_ontology_bridge import SimpleOntologyBridge

    ONTOLOGY_BRIDGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Ontology bridge not available: {e}")
    ONTOLOGY_BRIDGE_AVAILABLE = False

from .model_manager import ModelManager
from .vocabulary_aligner import VocabularyAligner
from ..generators.code_generator import CodeGenerator
from ..cleaners.duplication_cleaner import DuplicationCleaner
from ..logging_config import log_data_transformation, log_error_with_context

logger = logging.getLogger(__name__)


class RoundTripSystem:
    """Main orchestrator for round-trip engineering operations."""

    def __init__(self):
        """Initialize the round-trip system with all components."""
        # Initialize profiling
        self.profiler = cProfile.Profile()
        self.profiler_stats = None

        # Initialize ontology bridge for vocabulary alignment
        if ONTOLOGY_BRIDGE_AVAILABLE:
            try:
                self.ontology_bridge = SimpleOntologyBridge()
                logger.info(
                    "✅ Ontology vocabulary bridge initialized for vocabulary alignment"
                )
            except Exception as e:
                logger.warning(f"Warning: Failed to initialize ontology bridge: {e}")
                self.ontology_bridge = None
        else:
            self.ontology_bridge = None

        # Initialize core components
        self.model_manager = ModelManager()
        self.vocabulary_aligner = VocabularyAligner(self.ontology_bridge)
        self.code_generator = CodeGenerator()
        self.duplication_cleaner = DuplicationCleaner()

        logger.info("✅ Round-trip system initialized with all components")

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
            self.profiler.enable()

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
            logger.info(
                f"🚀 CALLING duplication_cleaner.clean_code with {len(generated_code)} chars"
            )
            cleaned_code = self.duplication_cleaner.clean_code(generated_code)
            logger.info(
                f"✅ duplication_cleaner.clean_code COMPLETED, returned {len(cleaned_code)} chars"
            )

            # Log duplication cleaning results
            original_lines = len(generated_code.split("\n"))
            cleaned_lines = len(cleaned_code.split("\n"))
            log_data_transformation(
                logger,
                "duplication_cleaning",
                generated_code,
                cleaned_code,
                {"original_lines": original_lines, "cleaned_lines": cleaned_lines},
            )

            logger.info(f"✅ Generated {target_language} code successfully")
            logger.info(f"🏁 EXITING generate_code_from_extracted_model - SUCCESS")
            return cleaned_code

        except Exception as e:
            log_error_with_context(
                logger,
                e,
                "generate_code_from_extracted_model",
                {
                    "target_language": target_language,
                    "extracted_model_keys": list(extracted_model.keys()),
                },
            )
            raise
        finally:
            # Stop profiling and collect stats
            self.profiler.disable()
            self.profiler_stats = pstats.Stats(self.profiler)

    def create_model_from_design(self, design_spec: Dict[str, Any]) -> Any:
        """Create a model from design specification."""
        try:
            result = self.model_manager.create_model_from_design(design_spec)
            return result
        except Exception as e:
            log_error_with_context(
                logger,
                e,
                "create_model_from_design",
                {"design_spec_keys": list(design_spec.keys())},
            )
            raise

    def save_model(self, model_name: str, file_path: str) -> None:
        """Save a model to file."""
        try:
            self.model_manager.save_model(model_name, file_path)
        except Exception as e:
            log_error_with_context(
                logger,
                e,
                "save_model",
                {"model_name": model_name, "file_path": file_path},
            )
            raise

    def load_model(self, file_path: str) -> Any:
        """Load a model from file."""
        try:
            result = self.model_manager.load_model(file_path)
            return result
        except Exception as e:
            log_error_with_context(logger, e, "load_model", {"file_path": file_path})
            raise

    def generate_code_from_model(self, model_name: str) -> Dict[str, str]:
        """Generate code from a stored model."""
        try:
            model = self.model_manager.get_model(model_name)
            if not model:
                raise ValueError(f"Model {model_name} not found")

            result = self.code_generator.generate_from_model(model)
            return result
        except Exception as e:
            log_error_with_context(
                logger, e, "generate_code_from_model", {"model_name": model_name}
            )
            raise

    def get_profiling_stats(self) -> pstats.Stats:
        """Get profiling statistics."""
        return self.profiler_stats

    def print_profiling_summary(
        self, sort_by: str = "cumulative", limit: int = 10
    ) -> None:
        """Print profiling summary sorted by specified criteria."""
        if self.profiler_stats:
            self.profiler_stats.sort_stats(sort_by)
            self.profiler_stats.print_stats(limit)
        else:
            logger.warning("No profiling data available")
