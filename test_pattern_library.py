#!/usr/bin/env python3
"""Test pattern library approaches to code generation"""

import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


class PatternLibrary:
    """Simple pattern library for code generation"""

    @staticmethod
    def function_pattern(name: str, params: list, body: str) -> str:
        """Generate simple function"""
        param_str = ", ".join(params)
        return f"""def {name}({param_str}):
    {body}"""

    @staticmethod
    def class_pattern(name: str, methods: list) -> str:
        """Generate simple class"""
        method_code = "\\n\\n".join(methods)
        return f"""class {name}:
{method_code}"""

    @staticmethod
    def method_pattern(name: str, params: list, body: str) -> str:
        """Generate simple method"""
        param_str = ", ".join(params)
        return f"""    def {name}(self, {param_str}):
        {body}"""


def generate_with_patterns() -> str:
    """Generate code using pattern library"""
    patterns = PatternLibrary()

    # Generate simple function
    func = patterns.function_pattern("process", ["data"], "return len(data)")

    # Generate simple method
    method = patterns.method_pattern("transform", ["item"], "return str(item)")

    # Generate simple class
    cls = patterns.class_pattern("Processor", [method])

    return f"{func}\\n\\n{cls}"


def generate_without_patterns() -> str:
    """Generate same code without patterns"""
    return """def process(data):
    return len(data)


class Processor:
    def transform(self, item):
        return str(item)"""


def main():
    """Compare pattern library vs manual generation"""
    print("🔍 Pattern Library vs Manual Generation Comparison:")

    # Test pattern library
    pattern_code = generate_with_patterns()
    pattern_nodes = count_ast_nodes(pattern_code)

    # Test manual generation
    manual_code = generate_without_patterns()
    manual_nodes = count_ast_nodes(manual_code)

    print(f"Pattern library: {pattern_nodes} nodes")
    print(f"Manual generation: {manual_nodes} nodes")
    print(f"Difference: {pattern_nodes - manual_nodes} nodes")
    print(f"Complexity ratio: {pattern_nodes / manual_nodes:.2f}x")

    if pattern_nodes <= manual_nodes:
        print("✅ Pattern library maintains or reduces complexity")
    else:
        print("❌ Pattern library increases complexity")


if __name__ == "__main__":
    main()


import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


class PatternLibrary:
    """Simple pattern library for code generation"""

    @staticmethod
    def function_pattern(name: str, params: list, body: str) -> str:
        """Generate simple function"""
        param_str = ", ".join(params)
        return f"""def {name}({param_str}):
    {body}"""

    @staticmethod
    def class_pattern(name: str, methods: list) -> str:
        """Generate simple class"""
        method_code = "\\n\\n".join(methods)
        return f"""class {name}:
{method_code}"""

    @staticmethod
    def method_pattern(name: str, params: list, body: str) -> str:
        """Generate simple method"""
        param_str = ", ".join(params)
        return f"""    def {name}(self, {param_str}):
        {body}"""


def generate_with_patterns() -> str:
    """Generate code using pattern library"""
    patterns = PatternLibrary()

    # Generate simple function
    func = patterns.function_pattern("process", ["data"], "return len(data)")

    # Generate simple method
    method = patterns.method_pattern("transform", ["item"], "return str(item)")

    # Generate simple class
    cls = patterns.class_pattern("Processor", [method])

    return f"{func}\\n\\n{cls}"


def generate_without_patterns() -> str:
    """Generate same code without patterns"""
    return """def process(data):
    return len(data)


class Processor:
    def transform(self, item):
        return str(item)"""


def main():
    """Compare pattern library vs manual generation"""
    print("🔍 Pattern Library vs Manual Generation Comparison:")

    # Test pattern library
    pattern_code = generate_with_patterns()
    pattern_nodes = count_ast_nodes(pattern_code)

    # Test manual generation
    manual_code = generate_without_patterns()
    manual_nodes = count_ast_nodes(manual_code)

    print(f"Pattern library: {pattern_nodes} nodes")
    print(f"Manual generation: {manual_nodes} nodes")
    print(f"Difference: {pattern_nodes - manual_nodes} nodes")
    print(f"Complexity ratio: {pattern_nodes / manual_nodes:.2f}x")

    if pattern_nodes <= manual_nodes:
        print("✅ Pattern library maintains or reduces complexity")
    else:
        print("❌ Pattern library increases complexity")


if __name__ == "__main__":
    main()
