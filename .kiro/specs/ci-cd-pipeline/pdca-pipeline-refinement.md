# PDCA: Pipeline Refinement Cycle

## Purpose

The CI/CD pipeline itself must evolve through continuous refinement. PDCA (Plan, Do, Check, Adjust) ensures the pipeline adapts to discovered issues, performance problems, and changing requirements.

## PDCA Cycle for Pipeline

### Plan
**What**: Identify needed pipeline improvements
**When**: After failures, performance issues, or requirement changes
**Output**: Documented improvement requirements

**Triggers**:
- CI fails in unexpected ways
- Tests take too long
- False positives block valid PRs
- New tools/frameworks need integration
- Security vulnerabilities discovered

**Example**:
```
Observation: beast-ai-dev-agent dependency caused CI failure
Plan: Add allow-direct-references to pyproject.toml
```

### Do
**What**: Implement the pipeline changes
**When**: After planning phase
**Output**: Updated workflows/scripts/configuration

**Actions**:
- Modify .github/workflows/*.yml
- Update scripts in scripts/
- Change configuration in pyproject.toml, Makefile, etc.
- Document changes in .kiro/specs/ci-cd-pipeline/

**Example**:
```yaml
# Modified pyproject.toml
[tool.hatch.metadata]
allow-direct-references = true  # ← Added
```

### Check
**What**: Verify the pipeline changes work
**When**: After implementation
**Output**: Test results confirming fix

**Validation**:
- Test locally (uv sync, docker build, etc.)
- Push to feature branch (CI runs)
- Monitor CI results
- Check observatory for metrics

**Example**:
```
✅ uv sync - passes locally
✅ CI copilot-review - passes
✅ Docker build - succeeds
```

### Adjust
**What**: Refine based on feedback
**When**: After checking results
**Output**: Further improvements or rollback

**Actions**:
- If working: Document in requirements/design
- If partial: Identify what still needs work
- If broken: Rollback and re-plan
- Always: Update specs to reflect reality

**Example**:
```
Result: CI passes but took 8min (was 6min)
Adjust: Add caching for dependencies
Document: Update design.md with caching strategy
```

## PDCA Application Examples

### Example 1: Python Version Mismatch

**Plan**:
```
Issue: beast-ai-dev-agent requires 3.10+, OpenFlow had 3.9+
Plan: Update requires-python in pyproject.toml
```

**Do**:
```toml
# Changed
requires-python = ">=3.10"  # was ">=3.9"
```

**Check**:
```
✅ uv sync passes locally
✅ CI passes
```

**Adjust**:
```
Document: Update requirements.md to note Python 3.10+ requirement
Result: Gap closed
```

### Example 2: Missing Tests in CI

**Plan**:
```
Issue: Tests exist but don't run in CI (TDD gap)
Plan: Add pytest step to quality-gates.yml
```

**Do**:
```yaml
# Added to quality-gates.yml
- name: Run Tests
  run: uv run pytest tests/ -v --cov=src --cov-report=json
```

**Check**:
```
✅ YAML syntax valid
✅ pytest runs in CI
```

**Adjust**:
```
Document: Update design.md with test execution flow
Update: requirements-gap-analysis.md - TDD gap closed
```

### Example 3: Observatory Integration

**Plan**:
```
Issue: No real-time monitoring (Observatory gap)
Plan: Add event notifications to all workflows
```

**Do**:
```yaml
# Added to copilot-review.yml, quality-gates.yml, cloud-build.yml
- name: Notify Observatory - Started
  run: curl -X POST https://observatory.nkllon.com/api/events ...
```

**Check**:
```
⏳ Waiting for observatory implementation
⏳ Will verify events received
```

**Adjust**:
```
Next: Implement observatory API to receive events
Then: Verify events appear in dashboard
```

## Pipeline Evolution Tracking

### Changes This Session

| Change | Type | Status | PDCA Phase |
|--------|------|--------|------------|
| Python 3.9 → 3.10 | Fix | ✅ Complete | Adjust (closed) |
| allow-direct-references | Fix | ✅ Complete | Adjust (closed) |
| Add pytest to CI | Enhancement | ✅ Complete | Adjust (closed) |
| Observatory notifications | Enhancement | ✅ Complete | Check (waiting for API) |
| Test coverage tracking | Enhancement | ✅ Complete | Adjust (closed) |

### Open PDCA Cycles

| Issue | Current Phase | Next Action |
|-------|---------------|-------------|
| Observatory API not live | Check | Implement FastAPI in beast-observatory |
| No staged deployments | Plan | Define dev/staging/prod strategy |
| Structured logging missing | Plan | Design logging architecture |

## PDCA Integration with SDD

**PDCA complements SDD**:
- SDD: For new features (requirements → design → tasks → impl)
- PDCA: For pipeline refinement (observe → improve → verify → refine)

**When to use PDCA**:
- Pipeline fails unexpectedly
- Performance degrades
- False positives occur
- Tools need updating

**When to use SDD**:
- New feature development
- New agent creation
- New integration

**Both use**:
- Documentation in .kiro/specs/
- Systematic approach
- Validation before completion

## Continuous Improvement

The pipeline is never "done" - it continuously evolves:

```
CI Failure → PDCA
    ↓
Plan: Read full logs, identify all errors
    ↓
Do: Fix all errors, test locally
    ↓
Check: Push, watch CI
    ↓
Adjust: Document changes in specs
    ↓
→ Pipeline improved
    ↓
Next failure → PDCA again
```

## Success Criteria

### PDCA is Working When:
- ✅ Pipeline failures decrease over time
- ✅ Each failure is documented and fixed systematically
- ✅ Specs stay synchronized with implementation
- ✅ Improvements are tracked in requirements-gap-analysis.md
- ✅ Team learns from each PDCA cycle

---

**Status**: PDCA process documented  
**Current Cycle**: Observatory integration (Check phase)  
**Next**: Hackathon sprint (will use PDCA for rapid iteration)

