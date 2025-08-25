"""
Pattern Manager for Security Scanning

This module manages security patterns and provides file scanning
capabilities for detecting security issues.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PatternManager:
    """
    Manages security patterns and provides file scanning capabilities

    Features:
    - Credential detection patterns
    - Vulnerability detection patterns
    - Compliance checking patterns
    - False positive filtering
    - Pattern configuration
    """

    def __init__(self, config=None):
        """
        Initialize pattern manager

        Args:
            config: Configuration manager (optional)
        """
        self.config = config
        self.patterns = self._load_security_patterns()

        logger.debug("Pattern manager initialized")

    def _load_security_patterns(self) -> list[dict[str, Any]]:
        """Load security detection patterns"""
        return [
            # API Keys
            {
                "name": "OpenAI API Key",
                "pattern": r"sk-[a-zA-Z0-9]{48}",
                "severity": "CRITICAL",
                "description": "OpenAI API key detected",
                "category": "credentials",
                "false_positive_patterns": [r"sk-test", r"sk-demo", r"YOUR_API_KEY"],
            },
            {
                "name": "Anthropic API Key",
                "pattern": r"sk-ant-[a-zA-Z0-9]{48}",
                "severity": "CRITICAL",
                "description": "Anthropic API key detected",
                "category": "credentials",
                "false_positive_patterns": [
                    r"sk-ant-test",
                    r"sk-ant-demo",
                    r"YOUR_ANTHROPIC_KEY",
                ],
            },
            {
                "name": "Generic API Key",
                "pattern": r'(?:api[_-]?key|apikey|api_key)\s*[=:]\s*[\'"]?[a-zA-Z0-9]{20,}[\'"]?',
                "severity": "HIGH",
                "description": "Generic API key pattern detected",
                "category": "credentials",
                "false_positive_patterns": [
                    r"YOUR_API_KEY",
                    r"API_KEY_PLACEHOLDER",
                    r"example_key",
                ],
            },
            # AWS Credentials
            {
                "name": "AWS Access Key ID",
                "pattern": r"AKIA[0-9A-Z]{16}",
                "severity": "CRITICAL",
                "description": "AWS access key ID detected",
                "category": "credentials",
                "false_positive_patterns": [r"AKIAEXAMPLE", r"AKIA_DEMO"],
            },
            {
                "name": "AWS Secret Access Key",
                "pattern": r"[0-9a-zA-Z/+=]{40}",
                "severity": "CRITICAL",
                "description": "AWS secret access key detected",
                "category": "credentials",
                "false_positive_patterns": [r"EXAMPLE_KEY", r"DEMO_SECRET"],
            },
            # Private Keys
            {
                "name": "Private Key",
                "pattern": r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----",
                "severity": "CRITICAL",
                "description": "Private key detected",
                "category": "credentials",
                "false_positive_patterns": [r"EXAMPLE_KEY", r"DEMO_KEY"],
            },
            # Database Credentials
            {
                "name": "Database Connection String",
                "pattern": r"(?:mysql|postgresql|mongodb|redis)://[^\s]+",
                "severity": "HIGH",
                "description": "Database connection string detected",
                "category": "credentials",
                "false_positive_patterns": [
                    r"localhost",
                    r"127\.0\.0\.1",
                    r"example\.com",
                ],
            },
            # OAuth and JWT
            {
                "name": "OAuth Client Secret",
                "pattern": r"[a-zA-Z0-9]{32,}",
                "severity": "HIGH",
                "description": "Potential OAuth client secret detected",
                "category": "credentials",
                "false_positive_patterns": [
                    r"YOUR_CLIENT_SECRET",
                    r"CLIENT_SECRET_PLACEHOLDER",
                ],
            },
            {
                "name": "JWT Token",
                "pattern": r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
                "severity": "MEDIUM",
                "description": "JWT token detected",
                "category": "credentials",
                "false_positive_patterns": [r"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"],
            },
            # Generic Secrets
            {
                "name": "Generic Secret",
                "pattern": r'(?:secret|password|token|key)\s*[=:]\s*[\'"]?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?]{8,}[\'"]?',
                "severity": "MEDIUM",
                "description": "Generic secret pattern detected",
                "category": "credentials",
                "false_positive_patterns": [
                    r"YOUR_SECRET",
                    r"PASSWORD_PLACEHOLDER",
                    r"example_secret",
                ],
            },
        ]

    def scan_file(self, file_path: Path) -> list[dict[str, Any]]:
        """
        Scan a single file for security issues with parallel pattern matching

        Args:
            file_path: Path to file to scan

        Returns:
            List of security findings
        """
        findings = []

        try:
            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Scan each line for patterns
            for line_num, line in enumerate(lines, 1):
                line_findings = self._scan_line(line, line_num, file_path)
                findings.extend(line_findings)

            # Remove duplicates and sort by severity
            unique_findings = self._deduplicate_findings(findings)
            return self._sort_findings_by_severity(unique_findings)

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")
            return [
                {
                    "pattern_name": "Scan Error",
                    "severity": "LOW",
                    "description": f"Error scanning file: {e}",
                    "line_number": 0,
                    "matched_text": "",
                    "context": "",
                    "false_positive": False,
                    "category": "error",
                }
            ]

    def _scan_line(
        self, line: str, line_num: int, file_path: Path
    ) -> list[dict[str, Any]]:
        """
        Scan a single line for security patterns

        Args:
            line: Line content to scan
            line_number: Line number in file
            file_path: Path to file being scanned

        Returns:
            List of findings for this line
        """
        findings = []

        for pattern in self.patterns:
            try:
                matches = re.finditer(pattern["pattern"], line, re.IGNORECASE)

                for match in matches:
                    matched_text = match.group(0)

                    # Check if this is a false positive
                    is_false_positive = self._is_false_positive(
                        pattern, matched_text, line, file_path
                    )

                    # Create finding
                    finding = {
                        "pattern_name": pattern["name"],
                        "severity": pattern["severity"],
                        "description": pattern["description"],
                        "line_number": line_num,
                        "matched_text": matched_text,
                        "context": line.strip(),
                        "false_positive": is_false_positive,
                        "category": pattern["category"],
                        "file_path": str(file_path),
                    }

                    findings.append(finding)

            except Exception as e:
                logger.warning(f"Error applying pattern {pattern['name']}: {e}")

        return findings

    def _is_false_positive(
        self, pattern: dict[str, Any], matched_text: str, line: str, file_path: Path
    ) -> bool:
        """
        Check if a pattern match is a false positive

        Args:
            pattern: Pattern that matched
            matched_text: Text that matched the pattern
            line: Full line content
            file_path: Path to file being scanned

        Returns:
            True if this is a false positive
        """
        # Check false positive patterns
        false_positive_patterns = pattern.get("false_positive_patterns", [])
        for fp_pattern in false_positive_patterns:
            if re.search(fp_pattern, line, re.IGNORECASE):
                return True

        # Check for common false positive indicators
        false_positive_indicators = [
            "YOUR_",
            "PLACEHOLDER",
            "EXAMPLE_",
            "DEMO_",
            "TEST_",
            "TODO:",
            "FIXME:",
            "NOTE:",
            "WARNING:",
            "example",
            "demo",
            "test",
            "placeholder",
            "template",
        ]

        for indicator in false_positive_indicators:
            if indicator.lower() in line.lower():
                return True

        # Check file path for test/example indicators
        return bool(
            any(
                indicator in str(file_path).lower()
                for indicator in ["test", "example", "demo", "template", "sample"]
            )
        )

    def _deduplicate_findings(
        self, findings: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Remove duplicate findings

        Args:
            findings: List of findings to deduplicate

        Returns:
            Deduplicated list of findings
        """
        seen = set()
        unique_findings = []

        for finding in findings:
            # Create unique key for deduplication
            key = f"{finding['file_path']}:{finding['line_number']}:{finding['pattern_name']}"

            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)

        return unique_findings

    def _sort_findings_by_severity(
        self, findings: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Sort findings by severity level

        Args:
            findings: List of findings to sort

        Returns:
            Sorted list of findings
        """
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

        return sorted(findings, key=lambda x: severity_order.get(x["severity"], 4))
