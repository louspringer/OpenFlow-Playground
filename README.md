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
- **NEW**: Spec-Driven Development workflow via [cc-sdd](https://github.com/gotalab/cc-sdd) integration
- **NEW**: Project Memory (steering) system for maintaining context across sessions
- **NEW**: Structured requirements → design → tasks → implementation workflow

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

## Spec-Driven Development (NEW)

OpenFlow Playground now integrates [cc-sdd](https://github.com/gotalab/cc-sdd) for structured, systematic development workflows.

### Kiro Commands

```bash
# Project context
/kiro:steering                    # Generate/update project memory
/kiro:steering-custom            # Add domain-specific steering

# Feature development
/kiro:spec-init <feature>        # Start new feature spec
/kiro:spec-requirements <feature>  # Create requirements.md
/kiro:spec-design <feature>      # Create design.md  
/kiro:spec-tasks <feature>       # Create tasks.md
/kiro:spec-impl <feature> <tasks>  # Implement specific tasks

# Validation
/kiro:validate-gap <feature>     # Analyze existing vs requirements
/kiro:validate-design <feature>  # Validate design integration
/kiro:spec-status <feature>      # Check feature status
```

### Example: Research Agent Feature

```bash
/kiro:spec-init Research Agent with Vercel AI SDK
/kiro:spec-requirements research-agent
/kiro:spec-design research-agent -y
/kiro:spec-tasks research-agent -y
/kiro:spec-impl research-agent 1.1,1.2,1.3
```

See `.kiro/specs/vercel-ai-chatui-research-agent/requirements.md` for a complete example.

## Documentation

- **For AI Agents**: Read `AGENTS.md` for context and patterns
- **Project Memory**: See `.kiro/steering/` for product, tech, and structure docs
- **Domain Architecture**: Check `docs/DOMAIN_ARCHITECTURE.md`
- **Cursor Rules**: Browse `.cursor/rules/` for development guidelines

## License & Attribution

**OpenFlow Playground**: MIT License

**Integrated Tools**:
- [cc-sdd](https://github.com/gotalab/cc-sdd) - MIT License - © gotalab  
  Spec-driven development workflow for AI-assisted development

______________________________________________________________________

*This spore was created by claude_assistant on 2025-09-06T18:45:00Z*  
*Enhanced with cc-sdd integration on 2025-01-30*
