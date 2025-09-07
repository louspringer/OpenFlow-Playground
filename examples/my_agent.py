#!/usr/bin/env python3
"""
My Agent - A Complete Example

This shows you how to build a real agent that can:
- Discover other agents
- Send and receive messages
- Request help when needed
- Respond to help requests
"""

import asyncio
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MyAgent:
    """A complete agent implementation."""

    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities

        # Initialize components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)

        # Track discovered agents
        self.discovered_agents = []

    async def start(self):
        """Start the agent."""
        logger.info(f"🤖 Starting {self.agent_id}...")

        # Connect to Redis
        if not await self.redis_manager.connect():
            logger.error("❌ Failed to connect to Redis")
            return False

        # Announce presence
        await self.discovery_manager.announce_presence()
        logger.info(f"✅ {self.agent_id} is ready with capabilities: {self.capabilities}")

        return True

    async def stop(self):
        """Stop the agent."""
        logger.info(f"🛑 Stopping {self.agent_id}...")
        await self.redis_manager.disconnect()

    async def send_message(self, target_agent: str, message_text: str):
        """Send a message to another agent."""
        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=target_agent, payload={"message": message_text})

        await self.redis_manager.publish("beast_mode_network", message.to_json())
        logger.info(f"📤 Sent to {target_agent}: {message_text}")

    async def request_help(self, required_capabilities: list, description: str):
        """Request help from other agents."""
        logger.info(f"🆘 Requesting help for: {required_capabilities}")
        request_id = await self.help_manager.request_help(required_capabilities, description)
        return request_id

    async def discover_agents(self):
        """Discover other agents on the network."""
        self.discovered_agents = await self.discovery_manager.get_discovered_agents()
        logger.info(f"👀 Discovered {len(self.discovered_agents)} agents:")
        for agent in self.discovered_agents:
            logger.info(f"   - {agent.agent_id}: {agent.capabilities}")
        return self.discovered_agents

    async def get_help_requests(self):
        """Get current help requests."""
        return await self.help_manager.get_help_requests()

    async def get_collaboration_metrics(self):
        """Get collaboration success metrics."""
        return await self.help_manager.get_collaboration_metrics()


async def main():
    """Main function - shows how to use your agent."""

    print("🚀 MY AGENT - BEAST MODE COLLABORATION NETWORK")
    print("=" * 50)

    # Create your agent
    my_agent = MyAgent("my_agent", ["python_coding", "gcp_optimization", "data_analysis"])

    try:
        # Start the agent
        if not await my_agent.start():
            print("❌ Failed to start agent")
            return

        # Discover other agents
        print("\n1. Discovering other agents...")
        await my_agent.discover_agents()

        # Send a message
        print("\n2. Sending a message...")
        await my_agent.send_message("broadcast", "Hello from my agent!")

        # Request help
        print("\n3. Requesting help...")
        request_id = await my_agent.request_help(["python_coding"], "I need help with Python development")
        print(f"   Help request ID: {request_id}")

        # Show capabilities
        print("\n4. My agent capabilities:")
        print(f"   Agent ID: {my_agent.agent_id}")
        print(f"   Capabilities: {my_agent.capabilities}")

        # Show message types
        print("\n5. Available message types:")
        for msg_type in MessageType:
            print(f"   - {msg_type.value}")

        print("\n✅ Your agent is working!")
        print("   It can discover other agents, send messages, and request help.")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await my_agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
