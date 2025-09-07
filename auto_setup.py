#!/usr/bin/env python3
"""
Auto-Setup Script for Beast Mode Agent Collaboration Network

This script automatically sets up the system and creates a working agent.
"""

import asyncio
import sys
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import the core modules
from message_models import BeastModeMessage, MessageType, AgentCapabilities
from redis_foundation import RedisConnectionManager
from agent_discovery import AgentDiscoveryManager
from help_system import HelpSystemManager
from bus_client import BeastModeBusClient


class AutoAgent:
    """An automatically configured agent that can be used immediately."""

    def __init__(self, agent_id: str = None, capabilities: list = None):
        self.agent_id = agent_id or f"auto_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.capabilities = capabilities or ["general_assistance", "information_processing"]

        # Initialize all components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(self.agent_id, self.capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(self.agent_id, self.discovery_manager)
        self.bus_client = BeastModeBusClient(agent_id=self.agent_id, capabilities=self.capabilities)

        # Register message handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up message handlers for different message types."""
        self.bus_client.register_message_handler(MessageType.SIMPLE_MESSAGE, self._handle_simple_message)
        self.bus_client.register_message_handler(MessageType.AGENT_DISCOVERY, self._handle_agent_discovery)
        self.bus_client.register_message_handler(MessageType.HELP_WANTED, self._handle_help_wanted)
        self.bus_client.register_message_handler(MessageType.HELP_RESPONSE, self._handle_help_response)

    async def _handle_simple_message(self, message: BeastModeMessage):
        """Handle simple messages."""
        logger.info(f"📨 Received message from {message.source}: {message.payload.get('message', '')}")

    async def _handle_agent_discovery(self, message: BeastModeMessage):
        """Handle agent discovery messages."""
        if message.source != self.agent_id:
            logger.info(f"🔍 Discovered new agent: {message.source}")

    async def _handle_help_wanted(self, message: BeastModeMessage):
        """Handle help wanted messages."""
        if message.source != self.agent_id:
            required_caps = message.payload.get("required_capabilities", [])
            if any(cap in self.capabilities for cap in required_caps):
                logger.info(f"🆘 Can help {message.source} with: {required_caps}")

    async def _handle_help_response(self, message: BeastModeMessage):
        """Handle help response messages."""
        if message.source != self.agent_id:
            logger.info(f"✅ Received help response from {message.source}")

    async def start(self):
        """Start the agent."""
        logger.info(f"🚀 Starting Beast Mode Agent: {self.agent_id}")

        # Connect to Redis
        if not await self.redis_manager.connect():
            logger.error("❌ Failed to connect to Redis. Please start Redis server.")
            return False

        # Connect bus client
        if not await self.bus_client.connect():
            logger.error("❌ Failed to connect bus client")
            return False

        # Announce presence
        await self.bus_client.announce_presence()

        # Start listening
        await self.bus_client.listen_for_messages()

        logger.info(f"✅ Agent {self.agent_id} is ready and listening!")
        return True

    async def stop(self):
        """Stop the agent."""
        logger.info(f"🛑 Stopping agent {self.agent_id}...")
        self.bus_client.stop_listening()
        await self.bus_client.disconnect()
        await self.redis_manager.disconnect()

    async def send_message(self, target_agent: str, message_text: str):
        """Send a message to another agent."""
        await self.bus_client.send_simple_message(message_text, target_agent)
        logger.info(f"📤 Sent to {target_agent}: {message_text}")

    async def request_help(self, required_capabilities: list, description: str):
        """Request help from other agents."""
        request_id = await self.help_manager.request_help(required_capabilities, description)
        logger.info(f"🆘 Requested help: {description}")
        return request_id

    async def discover_agents(self):
        """Discover other agents on the network."""
        agents = await self.discovery_manager.get_discovered_agents()
        logger.info(f"👀 Discovered {len(agents)} agents:")
        for agent in agents:
            logger.info(f"   - {agent.agent_id}: {agent.capabilities}")
        return agents


async def main():
    """Main function - demonstrates the complete system."""
    print("🚀 BEAST MODE AGENT COLLABORATION NETWORK - AUTO SETUP")
    print("=" * 60)

    # Check Redis connection
    redis_manager = RedisConnectionManager()
    if not await redis_manager.connect():
        print("❌ Redis not available. Please start Redis first:")
        print("   macOS: brew install redis && redis-server")
        print("   Ubuntu: sudo apt-get install redis-server && sudo systemctl start redis")
        return

    await redis_manager.disconnect()
    print("✅ Redis connection verified")

    # Create and start agent
    agent = AutoAgent("demo_agent", ["python_coding", "gcp_optimization", "data_analysis"])

    try:
        if await agent.start():
            print("\n🎉 Agent is ready! Here's what you can do:")
            print("1. Send messages: await agent.send_message('target', 'Hello!')")
            print("2. Request help: await agent.request_help(['python_coding'], 'I need help')")
            print("3. Discover agents: await agent.discover_agents()")
            print("\nThe agent is now listening for messages and ready to collaborate!")

            # Demo some functionality
            await agent.send_message("broadcast", "Hello from the Beast Mode network!")
            await agent.request_help(["python_coding"], "I need help with Python development")

            # Wait a moment to see activity
            await asyncio.sleep(2)

            # Discover agents
            await agent.discover_agents()

            print("\n✅ Demo complete! The system is working.")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
