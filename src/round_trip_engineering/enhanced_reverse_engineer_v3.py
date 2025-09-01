#!/usr/bin/env python3
"""
Enhanced Reverse Engineer V3 - Simple and Effective

Purpose: Extract file structure and metadata without AST complexity
Replaces: The over-engineered V2 that had 3332 AST nodes
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class EnhancedReverseEngineerV3:
    """Simple and effective file reverse engineering"""

    def __init__(self) -> None:
        self.model_data: dict[str, Any] = {}

    def reverse_engineer_file(self, file_path: str) -> dict[str, Any]:
        """Reverse engineer a Python file into a clean model"""
        try:
            print(f"🔍 V3 Analysis: {file_path}")

            # Generate unique model ID
            model_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()

            # Read and analyze file
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Build clean model
            self.model_data = {
                "model_id": model_id,
                "timestamp": timestamp,
                "source_file": file_path,
                "file_metadata": self._extract_file_metadata(content, lines),
                "imports": self._extract_imports(lines),
                "classes": self._extract_classes(lines),
                "functions": self._extract_functions(lines),
                "file_structure": self._analyze_structure(lines),
            }

            print(f"✅ V3 Analysis complete: {len(lines)} lines")
            return self.model_data

        except Exception as e:
            print(f"❌ Error in V3: {e}")
            return {"error": str(e)}

    def _extract_file_metadata(self, content: str, lines: list[str]) -> dict[str, Any]:
        """Extract basic file metadata"""
        return {
            "executable": "if __name__ == '__main__'" in content,
            "is_test_file": any("test_" in line for line in lines),
            "line_count": len(lines),
            "file_size": len(content),
            "has_docstring": any(line.strip().startswith(('"""', "'''")) for line in lines),
        }

    def _extract_imports(self, lines: list[str]) -> list[str]:
        """Extract import statements"""
        imports = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                imports.append(stripped)
        return imports

    def _extract_classes(self, lines: list[str]) -> dict[str, Any]:
        """Extract class information"""
        classes = {}
        current_class: dict[str, Any] | None = None
        in_class = False
        class_indent = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:  # Skip empty lines
                continue

            # Calculate indentation level
            indent = len(line) - len(line.lstrip())

            if stripped.startswith("class "):
                # Extract class name and bases
                class_def = stripped[6:]  # Remove 'class '
                class_name = class_def.split("(")[0].split(":")[0].strip()

                # Extract base classes
                bases = []
                if "(" in class_def and ")" in class_def:
                    base_part = class_def.split("(")[1].split(")")[0]
                    bases = [base.strip() for base in base_part.split(",") if base.strip()]

                current_class = {
                    "name": class_name,
                    "line": i,
                    "bases": bases,
                    "methods": [],
                    "docstring": "",
                    "decorators": [],
                }
                classes[class_name] = current_class
                in_class = True
                class_indent = indent

                # Check for decorators on previous lines
                j = i - 2
                while j >= 0 and lines[j].strip().startswith("@"):
                    current_class["decorators"].insert(0, lines[j].strip())
                    j -= 1

            elif in_class and current_class and stripped.startswith("def ") and indent > class_indent:
                # This is a method (indented more than class)
                method_name = stripped.split("def ")[1].split("(")[0].strip()
                current_class["methods"].append({"name": method_name, "line": i, "signature": stripped})
            elif in_class and current_class and stripped.startswith(('"""', "'''")) and indent > class_indent:
                # Extract docstring (indented more than class)
                if not current_class["docstring"]:
                    current_class["docstring"] = stripped.strip("\"'")
            elif in_class and indent <= class_indent and stripped and not stripped.startswith("#"):
                # We've left the class (same or less indentation, not empty, not comment)
                in_class = False
                current_class = None

        return classes

    def _extract_functions(self, lines: list[str]) -> list[dict[str, Any]]:
        """Extract module-level functions"""
        functions = []
        current_function: dict[str, Any] | None = None

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:  # Skip empty lines
                continue

            # Calculate indentation level
            indent = len(line) - len(line.lstrip())

            # Check for top-level function (not indented, not in class)
            if (stripped.startswith(("def ", "async def "))) and indent == 0:
                # Extract function name, handling both 'def' and 'async def'
                if stripped.startswith("async def "):
                    func_name = stripped.split("async def ")[1].split("(")[0].strip()
                else:
                    func_name = stripped.split("def ")[1].split("(")[0].strip()
                current_function = {
                    "name": func_name,
                    "line": i,
                    "signature": stripped,
                    "docstring": "",
                    "decorators": [],
                }
                functions.append(current_function)

                # Check for decorators on previous lines
                j = i - 2
                while j >= 0 and lines[j].strip().startswith("@"):
                    current_function["decorators"].insert(0, lines[j].strip())
                    j -= 1

            elif current_function and stripped.startswith(('"""', "'''")) and indent == 0:
                # Extract docstring (only for top-level functions)
                if not current_function["docstring"]:
                    current_function["docstring"] = stripped.strip("\"'")

        return functions

    def _analyze_structure(self, lines: list[str]) -> dict[str, Any]:
        """Analyze overall file structure"""
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
        comment_lines = len([line for line in lines if line.strip().startswith("#")])
        blank_lines = len([line for line in lines if not line.strip()])

        return {
            "total_lines": len(lines),
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "complexity_score": code_lines + (comment_lines // 2),  # Simple complexity metric
        }


def main() -> None:
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_reverse_engineer_v3.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Run V3 analysis
    engineer = EnhancedReverseEngineerV3()
    model = engineer.reverse_engineer_file(file_path)

    # Save results
    output_file = "enhanced_reverse_engineered_v3.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)

    print(f"✅ V3 Model saved to: {output_file}")
    print(f"📦 Classes: {len(model.get('classes', {}))}")
    print(f"🔧 Functions: {len(model.get('functions', []))}")
    print(f"📏 Lines: {model.get('file_structure', {}).get('total_lines', 0)}")


if __name__ == "__main__":
    import sys

    main()

    import sys

    main()

    import sys

    main()

    import sys

    main()
