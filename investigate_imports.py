#!/usr/bin/env python3
"""
Investigate import discrepancy between original file and enhanced AST data.
"""

import ast
from src.round_trip_engineering.core.round_trip_system import RoundTripSystem


def analyze_original_imports():
    """Analyze imports in the original file."""
    print("🎯 ORIGINAL FILE IMPORTS:")
    with open("scripts/cli_parser.py", "r") as f:
        tree = ast.parse(f.read())
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        for imp in imports:
            print(f"  {type(imp).__name__}: {ast.unparse(imp)}")


def analyze_enhanced_ast_imports():
    """Analyze imports in the enhanced AST data."""
    print("\n🎯 ENHANCED AST DATA IMPORTS:")
    rts = RoundTripSystem()
    result = rts.analyze_and_generate_code("scripts/cli_parser.py", "python")

    enhanced_ast = result.get("extracted_model", {}).get("enhanced_ast_data", {})
    print(f"Enhanced AST keys: {list(enhanced_ast.keys()) if enhanced_ast else 'No enhanced_ast_data'}")

    if enhanced_ast:
        print("Enhanced AST content:")
        for key, value in enhanced_ast.items():
            print(f"  {key}: {type(value)} - {str(value)[:100]}...")


def analyze_components_imports():
    """Analyze imports in the components data."""
    print("\n🎯 COMPONENTS DATA IMPORTS:")
    rts = RoundTripSystem()
    result = rts.analyze_and_generate_code("scripts/cli_parser.py", "python")

    components = result.get("extracted_model", {}).get("components", [])
    print(f"Components type: {type(components)}")
    print(f"Components length: {len(components) if isinstance(components, list) else 'N/A'}")

    if isinstance(components, list) and components:
        component = components[0]
        print(f"First component keys: {list(component.keys())}")
        enhanced_ast = component.get("enhanced_ast", {})
        print(f"Component enhanced_ast keys: {list(enhanced_ast.keys()) if enhanced_ast else 'No enhanced_ast'}")


if __name__ == "__main__":
    analyze_original_imports()
    analyze_enhanced_ast_imports()
    analyze_components_imports()
