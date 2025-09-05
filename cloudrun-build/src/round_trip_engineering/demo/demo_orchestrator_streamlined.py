#!/usr/bin/env python3
"""
Round-Trip Engineering Demo Orchestrator - BEAST MODE STREAMLINED

A Reflective Module that orchestrates the demo workflow with RM compliance.
Streamlined to meet 200-line limit through focused delegation.
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from ..core.round_trip_system import RoundTripSystem
from ..core.model_manager import ModelManager
from ..core.vocabulary_aligner import VocabularyAligner
from .demo_design_specs import DemoDesignSpecs
from .demo_executor import DemoExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DemoOrchestrator(BaseReflectiveModule):
    """
    Demo Orchestrator - BEAST MODE STREAMLINED

    RM Compliance:
    - Single responsibility: Demo orchestration only
    - Self-monitoring: Health indicators and status tracking
    - Operational visibility: External interfaces for status
    - Architecture boundaries: Delegates to focused modules
    """

    def __init__(self) -> None:
        """Initialize the demo orchestrator with RM compliance."""
        super().__init__()
        self.round_trip_system = RoundTripSystem()
        self.model_manager = ModelManager()
        self.vocabulary_aligner = VocabularyAligner()
        self.design_specs = DemoDesignSpecs()
        self.executor = DemoExecutor(self.round_trip_system, self.design_specs)
        self.demo_results: Dict[str, Any] = {}
        self.current_demo_step = "idle"
        self.demo_start_time: Optional[float] = None
        self._health_indicators = {"status": "initialized", "error_count": 0}

        logger.info("🦁 BEAST MODE: Demo Orchestrator initialized with RM compliance")

    async def get_module_capabilities(self) -> List[Dict[str, Any]]:
        """Get module capabilities - RM compliance."""
        return [
            {
                "name": "demo_orchestration",
                "description": "Orchestrates round-trip engineering demos",
                "available": True,
                "version": "1.0.0",
            },
            {
                "name": "workflow_execution",
                "description": "Executes complete round-trip workflows",
                "available": True,
                "version": "1.0.0",
            },
            {
                "name": "result_analysis",
                "description": "Analyzes demo results and performance",
                "available": True,
                "version": "1.0.0",
            },
        ]

    async def get_module_status(self) -> Dict[str, Any]:
        """Get module status - RM compliance."""
        return {
            "status": "operational" if self._health_indicators["error_count"] == 0 else "degraded",
            "current_step": self.current_demo_step,
            "health_indicators": self._health_indicators,
            "capabilities": await self.get_module_capabilities(),
            "timestamp": time.time(),
        }

    async def is_healthy(self) -> bool:
        """Health check - RM compliance."""
        return self._health_indicators["error_count"] == 0

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get health indicators - RM compliance."""
        return self._health_indicators

    def _create_basic_design_spec(self) -> Dict[str, Any]:
        """Create basic design specification - RM compliance."""
        return self.design_specs.create_basic_design_spec()

    def _create_advanced_design_spec(self) -> Dict[str, Any]:
        """Create advanced design specification - RM compliance."""
        return self.design_specs.create_advanced_design_spec()

    def _create_performance_design_spec(self) -> Dict[str, Any]:
        """Create performance design specification - RM compliance."""
        return self.design_specs.create_performance_design_spec()

    async def run_basic_demo(self) -> Dict[str, Any]:
        """Run basic demo with RM compliance."""
        try:
            self._track_success()
            self.current_demo_step = "basic_demo"
            self.demo_start_time = time.time()

            logger.info("🦁 BEAST MODE: Starting basic demo")

            demo_file = self.executor.create_demo_python_file()
            self.demo_results = self.executor.execute_basic_demo(demo_file, self.demo_start_time)

            logger.info(f"✅ Basic demo completed in {self.demo_results.get('duration', 0):.2f}s")
            return self.demo_results

        except Exception as e:
            self._track_error(f"Basic demo failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    async def run_advanced_demo(self) -> Dict[str, Any]:
        """Run advanced demo with RM compliance."""
        try:
            self._track_success()
            self.current_demo_step = "advanced_demo"
            self.demo_start_time = time.time()

            logger.info("🦁 BEAST MODE: Starting advanced demo")

            demo_file = self.executor.create_demo_python_file()
            self.demo_results = self.executor.execute_advanced_demo(demo_file, self.demo_start_time)

            logger.info(f"✅ Advanced demo completed in {self.demo_results.get('duration', 0):.2f}s")
            return self.demo_results

        except Exception as e:
            self._track_error(f"Advanced demo failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    async def run_performance_demo(self) -> Dict[str, Any]:
        """Run performance demo with RM compliance."""
        try:
            self._track_success()
            self.current_demo_step = "performance_demo"
            self.demo_start_time = time.time()

            logger.info("🦁 BEAST MODE: Starting performance demo")

            demo_file = self.executor.create_demo_python_file()
            self.demo_results = self.executor.execute_performance_demo(demo_file, self.demo_start_time)

            logger.info(f"✅ Performance demo completed in {self.demo_results.get('duration', 0):.2f}s")
            return self.demo_results

        except Exception as e:
            self._track_error(f"Performance demo failed: {e}")
            logger.error(f"❌ Performance demo failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    def _track_success(self) -> None:
        """Track successful operations - RM compliance."""
        self._health_indicators["last_success"] = time.time()
        if "error_count" in self._health_indicators:
            self._health_indicators["error_count"] = max(0, self._health_indicators["error_count"] - 1)

    def _track_error(self, error_msg: str) -> None:
        """Track errors - RM compliance."""
        self._health_indicators["error_count"] = self._health_indicators.get("error_count", 0) + 1
        self._health_indicators["last_error"] = error_msg
        self._health_indicators["last_error_time"] = time.time()
        logger.error(f"❌ Demo Orchestrator error: {error_msg}")

    async def get_demo_status(self) -> Dict[str, Any]:
        """Get current demo status - RM compliance."""
        return {
            "current_step": self.current_demo_step,
            "is_running": self.current_demo_step != "idle",
            "success_rate": 1.0 if self._health_indicators["error_count"] == 0 else 0.5,
            "last_demo_results": self.demo_results,
            "timestamp": time.time(),
        }

    def __enter__(self):
        """Context manager entry - RM compliance."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - RM compliance."""
        if exc_type:
            self._track_error(f"Context manager error: {exc_val}")
        # Cleanup demo files
        demo_file = Path("demo_test_file.py")
        if demo_file.exists():
            demo_file.unlink()
