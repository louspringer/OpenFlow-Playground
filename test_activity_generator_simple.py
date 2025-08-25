#!/usr/bin/env python3
"""
Simple test script for Activity Model Generator components
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from activity_model_generator import PlantUMLGenerator, PyreverseAnalyzer

def test_plantuml_generation():
    """Test PlantUML generation without Pyreverse dependency"""
    print("🧪 Testing PlantUML generation...")
    
    # Test data
    class_structure = {
        "RoundTripSystem": {
            "name": "RoundTripSystem",
            "methods": [
                {"name": "create_model_from_design", "args": ["design_spec"], "docstring": "Create model from design"},
                {"name": "generate_code_from_model", "args": ["model_name"], "docstring": "Generate code from model"}
            ],
            "attributes": ["model_manager", "code_generator"],
            "docstring": "Main orchestrator for round-trip engineering"
        },
        "ModelManager": {
            "name": "ModelManager", 
            "methods": [
                {"name": "create_model", "args": ["design_spec"], "docstring": "Create a new model"}
            ],
            "attributes": ["models"],
            "docstring": "Manages model creation and storage"
        }
    }
    
    # Test PlantUML generation
    plantuml_gen = PlantUMLGenerator()
    
    try:
        # Generate activity diagram
        activity_path = "test_activity_diagram.png"
        plantuml_gen.generate_activity_diagram(class_structure, activity_path)
        print(f"✅ Activity diagram generated: {activity_path}")
        
        # Generate sequence diagram  
        sequence_path = "test_sequence_diagram.png"
        plantuml_gen.generate_sequence_diagram(class_structure, sequence_path)
        print(f"✅ Sequence diagram generated: {sequence_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ PlantUML generation failed: {e}")
        return False

def test_pyreverse_analysis():
    """Test Pyreverse analysis separately"""
    print("🧪 Testing Pyreverse analysis...")
    
    try:
        analyzer = PyreverseAnalyzer("test_pyreverse")
        results = analyzer.analyze_module("src/round_trip_engineering/core/round_trip_system.py")
        
        if results['analysis_successful']:
            print(f"✅ Pyreverse analysis successful")
            print(f"   - Generated {len(results['diagram_files'])} diagrams")
            print(f"   - Found {len(results['class_structure'])} classes")
            return True
        else:
            print(f"❌ Pyreverse analysis failed: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Pyreverse test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Activity Model Generator Components")
    print("=" * 50)
    
    # Test PlantUML generation
    plantuml_success = test_plantuml_generation()
    
    print()
    
    # Test Pyreverse analysis
    pyreverse_success = test_pyreverse_analysis()
    
    print()
    print("📊 Test Results Summary")
    print("=" * 30)
    print(f"PlantUML Generation: {'✅ PASS' if plantuml_success else '❌ FAIL'}")
    print(f"Pyreverse Analysis:  {'✅ PASS' if pyreverse_success else '❌ FAIL'}")
    
    if plantuml_success and pyreverse_success:
        print("\n🎉 All tests passed! Activity Model Generator is working.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
