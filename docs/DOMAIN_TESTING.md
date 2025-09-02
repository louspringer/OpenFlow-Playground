# Domain Testing

## 🎯 **Overview**

Domain testing ensures that all domains in the OpenFlow Playground project meet quality standards, functional requirements, and compliance requirements. This guide covers comprehensive testing strategies, standards, and implementation for domain development.

## 🏗️ **Testing Architecture**

### **Testing Pyramid**

```
        /\
       /  \
      /E2E \     <- End-to-End Tests (Few)
     /______\
    /        \
   /Integration\ <- Integration Tests (Some)
  /____________\
 /              \
/   Unit Tests   \ <- Unit Tests (Many)
/________________\
```

### **Testing Layers**

#### **1. Unit Tests**

- **Scope**: Individual components and methods
- **Coverage**: High coverage of individual functionality
- **Speed**: Fast execution
- **Isolation**: Completely isolated from external dependencies

#### **2. Integration Tests**

- **Scope**: Component interactions and workflows
- **Coverage**: Medium coverage of integration points
- **Speed**: Moderate execution time
- **Dependencies**: May include external dependencies

#### **3. End-to-End Tests**

- **Scope**: Complete workflows and user scenarios
- **Coverage**: Low coverage but high confidence
- **Speed**: Slow execution
- **Dependencies**: Full system dependencies

#### **4. Compliance Tests**

- **Scope**: RM compliance and standards adherence
- **Coverage**: Complete compliance validation
- **Speed**: Fast to moderate execution
- **Dependencies**: Minimal external dependencies

## 🔧 **Testing Standards**

### **Test Organization**

```
src/domain_name/tests/
├── __init__.py
├── test_core.py              # Core functionality tests
├── test_tools.py             # Tool integration tests
├── test_models.py            # Data model tests
├── test_utils.py             # Utility function tests
├── test_integration.py       # Integration tests
├── test_compliance.py        # RM compliance tests
└── fixtures/                 # Test fixtures
    ├── __init__.py
    ├── sample_data.py
    └── mock_objects.py
```

### **Test Naming Conventions**

```python
# Test class naming
class TestDomainImplementation:
    """Test domain implementation."""

class TestDomainTools:
    """Test domain tools."""

class TestDomainCompliance:
    """Test domain RM compliance."""

# Test method naming
def test_initialization():
    """Test domain initialization."""

def test_get_module_status():
    """Test module status reporting."""

def test_health_check():
    """Test health checking functionality."""

async def test_async_operation():
    """Test async operation."""
```

### **Test Structure**

```python
import pytest
from unittest.mock import Mock, patch
from src.domain_name.core.domain_class import DomainImplementation

class TestDomainImplementation:
    """Test domain implementation."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.domain = DomainImplementation()
    
    def teardown_method(self):
        """Teardown for each test method."""
        # Cleanup if needed
        pass
    
    def test_initialization(self):
        """Test domain initialization."""
        # Arrange
        # Act
        domain = DomainImplementation()
        # Assert
        assert domain is not None
        assert not domain.initialized
    
    async def test_async_operation(self):
        """Test async operation."""
        # Arrange
        expected_result = "expected"
        # Act
        result = await self.domain.async_operation()
        # Assert
        assert result == expected_result
```

## 🧪 **Unit Testing**

### **Core Functionality Testing**

```python
class TestDomainCore:
    """Test domain core functionality."""
    
    def test_initialization(self):
        """Test domain initialization."""
        domain = DomainImplementation()
        assert domain is not None
        assert not domain.initialized
    
    async def test_initialize(self):
        """Test domain initialization."""
        domain = DomainImplementation()
        await domain.initialize()
        assert domain.initialized
    
    def test_configuration(self):
        """Test domain configuration."""
        domain = DomainImplementation()
        config = domain.get_configuration()
        assert isinstance(config, dict)
        assert "setting1" in config
    
    def test_error_handling(self):
        """Test error handling."""
        domain = DomainImplementation()
        with pytest.raises(ValueError):
            domain.invalid_operation()
```

### **Tool Integration Testing**

```python
class TestDomainTools:
    """Test domain tool integration."""
    
    def test_tool_initialization(self):
        """Test tool initialization."""
        tool = DomainTool()
        assert tool is not None
        assert tool.initialized
    
    def test_tool_execution(self):
        """Test tool execution."""
        tool = DomainTool()
        result = tool.execute("input")
        assert result is not None
        assert result.success
    
    def test_tool_error_handling(self):
        """Test tool error handling."""
        tool = DomainTool()
        with pytest.raises(ToolError):
            tool.execute("invalid_input")
    
    @patch('external_service.call')
    def test_tool_external_dependency(self, mock_call):
        """Test tool with external dependency."""
        mock_call.return_value = "mocked_response"
        tool = DomainTool()
        result = tool.execute_with_external("input")
        assert result == "mocked_response"
        mock_call.assert_called_once_with("input")
```

### **Data Model Testing**

```python
class TestDomainModels:
    """Test domain data models."""
    
    def test_model_creation(self):
        """Test model creation."""
        model = DomainModel(
            field1="value1",
            field2="value2"
        )
        assert model.field1 == "value1"
        assert model.field2 == "value2"
    
    def test_model_validation(self):
        """Test model validation."""
        with pytest.raises(ValidationError):
            DomainModel(
                field1="",  # Invalid empty value
                field2="value2"
            )
    
    def test_model_serialization(self):
        """Test model serialization."""
        model = DomainModel(
            field1="value1",
            field2="value2"
        )
        data = model.model_dump()
        assert isinstance(data, dict)
        assert data["field1"] == "value1"
    
    def test_model_deserialization(self):
        """Test model deserialization."""
        data = {
            "field1": "value1",
            "field2": "value2"
        }
        model = DomainModel.model_validate(data)
        assert model.field1 == "value1"
        assert model.field2 == "value2"
```

## 🔗 **Integration Testing**

### **Component Integration**

```python
class TestDomainIntegration:
    """Test domain component integration."""
    
    async def test_core_tool_integration(self):
        """Test core and tool integration."""
        domain = DomainImplementation()
        await domain.initialize()
        
        tool = DomainTool()
        result = await domain.execute_with_tool("input")
        
        assert result is not None
        assert result.success
    
    async def test_workflow_integration(self):
        """Test complete workflow integration."""
        domain = DomainImplementation()
        await domain.initialize()
        
        workflow_result = await domain.execute_workflow({
            "step1": "input1",
            "step2": "input2"
        })
        
        assert workflow_result is not None
        assert workflow_result.completed
        assert len(workflow_result.steps) == 2
    
    def test_external_service_integration(self):
        """Test external service integration."""
        domain = DomainImplementation()
        
        with patch('external_service.ExternalService') as mock_service:
            mock_service.return_value.call.return_value = "success"
            
            result = domain.call_external_service("input")
            
            assert result == "success"
            mock_service.return_value.call.assert_called_once_with("input")
```

### **Cross-Domain Integration**

```python
class TestCrossDomainIntegration:
    """Test integration with other domains."""
    
    async def test_domain_a_to_domain_b(self):
        """Test integration from domain A to domain B."""
        domain_a = DomainAImplementation()
        domain_b = DomainBImplementation()
        
        await domain_a.initialize()
        await domain_b.initialize()
        
        result = await domain_a.integrate_with_domain_b("input")
        
        assert result is not None
        assert result.success
    
    async def test_shared_resource_integration(self):
        """Test shared resource integration."""
        domain1 = DomainImplementation()
        domain2 = DomainImplementation()
        
        await domain1.initialize()
        await domain2.initialize()
        
        # Test shared resource access
        resource1 = await domain1.get_shared_resource()
        resource2 = await domain2.get_shared_resource()
        
        assert resource1 is not None
        assert resource2 is not None
        assert resource1.id == resource2.id
```

## ✅ **Compliance Testing**

### **RM Compliance Testing**

```python
class TestDomainCompliance:
    """Test domain RM compliance."""
    
    async def test_module_status(self):
        """Test module status reporting."""
        domain = DomainImplementation()
        status = await domain.get_module_status()
        
        assert isinstance(status, ModuleHealth)
        assert status.status in [ModuleStatus.AVAILABLE, ModuleStatus.PARTIALLY_AVAILABLE, ModuleStatus.NOT_AVAILABLE]
        assert isinstance(status.message, str)
        assert isinstance(status.capabilities, list)
        assert isinstance(status.health_indicators, dict)
        assert isinstance(status.timestamp, float)
    
    async def test_module_capabilities(self):
        """Test module capability reporting."""
        domain = DomainImplementation()
        capabilities = await domain.get_module_capabilities()
        
        assert isinstance(capabilities, list)
        for capability in capabilities:
            assert isinstance(capability, ModuleCapability)
            assert isinstance(capability.name, str)
            assert isinstance(capability.description, str)
            assert isinstance(capability.available, bool)
            assert isinstance(capability.version, str)
            assert isinstance(capability.details, dict)
    
    async def test_health_check(self):
        """Test health checking."""
        domain = DomainImplementation()
        is_healthy = await domain.is_healthy()
        
        assert isinstance(is_healthy, bool)
    
    async def test_health_indicators(self):
        """Test health indicators."""
        domain = DomainImplementation()
        indicators = await domain.get_health_indicators()
        
        assert isinstance(indicators, dict)
        assert "error_count" in indicators
        assert "success_rate" in indicators
        assert "last_operation" in indicators
```

### **Tool Compliance Testing**

```python
class TestToolCompliance:
    """Test tool compliance with domain specifications."""
    
    def test_linter_compliance(self):
        """Test linter compliance."""
        domain_files = get_domain_files("domain_name")
        
        for file_path in domain_files:
            result = run_linter(file_path)
            assert result.exit_code == 0, f"Linting failed for {file_path}: {result.stdout}"
    
    def test_formatter_compliance(self):
        """Test formatter compliance."""
        domain_files = get_domain_files("domain_name")
        
        for file_path in domain_files:
            result = run_formatter(file_path)
            assert result.exit_code == 0, f"Formatting failed for {file_path}: {result.stdout}"
    
    def test_validator_compliance(self):
        """Test validator compliance."""
        domain_files = get_domain_files("domain_name")
        
        for file_path in domain_files:
            result = run_validator(file_path)
            assert result.exit_code == 0, f"Validation failed for {file_path}: {result.stdout}"
```

## 🚀 **End-to-End Testing**

### **Complete Workflow Testing**

```python
class TestDomainE2E:
    """Test complete domain workflows."""
    
    async def test_complete_workflow(self):
        """Test complete domain workflow."""
        # Setup
        domain = DomainImplementation()
        await domain.initialize()
        
        # Execute complete workflow
        workflow_input = {
            "input1": "value1",
            "input2": "value2"
        }
        
        result = await domain.execute_complete_workflow(workflow_input)
        
        # Verify results
        assert result is not None
        assert result.success
        assert result.output is not None
        assert len(result.steps) > 0
        
        # Verify each step
        for step in result.steps:
            assert step.completed
            assert step.result is not None
    
    async def test_error_recovery_workflow(self):
        """Test error recovery workflow."""
        domain = DomainImplementation()
        await domain.initialize()
        
        # Simulate error condition
        with patch('domain_operation') as mock_operation:
            mock_operation.side_effect = [Exception("Simulated error"), "success"]
            
            result = await domain.execute_workflow_with_recovery("input")
            
            assert result is not None
            assert result.success
            assert result.recovery_attempts > 0
```

### **User Scenario Testing**

```python
class TestUserScenarios:
    """Test user scenarios."""
    
    async def test_user_scenario_1(self):
        """Test user scenario 1."""
        # Setup user context
        user_context = create_user_context()
        domain = DomainImplementation()
        await domain.initialize()
        
        # Execute user scenario
        result = await domain.execute_user_scenario(user_context)
        
        # Verify user experience
        assert result is not None
        assert result.user_satisfied
        assert result.completion_time < 30  # seconds
    
    async def test_user_scenario_2(self):
        """Test user scenario 2."""
        # Setup different user context
        user_context = create_advanced_user_context()
        domain = DomainImplementation()
        await domain.initialize()
        
        # Execute advanced scenario
        result = await domain.execute_advanced_scenario(user_context)
        
        # Verify advanced functionality
        assert result is not None
        assert result.advanced_features_used
        assert result.performance_acceptable
```

## 🔍 **Test Fixtures and Utilities**

### **Test Fixtures**

```python
# fixtures/sample_data.py
import pytest
from typing import Dict, Any

@pytest.fixture
def sample_domain_config():
    """Sample domain configuration."""
    return {
        "setting1": "value1",
        "setting2": "value2",
        "timeout": 30
    }

@pytest.fixture
def sample_domain_input():
    """Sample domain input."""
    return {
        "input1": "test_value1",
        "input2": "test_value2"
    }

@pytest.fixture
def mock_external_service():
    """Mock external service."""
    with patch('external_service.ExternalService') as mock:
        mock.return_value.call.return_value = "mocked_response"
        yield mock

# fixtures/mock_objects.py
from unittest.mock import Mock

@pytest.fixture
def mock_domain_tool():
    """Mock domain tool."""
    mock = Mock()
    mock.execute.return_value = Mock(success=True, result="mocked_result")
    return mock

@pytest.fixture
def mock_health_monitor():
    """Mock health monitor."""
    mock = Mock()
    mock.get_success_rate.return_value = 0.95
    mock.get_error_count.return_value = 0
    return mock
```

### **Test Utilities**

```python
# test_utils.py
import asyncio
from typing import Any, Dict

def run_async_test(coro):
    """Run async test."""
    return asyncio.run(coro)

def create_test_domain():
    """Create test domain instance."""
    return DomainImplementation()

def assert_domain_healthy(domain):
    """Assert domain is healthy."""
    assert domain is not None
    assert domain.initialized

def assert_workflow_result(result):
    """Assert workflow result."""
    assert result is not None
    assert result.success
    assert result.completion_time is not None
```

## 📊 **Test Coverage and Metrics**

### **Coverage Requirements**

- **Unit Tests**: Minimum 90% line coverage
- **Integration Tests**: Minimum 70% integration coverage
- **Compliance Tests**: 100% compliance coverage
- **E2E Tests**: Critical path coverage

### **Coverage Measurement**

```bash
# Run coverage analysis
uv run python -m pytest --cov=src/domain_name --cov-report=html --cov-report=term

# Generate coverage report
uv run python -m coverage report --show-missing

# Generate HTML coverage report
uv run python -m coverage html
```

### **Test Metrics**

```python
# test_metrics.py
import time
from typing import Dict, Any

class TestMetrics:
    """Test execution metrics."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.test_results = []
    
    def start_test(self, test_name: str):
        """Start test timing."""
        self.start_time = time.time()
        self.current_test = test_name
    
    def end_test(self, success: bool):
        """End test timing."""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        self.test_results.append({
            "test_name": self.current_test,
            "success": success,
            "duration": duration
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary."""
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        total_duration = sum(r["duration"] for r in self.test_results)
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": total_duration / total_tests if total_tests > 0 else 0
        }
```

## 🚀 **Test Automation**

### **Continuous Integration**

```yaml
# .github/workflows/domain_testing.yml
name: Domain Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        domain: [domain1, domain2, domain3]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: uv sync
      - name: Test domain
        run: make ${{ matrix.domain }}-test
      - name: Lint domain
        run: make ${{ matrix.domain }}-lint
      - name: Check compliance
        run: make ${{ matrix.domain }}-compliance
```

### **Test Automation Scripts**

```bash
#!/bin/bash
# scripts/run_domain_tests.sh

DOMAIN_NAME=$1
if [ -z "$DOMAIN_NAME" ]; then
    echo "Usage: $0 <domain_name>"
    exit 1
fi

echo "🧪 Testing domain: $DOMAIN_NAME"

# Run unit tests
echo "Running unit tests..."
uv run python -m pytest src/$DOMAIN_NAME/tests/ -v

# Run integration tests
echo "Running integration tests..."
uv run python -m pytest tests/test_${DOMAIN_NAME}_integration.py -v

# Run compliance tests
echo "Running compliance tests..."
uv run python -m pytest tests/test_rm_compliance.py::Test${DOMAIN_NAME^}Compliance -v

# Run coverage analysis
echo "Running coverage analysis..."
uv run python -m pytest --cov=src/$DOMAIN_NAME --cov-report=term

echo "✅ Domain testing completed for $DOMAIN_NAME"
```

## 📚 **Best Practices**

### **Test Design**

- **Test Isolation**: Each test should be independent
- **Clear Naming**: Use descriptive test names
- **Single Responsibility**: Each test should test one thing
- **Arrange-Act-Assert**: Follow AAA pattern

### **Test Implementation**

- **Mock External Dependencies**: Mock external services and dependencies
- **Use Fixtures**: Use pytest fixtures for setup and teardown
- **Async Testing**: Properly handle async operations
- **Error Testing**: Test error conditions and edge cases

### **Test Maintenance**

- **Keep Tests Current**: Update tests when code changes
- **Remove Dead Tests**: Remove tests for removed functionality
- **Refactor Tests**: Refactor tests to improve maintainability
- **Monitor Performance**: Monitor test execution performance

## 🔗 **Integration Points**

### **Build System Integration**

```makefile
# Makefile targets for domain testing
domain_name-test:
	@echo "🧪 Testing domain_name domain"
	uv run python -m pytest src/domain_name/tests/ -v

domain_name-test-coverage:
	@echo "📊 Testing domain_name with coverage"
	uv run python -m pytest --cov=src/domain_name --cov-report=html

domain_name-test-compliance:
	@echo "✅ Testing domain_name compliance"
	uv run python -m pytest tests/test_rm_compliance.py::TestDomainNameCompliance -v
```

### **CI/CD Integration**

- **Automated Testing**: CI/CD runs all domain tests
- **Quality Gates**: Tests must pass for deployment
- **Coverage Reporting**: CI/CD reports test coverage
- **Performance Monitoring**: CI/CD monitors test performance

### **Registry Integration**

- **Test Discovery**: Registry enables automatic test discovery
- **Tool Integration**: Registry integrates testing tools
- **Compliance Validation**: Registry validates test compliance
- **Reporting Integration**: Registry integrates test reporting

## 📚 **Related Documentation**

- [DOMAIN_ARCHITECTURE.md](./DOMAIN_ARCHITECTURE.md) - Overall domain architecture
- [DOMAIN_REGISTRY.md](./DOMAIN_REGISTRY.md) - Project model registry structure
- [DOMAIN_COMPLIANCE.md](./DOMAIN_COMPLIANCE.md) - RM compliance requirements
- [DOMAIN_DEVELOPMENT.md](./DOMAIN_DEVELOPMENT.md) - Domain development guidelines
- [project_model_registry.json](../project_model_registry.json) - Central domain registry
