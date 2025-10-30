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
