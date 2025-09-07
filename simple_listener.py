#!/usr/bin/env python3
"""
Simple Beast Mode Bus Listener
- Runs forever
- Listens for messages on the bus
- Logs all messages to a file
- Never dies unless killed
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime


class SimpleListener:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis_url = redis_url
        self.client = None
        self.log_file = "bus_messages.log"

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

    async def listen_forever(self):
        """Listen for messages forever and log them"""
        pubsub = self.client.pubsub()
        await pubsub.subscribe("beast_mode_network")

        print("📥 Listening for messages on beast_mode_network...")
        print(f"📝 Logging to: {self.log_file}")
        print("🛑 Press Ctrl+C to stop")

        try:
            async for raw_message in pubsub.listen():
                if raw_message["type"] == "message":
                    timestamp = datetime.now().isoformat()
                    message_data = raw_message["data"].decode("utf-8")

                    # Log to file
                    with open(self.log_file, "a") as f:
                        f.write(f"[{timestamp}] {message_data}\n")

                    print(f"📨 [{timestamp}] Message logged")

        except KeyboardInterrupt:
            print("\n🛑 Stopping listener...")
        finally:
            await pubsub.close()
            await self.client.aclose()


async def main():
    listener = SimpleListener()

    if not await listener.connect():
        return

    await listener.listen_forever()


if __name__ == "__main__":
    asyncio.run(main())
