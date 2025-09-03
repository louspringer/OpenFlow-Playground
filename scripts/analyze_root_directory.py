#!/usr/bin/env python3
"""
Root Directory Analysis Script
Analyzes the current root directory structure and categorizes files for reorganization
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """File information for categorization."""

    path: str
    name: str
    extension: str
    size: int
    category: str
    subcategory: str
    domain: str
    references: List[str]
    dependencies: List[str]
    is_duplicate: bool
    is_archived: bool
    is_experimental: bool
    is_config: bool
    is_documentation: bool
    is_script: bool
    is_data: bool
    is_model: bool
    is_report: bool
    is_cache: bool
    is_backup: bool
    is_temporary: bool
    is_legacy: bool
    is_deprecated: bool
    is_orphaned: bool
    priority: str  # 'keep', 'move', 'archive', 'delete'
    suggested_location: str
    notes: str


class RootDirectoryAnalyzer:
    """Analyzes root directory structure for reorganization."""

    def __init__(self, project_root: str = "."):
        """Initialize the analyzer."""
        self.project_root = Path(project_root)
        self.files: List[FileInfo] = []
        self.categories: Dict[str, List[FileInfo]] = defaultdict(list)
        self.domains: Dict[str, List[FileInfo]] = defaultdict(list)
        self.duplicates: List[List[FileInfo]] = []
        self.orphaned_files: List[FileInfo] = []
        self.references: Dict[str, List[str]] = defaultdict(list)
        self.dependencies: Dict[str, List[str]] = defaultdict(list)

        # Load project model registry
        self.project_model = self._load_project_model()

        logger.info("Root Directory Analyzer initialized")

    def _load_project_model(self) -> Dict[str, Any]:
        """Load project model registry."""
        model_path = self.project_root / "project_model_registry.json"
        if model_path.exists():
            with open(model_path, "r") as f:
                return json.load(f)
        return {}

    def analyze_root_directory(self) -> Dict[str, Any]:
        """Analyze the root directory structure."""
        logger.info("Analyzing root directory structure...")

        # Get all files in root directory
        root_files = [f for f in self.project_root.iterdir() if f.is_file()]

        logger.info(f"Found {len(root_files)} files in root directory")

        # Analyze each file
        for file_path in root_files:
            file_info = self._analyze_file(file_path)
            self.files.append(file_info)

            # Categorize file
            self.categories[file_info.category].append(file_info)
            self.domains[file_info.domain].append(file_info)

            # Check for duplicates
            self._check_duplicates(file_info)

            # Check for orphaned files
            if file_info.is_orphaned:
                self.orphaned_files.append(file_info)

        # Analyze references and dependencies
        self._analyze_references()
        self._analyze_dependencies()

        # Generate analysis report
        report = self._generate_analysis_report()

        logger.info(f"Analysis complete: {len(self.files)} files analyzed")
        return report

    def _analyze_file(self, file_path: Path) -> FileInfo:
        """Analyze a single file."""
        name = file_path.name
        extension = file_path.suffix.lower()
        size = file_path.stat().st_size

        # Determine category
        category = self._determine_category(name, extension, size)
        subcategory = self._determine_subcategory(name, extension)
        domain = self._determine_domain(name, extension)

        # Determine file properties
        is_duplicate = self._is_duplicate(name)
        is_archived = self._is_archived(name)
        is_experimental = self._is_experimental(name)
        is_config = self._is_config(name, extension)
        is_documentation = self._is_documentation(name, extension)
        is_script = self._is_script(name, extension)
        is_data = self._is_data(name, extension)
        is_model = self._is_model(name, extension)
        is_report = self._is_report(name, extension)
        is_cache = self._is_cache(name, extension)
        is_backup = self._is_backup(name, extension)
        is_temporary = self._is_temporary(name, extension)
        is_legacy = self._is_legacy(name, extension)
        is_deprecated = self._is_deprecated(name, extension)
        is_orphaned = self._is_orphaned(name, extension, domain)

        # Determine priority
        priority = self._determine_priority(
            is_duplicate, is_archived, is_experimental, is_config, is_documentation, is_script, is_data, is_model, is_report, is_cache, is_backup, is_temporary, is_legacy, is_deprecated, is_orphaned
        )

        # Suggest location
        suggested_location = self._suggest_location(category, subcategory, domain, priority)

        # Generate notes
        notes = self._generate_notes(
            is_duplicate, is_archived, is_experimental, is_config, is_documentation, is_script, is_data, is_model, is_report, is_cache, is_backup, is_temporary, is_legacy, is_deprecated, is_orphaned
        )

        return FileInfo(
            path=str(file_path),
            name=name,
            extension=extension,
            size=size,
            category=category,
            subcategory=subcategory,
            domain=domain,
            references=[],
            dependencies=[],
            is_duplicate=is_duplicate,
            is_archived=is_archived,
            is_experimental=is_experimental,
            is_config=is_config,
            is_documentation=is_documentation,
            is_script=is_script,
            is_data=is_data,
            is_model=is_model,
            is_report=is_report,
            is_cache=is_cache,
            is_backup=is_backup,
            is_temporary=is_temporary,
            is_legacy=is_legacy,
            is_deprecated=is_deprecated,
            is_orphaned=is_orphaned,
            priority=priority,
            suggested_location=suggested_location,
            notes=notes,
        )

    def _determine_category(self, name: str, extension: str, size: int) -> str:
        """Determine file category."""
        if extension in [".py"]:
            if "test" in name.lower():
                return "test"
            elif "demo" in name.lower():
                return "experimental"
            elif "analyze" in name.lower() or "check" in name.lower():
                return "tool"
            elif "generate" in name.lower() or "create" in name.lower():
                return "tool"
            elif "debug" in name.lower() or "fix" in name.lower():
                return "tool"
            else:
                return "script"
        elif extension in [".md", ".rst", ".txt"]:
            return "documentation"
        elif extension in [".json"]:
            if "model" in name.lower():
                return "model"
            elif "report" in name.lower() or "analysis" in name.lower():
                return "report"
            elif "cache" in name.lower():
                return "cache"
            elif "config" in name.lower():
                return "config"
            else:
                return "data"
        elif extension in [".yml", ".yaml"]:
            return "config"
        elif extension in [".log"]:
            return "log"
        elif extension in [".dot", ".svg", ".png", ".jpg"]:
            return "visualization"
        elif extension in [".cypher"]:
            return "data"
        elif extension in [".jar", ".exe", ".dll", ".so"]:
            return "binary"
        elif extension in [".backup", ".bak"]:
            return "backup"
        elif extension in [".tmp", ".temp"]:
            return "temporary"
        else:
            return "other"

    def _determine_subcategory(self, name: str, extension: str) -> str:
        """Determine file subcategory."""
        if "ghostbusters" in name.lower():
            return "ghostbusters"
        elif "round_trip" in name.lower():
            return "round_trip"
        elif "artifact" in name.lower():
            return "artifact"
        elif "quality" in name.lower():
            return "quality"
        elif "security" in name.lower():
            return "security"
        elif "test" in name.lower():
            return "test"
        elif "demo" in name.lower():
            return "demo"
        elif "analysis" in name.lower():
            return "analysis"
        elif "report" in name.lower():
            return "report"
        elif "model" in name.lower():
            return "model"
        elif "config" in name.lower():
            return "config"
        elif "cache" in name.lower():
            return "cache"
        elif "backup" in name.lower():
            return "backup"
        elif "temp" in name.lower() or "tmp" in name.lower():
            return "temporary"
        else:
            return "general"

    def _determine_domain(self, name: str, extension: str) -> str:
        """Determine file domain."""
        # Check against project model domains
        if self.project_model and "domains" in self.project_model:
            for domain_name, domain_config in self.project_model["domains"].items():
                if "patterns" in domain_config:
                    for pattern in domain_config["patterns"]:
                        if self._matches_pattern(name, pattern):
                            return domain_name

        # Fallback to name-based detection
        if "ghostbusters" in name.lower():
            return "ghostbusters"
        elif "round_trip" in name.lower():
            return "round_trip"
        elif "artifact" in name.lower():
            return "artifact_forge"
        elif "quality" in name.lower():
            return "code_quality"
        elif "security" in name.lower():
            return "security"
        elif "test" in name.lower():
            return "testing"
        elif "demo" in name.lower():
            return "demo"
        elif "analysis" in name.lower():
            return "analysis"
        elif "report" in name.lower():
            return "reporting"
        elif "model" in name.lower():
            return "model_driven"
        elif "config" in name.lower():
            return "configuration"
        elif "cache" in name.lower():
            return "caching"
        elif "backup" in name.lower():
            return "backup"
        elif "temp" in name.lower() or "tmp" in name.lower():
            return "temporary"
        else:
            return "orphaned"

    def _matches_pattern(self, name: str, pattern: str) -> bool:
        """Check if name matches pattern."""
        # Simple pattern matching (can be enhanced)
        if "*" in pattern:
            import fnmatch

            return fnmatch.fnmatch(name, pattern)
        else:
            return name == pattern

    def _is_duplicate(self, name: str) -> bool:
        """Check if file is a duplicate."""
        return " 2" in name or " copy" in name or " backup" in name

    def _is_archived(self, name: str) -> bool:
        """Check if file is archived."""
        return "old" in name.lower() or "archive" in name.lower()

    def _is_experimental(self, name: str) -> bool:
        """Check if file is experimental."""
        return "demo" in name.lower() or "experiment" in name.lower() or "prototype" in name.lower()

    def _is_config(self, name: str, extension: str) -> bool:
        """Check if file is configuration."""
        return extension in [".yml", ".yaml", ".json"] and "config" in name.lower()

    def _is_documentation(self, name: str, extension: str) -> bool:
        """Check if file is documentation."""
        return extension in [".md", ".rst", ".txt"] and not "test" in name.lower()

    def _is_script(self, name: str, extension: str) -> bool:
        """Check if file is a script."""
        return extension in [".py", ".sh", ".bash"] and not "test" in name.lower()

    def _is_data(self, name: str, extension: str) -> bool:
        """Check if file is data."""
        return extension in [".json", ".csv", ".xml", ".cypher"] and not "config" in name.lower()

    def _is_model(self, name: str, extension: str) -> bool:
        """Check if file is a model."""
        return extension in [".json"] and "model" in name.lower()

    def _is_report(self, name: str, extension: str) -> bool:
        """Check if file is a report."""
        return extension in [".json", ".md"] and "report" in name.lower()

    def _is_cache(self, name: str, extension: str) -> bool:
        """Check if file is cache."""
        return "cache" in name.lower() or extension in [".cache", ".tmp"]

    def _is_backup(self, name: str, extension: str) -> bool:
        """Check if file is backup."""
        return "backup" in name.lower() or extension in [".backup", ".bak"]

    def _is_temporary(self, name: str, extension: str) -> bool:
        """Check if file is temporary."""
        return "temp" in name.lower() or "tmp" in name.lower() or extension in [".tmp", ".temp"]

    def _is_legacy(self, name: str, extension: str) -> bool:
        """Check if file is legacy."""
        return "legacy" in name.lower() or "old" in name.lower()

    def _is_deprecated(self, name: str, extension: str) -> bool:
        """Check if file is deprecated."""
        return "deprecated" in name.lower() or "deprecate" in name.lower()

    def _is_orphaned(self, name: str, extension: str, domain: str) -> bool:
        """Check if file is orphaned."""
        return domain == "orphaned" or extension in [".tmp", ".temp", ".cache"]

    def _determine_priority(self, *flags) -> str:
        """Determine file priority."""
        if any(flags[0:3]):  # duplicate, archived, experimental
            return "archive"
        elif any(flags[3:6]):  # config, documentation, script
            return "keep"
        elif any(flags[6:9]):  # data, model, report
            return "move"
        elif any(flags[9:12]):  # cache, backup, temporary
            return "delete"
        elif any(flags[12:15]):  # legacy, deprecated, orphaned
            return "archive"
        else:
            return "move"

    def _suggest_location(self, category: str, subcategory: str, domain: str, priority: str) -> str:
        """Suggest file location."""
        if priority == "delete":
            return "DELETE"
        elif priority == "archive":
            return "archive/"
        elif category == "config":
            return "config/"
        elif category == "documentation":
            return "docs/"
        elif category == "script":
            return "scripts/"
        elif category == "tool":
            return "tools/"
        elif category == "experimental":
            return "experiments/"
        elif category == "model":
            return "artifacts/models/"
        elif category == "report":
            return "artifacts/reports/"
        elif category == "data":
            return "data/"
        elif category == "cache":
            return "artifacts/cache/"
        elif category == "log":
            return "logs/"
        elif category == "backup":
            return "archive/backups/"
        elif category == "temporary":
            return "DELETE"
        else:
            return "artifacts/analysis/"

    def _generate_notes(self, *flags) -> str:
        """Generate notes for file."""
        notes = []
        if flags[0]:  # duplicate
            notes.append("Duplicate file")
        if flags[1]:  # archived
            notes.append("Archived file")
        if flags[2]:  # experimental
            notes.append("Experimental code")
        if flags[3]:  # config
            notes.append("Configuration file")
        if flags[4]:  # documentation
            notes.append("Documentation file")
        if flags[5]:  # script
            notes.append("Script file")
        if flags[6]:  # data
            notes.append("Data file")
        if flags[7]:  # model
            notes.append("Model file")
        if flags[8]:  # report
            notes.append("Report file")
        if flags[9]:  # cache
            notes.append("Cache file")
        if flags[10]:  # backup
            notes.append("Backup file")
        if flags[11]:  # temporary
            notes.append("Temporary file")
        if flags[12]:  # legacy
            notes.append("Legacy file")
        if flags[13]:  # deprecated
            notes.append("Deprecated file")
        if flags[14]:  # orphaned
            notes.append("Orphaned file")

        return "; ".join(notes) if notes else "No special notes"

    def _check_duplicates(self, file_info: FileInfo):
        """Check for duplicate files."""
        # Simple duplicate detection based on name patterns
        if file_info.is_duplicate:
            # Find potential duplicates
            base_name = file_info.name.replace(" 2", "").replace(" copy", "").replace(" backup", "")
            duplicates = [f for f in self.files if f.name.startswith(base_name) and f != file_info]
            if duplicates:
                self.duplicates.append([file_info] + duplicates)

    def _analyze_references(self):
        """Analyze file references."""
        # This would analyze actual file references
        # For now, we'll use a simple approach
        for file_info in self.files:
            if file_info.extension == ".py":
                # Check for imports and references
                try:
                    with open(file_info.path, "r") as f:
                        content = f.read()
                        # Simple reference detection
                        for other_file in self.files:
                            if other_file.name in content and other_file != file_info:
                                self.references[file_info.name].append(other_file.name)
                except Exception as e:
                    logger.debug(f"Error reading {file_info.path}: {e}")

    def _analyze_dependencies(self):
        """Analyze file dependencies."""
        # This would analyze actual file dependencies
        # For now, we'll use a simple approach
        for file_info in self.files:
            if file_info.extension == ".py":
                # Check for imports
                try:
                    with open(file_info.path, "r") as f:
                        content = f.read()
                        # Simple import detection
                        import re

                        imports = re.findall(r"import\s+(\w+)", content)
                        for imp in imports:
                            # Find matching files
                            matching_files = [f for f in self.files if f.name.startswith(imp)]
                            self.dependencies[file_info.name].extend([f.name for f in matching_files])
                except Exception as e:
                    logger.debug(f"Error reading {file_info.path}: {e}")

    def _generate_analysis_report(self) -> Dict[str, Any]:
        """Generate analysis report."""
        report = {
            "analysis_info": {"generated_at": datetime.now().isoformat(), "project_root": str(self.project_root), "total_files": len(self.files), "report_version": "1.0"},
            "summary": {
                "total_files": len(self.files),
                "categories": {cat: len(files) for cat, files in self.categories.items()},
                "domains": {domain: len(files) for domain, files in self.domains.items()},
                "duplicates": len(self.duplicates),
                "orphaned_files": len(self.orphaned_files),
                "files_to_delete": len([f for f in self.files if f.priority == "delete"]),
                "files_to_archive": len([f for f in self.files if f.priority == "archive"]),
                "files_to_move": len([f for f in self.files if f.priority == "move"]),
                "files_to_keep": len([f for f in self.files if f.priority == "keep"]),
            },
            "categories": {cat: [asdict(f) for f in files] for cat, files in self.categories.items()},
            "domains": {domain: [asdict(f) for f in files] for domain, files in self.domains.items()},
            "duplicates": [[asdict(f) for f in group] for group in self.duplicates],
            "orphaned_files": [asdict(f) for f in self.orphaned_files],
            "references": dict(self.references),
            "dependencies": dict(self.dependencies),
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations."""
        recommendations = []

        if len(self.orphaned_files) > 0:
            recommendations.append(f"Archive {len(self.orphaned_files)} orphaned files")

        if len(self.duplicates) > 0:
            recommendations.append(f"Remove {len(self.duplicates)} duplicate files")

        if len([f for f in self.files if f.priority == "delete"]) > 0:
            recommendations.append(f"Delete {len([f for f in self.files if f.priority == 'delete'])} temporary/cache files")

        if len([f for f in self.files if f.priority == "move"]) > 0:
            recommendations.append(f"Move {len([f for f in self.files if f.priority == 'move'])} files to appropriate directories")

        if len([f for f in self.files if f.priority == "archive"]) > 0:
            recommendations.append(f"Archive {len([f for f in self.files if f.priority == 'archive'])} legacy/deprecated files")

        recommendations.append("Create new directory structure: artifacts/, tools/, experiments/, archive/")
        recommendations.append("Update Makefile references to new directory structure")
        recommendations.append("Update project model registry with new file paths")
        recommendations.append("Update Python import statements")
        recommendations.append("Update documentation references")

        return recommendations


def main():
    """Main function for testing."""
    # Create analyzer
    analyzer = RootDirectoryAnalyzer()

    # Analyze root directory
    report = analyzer.analyze_root_directory()

    # Display results
    print("🗂️ Root Directory Analysis - Reorganization Planning")
    print("=" * 60)
    print(f"Total Files: {report['summary']['total_files']}")
    print(f"Categories: {len(report['summary']['categories'])}")
    print(f"Domains: {len(report['summary']['domains'])}")
    print(f"Duplicates: {report['summary']['duplicates']}")
    print(f"Orphaned Files: {report['summary']['orphaned_files']}")
    print(f"Files to Delete: {report['summary']['files_to_delete']}")
    print(f"Files to Archive: {report['summary']['files_to_archive']}")
    print(f"Files to Move: {report['summary']['files_to_move']}")
    print(f"Files to Keep: {report['summary']['files_to_keep']}")

    # Show categories
    print("\n📊 File Categories:")
    for category, count in report["summary"]["categories"].items():
        print(f"  {category}: {count} files")

    # Show domains
    print("\n🏷️ File Domains:")
    for domain, count in report["summary"]["domains"].items():
        print(f"  {domain}: {count} files")

    # Show recommendations
    print("\n💡 Recommendations:")
    for recommendation in report["recommendations"]:
        print(f"  • {recommendation}")

    # Save report
    with open("root_directory_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Analysis report saved to: root_directory_analysis_report.json")


if __name__ == "__main__":
    main()
