#!/usr/bin/env python3
"""
Main entry point for Kiro Agent
HTTP server with health endpoints and task coordination API
"""

import asyncio
import logging
import signal
import sys
import json
from pathlib import Path
from aiohttp import web, web_request
from aiohttp.web_response import Response

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agent_coordination.agent_coordinator import AgentCoordinator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


class KiroAgentServer:
    def __init__(self):
        self.coordinator = None
        self.app = web.Application()
        self.setup_routes()

    def setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get("/health", self.health_check)
        self.app.router.add_get("/ready", self.ready_check)
        self.app.router.add_get("/status", self.status_check)
        self.app.router.add_post("/tasks", self.submit_task)
        self.app.router.add_get("/tasks", self.list_tasks)
        self.app.router.add_get("/metrics", self.metrics)

    async def health_check(self, request: web_request.Request) -> Response:
        """Health check endpoint"""
        return web.json_response({"status": "healthy", "service": "kiro-agent", "coordinator_running": self.coordinator is not None})

    async def ready_check(self, request: web_request.Request) -> Response:
        """Readiness check endpoint"""
        if self.coordinator is None:
            return web.json_response({"status": "not_ready", "reason": "coordinator_not_started"}, status=503)

        return web.json_response({"status": "ready", "service": "kiro-agent", "coordinator_running": True})

    async def status_check(self, request: web_request.Request) -> Response:
        """Detailed status endpoint"""
        if self.coordinator is None:
            return web.json_response({"status": "not_started", "coordinator": None})

        return web.json_response(
            {"status": "running", "coordinator": {"registered_agents": len(self.coordinator.registered_agents), "active_tasks": len(self.coordinator.active_tasks), "stats": self.coordinator.stats}}
        )

    async def submit_task(self, request: web_request.Request) -> Response:
        """Submit a new task to the coordinator"""
        try:
            data = await request.json()
            task_id = f"task_{len(self.coordinator.active_tasks) + 1}"

            # Submit task to coordinator
            await self.coordinator.submit_task(
                task_type=data.get("type", "general"), description=data.get("description", "No description"), requirements=data.get("requirements", {}), deadline=data.get("deadline")
            )

            return web.json_response({"status": "submitted", "task_id": task_id, "message": "Task submitted successfully"})

        except Exception as e:
            logger.error(f"Error submitting task: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def list_tasks(self, request: web_request.Request) -> Response:
        """List all active tasks"""
        if self.coordinator is None:
            return web.json_response({"tasks": []})

        tasks = []
        for task_id, task in self.coordinator.active_tasks.items():
            tasks.append({"task_id": task_id, "type": task.task_type, "description": task.description, "status": task.status, "assigned_agent": task.assigned_agent})

        return web.json_response({"tasks": tasks})

    async def metrics(self, request: web_request.Request) -> Response:
        """Prometheus-style metrics endpoint"""
        if self.coordinator is None:
            return web.Response(text="# No metrics available\n")

        metrics_text = f"""# HELP kiro_agent_registered_agents Number of registered agents
# TYPE kiro_agent_registered_agents gauge
kiro_agent_registered_agents {len(self.coordinator.registered_agents)}

# HELP kiro_agent_active_tasks Number of active tasks
# TYPE kiro_agent_active_tasks gauge
kiro_agent_active_tasks {len(self.coordinator.active_tasks)}

# HELP kiro_agent_tasks_completed Total completed tasks
# TYPE kiro_agent_tasks_completed counter
kiro_agent_tasks_completed {self.coordinator.stats.get('tasks_completed', 0)}

# HELP kiro_agent_tasks_failed Total failed tasks
# TYPE kiro_agent_tasks_failed counter
kiro_agent_tasks_failed {self.coordinator.stats.get('tasks_failed', 0)}
"""
        return web.Response(text=metrics_text, content_type="text/plain")


async def main():
    """Main entry point"""
    logger.info("🚀 Starting Kiro Agent Server...")

    # Create server
    server = KiroAgentServer()

    # Create agent coordinator
    server.coordinator = AgentCoordinator()

    # Start the coordinator
    await server.coordinator.start()

    logger.info("✅ Kiro Agent started successfully!")
    logger.info("🌐 Starting HTTP server on port 8080...")

    # Start HTTP server
    runner = web.AppRunner(server.app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    logger.info("🎯 Kiro Agent is LIVE! Endpoints available:")
    logger.info("   Health: http://localhost:8080/health")
    logger.info("   Status: http://localhost:8080/status")
    logger.info("   Tasks:  http://localhost:8080/tasks")
    logger.info("   Metrics: http://localhost:8080/metrics")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Kiro Agent...")
        await runner.cleanup()
        await server.coordinator.stop()
        logger.info("✅ Kiro Agent stopped")


if __name__ == "__main__":
    asyncio.run(main())
