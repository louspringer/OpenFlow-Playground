"""
RM-DDD Codebase Analyzer

Main analyzer that orchestrates all analysis components.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..core.base import DomainReflectiveModule
from ..core.types import ModuleHealth, ModuleStatus, ValidationResult
from .ddd_detector import DDDDetector, DDDPattern
from .rm_compliance import RMComplianceAnalyzer, ComplianceReport
from .bounded_context import BoundedContextAnalyzer, ContextAnalysis
from .ubiquitous_language import UbiquitousLanguageAnalyzer, LanguageAnalysis
from .complexity import ComplexityAnalyzer, ComplexityReport


@dataclass
class AnalysisResult:
    """Comprehensive analysis result"""

    timestamp: datetime = field(default_factory=datetime.now)
    codebase_path: str = ""
    total_files: int = 0
    analyzed_files: int = 0
    ddd_patterns: List[DDDPattern] = field(default_factory=list)
    rm_compliance: ComplianceReport = field(default_factory=ComplianceReport)
    bounded_contexts: List[ContextAnalysis] = field(default_factory=list)
    language_analysis: LanguageAnalysis = field(default_factory=LanguageAnalysis)
    complexity_analysis: ComplexityReport = field(default_factory=ComplexityReport)
    recommendations: List[str] = field(default_factory=list)
    overall_score: float = 0.0

    def add_recommendation(self, recommendation: str):
        """Add analysis recommendation"""
        self.recommendations.append(recommendation)

    def calculate_overall_score(self) -> float:
        """Calculate overall DDD/RM maturity score"""
        scores = []

        # DDD pattern score (0-100)
        ddd_score = min(100, len(self.ddd_patterns) * 10)
        scores.append(ddd_score)

        # RM compliance score
        if self.rm_compliance:
            scores.append(self.rm_compliance.compliance_percentage)

        # Language consistency score
        if self.language_analysis:
            scores.append(self.language_analysis.consistency_score * 100)

        # Complexity score (inverted - lower complexity = higher score)
        if self.complexity_analysis:
            complexity_score = max(0, 100 - self.complexity_analysis.overall_complexity * 10)
            scores.append(complexity_score)

        self.overall_score = sum(scores) / len(scores) if scores else 0.0
        return self.overall_score


class CodebaseAnalyzer(DomainReflectiveModule):
    """Main codebase analyzer with RM compliance"""

    def __init__(self, domain_context: str = "analysis"):
        super().__init__(domain_context, "codebase_analyzer")
        self.ddd_detector = DDDDetector()
        self.rm_analyzer = RMComplianceAnalyzer()
        self.context_analyzer = BoundedContextAnalyzer()
        self.language_analyzer = UbiquitousLanguageAnalyzer()
        self.complexity_analyzer = ComplexityAnalyzer()
        self._analysis_cache: Dict[str, AnalysisResult] = {}

    async def analyze_codebase(self, codebase_path: str, include_patterns: Optional[List[str]] = None, exclude_patterns: Optional[List[str]] = None) -> AnalysisResult:
        """Analyze entire codebase for DDD patterns and RM compliance"""

        # Check cache first
        cache_key = f"{codebase_path}:{hash(str(include_patterns))}:{hash(str(exclude_patterns))}"
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key]

        result = AnalysisResult(codebase_path=codebase_path)

        try:
            # Find all Python files
            python_files = self._find_python_files(codebase_path, include_patterns, exclude_patterns)
            result.total_files = len(python_files)

            # Analyze each file
            for file_path in python_files:
                try:
                    await self._analyze_file(file_path, result)
                    result.analyzed_files += 1
                except Exception as e:
                    result.add_recommendation(f"Error analyzing {file_path}: {str(e)}")

            # Run comprehensive analysis
            await self._run_comprehensive_analysis(result)

            # Calculate overall score
            result.calculate_overall_score()

            # Cache result
            self._analysis_cache[cache_key] = result

        except Exception as e:
            result.add_recommendation(f"Analysis failed: {str(e)}")

        return result

    def _find_python_files(self, codebase_path: str, include_patterns: Optional[List[str]] = None, exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """Find all Python files in codebase"""
        python_files = []
        path = Path(codebase_path)

        if not path.exists():
            return python_files

        # Default exclude patterns
        default_excludes = {"__pycache__", ".git", ".venv", "venv", "node_modules", ".pytest_cache", ".mypy_cache", "build", "dist"}

        exclude_patterns = exclude_patterns or []
        exclude_patterns.extend(default_excludes)

        for file_path in path.rglob("*.py"):
            # Check if file should be excluded
            if any(exclude in str(file_path) for exclude in exclude_patterns):
                continue

            # Check include patterns if specified
            if include_patterns:
                if not any(include in str(file_path) for include in include_patterns):
                    continue

            python_files.append(str(file_path))

        return python_files

    async def _analyze_file(self, file_path: str, result: AnalysisResult):
        """Analyze individual file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Detect DDD patterns
            ddd_patterns = self.ddd_detector.detect_patterns(tree, file_path)
            result.ddd_patterns.extend(ddd_patterns)

            # Check RM compliance
            rm_compliance = self.rm_analyzer.analyze_file(tree, file_path)
            if rm_compliance:
                result.rm_compliance.merge(rm_compliance)

            # Analyze bounded contexts
            context_analysis = self.context_analyzer.analyze_file(tree, file_path)
            if context_analysis:
                result.bounded_contexts.append(context_analysis)

            # Analyze ubiquitous language
            language_analysis = self.language_analyzer.analyze_file(tree, file_path)
            if language_analysis:
                result.language_analysis.merge(language_analysis)

            # Analyze complexity
            complexity_analysis = self.complexity_analyzer.analyze_file(tree, file_path)
            if complexity_analysis:
                result.complexity_analysis.merge(complexity_analysis)

        except SyntaxError as e:
            result.add_recommendation(f"Syntax error in {file_path}: {str(e)}")
        except Exception as e:
            result.add_recommendation(f"Error parsing {file_path}: {str(e)}")

    async def _run_comprehensive_analysis(self, result: AnalysisResult):
        """Run comprehensive analysis across all files"""

        # Analyze DDD pattern relationships
        self._analyze_pattern_relationships(result)

        # Analyze bounded context boundaries
        self._analyze_context_boundaries(result)

        # Generate recommendations
        self._generate_recommendations(result)

    def _analyze_pattern_relationships(self, result: AnalysisResult):
        """Analyze relationships between DDD patterns"""
        entities = [p for p in result.ddd_patterns if p.pattern_type == "entity"]
        aggregates = [p for p in result.ddd_patterns if p.pattern_type == "aggregate"]
        repositories = [p for p in result.ddd_patterns if p.pattern_type == "repository"]

        # Check for orphaned entities (entities not in aggregates)
        orphaned_entities = []
        for entity in entities:
            if not any(entity.class_name in agg.details.get("entities", []) for agg in aggregates):
                orphaned_entities.append(entity.class_name)

        if orphaned_entities:
            result.add_recommendation(f"Found orphaned entities not in aggregates: {', '.join(orphaned_entities)}")

        # Check for aggregates without repositories
        aggregates_without_repos = []
        for aggregate in aggregates:
            if not any(agg.class_name in repo.details.get("aggregate", "") for repo in repositories):
                aggregates_without_repos.append(aggregate.class_name)

        if aggregates_without_repos:
            result.add_recommendation(f"Found aggregates without repositories: {', '.join(aggregates_without_repos)}")

    def _analyze_context_boundaries(self, result: AnalysisResult):
        """Analyze bounded context boundaries"""
        if len(result.bounded_contexts) < 2:
            return

        # Check for context leakage
        context_names = [ctx.context_name for ctx in result.bounded_contexts]

        for ctx in result.bounded_contexts:
            # Check for cross-context dependencies
            for dependency in ctx.dependencies:
                if dependency not in context_names:
                    result.add_recommendation(f"Context '{ctx.context_name}' depends on undefined context '{dependency}'")

    def _generate_recommendations(self, result: AnalysisResult):
        """Generate actionable recommendations"""

        # DDD pattern recommendations
        if not result.ddd_patterns:
            result.add_recommendation("No DDD patterns detected. Consider implementing domain entities and aggregates.")

        # RM compliance recommendations
        if result.rm_compliance.compliance_percentage < 50:
            result.add_recommendation("Low RM compliance. Implement ReflectiveModule base classes for better monitoring.")

        # Language consistency recommendations
        if result.language_analysis.consistency_score < 0.7:
            result.add_recommendation("Low ubiquitous language consistency. Review and standardize domain terminology.")

        # Complexity recommendations
        if result.complexity_analysis.overall_complexity > 0.8:
            result.add_recommendation("High complexity detected. Consider breaking down large classes and methods.")

    async def get_module_status(self) -> ModuleHealth:
        """Get analyzer health status"""
        is_healthy = await self.is_healthy()
        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if is_healthy else ModuleStatus.DEGRADED,
            message=f"Codebase analyzer for {self.domain_context}",
            capabilities=await self.get_module_capabilities(),
            indicators=await self.get_health_indicators(),
        )

    async def is_healthy(self) -> bool:
        """Check if analyzer is healthy"""
        return len(self._analysis_cache) < 1000  # Prevent memory issues

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get analyzer health indicators"""
        return {
            "cached_analyses": len(self._analysis_cache),
            "domain_context": self.domain_context,
            "analyzer_type": "codebase_analyzer",
            "memory_usage": len(self._analysis_cache) * 0.1,  # Rough estimate
        }

    def get_domain_boundaries(self):
        """Get domain boundaries for analyzer"""
        from ..core.types import DomainBoundaries

        return DomainBoundaries(context=self.domain_context, bounded_context_rules=["Codebase analysis and DDD pattern detection", "RM compliance validation and reporting"])

    def validate_domain_invariants(self) -> ValidationResult:
        """Validate analyzer invariants"""
        result = ValidationResult(is_valid=True)

        if not self.ddd_detector:
            result.add_error("DDD detector not initialized")

        if not self.rm_analyzer:
            result.add_error("RM analyzer not initialized")

        return result
