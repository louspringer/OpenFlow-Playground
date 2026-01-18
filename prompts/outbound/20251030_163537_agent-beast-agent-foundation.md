# Request to Agent: Build `beast-agent` Foundation Package (Tier 1)

**Priority:** 🔥 **HIGHEST** - All other Beast Mode packages depend on this

**Target Repository:** `nkllon/beast-agent` (CREATE NEW REPOSITORY)

---

## 🎯 Context

You are building the **foundational base class** (`BaseAgent`) for the entire Beast Mode multi-agent ecosystem. This is **Tier 1** in our dependency graph - every other agent package will inherit from this.

**Why This Matters:**
- **`beast-mailbox-agent`** will extend `BaseAgent` (specific LLM implementation)
- **`beast-agentic-framework`** will use `BaseAgent` for orchestration
- **Platform adapters** (AWS, GCP) will use `BaseAgent` for agent-driven deployments
- **At least one agent per repo, more per branch** - standardizes ALL agent development

**Quality Bar:** Match `beast-mailbox-core` (90%+ coverage, 0 defects, SonarCloud A rating, comprehensive docs)

---

## 📋 What You Need to Build

### 1. **Core `BaseAgent` Class**
**File:** `src/beast_agent/base_agent.py`

**Must Provide:**
- Agent lifecycle (`__init__`, `start`, `stop`)
- Integration with `beast-mailbox-core` for messaging
- Agent registration and discovery (Redis-based)
- Capability declaration system
- Message handler registration
- Standardized logging/telemetry hooks (for `beast-observability`)
- Configuration management (env vars, config files, programmatic)

**Key Methods:**
```python
class BaseAgent:
    def __init__(self, agent_id: str, capabilities: List[str], config: Optional[AgentConfig] = None)
    async def start(self) -> None
    async def stop(self) -> None
    def register_handler(self, message_type: str, handler: Callable) -> None
    async def send_message(self, recipient_id: str, message: dict) -> None
    async def publish_event(self, event_type: str, data: dict) -> None
```

### 2. **Agent Discovery Service**
**File:** `src/beast_agent/discovery.py`

- Redis-based agent registry (key-value store: `agents:{agent_id}`)
- Capability querying
- Health check ping/pong

### 3. **Configuration Management**
**File:** `src/beast_agent/config.py`

- `AgentConfig` dataclass
- Environment variable loading
- YAML config file support
- Validation

### 4. **Example Agents**
**Directory:** `examples/`

- `examples/echo_agent.py` - Simple echo agent
- `examples/calculator_agent.py` - Basic capability demo
- Show how to extend `BaseAgent`

### 5. **Comprehensive Tests**
**Directory:** `tests/`

- `tests/test_base_agent.py` - Lifecycle, handlers
- `tests/test_discovery.py` - Registration, querying
- `tests/test_config.py` - Config loading, validation
- **Target:** >= 90% coverage (match beast-mailbox-core)

### 6. **Documentation**
- `README.md` - Features, installation, quickstart, badges
- `docs/AGENT_GUIDE.md` - How to build agents extending BaseAgent
- `docs/DEPLOYMENT.md` - Deployment patterns
- `AGENT.md` - AI maintainer guide (following beast-mailbox-core pattern)
- `CHANGELOG.md` - Version history

---

## 📚 Specifications Provided

**In OpenFlow-Playground `.kiro/specs/` directory:**

1. **`beast-agent/requirements.md`** - Complete functional & non-functional requirements
2. **`QUALITY_STANDARDS_TEMPLATE.md`** - Badges, coverage, SonarCloud integration
3. **`SONARCLOUD_INTEGRATION_GUIDE.md`** - Setup instructions, workflow, troubleshooting

**Reference Implementation:**
- **`nkllon/beast-mailbox-core`** - Shows quality standards, test patterns, documentation structure

---

## 🛠️ Technical Requirements

### Dependencies
```toml
[project]
dependencies = [
  "beast-mailbox-core>=0.3.0",  # For messaging
  "pydantic>=2.0.0",             # Config validation
  "redis>=5.0.0",                # Discovery service
]

[project.optional-dependencies]
dev = [
  "pytest>=7.0.0",
  "pytest-asyncio>=0.21.0",
  "pytest-cov>=4.0.0",
  "pytest-mock>=3.11.0",
  "black>=23.0.0",
  "flake8>=6.0.0",
  "mypy>=1.0.0",
]
```

### File Structure
```
beast-agent/
├── .github/
│   └── workflows/
│       ├── tests.yml          (pytest + coverage)
│       └── sonarcloud.yml     (SonarCloud analysis)
├── src/
│   └── beast_agent/
│       ├── __init__.py        (exports BaseAgent)
│       ├── base_agent.py      (core BaseAgent class)
│       ├── discovery.py       (agent discovery)
│       └── config.py          (configuration)
├── examples/
│   ├── echo_agent.py
│   └── calculator_agent.py
├── tests/
│   ├── test_base_agent.py
│   ├── test_discovery.py
│   └── test_config.py
├── docs/
│   ├── AGENT_GUIDE.md
│   └── DEPLOYMENT.md
├── pyproject.toml
├── sonar-project.properties
├── README.md
├── AGENT.md
├── CHANGELOG.md
└── LICENSE (MIT)
```

---

## ✅ Quality Checklist (MUST PASS before PR)

- [ ] **Coverage >= 90%** (pytest-cov)
- [ ] **Black formatting** (100% compliance)
- [ ] **All tests passing** (pytest)
- [ ] **SonarCloud Quality Gate: PASSED**
- [ ] **0 Code Smells** (SonarCloud)
- [ ] **Maintainability Rating: A** (SonarCloud)
- [ ] **README with badges** (PyPI, Python versions, license, quality gate, coverage)
- [ ] **AGENT.md exists** (AI maintainer guide)
- [ ] **Examples functional** (can run and demonstrate usage)
- [ ] **MIT License** included

---

## 🚀 Response Delivery Instructions (PR-Based)

**CRITICAL**: You are stateless and security-constrained. Follow these EXACT instructions:

### Repository Information
- **GitHub Organization:** `nkllon`
- **Repository Name:** `beast-agent` (**CREATE NEW REPOSITORY**)
- **Target Branch:** `main`
- **Your Agent ID:** `beast-agent-builder`

### Step 1: Create Repository
**YOU MUST CREATE THIS REPOSITORY FIRST**

```bash
# Create new repository via GitHub API or web UI
# Repository: nkllon/beast-agent
# Description: "Foundational base class for Beast Mode multi-agent ecosystem"
# Public: Yes
# License: MIT
# Initialize: Yes (with README, .gitignore Python)
```

### Step 2: Create Feature Branch
- **Exact branch name:** `feature/initial-implementation`

### Step 3: Implement Complete Package
**Commit all files:**
- `src/beast_agent/` (all Python modules)
- `tests/` (all test files)
- `examples/` (example agents)
- `docs/` (documentation)
- `.github/workflows/` (CI/CD)
- `pyproject.toml`, `sonar-project.properties`
- `README.md`, `AGENT.md`, `CHANGELOG.md`, `LICENSE`

### Step 4: Verify Quality Gates
**Before creating PR, ensure:**
- ✅ All tests pass locally
- ✅ Coverage >= 90%
- ✅ Black formatting applied
- ✅ No linter errors

### Step 5: Create Pull Request
- **Title:** `feat: initial beast-agent foundation implementation`
- **Target branch:** `main`
- **Repository:** `nkllon/beast-agent`

**PR Description Template:**
```markdown
## 🎯 Foundation Package Implementation

Complete Tier 1 foundation package for Beast Mode multi-agent ecosystem.

### Implemented
- [x] `BaseAgent` class with lifecycle management
- [x] Agent discovery service (Redis-based)
- [x] Configuration management (env vars, YAML)
- [x] Message handler registration
- [x] Integration with beast-mailbox-core
- [x] Telemetry hooks for beast-observability
- [x] Example agents (echo, calculator)

### Quality Metrics
- **Coverage:** X%
- **Tests:** Y passing
- **SonarCloud:** Quality Gate PASSED
- **Maintainability:** A

### Dependencies
- `beast-mailbox-core>=0.3.0`
- `pydantic>=2.0.0`
- `redis>=5.0.0`

### Breaking Changes
None (initial release)

### Documentation
- ✅ README.md with badges and quickstart
- ✅ AGENT_GUIDE.md (how to extend BaseAgent)
- ✅ DEPLOYMENT.md (deployment patterns)
- ✅ AGENT.md (AI maintainer guide)

### Next Steps
- Publish to PyPI as v0.1.0
- Update beast-mailbox-agent to extend BaseAgent
- Build Tier 2 packages (adapters, framework)
```

---

## 📖 Reference Materials

**Study these before implementing:**

1. **`beast-mailbox-core`** repository structure
   - https://github.com/nkllon/beast-mailbox-core
   - Study: `README.md`, `AGENT.md`, `pyproject.toml`, `.github/workflows/`, `docs/`

2. **Specifications** (in OpenFlow-Playground)
   - `.kiro/specs/beast-agent/requirements.md`
   - `.kiro/specs/QUALITY_STANDARDS_TEMPLATE.md`
   - `.kiro/specs/SONARCLOUD_INTEGRATION_GUIDE.md`

3. **Dependency Map** (in OpenFlow-Playground)
   - `.kiro/specs/DEPENDENCY_MAP_AND_PACKAGES.md`

---

## ⚠️ Critical Constraints

1. **MUST depend on `beast-mailbox-core>=0.3.0`** (for messaging)
2. **MUST support Python 3.9, 3.10, 3.11, 3.12**
3. **MUST achieve >= 90% coverage** (no exceptions)
4. **MUST pass SonarCloud Quality Gate** before merge
5. **MUST include comprehensive documentation**
6. **MUST provide working examples**
7. **MIT License REQUIRED**

---

## 🎓 Implementation Guidance

### BaseAgent Lifecycle Pattern
```python
# Agent starts
await agent.start()
  → Connects to beast-mailbox-core
  → Registers with discovery service
  → Registers message handlers
  → Sets up telemetry hooks
  → Enters message processing loop

# Agent processes messages
message received → handler lookup → execute handler → send response

# Agent stops
await agent.stop()
  → Unregisters from discovery
  → Disconnects from mailbox
  → Cleanup resources
```

### Message Handler Registration
```python
agent = BaseAgent("my-agent", ["capability1", "capability2"])
agent.register_handler("REQUEST", handle_request)
agent.register_handler("HELP_WANTED", handle_help_request)
await agent.start()
```

### Discovery Service Pattern
```python
# Agent registers
await discovery.register(agent_id, capabilities, metadata)

# Other agents query
agents = await discovery.find_by_capability("data_classification")
```

---

## 📦 Deliverables Checklist

### Code
- [ ] `src/beast_agent/base_agent.py` - Core BaseAgent class
- [ ] `src/beast_agent/discovery.py` - Agent discovery service
- [ ] `src/beast_agent/config.py` - Configuration management
- [ ] `src/beast_agent/__init__.py` - Package exports

### Tests
- [ ] `tests/test_base_agent.py` - Lifecycle, handlers, messaging
- [ ] `tests/test_discovery.py` - Registration, querying, health checks
- [ ] `tests/test_config.py` - Config loading, validation
- [ ] Coverage >= 90%

### Examples
- [ ] `examples/echo_agent.py` - Simple echo agent
- [ ] `examples/calculator_agent.py` - Capability demonstration
- [ ] Both examples runnable and documented

### Documentation
- [ ] `README.md` - Badges, features, installation, quickstart
- [ ] `docs/AGENT_GUIDE.md` - How to extend BaseAgent
- [ ] `docs/DEPLOYMENT.md` - Deployment patterns
- [ ] `AGENT.md` - AI maintainer guide
- [ ] `CHANGELOG.md` - Version history

### CI/CD
- [ ] `.github/workflows/tests.yml` - Pytest + coverage
- [ ] `.github/workflows/sonarcloud.yml` - SonarCloud analysis
- [ ] `sonar-project.properties` - SonarCloud configuration

### Configuration
- [ ] `pyproject.toml` - Package metadata, dependencies, build config
- [ ] `.gitignore` - Python standard ignores
- [ ] `LICENSE` - MIT License

---

## 🔗 Integration Points

**`beast-mailbox-core` Integration:**
- Import `RedisMailbox` from `beast-mailbox-core`
- Use for agent-to-agent messaging
- Follow async/await patterns from beast-mailbox-core

**`beast-observability` Integration:**
- Provide hooks for logging/metrics/tracing
- Don't implement observability - just provide integration points
- Example: `self._log_hook(level, message)` for agents to override

---

## 🚨 Common Pitfalls to Avoid

1. ❌ **Don't implement LLM logic** - BaseAgent is foundation, not LLM-specific
2. ❌ **Don't create circular dependencies** - beast-mailbox-core is external dependency
3. ❌ **Don't skip tests** - Coverage >= 90% is non-negotiable
4. ❌ **Don't ignore SonarCloud** - Quality Gate must pass
5. ❌ **Don't over-engineer** - Keep it simple, focused, extensible

---

## 📐 Architecture Principles

1. **Separation of Concerns**
   - BaseAgent handles lifecycle, messaging, discovery
   - Subclasses handle specific logic (LLM, data processing, etc.)

2. **Dependency Injection**
   - Accept mailbox client, discovery client via constructor
   - Allow testing with mocks

3. **Async First**
   - All I/O operations use async/await
   - Follow beast-mailbox-core async patterns

4. **Configuration Over Convention**
   - Support env vars, config files, programmatic config
   - Validate configuration on startup

5. **Telemetry Hooks**
   - Provide integration points, don't implement
   - Allow agents to plug in their own telemetry

---

## 🎯 Success Criteria

Your PR will be merged if:

✅ **Functional**
- BaseAgent can be instantiated and extended
- Agents can register and be discovered
- Message handlers work correctly
- Integration with beast-mailbox-core functional
- Examples run without errors

✅ **Quality**
- Coverage >= 90%
- SonarCloud Quality Gate: PASSED
- 0 Critical/Major defects
- Black formatting: 100%
- All tests passing

✅ **Documentation**
- README with badges (Quality Gate, Coverage, PyPI, License)
- AGENT_GUIDE explains how to extend BaseAgent
- DEPLOYMENT covers deployment patterns
- AGENT.md provides AI maintainer guidance
- Examples well-documented

✅ **Structure**
- Follows beast-mailbox-core project structure
- CI/CD workflows configured
- SonarCloud integrated
- MIT License included

---

## 📋 Response Format (Machine-Parseable Headers)

When you create the PR, include these headers in the PR description:

```markdown
Requirements: FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-AGENT-006
Components: BaseAgent, AgentDiscovery, AgentConfig
Artifacts:
  - code: https://github.com/nkllon/beast-agent/tree/feature/initial-implementation
  - tests: tests/
  - docs: docs/
  - examples: examples/
Coverage: X%
Quality-Gate: PASSED
Next:
  - [ ] Publish to PyPI as v0.1.0
  - [ ] Update beast-mailbox-agent to extend BaseAgent
  - [ ] Create Tier 2 packages (adapters, framework)
```

---

## 🔍 Specifications Reference

**All specs are in `louspringer/OpenFlow-Playground` repository:**

- Path: `.kiro/specs/beast-agent/requirements.md`
- Path: `.kiro/specs/QUALITY_STANDARDS_TEMPLATE.md`
- Path: `.kiro/specs/SONARCLOUD_INTEGRATION_GUIDE.md`
- Path: `.kiro/specs/DEPENDENCY_MAP_AND_PACKAGES.md`

**Clone OpenFlow-Playground to access specs:**
```bash
git clone https://github.com/louspringer/OpenFlow-Playground.git
cd OpenFlow-Playground/.kiro/specs/
cat beast-agent/requirements.md
cat QUALITY_STANDARDS_TEMPLATE.md
cat SONARCLOUD_INTEGRATION_GUIDE.md
```

---

## 💡 If You Get Lost

**Re-read this entire prompt** (you are stateless - all context is HERE)

**Key reminders:**
1. You're building **Tier 1 foundation** - other packages depend on you
2. Quality bar: Match `beast-mailbox-core` (90%+ coverage, 0 defects)
3. Repository: `nkllon/beast-agent` (**CREATE NEW**)
4. Branch: `feature/initial-implementation`
5. PR title: `feat: initial beast-agent foundation implementation`
6. ALL information is in THIS document

**Reference repositories:**
- Study: `nkllon/beast-mailbox-core` (quality standards)
- Do NOT modify: `nkllon/beast-mailbox-agent` (depends on beast-agent, build AFTER)

---

## 🎓 Learning Resources

**Study before implementing:**

1. **beast-mailbox-core README:**
   - https://github.com/nkllon/beast-mailbox-core/blob/main/README.md
   - Note the badges, structure, quality metrics

2. **beast-mailbox-core AGENT.md:**
   - https://github.com/nkllon/beast-mailbox-core/blob/main/AGENT.md
   - Copy this pattern for beast-agent AGENT.md

3. **beast-mailbox-core tests:**
   - https://github.com/nkllon/beast-mailbox-core/tree/main/tests
   - Follow these testing patterns

4. **beast-mailbox-core workflows:**
   - https://github.com/nkllon/beast-mailbox-core/tree/main/.github/workflows
   - Copy and adapt for beast-agent

---

## 🎯 Timeline Estimate

**Day 1 (Today):**
- Create repository
- Implement `BaseAgent` class
- Implement agent discovery
- Implement configuration management

**Day 1.5:**
- Write comprehensive tests
- Achieve >= 90% coverage
- Create example agents

**Day 2:**
- Write documentation (README, AGENT_GUIDE, DEPLOYMENT, AGENT.md)
- Add badges to README
- Configure SonarCloud

**Day 2.5:**
- Verify all quality gates pass
- Test examples
- Finalize CHANGELOG

**Day 3:**
- Create PR
- Address any review feedback
- Prepare for PyPI publication

---

## 🎖️ Success Metrics

**This implementation succeeds when:**

1. ✅ Other agents can extend `BaseAgent` easily
2. ✅ Agent discovery works reliably
3. ✅ Message handlers integrate seamlessly with beast-mailbox-core
4. ✅ Examples demonstrate clear usage patterns
5. ✅ Documentation enables independent agent development
6. ✅ Quality matches beast-mailbox-core standards
7. ✅ Ready for PyPI publication

---

**Remember:** This is the **foundation** of the entire Beast Mode ecosystem. Every agent (beast-mailbox-agent, platform adapters, orchestration framework) will depend on your work. Build it solid, test it thoroughly, document it comprehensively.

**Quality over speed. Get it right the first time.**

---

**Requester:** OpenFlow-Playground AI Agent  
**Date:** 2025-10-30  
**Urgency:** High (blocks all Tier 2+ packages)  
**Expected Completion:** 3 days  
**Questions?** Re-read this document (you are stateless - everything you need is here)

