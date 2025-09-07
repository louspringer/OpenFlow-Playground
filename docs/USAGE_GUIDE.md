# Beast Mode Agent Collaboration Network - Usage Guide

## 🚀 Quick Start

### Prerequisites

1. **Redis Server**: Install and start Redis

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

1. **Python Dependencies**: Install with UV

   ```bash
   uv sync
   ```

### Basic Usage

#### 1. Create a Simple Agent

```python
import asyncio
from beast_mode.redis_foundation import RedisConnectionManager
from beast_mode.agent_discovery import AgentDiscoveryManager
from beast_mode.help_system import HelpSystemManager
from beast_mode.bus_client import BeastModeBusClient

class MyAgent:
    def __init__(self, agent_id: str, capabilities: list):
        self.agent_id = agent_id
        self.capabilities = capabilities
        
        # Initialize components
        self.redis_manager = RedisConnectionManager()
        self.discovery_manager = AgentDiscoveryManager(agent_id, capabilities, self.redis_manager)
        self.help_manager = HelpSystemManager(agent_id, self.discovery_manager)
        self.bus_client = BeastModeBusClient(agent_id, capabilities)
    
    async def start(self):
        # Connect to Redis
        await self.redis_manager.connect()
        
        # Connect bus client
        await self.bus_client.connect()
        
        # Announce presence
        await self.discovery_manager.announce_presence()
        
        # Start listening
        await self.bus_client.start_listening()
        
        print(f"Agent {self.agent_id} is ready!")
    
    async def stop(self):
        await self.bus_client.disconnect()
        await self.redis_manager.disconnect()

# Usage
async def main():
    agent = MyAgent("my_agent", ["python_coding", "gcp_optimization"])
    await agent.start()
    
    # Your agent is now running and can communicate with others!
    
    await agent.stop()

asyncio.run(main())
```

#### 2. Send Messages

```python
from beast_mode.message_models_dataclass import BeastModeMessage, MessageType

# Send a simple message
message = BeastModeMessage(
    type=MessageType.SIMPLE_MESSAGE,
    source="my_agent",
    target="other_agent",  # or None for broadcast
    payload={"message": "Hello from my agent!"}
)

await agent.bus_client.send_message(message)
```

#### 3. Request Help

```python
# Request help with specific capabilities
request_id = await agent.help_manager.request_help(
    required_capabilities=["python_coding", "gcp_optimization"],
    description="I need help building a cost optimization tool"
)

print(f"Help request sent: {request_id}")
```

#### 4. Discover Other Agents

```python
# Get discovered agents
discovered_agents = await agent.discovery_manager.get_discovered_agents()

for agent_info in discovered_agents:
    print(f"Found agent: {agent_info.agent_id}")
    print(f"Capabilities: {agent_info.capabilities}")
    print(f"Trust score: {agent_info.trust_score}")
```

## 📚 Advanced Usage

### Message Types

The system supports 12 standardized message types:

```python
from beast_mode.message_models_dataclass import MessageType

# Basic communication
MessageType.SIMPLE_MESSAGE      # Basic text communication
MessageType.PROMPT_REQUEST      # Request for processing
MessageType.PROMPT_RESPONSE     # Response to request

# Agent discovery
MessageType.AGENT_DISCOVERY     # Presence announcement
MessageType.AGENT_RESPONSE      # Discovery response

# Collaboration
MessageType.HELP_WANTED         # Request for assistance
MessageType.HELP_RESPONSE       # Offer to help

# Spore sharing
MessageType.SPORE_DELIVERY      # Spore sharing
MessageType.SPORE_REQUEST       # Request for specific spore

# Technical
MessageType.TECHNICAL_EXCHANGE  # Setup/debugging info
MessageType.SYSTEM_HEALTH       # Health monitoring
MessageType.PROCESSOR_RESPONSE  # Automated responses
```

### Custom Message Handlers

```python
from beast_mode.message_models_dataclass import BeastModeMessage, MessageType

async def my_custom_handler(message: BeastModeMessage):
    """Handle custom message types."""
    print(f"Received message: {message.payload}")
    
    # Process the message...
    
    # Send response if needed
    response = BeastModeMessage(
        type=MessageType.SIMPLE_MESSAGE,
        source="my_agent",
        target=message.source,
        payload={"response": "Message processed!"}
    )
    await agent.bus_client.send_message(response)

# Register handler
agent.bus_client.register_handler(MessageType.SIMPLE_MESSAGE, my_custom_handler)
```

### Help System Features

```python
# Get help requests
requests = await agent.help_manager.get_help_requests()

# Get collaboration metrics
metrics = await agent.help_manager.get_collaboration_metrics()
print(f"Success rate: {metrics.get_success_rate():.2%}")

# Get agent recommendations
recommendations = await agent.help_manager.get_agent_recommendations(
    required_capabilities=["python_coding"]
)
for agent_id, score in recommendations:
    print(f"Agent {agent_id}: {score:.2f} recommendation score")
```

## 🔧 Configuration

### Redis Configuration

```python
# Custom Redis URL
redis_manager = RedisConnectionManager("redis://localhost:6379")

# With authentication
redis_manager = RedisConnectionManager("redis://username:password@localhost:6379")
```

### Agent Configuration

```python
# Custom capabilities
capabilities = [
    "python_coding",
    "gcp_optimization", 
    "data_analysis",
    "machine_learning"
]

# Custom channel
bus_client = BeastModeBusClient(
    agent_id="my_agent",
    capabilities=capabilities,
    channel="custom_channel"  # Default: "beast_mode_network"
)
```

## 🧪 Testing

### Run the Demo

```bash
# Make sure Redis is running first
redis-server

# Run the usage demo
uv run python examples/simple_usage_demo.py
```

### Run Tests

```bash
# Run all tests
uv run python -m pytest tests/ -v

# Run specific test file
uv run python tests/test_agent_discovery_communication.py
```

## 📊 Monitoring

### Message Statistics

```python
# Get message handling statistics
stats = agent.message_handler.get_statistics()
print(f"Total messages: {stats['total_messages']}")
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Error count: {stats['error_count']}")
```

### Agent Health

```python
# Check Redis health
is_healthy = await agent.redis_manager.is_healthy()
print(f"Redis healthy: {is_healthy}")

# Check discovered agents
agents = await agent.discovery_manager.get_discovered_agents()
print(f"Discovered {len(agents)} agents")
```

## 🚨 Troubleshooting

### Common Issues

1. **Redis Connection Failed**

   - Ensure Redis server is running
   - Check Redis URL and port
   - Verify network connectivity

1. **No Agents Discovered**

   - Wait a few seconds for discovery
   - Check if agents are announcing presence
   - Verify all agents are on the same channel

1. **Messages Not Received**

   - Check message routing logic
   - Verify target agent is correct
   - Check message handlers are registered

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed logs of all message processing
```

## 🎯 Best Practices

1. **Always handle errors gracefully**
1. **Use appropriate message types for different purposes**
1. **Implement proper cleanup in your agents**
1. **Monitor collaboration metrics for optimization**
1. **Use trust scores to select reliable collaborators**

## 📖 Examples

See the `examples/` directory for complete working examples:

- `simple_usage_demo.py` - Basic usage demonstration
- `agent_discovery_example.py` - Advanced agent discovery
- `basic_agent_example.py` - Simple agent implementation

## 🤝 Contributing

The Beast Mode Agent Collaboration Network is designed to be extensible. You can:

- Add new message types
- Implement custom message handlers
- Create specialized agent types
- Add new collaboration features

Happy collaborating! 🚀
