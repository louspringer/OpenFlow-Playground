#!/usr/bin/env python3
"""
Demo Executor - BEAST MODE EXTRACTED

Handles demo execution logic to maintain 200-line limit for orchestrator.
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DemoExecutor:
    """Handles demo execution with RM compliance."""

    def __init__(self, round_trip_system, design_specs):
        """Initialize demo executor."""
        self.round_trip_system = round_trip_system
        self.design_specs = design_specs

    def execute_basic_demo(self, demo_file: Path, start_time: float) -> Dict[str, Any]:
        """Execute basic demo workflow."""
        try:
            logger.info("🦁 BEAST MODE: Executing basic demo")

            results = self.round_trip_system.analyze_and_generate_code(demo_file)
            workflow_analysis = self.round_trip_system.get_workflow_analysis(demo_file)
            system_status = self.round_trip_system.get_system_status()

            demo_duration = time.time() - start_time
            return {
                "demo_type": "basic",
                "status": "success",
                "duration": demo_duration,
                "round_trip_successful": results.get("success", True),
                "workflow_analysis": workflow_analysis,
                "system_status": system_status,
                "components_count": 1,
                "timestamp": time.time(),
            }
        except Exception as e:
            logger.error(f"❌ Basic demo execution failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    def execute_advanced_demo(self, demo_file: Path, start_time: float) -> Dict[str, Any]:
        """Execute advanced demo workflow."""
        try:
            logger.info("🦁 BEAST MODE: Executing advanced demo")

            results = self.round_trip_system.analyze_and_generate_code(demo_file)

            demo_duration = time.time() - start_time
            return {"demo_type": "advanced", "status": "success", "duration": demo_duration, "round_trip_successful": results.get("success", True), "components_count": 2, "timestamp": time.time()}
        except Exception as e:
            logger.error(f"❌ Advanced demo execution failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    def execute_performance_demo(self, demo_file: Path, start_time: float) -> Dict[str, Any]:
        """Execute performance demo workflow."""
        try:
            logger.info("🦁 BEAST MODE: Executing performance demo")

            results = self.round_trip_system.analyze_and_generate_code(demo_file)

            # Check if results are valid for performance testing
            if hasattr(results, "__len__") and len(results) > 0:
                demo_duration = time.time() - start_time
                return {"demo_type": "performance", "status": "success", "duration": demo_duration, "performance_metrics": {"items_processed": len(results)}, "timestamp": time.time()}
            else:
                raise ValueError("Performance demo failed: invalid results format")

        except Exception as e:
            logger.error(f"❌ Performance demo execution failed: {e}")
            return {"status": "failed", "error": str(e), "timestamp": time.time()}

    def create_demo_python_file(self) -> Path:
        """Create a demo Python file for testing."""
        demo_content = '''#!/usr/bin/env python3
"""Demo Python file for round-trip engineering testing."""

class DemoClass:
    """A simple demo class."""
    
    def __init__(self, value: str):
        """Initialize with a value."""
        self.value = value
    
    def get_value(self) -> str:
        """Get the stored value."""
        return self.value
    
    def set_value(self, new_value: str) -> None:
        """Set a new value."""
        self.value = new_value
'''

        demo_file = Path("demo_test_file.py")
        demo_file.write_text(demo_content)
        return demo_file
