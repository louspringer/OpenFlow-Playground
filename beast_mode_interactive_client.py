#!/usr/bin/env python3
"""
Beast Mode Interactive Bus Client - With Actual Usage Instructions!
"""

import asyncio
import json
import uuid
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

try:
    import redis.asyncio as redis
    from pydantic import BaseModel
except ImportError:
    print("Installing dependencies...")
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "redis", "pydantic"])
    import redis.asyncio as redis
    from pydantic import BaseModel


class MessageType(str, Enum):
    AGENT_DISCOVERY = "agent_discovery"
    AGENT_RESPONSE = "agent_response"
    HELP_WANTED = "help_wanted"
    HELP_RESPONSE = "help_response"
    PROMPT_REQUEST = "prompt_request"
    PROMPT_RESPONSE = "prompt_response"
    SPORE_REQUEST = "spore_request"
    SYSTEM_HEALTH = "system_health"


class BeastModeMessage(BaseModel):
    id: str
    type: MessageType
    source: str
    target: Optional[str]
    payload: Dict[str, Any]
    timestamp: datetime
    priority: int = 5


class BeastModeInteractiveClient:
    """Interactive Beast Mode network client with actual usage!"""

    def __init__(self, redis_url="redis://localhost:6379", capabilities=None):
        self.redis_url = redis_url
        self.instance_id = f"beast_mode_{uuid.uuid4().hex[:8]}"
        self.capabilities = capabilities or ["basic_participation", "message_relay"]
        self.client = None
        self.is_connected = False
        self.running = True

    async def connect(self):
        """Connect to Beast Mode network"""
        try:
            self.client = redis.from_url(self.redis_url)
            await self.client.ping()
            self.is_connected = True
            print(f"🧬 {self.instance_id} connected to Beast Mode network")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    async def announce_presence(self):
        """Announce presence to the network"""
        message = BeastModeMessage(
            id=str(uuid.uuid4()),
            type=MessageType.AGENT_DISCOVERY,
            source=self.instance_id,
            target=None,
            payload={
                "agent_id": self.instance_id,
                "capabilities": self.capabilities,
                "availability": "ready_for_business",
                "message": f"Hi! I'm {self.instance_id}. My capabilities are {self.capabilities}. Is anybody out there?",
            },
            timestamp=datetime.now(),
            priority=8,
        )

        await self.client.publish("beast_mode_network", message.model_dump_json())
        print(f"📡 Announced presence with capabilities: {self.capabilities}")

    async def listen_for_messages(self):
        """Listen for network messages in background"""
        pubsub = self.client.pubsub()
        await pubsub.subscribe("beast_mode_network")

        print("📥 Listening for Beast Mode network messages...")

        async for raw_message in pubsub.listen():
            if not self.running:
                break
            if raw_message["type"] == "message":
                try:
                    data = json.loads(raw_message["data"])
                    message = BeastModeMessage(**data)

                    # Don't process our own messages
                    if message.source == self.instance_id:
                        continue

                    await self.handle_message(message)

                except Exception as e:
                    print(f"❌ Error processing message: {e}")

    async def handle_message(self, message: BeastModeMessage):
        """Handle incoming messages"""
        print(f"\n🧬 Received {message.type} from {message.source}")

        if message.type == MessageType.AGENT_DISCOVERY:
            await self.respond_to_discovery(message)
        elif message.type == MessageType.HELP_WANTED:
            await self.check_help_request(message)
        elif message.type == MessageType.PROMPT_REQUEST:
            await self.handle_prompt(message)
        else:
            print(f"   📝 {message.payload.get('message', 'No message')}")

    async def respond_to_discovery(self, message: BeastModeMessage):
        """Respond to agent discovery"""
        discovering_agent = message.payload.get("agent_id", message.source)

        response = BeastModeMessage(
            id=str(uuid.uuid4()),
            type=MessageType.AGENT_RESPONSE,
            source=self.instance_id,
            target=discovering_agent,
            payload={
                "agent_id": self.instance_id,
                "capabilities": self.capabilities,
                "availability": "ready_for_business",
                "message": f"Hi {discovering_agent}! I'm {self.instance_id}. I'm here and ready!",
            },
            timestamp=datetime.now(),
            priority=7,
        )

        await self.client.publish("beast_mode_network", response.model_dump_json())
        print(f"👋 Responded to discovery from {discovering_agent}")

    async def check_help_request(self, message: BeastModeMessage):
        """Check if we can help with a request"""
        required_caps = message.payload.get("required_capabilities", [])
        task_desc = message.payload.get("task_description", "")

        can_help = any(cap in self.capabilities for cap in required_caps) if required_caps else True

        if can_help:
            response = BeastModeMessage(
                id=str(uuid.uuid4()),
                type=MessageType.HELP_RESPONSE,
                source=self.instance_id,
                target=message.source,
                payload={"available": True, "matching_capabilities": [cap for cap in required_caps if cap in self.capabilities], "message": f"I can help with: {task_desc}"},
                timestamp=datetime.now(),
                priority=8,
            )

            await self.client.publish("beast_mode_network", response.model_dump_json())
            print(f"🤝 Offered help for: {task_desc}")

    async def handle_prompt(self, message: BeastModeMessage):
        """Handle prompt requests"""
        prompt = message.payload.get("prompt", "")
        print(f"🤖 Received prompt: {prompt[:50]}...")

        response = BeastModeMessage(
            id=str(uuid.uuid4()),
            type=MessageType.PROMPT_RESPONSE,
            source=self.instance_id,
            target=message.source,
            payload={"response": f"Echo from {self.instance_id}: {prompt}", "status": "processed"},
            timestamp=datetime.now(),
            priority=6,
        )

        await self.client.publish("beast_mode_network", response.model_dump_json())
        print(f"✅ Responded to prompt from {message.source}")

    async def send_help_request(self, task_description: str, required_capabilities: list = None):
        """Send a help request to the network"""
        payload = {"task_description": task_description, "required_capabilities": required_capabilities or [], "urgency": "normal"}

        await self.send_message(MessageType.HELP_WANTED, payload, priority=8)
        print(f"🆘 Sent help request: {task_description}")

    async def send_prompt(self, prompt: str):
        """Send a prompt to the network"""
        payload = {"prompt": prompt, "context": "general"}

        await self.send_message(MessageType.PROMPT_REQUEST, payload, priority=6)
        print(f"🤖 Sent prompt: {prompt[:50]}...")

    async def request_spore(self, spore_type: str, description: str):
        """Request a specific spore from the network"""
        payload = {"spore_type": spore_type, "description": description, "requirements": "ready_to_deploy"}

        await self.send_message(MessageType.SPORE_REQUEST, payload, priority=7)
        print(f"🧬 Requested spore: {spore_type}")

    async def send_message(self, message_type: MessageType, payload: dict, target=None, priority=5):
        """Send a message to the network"""
        message = BeastModeMessage(id=str(uuid.uuid4()), type=message_type, source=self.instance_id, target=target, payload=payload, timestamp=datetime.now(), priority=priority)

        await self.client.publish("beast_mode_network", message.model_dump_json())

    async def disconnect(self):
        """Disconnect from network"""
        self.running = False
        if self.client:
            await self.client.aclose()
        print(f"🔌 {self.instance_id} disconnected")

    def show_menu(self):
        """Show interactive menu"""
        print("\n" + "=" * 50)
        print("🧬 Beast Mode Interactive Commands")
        print("=" * 50)
        print("1. Send Help Request - Ask for specific capabilities")
        print("2. Send Prompt - Send a prompt to the network")
        print("3. Request Spore - Ask for a specific spore")
        print("4. Announce Capabilities - Broadcast your skills")
        print("5. Show Status - Display current status")
        print("6. Quit - Exit the client")
        print("=" * 50)

    async def interactive_loop(self):
        """Main interactive loop"""
        while self.running:
            try:
                self.show_menu()
                choice = input("\nEnter command number (1-6): ").strip()

                if choice == "1":
                    task = input("Enter task description: ").strip()
                    caps = input("Enter required capabilities (comma-separated, or press Enter for any): ").strip()
                    required_caps = [cap.strip() for cap in caps.split(",")] if caps else []
                    await self.send_help_request(task, required_caps)

                elif choice == "2":
                    prompt = input("Enter your prompt: ").strip()
                    await self.send_prompt(prompt)

                elif choice == "3":
                    spore_type = input("Enter spore type: ").strip()
                    description = input("Enter description: ").strip()
                    await self.request_spore(spore_type, description)

                elif choice == "4":
                    await self.announce_presence()

                elif choice == "5":
                    print(f"\n📊 Status:")
                    print(f"   Agent ID: {self.instance_id}")
                    print(f"   Capabilities: {self.capabilities}")
                    print(f"   Connected: {self.is_connected}")
                    print(f"   Running: {self.running}")

                elif choice == "6":
                    print("🛑 Shutting down...")
                    self.running = False
                    break

                else:
                    print("❌ Invalid choice. Please enter 1-6.")

            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Main client function"""
    print("🧬 Beast Mode Interactive Bus Client")
    print("=" * 40)

    # Customize your capabilities here!
    my_capabilities = ["basic_participation", "message_relay", "echo_service", "python_coding", "systematic_analysis", "prompt_processing"]

    client = BeastModeInteractiveClient(capabilities=my_capabilities)

    try:
        # Connect to network
        if not await client.connect():
            return

        # Announce presence
        await client.announce_presence()

        # Start listening in background
        listen_task = asyncio.create_task(client.listen_for_messages())

        # Start interactive loop
        await client.interactive_loop()

        # Cancel listening task
        listen_task.cancel()

    except KeyboardInterrupt:
        print("\n🛑 Disconnecting from Beast Mode network...")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
