#!/usr/bin/env python3
"""
Regression Test Suite: V2 vs V3 Compatibility

Purpose: Ensure V3 produces compatible output with V2
Critical: This is infrastructure code that other systems depend on
"""

import sys
import tempfile
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import after path setup
from round_trip_engineering.enhanced_reverse_engineer_v2 import (
    EnhancedReverseEngineerV2,
)

# noqa: E402
from round_trip_engineering.enhanced_reverse_engineer_v3 import (
    EnhancedReverseEngineerV3,
)


class V2V3CompatibilityTester:
    """Test compatibility between V2 and V3 outputs"""

    def __init__(self):
        self.v2_engineer = EnhancedReverseEngineerV2()
        self.v3_engineer = EnhancedReverseEngineerV3()
        self.test_files = []

    def setup_test_files(self):
        """Create test files with various Python constructs"""
        test_cases = [
            self._create_simple_class_file(),
            self._create_complex_class_file(),
            self._create_function_file(),
            self._create_mixed_file(),
            self._create_edge_case_file(),
        ]

        for test_file in test_cases:
            self.test_files.append(test_file)
            print(f"📝 Created test file: {test_file}")

    def _create_simple_class_file(self) -> str:
        """Create a file with a simple class"""
        content = '''#!/usr/bin/env python3
"""
Simple class test file
"""

class SimpleClass:
    """A simple test class"""

    def __init__(self):
        self.value = 42

    def get_value(self):
        return self.value
'''
        return self._write_temp_file(content, "simple_class.py")

    def _create_complex_class_file(self) -> str:
        """Create a file with complex class structure"""
        content = '''#!/usr/bin/env python3
"""
Complex class test file
"""

from typing import List, Dict, Optional

class ComplexClass:
    """A complex test class with inheritance and decorators"""

    def __init__(self, name: str, items: List[str]):
        self.name = name
        self.items = items

    @property
    def item_count(self) -> int:
        return len(self.items)

    def add_item(self, item: str) -> None:
        self.items.append(item)

    @classmethod
    def create_empty(cls) -> 'ComplexClass':
        return cls("empty", [])

    @staticmethod
    def validate_name(name: str) -> bool:
        return len(name) > 0

class InheritedClass(ComplexClass):
    """Inherited class"""

    def __init__(self, name: str, items: List[str], extra: str):
        super().__init__(name, items)
        self.extra = extra
'''
        return self._write_temp_file(content, "complex_class.py")

    def _create_function_file(self) -> str:
        """Create a file with module functions"""
        content = '''#!/usr/bin/env python3
"""
Module functions test file
"""

import os
from pathlib import Path

def simple_function():
    """Simple function"""
    return "hello"

def function_with_args(name: str, age: int = 25) -> str:
    """Function with arguments and type hints"""
    return f"{name} is {age} years old"

async def async_function():
    """Async function"""
    await asyncio.sleep(1)
    return "async result"

def function_with_decorator():
    """Function with decorator"""
    @decorator
    def inner():
        pass
    return inner
'''
        return self._write_temp_file(content, "functions.py")

    def _create_mixed_file(self) -> str:
        """Create a file with mixed constructs"""
        content = '''#!/usr/bin/env python3
"""
Mixed constructs test file
"""

import json
from typing import Any

# Module-level constants
DEFAULT_VALUE = 42
CONFIG = {"debug": True}

class MixedClass:
    """Class with mixed content"""

    def __init__(self):
        self.value = DEFAULT_VALUE

    def method(self):
        return self.value

def module_function():
    """Module-level function"""
    return CONFIG

if __name__ == "__main__":
    print("Running mixed file")
'''
        return self._write_temp_file(content, "mixed.py")

    def _create_edge_case_file(self) -> str:
        """Create a file with edge cases"""
        content = '''#!/usr/bin/env python3
"""
Edge cases test file
"""

# Empty lines and comments
# Multiple comments

class EdgeCaseClass:
    """Class with edge cases"""

    # Class-level comment

    def __init__(self):
        # Method comment
        pass

    def empty_method(self):
        pass

    def method_with_complex_decorator(self):
        @decorator(param1="value1", param2="value2")
        def inner():
            pass
        return inner

# Trailing empty lines


'''
        return self._write_temp_file(content, "edge_cases.py")

    def _write_temp_file(self, content: str, filename: str) -> str:
        """Write content to temporary file"""
        temp_dir = Path(tempfile.gettempdir()) / "v2v3_test"
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / filename
        with open(file_path, "w") as f:
            f.write(content)

        return str(file_path)

    def run_compatibility_tests(self) -> dict[str, Any]:
        """Run full compatibility test suite"""
        print("🧪 Starting V2 vs V3 Compatibility Tests")
        print("=" * 50)

        results = {"total_tests": 0, "passed": 0, "failed": 0, "test_results": []}

        for test_file in self.test_files:
            print(f"\n🔍 Testing: {Path(test_file).name}")

            try:
                # Run V2 analysis
                v2_result = self.v2_engineer.reverse_engineer_file(test_file)

                # Run V3 analysis
                v3_result = self.v3_engineer.reverse_engineer_file(test_file)

                # Compare outputs
                test_result = self._compare_outputs(test_file, v2_result, v3_result)
                results["test_results"].append(test_result)
                results["total_tests"] += 1

                if test_result["passed"]:
                    results["passed"] += 1
                    print(f"  ✅ PASSED: {test_result['summary']}")
                else:
                    results["failed"] += 1
                    print(f"  ❌ FAILED: {test_result['summary']}")
                    for issue in test_result["issues"]:
                        print(f"     🚨 {issue}")

            except Exception as e:
                results["total_tests"] += 1
                results["failed"] += 1
                test_result = {
                    "file": test_file,
                    "passed": False,
                    "summary": f"Exception: {e}",
                    "issues": [f"Exception occurred: {e}"],
                }
                results["test_results"].append(test_result)
                print(f"  💥 EXCEPTION: {e}")

        return results

    def _compare_outputs(
        self, file_path: str, v2_result: dict[str, Any], v3_result: dict[str, Any]
    ) -> dict[str, Any]:
        """Compare V2 and V3 outputs for compatibility"""
        issues = []

        # Check if both produced results
        if not v2_result or not v3_result:
            issues.append("One or both engines failed to produce results")
            return {
                "file": file_path,
                "passed": False,
                "summary": "Engine failure",
                "issues": issues,
            }

        # Check basic structure compatibility
        # V2 uses 'components' and 'module_functions', V3 uses 'classes' and 'functions'
        v2_has_classes = "components" in v2_result
        v3_has_classes = "classes" in v3_result
        v2_has_functions = "module_functions" in v2_result
        v3_has_functions = "functions" in v3_result

        if not v2_has_classes or not v3_has_classes:
            issues.append("Missing classes key in one or both engines")
        if not v2_has_functions or not v3_has_functions:
            issues.append("Missing functions key in one or both engines")

        # Check class extraction compatibility
        if v2_has_classes and v3_has_classes:
            v2_classes = v2_result["components"]  # V2 uses 'components'
            v3_classes = v3_result["classes"]  # V3 uses 'classes'

            if len(v2_classes) != len(v3_classes):
                issues.append(
                    f"Class count mismatch: V2={len(v2_classes)}, V3={len(v3_classes)}"
                )

            # Check if same class names are extracted
            v2_class_names = set(v2_classes.keys())
            v3_class_names = set(v3_classes.keys())

            if v2_class_names != v3_class_names:
                missing_in_v3 = v2_class_names - v3_class_names
                extra_in_v3 = v3_class_names - v2_class_names
                if missing_in_v3:
                    issues.append(f"Classes missing in V3: {missing_in_v3}")
                if extra_in_v3:
                    issues.append(f"Extra classes in V3: {extra_in_v3}")

        # Check function extraction compatibility
        if v2_has_functions and v3_has_functions:
            v2_funcs = v2_result["module_functions"]  # V2 uses 'module_functions'
            v3_funcs = v3_result["functions"]  # V3 uses 'functions'

            if len(v2_funcs) != len(v3_funcs):
                issues.append(
                    f"Function count mismatch: V2={len(v2_funcs)}, V3={len(v3_funcs)}"
                )

        # Check import extraction compatibility
        if "imports" in v2_result and "imports" in v3_result:
            v2_imports = set(v2_result["imports"])
            v3_imports = set(v3_result["imports"])

            if v2_imports != v3_imports:
                missing_in_v3 = v2_imports - v3_imports
                extra_in_v3 = v3_imports - v2_imports
                if missing_in_v3:
                    issues.append(f"Imports missing in V3: {missing_in_v3}")
                if extra_in_v3:
                    issues.append(f"Extra imports in V3: {extra_in_v3}")

        passed = len(issues) == 0
        summary = f"Compatibility check {'PASSED' if passed else 'FAILED'}"

        return {
            "file": file_path,
            "passed": passed,
            "summary": summary,
            "issues": issues,
            "v2_result": v2_result,
            "v3_result": v3_result,
        }

    def cleanup(self):
        """Clean up test files"""
        for test_file in self.test_files:
            try:
                Path(test_file).unlink()
                print(f"🧹 Cleaned up: {test_file}")
            except Exception as e:
                print(f"⚠️  Could not clean up {test_file}: {e}")


def main():
    """Run the compatibility test suite"""
    print("🚀 V2 vs V3 Compatibility Test Suite")
    print("=" * 50)

    tester = V2V3CompatibilityTester()

    try:
        # Setup test files
        print("\n📝 Setting up test files...")
        tester.setup_test_files()

        # Run tests
        print("\n🧪 Running compatibility tests...")
        results = tester.run_compatibility_tests()

        # Report results
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed']} ✅")
        print(f"Failed: {results['failed']} ❌")
        print(
            f"Success Rate: {(results['passed'] / results['total_tests'] * 100):.1f}%"
        )

        if results["failed"] > 0:
            print("\n🚨 COMPATIBILITY ISSUES DETECTED!")
            print("V3 may not be a drop-in replacement for V2")
            return 1
        print("\n🎉 ALL TESTS PASSED!")
        print("V3 appears to be compatible with V2")
        return 0

    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        return 1
    finally:
        # Cleanup
        print("\n🧹 Cleaning up test files...")
        tester.cleanup()


if __name__ == "__main__":
    sys.exit(main())
