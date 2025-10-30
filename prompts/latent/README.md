# Latent Prompts

This directory contains prompts or responses that have been intentionally deferred, require clarification, or are out of scope.

## When to Move Items Here
- Additional input is required before work can proceed
- The request conflicts with current priorities or capacity
- The response is incomplete and waiting on a follow-up PR
- The prompt has been acknowledged but intentionally parked for later review

## Required Metadata Block
Add a short YAML front matter section explaining the status:
```markdown
---
status: latent
reason: awaiting-additional-context | deprioritized | superseded
next_review: <ISO timestamp>
owner: <maintainer or team>
notes: |
  Short explanation of what is blocking progress
---
```

## Stewardship Practices
- Review latent items during weekly planning or operations reviews
- Promote files to `prompts/processed/` once actioned or superseded
- If no longer relevant, document the decision and keep the record for historical traceability

For the full lifecycle overview, see `prompts/README.md` and `prompts/WORKFLOW.md`.
