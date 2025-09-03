#!/usr/bin/env python3
"""
RDI Requirements Validator

This script validates requirements following the RDI (Requirements→Design→Implementation) methodology.
It ensures requirements are clear, testable, and traceable.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add src to path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class RDIRequirementsValidator:
    """RDI Requirements Validator for systematic requirements validation."""

    def __init__(self):
        """Initialize the RDI requirements validator."""
        self.requirements_dir = Path("requirements")
        self.validation_results = []
        self.requirements_count = 0
        self.valid_requirements = 0
        self.invalid_requirements = 0

    def validate_requirements_directory(self) -> bool:
        """Validate requirements directory structure."""
        print("🔍 Validating requirements directory structure...")

        if not self.requirements_dir.exists():
            print(f"❌ Requirements directory not found: {self.requirements_dir}")
            print("💡 Creating requirements directory...")
            self.requirements_dir.mkdir(parents=True, exist_ok=True)
            return False

        print(f"✅ Requirements directory exists: {self.requirements_dir}")
        return True

    def validate_requirement_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a single requirement file."""
        result = {"file": str(file_path), "valid": False, "issues": [], "requirements_count": 0, "valid_requirements": 0}

        try:
            content = file_path.read_text(encoding="utf-8")

            # Basic validation checks
            if not content.strip():
                result["issues"].append("File is empty")
                return result

            # Check for requirement patterns
            lines = content.split("\n")
            requirement_lines = [line for line in lines if line.strip().startswith(("REQ-", "REQUIREMENT", "FUNC-", "NON-FUNC-"))]

            result["requirements_count"] = len(requirement_lines)

            # Validate each requirement
            for line in requirement_lines:
                if self._validate_requirement_line(line):
                    result["valid_requirements"] += 1
                else:
                    result["issues"].append(f"Invalid requirement format: {line.strip()}")

            # Check for traceability markers
            if "TRACE:" not in content and "TRACEABILITY:" not in content and "**TRACE**:" not in content:
                result["issues"].append("Missing traceability markers")

            # Check for testability markers
            if "TEST:" not in content and "TESTABLE:" not in content and "**TEST**:" not in content:
                result["issues"].append("Missing testability markers")

            # Check for acceptance criteria
            if "ACCEPTANCE:" not in content and "ACCEPTANCE CRITERIA:" not in content and "**ACCEPTANCE**:" not in content:
                result["issues"].append("Missing acceptance criteria")

            # Check for performance requirements (if this is a performance requirements file)
            if "performance" in file_path.name.lower() and "REQ-PERF-" not in content:
                result["issues"].append("Missing performance requirements (REQ-PERF-XXX)")

            result["valid"] = len(result["issues"]) == 0

        except Exception as e:
            result["issues"].append(f"Error reading file: {str(e)}")

        return result

    def _validate_requirement_line(self, line: str) -> bool:
        """Validate a single requirement line."""
        line = line.strip()

        # Check for requirement ID
        if not any(line.startswith(prefix) for prefix in ["REQ-", "REQUIREMENT", "FUNC-", "NON-FUNC-"]):
            return False

        # Check for requirement description
        if len(line) < 20:  # Minimum length for meaningful requirement
            return False

        # Check for requirement format
        if ":" not in line and " - " not in line:
            return False

        return True

    def validate_all_requirements(self) -> Dict[str, Any]:
        """Validate all requirements files."""
        print("🔍 Validating all requirements files...")

        if not self.requirements_dir.exists():
            print("❌ Requirements directory does not exist")
            return {"valid": False, "message": "Requirements directory not found"}

        # Find all requirement files
        requirement_files = []
        for pattern in ["*.md", "*.yaml", "*.yml", "*.json"]:
            requirement_files.extend(self.requirements_dir.glob(pattern))

        if not requirement_files:
            print("⚠️  No requirement files found")
            return {
                "valid": False,
                "message": "No requirement files found",
                "total_files": 0,
                "valid_files": 0,
                "total_requirements": 0,
                "valid_requirements": 0,
                "invalid_requirements": 0,
                "validation_results": [],
            }

        print(f"📋 Found {len(requirement_files)} requirement files")

        # Validate each file
        for file_path in requirement_files:
            print(f"  🔍 Validating: {file_path.name}")
            result = self.validate_requirement_file(file_path)
            self.validation_results.append(result)

            if result["valid"]:
                print(f"    ✅ Valid ({result['valid_requirements']}/{result['requirements_count']} requirements)")
                self.valid_requirements += result["valid_requirements"]
            else:
                print(f"    ❌ Invalid: {', '.join(result['issues'])}")
                self.invalid_requirements += result["requirements_count"] - result["valid_requirements"]

            self.requirements_count += result["requirements_count"]

        return self._generate_validation_summary()

    def _generate_validation_summary(self) -> Dict[str, Any]:
        """Generate validation summary."""
        total_files = len(self.validation_results)
        valid_files = len([r for r in self.validation_results if r["valid"]])

        summary = {
            "valid": valid_files == total_files and self.invalid_requirements == 0,
            "total_files": total_files,
            "valid_files": valid_files,
            "total_requirements": self.requirements_count,
            "valid_requirements": self.valid_requirements,
            "invalid_requirements": self.invalid_requirements,
            "validation_results": self.validation_results,
        }

        return summary

    def generate_requirements_report(self) -> str:
        """Generate requirements validation report."""
        report = []
        report.append("# 📋 RDI Requirements Validation Report")
        report.append("")
        report.append("## 📊 Summary")
        report.append(f"- **Total Files**: {len(self.validation_results)}")
        report.append(f"- **Valid Files**: {len([r for r in self.validation_results if r['valid']])}")
        report.append(f"- **Total Requirements**: {self.requirements_count}")
        report.append(f"- **Valid Requirements**: {self.valid_requirements}")
        report.append(f"- **Invalid Requirements**: {self.invalid_requirements}")
        report.append("")

        if self.validation_results:
            report.append("## 📋 File Details")
            for result in self.validation_results:
                report.append(f"### {result['file']}")
                report.append(f"- **Valid**: {'✅' if result['valid'] else '❌'}")
                report.append(f"- **Requirements**: {result['valid_requirements']}/{result['requirements_count']}")
                if result["issues"]:
                    report.append("- **Issues**:")
                    for issue in result["issues"]:
                        report.append(f"  - {issue}")
                report.append("")

        return "\n".join(report)

    def create_sample_requirements(self) -> None:
        """Create sample requirements file."""
        sample_file = self.requirements_dir / "sample_requirements.md"

        sample_content = """# 📋 Sample Requirements

## Functional Requirements

### REQ-001: User Authentication
**Description**: The system shall provide user authentication functionality.
**TRACE**: AUTH-001
**TEST**: AUTH-001-TEST
**ACCEPTANCE**: 
- Users can log in with valid credentials
- Users cannot log in with invalid credentials
- Session management works correctly

### REQ-002: Data Validation
**Description**: The system shall validate all input data before processing.
**TRACE**: VALID-001
**TEST**: VALID-001-TEST
**ACCEPTANCE**:
- Invalid data is rejected with appropriate error messages
- Valid data is processed successfully
- Data validation rules are enforced

## Non-Functional Requirements

### NON-FUNC-001: Performance
**Description**: The system shall respond to user requests within 2 seconds.
**TRACE**: PERF-001
**TEST**: PERF-001-TEST
**ACCEPTANCE**:
- 95% of requests complete within 2 seconds
- System handles 100 concurrent users
- Response time is measured and logged

### NON-FUNC-002: Security
**Description**: The system shall implement security best practices.
**TRACE**: SEC-001
**TEST**: SEC-001-TEST
**ACCEPTANCE**:
- All data is encrypted in transit
- Authentication tokens are secure
- Security vulnerabilities are addressed
"""

        sample_file.write_text(sample_content, encoding="utf-8")
        print(f"✅ Created sample requirements file: {sample_file}")


def main():
    """Main entry point for RDI requirements validator."""
    validator = RDIRequirementsValidator()

    if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
        validator.validate_requirements_directory()
        validator.create_sample_requirements()
        return 0

    # Validate requirements directory
    if not validator.validate_requirements_directory():
        print("💡 Run with --create-sample to create sample requirements")
        return 1

    # Validate all requirements
    summary = validator.validate_all_requirements()

    # Print summary
    print("\n📊 Requirements Validation Summary")
    print("=" * 40)
    print(f"Total Files: {summary['total_files']}")
    print(f"Valid Files: {summary['valid_files']}")
    print(f"Total Requirements: {summary['total_requirements']}")
    print(f"Valid Requirements: {summary['valid_requirements']}")
    print(f"Invalid Requirements: {summary['invalid_requirements']}")

    if summary["valid"]:
        print("\n✅ All requirements are valid!")
        return 0
    else:
        print("\n❌ Some requirements are invalid. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
