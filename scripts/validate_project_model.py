#!/usr/bin/env python3
"""Project Model Registry Validation Script for Pre-commit Hooks"""

import json
import sys
from pathlib import Path


class ProjectModelValidator:
    """Validates project model registry consistency"""

    def __init__(self, model_file: str = "project_model_registry.json"):
        """Initialize validator with model file path"""
        self.model_file = Path(model_file)
        self.model = None
        self.errors = []
        self.warnings = []

    def load_model(self) -> bool:
        """Load and parse the project model registry"""
        try:
            if not self.model_file.exists():
                self.errors.append(f"Model file not found: {self.model_file}")
                return False

            with open(self.model_file) as f:
                self.model = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in model file: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading model file: {e}")
            return False

    def validate_structure(self) -> bool:
        """Validate basic model structure"""
        if not self.model:
            return False

        required_keys = [
            "description",
            "author",
            "project_purpose",
            "domain_architecture",
            "domains",
            "requirements_traceability",
        ]

        for key in required_keys:
            if key not in self.model:
                self.errors.append(f"Missing required key: {key}")

        return len(self.errors) == 0

    def validate_domains(self) -> bool:
        """Validate domain definitions"""
        if not self.model or "domains" not in self.model:
            return False

        domains = self.model["domains"]
        for domain_name, domain_config in domains.items():
            # Check required domain properties
            required_props = ["patterns", "content_indicators", "linter"]
            for prop in required_props:
                if prop not in domain_config:
                    self.errors.append(
                        f"Domain '{domain_name}' missing required property: {prop}"
                    )

            # Check if domain directory exists
            domain_path = Path(f"src/{domain_name}")
            if not domain_path.exists():
                self.warnings.append(f"Domain directory not found: {domain_path}")

        return len(self.errors) == 0

    def validate_requirements_traceability(self) -> bool:
        """Validate requirements traceability"""
        if not self.model or "requirements_traceability" not in self.model:
            return False

        requirements = self.model["requirements_traceability"]
        for req in requirements:
            # Check required requirement properties
            required_props = ["requirement", "test", "implementation"]
            for prop in required_props:
                if prop not in req:
                    self.errors.append(f"Requirement missing required property: {prop}")

            # Check if test file exists
            test_path = Path(f"tests/{req['test']}")
            if not test_path.exists():
                self.warnings.append(f"Test file not found: {test_path}")

        return len(self.errors) == 0

    def validate_staged_files(self) -> bool:
        """Validate that staged files align with model domains"""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                self.warnings.append("Could not get staged files from git")
                return True

            staged_files = result.stdout.strip().split("\n")
            if not staged_files or staged_files == [""]:
                return True  # No staged files

            # Check if staged files align with model domains
            domains = self.model.get("domains", {})
            for file_path in staged_files:
                file_path = Path(file_path)
                if file_path.suffix == ".py":
                    # Check if file belongs to a domain
                    domain_found = False
                    for domain_name, domain_config in domains.items():
                        patterns = domain_config.get("patterns", [])
                        for pattern in patterns:
                            if file_path.match(pattern):
                                domain_found = True
                                break

                    if not domain_found:
                        self.warnings.append(
                            f"Staged file {file_path} not mapped to any domain"
                        )

        except Exception as e:
            self.warnings.append(f"Error checking staged files: {e}")

        return True

    def run_validation(self) -> bool:
        """Run complete validation"""
        print("🔍 Validating Project Model Registry...")

        # Load model
        if not self.load_model():
            return False

        # Validate structure
        if not self.validate_structure():
            return False

        # Validate domains
        if not self.validate_domains():
            return False

        # Validate requirements
        if not self.validate_requirements_traceability():
            return False

        # Validate staged files
        self.validate_staged_files()

        return True

    def print_results(self) -> None:
        """Print validation results"""
        if self.errors:
            print("❌ VALIDATION ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("⚠️ VALIDATION WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("✅ Project model validation passed!")
        elif not self.errors:
            print("✅ Project model validation passed with warnings!")
        else:
            print("❌ Project model validation failed!")

    def get_exit_code(self) -> int:
        """Get exit code for pre-commit hook"""
        return 0 if not self.errors else 1


def main():
    """Main validation function"""
    validator = ProjectModelValidator()

    if validator.run_validation():
        validator.print_results()
        return validator.get_exit_code()

    validator.print_results()
    return 1


if __name__ == "__main__":
    sys.exit(main())
