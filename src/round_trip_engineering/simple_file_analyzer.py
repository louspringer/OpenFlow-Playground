#!/usr/bin/env python3
"""
Simple File Analyzer - Replaces the complex AST traversal

Purpose: Extract essential file information without AST complexity
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class SimpleFileAnalyzer:
    """Simple file analyzer without AST complexity"""

    def __init__(self) -> None:
        self.model_data: dict[str, Any] = {}

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a Python file using simple text analysis"""
        try:
            print(f"🔍 Simple analysis: {file_path}")

            # Generate unique model ID
            model_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Simple text-based analysis
            self.model_data = {
                "model_id": model_id,
                "timestamp": timestamp,
                "source_file": file_path,
                "file_stats": self._analyze_file_stats(content, lines),
                "imports": self._extract_imports(lines),
                "classes": self._extract_classes(lines),
                "functions": self._extract_functions(lines),
                "structure": self._analyze_structure(lines),
            }

            print(
                f"✅ Analysis complete: {len(lines)} lines, {len(self.model_data['classes'])} classes"
            )
            return self.model_data

        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return {"error": str(e)}

    def _analyze_file_stats(self, content: str, lines: list[str]) -> dict[str, Any]:
        """Analyze basic file statistics"""
        return {
            "total_lines": len(lines),
            "code_lines": len(
                [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ]
            ),
            "comment_lines": len(
                [line for line in lines if line.strip().startswith("#")]
            ),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "file_size": len(content),
        }

    def _extract_imports(self, lines: list[str]) -> list[str]:
        """Extract import statements"""
        imports = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                imports.append(stripped)
        return imports

    def _extract_classes(self, lines: list[str]) -> list[dict[str, Any]]:
        """Extract class definitions"""
        classes = []
        current_class: dict[str, Any] | None = None

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("class "):
                # Extract class name
                class_name = (
                    stripped.split("class ")[1].split("(")[0].split(":")[0].strip()
                )
                current_class = {
                    "name": class_name,
                    "line": i,
                    "methods": [],
                    "docstring": "",
                }
                classes.append(current_class)
            elif current_class and stripped.startswith("def "):
                # Extract method name
                method_name = stripped.split("def ")[1].split("(")[0].strip()
                current_class["methods"].append(method_name)
            elif current_class and stripped.startswith(('"""', "'''")):
                # Extract docstring
                if not current_class["docstring"]:
                    current_class["docstring"] = stripped.strip("\"'")

        return classes

    def _extract_functions(self, lines: list[str]) -> list[dict[str, Any]]:
        """Extract function definitions"""
        functions = []
        current_function: dict[str, Any] | None = None

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("def ") and not any(
                c in stripped for c in ["class ", "    "]
            ):
                # Top-level function (not indented)
                func_name = stripped.split("def ")[1].split("(")[0].strip()
                current_function = {"name": func_name, "line": i, "docstring": ""}
                functions.append(current_function)
            elif current_function and stripped.startswith(('"""', "'''")):
                # Extract docstring
                if not current_function["docstring"]:
                    current_function["docstring"] = stripped.strip("\"'")

        return functions

    def _analyze_structure(self, lines: list[str]) -> dict[str, Any]:
        """Analyze file structure"""
        return {
            "has_main": any("if __name__ == '__main__'" in line for line in lines),
            "is_test_file": any("test_" in line for line in lines),
            "has_docstring": any(
                line.strip().startswith(('"""', "'''")) for line in lines
            ),
            "indentation_levels": max(
                len(line) - len(line.lstrip()) for line in lines if line.strip()
            )
            // 4,
        }


def main() -> None:
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python simple_file_analyzer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Analyze the file
    analyzer = SimpleFileAnalyzer()
    result = analyzer.analyze_file(file_path)

    # Save the result
    output_file = "simple_analysis_result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Analysis saved to: {output_file}")
    print(
        f"📊 File stats: {result['file_stats']['total_lines']} lines, {result['file_stats']['code_lines']} code lines"
    )


if __name__ == "__main__":
    import sys

    main()
