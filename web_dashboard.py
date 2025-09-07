#!/usr/bin/env python3
"""
Web Dashboard for Beast Mode Agent Collaboration Network

Provides a real-time web interface for monitoring agent discovery,
trust scores, health status, and message flow.

Usage:
    python web_dashboard.py [--port 8080]
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from aiohttp import web, WSMsgType
from aiohttp.web import WebSocketResponse
import aiohttp_cors

from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager
from beast_mode.health_monitor import HealthMonitor
from beast_mode.web_discovery import WebDiscoveryManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BeastModeDashboard:
    """Web dashboard for Beast Mode Agent Collaboration Network."""

    def __init__(self, port: int = 8080):
        self.port = port
        self.redis_manager = None
        self.discovery_manager = None
        self.help_manager = None
        self.health_monitor = None
        self.web_discovery = None
        self.websockets: List[WebSocketResponse] = []
        self.app = None

    async def initialize(self):
        """Initialize all components."""
        logger.info("Initializing Beast Mode Dashboard...")

        # Initialize Redis connection
        self.redis_manager = RedisConnectionManager()
        await self.redis_manager.connect()

        # Initialize discovery manager
        self.discovery_manager = AgentDiscoveryManager(agent_id="dashboard_agent", capabilities=["monitoring", "visualization"], redis_manager=self.redis_manager)

        # Initialize help system
        self.help_manager = HelpSystemManager(agent_id="dashboard_agent", capabilities=["monitoring", "visualization"], redis_manager=self.redis_manager, discovery_manager=self.discovery_manager)

        # Initialize health monitor
        self.health_monitor = HealthMonitor(redis_manager=self.redis_manager, registry=self.discovery_manager.registry)

        # Initialize web discovery
        self.web_discovery = WebDiscoveryManager(agent_id="dashboard_agent", capabilities=["monitoring", "visualization"], redis_manager=self.redis_manager)

        # Start health monitoring
        await self.health_monitor.start_monitoring(interval_seconds=10)

        # Start web discovery
        await self.web_discovery.start_discovery()

        logger.info("Dashboard initialized successfully")

    async def create_app(self):
        """Create the web application."""
        app = web.Application()

        # Configure CORS
        cors = aiohttp_cors.setup(app, defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*")})

        # Add routes
        app.router.add_get("/", self.index_handler)
        app.router.add_get("/api/agents", self.agents_handler)
        app.router.add_get("/api/health", self.health_handler)
        app.router.add_get("/api/discovery", self.discovery_handler)
        app.router.add_get("/api/trust-scores", self.trust_scores_handler)
        app.router.add_get("/api/messages", self.messages_handler)
        app.router.add_get("/ws", self.websocket_handler)

        # Add static files
        app.router.add_static("/", path="web_static", name="static")

        # Add CORS to all routes
        for route in list(app.router.routes()):
            cors.add(route)

        self.app = app
        return app

    async def index_handler(self, request):
        """Serve the main dashboard page."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Beast Mode Agent Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .card h3 { margin-top: 0; color: #2c3e50; }
                .status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
                .status.healthy { background: #d4edda; color: #155724; }
                .status.degraded { background: #fff3cd; color: #856404; }
                .status.unhealthy { background: #f8d7da; color: #721c24; }
                .agent-list { max-height: 300px; overflow-y: auto; }
                .agent-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
                .agent-item:last-child { border-bottom: none; }
                .trust-score { font-weight: bold; color: #27ae60; }
                .capabilities { font-size: 12px; color: #666; }
                .refresh-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
                .refresh-btn:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔥 Beast Mode Agent Dashboard</h1>
                    <p>Real-time monitoring of agent collaboration network</p>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h3>Agent Discovery</h3>
                        <div id="discovery-stats">Loading...</div>
                        <button class="refresh-btn" onclick="refreshData()">Refresh</button>
                    </div>
                    
                    <div class="card">
                        <h3>Health Status</h3>
                        <div id="health-stats">Loading...</div>
                    </div>
                    
                    <div class="card">
                        <h3>Trust Scores</h3>
                        <div id="trust-scores">Loading...</div>
                    </div>
                    
                    <div class="card">
                        <h3>Discovered Agents</h3>
                        <div id="agents-list" class="agent-list">Loading...</div>
                    </div>
                </div>
            </div>
            
            <script>
                let ws = null;
                
                function connectWebSocket() {
                    ws = new WebSocket(`ws://${window.location.host}/ws`);
                    
                    ws.onopen = function() {
                        console.log('WebSocket connected');
                    };
                    
                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        updateDashboard(data);
                    };
                    
                    ws.onclose = function() {
                        console.log('WebSocket disconnected, reconnecting...');
                        setTimeout(connectWebSocket, 3000);
                    };
                }
                
                function updateDashboard(data) {
                    if (data.discovery) {
                        document.getElementById('discovery-stats').innerHTML = `
                            <p><strong>Total Agents:</strong> ${data.discovery.total_agents}</p>
                            <p><strong>HTTP Agents:</strong> ${data.discovery.http_agents}</p>
                            <p><strong>mDNS Agents:</strong> ${data.discovery.mdns_agents}</p>
                            <p><strong>Discovery Running:</strong> ${data.discovery.discovery_running ? 'Yes' : 'No'}</p>
                        `;
                    }
                    
                    if (data.health) {
                        const healthClass = data.health.status === 'healthy' ? 'healthy' : 
                                          data.health.status === 'degraded' ? 'degraded' : 'unhealthy';
                        document.getElementById('health-stats').innerHTML = `
                            <p><strong>Overall Status:</strong> <span class="status ${healthClass}">${data.health.status.toUpperCase()}</span></p>
                            <p><strong>Health Percentage:</strong> ${data.health.health_percentage.toFixed(1)}%</p>
                            <p><strong>Healthy Agents:</strong> ${data.health.healthy_agents}/${data.health.total_agents}</p>
                        `;
                    }
                    
                    if (data.agents) {
                        const agentsHtml = data.agents.map(agent => `
                            <div class="agent-item">
                                <div>
                                    <strong>${agent.agent_id}</strong>
                                    <div class="capabilities">${agent.capabilities.join(', ')}</div>
                                </div>
                                <div class="trust-score">${agent.trust_score.toFixed(2)}</div>
                            </div>
                        `).join('');
                        document.getElementById('agents-list').innerHTML = agentsHtml;
                    }
                }
                
                function refreshData() {
                    fetch('/api/discovery').then(r => r.json()).then(updateDashboard);
                    fetch('/api/health').then(r => r.json()).then(updateDashboard);
                    fetch('/api/agents').then(r => r.json()).then(updateDashboard);
                }
                
                // Connect WebSocket and load initial data
                connectWebSocket();
                refreshData();
                
                // Refresh data every 30 seconds
                setInterval(refreshData, 30000);
            </script>
        </body>
        </html>
        """
        return web.Response(text=html, content_type="text/html")

    async def agents_handler(self, request):
        """Get discovered agents."""
        try:
            # Get agents from both discovery systems
            redis_agents = await self.discovery_manager.get_discovered_agents()
            web_agents = await self.web_discovery.get_discovered_agents()

            # Combine and deduplicate
            all_agents = {}
            for agent in redis_agents:
                all_agents[agent.agent_id] = {
                    "agent_id": agent.agent_id,
                    "capabilities": agent.capabilities,
                    "specializations": agent.specializations,
                    "availability": agent.availability,
                    "trust_score": agent.trust_score,
                    "last_seen": agent.last_seen.isoformat(),
                    "discovery_method": "redis",
                }

            for agent in web_agents:
                all_agents[agent.agent_id] = {
                    "agent_id": agent.agent_id,
                    "capabilities": agent.capabilities,
                    "specializations": agent.specializations,
                    "availability": agent.availability,
                    "trust_score": agent.trust_score,
                    "last_seen": agent.last_seen.isoformat(),
                    "discovery_method": agent.discovery_method,
                }

            return web.json_response(list(all_agents.values()))

        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def health_handler(self, request):
        """Get health status."""
        try:
            summary = await self.health_monitor.get_health_summary()
            return web.json_response(summary)
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def discovery_handler(self, request):
        """Get discovery status."""
        try:
            summary = await self.web_discovery.get_discovery_summary()
            return web.json_response(summary)
        except Exception as e:
            logger.error(f"Error getting discovery status: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def trust_scores_handler(self, request):
        """Get trust scores."""
        try:
            trust_scores = await self.help_manager.get_trust_scores()
            return web.json_response(trust_scores)
        except Exception as e:
            logger.error(f"Error getting trust scores: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def messages_handler(self, request):
        """Get recent messages."""
        try:
            # This would read from the message log
            return web.json_response({"messages": "Not implemented yet"})
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def websocket_handler(self, request):
        """Handle WebSocket connections."""
        ws = WebSocketResponse()
        await ws.prepare(request)

        self.websockets.append(ws)
        logger.info(f"WebSocket connected. Total connections: {len(self.websockets)}")

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    # Handle incoming messages
                    pass
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.websockets.remove(ws)
            logger.info(f"WebSocket disconnected. Total connections: {len(self.websockets)}")

        return ws

    async def broadcast_update(self, data: Dict[str, Any]):
        """Broadcast update to all WebSocket clients."""
        if self.websockets:
            message = json.dumps(data)
            for ws in self.websockets.copy():
                try:
                    await ws.send_str(message)
                except Exception as e:
                    logger.error(f"Error sending WebSocket message: {e}")
                    self.websockets.remove(ws)

    async def start_monitoring(self):
        """Start monitoring and broadcasting updates."""
        while True:
            try:
                # Get current status
                discovery_summary = await self.web_discovery.get_discovery_summary()
                health_summary = await self.health_monitor.get_health_summary()

                # Get agents
                redis_agents = await self.discovery_manager.get_discovered_agents()
                web_agents = await self.web_discovery.get_discovered_agents()

                # Combine agents
                all_agents = []
                for agent in redis_agents:
                    all_agents.append({"agent_id": agent.agent_id, "capabilities": agent.capabilities, "trust_score": agent.trust_score, "availability": agent.availability})

                for agent in web_agents:
                    all_agents.append({"agent_id": agent.agent_id, "capabilities": agent.capabilities, "trust_score": agent.trust_score, "availability": agent.availability})

                # Broadcast update
                await self.broadcast_update({"discovery": discovery_summary, "health": health_summary, "agents": all_agents, "timestamp": datetime.now().isoformat()})

                await asyncio.sleep(5)  # Update every 5 seconds

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

    async def run(self):
        """Run the dashboard."""
        try:
            # Initialize components
            await self.initialize()

            # Create web app
            app = await self.create_app()

            # Start monitoring task
            monitoring_task = asyncio.create_task(self.start_monitoring())

            # Start web server
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", self.port)
            await site.start()

            logger.info(f"🔥 Beast Mode Dashboard running on http://localhost:{self.port}")
            logger.info("Press Ctrl+C to stop")

            # Keep running
            try:
                await asyncio.Future()  # Run forever
            except KeyboardInterrupt:
                logger.info("Shutting down dashboard...")
            finally:
                # Cleanup
                monitoring_task.cancel()
                await self.health_monitor.cleanup()
                await self.web_discovery.stop_discovery()
                await self.redis_manager.close()
                await runner.cleanup()

        except Exception as e:
            logger.error(f"Error running dashboard: {e}")
            raise


async def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Beast Mode Agent Dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Port to run dashboard on")

    args = parser.parse_args()

    dashboard = BeastModeDashboard(port=args.port)
    await dashboard.run()


if __name__ == "__main__":
    asyncio.run(main())
