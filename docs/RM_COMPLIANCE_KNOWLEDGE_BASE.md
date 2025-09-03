# 🏛️ **RM COMPLIANCE KNOWLEDGE BASE**

## **📋 RM VIOLATION PATTERNS & SOLUTIONS**

### **Pattern 1: Health Check Failures**

**Symptoms:**

- Components hang indefinitely
- No timeout mechanisms
- No health status reporting
- Blocks dependent operations

**RM Violations:**

- ❌ Self-Monitoring: No health detection
- ❌ Operational Visibility: No status reporting
- ❌ Graceful Degradation: No timeout handling

**Solution Template:**

```python
class RMCompliantHealthCheck:
    def __init__(self):
        self.health_status = "unknown"
        self.error_count = 0
        self.success_count = 0
    
    def get_health_status(self) -> Dict[str, Any]:
        """RM Self-Monitoring: Health status reporting"""
        return {
            "status": self.health_status,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "is_healthy": self.health_status == "healthy"
        }
    
    def run_with_timeout(self, timeout: int = 30) -> Dict[str, Any]:
        """RM Graceful Degradation: Timeout handling"""
        try:
            # Set up timeout handler
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            
            # Run operation with timeout
            result = subprocess.run([...], timeout=timeout)
            
        except TimeoutError:
            self.health_status = "timeout"
            return {"status": "timeout", "message": "Operation timed out"}
        except Exception as e:
            self.health_status = "error"
            return {"status": "error", "message": str(e)}
        finally:
            signal.alarm(0)  # Cancel timeout
```

### **Pattern 2: CLI Tool Import Failures**

**Symptoms:**

- `ImportError: attempted relative import with no known parent package`
- CLI tools fail when run directly
- Missing `sys.path` configuration

**RM Violations:**

- ❌ Single Responsibility: Import logic mixed with business logic
- ❌ Operational Visibility: No clear error reporting

**Solution Template:**

```python
import sys
import os

# Add src to path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Use absolute imports instead of relative
from src.module.submodule import ClassName
```

### **Pattern 3: Test Infrastructure Failures**

**Symptoms:**

- `AttributeError: 'async_generator' object has no attribute`
- `PytestCollectionWarning: cannot collect test class`
- `Fatal Python error: Bus error`

**RM Violations:**

- ❌ Testability: Tests not properly configured
- ❌ Single Responsibility: Mixed async/sync patterns

**Solution Template:**

```python
import pytest_asyncio

class TestClass:
    @pytest_asyncio.fixture
    async def async_fixture(self):
        """Proper async fixture with pytest_asyncio decorator"""
        yield fixture_value
    
    def test_method(self, async_fixture):
        """Test method using async fixture"""
        assert async_fixture is not None
```

### **Pattern 4: Pre-commit Hook Failures**

**Symptoms:**

- Hooks hang indefinitely
- Dependency corruption
- No graceful degradation

**RM Violations:**

- ❌ Graceful Degradation: No timeout handling
- ❌ Self-Monitoring: No health status reporting

**Solution Template:**

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: health-check
      name: Health Check (RM-Compliant)
      entry: uv run python scripts/health_check_wrapper.py
      language: system
      pass_filenames: false
      always_run: true
      description: Health check with timeout and graceful degradation
```

### **Pattern 5: Performance Requirements Gap**

**Symptoms:**

- No performance specifications in requirements
- No performance testing during development
- Performance issues discovered after deployment
- Slow operations blocking critical workflows

**RM Violations:**

- ❌ Self-Monitoring: No performance monitoring
- ❌ Operational Visibility: No performance status reporting
- ❌ Graceful Degradation: No performance-based failure handling

**Solution Template:**

```markdown
# Performance Requirements Template
### REQ-PERF-XXX: [Operation] Performance
**Description**: [Operation] shall complete within [X] seconds.
**TRACE**: PERF-XXX
**TEST**: PERF-XXX-TEST
**ACCEPTANCE**:
- Operation completes within [X] seconds
- Performance is measured and logged
- Performance degradation is detected
- Performance issues are tracked as incidents
```

## **🔧 RM COMPLIANCE CHECKLIST**

### **Self-Monitoring Requirements**

- [ ] Health status tracking implemented
- [ ] Error/success counting implemented
- [ ] Last check time tracking implemented
- [ ] Health status API available

### **Operational Visibility Requirements**

- [ ] External health status API implemented
- [ ] Health indicators API implemented
- [ ] Status reporting via CLI implemented
- [ ] Health dashboard integration available

### **Graceful Degradation Requirements**

- [ ] Timeout mechanism prevents hanging
- [ ] Error handling prevents crashes
- [ ] Status reporting enables monitoring
- [ ] Fallback mechanisms implemented

### **Single Responsibility Requirements**

- [ ] Focused on single operation only
- [ ] Clean separation from other operations
- [ ] Isolated error handling
- [ ] Clear interface boundaries

## **📊 RM COMPLIANCE METRICS**

### **Health Status Values**

- `healthy`: Component operating normally
- `degraded`: Component operating with reduced functionality
- `timeout`: Component operation timed out
- `error`: Component operation failed
- `unknown`: Component health status not determined

### **Success Rate Calculation**

```python
success_rate = success_count / (success_count + error_count)
if (success_count + error_count) == 0:
    success_rate = 0
```

### **Operational Status**

```python
is_operational = health_status in ["healthy", "degraded"]
```

## **🚨 RM VIOLATION DETECTION WORKFLOW**

### **Step 1: Identify Violation Type**

1. **Health Check Failure**: Component hangs or fails without graceful degradation
1. **CLI Tool Failure**: Import errors, missing dependencies, broken interfaces
1. **Test Infrastructure Failure**: Collection warnings, async fixture issues
1. **Pre-commit Hook Failure**: Dependency corruption, hanging processes

### **Step 2: Analyze Root Cause**

1. **Dependency Issues**: Corrupted files, missing packages
1. **Import Path Issues**: Relative imports, missing sys.path
1. **Configuration Issues**: Missing decorators, incorrect setup
1. **Resource Issues**: Memory corruption, bus errors

### **Step 3: Implement RM-Compliant Solution**

1. **Self-Monitoring**: Add health status tracking
1. **Operational Visibility**: Add external health APIs
1. **Graceful Degradation**: Add timeout and error handling
1. **Single Responsibility**: Refactor to focused design

### **Step 4: Validate RM Compliance**

1. **Test Health Monitoring**: Verify status tracking works
1. **Test Operational Visibility**: Verify external APIs work
1. **Test Graceful Degradation**: Verify timeout handling works
1. **Test Single Responsibility**: Verify focused design

## **📚 REFERENCE IMPLEMENTATIONS**

### **Safety Check Wrapper**

- **File**: `scripts/safety_check_wrapper.py`
- **Pattern**: Health Check Failure
- **RM Compliance**: Full compliance with all principles

### **Performance Requirements Integration**

- **File**: `requirements/performance_requirements.md`
- **Pattern**: Performance Requirements Gap
- **RM Compliance**: Performance monitoring and validation

### **Model Management CLI**

- **File**: `src/model_management/model_crud.py`
- **Pattern**: CLI Tool Import Failure
- **RM Compliance**: Import path fixes, absolute imports

### **Test Infrastructure**

- **Files**: `tests/test_agent_coordination.py`, `tests/test_rm_compliance_checker.py`
- **Pattern**: Test Infrastructure Failure
- **RM Compliance**: Proper async fixture configuration

## **🎯 PREVENTION STRATEGIES**

### **Proactive Monitoring**

1. **Health Check Validation**: Regular health status checks
1. **Dependency Integrity**: Regular dependency validation
1. **Test Infrastructure**: Regular test infrastructure validation
1. **Pre-commit Hooks**: Regular pre-commit hook validation

### **Automated Detection**

1. **RM Compliance Testing**: Automated RM compliance validation
1. **Health Status Monitoring**: Automated health status monitoring
1. **Error Rate Monitoring**: Automated error rate monitoring
1. **Performance Monitoring**: Automated performance monitoring

### **Recovery Mechanisms**

1. **Automatic Recovery**: Automatic recovery from common failures
1. **Fallback Mechanisms**: Fallback mechanisms for critical operations
1. **Alert Systems**: Alert systems for critical failures
1. **Escalation Procedures**: Escalation procedures for critical failures
