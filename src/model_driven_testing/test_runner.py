#!/usr/bin/env python3
"""
Test Runner - RM Compliant

This module runs generated tests and reports results.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any

from src.model_driven_testing.rm_enhancer import rm_enhance


class TestRunner:
    """Run generated tests and report results"""

    def __init__(self, test_dir: str = "tests/generated"):
        self.test_dir = Path(test_dir)
        self.logger = logging.getLogger(__name__)

    @rm_enhance
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all generated tests"""
        try:
            self.logger.info(f"🚀 Running all tests in {self.test_dir}")

            if not self.test_dir.exists():
                self.logger.warning(f"⚠️ Test directory {self.test_dir} does not exist")
                return {"status": "error", "message": "Test directory not found"}

            # Find all test files
            test_files = list(self.test_dir.glob("test_*_generated.py"))
            if not test_files:
                self.logger.info("ℹ️ No generated tests found")
                return {"status": "success", "tests_run": 0, "tests_passed": 0}

            self.logger.info(f"📁 Found {len(test_files)} test files")

            # Run pytest
            result = self._run_pytest(test_files)

            self.logger.info(f"✅ Test run completed: {result}")
            return result

        except Exception as e:
            self.logger.error(f"❌ Error running tests: {e}")
            return {"status": "error", "message": str(e)}

    def _run_pytest(self, test_files: List[Path]) -> Dict[str, Any]:
        """Run pytest on test files"""
        try:
            # Build pytest command
            cmd = ["uv", "run", "python", "-m", "pytest", "--tb=no", "-q"]
            cmd.extend([str(f) for f in test_files])

            self.logger.debug(f"🔧 Running command: {' '.join(cmd)}")

            # Execute pytest
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

            # Parse results
            if result.returncode == 0:
                # Success - parse output for test counts
                output = result.stdout
                tests_passed = self._parse_test_count(output)

                return {"status": "success", "tests_run": len(test_files), "tests_passed": tests_passed, "return_code": result.returncode, "output": output}
            else:
                # Failure - parse error output
                error_output = result.stderr or result.stdout
                return {"status": "failure", "tests_run": len(test_files), "tests_passed": 0, "return_code": result.returncode, "error": error_output}

        except Exception as e:
            self.logger.error(f"❌ Error executing pytest: {e}")
            return {"status": "error", "message": str(e)}

    def _parse_test_count(self, output: str) -> int:
        """Parse test count from pytest output"""
        try:
            # Look for patterns like "X passed" or "X failed"
            lines = output.split("\n")
            for line in lines:
                if "passed" in line and "failed" not in line:
                    # Extract number before "passed"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            if i > 0 and parts[i - 1].isdigit():
                                return int(parts[i - 1])
            return 0
        except Exception:
            return 0

    def run_specific_test(self, test_file: str) -> Dict[str, Any]:
        """Run a specific test file"""
        test_path = self.test_dir / test_file
        if not test_path.exists():
            return {"status": "error", "message": f"Test file {test_file} not found"}

        return self._run_pytest([test_path])

    def get_test_status(self) -> Dict[str, Any]:
        """Get current test status"""
        test_files = list(self.test_dir.glob("test_*_generated.py"))
        return {"test_directory": str(self.test_dir), "test_files_count": len(test_files), "test_files": [f.name for f in test_files], "status": "ready" if test_files else "no_tests"}
