#!/usr/bin/env python3
"""
Send Simple Bus System Spore to kiro_spore_creator
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime
import uuid


async def send_spore():
    """Send the simple bus system spore"""

    # Connect to Redis
    client = redis.from_url("redis://localhost:6379")
    await client.ping()

    # Read the spore content
    with open("docs/spores/simple-bus-system-spore.md", "r") as f:
        spore_content = f.read()

    # Create the spore message
    spore_message = {
        "id": str(uuid.uuid4()),
        "type": "spore_delivery",
        "source": "openflow_playground",
        "target": "kiro_spore_creator",
        "payload": {
            "spore_type": "Simple Bus System",
            "spore_content": spore_content,
            "description": "Dead simple message bus system with listener, sender, and processor scripts",
            "purpose": "Enable simple message logging and sending between agents",
            "timestamp": datetime.now().isoformat(),
        },
        "timestamp": datetime.now().isoformat(),
        "priority": 8,
    }

    # Send the spore
    await client.publish("beast_mode_network", json.dumps(spore_message))
    print("📤 Sent Simple Bus System Spore to kiro_spore_creator")
    print(f"   Spore ID: {spore_message['id']}")
    print(f"   Content length: {len(spore_content)} characters")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(send_spore())
