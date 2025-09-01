# 🕵️ clewcrew-common

**Your friendly neighborhood hallucination-busting task force.**

We chase down stray fictions, unravel tangled logic, and return clean, fact-checked truth.

Not affiliated with any cartoon dogs, paranormal investigators, or 80s movie franchises — just here to keep the LLM output on the level.

## **Overview**

clewcrew-common is the foundational package that eliminates duplication across all clewcrew components. It provides standardized utilities for confidence scoring, logging, configuration management, and more.

## **🏗️ Architecture**

```
clewcrew-common
├── Confidence Scoring     # Standardized confidence calculation
├── Logging Framework     # Unified logging and monitoring
├── Configuration         # Environment and config management
├── Data Models          # Common Pydantic models
├── Async Utilities      # Common async patterns
├── File Operations      # Path handling, file operations
└── Validation          # Common validation patterns
```

## **📦 Installation**

```bash
# Install from PyPI
pip install clewcrew-common

# Or install with UV
uv add clewcrew-common
```

## **🚀 Quick Start**

### **Confidence Scoring**

```python
from clewcrew_common import ConfidenceCalculator, ConfidenceScore

# Calculate agent confidence
delusions = [
    {"confidence": 0.8, "severity": "high"},
    {"confidence": 0.6, "severity": "medium"}
]

confidence = ConfidenceCalculator.calculate_agent_confidence(delusions)
print(f"Confidence: {confidence.value:.2f}")
print(f"Factors: {confidence.factors}")
```

### **Logging Framework**

```python
from clewcrew_common import ClewcrewLogger

logger = ClewcrewLogger("my-component")
logger.info("Component initialized successfully")
logger.warning("Potential issue detected")
logger.error("Error occurred during execution")
```

### **Configuration Management**

```python
from clewcrew_common import ConfigManager

config = ConfigManager()
api_key = config.get("API_KEY", required=True)
debug_mode = config.get("DEBUG", default=False)
```

## **🔧 Core Components**

### **1. Confidence Scoring** 🎯

**Purpose**: Eliminate duplication of confidence calculation logic

**Features**:

- **Agent Confidence**: Calculate confidence for expert agents
- **Recovery Confidence**: Calculate confidence for recovery engines
- **Validation Confidence**: Calculate confidence for validators
- **Workflow Confidence**: Calculate confidence for workflow execution
- **Score Combination**: Combine multiple confidence scores

### **2. Logging Framework** 📝

**Purpose**: Unified logging across all clewcrew components

**Features**:

- **Structured Logging**: Consistent log format
- **Log Levels**: Standardized log levels
- **Context Tracking**: Track execution context
- **Performance Monitoring**: Built-in performance tracking

### **3. Configuration Management** ⚙️

**Purpose**: Centralized configuration management

**Features**:

- **Environment Variables**: Load from environment
- **Configuration Files**: Support for YAML/JSON configs
- **Validation**: Validate configuration values
- **Defaults**: Sensible defaults for all settings

### **4. Data Models** 📊

**Purpose**: Common Pydantic models for all components

**Features**:

- **BaseResult**: Common result model
- **BaseConfig**: Common configuration model
- **Validation**: Built-in validation rules
- **Serialization**: Easy JSON serialization

### **5. Async Utilities** ⚡

**Purpose**: Common async patterns and utilities

**Features**:

- **AsyncExecutor**: Execute async operations
- **Retry Logic**: Built-in retry mechanisms
- **Timeout Handling**: Configurable timeouts
- **Error Handling**: Standardized error handling

### **6. File Operations** 📁

**Purpose**: Common file and path operations

**Features**:

- **Path Handling**: Cross-platform path operations
- **File Reading**: Safe file reading utilities
- **File Writing**: Safe file writing utilities
- **Directory Operations**: Directory management utilities

### **7. Validation Utilities** ✅

**Purpose**: Common validation patterns

**Features**:

- **Input Validation**: Validate user inputs
- **Data Validation**: Validate data structures
- **Schema Validation**: Validate against schemas
- **Error Reporting**: Standardized error messages

## **🔗 Dependencies**

### **Core Dependencies**

- **Pydantic**: Data validation and serialization
- **Typing Extensions**: Enhanced type hints

### **Development Dependencies**

- **Pytest**: Testing framework
- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking

## **🧪 Testing**

### **Run Tests**

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m "unit"
pytest -m "slow"
```

## **📚 Documentation**

### **API Reference**

- [Confidence Scoring API](docs/confidence.md)
- [Logging Framework API](docs/logging.md)
- [Configuration Management API](docs/configuration.md)
- [Data Models API](docs/data_models.md)
- [Async Utilities API](docs/async_utils.md)
- [File Operations API](docs/file_ops.md)
- [Validation Utilities API](docs/validation.md)

## **🤝 Contributing**

### **Development Setup**

1. Fork the repository
1. Create a feature branch
1. Make your changes
1. Add tests for new functionality
1. Ensure all tests pass
1. Submit a pull request

### **Code Standards**

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add docstrings for all classes and methods
- Maintain test coverage above 90%

## **📈 Performance**

### **Benchmarks**

- **Confidence Calculation**: < 1ms for typical workloads
- **Logging Operations**: < 0.1ms per log entry
- **Configuration Loading**: < 10ms for complex configs
- **File Operations**: < 5ms for typical file operations

## **🔒 Security**

### **Security Features**

- **Input Validation**: Validate all inputs
- **Safe File Operations**: Prevent path traversal
- **Configuration Security**: Secure configuration handling
- **Logging Security**: Sanitize sensitive data

## **🚀 Roadmap**

### **Version 0.2.0 (Next Month)**

- [ ] **Enhanced Logging**: Structured logging with correlation IDs
- [ ] **Configuration Validation**: Schema-based configuration validation
- [ ] **Performance Monitoring**: Built-in performance metrics
- [ ] **Error Handling**: Advanced error handling and recovery

### **Version 0.3.0 (Next Quarter)**

- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Metrics Collection**: Comprehensive metrics and analytics
- [ ] **Distributed Tracing**: Support for distributed systems
- [ ] **Caching Layer**: Intelligent caching mechanisms

## **📞 Support**

### **Getting Help**

- **Issues**: [GitHub Issues](https://github.com/louspringer/clewcrew-common/issues)
- **Discussions**: [GitHub Discussions](https://github.com/louspringer/clewcrew-common/discussions)
- **Documentation**: [Project Wiki](https://github.com/louspringer/clewcrew-common/wiki)

### **Contact**

- **Author**: Lou Springer
- **Email**: <lou@example.com>
- **Project**: [clewcrew-common](https://github.com/louspringer/clewcrew-common)

## **📄 License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

______________________________________________________________________

**Status**: 🚀 **ACTIVE DEVELOPMENT**\
**Version**: 0.1.0\
**Python**: 3.9+\
**License**: MIT

**Chase down hallucinations, unravel tangled logic, keep the output on the level!** 🕵️✨
