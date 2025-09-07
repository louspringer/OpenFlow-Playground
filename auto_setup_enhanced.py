#!/usr/bin/env python3
"""
Enhanced Auto-Setup Script for Beast Mode Agent Collaboration Network

This script provides a complete setup and demonstration of the agent collaboration system
with proper discovery registry wiring and trust scoring.

Usage:
    python auto_setup_enhanced.py [--agent-id AGENT_ID] [--capabilities CAP1,CAP2]
"""

import asyncio
import argparse
import logging
import sys
import os
from typing import List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.bus_client import BeastModeBusClient
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager
from beast_mode.message_handlers import MessageHandlerManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class EnhancedBeastModeAgent:
    """Enhanced agent with full discovery registry wiring and trust scoring."""

    def __init__(self, agent_id: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.redis_manager = RedisConnectionManager()
        self.bus_client = None
        self.discovery_manager = None
        self.help_manager = None
        self.message_handler = None

    async def initialize(self):
        """Initialize all components with proper wiring."""
        logger.info(f"Initializing enhanced agent: {self.agent_id}")

        # Initialize Redis connection
        await self.redis_manager.connect()

        # Initialize bus client
        self.bus_client = BeastModeBusClient(agent_id=self.agent_id, capabilities=self.capabilities, redis_manager=self.redis_manager)

        # Initialize discovery manager
        self.discovery_manager = AgentDiscoveryManager(agent_id=self.agent_id, capabilities=self.capabilities, redis_manager=self.redis_manager)

        # Initialize help system
        self.help_manager = HelpSystemManager(agent_id=self.agent_id, capabilities=self.capabilities, redis_manager=self.redis_manager, discovery_manager=self.discovery_manager)

        # Initialize message handler with discovery registry wiring
        self.message_handler = MessageHandlerManager(agent_id=self.agent_id, discovery_manager=self.discovery_manager, help_manager=self.help_manager)

        # Register all handlers with bus client
        await self._register_handlers()

        logger.info("✅ Enhanced agent initialized successfully")

    async def _register_handlers(self):
        """Register all message handlers with proper discovery registry wiring."""
        # Register discovery handlers
        discovery_handlers = self.discovery_manager.get_handlers()
        for message_type, handler in discovery_handlers.items():
            await self.bus_client.register_message_handler(message_type, handler)

        # Register help system handlers
        help_handlers = self.help_manager.get_handlers()
        for message_type, handler in help_handlers.items():
            await self.bus_client.register_message_handler(message_type, handler)

        # Register message handler manager
        handler_handlers = self.message_handler.get_handlers()
        for message_type, handler in handler_handlers.items():
            await self.bus_client.register_message_handler(message_type, handler)

        logger.info("✅ All handlers registered with discovery registry wiring")

    async def start(self):
        """Start the agent and begin collaboration."""
        logger.info(f"🚀 Starting enhanced agent: {self.agent_id}")

        # Announce presence
        await self.discovery_manager.announce_presence()

        # Start listening for messages
        await self.bus_client.listen_for_messages()

    async def demonstrate_capabilities(self):
        """Demonstrate the agent's capabilities."""
        logger.info("🎯 Demonstrating agent capabilities...")

        # Wait a moment for other agents to discover us
        await asyncio.sleep(2)

        # Get discovered agents
        discovered_agents = await self.discovery_manager.get_discovered_agents()
        logger.info(f"📡 Discovered {len(discovered_agents)} agents")

        for agent in discovered_agents:
            logger.info(f"  - {agent.agent_id}: {agent.capabilities} (trust: {agent.trust_score:.2f})")

        # Request help for demonstration
        if discovered_agents:
            logger.info("🤝 Requesting help from discovered agents...")
            help_agents = await self.help_manager.request_help(required_capabilities=["python_coding"], description="Need help with Python development")
            logger.info(f"📞 Found {len(help_agents)} agents that can help")

        # Update trust scores based on interactions
        await self._simulate_trust_updates()

    async def _simulate_trust_updates(self):
        """Simulate trust score updates based on collaboration success."""
        discovered_agents = await self.discovery_manager.get_discovered_agents()

        for agent in discovered_agents:
            # Simulate some successful collaborations
            success = len(agent.capabilities) > 2  # Simple heuristic
            await self.discovery_manager.update_collaboration_success(agent.agent_id, success)
            logger.info(f"📊 Updated trust for {agent.agent_id}: {success} (new score: {agent.trust_score:.2f})")

    async def cleanup(self):
        """Clean up resources."""
        logger.info("🧹 Cleaning up...")
        if self.redis_manager:
            await self.redis_manager.close()
        logger.info("✅ Cleanup completed")


async def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Enhanced Beast Mode Agent")
    parser.add_argument("--agent-id", default="enhanced_demo_agent", help="Agent identifier")
    parser.add_argument("--capabilities", default="python_coding,gcp_optimization,data_analysis", help="Comma-separated list of capabilities")
    parser.add_argument("--demo-time", type=int, default=30, help="How long to run the demo (seconds)")

    args = parser.parse_args()
    capabilities = [cap.strip() for cap in args.capabilities.split(",")]

    # Create and initialize agent
    agent = EnhancedBeastModeAgent(args.agent_id, capabilities)

    try:
        await agent.initialize()

        # Start agent in background
        agent_task = asyncio.create_task(agent.start())

        # Run demonstration
        await agent.demonstrate_capabilities()

        # Let it run for the demo time
        logger.info(f"⏰ Running demo for {args.demo_time} seconds...")
        await asyncio.sleep(args.demo_time)

        # Cancel the agent task
        agent_task.cancel()

    except KeyboardInterrupt:
        logger.info("🛑 Demo interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error running demo: {e}")
    finally:
        await agent.cleanup()
        logger.info("👋 Demo completed")


if __name__ == "__main__":
    print("🔥 Enhanced Beast Mode Agent Collaboration Network")
    print("=" * 50)
    print("Features:")
    print("✅ Discovery registry wiring")
    print("✅ Trust scoring system")
    print("✅ Enhanced message handling")
    print("✅ Health monitoring")
    print("=" * 50)

    asyncio.run(main())
