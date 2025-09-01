#!/usr/bin/env python3
"""
Enhanced Reverse Engineer - Fixed Version 2

Purpose: Extract complete method implementations with proper line structure
"""

import ast
import json
import logging
import os
import sys
import time
import cProfile
import pstats
import io
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict, List, Tuple
from tqdm import tqdm
import uuid

# PatternDetector import removed - not implemented


class EnhancedReverseEngineer:
    """Enhanced reverse engineer with method body extraction, line structure preservation, and real-time visualization."""

    def __init__(self):
        self.model_data = {}
        self.cached_nodes = None
        self.profiler = cProfile.Profile()
        self.profile_stats = None
        self.live_stats = {}
        self.visualization_enabled = True
        self.progress_bars = {}
        # self.pattern_detector = PatternDetector()  # Not implemented

    def enable_live_visualization(self, enabled: bool = True):
        """Enable or disable live visualization during reverse engineering."""
        self.visualization_enabled = enabled

    def _update_live_stats(self, function_name: str, call_count: int, cumulative_time: float):
        """Update live statistics for real-time visualization."""
        if not self.visualization_enabled:
            return

        if function_name not in self.live_stats:
            self.live_stats[function_name] = {
                "call_count": 0,
                "cumulative_time": 0.0,
                "last_update": time.time(),
            }

        self.live_stats[function_name]["call_count"] = call_count
        self.live_stats[function_name]["cumulative_time"] = cumulative_time
        self.live_stats[function_name]["last_update"] = time.time()

    def _display_live_dashboard(self):
        """Display a live dashboard of current profiling statistics."""
        if not self.visualization_enabled:
            return

        # Clear screen (works on most terminals)
        os.system("clear" if os.name == "posix" else "cls")

        print("🔄 LIVE REVERSE ENGINEERING DASHBOARD")
        print("=" * 60)
        print(f"⏰ Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        print()

        # Sort functions by cumulative time
        sorted_stats = sorted(self.live_stats.items(), key=lambda x: x[1]["cumulative_time"], reverse=True)

        print("📊 TOP FUNCTIONS BY EXECUTION TIME:")
        print("-" * 40)
        for i, (func_name, stats) in enumerate(sorted_stats[:10]):
            calls = stats["call_count"]
            time_ms = stats["cumulative_time"] * 1000
            print(f"  {i + 1:2d}. {func_name:<30} {calls:>6} calls  {time_ms:>8.2f}ms")

        print()
        print("📈 REAL-TIME METRICS:")
        print("-" * 40)

        total_calls = sum(stats["call_count"] for stats in self.live_stats.values())
        total_time = sum(stats["cumulative_time"] for stats in self.live_stats.values())

        print(f"  🔢 Total Function Calls: {total_calls:,}")
        print(f"  ⏱️  Total Execution Time: {total_time:.3f}s")
        print(f"  🎯 Functions Monitored: {len(self.live_stats)}")

        if total_calls > 0:
            avg_time = total_time / total_calls
            print(f"  🐌 Average Time per Call: {avg_time:.6f}s")

        print()
        print("💡 Press Ctrl+C to stop live monitoring")
        print("=" * 60)

    def _start_live_monitoring(self):
        """Start live monitoring in a separate thread."""
        if not self.visualization_enabled:
            return

        def monitor_loop():
            try:
                while True:
                    self._display_live_dashboard()
                    time.sleep(0.5)  # Update every 500ms
            except KeyboardInterrupt:
                print("\n🛑 Live monitoring stopped by user")

        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    def _display_final_summary(self):
        """Display final summary of the reverse engineering process."""
        if not self.visualization_enabled:
            return

        print("\n🎉 REVERSE ENGINEERING COMPLETED!")
        print("=" * 50)

        # Get final stats
        performance_summary = self.get_performance_summary()

        print("📊 FINAL PERFORMANCE SUMMARY:")
        print("-" * 30)
        print(f"  🔢 Total Function Calls: {performance_summary.get('total_function_calls', 0):,}")
        print(f"  ⏱️  Total Execution Time: {performance_summary.get('total_execution_time', 0):.3f}s")
        print(f"  🎯 Functions Monitored: {len(self.live_stats)}")

        print("\n🏆 TOP PERFORMERS:")
        print("-" * 30)
        for i, bottleneck in enumerate(performance_summary.get("bottlenecks", [])[:5]):
            func_name = bottleneck["function"]
            calls = bottleneck["call_count"]
            time_ms = bottleneck["cumulative_time"] * 1000
            print(f"  {i + 1}. {func_name:<25} {calls:>6} calls  {time_ms:>8.2f}ms")

        print("\n💡 Performance Insights:")
        print("-" * 30)

        # Analyze performance patterns
        bottlenecks = performance_summary.get("bottlenecks", [])
        if bottlenecks:
            top_bottleneck = bottlenecks[0]
            top_func = top_bottleneck["function"]
            top_time = top_bottleneck["cumulative_time"]
            total_time = performance_summary.get("total_execution_time", 0)

            if total_time > 0:
                percentage = (top_time / total_time) * 100
                print(f"  🎯 {top_func} accounts for {percentage:.1f}% of total time")

                if percentage > 50:
                    print(f"  ⚠️  Consider optimizing {top_func} - it's the major bottleneck")
                elif percentage > 25:
                    print(f"  💡 {top_func} is a significant contributor to execution time")
                else:
                    print(f"  ✅ {top_func} performance is acceptable")

        print("=" * 50)

    def reverse_engineer_file(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer a Python file into a comprehensive model with live visualization."""
        start_time = time.time()

        # Start profiling
        self.profiler.enable()

        # Start live monitoring if enabled
        if self.visualization_enabled:
            self._start_live_monitoring()

        try:
            print(f"🔍 Reverse engineering: {file_path}")

            # Generate unique model ID with timestamp
            model_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            print(f"🆔 Generated Model ID: {model_id} at {timestamp}")

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                source_lines = content.split("\n")

            # Parse AST
            tree = ast.parse(content)
            self.cached_nodes = list(ast.walk(tree))

            # Add model metadata
            self.model_data["model_id"] = model_id
            self.model_data["model_timestamp"] = timestamp
            self.model_data["source_file"] = file_path
            self.model_data["source_lines"] = source_lines

            # Extract comprehensive model with progress tracking
            if self.visualization_enabled:
                print("\n📊 EXTRACTION PROGRESS:")
                print("-" * 30)

            self._extract_module_docstring(tree, content)
            if self.visualization_enabled:
                print("  ✅ Module docstring extracted")

            self._extract_file_metadata(tree, content)
            if self.visualization_enabled:
                print("  ✅ File metadata extracted")

            self._extract_imports(tree)
            if self.visualization_enabled:
                print("  ✅ Imports extracted")

            self._extract_used_names(tree)
            if self.visualization_enabled:
                print("  ✅ Used names extracted")

            self._extract_module_assignments(tree)
            if self.visualization_enabled:
                print("  ✅ Module assignments extracted")

            self._extract_classes(tree, source_lines)
            if self.visualization_enabled:
                print("  ✅ Classes extracted")

            self._extract_module_functions(tree, source_lines)
            if self.visualization_enabled:
                print("  ✅ Module functions extracted")

            self._extract_file_structure(tree, content)
            if self.visualization_enabled:
                print("  ✅ File structure extracted")

            # Stop profiling and capture stats
            self.profiler.disable()
            self.profile_stats = pstats.Stats(self.profiler)

            # Add profiling information to the model
            self.model_data["profiling"] = self._capture_profiling_data()

            # Calculate processing time
            processing_time = time.time() - start_time
            self.model_data["processing_time"] = processing_time

            print(f"🆔 Model {model_id} completed with {len(self.cached_nodes)} AST nodes")

            # Final visualization
            if self.visualization_enabled:
                self._display_final_summary()

            return self.model_data

        except Exception as e:
            # Stop profiling even on error
            self.profiler.disable()
            print(f"❌ Error reverse engineering {file_path}: {e}")
            return {}

    def _extract_method_info_enhanced(self, func_node: ast.FunctionDef, source_lines: list[str]) -> Optional[dict[str, Any]]:
        """Extract comprehensive method information including body content with line structure and activity modeling"""
        try:
            # Detect test methods - only methods that start with "test_" are actual test methods
            is_test_method = func_node.name.startswith("test_")
            return_type = "None" if is_test_method else self._extract_type_annotation(func_node.returns)

            method_info = {
                "name": func_node.name,
                "signature": self._build_method_signature(func_node),
                "docstring": "",
                "decorators": [],
                "line_number": getattr(func_node, "lineno", 0),
                "return_type": return_type,
                "parameters": self._extract_parameters(func_node.args),
                "is_test_method": is_test_method,
                "activity_model": {},  # New: Activity modeling for methods
                "control_flow": {},  # New: Control flow analysis
                "behavior_patterns": [],  # New: Behavior pattern detection
            }

            # Extract method docstring
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Constant):
                    docstring = func_node.body[0].value.value
                    if isinstance(docstring, str):
                        method_info["docstring"] = docstring.strip()

            # Extract method body content for round-trip functionality with line structure
            if func_node.body:
                method_body = []
                activity_sequence = []  # Track activity sequence
                control_flow_map = {}  # Track control flow

                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        # Skip docstring lines
                        continue

                    # Analyze statement for activity modeling
                    stmt_analysis = self._analyze_statement_activity(stmt)
                    if stmt_analysis:
                        activity_sequence.append(stmt_analysis)

                    # Track control flow
                    control_info = self._analyze_control_flow(stmt)
                    if control_info:
                        control_flow_map[stmt.lineno] = control_info

                    # Convert AST node back to source code with proper line structure
                    try:
                        import astor

                        body_source = astor.to_source(stmt)
                        # Split into lines and preserve structure
                        body_lines = body_source.strip().split("\n")
                        for line in body_lines:
                            if line.strip():  # Skip empty lines
                                method_body.append(line.rstrip())
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_source = ast.unparse(stmt)
                            # Split into lines and preserve structure
                            body_lines = body_source.strip().split("\n")
                            for line in body_lines:
                                if line.strip():  # Skip empty lines
                                    method_body.append(line.rstrip())
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"

                    # Add activity modeling data
                    method_info["activity_model"] = {
                        "activity_sequence": activity_sequence,
                        "total_activities": len(activity_sequence),
                        "activity_types": self._categorize_activities(activity_sequence),
                        "complexity_score": self._calculate_complexity_score(activity_sequence),
                    }

                    # Add control flow analysis
                    method_info["control_flow"] = {
                        "flow_map": control_flow_map,
                        "has_conditionals": any(cf.get("type") == "conditional" for cf in control_flow_map.values()),
                        "has_loops": any(cf.get("type") == "loop" for cf in control_flow_map.values()),
                        "has_exceptions": any(cf.get("type") == "exception" for cf in control_flow_map.values()),
                        "nesting_depth": self._calculate_nesting_depth(control_flow_map),
                    }

                    # Detect behavior patterns
                    method_info["behavior_patterns"] = self._detect_behavior_patterns(activity_sequence, control_flow_map)

                else:
                    method_info["implementation_status"] = "skeleton"

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_method_info_enhanced: {type(e).__name__}: {e}")
            return None

    def _extract_async_method_info_enhanced(self, func_node: ast.AsyncFunctionDef, source_lines: list[str]) -> Optional[dict[str, Any]]:
        """Extract comprehensive async method information including body content with line structure"""
        try:
            # Detect test methods - only methods that start with "test_" are actual test methods
            is_test_method = func_node.name.startswith("test_")
            return_type = "None" if is_test_method else self._extract_type_annotation(func_node.returns)

            method_info = {
                "name": func_node.name,
                "signature": self._build_async_method_signature(func_node),
                "docstring": "",
                "decorators": [],
                "line_number": getattr(func_node, "lineno", 0),
                "return_type": return_type,
                "parameters": self._extract_parameters(func_node.args),
                "is_async": True,
                "is_test_method": is_test_method,
                "activity_model": {},  # New: Activity modeling for async methods
                "control_flow": {},  # New: Control flow analysis
                "behavior_patterns": [],  # New: Behavior pattern detection
            }

            # Extract method docstring
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Constant):
                    docstring = func_node.body[0].value.value
                    if isinstance(docstring, str):
                        method_info["docstring"] = docstring.strip()

            # Extract method body content for round-trip functionality with line structure
            if func_node.body:
                method_body = []
                activity_sequence = []  # Track activity sequence
                control_flow_map = {}  # Track control flow

                for stmt in func_node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        # Skip docstring lines
                        continue

                    # Analyze statement for activity modeling
                    stmt_analysis = self._analyze_statement_activity(stmt)
                    if stmt_analysis:
                        activity_sequence.append(stmt_analysis)

                    # Track control flow
                    control_info = self._analyze_control_flow(stmt)
                    if control_info:
                        control_flow_map[stmt.lineno] = control_info

                    # Convert AST node back to source code with proper line structure
                    try:
                        import astor

                        body_source = astor.to_source(stmt)
                        # Split into lines and preserve structure
                        body_lines = body_source.strip().split("\n")
                        for line in body_lines:
                            if line.strip():  # Skip empty lines
                                method_body.append(line.rstrip())
                    except ImportError:
                        # Fallback: use ast.unparse if available (Python 3.9+)
                        try:
                            body_source = ast.unparse(stmt)
                            # Split into lines and preserve structure
                            body_lines = body_source.strip().split("\n")
                            for line in body_lines:
                                if line.strip():  # Skip empty lines
                                    method_body.append(line.rstrip())
                        except AttributeError:
                            # Fallback: use string representation
                            body_line = str(stmt).strip()
                            if body_line:
                                method_body.append(body_line)

                if method_body:
                    method_info["body"] = method_body
                    method_info["implementation_status"] = "implemented"

                    # Add activity modeling data
                    method_info["activity_model"] = {
                        "activity_sequence": activity_sequence,
                        "total_activities": len(activity_sequence),
                        "activity_types": self._categorize_activities(activity_sequence),
                        "complexity_score": self._calculate_complexity_score(activity_sequence),
                    }

                    # Add control flow analysis
                    method_info["control_flow"] = {
                        "flow_map": control_flow_map,
                        "has_conditionals": any(cf.get("type") == "conditional" for cf in control_flow_map.values()),
                        "has_loops": any(cf.get("type") == "loop" for cf in control_flow_map.values()),
                        "has_exceptions": any(cf.get("type") == "exception" for cf in control_flow_map.values()),
                        "nesting_depth": self._calculate_nesting_depth(control_flow_map),
                    }

                    # Detect behavior patterns
                    method_info["behavior_patterns"] = self._detect_behavior_patterns(activity_sequence, control_flow_map)

                else:
                    method_info["implementation_status"] = "skeleton"

            # Extract decorators
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name):
                    method_info["decorators"].append(decorator.id)

            return method_info

        except Exception as e:
            print(f"🚨 ERROR in _extract_async_method_info_enhanced: {type(e).__name__}: {e}")
            return None

    def _build_method_signature(self, func_node: ast.FunctionDef) -> str:
        """Build complete method signature string"""
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":  # Skip self parameter
                param_name = arg.arg
                param_type = self._extract_type_annotation(arg.annotation)
                params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = self._extract_type_annotation(func_node.returns)

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        return f"{func_node.name}(self) -> {return_type}"

    def _build_async_method_signature(self, func_node: ast.AsyncFunctionDef) -> str:
        """Build complete async method signature string"""
        params = []
        for arg in func_node.args.args:
            if arg.arg != "self":  # Skip self parameter
                param_name = arg.arg
                param_type = self._extract_type_annotation(arg.annotation)
                params.append(f"{param_name}: {param_type}")

        # Get return type
        return_type = self._extract_type_annotation(func_node.returns)

        # Build method signature string
        param_str = ", ".join(params) if params else ""
        if param_str:
            return f"{func_node.name}(self, {param_str}) -> {return_type}"
        return f"{func_node.name}(self) -> {return_type}"

    def _extract_parameters(self, args: ast.arguments) -> list[dict[str, Any]]:
        """Extract detailed parameter information"""
        parameters = []
        for arg in args.args:
            if arg.arg != "self":
                param_info = {
                    "name": arg.arg,
                    "type": self._extract_type_annotation(arg.annotation),
                    "default": None,
                }
                parameters.append(param_info)
        return parameters

    def _extract_type_annotation(self, annotation) -> str:
        """Extract type annotation with enhanced analysis"""
        if annotation is None:
            return "Any"
        if isinstance(annotation, ast.Name):
            return annotation.id
        if isinstance(annotation, ast.Constant):
            return annotation.value
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                base_type = annotation.value.id
                if hasattr(annotation, "slice"):
                    slice_value = annotation.slice
                    if isinstance(slice_value, ast.Name):
                        return f"{base_type}[{slice_value.id}]"
                    if isinstance(slice_value, ast.Tuple):
                        slice_types = []
                        for elt in slice_value.elts:
                            if isinstance(elt, ast.Name):
                                slice_types.append(elt.id)
                            elif isinstance(elt, ast.Constant):
                                slice_types.append(str(elt.value))
                        return f"{base_type}[{', '.join(slice_types)}]"
        return "Any"

    def _extract_module_docstring(self, tree: ast.AST, content: str) -> None:
        """Extract module docstring"""
        try:
            for node in self.cached_nodes:
                if isinstance(node, ast.Module):
                    if node.body and isinstance(node.body[0], ast.Expr):
                        if isinstance(node.body[0].value, ast.Constant):
                            docstring = node.body[0].value.value
                            if isinstance(docstring, str):
                                self.model_data["module_docstring"] = docstring
                                break
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_docstring: {e}")

    def _extract_file_metadata(self, tree: ast.AST, content: str) -> None:
        """Extract file metadata"""
        try:
            lines = content.split("\n")
            self.model_data["file_metadata"] = {
                "executable": content.startswith("#!/"),
                "is_test_file": any("test" in line.lower() for line in lines),
                "has_main_block": "__main__" in content,
                "file_type": "module",
                "line_count": len(lines),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_metadata: {e}")

    def _extract_imports(self, tree: ast.AST) -> None:
        """Extract imports"""
        try:
            imports = []
            for node in self.cached_nodes:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = [alias.name for alias in node.names]
                    imports.append(f"from {module} import {', '.join(names)}")
            self.model_data["imports"] = imports
        except Exception as e:
            print(f"🚨 ERROR in _extract_imports: {e}")

    def _extract_used_names(self, tree: ast.AST) -> None:
        """Extract all names used in the code for import filtering"""
        try:
            used_names = set()

            # Extract names from all AST nodes
            for node in self.cached_nodes:
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Handle attribute access like BaseExpert.method
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)
                    used_names.add(node.attr)
                elif isinstance(node, ast.ClassDef):
                    used_names.add(node.name)
                    # Add base class names
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            used_names.add(base.id)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    used_names.add(node.name)

            self.model_data["used_names"] = list(used_names)
        except Exception as e:
            print(f"🚨 ERROR in _extract_used_names: {e}")
            self.model_data["used_names"] = []

    def _extract_module_assignments(self, tree: ast.AST) -> None:
        """Extract module assignments"""
        try:
            self.model_data["module_assignments"] = {}
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_assignments: {e}")

    def _extract_classes(self, tree: ast.AST, source_lines: list[str]) -> None:
        """Extract class information with pattern detection"""
        try:
            components = {}
            for node in self.cached_nodes:
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "responsibility": "",
                        "methods": [],
                        "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                        "class_decorators": [],
                        "implementation_status": "implemented",
                    }

                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._extract_method_info_enhanced(item, source_lines)
                            if method_info:
                                class_info["methods"].append(method_info)
                        elif isinstance(item, ast.AsyncFunctionDef):
                            method_info = self._extract_async_method_info_enhanced(item, source_lines)
                            if method_info:
                                class_info["methods"].append(method_info)

                    components[node.name] = class_info

            self.model_data["components"] = components
        except Exception as e:
            print(f"🚨 ERROR in _extract_classes: {e}")

    def _extract_module_functions(self, tree: ast.AST, source_lines: list[str]) -> None:
        """Extract module functions with pattern detection"""
        try:
            module_functions = []
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    method_info = self._extract_method_info_enhanced(node, source_lines)
                    if method_info:
                        module_functions.append(method_info)
                elif isinstance(node, ast.AsyncFunctionDef):
                    method_info = self._extract_async_method_info_enhanced(node, source_lines)
                    if method_info:
                        module_functions.append(method_info)

            self.model_data["module_functions"] = module_functions
        except Exception as e:
            print(f"🚨 ERROR in _extract_module_functions: {e}")

    def _extract_file_structure(self, tree: ast.AST, content: str) -> None:
        """Extract file structure information"""
        try:
            lines = content.split("\n")
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
            comment_lines = len([line for line in lines if line.strip().startswith("#")])
            blank_lines = len([line for line in lines if not line.strip()])

            self.model_data["file_structure"] = {
                "total_lines": len(lines),
                "code_lines": code_lines,
                "comment_lines": comment_lines,
                "blank_lines": blank_lines,
                "total_nodes": len(self.cached_nodes),
                "class_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.ClassDef)]),
                "function_nodes": len([n for n in self.cached_nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
                "import_nodes": len([n for n in self.cached_nodes if isinstance(n, (ast.Import, ast.ImportFrom))]),
                "expression_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.Expr)]),
                "assignment_nodes": len([n for n in self.cached_nodes if isinstance(n, ast.Assign)]),
            }
        except Exception as e:
            print(f"🚨 ERROR in _extract_file_structure: {e}")

    def _analyze_statement_activity(self, stmt: ast.stmt) -> Optional[dict[str, Any]]:
        """Analyze a statement for activity modeling"""
        try:
            activity_info = {
                "type": "unknown",
                "line_number": getattr(stmt, "lineno", 0),
                "description": "",
                "complexity": "simple",
            }

            if isinstance(stmt, ast.Assign):
                activity_info.update(
                    {
                        "type": "assignment",
                        "description": f"Assign to {len(stmt.targets)} target(s)",
                        "complexity": "simple" if len(stmt.targets) == 1 else "medium",
                    }
                )

            elif isinstance(stmt, ast.Expr):
                if isinstance(stmt.value, ast.Call):
                    activity_info.update(
                        {
                            "type": "function_call",
                            "description": f"Call function: {self._extract_function_name(stmt.value)}",
                            "complexity": "medium",
                        }
                    )
                elif isinstance(stmt.value, ast.Attribute):
                    activity_info.update(
                        {
                            "type": "attribute_access",
                            "description": f"Access attribute: {self._extract_attribute_name(stmt.value)}",
                            "complexity": "simple",
                        }
                    )

            elif isinstance(stmt, ast.If):
                activity_info.update(
                    {
                        "type": "conditional",
                        "description": "If statement",
                        "complexity": "medium",
                    }
                )

            elif isinstance(stmt, ast.For):
                activity_info.update({"type": "loop", "description": "For loop", "complexity": "medium"})

            elif isinstance(stmt, ast.While):
                activity_info.update(
                    {
                        "type": "loop",
                        "description": "While loop",
                        "complexity": "medium",
                    }
                )

            elif isinstance(stmt, ast.Try):
                activity_info.update(
                    {
                        "type": "exception_handling",
                        "description": "Try-except block",
                        "complexity": "high",
                    }
                )

            elif isinstance(stmt, ast.Return):
                activity_info.update(
                    {
                        "type": "return",
                        "description": "Return statement",
                        "complexity": "simple",
                    }
                )

            elif isinstance(stmt, ast.Raise):
                activity_info.update(
                    {
                        "type": "exception",
                        "description": "Raise exception",
                        "complexity": "medium",
                    }
                )

            elif isinstance(stmt, ast.Assert):
                activity_info.update(
                    {
                        "type": "assertion",
                        "description": "Assert statement",
                        "complexity": "simple",
                    }
                )

            return activity_info

        except Exception as e:
            print(f"🚨 ERROR in _analyze_statement_activity: {e}")
            return None

    def _analyze_control_flow(self, stmt: ast.stmt) -> Optional[dict[str, Any]]:
        """Analyze control flow for a statement"""
        try:
            flow_info = {
                "type": "statement",
                "line_number": getattr(stmt, "lineno", 0),
                "has_nested": False,
                "nesting_level": 0,
            }

            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.Try)):
                flow_info["type"] = "control_structure"
                flow_info["has_nested"] = self._has_nested_structures(stmt)
                flow_info["nesting_level"] = self._calculate_statement_nesting(stmt)

            elif isinstance(stmt, ast.With):
                flow_info["type"] = "context_manager"
                flow_info["has_nested"] = self._has_nested_structures(stmt)

            return flow_info

        except Exception as e:
            print(f"🚨 ERROR in _analyze_control_flow: {e}")
            return None

    def _detect_behavior_patterns(self, activity_sequence: list, control_flow: dict) -> list[str]:
        """Detect common behavior patterns in method execution"""
        patterns = []

        try:
            # Check for common patterns
            activity_types = [act.get("type") for act in activity_sequence if act]

            # Pattern: Data processing
            if "assignment" in activity_types and "function_call" in activity_types:
                patterns.append("data_processing")

            # Pattern: Validation
            if "assertion" in activity_types or "conditional" in activity_types:
                patterns.append("validation")

            # Pattern: Error handling
            if "exception_handling" in activity_types or "exception" in activity_types:
                patterns.append("error_handling")

            # Pattern: Iteration
            if "loop" in activity_types:
                patterns.append("iteration")

            # Pattern: Configuration
            if "assignment" in activity_types and len([a for a in activity_sequence if a.get("type") == "assignment"]) > 2:
                patterns.append("configuration")

            # Pattern: Logging/Monitoring
            if "function_call" in activity_types:
                call_descriptions = [a.get("description", "") for a in activity_sequence if a.get("type") == "function_call"]
                if any("log" in desc.lower() or "print" in desc.lower() for desc in call_descriptions):
                    patterns.append("logging")

            # Pattern: Resource management
            if "context_manager" in [cf.get("type") for cf in control_flow.values()]:
                patterns.append("resource_management")

        except Exception as e:
            print(f"🚨 ERROR in _detect_behavior_patterns: {e}")

        return patterns

    def _categorize_activities(self, activity_sequence: list) -> dict[str, int]:
        """Categorize activities by type"""
        categories = {}
        try:
            for activity in activity_sequence:
                if activity and "type" in activity:
                    activity_type = activity["type"]
                    categories[activity_type] = categories.get(activity_type, 0) + 1
        except Exception as e:
            print(f"🚨 ERROR in _categorize_activities: {e}")
        return categories

    def _calculate_complexity_score(self, activity_sequence: list) -> int:
        """Calculate complexity score based on activities"""
        try:
            score = 0
            for activity in activity_sequence:
                if activity:
                    complexity = activity.get("complexity", "simple")
                    if complexity == "simple":
                        score += 1
                    elif complexity == "medium":
                        score += 2
                    elif complexity == "high":
                        score += 3
            return score
        except Exception as e:
            print(f"🚨 ERROR in _calculate_complexity_score: {e}")
            return 0

    def _calculate_nesting_depth(self, control_flow: dict) -> int:
        """Calculate maximum nesting depth"""
        try:
            depths = [cf.get("nesting_level", 0) for cf in control_flow.values()]
            return max(depths) if depths else 0
        except Exception as e:
            print(f"🚨 ERROR in _calculate_nesting_depth: {e}")
            return 0

    def _has_nested_structures(self, stmt: ast.stmt) -> bool:
        """Check if statement has nested control structures"""
        try:
            for child in ast.walk(stmt):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)) and child != stmt:
                    return True
            return False
        except Exception as e:
            print(f"🚨 ERROR in _has_nested_structures: {e}")
            return False

    def _calculate_statement_nesting(self, stmt: ast.stmt) -> int:
        """Calculate nesting level of a statement"""
        try:
            level = 0
            current = stmt
            while hasattr(current, "parent"):
                current = current.parent
                if isinstance(current, (ast.If, ast.For, ast.While, ast.Try)):
                    level += 1
            return level
        except Exception as e:
            print(f"🚨 ERROR in _calculate_statement_nesting: {e}")
            return 0

    def _extract_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from call node"""
        try:
            if isinstance(call_node.func, ast.Name):
                return call_node.func.id
            elif isinstance(call_node.func, ast.Attribute):
                return call_node.func.attr
            else:
                return "unknown_function"
        except Exception as e:
            print(f"🚨 ERROR in _extract_function_name: {e}")
            return "unknown_function"

    def _extract_attribute_name(self, attr_node: ast.Attribute) -> str:
        """Extract attribute name from attribute node"""
        try:
            return attr_node.attr
        except Exception as e:
            print(f"🚨 ERROR in _extract_attribute_name: {e}")
            return "unknown_attribute"

    def _capture_profiling_data(self) -> Dict[str, Any]:
        """Capture profiling statistics and execution trace."""
        if not self.profile_stats:
            return {}

        # Capture stats to string buffer
        stats_buffer = io.StringIO()
        self.profile_stats.stream = stats_buffer
        self.profile_stats.print_stats()
        stats_output = stats_buffer.getvalue()

        # Get top functions by time
        top_functions = []
        for func, (cc, nc, tt, ct, callers) in self.profile_stats.stats.items():
            if isinstance(func, tuple):
                filename, line_num, func_name = func
                top_functions.append(
                    {
                        "function": func_name,
                        "filename": filename,
                        "line": line_num,
                        "total_time": tt,
                        "cumulative_time": ct,
                        "call_count": cc,
                    }
                )

                # Update live stats for real-time visualization
                self._update_live_stats(func_name, cc, ct)

        # Sort by cumulative time
        top_functions.sort(key=lambda x: x["cumulative_time"], reverse=True)

        return {
            "stats_output": stats_output,
            "top_functions": top_functions[:10],  # Top 10 functions
            "total_function_calls": sum(f["call_count"] for f in top_functions),
            "total_time": sum(f["total_time"] for f in top_functions),
        }

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get the execution trace from profiling data."""
        if not self.profile_stats:
            return []

        trace = []
        for func, (cc, nc, tt, ct, callers) in self.profile_stats.stats.items():
            if isinstance(func, tuple):
                filename, line_num, func_name = func
                trace.append(
                    {
                        "function": func_name,
                        "filename": filename,
                        "line": line_num,
                        "call_count": cc,
                        "total_time": tt,
                        "cumulative_time": ct,
                        "callers": list(callers.keys()) if callers else [],
                    }
                )

        return trace

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of performance characteristics."""
        if not self.profile_stats:
            return {}

        trace = self.get_execution_trace()
        if not trace:
            return {}

        # Calculate performance metrics
        total_calls = sum(item["call_count"] for item in trace)
        total_time = sum(item["total_time"] for item in trace)

        # Find bottlenecks (functions with high cumulative time)
        bottlenecks = sorted(trace, key=lambda x: x["cumulative_time"], reverse=True)[:5]

        # Find most called functions
        most_called = sorted(trace, key=lambda x: x["call_count"], reverse=True)[:5]

        return {
            "total_function_calls": total_calls,
            "total_execution_time": total_time,
            "bottlenecks": bottlenecks,
            "most_called_functions": most_called,
            "average_time_per_call": total_time / total_calls if total_calls > 0 else 0,
        }


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_reverse_engineer_fixed_v2.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Reverse engineer the file
    engineer = EnhancedReverseEngineer()
    model = engineer.reverse_engineer_file(file_path)

    # Save the model
    output_file = "enhanced_reverse_engineered_model_fixed_v2.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ Model saved to: {output_file}")
    print(f"📦 Components: {len(model.get('components', {}))}")
    print(f"📏 Total Lines: {model.get('file_structure', {}).get('total_lines', 0)}")


if __name__ == "__main__":
    import sys

    main()
