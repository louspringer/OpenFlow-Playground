# Model-Driven Testing System: Automatic Test Generation Behavior

## Overview

The model-driven testing system automatically generates test files in the `tests/generated/` directory during test execution. This behavior is **intentional and by design** - it implements the core requirement to "Generate unit tests directly from implementation models."

## What Happens

### 1. Automatic File Generation

- **Location**: `tests/generated/` directory
- **Pattern**: `test_*_*_generated.py` files
- **Timing**: During test execution when `tests/test_model_driven_testing_system.py` runs
- **Trigger**: Test calls `test_generator.generate_tests_for_file()`

### 2. File Naming Convention

Files follow the pattern: `test_{artifact_name}_{artifact_type}_generated.py`

Examples:

- `test_baseexpert_class_generated.py` - Generated from `BaseExpert` class
- `test_ghostbustersorchestrator_module_generated.py` - Generated from module
- `test_calculate_confidence_function_generated.py` - Generated from function

### 3. Generation Process

1. **Source Analysis**: System scans source files matching domain patterns in `project_model_registry.json`
2. **Model Extraction**: Extracts artifact models (classes, functions, modules) using AST analysis
3. **Test Generation**: Creates pytest-compatible test files with basic validation
4. **File Writing**: Writes generated tests to `tests/generated/` directory

## Why This Happens

### Requirements Implementation

This behavior directly implements these requirements from `project_model_registry.json`:

1. **"Generate unit tests directly from implementation models"**
2. **"Ensure tests stay in sync with actual code structure"**
3. **"Integrate with project model registry for comprehensive coverage"**

### Test Validation

The `tests/test_model_driven_testing_system.py` file validates this functionality by:

- Actually calling the test generator
- Creating real generated test files
- Verifying the generated tests are valid Python
- Ensuring tests stay in sync with implementation

## Safety Mechanisms

### Environment Variable Control

```bash
# Disable automatic test generation
export DISABLE_TEST_GENERATION=true

# Re-enable (default behavior)
unset DISABLE_TEST_GENERATION
```

### Code Location

The safety check is in `src/model_driven_testing/test_generator.py`:

```python
AUTO_GENERATION_DISABLED = (
    os.getenv("DISABLE_TEST_GENERATION", "false").lower() == "true"
)
```

## Generated Test Content

### Example Generated Test

```python
#!/usr/bin/env python3
"""
Generated tests for TestBaseExpert
"""

import pytest
from pathlib import Path
from src.ghostbusters.ghostbusters_orchestrator import BaseExpert

class TestBaseExpert:
    """Generated tests for BaseExpert"""

    @pytest.fixture
    def baseexpert(self):
        """Get a fresh BaseExpert instance"""
        return BaseExpert()

    def test_baseexpert_initialization(self, ghostbustersorchestrator):
        """Test that BaseExpert initializes correctly"""
        instance = BaseExpert()
        assert instance is not None
        assert isinstance(instance, BaseExpert)
```

## Configuration

### Domain Patterns

The system scans these patterns from `project_model_registry.json`:

```json
"model_driven_testing": {
  "patterns": [
    "src/model_driven_testing/*.py",
    "src/model_driven_testing/**/*.py",
    "tests/test_model_driven_testing_system.py",
    "**/*model_driven_testing*.py"
  ]
}
```

### Output Directory

Generated tests are written to `tests/generated/` by default.

## Troubleshooting

### Problem: Too Many Generated Files

**Solution**: Set environment variable

```bash
export DISABLE_TEST_GENERATION=true
```

### Problem: Generated Tests Causing Issues

**Solution**: Add to `.gitignore` or exclude from pytest

```bash
# Run tests excluding generated directory
uv run python -m pytest tests/ --ignore=tests/generated/
```

### Problem: Generated Tests Out of Sync

**Solution**: Regenerate by running the test suite

```bash
uv run python -m pytest tests/test_model_driven_testing_system.py -v
```

## Best Practices

### 1. Understand the Behavior

- This is **intentional functionality**, not a bug
- Generated tests validate the test generation system itself
- Files are created during normal test execution

### 2. Version Control

- Consider adding `tests/generated/` to `.gitignore`
- Generated tests are artifacts, not source code
- Regenerate as needed rather than committing

### 3. CI/CD Integration

- Set `DISABLE_TEST_GENERATION=true` in CI/CD environments
- Generated tests are for development/testing, not production

### 4. Development Workflow

- Use generated tests to understand system behavior
- Modify source code to change generated test patterns
- Regenerate tests after significant changes

## Related Files

- **Implementation**: `src/model_driven_testing/test_generator.py`
- **Test Suite**: `tests/test_model_driven_testing_system.py`
- **Configuration**: `project_model_registry.json` (model_driven_testing domain)
- **Output**: `tests/generated/` directory

## Summary

The automatic generation of test files in `tests/generated/` is a **core feature** of the model-driven testing system, not an unintended side effect. It implements the requirement to automatically generate tests from implementation models and validates this functionality through the test suite itself.

**Remember**: This behavior can be controlled with the `DISABLE_TEST_GENERATION` environment variable, but it's designed to work automatically by default.
