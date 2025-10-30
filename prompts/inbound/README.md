# Inbound Prompt Responses

This directory stores **raw responses delivered via pull request** from external LLM agents or other collaborators.

## Purpose
- Capture responses exactly as merged from the `prompt-response` PR workflow
- Provide a staging area for review, validation, and traceability updates
- Preserve the original machine-parseable headers for automation

## Expected Contents
- Files named using `YYYYMMDD_HHMMSS_<agent-id>-<topic>.md`
- Machine-parseable header block:
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
- Additional narrative or attachments referenced in the header

## Handling Checklist
1. Verify GitHub Actions validation succeeded on the originating PR
2. Review response content for completeness and accuracy
3. Update `program/requirements/mapping.yaml` or other downstream artifacts
4. Move the file to `prompts/processed/` once incorporated into the system of record
5. If the response is incomplete, open follow-up work and keep the file here until resolved

## Notes for Maintainers
- Do **not** edit files in-place after merge—apply corrections in follow-up commits or document deltas in processed records
- Use the timestamps to correlate responses with outbound prompts and audit logs
- Keep this directory small by promoting handled responses promptly

See `prompts/README.md` and `prompts/WORKFLOW.md` for the end-to-end protocol.
