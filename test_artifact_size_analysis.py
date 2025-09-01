#!/usr/bin/env python3
"""Test if large artifacts need internal modeling and breakup"""

import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


def analyze_file_complexity(file_path: str) -> dict[str, Any]:
    """Analyze complexity of a single file"""
    try:
        with open(file_path) as f:
            content = f.read()

        # Basic metrics
        lines = len(content.splitlines())
        characters = len(content)
        ast_nodes = count_ast_nodes(content)

        # Complexity ratios
        nodes_per_line = ast_nodes / lines if lines > 0 else 0
        nodes_per_char = ast_nodes / characters if characters > 0 else 0

        return {
            "file_path": file_path,
            "lines": lines,
            "characters": characters,
            "ast_nodes": ast_nodes,
            "nodes_per_line": nodes_per_line,
            "nodes_per_char": nodes_per_char,
            "parseable": ast_nodes > 0,
        }
    except Exception as e:
        return {"file_path": file_path, "error": str(e), "parseable": False}


def find_large_artifacts(directory: str = "src", min_lines: int = 100) -> list[dict[str, Any]]:
    """Find large artifacts in the codebase"""
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis = analyze_file_complexity(file_path)

                if analysis.get("parseable", False) and analysis.get("lines", 0) >= min_lines:
                    large_files.append(analysis)

    # Sort by complexity (AST nodes)
    large_files.sort(key=lambda x: x.get("ast_nodes", 0), reverse=True)
    return large_files


def analyze_complexity_patterns(files: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze patterns in file complexity"""
    if not files:
        return {}

    # Calculate statistics
    ast_nodes_list = [f.get("ast_nodes", 0) for f in files if f.get("parseable", False)]
    lines_list = [f.get("lines", 0) for f in files if f.get("parseable", False)]

    if not ast_nodes_list:
        return {}

    avg_ast_nodes = sum(ast_nodes_list) / len(ast_nodes_list)
    avg_lines = sum(lines_list) / len(lines_list)

    # Find outliers (files with complexity > 2x average)
    high_complexity_threshold = avg_ast_nodes * 2
    high_complexity_files = [f for f in files if f.get("ast_nodes", 0) > high_complexity_threshold]

    # Categorize by complexity level
    complexity_levels = {
        "low": [f for f in files if f.get("ast_nodes", 0) <= avg_ast_nodes * 0.5],
        "medium": [f for f in files if avg_ast_nodes * 0.5 < f.get("ast_nodes", 0) <= avg_ast_nodes * 1.5],
        "high": [f for f in files if avg_ast_nodes * 1.5 < f.get("ast_nodes", 0) <= avg_ast_nodes * 2.5],
        "extreme": [f for f in files if f.get("ast_nodes", 0) > avg_ast_nodes * 2.5],
    }

    return {
        "total_files": len(files),
        "parseable_files": len([f for f in files if f.get("parseable", False)]),
        "average_ast_nodes": avg_ast_nodes,
        "average_lines": avg_lines,
        "high_complexity_threshold": high_complexity_threshold,
        "high_complexity_count": len(high_complexity_files),
        "complexity_distribution": {level: len(files) for level, files in complexity_levels.items()},
        "top_complex_files": high_complexity_files[:5],
    }


def suggest_breakup_strategies(file_analysis: dict[str, Any]) -> list[str]:
    """Suggest strategies for breaking up large artifacts"""
    suggestions = []

    lines = file_analysis.get("lines", 0)
    ast_nodes = file_analysis.get("ast_nodes", 0)
    nodes_per_line = file_analysis.get("nodes_per_line", 0)

    # Line count suggestions
    if lines > 500:
        suggestions.append("File is extremely long (>500 lines) - break into multiple modules")
    elif lines > 300:
        suggestions.append("File is very long (>300 lines) - consider extracting classes/functions")
    elif lines > 200:
        suggestions.append("File is long (>200 lines) - extract related functionality")

    # AST complexity suggestions
    if ast_nodes > 1000:
        suggestions.append("Extremely high AST complexity (>1000 nodes) - needs major refactoring")
    elif ast_nodes > 500:
        suggestions.append("High AST complexity (>500 nodes) - extract complex logic")
    elif ast_nodes > 200:
        suggestions.append("Moderate AST complexity (>200 nodes) - consider extraction")

    # Complexity per line suggestions
    if nodes_per_line > 10:
        suggestions.append("High complexity per line (>10 nodes/line) - simplify individual lines")
    elif nodes_per_line > 5:
        suggestions.append("Moderate complexity per line (>5 nodes/line) - review complex expressions")

    # Specific strategies
    if ast_nodes > 500:
        suggestions.extend(
            [
                "Extract complex functions into separate modules",
                "Create utility classes for common operations",
                "Split large classes into smaller, focused classes",
                "Use composition instead of inheritance where possible",
            ]
        )

    return suggestions


def main():
    """Analyze large artifacts and suggest breakup strategies"""
    print("🧪 Testing Hypothesis 3: Large Artifacts Need Internal Modeling and Breakup")

    # Find large artifacts
    print("\n🔍 Scanning for large artifacts...")
    large_files = find_large_artifacts(min_lines=100)

    if not large_files:
        print("✅ No large artifacts found - codebase is well-structured!")
        return

    print(f"Found {len(large_files)} files with 100+ lines")

    # Analyze complexity patterns
    print("\n📊 Analyzing complexity patterns...")
    patterns = analyze_complexity_patterns(large_files)

    print(f"Total files analyzed: {patterns.get('total_files', 0)}")
    print(f"Parseable files: {patterns.get('parseable_files', 0)}")
    print(f"Average AST nodes: {patterns.get('average_ast_nodes', 0):.1f}")
    print(f"Average lines: {patterns.get('average_lines', 0):.1f}")
    print(f"High complexity threshold: {patterns.get('high_complexity_threshold', 0):.1f}")

    # Show complexity distribution
    print("\n📈 Complexity Distribution:")
    for level, count in patterns.get("complexity_distribution", {}).items():
        print(f"  {level.capitalize()}: {count} files")

    # Show top complex files
    print("\n🚨 Top Complex Files (Need Attention):")
    for i, file_info in enumerate(patterns.get("top_complex_files", [])[:5], 1):
        print(f"  {i}. {file_info['file_path']}")
        print(f"     Lines: {file_info['lines']}, AST: {file_info['ast_nodes']}, " f"Complexity: {file_info['nodes_per_line']:.1f} nodes/line")

        # Suggest breakup strategies
        suggestions = suggest_breakup_strategies(file_info)
        if suggestions:
            print("     Suggestions:")
            for suggestion in suggestions[:3]:  # Show top 3 suggestions
                print(f"       - {suggestion}")

    # Overall assessment
    high_complexity_count = patterns.get("high_complexity_count", 0)
    total_files = patterns.get("total_files", 0)

    print(f"\n🎯 Hypothesis 3 Assessment:")
    if high_complexity_count > 0:
        percentage = (high_complexity_count / total_files) * 100
        print(f"❌ CONFIRMED: {high_complexity_count}/{total_files} files ({percentage:.1f}%) are too complex")
        print("   These artifacts need internal modeling and breakup!")

        if high_complexity_count > total_files * 0.2:
            print("   🚨 CRITICAL: Over 20% of files are too complex - systemic issue!")
        elif high_complexity_count > total_files * 0.1:
            print("   ⚠️ WARNING: Over 10% of files are too complex - needs attention!")
    else:
        print("✅ REJECTED: No files exceed complexity threshold")
        print("   Codebase is well-structured and doesn't need breakup")


if __name__ == "__main__":
    main()

"""Test if large artifacts need internal modeling and breakup"""

import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


def analyze_file_complexity(file_path: str) -> dict[str, Any]:
    """Analyze complexity of a single file"""
    try:
        with open(file_path) as f:
            content = f.read()

        # Basic metrics
        lines = len(content.splitlines())
        characters = len(content)
        ast_nodes = count_ast_nodes(content)

        # Complexity ratios
        nodes_per_line = ast_nodes / lines if lines > 0 else 0
        nodes_per_char = ast_nodes / characters if characters > 0 else 0

        return {
            "file_path": file_path,
            "lines": lines,
            "characters": characters,
            "ast_nodes": ast_nodes,
            "nodes_per_line": nodes_per_line,
            "nodes_per_char": nodes_per_char,
            "parseable": ast_nodes > 0,
        }
    except Exception as e:
        return {"file_path": file_path, "error": str(e), "parseable": False}


def find_large_artifacts(directory: str = "src", min_lines: int = 100) -> list[dict[str, Any]]:
    """Find large artifacts in the codebase"""
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis = analyze_file_complexity(file_path)

                if analysis.get("parseable", False) and analysis.get("lines", 0) >= min_lines:
                    large_files.append(analysis)

    # Sort by complexity (AST nodes)
    large_files.sort(key=lambda x: x.get("ast_nodes", 0), reverse=True)
    return large_files


def analyze_complexity_patterns(files: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze patterns in file complexity"""
    if not files:
        return {}

    # Calculate statistics
    ast_nodes_list = [f.get("ast_nodes", 0) for f in files if f.get("parseable", False)]
    lines_list = [f.get("lines", 0) for f in files if f.get("parseable", False)]

    if not ast_nodes_list:
        return {}

    avg_ast_nodes = sum(ast_nodes_list) / len(ast_nodes_list)
    avg_lines = sum(lines_list) / len(lines_list)

    # Find outliers (files with complexity > 2x average)
    high_complexity_threshold = avg_ast_nodes * 2
    high_complexity_files = [f for f in files if f.get("ast_nodes", 0) > high_complexity_threshold]

    # Categorize by complexity level
    complexity_levels = {
        "low": [f for f in files if f.get("ast_nodes", 0) <= avg_ast_nodes * 0.5],
        "medium": [f for f in files if avg_ast_nodes * 0.5 < f.get("ast_nodes", 0) <= avg_ast_nodes * 1.5],
        "high": [f for f in files if avg_ast_nodes * 1.5 < f.get("ast_nodes", 0) <= avg_ast_nodes * 2.5],
        "extreme": [f for f in files if f.get("ast_nodes", 0) > avg_ast_nodes * 2.5],
    }

    return {
        "total_files": len(files),
        "parseable_files": len([f for f in files if f.get("parseable", False)]),
        "average_ast_nodes": avg_ast_nodes,
        "average_lines": avg_lines,
        "high_complexity_threshold": high_complexity_threshold,
        "high_complexity_count": len(high_complexity_files),
        "complexity_distribution": {level: len(files) for level, files in complexity_levels.items()},
        "top_complex_files": high_complexity_files[:5],
    }


def suggest_breakup_strategies(file_analysis: dict[str, Any]) -> list[str]:
    """Suggest strategies for breaking up large artifacts"""
    suggestions = []

    lines = file_analysis.get("lines", 0)
    ast_nodes = file_analysis.get("ast_nodes", 0)
    nodes_per_line = file_analysis.get("nodes_per_line", 0)

    # Line count suggestions
    if lines > 500:
        suggestions.append("File is extremely long (>500 lines) - break into multiple modules")
    elif lines > 300:
        suggestions.append("File is very long (>300 lines) - consider extracting classes/functions")
    elif lines > 200:
        suggestions.append("File is long (>200 lines) - extract related functionality")

    # AST complexity suggestions
    if ast_nodes > 1000:
        suggestions.append("Extremely high AST complexity (>1000 nodes) - needs major refactoring")
    elif ast_nodes > 500:
        suggestions.append("High AST complexity (>500 nodes) - extract complex logic")
    elif ast_nodes > 200:
        suggestions.append("Moderate AST complexity (>200 nodes) - consider extraction")

    # Complexity per line suggestions
    if nodes_per_line > 10:
        suggestions.append("High complexity per line (>10 nodes/line) - simplify individual lines")
    elif nodes_per_line > 5:
        suggestions.append("Moderate complexity per line (>5 nodes/line) - review complex expressions")

    # Specific strategies
    if ast_nodes > 500:
        suggestions.extend(
            [
                "Extract complex functions into separate modules",
                "Create utility classes for common operations",
                "Split large classes into smaller, focused classes",
                "Use composition instead of inheritance where possible",
            ]
        )

    return suggestions


def main():
    """Analyze large artifacts and suggest breakup strategies"""
    print("🧪 Testing Hypothesis 3: Large Artifacts Need Internal Modeling and Breakup")

    # Find large artifacts
    print("\n🔍 Scanning for large artifacts...")
    large_files = find_large_artifacts(min_lines=100)

    if not large_files:
        print("✅ No large artifacts found - codebase is well-structured!")
        return

    print(f"Found {len(large_files)} files with 100+ lines")

    # Analyze complexity patterns
    print("\n📊 Analyzing complexity patterns...")
    patterns = analyze_complexity_patterns(large_files)

    print(f"Total files analyzed: {patterns.get('total_files', 0)}")
    print(f"Parseable files: {patterns.get('parseable_files', 0)}")
    print(f"Average AST nodes: {patterns.get('average_ast_nodes', 0):.1f}")
    print(f"Average lines: {patterns.get('average_lines', 0):.1f}")
    print(f"High complexity threshold: {patterns.get('high_complexity_threshold', 0):.1f}")

    # Show complexity distribution
    print("\n📈 Complexity Distribution:")
    for level, count in patterns.get("complexity_distribution", {}).items():
        print(f"  {level.capitalize()}: {count} files")

    # Show top complex files
    print("\n🚨 Top Complex Files (Need Attention):")
    for i, file_info in enumerate(patterns.get("top_complex_files", [])[:5], 1):
        print(f"  {i}. {file_info['file_path']}")
        print(f"     Lines: {file_info['lines']}, AST: {file_info['ast_nodes']}, " f"Complexity: {file_info['nodes_per_line']:.1f} nodes/line")

        # Suggest breakup strategies
        suggestions = suggest_breakup_strategies(file_info)
        if suggestions:
            print("     Suggestions:")
            for suggestion in suggestions[:3]:  # Show top 3 suggestions
                print(f"       - {suggestion}")

    # Overall assessment
    high_complexity_count = patterns.get("high_complexity_count", 0)
    total_files = patterns.get("total_files", 0)

    print(f"\n🎯 Hypothesis 3 Assessment:")
    if high_complexity_count > 0:
        percentage = (high_complexity_count / total_files) * 100
        print(f"❌ CONFIRMED: {high_complexity_count}/{total_files} files ({percentage:.1f}%) are too complex")
        print("   These artifacts need internal modeling and breakup!")

        if high_complexity_count > total_files * 0.2:
            print("   🚨 CRITICAL: Over 20% of files are too complex - systemic issue!")
        elif high_complexity_count > total_files * 0.1:
            print("   ⚠️ WARNING: Over 10% of files are too complex - needs attention!")
    else:
        print("✅ REJECTED: No files exceed complexity threshold")
        print("   Codebase is well-structured and doesn't need breakup")


if __name__ == "__main__":
    main()
