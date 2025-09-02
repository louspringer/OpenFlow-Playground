# Domain Template

## 🎯 **Overview**

This template provides a standardized structure for creating new domains in the OpenFlow Playground project. It ensures consistency, compliance, and quality across all domains.

## 📋 **Domain Creation Checklist**

### **Phase 1: Planning**

- [ ] Define domain purpose and boundaries
- [ ] Identify dependencies and interfaces
- [ ] Select appropriate tools and technologies
- [ ] Plan package structure and organization

### **Phase 2: Implementation**

- [ ] Create package structure
- [ ] Implement Reflective Module interfaces
- [ ] Add core functionality
- [ ] Implement tools and utilities

### **Phase 3: Registry Integration**

- [ ] Add domain to project model registry
- [ ] Update domain architecture categories
- [ ] Configure tool mappings
- [ ] Set up workflows and capabilities

### **Phase 4: Testing and Validation**

- [ ] Write comprehensive tests
- [ ] Validate RM compliance
- [ ] Test tool integration
- [ ] Validate registry integration

### **Phase 5: Documentation**

- [ ] Create domain documentation
- [ ] Document APIs and interfaces
- [ ] Add usage examples
- [ ] Update related documentation

## 🏗️ **Package Structure Template**

```
src/domain_name/
├── __init__.py              # Domain package initialization
├── core/                    # Core domain functionality
│   ├── __init__.py
│   ├── domain_class.py      # Main domain class
│   ├── interfaces.py        # Domain interfaces
│   └── models.py            # Domain data models
├── tools/                   # Domain-specific tools
│   ├── __init__.py
│   ├── tool1.py
│   ├── tool2.py
│   └── utils.py
├── models/                  # Data models and schemas
│   ├── __init__.py
│   ├── data_models.py
│   ├── schemas.py
│   └── validators.py
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── helpers.py
│   ├── validators.py
│   └── exceptions.py
└── tests/                   # Domain tests
    ├── __init__.py
    ├── test_core.py
    ├── test_tools.py
    ├── test_models.py
    ├── test_integration.py
    ├── test_compliance.py
    └── fixtures/
        ├── __init__.py
        ├── sample_data.py
        └── mock_objects.py
```

## 🔧 **Core Implementation Template**

### **Main Domain Class**

```python
# src/domain_name/core/domain_class.py
"""
Domain Name - Core Implementation

This module provides the core functionality for the domain_name domain.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from src.reflective_modules.base_reflective_module import ReflectiveModule
from src.reflective_modules.models import ModuleHealth, ModuleStatus, ModuleCapability
from .interfaces import DomainInterface
from .models import DomainConfig, DomainResult
from ..utils.exceptions import DomainError


class DomainState(Enum):
    """Domain operational states."""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class DomainMetrics:
    """Domain performance metrics."""
    operations_count: int = 0
    success_count: int = 0
    error_count: int = 0
    last_operation_time: float = 0.0
    average_response_time: float = 0.0


class DomainImplementation(ReflectiveModule):
    """
    Domain Name Implementation
    
    This class implements the core functionality for the domain_name domain
    with full Reflective Module compliance.
    """
    
    def __init__(self, config: Optional[DomainConfig] = None):
        """Initialize the domain implementation."""
        super().__init__()
        self.config = config or DomainConfig()
        self.state = DomainState.INITIALIZING
        self.metrics = DomainMetrics()
        self.health_monitor = DomainHealthMonitor()
        self.initialized = False
    
    async def initialize(self) -> None:
        """Initialize the domain."""
        try:
            self.state = DomainState.INITIALIZING
            
            # Domain-specific initialization
            await self._initialize_domain()
            
            self.initialized = True
            self.state = DomainState.READY
            
        except Exception as e:
            self.state = DomainState.ERROR
            raise DomainError(f"Failed to initialize domain: {e}") from e
    
    async def _initialize_domain(self) -> None:
        """Domain-specific initialization logic."""
        # Implement domain-specific initialization
        pass
    
    async def execute_operation(self, operation: str, **kwargs) -> DomainResult:
        """Execute a domain operation."""
        start_time = time.time()
        
        try:
            self.state = DomainState.RUNNING
            self.metrics.operations_count += 1
            
            # Execute domain operation
            result = await self._execute_domain_operation(operation, **kwargs)
            
            # Update metrics
            self.metrics.success_count += 1
            self.metrics.last_operation_time = time.time()
            self.metrics.average_response_time = (
                (self.metrics.average_response_time * (self.metrics.operations_count - 1) + 
                 (time.time() - start_time)) / self.metrics.operations_count
            )
            
            self.state = DomainState.READY
            return result
            
        except Exception as e:
            self.metrics.error_count += 1
            self.state = DomainState.ERROR
            raise DomainError(f"Operation failed: {e}") from e
    
    async def _execute_domain_operation(self, operation: str, **kwargs) -> DomainResult:
        """Execute domain-specific operation."""
        # Implement domain-specific operation logic
        return DomainResult(success=True, result="operation_completed")
    
    # Reflective Module Compliance Methods
    
    async def get_module_status(self) -> ModuleHealth:
        """Get the current operational status of this module."""
        try:
            # Calculate health indicators
            success_rate = (
                self.metrics.success_count / self.metrics.operations_count 
                if self.metrics.operations_count > 0 else 1.0
            )
            
            # Determine status based on health indicators
            if self.state == DomainState.READY and success_rate > 0.95:
                status = ModuleStatus.AVAILABLE
                message = "Domain is fully operational"
            elif self.state == DomainState.READY and success_rate > 0.8:
                status = ModuleStatus.PARTIALLY_AVAILABLE
                message = f"Domain operational with {success_rate:.1%} success rate"
            elif self.state == DomainState.ERROR:
                status = ModuleStatus.NOT_AVAILABLE
                message = f"Domain in error state with {self.metrics.error_count} errors"
            else:
                status = ModuleStatus.NOT_AVAILABLE
                message = f"Domain in {self.state.value} state"
            
            return ModuleHealth(
                status=status,
                message=message,
                capabilities=await self.get_module_capabilities(),
                health_indicators={
                    "state": self.state.value,
                    "operations_count": self.metrics.operations_count,
                    "success_count": self.metrics.success_count,
                    "error_count": self.metrics.error_count,
                    "success_rate": success_rate,
                    "last_operation_time": self.metrics.last_operation_time,
                    "average_response_time": self.metrics.average_response_time,
                    "initialized": self.initialized
                },
                timestamp=time.time()
            )
            
        except Exception as e:
            return ModuleHealth(
                status=ModuleStatus.NOT_AVAILABLE,
                message=f"Status check failed: {e}",
                capabilities=[],
                health_indicators={"error": str(e)},
                timestamp=time.time()
            )
    
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get the capabilities this module provides."""
        try:
            return [
                ModuleCapability(
                    name="core_operations",
                    description="Core domain operations",
                    available=self.initialized,
                    version="1.0.0",
                    details={
                        "class_name": self.__class__.__name__,
                        "state": self.state.value
                    }
                ),
                ModuleCapability(
                    name="health_monitoring",
                    description="Reflective Module health monitoring",
                    available=True,
                    version="1.0.0",
                    details={
                        "monitoring": "enabled",
                        "metrics": "comprehensive"
                    }
                ),
                ModuleCapability(
                    name="operational_tracking",
                    description="Operational state tracking",
                    available=True,
                    version="1.0.0",
                    details={
                        "state_tracking": "enabled",
                        "metrics_collection": "enabled"
                    }
                )
            ]
        except Exception as e:
            return []
    
    async def is_healthy(self) -> bool:
        """Check if this module is currently healthy."""
        try:
            status = await self.get_module_status()
            return status.status == ModuleStatus.AVAILABLE
        except Exception:
            return False
    
    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        try:
            status = await self.get_module_status()
            return status.health_indicators
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}


class DomainHealthMonitor:
    """Health monitoring for domain compliance."""
    
    def __init__(self):
        self.start_time = time.time()
        self.health_checks = 0
        self.health_check_failures = 0
    
    def record_health_check(self, success: bool):
        """Record a health check result."""
        self.health_checks += 1
        if not success:
            self.health_check_failures += 1
    
    def get_health_check_success_rate(self) -> float:
        """Get health check success rate."""
        if self.health_checks == 0:
            return 1.0
        return (self.health_checks - self.health_check_failures) / self.health_checks
    
    def get_uptime(self) -> float:
        """Get domain uptime in seconds."""
        return time.time() - self.start_time
```

### **Domain Interfaces**

```python
# src/domain_name/core/interfaces.py
"""
Domain Name - Interfaces

This module defines the interfaces for the domain_name domain.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import DomainConfig, DomainResult


class DomainInterface(ABC):
    """Base interface for domain implementations."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the domain."""
        pass
    
    @abstractmethod
    async def execute_operation(self, operation: str, **kwargs) -> DomainResult:
        """Execute a domain operation."""
        pass
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """Get domain status."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the domain."""
        pass


class DomainToolInterface(ABC):
    """Interface for domain tools."""
    
    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the tool with input data."""
        pass
    
    @abstractmethod
    def get_tool_info(self) -> Dict[str, Any]:
        """Get tool information."""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data."""
        pass
```

### **Domain Models**

```python
# src/domain_name/core/models.py
"""
Domain Name - Models

This module defines the data models for the domain_name domain.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


class OperationType(Enum):
    """Types of domain operations."""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    PROCESS = "process"


@dataclass
class DomainConfig:
    """Domain configuration."""
    name: str = "domain_name"
    version: str = "1.0.0"
    timeout: int = 30
    max_retries: int = 3
    debug: bool = False
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.settings is None:
            self.settings = {}


@dataclass
class DomainResult:
    """Result of a domain operation."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    execution_time: float = 0.0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DomainOperation:
    """Domain operation definition."""
    operation_type: OperationType
    name: str
    description: str
    parameters: Dict[str, Any] = None
    required_parameters: List[str] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.required_parameters is None:
            self.required_parameters = []
```

## 🛠️ **Tool Implementation Template**

### **Domain Tool**

```python
# src/domain_name/tools/tool1.py
"""
Domain Name - Tool 1

This module implements tool1 for the domain_name domain.
"""

import asyncio
from typing import Any, Dict, List, Optional
from ..core.interfaces import DomainToolInterface
from ..core.models import DomainResult
from ..utils.exceptions import ToolError


class Tool1(DomainToolInterface):
    """Tool 1 implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the tool."""
        self.config = config or {}
        self.initialized = False
    
    async def initialize(self) -> None:
        """Initialize the tool."""
        try:
            # Tool-specific initialization
            await self._initialize_tool()
            self.initialized = True
        except Exception as e:
            raise ToolError(f"Failed to initialize tool1: {e}") from e
    
    async def _initialize_tool(self) -> None:
        """Tool-specific initialization logic."""
        # Implement tool initialization
        pass
    
    async def execute(self, input_data: Any) -> Any:
        """Execute the tool with input data."""
        if not self.initialized:
            await self.initialize()
        
        try:
            # Validate input
            if not self.validate_input(input_data):
                raise ToolError("Invalid input data")
            
            # Execute tool logic
            result = await self._execute_tool_logic(input_data)
            
            return result
            
        except Exception as e:
            raise ToolError(f"Tool execution failed: {e}") from e
    
    async def _execute_tool_logic(self, input_data: Any) -> Any:
        """Execute tool-specific logic."""
        # Implement tool logic
        return {"result": "tool1_executed", "input": input_data}
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get tool information."""
        return {
            "name": "tool1",
            "version": "1.0.0",
            "description": "Tool 1 for domain_name",
            "initialized": self.initialized,
            "config": self.config
        }
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data."""
        # Implement input validation
        return input_data is not None
```

## 🧪 **Testing Template**

### **Core Tests**

```python
# src/domain_name/tests/test_core.py
"""
Domain Name - Core Tests

This module contains tests for the core domain functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from ..core.domain_class import DomainImplementation, DomainState
from ..core.models import DomainConfig, DomainResult
from ..utils.exceptions import DomainError


class TestDomainImplementation:
    """Test domain implementation."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.config = DomainConfig(name="test_domain")
        self.domain = DomainImplementation(self.config)
    
    def teardown_method(self):
        """Teardown for each test method."""
        # Cleanup if needed
        pass
    
    def test_initialization(self):
        """Test domain initialization."""
        assert self.domain is not None
        assert self.domain.config.name == "test_domain"
        assert self.domain.state == DomainState.INITIALIZING
        assert not self.domain.initialized
    
    async def test_initialize(self):
        """Test domain initialization."""
        await self.domain.initialize()
        assert self.domain.initialized
        assert self.domain.state == DomainState.READY
    
    async def test_execute_operation(self):
        """Test operation execution."""
        await self.domain.initialize()
        
        result = await self.domain.execute_operation("test_operation")
        
        assert isinstance(result, DomainResult)
        assert result.success
        assert self.domain.metrics.operations_count == 1
        assert self.domain.metrics.success_count == 1
    
    async def test_operation_error_handling(self):
        """Test operation error handling."""
        await self.domain.initialize()
        
        with patch.object(self.domain, '_execute_domain_operation', side_effect=Exception("Test error")):
            with pytest.raises(DomainError):
                await self.domain.execute_operation("failing_operation")
        
        assert self.domain.metrics.error_count == 1
        assert self.domain.state == DomainState.ERROR
    
    async def test_rm_compliance(self):
        """Test RM compliance."""
        # Test module status
        status = await self.domain.get_module_status()
        assert status is not None
        assert status.status in [ModuleStatus.AVAILABLE, ModuleStatus.PARTIALLY_AVAILABLE, ModuleStatus.NOT_AVAILABLE]
        
        # Test capabilities
        capabilities = await self.domain.get_module_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        
        # Test health check
        is_healthy = await self.domain.is_healthy()
        assert isinstance(is_healthy, bool)
        
        # Test health indicators
        indicators = await self.domain.get_health_indicators()
        assert isinstance(indicators, dict)
```

### **Tool Tests**

```python
# src/domain_name/tests/test_tools.py
"""
Domain Name - Tool Tests

This module contains tests for domain tools.
"""

import pytest
from unittest.mock import Mock, patch
from ..tools.tool1 import Tool1
from ..utils.exceptions import ToolError


class TestTool1:
    """Test tool1 implementation."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.tool = Tool1()
    
    def test_initialization(self):
        """Test tool initialization."""
        assert self.tool is not None
        assert not self.tool.initialized
    
    async def test_initialize(self):
        """Test tool initialization."""
        await self.tool.initialize()
        assert self.tool.initialized
    
    async def test_execute(self):
        """Test tool execution."""
        await self.tool.initialize()
        
        result = await self.tool.execute("test_input")
        
        assert result is not None
        assert "result" in result
        assert result["input"] == "test_input"
    
    def test_validate_input(self):
        """Test input validation."""
        assert self.tool.validate_input("valid_input")
        assert not self.tool.validate_input(None)
    
    def test_get_tool_info(self):
        """Test tool info retrieval."""
        info = self.tool.get_tool_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert "version" in info
        assert "description" in info
        assert info["name"] == "tool1"
```

### **Compliance Tests**

```python
# src/domain_name/tests/test_compliance.py
"""
Domain Name - Compliance Tests

This module contains tests for RM compliance.
"""

import pytest
from ..core.domain_class import DomainImplementation
from src.reflective_modules.models import ModuleStatus


class TestDomainCompliance:
    """Test domain RM compliance."""
    
    async def test_module_status_compliance(self):
        """Test module status compliance."""
        domain = DomainImplementation()
        await domain.initialize()
        
        status = await domain.get_module_status()
        
        # Check required fields
        assert hasattr(status, 'status')
        assert hasattr(status, 'message')
        assert hasattr(status, 'capabilities')
        assert hasattr(status, 'health_indicators')
        assert hasattr(status, 'timestamp')
        
        # Check field types
        assert status.status in [ModuleStatus.AVAILABLE, ModuleStatus.PARTIALLY_AVAILABLE, ModuleStatus.NOT_AVAILABLE]
        assert isinstance(status.message, str)
        assert isinstance(status.capabilities, list)
        assert isinstance(status.health_indicators, dict)
        assert isinstance(status.timestamp, float)
    
    async def test_module_capabilities_compliance(self):
        """Test module capabilities compliance."""
        domain = DomainImplementation()
        
        capabilities = await domain.get_module_capabilities()
        
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        
        for capability in capabilities:
            assert hasattr(capability, 'name')
            assert hasattr(capability, 'description')
            assert hasattr(capability, 'available')
            assert hasattr(capability, 'version')
            assert hasattr(capability, 'details')
            
            assert isinstance(capability.name, str)
            assert isinstance(capability.description, str)
            assert isinstance(capability.available, bool)
            assert isinstance(capability.version, str)
            assert isinstance(capability.details, dict)
    
    async def test_health_check_compliance(self):
        """Test health check compliance."""
        domain = DomainImplementation()
        
        is_healthy = await domain.is_healthy()
        assert isinstance(is_healthy, bool)
    
    async def test_health_indicators_compliance(self):
        """Test health indicators compliance."""
        domain = DomainImplementation()
        
        indicators = await domain.get_health_indicators()
        assert isinstance(indicators, dict)
```

## 📋 **Registry Entry Template**

### **Project Model Registry Entry**

```json
{
  "domains": {
    "domain_name": {
      "patterns": [
        "src/domain_name/*.py",
        "**/*domain_name*.py",
        "tests/test_domain_name*.py"
      ],
      "content_indicators": [
        "DomainImplementation",
        "domain_name",
        "DomainState",
        "DomainConfig"
      ],
      "linter": "flake8",
      "validator": "pytest",
      "formatter": "black",
      "requirements": [
        "Implement Reflective Module interfaces",
        "Provide core domain functionality",
        "Support tool integration",
        "Maintain health monitoring",
        "Enable operational tracking"
      ],
      "tools": [
        "tool1",
        "tool2"
      ],
      "capabilities": [
        "core_operations",
        "health_monitoring",
        "operational_tracking",
        "tool_integration"
      ],
      "workflows": {
        "initialization": {
          "step1": "Create domain instance",
          "step2": "Initialize domain",
          "step3": "Verify initialization",
          "step4": "Set ready state"
        },
        "operation_execution": {
          "step1": "Validate operation",
          "step2": "Execute operation",
          "step3": "Update metrics",
          "step4": "Return result"
        },
        "health_monitoring": {
          "step1": "Check domain state",
          "step2": "Calculate metrics",
          "step3": "Determine health status",
          "step4": "Return health indicators"
        }
      },
      "tool_rules": {
        "rm_compliance": "All domains must implement Reflective Module interfaces",
        "health_monitoring": "All domains must provide health monitoring",
        "error_handling": "All domains must implement comprehensive error handling",
        "testing": "All domains must have comprehensive test coverage"
      },
      "exclusions": [
        "*.pyc",
        "__pycache__",
        "*.log",
        ".pytest_cache"
      ],
      "demo_role": "tool",
      "extraction_candidate": "MEDIUM",
      "reason": "Well-defined domain with clear boundaries and interfaces",
      "status": "completed",
      "completion_date": "2024-01-01"
    }
  }
}
```

## 🚀 **Usage Examples**

### **Basic Usage**

```python
from src.domain_name.core.domain_class import DomainImplementation
from src.domain_name.core.models import DomainConfig

# Create domain instance
config = DomainConfig(name="my_domain", debug=True)
domain = DomainImplementation(config)

# Initialize domain
await domain.initialize()

# Execute operation
result = await domain.execute_operation("my_operation", param1="value1")

# Check health
is_healthy = await domain.is_healthy()
status = await domain.get_module_status()

# Get capabilities
capabilities = await domain.get_module_capabilities()
```

### **Tool Usage**

```python
from src.domain_name.tools.tool1 import Tool1

# Create tool instance
tool = Tool1({"setting": "value"})

# Initialize tool
await tool.initialize()

# Execute tool
result = await tool.execute("input_data")

# Get tool info
info = tool.get_tool_info()
```

### **Testing Usage**

```python
import pytest
from src.domain_name.core.domain_class import DomainImplementation

@pytest.mark.asyncio
async def test_domain_operation():
    """Test domain operation."""
    domain = DomainImplementation()
    await domain.initialize()
    
    result = await domain.execute_operation("test_operation")
    
    assert result.success
    assert result.result is not None
```

## 📚 **Best Practices**

### **Implementation**

- **Follow the template structure** exactly
- **Implement all required interfaces** for RM compliance
- **Use comprehensive error handling** throughout
- **Maintain consistent naming conventions**

### **Testing**

- **Write comprehensive tests** for all functionality
- **Test RM compliance** thoroughly
- **Use fixtures** for test setup and teardown
- **Mock external dependencies** appropriately

### **Documentation**

- **Document all public interfaces** clearly
- **Provide usage examples** for common scenarios
- **Update documentation** when making changes
- **Follow documentation standards** consistently

### **Registry Integration**

- **Add complete registry entries** with all required fields
- **Update domain architecture** categories appropriately
- **Validate registry integration** thoroughly
- **Test domain detection** and tool integration

## 🔗 **Related Documentation**

- [DOMAIN_ARCHITECTURE.md](./DOMAIN_ARCHITECTURE.md) - Overall domain architecture
- [DOMAIN_REGISTRY.md](./DOMAIN_REGISTRY.md) - Project model registry structure
- [DOMAIN_COMPLIANCE.md](./DOMAIN_COMPLIANCE.md) - RM compliance requirements
- [DOMAIN_DEVELOPMENT.md](./DOMAIN_DEVELOPMENT.md) - Domain development guidelines
- [DOMAIN_TESTING.md](./DOMAIN_TESTING.md) - Domain testing standards
- [project_model_registry.json](../project_model_registry.json) - Central domain registry
