# Prompt Management System

## Purpose

Canonical location for managing prompts across all agents, workflows, and planning activities.

## Directory Structure

```
prompts/
├── inbound/          # Prompts received from external sources
├── outbound/         # Prompts sent to external agents/systems
├── processed/        # Prompts that have been acted upon
├── latent/           # Prompts waiting for action or ignored
└── README.md         # This file
```

## Workflow

```
External Source → inbound/ → [Processing] → outbound/ (if query needed)
                                ↓
                           processed/ (when complete)
                                ↓
                           latent/ (if deferred/ignored)
```

## File Naming Convention

```
YYYYMMDD_HHMMSS_<source>_<topic>.md
```

**Examples**:
- `20251030_143000_master-planner_hackathon-plan.md`
- `20251030_150000_user_feature-request.md`
- `20251030_160000_ci-failure_dependency-issue.md`

## Inbound Prompts

**Location**: `prompts/inbound/`  
**Purpose**: Store prompts received from external sources

**Sources**:
- User requests
- Master Planner responses
- CI/CD failure notifications
- Agent collaboration requests
- Observatory alerts

**Lifecycle**:
1. Receive prompt → Save to `inbound/`
2. Process prompt → Move to `processed/` when complete
3. If needs response → Create prompt in `outbound/`
4. If deferred → Move to `latent/`

**Example**:
```markdown
# inbound/20251030_143000_master-planner_hackathon-plan.md

From: Master Planner
Date: 2025-10-30 14:30:00
Topic: Two Hackathon Sprint Plan

[Master planner's response here]
```

## Outbound Prompts

**Location**: `prompts/outbound/`  
**Purpose**: Store prompts sent to external agents/systems

**Destinations**:
- Master Planner
- Other AI agents
- External APIs
- Team members
- Stakeholders

**Lifecycle**:
1. Create prompt → Save to `outbound/`
2. Send prompt → Mark as sent
3. Receive response → Save response to `inbound/`
4. Complete cycle → Move both to `processed/`

**Example**:
```markdown
# outbound/20251030_143000_master-planner_hackathon-request.md

To: Master Planner
Date: 2025-10-30 14:30:00
Topic: Request comprehensive hackathon plan
Status: SENT

[Request details here]

Response Expected: Yes
Response Received: [inbound/20251030_150000_master-planner_hackathon-plan.md]
```

## Processed Prompts

**Location**: `prompts/processed/`  
**Purpose**: Archive of completed prompt-response cycles

**Contents**:
- Prompts that have been fully acted upon
- Linked to corresponding work (PRs, commits, specs)
- Historical reference for future PDCA cycles

**Metadata**:
```markdown
---
status: processed
received: 2025-10-30T14:30:00Z
completed: 2025-10-30T16:00:00Z
outcome: success
related_work:
  - PR #26
  - .kiro/specs/hackathon-1/
  - commits: abc123, def456
---
```

## Latent Prompts

**Location**: `prompts/latent/`  
**Purpose**: Prompts waiting for action or intentionally ignored

**Categories**:
- **Deferred**: Will process later (with target date)
- **Blocked**: Waiting on dependencies
- **Low Priority**: Not urgent
- **Ignored**: Explicitly decided not to act

**Metadata**:
```markdown
---
status: latent
reason: deferred
target_date: 2025-11-15
blocker: Waiting for hackathon results
priority: low
---
```

## Integration Points

### With cc-sdd Workflow

```bash
# Inbound prompt triggers spec creation
prompts/inbound/<prompt> → /kiro:spec-init <feature>

# Spec completion moves prompt to processed
.kiro/specs/<feature>/complete → prompts/processed/<prompt>
```

### With Observatory

```python
# Prompts generate observatory events
{
  "event_type": "prompt_received",
  "source": "inbound",
  "data": {
    "prompt_file": "20251030_143000_master-planner_hackathon-plan.md",
    "status": "processing"
  }
}
```

### With Beast Mode

```python
# Prompts can trigger agent help requests
prompt = load_prompt("inbound/20251030_143000_user_feature-request.md")
→ publish_message(MessageType.HELP_WANTED, prompt_data)
```

## Prompt Template

```markdown
---
id: <unique-id>
type: inbound | outbound | processed | latent
source: <origin>
destination: <target> (for outbound)
created: <ISO8601 timestamp>
status: received | sent | processing | processed | deferred | ignored
priority: high | medium | low
tags: [hackathon, feature-request, bug-fix, etc.]
---

# <Title>

## Context
<Background information>

## Request/Response
<Actual prompt content>

## Expected Outcome
<What should happen>

## Related Work
- PR #XX
- .kiro/specs/<spec>/
- Commits: <sha1>, <sha2>

## Metadata
- Received: <timestamp>
- Processed: <timestamp>
- Outcome: success | failure | partial
```

## Example Workflow

### 1. Receive Hackathon Plan

```bash
# Master planner responds
cat > prompts/inbound/20251030_150000_master-planner_hackathon-plan.md

# Process the plan
/kiro:spec-init <Hackathon-Name>
/kiro:spec-requirements <hackathon>

# Mark as processed
mv prompts/inbound/20251030_150000_master-planner_hackathon-plan.md \
   prompts/processed/
```

### 2. Send Query

```bash
# Create outbound prompt
cat > prompts/outbound/20251030_143000_master-planner_hackathon-request.md

# Send to master planner (via user)
cat prompts/outbound/20251030_143000_master-planner_hackathon-request.md

# Wait for response in inbound/
```

### 3. Defer Low Priority

```bash
# Low priority feature request
mv prompts/inbound/20251030_120000_user_nice-to-have.md \
   prompts/latent/20251030_120000_user_nice-to-have.md

# Add metadata explaining why deferred
```

## Automation

### Auto-Generate Prompts from Events

```python
# scripts/prompt_generator.py (future)
def ci_failure_to_prompt(failure_data: dict):
    """Convert CI failure to inbound prompt for investigation"""
    prompt_file = f"prompts/inbound/{timestamp}_ci-failure_{failure_type}.md"
    # Generate prompt from failure logs
```

### Auto-Move Processed Prompts

```python
# scripts/prompt_lifecycle.py (future)
def check_prompt_completion(prompt_path: str):
    """Check if prompt has been completed and move to processed/"""
    if spec_exists_for_prompt(prompt):
        move_to_processed(prompt_path)
```

## Success Metrics

1. **Response Time**: Inbound prompts processed within 24 hours
2. **Completion Rate**: 90% of inbound prompts reach processed/
3. **Latent Visibility**: All latent prompts reviewed weekly
4. **Traceability**: 100% of prompts linked to work artifacts

---

**Status**: System defined  
**Current Use**: Master Planner hackathon request  
**Location**: `prompts/` directory  
**Next**: Populate with current prompt cycle

## Program Integration

- Outbound prompts MUST cite requirement IDs (e.g., RED-002, NFR-004) and target the primary component(s).
- Inbound responses MUST include headers:
  - `Requirements:` IDs covered
  - `Components:` impacted components
  - `Artifacts:` produced (code/policy/diagrams)
  - `Next:` actionable follow-ups/PRs
- Maintainers sync results into `program/requirements/mapping.yaml` and update `program/releases`.

## Master Planner Coordination (MCP)

The Master Planner (Codex MCP agent) orchestrates requirement → component → hackathon alignment while PR #26 is in review.

1. **Kickoff** – Create an outbound request under `prompts/outbound/` describing the planning goal (see `20251030_143000_master-planner_hackathon-request.md`).
2. **Inbound Response Handling** – Store responses in `prompts/inbound/`, extract requirement/component references, and promote to `processed/` once the mapping file is updated.
3. **Traceability Update** – Populate `program/requirements/mapping.yaml`:
   - Add/refresh requirement metadata, stakeholder personas, and hackathon deliverables.
   - Extend `requirement_component_hackathon_matrix` to capture cross-hackathon dependencies.
4. **Dependency Graph** – Reference the matrix when generating follow-up prompts so other agents know which components/hackathons/stakeholders are impacted.
5. **Status Broadcast** – Post a summary comment on the active PR noting updated mappings and pending data (e.g., missing official briefs).

> 📌 Keep MCP iterations linked to the same PR until both hackathon requirement packets are on file.
