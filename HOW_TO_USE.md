# 🚀 How to Use the Beast Mode Agent Collaboration Network

## **What We Built**

We created a complete **Agent Collaboration Network** with:

✅ **Agent Discovery** - Agents automatically find each other\
✅ **Help Wanted System** - Agents can request and offer help\
✅ **Message Types** - 12 standardized message types for communication\
✅ **Trust Scoring** - Agents build trust based on successful collaborations\
✅ **Redis Pub/Sub** - Fast, reliable message delivery

## **Quick Start**

### 1. **Start Redis** (Required)

```bash
# macOS
brew install redis
redis-server

# Ubuntu/Debian  
sudo apt-get install redis-server
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

### 2. **Run the Demo**

```bash
# Quick demo
uv run python quick_demo.py

# Complete example
uv run python examples/my_agent.py
```

## **How to Build Your Own Agent**

### **Basic Agent Template**

```python
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from beast_mode.message_models_dataclass import BeastModeMessage, MessageType
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager

class MyAgent:
    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities
        
        # Initialize components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)
    
    async def start(self):
        """Start the agent."""
        await self.redis_manager.connect()
        await self.discovery_manager.announce_presence()
        print(f"✅ {self.agent_id} is ready!")
    
    async def stop(self):
        """Stop the agent."""
        await self.redis_manager.disconnect()
    
    async def send_message(self, target_agent: str, message_text: str):
        """Send a message to another agent."""
        message = BeastModeMessage(
            type=MessageType.SIMPLE_MESSAGE,
            source=self.agent_id,
            target=target_agent,
            payload={"message": message_text}
        )
        await self.redis_manager.publish("beast_mode_network", message.to_json())
    
    async def request_help(self, required_capabilities: list, description: str):
        """Request help from other agents."""
        return await self.help_manager.request_help(required_capabilities, description)

# Usage
async def main():
    agent = MyAgent("my_agent", ["python_coding", "gcp_optimization"])
    await agent.start()
    
    # Send a message
    await agent.send_message("broadcast", "Hello world!")
    
    # Request help
    await agent.request_help(["python_coding"], "I need help with Python")
    
    await agent.stop()

asyncio.run(main())
```

## **What You Can Do**

### **1. Agent Discovery**

```python
# Discover other agents
discovered_agents = await agent.discovery_manager.get_discovered_agents()
for agent_info in discovered_agents:
    print(f"Found: {agent_info.agent_id} - {agent_info.capabilities}")
```

### **2. Send Messages**

```python
# Send to specific agent
await agent.send_message("other_agent", "Hello!")

# Broadcast to all
await agent.send_message("broadcast", "Hello everyone!")
```

### **3. Request Help**

```python
# Request help with specific capabilities
request_id = await agent.request_help(
    required_capabilities=["python_coding", "gcp_optimization"],
    description="I need help building a cost optimization tool"
)
```

### **4. Use Different Message Types**

```python
# Simple message
message = BeastModeMessage(
    type=MessageType.SIMPLE_MESSAGE,
    source="my_agent",
    payload={"message": "Hello!"}
)

# Prompt request
message = BeastModeMessage(
    type=MessageType.PROMPT_REQUEST,
    source="my_agent",
    payload={
        "prompt_type": "cost_analysis",
        "prompt_data": {"query": "What are the costs?"}
    }
)

# System health check
message = BeastModeMessage(
    type=MessageType.SYSTEM_HEALTH,
    source="my_agent",
    payload={"check_type": "redis_connection"}
)
```

## **Available Message Types**

- `simple_message` - Basic text communication
- `prompt_request` - Request for processing
- `prompt_response` - Response to request
- `agent_discovery` - Presence announcement
- `agent_response` - Discovery response
- `help_wanted` - Request for assistance
- `help_response` - Offer to help
- `spore_delivery` - Spore sharing
- `spore_request` - Request for specific spore
- `technical_exchange` - Setup/debugging info
- `system_health` - Health monitoring
- `processor_response` - Automated responses

## **Real-World Example**

Here's how you might use it for **GCP Cost Optimization**:

```python
# Create a cost optimization agent
cost_agent = MyAgent("cost_optimizer", ["gcp_optimization", "cost_analysis"])

# Discover other agents
await cost_agent.start()
discovered = await cost_agent.discover_agents()

# Request help from Python experts
await cost_agent.request_help(
    ["python_coding"],
    "I need help building a GCP cost analysis tool"
)

# Send cost data to other agents
await cost_agent.send_message("broadcast", "Current GCP costs: $6.50/month")
```

## **What's Next**

The system is ready for **Tasks 7-9**:

- **Task 7**: Persistent mailbox logger
- **Task 8**: Message history and retrieval
- **Task 9**: Spore management system

## **Files Created**

- `src/beast_mode/` - Core system components
- `examples/` - Working examples
- `tests/` - Comprehensive test suite
- `docs/` - Complete documentation
- `quick_demo.py` - Quick start demo
- `HOW_TO_USE.md` - This guide

## **🎉 You're Ready!**

The Beast Mode Agent Collaboration Network is **fully functional** and ready to use. You can:

1. **Create agents** that discover each other
1. **Send messages** between agents
1. **Request help** with specific capabilities
1. **Track collaboration** success
1. **Build trust networks** between agents

**No magic required** - just Redis and Python! 🚀
