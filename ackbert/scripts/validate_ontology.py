#!/usr/bin/env python3
"""
Ontology validation script for Ack-Bert framework.

This script validates RDF/Turtle ontology files for structural
correctness and completeness.
"""

import sys
from pathlib import Path
from typing import List

from ackbert.ontology import OntologyManager


def validate_ontology_file(ontology_path: Path) -> List[str]:
    """Validate a single ontology file."""
    issues = []

    try:
        ontology = OntologyManager(ontology_path)
        issues.extend(ontology.validate_ontology())

        # Additional custom validations
        candidates = ontology.get_candidates()
        requirements = ontology.get_requirements()

        if not candidates:
            issues.append("No candidates found in ontology")

        if not requirements:
            issues.append("No job requirements found in ontology")

        # Check for candidates without evidence strength
        for candidate in candidates:
            if candidate.evidence_strength.level < 1 or candidate.evidence_strength.level > 3:
                issues.append(f"Candidate '{candidate.name}' has invalid evidence strength level")

        # Check for requirements without descriptions
        for req in requirements:
            if not req.description:
                issues.append(f"Requirement '{req.name}' missing description")

    except Exception as e:
        issues.append(f"Failed to load ontology: {e}")

    return issues


def main():
    """Main validation function."""
    if len(sys.argv) != 2:
        print("Usage: python validate_ontology.py <ontology_file>")
        sys.exit(1)

    ontology_path = Path(sys.argv[1])

    if not ontology_path.exists():
        print(f"❌ Error: Ontology file not found: {ontology_path}")
        sys.exit(1)

    print(f"🔍 Validating ontology: {ontology_path}")
    print("=" * 50)

    issues = validate_ontology_file(ontology_path)

    if not issues:
        print("✅ Ontology validation passed!")
        print("All structural and content validations successful.")
    else:
        print("❌ Ontology validation failed!")
        print("Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
