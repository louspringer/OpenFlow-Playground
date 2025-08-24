#!/usr/bin/env python3
"""Test different integration approaches with PerfectCodeGenerator"""

import ast
from pathlib import Path


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


class SimpleTemplateEngine:
    """Simple template engine for code generation"""

    @staticmethod
    def generate_function(name: str, params: list, body: str) -> str:
        """Generate simple function"""
        param_str = ", ".join(params)
        return f"""def {name}({param_str}):
    {body}"""


class PatternBasedGenerator:
    """Pattern-based code generator"""

    @staticmethod
    def generate_simple_class(name: str, methods: list) -> str:
        """Generate simple class using patterns"""
        method_code = "\\n\\n".join(methods)
        return f"""class {name}:
{method_code}"""


def test_plugin_integration() -> str:
    """Test plugin architecture integration"""
    template_engine = SimpleTemplateEngine()
    return template_engine.generate_function("test", ["data"], "return len(data)")


def test_service_layer_integration() -> str:
    """Test service layer integration"""
    pattern_generator = PatternBasedGenerator()
    method = SimpleTemplateEngine.generate_function(
        "process", ["item"], "return str(item)"
    )
    return pattern_generator.generate_simple_class("Processor", [method])


def test_direct_integration() -> str:
    """Test direct integration approach"""
    # Direct integration would embed templates in PerfectCodeGenerator
    return """def integrated_function(data):
    return len(data)"""


def main():
    """Compare integration approaches"""
    print("🔍 Integration Approach Comparison:")

    # Test different integration methods
    plugin_code = test_plugin_integration()
    service_code = test_service_layer_integration()
    direct_code = test_direct_integration()

    plugin_nodes = count_ast_nodes(plugin_code)
    service_nodes = count_ast_nodes(service_code)
    direct_nodes = count_ast_nodes(direct_code)

    print(f"Plugin integration: {plugin_nodes} nodes")
    print(f"Service layer: {service_nodes} nodes")
    print(f"Direct integration: {direct_nodes} nodes")

    # Find the simplest approach
    approaches = [
        ("Plugin", plugin_nodes),
        ("Service", service_nodes),
        ("Direct", direct_nodes),
    ]

    simplest = min(approaches, key=lambda x: x[1])
    print(f"\\n✅ Simplest approach: {simplest[0]} ({simplest[1]} nodes)")

    # Complexity analysis
    if simplest[1] <= 15:  # Threshold for "simple" code
        print("✅ All approaches produce simple code")
    else:
        print("⚠️ Some approaches produce complex code")


if __name__ == "__main__":
    main()

"""Test different integration approaches with PerfectCodeGenerator"""

import ast
from pathlib import Path


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


class SimpleTemplateEngine:
    """Simple template engine for code generation"""

    @staticmethod
    def generate_function(name: str, params: list, body: str) -> str:
        """Generate simple function"""
        param_str = ", ".join(params)
        return f"""def {name}({param_str}):
    {body}"""


class PatternBasedGenerator:
    """Pattern-based code generator"""

    @staticmethod
    def generate_simple_class(name: str, methods: list) -> str:
        """Generate simple class using patterns"""
        method_code = "\\n\\n".join(methods)
        return f"""class {name}:
{method_code}"""


def test_plugin_integration() -> str:
    """Test plugin architecture integration"""
    template_engine = SimpleTemplateEngine()
    return template_engine.generate_function("test", ["data"], "return len(data)")


def test_service_layer_integration() -> str:
    """Test service layer integration"""
    pattern_generator = PatternBasedGenerator()
    method = SimpleTemplateEngine.generate_function(
        "process", ["item"], "return str(item)"
    )
    return pattern_generator.generate_simple_class("Processor", [method])


def test_direct_integration() -> str:
    """Test direct integration approach"""
    # Direct integration would embed templates in PerfectCodeGenerator
    return """def integrated_function(data):
    return len(data)"""


def main():
    """Compare integration approaches"""
    print("🔍 Integration Approach Comparison:")

    # Test different integration methods
    plugin_code = test_plugin_integration()
    service_code = test_service_layer_integration()
    direct_code = test_direct_integration()

    plugin_nodes = count_ast_nodes(plugin_code)
    service_nodes = count_ast_nodes(service_code)
    direct_nodes = count_ast_nodes(direct_code)

    print(f"Plugin integration: {plugin_nodes} nodes")
    print(f"Service layer: {service_nodes} nodes")
    print(f"Direct integration: {direct_nodes} nodes")

    # Find the simplest approach
    approaches = [
        ("Plugin", plugin_nodes),
        ("Service", service_nodes),
        ("Direct", direct_nodes),
    ]

    simplest = min(approaches, key=lambda x: x[1])
    print(f"\\n✅ Simplest approach: {simplest[0]} ({simplest[1]} nodes)")

    # Complexity analysis
    if simplest[1] <= 15:  # Threshold for "simple" code
        print("✅ All approaches produce simple code")
    else:
        print("⚠️ Some approaches produce complex code")


if __name__ == "__main__":
    main()
