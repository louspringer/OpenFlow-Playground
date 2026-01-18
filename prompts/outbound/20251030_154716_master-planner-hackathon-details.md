# Request to Master Planner: Complete Hackathon Requirements

## Context

We're currently working in OpenFlow Playground with ~5 days to hackathon deadline(s). The turnover manifest mentioned:
- **Google Cloud Run Hackathon** (Oct-Nov 2025)
- **AWS×NVIDIA Hackathon** (Sept-Dec 2025)

However, `.kiro/specs/november-hackathon-sprint/requirements-capture.md` states requirements are **MISSING**.

## What We Need

### Complete Hackathon Details

#### Google Cloud Run Hackathon
- **Official Name/Title**: ?
- **Platform**: Devpost? Google Cloud? Other?
- **Exact Deadline**: Date and time with timezone
- **Prize Amount**: ?
- **Official Rules Link**: URL to hackathon page
- **Submission Requirements**:
  - Demo video required? Length?
  - Code repository required? Public/private?
  - Written description? Word limit?
  - Other deliverables?
- **Judging Criteria**:
  - What are they looking for?
  - Scoring rubric if available
  - Key evaluation points

#### AWS×NVIDIA Hackathon
- **Official Name/Title**: ?
- **Platform**: Devpost? AWS? NVIDIA Developer? Other?
- **Exact Deadline**: Date and time with timezone
- **Prize Amount**: ?
- **Official Rules Link**: URL to hackathon page
- **Submission Requirements**:
  - Demo video required? Length?
  - Code repository required? Public/private?
  - Written description? Word limit?
  - AWS/NVIDIA specific requirements?
  - Other deliverables?
- **Judging Criteria**:
  - What are they looking for?
  - Scoring rubric if available
  - Key evaluation points

### Technical Requirements

#### What Must Be Demonstrated?
- Specific technologies required (Cloud Run, NVIDIA GPUs, etc.)
- Integration requirements
- Performance/scalability requirements
- Security requirements
- Any prohibited technologies or approaches

#### What Can We Leverage?
- **Beast Mode framework** - Multi-agent coordination
- **Snowflake OpenFlow infrastructure** - Already built
- **beast-ai-dev-agent** - Production-ready agent package
- **beast-mailbox-core** - Enterprise messaging
- **beast-observability** - Monitoring/telemetry
- **Ontology framework** - Requirements modeling

#### What Needs Building?
- New components required
- Integration work needed
- Demo-specific features
- Judging-specific polish

### Scope Definition

#### MVP Requirements (Must Have)
- What's the minimum viable submission?
- Core functionality required
- Critical integrations

#### Nice-to-Have Features
- What would improve our score?
- Optional enhancements
- Stretch goals

#### Out of Scope
- What should we NOT build?
- Time/effort traps to avoid

## Deliverables Requested

### 1. Complete Requirements Document
Format matching `.kiro/specs/november-hackathon-sprint/requirements-capture.md` template with ALL fields filled in.

### 2. Links to Official Hackathon Pages
Direct URLs to rules, submission guidelines, judging criteria.

### 3. Recommended Strategy
- Which hackathon to prioritize (if both are viable)
- Leverage strategy for existing components
- Build plan for new components
- Timeline with daily milestones

### 4. Risk Assessment
- What could disqualify us?
- What are the gotchas?
- What assumptions need validation?

## Response Delivery Instructions (PR-Based)

**CRITICAL**: You are stateless and security-constrained. Follow these EXACT instructions:

### Repository Information
- **Repository**: louspringer/OpenFlow-Playground
- **Target Branch**: feat/beast-hackathon-helm-charts-clean
- **Your Agent ID**: master-planner

### Step 1: Create Branch
- **Exact branch name**: codex/master-planner-hackathon-requirements

### Step 2: Add Response File
- **Exact file path**: `prompts/inbound/20251030_master-planner-hackathon-requirements.md`
- Include all requested information above
- Use the requirements-capture.md template structure
- Include direct links to official hackathon pages

### Step 3: Create Pull Request
- **Exact PR title**: prompt-response: Complete hackathon requirements
- **Target branch**: feat/beast-hackathon-helm-charts-clean
- **Repository**: louspringer/OpenFlow-Playground

### Required Response Format

```markdown
Requirements: [hackathon-details, technical-requirements, scope-definition]
Components: [beast-mode, snowflake-openflow, observability, classifier]
Artifacts:
  - requirements: prompts/inbound/20251030_master-planner-hackathon-requirements.md
  - links: [hackathon URLs]
Next:
  - [ ] Validate hackathon requirements
  - [ ] Create spec using /kiro:spec-init
  - [ ] Build MVP components
```

### If You Get Lost
- Re-read this entire prompt (you are stateless)
- All required information is in THIS document
- Repository: louspringer/OpenFlow-Playground
- Branch: codex/master-planner-hackathon-requirements
- Target: feat/beast-hackathon-helm-charts-clean

---

**URGENCY**: ~5 days to deadline. We need complete requirements ASAP to start execution using multi-LLM coordination framework.

