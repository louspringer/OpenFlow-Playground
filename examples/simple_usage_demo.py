#!/usr/bin/env python3
"""
Simple Usage Demo for Beast Mode Agent Collaboration Network

This demonstrates how to use the basic functionality of Tasks 1-6.
"""

import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import our Beast Mode components
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager
from beast_mode.message_handlers import MessageHandlerManager
from beast_mode.bus_client import BeastModeBusClient


class SimpleAgent:
    """A simple agent that demonstrates basic usage."""

    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities

        # Initialize components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)
        self.message_handler = MessageHandlerManager(agent_id, self.discovery_manager, self.help_manager)
        self.bus_client = BeastModeBusClient(agent_id=agent_id, capabilities=capabilities)

        # Register message handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register message handlers with the bus client."""
        handlers = self.message_handler.get_handlers()
        for message_type, handler in handlers.items():
            self.bus_client.register_message_handler(message_type, handler)

    async def start(self):
        """Start the agent."""
        logger.info(f"🤖 Starting agent: {self.agent_id}")

        # Connect to Redis
        if not await self.redis_manager.connect():
            logger.error(f"❌ Failed to connect to Redis for {self.agent_id}")
            return False

        # Connect bus client
        if not await self.bus_client.connect():
            logger.error(f"❌ Failed to connect bus client for {self.agent_id}")
            return False

        # Announce presence
        await self.discovery_manager.announce_presence()

        # Start listening for messages
        await self.bus_client.listen_for_messages()

        logger.info(f"✅ Agent {self.agent_id} is ready!")
        return True

    async def stop(self):
        """Stop the agent."""
        logger.info(f"🛑 Stopping agent: {self.agent_id}")
        await self.bus_client.disconnect()
        await self.redis_manager.disconnect()

    async def send_message(self, target_agent: str, message_text: str):
        """Send a simple message to another agent."""
        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=target_agent, payload={"message": message_text})

        await self.bus_client.send_message(message)
        logger.info(f"📤 Sent message to {target_agent}: {message_text}")

    async def request_help(self, required_capabilities: list, description: str = ""):
        """Request help from other agents."""
        logger.info(f"🆘 Requesting help for: {required_capabilities}")
        request_id = await self.help_manager.request_help(required_capabilities, description)
        return request_id

    async def get_discovered_agents(self):
        """Get list of discovered agents."""
        return await self.discovery_manager.get_discovered_agents()

    async def get_help_requests(self):
        """Get current help requests."""
        return await self.help_manager.get_help_requests()


async def demo_basic_communication():
    """Demonstrate basic agent communication."""
    print("\n" + "=" * 60)
    print("🔗 BASIC AGENT COMMUNICATION DEMO")
    print("=" * 60)

    # Create two agents
    alice = SimpleAgent("alice", ["python_coding", "data_analysis"])
    bob = SimpleAgent("bob", ["gcp_optimization", "cloud_architecture"])

    try:
        # Start both agents
        await alice.start()
        await bob.start()

        # Wait for discovery
        await asyncio.sleep(2)

        # Check discovered agents
        alice_agents = await alice.get_discovered_agents()
        bob_agents = await bob.get_discovered_agents()

        print(f"👀 Alice discovered {len(alice_agents)} agents:")
        for agent in alice_agents:
            print(f"   - {agent.agent_id}: {agent.capabilities}")

        print(f"👀 Bob discovered {len(bob_agents)} agents:")
        for agent in bob_agents:
            print(f"   - {agent.agent_id}: {agent.capabilities}")

        # Send messages between agents
        await alice.send_message("bob", "Hello Bob! I need help with GCP optimization.")
        await bob.send_message("alice", "Hi Alice! I can help with GCP. What do you need?")

        # Wait for message processing
        await asyncio.sleep(1)

    finally:
        await alice.stop()
        await bob.stop()


async def demo_help_system():
    """Demonstrate the help wanted system."""
    print("\n" + "=" * 60)
    print("🆘 HELP WANTED SYSTEM DEMO")
    print("=" * 60)

    # Create agents with different capabilities
    requester = SimpleAgent("requester", ["basic_coding"])
    helper1 = SimpleAgent("helper1", ["python_coding", "gcp_optimization"])
    helper2 = SimpleAgent("helper2", ["python_coding", "data_analysis"])

    try:
        # Start all agents
        await requester.start()
        await helper1.start()
        await helper2.start()

        # Wait for discovery
        await asyncio.sleep(2)

        # Request help
        request_id = await requester.request_help(["python_coding", "gcp_optimization"], "I need help building a GCP cost optimization tool in Python")

        print(f"📝 Help request sent: {request_id}")

        # Wait for responses
        await asyncio.sleep(3)

        # Check help requests
        requests = await requester.get_help_requests()
        print(f"📋 Help requests: {len(requests)}")
        for req in requests:
            print(f"   - {req.request_id}: {req.status}, responses: {req.responses}")

    finally:
        await requester.stop()
        await helper1.stop()
        await helper2.stop()


async def demo_message_types():
    """Demonstrate different message types."""
    print("\n" + "=" * 60)
    print("📨 MESSAGE TYPES DEMO")
    print("=" * 60)

    # Create agent
    agent = SimpleAgent("message_demo", ["python_coding", "system_architecture"])

    try:
        await agent.start()

        # Wait for setup
        await asyncio.sleep(1)

        # Send different types of messages
        from beast_mode.message_models_dataclass import BeastModeMessage, MessageType

        # Simple message
        simple_msg = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="demo_sender", payload={"message": "This is a simple message"})
        await agent.bus_client.send_message(simple_msg)

        # Prompt request
        prompt_msg = BeastModeMessage(type=MessageType.PROMPT_REQUEST, source="demo_sender", payload={"prompt_type": "cost_analysis", "prompt_data": {"query": "What are the current GCP costs?"}})
        await agent.bus_client.send_message(prompt_msg)

        # System health check
        health_msg = BeastModeMessage(type=MessageType.SYSTEM_HEALTH, source="demo_sender", payload={"check_type": "redis_connection", "health_data": {"status": "checking"}})
        await agent.bus_client.send_message(health_msg)

        # Wait for processing
        await asyncio.sleep(2)

        # Check message handling statistics
        stats = agent.message_handler.get_statistics()
        print(f"📊 Message handling statistics: {stats}")

    finally:
        await agent.stop()


async def main():
    """Main demo function."""
    print("🚀 BEAST MODE AGENT COLLABORATION NETWORK - USAGE DEMO")
    print("=" * 70)

    # Check if Redis is available
    redis_manager = RedisConnectionManager()
    if not await redis_manager.connect():
        print("❌ Redis is not available. Please start Redis server first.")
        print("   Install Redis: brew install redis")
        print("   Start Redis: redis-server")
        return

    await redis_manager.disconnect()
    print("✅ Redis connection verified")

    # Run demonstrations
    await demo_basic_communication()
    await demo_help_system()
    await demo_message_types()

    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("The Beast Mode Agent Collaboration Network is working!")
    print("Agents can discover each other, request help, and communicate effectively.")


if __name__ == "__main__":
    asyncio.run(main())
