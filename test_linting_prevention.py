#!/usr/bin/env python3
"""Test if simple templates actually prevent linting errors"""

import ast
import os
import subprocess
import tempfile


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
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Run MyPy
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

        # Clean up
        os.unlink(temp_file)

        if result.returncode == 0:
            return []  # No errors
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
            return []  # No errors
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


def generate_simple_template_code() -> str:
    """Generate code using simple templates"""
    return '''def process_data(data):
    """Process data with simple template"""
    result = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results):
    """Analyze results with simple template"""
    total = 0
    count = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0

class DataProcessor:
    """Data processor with simple template"""

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


def main():
    """Test if simple templates prevent linting errors"""
    print("🧪 Testing Linting Error Prevention in Simple Templates:")

    # Generate code with simple templates
    template_code = generate_simple_template_code()

    # Test AST complexity
    ast_nodes = count_ast_nodes(template_code)
    print(f"AST complexity: {ast_nodes} nodes")

    # Test MyPy compliance
    print("\\n🔍 Testing MyPy compliance...")
    mypy_errors = test_mypy_compliance(template_code)
    if mypy_errors:
        print(f"❌ MyPy found {len(mypy_errors)} errors:")
        for error in mypy_errors[:3]:  # Show first 3 errors
            print(f"  {error}")
    else:
        print("✅ MyPy compliance: PASSED")

    # Test Black compliance
    print("\\n🔍 Testing Black compliance...")
    black_passed = test_black_compliance(template_code)
    if black_passed:
        print("✅ Black compliance: PASSED")
    else:
        print("❌ Black compliance: FAILED")

    # Test Flake8 compliance
    print("\\n🔍 Testing Flake8 compliance...")
    flake8_errors = test_flake8_compliance(template_code)
    if flake8_errors:
        print(f"❌ Flake8 found {len(flake8_errors)} errors:")
        for error in flake8_errors[:3]:  # Show first 3 errors
            print(f"  {error}")
    else:
        print("✅ Flake8 compliance: PASSED")

    # Overall assessment
    print("\\n📊 Overall Assessment:")
    total_errors = len(mypy_errors) + len(flake8_errors) + (0 if black_passed else 1)
    if total_errors == 0:
        print("🎉 SUCCESS: Simple templates generate linting-compliant code!")
    else:
        print(
            f"⚠️ WARNING: Simple templates still produce {total_errors} linting issues"
        )
        print("   This means our approach needs refinement!")


if __name__ == "__main__":
    main()

"""Test if simple templates actually prevent linting errors"""

import ast
import os
import subprocess
import tempfile


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
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Run MyPy
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

        # Clean up
        os.unlink(temp_file)

        if result.returncode == 0:
            return []  # No errors
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
            return []  # No errors
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


def generate_simple_template_code() -> str:
    """Generate code using simple templates"""
    return '''def process_data(data):
    """Process data with simple template"""
    result = {}
    for item in data:
        if isinstance(item, str):
            result[item] = len(item)
        elif isinstance(item, int):
            result[str(item)] = item
    return result

def analyze_results(results):
    """Analyze results with simple template"""
    total = 0
    count = 0
    for key, value in results.items():
        if isinstance(value, (int, float)):
            total += value
            count += 1
    return total / count if count > 0 else 0

class DataProcessor:
    """Data processor with simple template"""

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


def main():
    """Test if simple templates prevent linting errors"""
    print("🧪 Testing Linting Error Prevention in Simple Templates:")

    # Generate code with simple templates
    template_code = generate_simple_template_code()

    # Test AST complexity
    ast_nodes = count_ast_nodes(template_code)
    print(f"AST complexity: {ast_nodes} nodes")

    # Test MyPy compliance
    print("\\n🔍 Testing MyPy compliance...")
    mypy_errors = test_mypy_compliance(template_code)
    if mypy_errors:
        print(f"❌ MyPy found {len(mypy_errors)} errors:")
        for error in mypy_errors[:3]:  # Show first 3 errors
            print(f"  {error}")
    else:
        print("✅ MyPy compliance: PASSED")

    # Test Black compliance
    print("\\n🔍 Testing Black compliance...")
    black_passed = test_black_compliance(template_code)
    if black_passed:
        print("✅ Black compliance: PASSED")
    else:
        print("❌ Black compliance: FAILED")

    # Test Flake8 compliance
    print("\\n🔍 Testing Flake8 compliance...")
    flake8_errors = test_flake8_compliance(template_code)
    if flake8_errors:
        print(f"❌ Flake8 found {len(flake8_errors)} errors:")
        for error in flake8_errors[:3]:  # Show first 3 errors
            print(f"  {error}")
    else:
        print("✅ Flake8 compliance: PASSED")

    # Overall assessment
    print("\\n📊 Overall Assessment:")
    total_errors = len(mypy_errors) + len(flake8_errors) + (0 if black_passed else 1)
    if total_errors == 0:
        print("🎉 SUCCESS: Simple templates generate linting-compliant code!")
    else:
        print(
            f"⚠️ WARNING: Simple templates still produce {total_errors} linting issues"
        )
        print("   This means our approach needs refinement!")


if __name__ == "__main__":
    main()
