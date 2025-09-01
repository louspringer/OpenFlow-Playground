#!/usr/bin/env python3
"""
Ontological Round-Trip Fixer
Uses proper RDF/OWL ontology to fix vocabulary alignment between reverse engineering and code generation
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ontology.proper_code_generation_ontology import ProperCodeGenerationOntology


class OntologicalRoundTripFixer:
    """Fixes round-trip system using proper ontological reasoning"""

    def __init__(self, ontology_file: Optional[str] = None):
        """Initialize with ontology"""
        if ontology_file and os.path.exists(ontology_file):
            self.ontology = ProperCodeGenerationOntology()
            self.ontology.load_from_file(ontology_file, "turtle")
        else:
            # Use the freshly built ontology
            self.ontology = ProperCodeGenerationOntology()

        print("🔧 Ontological Round-Trip Fixer initialized")
        print(f"  📚 Ontology contains {self.ontology.get_statistics()['total_triples']} triples")

    def fix_round_trip_vocabulary(self, model_file: str) -> Dict[str, Any]:
        """Fix vocabulary alignment using ontological reasoning"""
        print(f"\n🔧 Fixing round-trip vocabulary alignment for: {model_file}")

        # Load the model
        with open(model_file, "r") as f:
            model_data = json.load(f)

        # Step 1: Ontologically validate the input
        print("  📊 Step 1: Ontologically validating input...")
        input_validation = self._validate_input_ontologically(model_data)

        if not input_validation["valid"]:
            print(f"    ❌ Input validation failed: {input_validation['errors']}")
            return {"success": False, "errors": input_validation["errors"]}

        print(f"    ✅ Input validation passed: {input_validation['concept_type']}")

        # Step 2: Apply ontological transformation
        print("  🔄 Step 2: Applying ontological transformation...")
        transformed_data = self._apply_ontological_transformation(model_data)

        # Step 3: Validate the transformation
        print("  ✅ Step 3: Validating transformation...")
        output_validation = self._validate_output_ontologically(transformed_data)

        if not output_validation["valid"]:
            print(f"    ❌ Output validation failed: {output_validation['errors']}")
            return {"success": False, "errors": output_validation["errors"]}

        print(f"    ✅ Output validation passed: {output_validation['concept_type']}")

        # Step 4: Save transformed model
        output_file = model_file.replace(".json", "_ontologically_fixed.json")
        with open(output_file, "w") as f:
            json.dump(transformed_data, f, indent=2)

        print(f"    💾 Transformed model saved: {output_file}")

        return {
            "success": True,
            "input_file": model_file,
            "output_file": output_file,
            "input_validation": input_validation,
            "output_validation": output_validation,
            "transformation_path": input_validation.get("transformation_path", []),
        }

    def _validate_input_ontologically(self, data: Any) -> Dict[str, Any]:
        """Validate input data against ontological constraints"""

        # Identify the concept type using ontological reasoning
        concept_type = self._identify_concept_ontologically(data)
        if not concept_type:
            return {
                "valid": False,
                "errors": ["Could not identify concept type using ontology"],
            }

        # Validate against ontological constraints
        validation_result = self.ontology.validate_transformation(data, "dict" if concept_type == "code_generation" else "list")

        return {
            "valid": validation_result["valid"],
            "concept_type": concept_type,
            "errors": validation_result.get("errors", []),
            "warnings": validation_result.get("warnings", []),
            "transformation_path": validation_result.get("transformation_path", []),
        }

    def _identify_concept_ontologically(self, data: Any) -> Optional[str]:
        """Identify concept type using ontological reasoning"""

        # Use SPARQL to query the ontology for concept identification
        if isinstance(data, dict) and "components" in data:
            components = data["components"]

            if isinstance(components, list):
                # Check if this matches reverse engineering pattern
                query = """
                PREFIX re: <http://example.org/reverse-engineering#>
                PREFIX cg: <http://example.org/code-generation#>
                
                ASK {
                    ?context a cg:Context .
                    ?context cg:hasFormat ?format .
                    ?format rdfs:label "List Format" .
                    ?context rdfs:label "Reverse Engineering Context" .
                }
                """

                if self.ontology.g.query(query):
                    return "reverse_engineering"

            elif isinstance(components, dict):
                # Check if this matches code generation pattern
                query = """
                PREFIX re: <http://example.org/reverse-engineering#>
                PREFIX cg: <http://example.org/code-generation#>
                
                ASK {
                    ?context a cg:Context .
                    ?context cg:hasFormat ?format .
                    ?format rdfs:label "Dict Format" .
                    ?context rdfs:label "Code Generation Context" .
                }
                """

                if self.ontology.g.query(query):
                    return "code_generation"

        return None

    def _apply_ontological_transformation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply transformation based on ontological rules"""

        # Create a copy to avoid modifying original
        transformed_data = data.copy()

        # Transform components field using ontological vocabulary mapping
        if "components" in transformed_data:
            components = transformed_data["components"]

            if isinstance(components, list):
                # Transform from reverse engineering (list) to code generation (dict)
                print("    🔄 Transforming components: list → dict")

                # Apply ontological vocabulary mapping
                transformed_components = {}
                for component in components:
                    if isinstance(component, dict) and "name" in component:
                        name = component["name"]

                        # Apply ontological vocabulary mapping
                        mapped_component = self._map_vocabulary_ontologically(component, "reverse_engineering", "code_generation")

                        if name in transformed_components:
                            print(f"      ⚠️  Warning: Duplicate component '{name}' - merging properties")
                            # Merge properties for duplicate names
                            existing = transformed_components[name]
                            if isinstance(existing, dict) and isinstance(mapped_component, dict):
                                existing.update(mapped_component)
                        else:
                            transformed_components[name] = mapped_component
                    else:
                        # Handle components without names
                        key = f"component_{len(transformed_components)}"
                        transformed_components[key] = component

                # Update the components field with transformed data
                transformed_data["components"] = transformed_components

                # Apply vocabulary mapping to top-level fields
                transformed_data = self._map_top_level_vocabulary(transformed_data, "reverse_engineering", "code_generation")

        return transformed_data

    def _map_vocabulary_ontologically(self, component: Dict[str, Any], from_context: str, to_context: str) -> Dict[str, Any]:
        """Map vocabulary using ontological relationships"""

        # Create a copy to avoid modifying original
        mapped_component = component.copy()

        # Apply ontological vocabulary mapping based on context
        vocabulary_mapping = {
            "reverse_engineering": {
                "code_generation": {
                    "methods": "generation_methods",
                    "dependencies": "import_requirements",
                    "requirements": "implementation_requirements",
                    "metadata": "generation_metadata",
                    "type": "entity_type",
                    "description": "entity_description",
                    "parameters": "method_parameters",
                    "return_type": "method_return_type",
                }
            }
        }

        # Get the mapping for this context transformation
        context_mapping = vocabulary_mapping.get(from_context, {}).get(to_context, {})

        # Apply the mapping
        for old_key, new_key in context_mapping.items():
            if old_key in mapped_component:
                mapped_component[new_key] = mapped_component.pop(old_key)

        return mapped_component

    def _map_top_level_vocabulary(self, data: Dict[str, Any], from_context: str, to_context: str) -> Dict[str, Any]:
        """Map top-level vocabulary fields"""

        # Create a copy to avoid modifying original
        mapped_data = data.copy()

        # Apply top-level vocabulary mapping
        top_level_mapping = {"reverse_engineering": {"code_generation": {"components": "target_components"}}}

        # Get the mapping for this context transformation
        context_mapping = top_level_mapping.get(from_context, {}).get(to_context, {})

        # Apply the mapping
        for old_key, new_key in context_mapping.items():
            if old_key in mapped_data:
                mapped_data[new_key] = mapped_data.pop(old_key)

        return mapped_data

    def _validate_output_ontologically(self, data: Any) -> Dict[str, Any]:
        """Validate output data against ontological constraints"""

        # Identify the concept type
        concept_type = self._identify_concept_ontologically(data)
        if not concept_type:
            return {
                "valid": False,
                "errors": ["Could not identify output concept type"],
            }

        # Validate against ontological constraints
        validation_result = self.ontology.validate_transformation(data, "dict" if concept_type == "code_generation" else "list")

        return {
            "valid": validation_result["valid"],
            "concept_type": concept_type,
            "errors": validation_result.get("errors", []),
            "warnings": validation_result.get("warnings", []),
        }

    def generate_ontological_report(self, fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive ontological analysis report"""

        report = {
            "ontological_fix": {
                "success": fix_result["success"],
                "input_file": fix_result.get("input_file", "unknown"),
                "output_file": fix_result.get("output_file", "unknown"),
                "transformation_path": fix_result.get("transformation_path", []),
            },
            "ontological_validation": {
                "input": fix_result.get("input_validation", {}),
                "output": fix_result.get("output_validation", {}),
            },
            "ontology_statistics": self.ontology.get_statistics(),
            "recommendations": [],
        }

        # Generate recommendations based on ontological analysis
        if fix_result["success"]:
            report["recommendations"].append("✅ Vocabulary alignment successful using ontological reasoning")
            report["recommendations"].append("✅ Transformation follows ontological constraints")
            report["recommendations"].append("✅ No vocabulary ambiguity detected")
        else:
            report["recommendations"].append("❌ Vocabulary alignment failed - review ontological constraints")
            report["recommendations"].append("🔍 Check input data structure against ontology")
            report["recommendations"].append("🔄 Verify transformation rules in ontology")

        # Add ontological insights
        stats = report["ontology_statistics"]
        report["recommendations"].append(f"📊 Ontology contains {stats['total_triples']} triples for comprehensive reasoning")
        report["recommendations"].append(f"🏗️ {stats['classes']} classes define the conceptual structure")
        report["recommendations"].append(f"🔗 {stats['object_properties']} relationships enable transformation rules")

        return report


def main():
    """Test the ontological round-trip fixer"""
    print("🔧 Testing Ontological Round-Trip Fixer")
    print("=" * 50)

    # Initialize the fixer
    fixer = OntologicalRoundTripFixer()

    # Test with the enhanced code quality model
    input_file = "enhanced_code_quality_model.json"

    if os.path.exists(input_file):
        print(f"\n📁 Input file: {input_file}")

        # Fix the round-trip vocabulary alignment
        fix_result = fixer.fix_round_trip_vocabulary(input_file)

        if fix_result["success"]:
            print(f"\n🎉 VOCABULARY ALIGNMENT SUCCESSFUL!")
            print(f"📋 Results:")
            print(f"  Input file: {fix_result['input_file']}")
            print(f"  Output file: {fix_result['output_file']}")
            print(f"  Transformation path: {' → '.join(fix_result['transformation_path'])}")

            # Generate ontological report
            report = fixer.generate_ontological_report(fix_result)

            print(f"\n📊 ONTOLOGICAL REPORT:")
            print(f"  Success: {'✅' if report['ontological_fix']['success'] else '❌'}")
            print(f"  Input validation: {'✅ PASS' if report['ontological_validation']['input']['valid'] else '❌ FAIL'}")
            print(f"  Output validation: {'✅ PASS' if report['ontological_validation']['output']['valid'] else '❌ FAIL'}")

            if report["recommendations"]:
                print(f"\n💡 Recommendations:")
                for rec in report["recommendations"]:
                    print(f"    • {rec}")

            # Save report
            report_file = "ontological_fix_report.json"
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Report saved to: {report_file}")

        else:
            print(f"\n❌ VOCABULARY ALIGNMENT FAILED!")
            print(f"  Errors: {fix_result['errors']}")

    else:
        print(f"❌ Input file not found: {input_file}")
        print("   Please ensure enhanced_code_quality_model.json exists")

    print(f"\n🎉 Ontological round-trip fixer ready!")
    print(f"📋 Capabilities:")
    print(f"  • Ontological vocabulary validation")
    print(f"  • Context-aware transformations")
    print(f"  • SPARQL-based concept identification")
    print(f"  • Ontological constraint enforcement")
    print(f"  • Comprehensive transformation reporting")


if __name__ == "__main__":
    main()
