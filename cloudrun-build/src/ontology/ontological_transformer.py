#!/usr/bin/env python3
"""
Ontological Transformer
Uses formal ontology to transform data between reverse engineering and code generation formats
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology.code_generation_ontology import (
    CodeGenerationOntology,
    ContextType,
    FormatType,
    RelationshipType,
)


class OntologicalTransformer:
    """Transforms data between contexts using formal ontological rules"""

    def __init__(self, ontology_file: Optional[str] = None):
        """Initialize with ontology"""
        if ontology_file and os.path.exists(ontology_file):
            self.ontology = CodeGenerationOntology.load_from_file(ontology_file)
        else:
            self.ontology = CodeGenerationOntology()

        self.transformation_cache = {}

    def transform_reverse_engineering_to_code_generation(self, reverse_engineering_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform reverse engineering output to code generation input"""
        print("🔄 Transforming reverse engineering → code generation using ontology")

        # Validate the transformation is possible
        validation = self.ontology.validate_transformation(reverse_engineering_data, FormatType.DICT)

        if not validation["valid"]:
            raise ValueError(f"Transformation validation failed: {validation['errors']}")

        print(f"  ✅ Validation passed: {validation['transformation_path']}")

        # Apply ontological transformation
        transformed_data = self._apply_ontological_transformation(
            reverse_engineering_data,
            ContextType.REVERSE_ENGINEERING,
            ContextType.CODE_GENERATION,
        )

        return transformed_data

    def _apply_ontological_transformation(self, data: Any, from_context: ContextType, to_context: ContextType) -> Any:
        """Apply ontological transformation between contexts"""

        if isinstance(data, dict):
            transformed = {}
            for key, value in data.items():
                # Transform the key using vocabulary mapping
                new_key = self._map_vocabulary_key(key, from_context, to_context)

                # Transform the value recursively
                if isinstance(value, (dict, list)):
                    transformed_value = self._apply_ontological_transformation(value, from_context, to_context)
                else:
                    transformed_value = value

                transformed[new_key] = transformed_value

            return transformed

        elif isinstance(data, list):
            # Handle list transformations based on ontological rules
            if self._should_transform_list_to_dict(data, from_context, to_context):
                return self._transform_list_to_dict_by_name(data)
            else:
                return [self._apply_ontological_transformation(item, from_context, to_context) for item in data]

        else:
            return data

    def _map_vocabulary_key(self, key: str, from_context: ContextType, to_context: ContextType) -> str:
        """Map vocabulary keys between contexts using ontology"""

        # Get concepts from both contexts
        from_concepts = self.ontology.get_concepts_by_context(from_context)
        to_concepts = self.ontology.get_concepts_by_context(to_context)

        # Look for vocabulary mapping in the ontology
        for from_concept in from_concepts:
            if key in from_concept.constraints.get("naming", ""):
                # Find corresponding concept in target context
                for to_concept in to_concepts:
                    if from_concept.name in to_concept.get_relationships(RelationshipType.TRANSFORMS_FROM) or to_concept.name in from_concept.get_relationships(RelationshipType.TRANSFORMS_TO):
                        # Apply vocabulary mapping
                        return self._get_mapped_key(key, from_concept, to_concept)

        # Default: keep the same key if no mapping found
        return key

    def _get_mapped_key(self, key: str, from_concept, to_concept) -> str:
        """Get the mapped key based on ontological concepts"""

        # Apply vocabulary mapping rules
        vocabulary_mapping = {
            "components": "target_components",
            "methods": "generation_methods",
            "dependencies": "import_requirements",
            "requirements": "implementation_requirements",
            "metadata": "generation_metadata",
            "type": "entity_type",
            "description": "entity_description",
            "parameters": "method_parameters",
            "return_type": "method_return_type",
        }

        return vocabulary_mapping.get(key, key)

    def _should_transform_list_to_dict(self, data: List, from_context: ContextType, to_context: ContextType) -> bool:
        """Determine if a list should be transformed to dict based on ontology"""

        # Check if this is a list of components that should be transformed
        if from_context == ContextType.REVERSE_ENGINEERING and to_context == ContextType.CODE_GENERATION and data and isinstance(data[0], dict) and "name" in data[0]:
            # Validate against ontological constraints
            validation = self.ontology.validate_transformation(data, FormatType.DICT)
            return validation["valid"]

        return False

    def _transform_list_to_dict_by_name(self, components_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Transform list of components to dict keyed by name"""
        components_dict = {}

        for component in components_list:
            if isinstance(component, dict) and "name" in component:
                name = component["name"]
                if name in components_dict:
                    print(f"  ⚠️  Warning: Duplicate component name '{name}' - merging properties")
                    # Merge properties for duplicate names
                    existing = components_dict[name]
                    if isinstance(existing, dict) and isinstance(component, dict):
                        existing.update(component)
                else:
                    components_dict[name] = component
            else:
                # Handle components without names
                key = f"component_{len(components_dict)}"
                components_dict[key] = component

        return components_dict

    def transform_model_file(self, input_file: str, output_file: str) -> bool:
        """Transform a model file from reverse engineering to code generation format"""
        print(f"🔄 Transforming model file: {input_file} → {output_file}")

        try:
            # Load input model
            with open(input_file, "r") as f:
                input_data = json.load(f)

            # Transform using ontology
            transformed_data = self.transform_reverse_engineering_to_code_generation(input_data)

            # Save transformed model
            with open(output_file, "w") as f:
                json.dump(transformed_data, f, indent=2)

            print(f"  ✅ Transformation successful: {output_file}")
            return True

        except Exception as e:
            print(f"  ❌ Transformation failed: {e}")
            return False

    def validate_model_file(self, model_file: str, expected_context: ContextType) -> Dict[str, Any]:
        """Validate a model file against ontological constraints"""
        print(f"🔍 Validating model file: {model_file}")

        try:
            with open(model_file, "r") as f:
                model_data = json.load(f)

            # Determine the format based on context
            expected_format = FormatType.DICT if expected_context == ContextType.CODE_GENERATION else FormatType.LIST

            # Validate using ontology
            validation = self.ontology.validate_transformation(model_data, expected_format)

            print(f"  Validation: {'✅ PASS' if validation['valid'] else '❌ FAIL'}")
            if validation["errors"]:
                print(f"    Errors: {validation['errors']}")
            if validation["warnings"]:
                print(f"    Warnings: {validation['warnings']}")

            return validation

        except Exception as e:
            print(f"  ❌ Validation failed: {e}")
            return {"valid": False, "errors": [str(e)], "warnings": []}

    def generate_transformation_report(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Generate a comprehensive transformation report"""
        print(f"📊 Generating transformation report...")

        report = {
            "transformation": {
                "input_file": input_file,
                "output_file": output_file,
                "timestamp": (str(Path(input_file).stat().st_mtime) if os.path.exists(input_file) else "unknown"),
            },
            "validation": {},
            "statistics": {},
            "recommendations": [],
        }

        # Validate input file
        if os.path.exists(input_file):
            input_validation = self.validate_model_file(input_file, ContextType.REVERSE_ENGINEERING)
            report["validation"]["input"] = input_validation

        # Validate output file
        if os.path.exists(output_file):
            output_validation = self.validate_model_file(output_file, ContextType.CODE_GENERATION)
            report["validation"]["output"] = output_validation

        # Generate statistics
        if os.path.exists(input_file) and os.path.exists(output_file):
            with open(input_file, "r") as f:
                input_data = json.load(f)
            with open(output_file, "r") as f:
                output_data = json.load(f)

            report["statistics"] = {
                "input_size": len(json.dumps(input_data)),
                "output_size": len(json.dumps(output_data)),
                "input_components": len(input_data.get("components", [])),
                "output_components": len(output_data.get("target_components", {})),
                "compression_ratio": (len(json.dumps(output_data)) / len(json.dumps(input_data)) if input_data else 0),
            }

        # Generate recommendations
        if "input" in report["validation"] and not report["validation"]["input"]["valid"]:
            report["recommendations"].append("Fix input validation errors before transformation")

        if "output" in report["validation"] and not report["validation"]["output"]["valid"]:
            report["recommendations"].append("Review transformation logic - output validation failed")

        if report["statistics"].get("compression_ratio", 1) > 1.5:
            report["recommendations"].append("Output significantly larger than input - review transformation efficiency")

        return report


def main():
    """Test the ontological transformer"""
    print("🔧 Testing Ontological Transformer")
    print("=" * 50)

    # Initialize transformer
    transformer = OntologicalTransformer()

    # Test with the enhanced code quality model
    input_file = "enhanced_code_quality_model.json"
    output_file = "enhanced_code_quality_model_ontologically_transformed.json"

    if os.path.exists(input_file):
        print(f"\n📁 Input file: {input_file}")

        # Validate input
        input_validation = transformer.validate_model_file(input_file, ContextType.REVERSE_ENGINEERING)

        # Transform the model
        success = transformer.transform_model_file(input_file, output_file)

        if success:
            # Validate output
            output_validation = transformer.validate_model_file(output_file, ContextType.CODE_GENERATION)

            # Generate report
            report = transformer.generate_transformation_report(input_file, output_file)

            print(f"\n📊 TRANSFORMATION REPORT:")
            print(f"  Input validation: {'✅ PASS' if input_validation['valid'] else '❌ FAIL'}")
            print(f"  Output validation: {'✅ PASS' if output_validation['valid'] else '❌ FAIL'}")
            print(f"  Input components: {report['statistics'].get('input_components', 'N/A')}")
            print(f"  Output components: {report['statistics'].get('output_components', 'N/A')}")

            if report["recommendations"]:
                print(f"\n💡 Recommendations:")
                for rec in report["recommendations"]:
                    print(f"    • {rec}")

            # Save report
            report_file = "transformation_report.json"
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Report saved to: {report_file}")

    else:
        print(f"❌ Input file not found: {input_file}")
        print("   Please ensure enhanced_code_quality_model.json exists")

    print(f"\n🎉 Ontological transformer ready!")
    print(f"📋 Capabilities:")
    print(f"  • Transform reverse engineering → code generation")
    print(f"  • Validate against ontological constraints")
    print(f"  • Generate transformation reports")
    print(f"  • Eliminate vocabulary ambiguity")


if __name__ == "__main__":
    main()
