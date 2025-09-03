#!/usr/bin/env python3
"""
File Reference Mapping Script
Maps all file references throughout the codebase to understand dependencies
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileReference:
    """File reference information."""

    source_file: str
    target_file: str
    reference_type: str  # 'import', 'include', 'reference', 'path', 'config'
    line_number: int
    context: str
    confidence: float  # 0.0 to 1.0
    is_relative: bool
    is_absolute: bool
    is_config_reference: bool
    is_makefile_reference: bool
    is_python_import: bool
    is_documentation_link: bool
    is_data_reference: bool


class FileReferenceMapper:
    """Maps file references throughout the codebase."""

    def __init__(self, project_root: str = "."):
        """Initialize the mapper."""
        self.project_root = Path(project_root)
        self.references: List[FileReference] = []
        self.reference_map: Dict[str, List[FileReference]] = defaultdict(list)
        self.dependency_map: Dict[str, List[str]] = defaultdict(list)
        self.reverse_dependency_map: Dict[str, List[str]] = defaultdict(list)
        self.orphaned_files: Set[str] = set()
        self.critical_files: Set[str] = set()

        logger.info("File Reference Mapper initialized")

    def map_all_references(self) -> Dict[str, Any]:
        """Map all file references in the project."""
        logger.info("Mapping all file references...")

        # Get all files in the project
        all_files = list(self.project_root.rglob("*"))
        all_files = [f for f in all_files if f.is_file() and not f.name.startswith(".")]

        logger.info(f"Found {len(all_files)} files to analyze")

        # Analyze each file for references
        for file_path in all_files:
            self._analyze_file_references(file_path, all_files)

        # Build dependency maps
        self._build_dependency_maps()

        # Identify orphaned files
        self._identify_orphaned_files(all_files)

        # Identify critical files
        self._identify_critical_files()

        # Generate mapping report
        report = self._generate_mapping_report()

        logger.info(f"Reference mapping complete: {len(self.references)} references found")
        return report

    def _analyze_file_references(self, file_path: Path, all_files: List[Path]):
        """Analyze a single file for references."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    # Analyze different types of references
                    self._analyze_python_imports(file_path, line, line_num, all_files)
                    self._analyze_makefile_references(file_path, line, line_num, all_files)
                    self._analyze_config_references(file_path, line, line_num, all_files)
                    self._analyze_documentation_links(file_path, line, line_num, all_files)
                    self._analyze_data_references(file_path, line, line_num, all_files)
                    self._analyze_path_references(file_path, line, line_num, all_files)

        except Exception as e:
            logger.debug(f"Error reading {file_path}: {e}")

    def _analyze_python_imports(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze Python import statements."""
        if file_path.suffix != ".py":
            return

        # Match various import patterns
        import_patterns = [
            r"import\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            r"from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import",
            r"import\s+([a-zA-Z_][a-zA-Z0-9_.]*)",
        ]

        for pattern in import_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                import_name = match.group(1)

                # Find matching files
                matching_files = self._find_matching_files(import_name, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="import",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.8,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=False,
                        is_makefile_reference=False,
                        is_python_import=True,
                        is_documentation_link=False,
                        is_data_reference=False,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _analyze_makefile_references(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze Makefile references."""
        if file_path.name not in ["Makefile", "makefile"] and not file_path.suffix == ".mk":
            return

        # Match file references in Makefiles
        makefile_patterns = [
            r"include\s+([^\s]+)",
            r"source\s+([^\s]+)",
            r"\.\s+([^\s]+)",
            r"([a-zA-Z0-9_/.-]+\.(py|sh|json|yml|yaml|md))",
        ]

        for pattern in makefile_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                file_ref = match.group(1)

                # Find matching files
                matching_files = self._find_files_by_name(file_ref, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="include",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.9,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=False,
                        is_makefile_reference=True,
                        is_python_import=False,
                        is_documentation_link=False,
                        is_data_reference=False,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _analyze_config_references(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze configuration file references."""
        if file_path.suffix not in [".json", ".yml", ".yaml", ".toml", ".ini", ".cfg"]:
            return

        # Match file references in config files
        config_patterns = [
            r'"([^"]*\.(py|sh|json|yml|yaml|md|txt))"',
            r"'([^']*\.(py|sh|json|yml|yaml|md|txt))'",
            r"([a-zA-Z0-9_/.-]+\.(py|sh|json|yml|yaml|md|txt))",
        ]

        for pattern in config_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                file_ref = match.group(1)

                # Find matching files
                matching_files = self._find_files_by_name(file_ref, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="config",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.7,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=True,
                        is_makefile_reference=False,
                        is_python_import=False,
                        is_documentation_link=False,
                        is_data_reference=False,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _analyze_documentation_links(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze documentation links."""
        if file_path.suffix not in [".md", ".rst", ".txt"]:
            return

        # Match markdown links and file references
        doc_patterns = [
            r"\[([^\]]+)\]\(([^)]+)\)",  # Markdown links
            r"([a-zA-Z0-9_/.-]+\.(py|sh|json|yml|yaml|md|txt))",  # File references
        ]

        for pattern in doc_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                if len(match.groups()) == 2:  # Markdown link
                    link_text, link_url = match.groups()
                    file_ref = link_url
                else:  # File reference
                    file_ref = match.group(1)

                # Find matching files
                matching_files = self._find_files_by_name(file_ref, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="link",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.6,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=False,
                        is_makefile_reference=False,
                        is_python_import=False,
                        is_documentation_link=True,
                        is_data_reference=False,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _analyze_data_references(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze data file references."""
        # Match file references in any file
        data_patterns = [
            r"([a-zA-Z0-9_/.-]+\.(json|csv|xml|cypher|sql|db))",
            r'open\(["\']([^"\']+)["\']',
            r'Path\(["\']([^"\']+)["\']',
            r'file_path\s*=\s*["\']([^"\']+)["\']',
        ]

        for pattern in data_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                file_ref = match.group(1)

                # Find matching files
                matching_files = self._find_files_by_name(file_ref, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="data",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.5,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=False,
                        is_makefile_reference=False,
                        is_python_import=False,
                        is_documentation_link=False,
                        is_data_reference=True,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _analyze_path_references(self, file_path: Path, line: str, line_num: int, all_files: List[Path]):
        """Analyze general path references."""
        # Match general file path patterns
        path_patterns = [
            r"([a-zA-Z0-9_/.-]+\.(py|sh|json|yml|yaml|md|txt|csv|xml|cypher|sql|db))",
        ]

        for pattern in path_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                file_ref = match.group(1)

                # Skip if already processed
                if any(ref.target_file.endswith(file_ref) for ref in self.references if ref.source_file == str(file_path)):
                    continue

                # Find matching files
                matching_files = self._find_files_by_name(file_ref, all_files)

                for target_file in matching_files:
                    reference = FileReference(
                        source_file=str(file_path),
                        target_file=str(target_file),
                        reference_type="path",
                        line_number=line_num,
                        context=line.strip(),
                        confidence=0.4,
                        is_relative=True,
                        is_absolute=False,
                        is_config_reference=False,
                        is_makefile_reference=False,
                        is_python_import=False,
                        is_documentation_link=False,
                        is_data_reference=False,
                    )
                    self.references.append(reference)
                    self.reference_map[str(file_path)].append(reference)

    def _find_matching_files(self, import_name: str, all_files: List[Path]) -> List[Path]:
        """Find files matching an import name."""
        matching_files = []

        # Convert import name to possible file names
        possible_names = [
            f"{import_name}.py",
            f"{import_name}/__init__.py",
            f"{import_name.replace('.', '/')}.py",
            f"{import_name.replace('.', '/')}/__init__.py",
        ]

        for name in possible_names:
            for file_path in all_files:
                if file_path.name == name or str(file_path).endswith(name):
                    matching_files.append(file_path)

        return matching_files

    def _find_files_by_name(self, file_name: str, all_files: List[Path]) -> List[Path]:
        """Find files by name."""
        matching_files = []

        for file_path in all_files:
            if file_path.name == file_name or str(file_path).endswith(file_name):
                matching_files.append(file_path)

        return matching_files

    def _build_dependency_maps(self):
        """Build dependency maps."""
        for reference in self.references:
            source = reference.source_file
            target = reference.target_file

            # Build forward dependency map
            if target not in self.dependency_map[source]:
                self.dependency_map[source].append(target)

            # Build reverse dependency map
            if source not in self.reverse_dependency_map[target]:
                self.reverse_dependency_map[target].append(source)

    def _identify_orphaned_files(self, all_files: List[Path]):
        """Identify orphaned files (files with no references)."""
        all_file_paths = {str(f) for f in all_files}
        referenced_files = {ref.target_file for ref in self.references}

        self.orphaned_files = all_file_paths - referenced_files

    def _identify_critical_files(self):
        """Identify critical files (files with many references)."""
        reference_counts = defaultdict(int)

        for reference in self.references:
            reference_counts[reference.target_file] += 1

        # Files with more than 5 references are considered critical
        self.critical_files = {file_path for file_path, count in reference_counts.items() if count > 5}

    def _generate_mapping_report(self) -> Dict[str, Any]:
        """Generate mapping report."""
        report = {
            "mapping_info": {
                "generated_at": datetime.now().isoformat(),
                "project_root": str(self.project_root),
                "total_references": len(self.references),
                "total_files_analyzed": len(self.reference_map),
                "report_version": "1.0",
            },
            "summary": {
                "total_references": len(self.references),
                "files_with_references": len(self.reference_map),
                "orphaned_files": len(self.orphaned_files),
                "critical_files": len(self.critical_files),
                "reference_types": {
                    "import": len([r for r in self.references if r.reference_type == "import"]),
                    "include": len([r for r in self.references if r.reference_type == "include"]),
                    "config": len([r for r in self.references if r.reference_type == "config"]),
                    "link": len([r for r in self.references if r.reference_type == "link"]),
                    "data": len([r for r in self.references if r.reference_type == "data"]),
                    "path": len([r for r in self.references if r.reference_type == "path"]),
                },
            },
            "references": [asdict(ref) for ref in self.references],
            "reference_map": {k: [asdict(ref) for ref in v] for k, v in self.reference_map.items()},
            "dependency_map": dict(self.dependency_map),
            "reverse_dependency_map": dict(self.reverse_dependency_map),
            "orphaned_files": list(self.orphaned_files),
            "critical_files": list(self.critical_files),
            "reorganization_impact": self._analyze_reorganization_impact(),
        }

        return report

    def _analyze_reorganization_impact(self) -> Dict[str, Any]:
        """Analyze the impact of reorganization."""
        impact = {"files_requiring_reference_updates": [], "critical_files_to_preserve": list(self.critical_files), "orphaned_files_safe_to_move": [], "high_impact_moves": [], "low_impact_moves": []}

        # Analyze each file for reorganization impact
        for file_path, references in self.reference_map.items():
            if len(references) > 3:  # High impact
                impact["high_impact_moves"].append({"file": file_path, "reference_count": len(references), "references": [ref.target_file for ref in references]})
            else:  # Low impact
                impact["low_impact_moves"].append({"file": file_path, "reference_count": len(references), "references": [ref.target_file for ref in references]})

        # Identify files that would require reference updates
        for reference in self.references:
            if reference.target_file not in impact["files_requiring_reference_updates"]:
                impact["files_requiring_reference_updates"].append(reference.target_file)

        # Identify orphaned files safe to move
        for orphaned_file in self.orphaned_files:
            if not orphaned_file.endswith((".py", ".json", ".yml", ".yaml")):  # Not critical file types
                impact["orphaned_files_safe_to_move"].append(orphaned_file)

        return impact


def main():
    """Main function for testing."""
    # Create mapper
    mapper = FileReferenceMapper()

    # Map all references
    report = mapper.map_all_references()

    # Display results
    print("🔗 File Reference Mapping - Reorganization Impact Analysis")
    print("=" * 60)
    print(f"Total References: {report['summary']['total_references']}")
    print(f"Files with References: {report['summary']['files_with_references']}")
    print(f"Orphaned Files: {report['summary']['orphaned_files']}")
    print(f"Critical Files: {report['summary']['critical_files']}")

    # Show reference types
    print("\n📊 Reference Types:")
    for ref_type, count in report["summary"]["reference_types"].items():
        print(f"  {ref_type}: {count} references")

    # Show critical files
    if report["critical_files"]:
        print("\n🔴 Critical Files (High Reference Count):")
        for file_path in report["critical_files"][:10]:  # Show first 10
            print(f"  {file_path}")

    # Show orphaned files
    if report["orphaned_files"]:
        print(f"\n🟡 Orphaned Files ({len(report['orphaned_files'])}):")
        for file_path in report["orphaned_files"][:10]:  # Show first 10
            print(f"  {file_path}")

    # Show reorganization impact
    impact = report["reorganization_impact"]
    print(f"\n📈 Reorganization Impact:")
    print(f"  Files requiring reference updates: {len(impact['files_requiring_reference_updates'])}")
    print(f"  Critical files to preserve: {len(impact['critical_files_to_preserve'])}")
    print(f"  Orphaned files safe to move: {len(impact['orphaned_files_safe_to_move'])}")
    print(f"  High impact moves: {len(impact['high_impact_moves'])}")
    print(f"  Low impact moves: {len(impact['low_impact_moves'])}")

    # Save report
    with open("file_reference_mapping_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Reference mapping report saved to: file_reference_mapping_report.json")


if __name__ == "__main__":
    main()
