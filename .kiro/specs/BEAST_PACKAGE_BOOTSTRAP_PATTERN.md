# Beast Mode Package Bootstrap Pattern

## 🎯 Purpose
**Reusable, standardized pattern for bootstrapping new Beast Mode PyPI packages with production-quality standards from day 1.**

This pattern was extracted from the `beast-agent` package creation and serves as the template for ALL future Beast Mode packages.

---

## 📦 Bootstrap Checklist

### Phase 1: Repository Structure
- [ ] Create repository directory
- [ ] Initialize git repository (`git init`)
- [ ] Create essential directories:
  ```bash
  mkdir -p src/{package_name} tests docs examples .github/workflows
  ```

### Phase 2: Package Configuration
- [ ] Create `pyproject.toml` with:
  - Project metadata (name, version, description)
  - Python version requirement (>=3.9)
  - Dependencies (core + dev)
  - Test configuration (pytest, coverage)
  - Tool configuration (black, mypy)
  - Build system (setuptools)
  
  **Template source**: `beast-agent/pyproject.toml`

### Phase 3: Source Code Structure
- [ ] Create `src/{package_name}/__init__.py` (package exports)
- [ ] Create core modules:
  - Main implementation files
  - Type definitions (`types.py` if needed)
  - Utilities (`decorators.py`, `utils.py` as needed)
- [ ] Add comprehensive docstrings
- [ ] Add type annotations
- [ ] Follow Black formatting

### Phase 4: Test Suite
- [ ] Create `tests/__init__.py`
- [ ] Create unit test files (`test_*.py`)
- [ ] Target 90%+ coverage
- [ ] Include:
  - Unit tests (70%+ coverage)
  - Integration tests (20%+ coverage)
  - Example usage tests

  **Template source**: `beast-agent/tests/`

### Phase 5: Quality & CI/CD
- [ ] Create `sonar-project.properties`:
  - Set `sonar.projectKey=nkllon_{package_name}`
  - Set `sonar.organization=nkllon`
  - Configure sources, tests, coverage paths
  
  **Template source**: `beast-agent/sonar-project.properties`

- [ ] Create `.github/workflows/sonarcloud.yml`:
  - Trigger on main/develop push and PRs
  - Run tests with coverage
  - SonarCloud scan
  
  **Template source**: `beast-agent/.github/workflows/sonarcloud.yml`

- [ ] Create `.gitignore` (Python standard)
  
  **Template source**: `beast-agent/.gitignore`

### Phase 6: Documentation
- [ ] Create `README.md` with:
  - [![PyPI version](https://img.shields.io/pypi/v/{package})](https://pypi.org/project/{package}/)
  - [![Python Versions](https://img.shields.io/pypi/pyversions/{package}.svg)](https://pypi.org/project/{package}/)
  - [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  - [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  - [![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=nkllon_{package}&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nkllon_{package})
  - Purpose statement
  - Quick start
  - Features
  - Installation
  - Examples
  - Documentation links
  
  **Template source**: `beast-agent/README.md`

- [ ] Create `LICENSE` (MIT)
  
  **Template source**: `beast-agent/LICENSE`

### Phase 7: Examples
- [ ] Create `examples/` directory
- [ ] Add simple example (`simple_{concept}.py`)
- [ ] Add advanced example if applicable
- [ ] Ensure examples are runnable
  
  **Template source**: `beast-agent/examples/simple_agent.py`

### Phase 8: Spec-Driven Development (cc-sdd)
- [ ] Create `.kiro/` directory structure:
  ```bash
  mkdir -p .kiro/specs .kiro/settings/templates/specs .kiro/settings/rules
  ```
- [ ] Create `.kiro/config.yaml`:
  - Project metadata (name, tier, category)
  - Specs directory configuration
  - Quality targets (coverage, maintainability)
  - Dependencies (upstream, downstream)
  
  **Template source**: `beast-agent/.kiro/config.yaml`

- [ ] Create `.kiro/README.md`:
  - cc-sdd workflow explanation
  - Available commands (/kiro:spec-init, etc.)
  - Example workflows
  - Quality gate integration
  
  **Template source**: `beast-agent/.kiro/README.md`

- [ ] Copy cc-sdd templates:
  - `settings/templates/specs/design.md`
  - `settings/templates/specs/requirements.md`
  - `settings/templates/specs/tasks.md`
  - `settings/templates/specs/init.json`
  
  **Source**: Copy from OpenFlow-Playground `.kiro/settings/templates/specs/`

- [ ] Copy cc-sdd rules:
  - `settings/rules/design-discovery-full.md`
  - `settings/rules/design-principles.md`
  - `settings/rules/ears-format.md`
  - `settings/rules/gap-analysis.md`
  - `settings/rules/tasks-generation.md`
  
  **Source**: Copy from OpenFlow-Playground `.kiro/settings/rules/`

- [ ] Create initial specs in `.kiro/specs/`:
  - `requirements.md` (package requirements)
  - `design.md` (architecture and design)
  - `tasks.md` (implementation tasks)
  - `QUALITY_STANDARDS_TEMPLATE.md` (from OpenFlow-Playground)
  - `SONARCLOUD_INTEGRATION_GUIDE.md` (from OpenFlow-Playground)

### Phase 9: AI Agent Guide
- [ ] Create `AGENT.md`:
  - Repository purpose and tier
  - **How to access specs** (cc-sdd clarification):
    - Method 1: Direct file reading (read_file tool)
    - Method 2: Cursor commands (/kiro:spec-init, etc.)
    - **Important**: cc-sdd uses Cursor commands, NOT an MCP server
  - Required reading order (specs first)
  - Architecture overview
  - Development workflow
  - Critical rules (DO NOT / ALWAYS)
  - Integration points (upstream/downstream)
  - Quality standards
  - Common tasks
  - Troubleshooting
  - Pre-commit checklist
  
  **Template source**: `beast-agent/AGENT.md`
  
  **Key Section**: "Using Spec-Driven Development (cc-sdd)" must clarify:
  - Specs are regular files accessed via read_file tool
  - /kiro: commands are Cursor IDE commands, not MCP
  - No MCP server required or expected

### Phase 10: Git & GitHub
- [ ] Commit bootstrap:
  ```bash
  git add -A
  git commit -m "feat: Bootstrap {package_name} package

  - Core implementation
  - Unit tests
  - SonarCloud integration
  - GitHub Actions workflow
  - Examples
  - Documentation

  Quality standards:
  - 90%+ test coverage target
  - Black formatting
  - Type annotations
  - Comprehensive docstrings

  Dependencies: {list_dependencies}

  Tier {tier_number} - {tier_description}"
  ```

- [ ] Create GitHub repository:
  ```bash
  gh repo create nkllon/{package_name} --public --source=. --remote=origin
  ```

- [ ] Push initial commit:
  ```bash
  git push -u origin main
  ```

---

## 🏗️ Package Structure Template

```
{package_name}/
├── .github/
│   └── workflows/
│       └── sonarcloud.yml          # CI/CD workflow
├── .kiro/                          # 🆕 Spec-driven development
│   ├── config.yaml                 # cc-sdd configuration
│   ├── README.md                   # cc-sdd workflow guide
│   ├── specs/
│   │   ├── requirements.md         # Package requirements
│   │   ├── design.md               # Architecture and design
│   │   ├── tasks.md                # Implementation tasks
│   │   ├── QUALITY_STANDARDS_TEMPLATE.md
│   │   └── SONARCLOUD_INTEGRATION_GUIDE.md
│   └── settings/
│       ├── templates/
│       │   └── specs/              # cc-sdd spec templates
│       │       ├── design.md
│       │       ├── requirements.md
│       │       ├── tasks.md
│       │       └── init.json
│       └── rules/                  # cc-sdd workflow rules
│           ├── design-discovery-full.md
│           ├── design-principles.md
│           ├── ears-format.md
│           ├── gap-analysis.md
│           └── tasks-generation.md
├── src/
│   └── {package_name}/
│       ├── __init__.py             # Package exports
│       ├── {main_module}.py        # Core implementation
│       ├── types.py                # Type definitions (optional)
│       └── {additional_modules}.py # Additional modules
├── tests/
│   ├── __init__.py
│   ├── test_{main_module}.py       # Unit tests
│   └── test_{additional}.py        # Additional tests
├── examples/
│   ├── simple_{concept}.py         # Simple example
│   └── advanced_{concept}.py       # Advanced example (optional)
├── docs/                           # Documentation (optional, created later)
├── .gitignore                      # Git ignore rules
├── AGENT.md                        # 🆕 AI agent working guide
├── LICENSE                         # MIT License
├── README.md                       # Package documentation
├── pyproject.toml                  # Package configuration
└── sonar-project.properties        # SonarCloud configuration
```

---

## 📊 Quality Standards (From beast-mailbox-core)

### Required Badges
```markdown
[![PyPI version](https://img.shields.io/pypi/v/{package}?label=PyPI&color=blue)](https://pypi.org/project/{package}/)
[![Python Versions](https://img.shields.io/pypi/pyversions/{package}.svg)](https://pypi.org/project/{package}/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nkllon_{package}&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nkllon_{package})
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=nkllon_{package}&metric=coverage)](https://sonarcloud.io/summary/new_code?id=nkllon_{package})
```

### Quality Metrics Targets
- **Coverage**: >= 90%
- **Maintainability Rating**: A
- **Security Rating**: A
- **Reliability Rating**: A
- **Duplications**: <= 3.0%
- **Code Smells**: Minimal
- **Bugs**: ZERO
- **Vulnerabilities**: ZERO

---

## 🔧 Automation Script Template

```bash
#!/bin/bash
# bootstrap_beast_package.sh
# Usage: ./bootstrap_beast_package.sh {package_name} {tier} {description}

PACKAGE_NAME=$1
TIER=$2
DESCRIPTION=$3

# Validation
if [ -z "$PACKAGE_NAME" ] || [ -z "$TIER" ] || [ -z "$DESCRIPTION" ]; then
  echo "Usage: $0 <package_name> <tier> <description>"
  exit 1
fi

# Create structure
mkdir -p $PACKAGE_NAME/{src/$PACKAGE_NAME,tests,examples,.github/workflows,docs}
mkdir -p $PACKAGE_NAME/.kiro/{specs,settings/templates/specs,settings/rules}
cd $PACKAGE_NAME

# Initialize git
git init

# Copy templates
cp ../templates/pyproject.toml.template ./pyproject.toml
cp ../templates/README.md.template ./README.md
cp ../templates/AGENT.md.template ./AGENT.md
cp ../templates/sonar-project.properties.template ./sonar-project.properties
cp ../templates/sonarcloud.yml.template ./.github/workflows/sonarcloud.yml
cp ../templates/LICENSE ./LICENSE
cp ../templates/.gitignore ./

# Copy cc-sdd templates
cp ../templates/.kiro/config.yaml.template ./.kiro/config.yaml
cp ../templates/.kiro/README.md.template ./.kiro/README.md
cp -r ../templates/.kiro/settings/templates/specs/* ./.kiro/settings/templates/specs/
cp -r ../templates/.kiro/settings/rules/* ./.kiro/settings/rules/

# Copy initial specs
cp ../templates/.kiro/specs/QUALITY_STANDARDS_TEMPLATE.md ./.kiro/specs/
cp ../templates/.kiro/specs/SONARCLOUD_INTEGRATION_GUIDE.md ./.kiro/specs/

# Replace placeholders
sed -i "s/{PACKAGE_NAME}/$PACKAGE_NAME/g" pyproject.toml
sed -i "s/{DESCRIPTION}/$DESCRIPTION/g" pyproject.toml
sed -i "s/{TIER}/$TIER/g" pyproject.toml
sed -i "s/{PACKAGE_NAME}/$PACKAGE_NAME/g" README.md
sed -i "s/{DESCRIPTION}/$DESCRIPTION/g" README.md
sed -i "s/{PACKAGE_NAME}/$PACKAGE_NAME/g" AGENT.md
sed -i "s/{TIER}/$TIER/g" AGENT.md
sed -i "s/{PACKAGE_NAME}/$PACKAGE_NAME/g" sonar-project.properties
sed -i "s/{PACKAGE_NAME}/$PACKAGE_NAME/g" .kiro/config.yaml
sed -i "s/{TIER}/$TIER/g" .kiro/config.yaml

# Create initial files
touch src/$PACKAGE_NAME/__init__.py
touch tests/__init__.py

echo "✅ Bootstrap complete for $PACKAGE_NAME (Tier $TIER)"
echo "📝 Next steps:"
echo "  1. Create specs: /kiro:spec-init $PACKAGE_NAME"
echo "  2. Write requirements: /kiro:spec-requirements $PACKAGE_NAME"
echo "  3. Design architecture: /kiro:spec-design $PACKAGE_NAME -y"
echo "  4. Break down tasks: /kiro:spec-tasks $PACKAGE_NAME -y"
echo "  5. Implement: /kiro:spec-impl $PACKAGE_NAME 1.1,1.2,1.3"
echo "  6. Test and validate"
echo "  7. Commit and push to GitHub"
```

---

## 📝 Template Files Location

All template files are based on `beast-agent` package:

### Core Configuration
- **pyproject.toml**: `beast-agent/pyproject.toml`
- **README.md**: `beast-agent/README.md`
- **AGENT.md**: `beast-agent/AGENT.md` 🆕
- **sonar-project.properties**: `beast-agent/sonar-project.properties`
- **sonarcloud.yml**: `beast-agent/.github/workflows/sonarcloud.yml`
- **.gitignore**: `beast-agent/.gitignore`
- **LICENSE**: `beast-agent/LICENSE`

### cc-sdd Integration 🆕
- **.kiro/config.yaml**: `beast-agent/.kiro/config.yaml`
- **.kiro/README.md**: `beast-agent/.kiro/README.md`
- **Spec templates**: `beast-agent/.kiro/settings/templates/specs/`
  - design.md, requirements.md, tasks.md, init.json
- **Workflow rules**: `beast-agent/.kiro/settings/rules/`
  - design-discovery-full.md, design-principles.md, ears-format.md, gap-analysis.md, tasks-generation.md
- **Initial specs**: `beast-agent/.kiro/specs/`
  - requirements.md, design.md, tasks.md
  - QUALITY_STANDARDS_TEMPLATE.md, SONARCLOUD_INTEGRATION_GUIDE.md

### Examples
- **Simple example**: `beast-agent/examples/simple_agent.py`

---

## 🎯 Package Tier Descriptions

### Tier 1: Foundation (No Dependencies)
- **beast-agent** - Base agent class
- **beast-redaction-client** - HMAC-protected classifier client
- **beast-observability** - Unified telemetry (minimal deps)

### Tier 2: Platform Adapters (Depend on Tier 1)
- **beast-adapter-aws** - AWS deployment helpers
- **beast-adapter-gcp** - GCP deployment helpers

### Tier 2.5: Agent Framework (Depends on Tier 1)
- **beast-agentic-framework** - Multi-agent coordination

### Tier 3: Specialized Integrations (Depend on Tier 2 + 2.5)
- **beast-nim-integration** - NVIDIA NIM client library
- **beast-adk-integration** - Google ADK integration

### Tier 4: Compliance/Security (Depend on Tier 1)
- **beast-compliance-toolkit** - Threat models, policy management

---

## 🚀 Usage Examples

### Example 1: Bootstrap beast-redaction-client
```bash
# Create package
./bootstrap_beast_package.sh beast-redaction-client 1 "HMAC-protected classifier client library"

# Implement core
cd beast-redaction-client
# ... implement src/beast_redaction_client/client.py
# ... implement tests/test_client.py
# ... add examples/simple_client.py

# Commit and push
git add -A
git commit -m "feat: Bootstrap beast-redaction-client package"
gh repo create nkllon/beast-redaction-client --public --source=. --remote=origin
git push -u origin main
```

### Example 2: Bootstrap beast-adapter-aws
```bash
# Create package
./bootstrap_beast_package.sh beast-adapter-aws 2 "AWS deployment helpers (EKS, SageMaker, ECR)"

# Implement core
cd beast-adapter-aws
# ... implement src/beast_adapter_aws/eks.py
# ... implement src/beast_adapter_aws/sagemaker.py
# ... implement tests/test_eks.py
# ... add examples/deploy_eks.py

# Commit and push
git add -A
git commit -m "feat: Bootstrap beast-adapter-aws package"
gh repo create nkllon/beast-adapter-aws --public --source=. --remote=origin
git push -u origin main
```

---

## ✅ Success Criteria

### Package is Ready When:
- [ ] All bootstrap files created
- [ ] Core implementation complete
- [ ] Tests passing (90%+ coverage)
- [ ] Linting passes (Black, Flake8, MyPy)
- [ ] Examples runnable
- [ ] Documentation complete
- [ ] Git committed
- [ ] GitHub repository created
- [ ] Initial push complete
- [ ] SonarCloud configured
- [ ] Quality Gate passing

---

## 🔗 References

- **beast-agent**: Reference implementation (Tier 1 foundation)
- **beast-mailbox-core**: Quality standards reference
- **QUALITY_STANDARDS_TEMPLATE.md**: Detailed quality metrics
- **SONARCLOUD_INTEGRATION_GUIDE.md**: SonarCloud setup guide
- **DEPENDENCY_MAP_AND_PACKAGES.md**: Package dependency graph

---

**This pattern ensures EVERY Beast Mode package starts with production-quality standards from day 1.**

**Use this checklist for ALL new packages. No exceptions.**

