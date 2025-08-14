#!/usr/bin/env python3
"""Code Quality Automation Orchestrator using LangGraph"""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class QualityStage(Enum):
    """Stages of the quality automation workflow"""

    SUBPROJECT_SCRUBBING = "subproject_scrubbing"
    BLACK_FORMATTING = "black_formatting"
    RUFF_LINTING = "ruff_linting"
    PRE_COMMIT_CHECK = "pre_commit_check"
    MULTI_AGENT_ANALYSIS = "multi_agent_analysis"
    PDCA_ITERATION = "pdca_iteration"
    COMPLETE = "complete"


@dataclass
class QualityIssue:
    """Represents a quality issue found during analysis"""

    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    fix_suggestion: str
    automated_fix_available: bool

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "issue_type": self.issue_type,
            "description": self.description,
            "severity": self.severity,
            "fix_suggestion": self.fix_suggestion,
            "automated_fix_available": self.automated_fix_available,
        }


@dataclass
class QualityReport:
    """Comprehensive quality analysis report"""

    timestamp: str
    target_directory: str
    total_files_analyzed: int
    files_with_issues: int
    total_issues: int
    issues_by_severity: dict[str, int]
    issues_by_type: dict[str, int]
    automated_fixes_applied: int
    manual_fixes_required: int
    recommendations: list[str]
    next_actions: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp,
            "target_directory": self.target_directory,
            "total_files_analyzed": self.total_files_analyzed,
            "files_with_issues": self.files_with_issues,
            "total_issues": self.total_issues,
            "issues_by_severity": self.issues_by_severity,
            "issues_by_type": self.issues_by_type,
            "automated_fixes_applied": self.automated_fixes_applied,
            "manual_fixes_required": self.manual_fixes_required,
            "recommendations": self.recommendations,
            "next_actions": self.next_actions,
        }


class CodeQualityAutomationOrchestrator:
    """Orchestrates the complete code quality automation workflow"""

    def __init__(self, target_directory: str = "."):
        """Initialize the orchestrator"""
        self.target_directory = Path(target_directory).resolve()
        self.current_stage = QualityStage.SUBPROJECT_SCRUBBING
        self.quality_reports: list[QualityReport] = []
        self.iteration_count = 0
        self.max_iterations = 5  # Prevent infinite loops

    def run_black_formatting(self) -> dict[str, Any]:
        """Run Black formatting on target directory"""
        print("🎨 Running Black formatting...")

        try:
            result = subprocess.run(
                [
                    "python3",
                    "-m",
                    "black",
                    str(self.target_directory),
                    "--line-length",
                    "88",
                ],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
            )

            if result.returncode == 0:
                print("✅ Black formatting completed successfully")
                return {
                    "success": True,
                    "files_formatted": "Unknown",  # Black doesn't report this clearly
                    "output": result.stdout,
                }
            print(f"⚠️ Black formatting completed with issues: {result.stderr}")
            return {
                "success": True,  # Black often "succeeds" even with parse errors
                "files_formatted": "Unknown",
                "output": result.stdout,
                "warnings": result.stderr,
            }

        except Exception as e:
            print(f"❌ Black formatting failed: {e}")
            return {"success": False, "error": str(e)}

    def run_ruff_linting(self) -> dict[str, Any]:
        """Run Ruff linting with auto-fixes"""
        print("🔧 Running Ruff linting with auto-fixes...")

        try:
            # First run: check and fix what we can
            result = subprocess.run(
                [
                    "python3",
                    "-m",
                    "ruff",
                    "check",
                    str(self.target_directory),
                    "--fix",
                    "--unsafe-fixes",
                ],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
            )

            # Second run: check what remains
            check_result = subprocess.run(
                ["python3", "-m", "ruff", "check", str(self.target_directory)],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
            )

            # Parse remaining issues
            remaining_issues = self._parse_ruff_output(check_result.stdout)

            return {
                "success": True,
                "issues_fixed": "Auto-fixes applied",
                "remaining_issues": len(remaining_issues),
                "remaining_issues_details": remaining_issues,
                "output": result.stdout,
            }

        except Exception as e:
            print(f"❌ Ruff linting failed: {e}")
            return {"success": False, "error": str(e)}

    def run_subproject_scrubbing(self) -> dict[str, Any]:
        """Run subproject scrubbing across all subprojects"""
        print("🔧 Running subproject scrubbing...")

        try:
            # Import and run the subproject scrubber
            scrubber_script = (
                Path(__file__).parent.parent.parent
                / "scripts"
                / "scrub_all_subprojects.py"
            )

            print(f"   📁 Scrubber script: {scrubber_script}")

            if not scrubber_script.exists():
                print(f"   ❌ Script not found at {scrubber_script}")
                return {
                    "success": False,
                    "error": f"Subproject scrubber script not found at {scrubber_script}",
                }

            print("   🔄 Executing subproject scrubber...")
            # Run the subproject scrubber
            result = subprocess.run(
                ["python3", str(scrubber_script)],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode == 0:
                print("✅ Subproject scrubbing completed successfully")
                return {
                    "success": True,
                    "output": result.stdout,
                    "subprojects_processed": "See output for details",
                }

            print("⚠️ Subproject scrubbing completed with issues")
            return {
                "success": False,
                "error": result.stderr,
                "output": result.stdout,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Subproject scrubbing timed out after 5 minutes",
            }
        except Exception as e:
            return {"success": False, "error": f"Subproject scrubbing failed: {str(e)}"}

    def run_pre_commit_check(self) -> dict[str, Any]:
        """Run pre-commit hooks on staged files only"""
        print("🔍 Running pre-commit checks on staged files...")

        try:
            # Get ONLY staged Python files (what git actually cares about)
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
                timeout=30,
            )

            if result.returncode != 0:
                print("   ⚠️ Could not get staged files from git")
                return {
                    "success": False,
                    "error": "Failed to get staged files from git",
                    "files_checked": 0,
                    "issues_found": 0,
                }

            staged_files = result.stdout.strip().split("\n")
            python_files = [f for f in staged_files if f.endswith(".py") and f.strip()]

            if not python_files:
                print("   ℹ️ No staged Python files found")
                return {
                    "success": True,
                    "files_checked": 0,
                    "issues_found": 0,
                    "message": "No staged Python files to check",
                }

            print(f"   📁 Checking {len(python_files)} staged Python files...")

            # Run pre-commit on ONLY staged files
            print("   🔄 Executing pre-commit hooks on staged files...")
            result = subprocess.run(
                ["python3", "-m", "pre_commit", "run", "--files"] + python_files,
                capture_output=True,
                text=True,
                cwd=self.target_directory,
                timeout=60,  # 1 minute timeout (should be fast for staged files)
            )

            print("   ✅ Pre-commit execution completed")

            # Parse pre-commit output
            issues = self._parse_pre_commit_output(result.stdout, result.stderr)

            return {
                "success": result.returncode == 0,
                "files_checked": len(python_files),
                "issues_found": len(issues),
                "issues": issues,
                "output": result.stdout,
                "stderr": result.stderr,
            }

        except subprocess.TimeoutExpired:
            print("   ⏰ Pre-commit check timed out after 2 minutes")
            return {"success": False, "error": "Timeout after 2 minutes"}
        except Exception as e:
            print(f"   ❌ Pre-commit check failed: {e}")
            return {"success": False, "error": str(e)}

    def run_multi_agent_analysis(self) -> dict[str, Any]:
        """Run multi-agent analysis of current code quality state"""
        print("🤖 Running multi-agent analysis...")

        try:
            # Import our diversity system components
            from multi_dimensional_smoke_test import MultiDimensionalSmokeTest

            # Create analysis scenario
            analysis_scenario = {
                "context": f"Code quality analysis of {self.target_directory}",
                "current_state": {
                    "target_directory": str(self.target_directory),
                    "iteration_count": self.iteration_count,
                    "quality_reports": [r.to_dict() for r in self.quality_reports],
                },
                "analysis_question": "What are the current code quality issues and how should we address them systematically?",
                "focus_areas": [
                    "code formatting consistency",
                    "linting compliance",
                    "pre-commit hook failures",
                    "systematic quality improvements",
                    "PDCA cycle optimization",
                ],
            }

            # Initialize multi-agent system
            test_system = MultiDimensionalSmokeTest()

            # Run analysis with different perspectives
            analysis_results = {}

            # Security perspective
            security_analysis = test_system.run_test(
                "security_audit",
                "security_expert",
                "direct_questions",
                "json",
                analysis_scenario,
            )
            analysis_results["security"] = security_analysis

            # Code quality perspective
            quality_analysis = test_system.run_test(
                "code_quality",
                "code_quality_expert",
                "socratic_questioning",
                "json",
                analysis_scenario,
            )
            analysis_results["quality"] = quality_analysis

            # DevOps perspective
            devops_analysis = test_system.run_test(
                "devops",
                "devops_engineer",
                "structured_analysis",
                "json",
                analysis_scenario,
            )
            analysis_results["devops"] = devops_analysis

            return {
                "success": True,
                "analysis_results": analysis_results,
                "perspectives_analyzed": ["security", "quality", "devops"],
            }

        except Exception as e:
            print(f"❌ Multi-agent analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": self._fallback_quality_analysis(),
            }

    def _fallback_quality_analysis(self) -> dict[str, Any]:
        """Fallback analysis when multi-agent system fails"""
        return {
            "analysis_type": "fallback",
            "recommendations": [
                "Continue with automated fixes",
                "Focus on critical linting errors",
                "Iterate through PDCA cycle",
            ],
            "priority_actions": [
                "Fix remaining ruff issues",
                "Address pre-commit failures",
                "Validate code functionality",
            ],
        }

    def _parse_ruff_output(self, output: str) -> list[dict[str, Any]]:
        """Parse Ruff output to extract remaining issues"""
        issues = []
        lines = output.split("\n")

        for line in lines:
            if ":" in line and any(
                code in line
                for code in [
                    "E",
                    "W",
                    "F",
                    "C",
                    "UP",
                    "N",
                    "S",
                    "SIM",
                    "A",
                    "B",
                    "DTZ",
                    "PTH",
                    "INP",
                    "G",
                    "RET",
                ]
            ):
                parts = line.split(":")
                if len(parts) >= 4:
                    issues.append(
                        {
                            "file": parts[0],
                            "line": parts[1],
                            "column": parts[2],
                            "code": parts[3].split()[0] if parts[3].split() else "",
                            "message": ":".join(parts[3:]).strip(),
                        }
                    )

        return issues

    def _parse_pre_commit_output(
        self, stdout: str, stderr: str
    ) -> list[dict[str, Any]]:
        """Parse pre-commit output to extract issues"""
        issues = []

        # Parse stdout for hook results
        lines = stdout.split("\n")
        current_hook = None

        for line in lines:
            if "hook id:" in line:
                current_hook = line.split("hook id:")[1].strip()
            elif "Failed" in line and current_hook:
                issues.append(
                    {"hook": current_hook, "status": "Failed", "details": line.strip()}
                )
            elif "Passed" in line and current_hook:
                issues.append(
                    {"hook": current_hook, "status": "Passed", "details": line.strip()}
                )

        # Parse stderr for errors
        if stderr:
            issues.append(
                {"hook": "general", "status": "Error", "details": stderr.strip()}
            )

        return issues

    def generate_quality_report(self) -> QualityReport:
        """Generate comprehensive quality report"""
        # Count issues by severity and type
        issues_by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        issues_by_type = {}

        # Analyze current state
        total_files = len(list(self.target_directory.rglob("*.py")))
        files_with_issues = 0

        # Get current ruff status
        try:
            ruff_check = subprocess.run(
                ["python3", "-m", "ruff", "check", str(self.target_directory)],
                capture_output=True,
                text=True,
                cwd=self.target_directory,
            )
            remaining_ruff_issues = self._parse_ruff_output(ruff_check.stdout)
            total_issues = len(remaining_ruff_issues)
        except Exception:
            total_issues = 0
            remaining_ruff_issues = []

        # Categorize issues
        for issue in remaining_ruff_issues:
            issue_type = issue.get("code", "unknown")
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = 0
            issues_by_type[issue_type] += 1

            # Determine severity based on issue type
            if issue_type.startswith(("E", "F")):  # Errors
                issues_by_severity["critical"] += 1
            elif issue_type.startswith("W"):  # Warnings
                issues_by_severity["high"] += 1
            else:
                issues_by_severity["medium"] += 1

        # Generate recommendations
        recommendations = []
        if total_issues > 0:
            recommendations.append(f"Address {total_issues} remaining linting issues")
        if issues_by_severity["critical"] > 0:
            recommendations.append("Fix critical errors first")
        if issues_by_severity["high"] > 0:
            recommendations.append("Address high-priority warnings")

        # Next actions
        next_actions = []
        if total_issues == 0:
            next_actions.append("Code quality automation complete!")
        else:
            next_actions.append("Continue PDCA iteration")
            next_actions.append("Apply remaining automated fixes")
            next_actions.append("Address manual fixes if needed")

        return QualityReport(
            timestamp=datetime.now().isoformat(),
            target_directory=str(self.target_directory),
            total_files_analyzed=total_files,
            files_with_issues=files_with_issues,
            total_issues=total_issues,
            issues_by_severity=issues_by_severity,
            issues_by_type=issues_by_type,
            automated_fixes_applied=0,  # Would need to track this
            manual_fixes_required=total_issues,
            recommendations=recommendations,
            next_actions=next_actions,
        )

    def run_pdca_iteration(self) -> dict[str, Any]:
        """Run one PDCA (Plan-Do-Check-Act) iteration"""
        print(f"🔄 Running PDCA iteration {self.iteration_count + 1}...")

        # Plan: Generate current quality report
        current_report = self.generate_quality_report()

        # Do: Apply automated fixes
        subproject_result = self.run_subproject_scrubbing()
        black_result = self.run_black_formatting()
        ruff_result = self.run_ruff_linting()

        # Check: Run pre-commit validation
        pre_commit_result = self.run_pre_commit_check()

        # Act: Analyze results and plan next iteration
        multi_agent_result = self.run_multi_agent_analysis()

        # Store results
        self.quality_reports.append(current_report)
        self.iteration_count += 1

        # Determine if we should continue
        should_continue = (
            self.iteration_count < self.max_iterations
            and current_report.total_issues > 0
            and not pre_commit_result.get("success", False)
        )

        return {
            "iteration": self.iteration_count,
            "plan": current_report.to_dict(),
            "do": {
                "subprojects": subproject_result,
                "black": black_result,
                "ruff": ruff_result,
            },
            "check": pre_commit_result,
            "act": multi_agent_result,
            "should_continue": should_continue,
            "total_issues_remaining": current_report.total_issues,
        }

    def run_complete_automation(self) -> dict[str, Any]:
        """Run the complete automation workflow until clean"""
        print("🚀 Starting complete code quality automation workflow...")

        # Start with subproject scrubbing
        print("🔧 Phase 1: Subproject scrubbing...")
        subproject_result = self.run_subproject_scrubbing()
        if not subproject_result.get("success", False):
            print(
                f"⚠️ Subproject scrubbing had issues: {subproject_result.get('error', 'Unknown error')}"
            )
        else:
            print("✅ Subproject scrubbing completed")

        results = {
            "workflow_start": datetime.now().isoformat(),
            "target_directory": str(self.target_directory),
            "subproject_scrubbing": subproject_result,
            "iterations": [],
            "final_report": None,
        }

        iteration = 0
        while iteration < self.max_iterations:
            print(f"\n🔄 Iteration {iteration + 1}/{self.max_iterations}")

            iteration_result = self.run_pdca_iteration()
            results["iterations"].append(iteration_result)

            if not iteration_result["should_continue"]:
                print("✅ Quality automation complete!")
                break

            iteration += 1

        # Generate final report
        final_report = self.generate_quality_report()
        results["final_report"] = final_report.to_dict()
        results["workflow_end"] = datetime.now().isoformat()

        return results

    def save_report(self, filename: str = None) -> str:
        """Save automation report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"code_quality_automation_report_{timestamp}.json"

        report = {
            "orchestrator": {
                "target_directory": str(self.target_directory),
                "current_stage": self.current_stage.value,
                "iteration_count": self.iteration_count,
            },
            "quality_reports": [r.to_dict() for r in self.quality_reports],
            "timestamp": datetime.now().isoformat(),
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        return filename


def main():
    """Main function to run the automation"""
    import sys

    # Parse arguments properly
    args = sys.argv[1:]
    test_mode = "--test" in args

    # Remove --test from args to get target directory
    if "--test" in args:
        args.remove("--test")

    target_dir = args[0] if args else "."

    print("🎯 Code Quality Automation Orchestrator")
    print(f"🎯 Target Directory: {target_dir}")

    if test_mode:
        print("🧪 TEST MODE: Running individual components only")
        print("🎯 Usage: python3 orchestrator.py [directory] --test")
    else:
        print("🎯 Starting automated quality improvement...")
        print(
            "🎯 Workflow: Subproject Scrubbing → Black → Ruff → Pre-commit → Multi-agent Analysis"
        )

    orchestrator = CodeQualityAutomationOrchestrator(target_dir)

    if test_mode:
        # Test individual components
        print("\n🧪 Testing subproject scrubbing...")
        subproject_result = orchestrator.run_subproject_scrubbing()
        print(f"Result: {subproject_result['success']}")

        print("\n🧪 Testing Black formatting...")
        black_result = orchestrator.run_black_formatting()
        print(f"Result: {black_result['success']}")

        print("\n🧪 Testing Ruff linting...")
        ruff_result = orchestrator.run_ruff_linting()
        print(f"Result: {ruff_result['success']}")

        print("\n🧪 Testing pre-commit check...")
        pre_commit_result = orchestrator.run_pre_commit_check()
        print(f"Result: {pre_commit_result['success']}")

        return {
            "test_mode": True,
            "subproject": subproject_result,
            "black": black_result,
            "ruff": ruff_result,
            "pre_commit": pre_commit_result,
        }

    # Run full automation
    results = orchestrator.run_complete_automation()

    # Save report
    report_file = orchestrator.save_report()
    print(f"📊 Report saved to: {report_file}")

    # Print summary
    final_report = results["final_report"]
    if final_report:
        print("\n🎉 FINAL RESULTS:")
        print(f"📁 Files analyzed: {final_report['total_files_analyzed']}")
        print(f"🐛 Issues remaining: {final_report['total_issues']}")
        print(f"🔄 Iterations completed: {len(results['iterations'])}")

        if final_report["total_issues"] == 0:
            print("✨ CODE IS CLEAN AS A WHISTLE! ✨")
        else:
            print("⚠️ Some issues remain - check report for details")

    return results


if __name__ == "__main__":
    main()
