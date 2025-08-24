#!/usr/bin/env python3
"""
Security Best Practices Domain Model

This module defines the domain model for security best practices,
focusing on using established tools instead of custom security scanners.
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SecurityToolType(Enum):
    """Types of security tools available"""

    PYTHON_PACKAGE = "python_package"
    EXTERNAL_BINARY = "external_binary"
    CONFIGURATION = "configuration"


class SecuritySeverity(Enum):
    """Security issue severity levels"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SecurityCategory(Enum):
    """Security issue categories"""

    CREDENTIALS = "credentials"
    VULNERABILITIES = "vulnerabilities"
    DEPENDENCIES = "dependencies"
    INFRASTRUCTURE = "infrastructure"
    CODE_QUALITY = "code_quality"
    SECRETS = "secrets"


@dataclass
class SecurityTool:
    """Represents a security tool configuration"""

    name: str
    tool_type: SecurityToolType
    description: str
    installation_command: str
    configuration_file: Optional[str] = None
    output_format: str = "json"
    exclude_patterns: list[str] = field(default_factory=list)
    include_patterns: list[str] = field(default_factory=list)
    enabled: bool = True
    version: Optional[str] = None


@dataclass
class SecurityFinding:
    """Represents a security finding from any tool"""

    tool_name: str
    finding_id: str
    severity: SecuritySeverity
    category: SecurityCategory
    description: str
    file_path: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    cwe_reference: Optional[str] = None
    confidence: float = 1.0
    false_positive: bool = False
    remediation: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityScanResult:
    """Represents the result of a security scan"""

    tool_name: str
    scan_timestamp: str
    files_scanned: int
    findings_count: int
    findings: list[SecurityFinding]
    scan_duration: float
    success: bool
    error_message: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityWorkflow:
    """Represents a security scanning workflow"""

    name: str
    description: str
    steps: list[str]
    tools: list[str]
    expected_outputs: list[str]
    success_criteria: list[str]
    estimated_duration: float


@dataclass
class SecurityBestPractices:
    """Main domain model for security best practices"""

    # Core principles
    core_principle: str = "Use established tools, not custom scanners"

    # Available security tools
    security_tools: list[SecurityTool] = field(default_factory=list)

    # Security workflows
    workflows: list[SecurityWorkflow] = field(default_factory=list)

    # Configuration
    configuration_file: str = "pyproject.toml"
    exclude_patterns: list[str] = field(default_factory=list)
    include_patterns: list[str] = field(default_factory=list)

    # Best practices
    best_practices: list[str] = field(default_factory=list)

    # Requirements
    requirements: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize default security tools and workflows"""
        if not self.security_tools:
            self._initialize_default_tools()

        if not self.workflows:
            self._initialize_default_workflows()

        if not self.best_practices:
            self._initialize_best_practices()

        if not self.requirements:
            self._initialize_requirements()

    def _initialize_default_tools(self):
        """Initialize the default set of security tools"""
        self.security_tools = [
            SecurityTool(
                name="Bandit",
                tool_type=SecurityToolType.PYTHON_PACKAGE,
                description="Python security scanning with 70+ checks",
                installation_command="uv add --dev --extra security",
                configuration_file="pyproject.toml",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["src/", "scripts/"],
            ),
            SecurityTool(
                name="Semgrep",
                tool_type=SecurityToolType.PYTHON_PACKAGE,
                description="Pattern-based security scanning",
                installation_command="uv add --dev semgrep",
                configuration_file="pyproject.toml",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["src/", "scripts/"],
            ),
            SecurityTool(
                name="Safety",
                tool_type=SecurityToolType.PYTHON_PACKAGE,
                description="Dependency vulnerability scanning",
                installation_command="uv add --dev --extra security",
                configuration_file="pyproject.toml",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["src/", "scripts/"],
            ),
            SecurityTool(
                name="Detect-Secrets",
                tool_type=SecurityToolType.PYTHON_PACKAGE,
                description="Secret detection in code",
                installation_command="uv add --dev --extra security",
                configuration_file=".secrets.baseline",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["src/", "scripts/"],
            ),
            SecurityTool(
                name="Gitleaks",
                tool_type=SecurityToolType.EXTERNAL_BINARY,
                description="Comprehensive secret detection in git repositories",
                installation_command="go install github.com/zricethezav/gitleaks/v8@latest",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["."],
            ),
            SecurityTool(
                name="Trivy",
                tool_type=SecurityToolType.EXTERNAL_BINARY,
                description="Infrastructure and dependency vulnerability scanning",
                installation_command="curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin",
                exclude_patterns=["tests/", ".venv/", "__pycache__/"],
                include_patterns=["."],
            ),
        ]

    def _initialize_default_workflows(self):
        """Initialize the default security workflows"""
        self.workflows = [
            SecurityWorkflow(
                name="Comprehensive Security Scan",
                description="Run all available security tools for complete coverage",
                steps=[
                    "Install security tools via Makefile targets",
                    "Configure security tools via pyproject.toml",
                    "Run comprehensive security scanning workflow",
                    "Generate security reports in multiple formats",
                    "Review and classify security findings",
                    "Fix security issues following best practices",
                    "Validate fixes with security tools",
                    "Document security improvements",
                    "Integrate security scanning into CI/CD",
                    "Maintain security tool configurations",
                ],
                tools=[
                    "Bandit",
                    "Semgrep",
                    "Safety",
                    "Detect-Secrets",
                    "Gitleaks",
                    "Trivy",
                ],
                expected_outputs=[
                    "bandit-report.json",
                    "semgrep-report.json",
                    "safety-report.json",
                    "gitleaks-report.json",
                    "trivy-report.json",
                ],
                success_criteria=[
                    "All security tools execute successfully",
                    "Security reports generated in expected formats",
                    "No critical vulnerabilities detected",
                    "All security findings addressed within SLA",
                ],
                estimated_duration=300.0,  # 5 minutes
            ),
            SecurityWorkflow(
                name="Quick Security Check",
                description="Run essential security checks for development workflow",
                steps=[
                    "Run Bandit for Python security issues",
                    "Run Safety for dependency vulnerabilities",
                    "Run Detect-Secrets for secret detection",
                    "Review findings and fix critical issues",
                ],
                tools=["Bandit", "Safety", "Detect-Secrets"],
                expected_outputs=["Console output with security findings"],
                success_criteria=[
                    "No critical security issues detected",
                    "All high-priority issues addressed",
                ],
                estimated_duration=60.0,  # 1 minute
            ),
        ]

    def _initialize_best_practices(self):
        """Initialize the security best practices"""
        self.best_practices = [
            "NEVER build custom security scanners",
            "ALWAYS use established, battle-tested tools",
            "Follow OWASP Top 10 guidelines",
            "Use CWE references for issue classification",
            "Implement proper severity levels",
            "Use comprehensive security scanning workflow",
            "Integrate multiple security tools for coverage",
            "Provide clear tool installation instructions",
            "Support both Python packages and external binaries",
            "Maintain security tool configurations",
            "Use environment variables for all secrets",
            "Validate and sanitize all user inputs",
            "Implement proper authentication and authorization",
            "Use secure cryptographic primitives",
            "Follow least privilege principle",
        ]

    def _initialize_requirements(self):
        """Initialize the security requirements"""
        self.requirements = [
            "Use established security tools instead of custom scanners",
            "Follow industry best practices (OWASP, CWE)",
            "Implement comprehensive security scanning workflow",
            "Use proper tool integration and configuration",
            "Maintain security tool availability and updates",
            "Document security best practices and workflows",
            "Integrate security scanning into CI/CD pipeline",
            "Provide clear installation and usage instructions",
            "Support multiple security scanning approaches",
            "Ensure security tool compatibility and integration",
        ]

    def get_tool_by_name(self, name: str) -> Optional[SecurityTool]:
        """Get a security tool by name"""
        for tool in self.security_tools:
            if tool.name.lower() == name.lower():
                return tool
        return None

    def get_workflow_by_name(self, name: str) -> Optional[SecurityWorkflow]:
        """Get a security workflow by name"""
        for workflow in self.workflows:
            if workflow.name.lower() == name.lower():
                return workflow
        return None

    def validate_configuration(self) -> list[str]:
        """Validate the security configuration"""
        errors = []

        # Check if all required tools are available
        for tool in self.security_tools:
            if tool.enabled and not self._is_tool_available(tool):
                errors.append(f"Tool {tool.name} is not available")

        # Check configuration files
        if not Path(self.configuration_file).exists():
            errors.append(f"Configuration file {self.configuration_file} not found")

        return errors

    def _is_tool_available(self, tool: SecurityTool) -> bool:
        """Check if a security tool is available"""
        # This is a simplified check - in practice, you'd check actual tool availability
        return True

    def to_dict(self) -> dict[str, Any]:
        """Convert the domain model to a dictionary"""
        return {
            "core_principle": self.core_principle,
            "security_tools": [tool.__dict__ for tool in self.security_tools],
            "workflows": [workflow.__dict__ for workflow in self.workflows],
            "configuration_file": self.configuration_file,
            "exclude_patterns": self.exclude_patterns,
            "include_patterns": self.include_patterns,
            "best_practices": self.best_practices,
            "requirements": self.requirements,
        }

    def save_configuration(self, file_path: str):
        """Save the configuration to a file"""
        config = self.to_dict()
        with open(file_path, "w") as f:
            json.dump(config, f, indent=2, default=str)

    @classmethod
    def load_configuration(cls, file_path: str) -> "SecurityBestPractices":
        """Load the configuration from a file"""
        with open(file_path) as f:
            config = json.load(f)

        # Reconstruct the domain model
        instance = cls()
        instance.core_principle = config.get("core_principle", instance.core_principle)
        instance.configuration_file = config.get(
            "configuration_file", instance.configuration_file
        )
        instance.exclude_patterns = config.get(
            "exclude_patterns", instance.exclude_patterns
        )
        instance.include_patterns = config.get(
            "include_patterns", instance.include_patterns
        )

        return instance


def main():
    """Main function to demonstrate the domain model"""
    # Create security best practices instance
    security_bp = SecurityBestPractices()

    # Print the domain model
    print("🔒 Security Best Practices Domain Model")
    print("=" * 50)
    print(f"Core Principle: {security_bp.core_principle}")
    print()

    print("🛠️  Available Security Tools:")
    for tool in security_bp.security_tools:
        print(f"  ✅ {tool.name}: {tool.description}")
        print(f"      Type: {tool.tool_type.value}")
        print(f"      Installation: {tool.installation_command}")
        print()

    print("🚀 Security Workflows:")
    for workflow in security_bp.workflows:
        print(f"  📋 {workflow.name}")
        print(f"      Description: {workflow.description}")
        print(f"      Estimated Duration: {workflow.estimated_duration}s")
        print()

    print("📚 Best Practices:")
    for i, practice in enumerate(security_bp.best_practices, 1):
        print(f"  {i:2d}. {practice}")

    print()
    print("📋 Requirements:")
    for i, requirement in enumerate(security_bp.requirements, 1):
        print(f"  {i:2d}. {requirement}")

    # Validate configuration
    errors = security_bp.validate_configuration()
    if errors:
        print(f"\n❌ Configuration Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"\n✅ Configuration Valid")


if __name__ == "__main__":
    main()
