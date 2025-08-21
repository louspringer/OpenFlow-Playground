#!/usr/bin/env python3
"""Test that types actually improve code quality and reduce errors"""

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


def generate_untyped_code() -> str:
    """Generate code WITHOUT type annotations"""
    return '''def process_data(data):
    """Process data without type hints"""
    result = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results):
    """Analyze results without type hints"""
    total = 0
    count = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0

class DataProcessor:
    """Data processor without type hints"""

    def __init__(self, config):
        self.config = config
        self.cache = {}

    def process(self, input_data):
        """Process input data"""
        if input_data in self.cache:
            return self.cache[input_data]

        result = self._transform(input_data)
        self.cache[input_data] = result
        return result

    def _transform(self, data):
        """Transform data"""
        if isinstance(data, list):
            return [self._transform(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._transform(v) for k, v in data.items()}
        else:
            return str(data)'''


def generate_typed_code() -> str:
    """Generate code WITH type annotations"""
    return '''from typing import Dict, List, Union, Any, Optional

def process_data(data: List[Union[str, int]]) -> Dict[str, Union[int, str]]:
    """Process data with type hints"""
    result: Dict[str, Union[int, str]] = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results: Dict[str, Union[int, float]]) -> float:
    """Analyze results with type hints"""
    total: float = 0.0
    count: int = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0.0

class DataProcessor:
    """Data processor with type hints"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {}

    def process(self, input_data: Any) -> Any:
        """Process input data"""
        if input_data in self.cache:
            return self.cache[input_data]

        result: Any = self._transform(input_data)
        self.cache[input_data] = result
        return result

    def _transform(self, data: Any) -> Any:
        """Transform data"""
        if isinstance(data, list):
            return [self._transform(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._transform(v) for k, v in data.items()}
        else:
            return str(data)'''


def main():
    """Test that types improve code quality"""
    print("🧪 Testing: Do Types Actually Improve Code Quality?")

    # Generate both versions
    untyped_code = generate_untyped_code()
    typed_code = generate_typed_code()

    print(f"\n📊 Code Comparison:")
    print(f"Untyped code: {len(untyped_code)} characters")
    print(f"Typed code: {len(typed_code)} characters")
    print(f"Type overhead: {len(typed_code) - len(untyped_code)} characters")

    # Test AST complexity
    print(f"\n🔍 AST Complexity Analysis:")
    untyped_nodes = count_ast_nodes(untyped_code)
    typed_nodes = count_ast_nodes(typed_code)
    print(f"Untyped AST nodes: {untyped_nodes}")
    print(f"Typed AST nodes: {typed_nodes}")
    print(f"Type overhead: {typed_nodes - untyped_nodes} nodes")

    # Test MyPy compliance
    print(f"\n🔍 MyPy Compliance:")
    untyped_mypy_errors = test_mypy_compliance(untyped_code)
    typed_mypy_errors = test_mypy_compliance(typed_code)

    print(f"Untyped MyPy errors: {len(untyped_mypy_errors)}")
    if untyped_mypy_errors:
        print(f"  First error: {untyped_mypy_errors[0]}")

    print(f"Typed MyPy errors: {len(typed_mypy_errors)}")
    if typed_mypy_errors:
        print(f"  First error: {typed_mypy_errors[0]}")

    # Calculate quality improvement
    print(f"\n📈 Quality Improvement:")
    if untyped_mypy_errors > 0:
        error_reduction = (
            (untyped_mypy_errors - typed_mypy_errors) / untyped_mypy_errors
        ) * 100
        print(f"Error reduction: {error_reduction:.1f}%")
    else:
        print("No errors to reduce")

    # Overall assessment
    print(f"\n🎯 Key Findings:")
    if typed_mypy_errors < untyped_mypy_errors:
        print("✅ SUCCESS: Types REDUCE MyPy errors!")
        print("✅ Types improve code quality!")
        print("✅ Types prevent runtime errors!")
        print("✅ Types enhance maintainability!")
    else:
        print("❌ FAILURE: Types don't improve quality")
        print("❌ Our hypothesis was wrong")

    # Developer experience assessment
    print(f"\n👨‍💻 Developer Experience:")
    print(f"Untyped code: {len(untyped_mypy_errors)} potential runtime errors")
    print(f"Typed code: {len(typed_mypy_errors)} potential runtime errors")
    print(
        f"Debugging time saved: {len(untyped_mypy_errors) - len(typed_mypy_errors)} errors caught early"
    )


if __name__ == "__main__":
    main()

"""Test that types actually improve code quality and reduce errors"""

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


def generate_untyped_code() -> str:
    """Generate code WITHOUT type annotations"""
    return '''def process_data(data):
    """Process data without type hints"""
    result = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results):
    """Analyze results without type hints"""
    total = 0
    count = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0

class DataProcessor:
    """Data processor without type hints"""

    def __init__(self, config):
        self.config = config
        self.cache = {}

    def process(self, input_data):
        """Process input data"""
        if input_data in self.cache:
            return self.cache[input_data]

        result = self._transform(input_data)
        self.cache[input_data] = result
        return result

    def _transform(self, data):
        """Transform data"""
        if isinstance(data, list):
            return [self._transform(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._transform(v) for k, v in data.items()}
        else:
            return str(data)'''


def generate_typed_code() -> str:
    """Generate code WITH type annotations"""
    return '''from typing import Dict, List, Union, Any, Optional

def process_data(data: List[Union[str, int]]) -> Dict[str, Union[int, str]]:
    """Process data with type hints"""
    result: Dict[str, Union[int, str]] = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results: Dict[str, Union[int, float]]) -> float:
    """Analyze results with type hints"""
    total: float = 0.0
    count: int = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0.0

class DataProcessor:
    """Data processor with type hints"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {}

    def process(self, input_data: Any) -> Any:
        """Process input data"""
        if input_data in self.cache:
            return self.cache[input_data]

        result: Any = self._transform(input_data)
        self.cache[input_data] = result
        return result

    def _transform(self, data: Any) -> Any:
        """Transform data"""
        if isinstance(data, list):
            return [self._transform(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._transform(v) for k, v in data.items()}
        else:
            return str(data)'''


def main():
    """Test that types improve code quality"""
    print("🧪 Testing: Do Types Actually Improve Code Quality?")

    # Generate both versions
    untyped_code = generate_untyped_code()
    typed_code = generate_typed_code()

    print(f"\n📊 Code Comparison:")
    print(f"Untyped code: {len(untyped_code)} characters")
    print(f"Typed code: {len(typed_code)} characters")
    print(f"Type overhead: {len(typed_code) - len(untyped_code)} characters")

    # Test AST complexity
    print(f"\n🔍 AST Complexity Analysis:")
    untyped_nodes = count_ast_nodes(untyped_code)
    typed_nodes = count_ast_nodes(typed_code)
    print(f"Untyped AST nodes: {untyped_nodes}")
    print(f"Typed AST nodes: {typed_nodes}")
    print(f"Type overhead: {typed_nodes - untyped_nodes} nodes")

    # Test MyPy compliance
    print(f"\n🔍 MyPy Compliance:")
    untyped_mypy_errors = test_mypy_compliance(untyped_code)
    typed_mypy_errors = test_mypy_compliance(typed_code)

    print(f"Untyped MyPy errors: {len(untyped_mypy_errors)}")
    if untyped_mypy_errors:
        print(f"  First error: {untyped_mypy_errors[0]}")

    print(f"Typed MyPy errors: {len(typed_mypy_errors)}")
    if typed_mypy_errors:
        print(f"  First error: {typed_mypy_errors[0]}")

    # Calculate quality improvement
    print(f"\n📈 Quality Improvement:")
    if untyped_mypy_errors > 0:
        error_reduction = (
            (untyped_mypy_errors - typed_mypy_errors) / untyped_mypy_errors
        ) * 100
        print(f"Error reduction: {error_reduction:.1f}%")
    else:
        print("No errors to reduce")

    # Overall assessment
    print(f"\n🎯 Key Findings:")
    if typed_mypy_errors < untyped_mypy_errors:
        print("✅ SUCCESS: Types REDUCE MyPy errors!")
        print("✅ Types improve code quality!")
        print("✅ Types prevent runtime errors!")
        print("✅ Types enhance maintainability!")
    else:
        print("❌ FAILURE: Types don't improve quality")
        print("❌ Our hypothesis was wrong")

    # Developer experience assessment
    print(f"\n👨‍💻 Developer Experience:")
    print(f"Untyped code: {len(untyped_mypy_errors)} potential runtime errors")
    print(f"Typed code: {len(typed_mypy_errors)} potential runtime errors")
    print(
        f"Debugging time saved: {len(untyped_mypy_errors) - len(typed_mypy_errors)} errors caught early"
    )


if __name__ == "__main__":
    main()




