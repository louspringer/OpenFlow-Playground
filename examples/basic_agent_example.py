#!/usr/bin/env python3
"""
Basic Agent Example for Beast Mode Agent Collaboration Network

Demonstrates Tasks 1-3: Core infrastructure usage
- Redis connection management
- Message models and serialization
- Basic bus client functionality
"""

import asyncio
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.message_models import MessageType, MessageSerializer
from beast_mode.bus_client import BeastModeBusClient


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class BasicAgent:
    """
    Example agent demonstrating Beast Mode network usage.
    """

    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.client = BeastModeBusClient(agent_id=agent_id, capabilities=capabilities)

        # Register message handlers
        self.client.register_message_handler(MessageType.SIMPLE_MESSAGE, self.handle_simple_message)
        self.client.register_message_handler(MessageType.PROMPT_REQUEST, self.handle_prompt_request)
        self.client.register_message_handler(MessageType.AGENT_DISCOVERY, self.handle_agent_discovery)

    async def start(self):
        """Start the agent and connect to the network."""
        logger.info(f"Starting agent {self.agent_id}...")

        # Connect to network
        if await self.client.connect():
            logger.info(f"✅ {self.agent_id} connected to Beast Mode network")

            # Announce presence
            await self.client.announce_presence()

            # Start listening for messages
            await self.client.listen_for_messages()
        else:
            logger.error(f"❌ {self.agent_id} failed to connect")

    async def stop(self):
        """Stop the agent and disconnect from network."""
        logger.info(f"Stopping agent {self.agent_id}...")
        await self.client.disconnect()
        logger.info(f"Agent {self.agent_id} stopped")

    def handle_simple_message(self, message):
        """Handle simple message."""
        logger.info(f"📨 Received simple message from {message.source}: {message.get_message_text()}")

        # Echo the message back
        response_text = f"Echo from {self.agent_id}: {message.get_message_text()}"
        asyncio.create_task(self.client.send_simple_message(response_text, target=message.source))

    def handle_prompt_request(self, message):
        """Handle prompt request."""
        prompt = message.payload.get("prompt", "")
        context = message.payload.get("context", "")

        logger.info(f"📨 Received prompt request from {message.source}: {prompt}")

        # Simple response based on capabilities
        if "gcp_optimization" in self.capabilities and "gcp" in prompt.lower():
            response = "I can help with GCP optimization! I specialize in cost reduction and performance tuning."
        elif "python_coding" in self.capabilities and "python" in prompt.lower():
            response = "I can help with Python coding! I'm experienced with async programming and testing."
        else:
            response = f"I received your request: '{prompt}'. I have these capabilities: {', '.join(self.capabilities)}"

        asyncio.create_task(self.client.send_simple_message(response, target=message.source))

    def handle_agent_discovery(self, message):
        """Handle agent discovery message."""
        capabilities = message.payload.get("capabilities", [])
        specializations = message.payload.get("specializations", [])

        logger.info(f"📨 Discovered agent {message.source} with capabilities: {capabilities}")

        # Check for capability matches
        matches = [cap for cap in capabilities if cap in self.capabilities]
        if matches:
            logger.info(f"🤝 Found capability matches with {message.source}: {matches}")

    async def send_test_messages(self):
        """Send some test messages to demonstrate functionality."""
        logger.info("Sending test messages...")

        # Send simple message
        await self.client.send_simple_message("Hello from the Beast Mode network!")

        # Send prompt request
        await self.client.send_prompt_request("Can you help with GCP cost optimization?", context="We need to reduce our monthly costs")

        # Send another prompt request
        await self.client.send_prompt_request("Do you know Python async programming?", context="Building a message bus system")


async def main():
    """Main example function."""
    print("🧬 Beast Mode Agent Collaboration Network - Basic Example")
    print("=" * 60)

    # Create example agents
    agent1 = BasicAgent(agent_id="gcp_optimizer", capabilities=["gcp_optimization", "cost_analysis", "cloud_architecture"])

    agent2 = BasicAgent(agent_id="python_developer", capabilities=["python_coding", "async_programming", "testing"])

    try:
        # Start agents
        await asyncio.gather(agent1.start(), agent2.start())

        # Wait a moment for discovery
        await asyncio.sleep(2)

        # Send test messages
        await agent1.send_test_messages()

        # Let agents communicate for a bit
        logger.info("Agents are communicating... Press Ctrl+C to stop")
        await asyncio.sleep(10)

    except KeyboardInterrupt:
        logger.info("Stopping example...")
    finally:
        # Stop agents
        await asyncio.gather(agent1.stop(), agent2.stop())

    print("\n✅ Example completed!")


if __name__ == "__main__":
    # Check if Redis is available
    try:
        import redis

        redis_client = redis.Redis(host="localhost", port=6379, db=0)
        redis_client.ping()
        print("✅ Redis is available")
    except Exception as e:
        print(f"❌ Redis is not available: {e}")
        print("Please start Redis server: brew services start redis")
        sys.exit(1)

    # Run example
    asyncio.run(main())
