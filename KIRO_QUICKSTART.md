# Kiro Commands Quick Start

## ✅ Integration Complete

cc-sdd spec-driven development is now fully integrated into OpenFlow Playground with 11 Kiro commands available in Cursor IDE.

## 🎯 Available Commands

### Project Memory
- `/kiro:steering` - Generate/update project memory (product, tech, structure)
- `/kiro:steering-custom` - Add domain-specific steering (api-standards, security, etc.)

### Feature Development
- `/kiro:spec-init <feature>` - Start new feature specification
- `/kiro:spec-requirements <feature>` - Create requirements.md
- `/kiro:spec-design <feature>` - Create design.md
- `/kiro:spec-tasks <feature>` - Create tasks.md
- `/kiro:spec-impl <feature> <task-ids>` - Implement specific tasks

### Validation
- `/kiro:validate-gap <feature>` - Analyze existing code vs requirements
- `/kiro:validate-design <feature>` - Validate design integration
- `/kiro:validate-impl <feature>` - Validate implementation

### Status
- `/kiro:spec-status <feature>` - Check feature status and progress

## 🚀 Try It Now

### Example 1: Continue Research Agent Development

The Research Agent specification is already created! Continue with design:

```
/kiro:spec-design vercel-ai-chatui-research-agent
```

This will create `.kiro/specs/vercel-ai-chatui-research-agent/design.md` based on the requirements.

### Example 2: Start a New Multi-Agent Feature

```
/kiro:spec-init Multi-Agent Task Orchestration System

/kiro:spec-requirements multi-agent-orchestration

/kiro:spec-design multi-agent-orchestration -y

/kiro:spec-tasks multi-agent-orchestration -y

/kiro:spec-impl multi-agent-orchestration 1.1,1.2,1.3
```

### Example 3: Update Project Memory

Already done! Check out the steering docs:

```bash
cat .kiro/steering/product.md
cat .kiro/steering/tech.md
cat .kiro/steering/structure.md
```

To refresh with latest codebase changes:

```
/kiro:steering
```

### Example 4: Add Domain-Specific Steering

```
/kiro:steering-custom beast-mode-patterns
```

This creates `.kiro/steering/custom/beast-mode-patterns.md` with agent collaboration patterns.

## 📁 What's Where

### Specifications
```
.kiro/specs/
└── vercel-ai-chatui-research-agent/
    └── requirements.md          ✅ Created
    # Next: design.md, tasks.md
```

### Project Memory
```
.kiro/steering/
├── product.md                   ✅ Created
├── tech.md                      ✅ Created
└── structure.md                 ✅ Created
```

### Templates (Customizable)
```
.kiro/settings/
├── templates/
│   ├── specs/                   # Requirements, design, tasks templates
│   ├── steering/                # Product, tech, structure templates
│   └── steering-custom/         # Domain-specific templates
└── rules/                       # SDD methodology rules
```

### Commands
```
.cursor/commands/kiro/           # 11 Kiro slash commands
```

## 🎨 Customization

### Customize Templates

Edit templates in `.kiro/settings/templates/` to match your workflow:

**Example: Add security review section to requirements**
```bash
# Edit template
vim .kiro/settings/templates/specs/requirements.md

# Add new section
## Security Considerations
- [ ] Authentication requirements
- [ ] Authorization model
- [ ] Data encryption
- [ ] Input validation
```

**Example: Add Beast Mode integration checklist to design**
```bash
vim .kiro/settings/templates/specs/design.md

# Add checklist
## Beast Mode Integration
- [ ] Message types defined
- [ ] Agent discovery implemented
- [ ] Capability registration
- [ ] Trust metrics integration
```

### Customize Steering

Edit steering docs to reflect your architecture:

```bash
vim .kiro/steering/tech.md
# Add new technical decision
# Update conventions
# Document new patterns
```

## 🔍 Validation Workflow

For existing code (brownfield development):

```bash
# 1. Create requirements
/kiro:spec-requirements user-authentication

# 2. Check what's missing (gap analysis)
/kiro:validate-gap user-authentication

# 3. Create design
/kiro:spec-design user-authentication

# 4. Validate design fits architecture
/kiro:validate-design user-authentication

# 5. If approved, proceed with tasks
/kiro:spec-tasks user-authentication -y

# 6. Implement
/kiro:spec-impl user-authentication 1.1,1.2,1.3
```

## 🎓 Learning Resources

### Internal Docs
- **Integration Summary**: `CC_SDD_INTEGRATION_SUMMARY.md`
- **AI Agent Context**: `AGENTS.md`
- **Project README**: `README.md` (updated with SDD section)

### External Resources
- **cc-sdd GitHub**: https://github.com/gotalab/cc-sdd
- **Command Reference**: `cc-sdd/docs/guides/command-reference.md`
- **Customization Guide**: `cc-sdd/docs/guides/customization-guide.md`
- **Kiro Methodology**: https://kiro.dev/docs/specs/

## 🤝 Beast Mode Integration

Research Agent spec already includes Beast Mode requirements:

**From requirements.md:**
```markdown
### Requirement 7: Beast Mode Integration
WHEN the Research Agent is initialized THEN it SHALL register with the Beast Mode agent discovery system
WHEN research requests are received via Redis pub/sub THEN the system SHALL process them and respond appropriately
```

This demonstrates how SDD + Beast Mode work together:
- **SDD**: Structured requirements and design
- **Beast Mode**: Multi-agent coordination implementation
- **Combined**: Systematic multi-agent feature development

## 💡 Pro Tips

### 1. Use Quality Gates
Don't skip approval steps (avoid `-y` in production):
```bash
/kiro:spec-requirements research-agent
# Review requirements.md, make edits if needed
/kiro:spec-design research-agent
# Review design.md, ensure it matches architecture
```

### 2. Version Control Specs
Commit specs with code:
```bash
git add .kiro/specs/research-agent/
git commit -m "feat(research-agent): Add requirements and design"
```

### 3. Update Steering Regularly
When architecture changes:
```bash
/kiro:steering
# Reviews codebase and updates steering docs
```

### 4. Validate Before Implementation
Catch issues early:
```bash
/kiro:validate-gap <feature>      # Before design
/kiro:validate-design <feature>   # Before tasks
```

## 🐛 Troubleshooting

### Commands Not Showing in Cursor

1. Reload Cursor window: `Cmd+Shift+P` → "Reload Window"
2. Check commands exist: `ls -la .cursor/commands/kiro/`
3. Verify Cursor recognizes them: Type `/kiro:` and see autocomplete

### Steering Docs Not Loading

Steering docs are manually managed (not auto-loaded by commands). To reference:
```bash
# View current steering
cat .kiro/steering/*.md

# Update steering
/kiro:steering
```

### Template Customization Not Working

After editing templates in `.kiro/settings/templates/`, they apply to **new specs only**. Existing specs need manual updates:

```bash
# Existing spec (not affected by template changes)
.kiro/specs/research-agent/requirements.md

# New spec (uses updated template)
/kiro:spec-requirements new-feature
```

## 🎯 Next Steps

### Immediate
1. ✅ **Try Research Agent design**: `/kiro:spec-design vercel-ai-chatui-research-agent`
2. ✅ **Create tasks**: `/kiro:spec-tasks vercel-ai-chatui-research-agent -y`
3. ✅ **Implement first task**: `/kiro:spec-impl vercel-ai-chatui-research-agent 1.1`

### Short-term
- Customize templates for OpenFlow-specific workflows
- Add Beast Mode patterns to steering-custom
- Create specs for other planned features
- Test validation commands on existing code

### Long-term
- Build library of reusable multi-agent specs
- Contribute improvements back to cc-sdd
- Document OpenFlow SDD patterns
- Train team on spec-driven workflow

## 📊 Success Metrics

Track your SDD adoption:

```bash
# Count specs
ls -1 .kiro/specs/ | wc -l

# Check completion
grep -r "Status:" .kiro/specs/*/requirements.md

# Review steering freshness
ls -lt .kiro/steering/
```

---

**Ready to use!** Start with `/kiro:spec-design vercel-ai-chatui-research-agent` to continue the Research Agent feature.

**Questions?** See `AGENTS.md` for AI agent guidance or `CC_SDD_INTEGRATION_SUMMARY.md` for complete integration details.

