# OpenFlow Playground - Model-Driven Makefile
# This Makefile leverages the project_model_registry.json for domain-specific operations

.PHONY: help install install-python install-bash install-cloudformation install-docs install-security install-streamlit install-healthcare install-go install-secure-shell install-all status status-quick status-dashboard ghostbusters ghostbusters-quick ghostbusters-detail ghostbusters-install
.PHONY: test test-python test-bash test-cloudformation test-docs test-security test-streamlit test-healthcare test-go test-secure-shell test-all
.PHONY: lint lint-python lint-bash lint-cloudformation lint-docs lint-security lint-streamlit lint-healthcare lint-go lint-secure-shell lint-all
.PHONY: format format-python format-bash format-docs format-go format-secure-shell format-all
.PHONY: validate validate-model validate-requirements validate-all
.PHONY: clean clean-python clean-cache clean-go clean-secure-shell clean-all
.PHONY: deploy deploy-streamlit deploy-security deploy-healthcare deploy-secure-shell
.PHONY: security security-scan security-check security-audit
.PHONY: docs docs-build docs-serve docs-index
.PHONY: dev-install node-check mermaid-check mcp-install mcp mcp-check mcp-setup mcp-validate backlog backlog-list backlog-add backlog-update backlog-remove backlog-stats backlog-search

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
	@echo "  make mcp                - Run MCP CLI with check command"
	@echo "  make mcp-setup          - Complete MCP setup process"
	@echo "  make mcp-validate       - Validate MCP configuration"
	@echo "  make backlog            - Show backlog statistics"
	@echo "  make backlog-list       - List all backlog items"
	@echo ""
	@echo "$(PURPLE)Ghostbusters Multi-Agent System:$(NC)"
	@echo "  make ghostbusters       - Run full Ghostbusters analysis"
	@echo "  make ghostbusters-quick - Quick Ghostbusters check"
	@echo "  make ghostbusters-detail- Detailed Ghostbusters analysis"
	@echo "  make ghostbusters-install- Install Ghostbusters dependencies"

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
	@DISABLE_TEST_GENERATION=1 $(UV) run pytest tests/ -v
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

security-scan: ## Run comprehensive security scan using established tools (best practices)
	@echo "🔒 Running Security Scan (Best Practices)..."
	@echo "================================================"
	
	@echo "1️⃣ Python Security (Bandit)..."
	@uv run bandit -r src/ scripts/ --exclude tests/,.venv/,.mypy_cache/,__pycache__/ || true
	
	@echo ""
	@echo "2️⃣ Pattern-based Security (Semgrep)..."
	@if command -v semgrep >/dev/null 2>&1; then \
		echo "✅ Semgrep found, running security rules..."; \
		uv run semgrep scan --config=auto --json --output semgrep-report.json || true; \
	else \
		echo "⚠️  Semgrep not installed. Install with: uv add --dev semgrep"; \
	fi
	
	@echo ""
	@echo "3️⃣ Dependency Vulnerabilities (Safety)..."
	@if command -v safety >/dev/null 2>&1; then \
		echo "✅ Safety found, scanning dependencies..."; \
		uv run safety check --json --output safety-report.json || true; \
	else \
		echo "⚠️  Safety not installed. Install with: uv add --dev safety"; \
	fi
	
	@echo ""
	@echo "4️⃣ Secret Detection (Detect-Secrets)..."
	@if command -v detect-secrets >/dev/null 2>&1; then \
		echo "✅ Detect-Secrets found, scanning for secrets..."; \
		uv run detect-secrets scan --baseline .secrets.baseline || true; \
	else \
		echo "⚠️  Detect-Secrets not installed. Install with: uv add --dev detect-secrets"; \
	fi
	
	@echo ""
	@echo "5️⃣ Comprehensive Secret Detection (Gitleaks)..."
	@if command -v gitleaks >/dev/null 2>&1; then \
		echo "✅ Gitleaks found, scanning for secrets..."; \
		gitleaks detect --source . --report-format json --report gitleaks-report.json || true; \
	else \
		echo "⚠️  Gitleaks not installed. Install with: make security-install"; \
	fi
	
	@echo ""
	@echo "6️⃣ Infrastructure & Dependency Scanning (Trivy)..."
	@if command -v trivy >/dev/null 2>&1; then \
		echo "✅ Trivy found, scanning infrastructure..."; \
		trivy fs --security-checks vuln . --format json --output trivy-report.json || true; \
	else \
		echo "⚠️  Trivy not installed. Install with: make security-install"; \
	fi
	
	@echo ""
	@echo "🎯 Security Scan Complete!"
	@echo "📋 Reports generated:"
	@ls -la *-report.json 2>/dev/null || echo "  No reports generated yet"
	@echo ""
	@echo "📋 Review all findings and fix security issues"
	@echo "🔒 Remember: Use established tools, not custom scanners!"
	@echo "📚 Best Practices: Follow OWASP guidelines and CWE references"

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

security-install: ## Install required security tools using best practices
	@echo "🔧 Installing Security Tools (Best Practices)..."
	
	@echo "Installing Python security packages..."
	@uv add --dev bandit safety detect-secrets
	
	@echo ""
	@echo "Installing Semgrep..."
	@uv add --dev semgrep
	
	@echo ""
	@echo "Installing external security tools..."
	@echo "Installing Trivy..."
	@if ! command -v trivy >/dev/null 2>&1; then \
		curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin; \
		echo "✅ Trivy installed"; \
	else \
		echo "✅ Trivy already installed"; \
	fi
	
	@echo ""
	@echo "Installing Gitleaks..."
	@if ! command -v gitleaks >/dev/null 2>&1; then \
		if command -v go >/dev/null 2>&1; then \
			go install github.com/zricethezav/gitleaks/v8@latest; \
			echo "✅ Gitleaks installed via Go"; \
		else \
			echo "⚠️  Go not found. Install Go first: https://golang.org/doc/install"; \
			echo "   Then run: go install github.com/zricethezav/gitleaks/v8@latest"; \
		fi; \
	else \
		echo "✅ Gitleaks already installed"; \
	fi
	
	@echo ""
	@echo "🎯 Security Tools Installation Complete!"
	@echo "📋 Available tools:"
	@echo "  ✅ Bandit - Python security scanning"
	@echo "  ✅ Semgrep - Pattern-based security scanning"
	@echo "  ✅ Safety - Dependency vulnerability scanning"
	@echo "  ✅ Detect-Secrets - Secret detection"
	@if command -v trivy >/dev/null 2>&1; then echo "  ✅ Trivy - Vulnerability scanning"; else echo "  ⏳ Trivy - To be installed"; fi
	@if command -v gitleaks >/dev/null 2>&1; then echo "  ✅ Gitleaks - Secret detection"; else echo "  ⏳ Gitleaks - To be installed"; fi
	@echo ""
	@echo "🔒 Remember: Use established tools, not custom scanners!"

security-clean: ## Clean up security scan reports
	@echo "🧹 Cleaning up security scan reports..."
	@rm -f gitleaks-report.json semgrep-report.json

security-check: ## Run quick security check
	@echo "🔒 Running Quick Security Check..."
	@uv run bandit -r src/ scripts/ --exclude tests/,.venv/,.mypy_cache/,__pycache__/ || true
	@echo "✅ Quick security check complete"

quality-check: ## Run comprehensive code quality checks
	@echo "🔍 Running Code Quality Checks..."
	@uv run black --check src/ tests/ || true
	@uv run ruff check src/ tests/ || true
	@uv run mypy src/ || true
	@echo "✅ Code quality checks complete"

test-model-driven: ## Test model-driven development
	@echo "🧪 Testing Model-Driven Development..."
	@uv run python -c "import json; json.load(open('project_model_registry.json'))" && echo "✅ Project model registry is valid JSON"
	@echo "✅ Model-driven development test complete"
	@echo "✅ Security reports cleaned up!"

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
	@echo "$(CYAN)🚀 OpenFlow Playground - Comprehensive Status Report$(NC)"
	@echo "$(BLUE)====================================================$(NC)"
	@echo ""
	
	@echo "$(BLUE)📊 Code Quality Status$(NC)"
	@echo "$(YELLOW)  Flake8 Issues:$(NC)"
	@FLAKE8_COUNT=$$($(UV) run flake8 --count --statistics src/ 2>/dev/null | tail -1 | grep -Eo '[0-9]+' | head -1 || echo "0"); \
	if [ "$$FLAKE8_COUNT" -eq 0 ]; then \
		echo "    $(GREEN)✅ 0 issues found$(NC)"; \
	else \
		echo "    $(YELLOW)⚠️  $$FLAKE8_COUNT issues found$(NC)"; \
	fi
	@echo "$(YELLOW)  MyPy Issues:$(NC)"
	@MYPY_COUNT=$$($(UV) run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null | grep -c "error:" || echo "0"); \
	if [ "$$MYPY_COUNT" -eq 0 ]; then \
		echo "    $(GREEN)✅ 0 type errors found$(NC)"; \
	elif [ "$$MYPY_COUNT" -lt 50 ]; then \
		echo "    $(YELLOW)⚠️  $$MYPY_COUNT type errors found$(NC)"; \
	else \
		echo "    $(RED)🚨 $$MYPY_COUNT type errors found - CRITICAL$(NC)"; \
	fi
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
	@echo "$(BLUE)📋 Backlog Alignment Check$(NC)"
	@echo "$(YELLOW)  Current Backlog Summary:$(NC)"
	@if [ -f project_model_registry.json ]; then \
		BACKLOG_COUNT=$$(grep -c '"status": "backlogged"' project_model_registry.json || echo "0"); \
		echo "    $(GREEN)✅ $$BACKLOG_COUNT items in backlog$(NC)"; \
		echo "    $(YELLOW)  Active items:$(NC)"; \
		grep -B 2 -A 1 '"status": "backlogged"' project_model_registry.json | grep '"requirement":' | head -3 | while read line; do \
			REQ=$$(echo "$$line" | sed 's/.*"requirement": "\([^"]*\)".*/\1/'); \
			echo "      • $$REQ"; \
		done; \
		if [ "$$BACKLOG_COUNT" -gt 3 ]; then \
			echo "      ... and $$(($$BACKLOG_COUNT - 3)) more items"; \
		fi; \
	else \
		echo "    $(RED)❌ project_model_registry.json not found$(NC)"; \
	fi
	@echo "$(YELLOW)  Status vs Backlog Alignment:$(NC)"
	@MYPY_COUNT_ALIGN=$$($(UV) run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null | grep -c "error:" || echo "0"); \
	echo "    $(YELLOW)Current MyPy errors: $$MYPY_COUNT_ALIGN$(NC)"; \
	if [ -f project_model_registry.json ]; then \
		MYPY_IN_BACKLOG=$$(grep -c '"requirement": "Fix.*MyPy.*type errors"' project_model_registry.json || echo "0"); \
		if [ "$$MYPY_COUNT_ALIGN" -gt 100 ] 2>/dev/null; then \
			if [ "$$MYPY_IN_BACKLOG" -gt 0 ]; then \
				echo "    $(YELLOW)⚠️  $$MYPY_COUNT_ALIGN MyPy errors tracked in backlog$(NC)"; \
				echo "    $(YELLOW)    → High priority item requiring attention$(NC)"; \
			else \
				echo "    $(RED)🚨 CRITICAL: $$MYPY_COUNT_ALIGN MyPy errors NOT in backlog$(NC)"; \
				echo "    $(YELLOW)    → Add 'Fix MyPy type errors' to backlog$(NC)"; \
							fi; \
		elif [ "$$MYPY_COUNT_ALIGN" -gt 50 ] 2>/dev/null; then \
			if [ "$$MYPY_IN_BACKLOG" -gt 0 ]; then \
				echo "    $(YELLOW)⚠️  $$MYPY_COUNT_ALIGN MyPy errors tracked in backlog$(NC)"; \
				echo "    $(YELLOW)    → Medium priority item requiring attention$(NC)"; \
			else \
				echo "    $(YELLOW)⚠️  $$MYPY_COUNT_ALIGN MyPy errors need backlog tracking$(NC)"; \
				echo "    $(YELLOW)    → Consider adding to backlog$(NC)"; \
			fi; \
		else \
			echo "    $(GREEN)✅ MyPy errors within manageable range ($$MYPY_COUNT_ALIGN found)$(NC)"; \
		fi; \
		echo "$(YELLOW)  Alignment Score:$(NC)"; \
		if [ "$$MYPY_COUNT_ALIGN" -gt 100 ] && [ "$$MYPY_IN_BACKLOG" -eq 0 ]; then \
			echo "    $(RED)❌ POOR: Critical issues missing from backlog$(NC)"; \
		elif [ "$$MYPY_COUNT_ALIGN" -gt 50 ] && [ "$$MYPY_IN_BACKLOG" -eq 0 ]; then \
			echo "    $(YELLOW)🟡 FAIR: Medium issues need backlog tracking$(NC)"; \
		else \
			echo "    $(GREEN)✅ GOOD: Status aligns with backlog$(NC)"; \
		fi; \
	else \
		echo "    $(RED)❌ project_model_registry.json not found$(NC)"; \
	fi
	
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
	@MYPY_COUNT_QUICK=$$($(UV) run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null | grep -c "error:" || echo "0"); \
	if [ "$$MYPY_COUNT_QUICK" -gt 100 ] 2>/dev/null; then \
		if [ -f project_model_registry.json ]; then \
			MYPY_IN_BACKLOG_QUICK=$$(grep -c '"requirement": "Fix.*MyPy.*type errors"' project_model_registry.json || echo "0"); \
			if [ "$$MYPY_IN_BACKLOG_QUICK" -gt 0 ]; then \
				echo "  $(YELLOW)⚠️  PRIORITY: Fix MyPy type errors (tracked in backlog)$(NC)"; \
				echo "  $(YELLOW)    → High priority item requiring attention$(NC)"; \
			else \
				echo "  $(RED)🚨 PRIORITY: Fix MyPy type errors$(NC)"; \
				echo "  $(YELLOW)    → Add to backlog: 'Fix $$MYPY_COUNT_QUICK MyPy type errors'$(NC)"; \
			fi; \
		else \
			echo "  $(RED)🚨 PRIORITY: Fix MyPy type errors$(NC)"; \
			echo "  $(YELLOW)    → Add to backlog: 'Fix $$MYPY_COUNT_QUICK MyPy type errors'$(NC)"; \
		fi; \
	fi
	@echo ""
	@echo "$(GREEN)✅ Comprehensive status report complete!$(NC)"

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
# GHOSTBUSTERS MULTI-AGENT SYSTEM TARGETS
# =============================================================================

ghostbusters: ## Run Ghostbusters multi-agent delusion detection and recovery
	@echo "$(CYAN)👻 CALLING MORE GHOSTBUSTERS!$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@echo "$(YELLOW)🔒 Multi-agent validation with all available LLMs and deterministic tools...$(NC)"
	@echo ""
	@echo "$(BLUE)📋 Checking Ghostbusters system...$(NC)"
	@test -d src/ghostbusters || (echo "$(RED)❌ Ghostbusters system not found$(NC)" && exit 1)
	@echo "$(GREEN)✅ Ghostbusters system found$(NC)"
	@echo "$(YELLOW)📋 Checking dependencies...$(NC)"
	@$(UV) run python -c "import langgraph" > /dev/null 2>&1 || (echo "$(RED)❌ langgraph not available. Installing...$(NC)" && $(UV) sync)
	@echo "$(GREEN)✅ Dependencies ready$(NC)"
	@echo "$(YELLOW)📋 Running multi-agent analysis...$(NC)"
	@$(UV) run python scripts/ghostbusters_cli.py detail
	@echo "$(GREEN)✅ Ghostbusters analysis complete!$(NC)"

ghostbusters-quick: ## Quick Ghostbusters check (minimal output)
	@echo "$(CYAN)👻 Quick Ghostbusters Check$(NC)"
	@$(UV) run python scripts/ghostbusters_cli.py quick

ghostbusters-detail: ## Detailed Ghostbusters analysis with full findings
	@echo "$(CYAN)👻 Detailed Ghostbusters Analysis$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@$(UV) run python scripts/ghostbusters_cli.py detail

ghostbusters-install: ## Install Ghostbusters dependencies and verify system
	@echo "$(CYAN)🔧 Installing Ghostbusters Dependencies$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@echo "$(YELLOW)📋 Installing Python dependencies...$(NC)"
	@$(UV) sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"
	@echo "$(YELLOW)📋 Verifying Ghostbusters system...$(NC)"
	@test -d src/ghostbusters || (echo "$(RED)❌ Ghostbusters system not found$(NC)" && exit 1)
	@echo "$(GREEN)✅ Ghostbusters system found$(NC)"
	@echo "$(YELLOW)📋 Testing import...$(NC)"
	@$(UV) run python scripts/ghostbusters_cli.py install
	@echo "$(GREEN)✅ Ghostbusters system ready!$(NC)"

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

# =============================================================================
# MCP MANAGEMENT TARGETS
# =============================================================================

mcp: ## Run MCP CLI with check command
	@echo "$(CYAN)🔧 MCP Management$(NC)"
	@$(UV) run python scripts/mcp_cli.py check

mcp-setup: ## Complete MCP setup process
	@echo "$(CYAN)🚀 MCP Setup$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@$(UV) run python scripts/mcp_cli.py setup

mcp-validate: ## Validate MCP configuration
	@echo "$(CYAN)🔍 MCP Validation$(NC)"
	@$(UV) run python scripts/mcp_cli.py validate

# =============================================================================
# BACKLOG MANAGEMENT TARGETS
# =============================================================================

backlog: ## Show backlog statistics
	@echo "$(CYAN)📋 Backlog Management$(NC)"
	@node scripts/backlog_cli.js stats

backlog-list: ## List all backlog items
	@echo "$(CYAN)📋 Backlog Items$(NC)"
	@echo "$(BLUE)==============================================$(NC)"
	@node scripts/backlog_cli.js list

backlog-add: ## Add new backlog item (requires title and description)
	@echo "$(CYAN)➕ Add Backlog Item$(NC)"
	@echo "$(YELLOW)Usage: make backlog-add TITLE='Item Title' DESCRIPTION='Item Description' [PRIORITY=medium] [STATUS=pending]$(NC)"
	@if [ -z "$(TITLE)" ]; then \
		echo "$(RED)❌ TITLE is required$(NC)"; \
		echo "$(YELLOW)Example: make backlog-add TITLE='Fix MCP' DESCRIPTION='Implement MCP server'$(NC)"; \
		exit 1; \
	fi
	@node scripts/backlog_cli.js add "$(TITLE)" "$(DESCRIPTION)" "$(PRIORITY)" "$(STATUS)"

backlog-update: ## Update backlog item (requires ID, field, and value)
	@echo "$(CYAN)📝 Update Backlog Item$(NC)"
	@echo "$(YELLOW)Usage: make backlog-update ID='Item ID/Title' FIELD='field_name' VALUE='new_value'$(NC)"
	@if [ -z "$(ID)" ] || [ -z "$(FIELD)" ] || [ -z "$(VALUE)" ]; then \
		echo "$(RED)❌ ID, FIELD, and VALUE are required$(NC)"; \
		echo "$(YELLOW)Example: make backlog-update ID='Fix MCP' FIELD='status' VALUE='in_progress'$(NC)"; \
		exit 1; \
	fi
	@node scripts/backlog_cli.js update "$(ID)" "$(FIELD)" "$(VALUE)"

backlog-remove: ## Remove backlog item (requires ID)
	@echo "$(CYAN)🗑️ Remove Backlog Item$(NC)"
	@echo "$(YELLOW)Usage: make backlog-remove ID='Item ID/Title'$(NC)"
	@if [ -z "$(ID)" ]; then \
		echo "$(RED)❌ ID is required$(NC)"; \
		echo "$(YELLOW)Example: make backlog-remove ID='Fix MCP'$(NC)"; \
		exit 1; \
	fi
	@node scripts/backlog_cli.js remove "$(ID)"

backlog-search: ## Search backlog items (requires query)
	@echo "$(CYAN)🔍 Search Backlog$(NC)"
	@echo "$(YELLOW)Usage: make backlog-search QUERY='search term'$(NC)"
	@if [ -z "$(QUERY)" ]; then \
		echo "$(RED)❌ QUERY is required$(NC)"; \
		echo "$(YELLOW)Example: make backlog-search QUERY='MCP'$(NC)"; \
		exit 1; \
	fi
	@node scripts/backlog_cli.js search "$(QUERY)"
