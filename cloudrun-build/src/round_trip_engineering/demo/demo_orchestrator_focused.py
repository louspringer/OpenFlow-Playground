#!/usr/bin/env python3
"""
Focused Demo Orchestrator - Lean orchestrator using focused modules.

Purpose: Orchestrate demo workflows using focused modules.
This is now a lean orchestrator that delegates to focused modules.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from .demo_file_generator import DemoFileGenerator
from .demo_executor import DemoExecutor
from .demo_design_spec import DemoDesignSpec

# Configure logging
logger = logging.getLogger(__name__)


class DemoOrchestrator(BaseReflectiveModule):
    """
    Focused Demo Orchestrator - Now a lean orchestrator using focused modules.

    This module follows Reflective Module principles:
    - Single responsibility: Demo orchestration only
    - Self-monitoring: Tracks demo execution status
    - Clear boundaries: Interfaces with focused modules
    - Testable: Can be tested in isolation
    - Size compliant: Under 200 lines
    """

    def __init__(self) -> None:
        """Initialize the focused demo orchestrator."""
        super().__init__()
        self.file_generator = DemoFileGenerator()
        self.executor = DemoExecutor()
        self.design_spec = DemoDesignSpec()
        self.demo_results: Dict[str, Any] = {}
        self.current_demo_step = "idle"
        self.demo_start_time: Optional[float] = None

        logger.info("🎯 Focused Demo Orchestrator initialized")

    async def get_module_capabilities(self) -> List[Dict[str, Any]]:
        """Get module capabilities."""
        return [
            {"name": "basic_demo", "description": "Run basic demo workflow", "async": True, "parameters": []},
            {"name": "advanced_demo", "description": "Run advanced demo workflow", "async": True, "parameters": []},
            {"name": "performance_demo", "description": "Run performance demo workflow", "async": True, "parameters": []},
            {"name": "get_demo_status", "description": "Get current demo status", "async": True, "parameters": []},
        ]

    async def run_basic_demo(self) -> Dict[str, Any]:
        """Run basic demo workflow."""
        self.current_demo_step = "basic_demo"
        self.demo_start_time = asyncio.get_event_loop().time()

        try:
            logger.info("🔄 Starting basic demo workflow")

            # Generate demo file
            demo_content = self.file_generator.create_basic_demo_file()

            # Execute demo
            result = await self.executor.execute_basic_demo(demo_content)

            self.demo_results["basic_demo"] = result
            logger.info("✅ Basic demo workflow completed")
            return result

        except Exception as e:
            result = {"status": "failed", "error": str(e), "round_trip_successful": False}
            self.demo_results["basic_demo"] = result
            logger.error(f"❌ Basic demo workflow failed: {e}")
            return result
        finally:
            self.current_demo_step = "idle"

    async def run_advanced_demo(self) -> Dict[str, Any]:
        """Run advanced demo workflow."""
        self.current_demo_step = "advanced_demo"
        self.demo_start_time = asyncio.get_event_loop().time()

        try:
            logger.info("🔄 Starting advanced demo workflow")

            # Generate demo file
            demo_content = self.file_generator.create_advanced_demo_file()

            # Execute demo
            result = await self.executor.execute_advanced_demo(demo_content)

            self.demo_results["advanced_demo"] = result
            logger.info("✅ Advanced demo workflow completed")
            return result

        except Exception as e:
            result = {"status": "failed", "error": str(e), "round_trip_successful": False}
            self.demo_results["advanced_demo"] = result
            logger.error(f"❌ Advanced demo workflow failed: {e}")
            return result
        finally:
            self.current_demo_step = "idle"

    async def run_performance_demo(self) -> Dict[str, Any]:
        """Run performance demo workflow."""
        self.current_demo_step = "performance_demo"
        self.demo_start_time = asyncio.get_event_loop().time()

        try:
            logger.info("🔄 Starting performance demo workflow")

            # Generate demo file
            demo_content = self.file_generator.create_performance_demo_file(1)

            # Execute demo
            result = await self.executor.execute_performance_demo(demo_content)

            self.demo_results["performance_demo"] = result
            logger.info("✅ Performance demo workflow completed")
            return result

        except Exception as e:
            result = {"status": "failed", "error": str(e), "round_trip_successful": False, "components_count": 0, "success_rate": 0.0}
            self.demo_results["performance_demo"] = result
            logger.error(f"❌ Performance demo workflow failed: {e}")
            return result
        finally:
            self.current_demo_step = "idle"

    async def get_demo_status(self) -> Dict[str, Any]:
        """Get current demo status."""
        execution_status = self.executor.get_execution_status()

        return {"current_demo_step": self.current_demo_step, "demo_start_time": self.demo_start_time, "execution_status": execution_status, "demo_results": self.demo_results}

    def _create_basic_design_spec(self) -> Dict[str, Any]:
        """Create a basic design specification."""
        return self.design_spec.create_basic_design_spec()

    async def _validate_vocabulary_alignment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate vocabulary alignment."""
        return {
            "valid": analysis_results.get("success", False),
            "score": 0.8 if analysis_results.get("success", False) else 0.0,
            "issues": [] if analysis_results.get("success", False) else ["Analysis failed"],
        }

    def get_module_status(self) -> Dict[str, Any]:
        """Get module status for RM compliance."""
        return {"name": "DemoOrchestrator", "status": "active", "current_step": self.current_demo_step, "demo_count": len(self.demo_results)}

    def cleanup(self) -> None:
        """Cleanup method for RM compliance."""
        self.file_generator.clear_generated_files()
        self.executor.clear_execution_results()
        self.design_spec.clear_specs()
        self.demo_results.clear()
        self.current_demo_step = "idle"
        self.demo_start_time = None
        logger.info("🧹 Demo Orchestrator cleaned up")
