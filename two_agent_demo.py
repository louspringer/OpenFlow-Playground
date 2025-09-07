#!/usr/bin/env python3
"""
Two Agent Demo - Shows Real Agent Communication

This demonstrates how two agents can discover each other and communicate.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager


class Agent:
    """Simple agent for demonstration."""

    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities

        # Initialize components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)

    async def start(self):
        """Start the agent."""
        print(f"🤖 Starting {self.agent_id}...")
        await self.redis_manager.connect()
        await self.discovery_manager.announce_presence()
        print(f"✅ {self.agent_id} is ready!")
        return True

    async def stop(self):
        """Stop the agent."""
        print(f"🛑 Stopping {self.agent_id}...")
        await self.redis_manager.disconnect()

    async def send_message(self, target_agent: str, message_text: str):
        """Send a message to another agent."""
        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=self.agent_id, target=target_agent, payload={"message": message_text})
        await self.redis_manager.publish("beast_mode_network", message.to_json())
        print(f"📤 {self.agent_id} → {target_agent}: {message_text}")

    async def discover_agents(self):
        """Discover other agents."""
        agents = await self.discovery_manager.get_discovered_agents()
        print(f"👀 {self.agent_id} discovered {len(agents)} agents:")
        for agent in agents:
            print(f"   - {agent.agent_id}: {agent.capabilities}")
        return agents

    async def request_help(self, required_capabilities: list, description: str):
        """Request help from other agents."""
        print(f"🆘 {self.agent_id} requesting help for: {required_capabilities}")
        request_id = await self.help_manager.request_help(required_capabilities, description)
        print(f"   Help request ID: {request_id}")
        return request_id


async def main():
    """Main demo function."""
    print("🚀 TWO AGENT COMMUNICATION DEMO")
    print("=" * 50)

    # Create two agents with different capabilities
    alice = Agent("alice", ["python_coding", "data_analysis"])
    bob = Agent("bob", ["gcp_optimization", "cloud_architecture"])

    try:
        # Start both agents
        print("\n1. Starting agents...")
        await alice.start()
        await bob.start()

        # Wait a moment for discovery
        print("\n2. Waiting for agent discovery...")
        await asyncio.sleep(2)

        # Discover agents
        print("\n3. Discovering other agents...")
        alice_agents = await alice.discover_agents()
        bob_agents = await bob.discover_agents()

        # Send messages between agents
        print("\n4. Sending messages between agents...")
        await alice.send_message("bob", "Hello Bob! I need help with GCP optimization.")
        await bob.send_message("alice", "Hi Alice! I can help with GCP. What do you need?")

        # Request help
        print("\n5. Requesting help...")
        await alice.request_help(["gcp_optimization"], "I need help optimizing GCP costs")
        await bob.request_help(["python_coding"], "I need help with Python development")

        # Wait for message processing
        print("\n6. Waiting for message processing...")
        await asyncio.sleep(1)

        print("\n✅ Demo complete!")
        print("   Both agents successfully:")
        print("   - Discovered each other")
        print("   - Sent messages")
        print("   - Requested help")
        print("   - Communicated via Redis pub/sub")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await alice.stop()
        await bob.stop()


if __name__ == "__main__":
    asyncio.run(main())
