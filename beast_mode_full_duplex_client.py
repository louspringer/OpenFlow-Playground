#!/usr/bin/env python3
"""
Beast Mode Full Duplex Client - Proper conversation support
"""

import asyncio
import json
import uuid
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional
import redis.asyncio as redis


class BeastModeFullDuplexClient:
    """Full duplex Beast Mode client with proper conversation support"""

    def __init__(self, redis_url="redis://localhost:6379", agent_id=None):
        self.redis_url = redis_url
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.client = None
        self.is_connected = False
        self.listening = False
        self.message_history = []

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

    async def peek_messages(self):
        """Peek at messages without consuming them"""
        if not self.is_connected:
            return []

        try:
            # Check if there are messages waiting
            info = await self.client.info("memory")
            print(f"📊 Redis memory info: {info}")

            # Try to get recent messages from history if available
            # This is a basic peek - Redis pub/sub doesn't store messages
            return []
        except Exception as e:
            print(f"❌ Peek failed: {e}")
            return []

    async def send_message(self, target: str, message: str, message_type: str = "prompt_request", priority: int = 5):
        """Send a message to the bus"""
        if not self.is_connected:
            print("❌ Not connected to bus")
            return False

        payload = {
            "id": str(uuid.uuid4()),
            "type": message_type,
            "source": self.agent_id,
            "target": target,
            "payload": {"prompt": message, "context": "conversation", "priority": priority},
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
        }

        await self.client.publish("beast_mode_network", json.dumps(payload))
        print(f"📤 Sent to {target}: {message[:50]}...")
        return True

    async def listen_for_messages(self, timeout: int = 30):
        """Listen for messages with timeout"""
        if not self.is_connected:
            print("❌ Not connected to bus")
            return

        pubsub = self.client.pubsub()
        await pubsub.subscribe("beast_mode_network")

        print(f"📥 Listening for messages (timeout: {timeout}s)...")
        self.listening = True

        try:
            start_time = time.time()
            async for raw_message in pubsub.listen():
                if not self.listening:
                    break

                if raw_message["type"] == "message":
                    try:
                        data = json.loads(raw_message["data"])

                        # Don't process our own messages
                        if data.get("source") == self.agent_id:
                            continue

                        # Store in history
                        self.message_history.append(data)

                        print(f"\n📨 MESSAGE RECEIVED:")
                        print(f"From: {data.get('source', 'unknown')}")
                        print(f"Type: {data.get('type', 'unknown')}")
                        print(f"Content: {data.get('payload', {}).get('prompt', 'No content')}")
                        print("-" * 40)

                        # Return the message
                        return data

                    except Exception as e:
                        print(f"❌ Error processing message: {e}")

                # Timeout check
                if time.time() - start_time > timeout:
                    print(f"⏰ Timeout after {timeout} seconds")
                    return None

        except Exception as e:
            print(f"❌ Listen error: {e}")
        finally:
            await pubsub.aclose()
            self.listening = False

    async def start_conversation(self, target: str, initial_message: str = None):
        """Start a full duplex conversation"""
        print(f"💬 Starting conversation with {target}")
        print("Commands: 'send <message>', 'listen', 'peek', 'history', 'quit'")

        if initial_message:
            await self.send_message(target, initial_message)

        while True:
            try:
                command = input(f"\n[{self.agent_id}] ").strip().lower()

                if command == "quit":
                    break
                elif command.startswith("send "):
                    message = command[5:]
                    await self.send_message(target, message)
                elif command == "listen":
                    await self.listen_for_messages(timeout=10)
                elif command == "peek":
                    await self.peek_messages()
                elif command == "history":
                    print(f"📚 Message history ({len(self.message_history)} messages):")
                    for i, msg in enumerate(self.message_history[-5:]):  # Last 5
                        print(f"  {i+1}. From {msg.get('source')}: {msg.get('payload', {}).get('prompt', '')[:50]}...")
                else:
                    print("❌ Unknown command. Use: send, listen, peek, history, quit")

            except KeyboardInterrupt:
                print("\n🛑 Stopping conversation...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    async def disconnect(self):
        """Disconnect from bus"""
        self.listening = False
        if self.client:
            await self.client.aclose()
        print(f"🔌 {self.agent_id} disconnected")


async def main():
    """Main function"""
    print("🧬 Beast Mode Full Duplex Client")
    print("=" * 40)

    # Get target agent
    target = input("Enter target agent ID: ").strip()
    if not target:
        target = "kiro_spore_creator"

    # Get initial message
    initial_message = input("Enter initial message (or press Enter to skip): ").strip()

    client = BeastModeFullDuplexClient()

    try:
        if await client.connect():
            await client.start_conversation(target, initial_message)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
