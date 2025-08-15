# MDC Rules System Documentation

## 🎯 **Overview**

The MDC Rules System is a comprehensive, model-driven approach to managing Cursor rules (`.mdc` files) with intelligent validation, rule firing identification, and systematic quality enforcement.

## 🏗️ **Architecture**

### **Core Components**

#### 1. **Project Model Registry** (`project_model_registry.json`)
- **Single source of truth** for all project architecture
- **Domain-driven design** with explicit tool mappings
- **Cursor rules domain** containing all mandatory MDC files
- **Rule firing identification** with emoji prefixes

#### 2. **Custom MDC Tools**
- **`mdc_parser.py`**: Handles Cursor's non-standard YAML format
- **`mdc_projector.py`**: Projects fixes from model to MDC files
- **`mdc_writer.py`**: Writes MDC files with proper formatting

#### 3. **Rule Firing Identifier** (`rule_firing_identifier.py`)
- **Identifies which rules apply** to given files and operations
- **Emoji prefixes** for visual identification
- **Operation-based matching** for contextual rule application

### **System Design Principles**

#### **Heuristic + Deterministic Approach**
- **Heuristic tools**: For detection and validation ("paranoia check")
- **Deterministic tools**: For safe modification ("safe fixer")
- **Combination**: Heuristic detection + deterministic fixing

#### **Model-Driven Architecture**
- **Always consult** `project_model_registry.json` first
- **Domain-specific tools** over generic solutions
- **Explicit requirements** traceability

## 📋 **MDC File Standards**

### **Required Frontmatter**
```yaml
---
description: "Clear description of the rule's purpose"
alwaysApply: true  # or false
---
```

### **Globs Field Rules**
- **`alwaysApply: true`**: No globs field needed
- **`alwaysApply: false`**: Must include `globs: *.py,*.js,*.ts,*.yaml` (comma-separated, no quotes)

### **Content Requirements**
- **Markdown content** after frontmatter
- **Clear structure** with proper headings
- **Code examples** where applicable
- **Implementation guidance**

## 🚀 **Rule Firing System**

### **How It Works**
1. **File Analysis**: Check file path against rule globs
2. **Operation Matching**: Match operations to rule purposes
3. **Always Apply**: Rules with `alwaysApply: true` fire regardless
4. **Emoji Identification**: Visual identification of firing rules

### **Operation Mappings**
```python
operation_rule_mapping = {
    "git": ["make_first_enforcement", "pr_procedure_enforcement"],
    "security": ["security"],
    "linting": ["python_quality_enforcement", "intelligent_linter_prevention"],
    "formatting": ["deterministic_editing", "python_quality_enforcement"],
    "package": ["package_management_uv"],
    "testing": ["ghostbusters", "call_more_ghostbusters"],
    "model": ["model_first_enforcement", "model_driven_enforcement"],
    "cleanup": ["cleanup_before_next_thing"],
    "investigation": ["investigation_analysis", "intelligent_policy"],
}
```

### **Emoji Prefixes**
- 🧠 `model_first_enforcement`
- 🔒 `security`
- 🛠️ `tool_integration_patterns`
- 👻 `ghostbusters`
- ⚙️ `deterministic_editing`
- 🐍 `python_quality_enforcement`
- 📦 `package_management_uv`
- 🎯 `make_first_enforcement`
- 📋 `pr_procedure_enforcement`
- 🧹 `cleanup_before_next_thing`
- 🧭 `intelligent_policy`
- 🔍 `investigation_analysis`
- 🏗️ `llm_architect`
- 📊 `model_driven_enforcement`
- 🎼 `model_driven_orchestration`
- 🚨 `call_more_ghostbusters`
- ☁️ `cloudformation_linting`
- 🔧 `dont_break_the_fixer`
- 🧹 `intelligent_linter_prevention`
- ⚡ `dynamic_prevention_rules`
- 📄 `yaml_type_specific`

## 🛠️ **Usage Examples**

### **Command Line Usage**
```bash
# Show all rules
python scripts/rule_firing_identifier.py --summary

# Check specific file
python scripts/rule_firing_identifier.py --file .cursor/rules/security.mdc

# Check with operation context
python scripts/rule_firing_identifier.py --file .cursor/rules/security.mdc --operation security

# Validate MDC file
python scripts/mdc_parser.py .cursor/rules/deterministic-editing.mdc
```

### **Python API Usage**
```python
from scripts.rule_firing_identifier import RuleFiringIdentifier
from scripts.mdc_parser import MDCParser

# Initialize rule firing identifier
rfi = RuleFiringIdentifier()

# Check which rules fire for a file
firing_rules = rfi.identify_firing_rules('example.py', 'linting')
rfi.print_firing_rules('example.py', 'linting')

# Parse MDC file
parser = MDCParser()
yaml_data, markdown_content = parser.parse_mdc('.cursor/rules/example.mdc')
```

## 🔧 **Maintenance and Updates**

### **Adding New Rules**
1. **Create MDC file** with proper frontmatter
2. **Add to project model** under `cursor_rules.domains`
3. **Assign emoji prefix** in `emoji_prefixes`
4. **Update operation mappings** if needed
5. **Test rule firing** with the identifier

### **Updating Existing Rules**
1. **Use MDC tools** for modifications
2. **Validate with parser** after changes
3. **Test rule firing** to ensure proper operation
4. **Update documentation** if needed

### **Quality Enforcement**
- **All MDC files** must pass parser validation
- **Rule firing** must work correctly
- **Emoji prefixes** must be unique
- **Documentation** must be current

## 🎯 **Best Practices**

### **Rule Design**
- **Single responsibility**: Each rule should have one clear purpose
- **Clear descriptions**: Use descriptive names and descriptions
- **Proper globs**: Only include globs when `alwaysApply: false`
- **Comprehensive content**: Include examples and implementation guidance

### **System Usage**
- **Always use model**: Consult `project_model_registry.json` first
- **Use custom tools**: Prefer MDC tools over generic YAML tools
- **Test rule firing**: Verify rules work as expected
- **Maintain consistency**: Keep emoji prefixes and operation mappings current

### **Troubleshooting**
- **Parser errors**: Check YAML frontmatter syntax
- **Rule not firing**: Verify globs and operation mappings
- **Emoji issues**: Ensure unique prefixes in project model
- **Validation failures**: Use MDC parser to identify issues

## 🚀 **Next Phase: Neo4j Integration & PyPI Packages**

### **Planned Enhancements**
1. **Neo4j Integration**: Graph-based project model visualization
2. **PyPI Packages**: Distribution of valuable components
3. **Advanced Queries**: Cypher-based architectural analysis
4. **Performance Optimization**: Large-scale query optimization

### **Component Candidates for PyPI**
- **MDC Tools**: Parser, projector, writer
- **Rule Firing Identifier**: Rule identification system
- **Ghostbusters Framework**: Multi-agent validation
- **Model-Driven Tools**: Projection and orchestration
- **Cursor Rules Framework**: Complete rule management system

## 📚 **References**

- **Project Model**: `project_model_registry.json`
- **MDC Tools**: `scripts/mdc_*.py`
- **Rule Firing**: `scripts/rule_firing_identifier.py`
- **Cursor Rules**: `.cursor/rules/*.mdc`

## 🎉 **Success Metrics**

- ✅ **24 MDC files** properly formatted and validated
- ✅ **Rule firing identification** working with emoji prefixes
- ✅ **Custom MDC tools** handling Cursor's special format
- ✅ **Model-driven architecture** fully implemented
- ✅ **DRY principle** enforced through consolidation
- ✅ **Quality gates** established and working

---

**The MDC Rules System is now production-ready and provides a robust foundation for AI-assisted development with comprehensive rule management and validation capabilities.** 🚀
