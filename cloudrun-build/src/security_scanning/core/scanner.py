"""
Main Security Scanner - Multi-threaded security scanning orchestrator

This module implements the core security scanning functionality using
the worker pool for optimal performance and comprehensive coverage.
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from src.security_scanning.configuration.config_manager import ConfigManager
from src.security_scanning.patterns.pattern_manager import PatternManager
from src.security_scanning.reporting.report_generator import ReportGenerator
from src.security_scanning.utils.file_utils import FileUtils

from .worker_pool import WorkerPool

logger = logging.getLogger(__name__)


class SecurityScanner:
    """
    High-performance multi-threaded security scanner

    Features:
    - Multi-threaded file processing
    - Comprehensive file coverage
    - Intelligent file exclusions
    - Performance monitoring
    - Configurable scanning patterns
    - Multiple output formats
    """

    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize the security scanner

        Args:
            config: Configuration manager (auto-created if None)
        """
        self.config = config or ConfigManager()
        self.pattern_manager = PatternManager(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.file_utils = FileUtils()

        # Performance tracking
        self.scan_start_time = None
        self.scan_end_time = None
        self.files_scanned = 0
        self.findings_count = 0

        logger.info("Security scanner initialized")

    def scan_project(
        self,
        project_path: str = ".",
        exclude_patterns: Optional[list[str]] = None,
        include_patterns: Optional[list[str]] = None,
        max_workers: Optional[int] = None,
        show_progress: bool = True,
    ) -> dict[str, Any]:
        """
        Perform comprehensive security scan of project

        Args:
            project_path: Path to project root
            exclude_patterns: Patterns to exclude from scanning
            include_patterns: Patterns to include in scanning
            max_workers: Maximum number of worker threads
            show_progress: Show progress updates

        Returns:
            Comprehensive security scan report
        """
        project_path = Path(project_path)
        self.scan_start_time = time.time()

        logger.info(f"Starting security scan of {project_path}")

        try:
            # 1. Identify scannable files
            scannable_files = self._identify_scannable_files(project_path, exclude_patterns, include_patterns)

            if not scannable_files:
                logger.warning("No scannable files found")
                return self._create_empty_report()

            logger.info(f"Found {len(scannable_files)} scannable files")

            # 2. Initialize worker pool
            with WorkerPool(max_workers=max_workers, enable_monitoring=True) as worker_pool:
                # 3. Process files using worker pool
                worker_results = worker_pool.process_files(scannable_files, self._scan_single_file, show_progress=show_progress)

                # 4. Collect and process results
                all_findings = self._process_worker_results(worker_results)

                # 5. Generate performance summary
                performance_summary = worker_pool.get_performance_summary()

                # 6. Generate comprehensive report
                report = self._generate_scan_report(all_findings, performance_summary, project_path)

                self.scan_end_time = time.time()
                self.files_scanned = len(scannable_files)
                self.findings_count = len(all_findings)

                logger.info(f"Security scan completed in {self.scan_end_time - self.scan_start_time:.2f}s")
                logger.info(f"Scanned {self.files_scanned} files, found {self.findings_count} issues")

                return report

        except Exception as e:
            logger.error(f"Security scan failed: {e}")
            self.scan_end_time = time.time()
            return self._create_error_report(str(e))

    def scan_files(
        self,
        file_paths: list[str],
        max_workers: Optional[int] = None,
        show_progress: bool = True,
    ) -> dict[str, Any]:
        """
        Scan specific files for security issues

        Args:
            file_paths: List of file paths to scan
            max_workers: Maximum number of worker threads
            show_progress: Show progress updates

        Returns:
            Security scan report for specified files
        """
        if not file_paths:
            return self._create_empty_report()

        # Convert to Path objects and validate
        valid_files = []
        for file_path in file_paths:
            path = Path(file_path)
            if path.exists() and self.file_utils.is_scannable_file(path):
                valid_files.append(path)
            else:
                logger.warning(f"Skipping invalid file: {file_path}")

        if not valid_files:
            logger.warning("No valid files to scan")
            return self._create_empty_report()

        logger.info(f"Scanning {len(valid_files)} specified files")

        # Use the same scanning logic as project scan
        with WorkerPool(max_workers=max_workers, enable_monitoring=True) as worker_pool:
            worker_results = worker_pool.process_files(valid_files, self._scan_single_file, show_progress=show_progress)

            all_findings = self._process_worker_results(worker_results)
            performance_summary = worker_pool.get_performance_summary()

            return self._generate_scan_report(all_findings, performance_summary, Path.cwd())

    def _identify_scannable_files(
        self,
        project_path: Path,
        exclude_patterns: Optional[list[str]] = None,
        include_patterns: Optional[list[str]] = None,
    ) -> list[Path]:
        """
        Identify files that should be scanned for security issues

        Args:
            project_path: Project root path
            exclude_patterns: Patterns to exclude
            include_patterns: Patterns to include

        Returns:
            List of scannable file paths
        """
        # Use file utilities to identify scannable files
        scannable_files = self.file_utils.find_scannable_files(project_path, exclude_patterns, include_patterns)

        # Sort files for consistent processing order
        scannable_files.sort()

        return scannable_files

    def _scan_single_file(self, file_path: Path) -> list[dict[str, Any]]:
        """
        Scan a single file for security issues

        Args:
            file_path: Path to file to scan

        Returns:
            List of security findings for the file
        """
        try:
            # Use pattern manager to scan file
            findings = self.pattern_manager.scan_file(file_path)

            # Add file metadata to findings
            for finding in findings:
                finding["file_path"] = str(file_path)
                finding["file_size"] = file_path.stat().st_size
                finding["scan_timestamp"] = time.time()

            return findings

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")
            return [
                {
                    "file_path": str(file_path),
                    "error": str(e),
                    "scan_timestamp": time.time(),
                }
            ]

    def _process_worker_results(self, worker_results: list[Any]) -> list[dict[str, Any]]:
        """
        Process results from worker threads

        Args:
            worker_results: Results from worker pool

        Returns:
            Consolidated list of all findings
        """
        all_findings = []

        for result in worker_results:
            if isinstance(result, list):
                # Direct list of findings
                all_findings.extend(result)
            elif isinstance(result, dict):
                if result.get("success", False):
                    # Extract findings from result
                    if "data" in result:
                        # Single result wrapped in data field
                        all_findings.append(result["data"])
                    else:
                        # Direct result
                        all_findings.append(result)
                else:
                    logger.warning(f"Worker failed for {result.get('file_path', 'unknown')}: {result.get('error', 'unknown error')}")
            else:
                # Direct result
                all_findings.append(result)

        # Remove duplicates and sort by severity
        unique_findings = self._deduplicate_findings(all_findings)
        return self._sort_findings_by_severity(unique_findings)

    def _deduplicate_findings(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Remove duplicate findings based on content and location

        Args:
            findings: List of findings to deduplicate

        Returns:
            Deduplicated list of findings
        """
        seen = set()
        unique_findings = []

        for finding in findings:
            # Create unique key for deduplication
            if "pattern_name" in finding and "line_number" in finding:
                key = f"{finding['file_path']}:{finding['line_number']}:{finding['pattern_name']}"
            else:
                key = f"{finding['file_path']}:{finding.get('pattern_name', 'unknown')}"

            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)

        return unique_findings

    def _sort_findings_by_severity(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Sort findings by severity level

        Args:
            findings: List of findings to sort

        Returns:
            Sorted list of findings
        """
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}

        def severity_key(finding):
            severity = finding.get("severity", "LOW")
            return severity_order.get(severity, 5)

        return sorted(findings, key=severity_key)

    def _generate_scan_report(
        self,
        findings: list[dict[str, Any]],
        performance_summary: dict[str, Any],
        project_path: Path,
    ) -> dict[str, Any]:
        """
        Generate comprehensive security scan report

        Args:
            findings: List of security findings
            performance_summary: Performance metrics
            project_path: Project path that was scanned

        Returns:
            Comprehensive security report
        """
        # Generate report using report generator
        return self.report_generator.generate_report(
            findings=findings,
            performance_metrics=performance_summary,
            project_path=str(project_path),
            scan_duration=(self.scan_end_time - self.scan_start_time if self.scan_end_time else 0),
        )

    def _create_empty_report(self) -> dict[str, Any]:
        """Create empty report when no files to scan"""
        return {
            "summary": {
                "files_scanned": 0,
                "findings_count": 0,
                "scan_duration": 0.0,
                "status": "completed",
                "message": "No scannable files found",
            },
            "findings": [],
            "performance": {},
            "recommendations": ["No files were scanned"],
        }

    def _create_error_report(self, error_message: str) -> dict[str, Any]:
        """Create error report when scan fails"""
        return {
            "summary": {
                "files_scanned": self.files_scanned,
                "findings_count": self.findings_count,
                "scan_duration": (self.scan_end_time - self.scan_start_time if self.scan_end_time else 0),
                "status": "failed",
                "error": error_message,
            },
            "findings": [],
            "performance": {},
            "recommendations": [f"Fix error: {error_message}"],
        }

    def get_scan_statistics(self) -> dict[str, Any]:
        """Get statistics about the last scan"""
        if not self.scan_start_time:
            return {"status": "no_scan_performed"}

        duration = self.scan_end_time - self.scan_start_time if self.scan_end_time else 0

        return {
            "files_scanned": self.files_scanned,
            "findings_count": self.findings_count,
            "scan_duration": duration,
            "files_per_second": self.files_scanned / duration if duration > 0 else 0,
            "findings_per_file": (self.findings_count / self.files_scanned if self.files_scanned > 0 else 0),
        }

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Cleanup if needed


def create_security_scanner(config: Optional[ConfigManager] = None) -> SecurityScanner:
    """
    Factory function to create a security scanner

    Args:
        config: Configuration manager (auto-created if None)

    Returns:
        Configured security scanner instance
    """
    return SecurityScanner(config)
