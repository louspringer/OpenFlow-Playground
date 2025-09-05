"""
File Utilities for Security Scanning

This module provides utilities for file discovery and filtering
for security scanning operations.
"""

import logging
import mimetypes
from pathlib import Path
from typing import List, Set

logger = logging.getLogger(__name__)


class FileUtils:
    """
    Utilities for file discovery and filtering

    Features:
    - File discovery with exclusion patterns
    - File type detection
    - Size filtering
    - Cache and binary file exclusion
    """

    def __init__(self, max_file_size: int = 10 * 1024 * 1024):  # 10MB default
        """
        Initialize file utilities

        Args:
            max_file_size: Maximum file size to scan in bytes
        """
        self.max_file_size = max_file_size
        self.default_exclusions = self._get_default_exclusions()
        self.default_inclusions = self._get_default_inclusions()

        logger.debug("File utilities initialized")

    def _get_default_exclusions(self) -> set[str]:
        """Get default file exclusion patterns"""
        return {
            # Cache and temporary files
            "*.cache",
            "*.tmp",
            "*.temp",
            "*.log",
            "*.out",
            "*.err",
            # Coverage and test artifacts
            ".coverage",
            "coverage.xml",
            "htmlcov",
            ".pytest_cache",
            "test-results",
            "test-output",
            # IDE and editor files
            ".vscode",
            ".idea",
            ".vs",
            ".sublime-project",
            ".sublime-workspace",
            "*.sublime-project",
            "*.sublime-workspace",
            # OS generated files
            ".DS_Store",
            "Thumbs.db",
            "desktop.ini",
            # Specific cache files
            "api_discovery_cache.json",
            "cache.json",
            "maven-metadata.xml",
            "maven-metadata-local.xml",
            # Large data files
            "*.csv",
            "*.tsv",
            "*.jsonl",
            "*.parquet",
            "*.avro",
            "*.h5",
            "*.hdf5",
            "*.pkl",
            "*.pickle",
            # Database files
            "*.db",
            "*.sqlite",
            "*.sqlite3",
            "*.mdb",
            "*.accdb",
        }

    def _get_default_inclusions(self) -> set[str]:
        """Get default file inclusion patterns"""
        return {
            # Source code files
            "*.py",
            "*.js",
            "*.ts",
            "*.jsx",
            "*.tsx",
            "*.vue",
            "*.java",
            "*.c",
            "*.cpp",
            "*.h",
            "*.hpp",
            "*.cs",
            "*.go",
            "*.rs",
            "*.rb",
            "*.php",
            "*.swift",
            "*.kt",
            # Configuration files
            "*.yaml",
            "*.yml",
            "*.json",
            "*.toml",
            "*.ini",
            "*.cfg",
            "*.conf",
            "*.config",
            "*.properties",
            "*.env",
            # Documentation files
            "*.md",
            "*.rst",
            "*.txt",
            "*.adoc",
            "*.asciidoc",
            "*.html",
            "*.htm",
            "*.xml",
            "*.svg",
            # Shell and script files
            "*.sh",
            "*.bash",
            "*.zsh",
            "*.fish",
            "*.ps1",
            "*.bat",
            "*.cmd",
            "*.vbs",
            "*.pl",
            # Infrastructure files
            "*.tf",
            "*.hcl",
            "Dockerfile*",
            "docker-compose*.yml",
            "*.dockerfile",
            # CI/CD files
            ".github/workflows/*.yml",
            ".gitlab-ci.yml",
            "Jenkinsfile",
            "azure-pipelines.yml",
            ".travis.yml",
            "circle.yml",
            # Package management
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "Pipfile",
            "package.json",
            "composer.json",
            "pom.xml",
            "build.gradle",
            "Cargo.toml",
            "go.mod",
            "Gemfile",
            "Rakefile",
        }

    def is_scannable_file(self, file_path: Path) -> bool:
        """
        Check if a file should be scanned for security issues

        Args:
            file_path: Path to file to check

        Returns:
            True if file should be scanned
        """
        try:
            # Check if file exists and is a file
            if not file_path.exists() or not file_path.is_file():
                return False

            # Check file size limit
            if file_path.stat().st_size > self.max_file_size:
                logger.debug(f"Skipping large file: {file_path} ({file_path.stat().st_size} bytes)")
                return False

            # Check if file is excluded
            if self._is_excluded_file(file_path):
                return False

            # Check if file is included
            if not self._is_included_file(file_path):
                return False

            # Check if file is text-based
            return self._is_text_file(file_path)

        except Exception as e:
            logger.warning(f"Error checking file {file_path}: {e}")
            return False

    def _is_excluded_file(self, file_path: Path) -> bool:
        """
        Check if file matches exclusion patterns

        Args:
            file_path: Path to file to check

        Returns:
            True if file should be excluded
        """
        file_name = file_path.name.lower()
        parent_dirs = [p.name.lower() for p in file_path.parents]

        for pattern in self.default_exclusions:
            if pattern.startswith(("*.", "*")):
                if file_name.endswith(pattern[1:]):
                    return True
            elif pattern in file_name or pattern in parent_dirs:
                return True

        return False

    def _is_included_file(self, file_path: Path) -> bool:
        """
        Check if file matches inclusion patterns

        Args:
            file_path: Path to file to check

        Returns:
            True if file should be included
        """
        file_name = file_path.name.lower()

        for pattern in self.default_inclusions:
            if pattern.startswith(("*.", "*")):
                if file_name.endswith(pattern[1:]):
                    return True
            elif pattern in file_name:
                return True

        return False

    def _is_text_file(self, file_path: Path) -> bool:
        """
        Check if file is text-based

        Args:
            file_path: Path to file to check

        Returns:
            True if file is text-based
        """
        try:
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and mime_type.startswith("text/"):
                return True

            # Check file extension for known text files
            text_extensions = {
                ".py",
                ".js",
                ".ts",
                ".jsx",
                ".tsx",
                ".vue",
                ".java",
                ".c",
                ".cpp",
                ".h",
                ".hpp",
                ".cs",
                ".go",
                ".rs",
                ".rb",
                ".php",
                ".swift",
                ".kt",
                ".yaml",
                ".yml",
                ".json",
                ".toml",
                ".ini",
                ".cfg",
                ".conf",
                ".config",
                ".properties",
                ".env",
                ".md",
                ".rst",
                ".txt",
                ".adoc",
                ".asciidoc",
                ".html",
                ".htm",
                ".xml",
                ".svg",
                ".sh",
                ".bash",
                ".zsh",
                ".fish",
                ".ps1",
                ".bat",
                ".cmd",
                ".vbs",
                ".tf",
                ".hcl",
                ".dockerfile",
            }

            if file_path.suffix.lower() in text_extensions:
                return True

            # Try to read first few bytes to check if it's text
            try:
                with open(file_path, encoding="utf-8") as f:
                    f.read(1024)
                return True
            except (UnicodeDecodeError, UnicodeError):
                return False

        except Exception as e:
            logger.debug(f"Error checking if {file_path} is text: {e}")
            return False

    def find_scannable_files(
        self,
        project_path: Path,
        exclude_patterns: list[str] = None,
        include_patterns: list[str] = None,
    ) -> list[Path]:
        """
        Find all scannable files in a project directory

        Args:
            project_path: Root path of project to scan
            exclude_patterns: Additional exclusion patterns
            include_patterns: Additional inclusion patterns

        Returns:
            List of scannable file paths
        """
        if not project_path.exists() or not project_path.is_dir():
            logger.warning(f"Project path does not exist or is not a directory: {project_path}")
            return []

        # Add custom patterns to defaults
        custom_exclusions = set(exclude_patterns or [])
        custom_inclusions = set(include_patterns or [])

        all_exclusions = self.default_exclusions | custom_exclusions
        all_inclusions = self.default_inclusions | custom_inclusions

        scannable_files = []
        total_files = 0
        excluded_files = 0

        logger.info(f"Scanning for files in {project_path}")

        try:
            # Walk through project directory
            for file_path in project_path.rglob("*"):
                total_files += 1

                if file_path.is_file():
                    # Check if file should be scanned
                    if self._is_scannable_with_patterns(file_path, all_exclusions, all_inclusions):
                        scannable_files.append(file_path)
                    else:
                        excluded_files += 1

                        # Log some exclusions for debugging
                        if excluded_files <= 10:
                            logger.debug(f"Excluded: {file_path}")
                        elif excluded_files == 11:
                            logger.debug("... and more files excluded")

            logger.info(f"File discovery complete: {len(scannable_files)} scannable, {excluded_files} excluded, {total_files} total")

            return scannable_files

        except Exception as e:
            logger.error(f"Error discovering files in {project_path}: {e}")
            return []

    def _is_scannable_with_patterns(self, file_path: Path, exclusions: set[str], inclusions: set[str]) -> bool:
        """
        Check if file is scannable using custom patterns

        Args:
            file_path: Path to file to check
            exclusions: Set of exclusion patterns
            inclusions: Set of inclusion patterns

        Returns:
            True if file should be scanned
        """
        try:
            # Check file size
            if file_path.stat().st_size > self.max_file_size:
                return False

            # Check exclusions
            file_name = file_path.name.lower()
            parent_dirs = [p.name.lower() for p in file_path.parents]

            for pattern in exclusions:
                if pattern.startswith(("*.", "*")):
                    if file_name.endswith(pattern[1:]):
                        return False
                elif pattern in file_name or pattern in parent_dirs:
                    return False

            # Check inclusions
            for pattern in inclusions:
                if pattern.startswith(("*.", "*")):
                    if file_name.endswith(pattern[1:]):
                        return True
                elif pattern in file_name:
                    return True

            # Default to False if no inclusion patterns match
            return False

        except Exception as e:
            logger.warning(f"Error checking patterns for {file_path}: {e}")
            return False

    def get_file_statistics(self, file_paths: list[Path]) -> dict:
        """
        Get statistics about the files to be scanned

        Args:
            file_paths: List of file paths to analyze

        Returns:
            Dictionary with file statistics
        """
        if not file_paths:
            return {}

        stats = {
            "total_files": len(file_paths),
            "total_size": 0,
            "file_types": {},
            "largest_files": [],
            "average_size": 0,
        }

        try:
            # Calculate statistics
            for file_path in file_paths:
                try:
                    file_size = file_path.stat().st_size
                    stats["total_size"] += file_size

                    # Count file types
                    extension = file_path.suffix.lower()
                    stats["file_types"][extension] = stats["file_types"].get(extension, 0) + 1

                    # Track largest files
                    stats["largest_files"].append((file_path, file_size))

                except Exception as e:
                    logger.debug(f"Error getting stats for {file_path}: {e}")

            # Calculate averages and sort largest files
            if stats["total_files"] > 0:
                stats["average_size"] = stats["total_size"] / stats["total_files"]

            # Sort largest files by size (descending)
            stats["largest_files"].sort(key=lambda x: x[1], reverse=True)
            stats["largest_files"] = stats["largest_files"][:10]  # Top 10

            # Sort file types by count (descending)
            stats["file_types"] = dict(sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True))

        except Exception as e:
            logger.error(f"Error calculating file statistics: {e}")

        return stats
