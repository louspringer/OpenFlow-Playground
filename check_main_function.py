#!/usr/bin/env python3
"""Check main function structure"""

import ast


def check_main_function(file_path: str):
    """Check the main function for nested functions"""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    # Find main function
    main_func = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            main_func = node
            break

    if not main_func:
        print("❌ Main function not found")
        return

    print(f"🔍 Main function structure:")
    print(f"  Body nodes: {len(main_func.body)}")
    print(f"  Node types: {[type(n).__name__ for n in main_func.body[:5]]}")

    # Look for nested functions
    nested_funcs = []
    for node in ast.walk(main_func):
        if isinstance(node, ast.FunctionDef) and node != main_func:
            nested_funcs.append(node)

    print(f"🔍 Nested functions found: {len(nested_funcs)}")
    for func in nested_funcs:
        print(f"    {func.name} at line {func.lineno}")
        print(f"      Body nodes: {len(func.body)}")
        print(f"      Node types: {[type(n).__name__ for n in func.body[:3]]}")


if __name__ == "__main__":
    check_main_function("src/ssh_key_management/ssh_key_manager.py")
