#!/usr/bin/env python3
"""
Quick Demo: How to Use Beast Mode Agent Collaboration Network

This shows you exactly how to use the system we built.
"""

import asyncio
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType, AgentCapabilities
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager


async def demo_basic_usage():
    """Show basic usage of the Beast Mode system."""

    print("🚀 BEAST MODE AGENT COLLABORATION NETWORK - QUICK DEMO")
    print("=" * 60)

    # 1. Check Redis connection
    print("1. Checking Redis connection...")
    redis_manager = RedisConnectionManager()
    if not await redis_manager.connect():
        print("❌ Redis not available. Please start Redis first:")
        print("   brew install redis && redis-server")
        return
    print("✅ Redis connected!")
    await redis_manager.disconnect()

    # 2. Create a simple agent
    print("\n2. Creating an agent...")
    agent_id = "demo_agent"
    capabilities = ["python_coding", "gcp_optimization", "data_analysis"]

    # Initialize components
    redis_manager = RedisConnectionManager()
    discovery_manager = AgentDiscoveryManager(agent_id, capabilities, redis_manager)
    help_manager = HelpSystemManager(agent_id, discovery_manager)

    # 3. Connect and announce presence
    print("3. Connecting agent to network...")
    await redis_manager.connect()
    await discovery_manager.announce_presence()
    print(f"✅ Agent '{agent_id}' announced with capabilities: {capabilities}")

    # 4. Create and send a message
    print("\n4. Creating and sending a message...")
    message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source=agent_id, target=None, payload={"message": "Hello from the Beast Mode network!"})  # Broadcast to all

    await redis_manager.publish("beast_mode_network", message.to_json())
    print("✅ Message sent!")

    # 5. Request help
    print("\n5. Requesting help...")
    request_id = await help_manager.request_help(required_capabilities=["python_coding"], description="I need help with Python development")
    print(f"✅ Help request sent: {request_id}")

    # 6. Show agent capabilities
    print("\n6. Agent capabilities:")
    capabilities_obj = AgentCapabilities(agent_id=agent_id, capabilities=capabilities, availability="ready_for_business")
    print(f"   Agent ID: {capabilities_obj.agent_id}")
    print(f"   Capabilities: {capabilities_obj.capabilities}")
    print(f"   Availability: {capabilities_obj.availability}")

    # 7. Show message types available
    print("\n7. Available message types:")
    for msg_type in MessageType:
        print(f"   - {msg_type.value}")

    # 8. Cleanup
    print("\n8. Cleaning up...")
    await redis_manager.disconnect()
    print("✅ Demo complete!")

    print("\n" + "=" * 60)
    print("🎉 THAT'S HOW YOU USE IT!")
    print("=" * 60)
    print("The Beast Mode Agent Collaboration Network provides:")
    print("✅ Agent discovery and capability matching")
    print("✅ Help wanted system with collaboration tracking")
    print("✅ 12 standardized message types")
    print("✅ Redis-based pub/sub communication")
    print("✅ Trust scoring and agent recommendations")
    print("✅ Comprehensive error handling")


if __name__ == "__main__":
    asyncio.run(demo_basic_usage())
