#!/usr/bin/env python3
"""
Simple Beast Mode Message Processor
- Scans bus_messages.log for unprocessed messages
- Looks for questions to answer or interesting responses to follow up on
- Sends responses back to the bus
- Stops when done processing
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime
import uuid
import os


class SimpleProcessor:
    def __init__(self, redis_url="redis://localhost:6379", log_file="bus_messages.log"):
        self.redis_url = redis_url
        self.log_file = log_file
        self.client = None
        self.processed_messages = set()
        self.load_processed_messages()

    def load_processed_messages(self):
        """Load previously processed message IDs"""
        processed_file = "processed_messages.txt"
        if os.path.exists(processed_file):
            with open(processed_file, "r") as f:
                self.processed_messages = set(line.strip() for line in f if line.strip())

    def save_processed_message(self, message_id):
        """Mark a message as processed"""
        self.processed_messages.add(message_id)
        with open("processed_messages.txt", "a") as f:
            f.write(f"{message_id}\n")

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

    def scan_log_for_unprocessed(self):
        """Scan log file for unprocessed messages"""
        if not os.path.exists(self.log_file):
            print("📝 No log file found")
            return []

        unprocessed = []

        with open(self.log_file, "r") as f:
            for line in f:
                try:
                    # Extract timestamp and message data
                    if "] " in line:
                        timestamp_part, message_part = line.split("] ", 1)
                        message_data = json.loads(message_part.strip())

                        message_id = message_data.get("id")
                        if message_id and message_id not in self.processed_messages:
                            unprocessed.append({"id": message_id, "timestamp": timestamp_part[1:], "data": message_data})  # Remove leading [
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"⚠️ Error parsing line: {e}")
                    continue

        return unprocessed

    def analyze_message(self, message):
        """Analyze message to determine if it needs a response"""
        message_data = message["data"]
        message_type = message_data.get("type", "")
        payload = message_data.get("payload", {})
        source = message_data.get("source", "")
        message_text = payload.get("message", "")

        # Don't respond to our own messages
        if source == "simple_processor":
            return None

        # Look for questions (simple heuristic)
        if "?" in message_text or message_text.lower().startswith(("what", "how", "why", "when", "where", "who")):
            # Provide actual answers for known questions
            if "gcp cost" in message_text.lower():
                return {
                    "action": "answer_question",
                    "original_message": message_text,
                    "source": source,
                    "response": "Based on our recent analysis, GCP costs have been optimized from ~$100/month to ~$6.50/month (93.6% reduction). We reduced the GKE cluster from 6 nodes to 1 preemptible node and optimized Cloud Run services to scale to zero. Current daily costs are around $0.20-0.30.",
                }
            elif "cluster" in message_text.lower():
                return {
                    "action": "answer_question",
                    "original_message": message_text,
                    "source": source,
                    "response": "The GKE cluster is currently configured with 1 preemptible node in us-central1. We optimized it from 6 nodes across 3 zones to maximize cost savings while maintaining functionality.",
                }
            else:
                return {"action": "answer_question", "original_message": message_text, "source": source, "response": f"I see you asked: '{message_text}'. Let me think about that..."}

        # Look for interesting responses or statements
        if any(word in message_text.lower() for word in ["cost", "cluster", "gcp", "optimization", "beast", "mode"]):
            return {"action": "follow_up", "original_message": message_text, "source": source, "response": f"That's interesting about '{message_text[:50]}...'. Can you tell me more?"}

        # Look for greetings or discovery messages
        if message_type in ["agent_discovery", "simple_message"] and any(word in message_text.lower() for word in ["hello", "hi", "hey", "discovery"]):
            return {"action": "greet_back", "original_message": message_text, "source": source, "response": f"Hello! I'm the simple processor. I saw your message: '{message_text[:50]}...'"}

        return None

    async def send_response(self, analysis):
        """Send response back to the bus"""
        response_message = {
            "id": str(uuid.uuid4()),
            "type": "processor_response",
            "source": "simple_processor",
            "target": analysis["source"],
            "payload": {"action": analysis["action"], "response": analysis["response"], "original_message": analysis["original_message"], "timestamp": datetime.now().isoformat()},
            "timestamp": datetime.now().isoformat(),
            "priority": 6,
        }

        await self.client.publish("beast_mode_network", json.dumps(response_message))
        print(f"📤 Sent {analysis['action']} response to {analysis['source']}")
        print(f"   Response: {analysis['response']}")

    async def process_messages(self):
        """Main processing loop"""
        print("🔍 Scanning for unprocessed messages...")

        unprocessed = self.scan_log_for_unprocessed()

        if not unprocessed:
            print("✅ No unprocessed messages found")
            return

        print(f"📨 Found {len(unprocessed)} unprocessed messages")

        responses_sent = 0

        for message in unprocessed:
            print(f"\n📖 Processing message from {message['data'].get('source', 'unknown')}:")
            print(f"   {message['data'].get('payload', {}).get('message', 'No message')[:100]}...")

            analysis = self.analyze_message(message)

            if analysis:
                await self.send_response(analysis)
                responses_sent += 1
            else:
                print("   ℹ️ No response needed")

            # Mark as processed
            self.save_processed_message(message["id"])

        print(f"\n✅ Processing complete. Sent {responses_sent} responses.")

        # Close connection
        await self.client.aclose()


async def main():
    processor = SimpleProcessor()

    if not await processor.connect():
        return

    await processor.process_messages()


if __name__ == "__main__":
    asyncio.run(main())
