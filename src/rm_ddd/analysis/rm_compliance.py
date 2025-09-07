"""
RM Compliance Analyzer

Analyzes code for Reflective Module compliance.
"""

import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ComplianceLevel(Enum):
    """RM compliance levels"""

    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass
class ComplianceIssue:
    """Represents a compliance issue"""

    issue_type: str
    severity: str  # "error", "warning", "info"
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ComplianceReport:
    """RM compliance report for a file or codebase"""

    file_path: str = ""
    compliance_level: ComplianceLevel = ComplianceLevel.UNKNOWN
    compliance_percentage: float = 0.0
    issues: List[ComplianceIssue] = field(default_factory=list)
    implemented_methods: List[str] = field(default_factory=list)
    missing_methods: List[str] = field(default_factory=list)
    health_indicators: List[str] = field(default_factory=list)

    def add_issue(self, issue: ComplianceIssue):
        """Add compliance issue"""
        self.issues.append(issue)

    def add_implemented_method(self, method: str):
        """Add implemented method"""
        if method not in self.implemented_methods:
            self.implemented_methods.append(method)

    def add_missing_method(self, method: str):
        """Add missing method"""
        if method not in self.missing_methods:
            self.missing_methods.append(method)

    def add_health_indicator(self, indicator: str):
        """Add health indicator"""
        if indicator not in self.health_indicators:
            self.health_indicators.append(indicator)

    def merge(self, other: "ComplianceReport"):
        """Merge another compliance report"""
        self.issues.extend(other.issues)
        self.implemented_methods.extend(other.implemented_methods)
        self.missing_methods.extend(other.missing_methods)
        self.health_indicators.extend(other.health_indicators)

        # Recalculate compliance percentage
        self._calculate_compliance_percentage()

    def _calculate_compliance_percentage(self):
        """Calculate overall compliance percentage"""
        required_methods = ["get_module_status", "get_module_capabilities", "is_healthy", "get_health_indicators"]

        implemented_count = sum(1 for method in required_methods if method in self.implemented_methods)
        self.compliance_percentage = (implemented_count / len(required_methods)) * 100

        # Determine compliance level
        if self.compliance_percentage >= 100:
            self.compliance_level = ComplianceLevel.FULL
        elif self.compliance_percentage >= 50:
            self.compliance_level = ComplianceLevel.PARTIAL
        else:
            self.compliance_level = ComplianceLevel.NONE


class RMComplianceAnalyzer:
    """Analyzes code for RM compliance"""

    def __init__(self):
        self.required_methods = ["get_module_status", "get_module_capabilities", "is_healthy", "get_health_indicators"]

        self.optional_methods = ["get_domain_boundaries", "validate_domain_invariants"]

    def analyze_file(self, tree: ast.AST, file_path: str) -> Optional[ComplianceReport]:
        """Analyze file for RM compliance"""
        report = ComplianceReport(file_path=file_path)

        # Find all classes
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        for class_node in classes:
            self._analyze_class(class_node, report)

        # Calculate final compliance
        report._calculate_compliance_percentage()

        return report if report.issues or report.implemented_methods else None

    def _analyze_class(self, class_node: ast.ClassDef, report: ComplianceReport):
        """Analyze individual class for RM compliance"""

        # Check for RM base class inheritance
        has_rm_base = False
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                if "ReflectiveModule" in base.id or "DomainReflectiveModule" in base.id:
                    has_rm_base = True
                    report.add_issue(ComplianceIssue(issue_type="inheritance", severity="info", message=f"Class {class_node.name} inherits from RM base class", line_number=class_node.lineno))

        if not has_rm_base:
            report.add_issue(
                ComplianceIssue(
                    issue_type="inheritance",
                    severity="warning",
                    message=f"Class {class_node.name} should inherit from ReflectiveModule or DomainReflectiveModule",
                    line_number=class_node.lineno,
                    suggestion="Add ReflectiveModule or DomainReflectiveModule to base classes",
                )
            )

        # Analyze methods
        methods = [node for node in class_node.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]

        for method in methods:
            self._analyze_method(method, report, class_node.name)

        # Check for module_id attribute (including in methods)
        has_module_id = False
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "module_id":
                        has_module_id = True
                        break
            elif isinstance(item, ast.FunctionDef):
                # Check inside methods for module_id assignment
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and target.attr == "module_id":
                                has_module_id = True
                                break

        if not has_module_id:
            report.add_issue(
                ComplianceIssue(
                    issue_type="attribute",
                    severity="warning",
                    message=f"Class {class_node.name} should have module_id attribute",
                    line_number=class_node.lineno,
                    suggestion="Add module_id attribute to class",
                )
            )

    def _analyze_method(self, method: ast.FunctionDef | ast.AsyncFunctionDef, report: ComplianceReport, class_name: str):
        """Analyze individual method for RM compliance"""
        method_name = method.name

        # Check if it's a required RM method
        if method_name in self.required_methods:
            report.add_implemented_method(method_name)

            # Validate method signature and implementation
            self._validate_rm_method(method, report, class_name)

        # Check for health indicators in get_health_indicators
        if method_name == "get_health_indicators":
            self._analyze_health_indicators(method, report)

        # Check for domain-specific methods
        if method_name in self.optional_methods:
            report.add_implemented_method(method_name)
            report.add_issue(ComplianceIssue(issue_type="method", severity="info", message=f"Class {class_name} implements optional RM method: {method_name}", line_number=method.lineno))

    def _validate_rm_method(self, method: ast.FunctionDef | ast.AsyncFunctionDef, report: ComplianceReport, class_name: str):
        """Validate RM method implementation"""
        method_name = method.name

        # Check if method is async
        is_async = method.name in ["get_module_status", "get_module_capabilities", "is_healthy", "get_health_indicators"]
        is_actually_async = isinstance(method, ast.AsyncFunctionDef)
        if is_async and not is_actually_async:
            report.add_issue(
                ComplianceIssue(
                    issue_type="signature", severity="error", message=f"Method {method_name} should be async", line_number=method.lineno, suggestion="Add async keyword to method definition"
                )
            )

        # Check for proper return type annotations
        if method_name == "get_module_status" and not method.returns:
            report.add_issue(
                ComplianceIssue(
                    issue_type="annotation",
                    severity="warning",
                    message="get_module_status should have return type annotation",
                    line_number=method.lineno,
                    suggestion="Add -> ModuleHealth return type annotation",
                )
            )

        if method_name == "get_module_capabilities" and not method.returns:
            report.add_issue(
                ComplianceIssue(
                    issue_type="annotation",
                    severity="warning",
                    message="get_module_capabilities should have return type annotation",
                    line_number=method.lineno,
                    suggestion="Add -> List[ModuleCapability] return type annotation",
                )
            )

        if method_name == "is_healthy" and not method.returns:
            report.add_issue(
                ComplianceIssue(
                    issue_type="annotation", severity="warning", message="is_healthy should have return type annotation", line_number=method.lineno, suggestion="Add -> bool return type annotation"
                )
            )

        if method_name == "get_health_indicators" and not method.returns:
            report.add_issue(
                ComplianceIssue(
                    issue_type="annotation",
                    severity="warning",
                    message="get_health_indicators should have return type annotation",
                    line_number=method.lineno,
                    suggestion="Add -> Dict[str, Any] return type annotation",
                )
            )

        # Check for proper implementation
        if not method.body or (len(method.body) == 1 and isinstance(method.body[0], ast.Pass)):
            report.add_issue(
                ComplianceIssue(
                    issue_type="implementation",
                    severity="warning",
                    message=f"Method {method_name} appears to be empty or not implemented",
                    line_number=method.lineno,
                    suggestion="Implement the method with proper logic",
                )
            )

    def _analyze_health_indicators(self, method: ast.FunctionDef | ast.AsyncFunctionDef, report: ComplianceReport):
        """Analyze health indicators implementation"""
        indicators_found = []

        # Look for return statements with dictionaries
        for node in ast.walk(method):
            if isinstance(node, ast.Return):
                if isinstance(node.value, ast.Dict):
                    # Extract keys from dictionary
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant):
                            indicators_found.append(key.value)
                        elif isinstance(key, ast.Str):  # Python < 3.8
                            indicators_found.append(key.s)

        # Look for dictionary assignments
        for node in ast.walk(method):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ["indicators", "health_indicators", "metrics"]:
                        if isinstance(node.value, ast.Dict):
                            for key in node.value.keys:
                                if isinstance(key, ast.Constant):
                                    indicators_found.append(key.value)
                                elif isinstance(key, ast.Str):  # Python < 3.8
                                    indicators_found.append(key.s)

        # Add found indicators to report
        for indicator in indicators_found:
            if isinstance(indicator, str):
                report.add_health_indicator(indicator)

        # Check for common health indicators
        common_indicators = ["uptime", "memory_usage", "cpu_usage", "error_count", "request_count"]
        missing_indicators = [ind for ind in common_indicators if ind not in indicators_found]

        if missing_indicators:
            report.add_issue(
                ComplianceIssue(
                    issue_type="indicators",
                    severity="info",
                    message=f"Consider adding common health indicators: {', '.join(missing_indicators)}",
                    line_number=method.lineno,
                    suggestion="Add standard health indicators for better monitoring",
                )
            )

    def get_compliance_summary(self, reports: List[ComplianceReport]) -> Dict[str, Any]:
        """Get summary of compliance across multiple reports"""
        total_files = len(reports)
        if total_files == 0:
            return {
                "total_files": 0,
                "compliance_percentage": 0.0,
                "compliance_level": ComplianceLevel.NONE,
                "total_issues": 0,
                "issues_by_severity": {"error": 0, "warning": 0, "info": 0},
                "implemented_methods": [],
                "missing_methods": [],
                "health_indicators": [],
            }

        # Aggregate data
        total_issues = sum(len(report.issues) for report in reports)
        issues_by_severity = {"error": 0, "warning": 0, "info": 0}

        all_implemented = set()
        all_missing = set()
        all_indicators = set()

        for report in reports:
            # Count issues by severity
            for issue in report.issues:
                issues_by_severity[issue.severity] += 1

            # Collect methods and indicators
            all_implemented.update(report.implemented_methods)
            all_missing.update(report.missing_methods)
            all_indicators.update(report.health_indicators)

        # Calculate average compliance
        avg_compliance = sum(report.compliance_percentage for report in reports) / total_files

        # Determine overall compliance level
        if avg_compliance >= 100:
            overall_level = ComplianceLevel.FULL
        elif avg_compliance >= 50:
            overall_level = ComplianceLevel.PARTIAL
        else:
            overall_level = ComplianceLevel.NONE

        return {
            "total_files": total_files,
            "compliance_percentage": avg_compliance,
            "compliance_level": overall_level,
            "total_issues": total_issues,
            "issues_by_severity": issues_by_severity,
            "implemented_methods": list(all_implemented),
            "missing_methods": list(all_missing),
            "health_indicators": list(all_indicators),
        }
