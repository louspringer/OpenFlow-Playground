#!/usr/bin/env python3
"""
AST Analysis API - Language-agnostic interface for other domains

RM Compliance: Interface constraints, health monitoring, self-documentation
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from ..core.ast_parser import ASTParser, ASTParseResult, ArtifactInfo

logger = logging.getLogger(__name__)


class ASTAnalysisAPI:
    """RM Compliance: Language-agnostic API with interface constraints"""

    def __init__(self):
        # RM Compliance: Single responsibility - delegate to core parser
        self._parser = ASTParser()
        logger.info("✅ ASTAnalysisAPI initialized with language-agnostic support")

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """RM Compliance: Analyze file and return structured results"""
        try:
            path = Path(file_path)
            parse_result = self._parser.parse_file(path)

            if not parse_result.is_valid():
                return {"success": False, "errors": parse_result.errors, "health_status": self._parser.get_health_status(), "language": parse_result.language}

            # Extract artifacts using the core parser
            with open(path, "r", encoding="utf-8") as f:
                source_code = f.read()

            artifacts = self._parser.extract_artifacts(parse_result.ast_tree, source_code, parse_result.language)

            # RM Compliance: Structured output with validation
            return {
                "success": True,
                "file_path": str(file_path),
                "language": parse_result.language,
                "parse_time": parse_result.parse_time,
                "artifacts": self._format_artifacts(artifacts),
                "health_status": self._parser.get_health_status(),
                "artifact_counts": self._count_artifacts(artifacts),
            }

        except Exception as e:
            logger.error(f"❌ API error analyzing {file_path}: {e}")
            return {"success": False, "errors": [str(e)], "health_status": self._parser.get_health_status(), "language": "unknown"}

    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """RM Compliance: Python-specific analysis"""
        result = self.analyze_file(file_path)
        if result["success"] and result["language"] == "python":
            return result
        else:
            return {"success": False, "errors": ["Not a Python file or parsing failed"], "language": "python"}

    def analyze_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """RM Compliance: Markdown-specific analysis (future)"""
        result = self.analyze_file(file_path)
        if result["success"] and result["language"] == "markdown":
            return result
        else:
            return {"success": False, "errors": ["Not a Markdown file or parsing failed"], "language": "markdown"}

    def analyze_javascript_file(self, file_path: str) -> Dict[str, Any]:
        """RM Compliance: JavaScript-specific analysis (future)"""
        result = self.analyze_file(file_path)
        if result["success"] and result["language"] == "javascript":
            return result
        else:
            return {"success": False, "errors": ["Not a JavaScript file or parsing failed"], "language": "javascript"}

    def get_classes(self, file_path: str) -> List[Dict[str, Any]]:
        """RM Compliance: Get only classes from file"""
        result = self.analyze_file(file_path)
        if not result["success"]:
            return []

        return [artifact for artifact in result["artifacts"] if artifact["type"] == "class"]

    def get_methods(self, file_path: str, class_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """RM Compliance: Get methods, optionally filtered by class"""
        result = self.analyze_file(file_path)
        if not result["success"]:
            return []

        methods = [artifact for artifact in result["artifacts"] if artifact["type"] == "method"]

        if class_name:
            methods = [method for method in methods if method.get("parent_class") == class_name]

        return methods

    def get_functions(self, file_path: str) -> List[Dict[str, Any]]:
        """RM Compliance: Get only standalone functions"""
        result = self.analyze_file(file_path)
        if not result["success"]:
            return []

        return [artifact for artifact in result["artifacts"] if artifact["type"] == "function"]

    def get_supported_languages(self) -> List[str]:
        """RM Compliance: Get list of supported languages"""
        health_status = self._parser.get_health_status()
        return health_status.get("supported_languages", [])

    def can_parse_file(self, file_path: str) -> bool:
        """RM Compliance: Check if file can be parsed"""
        path = Path(file_path)
        return self._parser._get_parser_for_file(path) is not None

    def get_health_status(self) -> Dict[str, Any]:
        """RM Compliance: Health monitoring for other domains"""
        return self._parser.get_health_status()

    def self_correct(self) -> bool:
        """RM Compliance: Self-correction capabilities"""
        return self._parser.self_correct()

    def _format_artifacts(self, artifacts: List[ArtifactInfo]) -> List[Dict[str, Any]]:
        """RM Compliance: Format artifacts for external consumption"""
        formatted = []

        for artifact in artifacts:
            if artifact.validate():
                formatted.append(
                    {
                        "name": artifact.name,
                        "type": artifact.artifact_type,
                        "line_number": artifact.line_number,
                        "end_line": artifact.end_line,
                        "parent_class": artifact.parent_class,
                        "source_code": artifact.source_code,
                        "language": artifact.language,
                        "is_valid": artifact.is_valid,
                    }
                )
            else:
                logger.warning(f"⚠️ Invalid artifact {artifact.name}: {artifact.validation_errors}")

        return formatted

    def _count_artifacts(self, artifacts: List[ArtifactInfo]) -> Dict[str, int]:
        """RM Compliance: Provide artifact statistics"""
        counts = {"class": 0, "method": 0, "function": 0, "total": len(artifacts)}

        for artifact in artifacts:
            if artifact.artifact_type in counts:
                counts[artifact.artifact_type] += 1

        return counts
