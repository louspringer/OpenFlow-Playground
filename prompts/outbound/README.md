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

**You are security-constrained and can ONLY deliver via pull request. This is correct and expected.**

### PR-Based Delivery Process

**Step 1: Create Branch**
- Branch name: `codex/<agent>-<topic>`

**Step 2: Add Response File**
- File path: `prompts/inbound/YYYYMMDD_HHMMSS_<agent>-<topic>.md`
- Include required machine-parseable headers (see format below)

**Step 3: Create Pull Request**
- PR title: `prompt-response: <topic>`
- PR body: Brief summary of response
- Target branch: Current working branch (check outbound request)

**Step 4: Automated Validation**
- GitHub Actions will validate:
  - PR title format
  - File naming convention
  - Required headers present
  - No secrets exposed
  - Valid markdown syntax

**Step 5: Human Review**
- Maintainer reviews content
- PR merged (response lands in `prompts/inbound/`)
- Moved to `prompts/processed/` after validation
- Mappings updated in `program/requirements/mapping.yaml`

**Note**: PRs are the ONLY mechanism available to external LLMs for security reasons. This "hinkiness" is unavoidable and by design. See `prompts/WORKFLOW.md` for complete protocol.
