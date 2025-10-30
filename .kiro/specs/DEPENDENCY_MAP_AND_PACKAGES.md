# Dependency Map & Package Strategy

**Philosophy**: Win whether we win or lose by creating production-ready Beast Mode packages.

**Real Stakeholder**: US - Every component becomes a tested, packageable, reusable asset.

---

## 🎯 Packageable Components (Beast Mode Ecosystem)

### Tier 1: Foundation Packages (No Dependencies)

#### 1. **beast-agent** → PyPI Package ⭐ NEW
- **Purpose**: Base agent class for all Beast Mode agents
- **Dependencies**: beast-mailbox-core (external), minimal stdlib
- **Package Name**: `beast-agent`
- **Reusability**: ANY agent in any repo/branch
- **Pattern**: At least one agent per repo, potentially more per branch
- **Provides**:
  - `BaseAgent` class (all agents inherit)
  - Agent lifecycle (startup, shutdown, health checks)
  - Agent registration and discovery
  - Message handling (via beast-mailbox-core)
  - Capability declaration
  - Standard logging/telemetry hooks
- **Tests**: Unit tests for lifecycle, integration tests for messaging
- **Documentation**: Agent development guide, deployment patterns
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE - HIGHEST PRIORITY

#### 2. **beast-redaction-client** → PyPI Package
- **Purpose**: HMAC-protected classifier client library
- **Dependencies**: NONE (pure client library)
- **Package Name**: `beast-redaction-client`
- **Reusability**: ANY application needing data classification/redaction
- **Tests**: Unit tests for HMAC, integration tests with mock classifier
- **Documentation**: Full API docs, usage examples
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

#### 3. **beast-observability** → PyPI Package  
- **Purpose**: Unified telemetry (logs/metrics/traces) with signed outputs
- **Dependencies**: OTEL SDK (external), Redis (optional)
- **Package Name**: `beast-observability`
- **Reusability**: ANY distributed application needing observability
- **Tests**: Unit tests for collectors, integration tests for OTEL
- **Documentation**: Full instrumentation guide
- **Status**: ✅ EXISTS - needs production hardening

#### 4. **beast-spec-mcp** → MCP Server Package ⭐ NEW
- **Purpose**: MCP server for centralized spec access in multi-agent clusters
- **Dependencies**: MCP SDK, watchdog (file watching), minimal stdlib
- **Package Name**: `beast-spec-mcp`
- **Reusability**: ANY Beast Mode cluster, ANY cc-sdd multi-agent environment
- **Pattern**: One MCP server per cluster
- **Provides**:
  - 11+ MCP tools (get_requirements, get_design, get_tasks, search_specs, etc.)
  - MCP resources for all `.kiro/specs/` files
  - Multi-repository support
  - Real-time spec update propagation
  - Access logging and observability
- **Tests**: Unit tests for MCP protocol, integration tests with agents
- **Documentation**: MCP server setup, cluster integration guide
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE - HIGH PRIORITY (Cluster Infrastructure)
- **Contribution Target**: Pull request to `gotalab/cc-sdd`

### Tier 2: Platform Adapters (Depend on Tier 1)

#### 3. **beast-adapter-aws** → PyPI Package
- **Purpose**: AWS deployment helpers (EKS, SageMaker, ECR)
- **Dependencies**: 
  - boto3 (AWS SDK)
  - beast-observability (telemetry)
  - beast-redaction-client (optional, for secure deployments)
- **Package Name**: `beast-adapter-aws`
- **Reusability**: ANY AWS deployment automation
- **Tests**: Unit tests with mocked AWS, integration tests with localstack
- **Documentation**: EKS/SageMaker deployment guides
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

#### 4. **beast-adapter-gcp** → PyPI Package
- **Purpose**: GCP deployment helpers (Cloud Run, GKE, Artifact Registry)
- **Dependencies**:
  - google-cloud-run (GCP SDK)
  - beast-observability (telemetry)
  - beast-redaction-client (optional, for secure deployments)
- **Package Name**: `beast-adapter-gcp`
- **Reusability**: ANY GCP deployment automation
- **Tests**: Unit tests with mocked GCP, integration tests with emulator
- **Documentation**: Cloud Run deployment guides
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

### Tier 2.5: Agent Framework (Depends on Tier 1)

#### 5. **beast-agentic-framework** → PyPI Package
- **Purpose**: High-level multi-agent coordination framework
- **Dependencies**:
  - beast-agent (base agent class) ⭐
  - beast-mailbox-core (messaging)
  - beast-observability (telemetry)
- **Package Name**: `beast-agentic-framework`
- **Reusability**: ANY multi-agent AI application
- **Provides**:
  - Orchestration patterns
  - Task planning and delegation
  - Agent-to-agent communication patterns
  - Workflow management
  - Trust network validation
- **Tests**: Full test suite, example multi-agent apps
- **Documentation**: Multi-agent patterns, orchestration tutorials
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

### Tier 3: Specialized Integration Packages (Depend on Tier 2 + 2.5)

#### 6. **beast-nim-integration** → PyPI Package
- **Purpose**: NVIDIA NIM client library (LLM + Retrieval)
- **Dependencies**:
  - NVIDIA NIM SDK
  - beast-agent (for NIM-powered agents) ⭐
  - beast-observability (telemetry)
  - beast-adapter-aws (deployment)
- **Package Name**: `beast-nim-integration`
- **Reusability**: ANY application using NVIDIA NIMs
- **Tests**: Unit tests with mock NIMs, integration tests with build.nvidia.com
- **Documentation**: NIM deployment patterns, best practices
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

#### 7. **beast-adk-integration** → PyPI Package
- **Purpose**: Google ADK integration for Cloud Run agents
- **Dependencies**:
  - Google ADK
  - beast-agent (for ADK-powered agents) ⭐
  - beast-observability (telemetry)
  - beast-adapter-gcp (deployment)
- **Package Name**: `beast-adk-integration`
- **Reusability**: ANY application using Google ADK
- **Tests**: Unit tests with mock ADK, integration tests with Cloud Run
- **Documentation**: ADK deployment patterns, agent examples
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

### Tier 4: Compliance/Security Packages (Depend on Tier 1)

#### 7. **beast-compliance-toolkit** → PyPI Package
- **Purpose**: Threat models, policy management, audit trails
- **Dependencies**:
  - beast-observability (audit logging)
  - beast-redaction-client (policy enforcement)
- **Package Name**: `beast-compliance-toolkit`
- **Reusability**: ANY enterprise application needing compliance
- **Tests**: Policy validation tests, audit trail tests
- **Documentation**: Compliance frameworks, templates
- **Status**: ⏳ CREATE AS STANDALONE PACKAGE

---

## 📦 Hackathon-Specific Applications (NOT Packages)

### 8. **aws-nvidia-hackathon-app** → Demo Application
- **Purpose**: Agentic application for AWS×NVIDIA submission
- **Dependencies**: ALL Tier 1-3 packages
- **Package**: NO - this is a demo/reference implementation
- **Reusability**: Reference architecture for others
- **Tests**: E2E tests, deployment validation
- **Documentation**: Full deployment guide, architecture docs
- **Status**: ⏳ BUILD USING PACKAGES

### 9. **gcp-cloud-run-app** → Demo Application (if hackathon exists)
- **Purpose**: Agentic application for Cloud Run submission
- **Dependencies**: Tier 1-2 packages + beast-agentic-framework
- **Package**: NO - this is a demo/reference implementation
- **Reusability**: Reference architecture for GCP
- **Tests**: E2E tests, Cloud Run deployment validation
- **Documentation**: Full deployment guide
- **Status**: ⏳ BUILD IF HACKATHON CONFIRMED

---

## 🔗 Dependency Tree

```
beast-mailbox-core (External package)
│
└── beast-agent (Tier 1) ⭐ FOUNDATION
    │
    ├── beast-agentic-framework (Tier 2.5)
    │   ├── aws-nvidia-hackathon-app (Tier 4)
    │   └── cloud-run-hackathon-app (Tier 4)
    │
    ├── beast-nim-integration (Tier 3)
    │   └── aws-nvidia-hackathon-app (Tier 4)
    │
    └── beast-adk-integration (Tier 3)
        └── cloud-run-hackathon-app (Tier 4)

beast-redaction-client (Tier 1, no deps)
│
├── beast-adapter-aws (Tier 2)
│   └── aws-nvidia-hackathon-app (Tier 4)
│
├── beast-adapter-gcp (Tier 2)
│   └── cloud-run-hackathon-app (Tier 4)
│
└── beast-compliance-toolkit (Tier 4)

beast-observability (Tier 1, minimal deps)
│
├── beast-agent (Tier 1) ⭐
├── beast-adapter-aws (Tier 2)
├── beast-adapter-gcp (Tier 2)
├── beast-nim-integration (Tier 3)
├── beast-adk-integration (Tier 3)
├── beast-agentic-framework (Tier 2.5)
└── beast-compliance-toolkit (Tier 4)

beast-nim-integration (Tier 3)
│
└── aws-nvidia-hackathon-app (Tier 4)
└── gcp-cloud-run-app (Tier 4)

beast-agentic-framework (Tier 3)
│
└── aws-nvidia-hackathon-app (Tier 4)
└── gcp-cloud-run-app (Tier 4)
```

---

## 🎯 Build Order (Bottom-Up, Dependency-Driven)

### Phase 1: Foundation (Tier 1) - START HERE
1. **beast-agent** ⭐ HIGHEST PRIORITY
   - Dependencies: beast-mailbox-core (already exists)
   - Why first: Every other agent/framework depends on this
   - Impact: Standardizes ALL agent development
   - Pattern: One agent per repo minimum, more per branch

2. **beast-redaction-client**
   - Dependencies: NONE
   - Why: Pure client library, no agent dependency

3. **beast-observability** (update)
   - Dependencies: Minimal external
   - Why: Provides telemetry to beast-agent

### Phase 2: Platform Adapters + Framework (Tier 2 + 2.5)  
4. **beast-adapter-aws** - Depends on Tier 1
5. **beast-adapter-gcp** - Depends on Tier 1
6. **beast-agentic-framework** - Depends on beast-agent, beast-observability, beast-mailbox-core

### Phase 3: Specialized Integrations (Tier 3)
7. **beast-nim-integration** - Depends on beast-agent, beast-adapter-aws
8. **beast-adk-integration** - Depends on beast-agent, beast-adapter-gcp

### Phase 4: Compliance (Tier 4)
7. **beast-compliance-toolkit** - Depends on Tier 1

### Phase 5: Applications (Use All Packages)
8. **aws-nvidia-hackathon-app** - Demo using all packages
9. **gcp-cloud-run-app** - Demo using all packages (if time permits)

---

## 📊 Package Quality Standards

### Each Package Must Have:
- ✅ **PyPI-ready structure** (`pyproject.toml`, proper versioning)
- ✅ **90%+ test coverage** (like beast-mailbox-core)
- ✅ **Full documentation** (README, API docs, examples)
- ✅ **Type annotations** (MyPy strict mode)
- ✅ **CI/CD pipeline** (tests, coverage, publish)
- ✅ **Security scan** (Bandit, no vulnerabilities)
- ✅ **Black/Flake8/Ruff** compliant
- ✅ **Semantic versioning** (start at 0.1.0)

### Each Package Gets:
- Dedicated GitHub repo (optional, can be monorepo with subdirs)
- PyPI publication workflow
- Comprehensive README
- Usage examples
- Integration tests

---

## 🏆 Success Metrics

### Hackathon Submission
- ✅ Working demo by Nov 3 @ 2:00pm ET
- ✅ All requirements met
- ✅ High-quality submission

### Real Win (Production Packages)
- ✅ 5-7 new PyPI packages published
- ✅ 90%+ test coverage each
- ✅ Production-ready, reusable
- ✅ Documented and tested
- ✅ Form coherent ecosystem

**Even if we don't win hackathon, we have 5-7 production packages to show for it.**

---

## 🚀 Execution Strategy

### Spec Creation Priority
1. **beast-redaction-client** (Tier 1, foundational)
2. **beast-adapter-aws** (Tier 2, needed for submission)
3. **beast-nim-integration** (Tier 3, hackathon-specific)
4. **beast-agentic-framework** (Tier 3, core capability)
5. **aws-nvidia-hackathon-app** (Tier 4, submission vehicle)
6. **beast-adapter-gcp** (Tier 2, for Cloud Run if time)
7. **beast-compliance-toolkit** (Tier 4, enterprise value)

### Development Approach
- **Package-first**: Each component is a standalone package from day 1
- **Test-driven**: 90%+ coverage requirement enforced
- **Documentation-driven**: README before code
- **Integration-ready**: Examples and usage guides

---

## 🎯 Next Action

Create specs in dependency order, treating each as a **production PyPI package**, not just "hackathon code."

**Start with**: `beast-redaction-client` (no dependencies, foundational, reusable)

Ready?

