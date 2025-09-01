#!/usr/bin/env python3
"""Check AST structure for recursive descent"""

import ast


def analyze_ast_structure(file_path: str):
    """Analyze AST structure recursively"""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    print(f"🔍 AST Structure for {file_path}:")
    print(f"  Top-level functions: {len([n for n in tree.body if isinstance(n, ast.FunctionDef)])}")
    print(f"  Top-level classes: {len([n for n in tree.body if isinstance(n, ast.ClassDef)])}")

    print("🔍 Top-level functions:")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            print(f"    {node.name}")
            # Check for nested functions
            nested_funcs = [n for n in ast.walk(node) if isinstance(n, ast.FunctionDef) and n != node]
            if nested_funcs:
                print(f"      Nested functions: {[f.name for f in nested_funcs]}")

    print("🔍 Top-level classes:")
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            print(f"    {node.name}")
            # Check for methods
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            if methods:
                print(f"      Methods: {[m.name for m in methods]}")


if __name__ == "__main__":
    analyze_ast_structure("src/ssh_key_management/ssh_key_manager.py")
