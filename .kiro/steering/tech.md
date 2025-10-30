# Technical Steering: OpenFlow Playground

## Technology Stack

### Core Languages
- **Python 3.10+**: Primary development language
- **TypeScript**: For cc-sdd integration and Node-based tooling
- **Bash/Shell**: Automation scripts and Make targets

### Frameworks & Libraries

#### Multi-Agent Framework
- **Redis**: Pub/sub messaging for agent communication
- **Python async/await**: Asynchronous agent coordination
- **Custom Beast Mode Protocol**: 12 message types for agent collaboration

#### AI & LLM Integration
- **Vercel AI SDK v5**: Research Agent implementation
- **AI Elements**: Rich UI components for AI interactions
- **LangChain/LangGraph** (planned): Complex agent workflows

#### Web & UI
- **Streamlit**: Primary GUI framework
- **Plotly**: Data visualization and analytics
- **Pandas**: Data processing and analysis

#### Quality & Testing
- **Black**: Code formatting (line-length: 100)
- **Flake8**: Linting (select: F401, E302, E305, W291, W292)
- **MyPy**: Type checking
- **Bandit**: Security scanning
- **Pytest**: Testing framework
- **AST-Enhanced Linter**: Custom Python AST analysis

### Infrastructure

#### Cloud Platform
- **Google Cloud Platform (GCP)**: Primary cloud provider
- **Cloud Build**: CI/CD pipelines
- **Cloud Run**: Containerized deployments
- **Kubernetes/GKE**: Orchestration (Autopilot mode)

#### Data & Storage
- **Neo4j**: Graph database for project relationships
- **Snowflake**: Data warehouse (healthcare demo)
- **Redis**: Agent messaging and caching
- **S3-compatible storage**: Artifact storage

#### Development Tools
- **UV**: Python package management (uv add, uv sync, uv run)
- **Make**: Task automation (Makefile-driven workflows)
- **Docker**: Containerization
- **Git**: Version control with GitHub

## Key Technical Decisions

### 1. UV Over pip/poetry
**Decision**: Use UV for all Python package management  
**Rationale**: Faster, deterministic dependency resolution  
**Enforcement**: Python execution via `uv run python`, never direct `python` commands  
**Configuration**: `pyproject.toml` + `uv.lock`

### 2. Model-Driven Architecture
**Decision**: Project model registry as single source of truth  
**Rationale**: Explicit configuration prevents implicit assumptions  
**Implementation**: `project_model_registry.json` consulted before all tool operations  
**Benefits**: Domain-specific validation, clear tool mappings

### 3. Deterministic File Editing
**Decision**: Never use heuristic editors for structured files  
**Rationale**: Predictable, reproducible changes  
**Tools**:
- **YAML**: `ruamel.yaml` for parsing/serializing
- **JSON**: `json` library with proper formatting
- **Python**: AST + Black for code generation
- **MDC**: Structured tools for Cursor rules

### 4. Quality Gates Enforcement
**Decision**: All code must pass quality checks before commit  
**Rationale**: Prevent technical debt accumulation  
**Implementation**:
- Black formatting required
- Flake8 linting zero errors
- AST parsing successful
- Bandit security scan clean
- **No `--no-verify`** allowed

### 5. Make-First Execution
**Decision**: Use Make targets for all operations  
**Rationale**: Standardized workflows, reproducible builds  
**Examples**:
```bash
make test
make lint
make format
make ghostbusters
make deploy-beast
```

### 6. Security-First Development
**Decision**: No hardcoded credentials, ever  
**Rationale**: Treat every codebase as public  
**Enforcement**:
- Environment variables for secrets
- 1Password integration (`op` CLI)
- Bandit security scanning
- GitGuardian integration (planned)

## Conventions & Patterns

### Project Structure
```
OpenFlow-Playground/
├── src/                    # Source code (34 domains)
│   ├── ghostbusters/      # Multi-agent validation
│   ├── artifact_forge/    # Code analysis
│   ├── beast_mode/        # Agent messaging
│   └── ...
├── tests/                 # Comprehensive test suite
├── scripts/               # Utility scripts
├── .kiro/                 # Spec-driven development
│   ├── specs/            # Feature specifications
│   ├── steering/         # Project memory
│   └── settings/         # Templates and rules
├── project_model_registry.json  # Domain registry
├── pyproject.toml        # UV configuration
└── Makefile              # Task automation
```

### Code Organization
- **Domain-Driven**: Each domain in `src/<domain_name>/`
- **Reflective Module (RM)**: Consistent interfaces across domains
- **Health Monitoring**: Built-in health checks and status reporting
- **Operational Tracking**: Capability reporting and state management

### Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore()`

### Import Strategy
- **Standard library**: First block
- **Third-party**: Second block
- **Local**: Third block
- **No unused imports**: Flake8 F401 enforced

### Type Annotations
- **Required**: For all public functions
- **Optional**: For private/internal functions
- **Tools**: MyPy for type checking
- **Style**: Python 3.10+ syntax (`list[str]` over `List[str]`)

### Error Handling
- **Explicit exceptions**: Custom exception classes per domain
- **Logging**: Comprehensive logging at appropriate levels
- **Graceful degradation**: Fallbacks for non-critical failures
- **User-friendly messages**: Clear error messages for end users

### Testing Strategy
- **Unit tests**: Per-function/class testing
- **Integration tests**: Cross-domain interaction testing
- **Beast Mode tests**: Multi-agent collaboration testing
- **Coverage**: Target 80%+ coverage
- **Fast tests**: Unit tests < 1s, integration tests < 10s

## Tool Integration

### AST-Enhanced Linting
- **Primary**: Use ASTEnhancedLinter for Python analysis
- **Fallback**: Subprocess to Flake8/Black if API unavailable
- **Configuration**: Projected from project_model_registry.json

### Black API Usage
- **Preferred**: Black Python API over CLI
- **Configuration**: `line_length=100`, `target_version="py310"`
- **Enforcement**: Pre-commit hooks + CI/CD

### Git Operations
- **GitHub CLI**: Use `gh` for PR/issue operations
- **Python scripts**: For complex git operations
- **Avoid**: Shell string interpolation and escaping issues

### MCP Integration
- **Use for**: Repository metadata, issue tracking, code review
- **Don't use for**: Local git operations, file modifications
- **Limitation**: MCP servers don't execute shell commands

## Performance Considerations

- **Lazy loading**: JIT tool initialization
- **Caching**: Redis for agent state and responses
- **Streaming**: Real-time updates via WebSocket/SSE
- **Batch processing**: Bulk operations where possible
- **Profiling**: AST profiler for activity modeling

## Security Practices

- **No secrets in code**: Environment variables or 1Password
- **Input validation**: Sanitize all user inputs
- **Output encoding**: Prevent injection attacks
- **SSL/TLS**: HTTPS for all external APIs
- **Least privilege**: Minimal IAM permissions
- **Encryption at rest**: Sensitive data encrypted

## Deployment Architecture

### Container Strategy
- **Base images**: Official Python slim images
- **Multi-stage builds**: Minimal production images
- **Health checks**: Liveness and readiness probes
- **Resource limits**: Memory and CPU constraints

### Cloud Run Configuration
- **Concurrency**: 100 requests per instance
- **CPU**: 2 vCPUs per instance
- **Memory**: 4 GB per instance
- **Auto-scaling**: 0 to 10 instances
- **Timeout**: 300 seconds

### CI/CD Pipeline
- **Trigger**: Push to develop/main branches
- **Stages**: Lint → Test → Build → Deploy
- **Artifacts**: Docker images to GCP Container Registry
- **Rollback**: Automatic on health check failures

---

**Last Updated**: 2025-01-30  
**Maintained By**: OpenFlow Playground Team  
**Status**: Active Development

