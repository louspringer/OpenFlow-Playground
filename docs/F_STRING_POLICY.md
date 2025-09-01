# F-String Policy: Complete Guide

## Overview

This project has eliminated the F541 linting rule and standardized on f-strings as the primary string formatting method.

## Policy Statement

**F-strings are mandatory for all string formatting in this project.**

## Why F541 Was Eliminated

- **No security value**: F-strings without placeholders pose no security risk
- **False positives**: Rule creates unnecessary cognitive overhead
- **Style enforcement**: Enforces personal preferences as security requirements
- **Real security focus**: Should be on input validation, SQL injection, command injection

## Usage Standards

### ✅ Always Use F-Strings

```python
# Simple messages (even without placeholders)
print(f"Starting process...")
logger.info(f"Configuration loaded")

# With variables
print(f"Processing {filename}")
logger.info(f"Found {count} items")

# Complex expressions
print(f"Result: {calculate_result()}")
logger.info(f"User {user.name} performed {action}")

# Debug messages
print(f"Debug: {variable}")
logger.debug(f"Processing item {i} of {total}")
```

### ❌ Never Use Alternatives

```python
# Don't use these:
print("Starting process...")  # Inconsistent
print("Processing {}".format(filename))  # Old style
print("Found %d items" % count)  # Old style
logger.info("User %s performed %s" % (user.name, action))  # Old style
```

## Linting Configuration

The F541 rule is completely ignored in `.ruff.toml`:

```toml
"F541",  # f-string without any placeholders (PEP 8's most annoying rule - f-strings are valid even without placeholders)
```

## Migration Guide

If you find old-style string formatting:

1. **Convert to f-strings** immediately
1. **Maintain consistency** with existing code
1. **No exceptions** - f-strings are mandatory

## Benefits

- **Consistency**: All string formatting uses the same method
- **Readability**: F-strings are more readable than alternatives
- **Performance**: Negligible difference, but consistent approach
- **Future-proof**: Easy to add placeholders later if needed

## Examples by Context

### Logging

```python
# ✅ Good
logger.info(f"Processing file: {filename}")
logger.error(f"Failed to process {count} items")
logger.debug(f"Configuration: {config}")

# ❌ Bad
logger.info("Processing file: {}".format(filename))
logger.error("Failed to process %d items" % count)
logger.debug("Configuration: %s" % config)
```

### User Messages

```python
# ✅ Good
print(f"Welcome, {user.name}!")
print(f"Found {len(items)} items to process")
print(f"Operation completed in {duration:.2f} seconds")

# ❌ Bad
print("Welcome, {}!".format(user.name))
print("Found %d items to process" % len(items))
print("Operation completed in %.2f seconds" % duration)
```

### Error Messages

```python
# ✅ Good
raise ValueError(f"Invalid configuration: {config}")
assert condition, f"Condition failed: {condition}"
return f"Error processing {item}: {error}"

# ❌ Bad
raise ValueError("Invalid configuration: {}".format(config))
assert condition, "Condition failed: %s" % condition
return "Error processing %s: %s" % (item, error)
```

## Enforcement

### Pre-commit Hooks

The project's pre-commit hooks are configured to ignore F541 violations.

### Code Review

All code reviews should enforce f-string usage:

- ✅ F-strings used consistently
- ❌ Old-style formatting found
- ❌ Mixed formatting approaches

### IDE Configuration

- **Ruff**: F541 rule disabled
- **Black**: No impact on f-strings
- **MyPy**: No impact on f-strings

## Common Patterns

### Simple Messages

```python
# ✅ Always use f-strings
print(f"Starting...")
print(f"Complete!")
print(f"Error occurred")
```

### Variable Interpolation

```python
# ✅ Use f-strings with variables
name = "Alice"
count = 42
print(f"Hello, {name}!")
print(f"Found {count} items")
```

### Complex Expressions

```python
# ✅ F-strings handle complex expressions
print(f"Result: {calculate_result()}")
print(f"Status: {get_status()}")
print(f"Time: {datetime.now():%Y-%m-%d %H:%M:%S}")
```

### Multi-line Strings

```python
# ✅ F-strings work with multi-line strings
message = f"""
Processing complete:
- Items processed: {count}
- Time taken: {duration:.2f}s
- Status: {status}
"""
```

## Troubleshooting

### "F541: f-string without any placeholders"

This warning is completely ignored in this project. F-strings without placeholders are perfectly valid and encouraged.

### "Should I convert this to a regular string?"

**No!** Always use f-strings for consistency, even without placeholders.

### "What about performance?"

The performance difference is negligible. Consistency and readability are more important.

## Summary

**F-strings are mandatory for all string formatting in this project. The F541 rule has been eliminated. Use f-strings consistently and ignore any warnings about missing placeholders.**
