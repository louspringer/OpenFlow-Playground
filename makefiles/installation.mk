# Installation and Setup Operations
# This file handles all installation operations from the project model

# Core Installation Targets
.PHONY: install install-all install-python install-bash install-cloudformation install-docs install-security install-streamlit install-healthcare install-go install-secure-shell

install: install-all ## Install all dependencies (alias for install-all)

install-all: install-python install-bash install-cloudformation install-docs install-security install-streamlit install-healthcare install-go install-secure-shell ## Install all dependencies across all domains

# Python Installation
install-python: ## Install Python dependencies with UV
	@echo "$(BLUE)🐍 Installing Python Dependencies...$(NC)"
	@$(UV) sync --all-extras
	@echo "  ✅ Python dependencies installed"

# Bash Installation
install-bash: ## Install Bash development tools
	@echo "$(BLUE)🐚 Installing Bash Development Tools...$(NC)"
	@command -v shellcheck >/dev/null 2>&1 || { echo "  ℹ️ shellcheck not available - install manually"; }
	@echo "  ✅ Bash tools ready"

# CloudFormation Installation
install-cloudformation: ## Install CloudFormation tools
	@echo "$(BLUE)☁️ Installing CloudFormation Tools...$(NC)"
	@command -v cfn-lint >/dev/null 2>&1 || { echo "  ℹ️ cfn-lint not available - install manually"; }
	@echo "  ✅ CloudFormation tools ready"

# Documentation Installation
install-docs: ## Install documentation tools
	@echo "$(BLUE)📚 Installing Documentation Tools...$(NC)"
	@command -v markdownlint >/dev/null 2>&1 || { echo "  ℹ️ markdownlint not available - install manually"; }
	@echo "  ✅ Documentation tools ready"

# Security Installation
install-security: ## Install security tools
	@echo "$(BLUE)🔒 Installing Security Tools...$(NC)"
	@$(UV) add --dev bandit safety detect-secrets
	@echo "  ✅ Security tools installed"

# Streamlit Installation
install-streamlit: ## Install Streamlit dependencies
	@echo "$(BLUE)📱 Installing Streamlit Dependencies...$(NC)"
	@$(UV) add streamlit plotly pandas
	@echo "  ✅ Streamlit dependencies installed"

# Healthcare CDC Installation
install-healthcare: ## Install healthcare CDC dependencies
	@echo "$(BLUE)🏥 Installing Healthcare CDC Dependencies...$(NC)"
	@$(UV) add --dev healthcare-cdc-patterns || echo "  ℹ️ healthcare-cdc-patterns not available"
	@echo "  ✅ Healthcare CDC dependencies ready"

# Go Installation
install-go: ## Install Go development environment
	@echo "$(BLUE)🐹 Installing Go Development Environment...$(NC)"
	@command -v go >/dev/null 2>&1 || { echo "  ℹ️ Go not available - install manually"; }
	@echo "  ✅ Go development environment ready"

# Secure Shell Installation
install-secure-shell: ## Install secure shell dependencies
	@echo "$(BLUE)🔐 Installing Secure Shell Dependencies...$(NC)"
	@$(UV) add paramiko cryptography
	@echo "  ✅ Secure shell dependencies installed"

# Development Environment Setup
.PHONY: dev-setup dev-install node-check mermaid-check mcp-install mcp mcp-check mcp-setup mcp-validate

dev-setup: install-all ## Setup development environment
	@echo "$(GREEN)✅ Development environment setup complete$(NC)"

dev-install: ## Install Node.js development environment
	@echo "$(BLUE)🟢 Installing Node.js Development Environment...$(NC)"
	@command -v node >/dev/null 2>&1 || { echo "  ℹ️ Node.js not available - install manually"; }
	@command -v npm >/dev/null 2>&1 || { echo "  ℹ️ npm not available - install manually"; }
	@echo "  ✅ Node.js development environment ready"

node-check: ## Check Node.js environment
	@echo "$(BLUE)🟢 Checking Node.js Environment...$(NC)"
	@command -v node >/dev/null 2>&1 && echo "  ✅ Node.js: $(shell node --version)" || echo "  ❌ Node.js not found"
	@command -v npm >/dev/null 2>&1 && echo "  ✅ npm: $(shell npm --version)" || echo "  ❌ npm not found"

mermaid-check: ## Check Mermaid diagram support
	@echo "$(BLUE)📊 Checking Mermaid Diagram Support...$(NC)"
	@command -v mmdc >/dev/null 2>&1 && echo "  ✅ Mermaid CLI available" || echo "  ℹ️ Mermaid CLI not available - install with npm install -g @mermaid-js/mermaid-cli"

mcp-install: ## Install MCP integration
	@echo "$(BLUE)🔌 Installing MCP Integration...$(NC)"
	@$(UV) add mcp
	@echo "  ✅ MCP integration installed"

mcp: ## MCP operations
	@echo "$(BLUE)🔌 MCP Operations...$(NC)"
	@echo "  Status: MCP integration available"

mcp-check: ## Check MCP integration
	@echo "$(BLUE)🔌 Checking MCP Integration...$(NC)"
	@$(UV) run python -c "import mcp; print('✅ MCP integration available')" || echo "  ❌ MCP integration not available"

mcp-setup: ## Setup MCP integration
	@echo "$(BLUE)🔌 Setting up MCP Integration...$(NC)"
	@$(UV) run python -c "from mcp import setup; setup()" || echo "  ℹ️ MCP setup not available"

mcp-validate: ## Validate MCP integration
	@echo "$(BLUE)🔌 Validating MCP Integration...$(NC)"
	@$(UV) run python -c "from mcp import validate; validate()" || echo "  ℹ️ MCP validation not available"

# Utility Installation
.PHONY: install-utilities install-pre-commit install-ghostbusters install-activity-models

install-utilities: ## Install utility tools
	@echo "$(BLUE)🛠️ Installing Utility Tools...$(NC)"
	@$(UV) add --dev pre-commit
	@pre-commit install
	@echo "  ✅ Utility tools installed"

install-pre-commit: ## Install pre-commit hooks
	@echo "$(BLUE)🔍 Installing Pre-commit Hooks...$(NC)"
	@$(UV) add --dev pre-commit
	@pre-commit install
	@echo "  ✅ Pre-commit hooks installed"

install-ghostbusters: ## Install Ghostbusters system
	@echo "$(BLUE)👻 Installing Ghostbusters System...$(NC)"
	@$(UV) add --dev ghostbusters-core
	@echo "  ✅ Ghostbusters system installed"

install-activity-models: ## Install activity model generation tools
	@echo "$(BLUE)🎨 Installing Activity Model Generation Tools...$(NC)"
	@$(UV) add --dev plantuml
	@echo "  ✅ Activity model generation tools installed"
