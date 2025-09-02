#!/usr/bin/env python3
"""
Enhanced Reverse Engineer - Orchestrator Only

Purpose: Orchestrate the reverse engineering process using focused modules.
This is now a lean orchestrator that delegates to focused modules.
"""

import ast
import json
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict, List, Tuple
from tqdm import tqdm

from .profiler import Profiler
from .ast_extractor import ASTExtractor

# Setup logger for RM compliance
logger = logging.getLogger(__name__)


class EnhancedReverseEngineer:
    """Enhanced reverse engineer - now just an orchestrator using focused modules."""

    def __init__(self):
        self.model_data = {}
        self.cached_nodes = None
        self.profiler = Profiler()  # Use focused Profiler class
        self.ast_extractor = ASTExtractor()  # Use focused AST Extractor class
        self.dashboard = None
        self.progress_bars = {}

    def enable_live_visualization(self, enabled: bool = True):
        """Enable or disable live visualization using visualization domain dashboard."""
        if enabled and self.dashboard is None:
            try:
                from src.visualization.live_diagnostic_dashboard import LiveDiagnosticDashboard

                self.dashboard = LiveDiagnosticDashboard()
                logger.info("✅ Live visualization enabled via dashboard")
            except Exception as e:
                logger.warning(f"Failed to enable live visualization: {e}")
        elif not enabled and self.dashboard is not None:
            self.dashboard.stop()
            self.dashboard = None
            logger.info("✅ Live visualization disabled")

    def _update_live_stats(self, function_name: str, call_count: int, cumulative_time: float):
        """Update live statistics for real-time visualization."""
        # Update profiler stats
        self.profiler.update_live_stats(function_name, call_count, cumulative_time)

        # Send to dashboard if available
        if self.dashboard is not None:
            try:
                self.dashboard.add_metric(
                    name=f"function_{function_name}",
                    value=f"{call_count} calls, {cumulative_time:.3f}s",
                    category="profiling",
                    metadata={"function_name": function_name, "call_count": call_count, "cumulative_time": cumulative_time, "last_update": time.time()},
                )
            except Exception as e:
                logger.warning(f"Failed to send metric to dashboard: {e}")

    def _display_live_dashboard(self):
        """Send metrics to visualization domain dashboard instead of local display."""
        if self.dashboard is None:
            return

        try:
            # Send profiling metrics to dashboard
            live_stats = self.profiler.get_live_stats()
            for func_name, stats in live_stats.items():
                self.dashboard.add_metric(
                    name=f"function_{func_name}",
                    value=f"{stats['call_count']} calls, {stats['cumulative_time']:.3f}s",
                    category="profiling",
                    metadata={"function_name": func_name, "call_count": stats["call_count"], "cumulative_time": stats["cumulative_time"], "last_update": stats["last_update"]},
                )
        except Exception as e:
            logger.warning(f"Failed to send metrics to dashboard: {e}")

    def _start_live_monitoring(self):
        """Start live monitoring using visualization domain dashboard."""
        if self.dashboard is None:
            return

        try:
            if not self.dashboard.is_active():
                self.dashboard.start()
                logger.info("✅ Live monitoring started via dashboard")
        except Exception as e:
            logger.warning(f"Failed to start live monitoring: {e}")

    def _stop_live_monitoring(self):
        """Stop live monitoring cleanly via visualization domain dashboard."""
        if self.dashboard is not None:
            try:
                self.dashboard.stop()
                logger.info("✅ Live monitoring stopped via dashboard")
            except Exception as e:
                logger.warning(f"Failed to stop live monitoring: {e}")

    def __del__(self):
        """Cleanup method for RM compliance."""
        self._stop_live_monitoring()

    def __enter__(self):
        """Context manager entry for RM compliance."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit for RM compliance."""
        self._stop_live_monitoring()
        return False  # Don't suppress exceptions

    def _display_final_summary(self):
        """Display final summary of the reverse engineering process."""
        if self.dashboard is None:
            return

        try:
            # Get performance summary from profiler
            performance_summary = self.profiler.get_profiling_data().get("summary", {})

            print("\n🎯 FINAL PERFORMANCE SUMMARY:")
            print("=" * 50)
            print(f"  🔢 Total Function Calls: {performance_summary.get('total_function_calls', 0):,}")
            print(f"  ⏱️  Total Execution Time: {performance_summary.get('total_execution_time', 0):.3f}s")
            print(f"  🎯 Functions Monitored: {len(self.profiler.get_live_stats())}")

            print("\n🏆 TOP PERFORMERS:")
            bottlenecks = self.profiler.get_profiling_data().get("bottlenecks", [])
            for i, bottleneck in enumerate(bottlenecks[:5], 1):
                func_name = bottleneck["function"]
                call_count = bottleneck.get("call_count", 0)
                cumulative_time = bottleneck.get("cumulative_time", 0)
                print(f"  {i}. {func_name}: {call_count} calls, {cumulative_time:.3f}s")

            # Show top bottleneck analysis
            if bottlenecks:
                top_bottleneck = bottlenecks[0]
                top_func = top_bottleneck["function"]
                top_time = top_bottleneck.get("cumulative_time", 0)
                total_time = performance_summary.get("total_execution_time", 0)

                if total_time > 0:
                    percentage = (top_time / total_time) * 100
                    print(f"\n💡 PERFORMANCE INSIGHT:")
                    print(f"  🎯 {top_func} accounts for {percentage:.1f}% of total execution time")
                    if percentage > 50:
                        print(f"  💡 {top_func} is a significant contributor to execution time")

        except Exception as e:
            logger.warning(f"Failed to display final summary: {e}")

    def reverse_engineer_file(self, file_path: str) -> Dict[str, Any]:
        """Reverse engineer a Python file into a comprehensive model with live visualization."""
        start_time = time.time()

        try:
            # Generate unique model ID with timestamp
            model_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            print(f"🆔 Generated Model ID: {model_id} at {timestamp}")

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                source_lines = content.split("\n")

            # Parse AST using focused extractor
            tree = self.ast_extractor.parse_file(file_path)
            if tree is None:
                print(f"❌ Failed to parse {file_path}")
                return {}

            self.cached_nodes = list(ast.walk(tree))

            # Add model metadata
            self.model_data["model_id"] = model_id
            self.model_data["model_timestamp"] = timestamp
            self.model_data["source_file"] = file_path

            # Start profiling
            self.profiler.start_profiling()

            # Start live monitoring if dashboard is available
            if self.dashboard is not None:
                self._start_live_monitoring()

            # Extract comprehensive model with progress tracking
            if self.dashboard is not None:
                print("\n📊 EXTRACTION PROGRESS:")
                print("-" * 30)

            # Extract using focused AST extractor
            self.model_data["module_docstring"] = self.ast_extractor.extract_module_docstring(tree, content)
            if self.dashboard is not None:
                print("  ✅ Module docstring extracted")

            self.model_data["file_metadata"] = self.ast_extractor.extract_file_metadata(tree, content)
            if self.dashboard is not None:
                print("  ✅ File metadata extracted")

            self.model_data["imports"] = self.ast_extractor.extract_imports(tree)
            if self.dashboard is not None:
                print("  ✅ Imports extracted")

            # Keep some legacy extraction methods for now
            self._extract_used_names(tree)
            if self.dashboard is not None:
                print("  ✅ Used names extracted")

            self._extract_module_assignments(tree)
            if self.dashboard is not None:
                print("  ✅ Module assignments extracted")

            self.model_data["classes"] = self.ast_extractor.extract_classes(tree, source_lines)
            if self.dashboard is not None:
                print("  ✅ Classes extracted")

            self.model_data["module_functions"] = self.ast_extractor.extract_module_functions(tree, source_lines)
            if self.dashboard is not None:
                print("  ✅ Module functions extracted")

            self._extract_file_structure(tree, content)
            if self.dashboard is not None:
                print("  ✅ File structure extracted")

            # Stop profiling and capture stats
            self.profiler.stop_profiling()

            # Add profiling information to the model
            self.model_data["profiling"] = self.profiler.get_profiling_data()

            # Calculate processing time
            processing_time = time.time() - start_time
            self.model_data["processing_time"] = processing_time

            print(f"🆔 Model {model_id} completed with {len(self.cached_nodes)} AST nodes")

            # Final visualization
            if self.dashboard is not None:
                self._display_final_summary()

            return self.model_data

        except Exception as e:
            # Stop profiling even on error
            self.profiler.stop_profiling()
            print(f"❌ Error reverse engineering {file_path}: {e}")
            return {}

    def _extract_used_names(self, tree: ast.AST) -> None:
        """Extract all names used in the code for import filtering"""
        try:
            used_names = set()

            # Extract names from all AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    used_names.add(node.attr)

            self.model_data["used_names"] = list(used_names)
        except Exception as e:
            print(f"🚨 ERROR in _extract_used_names: {e}")

    def _extract_module_assignments(self, tree: ast.AST) -> None:
        """Extract module assignments"""
        try:
            self.model_data["module_assignments"] = {}
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_assignments: {e}")

    def _extract_file_structure(self, tree: ast.AST, content: str) -> None:
        """Extract file structure information"""
        try:
            lines = content.split("\n")
            self.model_data["file_structure"] = {
                "total_lines": len(lines),
                "non_empty_lines": len([line for line in lines if line.strip()]),
                "comment_lines": len([line for line in lines if line.strip().startswith("#")]),
                "import_lines": len([line for line in lines if line.strip().startswith(("import ", "from "))]),
                "class_count": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                "function_count": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                "async_function_count": len([node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_structure: {e}")

    def _capture_profiling_data(self) -> Dict[str, Any]:
        """Capture profiling statistics and execution trace."""
        # Use the profiler's data
        return self.profiler.get_profiling_data()

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get the execution trace from profiling data."""
        # Use the profiler's data
        profiler_data = self.profiler.get_profiling_data()
        return profiler_data.get("top_functions", [])

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of performance characteristics."""
        # Use the profiler's data
        profiler_data = self.profiler.get_profiling_data()
        return profiler_data.get("summary", {})


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_reverse_engineer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Reverse engineer the file
    engineer = EnhancedReverseEngineer()
    model = engineer.reverse_engineer_file(file_path)

    # Save the model
    output_file = "enhanced_reverse_engineered_model.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ Model saved to: {output_file}")
    print(f"📦 Components: {len(model.get('components', {}))}")
    print(f"📏 Total Lines: {model.get('file_structure', {}).get('total_lines', 0)}")


if __name__ == "__main__":
    import sys

    main()
