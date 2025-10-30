# Outbound Prompts

This directory contains prompts sent to external agents, systems, or stakeholders.

## Current Outbound Prompts

### 20251030_143000_master-planner_hackathon-request.md
**To**: Master Planner  
**Status**: SENT  
**Topic**: Two hackathon sprint plan request  
**Response Expected**: Yes  
**Response Location**: `prompts/inbound/` (when received)

---

See `prompts/README.md` for full prompt management system documentation.

## Required Output Format (for responders)

Include a machine-parseable header:

```
Requirements: [FR-050, RED-002, OBS-002]
Components: [kiro-ai-development-hackathon, beast-redaction-client, NiFi]
Artifacts:
  - code: path/to/file or repo link
  - policy: program/requirements/redaction-policy.md (sections X/Y)
  - diagrams: program/devpost/arch.svg
Next:
  - [ ] open PR in kiro with integration
  - [ ] update release pin in program/releases/REL-2025-11.md
```

## Delivery Instructions (for external agents)

**CRITICAL ASSUMPTIONS**:
- You are **stateless** (no memory between invocations)
- You are **security-constrained** (can ONLY deliver via pull request)
- You need **explicit instructions** (repo, branch, agent-id, file paths)

### PR-Based Delivery Process

Each outbound request MUST include these explicit details for stateless agents:

#### Required Information in Every Outbound Request
- **Repository**: Full GitHub repo path (e.g., `louspringer/OpenFlow-Playground`)
- **Target Branch**: Exact branch name to target PR to (e.g., `feat/beast-hackathon-helm-charts-clean`)
- **Agent ID**: Your identifier for file naming (e.g., `master-planner`, `codex`, etc.)
- **Exact PR Title**: Complete title to use (e.g., `prompt-response: hackathon master plan`)
- **Exact File Path**: Complete path with naming format (e.g., `prompts/inbound/YYYYMMDD_HHMMSS_master-planner-topic.md`)

#### Step-by-Step Instructions (For Agents)

**Step 1: Create Branch**
- Branch name: `codex/<agent-id>-<topic>` (exact name provided in request)
- Fork from: Target branch (exact name provided in request)

**Step 2: Add Response File**
- File path: `prompts/inbound/YYYYMMDD_HHMMSS_<agent-id>-<topic>.md` (exact path provided)
- Include required machine-parseable headers (format provided in request)

**Step 3: Create Pull Request**
- PR title: `prompt-response: <topic>` (exact title provided in request)
- PR body: Use template provided in request
- Target branch: Exact branch name from request (CRITICAL - don't guess!)
- Repository: Full repo path from request

**Step 4: Automated Validation (We Handle This)**
- GitHub Actions will validate:
  - PR title format
  - File naming convention
  - Required headers present
  - No secrets exposed
  - Valid markdown syntax

**Step 5: Human Review (We Handle This)**
- Maintainer reviews content
- PR merged (response lands in `prompts/inbound/`)
- Moved to `prompts/processed/` after validation
- Mappings updated in `program/requirements/mapping.yaml`

#### Why Explicit Instructions Matter

**You are stateless**:
- No conversational memory
- Cannot remember previous instructions
- Cannot infer context from earlier messages
- Must have all information in the prompt itself

**Common failures without explicit instructions**:
- PR targets wrong branch (e.g., `main` instead of `feat/...`)
- File lands in wrong directory
- PR title doesn't match validation rules
- Agent ID mismatch between file name and branch name

#### Template for Outbound Requests

```markdown
### Response Delivery Instructions (PR-Based)

**CRITICAL**: You are stateless and security-constrained. Follow these EXACT instructions:

#### Repository Information
- **Repository**: `owner/repo-name`
- **Target Branch**: `branch-name`
- **Your Agent ID**: `agent-identifier`

#### Step 1: Create Branch
- **Exact branch name**: `codex/<agent-id>-<topic>`

#### Step 2: Add Response File
- **Exact file path**: `prompts/inbound/YYYYMMDD_HHMMSS_<agent-id>-<topic>.md`
- **Required content**: [Specify what should be in the response]

#### Step 3: Create Pull Request
- **Exact PR title**: `prompt-response: <topic>`
- **Target branch**: `branch-name` (MUST match exactly)
- **Repository**: `owner/repo-name`

#### If You Get Lost
- Re-read this entire prompt (you are stateless)
- All required information is in THIS document
```

**Note**: PRs are the ONLY mechanism available to external LLMs for security reasons. This "hinkiness" is unavoidable and by design. See `prompts/WORKFLOW.md` for complete protocol.
