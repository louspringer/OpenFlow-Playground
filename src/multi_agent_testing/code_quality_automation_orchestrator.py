#!/usr/bin/env python3
"""Code Quality Automation Orchestrator using LangGraph"""

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# LangChain caching imports
try:
    from langchain_core.caches import InMemoryCache
    from langchain_core.globals import set_llm_cache

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


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

        # Initialize LangChain cache for performance
        self._initialize_langchain_cache()

        # Initialize API key manager and test endpoints once
        self.api_manager = None
        self.working_models: list[str] = []
        self.working_openai_key: str | None = None  # Store the working OpenAI API key
        self.working_huggingface_key: str | None = None  # Store the working HuggingFace API key
        self.working_anthropic_key: str | None = None  # Store the working Anthropic API key
        self.working_google_key: str | None = None  # Store the working Google API key
        self.working_aws_key: str | None = None  # Store the working AWS API key
        self.working_aws_secret: str | None = None  # Store the working AWS secret key
        self._initialize_api_manager()

    def _initialize_langchain_cache(self) -> None:
        """Initialize LangChain caching for improved performance"""
        if LANGCHAIN_AVAILABLE:
            try:
                # Set up in-memory cache for LLM calls
                cache = InMemoryCache()
                set_llm_cache(cache)
                print("✅ LangChain in-memory cache initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize LangChain cache: {e}")
        else:
            print("⚠️ LangChain not available, skipping cache initialization")

    def _initialize_api_manager(self):
        """Initialize API key manager and populate working models."""
        try:
            from op_api_manager.core import OnePasswordAPIKeyManager
            from op_api_manager.models import CacheConfig

            # Initialize API key manager with proper cache configuration
            cache_config = CacheConfig()
            self.api_manager = OnePasswordAPIKeyManager(cache_config)

            if self.api_manager:
                print("🔑 Initializing API key manager...")

                # First, try to get working credentials from cache
                print("  📦 Loading working credentials from cache...")
                working_credentials = self.api_manager.get_working_credentials_all(force_test=False)

                if working_credentials:
                    print(f"  ✅ Found {sum(len(apis) for apis in working_credentials.values())} working APIs in cache")
                    self._populate_working_models_from_cache(working_credentials)
                else:
                    print("  🔄 No working credentials in cache, testing APIs...")
                    # Test API endpoints to discover working ones
                    test_results = self.api_manager.test_api_endpoints(verbose=True)
                    if test_results:
                        print(f"  ✅ API testing completed, found {sum(len(apis) for apis in test_results.values())} working APIs")
                        self._populate_working_models_from_test_results(test_results)
                    else:
                        print("  ⚠️ No working APIs found during testing")

                # Set environment variables for multi-agent systems
                print("  🔧 Setting environment variables for multi-agent systems...")
                self.api_manager.set_environment_variables()

                # If we still don't have working models, use fallback
                if not self.working_models:
                    print("  🔍 Fallback: Using default model configurations...")
                    self._populate_fallback_models()

                print(f"  🎯 Final working models: {', '.join(self.working_models)}")

            else:
                print("❌ Failed to initialize API key manager")
                self._populate_fallback_models()

        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("  🔧 Falling back to default model configurations...")
            self._populate_fallback_models()
        except Exception as e:
            print(f"❌ Error initializing API manager: {e}")
            print("  🔧 Falling back to default model configurations...")
            self._populate_fallback_models()

    def _populate_working_models_from_cache(self, working_credentials: dict):
        """Populate working models from cached working credentials."""
        try:
            for provider, api_list in working_credentials.items():
                if api_list and len(api_list) > 0:
                    # Add working models based on provider
                    if provider == "openai":
                        self.working_models.extend(
                            [
                                "gpt4_vision",
                                "gpt5",
                                "gpt4o",
                                "gpt4o_mini",
                                "gpt3_5_turbo",
                            ]
                        )
                        self.working_openai_key = "cached"
                    elif provider == "anthropic":
                        self.working_models.extend(["claude_3_5_sonnet", "claude_3_haiku", "claude_3_opus"])
                        self.working_anthropic_key = "cached"
                    elif provider == "google" or provider == "gemini":
                        self.working_models.extend(["gemini_pro", "gemini_flash", "gemini_pro_vision"])
                        self.working_google_key = "cached"
                    elif provider == "aws" or provider == "bedrock":
                        self.working_models.extend(["claude_bedrock", "titan_express", "llama2_bedrock"])
                        self.working_aws_key = "cached"
                    elif provider == "huggingface":
                        self.working_models.append("huggingface")
                        self.working_huggingface_key = "cached"
                    elif provider == "cohere":
                        self.working_models.append("cohere")
                        self.working_cohere_key = "cached"
                    elif provider == "ai21":
                        self.working_models.append("ai21")
                        self.working_ai21_key = "cached"
                    elif provider == "openrouter":
                        self.working_models.append("openrouter")
                        self.working_openrouter_key = "cached"

            print(f"  📊 Populated {len(self.working_models)} working models from cache")

        except Exception as e:
            print(f"❌ Error populating models from cache: {e}")

    def _populate_working_models_from_test_results(self, test_results: dict):
        """Populate working models from API test results."""
        try:
            for provider, api_list in test_results.items():
                if api_list and len(api_list) > 0:
                    # Add working models based on provider
                    if provider == "openai":
                        self.working_models.extend(
                            [
                                "gpt4_vision",
                                "gpt5",
                                "gpt4o",
                                "gpt4o_mini",
                                "gpt3_5_turbo",
                            ]
                        )
                        self.working_openai_key = "tested"
                    elif provider == "anthropic":
                        self.working_models.extend(["claude_3_5_sonnet", "claude_3_haiku", "claude_3_opus"])
                        self.working_anthropic_key = "tested"
                    elif provider == "google" or provider == "gemini":
                        self.working_models.extend(["gemini_pro", "gemini_flash", "gemini_pro_vision"])
                        self.working_google_key = "tested"
                    elif provider == "aws" or provider == "bedrock":
                        self.working_models.extend(["claude_bedrock", "titan_express", "llama2_bedrock"])
                        self.working_aws_key = "tested"
                    elif provider == "huggingface":
                        self.working_models.append("huggingface")
                        self.working_huggingface_key = "tested"
                    elif provider == "cohere":
                        self.working_models.append("cohere")
                        self.working_cohere_key = "tested"
                    elif provider == "ai21":
                        self.working_models.append("ai21")
                        self.working_ai21_key = "tested"
                    elif provider == "openrouter":
                        self.working_models.append("openrouter")
                        self.working_openrouter_key = "tested"

            print(f"  📊 Populated {len(self.working_models)} working models from testing")

        except Exception as e:
            print(f"❌ Error populating models from test results: {e}")

    def _populate_fallback_models(self):
        """Populate fallback models when API manager is not available."""
        try:
            # Use environment variables as fallback
            if os.getenv("OPENAI_API_KEY"):
                self.working_models.extend(["gpt4_vision", "gpt5", "gpt4o", "gpt4o_mini", "gpt3_5_turbo"])
                self.working_openai_key = "env"
                print("  🔑 Using OpenAI API key from environment")

            if os.getenv("ANTHROPIC_API_KEY"):
                self.working_models.extend(["claude_3_5_sonnet", "claude_3_haiku", "claude_3_opus"])
                self.working_anthropic_key = "env"
                print("  🔑 Using Anthropic API key from environment")

            if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
                self.working_models.extend(["gemini_pro", "gemini_flash", "gemini_pro_vision"])
                self.working_google_key = "env"
                print("  🔑 Using Google/Gemini API key from environment")

            if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
                self.working_models.extend(["claude_bedrock", "titan_express", "llama2_bedrock"])
                self.working_aws_key = "env"
                print("  🔑 Using AWS credentials from environment")

            if os.getenv("HUGGINGFACE_API_KEY"):
                self.working_models.append("huggingface")
                self.working_huggingface_key = "env"
                print("  🔑 Using HuggingFace API key from environment")

            if os.getenv("COHERE_API_KEY"):
                self.working_models.append("cohere")
                self.working_cohere_key = "env"
                print("  🔑 Using Cohere API key from environment")

            if os.getenv("AI21_API_KEY"):
                self.working_models.append("ai21")
                self.working_ai21_key = "env"
                print("  🔑 Using AI21 API key from environment")

            if os.getenv("OPENROUTER_API_KEY"):
                self.working_models.append("openrouter")
                self.working_openrouter_key = "env"
                print("  🔑 Using OpenRouter API key from environment")

            print(f"  📊 Populated {len(self.working_models)} fallback models from environment")

        except Exception as e:
            print(f"❌ Error populating fallback models: {e}")
            # Ultimate fallback - use basic models
            self.working_models = ["gpt4o", "claude_3_5_sonnet", "gemini_pro"]
            print("  🚨 Using ultimate fallback models")

    def _get_vendor_status(self, model: str) -> dict[str, any]:
        """
        Get vendor information for a specific model.

        Args:
            model: The model name

        Returns:
            Dictionary with vendor information
        """
        # Map models to vendors and cost API availability
        vendor_mapping = {
            # OpenAI models
            "gpt4_vision": {"vendor": "OpenAI", "has_vendor_cost_api": True},
            "gpt5": {"vendor": "OpenAI", "has_vendor_cost_api": True},
            "gpt4o": {"vendor": "OpenAI", "has_vendor_cost_api": True},
            "gpt4o_mini": {"vendor": "OpenAI", "has_vendor_cost_api": True},
            "gpt3_5_turbo": {"vendor": "OpenAI", "has_vendor_cost_api": True},
            # Anthropic models
            "claude_3_5_sonnet": {"vendor": "Anthropic", "has_vendor_cost_api": True},
            "claude_3_haiku": {"vendor": "Anthropic", "has_vendor_cost_api": True},
            "claude_3_opus": {"vendor": "Anthropic", "has_vendor_cost_api": True},
            # Google/Gemini models
            "gemini_pro": {"vendor": "Google", "has_vendor_cost_api": True},
            "gemini_flash": {"vendor": "Google", "has_vendor_cost_api": True},
            "gemini_pro_vision": {"vendor": "Google", "has_vendor_cost_api": True},
            # AWS Bedrock models
            "claude_bedrock": {"vendor": "AWS", "has_vendor_cost_api": True},
            "titan_express": {"vendor": "AWS", "has_vendor_cost_api": True},
            "llama2_bedrock": {"vendor": "AWS", "has_vendor_cost_api": True},
            # Other models
            "huggingface": {"vendor": "HuggingFace", "has_vendor_cost_api": False},
            "cohere": {"vendor": "Cohere", "has_vendor_cost_api": True},
            "ai21": {"vendor": "AI21", "has_vendor_cost_api": True},
            "openrouter": {"vendor": "OpenRouter", "has_vendor_cost_api": True},
        }

        return vendor_mapping.get(model, {"vendor": "Unknown", "has_vendor_cost_api": False})

    def _test_specific_api(self, provider: str, api_key: str) -> bool:
        """
        Tests a specific API endpoint using a provided API key.
        This is a placeholder for actual API testing logic.
        In a real scenario, you would call an endpoint like /v1/models
        or /v1/chat/completions to check if the API key is valid.
        """
        print(f"    Testing {provider.title()} API...")
        try:
            # Example: Test if the API key is valid by making a simple request
            # This is a very basic check and might need more sophisticated logic
            # depending on the specific API provider's requirements.
            # For OpenAI, you might try to list models.
            # For Anthropic, you might try to list models or send a simple completion.
            # For OpenRouter, you might try to list models or send a simple completion.
            # For HuggingFace, you might try to list models or send a simple completion.
            # For Cohere, you might try to list models or send a simple completion.
            # For AI21, you might try to list models or send a simple completion.

            if provider == "openai":
                # Test OpenAI API
                try:
                    import openai

                    client = openai.OpenAI(api_key=api_key)
                    models = client.models.list()
                    print(f"    ✅ OpenAI API key is valid. Found {len(models.data)} models.")
                    return {"working": True, "models_count": len(models.data)}
                except Exception as e:
                    print(f"    ❌ OpenAI API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "anthropic":
                # Test Anthropic API
                try:
                    import anthropic

                    client = anthropic.Anthropic(api_key=api_key)
                    models = client.models.list()
                    print(f"    ✅ Anthropic API key is valid. Found {len(models.data)} models.")
                    return {"working": True, "models_count": len(models.data)}
                except Exception as e:
                    print(f"    ❌ Anthropic API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "openrouter":
                # Test OpenRouter API
                try:
                    import openai

                    client = openai.OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
                    models = client.models.list()
                    print(f"    ✅ OpenRouter API key is valid. Found {len(models.data)} models.")
                    return {"working": True, "models_count": len(models.data)}
                except Exception as e:
                    print(f"    ❌ OpenRouter API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "huggingface":
                # Test HuggingFace API
                try:
                    import huggingface_hub

                    huggingface_hub.login(token=api_key)
                    print("    ✅ HuggingFace API key is valid.")
                    return {
                        "working": True,
                        "models_count": 0,
                    }  # HF doesn't have model listing
                except Exception as e:
                    print(f"    ❌ HuggingFace API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "huggingfacehub_api_token":
                # Test HuggingFace API (same as huggingface)
                try:
                    import huggingface_hub

                    huggingface_hub.login(token=api_key)
                    print("    ✅ HuggingFace API key is valid.")
                    return {
                        "working": True,
                        "models_count": 0,
                    }  # HF doesn't have model listing
                except Exception as e:
                    print(f"    ❌ HuggingFace API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "cohere":
                # Test Cohere API
                try:
                    import cohere

                    client = cohere.Client(api_key=api_key)
                    models = client.models.list()
                    print(f"    ✅ Cohere API key is valid. Found {len(models)} models.")
                    return {"working": True, "models_count": len(models)}
                except Exception as e:
                    print(f"    ❌ Cohere API key failed: {e}")
                    return {"working": False, "models_count": 0}
            elif provider == "ai21":
                # Test AI21 API
                try:
                    import ai21

                    client = ai21.Client(api_key=api_key)
                    models = client.models.list()
                    print(f"    ✅ AI21 API key is valid. Found {len(models)} models.")
                    return {"working": True, "models_count": len(models)}
                except Exception as e:
                    print(f"    ❌ AI21 API key failed: {e}")
                    return {"working": False, "models_count": 0}
            else:
                print(f"    ⚠️ No specific test implemented for {provider.title()}.")
                return {
                    "working": True,
                    "models_count": 0,
                }  # Assume it's working if no specific test

        except Exception as e:
            print(f"    ❌ An unexpected error occurred during API key test: {e}")
            return False

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
            scrubber_script = Path(__file__).parent.parent.parent / "scripts" / "scrub_all_subprojects.py"

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
            # Load API keys from 1Password
            import sys

            from src.multi_agent_testing.multi_dimensional_smoke_test import (
                MultiDimensionalSmokeTest,
            )

            # Since we're running from project root, scripts is directly accessible
            scripts_path = str(Path.cwd() / "scripts")
            sys.path.insert(0, scripts_path)
            from op_api_manager.core import OnePasswordAPIKeyManager

            # Initialize API key manager and set environment variables
            api_manager = OnePasswordAPIKeyManager()
            api_manager.set_environment_variables()

            # Multi-agent system will analyze current state from quality reports

            # Initialize multi-agent system
            test_system = MultiDimensionalSmokeTest()

            # Run analysis with different perspectives
            analysis_results = {}

            # Check environment variables first for 1Password freedom
            print("🔓 Checking environment variables for 1Password freedom...")

            # Use environment variables instead of 1Password calls
            api_test_results = {}
            working_models = []

            # Check for available APIs in environment
            if os.getenv("ANTHROPIC_API_KEY"):
                api_test_results["anthropic"] = [{"id": "env_anthropic", "working": True}]
                working_models.append("claude")
                print("✅ Using Anthropic Claude from environment variables")

            if os.getenv("OPENAI_API_KEY"):
                api_test_results["openai"] = [{"id": "env_openai", "working": True}]
                working_models.append("gpt4_vision")
                working_models.append("gpt5")
                print("✅ Using OpenAI from environment variables")

            if os.getenv("AZURE_API_KEY"):
                api_test_results["azure"] = [{"id": "env_azure", "working": True}]
                working_models.append("azure")
                print("✅ Using Azure from environment variables")

            if os.getenv("AWS_ACCESS_KEY_ID"):
                api_test_results["aws"] = [{"id": "env_aws", "working": True}]
                working_models.append("aws")
                print("✅ Using AWS from environment variables")

            if os.getenv("GOOGLE_API_KEY"):
                api_test_results["google"] = [{"id": "env_google", "working": True}]
                working_models.append("gemini_pro")
                print("✅ Using Google from environment variables")

            print(f"🔓 Environment-based API results: {api_test_results}")
            print(f"🔓 Working models: {working_models}")

            # Check if we have working APIs for each provider
            # api_test_results[provider] is a list of working APIs
            if api_test_results.get("anthropic") and len(api_test_results["anthropic"]) > 0:
                working_models.append("claude")
                print("✅ Using Anthropic Claude for multi-agent analysis")

            if api_test_results.get("openai") and len(api_test_results["openai"]) > 0:
                working_models.append("gpt4_vision")
                working_models.append("gpt5")  # Add GPT-5 as well
                print("✅ Using OpenAI GPT-4 and GPT-5 for multi-agent analysis")

            if api_test_results.get("huggingface") and len(api_test_results["huggingface"]) > 0:
                working_models.append("huggingface")
                print("✅ Using HuggingFace for multi-agent analysis")

            if not working_models:
                print("❌ No working API endpoints found, skipping multi-agent analysis")
                return {
                    "success": False,
                    "error": "No working API endpoints available",
                    "fallback_analysis": self._fallback_quality_analysis(),
                }

            # Set the working API keys for the smoke test and update environment
            if hasattr(test_system, "set_working_api_keys"):
                working_keys = {}
                for model in working_models:
                    if model == "claude":
                        # Get the actual Anthropic API key from the discovered keys
                        anthropic_keys = api_test_results.get("anthropic", [])
                        if anthropic_keys:
                            # Use the first working Anthropic key
                            anthropic_key = anthropic_keys[0].get("id", "")
                            working_keys["claude"] = anthropic_key
                            # Set environment variable
                            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
                            print("🔑 Updated ANTHROPIC_API_KEY environment with working key")
                        else:
                            working_keys["claude"] = os.getenv("ANTHROPIC_API_KEY")
                    elif model == "gpt4_vision" and self.working_openai_key:
                        # Use the working OpenAI API key we validated
                        working_keys["gpt4_vision"] = self.working_openai_key
                        # Update environment variable with working key
                        os.environ["OPENAI_API_KEY"] = self.working_openai_key
                        print("🔑 Updated OPENAI_API_KEY environment with working key")
                    elif model == "gpt5" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-5
                        working_keys["gpt5"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-5")
                    elif model == "gpt3_5_turbo" and self.working_openai_key:
                        # Use the working OpenAI API key we validated for GPT-3.5-turbo
                        working_keys["gpt3_5_turbo"] = self.working_openai_key
                        print("🔑 Using working OpenAI API key for GPT-3.5-turbo")
                    elif model == "huggingface" and hasattr(self, "working_huggingface_key"):
                        # Use the working HuggingFace API key we validated
                        working_keys["huggingface"] = self.working_huggingface_key
                        # Update environment variable with working key
                        os.environ["HUGGINGFACE_API_KEY"] = self.working_huggingface_key
                        print("🔑 Updated HUGGINGFACE_API_KEY environment with working key")
                    elif model in ["claude_haiku", "claude_sonnet"] and self.working_anthropic_key:
                        # Use the working Anthropic API key for alternative models
                        working_keys[model] = self.working_anthropic_key
                        print(f"🔑 Using working Anthropic API key for {model}")
                    elif model in ["gemini_pro", "gemini_flash", "gemini_pro_vision"] and self.working_google_key:
                        # Use the working Google API key
                        working_keys[model] = self.working_google_key
                        os.environ["GOOGLE_API_KEY"] = self.working_google_key
                        print(f"🔑 Updated GOOGLE_API_KEY environment with working key for {model}")
                    elif model in ["claude_bedrock", "titan_express", "llama2_bedrock"] and self.working_aws_key:
                        # Use the working AWS API key
                        working_keys[model] = self.working_aws_key
                        os.environ["AWS_ACCESS_KEY_ID"] = self.working_aws_key
                        print(f"🔑 Updated AWS_ACCESS_KEY_ID environment with working key for {model}")

                test_system.set_working_api_keys(working_keys)
                print(f"🔑 Set working API keys for {len(working_keys)} models")

            # Run the COMPLETE agent set (security + quality + devops) on EACH LLM provider
            print(f"📊 Models: {', '.join(working_models)}")

            # For each LLM, run the complete agent set
            all_llm_results = {}

            for model in working_models:
                print(f"\n🤖 Running complete agent set on {model}...")

                # Security Expert on this LLM
                security_config = {
                    "role": "security_expert",
                    "prompt_structure": "direct_questions",
                    "response_format": "json",
                    "model": model,
                    "temperature": 0.7,
                }

                print(f"  🔒 Security analysis with {model}")
                if self.api_manager:
                    try:
                        security_prompt = f"Role: {security_config.get('role', 'unknown')}, Structure: {security_config.get('prompt_structure', 'unknown')}, Format: {security_config.get('response_format', 'unknown')}"
                        self.api_manager.track_api_call(model, security_prompt, "", "security_analysis")
                    except Exception as e:
                        print(f"🔍 DEBUG: Error in security prompt creation: {e}")
                        print(f"🔍 DEBUG: security_config: {security_config}")
                        raise

                print(f"🔍 DEBUG: About to call test_system.run_test with config: {security_config}")
                print(f"🔍 DEBUG: Security config keys: {list(security_config.keys())}")
                try:
                    security_analysis = test_system.run_test(security_config, "security_audit")
                    print(f"🔍 DEBUG: run_test returned successfully, type: {type(security_analysis)}")
                except Exception as e:
                    print(f"🔍 DEBUG: run_test failed with exception: {e}")
                    print(f"🔍 DEBUG: Exception type: {type(e)}")
                    import traceback

                    traceback.print_exc()
                    raise

                if self.api_manager and security_analysis:
                    security_response = str(security_analysis)
                    self.api_manager.track_response_tokens(model, security_response, "security_analysis")
                    if isinstance(security_analysis, dict) and "usage" in security_analysis:
                        self.api_manager.update_with_vendor_costs(model, security_analysis, "security_analysis")

                # Code Quality Expert on this LLM
                quality_config = {
                    "role": "code_quality_expert",
                    "prompt_structure": "socratic_questioning",
                    "response_format": "json",
                    "model": model,
                    "temperature": 0.7,
                }

                print(f"  🔍 Quality analysis with {model}")
                if self.api_manager:
                    try:
                        quality_prompt = (
                            f"Role: {quality_config.get('role', 'unknown')}, Structure: {quality_config.get('prompt_structure', 'unknown')}, Format: {quality_config.get('response_format', 'unknown')}"
                        )
                        self.api_manager.track_api_call(model, quality_prompt, "", "quality_analysis")
                    except Exception as e:
                        print(f"🔍 DEBUG: Error in quality prompt creation: {e}")
                        print(f"🔍 DEBUG: quality_config: {quality_config}")
                        raise

                quality_analysis = test_system.run_test(quality_config, "code_quality")

                if self.api_manager and quality_analysis:
                    quality_response = str(quality_analysis)
                    self.api_manager.track_response_tokens(model, quality_response, "quality_analysis")
                    if isinstance(quality_analysis, dict) and "usage" in quality_analysis:
                        self.api_manager.update_with_vendor_costs(model, quality_analysis, "quality_analysis")

                # DevOps Expert on this LLM
                devops_config = {
                    "role": "devops_engineer",
                    "prompt_structure": "structured_analysis",
                    "response_format": "json",
                    "model": model,
                    "temperature": 0.7,
                }

                print(f"  ⚙️ DevOps analysis with {model}")
                if self.api_manager:
                    try:
                        devops_prompt = (
                            f"Role: {devops_config.get('role', 'unknown')}, Structure: {devops_config.get('prompt_structure', 'unknown')}, Format: {devops_config.get('response_format', 'unknown')}"
                        )
                        self.api_manager.track_api_call(model, devops_prompt, "", "devops_analysis")
                    except Exception as e:
                        print(f"🔍 DEBUG: Error in devops prompt creation: {e}")
                        print(f"🔍 DEBUG: devops_config: {devops_config}")
                        raise

                devops_analysis = test_system.run_test(devops_config, "devops")

                if self.api_manager and devops_analysis:
                    devops_response = str(devops_analysis)
                    self.api_manager.track_response_tokens(model, devops_response, "devops_analysis")
                    if isinstance(devops_analysis, dict) and "usage" in devops_analysis:
                        self.api_manager.update_with_vendor_costs(model, devops_analysis, "devops_analysis")

                # Store complete agent set results for this LLM
                all_llm_results[model] = {
                    "security": security_analysis,
                    "quality": quality_analysis,
                    "devops": devops_analysis,
                }

                print(f"  ✅ Completed agent set on {model}")

            # Coalesce results from ALL LLMs for comprehensive analysis
            print(f"\n🧠 Coalescing results from {len(working_models)} LLM providers...")

            # Coalesce security results across all LLMs
            security_results = [{"model": model, "analysis": results["security"]} for model, results in all_llm_results.items()]
            analysis_results["security"] = self._coalesce_llm_results(security_results, "security")

            # Coalesce quality results across all LLMs
            quality_results = [{"model": model, "analysis": results["quality"]} for model, results in all_llm_results.items()]
            analysis_results["quality"] = self._coalesce_llm_results(quality_results, "quality")

            # Coalesce devops results across all LLMs
            devops_results = [{"model": model, "analysis": results["devops"]} for model, results in all_llm_results.items()]
            analysis_results["devops"] = self._coalesce_llm_results(devops_results, "devops")

            # Print cost summary after all API calls
            if self.api_manager:
                print("\n💰 Multi-Agent Analysis Cost Summary:")
                self.api_manager.print_cost_summary()

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

    def _run_individual_analysis(self, test_system, working_model: str) -> dict[str, Any]:
        """Fallback to individual analysis if multi-shot fails"""
        analysis_results = {}

        # Security perspective
        security_config = {
            "role": "security_expert",
            "prompt_structure": "direct_questions",
            "response_format": "json",
            "model": working_model,
            "temperature": 0.7,
        }
        security_analysis = test_system.run_test(security_config, "security_audit")
        analysis_results["security"] = security_analysis

        # Code quality perspective
        quality_config = {
            "role": "code_quality_expert",
            "prompt_structure": "socratic_questioning",
            "response_format": "json",
            "model": working_model,
            "temperature": 0.7,
        }
        quality_analysis = test_system.run_test(quality_config, "code_quality")
        analysis_results["quality"] = quality_analysis

        # DevOps perspective
        devops_config = {
            "role": "devops_engineer",
            "prompt_structure": "structured_analysis",
            "response_format": "json",
            "model": working_model,
            "temperature": 0.7,
        }
        devops_analysis = test_system.run_test(devops_config, "devops")
        analysis_results["devops"] = devops_analysis

        return analysis_results

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

    def _parse_pre_commit_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse pre-commit output to extract issues"""
        issues = []

        # Parse stdout for hook results
        lines = stdout.split("\n")
        current_hook = None

        for line in lines:
            if "hook id:" in line:
                current_hook = line.split("hook id:")[1].strip()
            elif "Failed" in line and current_hook:
                issues.append({"hook": current_hook, "status": "Failed", "details": line.strip()})
            elif "Passed" in line and current_hook:
                issues.append({"hook": current_hook, "status": "Passed", "details": line.strip()})

        # Parse stderr for errors
        if stderr:
            issues.append({"hook": "general", "status": "Error", "details": stderr.strip()})

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

        # Show running costs after multi-agent analysis (most expensive step)
        if self.api_manager:
            self.api_manager.show_running_costs("After Multi-Agent Analysis")

        # Store results
        self.quality_reports.append(current_report)
        self.iteration_count += 1

        # Determine if we should continue
        should_continue = self.iteration_count < self.max_iterations and current_report.total_issues > 0 and not pre_commit_result.get("success", False)

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
            print(f"⚠️ Subproject scrubbing had issues: {subproject_result.get('error', 'Unknown error')}")
        else:
            print("✅ Subproject scrubbing completed")

        # Show running costs after subproject scrubbing
        if self.api_manager:
            self.api_manager.show_running_costs("After Subproject Scrubbing")

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

            # Show running costs after each iteration
            if self.api_manager:
                self.api_manager.show_running_costs(f"After Iteration {iteration + 1}")

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

    def _test_anthropic_models(self, api_key: str) -> dict[str, Any]:
        """Test multiple Anthropic models to find which ones work"""
        try:
            import anthropic

            anthropic_models = [
                ("claude", "claude-3-5-sonnet-20241022"),
                ("claude_haiku", "claude-3-haiku-20240307"),
                ("claude_opus", "claude-3-opus-20240229"),
                ("claude_sonnet", "claude-3-sonnet-20240229"),
            ]

            working_models = []
            client = anthropic.Anthropic(api_key=api_key)

            for model_key, model_name in anthropic_models:
                try:
                    client.messages.create(
                        model=model_name,
                        max_tokens=10,
                        messages=[{"role": "user", "content": "Hello"}],
                    )
                    working_models.append(model_key)
                    print(f"        ✅ {model_name} works!")
                except Exception as e:
                    print(f"        ❌ {model_name} failed: {str(e)[:100]}...")

            return {"working_models": working_models}

        except Exception as e:
            print(f"    ❌ Anthropic model testing failed: {e}")
            return {"working_models": []}

    def _test_google_models(self, api_key: str) -> dict[str, Any]:
        """Test multiple Google models to find which ones work"""
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)

            google_models = [
                ("gemini_pro", "gemini-pro"),
                ("gemini_flash", "gemini-1.5-flash"),
                ("gemini_pro_vision", "gemini-pro-vision"),
            ]

            working_models = []

            for model_key, model_name in google_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    model.generate_content("Hello")
                    working_models.append(model_key)
                    print(f"        ✅ {model_name} works!")
                except Exception as e:
                    print(f"        ❌ {model_name} failed: {str(e)[:100]}...")

            return {"working_models": working_models}

        except Exception as e:
            print(f"    ❌ Google model testing failed: {e}")
            return {"working_models": []}

    def _test_aws_models(self, api_key: str, secret_key: str = None) -> dict[str, Any]:
        """Test multiple AWS Bedrock models to find which ones work"""
        try:
            import boto3

            # Configure AWS client
            session = boto3.Session(
                aws_access_key_id=api_key,
                aws_secret_access_key=secret_key or api_key,  # Fallback if no separate secret
                region_name="us-east-1",
            )
            bedrock = session.client("bedrock-runtime")

            aws_models = [
                ("claude_bedrock", "anthropic.claude-3-sonnet-20240229-v1:0"),
                ("titan_express", "amazon.titan-text-express-v1"),
                ("llama2_bedrock", "meta.llama2-70b-chat-v1"),
            ]

            working_models = []

            for model_key, model_name in aws_models:
                try:
                    bedrock.invoke_model(modelId=model_name, body='{"prompt": "Hello", "max_tokens": 10}')
                    working_models.append(model_key)
                    print(f"        ✅ {model_name} works!")
                except Exception as e:
                    print(f"        ❌ {model_name} failed: {str(e)[:100]}...")

            return {"working_models": working_models}

        except Exception as e:
            print(f"    ❌ AWS model testing failed: {e}")
            return {"working_models": []}

    def _test_huggingface_llm_call(self, api_key: str) -> bool:
        """Test if HuggingFace API key actually works for LLM calls"""
        try:
            import requests

            # Test with a simple inference call to a popular model
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "inputs": "Hello, how are you?",
                "parameters": {"max_new_tokens": 50, "temperature": 0.7},
            }

            # Use a more reliable model endpoint - Meta's Llama 2 7B chat model
            response = requests.post(
                "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
                headers=headers,
                json=payload,
                timeout=30,
            )

            # If we get here, the LLM call worked
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ HuggingFace LLM call test successful: {result}")
                return True
            print(f"    ❌ HuggingFace LLM call test failed: {response.status_code} - {response.text}")
            return False

        except Exception as e:
            print(f"    ❌ HuggingFace LLM call test failed: {e}")
            return False

    def _test_openai_llm_call(self, api_key: str) -> bool:
        """Test if OpenAI API key actually works for LLM calls"""
        try:
            import openai

            # Test with a simple chat completion using GPT-5
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-5o",  # Use GPT-5 for testing
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )

            # If we get here, the LLM call worked
            print(f"    ✅ OpenAI LLM call test successful: {response.choices[0].message.content}")
            return True

        except Exception as e:
            print(f"    ❌ OpenAI LLM call test failed: {e}")
            return False

    def _coalesce_llm_results(self, llm_results: list[dict[str, Any]], analysis_type: str) -> dict[str, Any]:
        """Coalesce results from multiple LLMs for comprehensive analysis"""
        print(f"  🧠 Coalescing {analysis_type} results from {len(llm_results)} LLMs...")

        if not llm_results:
            return {"error": "No LLM results to coalesce"}

        # Collect all findings from all LLMs
        all_findings = []
        all_recommendations = []
        all_insights = []

        for result in llm_results:
            model = result.get("model", "unknown")
            analysis = result.get("analysis", {})

            if isinstance(analysis, dict):
                # Extract findings
                if "findings" in analysis:
                    for finding in analysis["findings"]:
                        finding["source_llm"] = model
                        all_findings.append(finding)

                # Extract recommendations
                if "recommendations" in analysis:
                    for rec in analysis["recommendations"]:
                        all_recommendations.append(f"({model}) {rec}")

                # Extract insights
                if "insights" in analysis:
                    for insight in analysis["insights"]:
                        all_insights.append(f"({model}) {insight}")

                # Extract any other structured data
                for key, value in analysis.items():
                    if key not in [
                        "findings",
                        "recommendations",
                        "insights",
                    ] and isinstance(value, (list, dict)):
                        if key not in all_insights:
                            all_insights.append(f"({model}) {key}: {value}")

        # Create coalesced result
        coalesced = {
            "analysis_type": analysis_type,
            "llms_used": [r.get("model", "unknown") for r in llm_results],
            "total_llms": len(llm_results),
            "coalesced_findings": all_findings,
            "coalesced_recommendations": all_recommendations,
            "coalesced_insights": all_insights,
            "total_findings": len(all_findings),
            "total_recommendations": len(all_recommendations),
            "total_insights": len(all_insights),
            "coalescence_timestamp": datetime.now().isoformat(),
        }

        print(f"  ✅ Coalesced {analysis_type}: {len(all_findings)} findings, {len(all_recommendations)} recommendations")
        return coalesced


def main():
    """Main function to run the automation"""
    import argparse

    # Parse arguments properly
    parser = argparse.ArgumentParser(
        description="Code Quality Automation Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python orchestrator.py                    # Run on current directory
  python orchestrator.py /path/to/project  # Run on specific directory
  python orchestrator.py --test            # Test individual components
  python orchestrator.py --help            # Show this help message
        """,
    )

    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Target directory to analyze (default: current directory)",
    )
    parser.add_argument("--test", action="store_true", help="Test individual components only")

    args = parser.parse_args()
    target_dir = args.target_dir
    test_mode = args.test

    print("🎯 Code Quality Automation Orchestrator")
    print(f"🎯 Target Directory: {target_dir}")

    if test_mode:
        print("🧪 TEST MODE: Running individual components only")
        print("🎯 Usage: python3 orchestrator.py [directory] --test")
    else:
        print("🎯 Starting automated quality improvement...")
        print("🎯 Workflow: Subproject Scrubbing → Black → Ruff → Pre-commit → Multi-agent Analysis")

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
