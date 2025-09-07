#!/usr/bin/env python3
"""
Beast Mode Responder Agent
Listens for messages and responds appropriately
"""

import asyncio
import json
import redis.asyncio as redis
import uuid
from datetime import datetime
from typing import Dict, Any


class BeastModeResponder:
    def __init__(self, redis_url="redis://localhost:6379", agent_name="beast_responder"):
        self.redis_url = redis_url
        self.agent_name = agent_name
        self.instance_id = f"{agent_name}_{uuid.uuid4().hex[:8]}"
        self.client = None
        self.message_count = 0

    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.from_url(self.redis_url)
            await self.client.ping()
            print(f"🧬 {self.instance_id} connected to Beast Mode network")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def announce_presence(self):
        """Announce our presence"""
        message = {
            "id": str(uuid.uuid4()),
            "type": "agent_discovery",
            "source": self.instance_id,
            "target": None,
            "payload": {
                "agent_id": self.instance_id,
                "agent_name": self.agent_name,
                "capabilities": ["message_responding", "status_reporting", "collaboration", "task_execution"],
                "availability": "ready_for_collaboration",
                "message": f"Hello! I'm {self.agent_name} ({self.instance_id}). I'm here to respond to messages!",
            },
            "timestamp": datetime.now().isoformat(),
            "priority": 8,
        }

        await self.client.publish("beast_mode_network", json.dumps(message))
        print(f"📡 Announced presence: {self.agent_name}")

    async def respond_to_message(self, original_message: Dict[str, Any]):
        """Respond to a received message"""
        self.message_count += 1

        # Create response based on message type
        if original_message.get("type") == "agent_discovery":
            response = {
                "id": str(uuid.uuid4()),
                "type": "agent_response",
                "source": self.instance_id,
                "target": original_message.get("source"),
                "payload": {
                    "responding_to": original_message.get("id"),
                    "message": f"Hello {original_message.get('source')}! I received your discovery message. I'm {self.agent_name} and I'm ready to collaborate!",
                    "my_capabilities": ["responding", "collaboration", "status_updates"],
                    "status": "active_and_responding",
                },
                "timestamp": datetime.now().isoformat(),
                "priority": 6,
            }
        elif original_message.get("type") == "collaboration_request":
            response = {
                "id": str(uuid.uuid4()),
                "type": "collaboration_response",
                "source": self.instance_id,
                "target": original_message.get("source"),
                "payload": {
                    "responding_to": original_message.get("id"),
                    "request_type": original_message.get("payload", {}).get("request_type", "unknown"),
                    "message": f"I received your {original_message.get('payload', {}).get('request_type', 'request')}! Here's my status: I'm active, responding to messages, and ready to help.",
                    "status_report": {
                        "agent_id": self.instance_id,
                        "status": "active",
                        "messages_processed": self.message_count,
                        "capabilities": ["responding", "collaboration", "status_updates"],
                        "last_activity": datetime.now().isoformat(),
                    },
                },
                "timestamp": datetime.now().isoformat(),
                "priority": 7,
            }
        else:
            # Generic response
            response = {
                "id": str(uuid.uuid4()),
                "type": "agent_response",
                "source": self.instance_id,
                "target": original_message.get("source"),
                "payload": {
                    "responding_to": original_message.get("id"),
                    "message": f"I received your {original_message.get('type', 'message')}! I'm {self.agent_name} and I'm here to help.",
                    "status": "active_and_responding",
                },
                "timestamp": datetime.now().isoformat(),
                "priority": 5,
            }

        # Send the response
        await self.client.publish("beast_mode_network", json.dumps(response))
        print(f"📤 Responded to {original_message.get('source', 'unknown')} with {response['type']}")

    async def listen_and_respond(self, duration_seconds=60):
        """Listen for messages and respond"""
        pubsub = self.client.pubsub()
        await pubsub.subscribe("beast_mode_network")

        print(f"👂 Listening for messages for {duration_seconds} seconds...")
        print("=" * 50)

        start_time = datetime.now()

        try:
            async for raw_message in pubsub.listen():
                if raw_message["type"] == "message":
                    try:
                        data = json.loads(raw_message["data"])

                        # Skip our own messages
                        if data.get("source") == self.instance_id:
                            continue

                        print(f"\n🧬 RECEIVED MESSAGE #{self.message_count + 1}")
                        print(f"   From: {data.get('source', 'unknown')}")
                        print(f"   Type: {data.get('type', 'unknown')}")
                        print(f"   Message: {data.get('payload', {}).get('message', 'no message')}")

                        # Respond to the message
                        await self.respond_to_message(data)

                    except Exception as e:
                        print(f"❌ Error processing message: {e}")
                        print(f"   Raw data: {raw_message['data']}")

                # Check if we should stop
                if (datetime.now() - start_time).total_seconds() >= duration_seconds:
                    break

        except Exception as e:
            print(f"❌ Error listening: {e}")
        finally:
            await pubsub.close()

    async def disconnect(self):
        """Disconnect from network"""
        if self.client:
            await self.client.close()
        print(f"👋 {self.instance_id} disconnected")


async def main():
    """Main function"""
    responder = BeastModeResponder(agent_name="beast_responder")

    # Connect
    if not await responder.connect():
        return

    # Announce presence
    await responder.announce_presence()

    # Listen and respond
    await responder.listen_and_respond(duration_seconds=120)

    # Disconnect
    await responder.disconnect()

    print(f"\n📊 Session Summary:")
    print(f"   Messages processed: {responder.message_count}")
    print(f"   Agent ID: {responder.instance_id}")


if __name__ == "__main__":
    asyncio.run(main())
