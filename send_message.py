#!/usr/bin/env python3
"""
Send a message from a file or stdin
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime
import uuid
import sys


async def send_message_from_file(filename):
    """Send message from file content"""
    try:
        with open(filename, "r") as f:
            message_text = f.read().strip()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return False

    return await send_message(message_text)


async def send_message_from_stdin():
    """Send message from stdin"""
    print("Enter your message (press Ctrl+D when done):")
    message_text = sys.stdin.read().strip()
    return await send_message(message_text)


async def send_message(message_text):
    """Send the actual message"""
    if not message_text:
        print("No message to send")
        return False

    # Connect to Redis
    client = redis.from_url("redis://localhost:6379")
    await client.ping()

    # Create message
    message = {
        "id": str(uuid.uuid4()),
        "type": "simple_message",
        "source": "claude_assistant",
        "target": None,
        "payload": {"message": message_text, "timestamp": datetime.now().isoformat()},
        "timestamp": datetime.now().isoformat(),
        "priority": 5,
    }

    # Send message
    await client.publish("beast_mode_network", json.dumps(message))
    print(f"📤 Sent message: {message_text[:100]}...")

    await client.aclose()
    return True


async def main():
    if len(sys.argv) > 1:
        # Send from file
        filename = sys.argv[1]
        await send_message_from_file(filename)
    else:
        # Send from stdin
        await send_message_from_stdin()


if __name__ == "__main__":
    asyncio.run(main())
