# Requirements Document: Beast Observatory

## Introduction

Beast Observatory is a real-time observability and monitoring platform for the Beast Mode multi-agent ecosystem. It provides centralized visibility into CI/CD pipelines, agent activity, quality metrics, and system health across all nkllon projects.

**Public URL**: https://observatory.nkllon.com  
**Repository**: https://github.com/nkllon/beast-observatory  
**Infrastructure**: Dockerized stack on vonnegut.local with Cloudflare tunnel  
**License**: MIT

## System Context

### Existing Infrastructure (vonnegut.local)

**Base Cluster Services**:
- **Redis**: Message bus and cache (Beast Mode coordination)
- **Prometheus**: Metrics collection and time-series database
- **Directus**: Headless CMS for content management
- **Cloudflare**: Tunnel to public endpoint (vonnegut.local → observatory.nkllon.com)

**Deployment**:
- Dockerized services (docker-compose or Kubernetes)
- Local server: vonnegut.local
- Public access: https://observatory.nkllon.com

## Requirements

### Requirement 1: Event Ingestion API
**Objective:** As a system (OpenFlow Playground, agents, CI/CD), I want to send events to the observatory, so that activity is tracked in real-time.

#### Acceptance Criteria
1. WHEN an event is POSTed to `/api/events` THEN it SHALL be accepted within 100ms
2. WHEN batch events are sent to `/api/events/batch` THEN all events SHALL be queued
3. IF authentication fails THEN 401 SHALL be returned with error message
4. WHERE event schema is invalid THE 400 SHALL be returned with validation errors
5. WHEN events are received THEN they SHALL be stored in Directus and published to Redis

### Requirement 2: Real-Time Dashboard
**Objective:** As a stakeholder, I want to see real-time system activity, so that I can monitor operations without delay.

#### Acceptance Criteria
1. WHEN events are ingested THEN dashboard SHALL update within 5 seconds
2. WHEN viewing dashboard THEN WebSocket connection SHALL provide live updates
3. IF connection drops THEN client SHALL reconnect automatically
4. WHERE historical data is shown THE real-time updates SHALL continue
5. WHEN filtering events THEN only relevant real-time updates SHALL appear

### Requirement 3: Redis Integration
**Objective:** As the Beast Mode system, I want to use Redis for event pub/sub, so that agents can subscribe to observatory events.

#### Acceptance Criteria
1. WHEN events are ingested THEN they SHALL be published to Redis channels
2. WHEN agents subscribe THEN they SHALL receive real-time event streams
3. IF Redis is unavailable THEN events SHALL queue until reconnection
4. WHERE multiple agents listen THE events SHALL be broadcast to all
5. WHEN events are published THEN TTL SHALL be configured (1 hour default)

### Requirement 4: Prometheus Metrics
**Objective:** As an operator, I want Prometheus to collect and aggregate metrics, so that I can query and alert on system behavior.

#### Acceptance Criteria
1. WHEN metrics are generated THEN they SHALL be exposed at `/metrics` endpoint
2. WHEN Prometheus scrapes THEN all agent/pipeline metrics SHALL be available
3. IF metrics are missing THEN default values SHALL be provided
4. WHERE time-series data is needed THE Prometheus SHALL store historical metrics
5. WHEN querying metrics THEN PromQL queries SHALL be supported

### Requirement 5: Directus CMS Integration
**Objective:** As a content manager, I want Directus to manage observatory content and configuration, so that non-technical users can update dashboards.

#### Acceptance Criteria
1. WHEN events are stored THEN Directus collections SHALL persist them
2. WHEN dashboard config changes THEN Directus SHALL provide the updates
3. IF content is edited THEN changes SHALL appear immediately in observatory
4. WHERE historical events are queried THE Directus API SHALL provide them
5. WHEN authentication is configured THEN Directus roles SHALL control access

### Requirement 6: Cloudflare Tunnel
**Objective:** As a system architect, I want Cloudflare to tunnel vonnegut.local to public internet, so that the observatory is accessible from anywhere.

#### Acceptance Criteria
1. WHEN requests arrive at observatory.nkllon.com THEN Cloudflare SHALL route to vonnegut.local
2. WHEN SSL is configured THEN HTTPS SHALL be enforced
3. IF tunnel is down THEN automatic reconnection SHALL occur
4. WHERE DDoS protection is enabled THE Cloudflare SHALL filter malicious traffic
5. WHEN traffic spikes THEN Cloudflare SHALL cache static assets

### Requirement 7: Multi-Project Support
**Objective:** As a project manager, I want the observatory to support multiple projects, so that all nkllon projects share one monitoring system.

#### Acceptance Criteria
1. WHEN events are sent THEN source project SHALL be identified
2. WHEN filtering THEN projects SHALL be selectable
3. IF multiple projects are active THEN dashboard SHALL show all
4. WHERE project-specific views are needed THE filtering SHALL isolate them
5. WHEN new projects are added THEN zero configuration changes SHALL be required

### Requirement 8: API Authentication
**Objective:** As a security engineer, I want secure API authentication, so that only authorized systems can publish events.

#### Acceptance Criteria
1. WHEN API requests arrive THEN Bearer token SHALL be validated
2. WHEN token is invalid THEN 401 SHALL be returned
3. IF token is expired THEN 401 with expiration message SHALL be returned
4. WHERE tokens are generated THE they SHALL be stored in 1Password or GitHub Secrets
5. WHEN rotating tokens THEN old tokens SHALL have grace period (24 hours)

### Requirement 9: Event Schema Validation
**Objective:** As a developer, I want event schemas validated, so that data quality is enforced.

#### Acceptance Criteria
1. WHEN events are submitted THEN JSON schema validation SHALL occur
2. WHEN validation fails THEN detailed error messages SHALL be returned
3. IF required fields are missing THEN 400 with field list SHALL be returned
4. WHERE event types are defined THE schema SHALL be versioned
5. WHEN schema evolves THEN backward compatibility SHALL be maintained

### Requirement 10: Historical Data Query
**Objective:** As an analyst, I want to query historical events, so that I can analyze trends and patterns.

#### Acceptance Criteria
1. WHEN querying events THEN Directus API SHALL provide results
2. WHEN filtering by date range THEN only matching events SHALL be returned
3. IF pagination is needed THEN cursor-based pagination SHALL be used
4. WHERE aggregations are requested THE Directus SHALL compute them
5. WHEN exporting data THEN JSON/CSV formats SHALL be available

### Requirement 11: Alerting & Notifications
**Objective:** As an operator, I want alerts on critical events, so that I can respond quickly to issues.

#### Acceptance Criteria
1. WHEN critical events occur THEN alerts SHALL be triggered
2. WHEN CI fails THEN notification SHALL be sent (Slack/Discord/email)
3. IF agent fails THEN alert SHALL include failure context
4. WHERE alert rules are configured THE they SHALL be evaluated in real-time
5. WHEN alerts are acknowledged THEN they SHALL not re-trigger

### Requirement 12: Performance & Scalability
**Objective:** As a system architect, I want the observatory to handle high event volume, so that it scales with system growth.

#### Acceptance Criteria
1. WHEN event rate is 100/second THEN all SHALL be processed without lag
2. WHEN storage grows THEN automatic cleanup SHALL remove old events (90 day retention)
3. IF database is slow THEN Redis caching SHALL improve query performance
4. WHERE memory is limited THE system SHALL apply backpressure
5. WHEN scaling THEN horizontal scaling SHALL be supported

## System Architecture

### Technology Stack

**Frontend**:
- Directus (Headless CMS + Admin UI)
- WebSocket for real-time updates
- Cloudflare for CDN and DDoS protection

**Backend**:
- FastAPI (Event ingestion API)
- Redis (Event pub/sub + caching)
- Prometheus (Metrics collection)
- Directus (Data persistence + API)

**Infrastructure**:
- Docker Compose (service orchestration)
- vonnegut.local (physical server)
- Cloudflare Tunnel (public access)
- Nginx (reverse proxy)

### Service Architecture

```
Internet
    ↓
https://observatory.nkllon.com (Cloudflare)
    ↓
Cloudflare Tunnel
    ↓
vonnegut.local (Nginx)
    ↓
┌─────────────────────────────────────────────┐
│         Docker Compose Services             │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  FastAPI │  │ Directus │  │   Nginx  │ │
│  │  Events  │→ │   CMS    │  │  Proxy   │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       ↓              ↓                      │
│  ┌──────────┐  ┌──────────┐               │
│  │  Redis   │  │Prometheus│               │
│  │ Pub/Sub  │  │ Metrics  │               │
│  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────┘
```

### Data Flow

```
OpenFlow Playground CI/CD
    ↓
POST https://observatory.nkllon.com/api/events
    ↓
FastAPI validates and accepts
    ↓
Parallel writes:
    ├─→ Directus (persistent storage)
    ├─→ Redis pub/sub (real-time broadcast)
    └─→ Prometheus (metrics aggregation)
    ↓
WebSocket clients receive updates
    ↓
Dashboard displays real-time activity
```

## Repository Structure

```
beast-observatory/
├── api/                          # FastAPI event ingestion
│   ├── main.py                  # FastAPI app
│   ├── models.py                # Event schemas (Pydantic)
│   ├── routes/
│   │   ├── events.py           # /api/events endpoints
│   │   ├── metrics.py          # /api/metrics endpoints
│   │   └── health.py           # /health endpoint
│   ├── integrations/
│   │   ├── directus.py         # Directus client
│   │   ├── redis.py            # Redis pub/sub
│   │   └── prometheus.py       # Metrics export
│   └── auth.py                  # API token validation
├── directus/                     # Directus configuration
│   ├── collections/             # Event collections schema
│   ├── flows/                   # Automation workflows
│   └── extensions/              # Custom extensions
├── prometheus/                   # Prometheus configuration
│   ├── prometheus.yml           # Scrape configs
│   └── alerts/                  # Alert rules
├── nginx/                        # Nginx reverse proxy
│   └── observatory.conf         # Routing configuration
├── cloudflare/                   # Cloudflare tunnel config
│   └── tunnel-config.yml        # Tunnel settings
├── docker-compose.yml            # Service orchestration
├── pyproject.toml               # Python dependencies
├── Dockerfile.api               # FastAPI container
├── README.md                    # Documentation
└── .env.example                 # Environment variables template
```

## Docker Compose Services

```yaml
services:
  # Event ingestion API
  api:
    build: .
    ports: ["8000:8000"]
    depends_on: [redis, directus]
    environment:
      - REDIS_URL=redis://redis:6379
      - DIRECTUS_URL=http://directus:8055
      - PROMETHEUS_URL=http://prometheus:9090
  
  # Directus CMS
  directus:
    image: directus/directus:latest
    ports: ["8055:8055"]
    depends_on: [redis]
    volumes:
      - directus-data:/directus/database
      - directus-uploads:/directus/uploads
  
  # Redis pub/sub + cache
  redis:
    image: redis:alpine
    ports: ["6379:6379"]
    volumes:
      - redis-data:/data
  
  # Prometheus metrics
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
  
  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx/observatory.conf:/etc/nginx/conf.d/default.conf
    depends_on: [api, directus]
```

## Integration with OpenFlow Playground

### Client Library

**Location**: `src/observability/observatory_client.py` (in OpenFlow)

```python
import httpx
from typing import Dict, Any

class ObservatoryClient:
    def __init__(
        self,
        api_url: str = "https://observatory.nkllon.com",
        api_token: str = None
    ):
        self.api_url = api_url
        self.api_token = api_token or os.getenv("OBSERVATORY_TOKEN")
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
    
    async def send_event(self, event_type: str, data: Dict[str, Any]):
        """Send single event"""
        await self.client.post(
            f"{self.api_url}/api/events",
            json={
                "event_type": event_type,
                "source": "openflow-playground",
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
        )
```

### GitHub Actions Integration

**Add to all workflows**:
```yaml
env:
  OBSERVATORY_URL: https://observatory.nkllon.com
  OBSERVATORY_TOKEN: ${{ secrets.OBSERVATORY_TOKEN }}

steps:
  - name: Notify Observatory - Start
    if: always()
    run: |
      curl -X POST ${{ env.OBSERVATORY_URL }}/api/events \
        -H "Authorization: Bearer ${{ env.OBSERVATORY_TOKEN }}" \
        -H "Content-Type: application/json" \
        -d '{
          "event_type": "workflow_started",
          "source": "github-actions",
          "data": {
            "workflow": "${{ github.workflow }}",
            "repository": "${{ github.repository }}",
            "pr_number": "${{ github.event.number }}",
            "commit_sha": "${{ github.sha }}"
          }
        }'
```

## Non-Functional Requirements

### Performance
- Event ingestion: < 100ms latency
- Dashboard updates: < 5 seconds
- API throughput: 1000 events/second
- Query response: < 1 second for recent events

### Scalability
- Horizontal scaling of FastAPI instances
- Redis clustering for high availability
- Prometheus federation for multiple clusters
- Directus database can grow to 100GB+

### Reliability
- 99.9% uptime for API
- Event queue persistence during downtime
- Automatic service restart on failure
- Data backup daily

### Security
- HTTPS only (enforced by Cloudflare)
- API token authentication
- Rate limiting per token (100 req/min)
- SQL injection prevention (Directus ORM)
- CORS configured for observatory.nkllon.com only

## Success Metrics

1. **Event Delivery**: 99.9% of events successfully ingested
2. **Latency**: 95% of events appear in dashboard within 5 seconds
3. **Uptime**: 99.9% API availability
4. **Coverage**: 100% of OpenFlow Playground CI/CD activity tracked
5. **Adoption**: 3+ projects using observatory within 1 month

## Dependencies

### External Services
- Cloudflare tunnel (public access)
- vonnegut.local (hosting infrastructure)

### Docker Images
- `directus/directus:latest` - CMS
- `redis:alpine` - Redis
- `prom/prometheus:latest` - Metrics
- `nginx:alpine` - Reverse proxy

### Python Packages (for API)
```toml
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.23.0",
    "redis>=5.0.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "prometheus-client>=0.17.0",
    "python-json-logger>=2.0.0",
    "websockets>=12.0",
]
```

## Integration Points

### 1. OpenFlow Playground
- CI/CD workflows send events
- Agents send activity events
- Quality system publishes metrics

### 2. beast-ai-dev-agent
- Agent lifecycle events
- Request/response tracking
- Health check results

### 3. Future Projects
- Hackathon submissions
- Other nkllon projects
- Community contributions

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| vonnegut.local downtime | High | Event queue + retry logic |
| Cloudflare tunnel failure | High | Health monitoring + alerts |
| Redis memory exhaustion | Medium | TTL on events + max memory config |
| Directus database growth | Medium | Auto-cleanup after 90 days |
| High event volume | Medium | Rate limiting + backpressure |

## Next Steps

1. **Create Repository**: `gh repo create nkllon/beast-observatory --public`
2. **Initialize Structure**: Docker Compose + service directories
3. **Implement FastAPI**: Event ingestion API
4. **Configure Directus**: Collections for events
5. **Set up Cloudflare**: Tunnel configuration
6. **Deploy to vonnegut.local**: Docker Compose up
7. **Test Integration**: Send events from OpenFlow Playground
8. **Create Dashboard**: Real-time event display

---

**Document Status**: Draft  
**Created**: 2025-10-30  
**Infrastructure**: Existing (vonnegut.local + Cloudflare)  
**Services**: Redis, Prometheus, Directus (already running)  
**Next**: Design + Implementation

