## Prompts Workflow

This repository uses a **PR-based prompts workflow** to coordinate with external agents (e.g., Master Planner/Codex).

### Directories
- `prompts/outbound/`: Requests we send out
- `prompts/inbound/`: Raw responses delivered via PR
- `prompts/processed/`: Validated responses after PR merge and review
- `prompts/latent/`: Ignored or deferred items

### Why PR-Based?

**External LLMs (ChatGPT Codex, Claude Projects, etc.) are constrained by security models:**
- ❌ Cannot write directly to repositories
- ❌ Cannot push files without GitHub review
- ❌ Cannot bypass branch protection
- ✅ **CAN create pull requests** (only mechanism available)

**This is by design** - product teams balance capability vs. security. We embrace the constraint.

### Delivery Protocol for External Agents

**Step 1: Create PR with Response**
1. Create a new branch: `codex/<agent>-<topic>-<timestamp>`
2. Add file: `prompts/inbound/YYYYMMDD_HHMMSS_<agent>-<topic>.md`
3. Create PR with title: `prompt-response: <topic>`
4. Include this machine-parseable header in the file:
```
Requirements: [ID, ...]
Components: [component, ...]
Artifacts:
  - code: <repo/path or URL>
  - policy: <path>
  - diagrams: <path>
Next:
  - [ ] follow-up PR/actions
```

**Step 2: PR Review Gate (Automated + Human)**
- GitHub Actions validate response format
- Check required headers are present
- Verify no secrets or binaries
- Human reviews content quality

**Step 3: Merge to Inbound**
- PR approved and merged to target branch
- Response file lands in `prompts/inbound/`

**Step 4: Validation and Processing**
- Maintainer validates response
- Moves to `prompts/processed/` if accepted
- Updates `program/requirements/mapping.yaml`
- Creates implementation PRs as needed

**Step 5: Latent (Optional)**
- If response is deferred, moves to `prompts/latent/`
- Can be revisited later

### Maintainer Validation Checklist
- [ ] PR title format: `prompt-response: <topic>`
- [ ] File path: `prompts/inbound/YYYYMMDD_HHMMSS_<agent>-<topic>.md`
- [ ] Required header present and parseable
- [ ] No binary or secrets included
- [ ] Links resolve or are locally referenced
- [ ] Response addresses outbound prompt
- [ ] Ready to move to `prompts/processed/`

### GitHub Actions Validation

See `.github/workflows/validate-prompt-response.yml` for automated checks:
- File naming convention
- Required header format
- No secrets exposed
- Valid markdown syntax
- Links are resolvable

### Rationale

**The "hinkiness" is unavoidable:**
- External LLMs will ALWAYS be PR-constrained for security
- This is not a bug in our design, it's the product reality
- We design workflows that work WITH the constraints, not against them
- PR-based flow provides audit trail and review gates
- Automation can reduce friction but cannot eliminate PRs

**Product Manager Reality Check:**
> "What can web-based LLMs do safely?" → Create PRs, not much else.

### Architecture Diagram

```
┌──────────────────┐
│  Outbound Prompt │  (We create request in prompts/outbound/)
└────────┬─────────┘
         │
         ↓ Human sends to external LLM
┌──────────────────┐
│  External LLM    │  (Codex, ChatGPT, Claude)
│  (Sandboxed)     │
└────────┬─────────┘
         │
         ↓ ONLY METHOD: Create PR
┌──────────────────┐
│  Pull Request    │  (Branch: codex/<topic>)
│  prompts/inbound │  (File: YYYYMMDD_HHMMSS_<agent>-<topic>.md)
└────────┬─────────┘
         │
         ↓ GitHub Actions validate format
┌──────────────────┐
│  Review Gate     │  (Human + CI checks)
└────────┬─────────┘
         │
         ↓ Merge PR
┌──────────────────┐
│  prompts/inbound │  (Response lands here)
└────────┬─────────┘
         │
         ↓ Human validation
┌──────────────────┐
│ prompts/processed│  (Accepted responses)
└──────────────────┘
```

### Future Enhancements

**When LLM products mature (if ever):**
- Direct file write APIs (unlikely for security)
- Authenticated push access (risky)
- Auto-merge for trusted agents (dangerous)

**Until then:** PRs are our multi-agent handshake mechanism.

