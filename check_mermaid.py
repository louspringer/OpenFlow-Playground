#!/usr/bin/env python3
"""Check Mermaid blocks in markdown file"""

import re
from pathlib import Path


def check_mermaid_blocks():
    """Check Mermaid blocks in the markdown file"""
    file_path = Path("docs/GHOSTBUSTERS_COMPREHENSIVE_DESIGN.md")

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Find all Mermaid blocks
    mermaid_blocks = re.findall(
        r"```mermaid\s*\n(.*?)(?=\n```|\n---|\n##|\n###|\n$|\n\n)", content, re.DOTALL
    )

    print(f"🔍 Found {len(mermaid_blocks)} Mermaid blocks")

    for i, block in enumerate(mermaid_blocks, 1):
        print(f"\n--- Block {i} ---")
        print(block[:200] + "..." if len(block) > 200 else block)

        # Check for syntax issues
        if "-->" in block:
            print("✅ Contains arrows")
        else:
            print("⚠️  No arrows found")

        # Check for proper structure
        if "graph" in block or "classDiagram" in block or "stateDiagram" in block:
            print("✅ Valid diagram type")
    else:
        print("⚠️  Unknown diagram type")


if __name__ == "__main__":
    check_mermaid_blocks()
