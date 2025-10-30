# Requirements Document: Observatory Real-Time Integration

## Introduction

Integration with https://observatory.nkllon.com to provide real-time visibility into OpenFlow Playground pipeline activity, agent operations, and quality metrics. The observatory must receive live updates from CI/CD workflows, agent operations, and quality checks.

**Observatory URL**: https://observatory.nkllon.com  
**Integration Type**: Real-time event streaming  
**Purpose**: Centralized observability and monitoring

## Requirements

### Requirement 1: CI/CD Event Streaming
**Objective:** As an operator, I want to see real-time CI/CD pipeline activity in the observatory, so that I can monitor builds, deployments, and quality checks.

#### Acceptance Criteria
1. WHEN a CI workflow starts THEN observatory SHALL show "build started" event within 5 seconds
2. WHEN tests complete THEN observatory SHALL display test results and coverage
3. IF a build fails THEN observatory SHALL highlight the failure with error details
4. WHERE quality gates run THE observatory SHALL show quality scores in real-time
5. WHEN deployment completes THEN observatory SHALL update deployment status

### Requirement 2: Agent Activity Monitoring
**Objective:** As an operator, I want to see Beast Mode agent activity in real-time, so that I can monitor agent health and collaboration.

#### Acceptance Criteria
1. WHEN an agent starts THEN observatory SHALL show agent registration
2. WHEN agents communicate THEN observatory SHALL track message flow
3. IF an agent fails THEN observatory SHALL alert on the failure
4. WHERE help requests occur THE observatory SHALL show collaboration patterns
5. WHEN trust is built THEN observatory SHALL visualize trust networks

### Requirement 3: Quality Metrics Publishing
**Objective:** As a quality engineer, I want quality metrics published to the observatory, so that I can track quality trends over time.

#### Acceptance Criteria
1. WHEN quality analysis runs THEN metrics SHALL be sent to observatory
2. WHEN quality scores change THEN observatory SHALL show the trend
3. IF quality degrades THEN observatory SHALL trigger alerts
4. WHERE quality gates exist THE observatory SHALL show gate pass/fail status
5. WHEN improvements occur THEN observatory SHALL highlight positive trends

### Requirement 4: Real-Time Dashboard Updates
**Objective:** As a stakeholder, I want the observatory dashboard to update in real-time, so that I always see current system state.

#### Acceptance Criteria
1. WHEN events occur THEN dashboard SHALL update within 5 seconds
2. WHEN multiple events happen THEN updates SHALL be batched efficiently
3. IF connection is lost THEN client SHALL reconnect and catch up
4. WHERE bandwidth is limited THE updates SHALL be compressed
5. WHEN viewing historical data THEN real-time updates SHALL continue

### Requirement 5: Authentication & Authorization
**Objective:** As a security engineer, I want secure authentication for observatory updates, so that only authorized systems can publish events.

#### Acceptance Criteria
1. WHEN sending events THEN API token SHALL be required
2. WHEN token is invalid THEN request SHALL be rejected with 401
3. IF token is expired THEN system SHALL handle rotation gracefully
4. WHERE secrets are stored THE system SHALL use GitHub Secrets or 1Password
5. WHEN rotating tokens THEN zero downtime SHALL be maintained

### Requirement 6: Event Schema & Types
**Objective:** As a developer, I want well-defined event schemas, so that I can reliably send and consume events.

#### Acceptance Criteria
1. WHEN sending events THEN JSON schema SHALL be validated
2. WHEN event types are defined THEN they SHALL be documented
3. IF schema validation fails THEN clear error messages SHALL be returned
4. WHERE event data is large THE system SHALL support streaming
5. WHEN schema evolves THEN backward compatibility SHALL be maintained

### Requirement 7: Error Handling & Retry
**Objective:** As a reliability engineer, I want robust error handling, so that transient failures don't lose events.

#### Acceptance Criteria
1. WHEN network fails THEN events SHALL be queued for retry
2. WHEN retry succeeds THEN queued events SHALL be sent in order
3. IF retries exhaust THEN events SHALL be logged locally
4. WHERE observatory is down THE system SHALL degrade gracefully
5. WHEN observatory recovers THEN missed events SHALL be backfilled

### Requirement 8: Performance & Scalability
**Objective:** As a performance engineer, I want efficient event delivery, so that observatory integration doesn't slow down pipelines.

#### Acceptance Criteria
1. WHEN sending events THEN overhead SHALL be < 100ms
2. WHEN high volume occurs THEN batching SHALL be used
3. IF event queue grows THEN backpressure SHALL be applied
4. WHERE bandwidth is limited THE compression SHALL be used
5. WHEN scaling THEN event delivery SHALL remain reliable

## Event Types

### CI/CD Events
```json
{
  "event_type": "ci_build_started",
  "repository": "OpenFlow-Playground",
  "branch": "feat/...",
  "pr_number": 26,
  "commit_sha": "abc123",
  "workflow": "copilot-review",
  "timestamp": "2025-10-30T14:32:00Z"
}

{
  "event_type": "ci_build_completed",
  "build_id": "abc123",
  "status": "success" | "failure",
  "duration_seconds": 120,
  "artifacts": [...]
}

{
  "event_type": "quality_check_completed",
  "quality_score": 85.5,
  "gates_passed": 12,
  "gates_failed": 2,
  "details": {...}
}
```

### Agent Events
```json
{
  "event_type": "agent_registered",
  "agent_id": "cloudrun_agent_1",
  "platform": "cloudrun",
  "capabilities": ["analysis", "coordination"],
  "timestamp": "..."
}

{
  "event_type": "agent_request_processed",
  "agent_id": "cloudrun_agent_1",
  "request_id": "req_123",
  "duration_ms": 150,
  "status": "success"
}
```

### Deployment Events
```json
{
  "event_type": "deployment_started",
  "environment": "production",
  "version": "v1.2.3",
  "deployer": "github-actions"
}

{
  "event_type": "health_check_completed",
  "endpoint": "/health",
  "status_code": 200,
  "response_time_ms": 45
}
```

## API Specification

### Observatory API Endpoint

**Base URL**: `https://observatory.nkllon.com/api`

**POST /events**
```
Headers:
  Authorization: Bearer <OBSERVATORY_TOKEN>
  Content-Type: application/json

Body:
{
  "event_type": string,
  "timestamp": ISO8601 string,
  "source": string,
  "data": object
}

Response: 202 Accepted
{
  "event_id": "evt_abc123",
  "received_at": "2025-10-30T...",
  "status": "queued"
}
```

**POST /events/batch**
```
Body:
{
  "events": [
    {event1},
    {event2},
    ...
  ]
}

Response: 202 Accepted
{
  "batch_id": "batch_abc123",
  "events_received": 5,
  "status": "queued"
}
```

**GET /status**
```
Response: 200 OK
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 12345
}
```

## Integration Points

### 1. GitHub Actions Integration

**Files to Modify**:
- `.github/workflows/copilot-review.yml`
- `.github/workflows/quality-gates.yml`
- `.github/workflows/cloud-build.yml`

**Pattern**:
```yaml
- name: Notify Observatory - <Event>
  if: always()  # Even on failure
  run: |
    curl -X POST https://observatory.nkllon.com/api/events \
      -H "Authorization: Bearer ${{ secrets.OBSERVATORY_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d @- << EOF
    {
      "event_type": "<event_type>",
      "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
      "source": "github-actions",
      "data": {
        "repository": "${{ github.repository }}",
        "pr_number": "${{ github.event.number }}",
        "workflow": "${{ github.workflow }}",
        "run_id": "${{ github.run_id }}"
      }
    }
    EOF
```

### 2. Beast AI Agent Integration

**File**: `beast-ai-dev-agent/src/beast_ai_dev_agent/observability/` (NEW)

**Implementation**:
```python
# In CloudRunKiroAgent
from .observability import observatory_client

class CloudRunKiroAgent(KiroAgentInterface):
    def __init__(self):
        super().__init__(platform="cloudrun")
        self.observatory = observatory_client
        
    async def process_request(self, request):
        await self.observatory.send_event("agent_request", {
            "agent_id": self.platform,
            "request_id": generate_id(),
            "path": request.path
        })
        # ... process
```

### 3. Quality System Integration

**File**: `src/code_quality_system/integrations/observatory_integration.py` (NEW)

**Implementation**:
```python
class ObservatoryIntegration:
    def publish_quality_metrics(self, metrics: dict):
        """Publish quality metrics to observatory"""
        
    def publish_gate_results(self, gates: list):
        """Publish quality gate results"""
        
    def publish_test_results(self, results: dict):
        """Publish test results"""
```

## Technical Architecture

### Component: Observatory Client

**Location**: `src/observability/observatory_client.py` (NEW)

**Class Diagram**:
```python
class ObservatoryClient:
    def __init__(self, api_url: str, api_token: str)
    async def send_event(self, event_type: str, data: dict) -> str
    async def send_batch(self, events: list) -> str
    async def health_check() -> bool
    def _queue_for_retry(self, event: dict)
    def _flush_retry_queue()
```

**Dependencies**:
- `httpx` - Async HTTP client
- `tenacity` - Retry logic
- `structlog` - Structured logging

### Component: Event Queue

**Purpose**: Buffer events during observatory downtime

**Design**:
```python
# src/observability/event_queue.py (NEW)
class EventQueue:
    def __init__(self, max_size: int = 1000):
        self.queue = deque(maxlen=max_size)
    
    def enqueue(self, event: dict):
        self.queue.append(event)
    
    async def flush(self, client: ObservatoryClient):
        while self.queue:
            event = self.queue.popleft()
            await client.send_event(**event)
```

## Non-Functional Requirements

### Performance
- Event send overhead: < 100ms (async, non-blocking)
- Batch size: Up to 100 events per request
- Retry attempts: 3 with exponential backoff
- Queue size: Max 1000 events

### Reliability
- Retry on transient failures (network, 5xx errors)
- Graceful degradation if observatory is down
- Event persistence for critical events
- Health check before sending

### Security
- HTTPS only (TLS 1.2+)
- API token authentication
- Token rotation support
- No sensitive data in events (sanitize logs)

### Scalability
- Async/non-blocking event sending
- Batch processing for high volume
- Compression for large payloads
- Rate limiting awareness

## Success Metrics

1. **Event Delivery**: 99.9% of events delivered successfully
2. **Latency**: < 100ms overhead for event sending
3. **Visibility**: 100% of CI/CD activity visible in observatory
4. **Uptime**: Observatory integration doesn't cause pipeline failures
5. **Adoption**: Team uses observatory for monitoring within 1 week

## Dependencies

### External
- `httpx` - Async HTTP client
- `tenacity` - Retry logic
- `structlog` - Structured logging
- `pydantic` - Event validation

### Internal
- Observatory API (https://observatory.nkllon.com/api)
- GitHub Secrets for OBSERVATORY_TOKEN
- Cloud Logging for backup logs

## Migration Plan

### Phase 1: Observatory Client (Day 1)
1. Create `src/observability/observatory_client.py`
2. Implement event sending with retry logic
3. Add tests for client
4. Deploy as library

### Phase 2: CI Integration (Day 2)
1. Add OBSERVATORY_TOKEN to GitHub Secrets
2. Update copilot-review.yml with event notifications
3. Update quality-gates.yml with metric publishing
4. Update cloud-build.yml with deployment events

### Phase 3: Agent Integration (Day 3)
1. Add observatory client to beast-ai-dev-agent
2. Emit agent lifecycle events
3. Track request/response metrics
4. Publish to observatory

### Phase 4: Quality System Integration (Day 4)
1. Create observatory_integration.py in quality system
2. Publish quality metrics
3. Publish gate results
4. Track quality trends

### Phase 5: Validation (Day 5)
1. End-to-end testing
2. Load testing (100 events/min)
3. Failure scenario testing
4. Documentation

---

**Document Status**: Draft  
**Created**: 2025-10-30  
**Priority**: P0 - Critical  
**Next**: Design (`/kiro:spec-design observatory-integration`)

