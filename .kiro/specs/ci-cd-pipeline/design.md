# Design Document: CI/CD Pipeline

## Introduction

This design document describes the CI/CD pipeline architecture derived from existing implementations. The system has **dual implementation** - local tools for developer testing and remote workflows for automated validation.

**Design Principle**: Local-Remote Parity - Developers can run the same checks locally that CI runs remotely.

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Workstation                     │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │ Makefile   │  │  Scripts   │  │ Quality System CLI  │   │
│  │  Targets   │→ │   (.py)    │→ │ (code_quality_cli)  │   │
│  └────────────┘  └────────────┘  └─────────────────────┘   │
│         ↓              ↓                     ↓               │
│    make test     quality_check.py    python -m ...cli ci    │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    git push origin
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions (Remote)                  │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │ copilot-   │  │ quality-   │  │   cloud-build       │   │
│  │ review.yml │  │ gates.yml  │  │   .yml              │   │
│  └────────────┘  └────────────┘  └─────────────────────┘   │
│         ↓              ↓                     ↓               │
│    Security &     Quality Gates        Docker Build         │
│    Compliance     + Model Check        + GCP Deploy         │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Local Components (Developer Tools)

#### 1. Makefile Targets
**File**: `Makefile`  
**Purpose**: Simple command interface for common operations

**Targets**:
```makefile
make test      # → uv run pytest tests/ -v
make lint      # → uv run flake8 + mypy
make format    # → uv run black src/ tests/
make install   # → pip install dependencies
make clean     # → Remove temp files
```

**Design Decision**: Thin wrappers around UV commands for consistency

#### 2. Quality Check Script
**File**: `scripts/quality_check.py`  
**Purpose**: Comprehensive local quality validation

**Checks Performed**:
```python
# scripts/quality_check.py
checks = [
    (["uv", "run", "black", "--check", "src/", "tests/"], "Python formatting"),
    (["uv", "run", "ruff", "check", "src/", "tests/"], "Python linting"),
    (["uv", "run", "mdformat", "--check", "docs/", "*.md"], "Markdown"),
    (["uv", "run", "yamlfix", "--check", "*.yaml", "*.yml"], "YAML"),
]
```

**Design Decision**: Run multiple formatters/linters in sequence

#### 3. Code Quality System CLI
**File**: `src/code_quality_system/cli.py`  
**Purpose**: Comprehensive quality analysis and enforcement

**Commands**:
```python
# src/code_quality_system/cli.py
python -m src.code_quality_system.cli ci        # CI/CD mode
python -m src.code_quality_system.cli analyze   # Analysis mode
python -m src.code_quality_system.cli enforce   # Enforcement mode
```

**Key Classes**:
- `CICDIntegration` - CI/CD pipeline integration
- `QualityEnforcer` - Quality rule enforcement
- `QualityMultiAgentAdapter` - Multi-agent analysis

**Design Decision**: Rich Python CLI for complex quality analysis

#### 4. Copilot Review Automation
**File**: `scripts/github_integration/copilot_review_automation.py`  
**Purpose**: GitHub Copilot integration with security-first approach

**Functions**:
```python
class CopilotReviewAutomation:
    async def request_copilot_review(pr_number: int)
    async def analyze_security(pr_number: int)
    async def check_model_compliance(pr_number: int)
```

**Design Decision**: Provides manual review instructions (GitHub App permissions not available)

### Remote Components (GitHub Actions)

#### 1. Copilot Review Workflow
**File**: `.github/workflows/copilot-review.yml`  
**Trigger**: PRs (opened, synchronize, reopened)

**Steps**:
```yaml
1. Checkout code
2. Setup Python 3.11
3. Install dependencies (pip + uv + uv sync)
4. Run Security Analysis (copilot_review_automation.py)
5. Comment Review Summary
6. Request Manual Copilot Review
```

**Permissions**: pull-requests: write, contents: read, actions: read

**Design Decision**: Automated security analysis with manual review instructions

#### 2. Quality Gates Workflow
**File**: `.github/workflows/quality-gates.yml`  
**Trigger**: PRs to main/develop/staging

**Steps**:
```yaml
1. Checkout code
2. Set up Python 3.11
3. Install UV (astral-sh/setup-uv@v1)
4. Install dependencies (uv sync --all-extras)
5. Run quality analysis (python -m src.code_quality_system.cli ci)
6. Upload quality report
7. Quality Gate Decision (fail if below threshold)
8. Quality Summary (to PR)
```

**Environment-Specific Thresholds**:
- Production: 85.0 (fail_on_quality: true)
- Staging: 70.0 (fail_on_quality: true)
- Development: 50.0 (fail_on_quality: false)

**Design Decision**: Environment-aware quality enforcement

#### 3. Cloud Build Workflow
**File**: `.github/workflows/cloud-build.yml`  
**Trigger**: PRs/pushes to main/develop/staging

**Steps**:
```yaml
1. Checkout code
2. Authenticate to Google Cloud
3. Setup Google Cloud CLI
4. Trigger Cloud Build (gcloud builds submit)
   - Polls for completion (15 min timeout)
   - Fetches logs on failure
5. Check deployment status (curl health endpoint)
```

**Design Decision**: Asynchronous Cloud Build with polling for status

### Cloud Build Implementation

#### CloudBuild Configuration
**File**: `cloudbuild.yaml`

**Steps**:
```yaml
1. Build Docker image (gcr.io/$PROJECT_ID/kiro-agent:latest)
   - Uses Dockerfile.kiro-agent
   - Multi-stage build (builder + runtime)
2. Push to Google Container Registry
```

**Design Decision**: Two-stage Docker build for optimal image size

#### Docker Implementation
**File**: `Dockerfile.kiro-agent`

**Architecture**:
```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
- Install build deps (build-essential, curl, git)
- Install UV package manager
- Copy pyproject.toml, uv.lock
- Run: uv sync --frozen --no-dev --no-install-project

# Stage 2: Runtime
FROM python:3.12-slim as runtime
- Install runtime deps (curl, ca-certificates)
- Create non-root user (kiro)
- Copy .venv from builder
- Copy application code:
  - src/
  - main.py
  - subprojects/kiro-ai-development-hackathon/
  - project_model_registry.json
  - pdca.mdc
- Set environment variables (BEAST_MODE_ENABLED, etc.)
- Expose ports 8080, 9090
- Health check: curl -f http://localhost:8080/health
- Run as non-root user
- CMD: python main.py
```

**Design Decision**: Minimal runtime image, non-root security, health checks

## Component Mapping: Local ↔ Remote

### Dependency Installation

**Local**:
```bash
uv sync                # Install all deps
uv sync --all-extras   # Install with optional deps
```

**Remote - copilot-review.yml**:
```yaml
- pip install uv
- uv sync
```

**Remote - quality-gates.yml**:
```yaml
- uses: astral-sh/setup-uv@v1
- uv sync --all-extras
```

**Design**: Same UV commands, different setup methods

### Quality Analysis

**Local**:
```bash
make lint                                    # Flake8 + MyPy
python scripts/quality_check.py              # Black, Ruff, mdformat
python -m src.code_quality_system.cli ci     # Comprehensive analysis
```

**Remote - quality-gates.yml**:
```yaml
- python -m src.code_quality_system.cli ci
```

**Design**: Remote uses the same CLI that runs locally

### Security Analysis

**Local**:
```bash
python scripts/github_integration/copilot_review_automation.py
```

**Remote - copilot-review.yml**:
```yaml
- python scripts/github_integration/copilot_review_automation.py
```

**Design**: Exact same script runs locally and remotely

### Docker Build

**Local**:
```bash
docker build -f Dockerfile.kiro-agent -t kiro-agent:test .
docker run -p 8080:8080 kiro-agent:test
curl http://localhost:8080/health
```

**Remote - cloud-build.yml → cloudbuild.yaml**:
```yaml
gcloud builds submit --config=cloudbuild.yaml
# Then polls for completion
# Then checks: curl https://.../health
```

**Design**: Local Docker mirrors remote Cloud Build

## Data Flow

### Pull Request Flow

```
Developer → git push
     ↓
GitHub detects PR
     ↓
Triggers 3 workflows in parallel:
     ├─→ copilot-review.yml
     │     ├─ Install deps (uv sync)
     │     ├─ Security analysis
     │     └─ Comment summary
     │
     ├─→ quality-gates.yml
     │     ├─ Install deps (uv sync --all-extras)
     │     ├─ Quality analysis (cli ci)
     │     ├─ Check threshold
     │     └─ Upload report
     │
     └─→ cloud-build.yml
           ├─ Authenticate GCP
           ├─ Submit Cloud Build
           ├─ Poll for completion
           └─ Check health endpoint
```

### Cloud Build Flow

```
cloud-build.yml → gcloud builds submit
     ↓
Cloud Build reads cloudbuild.yaml
     ↓
Executes build steps:
  1. docker build -f Dockerfile.kiro-agent
       ↓
     Builder stage:
       - Install UV
       - uv sync (install deps from pyproject.toml)
       ↓
     Runtime stage:
       - Copy .venv from builder
       - Copy src/, main.py, etc.
       - Set user to kiro (non-root)
       ↓
  2. docker push gcr.io/.../kiro-agent:latest
     ↓
cloud-build.yml polls for SUCCESS
     ↓
Checks health endpoint
     ↓
PR check passes
```

## Configuration Points

### 1. Python Version
**Locations**:
- `pyproject.toml`: `requires-python = ">=3.10"`
- `.github/workflows/*.yml`: `python-version: '3.11'`
- `Dockerfile.kiro-agent`: `FROM python:3.12-slim`

**Design**: Must work across 3.10, 3.11, 3.12

### 2. Dependencies
**Source**: `pyproject.toml`
**Install Method**: `uv sync`
**Special**: Git dependency requires `allow-direct-references = true`

**Locations**:
```toml
# pyproject.toml
[tool.hatch.metadata]
allow-direct-references = true  # For beast-ai-dev-agent

dependencies = [
    "beast-ai-dev-agent @ git+https://github.com/nkllon/beast-ai-dev-agent.git",
    # ... 140+ other deps
]
```

### 3. Quality Thresholds
**Source**: `.github/workflows/quality-gates.yml`

```yaml
env:
  QUALITY_THRESHOLD: ${{ github.ref == 'refs/heads/main' && '85.0' || github.ref == 'refs/heads/staging' && '70.0' || '50.0' }}
  FAIL_ON_QUALITY: ${{ github.ref == 'refs/heads/main' && 'true' || github.ref == 'refs/heads/staging' && 'true' || 'false' }}
```

**Design**: Stricter for production, lenient for development

### 4. GCP Configuration
**Source**: `.github/workflows/cloud-build.yml`

```yaml
- project_id: gen-lang-client-0128452200
- credentials: ${{ secrets.GCP_SA_KEY }}
- health_url: https://ghostbusters-api-container-1077539189076.us-central1.run.app/health
```

## Implementation Components

### Component 1: CICDIntegration
**File**: `src/code_quality_system/integrations/ci_cd_integration.py`

**Responsibilities**:
- Detect CI environment (GitHub Actions, GitLab CI, etc.)
- Load CI-specific configuration
- Run multi-agent quality analysis
- Generate quality reports
- Apply environment-specific rules

**Key Methods**:
```python
_detect_ci_environment() -> str       # "github_actions", "gitlab_ci", etc.
_load_ci_config() -> dict            # CI-specific config
_load_environment_rules() -> dict    # development/staging/production rules
run_ci_quality_check() -> dict       # Main CI entry point
```

### Component 2: QualityEnforcer
**File**: `src/code_quality_system/quality_enforcer.py`

**Responsibilities**:
- Enforce quality standards
- Calculate quality scores
- Evaluate quality gates
- Auto-fix issues (if enabled)
- Block on failure (if configured)

**Configuration**:
```python
enforcement_level: "strict" | "moderate" | "lenient"
auto_fix_enabled: bool
block_on_failure: bool
```

### Component 3: CopilotReviewAutomation
**File**: `scripts/github_integration/copilot_review_automation.py`

**Responsibilities**:
- Request Copilot code reviews
- Analyze security issues
- Check model compliance
- Post review summaries

**Fallback Behavior**:
```python
# Handles missing grpc module gracefully
try:
    from src.secure_shell_service.elegant_client import secure_execute
except ImportError:
    # Fallback implementation without grpc
    async def secure_execute(command: str) -> dict:
        # Alternative implementation
```

### Component 4: RoundTripQualityValidator
**File**: `src/code_quality_system/round_trip_validation.py`

**Responsibilities**:
- Validate end-to-end workflows
- Test each workflow step independently
- Ensure round-trip consistency

**Workflow Steps Tested**:
1. development_quality_check
2. pre_commit_validation
3. ci_cd_quality_gates
4. deployment_approval
5. post_deployment_validation

## Execution Paths

### Path 1: Local Development
```
Developer makes changes
     ↓
make lint               # Local linting
     ↓
make test               # Local tests
     ↓
python -m ...cli ci     # Local quality check (optional)
     ↓
git commit              # No pre-commit hooks currently
     ↓
git push
```

### Path 2: Pull Request (Remote)
```
PR opened/updated
     ↓
Parallel execution:
     ├─→ copilot-review.yml (18s)
     │     ├─ uv sync
     │     └─ copilot_review_automation.py
     │
     ├─→ quality-gates.yml (~2-3min)
     │     ├─ uv sync --all-extras
     │     └─ python -m ...cli ci
     │
     └─→ cloud-build.yml (~6-10min)
           ├─ gcloud builds submit
           ├─ Docker multi-stage build
           ├─ uv sync in container
           ├─ Push to GCR
           └─ Health check
```

### Path 3: Cloud Build (GCP)
```
gcloud builds submit
     ↓
Read cloudbuild.yaml
     ↓
docker build -f Dockerfile.kiro-agent
     ↓
Stage 1 (builder):
  - Install UV
  - Copy pyproject.toml, uv.lock
  - uv sync --frozen --no-dev --no-install-project
  - Creates .venv with all deps (including beast-ai-dev-agent)
     ↓
Stage 2 (runtime):
  - Copy .venv from builder
  - Copy application code (src/, main.py, etc.)
  - Set non-root user (kiro)
  - Set environment variables
  - HEALTHCHECK configured
  - CMD: python main.py
     ↓
Push to gcr.io/gen-lang-client-0128452200/kiro-agent:latest
     ↓
Deploy to Cloud Run (implied)
```

## Design Decisions

### 1. UV Package Manager
**Rationale**: Fast, deterministic dependency resolution  
**Implementation**: Used in local Makefile, all CI workflows, and Dockerfile  
**Alternative Considered**: pip, poetry (rejected for speed/consistency)

### 2. Multi-Stage Docker Build
**Rationale**: Smaller runtime images, faster deployments  
**Implementation**: Separate builder and runtime stages  
**Benefit**: Runtime image doesn't include build tools (435 MB smaller)

### 3. Local-Remote Parity
**Rationale**: Developers can reproduce CI failures locally  
**Implementation**: Same commands run locally and in CI  
**Benefit**: Faster debugging, fewer surprise CI failures

### 4. Parallel Workflow Execution
**Rationale**: Faster feedback to developers  
**Implementation**: 3 independent GitHub Actions workflows  
**Tradeoff**: Uses more CI minutes but provides faster results

### 5. Environment-Specific Quality Rules
**Rationale**: Different quality bars for different environments  
**Implementation**: Environment detection in quality-gates.yml  
**Benefit**: Strict in production, lenient in development

### 6. Git Dependencies Support
**Rationale**: Enable use of private/unreleased packages  
**Implementation**: `allow-direct-references = true` in pyproject.toml  
**Requirement**: Hatchling build backend configuration

### 7. Non-Root Container Execution
**Rationale**: Security best practice  
**Implementation**: Create `kiro` user in Dockerfile  
**Benefit**: Reduces attack surface

## Interface Specifications

### Health Check Endpoint

**URL**: `GET /health`  
**Response**:
```json
{
  "status": "healthy",
  "platform": "cloudrun",
  "timestamp": "2025-10-30T14:34:56.056838",
  "uptime": 0.0,
  "request_count": 0,
  "error_count": 0,
  "checks": {
    "redis": "healthy",
    "disk": "healthy"
  }
}
```

**Implementation**: `beast_ai_dev_agent.cloudrun.agent.CloudRunKiroAgent.health_check()`

### Analysis Endpoint

**URL**: `POST /analyze`  
**Request**:
```json
{
  "data": "analysis data here"
}
```

**Response**:
```json
{
  "analysis_id": "kiro_cloudrun_abc123",
  "platform": "cloudrun",
  "timestamp": "2025-10-30T...",
  "input_data": {...},
  "analysis_result": {...},
  "metadata": {
    "processing_time": 0.123,
    "data_size": 45
  }
}
```

**Implementation**: `beast_ai_dev_agent.cloudrun.agent.CloudRunKiroAgent.process_request()`

### Metrics Endpoint

**URL**: `GET /metrics`  
**Response**:
```json
{
  "platform": "cloudrun",
  "request_count": 5,
  "error_count": 0,
  "avg_response_time": 0.15,
  "memory_usage": 145.2,
  "cpu_usage": 12.5
}
```

**Implementation**: `beast_ai_dev_agent.cloudrun.agent.CloudRunKiroAgent.get_metrics()`

## Deployment Architecture

### Container Runtime Configuration

**Environment Variables**:
```dockerfile
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:/app/src"
ENV BEAST_MODE_ENABLED="true"
ENV AGENT_COORDINATION_ENABLED="true"
ENV GKE_SERVICE_INTERFACE_ENABLED="true"
ENV LANGCHAIN_ENABLED="true"
ENV LANGGRAPH_ENABLED="true"
ENV LOCAL_LLM_ENABLED="true"
```

**Ports**:
- 8080: HTTP server (FastAPI)
- 9090: Metrics/monitoring (future use)

**Health Check**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

## Testing Strategy

### Local Testing (Before Push)
```bash
# 1. Dependency check
uv sync

# 2. Import test
uv run python -c "from beast_ai_dev_agent import CloudRunKiroAgent"

# 3. Quality check
python -m src.code_quality_system.cli ci

# 4. Docker build
docker build -f Dockerfile.kiro-agent -t kiro-agent:test .

# 5. Container test
docker run -d -p 8080:8080 kiro-agent:test
curl http://localhost:8080/health
```

### Remote Testing (CI)
- copilot-review: Security & compliance
- quality-gates: Quality analysis
- cloud-build: Docker build + deployment

## Success Criteria

### For PR Merge
- [x] copilot-review passes
- [x] quality-gates passes (or environment allows failure)
- [x] cloud-build passes
- [x] GitGuardian passes

### For Container Deployment
- [x] Docker image builds
- [x] All dependencies install
- [x] Container starts
- [x] Health check returns 200
- [x] Agent serves requests

### For Local Verification
- [x] `uv sync` completes
- [x] Imports work
- [x] Docker builds locally
- [x] Container runs locally
- [x] Health check passes locally

---

**Document Status**: Reverse-engineered from implementation  
**Created**: 2025-10-30  
**Source**: .github/workflows/, Makefile, scripts/, src/code_quality_system/  
**Validation**: All components tested locally

