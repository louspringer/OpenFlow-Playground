#!/usr/bin/env python3
"""
Command-line interface for the multi-threaded security scanner

This CLI provides easy access to the security scanning functionality
with proper performance monitoring and reporting.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.security_scanning import SecurityScanner, create_security_scanner

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Multi-threaded Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  python -m src.security_scanning.cli.main

  # Scan specific directory
  python -m src.security_scanning.cli.main --path /path/to/project

  # Scan with custom worker count
  python -m src.security_scanning.cli.main --workers 8

  # Scan specific files
  python -m src.security_scanning.cli.main --files file1.py file2.py

  # Export to JSON
  python -m src.security_scanning.cli.main --output report.json
        """,
    )

    parser.add_argument("--path", default=".", help="Path to scan (default: current directory)")

    parser.add_argument("--files", nargs="+", help="Specific files to scan (overrides --path)")

    parser.add_argument(
        "--workers",
        type=int,
        help="Number of worker threads (auto-detected if not specified)",
    )

    parser.add_argument("--output", help="Output file for JSON report")

    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    parser.add_argument("--version", action="version", version="1.0.0")

    args = parser.parse_args()

    try:
        # Create security scanner
        scanner = create_security_scanner()

        if args.files:
            # Scan specific files
            logger.info(f"Scanning {len(args.files)} specified files")
            report = scanner.scan_files(
                file_paths=args.files,
                max_workers=args.workers,
                show_progress=not args.quiet,
            )
        else:
            # Scan entire project
            logger.info(f"Scanning project at {args.path}")
            report = scanner.scan_project(
                project_path=args.path,
                max_workers=args.workers,
                show_progress=not args.quiet,
            )

        # Print console report
        scanner.report_generator.print_console_report(report)

        # Export to JSON if requested
        if args.output:
            scanner.report_generator.export_json(report, args.output)
            logger.info(f"Report exported to {args.output}")

        # Exit with appropriate code
        if report["summary"]["critical_issues"] > 0:
            logger.error("Critical security issues found!")
            sys.exit(1)
        elif report["summary"]["high_issues"] > 0:
            logger.warning("High priority security issues found")
            sys.exit(2)
        else:
            logger.info("No critical security issues found")
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Security scan failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
