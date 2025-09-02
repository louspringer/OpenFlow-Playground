# Domain Registry

## 🎯 **Overview**

The **Project Model Registry** (`project_model_registry.json`) is the central authority that defines, manages, and orchestrates all domains in the OpenFlow Playground project. It serves as the single source of truth for domain definitions, tool mappings, compliance requirements, and operational workflows.

## 🏗️ **Registry Structure**

### **Top-Level Organization**

```json
{
  "description": "Project description and purpose",
  "author": "Project authors and contributors",
  "project_purpose": {
    "primary_goal": "Main project objective",
    "secondary_goal": "Secondary objectives",
    "architecture_type": "Architecture classification",
    "target_audience": "Intended users and stakeholders"
  },
  "domain_architecture": {
    "demo_core": {...},
    "demo_tools": {...},
    "demo_infrastructure": {...},
    "demo_utilities": {...}
  },
  "domains": {
    "domain_name": {...}
  }
}
```

### **Domain Architecture Categories**

#### **Demo Core**

Core domains that implement the Snowflake OpenFlow demo:

```json
"demo_core": {
  "description": "Core domains that implement the Snowflake OpenFlow demo",
  "domains": [
    "snowflake_openflow_demo",
    "deployment_automation", 
    "setup_wizard",
    "streamlit_demo_app"
  ],
  "purpose": "Provide the actual demo functionality and user experience"
}
```

#### **Demo Tools**

Comprehensive tool ecosystem supporting the demo:

```json
"demo_tools": {
  "domains": [
    "ghostbusters",
    "intelligent_linter_system",
    "code_quality_system",
    "multi_agent_testing",
    "model_driven_testing",
    "round_trip_engineering",
    "artifact_forge",
    "visualization"
  ]
}
```

#### **Demo Infrastructure**

Supporting infrastructure and foundation:

```json
"demo_infrastructure": {
  "description": "Infrastructure and supporting domains for the demo ecosystem",
  "domains": [
    "model_driven_projection",
    "mdc_generator", 
    "security_first",
    "package_management",
    "rule_compliance"
  ],
  "purpose": "Provide the foundation and supporting infrastructure"
}
```

#### **Demo Utilities**

Utility domains for development and deployment:

```json
"demo_utilities": {
  "description": "Utility domains for demo development and deployment",
  "domains": [
    "bash",
    "documentation",
    "data",
    "cloudformation",
    "build_system"
  ],
  "purpose": "Provide utilities and support for demo development"
}
```

## 🔧 **Domain Definition Structure**

### **Required Fields**

Every domain must include these essential fields:

```json
{
  "patterns": [
    "src/domain_name/*.py",
    "**/*domain_name*.py",
    "tests/test_domain_name*.py"
  ],
  "content_indicators": [
    "DomainClassName",
    "domain_specific_keyword",
    "domain_functionality"
  ],
  "linter": "flake8",
  "validator": "pytest", 
  "formatter": "black",
  "requirements": [
    "Domain requirement 1",
    "Domain requirement 2"
  ],
  "tools": [
    "tool1",
    "tool2"
  ],
  "capabilities": [
    "capability1",
    "capability2"
  ],
  "workflows": {
    "workflow_name": {
      "step1": "description",
      "step2": "description"
    }
  },
  "tool_rules": {
    "rule_name": "rule_description"
  },
  "exclusions": [
    "*.pyc",
    "__pycache__"
  ]
}
```

### **Optional Fields**

Additional fields for enhanced domain management:

```json
{
  "demo_role": "tool|utility|core|infrastructure",
  "extraction_candidate": "HIGH|MEDIUM|LOW|false",
  "reason": "Extraction rationale",
  "status": "completed|in_progress|planned",
  "completion_date": "2024-01-01",
  "implementation_details": {
    "architecture": "description",
    "modules": ["module1", "module2"],
    "compliance": "compliance details"
  }
}
```

## 🛠️ **Registry Operations**

### **Reading the Registry**

```bash
# Read entire registry
uv run python src/model_management/model_crud.py read

# List all domains
uv run python src/model_management/model_crud.py list-domains

# Get specific domain info
uv run python src/model_management/model_crud.py list-domain-requirements --domain domain_name
```

### **Domain Detection**

The registry enables automatic domain detection through:

#### **Pattern Matching**

- **File Patterns**: Match files based on path and naming conventions
- **Content Indicators**: Identify domain content through keywords
- **Exclusion Patterns**: Filter out irrelevant files

#### **Tool Integration**

- **Linter**: Domain-specific code quality checking
- **Validator**: Functional validation and testing
- **Formatter**: Code formatting and style enforcement

### **Model-Driven Operations**

All domain operations are driven by the registry:

#### **Tool Selection**

```python
# Domain detection
domain = detect_domain(file_path)

# Tool selection from registry
tools = registry.domains[domain].tools
linter = registry.domains[domain].linter
validator = registry.domains[domain].validator
```

#### **Workflow Execution**

```python
# Get workflow from registry
workflow = registry.domains[domain].workflows["workflow_name"]

# Execute workflow steps
for step, description in workflow.items():
    execute_step(step, description)
```

## 📊 **Registry Validation**

### **Schema Validation**

The registry must conform to a defined schema:

#### **Required Structure**

- All domains must have required fields
- Domain architecture categories must be properly defined
- Dependencies must be valid and resolvable

#### **Content Validation**

- Patterns must be valid glob patterns
- Content indicators must be meaningful
- Tools must be available and functional

### **Compliance Checking**

- **RM Compliance**: All domains must implement Reflective Module interfaces
- **Tool Consistency**: All specified tools must be available
- **Workflow Validation**: All workflows must be testable
- **Model Conformance**: All domains must conform to registry schema

## 🔍 **Domain Discovery**

### **Automatic Detection**

```python
def detect_domain(file_path: str) -> str:
    """Detect domain for a given file path."""
    for domain_name, domain_config in registry.domains.items():
        if matches_patterns(file_path, domain_config.patterns):
            if has_content_indicators(file_path, domain_config.content_indicators):
                return domain_name
    return "unknown"
```

### **Content Analysis**

```python
def has_content_indicators(file_path: str, indicators: List[str]) -> bool:
    """Check if file contains domain-specific content indicators."""
    content = read_file(file_path)
    return any(indicator in content for indicator in indicators)
```

## 🚀 **Registry Management**

### **Adding New Domains**

1. **Define Domain Structure**: Create domain definition with all required fields
1. **Add to Registry**: Insert domain into appropriate category
1. **Update Dependencies**: Add domain to dependency relationships
1. **Validate**: Run registry validation to ensure compliance
1. **Test**: Verify domain detection and tool integration

### **Updating Existing Domains**

1. **Modify Definition**: Update domain fields as needed
1. **Validate Changes**: Ensure changes maintain compliance
1. **Update Dependencies**: Adjust dependency relationships if needed
1. **Test Integration**: Verify domain still works with existing systems

### **Registry Maintenance**

- **Regular Validation**: Periodic schema and content validation
- **Dependency Checking**: Ensure all dependencies are resolvable
- **Tool Verification**: Verify all specified tools are available
- **Performance Monitoring**: Monitor registry performance and size

## 📚 **Best Practices**

### **Domain Definition**

- **Clear Patterns**: Use specific, non-overlapping file patterns
- **Meaningful Indicators**: Content indicators should be domain-specific
- **Comprehensive Tools**: Include all tools used by the domain
- **Complete Workflows**: Document all domain workflows

### **Registry Organization**

- **Logical Grouping**: Group domains by function and purpose
- **Clear Dependencies**: Define clear dependency relationships
- **Consistent Naming**: Use consistent naming conventions
- **Documentation**: Maintain comprehensive registry documentation

### **Operations**

- **Model-Driven**: Always use the registry for domain operations
- **Validation**: Validate all registry changes
- **Testing**: Test domain detection and tool integration
- **Monitoring**: Monitor registry health and performance

## 🔗 **Integration Points**

### **Build System Integration**

- **Makefile Targets**: Registry drives Makefile target generation
- **Tool Selection**: Build system uses registry for tool selection
- **Workflow Execution**: Build system executes registry-defined workflows

### **Testing Integration**

- **Test Discovery**: Registry enables automatic test discovery
- **Tool Integration**: Testing uses registry-specified tools
- **Compliance Testing**: Registry drives compliance validation

### **CI/CD Integration**

- **Pipeline Generation**: Registry drives CI/CD pipeline generation
- **Quality Gates**: Registry defines quality gate requirements
- **Deployment**: Registry drives deployment workflows

## 📚 **Related Documentation**

- [DOMAIN_ARCHITECTURE.md](./DOMAIN_ARCHITECTURE.md) - Overall domain architecture
- [DOMAIN_COMPLIANCE.md](./DOMAIN_COMPLIANCE.md) - RM compliance requirements
- [DOMAIN_DEVELOPMENT.md](./DOMAIN_DEVELOPMENT.md) - Domain development guidelines
- [DOMAIN_TESTING.md](./DOMAIN_TESTING.md) - Domain testing standards
- [project_model_registry.json](../project_model_registry.json) - Central domain registry
