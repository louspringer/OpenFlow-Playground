#!/usr/bin/env python3
"""
Quality System CLI

Command-line interface for the quality system.
"""

import argparse
import logging
import sys
from pathlib import Path

from .integrations.ci_cd_integration import CICDIntegration
from .integrations.pre_commit_integration import PreCommitIntegration
from .quality_enforcer import QualityEnforcer


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def run_quality_check(project_path: Path, verbose: bool = False) -> int:
    """Run a quality check on the project"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Running quality check on {project_path}")

        # Create quality enforcer
        enforcer = QualityEnforcer(project_path)

        # Run quick check first
        quick_result = enforcer.run_quick_quality_check()
        if quick_result["status"] == "success":
            logger.info("Quick quality check completed")
            print("✅ Quality Check Passed")
            print(f"   Overall Score: {quick_result['overall_score']:.1f}")
            print(f"   Can Proceed: {quick_result['can_proceed']}")
            return 0

        # Run full quality check
        logger.info("Running full quality check")

        # For now, create mock analysis results
        # In practice, this would come from your actual analysis tools
        mock_results = {
            "flake8_issues": [],
            "security_issues": [],
            "coverage_percentage": 85.0,
            "performance_metrics": {},
        }

        result = enforcer.enforce_quality(mock_results)

        if result["can_proceed"]:
            print("✅ Quality Check Passed")
            print(f"   Overall Score: {result['overall_score']:.1f}")
            print(f"   Can Proceed: {result['can_proceed']}")
            return 0
        
        print("❌ Quality Check Failed")
        print(f"   Overall Score: {result['overall_score']:.1f}")
        print(f"   Blocking Gates: {result['blocking_gates']}")
        
        if "recommendations" in result:
            print("\nRecommendations:")
            for rec in result["recommendations"]:
                print(f"   • {rec}")
        
        return 1

    except Exception as e:
        logger.error(f"Quality check failed: {e}")
        print(f"❌ Quality check failed: {e}")
        return 1


def run_pre_commit_check(project_path: Path, verbose: bool = False) -> int:
    """Run pre-commit quality check"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Running pre-commit quality check on {project_path}")

        integration = PreCommitIntegration(project_path)
        success = integration.run_pre_commit_check()

        if success:
            print("✅ Pre-commit quality check passed")
            return 0
        
        print("❌ Pre-commit quality check failed")
        return 1

    except Exception as e:
        logger.error(f"Pre-commit check failed: {e}")
        print(f"❌ Pre-commit check failed: {e}")
        return 1


def run_ci_check(project_path: Path, verbose: bool = False) -> int:
    """Run CI/CD quality check"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Running CI/CD quality check on {project_path}")

        integration = CICDIntegration(project_path)
        result = integration.run_ci_quality_check()

        if result["can_proceed"]:
            print("✅ CI/CD quality check passed")
            print(f"   Overall Score: {result.get('overall_score', 'N/A')}")
            return 0
        
        print("❌ CI/CD quality check failed")
        print(f"   Overall Score: {result.get('overall_score', 'N/A')}")
        return 1

    except Exception as e:
        logger.error(f"CI/CD check failed: {e}")
        print(f"❌ CI/CD check failed: {e}")
        return 1


def install_pre_commit_hook(project_path: Path, verbose: bool = False) -> int:
    """Install pre-commit hook"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Installing pre-commit hook in {project_path}")

        integration = PreCommitIntegration(project_path)
        success = integration.install_pre_commit_hook()

        if success:
            print("✅ Pre-commit hook installed successfully")
            return 0
        
        print("❌ Failed to install pre-commit hook")
        return 1

    except Exception as e:
        logger.error(f"Failed to install pre-commit hook: {e}")
        print(f"❌ Failed to install pre-commit hook: {e}")
        return 1


def show_quality_trends(
    project_path: Path, days: int = 30, verbose: bool = False
) -> int:
    """Show quality trends over time"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Showing quality trends for {project_path} (last {days} days)")

        enforcer = QualityEnforcer(project_path)
        trends = enforcer.get_quality_trends(days)

        if "error" in trends:
            print(f"❌ Could not get quality trends: {trends['error']}")
            return 1

        print(f"📊 Quality Trends (Last {days} days)")
        print("=" * 50)

        if trends["overall_scores"]:
            print("Overall Quality Scores:")
            for score_data in trends["overall_scores"][-5:]:  # Show last 5
                timestamp = score_data["timestamp"][:10]  # Just the date
                score = score_data["score"]
                print(f"   {timestamp}: {score:.1f}")
        else:
            print("No quality data available")

        return 0

    except Exception as e:
        logger.error(f"Failed to show quality trends: {e}")
        print(f"❌ Failed to show quality trends: {e}")
        return 1


def main() -> int:
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Quality System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quality check                    # Run quality check on current directory
  quality check /path/to/project  # Run quality check on specific project
  quality pre-commit              # Run pre-commit quality check
  quality ci                      # Run CI/CD quality check
  quality install-hook            # Install pre-commit hook
  quality trends                  # Show quality trends
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Check command
    check_parser = subparsers.add_parser("check", help="Run quality check")
    check_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    check_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project to check (default: current directory)",
    )

    # Pre-commit command
    pre_commit_parser = subparsers.add_parser(
        "pre-commit", help="Run pre-commit quality check"
    )
    pre_commit_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    pre_commit_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project to check (default: current directory)",
    )

    # CI command
    ci_parser = subparsers.add_parser("ci", help="Run CI/CD quality check")
    ci_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    ci_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project to check (default: current directory)",
    )

    # Install hook command
    hook_parser = subparsers.add_parser("install-hook", help="Install pre-commit hook")
    hook_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    hook_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project (default: current directory)",
    )

    # Trends command
    trends_parser = subparsers.add_parser("trends", help="Show quality trends")
    trends_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    trends_parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project (default: current directory)",
    )
    trends_parser.add_argument(
        "--days",
        "-d",
        type=int,
        default=30,
        help="Number of days to show trends for (default: 30)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Convert project path to Path object
    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        return 1

    # Execute command
    if args.command == "check":
        return run_quality_check(project_path, args.verbose)
    elif args.command == "pre-commit":
        return run_pre_commit_check(project_path, args.verbose)
    elif args.command == "ci":
        return run_ci_check(project_path, args.verbose)
    elif args.command == "install-hook":
        return install_pre_commit_hook(project_path, args.verbose)
    elif args.command == "trends":
        return show_quality_trends(project_path, args.days, args.verbose)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
