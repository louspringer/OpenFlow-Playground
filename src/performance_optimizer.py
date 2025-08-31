#!/usr/bin/env python3
"""
Performance Optimization System

Addresses UC-9 low risk use case for performance optimization and benchmarking.
This system benchmarks integrated system performance, optimizes bottlenecks, and prepares for production.
"""

import time
import psutil
import os
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import statistics
from dataclasses import dataclass
from src.control_flow_analyzer import ControlFlowAnalyzer
from src.multi_file_workflow_analyzer import MultiFileWorkflowAnalyzer
from src.uml_activity_generator import UMLActivityGenerator
from src.complexity_metrics_analyzer import ComplexityMetricsAnalyzer


@dataclass
class PerformanceMetrics:
    """Performance metrics data class."""

    execution_time: float
    memory_usage: float
    cpu_usage: float
    file_size: int
    success: bool
    error: Optional[str] = None


class PerformanceOptimizer:
    """Optimizes performance of workflow extraction system."""

    def __init__(self):
        self.control_flow_analyzer = ControlFlowAnalyzer()
        self.multi_file_analyzer = MultiFileWorkflowAnalyzer()
        self.uml_generator = UMLActivityGenerator()
        self.complexity_analyzer = ComplexityMetricsAnalyzer()
        self.performance_cache = {}

    def benchmark_system_performance(
        self, test_files: List[str] = None
    ) -> Dict[str, Any]:
        """
        Benchmark the performance of the integrated workflow extraction system.

        Args:
            test_files: List of test files to benchmark

        Returns:
            Comprehensive performance benchmark results
        """
        if test_files is None:
            test_files = [
                "src/enhanced_activity_generator.py",
                "src/control_flow_analyzer.py",
                "src/multi_file_workflow_analyzer.py",
            ]

        benchmark_results = {
            "test_files": test_files,
            "total_files": len(test_files),
            "benchmark_timestamp": time.time(),
            "component_benchmarks": {},
            "overall_performance": {},
            "bottlenecks": [],
            "optimization_recommendations": [],
        }

        # Benchmark each component
        print("🔍 Benchmarking Control Flow Analysis...")
        benchmark_results["component_benchmarks"]["control_flow"] = (
            self._benchmark_control_flow(test_files)
        )

        print("🔍 Benchmarking Multi-File Analysis...")
        benchmark_results["component_benchmarks"]["multi_file"] = (
            self._benchmark_multi_file_analysis(test_files)
        )

        print("🔍 Benchmarking UML Generation...")
        benchmark_results["component_benchmarks"]["uml_generation"] = (
            self._benchmark_uml_generation(test_files)
        )

        print("🔍 Benchmarking Complexity Analysis...")
        benchmark_results["component_benchmarks"]["complexity"] = (
            self._benchmark_complexity_analysis(test_files)
        )

        # Calculate overall performance metrics
        benchmark_results["overall_performance"] = self._calculate_overall_performance(
            benchmark_results["component_benchmarks"]
        )

        # Identify bottlenecks
        benchmark_results["bottlenecks"] = self._identify_bottlenecks(
            benchmark_results["component_benchmarks"]
        )

        # Generate optimization recommendations
        benchmark_results["optimization_recommendations"] = (
            self._generate_optimization_recommendations(
                benchmark_results["bottlenecks"],
                benchmark_results["overall_performance"],
            )
        )

        return benchmark_results

    def _benchmark_control_flow(self, test_files: List[str]) -> Dict[str, Any]:
        """Benchmark control flow analysis performance."""
        results = {
            "files": {},
            "total_execution_time": 0,
            "total_memory_usage": 0,
            "total_cpu_usage": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
        }

        for test_file in test_files:
            try:
                # Measure performance
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                start_cpu = psutil.cpu_percent()

                # Run analysis
                result = self.control_flow_analyzer.analyze_control_flow(test_file)

                # Measure end metrics
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                memory_usage = end_memory - start_memory
                cpu_usage = (start_cpu + end_cpu) / 2

                file_metrics = PerformanceMetrics(
                    execution_time=execution_time,
                    memory_usage=memory_usage,
                    cpu_usage=cpu_usage,
                    file_size=os.path.getsize(test_file),
                    success=result["analysis_success"],
                )

                results["files"][test_file] = file_metrics
                results["total_execution_time"] += execution_time
                results["total_memory_usage"] += memory_usage
                results["total_cpu_usage"] += cpu_usage

                if result["analysis_success"]:
                    results["successful_analyses"] += 1
                else:
                    results["failed_analyses"] += 1

            except Exception as e:
                file_metrics = PerformanceMetrics(
                    execution_time=0,
                    memory_usage=0,
                    cpu_usage=0,
                    file_size=0,
                    success=False,
                    error=str(e),
                )
                results["files"][test_file] = file_metrics
                results["failed_analyses"] += 1

        return results

    def _benchmark_multi_file_analysis(self, test_files: List[str]) -> Dict[str, Any]:
        """Benchmark multi-file analysis performance."""
        try:
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            start_cpu = psutil.cpu_percent()

            # Run analysis on source directory
            result = self.multi_file_analyzer.analyze_project_workflow("src")

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent()

            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            cpu_usage = (start_cpu + end_cpu) / 2

            return {
                "execution_time": execution_time,
                "memory_usage": memory_usage,
                "cpu_usage": cpu_usage,
                "success": result["analysis_success"],
                "total_files_analyzed": result.get("total_files", 0),
                "error": result.get("error"),
            }

        except Exception as e:
            return {
                "execution_time": 0,
                "memory_usage": 0,
                "cpu_usage": 0,
                "success": False,
                "total_files_analyzed": 0,
                "error": str(e),
            }

    def _benchmark_uml_generation(self, test_files: List[str]) -> Dict[str, Any]:
        """Benchmark UML generation performance."""
        results = {
            "files": {},
            "total_execution_time": 0,
            "total_memory_usage": 0,
            "total_cpu_usage": 0,
            "successful_generations": 0,
            "failed_generations": 0,
        }

        for test_file in test_files:
            try:
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                start_cpu = psutil.cpu_percent()

                # Generate UML diagram
                output_file = f"test_uml_{Path(test_file).stem}"
                result = self.uml_generator.generate_activity_diagram(
                    test_file, output_file
                )

                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                memory_usage = end_memory - start_memory
                cpu_usage = (start_cpu + end_cpu) / 2

                file_metrics = PerformanceMetrics(
                    execution_time=execution_time,
                    memory_usage=memory_usage,
                    cpu_usage=cpu_usage,
                    file_size=os.path.getsize(test_file),
                    success=result["success"],
                )

                results["files"][test_file] = file_metrics
                results["total_execution_time"] += execution_time
                results["total_memory_usage"] += memory_usage
                results["total_cpu_usage"] += cpu_usage

                if result["success"]:
                    results["successful_generations"] += 1
                else:
                    results["failed_generations"] += 1

            except Exception as e:
                file_metrics = PerformanceMetrics(
                    execution_time=0,
                    memory_usage=0,
                    cpu_usage=0,
                    file_size=0,
                    success=False,
                    error=str(e),
                )
                results["files"][test_file] = file_metrics
                results["failed_generations"] += 1

        return results

    def _benchmark_complexity_analysis(self, test_files: List[str]) -> Dict[str, Any]:
        """Benchmark complexity analysis performance."""
        results = {
            "files": {},
            "total_execution_time": 0,
            "total_memory_usage": 0,
            "total_cpu_usage": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
        }

        for test_file in test_files:
            try:
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                start_cpu = psutil.cpu_percent()

                # Run complexity analysis
                result = self.complexity_analyzer.analyze_complexity(test_file)

                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                memory_usage = end_memory - start_memory
                cpu_usage = (start_cpu + end_cpu) / 2

                file_metrics = PerformanceMetrics(
                    execution_time=execution_time,
                    memory_usage=memory_usage,
                    cpu_usage=cpu_usage,
                    file_size=os.path.getsize(test_file),
                    success=result["analysis_success"],
                )

                results["files"][test_file] = file_metrics
                results["total_execution_time"] += execution_time
                results["total_memory_usage"] += memory_usage
                results["total_cpu_usage"] += cpu_usage

                if result["analysis_success"]:
                    results["successful_analyses"] += 1
                else:
                    results["failed_analyses"] += 1

            except Exception as e:
                file_metrics = PerformanceMetrics(
                    execution_time=0,
                    memory_usage=0,
                    cpu_usage=0,
                    file_size=0,
                    success=False,
                    error=str(e),
                )
                results["files"][test_file] = file_metrics
                results["failed_analyses"] += 1

        return results

    def _calculate_overall_performance(
        self, component_benchmarks: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall performance metrics."""
        overall = {
            "total_execution_time": 0,
            "total_memory_usage": 0,
            "total_cpu_usage": 0,
            "component_performance": {},
            "performance_score": 0,
        }

        # Aggregate component metrics
        for component_name, benchmark in component_benchmarks.items():
            if "total_execution_time" in benchmark:
                # Individual file benchmarks
                overall["total_execution_time"] += benchmark["total_execution_time"]
                overall["total_memory_usage"] += benchmark["total_memory_usage"]
                overall["total_cpu_usage"] += benchmark["total_cpu_usage"]

                overall["component_performance"][component_name] = {
                    "execution_time": benchmark["total_execution_time"],
                    "memory_usage": benchmark["total_memory_usage"],
                    "cpu_usage": benchmark["total_cpu_usage"],
                }
            else:
                # Single operation benchmarks
                overall["total_execution_time"] += benchmark["execution_time"]
                overall["total_memory_usage"] += benchmark["memory_usage"]
                overall["total_cpu_usage"] += benchmark["cpu_usage"]

                overall["component_performance"][component_name] = {
                    "execution_time": benchmark["execution_time"],
                    "memory_usage": benchmark["memory_usage"],
                    "cpu_usage": benchmark["cpu_usage"],
                }

        # Calculate performance score (0-100, higher is better)
        # Base score: 100
        # Deduct for execution time > 10s
        # Deduct for memory usage > 100MB
        # Deduct for CPU usage > 50%

        performance_score = 100

        if overall["total_execution_time"] > 10:
            performance_score -= min(30, (overall["total_execution_time"] - 10) * 2)

        if overall["total_memory_usage"] > 100:
            performance_score -= min(30, (overall["total_memory_usage"] - 100) * 0.3)

        if overall["total_cpu_usage"] > 50:
            performance_score -= min(20, (overall["total_cpu_usage"] - 50) * 0.4)

        overall["performance_score"] = max(0, performance_score)

        return overall

    def _identify_bottlenecks(
        self, component_benchmarks: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []

        # Define thresholds
        execution_threshold = 2.0  # seconds
        memory_threshold = 50.0  # MB
        cpu_threshold = 30.0  # percentage

        for component_name, benchmark in component_benchmarks.items():
            if "total_execution_time" in benchmark:
                # Check execution time
                if benchmark["total_execution_time"] > execution_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "execution_time",
                            "value": benchmark["total_execution_time"],
                            "threshold": execution_threshold,
                            "severity": (
                                "high"
                                if benchmark["total_execution_time"]
                                > execution_threshold * 2
                                else "medium"
                            ),
                        }
                    )

                # Check memory usage
                if benchmark["total_memory_usage"] > memory_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "memory_usage",
                            "value": benchmark["total_memory_usage"],
                            "threshold": memory_threshold,
                            "severity": (
                                "high"
                                if benchmark["total_memory_usage"]
                                > memory_threshold * 2
                                else "medium"
                            ),
                        }
                    )

                # Check CPU usage
                if benchmark["total_cpu_usage"] > cpu_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "cpu_usage",
                            "value": benchmark["total_cpu_usage"],
                            "threshold": cpu_threshold,
                            "severity": (
                                "high"
                                if benchmark["total_cpu_usage"] > cpu_threshold * 2
                                else "medium"
                            ),
                        }
                    )
            else:
                # Single operation benchmarks
                if benchmark["execution_time"] > execution_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "execution_time",
                            "value": benchmark["execution_time"],
                            "threshold": execution_threshold,
                            "severity": (
                                "high"
                                if benchmark["execution_time"] > execution_threshold * 2
                                else "medium"
                            ),
                        }
                    )

                if benchmark["memory_usage"] > memory_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "memory_usage",
                            "value": benchmark["memory_usage"],
                            "threshold": memory_threshold,
                            "severity": (
                                "high"
                                if benchmark["memory_usage"] > memory_threshold * 2
                                else "medium"
                            ),
                        }
                    )

                if benchmark["cpu_usage"] > cpu_threshold:
                    bottlenecks.append(
                        {
                            "component": component_name,
                            "type": "cpu_usage",
                            "value": benchmark["cpu_usage"],
                            "threshold": cpu_threshold,
                            "severity": (
                                "high"
                                if benchmark["cpu_usage"] > cpu_threshold * 2
                                else "medium"
                            ),
                        }
                    )

        return bottlenecks

    def _generate_optimization_recommendations(
        self, bottlenecks: List[Dict[str, Any]], overall_performance: Dict[str, Any]
    ) -> List[str]:
        """Generate optimization recommendations based on bottlenecks."""
        recommendations = []

        # General recommendations based on overall performance
        if overall_performance["performance_score"] < 70:
            recommendations.append(
                "Overall performance is below target. Consider implementing caching strategies."
            )

        if overall_performance["total_execution_time"] > 10:
            recommendations.append(
                "Total execution time is high. Consider parallel processing for independent operations."
            )

        if overall_performance["total_memory_usage"] > 100:
            recommendations.append(
                "Memory usage is high. Consider implementing memory pooling and cleanup strategies."
            )

        # Specific recommendations based on bottlenecks
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "execution_time":
                if bottleneck["component"] == "control_flow":
                    recommendations.append(
                        f"Control flow analysis is slow ({bottleneck['value']:.2f}s). Consider AST caching and incremental analysis."
                    )
                elif bottleneck["component"] == "multi_file":
                    recommendations.append(
                        f"Multi-file analysis is slow ({bottleneck['value']:.2f}s). Consider parallel file processing and dependency caching."
                    )
                elif bottleneck["component"] == "uml_generation":
                    recommendations.append(
                        f"UML generation is slow ({bottleneck['value']:.2f}s). Consider template caching and lazy diagram generation."
                    )
                elif bottleneck["component"] == "complexity":
                    recommendations.append(
                        f"Complexity analysis is slow ({bottleneck['value']:.2f}s). Consider result caching and selective analysis."
                    )

            elif bottleneck["type"] == "memory_usage":
                recommendations.append(
                    f"{bottleneck['component'].title()} uses excessive memory ({bottleneck['value']:.1f}MB). Implement memory-efficient data structures."
                )

            elif bottleneck["type"] == "cpu_usage":
                recommendations.append(
                    f"{bottleneck['component'].title()} uses excessive CPU ({bottleneck['value']:.1f}%). Consider implementing async processing and CPU throttling."
                )

        # Add general optimization strategies
        recommendations.extend(
            [
                "Implement result caching for repeated analyses",
                "Use lazy loading for large data structures",
                "Consider parallel processing for independent operations",
                "Implement progress tracking for long-running operations",
                "Add memory monitoring and cleanup routines",
            ]
        )

        return list(set(recommendations))  # Remove duplicates

    def generate_performance_report(self, benchmark_results: Dict[str, Any]) -> str:
        """Generate comprehensive performance report."""
        report = f"""
Performance Benchmark Report
===========================
Timestamp: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(benchmark_results["benchmark_timestamp"]))}
Total Test Files: {benchmark_results["total_files"]}

Overall Performance:
-------------------
Performance Score: {benchmark_results["overall_performance"]["performance_score"]:.1f}/100
Total Execution Time: {benchmark_results["overall_performance"]["total_execution_time"]:.2f}s
Total Memory Usage: {benchmark_results["overall_performance"]["total_memory_usage"]:.1f}MB
Total CPU Usage: {benchmark_results["overall_performance"]["total_cpu_usage"]:.1f}%

Component Performance:
---------------------
"""

        for component_name, performance in benchmark_results["overall_performance"][
            "component_performance"
        ].items():
            report += f"{component_name.title()}:\n"
            report += f"  Execution Time: {performance['execution_time']:.2f}s\n"
            report += f"  Memory Usage: {performance['memory_usage']:.1f}MB\n"
            report += f"  CPU Usage: {performance['cpu_usage']:.1f}%\n\n"

        # Add bottlenecks
        if benchmark_results["bottlenecks"]:
            report += "Performance Bottlenecks:\n"
            report += "----------------------\n"
            for bottleneck in benchmark_results["bottlenecks"]:
                report += f"• {bottleneck['component'].title()}: {bottleneck['type']} = {bottleneck['value']:.2f} "
                report += f"(threshold: {bottleneck['threshold']}, severity: {bottleneck['severity']})\n"

        # Add recommendations
        if benchmark_results["optimization_recommendations"]:
            report += "\nOptimization Recommendations:\n"
            report += "-----------------------------\n"
            for i, recommendation in enumerate(
                benchmark_results["optimization_recommendations"], 1
            ):
                report += f"{i}. {recommendation}\n"

        return report


def test_performance_optimizer():
    """Test the performance optimizer."""
    optimizer = PerformanceOptimizer()

    print("🚀 Testing Performance Optimization System:")
    print("=" * 60)

    # Run benchmarks
    benchmark_results = optimizer.benchmark_system_performance()

    print(f"✅ Benchmark completed!")
    print(f"Total test files: {benchmark_results['total_files']}")
    print(
        f"Performance score: {benchmark_results['overall_performance']['performance_score']:.1f}/100"
    )
    print(
        f"Total execution time: {benchmark_results['overall_performance']['total_execution_time']:.2f}s"
    )
    print(
        f"Total memory usage: {benchmark_results['overall_performance']['total_memory_usage']:.1f}MB"
    )

    print(f"\nComponent Performance:")
    for component_name, performance in benchmark_results["overall_performance"][
        "component_performance"
    ].items():
        print(
            f"  {component_name.title()}: {performance['execution_time']:.2f}s, {performance['memory_usage']:.1f}MB"
        )

    print(f"\nBottlenecks Found: {len(benchmark_results['bottlenecks'])}")
    for bottleneck in benchmark_results["bottlenecks"]:
        print(
            f"  • {bottleneck['component']}: {bottleneck['type']} = {bottleneck['value']:.2f} ({bottleneck['severity']})"
        )

    print(
        f"\nOptimization Recommendations: {len(benchmark_results['optimization_recommendations'])}"
    )
    for i, recommendation in enumerate(
        benchmark_results["optimization_recommendations"][:5], 1
    ):
        print(f"  {i}. {recommendation}")

    # Generate detailed report
    print(f"\nDetailed Performance Report:")
    report = optimizer.generate_performance_report(benchmark_results)
    print(report)

    return benchmark_results


if __name__ == "__main__":
    test_performance_optimizer()
