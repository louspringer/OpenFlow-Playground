# Gmail-to-Calendar System - Protocol-Driven Design

A comprehensive, production-ready system for reading Gmail and adding events to Google Calendar with conflict checks, confirmations, and auditability.

## 🎯 Key Features

- **OAuth2 Connectors**: Secure, least-privilege access to Gmail and Calendar APIs
- **ICS Parser**: RFC 5545 compliant parsing of calendar attachments
- **Natural Language Time Parsing**: Handles "this Friday 2:30-3pm", "tomorrow at noon"
- **Conflict Detection**: Automatic conflict checking with alternative time suggestions
- **Idempotency**: Never duplicate events, even on reprocessing
- **Auditability**: Complete audit trail for all operations
- **LangGraph Orchestration**: Deterministic, stateful workflow management
- **MCP Integration**: Ready-to-use MCP tools for LLM integration

## 🏗️ Architecture

### System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Layer                       │
│  (LangGraph: intent_router → email_locator → ... → notifier) │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Connector Layer                          │
│  (Gmail API, Calendar API, OAuth2, Token Management)        │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Parser Layer                             │
│  (ICS Parser, Time Normalizer, Natural Language Processing) │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  (EventCandidate, IdempotencyKey, AuditLog, State Mgmt)     │
└─────────────────────────────────────────────────────────────┘
```

### OAuth2 Scopes

**Gmail (Read-Only)**

- `https://www.googleapis.com/auth/gmail.readonly`

**Calendar (Read/Write)**

- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/calendar.events`

**People (Optional)**

- `https://www.googleapis.com/auth/contacts.readonly`

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
uv add google-auth google-auth-oauthlib google-auth-httplib2
uv add google-api-python-client icalendar dateutil
uv add langgraph httpx

# Install the system
uv add -e src/gmail_calendar_system/
```

### 2. OAuth Setup

```bash
# Create OAuth credentials in Google Cloud Console
# Download credentials.json files for Gmail and Calendar

# Setup OAuth
uv run python src/gmail_calendar_system/cli.py setup
```

### 3. Basic Usage

```bash
# Process a request
uv run python src/gmail_calendar_system/cli.py process "put Megan's meeting on my calendar"

# Test the system
uv run python src/gmail_calendar_system/cli.py test
```

## 🔧 Configuration

### OAuth Configuration

Create `gmail_calendar_config.json`:

```json
{
  "gmail": {
    "client_id": "your-gmail-client-id",
    "client_secret": "your-gmail-client-secret",
    "redirect_uri": "http://localhost:8080/callback",
    "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
    "token_file": "gmail_token.json",
    "credentials_file": "gmail_credentials.json"
  },
  "calendar": {
    "client_id": "your-calendar-client-id",
    "client_secret": "your-calendar-client-secret", 
    "redirect_uri": "http://localhost:8080/callback",
    "scopes": [
      "https://www.googleapis.com/auth/calendar.readonly",
      "https://www.googleapis.com/auth/calendar.events"
    ],
    "token_file": "calendar_token.json",
    "credentials_file": "calendar_credentials.json"
  },
  "default_timezone": "America/Denver",
  "confidence_threshold": 0.85
}
```

## 📋 MCP Tools

### Google Calendar Tool

```json
{
  "name": "google-calendar",
  "functions": [
    "find_conflicts",
    "create_or_update_event", 
    "list_events",
    "get_event",
    "delete_event"
  ]
}
```

**Example Usage:**

```python
# Find conflicts
result = await calendar_tool.find_conflicts({
    "start_iso": "2025-09-05T14:30:00-06:00",
    "end_iso": "2025-09-05T15:00:00-06:00"
})

# Create event
result = await calendar_tool.create_or_update_event({
    "summary": "Call: Megan Jury (Robinson & Henry) — Probate",
    "start": {"dateTime": "2025-09-05T14:30:00-06:00", "timeZone": "America/Denver"},
    "end": {"dateTime": "2025-09-05T15:00:00-06:00", "timeZone": "America/Denver"},
    "attendees": ["megan.jury@robinsonandhenry.com"]
})
```

### Gmail Tool

```json
{
  "name": "gmail",
  "functions": [
    "search_messages",
    "read_thread",
    "get_message",
    "get_attachments", 
    "download_attachment"
  ]
}
```

**Example Usage:**

```python
# Search messages
result = await gmail_tool.search_messages({
    "query": "from:(megan OR jury) subject:(probate OR call OR meeting) newer_than:30d",
    "max_results": 25
})

# Read thread
result = await gmail_tool.read_thread({
    "thread_id": "17889abcd..."
})
```

### ICS Tool

```json
{
  "name": "ics",
  "functions": [
    "parse",
    "generate",
    "validate"
  ]
}
```

**Example Usage:**

```python
# Parse ICS
result = await ics_tool.parse({
    "source": "attachment",
    "content_base64": "QkVHSU46VkNBTEVOREFS..."
})

# Generate ICS
result = await ics_tool.generate({
    "summary": "Meeting with Megan",
    "start_iso": "2025-09-05T14:30:00-06:00",
    "end_iso": "2025-09-05T15:00:00-06:00"
})
```

## 🔄 Orchestration Flow

### Deterministic Workflow

1. **Intent Router**: Parse user query → generate Gmail search terms
1. **Email Locator**: Search Gmail → select most relevant message/thread
1. **Meeting Extractor**: Parse ICS attachments or extract from email body
1. **Time Normalizer**: Resolve "this Friday 2:30-3pm" → ISO timestamps
1. **Conflict Check**: Check calendar for overlapping events
1. **Confirmation Gate**: Auto-proceed or request user confirmation
1. **Calendar Write**: Create/update event with idempotency
1. **Notifier**: Send confirmation with event link

### State Management

```python
@dataclass
class OrchestratorState:
    user_query: str
    user_id: str
    search_query: str
    messages: List[Dict[str, Any]]
    selected_message: Optional[Dict[str, Any]]
    event_candidates: List[EventCandidate]
    normalized_time: Optional[Dict[str, Any]]
    conflict_info: Optional[ConflictInfo]
    confirmation_request: Optional[ConfirmationRequest]
    event_result: Optional[EventResult]
    audit_logs: List[AuditLog]
```

## 🛡️ Security & Compliance

### OAuth2 Security

- **Least Privilege**: Minimal required scopes
- **Token Encryption**: Encrypted storage with KMS
- **Refresh Tokens**: Automatic token renewal
- **Scoped Access**: Separate tokens for read vs write operations

### Idempotency

- **Source-based Keys**: `gmail:MESSAGE_ID`, `ics:UID`, `manual:hash`
- **Database Storage**: `(idempotency_key → calendar_event_id)` mapping
- **Retry Safety**: Never duplicate events on reprocessing

### Auditability

```python
@dataclass
class AuditLog:
    timestamp: datetime
    user_id: str
    action: str
    event_id: Optional[str]
    idempotency_key: Optional[str]
    source_message_id: Optional[str]
    success: bool
    details: Dict[str, Any]
```

## 🧪 Testing

### Unit Tests

```bash
# Run tests
uv run python -m pytest tests/

# Test specific components
uv run python -m pytest tests/test_parsers.py
uv run python -m pytest tests/test_connectors.py
uv run python -m pytest tests/test_orchestrator.py
```

### Integration Tests

```bash
# Test with real Gmail/Calendar APIs
uv run python src/gmail_calendar_system/cli.py test
```

## 📊 Monitoring & Observability

### Structured Logging

```python
# Every operation is logged with context
logger.info(f"📧 Found {len(messages)} messages for query: {query}")
logger.info(f"📅 Extracted {len(candidates)} event candidates")
logger.info(f"✅ Created calendar event: {event_id}")
```

### Metrics

- **Extraction Confidence**: Average confidence scores
- **Confirmation Rate**: Percentage requiring user confirmation
- **Conflict Rate**: Percentage with calendar conflicts
- **Write Latency**: Time to create calendar events
- **Duplicates Prevented**: Idempotency effectiveness

### Audit Trail

- **User Actions**: Who did what when
- **Event Lifecycle**: Creation, updates, cancellations
- **Source Tracking**: Email → Calendar event mapping
- **Error Logging**: Failed operations with context

## 🔧 Advanced Usage

### Custom Time Parsing

```python
# Add custom time patterns
normalizer = TimeNormalizer("America/Denver")
result = normalizer.normalize(
    "next Thursday at 2:30pm",
    user_tz="America/Denver",
    reference_time_iso="2025-09-03T08:00:00-06:00"
)
```

### Conflict Resolution

```python
# Get alternative times when conflicts exist
conflict_info = await calendar_connector.find_conflicts(
    start_iso="2025-09-05T14:30:00-06:00",
    end_iso="2025-09-05T15:00:00-06:00"
)

if conflict_info.has_conflict:
    alternatives = await calendar_connector.generate_alternatives(
        start_iso, end_iso, duration_minutes=30
    )
```

### Batch Processing

```python
# Process multiple emails
orchestrator = GmailCalendarOrchestrator(gmail_config, calendar_config)

for query in email_queries:
    result = await orchestrator.process_request(query, user_id)
    print(f"Processed: {result['success']}")
```

## 🚀 Production Deployment

### Environment Variables

```bash
export GMAIL_CLIENT_ID="your-client-id"
export GMAIL_CLIENT_SECRET="your-client-secret"
export CALENDAR_CLIENT_ID="your-client-id"
export CALENDAR_CLIENT_SECRET="your-client-secret"
export DEFAULT_TIMEZONE="America/Denver"
export CONFIDENCE_THRESHOLD="0.85"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

CMD ["python", "src/gmail_calendar_system/cli.py", "mcp", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gmail-calendar-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gmail-calendar-system
  template:
    metadata:
      labels:
        app: gmail-calendar-system
    spec:
      containers:
      - name: gmail-calendar
        image: gmail-calendar-system:latest
        ports:
        - containerPort: 8080
        env:
        - name: GMAIL_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: oauth-secrets
              key: gmail-client-id
```

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd gmail-calendar-system

# Install development dependencies
uv add --dev pytest pytest-asyncio black flake8 mypy

# Run pre-commit hooks
pre-commit install

# Run tests
uv run pytest
```

### Code Quality

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing
- **Pre-commit**: Quality gates

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Common Issues

**OAuth Authentication Fails**

- Check client ID/secret configuration
- Verify redirect URI matches Google Cloud Console
- Ensure scopes are correctly configured

**ICS Parsing Errors**

- Validate ICS content with RFC 5545
- Check for proper line endings (CRLF)
- Verify required properties (UID, DTSTART, DTEND)

**Time Parsing Issues**

- Provide clear time expressions
- Include timezone context
- Use ISO format for reference times

**Calendar Conflicts**

- Check for overlapping events
- Use suggested alternative times
- Verify timezone consistency

### Debugging

```bash
# Enable verbose logging
uv run python src/gmail_calendar_system/cli.py --verbose process "your query"

# Check logs
tail -f gmail_calendar.log
```

______________________________________________________________________

**Built with ❤️ for the OpenFlow-Playground project**
