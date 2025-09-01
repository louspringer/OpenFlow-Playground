# Ghostbusters Reflective Module Architecture

## 🎯 **Overview**

This document describes the new reflective module architecture for Ghostbusters, which provides clean separation between functional capabilities and operational concerns while enforcing architectural boundaries. The architecture follows the principle of **module reflection** - modules expose their own status and capabilities through defined interfaces rather than being probed internally.

## 🏗️ **Architectural Principles**

### **1. Model-Driven + Runtime Monitoring**

- **Project model as specification**: Defines what should exist, what tools should work, what requirements should be met
- **Runtime monitoring for health**: Checks what's actually working right now vs. what's broken
- **Combined intelligence**: "You can't manage it if you don't monitor it. And you can't monitor it unless you know what it's supposed to do and not do."

### **2. Dual-Dimensional Architecture**

- **Multi-Perspective Analysis**: Current system using expert agents for different viewpoints
- **Multi-Agent System**: Future system using external LLMs and AI agents
- **Complementary dimensions**: Both systems work together, not as alternatives

### **3. Graceful Degradation**

- **Feature flags**: Perspectives can be broken without killing the whole system
- **Health monitoring**: Real-time status of what's working vs. what's broken
- **Impact assessment**: Understanding how broken components affect overall results

## 🔧 **Core Components**

### **1. Reflective Module Interfaces**

#### **Base Reflective Module Interface**

```python
class ReflectiveModule(ABC):
    @abstractmethod
    async def get_module_status(self) -> ModuleHealth:
        """Get current module status"""
        pass

    @abstractmethod
    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get module capabilities"""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if module is healthy"""
        pass
```

#### **Multi-Perspective Reflective Module Interface**

```python
class MultiPerspectiveReflectiveModule(ReflectiveModule):
    @abstractmethod
    async def get_available_perspectives(self) -> List[str]:
        """Get list of available analysis perspectives"""
        pass

    @abstractmethod
    async def get_perspective_status(self, perspective: str) -> ModuleHealth:
        """Get status of a specific perspective"""
        pass
```

#### **Multi-Agent Reflective Module Interface**

```python
class MultiAgentReflectiveModule(ReflectiveModule):
    @abstractmethod
    async def get_available_agents(self) -> List[str]:
        """Get list of available AI agents"""
        pass

    @abstractmethod
    async def get_agent_status(self, agent: str) -> ModuleHealth:
        """Get status of a specific agent"""
        pass

    @abstractmethod
    async def get_llm_provider_status(self) -> Dict[str, ModuleHealth]:
        """Get status of LLM providers (OpenAI, Anthropic, etc.)"""
        pass
```

### **2. Project Model Integration**

The `project_model_registry.json` serves as the central specification and capability registry for all reflective modules:

```python
# Instead of a separate service registry, we use the project model
# to define what should exist and validate what actually exists

class ProjectModelIntegration:
    def load_project_model(self) -> Dict[str, Any]
    def get_ghostbusters_domain(self) -> Dict[str, Any]
    def get_module_requirements(self) -> List[str]
    def validate_module_compliance(self, module: ReflectiveModule) -> bool
    def get_expected_capabilities(self) -> List[str]
```

### **3. Module Health and Status**

#### **Module Status Enumeration**

```python
class ModuleStatus(Enum):
    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    NOT_AVAILABLE = "not_available"
    UNKNOWN = "unknown"
```

#### **Service Health Structure**

```python
@dataclass
class ServiceHealth:
    status: ServiceStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None
```

#### **Service Capability Structure**

```python
@dataclass
class ServiceCapability:
    name: str
    available: bool
    description: str
    version: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
```

## 🚀 **Implementation Status**

### **✅ Completed Components**

1. **Service Interfaces** (`src/ghostbusters/service_interfaces.py`)

   - Base service interface definitions
   - Multi-perspective and multi-agent interfaces
   - Service health and capability structures

1. **Multi-Perspective Service** (`src/ghostbusters/multi_perspective_service.py`)

   - Implements `MultiPerspectiveServiceInterface`
   - Wraps existing expert agents
   - **Integrates with project model** for capability discovery
   - Provides health monitoring and requirement mapping

1. **Project Model Integration** (`project_model_registry.json`)

   - **Specification baseline**: Defines what should exist and work
   - **Requirement mapping**: Links perspectives to specific requirements
   - **Tool orchestration**: Specifies linter/validator/formatter mappings

1. **Updated Availability Test** (`src/ghostbusters/availability_test.py`)

   - **Model-driven validation**: Uses project model as specification
   - **Runtime health monitoring**: Checks what's actually working
   - **Combined intelligence**: Shows compliance + health status
   - **Graceful degradation reporting**: Shows impact of broken components

### **🔄 In Progress**

1. **Service Interface Implementation**
   - Recovery engines need `RecoveryServiceInterface`
   - Validators need `ValidationServiceInterface`
   - All services need to implement base interfaces

### **📋 Planned Components**

1. **Recovery Service Interfaces**

   - `SyntaxRecoveryEngine` → `RecoveryServiceInterface`
   - `IndentationFixer` → `RecoveryServiceInterface`
   - `ImportResolver` → `RecoveryServiceInterface`
   - `TypeAnnotationFixer` → `RecoveryServiceInterface`

1. **Validation Service Interfaces**

   - `SecurityValidator` → `ValidationServiceInterface`
   - `CodeQualityValidator` → `ValidationServiceInterface`
   - `TestValidator` → `ValidationServiceInterface`
   - `BuildValidator` → `ValidationServiceInterface`
   - `ArchitectureValidator` → `ValidationServiceInterface`
   - `ModelValidator` → `ValidationServiceInterface`

1. **Multi-Agent Service Implementation**

   - Future LLM integration
   - External AI agent orchestration
   - LangChain/LangGraph integration

## 🔍 **Usage Examples**

### **1. Running Availability Test (Combines Model + Runtime)**

```python
from src.ghostbusters.availability_test import GhostbustersAvailabilityTest

# Run comprehensive test that combines project model with runtime health
tester = GhostbustersAvailabilityTest()
results = await tester.run_comprehensive_test()

# Get human-readable status combining both
status_message = tester.get_status_message()
print(status_message)
# Output: "Multi-perspective analysis + Multi-agent system available (6 perspectives, 7 capabilities)"
```

### **2. Using Multi-Perspective Service (Model-Integrated)**

```python
from src.ghostbusters.multi_perspective_service import MultiPerspectiveService

# Create service that integrates with project model
service = MultiPerspectiveService()

# Get capabilities based on project model requirements
capabilities = await service.get_service_capabilities()
for cap in capabilities:
    print(f"{cap.name}: {cap.description}")
    if cap.details.get("project_model_requirements"):
        print(f"  Requirements: {cap.details['project_model_requirements']}")
```

### **3. Checking Project Model Compliance**

```python
# The availability test automatically checks:
# - Project model availability and structure
# - Ghostbusters domain configuration
# - Required patterns and content indicators
# - Requirements traceability
# - Runtime health of all perspectives
```

### **2. Checking Service Health**

```python
from src.ghostbusters.service_registry import is_ghostbusters_healthy

# Check if all services are healthy
is_healthy = await is_ghostbusters_healthy()
if is_healthy:
    print("✅ All Ghostbusters services are healthy")
else:
    print("❌ Some services are unhealthy")
```

### **3. Running Availability Test**

```python
from src.ghostbusters.availability_test import GhostbustersAvailabilityTest

# Run comprehensive availability test
tester = GhostbustersAvailabilityTest()
results = await tester.run_comprehensive_test()

# Get human-readable status
status_message = tester.get_status_message()
print(status_message)
```

### **4. Using Multi-Perspective Service**

```python
from src.ghostbusters.multi_perspective_service import MultiPerspectiveService

# Create service instance
service = MultiPerspectiveService()

# Get available perspectives
perspectives = await service.get_available_perspectives()
print(f"Available perspectives: {perspectives}")

# Run analysis with specific perspective
result = await service.run_analysis("security", project_path=".")
print(f"Security analysis found {result['delusions_found']} delusions")
```

## 🎯 **Benefits of New Architecture**

### **1. Model-Driven + Runtime Monitoring**

- **Project model as specification**: Defines what should exist and work
- **Runtime health monitoring**: Shows what's actually working right now
- **Combined intelligence**: "You can't manage it if you don't monitor it. And you can't monitor it unless you know what it's supposed to do and not do."

### **2. Graceful Degradation Management**

- **Feature flags**: Individual perspectives can be broken without killing the whole system
- **Health monitoring**: Real-time status of what's working vs. what's broken
- **Impact assessment**: Understanding how broken components affect overall results

### **2. Easier Testing and Mocking**

- **Interface-based testing**: Mock services by implementing interfaces
- **Isolated testing**: Test functional logic without operational concerns
- **Better test coverage**: Clear contracts make testing more reliable

### **3. Better Monitoring and Observability**

- **Health monitoring**: Each service reports its own health
- **Capability discovery**: Services expose what they can do
- **Performance metrics**: Track success rates and error counts

### **4. Future-Proof Design**

- **Easy to add new services**: Just implement the interfaces
- **Easy to extend capabilities**: Add new interface methods
- **Easy to integrate**: External systems use clean APIs

### **5. Enterprise Readiness**

- **Service discovery**: Find available services automatically
- **Health dashboards**: Monitor all services from one place
- **Integration friendly**: Clean APIs for external systems

## 🔄 **Migration Path**

### **Phase 1: Core Interfaces (✅ Complete)**

- [x] Define service interfaces
- [x] Implement multi-perspective service
- [x] Create service registry
- [x] Update availability tests

### **Phase 2: Service Enhancement (🔄 In Progress)**

- [ ] Implement `RecoveryServiceInterface` for all recovery engines
- [ ] Implement `ValidationServiceInterface` for all validators
- [ ] Add health monitoring to all services
- [ ] Implement capability discovery for all services

### **Phase 3: Advanced Features (📋 Planned)**

- [ ] Service auto-discovery and registration
- [ ] Dynamic capability loading
- [ ] Service dependency management
- [ ] Automated health recovery

### **Phase 4: Multi-Agent Integration (📋 Future)**

- [ ] Implement `MultiAgentServiceInterface`
- [ ] Add LLM provider status monitoring
- [ ] Implement agent health monitoring
- [ ] Add fallback mechanisms for LLM failures

## 🧪 **Testing Strategy**

### **1. Interface Compliance Testing**

```python
def test_service_interface_compliance():
    """Test that all services implement required interfaces"""
    services = get_all_services()
    for service in services:
        assert hasattr(service, 'get_service_status')
        assert hasattr(service, 'get_service_capabilities')
        assert hasattr(service, 'is_healthy')
```

### **2. Service Registry Testing**

```python
def test_service_registry_functionality():
    """Test service registry operations"""
    registry = GhostbustersServiceRegistry()
    await registry.initialize_registry()
    
    # Test service registration
    assert len(registry.services) > 0
    
    # Test health checking
    is_healthy = await registry.health_check()
    assert isinstance(is_healthy, bool)
```

### **3. Availability Test Testing**

```python
def test_availability_test_uses_interfaces():
    """Test that availability test uses service interfaces"""
    tester = GhostbustersAvailabilityTest()
    results = await tester.run_comprehensive_test()
    
    # Should not contain implementation details
    assert 'implementation' not in str(results)
    assert 'internal' not in str(results)
```

## 🚨 **Breaking Changes**

### **What Changes:**

- **Availability Testing**: No more implementation probing
- **Service Status**: Must come through interfaces
- **Health Checks**: Services must implement health monitoring
- **Capability Discovery**: Must be explicit through interfaces

### **What Stays the Same:**

- **Core Functionality**: All existing analysis capabilities
- **Recovery Engines**: All existing fix capabilities
- **Validation Logic**: All existing validation rules
- **Multi-Perspective Analysis**: Current perspective implementations

## 🎯 **Success Criteria**

### **✅ Service Interface Compliance**

- All services implement required interfaces
- No implementation details exposed through status APIs
- Services are completely reflective about their capabilities

### **✅ External Status Interface**

- Availability tests use only service interfaces
- No reaching inside implementations
- Clear, meaningful status messages

### **✅ Service Health Monitoring**

- Each service monitors its own health
- Degraded states are properly reported
- Recovery information is provided

### **✅ Registry Management**

- All services are properly registered
- Service discovery works correctly
- Failures are handled gracefully

## 🚀 **Next Steps**

1. **Complete Service Interfaces**: Implement interfaces for recovery engines and validators
1. **Add Health Monitoring**: Each service monitors itself
1. **Create Health Dashboards**: Visual monitoring of all services
1. **Implement Multi-Agent**: Add AI agent capabilities
1. **Add Advanced Features**: Auto-discovery, dependency management

## 📚 **Related Documentation**

- [Revised Ghostbusters Requirements](./REVISED_GHOSTBUSTERS_REQUIREMENTS.md)
- [System Degradation Management Principles](./SYSTEM_DEGRADATION_MANAGEMENT.md)
- [Service Interface Definitions](../src/ghostbusters/service_interfaces.py)
- [Multi-Perspective Service](../src/ghostbusters/multi_perspective_service.py)

______________________________________________________________________

**This architecture shift makes Ghostbusters more maintainable, testable, and future-proof while preserving all existing functionality.**
