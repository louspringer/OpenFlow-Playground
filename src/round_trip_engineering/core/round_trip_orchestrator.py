#!/usr/bin/env python3
"""
Round Trip Orchestrator
Orchestrates round-trip engineering operations using focused modules
"""

import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from ..models.design_model_manager import DesignModelManager
from ..models.extracted_model_processor import ExtractedModelProcessor
from ..reverse_engineering.enhanced_reverse_engineer import EnhancedReverseEngineer
from ..alignment.vocabulary_aligner import VocabularyAligner
from ..generators.design_model_generator import DesignModelGenerator


logger = logging.getLogger(__name__)


class RoundTripOrchestrator(BaseReflectiveModule):
    """Orchestrates round-trip engineering operations using focused modules"""

    def __init__(self) -> None:
        super().__init__()

        # Initialize focused modules
        self.design_model_manager = DesignModelManager()
        self.extracted_model_processor = ExtractedModelProcessor()
        self.enhanced_reverse_engineer = EnhancedReverseEngineer()
        self.vocabulary_aligner = VocabularyAligner()
        self.design_model_generator = DesignModelGenerator()

        logger.info("✅ Round-trip orchestrator initialized with focused modules")

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities"""
        return {
            "round_trip_engineering": [
                "create_model_from_design",
                "generate_code_from_model",
                "reverse_engineer_code",
                "round_trip_validation",
            ],
            "model_management": ["manage_design_models", "process_extracted_models"],
            "vocabulary_alignment": ["align_vocabulary", "manage_domain_vocabularies"],
        }

    def create_model_from_design(self, design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a model directly from design specification (forward engineering)"""
        logger.info(f"🎯 Creating model from design: {design_spec.get('name', 'Unknown')}")

        try:
            # Use design model manager
            design_model = self.design_model_manager.create_model_from_design(design_spec)

            # Save the model
            self.design_model_manager.save_model(design_model.name)

            result = {
                "success": True,
                "model_name": design_model.name,
                "component_count": len(design_model.components),
                "message": f"✅ Created design model with {len(design_model.components)} components",
            }

            logger.info(f"✅ Successfully created design model: {design_model.name}")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to create design model: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Failed to create design model: {e}",
            }

    def generate_code_from_model(self, model_name: str) -> Dict[str, Any]:
        """Generate code from a design model (forward engineering)"""
        logger.info(f"🎯 Generating code from model: {model_name}")

        try:
            # Get the model
            model = self.design_model_manager.get_model(model_name)
            if not model:
                raise ValueError(f"Model {model_name} not found")

            # Convert model components to the format expected by design model generator
            components = []
            for component in model.components:
                components.append(
                    {
                        "name": component.name,
                        "type": component.type,
                        "description": component.description,
                        "requirements": component.requirements,
                        "dependencies": component.dependencies,
                        "metadata": component.metadata,
                    }
                )

            # Generate code using design model generator
            generated_files = self.design_model_generator.generate_code_from_model(components)

            result = {
                "success": True,
                "model_name": model_name,
                "generated_files": list(generated_files.keys()),
                "file_count": len(generated_files),
                "message": f"✅ Generated {len(generated_files)} files from model {model_name}",
            }

            logger.info(f"✅ Successfully generated code from model: {model_name}")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to generate code from model: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Failed to generate code from model: {e}",
            }

    def reverse_engineer_code(self, file_path: str) -> Dict[str, Any]:
        """Reverse engineer code to extract a model"""
        logger.info(f"🎯 Reverse engineering code: {file_path}")

        try:
            # Use enhanced reverse engineer
            extracted_model = self.enhanced_reverse_engineer.parse_python_file(file_path)

            # Process the extracted model
            processed_model = self.extracted_model_processor.process_extracted_model(extracted_model)

            result = {
                "success": True,
                "file_path": file_path,
                "model_name": processed_model["name"],
                "class_count": len(processed_model.get("classes", {})),
                "function_count": len(processed_model.get("functions", {})),
                "import_count": len(processed_model.get("imports", [])),
                "message": f"✅ Reverse engineered {file_path} successfully",
            }

            logger.info(f"✅ Successfully reverse engineered: {file_path}")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to reverse engineer {file_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Failed to reverse engineer {file_path}: {e}",
            }

    def round_trip_validation(self, source_file: str, target_file: str) -> Dict[str, Any]:
        """Validate round-trip engineering by comparing source and generated files"""
        logger.info(f"🎯 Validating round-trip: {source_file} -> {target_file}")

        try:
            # Reverse engineer source file
            source_model = self.reverse_engineer_code(source_file)
            if not source_model["success"]:
                raise ValueError(f"Failed to reverse engineer source: {source_model['error']}")

            # Reverse engineer target file
            target_model = self.reverse_engineer_code(target_file)
            if not target_model["success"]:
                raise ValueError(f"Failed to reverse engineer target: {target_model['error']}")

            # Compare models
            comparison = self._compare_models(source_model, target_model)

            result = {
                "success": True,
                "source_file": source_file,
                "target_file": target_file,
                "comparison": comparison,
                "message": "✅ Round-trip validation completed",
            }

            logger.info(f"✅ Round-trip validation completed: {source_file} -> {target_file}")
            return result

        except Exception as e:
            logger.error(f"❌ Round-trip validation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Round-trip validation failed: {e}",
            }

    def _compare_models(self, source_model: Dict[str, Any], target_model: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two models for round-trip validation"""
        comparison = {
            "structural_similarity": 0.0,
            "class_preservation": 0.0,
            "function_preservation": 0.0,
            "import_preservation": 0.0,
            "overall_score": 0.0,
            "details": {},
        }

        # Compare class preservation
        source_classes = set(source_model.get("classes", {}).keys())
        target_classes = set(target_model.get("classes", {}).keys())

        if source_classes:
            class_preservation = len(source_classes.intersection(target_classes)) / len(source_classes)
            comparison["class_preservation"] = class_preservation

        # Compare function preservation
        source_functions = set(source_model.get("functions", {}).keys())
        target_functions = set(target_model.get("functions", {}).keys())

        if source_functions:
            function_preservation = len(source_functions.intersection(target_functions)) / len(source_functions)
            comparison["function_preservation"] = function_preservation

        # Compare import preservation
        source_imports = set(str(imp) for imp in source_model.get("imports", []))
        target_imports = set(str(imp) for imp in target_model.get("imports", []))

        if source_imports:
            import_preservation = len(source_imports.intersection(target_imports)) / len(source_imports)
            comparison["import_preservation"] = import_preservation

        # Calculate overall score
        scores = [
            comparison["class_preservation"],
            comparison["function_preservation"],
            comparison["import_preservation"],
        ]
        comparison["overall_score"] = sum(scores) / len(scores)

        # Add detailed comparison
        comparison["details"] = {
            "source_classes": list(source_classes),
            "target_classes": list(target_classes),
            "source_functions": list(source_functions),
            "target_functions": list(target_functions),
            "source_imports": list(source_imports),
            "target_imports": list(target_imports),
        }

        return comparison

    def get_system_status(self) -> Dict[str, Any]:
        """Get the status of all modules"""
        return {
            "orchestrator": {"status": "operational", "module_count": 5},
            "modules": {
                "design_model_manager": self.design_model_manager.is_healthy(),
                "extracted_model_processor": self.extracted_model_processor.is_healthy(),
                "enhanced_reverse_engineer": self.enhanced_reverse_engineer.is_healthy(),
                "vocabulary_aligner": self.vocabulary_aligner.is_healthy(),
                "design_model_generator": self.design_model_generator.is_healthy(),
            },
        }

    def get_available_models(self) -> List[str]:
        """Get list of available design models"""
        return self.design_model_manager.list_models()

    def get_parsed_files(self) -> List[str]:
        """Get list of parsed files"""
        return self.enhanced_reverse_engineer.list_parsed_files()

    def clear_all_data(self) -> None:
        """Clear all data from all modules"""
        self.design_model_manager.design_models.clear()
        self.extracted_model_processor.clear_processed_models()
        self.enhanced_reverse_engineer.clear_parsed_files()
        logger.info("✅ Cleared all data from all modules")
