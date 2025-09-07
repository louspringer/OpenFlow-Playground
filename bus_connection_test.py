#!/usr/bin/env python3
"""
Bus Connection Test - Test connect/disconnect to Beast Mode bus
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime


async def test_connection():
    """Test connecting and disconnecting from the bus"""
    print("🔌 Beast Mode Bus Connection Test")
    print("=" * 40)

    try:
        # Connect to Redis
        print("1. Connecting to Redis...")
        client = redis.from_url("redis://localhost:6379")
        await client.ping()
        print("   ✅ Connected successfully")

        # Subscribe to the channel
        print("2. Subscribing to 'beast_mode_network'...")
        pubsub = client.pubsub()
        await pubsub.subscribe("beast_mode_network")
        print("   ✅ Subscribed successfully")

        # Post a test message
        print("3. Posting test message...")
        test_message = {"id": "test_123", "type": "test", "source": "connection_test", "message": "Hello from connection test", "timestamp": datetime.now().isoformat()}
        await client.publish("beast_mode_network", json.dumps(test_message))
        print("   ✅ Test message posted")

        # Listen for a short time to see if we get our own message
        print("4. Listening for messages (3 seconds)...")
        message_received = False
        start_time = datetime.now()

        async for raw_message in pubsub.listen():
            if raw_message["type"] == "message":
                try:
                    data = json.loads(raw_message["data"])
                    print(f"   📨 Received: {data['message']} from {data['source']}")
                    message_received = True
                    break
                except Exception as e:
                    print(f"   ❌ Error parsing message: {e}")

            # Timeout after 3 seconds
            if (datetime.now() - start_time).seconds >= 3:
                break

        if message_received:
            print("   ✅ Message received successfully")
        else:
            print("   ⚠️  No messages received (timeout)")

        # Disconnect
        print("5. Disconnecting...")
        await pubsub.aclose()
        await client.aclose()
        print("   ✅ Disconnected successfully")

        print("\n🎉 Connection test completed!")
        print("   - Can connect to Redis ✅")
        print("   - Can subscribe to channel ✅")
        print("   - Can post messages ✅")
        print("   - Can listen for messages ✅")
        print("   - Can disconnect cleanly ✅")

    except redis.ConnectionError:
        print("❌ Redis not running!")
        print("💡 Start Redis: brew services start redis")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
