"""
Architectural Drift Detector
============================

RM-compliant tool for detecting architectural drift in documentation,
cursor rules, and configuration files that reference deleted or moved implementations.

This addresses the sneaky RM violation where cursor rules point to old paths
like `scripts/model_crud.py` instead of current ones like `src/model_management/model_crud.py`.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DriftViolation:
    """Represents an architectural drift violation"""

    file_path: str
    line_number: int
    old_reference: str
    current_reference: str
    violation_type: str
    severity: str
    description: str


class ArchitecturalDriftDetector:
    """
    RM-compliant architectural drift detector.

    Implements:
    - Self-Monitoring: Detects drift automatically
    - Self-Reporting: Reports violations with context
    - Single Responsibility: Only detects drift, doesn't fix
    - Operational Visibility: Makes drift visible
    - Testability: Can be tested in isolation
    """

    def __init__(self, project_root: str = "."):
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(project_root)

        # Known path migrations (old -> new)
        self.path_migrations = {
            "scripts/model_crud.py": "src/model_management/model_crud.py",
            "scripts/": "src/",
            "src.round_trip_engineering.tools": "src.round_trip_engineering.tools",  # Still valid
        }

        # File patterns to check
        self.check_patterns = [
            "**/.cursor/rules/*.mdc",
            "**/*.md",
            "**/*.py",
            "**/README.md",
            "**/docs/**/*.md",
        ]

        # Reference patterns to detect
        self.reference_patterns = [
            r"uv run python\s+([^\s]+\.py)",  # CLI commands
            r"from\s+([^\s]+)\s+import",  # Python imports
            r"import\s+([^\s]+)",  # Python imports
            r"`([^`]+\.py)`",  # Code blocks
            r'"([^"]+\.py)"',  # String references
            r"'([^']+\.py)'",  # String references
        ]

    def detect_drift(self) -> List[DriftViolation]:
        """
        Detect architectural drift across the project.

        Returns:
            List of drift violations found
        """
        self.logger.info("🔍 Starting architectural drift detection")

        violations = []

        # Check all relevant files
        for pattern in self.check_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    file_violations = self._check_file_for_drift(file_path)
                    violations.extend(file_violations)

        self.logger.info(f"✅ Drift detection complete: {len(violations)} violations found")
        return violations

    def _check_file_for_drift(self, file_path: Path) -> List[DriftViolation]:
        """Check a single file for drift violations"""
        violations = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            for line_num, line in enumerate(lines, 1):
                for pattern in self.reference_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        reference = match.group(1)
                        violation = self._check_reference(file_path, line_num, reference, line)
                        if violation:
                            violations.append(violation)

        except Exception as e:
            self.logger.error(f"❌ Error checking {file_path}: {e}")

        return violations

    def _check_reference(self, file_path: Path, line_num: int, reference: str, line: str) -> DriftViolation:
        """Check if a reference is stale"""

        # Check if reference matches known migrations
        for old_path, new_path in self.path_migrations.items():
            if old_path in reference:
                # Check if old path doesn't exist
                old_full_path = self.project_root / old_path
                if not old_full_path.exists():
                    return DriftViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        old_reference=reference,
                        current_reference=reference.replace(old_path, new_path),
                        violation_type="stale_path_reference",
                        severity="high",
                        description=f"References deleted path '{old_path}', should be '{new_path}'",
                    )

        # Check if reference points to non-existent file
        if reference.endswith(".py") and not reference.startswith("src."):
            # It's a file path, check if it exists
            ref_path = self.project_root / reference
            if not ref_path.exists():
                return DriftViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    old_reference=reference,
                    current_reference="[UNKNOWN - needs investigation]",
                    violation_type="missing_file_reference",
                    severity="medium",
                    description=f"References non-existent file '{reference}'",
                )

        return None

    def generate_report(self, violations: List[DriftViolation]) -> str:
        """Generate a comprehensive drift report"""

        if not violations:
            return "✅ No architectural drift detected"

        report = []
        report.append("🚨 ARCHITECTURAL DRIFT DETECTION REPORT")
        report.append("=" * 60)
        report.append(f"📊 Total Violations: {len(violations)}")
        report.append(f"🕐 Detection Time: {datetime.now().isoformat()}")
        report.append("")

        # Group by violation type
        by_type = {}
        for violation in violations:
            if violation.violation_type not in by_type:
                by_type[violation.violation_type] = []
            by_type[violation.violation_type].append(violation)

        for violation_type, type_violations in by_type.items():
            report.append(f"📋 {violation_type.upper().replace('_', ' ')} ({len(type_violations)} violations)")
            report.append("-" * 40)

            for violation in type_violations:
                report.append(f"  📁 {violation.file_path}:{violation.line_number}")
                report.append(f"     ❌ Old: {violation.old_reference}")
                report.append(f"     ✅ New: {violation.current_reference}")
                report.append(f"     📝 {violation.description}")
                report.append("")

        # Summary
        report.append("🎯 SUMMARY")
        report.append("-" * 20)
        high_severity = len([v for v in violations if v.severity == "high"])
        medium_severity = len([v for v in violations if v.severity == "medium"])

        report.append(f"🔴 High Severity: {high_severity}")
        report.append(f"🟡 Medium Severity: {medium_severity}")
        report.append("")

        if high_severity > 0:
            report.append("🚨 IMMEDIATE ACTION REQUIRED:")
            report.append("  - Fix high severity violations immediately")
            report.append("  - Update cursor rules and documentation")
            report.append("  - Verify all references point to existing files")

        return "\n".join(report)

    def get_health_status(self) -> Dict[str, any]:
        """Get health status for RM compliance"""
        violations = self.detect_drift()

        high_severity = len([v for v in violations if v.severity == "high"])
        medium_severity = len([v for v in violations if v.severity == "medium"])

        return {
            "healthy": high_severity == 0,
            "total_violations": len(violations),
            "high_severity": high_severity,
            "medium_severity": medium_severity,
            "last_check": datetime.now().isoformat(),
            "status": "critical" if high_severity > 0 else "warning" if medium_severity > 0 else "healthy",
        }


def main():
    """CLI interface for drift detection"""
    import argparse

    parser = argparse.ArgumentParser(description="Detect architectural drift")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--health", action="store_true", help="Show health status")

    args = parser.parse_args()

    detector = ArchitecturalDriftDetector(args.project_root)

    if args.health:
        health = detector.get_health_status()
        print(f"Health Status: {health['status']}")
        print(f"Violations: {health['total_violations']} (High: {health['high_severity']}, Medium: {health['medium_severity']})")
        return

    violations = detector.detect_drift()

    if args.report:
        report = detector.generate_report(violations)
        print(report)
    else:
        print(f"Found {len(violations)} architectural drift violations")
        for violation in violations:
            print(f"  {violation.file_path}:{violation.line_number} - {violation.description}")


if __name__ == "__main__":
    main()
