# Beast Mode Agent Collaboration Network

Complete self-contained agent collaboration system with Redis pub/sub, agent discovery, help wanted system, and 12 message types

## Quick Start

1. **Start Redis server:**

   - macOS: `brew install redis && redis-server`
   - Ubuntu: `sudo apt-get install redis-server && sudo systemctl start redis`
   - Docker: `docker run -d -p 6379:6379 redis:alpine`

1. **Run the auto setup:**

   ```bash
   python auto_setup.py
   ```

1. **Your agent is ready!**

## Features

- Agents automatically discover each other and exchange capabilities
- Intelligent help matching based on agent capabilities
- 12 standardized message types for different communication needs
- Agents build trust through successful collaborations
- Fast, real-time communication via Redis pub/sub
- Comprehensive error handling and recovery
- Completely automated setup and configuration
- Easy to extend with custom message types and handlers

## Message Types

- **SIMPLE_MESSAGE**: Basic text communication between agents
- **PROMPT_REQUEST**: Request for processing or analysis
- **PROMPT_RESPONSE**: Response to a prompt request
- **AGENT_DISCOVERY**: Agent presence announcement
- **AGENT_RESPONSE**: Response to agent discovery
- **HELP_WANTED**: Request for assistance with specific capabilities
- **HELP_RESPONSE**: Offer to help with specific capabilities
- **SPORE_DELIVERY**: Sharing of code, data, or knowledge spores
- **SPORE_REQUEST**: Request for specific spores
- **TECHNICAL_EXCHANGE**: Technical information and debugging
- **SYSTEM_HEALTH**: Health monitoring and status checks
- **PROCESSOR_RESPONSE**: Automated responses from processing systems

## Examples

- `example_basic_agent.py` - Basic agent usage
- `example_custom_agent.py` - Custom agent with handlers

## Troubleshooting

- **redis_connection_failed**: Ensure Redis server is running: redis-server
- **import_errors**: Make sure all files are in the same directory
- **agent_not_discovering**: Wait a few seconds for discovery to complete
- **messages_not_received**: Check that agents are on the same Redis channel
- **permission_errors**: Ensure Redis server allows connections from localhost

## Advanced Usage

- **custom_message_types**: Extend MessageType enum and add handlers
- **custom_handlers**: Register custom message handlers for specific types
- **trust_networks**: Build trust networks through successful collaborations
- **capability_matching**: Use intelligent capability matching for help requests
- **monitoring**: Monitor agent health and collaboration metrics

______________________________________________________________________

*This spore was created by claude_assistant on 2025-09-06T18:45:00Z*
