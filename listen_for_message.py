#!/usr/bin/env python3
"""
Listen for Message - Wait for first message on Beast Mode bus
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime


async def listen_for_first_message():
    """Listen for the first message on the bus"""
    print("👂 Listening for first message on Beast Mode bus...")
    print("Channel: beast_mode_network")
    print("Waiting for any message...")
    print("=" * 50)

    try:
        # Connect to Redis
        client = redis.from_url("redis://localhost:6379")
        await client.ping()
        print("✅ Connected to Redis")

        # Subscribe to the channel
        pubsub = client.pubsub()
        await pubsub.subscribe("beast_mode_network")
        print("📡 Subscribed to 'beast_mode_network'")
        print("⏳ Waiting for message...")

        # Listen for the first message
        async for raw_message in pubsub.listen():
            if raw_message["type"] == "message":
                print(f"\n🎉 MESSAGE RECEIVED!")
                print("=" * 30)
                print(f"Raw data: {raw_message['data']}")

                # Try to parse as JSON, but handle raw text too
                try:
                    data = json.loads(raw_message["data"])
                    print(f"Parsed JSON: {data}")
                except:
                    print(f"Raw text: {raw_message['data']}")

                print("=" * 30)
                print("✅ First message received - stopping!")
                break

    except redis.ConnectionError:
        print("❌ Redis not running!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if "client" in locals():
            await client.aclose()
        print("🔌 Disconnected")


if __name__ == "__main__":
    asyncio.run(listen_for_first_message())
