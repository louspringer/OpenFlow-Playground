#!/usr/bin/env python3
"""
Performance Validation Test Suite
Benchmarks refactored modules to ensure no performance regression.
"""

import pytest
import time
import asyncio
from typing import Dict, Any, List
import statistics

# Import the refactored modules
from src.round_trip_engineering.generators.class_generator import ClassGenerator
from src.round_trip_engineering.generators.class_structure_generator import (
    ClassStructureGenerator,
)
from src.round_trip_engineering.generators.method_validator import MethodValidator
from src.round_trip_engineering.generators.method_processor import MethodCompleter
from src.round_trip_engineering.generators.operational_methods_generator import (
    OperationalMethodsGenerator,
)
from src.round_trip_engineering.generators.base_reflective_module import (
    BaseReflectiveModule,
)


class TestPerformanceBenchmarks:
    """Test performance benchmarks for refactored modules."""

    def test_class_structure_generator_performance(self):
        """Test ClassStructureGenerator performance with various inputs."""
        generator = ClassStructureGenerator()

        # Test data
        test_cases = [
            {"name": "SimpleClass", "bases": [], "docstring": "Simple class"},
            {
                "name": "ComplexClass",
                "bases": ["Base1", "Base2", "Mixin"],
                "docstring": "Complex class with inheritance",
            },
            {"name": "NoDocClass", "bases": [], "docstring": ""},
            {
                "name": "LongDocClass",
                "bases": ["Base"],
                "docstring": "A very long docstring that tests performance with extended text content",
            },
        ]

        performance_results = []

        for i, test_case in enumerate(test_cases):
            start_time = time.perf_counter()

            # Run multiple iterations for accurate timing
            for _ in range(100):
                result = generator.generate_class_structure(
                    test_case["name"],
                    {"bases": test_case["bases"], "docstring": test_case["docstring"]},
                )

            end_time = time.perf_counter()
            total_time = end_time - start_time
            avg_time = total_time / 100

            performance_results.append(
                {
                    "case": f"Case {i + 1}: {test_case['name']}",
                    "total_time": total_time,
                    "avg_time": avg_time,
                    "iterations": 100,
                }
            )

            # Performance assertion: each operation should complete in under 1ms
            assert avg_time < 0.001, (
                f"Performance regression: {test_case['name']} took {avg_time:.6f}s per operation"
            )

        # Log performance results
        print(f"\n📊 ClassStructureGenerator Performance Results:")
        for result in performance_results:
            print(
                f"  {result['case']}: {result['avg_time']:.6f}s avg ({result['total_time']:.6f}s total)"
            )

    def test_method_validator_performance(self):
        """Test MethodValidator performance with various method sources."""
        validator = MethodValidator()

        # Test data
        test_methods = [
            # Simple method
            """def simple_method(self):
    return True""",
            # Method with parameters
            """def param_method(self, param1, param2=None):
    result = param1 + (param2 or 0)
    return result""",
            # Async method
            """async def async_method(self):
    await asyncio.sleep(0.001)
    return "async_result" """,
            # Complex method
            """def complex_method(self, data):
    try:
        if isinstance(data, dict):
            return {k: v * 2 for k, v in data.items()}
        elif isinstance(data, list):
            return [item * 2 for item in data]
        else:
            return data * 2
    except Exception as e:
        return None""",
        ]

        performance_results = []

        for i, method_source in enumerate(test_methods):
            start_time = time.perf_counter()

            # Run multiple iterations for accurate timing
            for _ in range(50):
                result = validator.is_valid_method_source(method_source)

            end_time = time.perf_counter()
            total_time = end_time - start_time
            avg_time = total_time / 50

            performance_results.append(
                {
                    "case": f"Method {i + 1}",
                    "total_time": total_time,
                    "avg_time": avg_time,
                    "iterations": 50,
                }
            )

            # Performance assertion: each validation should complete in under 2ms
            assert avg_time < 0.002, (
                f"Performance regression: Method {i + 1} took {avg_time:.6f}s per validation"
            )

        # Log performance results
        print(f"\n📊 MethodValidator Performance Results:")
        for result in performance_results:
            print(
                f"  {result['case']}: {result['avg_time']:.6f}s avg ({result['total_time']:.6f}s total)"
            )

    def test_method_completer_performance(self):
        """Test MethodCompleter performance with various incomplete methods."""
        completer = MethodCompleter()

        # Test data
        test_methods = [
            # Basic incomplete method
            """def basic_method(self):
    if True:
        return True""",
            # Method with try block
            """def try_method(self):
    try:
        result = self.process_data()
        return result""",
            # Method with dictionary
            """def dict_method(self):
    return {
        "status": "success",
        "data": self.get_data()
    }""",
            # Method with multiple conditions
            """def multi_condition_method(self, value):
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    else:
        return "zero" """,
        ]

        performance_results = []

        for i, method_source in enumerate(test_methods):
            start_time = time.perf_counter()

            # Run multiple iterations for accurate timing
            for _ in range(50):
                result = completer.complete_method_source(method_source)

            end_time = time.perf_counter()
            total_time = end_time - start_time
            avg_time = total_time / 50

            performance_results.append(
                {
                    "case": f"Method {i + 1}",
                    "total_time": total_time,
                    "avg_time": avg_time,
                    "iterations": 50,
                }
            )

            # Performance assertion: each completion should complete in under 2ms
            assert avg_time < 0.002, (
                f"Performance regression: Method {i + 1} took {avg_time:.6f}s per completion"
            )

        # Log performance results
        print(f"\n📊 MethodCompleter Performance Results:")
        for result in performance_results:
            print(
                f"  {result['case']}: {result['avg_time']:.6f}s avg ({result['total_time']:.6f}s total)"
            )

    def test_operational_methods_generator_performance(self):
        """Test OperationalMethodsGenerator performance."""
        generator = OperationalMethodsGenerator()

        # Test data
        test_class_names = [
            "SimpleClass",
            "ComplexClassWithLongName",
            "VeryLongClassNameThatTestsPerformance",
            "ClassWithSpecialCharacters123",
        ]

        performance_results = []

        for i, class_name in enumerate(test_class_names):
            start_time = time.perf_counter()

            # Run multiple iterations for accurate timing
            for _ in range(100):
                result = generator.generate_operational_methods(class_name)

            end_time = time.perf_counter()
            total_time = end_time - start_time
            avg_time = total_time / 100

            performance_results.append(
                {
                    "case": f"Class {i + 1}: {class_name}",
                    "total_time": total_time,
                    "avg_time": avg_time,
                    "iterations": 100,
                }
            )

            # Performance assertion: each generation should complete in under 1ms
            assert avg_time < 0.001, (
                f"Performance regression: Class {class_name} took {avg_time:.6f}s per generation"
            )

        # Log performance results
        print(f"\n📊 OperationalMethodsGenerator Performance Results:")
        for result in performance_results:
            print(
                f"  {result['case']}: {result['avg_time']:.6f}s avg ({result['total_time']:.6f}s total)"
            )

    def test_integrated_class_generator_performance(self):
        """Test integrated ClassGenerator performance with full workflow."""
        generator = ClassGenerator()

        # Test data - simulate a complex class generation scenario
        test_scenario = {
            "class_name": "PerformanceTestClass",
            "enhanced_ast": {
                "bases": ["BaseClass", "MixinClass"],
                "docstring": "A comprehensive test class for performance validation",
                "methods": [
                    {
                        "name": "simple_method",
                        "source": """def simple_method(self):
    return True""",
                    },
                    {
                        "name": "complex_method",
                        "source": """def complex_method(self, data):
    try:
        if isinstance(data, dict):
            return {k: v * 2 for k, v in data.items()}
        elif isinstance(data, list):
            return [item * 2 for item in data]
        else:
            return data * 2
    except Exception as e:
        return None""",
                    },
                ],
            },
        }

        start_time = time.perf_counter()

        # Run multiple iterations for accurate timing
        for _ in range(20):
            # Simulate the full workflow
            class_structure = (
                generator.class_structure_generator.generate_class_structure(
                    test_scenario["class_name"], test_scenario["enhanced_ast"]
                )
            )

            # Validate methods
            for method in test_scenario["enhanced_ast"]["methods"]:
                is_valid = generator.method_validator.is_valid_method_source(
                    method["source"]
                )
                if not is_valid:
                    completed = generator.method_completer.complete_method_source(
                        method["source"]
                    )

            # Generate operational methods
            operational_methods = (
                generator.operational_methods_generator.generate_operational_methods(
                    test_scenario["class_name"]
                )
            )

        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time = total_time / 20

        # Performance assertion: each full workflow should complete in under 10ms
        assert avg_time < 0.01, (
            f"Performance regression: Full workflow took {avg_time:.6f}s per iteration"
        )

        print(f"\n📊 Integrated ClassGenerator Performance Results:")
        print(
            f"  Full workflow: {avg_time:.6f}s avg ({total_time:.6f}s total for 20 iterations)"
        )

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable during operations."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Run intensive operations
        generator = ClassGenerator()

        for i in range(1000):
            # Generate class structure
            generator.class_structure_generator.generate_class_structure(
                f"MemoryTestClass{i}",
                {"bases": [], "docstring": f"Memory test class {i}"},
            )

            # Validate methods
            test_method = f"""def test_method_{i}(self):
    return {i}"""
            generator.method_validator.is_valid_method_source(test_method)

            # Complete methods
            incomplete_method = f"""def incomplete_method_{i}(self):
    if True:
        return {i}"""
            generator.method_completer.complete_method_source(incomplete_method)

            # Generate operational methods
            generator.operational_methods_generator.generate_operational_methods(
                f"MemoryTestClass{i}"
            )

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"\n📊 Memory Usage Results:")
        print(f"  Initial memory: {initial_memory:.2f} MB")
        print(f"  Final memory: {final_memory:.2f} MB")
        print(f"  Memory increase: {memory_increase:.2f} MB")

        # Memory assertion: memory increase should be reasonable (< 50MB)
        assert memory_increase < 50, (
            f"Memory usage increased by {memory_increase:.2f} MB, which is excessive"
        )

    def test_concurrent_operation_performance(self):
        """Test performance under concurrent operations."""
        import concurrent.futures

        generator = ClassGenerator()

        def generate_class_workload(class_id: int) -> float:
            """Individual workload for concurrent testing."""
            start_time = time.perf_counter()

            # Generate class structure
            class_structure = (
                generator.class_structure_generator.generate_class_structure(
                    f"ConcurrentClass{class_id}",
                    {"bases": [], "docstring": f"Concurrent test class {class_id}"},
                )
            )

            # Validate methods
            test_method = f"""def test_method_{class_id}(self):
    return {class_id}"""
            is_valid = generator.method_validator.is_valid_method_source(test_method)

            # Complete methods
            incomplete_method = f"""def incomplete_method_{class_id}(self):
    if True:
        return {class_id}"""
            completed = generator.method_completer.complete_method_source(
                incomplete_method
            )

            # Generate operational methods
            operational_methods = (
                generator.operational_methods_generator.generate_operational_methods(
                    f"ConcurrentClass{class_id}"
                )
            )

            end_time = time.perf_counter()
            return end_time - start_time

        # Test with different levels of concurrency
        concurrency_levels = [1, 2, 4, 8]
        performance_results = []

        for concurrency in concurrency_levels:
            start_time = time.perf_counter()

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=concurrency
            ) as executor:
                futures = [
                    executor.submit(generate_class_workload, i) for i in range(20)
                ]
                results = [
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                ]

            end_time = time.perf_counter()
            total_time = end_time - start_time

            performance_results.append(
                {
                    "concurrency": concurrency,
                    "total_time": total_time,
                    "avg_individual_time": statistics.mean(results),
                    "max_individual_time": max(results),
                    "min_individual_time": min(results),
                }
            )

            # Performance assertion: total time should scale reasonably with concurrency
            expected_time = 20 * 0.001 * concurrency  # Rough estimate
            assert total_time < expected_time * 2, (
                f"Performance regression: {concurrency} workers took {total_time:.6f}s (expected < {expected_time * 2:.6f}s)"
            )

        print(f"\n📊 Concurrent Operation Performance Results:")
        for result in performance_results:
            print(
                f"  {result['concurrency']} workers: {result['total_time']:.6f}s total, {result['avg_individual_time']:.6f}s avg per operation"
            )


class TestPerformanceRegressionDetection:
    """Test that performance regressions are detected."""

    def test_performance_baseline_validation(self):
        """Validate that performance meets baseline expectations."""
        generator = ClassGenerator()

        # Baseline performance expectations
        baseline_expectations = {
            "class_structure_generation": 0.001,  # 1ms
            "method_validation": 0.002,  # 2ms
            "method_completion": 0.002,  # 2ms
            "operational_methods_generation": 0.001,  # 1ms
        }

        # Test class structure generation
        start_time = time.perf_counter()
        for _ in range(100):
            generator.class_structure_generator.generate_class_structure(
                "BaselineClass", {"bases": [], "docstring": "Baseline test"}
            )
        end_time = time.perf_counter()
        avg_time = (end_time - start_time) / 100

        assert avg_time < baseline_expectations["class_structure_generation"], (
            f"Class structure generation performance regression: {avg_time:.6f}s (expected < {baseline_expectations['class_structure_generation']:.6f}s)"
        )

        # Test method validation
        test_method = """def baseline_method(self):
    return True"""

        start_time = time.perf_counter()
        for _ in range(100):
            generator.method_validator.is_valid_method_source(test_method)
        end_time = time.perf_counter()
        avg_time = (end_time - start_time) / 100

        assert avg_time < baseline_expectations["method_validation"], (
            f"Method validation performance regression: {avg_time:.6f}s (expected < {baseline_expectations['method_validation']:.6f}s)"
        )

        print(f"\n✅ Performance baseline validation passed:")
        print(f"  Class structure generation: {avg_time:.6f}s avg")
        print(f"  Method validation: {avg_time:.6f}s avg")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
