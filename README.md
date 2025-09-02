# OpenFlow Playground

A comprehensive, model-driven development environment with security-first architecture, multi-agent testing, healthcare CDC compliance, and advanced round-trip engineering capabilities.

## 🚀 Features

### **🏆 Enhanced AST Round-Trip Engineering System** ⭐ **NEW**

- **Code Preservation**: Full method implementations preserved via enhanced AST extraction
- **7x Quality Improvement**: From 1,744 to 12,313 characters generated
- **MyPy Compliance**: 100% type safety with zero errors
- **Inheritance Preservation**: Complete class hierarchies maintained
- **Workflow Integration**: 45-node workflow analysis via ArtifactForge
- **Production Ready**: Complete round-trip engineering system

### **👻 Ghostbusters Multi-Agent System** ⭐ **NEW**

- **Delusion Detection**: 6 expert agents (Security, Code Quality, Test, Build, Architecture, Model)
- **Recovery Engines**: Automated fix strategies for syntax, indentation, imports, and type annotations
- **LangGraph Orchestration**: Advanced workflow management with async processing
- **Cloud Functions**: GCP deployment with ML integration and enterprise features
- **Real-time Dashboard**: Streamlit-based monitoring and analytics
- **Zero False Positives**: Comprehensive validation and recovery system

### **Model-Driven Development**

- **Project Model Registry**: Single source of truth for domain detection, tool selection, and requirements traceability
- **MDC Generator**: Python-based component for modeling and generating `.mdc` rule files
- **Deterministic Editing**: Enforced through specialized tools and validation
- **Model-Driven Testing**: Automatic test generation from implementation models (see [Model-Driven Testing Behavior](docs/MODEL_DRIVEN_TESTING_BEHAVIOR.md))
- **34 Domains**: Comprehensive domain architecture with tool ecosystem

### **Security-First Architecture**

- **Credential Management**: Environment variables and secure storage
- **HTTPS Enforcement**: SSL/TLS validation and redirect enforcement
- **Rate Limiting**: Redis-based rate limiting for API protection
- **CSRF Protection**: Token-based CSRF protection for web forms
- **Audit Logging**: Immutable audit trails for compliance
- **Bandit Integration**: Automated security scanning with Python API
- **1Password Integration**: Secure credential management

### **Multi-Agent Testing**

- **Blind Spot Detection**: AI agents identify overlooked issues
- **Diversity Testing**: Multiple perspectives for comprehensive coverage
- **Automated Validation**: Continuous testing and validation
- **100% Test Success**: All 144 tests passing with comprehensive coverage

### **Healthcare CDC Compliance**

- **HIPAA Compliance**: PHI detection and validation
- **Data Encryption**: Healthcare data encryption at rest and in transit
- **Access Control**: Role-based access control for clinical data
- **Audit Logging**: Immutable audit trails for regulatory compliance

### **Advanced Integrations**

- **Neo4j Integration**: Graph database for project modeling and analysis
- **PyPI Package Generation**: Automated package creation and publishing
- **Cloud Functions**: GCP deployment with ML integration
- **Vertex AI**: ML-powered insights and anomaly detection
- **Streamlit Applications**: Interactive dashboards and demos
- **ArtifactForge**: AST parsing and workflow analysis

### **Package Management**

- **UV Integration**: Modern Python package management with UV
- **Lock File Enforcement**: Reproducible builds with `uv.lock`
- **Security Scanning**: Automated vulnerability detection

## 🛠️ Quick Start

### **Installation**

```bash
# Clone the repository
git clone https://github.com/louspringer/OpenFlow-Playground.git
cd OpenFlow-Playground

# Install dependencies with UV
uv sync --all-extras

# Run comprehensive status check
make status

# Run all tests (100% success rate)
make test

# Test the Enhanced AST Round-Trip Engineering System
uv run python -c "from src.round_trip_engineering.core.round_trip_system import RoundTripSystem; system = RoundTripSystem(); result = system.analyze_and_generate_code('src/round_trip_engineering/core/round_trip_system.py'); print(f'✅ Enhanced AST System: {len(result[\"generated_code\"])} chars generated')"

# Test Ghostbusters Multi-Agent System
make ghostbusters

# Note: Model-driven testing automatically generates test files in tests/generated/
# To disable this behavior: export DISABLE_TEST_GENERATION=true
```

### **Development**

```bash
# Install development dependencies
uv sync --extra dev

# Run comprehensive quality checks
make lint
make format

# Run all tests with coverage
make test

# Run security scans
make security

# Run Ghostbusters delusion detection
make ghostbusters

# Generate activity models
make activity-models
```

### **Advanced Features**

```bash
# Run Neo4j integration
uv run python scripts/neo4j_poc.py

# Generate PyPI packages
uv run python scripts/pypi_package_generator.py

# Run comprehensive security scanning
uv run python scripts/comprehensive_security_scanner.py

# Test round-trip engineering
uv run python scripts/round_trip_cli.py
```

## 📁 Project Structure

```
OpenFlow-Playground/
├── src/                          # Source code
│   ├── streamlit/                # Streamlit applications and dashboards
│   ├── security_first/           # Security-first architecture components
│   ├── multi_agent_testing/      # Multi-agent testing framework
│   ├── ghostbusters/             # Ghostbusters multi-agent system ⭐
│   ├── ghostbusters_gcp/         # GCP Cloud Functions deployment
│   ├── mdc_generator/           # MDC file generator
│   ├── round_trip_engineering/   # Enhanced AST round-trip system ⭐
│   ├── artifact_forge/           # AST parsing and workflow analysis
│   ├── reflective_modules/       # RM-compliant architecture
│   ├── visualization/            # SVG visualization engine
│   ├── intelligent_linter_system.py # AI-powered linting system
│   ├── code_quality_system/      # Comprehensive quality management
│   ├── model_driven_testing/     # Model-driven test generation
│   ├── security_scanning/        # Security scanning and validation
│   ├── mcp_integration/          # MCP server integration
│   └── ontology/                 # Ontological modeling system
├── tests/                        # Test suite (100% success rate)
│   └── generated/               # Auto-generated test files (see Model-Driven Testing Behavior)
├── scripts/                      # Utility scripts and tools
│   ├── ghostbusters_cli.py      # Ghostbusters command-line interface
│   ├── neo4j_poc.py             # Neo4j integration proof of concept
│   ├── pypi_package_generator.py # PyPI package generation
│   ├── comprehensive_security_scanner.py # Security scanning
│   └── round_trip_cli.py        # Round-trip engineering CLI
├── config/                       # Configuration files
├── docs/                         # Comprehensive documentation
├── healthcare-cdc/              # Healthcare CDC compliance components
├── .cursor/                      # Cursor IDE configuration
│   ├── rules/                   # MDC rule files
│   └── plugins/                 # IDE plugins
├── makefiles/                    # Modular Makefile system
├── project_model_registry.json   # Model registry (34 domains)
├── pyproject.toml               # UV project configuration
├── uv.lock                      # UV lock file
└── Makefile                     # Build system
```

## 🔧 Model-Driven Architecture

### **Domain Detection**

The project uses a model-driven approach with `project_model_registry.json` as the single source of truth:

- **Domain Detection**: Automatic detection of file types and domains
- **Tool Selection**: Domain-specific linting, formatting, and validation
- **Requirements Traceability**: Link requirements to implementations

### **Rule Compliance**

- **MDC Linter**: Validates `.mdc` files for proper structure
- **Pre-commit Hooks**: Automated rule enforcement
- **IDE Integration**: Cursor IDE plugin for immediate feedback

## 🧪 Testing

### **Test Categories**

- **Python Tests**: Core functionality and security validation
- **Core Concept Tests**: Architecture and design pattern validation
- **Healthcare CDC Tests**: HIPAA compliance and PHI detection
- **Rule Compliance Tests**: MDC validation and rule enforcement

### **Running Tests**

```bash
# Run all tests
make test

# Run specific test categories
make test-python
make test-core-concepts
make test-healthcare-cdc
make test-rule-compliance
```

## 🔒 Security Features

### **Credential Management**

- Environment variables for all sensitive data
- AWS Secrets Manager integration
- No hardcoded credentials in source code

### **Data Protection**

- Encryption at rest and in transit
- PHI detection and validation
- Immutable audit logging

### **Access Control**

- Role-based access control (RBAC)
- JWT-based session management
- Multi-factor authentication support

## 📊 Healthcare CDC Features

### **HIPAA Compliance**

- PHI detection and validation
- Healthcare data encryption
- Access control and authentication
- Immutable audit logging

### **CDC Integration**

- Clinical data transformation
- CDC format compliance
- Data retention policies

## 🚀 Deployment

### **Streamlit Application**

```bash
# Run the Streamlit app
streamlit run src/streamlit/openflow_quickstart_app.py
```

### **Security Validation**

```bash
# Run security scans
make security

# Check for vulnerabilities
uv run safety check
```

## 📚 Documentation

- [Enhanced AST Achievement Summary](docs/ENHANCED_AST_ACHIEVEMENT_SUMMARY.md) - Complete round-trip engineering system 🏆
- [Round-Trip Engineering Refactoring Plan](docs/ROUND_TRIP_ENGINEERING_REFACTORING_PLAN.md) - PDCA cycles and implementation details
- [Model-Driven Testing Behavior](docs/MODEL_DRIVEN_TESTING_BEHAVIOR.md) - Understanding auto-generated test files
- **Architecture**: Model-driven development patterns
- **Security**: Security-first design principles
- **Testing**: Multi-agent testing framework
- **Healthcare**: CDC compliance and HIPAA requirements

## 🤝 Contributing

1. Follow the model-driven development approach
1. Ensure all tests pass
1. Follow security-first principles
1. Update documentation as needed

## 📄 License

[License information]

______________________________________________________________________

**Built with security-first principles and model-driven development.**
