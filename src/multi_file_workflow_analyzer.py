#!/usr/bin/env python3
"""
Multi-File Workflow Analysis System

Addresses UC-6 important risk use case for analyzing workflows across multiple files.
This system tests pydeps cross-file capabilities, implements circular dependency detection,
and validates namespace resolution.
"""

import os
import ast
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import subprocess
import networkx as nx
from collections import defaultdict


class MultiFileWorkflowAnalyzer:
    """Analyzes workflows across multiple Python files."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.dependency_graph = nx.DiGraph()
        self.circular_dependencies = []
        self.namespace_resolution = {}
        self.cross_file_calls = {}

    def analyze_project_workflow(self, source_dir: str = "src") -> Dict[str, Any]:
        """
        Analyze workflow across multiple files in a project.

        Args:
            source_dir: Directory containing source files

        Returns:
            Multi-file workflow analysis results
        """
        try:
            source_path = self.project_root / source_dir
            if not source_path.exists():
                return {
                    "error": f"Source directory {source_dir} not found",
                    "analysis_success": False,
                }

            # Find all Python files
            python_files = list(source_path.rglob("*.py"))

            # Analyze dependencies using pydeps
            dependency_analysis = self._analyze_dependencies_with_pydeps(python_files)

            # Detect circular dependencies
            circular_deps = self._detect_circular_dependencies()

            # Analyze namespace resolution
            namespace_analysis = self._analyze_namespace_resolution(python_files)

            # Analyze cross-file function calls
            cross_file_calls = self._analyze_cross_file_calls(python_files)

            # Generate workflow graph
            workflow_graph = self._generate_workflow_graph(python_files)

            analysis_result = {
                "source_directory": str(source_path),
                "total_files": len(python_files),
                "python_files": [str(f) for f in python_files],
                "dependency_analysis": dependency_analysis,
                "circular_dependencies": circular_deps,
                "namespace_resolution": namespace_analysis,
                "cross_file_calls": cross_file_calls,
                "workflow_graph": workflow_graph,
                "analysis_success": True,
            }

            return analysis_result

        except Exception as e:
            return {"error": str(e), "analysis_success": False}

    def _analyze_dependencies_with_pydeps(
        self, python_files: List[Path]
    ) -> Dict[str, Any]:
        """Analyze dependencies using pydeps."""
        try:
            # Use pydeps to analyze the entire source directory
            source_dir = python_files[0].parent if python_files else Path("src")

            # Run pydeps on the source directory
            result = subprocess.run(
                ["uv", "run", "pydeps", str(source_dir), "--show-dot"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                # Parse the dot output to extract dependencies
                dependencies = self._parse_pydeps_output(result.stdout)

                # Build dependency graph
                self._build_dependency_graph(dependencies)

                return {
                    "pydeps_success": True,
                    "total_dependencies": len(dependencies),
                    "dependency_graph_nodes": self.dependency_graph.number_of_nodes(),
                    "dependency_graph_edges": self.dependency_graph.number_of_edges(),
                    "raw_output": (
                        result.stdout[:500] + "..."
                        if len(result.stdout) > 500
                        else result.stdout
                    ),
                }
            else:
                return {
                    "pydeps_success": False,
                    "error": result.stderr,
                    "return_code": result.returncode,
                }

        except Exception as e:
            return {"pydeps_success": False, "error": str(e)}

    def _parse_pydeps_output(self, dot_output: str) -> List[Tuple[str, str]]:
        """Parse pydeps dot output to extract dependencies."""
        dependencies = []

        # Simple parsing of dot format
        lines = dot_output.split("\n")
        for line in lines:
            if " -> " in line:
                # Extract source and target from "source -> target" format
                parts = line.split(" -> ")
                if len(parts) == 2:
                    source = parts[0].strip()
                    target = parts[1].strip()

                    # Clean up the names
                    source = self._clean_dependency_name(source)
                    target = self._clean_dependency_name(target)

                    if source and target and source != target:
                        dependencies.append((source, target))

        return dependencies

    def _clean_dependency_name(self, name: str) -> str:
        """Clean up dependency names from pydeps output."""
        # Remove quotes and extra formatting
        name = name.strip('"')
        name = name.strip("'")

        # Remove file extensions
        if name.endswith(".py"):
            name = name[:-3]

        # Remove path prefixes
        if "/" in name:
            name = name.split("/")[-1]

        return name

    def _build_dependency_graph(self, dependencies: List[Tuple[str, str]]):
        """Build NetworkX dependency graph."""
        for source, target in dependencies:
            self.dependency_graph.add_edge(source, target)

    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the graph."""
        try:
            # Find simple cycles
            cycles = list(nx.simple_cycles(self.dependency_graph))

            # Find strongly connected components (more comprehensive)
            scc = list(nx.strongly_connected_components(self.dependency_graph))

            # Filter out single-node components
            circular_components = [comp for comp in scc if len(comp) > 1]

            return {
                "simple_cycles": cycles,
                "strongly_connected_components": circular_components,
                "total_circular_deps": len(cycles) + len(circular_components),
            }

        except Exception as e:
            return {
                "error": str(e),
                "simple_cycles": [],
                "strongly_connected_components": [],
                "total_circular_deps": 0,
            }

    def _analyze_namespace_resolution(self, python_files: List[Path]) -> Dict[str, Any]:
        """Analyze namespace resolution across files."""
        namespace_analysis = {
            "imports": defaultdict(list),
            "exports": defaultdict(list),
            "namespace_conflicts": [],
            "unresolved_imports": [],
        }

        for file_path in python_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                # Parse AST
                tree = ast.parse(content)

                # Extract imports
                imports = self._extract_imports(tree)
                for imp in imports:
                    namespace_analysis["imports"][str(file_path)].append(imp)

                # Extract exports (functions, classes, variables)
                exports = self._extract_exports(tree)
                namespace_analysis["exports"][str(file_path)].extend(exports)

            except Exception as e:
                namespace_analysis["unresolved_imports"].append(
                    {"file": str(file_path), "error": str(e)}
                )

        # Check for namespace conflicts
        namespace_analysis["namespace_conflicts"] = self._detect_namespace_conflicts(
            namespace_analysis["exports"]
        )

        return namespace_analysis

    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements from AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "lineno": getattr(node, "lineno", 0),
                        }
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(
                        {
                            "type": "from_import",
                            "module": module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "lineno": getattr(node, "lineno", 0),
                        }
                    )

        return imports

    def _extract_exports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract exportable items from AST."""
        exports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                exports.append(
                    {
                        "type": "function",
                        "name": node.name,
                        "lineno": getattr(node, "lineno", 0),
                    }
                )
            elif isinstance(node, ast.ClassDef):
                exports.append(
                    {
                        "type": "class",
                        "name": node.name,
                        "lineno": getattr(node, "lineno", 0),
                    }
                )
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        exports.append(
                            {
                                "type": "variable",
                                "name": target.id,
                                "lineno": getattr(node, "lineno", 0),
                            }
                        )

        return exports

    def _detect_namespace_conflicts(
        self, exports: Dict[str, List]
    ) -> List[Dict[str, Any]]:
        """Detect namespace conflicts across files."""
        conflicts = []

        # Build name to file mapping
        name_to_files = defaultdict(list)
        for file_path, file_exports in exports.items():
            for export in file_exports:
                name_to_files[export["name"]].append(
                    {
                        "file": file_path,
                        "type": export["type"],
                        "lineno": export["lineno"],
                    }
                )

        # Check for conflicts
        for name, occurrences in name_to_files.items():
            if len(occurrences) > 1:
                conflicts.append(
                    {
                        "name": name,
                        "occurrences": occurrences,
                        "conflict_type": "duplicate_name",
                    }
                )

        return conflicts

    def _analyze_cross_file_calls(self, python_files: List[Path]) -> Dict[str, Any]:
        """Analyze function calls across different files."""
        cross_file_calls = {
            "inter_file_calls": [],
            "call_graph": defaultdict(list),
            "entry_points": [],
            "exit_points": [],
        }

        # Build a mapping of function definitions to files
        function_locations = {}
        for file_path in python_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                tree = ast.parse(content)
                functions = self._extract_function_definitions(tree)

                for func in functions:
                    function_locations[func["name"]] = {
                        "file": str(file_path),
                        "lineno": func["lineno"],
                    }

            except Exception as e:
                continue

        # Analyze function calls in each file
        for file_path in python_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                tree = ast.parse(content)
                calls = self._extract_function_calls(tree)

                for call in calls:
                    if call["function"] in function_locations:
                        target_file = function_locations[call["function"]]["file"]
                        if target_file != str(file_path):
                            cross_file_calls["inter_file_calls"].append(
                                {
                                    "source_file": str(file_path),
                                    "target_file": target_file,
                                    "function": call["function"],
                                    "lineno": call["lineno"],
                                }
                            )

                            cross_file_calls["call_graph"][str(file_path)].append(
                                {"target": target_file, "function": call["function"]}
                            )

            except Exception as e:
                continue

        # Identify entry and exit points
        cross_file_calls["entry_points"] = self._identify_entry_points(
            function_locations
        )
        cross_file_calls["exit_points"] = self._identify_exit_points(function_locations)

        return cross_file_calls

    def _extract_function_definitions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from AST."""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(
                    {
                        "name": node.name,
                        "lineno": getattr(node, "lineno", 0),
                        "args": [arg.arg for arg in node.args.args],
                    }
                )

        return functions

    def _extract_function_calls(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function calls from AST."""
        calls = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, "id"):
                    calls.append(
                        {"function": node.func.id, "lineno": getattr(node, "lineno", 0)}
                    )

        return calls

    def _identify_entry_points(self, function_locations: Dict[str, Dict]) -> List[str]:
        """Identify potential entry points (functions not called by others)."""
        called_functions = set()

        # Find all called functions
        for file_path in function_locations.values():
            # This is a simplified approach - in practice, we'd need to analyze all calls
            pass

        # Entry points are functions that are defined but not called
        entry_points = []
        for func_name, location in function_locations.items():
            if func_name not in called_functions:
                entry_points.append(f"{location['file']}:{func_name}")

        return entry_points

    def _identify_exit_points(self, function_locations: Dict[str, Dict]) -> List[str]:
        """Identify potential exit points (functions that don't call others)."""
        # This would require analyzing the call graph to find leaf functions
        # For now, return a placeholder
        return ["placeholder_exit_points"]

    def _generate_workflow_graph(self, python_files: List[Path]) -> Dict[str, Any]:
        """Generate a comprehensive workflow graph."""
        workflow_graph = {
            "nodes": [],
            "edges": [],
            "file_dependencies": {},
            "function_dependencies": {},
            "module_hierarchy": {},
        }

        # Add file nodes
        for file_path in python_files:
            workflow_graph["nodes"].append(
                {
                    "id": str(file_path),
                    "type": "file",
                    "name": file_path.name,
                    "path": str(file_path),
                }
            )

        # Add dependency edges
        for edge in self.dependency_graph.edges():
            workflow_graph["edges"].append(
                {"source": edge[0], "target": edge[1], "type": "dependency"}
            )

        # Add cross-file call edges
        for source_file, calls in self.cross_file_calls.get("call_graph", {}).items():
            for call in calls:
                workflow_graph["edges"].append(
                    {
                        "source": source_file,
                        "target": call["target"],
                        "type": "function_call",
                        "function": call["function"],
                    }
                )

        return workflow_graph

    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report."""
        if not hasattr(self, "last_analysis_result"):
            return (
                "No analysis results available. Run analyze_project_workflow() first."
            )

        result = self.last_analysis_result

        report = f"""
Multi-File Workflow Analysis Report
==================================
Source Directory: {result.get("source_directory", "N/A")}
Total Files: {result.get("total_files", 0)}

Dependency Analysis:
-------------------
Pydeps Success: {result.get("dependency_analysis", {}).get("pydeps_success", False)}
Total Dependencies: {result.get("dependency_analysis", {}).get("total_dependencies", 0)}
Graph Nodes: {result.get("dependency_analysis", {}).get("dependency_graph_nodes", 0)}
Graph Edges: {result.get("dependency_analysis", {}).get("dependency_graph_edges", 0)}

Circular Dependencies:
---------------------
Total Circular Dependencies: {result.get("circular_dependencies", {}).get("total_circular_deps", 0)}
Simple Cycles: {len(result.get("circular_dependencies", {}).get("simple_cycles", []))}
Strongly Connected Components: {len(result.get("circular_dependencies", {}).get("strongly_connected_components", []))}

Cross-File Analysis:
-------------------
Inter-File Calls: {len(result.get("cross_file_calls", {}).get("inter_file_calls", []))}
Entry Points: {len(result.get("cross_file_calls", {}).get("entry_points", []))}
Exit Points: {len(result.get("cross_file_calls", {}).get("exit_points", []))}

Namespace Resolution:
-------------------
Total Imports: {sum(len(imports) for imports in result.get("namespace_resolution", {}).get("imports", {}).values())}
Total Exports: {sum(len(exports) for exports in result.get("namespace_resolution", {}).get("exports", {}).values())}
Namespace Conflicts: {len(result.get("namespace_resolution", {}).get("namespace_conflicts", []))}
Unresolved Imports: {len(result.get("namespace_resolution", {}).get("unresolved_imports", []))}

Workflow Graph:
--------------
Total Nodes: {len(result.get("workflow_graph", {}).get("nodes", []))}
Total Edges: {len(result.get("workflow_graph", {}).get("edges", []))}
"""
        return report


def test_multi_file_analyzer():
    """Test the multi-file workflow analyzer."""
    analyzer = MultiFileWorkflowAnalyzer()

    # Analyze the project
    result = analyzer.analyze_project_workflow("src")

    if result["analysis_success"]:
        print("Multi-File Workflow Analysis Results:")
        print("=" * 60)

        print(f"Source Directory: {result['source_directory']}")
        print(f"Total Python Files: {result['total_files']}")

        print(f"\nDependency Analysis:")
        dep_analysis = result["dependency_analysis"]
        if dep_analysis.get("pydeps_success"):
            print(f"  ✅ Pydeps Analysis Successful")
            print(f"  Total Dependencies: {dep_analysis.get('total_dependencies', 0)}")
            print(f"  Graph Nodes: {dep_analysis.get('dependency_graph_nodes', 0)}")
            print(f"  Graph Edges: {dep_analysis.get('dependency_graph_edges', 0)}")
        else:
            print(
                f"  ❌ Pydeps Analysis Failed: {dep_analysis.get('error', 'Unknown error')}"
            )

        print(f"\nCircular Dependencies:")
        circular_deps = result["circular_dependencies"]
        print(
            f"  Total Circular Dependencies: {circular_deps.get('total_circular_deps', 0)}"
        )
        print(f"  Simple Cycles: {len(circular_deps.get('simple_cycles', []))}")
        print(
            f"  Strongly Connected Components: {len(circular_deps.get('strongly_connected_components', []))}"
        )

        print(f"\nCross-File Analysis:")
        cross_file = result["cross_file_calls"]
        print(f"  Inter-File Calls: {len(cross_file.get('inter_file_calls', []))}")
        print(f"  Entry Points: {len(cross_file.get('entry_points', []))}")

        print(f"\nNamespace Resolution:")
        namespace = result["namespace_resolution"]
        total_imports = sum(
            len(imports) for imports in namespace.get("imports", {}).values()
        )
        total_exports = sum(
            len(exports) for exports in namespace.get("exports", {}).values()
        )
        print(f"  Total Imports: {total_imports}")
        print(f"  Total Exports: {total_exports}")
        print(f"  Namespace Conflicts: {len(namespace.get('namespace_conflicts', []))}")

        # Store result for report generation
        analyzer.last_analysis_result = result

        # Generate detailed report
        print(f"\nDetailed Report:")
        print(analyzer.generate_analysis_report())

    else:
        print(f"Analysis failed: {result.get('error', 'Unknown error')}")

    return result


if __name__ == "__main__":
    test_multi_file_analyzer()
