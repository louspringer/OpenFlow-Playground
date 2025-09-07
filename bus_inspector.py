#!/usr/bin/env python3
"""
Bus Inspector - Connect to the Beast Mode bus and see what's actually there
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime


async def inspect_bus():
    """Connect to the bus and see what's there"""
    print("🔍 Beast Mode Bus Inspector")
    print("=" * 30)

    try:
        # Connect to Redis (same as the original client)
        client = redis.from_url("redis://localhost:6379")
        await client.ping()
        print("✅ Connected to Redis")

        # Subscribe to the same channel as the original client
        pubsub = client.pubsub()
        await pubsub.subscribe("beast_mode_network")
        print("📡 Subscribed to 'beast_mode_network' channel")

        # Check if there are any messages waiting
        print("🔍 Checking for existing messages...")

        # Listen for a few seconds to see if there's any activity
        message_count = 0
        start_time = datetime.now()

        print("📥 Listening for messages (10 seconds)...")

        async for raw_message in pubsub.listen():
            if raw_message["type"] == "message":
                message_count += 1
                print(f"\n📨 MESSAGE #{message_count} FOUND:")
                print("-" * 40)

                try:
                    data = json.loads(raw_message["data"])
                    print(f"ID: {data.get('id', 'N/A')}")
                    print(f"Type: {data.get('type', 'N/A')}")
                    print(f"Source: {data.get('source', 'N/A')}")
                    print(f"Target: {data.get('target', 'N/A')}")
                    print(f"Timestamp: {data.get('timestamp', 'N/A')}")
                    print(f"Priority: {data.get('priority', 'N/A')}")
                    print(f"Payload: {json.dumps(data.get('payload', {}), indent=2)}")

                except Exception as e:
                    print(f"❌ Error parsing message: {e}")
                    print(f"Raw data: {raw_message['data']}")

                print("-" * 40)

                # Stop after first message or timeout
                if message_count >= 1:
                    break

            # Timeout after 10 seconds
            if (datetime.now() - start_time).seconds >= 10:
                break

        if message_count == 0:
            print("📭 Q empty - No messages found on the bus")
        else:
            print(f"✅ Found {message_count} message(s) on the bus")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure Redis is running: redis-cli ping")

    finally:
        if "client" in locals():
            await client.aclose()
        print("🔌 Disconnected from bus")


if __name__ == "__main__":
    asyncio.run(inspect_bus())
