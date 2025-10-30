# OpenFlow Playground

> **Multi-Agent Collaboration Framework with Spec-Driven Development**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Redis](https://img.shields.io/badge/redis-required-red.svg)](https://redis.io/)
[![cc-sdd](https://img.shields.io/badge/cc--sdd-integrated-green.svg)](https://github.com/gotalab/cc-sdd)

Complete self-contained agent collaboration system with Redis pub/sub, agent discovery, help wanted system, and 12 message types. Now enhanced with **spec-driven development workflow** for systematic feature development.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Spec-Driven Development](#spec-driven-development-new)
  - [Kiro Commands](#kiro-commands)
  - [Getting Started with SDD](#getting-started-with-sdd)
- [Message Types](#message-types)
- [Examples](#examples)
- [Documentation](#documentation)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [License & Attribution](#license--attribution)

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

### Getting Started with SDD

1. **Read the Quick Start Guide**: [`KIRO_QUICKSTART.md`](KIRO_QUICKSTART.md) - Comprehensive guide with examples
2. **Explore Project Memory**: Check `.kiro/steering/` to understand the project context
3. **Try Your First Spec**: Use `/kiro:spec-init` to start a new feature
4. **Customize Templates**: Edit templates in `.kiro/settings/templates/` to match your workflow

**Quick Links**:
- 📖 [Kiro Quick Start Guide](KIRO_QUICKSTART.md) - Start here!
- 🤖 [AI Agent Context](AGENTS.md) - Essential context for AI coding assistants
- 📊 [Integration Summary](CC_SDD_INTEGRATION_SUMMARY.md) - Complete integration details
- 🧪 [Research Agent Example](.kiro/specs/vercel-ai-chatui-research-agent/requirements.md) - Full specification example

## Documentation

### Core Documentation
- **[Kiro Quick Start](KIRO_QUICKSTART.md)** - Get started with spec-driven development
- **[AI Agent Context](AGENTS.md)** - Essential context for AI coding assistants
- **[Integration Summary](CC_SDD_INTEGRATION_SUMMARY.md)** - Complete cc-sdd integration details
- **[Merge Readiness Report](MERGE_READINESS_REPORT.md)** - Pre-merge testing and validation

### Project Architecture
- **[Project Memory](.kiro/steering/)** - Product, tech, and structure documentation
  - [Product Vision](.kiro/steering/product.md) - Purpose, capabilities, and principles
  - [Technology Stack](.kiro/steering/tech.md) - Technical decisions and conventions
  - [Project Structure](.kiro/steering/structure.md) - Organization and patterns
- **[Domain Architecture](docs/DOMAIN_ARCHITECTURE.md)** - 34 domains organized into 5 categories
- **[Domain Registry](docs/DOMAIN_REGISTRY.md)** - Complete domain catalog

### Development Guidelines
- **[Cursor Rules](.cursor/rules/)** - 21+ development rules and patterns
- **Project Model**: `project_model_registry.json` - Single source of truth for domain configuration

## License & Attribution

**OpenFlow Playground**: MIT License

**Integrated Tools**:
- [cc-sdd](https://github.com/gotalab/cc-sdd) - MIT License - © gotalab  
  Spec-driven development workflow for AI-assisted development

______________________________________________________________________

*This spore was created by claude_assistant on 2025-09-06T18:45:00Z*  
*Enhanced with cc-sdd integration on 2025-01-30*
