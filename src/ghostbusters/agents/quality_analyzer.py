#!/usr/bin/env python3
"""
Quality Analyzer Agent

This agent specializes in analyzing code quality metrics and identifying quality issues.
"""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class QualityAnalyzer:
    """Agent for analyzing code quality metrics"""

    def __init__(self, config: dict[str, Any] = None):
        """Initialize the quality analyzer agent"""
        self.config = config or {}
        self.analysis_results = {}

        logger.info("🔍 Quality Analyzer Agent initialized")

    def analyze_code_quality(self, target_path: str) -> dict[str, Any]:
        """Analyze code quality for the target path"""
        logger.info(f"🔍 Analyzing code quality for: {target_path}")

        analysis = {
            "target_path": target_path,
            "quality_metrics": {},
            "issues_found": [],
            "recommendations": [],
        }

        try:
            path = Path(target_path)
            if path.is_file():
                analysis["quality_metrics"] = self._analyze_single_file_quality(path)
            elif path.is_dir():
                analysis["quality_metrics"] = self._analyze_directory_quality(path)

            # Generate recommendations based on analysis
            analysis["recommendations"] = self._generate_quality_recommendations(analysis["quality_metrics"])

            logger.info("✅ Code quality analysis complete")

        except Exception as e:
            logger.error(f"❌ Code quality analysis failed: {e}")
            analysis["error"] = str(e)

        return analysis

    def _analyze_single_file_quality(self, file_path: Path) -> dict[str, Any]:
        """Analyze quality metrics for a single file"""
        metrics = {
            "file_size": file_path.stat().st_size,
            "line_count": 0,
            "complexity_score": 0,
            "quality_score": 100.0,
        }

        try:
            content = file_path.read_text()
            lines = content.splitlines()
            metrics["line_count"] = len(lines)

            # Simple complexity calculation
            complexity = 0
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("if ", "for ", "while ", "def ", "class ")):
                    complexity += 1
                if "import " in stripped or "from " in stripped:
                    complexity += 0.5

            metrics["complexity_score"] = complexity

            # Adjust quality score based on complexity
            if complexity > 20:
                metrics["quality_score"] = max(50.0, 100.0 - (complexity - 20) * 2)

        except Exception as e:
            logger.error(f"❌ Failed to analyze file {file_path}: {e}")
            metrics["quality_score"] = 0.0

        return metrics

    def _analyze_directory_quality(self, dir_path: Path) -> dict[str, Any]:
        """Analyze quality metrics for a directory"""
        metrics = {
            "total_files": 0,
            "python_files": 0,
            "average_quality": 0.0,
            "overall_score": 0.0,
        }

        try:
            python_files = list(dir_path.rglob("*.py"))
            metrics["python_files"] = len(python_files)
            metrics["total_files"] = len(list(dir_path.rglob("*")))

            if python_files:
                total_quality = 0
                for py_file in python_files:
                    file_metrics = self._analyze_single_file_quality(py_file)
                    total_quality += file_metrics.get("quality_score", 0)

                metrics["average_quality"] = total_quality / len(python_files)
                metrics["overall_score"] = metrics["average_quality"]

        except Exception as e:
            logger.error(f"❌ Failed to analyze directory {dir_path}: {e}")
            metrics["overall_score"] = 0.0

        return metrics

    def _generate_quality_recommendations(self, metrics: dict[str, Any]) -> list[str]:
        """Generate quality improvement recommendations"""
        recommendations = []

        if metrics.get("complexity_score", 0) > 20:
            recommendations.append("🔧 Consider breaking down complex functions into smaller ones")

        if metrics.get("average_quality", 100) < 80:
            recommendations.append("📚 Review code quality standards and implement improvements")

        if metrics.get("python_files", 0) > 100:
            recommendations.append("🏗️ Consider modularizing the codebase for better maintainability")

        if not recommendations:
            recommendations.append("🎉 Code quality looks good! Keep up the excellent work!")

        return recommendations
