# Security-First Code Review Guidelines

## Security Vulnerabilities to Flag

1. **Subprocess Usage**: Flag subprocess.run, os.system, os.popen
1. **Credential Exposure**: Check for hardcoded secrets/credentials
1. **Input Validation**: Ensure all user inputs are validated
1. **Error Handling**: Verify proper exception handling
1. **Secure Shell**: Prefer elegant secure shell client over direct subprocess

## Model-Driven Architecture

1. **Project Model Registry**: Align with project_model_registry.json
1. **Domain Detection**: Verify proper domain classification
1. **Tool Selection**: Check appropriate linters/validators
1. **Requirements Traceability**: Ensure changes trace to model requirements

## Code Quality Standards

1. **Python Standards**: PEP 8, type hints, docstrings
1. **Error Handling**: Comprehensive exception handling
1. **Logging**: Appropriate levels, secure logging
1. **Testing**: Adequate test coverage
1. **Documentation**: Update docs for significant changes

## Security-First Review Checklist

### High Priority Security Issues

- [ ] **Subprocess vulnerabilities** - Use elegant secure shell client instead
- [ ] **Hardcoded credentials** - Move to environment variables
- [ ] **Unvalidated inputs** - Add proper input validation
- [ ] **Insecure error handling** - Implement proper exception handling
- [ ] **Missing type hints** - Add comprehensive type annotations

### Model-Driven Requirements

- [ ] **Domain classification** - Ensure proper domain detection
- [ ] **Tool selection** - Verify appropriate linters/validators
- [ ] **Requirements traceability** - Link changes to model requirements
- [ ] **Project structure** - Follow established patterns

### Code Quality Requirements

- [ ] **PEP 8 compliance** - Follow Python style guidelines
- [ ] **Type hints** - Add comprehensive type annotations
- [ ] **Docstrings** - Include proper documentation
- [ ] **Error handling** - Implement robust exception handling
- [ ] **Logging** - Use appropriate logging levels
- [ ] **Testing** - Ensure adequate test coverage
- [ ] **Documentation** - Update relevant documentation

## Repository-Specific Guidelines

### Security-First Architecture

- **Prefer secure shell client** over direct subprocess calls
- **Use environment variables** for all credentials
- **Implement input validation** for all user inputs
- **Add comprehensive error handling** with proper logging
- **Follow least privilege principle** for all operations

### Model-Driven Development

- **Check project_model_registry.json** for domain requirements
- **Verify tool selection** matches domain configuration
- **Ensure requirements traceability** to model requirements
- **Follow established patterns** for new components

### Integration Requirements

- **GitHub MCP Integration** - Leverage repository context
- **Ghostbusters Integration** - Address detected delusions
- **Secure Shell Service** - Use elegant client for shell operations
- **Model-Driven Architecture** - Follow established patterns

## Review Focus Areas

### Security

1. **Subprocess Usage** - Flag and suggest secure alternatives
1. **Credential Management** - Ensure no hardcoded secrets
1. **Input Validation** - Verify all inputs are properly validated
1. **Error Handling** - Check for comprehensive exception handling
1. **Secure Logging** - Ensure sensitive data is not logged

### Quality

1. **Code Standards** - Follow PEP 8 and project conventions
1. **Type Safety** - Add comprehensive type hints
1. **Documentation** - Include proper docstrings and comments
1. **Testing** - Ensure adequate test coverage
1. **Performance** - Check for efficient implementations

### Architecture

1. **Model Alignment** - Verify changes align with project model
1. **Domain Classification** - Ensure proper domain detection
1. **Tool Integration** - Check appropriate tools are used
1. **Requirements Traceability** - Link changes to requirements
1. **Pattern Consistency** - Follow established architectural patterns
