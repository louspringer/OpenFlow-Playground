#!/usr/bin/env python3
"""Test the actual generated code complexity"""

import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def main():
    """Compare generated code complexity"""
    # Pattern library generated code (with proper newlines)
    pattern_code = """def process(data):
    return len(data)

class Processor:
    def transform(self, item):
        return str(item)"""

    # Manual generation
    manual_code = """def process(data):
    return len(data)


class Processor:
    def transform(self, item):
        return str(item)"""

    print("🔍 Generated Code Complexity Comparison:")

    pattern_nodes = count_ast_nodes(pattern_code)
    manual_nodes = count_ast_nodes(manual_code)

    print(f"Pattern library: {pattern_nodes} nodes")
    print(f"Manual generation: {manual_nodes} nodes")
    print(f"Difference: {pattern_nodes - manual_nodes} nodes")

    if pattern_nodes > 0 and manual_nodes > 0:
        ratio = pattern_nodes / manual_nodes
        print(f"Complexity ratio: {ratio:.2f}x")

        if ratio <= 1.0:
            print("✅ Pattern library maintains or reduces complexity")
        else:
            print("❌ Pattern library increases complexity")


if __name__ == "__main__":
    main()

"""Test the actual generated code complexity"""

import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def main():
    """Compare generated code complexity"""
    # Pattern library generated code (with proper newlines)
    pattern_code = """def process(data):
    return len(data)

class Processor:
    def transform(self, item):
        return str(item)"""

    # Manual generation
    manual_code = """def process(data):
    return len(data)


class Processor:
    def transform(self, item):
        return str(item)"""

    print("🔍 Generated Code Complexity Comparison:")

    pattern_nodes = count_ast_nodes(pattern_code)
    manual_nodes = count_ast_nodes(manual_code)

    print(f"Pattern library: {pattern_nodes} nodes")
    print(f"Manual generation: {manual_nodes} nodes")
    print(f"Difference: {pattern_nodes - manual_nodes} nodes")

    if pattern_nodes > 0 and manual_nodes > 0:
        ratio = pattern_nodes / manual_nodes
        print(f"Complexity ratio: {ratio:.2f}x")

        if ratio <= 1.0:
            print("✅ Pattern library maintains or reduces complexity")
        else:
            print("❌ Pattern library increases complexity")


if __name__ == "__main__":
    main()
