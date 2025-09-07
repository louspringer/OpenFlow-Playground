#!/usr/bin/env python3
"""
Bus Peeker - Actually check what's on the Beast Mode bus
"""

import redis
import json
import time


def peek_bus():
    """Peek at the bus to see what's actually there"""
    print("🔍 Beast Mode Bus Peeker")
    print("=" * 30)

    try:
        # Connect to Redis
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        print("✅ Connected to Redis")

        # Check if the channel exists and has messages
        channel = "beast_mode_network"

        # Try different Redis data structures
        print(f"\n📊 Checking channel: {channel}")

        # Check if it's a list
        list_length = r.llen(channel)
        print(f"List length: {list_length}")

        if list_length > 0:
            print("📨 Messages found in list:")
            messages = r.lrange(channel, 0, -1)
            for i, msg in enumerate(messages):
                try:
                    data = json.loads(msg)
                    print(f"  {i+1}. {data}")
                except:
                    print(f"  {i+1}. {msg}")

        # Check if it's a stream
        try:
            streams = r.xread({channel: 0}, count=10)
            if streams:
                print(f"📨 Messages found in stream:")
                for stream, messages in streams:
                    for msg_id, fields in messages:
                        print(f"  {msg_id}: {fields}")
        except:
            print("Not a stream")

        # Check if it's a pub/sub channel (can't peek, but can check if it exists)
        print(f"\n📡 Channel info:")
        print(f"  Channel: {channel}")
        print(f"  Type: pub/sub (can't peek, need to subscribe)")

        # Show how to actually use it
        print(f"\n💡 How to actually use it:")
        print(f"  1. Post a message:")
        print(f'     redis-cli publish {channel} \'{{"test": "message"}}\'')
        print(f"  2. Listen for messages:")
        print(f"     redis-cli subscribe {channel}")
        print(f"  3. Or use Python:")
        print(f"     r.publish('{channel}', 'test message')")

    except redis.ConnectionError:
        print("❌ Redis not running!")
        print("💡 Start Redis: brew services start redis")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    peek_bus()
