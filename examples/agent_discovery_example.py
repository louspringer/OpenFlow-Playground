#!/usr/bin/env python3
"""
Agent Discovery and Communication Example

Demonstrates Tasks 4-6: Agent discovery, help wanted system, and message type handling.
"""

import asyncio
import logging
from datetime import datetime

from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager
from beast_mode.message_handlers import MessageHandlerManager
from beast_mode.bus_client import BeastModeBusClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CollaborativeAgent:
    """Example collaborative agent that demonstrates all Tasks 4-6 functionality."""

    def __init__(self, agent_id: str, capabilities: list, redis_url: str = "redis://localhost:6379"):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.redis_url = redis_url

        # Initialize components
        self.redis_manager = RedisConnectionManager(redis_url)
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)
        self.message_handler = MessageHandlerManager(agent_id, self.discovery_manager, self.help_manager)
        self.bus_client = BeastModeBusClient(agent_id, capabilities, redis_url)

    async def start(self):
        """Start the collaborative agent."""
        logger.info(f"Starting collaborative agent: {self.agent_id}")

        # Connect to Redis
        if not await self.redis_manager.connect():
            logger.error(f"Failed to connect to Redis for {self.agent_id}")
            return False

        # Connect bus client
        if not await self.bus_client.connect():
            logger.error(f"Failed to connect bus client for {self.agent_id}")
            return False

        # Register message handlers
        handlers = self.message_handler.get_handlers()
        for message_type, handler in handlers.items():
            self.bus_client.register_handler(message_type, handler)

        # Announce presence
        await self.discovery_manager.announce_presence()

        # Start listening for messages
        await self.bus_client.start_listening()

        logger.info(f"Agent {self.agent_id} is ready for collaboration!")
        return True

    async def stop(self):
        """Stop the collaborative agent."""
        logger.info(f"Stopping agent: {self.agent_id}")
        await self.bus_client.disconnect()
        await self.redis_manager.disconnect()

    async def request_help(self, required_capabilities: list, description: str = ""):
        """Request help from other agents."""
        logger.info(f"Requesting help for capabilities: {required_capabilities}")
        request_id = await self.help_manager.request_help(required_capabilities, description)
        return request_id

    async def get_discovered_agents(self):
        """Get list of discovered agents."""
        return await self.discovery_manager.get_discovered_agents()

    async def get_help_requests(self):
        """Get current help requests."""
        return await self.help_manager.get_help_requests()

    async def get_collaboration_metrics(self):
        """Get collaboration metrics."""
        return await self.help_manager.get_collaboration_metrics()

    async def send_message(self, target_agent: str, message_text: str):
        """Send a simple message to another agent."""
        from beast_mode.message_models import BeastModeMessage, MessageType

        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=target_agent, payload={"message": message_text})

        await self.bus_client.send_message(message)
        logger.info(f"Sent message to {target_agent}: {message_text}")


async def demonstrate_agent_discovery():
    """Demonstrate agent discovery functionality."""
    print("\n=== AGENT DISCOVERY DEMONSTRATION ===")

    # Create two agents with different capabilities
    agent1 = CollaborativeAgent("python_expert", ["python_coding", "data_analysis", "machine_learning"])
    agent2 = CollaborativeAgent("gcp_specialist", ["gcp_optimization", "cloud_architecture", "cost_analysis"])

    try:
        # Start both agents
        await agent1.start()
        await agent2.start()

        # Wait a moment for discovery
        await asyncio.sleep(2)

        # Check discovered agents
        discovered_1 = await agent1.get_discovered_agents()
        discovered_2 = await agent2.get_discovered_agents()

        print(f"Agent 1 discovered {len(discovered_1)} agents:")
        for agent in discovered_1:
            print(f"  - {agent.agent_id}: {agent.capabilities}")

        print(f"Agent 2 discovered {len(discovered_2)} agents:")
        for agent in discovered_2:
            print(f"  - {agent.agent_id}: {agent.capabilities}")

        # Send messages between agents
        await agent1.send_message("gcp_specialist", "Hello! I need help with GCP optimization.")
        await agent2.send_message("python_expert", "Hi! I can help with GCP. What do you need?")

        # Wait for message processing
        await asyncio.sleep(1)

    finally:
        await agent1.stop()
        await agent2.stop()


async def demonstrate_help_system():
    """Demonstrate help wanted system."""
    print("\n=== HELP WANTED SYSTEM DEMONSTRATION ===")

    # Create agents
    requester = CollaborativeAgent("requester", ["basic_coding"])
    helper1 = CollaborativeAgent("helper1", ["python_coding", "gcp_optimization"])
    helper2 = CollaborativeAgent("helper2", ["python_coding", "data_analysis"])

    try:
        # Start all agents
        await requester.start()
        await helper1.start()
        await helper2.start()

        # Wait for discovery
        await asyncio.sleep(2)

        # Request help
        request_id = await requester.request_help(["python_coding", "gcp_optimization"], "I need help building a GCP cost optimization tool in Python")

        print(f"Help request sent: {request_id}")

        # Wait for responses
        await asyncio.sleep(3)

        # Check help requests
        requests = await requester.get_help_requests()
        print(f"Help requests: {len(requests)}")
        for req in requests:
            print(f"  - {req.request_id}: {req.status}, responses: {req.responses}")

        # Check collaboration metrics
        metrics = await requester.get_collaboration_metrics()
        print(f"Collaboration metrics: {metrics.total_requests} requests, {metrics.get_success_rate():.2%} success rate")

    finally:
        await requester.stop()
        await helper1.stop()
        await helper2.stop()


async def demonstrate_message_handling():
    """Demonstrate message type handling."""
    print("\n=== MESSAGE TYPE HANDLING DEMONSTRATION ===")

    # Create agent
    agent = CollaborativeAgent("message_handler", ["python_coding", "system_architecture"])

    try:
        await agent.start()

        # Wait for setup
        await asyncio.sleep(1)

        # Send different types of messages
        from beast_mode.message_models import BeastModeMessage, MessageType

        # Simple message
        simple_msg = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="test_sender", payload={"message": "This is a simple message"})
        await agent.bus_client.send_message(simple_msg)

        # Prompt request
        prompt_msg = BeastModeMessage(type=MessageType.PROMPT_REQUEST, source="test_sender", payload={"prompt_type": "cost_analysis", "prompt_data": {"query": "What are the current GCP costs?"}})
        await agent.bus_client.send_message(prompt_msg)

        # System health check
        health_msg = BeastModeMessage(type=MessageType.SYSTEM_HEALTH, source="test_sender", payload={"check_type": "redis_connection", "health_data": {"status": "checking"}})
        await agent.bus_client.send_message(health_msg)

        # Wait for processing
        await asyncio.sleep(2)

        # Check message handling statistics
        stats = agent.message_handler.get_statistics()
        print(f"Message handling statistics: {stats}")

    finally:
        await agent.stop()


async def main():
    """Main demonstration function."""
    print("Beast Mode Agent Collaboration Network - Tasks 4-6 Demonstration")
    print("=" * 70)

    # Check if Redis is available
    redis_manager = RedisConnectionManager()
    if not await redis_manager.connect():
        print("❌ Redis is not available. Please start Redis server first.")
        return

    await redis_manager.disconnect()
    print("✅ Redis connection verified")

    # Run demonstrations
    await demonstrate_agent_discovery()
    await demonstrate_help_system()
    await demonstrate_message_handling()

    print("\n=== DEMONSTRATION COMPLETE ===")
    print("All Tasks 4-6 functionality has been demonstrated:")
    print("✅ Task 4: Agent discovery protocol")
    print("✅ Task 5: Help wanted system")
    print("✅ Task 6: Message type handling")


if __name__ == "__main__":
    asyncio.run(main())
