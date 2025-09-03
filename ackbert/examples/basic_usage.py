#!/usr/bin/env python3
"""
Basic usage example for Ack-Bert framework.

This example demonstrates how to use the Ack-Bert framework
to perform candidate comparison and evaluation.
"""

import json
from pathlib import Path

from ackbert import OntologyManager, ComparisonEngine, EvidenceCollector, DiagramGenerator


def main():
    """Main example function."""
    print("🚀 Ack-Bert Basic Usage Example")
    print("=" * 50)

    # Initialize the ontology manager with the example ontology
    ontology_path = Path("ontology/ackbert-ontology.ttl")

    if not ontology_path.exists():
        print(f"❌ Ontology file not found: {ontology_path}")
        print("Please ensure the ontology file exists in the ontology/ directory")
        return

    try:
        # Load ontology
        print("📚 Loading ontology...")
        ontology = OntologyManager(ontology_path)

        # Validate ontology
        print("🔍 Validating ontology...")
        issues = ontology.validate_ontology()
        if issues:
            print("⚠️  Ontology validation issues found:")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print("✅ Ontology validation passed!")

        # Display candidates
        print("\n👥 Candidates found:")
        candidates = ontology.get_candidates()
        for candidate in candidates:
            print(f"  • {candidate.name}")
            print(f"    Evidence Level: {candidate.evidence_strength.label}")
            print(f"    Strengths: {', '.join(candidate.strengths) if candidate.strengths else 'None'}")
            print(f"    Gaps: {', '.join(candidate.gaps) if candidate.gaps else 'None'}")
            if candidate.comment:
                print(f"    Comment: {candidate.comment}")
            print()

        # Display requirements
        print("📋 Job Requirements:")
        requirements = ontology.get_requirements()
        for req in requirements:
            print(f"  • {req.name}")
            if req.description:
                print(f"    Description: {req.description}")
        print()

        # Generate comparison
        print("🔄 Generating comparison...")
        engine = ComparisonEngine(ontology)

        # Generate comparison matrix
        matrix = engine.generate_comparison_matrix()
        print("📊 Comparison Matrix:")
        print(json.dumps(matrix.to_dict(), indent=2))
        print()

        # Assess risks
        print("⚠️  Risk Assessment:")
        risks = engine.assess_risks()
        for risk in risks:
            print(f"  • {risk.candidate_name}: {risk.level.value.upper()} - {risk.description}")
            if risk.mitigation_strategies:
                print(f"    Mitigation: {', '.join(risk.mitigation_strategies)}")
        print()

        # Generate recommendations
        print("🎯 Recommendations:")
        recommendations = engine.synthesize_recommendations()
        for rec in recommendations:
            print(f"  • {rec.candidate_name}: {rec.action}")
            print(f"    Type: {rec.type.value}")
            print(f"    Reasoning: {rec.reasoning}")
            print(f"    Next Steps: {', '.join(rec.next_steps)}")
            print()

        # Generate comprehensive report
        print("📄 Generating comprehensive report...")
        report = engine.generate_report()

        # Save report to file
        report_path = Path("examples/comparison_report.json")
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved to {report_path}")

        # Generate diagrams
        print("🎨 Generating diagrams...")
        diagram_gen = DiagramGenerator()
        diagrams = diagram_gen.generate_all_diagrams(ontology, engine)

        print("📊 Generated diagrams:")
        for name, path in diagrams.items():
            print(f"  • {name}: {path}")

        print("\n🎉 Example completed successfully!")

    except Exception as e:
        print(f"❌ Error running example: {e}")
        raise


if __name__ == "__main__":
    main()
