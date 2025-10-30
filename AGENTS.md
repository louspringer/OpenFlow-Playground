# OpenFlow Playground AI Agents

This file provides context for AI coding assistants (Cursor, GitHub Copilot, etc.) working with the OpenFlow Playground project.

## Project Overview

**OpenFlow Playground** is a comprehensive multi-agent collaboration framework and software quality automation system. It combines:

- **Beast Mode Multi-Agent System**: Redis pub/sub-based agent collaboration with 12 message types
- **Ghostbusters**: Multi-agent delusion detection and code quality validation
- **Spec-Driven Development**: Integrated cc-sdd workflow for structured development
- **34 Domains**: Organized into Demo Core, Demo Tools, Infrastructure, Beast Mode, and Integration categories
- **Model-Driven Architecture**: project_model_registry.json as single source of truth

## Quick Start for Agents

### Essential Context Files

Before working on this project, read:

1. **`.kiro/steering/product.md`** - Product vision and capabilities
2. **`.kiro/steering/tech.md`** - Technology stack and decisions
3. **`.kiro/steering/structure.md`** - Project organization and patterns
4. **`project_model_registry.json`** - Domain registry and tool mappings
5. **`README.md`** - Project overview and quick start

### Cursor Rules

This project has 21+ Cursor rules in `.cursor/rules/`. Key rules:

- **`anti-no-verify.mdc`**: NEVER bypass quality gates
- **`model-driven-enforcement.mdc`**: ALWAYS consult project_model_registry.json first
- **`python-execution-enforcement.mdc`**: ALWAYS use `uv run python`, never direct `python`
- **`make-first-enforcement.mdc`**: ALWAYS use Make targets, never run commands directly
- **`security.mdc`**: No hardcoded credentials, use environment variables or 1Password
- **`deterministic-file-editing.mdc`**: Use AST/Black/ruamel.yaml, not heuristic editors
- **`python-quality-enforcement.mdc`**: All Python files must pass Black, Flake8, MyPy

### Kiro Commands Available

The project now has spec-driven development via cc-sdd:

```bash
# Project context
/kiro:steering                    # Generate/update project memory
/kiro:steering-custom            # Add domain-specific steering

# Feature development
/kiro:spec-init <feature>        # Start new feature spec
/kiro:spec-requirements <feature>  # Create requirements.md
/kiro:spec-design <feature>      # Create design.md
/kiro:spec-tasks <feature>       # Create tasks.md
/kiro:spec-impl <feature> <tasks>  # Implement specific tasks

# Validation
/kiro:validate-gap <feature>     # Analyze existing vs requirements
/kiro:validate-design <feature>  # Validate design integration
/kiro:spec-status <feature>      # Check feature status
```

## Development Workflow

### 1. Before Starting Work

```bash
# Read project context
cat .kiro/steering/*.md

# Check current domain
cat project_model_registry.json | jq '.domains'

# Understand Make targets
make help
```

### 2. For New Features

Use spec-driven development:

```bash
/kiro:spec-init Research Agent with Vercel AI SDK
/kiro:spec-requirements research-agent
/kiro:spec-design research-agent -y
/kiro:spec-tasks research-agent -y
/kiro:spec-impl research-agent 1.1,1.2,1.3
```

### 3. For Bug Fixes

```bash
# Run Ghostbusters for multi-agent analysis
make ghostbusters

# Or use specific quality checks
make lint      # Black + Flake8 + MyPy
make test      # Pytest suite
make security  # Bandit scan
```

### 4. Before Committing

```bash
# REQUIRED: All quality checks must pass
make quality-check

# This runs:
# - Black formatting
# - Flake8 linting
# - MyPy type checking
# - Pytest tests
# - Bandit security scan

# NO --no-verify allowed!
git commit -m "feat: Add research agent"
```

## Key Patterns

### Model-Driven Tool Selection

**ALWAYS** consult `project_model_registry.json` before using tools:

```python
# Load the model
with open('project_model_registry.json') as f:
    model = json.load(f)

# Get domain configuration
domain_config = model['domains']['ghostbusters']

# Use specified tools
linter = domain_config['linter']  # "flake8"
formatter = domain_config['formatter']  # "black"
```

### UV Python Execution

**NEVER** use direct `python` commands:

```bash
# ❌ WRONG
python script.py
python -m pytest tests/

# ✅ RIGHT
uv run python script.py
uv run pytest tests/

# ✅ BEST
make test
```

### Deterministic File Editing

**NEVER** use heuristic editors for structured files:

```python
# ✅ YAML files
from ruamel.yaml import YAML
yaml = YAML()
yaml.dump(data, file)

# ✅ JSON files
import json
with open('file.json', 'w') as f:
    json.dump(data, f, indent=2)

# ✅ Python files
import ast
import black
formatted = black.format_file_contents(content, mode=black.FileMode())
```

### Beast Mode Agent Integration

When creating new agents:

```python
from src.beast_mode.message_models import MessageType, BeastModeMessage
from src.beast_mode.beast_mode_bus_client import BeastModeBusClient

class ResearchAgent(BeastModeBusClient):
    def __init__(self):
        super().__init__(
            agent_id="research_agent",
            capabilities=["web_research", "citation_management"]
        )
        self.register_handler(MessageType.HELP_WANTED, self.handle_help_request)
    
    async def handle_help_request(self, message: BeastModeMessage):
        # Process research request
        results = await self.research(message.content)
        # Publish response
        await self.publish_response(MessageType.HELP_RESPONSE, results)
```

## Common Tasks

### Adding a New Domain

1. Create domain directory: `src/<domain_name>/`
2. Add to `project_model_registry.json`:
   ```json
   {
     "domains": {
       "<domain_name>": {
         "patterns": ["*.py"],
         "linter": "flake8",
         "formatter": "black",
         "requirements": ["Requirement 1", "Requirement 2"]
       }
     }
   }
   ```
3. Create domain README: `src/<domain_name>/README.md`
4. Add tests: `tests/unit/test_<domain_name>/`
5. Update documentation: `docs/DOMAIN_REGISTRY.md`

### Integrating External Libraries

1. Add via UV: `uv add <package>`
2. Update `pyproject.toml` if needed
3. Document in `.kiro/steering/tech.md`
4. Add to appropriate domain in model registry

### Creating Cursor Rules

1. Create MDC file: `.cursor/rules/<rule-name>.mdc`
2. Use structured format with YAML frontmatter
3. Document in rule comments
4. Add to model registry if domain-specific

## Troubleshooting

### Import Errors

```bash
# Ensure UV environment is synced
uv sync

# Check installed packages
uv pip list
```

### Quality Check Failures

```bash
# Run individual checks
make lint      # Identify linting issues
make format    # Auto-fix formatting
make type-check  # Type annotation errors
```

### Beast Mode Agent Issues

```bash
# Check Redis connection
redis-cli ping

# Monitor agent discovery
uv run python scripts/bus_inspector.py

# Check agent health
make test-beast-mode
```

### Spec-Driven Development Issues

```bash
# Check kiro installation
ls -la .cursor/commands/kiro/

# Verify templates
ls -la .kiro/settings/templates/

# Check steering docs
cat .kiro/steering/*.md
```

## References

### Internal Documentation
- `docs/DOMAIN_ARCHITECTURE.md` - Architecture overview
- `docs/DOMAIN_REGISTRY.md` - Complete domain catalog
- `docs/guides/` - How-to guides
- `.cursor/rules/` - Cursor rule definitions

### External Resources
- [cc-sdd GitHub](https://github.com/gotalab/cc-sdd) - Spec-driven development tool
- [Kiro IDE](https://kiro.dev) - Enhanced spec management
- [Vercel AI SDK](https://sdk.vercel.ai/docs) - AI SDK documentation
- [Beast Mode Paper](docs/spores/) - Multi-agent collaboration patterns

## External LLM Collaboration

### Multi-Agent Coordination Beyond Beast Mode

OpenFlow Playground coordinates with external LLM agents (Master Planner/Codex, Claude Projects, etc.) using a **PR-based prompts workflow**.

### Prompts System

**Directory Structure:**
```
prompts/
├── outbound/     # Requests we send to external agents
├── inbound/      # Responses delivered via PR
├── processed/    # Validated and accepted responses
└── latent/       # Deferred or ignored items
```

**See `prompts/WORKFLOW.md`** for complete protocol.

### External LLM Constraints

**Reality Check:** External LLMs are security-constrained:
- ❌ Cannot write directly to repositories
- ❌ Cannot push files without review gates
- ❌ Cannot bypass branch protection
- ✅ **CAN create pull requests** (only mechanism)

**This is by design** - product teams balance capability vs. security.

### Working with External Agents

**Step 1: Create Outbound Request**
```bash
# Create a request in prompts/outbound/
cat > prompts/outbound/YYYYMMDD_HHMMSS_<agent>-<topic>.md <<EOF
# Request to <Agent>: <Topic>

## Context
[Provide context]

## What We Need
[List requirements]

## Requested Output
[Specify deliverables]

## Response Delivery Instructions
See prompts/WORKFLOW.md for PR-based delivery protocol.
EOF
```

**Step 2: External Agent Creates PR**
- Agent creates branch: `codex/<agent>-<topic>`
- Adds file: `prompts/inbound/YYYYMMDD_HHMMSS_<agent>-<topic>.md`
- Creates PR with title: `prompt-response: <topic>`
- Includes machine-parseable headers

**Step 3: Review and Merge**
- GitHub Actions validate format
- Human reviews content
- Merge PR (response lands in `prompts/inbound/`)

**Step 4: Process Response**
- Validate response completeness
- Move to `prompts/processed/` if accepted
- Update `program/requirements/mapping.yaml`
- Create implementation PRs as needed

### Required Response Format

External agents must include machine-parseable headers:

```markdown
Requirements: [ID, ...]
Components: [component, ...]
Artifacts:
  - code: <repo/path or URL>
  - policy: <path>
  - diagrams: <path>
Next:
  - [ ] follow-up PR/actions
```

### GitHub Actions Validation

`.github/workflows/validate-prompt-response.yml` auto-checks:
- File naming convention
- Required header format
- No secrets or binaries
- Valid markdown syntax

### The "Hinkiness" Reality

**This PR-based workflow is awkward but unavoidable:**
- External LLMs will ALWAYS be PR-constrained for security
- This is not a bug, it's the product reality
- We design workflows that work WITH constraints, not against them

**Product Manager's Dilemma:**
> "What can web-based LLMs safely do?" → Create PRs, not much else.

### Architecture Pattern

```
┌──────────────┐
│   You/IDE    │ (Create outbound request)
└──────┬───────┘
       │
       ↓ Send to external LLM
┌──────────────┐
│ External LLM │ (Codex, ChatGPT, Claude)
└──────┬───────┘
       │
       ↓ ONLY METHOD: Create PR
┌──────────────┐
│ Pull Request │ (PR-based delivery)
└──────┬───────┘
       │
       ↓ Review + Merge
┌──────────────┐
│ prompts/     │ (Inbound response)
│ inbound/     │
└──────────────┘
```

### When to Use External LLM Coordination

**Use external agents for:**
- Strategic planning (Master Planner)
- Cross-project requirements analysis
- Architecture reviews requiring different perspectives
- Research tasks spanning multiple contexts

**Use Beast Mode (internal) for:**
- Real-time collaboration
- Trust network verification
- Delusion detection (Ghostbusters)
- Multi-agent validation

**Both systems complement each other:** Beast Mode for real-time internal collaboration, external LLM coordination for asynchronous strategic work.

## License & Attribution

**OpenFlow Playground**: MIT License  
**cc-sdd Integration**: MIT License - © gotalab ([github.com/gotalab/cc-sdd](https://github.com/gotalab/cc-sdd))

When working with cc-sdd components, maintain proper attribution as required by the MIT License.

---

**Last Updated**: 2025-01-30  
**For AI Agents**: This file provides essential context. Always read steering docs before making changes.  
**Status**: Active Development

