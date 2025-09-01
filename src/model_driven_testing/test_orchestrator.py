#!/usr/bin/env python3
"""
Test Orchestrator - RM Compliant

This module orchestrates the entire test generation and execution workflow.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from src.model_driven_testing.rm_enhancer import rm_enhance
from src.model_driven_testing.test_generator import TestGenerator
from src.model_driven_testing.test_runner import TestRunner


class TestOrchestrator:
    """Orchestrate test generation and execution"""

    def __init__(self, test_output_dir: str = "tests/generated"):
        self.test_output_dir = Path(test_output_dir)
        self.generator = TestGenerator(test_output_dir)
        self.runner = TestRunner(test_output_dir)
        self.logger = logging.getLogger(__name__)

    @rm_enhance
    def generate_and_run_tests(self, source_file: str) -> Dict[str, Any]:
        """Generate tests for a file and run them immediately"""
        try:
            self.logger.info(f"🎯 Orchestrating test generation and execution for {source_file}")

            # Step 1: Generate tests
            self.logger.info("📝 Step 1: Generating tests...")
            generated_files = self.generator.generate_tests_from_file(source_file)

            if not generated_files:
                return {"status": "no_tests_generated", "source_file": source_file, "message": "No tests were generated"}

            self.logger.info(f"✅ Generated {len(generated_files)} test files")

            # Step 2: Run the generated tests
            self.logger.info("🚀 Step 2: Running generated tests...")
            test_results = self.runner.run_all_tests()

            # Step 3: Compile results
            result = {
                "status": "success",
                "source_file": source_file,
                "generation": {"files_generated": len(generated_files), "generated_files": [str(f) for f in generated_files]},
                "execution": test_results,
                "summary": self._create_summary(generated_files, test_results),
            }

            self.logger.info(f"🎉 Orchestration completed: {result['summary']}")
            return result

        except Exception as e:
            self.logger.error(f"❌ Error in test orchestration: {e}")
            return {"status": "error", "source_file": source_file, "error": str(e)}

    def _create_summary(self, generated_files: List[Path], test_results: Dict[str, Any]) -> str:
        """Create a human-readable summary"""
        files_count = len(generated_files)
        tests_passed = test_results.get("tests_passed", 0)
        tests_run = test_results.get("tests_run", 0)

        if test_results.get("status") == "success":
            return f"Generated {files_count} test files, {tests_passed}/{tests_run} tests passed"
        else:
            return f"Generated {files_count} test files, but test execution failed"

    @rm_enhance
    def batch_generate_and_run(self, source_files: List[str]) -> Dict[str, Any]:
        """Generate and run tests for multiple source files"""
        try:
            self.logger.info(f"🎯 Batch orchestrating {len(source_files)} source files")

            results = []
            total_files_generated = 0
            total_tests_passed = 0
            total_tests_run = 0

            for source_file in source_files:
                self.logger.info(f"📝 Processing {source_file}...")
                result = self.generate_and_run_tests(source_file)
                results.append(result)

                if result["status"] == "success":
                    total_files_generated += result["generation"]["files_generated"]
                    total_tests_passed += result["execution"].get("tests_passed", 0)
                    total_tests_run += result["execution"].get("tests_run", 0)

            # Compile batch results
            batch_result = {
                "status": "batch_completed",
                "source_files_processed": len(source_files),
                "total_files_generated": total_files_generated,
                "total_tests_passed": total_tests_passed,
                "total_tests_run": total_tests_run,
                "individual_results": results,
                "summary": f"Processed {len(source_files)} files, generated {total_files_generated} test files, {total_tests_passed}/{total_tests_run} tests passed",
            }

            self.logger.info(f"🎉 Batch orchestration completed: {batch_result['summary']}")
            return batch_result

        except Exception as e:
            self.logger.error(f"❌ Error in batch orchestration: {e}")
            return {"status": "error", "error": str(e), "source_files_processed": 0}

    def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current orchestration status"""
        generator_health = self.generator.get_rm_health()
        runner_status = self.runner.get_test_status()

        return {"orchestrator": "ready", "generator_health": generator_health, "runner_status": runner_status, "test_output_dir": str(self.test_output_dir)}
