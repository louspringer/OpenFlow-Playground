#!/usr/bin/env python3
"""
Simple Beast Mode Bus Sender
- Puts a message on the bus
- Dies immediately after sending
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime
import uuid


class SimpleSender:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis_url = redis_url
        self.client = None

    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.from_url(self.redis_url)
            await self.client.ping()
            print(f"✅ Connected to Redis at {self.redis_url}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def send_message(self, message_text):
        """Send a message and die"""
        message = {
            "id": str(uuid.uuid4()),
            "type": "simple_message",
            "source": "simple_sender",
            "target": None,
            "payload": {"message": message_text, "timestamp": datetime.now().isoformat()},
            "timestamp": datetime.now().isoformat(),
            "priority": 5,
        }

        await self.client.publish("beast_mode_network", json.dumps(message))
        print(f"📤 Sent message: {message_text}")

        # Die immediately
        await self.client.aclose()
        print("💀 Sender died")


async def main():
    import sys

    # Get message from command line or use default
    if len(sys.argv) > 1:
        # Join all arguments after the script name
        message_text = " ".join(sys.argv[1:])
    else:
        message_text = "Hello from simple sender!"

    sender = SimpleSender()

    if not await sender.connect():
        return

    await sender.send_message(message_text)


if __name__ == "__main__":
    asyncio.run(main())
