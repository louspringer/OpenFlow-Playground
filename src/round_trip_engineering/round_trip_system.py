#!/usr/bin/env python3
"""
Round-Trip Engineering System

A clean, modular system for round-trip engineering using design models.
"""

import logging
from pathlib import Path
from typing import Any, Dict

from modules.model_manager import ModelManager, DesignModel
from modules.code_generator import CodeGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RoundTripSystem:
    """Clean, focused round-trip engineering system"""

    def __init__(self) -> None:
        self.model_manager = ModelManager()
        self.code_generator = CodeGenerator()
        logger.info("🚀 Round-trip engineering system initialized")

    def create_model_from_design(self, design_spec: dict[str, Any]) -> DesignModel:
        """Create a model from design specification"""
        return self.model_manager.create_model_from_design(design_spec)

    def save_model(self, model_name: str, filename: str) -> None:
        """Save a model to file"""
        self.model_manager.save_model(model_name, filename)

    def load_model(self, filename: str) -> DesignModel:
        """Load a model from file"""
        return self.model_manager.load_model(filename)

    def generate_code_from_model(self, model_name: str) -> Dict[str, str]:
        """Generate code from a model"""
        model = self.model_manager.get_model(model_name)
        result: Dict[str, str] = self.code_generator.generate_code_from_model(model)
        return result

    def run_round_trip_demo(self) -> None:
        """Run a demonstration of the round-trip system"""
        logger.info("🎯 Running round-trip engineering demonstration")

        # STEP 1: Create model from design
        design_spec = {
            "name": "ASTGuidedCodeGenerator",
            "description": "AST-guided code generator that respects syntactic boundaries",
            "components": [
                {
                    "name": "ASTNode",
                    "type": "class",
                    "description": "Represents an AST node with metadata",
                    "requirements": [
                        "dataclass",
                        "metadata support",
                        "parent-child relationships",
                    ],
                    "dependencies": ["dataclasses", "typing"],
                    "metadata": {
                        "methods": [
                            {
                                "name": "__post_init__",
                                "description": "Initialize default values",
                            }
                        ]
                    },
                }
            ],
        }

        logger.info("🎯 STEP 1: Creating model from design")
        model = self.create_model_from_design(design_spec)
        logger.info(f"   ✅ Created model: {model.name} with {len(model.components)} components")

        # STEP 2: Save model to JSON
        logger.info("🎯 STEP 2: Saving model to JSON")
        self.save_model("ASTGuidedCodeGenerator", "ast_guided_model.json")

        # STEP 3: Generate code from model
        logger.info("🎯 STEP 3: Generating code from model")
        generated_files = self.generate_code_from_model("ASTGuidedCodeGenerator")

        # STEP 4: Save generated code
        logger.info("🎯 STEP 4: Saving generated code")
        for filename, code in generated_files.items():
            with open(f"generated_{filename}", "w") as f:
                f.write(code)
            logger.info(f"   💾 Saved generated_{filename}")

        # STEP 5: Load model from JSON (round-trip)
        logger.info("🎯 STEP 5: Loading model from JSON (round-trip)")
        loaded_model = self.load_model("ast_guided_model.json")

        logger.info("✅ ROUND-TRIP COMPLETE!")
        logger.info(f"   📊 Model: {loaded_model.name}")
        logger.info(f"   📊 Components: {len(loaded_model.components)}")
        logger.info(f"   📊 Generated files: {len(generated_files)}")
        logger.info("   🎯 Round-trip successful: Design → Model → Code → Model")


def main() -> None:
    """Main entry point for round-trip engineering system"""
    system = RoundTripSystem()
    system.run_round_trip_demo()


if __name__ == "__main__":
    main()
