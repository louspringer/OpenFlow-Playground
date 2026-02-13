# SDD Specifications Directory

This directory contains all Spec-Driven Development (SDD) specifications for the OpenFlow Playground project.

## Directory Structure

All specification files **MUST** be organized within `.kiro/specs/` following this structure:

```
.kiro/specs/
├── feature-name-1/
│   ├── requirements.md    # Initial phase - WHAT to build
│   ├── design.md          # Second phase - HOW to build it
│   └── tasks.md           # Final phase - Actionable implementation tasks
├── feature-name-2/
│   └── requirements.md    # Partial spec - only requirements phase complete
└── README.md              # This file
```

## File Organization Rules

### ✅ CORRECT Locations

- **Spec Files**: `.kiro/specs/<feature-name>/`
  - requirements.md
  - design.md
  - tasks.md
  - spec.json (optional metadata)

- **Templates**: `.kiro/settings/templates/specs/`
  - Used by `/kiro:spec-*` commands

- **Steering Context**: `.kiro/steering/`
  - product.md
  - tech.md
  - structure.md

### ❌ INCORRECT Locations

- **Root Level**: `/rm-ddd/`, `/feature-name/`
  - Spec directories should NEVER be at repository root
  - These are automatically ignored by .gitignore

- **Archives**: `/rm-ddd.zip`, `/feature-name.zip`
  - No archived specs at root level
  - These are automatically ignored by .gitignore

## SDD Workflow

The spec-driven development workflow follows three phases:

### Phase 1: Requirements
```bash
/kiro:spec-init <feature-description>
/kiro:spec-requirements <feature-name>
```
Creates `requirements.md` with EARS-formatted acceptance criteria.

### Phase 2: Design
```bash
/kiro:spec-design <feature-name>
```
Creates `design.md` with architecture and implementation approach.

### Phase 3: Tasks
```bash
/kiro:spec-tasks <feature-name>
```
Creates `tasks.md` with actionable implementation tasks.

### Implementation
```bash
/kiro:spec-impl <feature-name> <task-ids>
```
Implements specific tasks from the tasks.md file.

## Validation Commands

Check implementation gap (for brownfield projects):
```bash
/kiro:validate-gap <feature-name>
```

Validate design integration:
```bash
/kiro:validate-design <feature-name>
```

Check feature status:
```bash
/kiro:spec-status <feature-name>
```

## Current Specifications

Run this command to see current specs:
```bash
ls -1 .kiro/specs/
```

## Preventing Conflicts

To avoid duplicate or misplaced spec files:

1. **Always use the `/kiro:spec-*` commands** - Don't manually create spec directories
2. **Never create spec files at repository root** - They will be ignored by Git
3. **Archive old specs properly** - Move to `.kiro/specs/archive/` if needed
4. **Use the template system** - Templates ensure consistent formatting

## Migration from Root-Level Specs

If you find spec files at the repository root:

1. **Check for duplicates**: Compare with `.kiro/specs/<feature-name>/`
2. **Keep .kiro/specs/ version**: This is the canonical location
3. **Remove root-level files**: They should be deleted
4. **Verify .gitignore**: Ensure root-level spec patterns are ignored

## Support

For issues with SDD workflow:
- Check `.cursor/commands/kiro/` for command documentation
- Review `.kiro/settings/templates/specs/` for templates
- Consult `.kiro/steering/` for project context
