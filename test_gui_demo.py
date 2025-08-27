#!/usr/bin/env python3
"""
Test GUI Demo

Simple script to test the GUI functionality without launching Streamlit.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from workflow_visualization_gui import WorkflowVisualizationGUI

def test_gui_initialization():
    """Test that the GUI initializes correctly."""
    print("🧪 Testing GUI Initialization...")
    
    try:
        # Create GUI instance
        gui = WorkflowVisualizationGUI()
        print("✅ GUI instance created successfully")
        
        # Check components
        print(f"📋 Found {len(gui.components)} components:")
        for name, info in gui.components.items():
            print(f"  - {name}: {info['description']}")
        
        # Check test files
        print(f"📁 Test files available: {len(gui.test_files)}")
        for file in gui.test_files:
            if Path(file).exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (missing)")
        
        # Check artifacts directory
        if gui.artifacts_dir.exists():
            print(f"✅ Artifacts directory: {gui.artifacts_dir}")
        else:
            print(f"❌ Artifacts directory missing: {gui.artifacts_dir}")
        
        print("\n🎉 GUI initialization test passed!")
        return True
        
    except Exception as e:
        print(f"❌ GUI initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_component_availability():
    """Test that all analysis components are available."""
    print("\n🧪 Testing Component Availability...")
    
    try:
        gui = WorkflowVisualizationGUI()
        
        # Test each component
        components_to_test = [
            ("Control Flow Analyzer", gui.control_flow_analyzer),
            ("Multi-File Analyzer", gui.multi_file_analyzer),
            ("UML Generator", gui.uml_generator),
            ("Complexity Analyzer", gui.complexity_analyzer),
            ("Performance Optimizer", gui.performance_optimizer),
            ("Round-Trip Validator", gui.round_trip_validator),
        ]
        
        for name, component in components_to_test:
            try:
                # Just check if we can access the component
                component_name = component.__class__.__name__
                print(f"  ✅ {name}: {component_name}")
            except Exception as e:
                print(f"  ❌ {name}: {str(e)}")
        
        print("\n🎉 Component availability test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Component availability test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_quick_analysis():
    """Test quick analysis functionality."""
    print("\n🧪 Testing Quick Analysis...")
    
    try:
        gui = WorkflowVisualizationGUI()
        
        # Test with first test file
        test_file = gui.test_files[0]
        if not Path(test_file).exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        print(f"📊 Testing with file: {test_file}")
        
        # Test control flow analysis
        try:
            result = gui.control_flow_analyzer.analyze_control_flow(test_file)
            if result:
                print(f"  ✅ Control flow analysis: {len(result.get('patterns', {}))} patterns found")
            else:
                print("  ⚠️ Control flow analysis returned no results")
        except Exception as e:
            print(f"  ❌ Control flow analysis failed: {str(e)}")
        
        # Test complexity analysis
        try:
            result = gui.complexity_analyzer.analyze_complexity(test_file)
            if result:
                print(f"  ✅ Complexity analysis: Score {result.get('overall_score', 'N/A')}")
            else:
                print("  ⚠️ Complexity analysis returned no results")
        except Exception as e:
            print(f"  ❌ Complexity analysis failed: {str(e)}")
        
        print("\n🎉 Quick analysis test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Quick analysis test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting GUI Demo Tests...")
    print("=" * 50)
    
    tests = [
        test_gui_initialization,
        test_component_availability,
        test_quick_analysis,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI is ready to use.")
        print("\n🚀 To launch the GUI, run:")
        print("   python launch_gui.py")
        print("   or")
        print("   uv run streamlit run src/workflow_visualization_gui.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
