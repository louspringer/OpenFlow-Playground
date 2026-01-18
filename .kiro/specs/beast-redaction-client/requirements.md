# beast-redaction-client - Requirements

**Package Type**: PyPI-ready Python library  
**Tier**: 1 (Foundation - No Dependencies)  
**Purpose**: HMAC-protected data classification and redaction client  
**Target**: Production-ready, reusable, 90%+ coverage

---

## 🎯 Package Vision

**A standalone Python client library for secure data classification and redaction services, usable in any application regardless of cloud provider or framework.**

**Key Principle**: Security-first, zero-trust client that never sends unredacted data without proper authentication and verification.

---

## 📋 Functional Requirements

### FR-1: HMAC Authentication
- **Must** implement HMAC-SHA256 signing for all requests
- **Must** verify HMAC signatures on all responses
- **Must** support configurable shared secrets (from environment)
- **Must** reject unsigned or invalid signatures
- **Must** include timestamp/nonce to prevent replay attacks

### FR-2: Classify API
- **Must** provide `classify(text: str) -> Classification` method
- **Must** send HMAC-signed request to classifier endpoint
- **Must** verify HMAC signature on response
- **Must** return structured classification result
- **Must** handle classifier unavailability gracefully

### FR-3: Apply Redactions API
- **Must** provide `apply_redactions(text: str, classifications: List[Classification]) -> str` method
- **Must** apply redactions based on classification results
- **Must** support multiple redaction strategies (mask, hash, remove, tokenize)
- **Must** preserve text structure (line breaks, formatting)
- **Must** return redacted text

### FR-4: Policy Management
- **Must** support pluggable redaction policies
- **Must** load policies from configuration
- **Must** validate policy syntax
- **Must** provide default policies (PII, PHI, PCI, secrets)
- **Must** allow custom policy definitions

### FR-5: Error Handling
- **Must** handle network failures gracefully
- **Must** handle classifier timeout
- **Must** handle invalid HMAC signatures
- **Must** provide detailed error messages
- **Must** log errors appropriately (without leaking sensitive data)

### FR-6: Observability Integration
- **Must** emit metrics (request count, latency, errors)
- **Must** emit traces (with correlation IDs)
- **Must** emit structured logs
- **Should** integrate with beast-observability (optional dependency)
- **Must** work standalone without observability

---

## 🔒 Non-Functional Requirements

### NFR-1: Security
- **Must** never log unredacted sensitive data
- **Must** use secure HMAC implementation (hmac stdlib)
- **Must** validate all inputs
- **Must** pass Bandit security scan with ZERO high/medium issues
- **Must** support TLS for classifier endpoint
- **Must** implement rate limiting protection

### NFR-2: Performance
- **Must** handle <100ms overhead for HMAC operations
- **Must** support async/await for high-throughput scenarios
- **Must** implement connection pooling for classifier endpoint
- **Should** cache classification results (with TTL)

### NFR-3: Testing
- **Must** achieve 90%+ test coverage
- **Must** include unit tests for all methods
- **Must** include integration tests with mock classifier
- **Must** include security tests (invalid HMAC, replay attacks)
- **Must** include performance tests (latency benchmarks)

### NFR-4: Documentation
- **Must** include comprehensive README
- **Must** include API reference documentation
- **Must** include usage examples
- **Must** include deployment guide
- **Must** include security best practices guide

### NFR-5: Packaging
- **Must** be installable via `pip install beast-redaction-client`
- **Must** follow semantic versioning (start 0.1.0)
- **Must** include `pyproject.toml` with proper metadata
- **Must** include LICENSE (MIT)
- **Must** include CHANGELOG
- **Must** publish to PyPI (test.pypi.org first)

---

## 🧩 Component Architecture

### Core Classes

#### `RedactionClient`
```python
class RedactionClient:
    """Main client for data classification and redaction"""
    
    def __init__(
        self,
        classifier_url: str,
        hmac_secret: str,
        policy: Optional[RedactionPolicy] = None,
        observability: Optional[ObservabilityClient] = None
    ):
        """Initialize client with classifier endpoint and HMAC secret"""
        
    async def classify(self, text: str) -> Classification:
        """Classify text using HMAC-protected classifier"""
        
    def apply_redactions(
        self, 
        text: str, 
        classifications: List[Classification]
    ) -> str:
        """Apply redactions based on classification results"""
```

#### `HMACAuth`
```python
class HMACAuth:
    """HMAC authentication handler"""
    
    def sign_request(self, payload: dict) -> str:
        """Generate HMAC signature for request"""
        
    def verify_response(self, payload: dict, signature: str) -> bool:
        """Verify HMAC signature on response"""
```

#### `RedactionPolicy`
```python
class RedactionPolicy:
    """Redaction policy definition"""
    
    def should_redact(self, classification: Classification) -> bool:
        """Determine if classification should be redacted"""
        
    def get_strategy(self, classification: Classification) -> RedactionStrategy:
        """Get redaction strategy for classification"""
```

#### `Classification`
```python
@dataclass
class Classification:
    """Classification result from classifier"""
    category: str
    confidence: float
    start: int
    end: int
    metadata: dict
```

### Interfaces

#### Observability (Optional)
```python
class ObservabilityClient(Protocol):
    """Optional observability integration"""
    
    def emit_metric(self, name: str, value: float, tags: dict):
        """Emit metric"""
        
    def emit_trace(self, span_name: str, context: dict):
        """Emit trace span"""
        
    def emit_log(self, level: str, message: str, context: dict):
        """Emit structured log"""
```

---

## 🧪 Testing Requirements

### Unit Tests (70% coverage minimum)
- HMAC signing/verification
- Policy evaluation
- Redaction strategies
- Error handling
- Input validation

### Integration Tests (20% coverage minimum)
- Mock classifier integration
- End-to-end classify→redact flow
- HMAC authentication flow
- Policy loading and evaluation
- Error scenarios

### Security Tests (Required)
- Invalid HMAC signature rejection
- Replay attack prevention
- Secrets not logged
- Secure defaults enforced

### Performance Tests (Required)
- Latency benchmarks (<100ms HMAC overhead)
- Throughput tests (async)
- Connection pool efficiency

---

## 📚 Documentation Requirements

### README.md
- Quick start (install, basic usage)
- Features overview
- Security model explanation
- Examples (sync and async)
- Configuration guide
- Contributing guide

### API Documentation
- Full docstrings (Google style)
- Type annotations
- Parameter descriptions
- Return value descriptions
- Exception documentation

### Guides
- `docs/SECURITY.md` - Security best practices
- `docs/DEPLOYMENT.md` - Deployment patterns
- `docs/POLICIES.md` - Policy creation guide
- `examples/` - Working examples

---

## 🔄 Integration Points

### Required Integrations
- Classifier endpoint (HTTP/HTTPS)
- HMAC shared secret (environment variable)

### Optional Integrations
- beast-observability (telemetry)
- beast-mailbox-core (for distributed scenarios)
- Any logging framework (via stdlib logging)

### Zero Dependencies on Cloud Providers
- Works with AWS, GCP, Azure, on-prem
- No cloud-specific code
- Pure Python, platform-agnostic

---

## 🚀 Success Criteria

### Package Quality
- [ ] Published to PyPI
- [ ] 90%+ test coverage
- [ ] Zero Bandit HIGH/MEDIUM issues
- [ ] Black/Flake8/MyPy compliant
- [ ] Comprehensive documentation

### Reusability
- [ ] Used in aws-nvidia-hackathon-app
- [ ] Used in gcp-cloud-run-app (if built)
- [ ] Usable in ANY Python application
- [ ] No hard dependencies on other Beast packages

### Production-Ready
- [ ] Semantic versioning
- [ ] CHANGELOG maintained
- [ ] GitHub releases
- [ ] CI/CD pipeline
- [ ] Security best practices documented

---

## 🎯 Stakeholders

### Primary: Us
- Production-ready package for portfolio
- Reusable across projects
- Demonstrates security expertise

### Secondary: Hackathon Judges
- Shows quality software development
- Demonstrates security consciousness
- Evidence of enterprise thinking

### Tertiary: Open Source Community
- Useful standalone package
- Clear documentation
- Easy integration

---

## 📝 Traceability

**Maps to**:
- Hackathon Requirements: RED-001 (primary), SEC-011, DATA-011
- program/requirements/mapping.yaml: `beast-redaction-client` component
- AWS×NVIDIA Submission: Demonstrates technological implementation, security

**Used By**:
- aws-nvidia-hackathon-app
- gcp-cloud-run-app
- beast-compliance-toolkit
- Any future application needing classification/redaction

---

**Next**: Create `design.md` with architecture, API contracts, and implementation plan.

