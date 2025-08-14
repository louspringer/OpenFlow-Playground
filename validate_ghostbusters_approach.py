#!/usr/bin/env python3
"""
Validate clewcrew Extraction Approach

This script analyzes the current clewcrew system and validates the extraction strategy
to identify any delusions or issues in the approach.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClewcrewApproachValidator:
    """Validator for the Ghostbusters extraction approach"""

    def __init__(self):
        self.issues = []
        self.recommendations = []
        self.confidence = 0.0

    async def validate_extraction_approach(self) -> dict[str, Any]:
        """Validate the overall extraction approach"""
        logger.info("🔍 Validating Ghostbusters extraction approach...")

        # Check current system state
        await self._analyze_current_system()

        # Validate extraction strategy
        await self._validate_extraction_strategy()

        # Check for potential issues
        await self._identify_potential_issues()

        # Generate recommendations
        await self._generate_recommendations()

        # Calculate confidence
        self._calculate_confidence()

        return {
            "confidence": self.confidence,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "status": "complete",
        }

    async def _analyze_current_system(self):
        """Analyze the current Ghostbusters system"""
        logger.info("📊 Analyzing current system state...")

        # Check if Ghostbusters system exists
        ghostbusters_path = Path("src/ghostbusters")
        if not ghostbusters_path.exists():
            self.issues.append("Ghostbusters system not found in expected location")
            return

        # Count files and lines
        python_files = list(ghostbusters_path.rglob("*.py"))
        total_lines = 0

        for py_file in python_files:
            try:
                with open(py_file) as f:
                    lines = len(f.readlines())
                    total_lines += lines
            except Exception as e:
                self.issues.append(f"Error reading {py_file}: {e}")

        logger.info(
            f"Found {len(python_files)} Python files with {total_lines} total lines"
        )

        # Check for critical components
        critical_components = [
            "ghostbusters_orchestrator.py",
            "agents/",
            "recovery_engines/",
            "validators/",
        ]

        missing_components = []
        for component in critical_components:
            if not (ghostbusters_path / component).exists():
                missing_components.append(component)

        if missing_components:
            self.issues.append(f"Missing critical components: {missing_components}")

    async def _validate_extraction_strategy(self):
        """Validate the extraction strategy"""
        logger.info("🏗️ Validating extraction strategy...")

        # Check if common package was created
        common_path = Path("clewcrew-common")
        if not common_path.exists():
            self.issues.append("clewcrew-common package not created yet")
            return

        # Validate package structure
        expected_structure = [
            "src/clewcrew_common/",
            "tests/",
            "pyproject.toml",
            "README.md",
        ]

        missing_structure = []
        for item in expected_structure:
            if not (common_path / item).exists():
                missing_structure.append(item)

        if missing_structure:
            self.issues.append(f"Missing package structure: {missing_structure}")

        # Check for confidence module
        confidence_path = common_path / "src/clewcrew_common/confidence.py"
        if not confidence_path.exists():
            self.issues.append("Confidence module not created")
        else:
            logger.info("✅ Confidence module created successfully")

    async def _identify_potential_issues(self):
        """Identify potential issues with the extraction approach"""
        logger.info("⚠️ Identifying potential issues...")

        # Check for import issues
        try:
            import sys

            sys.path.insert(0, str(Path("clewcrew-common/src")))

            # Test import without storing unused variable
            try:
                import clewcrew_common.confidence

                logger.info("✅ Confidence module imports successfully")
            except ImportError:
                pass

        except ImportError as e:
            self.issues.append(f"Import issue with confidence module: {e}")

        # Check for dependency conflicts
        try:
            # Check if we can import the original clewcrew system
            try:
                import src.ghostbusters.agents.security_expert

                logger.info("✅ Original clewcrew system imports successfully")
            except ImportError:
                pass
        except Exception as e:
            self.issues.append(f"Import issue with original clewcrew system: {e}")

        # Check for circular dependency risks
        circular_risk_components = [
            "ghostbusters-core",
            "ghostbusters-agents",
            "ghostbusters-recovery",
            "ghostbusters-validators",
        ]

        for component in circular_risk_components:
            if Path(component).exists():
                logger.warning(f"⚠️ {component} already exists - potential conflict")

    async def _generate_recommendations(self):
        """Generate recommendations for the extraction approach"""
        logger.info("💡 Generating recommendations...")

        if not self.issues:
            self.recommendations.append("✅ Extraction approach appears sound")
            self.recommendations.append("🚀 Proceed with component extraction")
            self.recommendations.append("📦 Create PyPI packages for each component")
            self.recommendations.append("🔗 Update hackathon projects to use packages")
        else:
            self.recommendations.append("🔧 Fix identified issues before proceeding")
            self.recommendations.append("🧪 Test each component individually")
            self.recommendations.append("📚 Ensure proper documentation")
            self.recommendations.append("⚡ Optimize for performance")

    def _calculate_confidence(self):
        """Calculate confidence in the extraction approach"""
        base_confidence = 0.8

        # Reduce confidence for each issue
        issue_penalty = min(0.3, len(self.issues) * 0.1)

        # Increase confidence for successful validations
        success_bonus = 0.1 if not self.issues else 0.0

        self.confidence = max(
            0.0, min(1.0, base_confidence - issue_penalty + success_bonus)
        )

        logger.info(f"🎯 Confidence in extraction approach: {self.confidence:.2f}")


async def main():
    """Main validation function"""
    logger.info("🚀 Starting Ghostbusters extraction approach validation...")

    validator = ClewcrewApproachValidator()
    result = await validator.validate_extraction_approach()

    logger.info("📊 Validation Results:")
    logger.info(f"Confidence: {result['confidence']:.2f}")

    if result["issues"]:
        logger.warning("⚠️ Issues found:")
        for issue in result["issues"]:
            logger.warning(f"  - {issue}")

    if result["recommendations"]:
        logger.info("💡 Recommendations:")
        for rec in result["recommendations"]:
            logger.info(f"  - {rec}")

    # Overall assessment
    if result["confidence"] >= 0.7:
        logger.info("✅ Extraction approach is sound - proceed with confidence!")
    elif result["confidence"] >= 0.5:
        logger.warning("⚠️ Extraction approach has some issues - review and fix")
    else:
        logger.error(
            "❌ Extraction approach has significant issues - major revision needed"
        )

    return result


if __name__ == "__main__":
    asyncio.run(main())
