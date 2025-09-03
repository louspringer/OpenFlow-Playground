# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added

- Initial release of Gmail-to-Calendar system
- Core Gmail and Google Calendar API integration
- OAuth2 authentication with offline refresh tokens
- ICS (RFC 5545) parsing capabilities
- Natural language time parsing ("this Friday 2:30-3pm")
- Conflict detection and resolution
- Idempotency support to prevent duplicate events
- Comprehensive audit trails and logging
- MCP (Model Context Protocol) tools for LLM integration
- CLI interface for standalone usage
- LangGraph orchestration workflow
- Timezone handling with America/Denver default
- Security-first design with least-privilege access
- Comprehensive error handling and validation
- Type hints and Pydantic models throughout
- Extensive documentation and examples

### Features

- **Gmail Integration**: Read emails, parse threads, extract attachments
- **Calendar Management**: Create/update events with conflict detection
- **ICS Parsing**: RFC 5545 compliant calendar file processing
- **Natural Language Time**: Parse "this Friday 2:30-3pm", "tomorrow at noon"
- **Conflict Detection**: Automatic conflict checking with alternative suggestions
- **Idempotency**: Never duplicate events, even on reprocessing
- **Audit Trails**: Complete operation logging and tracking
- **MCP Tools**: Ready-to-use tools for LLM/agent integration
- **OAuth2 Security**: Secure, least-privilege access to Google services

### MCP Tools

- **Google Calendar Tool**: find_conflicts, create_or_update_event, list_events, get_event, delete_event
- **Gmail Tool**: search_messages, read_thread, get_message, get_attachments, download_attachment
- **ICS Tool**: parse, generate, validate

### CLI Commands

- `gmail-calendar setup`: Setup OAuth credentials
- `gmail-calendar process`: Process a request
- `gmail-calendar test`: Test the system

### Dependencies

- google-auth>=2.0.0
- google-auth-oauthlib>=1.0.0
- google-auth-httplib2>=0.2.0
- google-api-python-client>=2.0.0
- icalendar>=5.0.0
- python-dateutil>=2.8.0
- langgraph>=0.1.0
- httpx>=0.24.0
- pydantic>=2.0.0

### Documentation

- Comprehensive README with quick start guide
- API reference documentation
- MCP integration examples
- Security and OAuth setup instructions
- Performance benchmarks and analysis
- Dual-purpose packaging pattern documentation

### Testing

- Unit tests for all core components
- Integration tests for Gmail and Calendar APIs
- Performance benchmarks
- MCP tool validation tests
- CLI interface tests

### Security

- OAuth2 with offline refresh tokens
- Token encryption and secure storage
- Least-privilege access scopes
- Input validation and sanitization
- Comprehensive audit logging
- No hardcoded credentials

### Performance

- Async/await throughout for non-blocking operations
- Efficient API call batching
- Minimal memory footprint
- Fast startup time
- Optimized for concurrent usage

______________________________________________________________________

## [Unreleased]

### Planned

- Additional calendar providers (Outlook, Apple Calendar)
- Enhanced natural language processing
- Advanced conflict resolution strategies
- Webhook support for real-time updates
- Batch processing capabilities
- Enhanced error recovery mechanisms
- Additional MCP tools
- Web interface for configuration
- Docker containerization
- Kubernetes deployment guides
