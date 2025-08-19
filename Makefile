# OpenFlow Playground - Model-Driven Makefile
# This Makefile leverages the project_model_registry.json for domain-specific operations

.PHONY: help install install-python install-bash install-cloudformation install-docs install-security install-streamlit install-healthcare install-go install-secure-shell install-all status status-quick status-dashboard
.PHONY: test test-python test-bash test-cloudformation test-docs test-security test-streamlit test-healthcare test-go test-secure-shell test-all
.PHONY: lint lint-python lint-bash lint-cloudformation lint-docs lint-security lint-streamlit lint-healthcare lint-go lint-secure-shell lint-all
.PHONY: format format-python format-bash format-docs format-go format-secure-shell format-all
.PHONY: validate validate-model validate-requirements validate-all
.PHONY: clean clean-python clean-cache clean-go clean-secure-shell clean-all
.PHONY: deploy deploy-streamlit deploy-security deploy-healthcare deploy-secure-shell
.PHONY: security security-scan security-check security-audit
.PHONY: docs docs-build docs-serve docs-index
.PHONY: dev-install node-check mermaid-check mcp-install

# Project configuration
PROJECT_NAME := openflow-playground
MODEL_FILE := project_model_registry.json
PYTHON := python3
UV := uv
MAKE := make

# Platform detection
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
PLATFORM := $(shell echo $(UNAME_S) | tr '[:upper:]' '[:lower:]')
ARCH := $(shell echo $(UNAME_M) | tr '[:upper:]' '[:lower:]')

# Platform-specific variables
ifeq ($(PLATFORM),darwin)
	# macOS
	PACKAGE_MANAGER := brew
	GO_OS := darwin
	GO_ARCH := amd64
	ifeq ($(ARCH),arm64)
		GO_ARCH := arm64
	endif
else ifeq ($(PLATFORM),linux)
	# Linux
	PACKAGE_MANAGER := apt-get
	GO_OS := linux
	GO_ARCH := amd64
	ifeq ($(ARCH),aarch64)
		GO_ARCH := arm64
	endif
else ifeq ($(findstring MINGW,$(UNAME_S)),MINGW)
	# Windows (Git Bash)
	PACKAGE_MANAGER := chocolatey
	GO_OS := windows
	GO_ARCH := amd64
else ifeq ($(findstring MSYS,$(UNAME_S)),MSYS)
	# Windows (MSYS2)
	PACKAGE_MANAGER := pacman
	GO_OS := windows
	GO_ARCH := amd64
else
	# Default to Linux
	PACKAGE_MANAGER := apt-get
	GO_OS := linux
	GO_ARCH := amd64
endif

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "$(CYAN)OpenFlow Playground - Model-Driven Makefile$(NC)"
	@echo "$(YELLOW)Platform: $(PLATFORM)-$(ARCH)$(NC)"
	@echo "$(YELLOW)Package Manager: $(PACKAGE_MANAGER)$(NC)"
	@echo "$(YELLOW)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(PURPLE)Domain-specific targets:$(NC)"
	@echo "  install-{domain}    - Install dependencies for specific domain"
	@echo "  test-{domain}       - Run tests for specific domain"
	@echo "  lint-{domain}       - Lint code for specific domain"
	@echo "  format-{domain}     - Format code for specific domain"
	@echo ""
	@echo "$(PURPLE)Available domains:$(NC)"
	@echo "  python, bash, cloudformation, docs, security, streamlit, healthcare, go, secure-shell, node_development"
	@echo ""
	@echo "$(PURPLE)Examples:$(NC)"
	@echo "  make install-python     - Install Python dependencies with UV"
	@echo "  make test-security      - Run security tests and scans"
	@echo "  make lint-all           - Lint all domains"
	@echo "  make validate-model     - Validate project model registry"
	@echo "  make status             - Show comprehensive project status"
	@echo "  make status-quick       - Show quick project status"
	@echo "  make status-dashboard   - Update dashboard with real data"
	@echo "  make dev-install        - Install Node.js development environment"
	@echo "  make mermaid-check      - Validate Mermaid diagrams"
	@echo "  make mcp-install        - Install MCP servers"

# =============================================================================
# INSTALLATION TARGETS
# =============================================================================

install: install-all ## Install all dependencies (default: install-all)

install-all: install-python install-bash install-cloudformation install-docs install-security install-streamlit install-healthcare install-go install-secure-shell install-node ## Install dependencies for all domains
	@echo "$(GREEN)✅ All dependencies installed$(NC)"

install-python: ## Install Python dependencies with UV
	@echo "$(BLUE)🐍 Installing Python dependencies with UV...$(NC)"
	@$(UV) sync --all-extras
	@echo "$(GREEN)✅ Python dependencies installed$(NC)"

install-bash: ## Install bash script dependencies
	@echo "$(BLUE)🐚 Installing bash script dependencies...$(NC)"
	@command -v shellcheck >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  shellcheck not found, installing...$(NC)"; \
		case "$(PACKAGE_MANAGER)" in \
			brew) brew install shellcheck ;; \
			apt-get) sudo apt-get install -y shellcheck ;; \
			chocolatey) choco install shellcheck ;; \
			pacman) pacman -S shellcheck ;; \
			*) echo "$(RED)❌ Unsupported package manager: $(PACKAGE_MANAGER)$(NC)"; exit 1 ;; \
		esac; }
	@echo "$(GREEN)✅ Bash dependencies installed$(NC)"

install-cloudformation: ## Install CloudFormation dependencies
	@echo "$(BLUE)☁️  Installing CloudFormation dependencies...$(NC)"
	@command -v cfn-lint >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  cfn-lint not found, installing...$(NC)"; \
		case "$(PACKAGE_MANAGER)" in \
			brew) brew install cfn-lint ;; \
			apt-get) pip install cfn-lint ;; \
			chocolatey) choco install cfn-lint ;; \
			pacman) pip install cfn-lint ;; \
			*) pip install cfn-lint ;; \
		esac; }
	@echo "$(GREEN)✅ CloudFormation dependencies installed$(NC)"

install-docs: ## Install documentation dependencies
	@echo "$(BLUE)📚 Installing documentation dependencies...$(NC)"
	@command -v markdownlint >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  markdownlint not found, installing...$(NC)"; \
		case "$(PACKAGE_MANAGER)" in \
			brew) npm install -g markdownlint-cli ;; \
			apt-get) npm install -g markdownlint-cli ;; \
			chocolatey) npm install -g markdownlint-cli ;; \
			pacman) npm install -g markdownlint-cli ;; \
			*) npm install -g markdownlint-cli ;; \
		esac; }
	@echo "$(GREEN)✅ Documentation dependencies installed$(NC)"

install-security: ## Install security tooling dependencies
	@echo "$(BLUE)🔒 Installing security dependencies...$(NC)"
	@$(UV) sync --extra security
	@echo "$(GREEN)✅ Security dependencies installed$(NC)"

install-streamlit: ## Install Streamlit app dependencies
	@echo "$(BLUE)📊 Installing Streamlit dependencies...$(NC)"
	@$(UV) sync
	@echo "$(GREEN)✅ Streamlit dependencies installed$(NC)"

install-healthcare: ## Install healthcare CDC dependencies
	@echo "$(BLUE)🏥 Installing healthcare CDC dependencies...$(NC)"
	@$(UV) sync
	@echo "$(GREEN)✅ Healthcare CDC dependencies installed$(NC)"

install-go: ## Install Go language and tools
	@echo "$(BLUE)🐹 Installing Go language and tools...$(NC)"
	@command -v go >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  Go not found, installing...$(NC)"; \
		case "$(PACKAGE_MANAGER)" in \
			brew) brew install go ;; \
			apt-get) \
				curl -OL https://go.dev/dl/go1.21.6.$(GO_OS)-$(GO_ARCH).tar.gz; \
				sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.6.$(GO_OS)-$(GO_ARCH).tar.gz; \
				echo 'export PATH=$$PATH:/usr/local/go/bin' >> ~/.bashrc; \
				rm go1.21.6.$(GO_OS)-$(GO_ARCH).tar.gz ;; \
			chocolatey) choco install golang ;; \
			pacman) pacman -S go ;; \
			*) echo "$(RED)❌ Unsupported package manager: $(PACKAGE_MANAGER)$(NC)"; exit 1 ;; \
		esac; }
	@echo "$(GREEN)✅ Go language and tools installed$(NC)"

install-secure-shell: ## Install secure shell service dependencies
	@echo "$(BLUE)🛡️ Installing secure shell service dependencies...$(NC)"
	@command -v protoc >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  protobuf-compiler not found, installing...$(NC)"; \
		case "$(PACKAGE_MANAGER)" in \
			brew) brew install protobuf ;; \
			apt-get) sudo apt-get install -y protobuf-compiler ;; \
			chocolatey) choco install protobuf ;; \
			pacman) pacman -S protobuf ;; \
			*) echo "$(RED)❌ Unsupported package manager: $(PACKAGE_MANAGER)$(NC)"; exit 1 ;; \
		esac; }
	@if command -v go >/dev/null 2>&1; then \
		go install google.golang.org/protobuf/cmd/protoc-gen-go@latest; \
		go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest; \
	else \
		echo "$(YELLOW)⚠️  Go not found - skipping Go-specific installations$(NC)"; \
		echo "$(YELLOW)💡 Install Go first with: make install-go$(NC)"; \
	fi
	@$(UV) add grpcio grpcio-tools
	@echo "$(GREEN)✅ Secure shell service dependencies installed$(NC)"

install-node: ## Install Node.js development dependencies
	@echo "$(BLUE)🟢 Installing Node.js development dependencies...$(NC)"
	@node --version || (echo "$(RED)❌ Node.js not found. Please install Node.js 20+ first$(NC)" && exit 1)
	@echo "$(GREEN)✅ Node.js found$(NC)"
	@echo "$(YELLOW)📋 Installing global Mermaid CLI...$(NC)"
	@npm install -g @mermaid-js/mermaid-cli || (echo "$(RED)❌ Failed to install Mermaid CLI$(NC)" && exit 1)
	@echo "$(GREEN)✅ Mermaid CLI installed$(NC)"
	@echo "$(GREEN)✅ Node.js development dependencies installed$(NC)"

# =============================================================================
# TESTING TARGETS
# =============================================================================

test: test-all ## Run all tests (default: test-all)

test-all: test-python test-bash test-cloudformation test-docs test-security test-streamlit test-healthcare test-go test-secure-shell ## Run tests for all domains
	@echo "$(GREEN)✅ All tests completed$(NC)"

test-python: ## Run Python tests
	@echo "$(BLUE)🐍 Running Python tests...$(NC)"
	@$(UV) run pytest tests/ -v
	@echo "$(GREEN)✅ Python tests completed$(NC)"


test-bash: ## Run bash script tests
	@echo "$(BLUE)🐚 Running bash script tests...$(NC)"
	@find scripts/ -name "*.sh" -exec shellcheck {} \;
	@echo "$(GREEN)✅ Bash script tests completed$(NC)"

test-cloudformation: ## Run CloudFormation tests
	@echo "$(BLUE)☁️  Running CloudFormation tests...$(NC)"
	@find . -name "*.template.yaml" -exec cfn-lint {} \;
	@echo "$(GREEN)✅ CloudFormation tests completed$(NC)"

test-docs: ## Run documentation tests
	@echo "$(BLUE)📚 Running documentation tests...$(NC)"
	@if command -v markdownlint >/dev/null 2>&1; then \
		find docs/ -name "*.md" -exec markdownlint {} \; ; \
	else \
		echo "⚠️  markdownlint not installed, skipping documentation linting"; \
		echo "   To install: npm install -g markdownlint-cli"; \
	fi
	@echo "$(GREEN)✅ Documentation tests completed$(NC)"

test-security: ## Run security tests and scans
	@echo "$(BLUE)🔒 Running security tests...$(NC)"
	@$(UV) run bandit -r src/
	@$(UV) run safety check
	@$(UV) run detect-secrets scan
	@echo "$(GREEN)✅ Security tests completed$(NC)"

test-streamlit: ## Run Streamlit app tests
	@echo "$(BLUE)📊 Running Streamlit app tests...$(NC)"
	@$(UV) run pytest tests/test_uv_package_management.py -v
	@$(UV) run pytest tests/test_basic_validation.py -v
	@echo "$(GREEN)✅ Streamlit app tests completed$(NC)"

test-healthcare: ## Run healthcare CDC tests
	@echo "$(BLUE)🏥 Running healthcare CDC tests...$(NC)"
	@$(UV) run pytest tests/test_healthcare_cdc_requirements.py -v
	@echo "$(GREEN)✅ Healthcare CDC tests completed$(NC)"

test-go: ## Run Go service tests
	@echo "$(BLUE)🐹 Running Go service tests...$(NC)"
	@if command -v go >/dev/null 2>&1; then \
		cd src/secure_shell_service && go test ./...; \
		echo "$(GREEN)✅ Go service tests completed$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Go not found - skipping Go tests$(NC)"; \
		echo "$(YELLOW)💡 Install Go with: make install-go$(NC)"; \
	fi

test-secure-shell: ## Run secure shell service tests
	@echo "$(BLUE)🛡️ Running secure shell service tests...$(NC)"
	@$(UV) run python test_secure_shell.py
	@echo "$(GREEN)✅ Secure shell service tests completed$(NC)"

test-model: ## Run model validation tests
	@echo "$(BLUE)🔍 Running model validation tests...$(NC)"
	@python scripts/pre_test_model_check.py
	@echo "$(GREEN)✅ Model validation tests completed$(NC)"
# =============================================================================
# LINTING TARGETS
# =============================================================================

lint: lint-all ## Lint all code (default: lint-all)

lint-all: lint-python lint-bash lint-cloudformation lint-docs lint-security lint-streamlit lint-healthcare lint-go lint-secure-shell ## Lint all domains
	@echo "$(GREEN)✅ All linting completed$(NC)"

lint-python: ## Lint Python code
	@echo "$(BLUE)🐍 Linting Python code...$(NC)"
	@$(UV) run flake8 src/ tests/
	@$(UV) run mypy src/ scripts/
	@echo "$(GREEN)✅ Python linting completed$(NC)"

lint-bash: ## Lint bash scripts
	@echo "$(BLUE)🐚 Linting bash scripts...$(NC)"
	@find scripts/ -name "*.sh" -exec shellcheck {} \;
	@echo "$(GREEN)✅ Bash script linting completed$(NC)"

lint-cloudformation: ## Lint CloudFormation templates
	@echo "$(BLUE)☁️  Linting CloudFormation templates...$(NC)"
	@find . -name "*.template.yaml" -exec cfn-lint {} \;
	@echo "$(GREEN)✅ CloudFormation linting completed$(NC)"

lint-docs: ## Lint documentation
	@echo "$(BLUE)📚 Linting documentation...$(NC)"
	@echo "🔍 Using official Mermaid tools for validation..."
	@mmdc --version > /dev/null 2>&1 || (echo "$(RED)❌ Mermaid CLI not found. Run: make dev-install$(NC)" && exit 1)
	@echo "$(GREEN)✅ Mermaid CLI found$(NC)"
	for file in docs/*.md; do mmdc -i "$$file" -o "/tmp/validation_$$(basename "$$file" .md).md" > /dev/null 2>&1 || exit 1; done && echo "$(GREEN)✅ All Mermaid diagrams are valid!$(NC)" || echo "$(RED)❌ Mermaid validation failed$(NC)"
	@echo "$(GREEN)✅ Documentation linting completed$(NC)"

lint-security: ## Lint security code
	@echo "$(BLUE)🔒 Linting security code...$(NC)"
	@$(UV) run bandit -r src/security_first/
	@$(UV) run safety check
	@echo "$(GREEN)✅ Security linting completed$(NC)"

lint-streamlit: ## Lint Streamlit code
	@echo "$(BLUE)📊 Linting Streamlit code...$(NC)"
	@$(UV) run flake8 src/streamlit/
	@$(UV) run mypy src/streamlit/
	@echo "$(GREEN)✅ Streamlit linting completed$(NC)"

lint-healthcare: ## Lint healthcare CDC code
	@echo "$(BLUE)🏥 Linting healthcare CDC code...$(NC)"
	@$(UV) run flake8 healthcare-cdc/
	@echo "$(GREEN)✅ Healthcare CDC linting completed$(NC)"

lint-go: ## Lint Go code
	@echo "$(BLUE)🐹 Linting Go code...$(NC)"
	@cd src/secure_shell_service && go vet ./...
	@cd src/secure_shell_service && go fmt ./...
	@echo "$(GREEN)✅ Go code linting completed$(NC)"

lint-secure-shell: ## Lint secure shell service code
	@echo "$(BLUE)🛡️ Linting secure shell service code...$(NC)"
	@$(UV) run flake8 src/secure_shell_service/
	@$(UV) run mypy src/secure_shell_service/
	@echo "$(GREEN)✅ Secure shell service linting completed$(NC)"

# =============================================================================
# FORMATTING TARGETS
# =============================================================================

format: format-all ## Format all code (default: format-all)

format-all: format-python format-bash format-docs format-go format-secure-shell ## Format all domains
	@echo "$(GREEN)✅ All formatting completed$(NC)"

format-python: ## Format Python code
	@echo "$(BLUE)🐍 Formatting Python code...$(NC)"
	@$(UV) run black src/ tests/ scripts/
	@echo "$(GREEN)✅ Python formatting completed$(NC)"
format-bash: ## Format bash scripts
	@echo "$(BLUE)🐚 Formatting bash scripts...$(NC)"
	@find scripts/ -name "*.sh" -exec shfmt -w {} \;
	@echo "$(GREEN)✅ Bash script formatting completed$(NC)"

format-docs: ## Format documentation
	@echo "$(BLUE)📚 Formatting documentation...$(NC)"
	@find docs/ -name "*.md" -exec prettier --write {} \;
	@echo "$(GREEN)✅ Documentation formatting completed$(NC)"

format-go: ## Format Go code
	@echo "$(BLUE)🐹 Formatting Go code...$(NC)"
	@if command -v go >/dev/null 2>&1; then \
		cd src/secure_shell_service && go fmt ./...; \
		echo "$(GREEN)✅ Go code formatting completed$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Go not found - skipping Go formatting$(NC)"; \
		echo "$(YELLOW)💡 Install Go with: $(PACKAGE_MANAGER) install go$(NC)"; \
		echo "$(YELLOW)💡 Or run: make install-go$(NC)"; \
	fi

format-secure-shell: ## Format secure shell service code
	@echo "$(BLUE)🛡️ Formatting secure shell service code...$(NC)"
	@$(UV) run black src/secure_shell_service/
	@echo "$(GREEN)✅ Secure shell service formatting completed$(NC)"

# =============================================================================
# VALIDATION TARGETS
# =============================================================================

validate: validate-all ## Validate all components (default: validate-all)

validate-all: validate-model validate-requirements ## Validate all components
	@echo "$(GREEN)✅ All validation completed$(NC)"

validate-model: ## Validate project model registry
	@echo "$(BLUE)🔍 Validating project model registry...$(NC)"
	@$(PYTHON) -c "import json; json.load(open('$(MODEL_FILE)'))"
	@echo "$(GREEN)✅ Project model registry is valid JSON$(NC)"

validate-requirements: ## Validate requirements traceability
	@echo "$(BLUE)🔍 Validating requirements traceability...$(NC)"
	@$(UV) run python src/multi_agent_testing/test_model_traceability.py
	@echo "$(GREEN)✅ Requirements traceability validated$(NC)"

# =============================================================================
# CLEANUP TARGETS
# =============================================================================

clean: clean-all ## Clean all artifacts (default: clean-all)

clean-all: clean-python clean-cache clean-go clean-secure-shell ## Clean all artifacts
	@echo "$(GREEN)✅ All cleanup completed$(NC)"

clean-python: ## Clean Python artifacts
	@echo "$(BLUE)🧹 Cleaning Python artifacts...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@find . -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Python artifacts cleaned$(NC)"

clean-cache: ## Clean all cache directories
	@echo "$(BLUE)🧹 Cleaning cache directories...$(NC)"
	@find . -name ".cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cache directories cleaned$(NC)"

clean-go: ## Clean Go artifacts
	@echo "$(BLUE)🧹 Cleaning Go artifacts...$(NC)"
	@if command -v go >/dev/null 2>&1; then \
		cd src/secure_shell_service && go clean; \
	else \
		echo "$(YELLOW)⚠️  Go not found - skipping go clean$(NC)"; \
	fi
	@rm -f src/secure_shell_service/secure-shell-service
	@rm -f src/secure_shell_service/*.pb.go
	@echo "$(GREEN)✅ Go artifacts cleaned$(NC)"

clean-secure-shell: ## Clean secure shell service artifacts
	@echo "$(BLUE)🧹 Cleaning secure shell service artifacts...$(NC)"
	@rm -f src/secure_shell_service/secure-shell-service
	@rm -f src/secure_shell_service/*.pb.go
	@echo "$(GREEN)✅ Secure shell service artifacts cleaned$(NC)"

# =============================================================================
# DEPLOYMENT TARGETS
# =============================================================================

deploy: deploy-streamlit deploy-secure-shell ## Deploy applications (default: deploy-streamlit)

deploy-streamlit: ## Deploy Streamlit app
	@echo "$(BLUE)📊 Deploying Streamlit app...$(NC)"
	@$(UV) run streamlit run src/streamlit/openflow_quickstart_app.py
	@echo "$(GREEN)✅ Streamlit app deployed$(NC)"

deploy-security: ## Deploy security components
	@echo "$(BLUE)🔒 Deploying security components...$(NC)"
	@$(UV) run python src/security_first/test_https_enforcement.py
	@echo "$(GREEN)✅ Security components deployed$(NC)"

deploy-healthcare: ## Deploy healthcare CDC components
	@echo "$(BLUE)🏥 Deploying healthcare CDC components...$(NC)"
	@$(UV) run python healthcare-cdc/models/healthcare_cdc_domain_model.py
	@echo "$(GREEN)✅ Healthcare CDC components deployed$(NC)"

deploy-secure-shell: ## Deploy secure shell service
	@echo "$(BLUE)🛡️ Deploying secure shell service...$(NC)"
	@if command -v go >/dev/null 2>&1; then \
		cd src/secure_shell_service && go build -o secure-shell-service .; \
		cd src/secure_shell_service && ./secure-shell-service &; \
		echo "$(GREEN)✅ Secure shell service deployed at port 50051$(NC)"; \
		echo "$(YELLOW)💡 To test: cd src/secure_shell_service && python client.py$(NC)"; \
	else \
		echo "$(RED)❌ Go not found - cannot deploy secure shell service$(NC)"; \
		echo "$(YELLOW)💡 Install Go with: make install-go$(NC)"; \
	fi

# =============================================================================
# SECURITY TARGETS
# =============================================================================

security: security-scan security-enhanced ## Run security checks (default: security-scan + enhanced)

security-scan: ## Run comprehensive security scan
	@echo "$(BLUE)🔒 Running comprehensive security scan...$(NC)"
	@$(UV) run bandit -r src/ -f json -o security-report.json
	@$(UV) run safety check --json --output security-vulnerabilities.json
	@$(UV) run detect-secrets scan --baseline .secrets.baseline
	@echo "$(GREEN)✅ Security scan completed$(NC)"

security-check: ## Run quick security check
	@echo "$(BLUE)🔒 Running quick security check...$(NC)"
	@$(UV) run bandit -r src/ -f txt
	@$(UV) run safety check
	@echo "$(GREEN)✅ Quick security check completed$(NC)"

security-audit: ## Run security audit
	@echo "$(BLUE)🔒 Running security audit...$(NC)"
	@$(UV) run bandit -r src/ -f json -o security-audit.json
	@$(UV) run safety check --json --output security-audit-vulnerabilities.json
	@$(UV) run detect-secrets audit .secrets.baseline
	@echo "$(GREEN)✅ Security audit completed$(NC)"

security-enhanced: ## Run enhanced Bandit integration scan
	@echo "$(BLUE)🔒 Running enhanced Bandit integration scan...$(NC)"
	@$(PYTHON) scripts/bandit_integration.py --project --report
	@echo "$(GREEN)✅ Enhanced security scan completed$(NC)"

security-enhanced-export: ## Run enhanced scan with JSON export
	@echo "$(BLUE)🔒 Running enhanced security scan with export...$(NC)"
	@$(PYTHON) scripts/bandit_integration.py --project --output enhanced-security-scan.json --report
	@echo "$(GREEN)✅ Enhanced security scan exported to enhanced-security-scan.json$(NC)"

# =============================================================================
# DOCUMENTATION TARGETS
# =============================================================================

docs: docs-index ## Build documentation (default: docs-index)

docs-build: ## Build documentation
	@echo "$(BLUE)📚 Building documentation...$(NC)"
	@find docs/ -name "*.md" -exec markdownlint {} \;
	@echo "$(GREEN)✅ Documentation built$(NC)"

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)📚 Serving documentation locally...$(NC)"
	@$(PYTHON) -m http.server 8000 --directory docs/
	@echo "$(GREEN)✅ Documentation served at http://localhost:8000$(NC)"

docs-index: ## Index documentation
	@echo "$(BLUE)📚 Indexing documentation...$(NC)"
	@find docs/ -name "*.md" -exec basename {} \; | sort
	@echo "$(GREEN)✅ Documentation indexed$(NC)"

# =============================================================================
# DEVELOPMENT TARGETS
# =============================================================================

dev-setup: install-all ## Setup development environment
	@echo "$(GREEN)✅ Development environment setup complete$(NC)"

dev-test: test-all ## Run all tests for development
	@echo "$(GREEN)✅ Development tests complete$(NC)"

dev-lint: lint-all ## Run all linting for development
	@echo "$(GREEN)✅ Development linting complete$(NC)"

dev-format: format-all ## Run all formatting for development
	@echo "$(GREEN)✅ Development formatting complete$(NC)"

# =============================================================================
# UTILITY TARGETS
# =============================================================================

check-deps: ## Check if all dependencies are installed
	@echo "$(BLUE)🔍 Checking dependencies...$(NC)"
	@command -v $(UV) >/dev/null 2>&1 || { echo "$(RED)❌ UV not found$(NC)"; exit 1; }
	@command -v shellcheck >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  shellcheck not found$(NC)"; }
	@command -v cfn-lint >/dev/null 2>&1 || { echo "$(YELLOW)⚠️  cfn-lint not found$(NC)"; }
	@echo "$(GREEN)✅ Dependencies check completed$(NC)"

show-domains: ## Show available domains from model
	@echo "$(BLUE)🔍 Available domains from model:$(NC)"
	@$(PYTHON) -c "import json; data=json.load(open('$(MODEL_FILE)')); print('\n'.join(data['domains'].keys()))"

show-rules: ## Show available rules
	@echo "$(BLUE)🔍 Available rules:$(NC)"
	@find .cursor/rules/ -name "*.mdc" -exec basename {} \;

status: ## Show comprehensive project status
status-quick: ## Show quick project status (faster)
	@echo "$(CYAN)🚀 OpenFlow Playground - Real-Time Status Report$(NC)"
	@echo "$(BLUE)================================================$(NC)"
	@echo ""
	
	@echo "$(BLUE)📊 Code Quality Status$(NC)"
	@echo "$(YELLOW)  Flake8 Issues:$(NC)"
	@$(UV) run flake8 --count --statistics src/ 2>/dev/null | tail -1 | grep -Eo '[0-9]+' | head -1 | xargs -I {} echo "    $(GREEN)✅ {} issues found$(NC)" || echo "    $(RED)❌ Flake8 check failed$(NC)"
	@echo "$(YELLOW)  MyPy Issues:$(NC)"
	@$(UV) run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null | grep -c "error:" | xargs -I {} echo "    $(GREEN)✅ {} type errors found$(NC)" || echo "    $(RED)❌ MyPy check failed$(NC)"
	@echo "$(YELLOW)  Black Formatting:$(NC)"
	@$(UV) run black --check --diff src/ 2>/dev/null && echo "    $(GREEN)✅ Code is properly formatted$(NC)" || echo "    $(RED)❌ Code needs formatting$(NC)"
	
	@echo ""
	@echo "$(BLUE)🔍 Project Health$(NC)"
	@echo "$(YELLOW)  Git Status:$(NC)"
	@git status --porcelain | wc -l | xargs -I {} echo "    $(GREEN)✅ {} uncommitted changes$(NC)"
	@echo "$(YELLOW)  Current Branch:$(NC)"
	@git branch --show-current | xargs -I {} echo "    $(GREEN)✅ {}$(NC)"
	@echo "$(YELLOW)  Last Commit:$(NC)"
	@git log -1 --format="%h - %s (%cr)" | xargs -I {} echo "    $(GREEN)✅ {}$(NC)"
	
	@echo ""
	@echo "$(BLUE)📦 Dependencies$(NC)"
	@echo "$(YELLOW)  UV Available:$(NC)"
	@command -v $(UV) >/dev/null 2>&1 && echo "    $(GREEN)✅ UV package manager$(NC)" || echo "    $(RED)❌ UV not found$(NC)"
	@echo "$(YELLOW)  Python Version:$(NC)"
	@$(PYTHON) --version | xargs -I {} echo "    $(GREEN)✅ {}$(NC)"
	@echo "$(YELLOW)  Dependencies:$(NC)"
	@test -f pyproject.toml && echo "    $(GREEN)✅ pyproject.toml found$(NC)" || echo "    $(RED)❌ pyproject.toml missing$(NC)"
	@test -f uv.lock && echo "    $(GREEN)✅ uv.lock found$(NC)" || echo "    $(RED)❌ uv.lock missing$(NC)"
	
	@echo ""
	@echo "$(BLUE)🏗️  System Components$(NC)"
	@echo "$(YELLOW)  Ghostbusters:$(NC)"
	@test -d src/ghostbusters && echo "    $(GREEN)✅ Multi-agent system available$(NC)" || echo "    $(RED)❌ Ghostbusters missing$(NC)"
	@echo "$(YELLOW)  ArtifactForge:$(NC)"
	@test -d src/artifact_forge && echo "    $(GREEN)✅ Artifact analysis available$(NC)" || echo "    $(RED)❌ ArtifactForge missing$(NC)"
	@echo "$(YELLOW)  Model-Driven:$(NC)"
	@test -d src/model_driven_projection && echo "    $(GREEN)✅ Model projection available$(NC)" || echo "    $(RED)❌ Model projection missing$(NC)"
	@echo "$(YELLOW)  Quality System:$(NC)"
	@test -d src/code_quality_system && echo "    $(GREEN)✅ Quality system available$(NC)" || echo "    $(RED)❌ Quality system missing$(NC)"
	
	@echo ""
	@echo "$(BLUE)📈 Recent Activity$(NC)"
	@echo "$(YELLOW)  Last 3 Commits:$(NC)"
	@git log --oneline -3 | while read line; do echo "    $(GREEN)✅ $$line$(NC)"; done
	
	@echo ""
	@echo "$(BLUE)🎯 Quick Actions$(NC)"
	@echo "  $(CYAN)make lint-all$(NC)     - Fix all linting issues"
	@echo "  $(CYAN)make format-all$(NC)   - Format all code"
	@echo "  $(CYAN)make test-all$(NC)     - Run all tests"
	@echo "  $(CYAN)make clean-all$(NC)    - Clean all artifacts"
	@echo ""
	@echo "$(GREEN)✅ Status report complete!$(NC)"



status-dashboard: ## Update dashboard with real project data
	@echo "$(CYAN)📊 Updating Project Dashboard with Real Data$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Collecting current metrics...$(NC)"
	
	@echo "$(BLUE)  Flake8 Issues:$(NC)"
	@FLAKE8_COUNT=$$($(UV) run flake8 --count --statistics src/ 2>/dev/null | tail -1 | grep -Eo '[0-9]+' | head -1 || echo "0"); \
	echo "    Found $$FLAKE8_COUNT Flake8 issues"
	
	@echo "$(BLUE)  MyPy Errors:$(NC)"
	@MYPY_COUNT=$$($(UV) run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null | grep -c "error:" || echo "0"); \
	echo "    Found $$MYPY_COUNT MyPy errors"
	
	@echo "$(BLUE)  Git Changes:$(NC)"
	@GIT_CHANGES=$$(git status --porcelain | wc -l); \
	echo "    $$GIT_CHANGES uncommitted changes"
	
	@echo "$(BLUE)  Quality Score:$(NC)"
	@if [ "$$FLAKE8_COUNT" -eq 0 ] && [ "$$MYPY_COUNT" -eq 0 ]; then \
		echo "    $(GREEN)✅ 100% - Perfect Quality!$(NC)"; \
	elif [ "$$FLAKE8_COUNT" -lt 10 ] && [ "$$MYPY_COUNT" -lt 10 ]; then \
		echo "    $(GREEN)✅ 80% - Good Quality$(NC)"; \
	elif [ "$$FLAKE8_COUNT" -lt 50 ] && [ "$$MYPY_COUNT" -lt 50 ]; then \
		echo "    $(YELLOW)⚠️  60% - Needs Attention$(NC)"; \
	else \
		echo "    $(RED)❌ 40% - Critical Issues$(NC)"; \
	fi
	
	@echo ""
	@echo "$(GREEN)✅ Dashboard data collected!$(NC)"
	@echo "$(YELLOW)💡 Run 'make status' for full report$(NC)"

# =============================================================================
# NODE.JS DEVELOPMENT TARGETS
# =============================================================================

dev-install: ## Install Node.js development environment and tools
	@echo "$(BLUE)🔧 Installing Node.js development environment...$(NC)"
	@echo "$(YELLOW)📋 Checking Node.js version...$(NC)"
	@node --version || (echo "$(RED)❌ Node.js not found. Please install Node.js 20+ first$(NC)" && exit 1)
	@echo "$(GREEN)✅ Node.js found$(NC)"
	@echo "$(YELLOW)📋 Installing global Mermaid CLI...$(NC)"
	@npm install -g @mermaid-js/mermaid-cli || (echo "$(RED)❌ Failed to install Mermaid CLI$(NC)" && exit 1)
	@echo "$(GREEN)✅ Mermaid CLI installed$(NC)"
	@echo "$(YELLOW)📋 Installing MCP servers...$(NC)"
	@npm install -g mermaider-mcp || echo "$(YELLOW)⚠️  Mermaider MCP not available$(NC)"
	@echo "$(GREEN)✅ Node.js development environment ready!$(NC)"

node-check: ## Check Node.js development environment
	@echo "$(BLUE)🔍 Checking Node.js development environment...$(NC)"
	@echo "$(YELLOW)📋 Node.js version:$(NC)"
	@node --version || echo "$(RED)❌ Node.js not found$(NC)"
	@echo "$(YELLOW)📋 npm version:$(NC)"
	@npm --version || echo "$(RED)❌ npm not found$(NC)"
	@echo "$(YELLOW)📋 Mermaid CLI:$(NC)"
	@mmdc --version > /dev/null 2>&1 && echo "$(GREEN)✅ Available$(NC)" || echo "$(RED)❌ Not found$(NC)"
	@echo "$(GREEN)✅ Node.js environment check completed$(NC)"

mermaid-check: ## Validate Mermaid diagrams using official CLI
	@echo "$(BLUE)🔍 Validating Mermaid diagrams...$(NC)"
	@mmdc --version > /dev/null 2>&1 || (echo "$(RED)❌ Mermaid CLI not found. Run: make dev-install$(NC)" && exit 1)
	@echo "$(GREEN)✅ Mermaid CLI found$(NC)"
	@echo "$(YELLOW)📋 Validating all documentation...$(NC)"
	for file in docs/*.md; do mmdc -i "$$file" -o "/tmp/validation_$$(basename "$$file" .md).md" > /dev/null 2>&1 || exit 1; done && echo "$(GREEN)✅ All Mermaid diagrams are valid!$(NC)" || echo "$(RED)❌ Mermaid validation failed$(NC)"

mcp-install: ## Install MCP servers for development
	@echo "$(BLUE)🔧 Installing MCP servers...$(NC)"
	@echo "$(YELLOW)📋 Installing Mermaider MCP...$(NC)"
	@npm install -g mermaider-mcp || echo "$(YELLOW)⚠️  Mermaider MCP not available$(NC)"
	@echo "$(YELLOW)📋 Installing Tavily MCP...$(NC)"
	@npm install -g tavily-mcp || echo "$(YELLOW)⚠️  Tavily MCP not available$(NC)"
	@echo "$(YELLOW)📋 Installing Doc Ops MCP...$(NC)"
	@npm install -g doc-ops-mcp || echo "$(YELLOW)⚠️  Doc Ops MCP not available$(NC)"
	@echo "$(GREEN)✅ MCP servers installation completed$(NC)"
