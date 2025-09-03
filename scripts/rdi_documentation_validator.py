#!/usr/bin/env python3
"""
RDI Documentation Validator - RM Compliant
Validates documentation completeness and traceability in RDI methodology
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DocumentationRequirement:
    """Documentation requirement."""

    requirement_id: str
    title: str
    description: str
    documentation_type: str  # 'api', 'user_guide', 'technical_spec', 'troubleshooting'
    traceability: List[str]  # Links to requirements, design, implementation
    status: str  # 'complete', 'partial', 'missing'
    validation_criteria: List[str]


@dataclass
class DocumentationValidation:
    """Documentation validation result."""

    file_path: str
    requirement_id: str
    validation_type: str
    status: str
    issues: List[str]
    recommendations: List[str]
    traceability_score: float


class RDIDocumentationValidator:
    """RDI Documentation Validator - RM Compliant."""

    def __init__(self, project_root: str = "."):
        """Initialize the documentation validator."""
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.requirements_dir = self.project_root / "requirements"
        self.design_dir = self.project_root / "design"
        self.src_dir = self.project_root / "src"

        self.documentation_requirements: List[DocumentationRequirement] = []
        self.validation_results: List[DocumentationValidation] = []

        logger.info("RDI Documentation Validator initialized")

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status for RM compliance."""
        return {
            "service_name": "RDI Documentation Validator",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "capabilities": ["documentation_completeness_validation", "traceability_validation", "documentation_quality_assessment", "rdi_cycle_validation"],
            "metrics": {"total_requirements": len(self.documentation_requirements), "validation_results": len(self.validation_results), "completion_rate": self._calculate_completion_rate()},
        }

    def _calculate_completion_rate(self) -> float:
        """Calculate documentation completion rate."""
        if not self.validation_results:
            return 0.0

        complete_count = len([v for v in self.validation_results if v.status == "complete"])
        return (complete_count / len(self.validation_results)) * 100

    def validate_documentation_completeness(self) -> List[DocumentationValidation]:
        """Validate documentation completeness against requirements."""
        logger.info("Validating documentation completeness...")

        # Load requirements
        requirements = self._load_requirements()

        # Load design specifications
        design_specs = self._load_design_specifications()

        # Load implementation files
        implementation_files = self._load_implementation_files()

        # Generate documentation requirements
        self._generate_documentation_requirements(requirements, design_specs, implementation_files)

        # Validate each documentation requirement
        for req in self.documentation_requirements:
            validation = self._validate_documentation_requirement(req)
            self.validation_results.append(validation)

        logger.info(f"Documentation validation complete: {len(self.validation_results)} validations")
        return self.validation_results

    def _load_requirements(self) -> List[Dict[str, Any]]:
        """Load requirements from requirements directory."""
        requirements = []

        if self.requirements_dir.exists():
            for req_file in self.requirements_dir.glob("*.md"):
                try:
                    with open(req_file, "r") as f:
                        content = f.read()
                        # Parse requirements (simplified)
                        if "REQ-" in content:
                            requirements.append({"file": str(req_file), "content": content, "type": "requirement"})
                except Exception as e:
                    logger.debug(f"Error reading {req_file}: {e}")

        return requirements

    def _load_design_specifications(self) -> List[Dict[str, Any]]:
        """Load design specifications from design directory."""
        design_specs = []

        if self.design_dir.exists():
            for design_file in self.design_dir.glob("*.md"):
                try:
                    with open(design_file, "r") as f:
                        content = f.read()
                        design_specs.append({"file": str(design_file), "content": content, "type": "design"})
                except Exception as e:
                    logger.debug(f"Error reading {design_file}: {e}")

        return design_specs

    def _load_implementation_files(self) -> List[Dict[str, Any]]:
        """Load implementation files from src directory."""
        implementation_files = []

        if self.src_dir.exists():
            for impl_file in self.src_dir.rglob("*.py"):
                try:
                    with open(impl_file, "r") as f:
                        content = f.read()
                        implementation_files.append({"file": str(impl_file), "content": content, "type": "implementation"})
                except Exception as e:
                    logger.debug(f"Error reading {impl_file}: {e}")

        return implementation_files

    def _generate_documentation_requirements(self, requirements: List[Dict[str, Any]], design_specs: List[Dict[str, Any]], implementation_files: List[Dict[str, Any]]):
        """Generate documentation requirements from RDI artifacts."""

        # Generate requirements from requirements files
        for req in requirements:
            doc_req = DocumentationRequirement(
                requirement_id=f"DOC-REQ-{len(self.documentation_requirements) + 1}",
                title=f"Documentation for {Path(req['file']).stem}",
                description=f"Documentation for requirement: {Path(req['file']).stem}",
                documentation_type="requirement_doc",
                traceability=[req["file"]],
                status="missing",
                validation_criteria=["Documentation exists for requirement", "Documentation is up-to-date", "Documentation is comprehensive"],
            )
            self.documentation_requirements.append(doc_req)

        # Generate requirements from design specifications
        for design in design_specs:
            doc_req = DocumentationRequirement(
                requirement_id=f"DOC-DESIGN-{len(self.documentation_requirements) + 1}",
                title=f"Documentation for {Path(design['file']).stem}",
                description=f"Documentation for design: {Path(design['file']).stem}",
                documentation_type="design_doc",
                traceability=[design["file"]],
                status="missing",
                validation_criteria=["Design documentation exists", "Design documentation is clear", "Design documentation includes diagrams"],
            )
            self.documentation_requirements.append(doc_req)

        # Generate requirements from implementation files
        for impl in implementation_files:
            doc_req = DocumentationRequirement(
                requirement_id=f"DOC-IMPL-{len(self.documentation_requirements) + 1}",
                title=f"Documentation for {Path(impl['file']).stem}",
                description=f"Documentation for implementation: {Path(impl['file']).stem}",
                documentation_type="api_doc",
                traceability=[impl["file"]],
                status="missing",
                validation_criteria=["API documentation exists", "Code is well-documented", "Usage examples are provided"],
            )
            self.documentation_requirements.append(doc_req)

    def _validate_documentation_requirement(self, req: DocumentationRequirement) -> DocumentationValidation:
        """Validate a single documentation requirement."""
        issues = []
        recommendations = []

        # Check if documentation exists
        doc_exists = self._check_documentation_exists(req)
        if not doc_exists:
            issues.append(f"Documentation missing for {req.title}")
            recommendations.append(f"Create documentation for {req.title}")

        # Check documentation quality
        if doc_exists:
            quality_issues = self._check_documentation_quality(req)
            issues.extend(quality_issues)

            if quality_issues:
                recommendations.append("Improve documentation quality")

        # Check traceability
        traceability_score = self._check_traceability(req)
        if traceability_score < 0.8:
            issues.append("Poor traceability to RDI artifacts")
            recommendations.append("Improve traceability links")

        # Determine status
        if not issues:
            status = "complete"
        elif len(issues) <= 2:
            status = "partial"
        else:
            status = "missing"

        return DocumentationValidation(
            file_path=req.traceability[0] if req.traceability else "",
            requirement_id=req.requirement_id,
            validation_type=req.documentation_type,
            status=status,
            issues=issues,
            recommendations=recommendations,
            traceability_score=traceability_score,
        )

    def _check_documentation_exists(self, req: DocumentationRequirement) -> bool:
        """Check if documentation exists for requirement."""
        # Simple check - look for corresponding documentation file
        doc_patterns = [f"docs/{Path(req.traceability[0]).stem}.md", f"docs/{Path(req.traceability[0]).stem}_doc.md", f"docs/{req.documentation_type}/{Path(req.traceability[0]).stem}.md"]

        for pattern in doc_patterns:
            if Path(pattern).exists():
                return True

        return False

    def _check_documentation_quality(self, req: DocumentationRequirement) -> List[str]:
        """Check documentation quality."""
        issues = []

        # Find documentation file
        doc_file = None
        doc_patterns = [f"docs/{Path(req.traceability[0]).stem}.md", f"docs/{Path(req.traceability[0]).stem}_doc.md", f"docs/{req.documentation_type}/{Path(req.traceability[0]).stem}.md"]

        for pattern in doc_patterns:
            if Path(pattern).exists():
                doc_file = Path(pattern)
                break

        if doc_file:
            try:
                with open(doc_file, "r") as f:
                    content = f.read()

                    # Check for basic quality indicators
                    if len(content) < 100:
                        issues.append("Documentation too short")

                    if "TODO" in content or "FIXME" in content:
                        issues.append("Documentation contains TODO/FIXME")

                    if not any(keyword in content.lower() for keyword in ["overview", "description", "usage", "example"]):
                        issues.append("Documentation missing key sections")

            except Exception as e:
                issues.append(f"Error reading documentation: {e}")

        return issues

    def _check_traceability(self, req: DocumentationRequirement) -> float:
        """Check traceability score."""
        score = 0.0

        # Check if documentation references the source file
        if req.traceability:
            score += 0.5

            # Check if documentation has proper links
            doc_file = None
            doc_patterns = [f"docs/{Path(req.traceability[0]).stem}.md", f"docs/{Path(req.traceability[0]).stem}_doc.md", f"docs/{req.documentation_type}/{Path(req.traceability[0]).stem}.md"]

            for pattern in doc_patterns:
                if Path(pattern).exists():
                    doc_file = Path(pattern)
                    break

            if doc_file:
                try:
                    with open(doc_file, "r") as f:
                        content = f.read()
                        if req.traceability[0] in content:
                            score += 0.3
                        if "requirements" in content.lower() or "design" in content.lower():
                            score += 0.2
                except Exception:
                    pass

        return min(score, 1.0)

    def generate_documentation_report(self) -> Dict[str, Any]:
        """Generate documentation validation report."""
        total_requirements = len(self.documentation_requirements)
        complete_docs = len([v for v in self.validation_results if v.status == "complete"])
        partial_docs = len([v for v in self.validation_results if v.status == "partial"])
        missing_docs = len([v for v in self.validation_results if v.status == "missing"])

        avg_traceability = sum(v.traceability_score for v in self.validation_results) / len(self.validation_results) if self.validation_results else 0.0

        report = {
            "validation_info": {"generated_at": datetime.now().isoformat(), "project_root": str(self.project_root), "total_requirements": total_requirements, "report_version": "1.0"},
            "summary": {
                "total_requirements": total_requirements,
                "complete_documentation": complete_docs,
                "partial_documentation": partial_docs,
                "missing_documentation": missing_docs,
                "completion_rate": (complete_docs / total_requirements * 100) if total_requirements > 0 else 0.0,
                "average_traceability_score": avg_traceability,
            },
            "requirements": [asdict(req) for req in self.documentation_requirements],
            "validation_results": [asdict(v) for v in self.validation_results],
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate documentation recommendations."""
        recommendations = []

        missing_count = len([v for v in self.validation_results if v.status == "missing"])
        if missing_count > 0:
            recommendations.append(f"Create documentation for {missing_count} missing requirements")

        partial_count = len([v for v in self.validation_results if v.status == "partial"])
        if partial_count > 0:
            recommendations.append(f"Improve documentation for {partial_count} partial requirements")

        low_traceability = [v for v in self.validation_results if v.traceability_score < 0.5]
        if low_traceability:
            recommendations.append(f"Improve traceability for {len(low_traceability)} requirements")

        recommendations.append("Ensure all documentation follows RDI methodology")
        recommendations.append("Maintain documentation traceability to requirements, design, and implementation")

        return recommendations


def main():
    """Main function for testing."""
    # Create validator
    validator = RDIDocumentationValidator()

    # Validate documentation
    results = validator.validate_documentation_completeness()

    # Generate report
    report = validator.generate_documentation_report()

    # Display results
    print("📚 RDI Documentation Validation - RM Compliant")
    print("=" * 60)
    print(f"Total Requirements: {report['summary']['total_requirements']}")
    print(f"Complete Documentation: {report['summary']['complete_documentation']}")
    print(f"Partial Documentation: {report['summary']['partial_documentation']}")
    print(f"Missing Documentation: {report['summary']['missing_documentation']}")
    print(f"Completion Rate: {report['summary']['completion_rate']:.1f}%")
    print(f"Average Traceability Score: {report['summary']['average_traceability_score']:.2f}")

    # Show recommendations
    if report["recommendations"]:
        print("\n💡 Recommendations:")
        for recommendation in report["recommendations"]:
            print(f"  • {recommendation}")

    # Save report
    with open("rdi_documentation_validation_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Documentation validation report saved to: rdi_documentation_validation_report.json")


if __name__ == "__main__":
    main()
