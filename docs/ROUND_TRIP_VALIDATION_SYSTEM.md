# Round-Trip Validation System

## Overview
The Round-Trip Validation System is a core architectural component that ensures the project model and generated code stay perfectly synchronized through iterative refinement. This system prevents model-code drift and enforces quality standards at the generation level rather than post-generation fixes.

## Core Principle
**"Model and code must stay in sync through back-and-forth scrubbing"**

## Architecture

### Round-Trip Validation System Components
- **Model Registry**: `project_model_registry.json` - Single source of truth
- **Validation Engine**: `scripts/enforce_round_trip.py` - Enforces round-trip compliance
- **Schema Manager**: `scripts/schema_manager.js` - JavaScript-based model manipulation
- **Quality Gates**: Pre-commit hooks that validate generated code

### Key Components
1. **Model Conformance Requirements**: Define what generated code must meet
2. **Round-Trip Workflow**: Iterative extract → validate → correct → regenerate → test cycle
3. **Scrubbing Mechanism**: Back-and-forth refinement between model and code
4. **Enforcement Rules**: Blocking requirements that prevent quality gate failures

## Workflow

### 1. Extract Model from Current Code
```bash
# Use reverse engineering tools to extract current code into model
python scripts/enhanced_reverse_engineer_v2.py <file_path>
```

### 2. Validate Model Against Requirements
```bash
# Check model conformance using schema validation
node scripts/schema_manager.js
```

### 3. Generate Corrected Code from Validated Model
```bash
# Use model-driven generation to produce corrected code
python scripts/enforce_round_trip.py --generate
```

### 4. Test Generated Code for Correctness
```bash
# Run all quality gates on generated code
make lint
make type-check
make test
```

### 5. If Issues Found, Patch Model and Repeat
```bash
# Use JavaScript tools to update model
node -e "
const fs = require('fs');
const model = JSON.parse(fs.readFileSync('project_model_registry.json', 'utf8'));
// Patch model here
fs.writeFileSync('project_model_registry.json', JSON.stringify(model, null, 2));
"
```

### 6. Use ONLY the Final Generated Result
**Never hand-edit generated files** - only model patches allowed

## Model Conformance Requirements

### Documentation Standards
- **100% docstring coverage** for all public interfaces
- **Code generation MUST include docstrings** during generation, not after
- **Documentation coverage is a blocking requirement**, not a post-generation fix

### Code Quality Standards
- **100% compliance with quality gates** before generation
- **Zero linting errors** in generated code
- **Type checking must pass** with complete coverage
- **All imports must be validated** before code generation

### Round-Trip Engineering Standards
- **All code changes must go through round-trip validation**
- **Generated code must be used, never hand-edited**
- **Model must accurately reflect actual code structure**
- **All patches must go through the round-trip process**

## JavaScript Editing Tools

### Schema Manager (`scripts/schema_manager.js`)
- **JSON Schema validation** using Ajv
- **Schema-driven updates** instead of manual manipulation
- **Model integrity enforcement** through validation
- **Structured model updates** with error checking

### Usage Examples
```javascript
// Load and validate model
const manager = new ProjectModelSchemaManager();
if (manager.loadModel()) {
  // Add new domain
  manager.addDomain('new_domain', domainDefinition);
  
  // Add backlog item
  manager.addBacklogItem(backlogItem);
  
  // Save with validation
  manager.saveModel();
}
```

### Direct Model Manipulation
```javascript
// For complex updates, manipulate model directly
const fs = require('fs');
const model = JSON.parse(fs.readFileSync('project_model_registry.json', 'utf8'));

// Add new system
model.round_trip_validation_system = { /* ... */ };

// Save updated model
fs.writeFileSync('project_model_registry.json', JSON.stringify(model, null, 2));
```

## Benefits

### 1. Prevents Quality Gate Failures
- **No more `--no-verify` bypasses** needed
- **Code meets standards** before generation
- **Quality enforced at model level**, not code level

### 2. Maintains Model-Code Synchronization
- **Model always reflects** actual code structure
- **No drift** between intended and actual implementation
- **Consistent architecture** across the project

### 3. Enables Systematic Improvement
- **Iterative refinement** of both model and code
- **Back-and-forth scrubbing** identifies issues early
- **Continuous validation** prevents regression

### 4. Provides Tooling Infrastructure
- **JavaScript-based model management** for complex updates
- **Schema validation** ensures model integrity
- **Automated workflows** for round-trip compliance

## Implementation Status

### ✅ Completed
- [x] Round-trip validation system defined in model
- [x] Model conformance requirements established
- [x] JavaScript schema manager implemented
- [x] Documentation standards enforced
- [x] Code quality requirements defined

### 🔄 In Progress
- [ ] Integration with existing reverse engineering tools
- [ ] Automated round-trip workflow implementation
- [ ] Quality gate integration with model requirements

### 📋 Planned
- [ ] Round-trip compliance monitoring
- [ ] Automated model-code synchronization
- [ ] Integration with CI/CD pipeline

## Best Practices

### 1. Always Patch the Model First
```bash
# ❌ Wrong: Edit code directly
vim src/some_file.py

# ✅ Right: Update model, then regenerate
node -e "/* update model */"
python scripts/enforce_round_trip.py --generate
```

### 2. Use JavaScript Tools for Complex Updates
```bash
# For simple updates
node scripts/schema_manager.js

# For complex system additions
node -e "
const fs = require('fs');
const model = JSON.parse(fs.readFileSync('project_model_registry.json', 'utf8'));
// Complex model manipulation
fs.writeFileSync('project_model_registry.json', JSON.stringify(model, null, 2));
"
```

### 3. Validate Before Committing
```bash
# Always validate model changes
node scripts/schema_manager.js

# Run round-trip compliance check
python scripts/enforce_round_trip.py --validate
```

### 4. Never Bypass Quality Gates
```bash
# ❌ Wrong: Use --no-verify
git commit --no-verify -m "fix: something"

# ✅ Right: Fix the model, regenerate code
# Then commit clean, quality-compliant code
```

## Conclusion

The Round-Trip Validation System provides a robust foundation for maintaining code quality and architectural consistency. By enforcing model-driven development and preventing quality gate bypasses, it ensures that the project maintains high standards while enabling systematic improvement through iterative refinement.

This system transforms the development workflow from reactive quality fixes to proactive quality enforcement, making `--no-verify` bypasses unnecessary and ensuring that all code meets the project's quality standards from the moment of generation.
