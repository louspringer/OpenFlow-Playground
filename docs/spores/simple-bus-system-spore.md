# 🧬 Beast Mode Simple Bus System Spore

## Spore Metadata

- **Spore Type**: Simple Message Bus System
- **Target Platform**: Any system with Python 3.7+ and Redis
- **DNA Version**: 1.0 (Minimal message bus implementation)
- **Compatibility**: Universal (Works on macOS, Linux, Windows)
- **Purpose**: Enable simple message logging and sending between agents
- **Validation**: Tested and working

## 🎯 Spore Mission

Provide a dead-simple message bus system where agents can log messages and send responses when they have time.

______________________________________________________________________

## 🚀 Quick Start (Under 2 Minutes)

### Step 1: Install Redis

```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt install redis-server
sudo systemctl start redis-server

# Test connection
redis-cli ping
# Should return: PONG
```

### Step 2: Install Python Dependencies

```bash
pip install redis pydantic
```

### Step 3: Download the Three Scripts

Save these three files in your working directory:

______________________________________________________________________

## 📁 The Three Scripts

### 1. `simple_listener.py` - Logs Messages Forever

```python
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
                if raw_message['type'] == 'message':
                    timestamp = datetime.now().isoformat()
                    message_data = raw_message['data'].decode('utf-8')
                    
                    # Log to file
                    with open(self.log_file, 'a') as f:
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
```

### 2. `simple_sender.py` - Sends Messages and Dies

```python
#!/usr/bin/env python3
"""
Simple Beast Mode Bus Sender
- Puts a message on the bus
- Dies immediately after sending
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime
import uuid

class SimpleSender:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis_url = redis_url
        self.client = None
        
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
    
    async def send_message(self, message_text):
        """Send a message and die"""
        message = {
            "id": str(uuid.uuid4()),
            "type": "simple_message",
            "source": "simple_sender",
            "target": None,
            "payload": {
                "message": message_text,
                "timestamp": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat(),
            "priority": 5
        }
        
        await self.client.publish("beast_mode_network", json.dumps(message))
        print(f"📤 Sent message: {message_text}")
        
        # Die immediately
        await self.client.aclose()
        print("💀 Sender died")

async def main():
    import sys
    
    # Get message from command line or use default
    message_text = sys.argv[1] if len(sys.argv) > 1 else "Hello from simple sender!"
    
    sender = SimpleSender()
    
    if not await sender.connect():
        return
    
    await sender.send_message(message_text)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. `simple_processor.py` - Dumb Rule-Based Processor (Optional)

```python
#!/usr/bin/env python3
"""
Simple Beast Mode Message Processor
- Scans bus_messages.log for unprocessed messages
- Uses dumb rules to respond (not an LLM)
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
            with open(processed_file, 'r') as f:
                self.processed_messages = set(line.strip() for line in f if line.strip())
    
    def save_processed_message(self, message_id):
        """Mark a message as processed"""
        self.processed_messages.add(message_id)
        with open("processed_messages.txt", 'a') as f:
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
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    # Extract timestamp and message data
                    if '] ' in line:
                        timestamp_part, message_part = line.split('] ', 1)
                        message_data = json.loads(message_part.strip())
                        
                        message_id = message_data.get('id')
                        if message_id and message_id not in self.processed_messages:
                            unprocessed.append({
                                'id': message_id,
                                'timestamp': timestamp_part[1:],  # Remove leading [
                                'data': message_data
                            })
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"⚠️ Error parsing line: {e}")
                    continue
        
        return unprocessed
    
    def analyze_message(self, message):
        """Analyze message to determine if it needs a response"""
        message_data = message['data']
        message_type = message_data.get('type', '')
        payload = message_data.get('payload', {})
        source = message_data.get('source', '')
        message_text = payload.get('message', '')
        
        # Don't respond to our own messages
        if source == 'simple_processor':
            return None
        
        # Look for questions (simple heuristic)
        if '?' in message_text or message_text.lower().startswith(('what', 'how', 'why', 'when', 'where', 'who')):
            # Provide actual answers for known questions
            if 'gcp cost' in message_text.lower():
                return {
                    'action': 'answer_question',
                    'original_message': message_text,
                    'source': source,
                    'response': "Based on our recent analysis, GCP costs have been optimized from ~$100/month to ~$6.50/month (93.6% reduction). We reduced the GKE cluster from 6 nodes to 1 preemptible node and optimized Cloud Run services to scale to zero. Current daily costs are around $0.20-0.30."
                }
            elif 'cluster' in message_text.lower():
                return {
                    'action': 'answer_question',
                    'original_message': message_text,
                    'source': source,
                    'response': "The GKE cluster is currently configured with 1 preemptible node in us-central1. We optimized it from 6 nodes across 3 zones to maximize cost savings while maintaining functionality."
                }
            else:
                return {
                    'action': 'answer_question',
                    'original_message': message_text,
                    'source': source,
                    'response': f"I see you asked: '{message_text}'. Let me think about that..."
                }
        
        # Look for interesting responses or statements
        if any(word in message_text.lower() for word in ['cost', 'cluster', 'gcp', 'optimization', 'beast', 'mode']):
            return {
                'action': 'follow_up',
                'original_message': message_text,
                'source': source,
                'response': f"That's interesting about '{message_text[:50]}...'. Can you tell me more?"
            }
        
        # Look for greetings or discovery messages
        if message_type in ['agent_discovery', 'simple_message'] and any(word in message_text.lower() for word in ['hello', 'hi', 'hey', 'discovery']):
            return {
                'action': 'greet_back',
                'original_message': message_text,
                'source': source,
                'response': f"Hello! I'm the simple processor. I saw your message: '{message_text[:50]}...'"
            }
        
        return None
    
    async def send_response(self, analysis):
        """Send response back to the bus"""
        response_message = {
            "id": str(uuid.uuid4()),
            "type": "processor_response",
            "source": "simple_processor",
            "target": analysis['source'],
            "payload": {
                "action": analysis['action'],
                "response": analysis['response'],
                "original_message": analysis['original_message'],
                "timestamp": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat(),
            "priority": 6
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
            self.save_processed_message(message['id'])
        
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
```

______________________________________________________________________

## 🎯 How to Use

### Start the Listener (Background)

```bash
python simple_listener.py
```

This runs forever and logs all messages to `bus_messages.log`

### Send a Message

```bash
python simple_sender.py "Your message here"
```

This sends a message and dies immediately

### Check the Log

```bash
cat bus_messages.log
tail -f bus_messages.log  # Follow in real-time
```

### Process Messages (Optional)

```bash
python simple_processor.py
```

This uses dumb rules to respond (not an LLM)

______________________________________________________________________

## 🧬 What This Gets You

### Immediate Message Bus

- ✅ **Message Logging** - All messages saved to file
- ✅ **Message Sending** - Send messages and die
- ✅ **Simple Processing** - Basic rule-based responses
- ✅ **No Dependencies** - Just Redis and Python

### Ready for Enhancement

- 🔧 **LLM Integration** - Replace processor with real LLM
- 🔧 **Message Routing** - Add targeted messaging
- 🔧 **Persistence** - Messages logged forever
- 🔧 **Simple** - Dead simple to use

______________________________________________________________________

## 🎉 Success Criteria

### You're Connected When:

- [ ] Redis responds to `redis-cli ping` with `PONG`
- [ ] Listener connects without errors
- [ ] You see "Listening for messages" message
- [ ] Messages appear in `bus_messages.log`

### You're Ready for Business When:

- [ ] You can send messages with `simple_sender.py`
- [ ] Messages appear in the log file
- [ ] You can read the log to see what's happening
- [ ] You can respond when you have time

______________________________________________________________________

## 🔧 Troubleshooting

### Redis Connection Issues

```bash
# Check if Redis is running
redis-cli ping

# Start Redis if needed
brew services start redis  # macOS
sudo systemctl start redis-server  # Linux
```

### Python Dependencies

```bash
# Install missing packages
pip install redis pydantic
```

### Network Issues

- Check firewall settings for Redis port 6379
- Ensure Redis is bound to correct interface
- Verify no other services using port 6379

______________________________________________________________________

## 🧬 Ready for Simple Message Bus!

**Setup Time**: Under 2 minutes\
**Message Logging**: Immediate\
**Message Sending**: Immediate\
**Intelligence**: Manual (you read the log and decide)

**Your system is now ready for simple message bus communication!** 🚀

The beauty is in the simplicity - log messages, send when you want, read when you have time. No complex protocols, no fancy features, just dead simple message passing.
