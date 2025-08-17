#!/usr/bin/env python3
"""
Deterministic F-String Fixer

Purpose: Scan, parse, and fix broken f-strings across the entire codebase
Graph API Level: 1
Projection System: fstring_recovery
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict


class DeterministicFStringFixer:
    """Deterministic tool to fix broken f-strings in Python files"""

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.fixed_files: list[str] = []
        self.broken_files: list[str] = []
        self.fix_stats = {
            "total_files": 0,
            "files_with_fstrings": 0,
            "files_fixed": 0,
            "total_fstrings_fixed": 0,
            "errors": [],
        }

    def scan_workspace(self) -> dict[str, Any]:
        """Scan entire workspace for Python files with f-string issues"""
        print("🔍 Scanning workspace for Python files...")

        python_files = list(self.workspace_path.rglob("*.py"))
        self.fix_stats["total_files"] = len(python_files)

        print(f"📁 Found {len(python_files)} Python files")

        for py_file in python_files:
            try:
                self._analyze_file(py_file)
            except Exception as e:
                error_msg = f"Error analyzing {py_file}: {e}"
                self.fix_stats["errors"].append(error_msg)
                print(f"❌ {error_msg}")

        return self.fix_stats

    def _analyze_file(self, py_file: Path) -> None:
        """Analyze a single Python file for f-string issues"""
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # Always try to parse with AST first
            try:
                ast.parse(content)
                # File parses successfully, no syntax errors
                return
            except SyntaxError:
                # File has syntax errors, check if it's f-string related
                if 'f"' in content or "f'" in content:
                    self.fix_stats["files_with_fstrings"] += 1
                    print(f"🔍 Found broken f-strings in: {py_file}")
                    self.broken_files.append(str(py_file))

                    # Attempt to fix
                    fixed_content = self._fix_fstrings_in_content(content)
                    if fixed_content != content:
                        self._save_fixed_file(py_file, fixed_content)
                        self.fix_stats["files_fixed"] += 1
                else:
                    # Other syntax errors, still track as broken
                    print(f"🔍 Found syntax errors in: {py_file}")
                    self.broken_files.append(str(py_file))

        except Exception as e:
            error_msg = f"Error reading {py_file}: {e}"
            self.fix_stats["errors"].append(error_msg)

    def _fix_fstrings_in_content(self, content: str) -> str:
        """Fix broken f-strings in content"""
        original_content = content
        fixed_content = content

        # Pattern 1: Broken multi-line f-strings with { on separate lines
        pattern1 = r'f"([^"]*)\s*\{\s*\n\s*([^}]+)\s*\}\s*([^"]*)"'
        matches = re.finditer(pattern1, fixed_content, re.MULTILINE)

        for match in matches:
            prefix = match.group(1)
            variable = match.group(2).strip()
            suffix = match.group(3)
            replacement = f'f"{prefix}{{{variable}}}{suffix}"'
            fixed_content = fixed_content.replace(match.group(0), replacement)
            self.fix_stats["total_fstrings_fixed"] += 1

        # Pattern 2: Broken f-strings with multiple { on separate lines
        pattern2 = r'f"([^"]*)\s*\{\s*\n\s*([^}]+)\s*,\s*\n\s*([^}]+)\s*\}\s*([^"]*)"'
        matches = re.finditer(pattern2, fixed_content, re.MULTILINE)

        for match in matches:
            prefix = match.group(1)
            var1 = match.group(2).strip()
            var2 = match.group(3).strip()
            suffix = match.group(4)
            replacement = f'f"{prefix}{{{var1}, {var2}}}{suffix}"'
            fixed_content = fixed_content.replace(match.group(0), replacement)
            self.fix_stats["total_fstrings_fixed"] += 1

        # Pattern 3: Complex broken f-strings with nested formatting
        pattern3 = r'f"([^"]*)\s*\{\s*\n\s*([^}]+)\s*:\s*([^}]+)\s*\}\s*([^"]*)"'
        matches = re.finditer(pattern3, fixed_content, re.MULTILINE)

        for match in matches:
            prefix = match.group(1)
            var = match.group(2).strip()
            format_spec = match.group(3).strip()
            suffix = match.group(4)
            replacement = f'f"{prefix}{{{var}:{format_spec}}}{suffix}"'
            fixed_content = fixed_content.replace(match.group(0), replacement)
            self.fix_stats["total_fstrings_fixed"] += 1

        # Validate the fix worked
        if fixed_content != original_content:
            try:
                ast.parse(fixed_content)
                print(f"✅ Fixed f-strings in content")
                return fixed_content
            except SyntaxError:
                print(f"⚠️  Fix didn't resolve all syntax errors")
                return original_content

        return original_content

    def _save_fixed_file(self, py_file: Path, fixed_content: str) -> None:
        """Save the fixed content back to the file"""
        try:
            # Create backup
            backup_file = py_file.with_suffix(".py.backup")
            with open(backup_file, "w", encoding="utf-8") as f:
                with open(py_file, encoding="utf-8") as original:
                    f.write(original.read())

            # Save fixed content
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(fixed_content)

            print(f"💾 Fixed and saved: {py_file}")
            self.fixed_files.append(str(py_file))

        except Exception as e:
            error_msg = f"Error saving fixed file {py_file}: {e}"
            self.fix_stats["errors"].append(error_msg)
            print(f"❌ {error_msg}")

    def generate_report(self) -> str:
        """Generate a report of the fixing operation"""
        report = f"""
# F-String Fixing Report

## Summary
- **Total Python files scanned**: {self.fix_stats['total_files']}
- **Files with f-strings**: {self.fix_stats['files_with_fstrings']}
- **Files fixed**: {self.fix_stats['files_fixed']}
- **Total f-strings fixed**: {self.fix_stats['total_fstrings_fixed']}

## Fixed Files
"""

        for fixed_file in self.fixed_files:
            report += f"- {fixed_file}\n"

        if self.fix_stats["errors"]:
            report += "\n## Errors\n"
            for error in self.fix_stats["errors"]:
                report += f"- {error}\n"

        return report

    def validate_fixes(self) -> bool:
        """Validate that all fixed files now parse correctly"""
        print("🔍 Validating fixes...")

        all_valid = True
        for fixed_file in self.fixed_files:
            try:
                with open(fixed_file, encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
                print(f"✅ {fixed_file} - Valid syntax")
            except SyntaxError as e:
                print(f"❌ {fixed_file} - Still has syntax errors: {e}")
                all_valid = False

        return all_valid


def main():
    """Main function to run the f-string fixer"""
    import sys

    workspace_path = sys.argv[1] if len(sys.argv) > 1 else "."

    print("🚀 Deterministic F-String Fixer")
    print("=" * 50)

    fixer = DeterministicFStringFixer(workspace_path)

    # Scan and fix
    stats = fixer.scan_workspace()

    # Generate report
    report = fixer.generate_report()
    print(report)

    # Save report
    with open("fstring_fixing_report.md", "w") as f:
        f.write(report)

    # Validate fixes
    if fixer.fixed_files:
        print("\n🔍 Validating fixes...")
        all_valid = fixer.validate_fixes()

        if all_valid:
            print("✅ All fixed files now have valid syntax!")
        else:
            print("⚠️  Some files still have syntax errors")

    print(f"\n📊 Fixing complete! Report saved to fstring_fixing_report.md")


if __name__ == "__main__":
    main()
