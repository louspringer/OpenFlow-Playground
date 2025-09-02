# Domain Compliance

## 🎯 **Overview**

**Reflective Module (RM) Compliance** is a core requirement for all domains in the OpenFlow Playground project. Every domain must implement the Reflective Module interfaces and follow established compliance standards to ensure consistent behavior, health monitoring, and operational tracking across the entire system.

## 🏗️ **RM Compliance Requirements**

### **1. Required Interfaces**

All domains must implement the following Reflective Module interfaces:

#### **Core Interface Methods**

```python
async def get_module_status(self) -> ModuleHealth:
    """Get the current operational status of this module."""
    
async def get_module_capabilities(self) -> List[ModuleCapability]:
    """Get the capabilities this module provides."""
    
async def is_healthy(self) -> bool:
    """Check if this module is currently healthy."""
    
async def get_health_indicators(self) -> Dict[str, Any]:
    """Get detailed health indicators."""
```

#### **Health Status Types**

```python
class ModuleStatus(Enum):
    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    NOT_AVAILABLE = "not_available"

class ModuleHealth(BaseModel):
    status: ModuleStatus
    message: str
    capabilities: List[ModuleCapability]
    health_indicators: Dict[str, Any]
    timestamp: float

class ModuleCapability(BaseModel):
    name: str
    description: str
    available: bool
    version: str
    details: Dict[str, Any]
```

### **2. Operational State Tracking**

All domains must track and report their operational state:

#### **Health Indicators**

- **Error Count**: Number of errors encountered
- **Success Rate**: Percentage of successful operations
- **Last Operation**: Timestamp of last operation
- **Performance Metrics**: Response times, throughput, etc.
- **Resource Usage**: Memory, CPU, disk usage

#### **Status Reporting**

- **Real-time Status**: Current operational status
- **Capability Reporting**: Available capabilities and versions
- **Health Degradation**: Detection and reporting of health issues
- **Recovery Status**: Status of recovery operations

### **3. Compliance Validation**

All domains must pass compliance validation:

#### **Interface Compliance**

- All required methods must be implemented
- Method signatures must match interface definitions
- Return types must be correct
- Error handling must be implemented

#### **Behavioral Compliance**

- Health checks must be accurate and reliable
- Status reporting must be consistent
- Capability reporting must be complete
- Error handling must be robust

## 🔧 **Compliance Implementation**

### **Base Reflective Module**

All domains should inherit from the base Reflective Module:

```python
from src.reflective_modules.base_reflective_module import ReflectiveModule

class DomainImplementation(ReflectiveModule):
    """Domain implementation with RM compliance."""
    
    async def get_module_status(self) -> ModuleHealth:
        """Get the current operational status of this module."""
        try:
            # Check actual operational state
            is_operational = self._check_operational_state()
            error_count = self._get_error_count()
            success_rate = self._calculate_success_rate()
            
            # Determine status based on health indicators
            if is_operational and error_count == 0 and success_rate > 0.95:
                status = ModuleStatus.AVAILABLE
                message = "Module is fully operational"
            elif is_operational and success_rate > 0.8:
                status = ModuleStatus.PARTIALLY_AVAILABLE
                message = f"Module operational with {success_rate:.1%} success rate"
            else:
                status = ModuleStatus.NOT_AVAILABLE
                message = f"Module has {error_count} errors, {success_rate:.1%} success rate"
            
            return ModuleHealth(
                status=status,
                message=message,
                capabilities=await self.get_module_capabilities(),
                health_indicators={
                    "error_count": error_count,
                    "success_rate": success_rate,
                    "last_operation": time.time()
                },
                timestamp=time.time()
            )
            
        except Exception as e:
            return ModuleHealth(
                status=ModuleStatus.NOT_AVAILABLE,
                message=f"Module status check failed: {e}",
                capabilities=[],
                health_indicators={"error": str(e)},
                timestamp=time.time()
            )
    
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get the capabilities this module provides."""
        try:
            return [
                ModuleCapability(
                    name="core_functionality",
                    description="Core domain functionality",
                    available=True,
                    version="1.0.0",
                    details={"class_name": self.__class__.__name__}
                ),
                ModuleCapability(
                    name="operational_monitoring",
                    description="ReflectiveModule operational monitoring",
                    available=True,
                    version="1.0.0",
                    details={"monitoring": "enabled"}
                )
            ]
        except Exception as e:
            logger.error(f"❌ Failed to get capabilities: {e}")
            return []
    
    async def is_healthy(self) -> bool:
        """Check if this module is currently healthy."""
        try:
            status = await self.get_module_status()
            return status.status == ModuleStatus.AVAILABLE
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False
    
    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators."""
        try:
            status = await self.get_module_status()
            return status.health_indicators
        except Exception as e:
            logger.error(f"❌ Failed to get health indicators: {e}")
            return {"error": str(e), "status": "unhealthy"}
```

### **Health Monitoring Implementation**

```python
class DomainHealthMonitor:
    """Health monitoring for domain compliance."""
    
    def __init__(self, domain: ReflectiveModule):
        self.domain = domain
        self.error_count = 0
        self.success_count = 0
        self.last_operation_time = time.time()
    
    def record_operation(self, success: bool):
        """Record an operation for health tracking."""
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        self.last_operation_time = time.time()
    
    def get_success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.error_count
        return self.success_count / total if total > 0 else 1.0
    
    def get_error_count(self) -> int:
        """Get current error count."""
        return self.error_count
```

## 📊 **Compliance Validation**

### **Automated Compliance Checking**

```python
async def validate_rm_compliance(domain: ReflectiveModule) -> ComplianceReport:
    """Validate RM compliance for a domain."""
    report = ComplianceReport()
    
    # Check interface implementation
    required_methods = [
        'get_module_status',
        'get_module_capabilities', 
        'is_healthy',
        'get_health_indicators'
    ]
    
    for method in required_methods:
        if not hasattr(domain, method):
            report.add_violation(f"Missing required method: {method}")
        elif not callable(getattr(domain, method)):
            report.add_violation(f"Method {method} is not callable")
    
    # Check method signatures
    try:
        status = await domain.get_module_status()
        if not isinstance(status, ModuleHealth):
            report.add_violation("get_module_status must return ModuleHealth")
    except Exception as e:
        report.add_violation(f"get_module_status failed: {e}")
    
    # Check health indicators
    try:
        indicators = await domain.get_health_indicators()
        if not isinstance(indicators, dict):
            report.add_violation("get_health_indicators must return Dict[str, Any]")
    except Exception as e:
        report.add_violation(f"get_health_indicators failed: {e}")
    
    return report
```

### **Compliance Testing**

```python
class TestRMCompliance:
    """Test RM compliance for domains."""
    
    async def test_module_status(self, domain: ReflectiveModule):
        """Test module status reporting."""
        status = await domain.get_module_status()
        assert isinstance(status, ModuleHealth)
        assert status.status in [ModuleStatus.AVAILABLE, ModuleStatus.PARTIALLY_AVAILABLE, ModuleStatus.NOT_AVAILABLE]
        assert isinstance(status.message, str)
        assert isinstance(status.capabilities, list)
        assert isinstance(status.health_indicators, dict)
        assert isinstance(status.timestamp, float)
    
    async def test_module_capabilities(self, domain: ReflectiveModule):
        """Test module capability reporting."""
        capabilities = await domain.get_module_capabilities()
        assert isinstance(capabilities, list)
        for capability in capabilities:
            assert isinstance(capability, ModuleCapability)
            assert isinstance(capability.name, str)
            assert isinstance(capability.description, str)
            assert isinstance(capability.available, bool)
            assert isinstance(capability.version, str)
            assert isinstance(capability.details, dict)
    
    async def test_health_check(self, domain: ReflectiveModule):
        """Test health checking."""
        is_healthy = await domain.is_healthy()
        assert isinstance(is_healthy, bool)
    
    async def test_health_indicators(self, domain: ReflectiveModule):
        """Test health indicators."""
        indicators = await domain.get_health_indicators()
        assert isinstance(indicators, dict)
```

## 🚀 **Compliance Standards**

### **Performance Requirements**

- **Response Time**: Health checks must complete within 1 second
- **Availability**: Modules must report accurate availability status
- **Reliability**: Health indicators must be consistent and reliable
- **Error Handling**: All methods must handle errors gracefully

### **Monitoring Requirements**

- **Real-time Monitoring**: Health status must be available in real-time
- **Historical Tracking**: Health indicators must be tracked over time
- **Alerting**: Health degradation must trigger appropriate alerts
- **Reporting**: Comprehensive health reporting must be available

### **Integration Requirements**

- **Tool Integration**: Compliance must integrate with existing tools
- **Workflow Integration**: Compliance must support domain workflows
- **Testing Integration**: Compliance must support automated testing
- **CI/CD Integration**: Compliance must integrate with CI/CD pipelines

## 🔍 **Compliance Enforcement**

### **Build System Integration**

```makefile
# Makefile targets for compliance checking
test-rm-compliance:
	@echo "🧪 Testing RM compliance across all domains"
	uv run python -m pytest tests/test_rm_compliance.py -v

check-module-sizes:
	@echo "📏 Checking module sizes for RM compliance"
	uv run python scripts/check_module_sizes.py

validate-rm-interfaces:
	@echo "🔍 Validating Reflective Module interfaces"
	uv run python scripts/validate_rm_interfaces.py
```

### **Quality Gates**

- **Pre-commit Hooks**: RM compliance must be checked before commits
- **CI/CD Validation**: Compliance must be validated in CI/CD pipelines
- **Deployment Gates**: Compliance must be validated before deployment
- **Monitoring Alerts**: Compliance violations must trigger alerts

### **Tool Integration**

- **Linting**: RM compliance must be checked by linters
- **Testing**: RM compliance must be tested automatically
- **Validation**: RM compliance must be validated continuously
- **Reporting**: RM compliance must be reported comprehensively

## 📚 **Best Practices**

### **Implementation**

- **Inherit from Base**: Always inherit from base Reflective Module
- **Error Handling**: Implement comprehensive error handling
- **Health Tracking**: Track health indicators accurately
- **Status Reporting**: Report status consistently and reliably

### **Testing**

- **Compliance Tests**: Write comprehensive compliance tests
- **Health Tests**: Test health checking functionality
- **Integration Tests**: Test compliance integration
- **Performance Tests**: Test compliance performance

### **Monitoring**

- **Real-time Monitoring**: Monitor health in real-time
- **Historical Analysis**: Analyze health trends over time
- **Alerting**: Set up appropriate health alerts
- **Reporting**: Generate comprehensive health reports

## 🔗 **Integration Points**

### **Domain Registry Integration**

- **Compliance Validation**: Registry validates RM compliance
- **Tool Integration**: Registry integrates compliance tools
- **Workflow Integration**: Registry integrates compliance workflows
- **Monitoring Integration**: Registry integrates compliance monitoring

### **Build System Integration**

- **Makefile Targets**: Build system includes compliance targets
- **Quality Gates**: Build system enforces compliance gates
- **Testing Integration**: Build system integrates compliance testing
- **Deployment Integration**: Build system integrates compliance deployment

### **CI/CD Integration**

- **Pipeline Validation**: CI/CD validates compliance
- **Quality Gates**: CI/CD enforces compliance gates
- **Testing Integration**: CI/CD integrates compliance testing
- **Deployment Gates**: CI/CD enforces compliance deployment gates

## 📚 **Related Documentation**

- [DOMAIN_ARCHITECTURE.md](./DOMAIN_ARCHITECTURE.md) - Overall domain architecture
- [DOMAIN_REGISTRY.md](./DOMAIN_REGISTRY.md) - Project model registry structure
- [DOMAIN_DEVELOPMENT.md](./DOMAIN_DEVELOPMENT.md) - Domain development guidelines
- [DOMAIN_TESTING.md](./DOMAIN_TESTING.md) - Domain testing standards
- [src/reflective_modules/base_reflective_module.py](../src/reflective_modules/base_reflective_module.py) - Base Reflective Module implementation
