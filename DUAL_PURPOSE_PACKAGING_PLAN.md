# 🎯 Dual-Purpose Packaging Strategy

## Gmail-to-Calendar System

### **The Vision:**

- **Internal**: RM-compliant integration within OpenFlow-Playground
- **External**: Standalone OSS package for PyPI distribution

______________________________________________________________________

## 📦 **Package Architecture**

### **Core Package: `gmail-calendar-system` (PyPI)**

```
gmail-calendar-system/
├── src/gmail_calendar_system/
│   ├── __init__.py
│   ├── core/
│   │   ├── connectors.py      # OAuth2 Gmail/Calendar connectors
│   │   ├── parsers.py         # ICS parser, time normalizer
│   │   ├── models.py          # EventCandidate, IdempotencyKey
│   │   └── orchestrator.py    # LangGraph orchestration
│   ├── mcp_tools/
│   │   ├── google_calendar_tool.py
│   │   ├── gmail_tool.py
│   │   └── ics_tool.py
│   └── cli.py                 # Standalone CLI
├── pyproject.toml
├── README.md
└── setup.py
```

**Dependencies:**

```toml
[project]
dependencies = [
    "google-auth>=2.0.0",
    "google-auth-oauthlib>=1.0.0", 
    "google-api-python-client>=2.0.0",
    "icalendar>=5.0.0",
    "python-dateutil>=2.8.0",
    "langgraph>=0.1.0",
    "httpx>=0.24.0"
]
```

### **Project Integration: `gmail-calendar-rm` (Internal)**

```
src/gmail_calendar_rm/
├── __init__.py
├── rm_integration.py          # RM compliance wrapper
├── model_registry.py          # Project model integration
├── health_monitoring.py       # Project health checks
└── audit_system.py            # Project audit trails
```

**Dependencies:**

```toml
[project]
dependencies = [
    "gmail-calendar-system>=1.0.0",  # Core package
    "src.model_management",           # Project-specific
    "src.project_management"          # Project-specific
]
```

______________________________________________________________________

## 🚀 **Implementation Strategy**

### **Phase 1: Extract Core Package**

1. **Move core functionality** to standalone package
1. **Remove project dependencies** from core
1. **Create clean API** for external consumption
1. **Add PyPI packaging** (pyproject.toml, setup.py)

### **Phase 2: Create RM Integration Layer**

1. **Create RM wrapper** that uses core package
1. **Add project-specific features** (model registry, health monitoring)
1. **Maintain RM compliance** within project
1. **Keep project integration** working

### **Phase 3: Dual Distribution**

1. **Publish to PyPI** as `gmail-calendar-system`
1. **Use internally** as `gmail-calendar-rm`
1. **Document both use cases**
1. **Maintain compatibility**

______________________________________________________________________

## 📋 **Package Contents**

### **Core Package (`gmail-calendar-system`)**

```python
# Clean, minimal API
from gmail_calendar_system import GmailCalendarOrchestrator
from gmail_calendar_system.mcp_tools import GoogleCalendarMCPTool

# Usage
orchestrator = GmailCalendarOrchestrator(gmail_config, calendar_config)
result = await orchestrator.process_request("put meeting on calendar")
```

### **RM Integration (`gmail-calendar-rm`)**

```python
# Project-integrated API
from gmail_calendar_rm import RMGmailCalendarSystem
from gmail_calendar_rm import ModelRegistryIntegration

# Usage
system = RMGmailCalendarSystem()
system.register_with_model_registry()
result = await system.process_request("put meeting on calendar")
```

______________________________________________________________________

## 🎯 **Benefits of This Approach**

### **For OSS Distribution:**

- ✅ **Clean, minimal API** - no project dependencies
- ✅ **PyPI ready** - standard Python packaging
- ✅ **Generic LLM integration** - works with any agent stack
- ✅ **Self-contained** - all dependencies included
- ✅ **Documentation** - clear usage examples

### **For Internal Project:**

- ✅ **RM compliance** - meets project standards
- ✅ **Model registry integration** - works with project architecture
- ✅ **Health monitoring** - project-specific monitoring
- ✅ **Audit trails** - project-specific logging
- ✅ **Backward compatibility** - existing code still works

### **For Development:**

- ✅ **Separation of concerns** - core vs. project-specific
- ✅ **Reusability** - core can be used elsewhere
- ✅ **Maintainability** - clear boundaries
- ✅ **Testing** - test core independently

______________________________________________________________________

## 🔧 **Implementation Steps**

### **Step 1: Extract Core Package**

```bash
# Create standalone package
mkdir gmail-calendar-system/
cd gmail-calendar-system/

# Move core files
cp -r src/gmail_calendar_system/core/ src/
cp -r src/gmail_calendar_system/mcp_tools/ src/
cp src/gmail_calendar_system/cli.py src/

# Create pyproject.toml
# Add setup.py
# Add README.md
```

### **Step 2: Create RM Integration**

```bash
# Create RM wrapper
mkdir src/gmail_calendar_rm/
cd src/gmail_calendar_rm/

# Create RM integration files
# Add project-specific features
# Maintain RM compliance
```

### **Step 3: Update Project**

```bash
# Update project to use RM integration
# Remove direct core dependencies
# Test both internal and external usage
```

______________________________________________________________________

## 📊 **Success Metrics**

### **Core Package Success:**

- ✅ **PyPI publication** - successfully published
- ✅ **External usage** - used by other projects
- ✅ **Clean API** - no project dependencies
- ✅ **Documentation** - clear usage examples

### **RM Integration Success:**

- ✅ **Project compatibility** - works within project
- ✅ **RM compliance** - meets project standards
- ✅ **Backward compatibility** - existing code works
- ✅ **Health monitoring** - project monitoring works

______________________________________________________________________

## 🎯 **Next Steps**

1. **Extract core package** to standalone directory
1. **Create PyPI packaging** (pyproject.toml, setup.py)
1. **Create RM integration layer** for project use
1. **Test both scenarios** (standalone + project integration)
1. **Publish to PyPI** and update project

**This approach gives you the best of both worlds:**

- **Standalone OSS package** for external distribution
- **RM-compliant integration** for internal project use
