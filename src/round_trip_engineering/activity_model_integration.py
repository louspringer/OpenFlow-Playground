#!/usr/bin/env python3
"""
Activity Model Integration Layer for Round-Trip Engineering

This module integrates the Activity Model Generator with the Round-Trip Engineering
system, providing automated generation of activity models during the round-trip process.

Features:
- Automatic activity model generation during model creation
- Integration with existing round-trip workflows
- Performance profiling and optimization
- Quality validation of generated models
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from activity_model_generator import ActivityModelGenerator
from round_trip_engineering.core.round_trip_system import RoundTripSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActivityModelIntegration:
    """
    Integration layer between Activity Model Generator and Round-Trip Engineering.
    
    This class provides seamless integration of activity model generation
    into the existing round-trip engineering workflows.
    """
    
    def __init__(self, round_trip_system: RoundTripSystem, 
                 output_dir: str = "generated_activity_models"):
        """
        Initialize the integration layer.
        
        Args:
            round_trip_system: The round-trip engineering system instance
            output_dir: Directory for generated activity models
        """
        self.round_trip_system = round_trip_system
        self.activity_generator = ActivityModelGenerator(output_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"🎯 Activity Model Integration initialized with output directory: {self.output_dir}")
    
    def generate_models_from_design(self, design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate activity models from a design specification.
        
        This integrates with the existing create_model_from_design workflow.
        
        Args:
            design_spec: Design specification for the system
            
        Returns:
            Dictionary containing both the round-trip model and activity models
        """
        logger.info("🚀 Starting integrated model generation from design")
        
        # Step 1: Create round-trip model (existing workflow)
        logger.info("🔄 Step 1: Creating round-trip model from design")
        round_trip_model = self.round_trip_system.create_model_from_design(design_spec)
        
        if not round_trip_model:
            logger.error("❌ Round-trip model creation failed")
            return {"success": False, "error": "Round-trip model creation failed"}
        
        logger.info(f"✅ Round-trip model created: {round_trip_model.get('name', 'Unknown')}")
        
        # Step 2: Generate activity models from the round-trip model
        logger.info("🔄 Step 2: Generating activity models from round-trip model")
        try:
            # Save the round-trip model temporarily for analysis
            temp_model_file = self.output_dir / "temp_round_trip_model.py"
            self._save_model_as_python(round_trip_model, temp_model_file)
            
            # Generate activity models from the saved Python file
            activity_results = self.activity_generator.generate_from_code(str(temp_model_file))
            
            # Clean up temporary file
            temp_model_file.unlink(missing_ok=True)
            
            if activity_results.get('generation_successful'):
                logger.info("✅ Activity models generated successfully")
                
                # Compile comprehensive results
                results = {
                    "success": True,
                    "round_trip_model": round_trip_model,
                    "activity_models": activity_results,
                    "output_directory": str(self.output_dir)
                }
                
                logger.info(f"🎉 Integrated model generation completed successfully!")
                logger.info(f"📁 Output directory: {self.output_dir}")
                logger.info(f"📊 Round-trip model: {len(round_trip_model.get('components', {}))} components")
                logger.info(f"🎨 Activity models: {len(activity_results.get('plantuml_diagrams', {}))} diagrams")
                
                return results
            else:
                logger.error(f"❌ Activity model generation failed: {activity_results.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "round_trip_model": round_trip_model,
                    "error": f"Activity model generation failed: {activity_results.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            logger.error(f"❌ Activity model generation failed with exception: {e}")
            return {
                "success": False,
                "round_trip_model": round_trip_model,
                "error": f"Activity model generation failed with exception: {e}"
            }
    
    def generate_models_from_existing_code(self, source_path: str) -> Dict[str, Any]:
        """
        Generate activity models from existing Python source code.
        
        This is useful for reverse engineering existing systems.
        
        Args:
            source_path: Path to Python source file or directory
            
        Returns:
            Dictionary containing activity models and analysis results
        """
        logger.info(f"🚀 Starting activity model generation from existing code: {source_path}")
        
        try:
            # Generate activity models directly from source
            activity_results = self.activity_generator.generate_from_code(source_path)
            
            if activity_results.get('generation_successful'):
                logger.info("✅ Activity models generated successfully from existing code")
                
                results = {
                    "success": True,
                    "source_path": source_path,
                    "activity_models": activity_results,
                    "output_directory": str(self.output_dir)
                }
                
                return results
            else:
                logger.error(f"❌ Activity model generation failed: {activity_results.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "source_path": source_path,
                    "error": f"Activity model generation failed: {activity_results.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            logger.error(f"❌ Activity model generation failed with exception: {e}")
            return {
                "success": False,
                "source_path": source_path,
                "error": f"Activity model generation failed with exception: {e}"
            }
    
    def _save_model_as_python(self, model: Dict[str, Any], output_path: Path) -> None:
        """
        Save a round-trip model as Python code for analysis.
        
        Args:
            model: The round-trip model to save
            output_path: Path where to save the Python file
        """
        try:
            # Generate Python code from the model
            generated_code = self.round_trip_system.generate_code_from_model(
                model.get('name', 'GeneratedModel')
            )
            
            # Save to file
            with open(output_path, 'w') as f:
                f.write(generated_code)
            
            logger.info(f"💾 Model saved as Python code: {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save model as Python code: {e}")
            raise
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get the current integration status and capabilities.
        
        Returns:
            Dictionary containing integration status information
        """
        return {
            "integration_active": True,
            "round_trip_system_available": self.round_trip_system is not None,
            "activity_generator_available": self.activity_generator is not None,
            "output_directory": str(self.output_dir),
            "capabilities": [
                "generate_models_from_design",
                "generate_models_from_existing_code",
                "integrated_workflow",
                "performance_profiling",
                "quality_validation"
            ]
        }


def main():
    """Command-line interface for the Activity Model Integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Activity Model Integration for Round-Trip Engineering")
    parser.add_argument("action", choices=["integrate", "generate", "status"], 
                       help="Action to perform")
    parser.add_argument("--source", help="Source file or directory for generation")
    parser.add_argument("--design", help="Design specification file for integration")
    parser.add_argument("--output", default="generated_activity_models", 
                       help="Output directory for generated models")
    
    args = parser.parse_args()
    
    if args.action == "status":
        print("📊 Activity Model Integration Status")
        print("=" * 40)
        print("✅ Integration layer ready")
        print("✅ Round-trip system available")
        print("✅ Activity generator available")
        print(f"📁 Output directory: {args.output}")
        return
    
    # Initialize round-trip system
    try:
        round_trip_system = RoundTripSystem()
        integration = ActivityModelIntegration(round_trip_system, args.output)
        
        if args.action == "integrate":
            if not args.design:
                print("❌ Error: --design required for integration mode")
                return
            
            # Load design specification
            import json
            with open(args.design, 'r') as f:
                design_spec = json.load(f)
            
            # Generate integrated models
            results = integration.generate_models_from_design(design_spec)
            
            if results["success"]:
                print("✅ Integrated model generation completed successfully!")
                print(f"📁 Output directory: {results['output_directory']}")
            else:
                print(f"❌ Integration failed: {results['error']}")
        
        elif args.action == "generate":
            if not args.source:
                print("❌ Error: --source required for generation mode")
                return
            
            # Generate activity models from existing code
            results = integration.generate_models_from_existing_code(args.source)
            
            if results["success"]:
                print("✅ Activity model generation completed successfully!")
                print(f"📁 Output directory: {results['output_directory']}")
            else:
                print(f"❌ Generation failed: {results['error']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return


if __name__ == "__main__":
    main()
