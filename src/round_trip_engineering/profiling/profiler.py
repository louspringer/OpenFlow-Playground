"""
Comprehensive Profiler for Round-Trip Engineering System.

Integrates cProfile for execution path debugging and performance analysis.
Provides real-time profiling data and comprehensive statistics.
"""

import cProfile
import pstats
import io
import logging
import time
from typing import Any, Dict, List, Optional, Callable
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class Profiler:
    """
    Comprehensive profiler using cProfile for debugging and performance analysis.

    Provides execution path debugging, performance bottlenecks identification,
    and comprehensive statistics for the round-trip engineering system.
    """

    def __init__(self):
        """Initialize the profiler."""
        self.profiler = cProfile.Profile()
        self.profiler_stats = None
        self.start_time = None
        self.operation_name = None
        self.enabled = True

        logger.info("✅ Profiler initialized with cProfile integration")

    def start_profiling(self, operation_name: str = "unnamed_operation") -> None:
        """
        Start profiling for a specific operation.

        Args:
            operation_name: Name of the operation being profiled
        """
        if not self.enabled:
            return

        try:
            self.operation_name = operation_name
            self.start_time = time.time()
            self.profiler.enable()

            logger.info(f"🔍 Started profiling: {operation_name}")

        except Exception as e:
            logger.error(f"❌ Failed to start profiling: {e}")

    def stop_profiling(self) -> None:
        """Stop profiling and collect statistics."""
        if not self.enabled:
            return

        try:
            self.profiler.disable()

            # Collect profiling statistics
            s = io.StringIO()
            self.profiler_stats = pstats.Stats(self.profiler, stream=s)

            # Calculate execution time
            execution_time = time.time() - self.start_time if self.start_time else 0

            logger.info(f"✅ Profiling completed: {self.operation_name} in {execution_time:.4f}s")

        except Exception as e:
            logger.error(f"❌ Failed to stop profiling: {e}")

    @contextmanager
    def profile_operation(self, operation_name: str):
        """
        Context manager for profiling operations.

        Args:
            operation_name: Name of the operation to profile

        Yields:
            Profiler instance for the operation
        """
        try:
            self.start_profiling(operation_name)
            yield self
        finally:
            self.stop_profiling()

    def get_profiling_stats(self) -> Optional[pstats.Stats]:
        """
        Get profiling statistics from the last operation.

        Returns:
            pstats.Stats object with profiling data, or None if no data available
        """
        return self.profiler_stats

    def print_profiling_summary(self, top_n: int = 10) -> None:
        """
        Print profiling summary to console.

        Args:
            top_n: Number of top functions to display
        """
        if not self.profiler_stats:
            logger.warning("📊 No profiling data available")
            return

        try:
            print(f"\n📊 PROFILING SUMMARY: {self.operation_name}")
            print("=" * 60)

            # Sort by cumulative time and print top functions
            self.profiler_stats.sort_stats("cumulative")
            self.profiler_stats.print_stats(top_n)

            # Print callers and callees for top function
            if top_n > 0:
                print(f"\n🔍 TOP FUNCTION CALLERS:")
                self.profiler_stats.print_callers(top_n)

                print(f"\n🔍 TOP FUNCTION CALLEES:")
                self.profiler_stats.print_callees(top_n)

        except Exception as e:
            logger.error(f"❌ Failed to print profiling summary: {e}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive performance metrics.

        Returns:
            Dictionary containing performance metrics
        """
        if not self.profiler_stats:
            return {"error": "No profiling data available"}

        try:
            # Get basic stats
            stats = self.profiler_stats.stats

            # Calculate metrics
            total_calls = sum(stats[func][0] for func in stats)
            total_time = sum(stats[func][3] for func in stats)

            # Find top functions by time
            function_times = []
            for func, (calls, ncalls, tottime, cumtime, *rest) in stats.items():
                function_times.append(
                    {
                        "function": f"{func[0]}.{func[1]}:{func[2]}",
                        "calls": calls,
                        "total_time": tottime,
                        "cumulative_time": cumtime,
                        "time_per_call": tottime / calls if calls > 0 else 0,
                    }
                )

            # Sort by cumulative time
            function_times.sort(key=lambda x: x["cumulative_time"], reverse=True)

            return {
                "operation_name": self.operation_name,
                "total_calls": total_calls,
                "total_time": total_time,
                "top_functions": function_times[:10],
                "execution_time": (time.time() - self.start_time if self.start_time else 0),
            }

        except Exception as e:
            logger.error(f"❌ Failed to get performance metrics: {e}")
            return {"error": str(e)}

    def profile_function(self, func: Callable, *args, **kwargs) -> Any:
        """
        Profile a specific function call.

        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        operation_name = f"function_{func.__name__}"

        with self.profile_operation(operation_name):
            result = func(*args, **kwargs)

        return result

    def enable_profiling(self) -> None:
        """Enable profiling."""
        self.enabled = True
        logger.info("✅ Profiling enabled")

    def disable_profiling(self) -> None:
        """Disable profiling."""
        self.enabled = False
        logger.info("⏸️ Profiling disabled")

    def reset_profiler(self) -> None:
        """Reset profiler state."""
        self.profiler = cProfile.Profile()
        self.profiler_stats = None
        self.start_time = None
        self.operation_name = None
        logger.info("🔄 Profiler reset")

    def export_stats(self, filename: str) -> bool:
        """
        Export profiling statistics to a file.

        Args:
            filename: Output filename for statistics

        Returns:
            True if export successful, False otherwise
        """
        if not self.profiler_stats:
            logger.warning("📊 No profiling data to export")
            return False

        try:
            self.profiler_stats.dump_stats(filename)
            logger.info(f"💾 Profiling stats exported to: {filename}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export profiling stats: {e}")
            return False

    def get_function_call_graph(self) -> Dict[str, Any]:
        """
        Get function call graph for visualization.

        Returns:
            Dictionary representing the call graph
        """
        if not self.profiler_stats:
            return {"error": "No profiling data available"}

        try:
            stats = self.profiler_stats.stats
            call_graph = {}

            for func, (calls, ncalls, tottime, cumtime, *rest) in stats.items():
                func_name = f"{func[0]}.{func[1]}:{func[2]}"
                call_graph[func_name] = {
                    "calls": calls,
                    "total_time": tottime,
                    "cumulative_time": cumtime,
                    "callers": [],
                    "callees": [],
                }

            # Build call relationships (simplified - would need more complex analysis)
            return {
                "nodes": list(call_graph.keys()),
                "edges": [],  # Would need to analyze call patterns
                "metrics": call_graph,
            }

        except Exception as e:
            logger.error(f"❌ Failed to get call graph: {e}")
            return {"error": str(e)}
