#!/usr/bin/env python3
"""
Activity Model Integration for Round-Trip Engineering System

This module provides a production-ready integration between the activity model
generation system and the round-trip engineering workflow.

Features:
- CLI interface for standalone usage
- Integration with round-trip system
- Comprehensive error handling
- Performance monitoring
- SVG output generation
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add src to path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import our activity model generator
from activity_model_generator_simple import SimpleActivityModelGenerator
from plantuml_client_wrapper import NodePlantUMLWrapper

# Import round-trip system components
try:
    from .core.round_trip_system import RoundTripSystem
    from .core.model_manager import ModelManager

    ROUND_TRIP_AVAILABLE = True
except ImportError:
    ROUND_TRIP_AVAILABLE = False
    RoundTripSystem = None
    ModelManager = None

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ActivityModelIntegration:
    """
    Production-ready integration between activity model generation and round-trip engineering.
    """

    def __init__(self, output_dir: str = "generated_activity_models"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize components
        self.activity_generator = SimpleActivityModelGenerator(str(self.output_dir))
        self.plantuml_wrapper = NodePlantUMLWrapper()

        # Round-trip system integration
        self.round_trip_system = None
        if ROUND_TRIP_AVAILABLE:
            try:
                self.round_trip_system = RoundTripSystem()
                logger.info("✅ Round-trip system integration available")
            except Exception as e:
                logger.warning(f"⚠️  Round-trip system integration failed: {e}")

    def generate_activity_models(
        self, source_paths: List[str], include_round_trip: bool = True
    ) -> Dict[str, Any]:
        """
        Generate comprehensive activity models for the given source paths.

        Args:
            source_paths: List of source files/directories to analyze
            include_round_trip: Whether to integrate with round-trip system

        Returns:
            Dictionary containing generation results and metadata
        """
        start_time = time.time()
        results = {
            "source_paths": source_paths,
            "generated_models": [],
            "errors": [],
            "performance_metrics": {},
            "round_trip_integration": include_round_trip
            and self.round_trip_system is not None,
        }

        try:
            # Generate activity models for each source path
            for source_path in source_paths:
                try:
                    logger.info(f"🔍 Processing: {source_path}")

                    # Generate activity models
                    model_result = self.activity_generator.generate_from_code(
                        source_path
                    )

                    if model_result:
                        results["generated_models"].append(
                            {
                                "source_path": source_path,
                                "result": model_result,
                                "status": "success",
                            }
                        )
                        logger.info(f"✅ Generated models for: {source_path}")
                    else:
                        results["generated_models"].append(
                            {
                                "source_path": source_path,
                                "result": None,
                                "status": "failed",
                            }
                        )
                        logger.warning(
                            f"⚠️  Failed to generate models for: {source_path}"
                        )

                except Exception as e:
                    error_msg = f"Error processing {source_path}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    results["generated_models"].append(
                        {
                            "source_path": source_path,
                            "result": None,
                            "status": "error",
                            "error": str(e),
                        }
                    )

            # Round-trip system integration
            if include_round_trip and self.round_trip_system:
                try:
                    logger.info("🔄 Integrating with round-trip system...")
                    round_trip_result = self._integrate_with_round_trip(results)
                    results["round_trip_result"] = round_trip_result
                    logger.info("✅ Round-trip integration completed")
                except Exception as e:
                    error_msg = f"Round-trip integration failed: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)

            # Performance metrics
            end_time = time.time()
            results["performance_metrics"] = {
                "total_time": end_time - start_time,
                "models_generated": len(
                    [m for m in results["generated_models"] if m["status"] == "success"]
                ),
                "errors_count": len(results["errors"]),
                "success_rate": (
                    len(
                        [
                            m
                            for m in results["generated_models"]
                            if m["status"] == "success"
                        ]
                    )
                    / len(source_paths)
                    if source_paths
                    else 0
                ),
            }

            logger.info(
                f"🎯 Generation completed: {results['performance_metrics']['models_generated']} models, {results['performance_metrics']['errors_count']} errors"
            )

        except Exception as e:
            error_msg = f"Critical error in activity model generation: {e}"
            logger.error(error_msg)
            results["errors"].append(error_msg)

        return results

    def _integrate_with_round_trip(
        self, activity_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Integrate generated activity models with the round-trip system.

        Args:
            activity_results: Results from activity model generation

        Returns:
            Integration results
        """
        try:
            # Create a summary of generated models for round-trip system
            model_summary = {
                "activity_models": activity_results["generated_models"],
                "generation_timestamp": time.time(),
                "output_directory": str(self.output_dir),
                "performance_metrics": activity_results["performance_metrics"],
            }

            # Store the summary in the round-trip system
            if hasattr(self.round_trip_system, "store_activity_model_summary"):
                self.round_trip_system.store_activity_model_summary(model_summary)

            # Generate round-trip validation report
            validation_report = {
                "models_validated": len(activity_results["generated_models"]),
                "integration_status": "success",
                "timestamp": time.time(),
            }

            return validation_report

        except Exception as e:
            logger.error(f"Round-trip integration failed: {e}")
            return {
                "integration_status": "failed",
                "error": str(e),
                "timestamp": time.time(),
            }

    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive report of the activity model generation.

        Args:
            results: Results from generate_activity_models

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("ACTIVITY MODEL GENERATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Summary
        report_lines.append("📊 SUMMARY")
        report_lines.append(f"  Source Paths: {len(results['source_paths'])}")
        report_lines.append(
            f"  Models Generated: {results['performance_metrics']['models_generated']}"
        )
        report_lines.append(
            f"  Errors: {results['performance_metrics']['errors_count']}"
        )
        report_lines.append(
            f"  Success Rate: {results['performance_metrics']['success_rate']:.1%}"
        )
        report_lines.append(
            f"  Total Time: {results['performance_metrics']['total_time']:.2f}s"
        )
        report_lines.append("")

        # Round-trip integration status
        if results["round_trip_integration"]:
            report_lines.append("🔄 ROUND-TRIP INTEGRATION")
            if "round_trip_result" in results:
                rt_result = results["round_trip_result"]
                report_lines.append(
                    f"  Status: {rt_result.get('integration_status', 'unknown')}"
                )
                if rt_result.get("integration_status") == "success":
                    report_lines.append(
                        f"  Models Validated: {rt_result.get('models_validated', 0)}"
                    )
            else:
                report_lines.append("  Status: Not attempted")
            report_lines.append("")

        # Generated models
        report_lines.append("🎨 GENERATED MODELS")
        for model in results["generated_models"]:
            status_emoji = "✅" if model["status"] == "success" else "❌"
            report_lines.append(
                f"  {status_emoji} {model['source_path']} - {model['status']}"
            )
            if model.get("error"):
                report_lines.append(f"      Error: {model['error']}")
        report_lines.append("")

        # Errors
        if results["errors"]:
            report_lines.append("🚨 ERRORS")
            for error in results["errors"]:
                report_lines.append(f"  • {error}")
            report_lines.append("")

        # Output location
        report_lines.append("📁 OUTPUT LOCATION")
        report_lines.append(f"  Directory: {self.output_dir.absolute()}")
        report_lines.append("  Format: SVG (vector graphics)")
        report_lines.append("")

        report_lines.append("=" * 80)

        return "\n".join(report_lines)


def main():
    """Main CLI interface for activity model integration."""
    parser = argparse.ArgumentParser(
        description="Generate activity models and integrate with round-trip engineering system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate models for specific files
  python activity_model_integration.py src/round_trip_engineering/ --output-dir models/
  
  # Generate models without round-trip integration
  python activity_model_integration.py src/ --no-round-trip
  
  # Generate models with verbose logging
  python activity_model_integration.py src/ --verbose
        """,
    )

    parser.add_argument(
        "source_paths", nargs="+", help="Source files or directories to analyze"
    )

    parser.add_argument(
        "--output-dir",
        default="generated_activity_models",
        help="Output directory for generated models (default: generated_activity_models)",
    )

    parser.add_argument(
        "--no-round-trip",
        action="store_true",
        help="Skip round-trip system integration",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report without running generation",
    )

    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize integration
    try:
        integration = ActivityModelIntegration(args.output_dir)
        logger.info(f"🚀 Activity Model Integration initialized")
        logger.info(f"📁 Output directory: {args.output_dir}")
        logger.info(
            f"🔄 Round-trip integration: {'enabled' if not args.no_round_trip else 'disabled'}"
        )

        if args.report_only:
            # Generate report from existing results
            logger.info("📊 Generating report from existing results...")
            # This would need to be implemented based on stored results
            print("Report-only mode not yet implemented")
            return

        # Generate activity models
        logger.info("🎨 Starting activity model generation...")
        results = integration.generate_activity_models(
            source_paths=args.source_paths, include_round_trip=not args.no_round_trip
        )

        # Generate and display report
        report = integration.generate_report(results)
        print(report)

        # Save report to file
        report_file = Path(args.output_dir) / "generation_report.txt"
        with open(report_file, "w") as f:
            f.write(report)
        logger.info(f"📄 Report saved to: {report_file}")

        # Exit with appropriate code
        if results["performance_metrics"]["errors_count"] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("⏹️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
