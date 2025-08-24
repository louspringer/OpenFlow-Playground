#!/usr/bin/env python3
"""Test type-aware template system for generating linting-compliant code"""

import ast
import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Union


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def test_mypy_compliance(code: str) -> list[str]:
    """Test if code passes MyPy validation"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [
                "uv",
                "run",
                "mypy",
                "--show-error-codes",
                "--no-error-summary",
                temp_file,
            ],
            capture_output=True,
            text=True,
        )

        os.unlink(temp_file)

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"MyPy test failed: {e}"]


def test_black_compliance(code: str) -> bool:
    """Test if code passes Black formatting"""
    try:
        result = subprocess.run(
            ["uv", "run", "black", "--check", "-"],
            input=code,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def test_flake8_compliance(code: str) -> list[str]:
    """Test if code passes Flake8 validation"""
    try:
        result = subprocess.run(
            ["uv", "run", "flake8", "--select=F401,E302,E305,W291,W292", "-"],
            input=code,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


class TypeAwareTemplateEngine:
    """Template engine that generates type-annotated code"""

    def __init__(self):
        self.type_mappings = {
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "list": "List[Any]",
            "dict": "Dict[str, Any]",
            "any": "Any",
            "optional": "Optional[Any]",
        }

    def generate_function(
        self, name: str, params: list[dict[str, str]], return_type: str, body: str
    ) -> str:
        """Generate typed function"""
        param_str = ", ".join([f"{p['name']}: {p['type']}" for p in params])
        return f"""def {name}({param_str}) -> {return_type}:
    {body}"""

    def generate_class(self, name: str, methods: list[dict[str, Any]]) -> str:
        """Generate typed class"""
        class_code = f"""class {name}:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {{}}
"""

        for method in methods:
            param_str = ", ".join(
                [f"{p['name']}: {p['type']}" for p in method["params"]]
            )
            class_code += f"""
    def {method['name']}(self, {param_str}) -> {method['return_type']}:
        {method['body']}"""

        return class_code

    def generate_imports(self, imports: list[str]) -> str:
        """Generate typed imports"""
        return "from typing import " + ", ".join(imports) + "\n\n"


def generate_type_aware_code() -> str:
    """Generate code using type-aware templates"""
    engine = TypeAwareTemplateEngine()

    # Generate imports
    imports = engine.generate_imports(["Dict", "List", "Union", "Any", "Optional"])

    # Generate functions
    process_func = engine.generate_function(
        "process_data",
        [{"name": "data", "type": "List[Union[str, int]]"}],
        "Dict[str, Union[int, str]]",
        "result: Dict[str, Union[int, str]] = {}\n    for item in data:\n        if isinstance(item, str):\n            result[item] = len(item)\n        elif isinstance(item, int):\n            result[str(item)] = item\n    return result",
    )

    analyze_func = engine.generate_function(
        "analyze_results",
        [{"name": "results", "type": "Dict[str, Union[int, float]]"}],
        "float",
        "total: float = 0.0\n    count: int = 0\n    for key, value in results.items():\n        if isinstance(value, (int, float)):\n            total += value\n            count += 1\n    return total / count if count > 0 else 0.0",
    )

    # Generate class
    methods = [
        {
            "name": "process",
            "params": [{"name": "input_data", "type": "Any"}],
            "return_type": "Any",
            "body": "if input_data in self.cache:\n            return self.cache[input_data]\n        result: Any = self._transform(input_data)\n        self.cache[input_data] = result\n        return result",
        },
        {
            "name": "_transform",
            "params": [{"name": "data", "type": "Any"}],
            "return_type": "Any",
            "body": "if isinstance(data, list):\n            return [self._transform(item) for item in data]\n        elif isinstance(data, dict):\n            return {k: self._transform(v) for k, v in data.items()}\n        else:\n            return str(data)",
        },
    ]

    data_class = engine.generate_class("DataProcessor", methods)

    return imports + process_func + "\n\n" + analyze_func + "\n\n" + data_class


def main():
    """Test type-aware template system"""
    print("🧪 Testing Type-Aware Template System:")

    # Generate code with type-aware templates
    typed_code = generate_type_aware_code()

    print(f"Generated code length: {len(typed_code)} characters")

    # Test AST complexity
    ast_nodes = count_ast_nodes(typed_code)
    print(f"AST complexity: {ast_nodes} nodes")

    # Test MyPy compliance
    print("\n🔍 Testing MyPy compliance...")
    mypy_errors = test_mypy_compliance(typed_code)
    if mypy_errors:
        print(f"❌ MyPy found {len(mypy_errors)} errors:")
        for error in mypy_errors[:3]:
            print(f"  {error}")
    else:
        print("✅ MyPy compliance: PASSED")

    # Test Black compliance
    print("\n🔍 Testing Black compliance...")
    black_passed = test_black_compliance(typed_code)
    if black_passed:
        print("✅ Black compliance: PASSED")
    else:
        print("❌ Black compliance: FAILED")

    # Test Flake8 compliance
    print("\n🔍 Testing Flake8 compliance...")
    flake8_errors = test_flake8_compliance(typed_code)
    if flake8_errors:
        print(f"❌ Flake8 found {len(flake8_errors)} errors:")
        for error in flake8_errors[:3]:
            print(f"  {error}")
    else:
        print("✅ Flake8 compliance: PASSED")

    # Overall assessment
    print("\n📊 Overall Assessment:")
    total_errors = len(mypy_errors) + len(flake8_errors) + (0 if black_passed else 1)
    if total_errors == 0:
        print("🎉 SUCCESS: Type-aware templates generate linting-compliant code!")
        print("✅ Hypothesis 1 CONFIRMED: Types eliminate linting errors!")
    else:
        print(
            f"⚠️ WARNING: Type-aware templates still produce {total_errors} linting issues"
        )
        print("   Hypothesis 1 REJECTED: Types don't eliminate all errors")


if __name__ == "__main__":
    main()

"""Test type-aware template system for generating linting-compliant code"""

import ast
import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Union


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def test_mypy_compliance(code: str) -> list[str]:
    """Test if code passes MyPy validation"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [
                "uv",
                "run",
                "mypy",
                "--show-error-codes",
                "--no-error-summary",
                temp_file,
            ],
            capture_output=True,
            text=True,
        )

        os.unlink(temp_file)

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"MyPy test failed: {e}"]


def test_black_compliance(code: str) -> bool:
    """Test if code passes Black formatting"""
    try:
        result = subprocess.run(
            ["uv", "run", "black", "--check", "-"],
            input=code,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def test_flake8_compliance(code: str) -> list[str]:
    """Test if code passes Flake8 validation"""
    try:
        result = subprocess.run(
            ["uv", "run", "flake8", "--select=F401,E302,E305,W291,W292", "-"],
            input=code,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


class TypeAwareTemplateEngine:
    """Template engine that generates type-annotated code"""

    def __init__(self):
        self.type_mappings = {
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "list": "List[Any]",
            "dict": "Dict[str, Any]",
            "any": "Any",
            "optional": "Optional[Any]",
        }

    def generate_function(
        self, name: str, params: list[dict[str, str]], return_type: str, body: str
    ) -> str:
        """Generate typed function"""
        param_str = ", ".join([f"{p['name']}: {p['type']}" for p in params])
        return f"""def {name}({param_str}) -> {return_type}:
    {body}"""

    def generate_class(self, name: str, methods: list[dict[str, Any]]) -> str:
        """Generate typed class"""
        class_code = f"""class {name}:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {{}}
"""

        for method in methods:
            param_str = ", ".join(
                [f"{p['name']}: {p['type']}" for p in method["params"]]
            )
            class_code += f"""
    def {method['name']}(self, {param_str}) -> {method['return_type']}:
        {method['body']}"""

        return class_code

    def generate_imports(self, imports: list[str]) -> str:
        """Generate typed imports"""
        return "from typing import " + ", ".join(imports) + "\n\n"


def generate_type_aware_code() -> str:
    """Generate code using type-aware templates"""
    engine = TypeAwareTemplateEngine()

    # Generate imports
    imports = engine.generate_imports(["Dict", "List", "Union", "Any", "Optional"])

    # Generate functions
    process_func = engine.generate_function(
        "process_data",
        [{"name": "data", "type": "List[Union[str, int]]"}],
        "Dict[str, Union[int, str]]",
        "result: Dict[str, Union[int, str]] = {}\n    for item in data:\n        if isinstance(item, str):\n            result[item] = len(item)\n        elif isinstance(item, int):\n            result[str(item)] = item\n    return result",
    )

    analyze_func = engine.generate_function(
        "analyze_results",
        [{"name": "results", "type": "Dict[str, Union[int, float]]"}],
        "float",
        "total: float = 0.0\n    count: int = 0\n    for key, value in results.items():\n        if isinstance(value, (int, float)):\n            total += value\n            count += 1\n    return total / count if count > 0 else 0.0",
    )

    # Generate class
    methods = [
        {
            "name": "process",
            "params": [{"name": "input_data", "type": "Any"}],
            "return_type": "Any",
            "body": "if input_data in self.cache:\n            return self.cache[input_data]\n        result: Any = self._transform(input_data)\n        self.cache[input_data] = result\n        return result",
        },
        {
            "name": "_transform",
            "params": [{"name": "data", "type": "Any"}],
            "return_type": "Any",
            "body": "if isinstance(data, list):\n            return [self._transform(item) for item in data]\n        elif isinstance(data, dict):\n            return {k: self._transform(v) for k, v in data.items()}\n        else:\n            return str(data)",
        },
    ]

    data_class = engine.generate_class("DataProcessor", methods)

    return imports + process_func + "\n\n" + analyze_func + "\n\n" + data_class


def main():
    """Test type-aware template system"""
    print("🧪 Testing Type-Aware Template System:")

    # Generate code with type-aware templates
    typed_code = generate_type_aware_code()

    print(f"Generated code length: {len(typed_code)} characters")

    # Test AST complexity
    ast_nodes = count_ast_nodes(typed_code)
    print(f"AST complexity: {ast_nodes} nodes")

    # Test MyPy compliance
    print("\n🔍 Testing MyPy compliance...")
    mypy_errors = test_mypy_compliance(typed_code)
    if mypy_errors:
        print(f"❌ MyPy found {len(mypy_errors)} errors:")
        for error in mypy_errors[:3]:
            print(f"  {error}")
    else:
        print("✅ MyPy compliance: PASSED")

    # Test Black compliance
    print("\n🔍 Testing Black compliance...")
    black_passed = test_black_compliance(typed_code)
    if black_passed:
        print("✅ Black compliance: PASSED")
    else:
        print("❌ Black compliance: FAILED")

    # Test Flake8 compliance
    print("\n🔍 Testing Flake8 compliance...")
    flake8_errors = test_flake8_compliance(typed_code)
    if flake8_errors:
        print(f"❌ Flake8 found {len(flake8_errors)} errors:")
        for error in flake8_errors[:3]:
            print(f"  {error}")
    else:
        print("✅ Flake8 compliance: PASSED")

    # Overall assessment
    print("\n📊 Overall Assessment:")
    total_errors = len(mypy_errors) + len(flake8_errors) + (0 if black_passed else 1)
    if total_errors == 0:
        print("🎉 SUCCESS: Type-aware templates generate linting-compliant code!")
        print("✅ Hypothesis 1 CONFIRMED: Types eliminate linting errors!")
    else:
        print(
            f"⚠️ WARNING: Type-aware templates still produce {total_errors} linting issues"
        )
        print("   Hypothesis 1 REJECTED: Types don't eliminate all errors")


if __name__ == "__main__":
    main()
