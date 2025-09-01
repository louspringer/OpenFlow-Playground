#!/usr/bin/env python3
"""
Ghostbusters Availability Test - Check what capabilities are actually available and working
Uses clean external service interfaces instead of reaching inside implementations
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List

import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GhostbustersAvailabilityTest:
    """Test what Ghostbusters capabilities are actually available and working
    Uses project model and clean service interfaces instead of reaching inside implementations
    """

    def __init__(self, project_path: str = ".") -> None:
        self.project_path = Path(project_path)
        self.results: Dict[str, Any] = {}
        self.project_model = self._load_project_model()

    def _load_project_model(self) -> dict:
        """Load the project model registry for capability discovery"""
        try:
            model_path = Path(self.project_path) / "project_model_registry.json"
            if model_path.exists():
                with open(model_path, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Project model not found at {model_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading project model: {e}")
            return {}

    async def test_project_model_availability(self) -> Dict[str, Any]:
        """Test if project model is available and contains Ghostbusters configuration"""
        logger.info("🔍 Testing project model availability...")

        try:
            if not self.project_model:
                return {
                    "available": False,
                    "message": "Project model not loaded",
                    "ghostbusters_domain": None,
                }

            ghostbusters_domain = self.project_model.get("domains", {}).get("ghostbusters", {})
            if not ghostbusters_domain:
                return {
                    "available": False,
                    "message": "Ghostbusters domain not found in project model",
                    "ghostbusters_domain": None,
                }

            return {
                "available": True,
                "message": "Project model available with Ghostbusters configuration",
                "ghostbusters_domain": ghostbusters_domain,
                "patterns": ghostbusters_domain.get("patterns", []),
                "content_indicators": ghostbusters_domain.get("content_indicators", []),
                "requirements": ghostbusters_domain.get("requirements", []),
            }

        except Exception as e:
            logger.error(f"❌ Project model test failed: {e}")
            return {
                "available": False,
                "message": f"Error testing project model: {e}",
                "ghostbusters_domain": None,
            }

    async def test_multi_perspective_service(self) -> Dict[str, Any]:
        """Test the multi-perspective service functionality"""
        logger.info("🔍 Testing multi-perspective service...")

        try:
            from .multi_perspective_service import MultiPerspectiveService

            service = MultiPerspectiveService(str(self.project_path))

            # Test service health
            is_healthy = await service.is_healthy()

            # Test capabilities
            capabilities = await service.get_service_capabilities()

            # Test available perspectives
            perspectives = await service.get_available_perspectives()

            return {
                "available": True,
                "healthy": is_healthy,
                "capabilities_count": len(capabilities),
                "perspectives_count": len(perspectives),
                "perspectives": perspectives,
                "capabilities": [cap.name for cap in capabilities if cap.available],
            }

        except Exception as e:
            logger.error(f"❌ Multi-perspective service test failed: {e}")
            return {"available": False, "error": str(e)}

    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive availability test using clean service interfaces"""
        logger.info("🚀 Starting comprehensive Ghostbusters availability test...")
        logger.info("🔍 Using clean service interfaces - no implementation probing")

        self.results = {
            "timestamp": asyncio.get_event_loop().time(),
            "project_path": str(self.project_path),
            "project_model_test": await self.test_project_model_availability(),
            "multi_perspective_test": await self.test_multi_perspective_service(),
        }

        # Extract key information from tests
        project_model_test = self.results["project_model_test"]
        multi_perspective_test = self.results["multi_perspective_test"]

        if not project_model_test.get("available", False):
            # Project model not available
            self.results["summary"] = {
                "project_model_working": False,
                "multi_perspective_available": False,
                "multi_agent_available": False,
                "message": "Project model not available - cannot determine service availability",
            }
        elif not multi_perspective_test.get("available", False):
            # Multi-perspective service not working
            self.results["summary"] = {
                "project_model_working": True,
                "multi_perspective_available": False,
                "multi_agent_available": False,
                "message": "Project model working but multi-perspective service not available",
            }
        else:
            # Both working
            multi_perspective_available = multi_perspective_test.get("healthy", False)
            perspectives_count = multi_perspective_test.get("perspectives_count", 0)
            capabilities_count = multi_perspective_test.get("capabilities_count", 0)

            # Check project model for multi-agent requirements
            ghostbusters_domain = project_model_test.get("ghostbusters_domain", {})
            requirements = ghostbusters_domain.get("requirements", [])
            multi_agent_requirements = [req for req in requirements if "multi-agent" in req.lower() or "langchain" in req.lower() or "langgraph" in req.lower()]
            multi_agent_available = len(multi_agent_requirements) > 0

            self.results["summary"] = {
                "project_model_working": True,
                "multi_perspective_available": multi_perspective_available,
                "multi_agent_available": multi_agent_available,
                "perspectives_count": perspectives_count,
                "capabilities_count": capabilities_count,
                "multi_agent_requirements": multi_agent_requirements,
                "message": f"Project model working - {perspectives_count} perspectives available, {capabilities_count} capabilities, multi-agent: {'available' if multi_agent_available else 'not available'}",
            }

        logger.info("✅ Comprehensive availability test completed")
        return self.results

    def get_status_message(self) -> str:
        """Get a human-readable status message based on test results"""
        if not self.results:
            return "Status: No availability test run yet"

        summary = self.results.get("summary", {})

        if not summary.get("project_model_working", False):
            return "Status: Project model not working - cannot determine service availability"

        # Check both dimensions
        multi_perspective_available = summary.get("multi_perspective_available", False)
        multi_agent_available = summary.get("multi_agent_available", False)

        if multi_perspective_available and multi_agent_available:
            # Both systems available
            perspectives_count = summary.get("perspectives_count", 0)
            capabilities_count = summary.get("capabilities_count", 0)
            return f"Status: Multi-perspective analysis + Multi-agent system available ({perspectives_count} perspectives, {capabilities_count} capabilities)"

        elif multi_perspective_available:
            # Only multi-perspective available
            perspectives_count = summary.get("perspectives_count", 0)
            capabilities_count = summary.get("capabilities_count", 0)
            return f"Status: Multi-perspective analysis system available ({perspectives_count} perspectives, {capabilities_count} capabilities) - Multi-agent system not available"

        elif multi_agent_available:
            # Only multi-agent available (unlikely but possible)
            multi_agent_reqs = summary.get("multi_agent_requirements", [])
            return f"Status: Multi-agent system available ({len(multi_agent_reqs)} requirements) - Multi-perspective analysis system not available"

        else:
            # Neither available
            return "Status: Neither multi-perspective analysis nor multi-agent system available - basic functionality only"


async def test_ghostbusters_availability(project_path: str = ".") -> Dict[str, Any]:
    """Convenience function to test Ghostbusters availability"""
    tester = GhostbustersAvailabilityTest(project_path)
    return await tester.run_comprehensive_test()


def get_ghostbusters_status(project_path: str = ".") -> str:
    """Get current Ghostbusters status without running full test"""
    # This would be a lightweight check using service interfaces
    return "Status: Multi-perspective and multi-agent system status unknown - run availability test for details"


if __name__ == "__main__":

    async def main():
        tester = GhostbustersAvailabilityTest()
        results = await tester.run_comprehensive_test()

        print("\n🎯 GHOSTBUSTERS AVAILABILITY TEST RESULTS")
        print("=" * 50)
        print(f"📊 Overall Status: {tester.get_status_message()}")

        summary = results["summary"]

        if summary.get("project_model_working", False):
            print(f"🔍 Project Model: ✅ Working")
            print(f"🎯 Multi-Perspective: {'Available' if summary['multi_perspective_available'] else 'Not Available'}")
            print(f"🚀 Multi-Agent: {'Available' if summary['multi_agent_available'] else 'Not Available'}")

            if summary.get("perspectives_count"):
                print(f"🔍 Perspectives: {summary['perspectives_count']} available")
            if summary.get("capabilities_count"):
                print(f"🔍 Capabilities: {summary['capabilities_count']} available")

            if summary.get("multi_agent_requirements"):
                print(f"📋 Multi-Agent Requirements: {len(summary['multi_agent_requirements'])} found")

            if summary["multi_perspective_available"] and summary["multi_agent_available"]:
                print("\n✅ Both multi-perspective analysis and multi-agent systems are available!")
            elif summary["multi_perspective_available"]:
                print("\n✅ Multi-perspective analysis system is available")
                print("❌ Multi-agent system is not available - basic functionality only")
            elif summary["multi_agent_available"]:
                print("\n✅ Multi-agent system is available")
                print("❌ Multi-perspective analysis system is not available")
            else:
                print("\n❌ Neither system is available - basic functionality only")
        else:
            print(f"🔍 Project Model: ❌ Not Working")
            print(f"🔍 Message: {summary.get('message', 'Unknown error')}")
            print("\n❌ Cannot determine service availability - project model needs to be fixed")

    asyncio.run(main())
