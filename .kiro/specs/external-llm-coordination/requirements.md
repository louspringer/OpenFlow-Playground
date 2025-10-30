# Requirements: External LLM Coordination System

**Feature**: Multi-agent collaboration with external LLMs via PR-based prompts workflow  
**Status**: Implemented (reverse-engineered requirements)  
**Date**: 2025-10-30  
**Context**: Enables collaboration with external LLM agents (ChatGPT Codex, Claude Projects, etc.) that are security-constrained to PR-only delivery

## Background

### Problem Statement

OpenFlow Playground requires coordination with external LLM agents for:
- Strategic planning (Master Planner/Codex)
- Cross-project requirements analysis
- Architecture reviews requiring different perspectives
- Research tasks spanning multiple contexts

**Constraints:**
- External LLMs cannot write directly to repositories (security model)
- External LLMs may have limited conversational memory (context overflow)
- External LLMs may be stateless (API-based) or stateful (web-based with sessions)
- Pull requests are the ONLY available mechanism for external LLMs to deliver work

### Product Reality

External LLM products balance capability vs. security:
- ✅ Can create pull requests
- ❌ Cannot push files without review
- ❌ Cannot bypass branch protection
- ❌ Cannot write directly to repositories

This creates "hinky" but unavoidable workflows that must embrace PR-based delivery.

## Core Requirements

### FR-EXT-001: Canonical Prompts Directory Structure

**Requirement**: Establish a structured directory system for managing prompts and responses.

**Acceptance Criteria:**
- [ ] `prompts/outbound/` directory exists for requests sent to external agents
- [ ] `prompts/inbound/` directory exists for raw responses delivered via PR
- [ ] `prompts/processed/` directory exists for validated and accepted responses
- [ ] `prompts/latent/` directory exists for deferred or ignored items
- [ ] Each directory has a `README.md` explaining its purpose
- [ ] Main `prompts/README.md` documents the complete workflow

**Priority**: P0 (Critical)  
**Status**: ✅ Implemented

---

### FR-EXT-002: PR-Based Delivery Protocol

**Requirement**: Define and document a PR-based workflow for external agent responses.

**Acceptance Criteria:**
- [ ] Protocol documented in `prompts/WORKFLOW.md`
- [ ] Step-by-step instructions for external agents
- [ ] PR title format specified: `prompt-response: <topic>`
- [ ] File naming convention specified: `prompts/inbound/YYYYMMDD_HHMMSS_<agent-id>-<topic>.md`
- [ ] Branch naming convention specified: `codex/<agent-id>-<topic>`
- [ ] Machine-parseable response headers defined (Requirements, Components, Artifacts, Next)
- [ ] Rationale documented (why PR-based, why unavoidable)

**Priority**: P0 (Critical)  
**Status**: ✅ Implemented

---

### FR-EXT-003: Stateless Agent Instructions

**Requirement**: Provide explicit, self-contained instructions for stateless or context-limited agents.

**Acceptance Criteria:**
- [ ] Every outbound request includes repository name
- [ ] Every outbound request includes target branch name
- [ ] Every outbound request includes agent ID
- [ ] Every outbound request includes exact PR title
- [ ] Every outbound request includes exact file path
- [ ] "If You Get Lost" section reminds agents to re-read prompt
- [ ] Template provided for creating outbound requests

**Priority**: P0 (Critical)  
**Status**: ✅ Implemented

---

### FR-EXT-004: Automated PR Validation

**Requirement**: Implement GitHub Actions workflow to validate prompt response PRs automatically.

**Acceptance Criteria:**
- [ ] `.github/workflows/validate-prompt-response.yml` exists
- [ ] Triggers on PRs affecting `prompts/inbound/**`
- [ ] Validates PR title format (`prompt-response: <topic>`)
- [ ] Validates file naming convention
- [ ] Validates required headers are present (Requirements, Components, Artifacts, Next)
- [ ] Scans for hardcoded secrets
- [ ] Validates markdown syntax
- [ ] Posts summary comment on PR with validation results

**Priority**: P1 (High)  
**Status**: ✅ Implemented

---

### FR-EXT-005: Agent Documentation

**Requirement**: Document external LLM constraints and coordination patterns in `AGENTS.md`.

**Acceptance Criteria:**
- [ ] "External LLM Collaboration" section added to `AGENTS.md`
- [ ] Stateless nature documented (no conversational memory, context overflow risks)
- [ ] Security constraints documented (PR-only delivery)
- [ ] Step-by-step working instructions provided
- [ ] Required response format specified
- [ ] Architecture diagram showing PR flow
- [ ] Distinction between Beast Mode (internal) and external LLM coordination clarified

**Priority**: P1 (High)  
**Status**: ✅ Implemented

---

### FR-EXT-006: Response Processing Workflow

**Requirement**: Define workflow for validating, accepting, and processing external agent responses.

**Acceptance Criteria:**
- [ ] Maintainer validation checklist defined
- [ ] Process for moving from `inbound/` to `processed/` documented
- [ ] Integration with `program/requirements/mapping.yaml` specified
- [ ] Guidelines for creating implementation PRs based on responses
- [ ] Process for moving to `latent/` if response is deferred

**Priority**: P1 (High)  
**Status**: ✅ Implemented (documented in `prompts/WORKFLOW.md`)

---

### FR-EXT-007: Bidirectional Communication

**Requirement**: Enable acknowledgment and status updates back to external agents.

**Acceptance Criteria:**
- [ ] Template for acknowledgment messages
- [ ] Process for sending status updates via outbound prompts
- [ ] Professional courtesy guidelines (even for AI agents)
- [ ] Traceability of agent collaboration maintained

**Priority**: P2 (Medium)  
**Status**: ✅ Implemented (acknowledgment to Master Planner sent)

---

## Non-Functional Requirements

### NFR-EXT-001: Security

**Requirement**: Ensure no secrets or credentials are exposed in prompt exchanges.

**Acceptance Criteria:**
- [ ] GitHub Actions scans for secrets in response files
- [ ] Common secret patterns detected (API keys, AWS keys, tokens, passwords)
- [ ] PRs rejected if secrets detected
- [ ] Security scanning integrated with validation workflow

**Priority**: P0 (Critical)  
**Status**: ✅ Implemented

---

### NFR-EXT-002: Auditability

**Requirement**: Maintain complete audit trail of agent collaboration.

**Acceptance Criteria:**
- [ ] All outbound requests stored in version control
- [ ] All inbound responses stored in version control
- [ ] PR history provides timeline of collaboration
- [ ] Machine-parseable headers enable automated tracking
- [ ] Status updates reference previous PRs for continuity

**Priority**: P1 (High)  
**Status**: ✅ Implemented

---

### NFR-EXT-003: Scalability

**Requirement**: Support coordination with multiple external agents simultaneously.

**Acceptance Criteria:**
- [ ] Agent ID system allows differentiation
- [ ] File naming prevents collisions
- [ ] Multiple PRs can be in flight simultaneously
- [ ] Validation workflow handles concurrent PRs

**Priority**: P2 (Medium)  
**Status**: ✅ Implemented

---

### NFR-EXT-004: Documentation Quality

**Requirement**: Provide comprehensive, accessible documentation for external agents.

**Acceptance Criteria:**
- [ ] `prompts/WORKFLOW.md` explains complete protocol
- [ ] `prompts/outbound/README.md` provides delivery instructions
- [ ] `AGENTS.md` documents constraints and patterns
- [ ] Examples and templates provided
- [ ] Architecture diagrams included
- [ ] "Hinkiness" acknowledged and explained

**Priority**: P1 (High)  
**Status**: ✅ Implemented

---

## Integration Requirements

### INT-EXT-001: Beast Mode Distinction

**Requirement**: Clarify when to use Beast Mode (internal) vs. external LLM coordination.

**Acceptance Criteria:**
- [ ] Use cases for external agents documented
- [ ] Use cases for Beast Mode documented
- [ ] Complementary nature explained
- [ ] Decision tree for tool selection provided

**Priority**: P2 (Medium)  
**Status**: ✅ Implemented

**Documented patterns:**
- **External agents**: Strategic planning, cross-project analysis, architecture reviews, research
- **Beast Mode**: Real-time collaboration, trust network verification, delusion detection, multi-agent validation

---

### INT-EXT-002: Requirements Mapping Integration

**Requirement**: Integrate external agent responses with `program/requirements/mapping.yaml`.

**Acceptance Criteria:**
- [ ] Process for extracting requirement IDs from responses
- [ ] Process for extracting component references from responses
- [ ] Guidelines for updating mapping.yaml based on responses
- [ ] Validation that requirements trace to components

**Priority**: P1 (High)  
**Status**: ✅ Implemented (Master Planner updated mapping.yaml in PR #28)

---

## Success Criteria

### Validation Metrics

**System is successful when:**
1. External agents can successfully deliver responses via PR
2. GitHub Actions automatically validate PR format
3. Human review and merge happens smoothly
4. Responses integrate with requirements mapping
5. No secrets or credentials exposed
6. Complete audit trail maintained

### Demonstrated Capability

**Proof of success:**
- ✅ Master Planner delivered comprehensive dual-hackathon plan via PR #28
- ✅ Response included 292 lines of strategic mapping
- ✅ Machine-parseable headers present and correct
- ✅ PR merged successfully to target branch
- ✅ Requirements mapping updated with hackathon alignment
- ✅ Acknowledgment sent back to Master Planner

## Dependencies

### External Dependencies
- GitHub API (for PR creation by external agents)
- GitHub Actions (for automated validation)
- External LLM products (ChatGPT, Claude, etc.)
- Human operators (to paste prompts and review PRs)

### Internal Dependencies
- `program/requirements/mapping.yaml` - Target for requirement updates
- Beast Mode system - Internal multi-agent collaboration
- Spec-driven development workflow - For creating implementation specs

## Risks and Mitigations

### Risk: Context Window Overflow

**Impact**: External agents lose early conversation context and forget critical details.

**Mitigation**: ✅ Implemented
- All critical information in self-contained prompts
- Explicit repository, branch, agent-id in every request
- "If You Get Lost" sections remind agents to re-read

### Risk: PR Title/Format Mismatch

**Impact**: PRs don't match validation rules and fail checks.

**Mitigation**: ✅ Implemented
- Exact PR title specified in outbound request
- GitHub Actions validate format automatically
- Clear error messages guide corrections

### Risk: Secret Exposure

**Impact**: Credentials or sensitive data leaked in prompt exchanges.

**Mitigation**: ✅ Implemented
- Automated secret scanning in GitHub Actions
- Pattern matching for common secret types
- PR rejection if secrets detected

### Risk: Agent Confusion

**Impact**: External agent delivers response to wrong branch or repository.

**Mitigation**: ✅ Implemented
- Explicit repository name in every request
- Explicit target branch in every request
- Validation workflow checks file location

## Future Enhancements

### Potential Improvements (Not Required)

**When LLM products mature:**
- Direct file write APIs (unlikely for security)
- Authenticated push access (risky)
- Auto-merge for trusted agents (dangerous)

**Workflow improvements:**
- Automated response parsing and mapping.yaml updates
- Chatbot interface for creating outbound requests
- Dashboard showing agent collaboration status
- Metrics on response quality and turnaround time

**Until then:** PRs are our multi-agent handshake mechanism.

## Traceability

### Implemented Components

| Requirement | Component | Status |
|-------------|-----------|--------|
| FR-EXT-001 | `prompts/` directory structure | ✅ Implemented |
| FR-EXT-002 | `prompts/WORKFLOW.md` | ✅ Implemented |
| FR-EXT-003 | Stateless agent instructions | ✅ Implemented |
| FR-EXT-004 | `.github/workflows/validate-prompt-response.yml` | ✅ Implemented |
| FR-EXT-005 | `AGENTS.md` External LLM section | ✅ Implemented |
| FR-EXT-006 | Response processing workflow | ✅ Implemented |
| FR-EXT-007 | Bidirectional communication | ✅ Implemented |
| NFR-EXT-001 | Secret scanning | ✅ Implemented |
| NFR-EXT-002 | Audit trail | ✅ Implemented |
| NFR-EXT-003 | Multi-agent support | ✅ Implemented |
| NFR-EXT-004 | Documentation quality | ✅ Implemented |
| INT-EXT-001 | Beast Mode distinction | ✅ Implemented |
| INT-EXT-002 | Requirements mapping | ✅ Implemented |

### Validation Evidence

**PR #28** demonstrates complete workflow:
- ✅ Outbound request created with all explicit instructions
- ✅ Master Planner delivered response via PR
- ✅ Response followed protocol (file in `prompts/inbound/`)
- ✅ Machine-parseable headers present
- ✅ Requirements mapping updated
- ✅ PR reviewed and merged
- ✅ Acknowledgment sent back

## Notes

### Reverse-Engineered Requirements

These requirements were **reverse-engineered from implemented solution**. Normally, requirements precede implementation. This spec documents:
- What was built (implementation-first)
- Why it was built (problem context)
- How it should work (acceptance criteria)
- What success looks like (validation metrics)

**Lesson learned**: "There are no solutions without requirements" - even if requirements come after implementation, they're necessary for documentation, validation, and future maintenance.

---

**Last Updated**: 2025-10-30  
**Implementation Status**: Complete  
**Validation**: Demonstrated via PR #28 (Master Planner collaboration)

