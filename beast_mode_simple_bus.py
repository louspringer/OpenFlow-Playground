#!/usr/bin/env python3
"""
Beast Mode Simple Bus - Trusted Message Exchange
Just post messages to topics, all subscribers see them. That's it.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import redis.asyncio as redis
except ImportError:
    print("Installing dependencies...")
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "redis"])
    import redis.asyncio as redis


class BeastModeSimpleBus:
    """Simple message bus - post to topics, all subscribers see it"""

    def __init__(self, redis_url="redis://localhost:6379", agent_id=None):
        self.redis_url = redis_url
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.client = None
        self.is_connected = False
        self.subscribed_topics = set()

    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.from_url(self.redis_url)
            await self.client.ping()
            self.is_connected = True
            print(f"🧬 {self.agent_id} connected to Beast Mode bus")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def subscribe_to_topic(self, topic: str):
        """Subscribe to a topic - you'll see all messages posted to it"""
        if not self.is_connected:
            print("❌ Not connected to bus")
            return False

        self.subscribed_topics.add(topic)
        print(f"📡 Subscribed to topic: {topic}")
        return True

    async def post_message(self, topic: str, message: str, metadata: Dict[str, Any] = None):
        """Post a message to a topic - all subscribers will see it"""
        if not self.is_connected:
            print("❌ Not connected to bus")
            return False

        payload = {"id": str(uuid.uuid4()), "agent_id": self.agent_id, "topic": topic, "message": message, "timestamp": datetime.now().isoformat(), "metadata": metadata or {}}

        await self.client.publish(f"beast_mode_topic_{topic}", json.dumps(payload))
        print(f"📤 Posted to {topic}: {message[:50]}...")
        return True

    async def listen_for_messages(self):
        """Listen for messages on all subscribed topics"""
        if not self.subscribed_topics:
            print("❌ No topics subscribed")
            return

        pubsub = self.client.pubsub()

        # Subscribe to all topics
        for topic in self.subscribed_topics:
            await pubsub.subscribe(f"beast_mode_topic_{topic}")
            print(f"👂 Listening to topic: {topic}")

        print("📥 Listening for messages... (Press Ctrl+C to stop)")

        try:
            async for raw_message in pubsub.listen():
                if raw_message["type"] == "message":
                    try:
                        data = json.loads(raw_message["data"])

                        # Don't show our own messages
                        if data["agent_id"] == self.agent_id:
                            continue

                        print(f"\n📨 [{data['topic']}] from {data['agent_id']}:")
                        print(f"   {data['message']}")

                        if data.get("metadata"):
                            print(f"   Metadata: {data['metadata']}")

                    except Exception as e:
                        print(f"❌ Error processing message: {e}")

        except KeyboardInterrupt:
            print("\n🛑 Stopping listener...")

    async def disconnect(self):
        """Disconnect from bus"""
        if self.client:
            await self.client.aclose()
        print(f"🔌 {self.agent_id} disconnected")


async def main():
    """Main function with simple interface"""
    print("🧬 Beast Mode Simple Bus")
    print("=" * 30)

    # Get agent ID
    agent_id = input("Enter your agent ID (or press Enter for random): ").strip()
    if not agent_id:
        agent_id = None

    bus = BeastModeSimpleBus(agent_id=agent_id)

    try:
        # Connect
        if not await bus.connect():
            return

        # Get topics to subscribe to
        topics_input = input("Enter topics to subscribe to (comma-separated): ").strip()
        if topics_input:
            topics = [topic.strip() for topic in topics_input.split(",")]
            for topic in topics:
                await bus.subscribe_to_topic(topic)
        else:
            print("No topics subscribed - you won't see any messages")

        # Start listening in background
        listen_task = asyncio.create_task(bus.listen_for_messages())

        # Interactive posting
        print("\n💬 Post messages to topics (format: topic:message)")
        print("Examples:")
        print("  prompts:How do I optimize Redis memory usage?")
        print("  code_review:Can someone review this Python function?")
        print("  tools:I need a Kubernetes monitoring setup")
        print("  general:Hello everyone!")
        print("\nType 'quit' to exit")

        while True:
            try:
                user_input = input(f"\n[{bus.agent_id}] ").strip()

                if user_input.lower() == "quit":
                    break

                if ":" in user_input:
                    topic, message = user_input.split(":", 1)
                    topic = topic.strip()
                    message = message.strip()

                    if topic and message:
                        await bus.post_message(topic, message)
                    else:
                        print("❌ Invalid format. Use: topic:message")
                else:
                    print("❌ Invalid format. Use: topic:message")

            except KeyboardInterrupt:
                break

        # Cancel listening task
        listen_task.cancel()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        await bus.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
