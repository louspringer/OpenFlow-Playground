# Structure Steering: OpenFlow Playground

## Organization Pattern

OpenFlow Playground follows a **domain-driven architecture** where functionality is organized into 34 distinct, well-defined domains. Each domain represents a cohesive area of responsibility with clear boundaries and compliance requirements.

## Top-Level Structure

```
OpenFlow-Playground/
├── src/                           # Source code (34 domains)
├── tests/                         # Comprehensive test suite
├── scripts/                       # Utility and automation scripts
├── docs/                          # Documentation
├── .kiro/                         # Spec-driven development (cc-sdd)
├── .cursor/                       # Cursor IDE integration
│   ├── commands/kiro/            # Kiro slash commands
│   └── rules/                    # Cursor rules (21+ MDC files)
├── hackathon/                    # BEAST hackathon implementations
├── deployments/                  # Deployment configurations
├── k8s/                          # Kubernetes manifests
├── project_model_registry.json   # Domain registry (single source of truth)
├── pyproject.toml                # UV package configuration
├── Makefile                      # Task automation
└── README.md                     # Project overview
```

## Domain Architecture

### Domain Categories (5 groups)

#### 1. Demo Core (4 domains)
Core functionality for Snowflake OpenFlow demo:
- `snowflake_openflow_demo` - Main demo implementation
- `deployment_automation` - CloudFormation deployment
- `setup_wizard` - Interactive configuration
- `streamlit_demo_app` - Demo interface

#### 2. Demo Tools (6 domains)
Comprehensive tool ecosystem:
- `ghostbusters` - Multi-agent delusion detection
- `intelligent_linter_system` - AI-powered linting
- `code_quality_system` - Quality management
- `multi_agent_testing` - Testing framework
- `visualization` - SVG visualization engine
- `artifact_forge` - Artifact analysis

#### 3. Demo Infrastructure (6 domains)
Foundation and supporting infrastructure:
- `model_driven_projection` - Model-driven development
- `round_trip_engineering` - Code generation and validation
- `mdc_generator` - Cursor rule generation
- `backlog_management` - Task tracking
- `security_first` - Security scanning (Bandit integration)
- `model_management` - Project model CRUD operations

#### 4. Beast Mode System (8 domains)
Multi-agent collaboration infrastructure:
- `beast_mode_messaging` - Message protocol and types
- `beast_mode_orchestration` - Agent coordination
- `beast_mode_discovery` - Agent discovery system
- `beast_mode_help_system` - Capability-based help matching
- `beast_mode_trust_network` - Trust metrics and reputation
- `beast_mode_monitoring` - Health monitoring and metrics
- `beast_mode_spore_exchange` - Knowledge sharing
- `beast_mode_technical_exchange` - Technical debugging

#### 5. Integration & Deployment (10 domains)
Cloud integration, deployment automation, and domain-specific implementations:
- `cloud_vocabulary_mapping` - Multi-cloud terminology
- `github_integration` - GitHub API and workflows
- `neo4j_integration` - Graph database integration
- `one_password_integration` - Secure credential management
- `project_management` - PDCA cycle and task management
- `healthcare_cdc` - Snowflake healthcare data pipeline
- `gmail_calendar_system` - Multi-service coordination
- `billing_management` - GCP cost analysis
- `cache_manager` - Redis caching layer
- `codeguard_common` - Common code quality utilities

## Source Code Organization

### Domain Structure Pattern
Each domain follows a consistent structure:

```
src/<domain_name>/
├── __init__.py              # Domain exports
├── <domain>_core.py         # Core functionality
├── <domain>_models.py       # Data models (Pydantic)
├── <domain>_handlers.py     # Message/event handlers
├── <domain>_utils.py        # Utility functions
├── tests/                   # Domain-specific tests
└── README.md                # Domain documentation
```

### Example: Ghostbusters Domain
```
src/ghostbusters/
├── __init__.py
├── ghostbusters_orchestrator.py      # Main orchestration
├── ghostbusters_code_quality_expert.py  # Quality analysis
├── ghostbusters_security_expert.py   # Security validation
├── ghostbusters_architecture_expert.py  # Design review
├── recovery_engines/                 # Fix automation
│   ├── type_annotation_fixer.py
│   ├── import_resolver.py
│   └── indentation_fixer.py
└── tests/
    ├── test_orchestrator.py
    └── test_recovery_engines.py
```

## Import Patterns

### Standard Pattern
```python
# Standard library imports
import os
import sys
from typing import List, Dict, Optional

# Third-party imports
import redis
import streamlit as st
from pydantic import BaseModel

# Local domain imports
from src.ghostbusters.ghostbusters_orchestrator import GhostbustersOrchestrator
from src.beast_mode.message_models import MessageType, BeastModeMessage
```

### Cross-Domain Imports (Discouraged)
Domains should communicate through well-defined APIs:
- **Preferred**: Message passing via Redis
- **Alternative**: Shared models in common utilities
- **Avoid**: Direct function imports across domains

## Configuration Files

### Project Model Registry
**Location**: `project_model_registry.json`  
**Purpose**: Single source of truth for domain configuration  
**Structure**:
```json
{
  "domains": {
    "domain_name": {
      "patterns": ["*.py", "*.yaml"],
      "content_indicators": ["keyword1", "keyword2"],
      "linter": "flake8",
      "validator": "pytest",
      "formatter": "black",
      "requirements": ["requirement 1", "requirement 2"]
    }
  }
}
```

### UV Configuration
**Location**: `pyproject.toml`  
**Key Sections**:
```toml
[project]
name = "openflow-playground"
version = "0.1.0"
dependencies = [
    "streamlit>=1.28.0",
    "redis>=4.6.0",
    "pydantic>=2.0.0",
    # ... 50+ dependencies
]

[project.optional-dependencies]
dev = ["pytest>=7.4.0", "black>=23.0.0", "flake8>=6.0.0"]
security = ["bandit>=1.7.0", "safety>=2.3.0"]
```

### Makefile Organization
**Location**: `Makefile`  
**Pattern**: Target per major operation
```makefile
# Quality checks
lint: black flake8 mypy
format: black-format
test: pytest
security: bandit-scan

# Deployment
deploy-beast: build-beast push-beast cloud-run-deploy
build-embeddings: process-documents index-vectors
```

## Test Organization

### Test Structure
```
tests/
├── unit/                    # Unit tests (per domain)
│   ├── test_ghostbusters/
│   ├── test_artifact_forge/
│   └── ...
├── integration/             # Integration tests
│   ├── test_beast_mode_collaboration.py
│   ├── test_multi_agent_workflow.py
│   └── ...
├── e2e/                    # End-to-end tests
│   └── test_snowflake_demo.py
└── conftest.py             # Shared fixtures
```

### Test Naming Convention
- **Unit**: `test_<function_name>.py`
- **Integration**: `test_<workflow_name>.py`
- **E2E**: `test_<scenario_name>.py`

## Documentation Organization

### Docs Structure
```
docs/
├── DOMAIN_ARCHITECTURE.md      # Domain overview
├── DOMAIN_REGISTRY.md          # Domain catalog
├── guides/                     # How-to guides
│   ├── beast_mode_setup.md
│   ├── quality_gates.md
│   └── deployment_guide.md
├── spores/                     # Knowledge artifacts
│   ├── beast_mode_spore.json
│   └── openflow_analysis.md
└── DOCUMENTATION_INDEX.md      # Master index
```

## Spec-Driven Development (.kiro/)

### Structure
```
.kiro/
├── specs/                      # Feature specifications
│   └── <feature-name>/
│       ├── requirements.md     # Requirements document
│       ├── design.md          # Design document
│       ├── tasks.md           # Task breakdown
│       └── implementation/    # Implementation artifacts
├── steering/                   # Project memory
│   ├── product.md             # Product context
│   ├── tech.md                # Technical decisions
│   └── structure.md           # This file
└── settings/                   # Templates and rules
    ├── templates/             # Document templates
    │   ├── specs/
    │   ├── steering/
    │   └── steering-custom/
    └── rules/                 # Steering principles
```

## Naming Conventions

### Files
- **Python modules**: `snake_case.py`
- **Configuration**: `kebab-case.yaml`, `snake_case.json`
- **Documentation**: `UPPER_SNAKE_CASE.md`, `Title_Case.md`
- **Scripts**: `snake_case.py`, `kebab-case.sh`

### Directories
- **Source code**: `snake_case/`
- **Documentation**: `kebab-case/`
- **Feature specs**: `kebab-case-name/`

### Classes & Functions
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore()`

## Anti-Patterns to Avoid

❌ **Don't**:
- Cross-domain direct imports (breaks isolation)
- Hardcoded file paths (use Path objects)
- Circular dependencies between domains
- Mixing configuration and code
- Bypassing quality gates (`--no-verify`)
- Direct Python execution (use `uv run python`)
- Heuristic editing of structured files
- Ignoring project_model_registry.json

✅ **Do**:
- Use message passing for cross-domain communication
- Use Path from pathlib for file operations
- Define clear domain boundaries
- Separate configuration into JSON/YAML
- Run all quality checks before commit
- Use `uv run python` or Make targets
- Use deterministic tools (AST, Black, ruamel.yaml)
- Consult project_model_registry.json first

## Evolution Guidelines

When adding new features:

1. **Check domain fit**: Does it belong in existing domain?
2. **Create new domain**: If functionality is distinct enough
3. **Update model registry**: Add to project_model_registry.json
4. **Follow RM pattern**: Implement Reflective Module interfaces
5. **Add tests**: Unit + integration tests required
6. **Update documentation**: README + domain docs
7. **Create spec**: Use cc-sdd workflow for complex features

---

**Last Updated**: 2025-01-30  
**Maintained By**: OpenFlow Playground Team  
**Status**: Active Development

