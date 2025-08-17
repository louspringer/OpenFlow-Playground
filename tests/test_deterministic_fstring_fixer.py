#!/usr/bin/env python3
"""
Tests for Deterministic F-String Fixer
"""

import tempfile
from pathlib import Path

import pytest

from scripts.deterministic_fstring_fixer import DeterministicFStringFixer


class TestDeterministicFStringFixer:
    """Test the DeterministicFStringFixer class"""

    @pytest.fixture
    def fixer(self):
        """Create a fixer instance for testing"""
        return DeterministicFStringFixer()

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_init(self, fixer):
        """Test fixer initialization"""
        assert fixer.workspace_path == Path()
        assert fixer.fixed_files == []
        assert fixer.errors == []

    def test_analyze_file_no_issues(self, fixer, temp_dir):
        """Test analyzing a file with no f-string issues"""
        test_file = temp_dir / "clean_file.py"
        test_file.write_text('print("Hello, world!")\nprint(f"Count: {count}")\n')

        issues = fixer._analyze_file(test_file)
        assert len(issues) == 0

    def test_analyze_file_with_broken_fstring(self, fixer, temp_dir):
        """Test analyzing a file with broken f-string"""
        test_file = temp_dir / "broken_file.py"
        test_file.write_text('print(f"Count: {len(\\\n    data)}")\n')

        issues = fixer._analyze_file(test_file)
        assert len(issues) > 0
        assert any(issue["type"] == "broken_fstring" for issue in issues)

    def test_analyze_file_syntax_error(self, fixer, temp_dir):
        """Test analyzing a file with syntax error"""
        test_file = temp_dir / "syntax_error.py"
        test_file.write_text('print("Hello"\n')  # Missing closing quote

        issues = fixer._analyze_file(test_file)
        assert len(issues) > 0
        assert any(issue["type"] == "syntax_error" for issue in issues)

    def test_fix_fstrings_in_content(self, fixer):
        """Test f-string fixing logic"""
        broken_content = 'print(f"Count: {len(\\\n    data)}")\n'
        fixed_content = fixer._fix_fstrings_in_content(broken_content)

        # Should remove the backslash and newline
        assert "\\" not in fixed_content
        assert fixed_content != broken_content

    def test_save_fixed_file_success(self, fixer, temp_dir):
        """Test successfully saving a fixed file"""
        test_file = temp_dir / "test_file.py"
        test_file.write_text('print("Hello")\n')

        fixed_content = 'print("Hello, fixed!")\n'
        result = fixer._save_fixed_file(test_file, fixed_content)

        assert result is True
        assert test_file.read_text() == fixed_content
        assert str(test_file) in fixer.fixed_files

    def test_save_fixed_file_syntax_error(self, fixer, temp_dir):
        """Test saving a file with syntax error fails"""
        test_file = temp_dir / "test_file.py"
        test_file.write_text('print("Hello")\n')

        broken_content = 'print("Hello"\n'  # Missing quote
        result = fixer._save_fixed_file(test_file, broken_content)

        assert result is False
        assert test_file.read_text() == 'print("Hello")\n'  # Original preserved

    def test_fix_file_no_issues(self, fixer, temp_dir):
        """Test fixing a file with no issues"""
        test_file = temp_dir / "clean_file.py"
        test_file.write_text('print("Hello, world!")\n')

        result = fixer.fix_file(str(test_file))
        assert result is True
        assert len(fixer.fixed_files) == 0  # No files were fixed

    def test_fix_file_with_issues(self, fixer, temp_dir):
        """Test fixing a file with f-string issues"""
        test_file = temp_dir / "broken_file.py"
        test_file.write_text('print(f"Count: {len(\\\n    data)}")\n')

        result = fixer.fix_file(str(test_file))
        assert result is True
        assert len(fixer.fixed_files) == 1
        assert str(test_file) in fixer.fixed_files

    def test_fix_file_not_found(self, fixer):
        """Test fixing a non-existent file"""
        result = fixer.fix_file("nonexistent_file.py")
        assert result is False

    def test_validate_fixes_all_valid(self, fixer, temp_dir):
        """Test validation when all fixes are valid"""
        # Create a valid file
        test_file = temp_dir / "valid_file.py"
        test_file.write_text('print("Hello")\n')

        # Add it to fixed files
        fixer.fixed_files.append(str(test_file))

        result = fixer.validate_fixes()
        assert result is True

    def test_validate_fixes_with_invalid(self, fixer, temp_dir):
        """Test validation when some fixes are invalid"""
        # Create an invalid file
        test_file = temp_dir / "invalid_file.py"
        test_file.write_text('print("Hello"\n')  # Missing quote

        # Add it to fixed files
        fixer.fixed_files.append(str(test_file))

        result = fixer.validate_fixes()
        assert result is False

    def test_generate_report(self, fixer, temp_dir):
        """Test report generation"""
        # Fix a file to generate some data
        test_file = temp_dir / "test_file.py"
        test_file.write_text('print(f"Count: {len(\\\n    data)}")\n')

        fixer.fix_file(str(test_file))

        report = fixer.generate_report()
        assert "F-String Fixer Report" in report
        assert "Files Fixed: 1" in report
        assert str(test_file) in report

    def test_scan_workspace(self, fixer, temp_dir):
        """Test workspace scanning"""
        # Create some test files
        (temp_dir / "file1.py").write_text('print("Hello")\n')
        (temp_dir / "file2.py").write_text('print(f"Count: {len(\\\n    data)}")\n')
        (temp_dir / "file3.py").write_text('print("World")\n')

        # Change workspace path to temp dir
        fixer.workspace_path = temp_dir

        results = fixer.scan_workspace()
        assert results["total_files"] == 3
        assert len(results["files_with_issues"]) > 0
        assert results["errors"] == []


class TestFStringFixerIntegration:
    """Integration tests for the f-string fixer"""

    def test_end_to_end_fix(self, temp_dir):
        """Test complete end-to-end f-string fixing"""
        fixer = DeterministicFStringFixer(str(temp_dir))

        # Create a file with broken f-strings
        test_file = temp_dir / "broken_fstrings.py"
        test_file.write_text(
            '''#!/usr/bin/env python3
"""
Test file with broken f-strings
"""

def print_counts():
    data = [1, 2, 3, 4, 5]
    print(f"Total count: {len(\\\n    data)}")
    print(f"First item: {data[0]}")
    print(f"Last item: {data[-1]}")
    print(f"Sum: {sum(\\\n    data)}")

if __name__ == "__main__":
    print_counts()
'''
        )

        # Fix the file
        result = fixer.fix_file(str(test_file))
        assert result is True

        # Verify the fix worked
        fixed_content = test_file.read_text()
        assert "\\" not in fixed_content
        assert "len(\\\n    data)" not in fixed_content

        # Verify the file still parses
        import ast

        ast.parse(fixed_content)

        # Verify it's in the fixed files list
        assert str(test_file) in fixer.fixed_files


if __name__ == "__main__":
    pytest.main([__file__])
