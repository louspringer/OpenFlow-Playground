#!/usr/bin/env python3
"""
Python-based Mermaid Syntax Validator for Documentation Linting

This validator checks Mermaid diagram syntax in markdown files and integrates
with the project's linting system to catch syntax errors before they cause issues.
"""

import re
import sys
from pathlib import Path


class MermaidValidator:
    """Validates Mermaid diagram syntax in markdown files."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single markdown file for Mermaid syntax."""
        if not file_path.exists():
            self.errors.append(f"File not found: {file_path}")
            return False

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return False

        return self._validate_content(content, file_path)

    def _validate_content(self, content: str, file_path: Path) -> bool:
        """Validate Mermaid content in a file."""
        mermaid_blocks = self._extract_mermaid_blocks(content)

        if not mermaid_blocks:
            return True  # No Mermaid blocks to validate

        is_valid = True

        for i, block in enumerate(mermaid_blocks):
            block_valid = self._validate_mermaid_block(block, i + 1, file_path)
            if not block_valid:
                is_valid = False

        return is_valid

    def _extract_mermaid_blocks(self, content: str) -> list[str]:
        """Extract all Mermaid code blocks from content."""
        pattern = r"```mermaid\s*\n(.*?)\n```"
        return re.findall(pattern, content, re.DOTALL)

    def _validate_mermaid_block(
        self, block: str, block_num: int, file_path: Path
    ) -> bool:
        """Validate a single Mermaid block."""
        is_valid = True

        # Check for basic syntax issues
        if not block.strip():
            self.errors.append(f"{file_path}:{block_num}: Empty Mermaid block")
            is_valid = False

        # Check for common syntax errors
        syntax_checks = [
            self._check_diagram_type(block, block_num, file_path),
            self._check_basic_syntax(block, block_num, file_path),
            self._check_class_diagram_syntax(block, block_num, file_path),
            self._check_state_diagram_syntax(block, block_num, file_path),
            self._check_graph_syntax(block, block_num, file_path),
        ]

        if not all(syntax_checks):
            is_valid = False

        return is_valid

    def _check_diagram_type(self, block: str, block_num: int, file_path: Path) -> bool:
        """Check if the diagram type is valid."""
        valid_types = [
            "graph",
            "flowchart",
            "sequenceDiagram",
            "classDiagram",
            "stateDiagram",
            "stateDiagram-v2",
            "pie",
            "gitgraph",
            "journey",
            "gantt",
            "C4Context",
            "C4Container",
            "C4Component",
        ]

        lines = block.strip().split("\n")
        if not lines:
            return True

        first_line = lines[0].strip()
        diagram_type = None

        for dt in valid_types:
            if first_line.startswith(dt):
                diagram_type = dt
                break

        if not diagram_type:
            self.errors.append(
                f"{file_path}:{block_num}: Invalid diagram type: {first_line}"
            )
            return False

        return True

    def _check_basic_syntax(self, block: str, block_num: int, file_path: Path) -> bool:
        """Check basic Mermaid syntax."""
        is_valid = True

        # Determine diagram type from first line
        lines = block.strip().split("\n")
        first_line = lines[0].strip() if lines else ""
        is_class_diagram = first_line.startswith("classDiagram")
        is_graph_like = first_line.startswith(("graph", "flowchart", "stateDiagram"))

        # Check for unmatched brackets/parentheses
        if block.count("(") != block.count(")"):
            self.errors.append(f"{file_path}:{block_num}: Unmatched parentheses")
            is_valid = False

        if block.count("[") != block.count("]"):
            self.errors.append(f"{file_path}:{block_num}: Unmatched brackets")
            is_valid = False

        if block.count("{") != block.count("}"):
            self.errors.append(f"{file_path}:{block_num}: Unmatched braces")
            is_valid = False

        # Generic arrow checks apply only to graph/flowchart/state diagrams
        if is_graph_like:
            arrow_pattern = r"-->|--|==>|==|-.->|-.|~>|~~"
            if re.search(arrow_pattern, block) and not re.search(
                r"[A-Za-z0-9_]\s*(?:-->|--|==>|==|-.->|-.|~>|~~)\s*[A-Za-z0-9_]", block
            ):
                self.warnings.append(
                    f"{file_path}:{block_num}: Potential arrow syntax issue"
                )

        # For classDiagram, perform relationship validation explicitly
        if is_class_diagram and not self._validate_class_relationships(
            block, file_path, block_num
        ):
            is_valid = False

        return is_valid

    def _validate_class_relationships(
        self, block: str, file_path: Path, block_num: int
    ) -> bool:
        """Validate classDiagram relationship lines using allowed operators."""
        allowed_ops = [
            r"<\|--",  # inheritance
            r"--\|>",  # inheritance reversed
            r"\*--",  # composition
            r"o--",  # aggregation
            r"-->",  # association with direction
            r"<--",  # association with reverse direction
            r"\\.\\.>",  # dotted with direction
            r"<\\.\\.",  # dotted reverse
            r"--",  # association
            r"\\.\\.",  # dotted
        ]
        op_regex = "(" + "|".join(allowed_ops) + ")"
        pattern = re.compile(
            r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*"
            + op_regex
            + r"\s*([A-Za-z_][A-Za-z0-9_]*)\b"
        )

        valid = True
        for line in block.splitlines():
            if (
                "--" in line or ".." in line or "<|" in line or "|>" in line
            ) and not line.strip().startswith("class "):
                if not pattern.search(line):
                    self.warnings.append(
                        f"{file_path}:{block_num}: Potential class relationship syntax issue: {line.strip()}"
                    )
        return valid

    def _check_class_diagram_syntax(
        self, block: str, block_num: int, file_path: Path
    ) -> bool:
        """Check class diagram specific syntax."""
        if not block.strip().startswith("classDiagram"):
            return True

        is_valid = True

        # Check for proper class syntax
        class_pattern = r"class\s+[A-Za-z_][A-Za-z0-9_]*\s*{"
        if not re.search(class_pattern, block):
            self.warnings.append(
                f"{file_path}:{block_num}: No explicit class bodies found (ok if using only relationships)"
            )

        # Check for proper inheritance syntax token presence (relationships validated elsewhere)
        if "<|--" in block and not re.search(
            r"[A-Za-z_][A-Za-z0-9_]*\s*<\|--\s*[A-Za-z_][A-Za-z0-9_]*", block
        ):
            self.warnings.append(
                f"{file_path}:{block_num}: Potential inheritance syntax issue"
            )

        return is_valid

    def _check_state_diagram_syntax(
        self, block: str, block_num: int, file_path: Path
    ) -> bool:
        """Check state diagram specific syntax."""
        if not block.strip().startswith("stateDiagram"):
            return True

        is_valid = True

        # Check for proper state syntax
        state_pattern = r"state\s+[A-Za-z_][A-Za-z0-9_]*\s*{"
        if re.search(r"state\s+", block) and not re.search(state_pattern, block):
            self.warnings.append(
                f"{file_path}:{block_num}: Potential state syntax issue"
            )

        # Check for proper transitions
        transition_pattern = r"[A-Za-z_][A-Za-z0-9_]*\s*-->.*?[A-Za-z_][A-Za-z0-9_]"
        if re.search(r"-->", block) and not re.search(transition_pattern, block):
            self.warnings.append(
                f"{file_path}:{block_num}: Potential transition syntax issue"
            )

        return is_valid

    def _check_graph_syntax(self, block: str, block_num: int, file_path: Path) -> bool:
        """Check graph/flowchart specific syntax."""
        if not (
            block.strip().startswith("graph") or block.strip().startswith("flowchart")
        ):
            return True

        is_valid = True

        # Check for proper node definitions
        node_pattern = r"[A-Za-z_][A-Za-z0-9_]*\s*\[.*?\]"
        if re.search(r"\[", block) and not re.search(node_pattern, block):
            self.warnings.append(
                f"{file_path}:{block_num}: Potential node syntax issue"
            )

        # Check for proper subgraph syntax
        subgraph_pattern = r'subgraph\s+["\'][^"\']*["\'].*?end'
        if re.search(r"subgraph", block) and not re.search(
            subgraph_pattern, block, re.DOTALL
        ):
            self.warnings.append(
                f"{file_path}:{block_num}: Potential subgraph syntax issue"
            )

        return is_valid

    def get_errors(self) -> list[str]:
        """Get all validation errors."""
        return self.errors

    def get_warnings(self) -> list[str]:
        """Get all validation warnings."""
        return self.warnings

    def has_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.errors) > 0

    def print_report(self) -> None:
        """Print validation report."""
        if not self.errors and not self.warnings:
            print("✅ All Mermaid diagrams are valid!")
            return

        if self.errors:
            print(f"❌ Found {len(self.errors)} Mermaid syntax errors:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"⚠️  Found {len(self.warnings)} Mermaid syntax warnings:")
            for warning in self.warnings:
                print(f"  {warning}")


def main() -> None:
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python mermaid_validator.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    validator = MermaidValidator()

    if target.is_file():
        # Validate single file
        if target.suffix == ".md":
            is_valid = validator.validate_file(target)
            validator.print_report()
            sys.exit(0 if is_valid else 1)
        else:
            print(f"❌ {target} is not a markdown file")
            sys.exit(1)

    elif target.is_dir():
        # Validate all markdown files in directory
        markdown_files = list(target.rglob("*.md"))

        if not markdown_files:
            print(f"❌ No markdown files found in {target}")
            sys.exit(1)

        all_valid = True
        for md_file in markdown_files:
            print(f"🔍 Validating {md_file}...")
            is_valid = validator.validate_file(md_file)
            if not is_valid:
                all_valid = False

        validator.print_report()
        sys.exit(0 if all_valid else 1)

    else:
        print(f"❌ {target} does not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
