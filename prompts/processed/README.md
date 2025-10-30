# Processed Prompt Responses

This directory archives prompt exchanges that have been fully incorporated into the program of record.

## Promotion Criteria
- Response content has been reviewed and accepted
- Follow-up work (specs, tasks, PRs) is captured in the relevant systems
- `program/requirements/mapping.yaml` and other traceability assets are updated
- Any outstanding actions are tracked elsewhere (tickets, outbound prompts, etc.)

## Recommended File Structure
Each processed file should retain the original inbound content plus a closing metadata section:
```markdown
---
status: processed
processed_by: <maintainer>
processed_on: <ISO timestamp>
related_work:
  - PR #NN
  - .kiro/specs/<feature>/
  - commits: <sha1>, <sha2>
notes: |
  Summary of how the response was integrated
---
```

## Maintenance Guidelines
- Do not delete historical records—this directory forms part of the audit trail
- Append metadata rather than rewriting the inbound response body
- If a processed response requires correction, create an additional entry documenting the fix

Refer to `prompts/README.md` for the overarching lifecycle and `prompts/WORKFLOW.md` for operational steps.
