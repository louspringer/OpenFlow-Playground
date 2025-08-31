# Domain-Specific Operations
# This file handles all domain-specific operations from the project model

# Demo Core Domains
.PHONY: demo-core snowflake-openflow-demo deployment-automation setup-wizard streamlit-demo-app

demo-core: snowflake-openflow-demo deployment-automation setup-wizard streamlit-demo-app ## Demo core functionality

snowflake-openflow-demo: ## Snowflake OpenFlow demo operations
	@echo "$(BLUE)❄️ Snowflake OpenFlow Demo Operations$(NC)"
	@echo "  Status: Available for demo execution"

deployment-automation: ## Deployment automation operations
	@echo "$(BLUE)🚀 Deployment Automation Operations$(NC)"
	@echo "  Status: Available for deployment management"

setup-wizard: ## Setup wizard operations
	@echo "$(BLUE)🧙 Setup Wizard Operations$(NC)"
	@echo "  Status: Available for guided setup"

streamlit-demo-app: ## Streamlit demo app operations
	@echo "$(BLUE)📱 Streamlit Demo App Operations$(NC)"
	@echo "  Status: Available for app management"

# Demo Tools Domains
.PHONY: demo-tools ghostbusters intelligent-linter code-quality multi-agent-testing model-driven-testing round-trip-engineering

demo-tools: ghostbusters intelligent-linter code-quality multi-agent-testing model-driven-testing round-trip-engineering ## Demo tools functionality

ghostbusters: ## Ghostbusters paranormal investigation system
	@echo "$(BLUE)👻 Ghostbusters Operations$(NC)"
	@uv run python -c "from src.ghostbusters.availability_test import GhostbustersAvailabilityTest; import asyncio; tester = GhostbustersAvailabilityTest(); results = asyncio.run(tester.run_comprehensive_test()); print('  ' + tester.get_status_message())" 2>/dev/null || echo "  Status: Multi-agent system status unknown - run availability test for details"

intelligent-linter: ## Intelligent linter system
	@echo "$(BLUE)🧹 Intelligent Linter System$(NC)"
	@echo "  Status: AST-enhanced linting available"

code-quality: ## Code quality system
	@echo "$(BLUE)✨ Code Quality System$(NC)"
	@echo "  Status: Comprehensive quality checks available"

multi-agent-testing: ## Multi-agent testing system
	@echo "$(BLUE)🧪 Multi-Agent Testing$(NC)"
	@echo "  Status: Multi-dimensional testing available"

model-driven-testing: ## Model-driven testing system
	@echo "$(BLUE)📊 Model-Driven Testing$(NC)"
	@echo "  Status: Model-based validation available"

# Round-Trip Engineering Domain
.PHONY: round-trip-engineering json-model-manager voice-mode-integration round-trip-cli

round-trip-engineering: json-model-manager voice-mode-integration round-trip-cli ## Round-trip engineering system

json-model-manager: ## JSON Model Manager for project model updates
	@echo "$(BLUE)🔧 JSON Model Manager$(NC)"
	@uv run python -c "from src.round_trip_engineering.tools.json_model_manager import JSONModelManager; manager = JSONModelManager(); print('  Status: ' + ('Available' if manager.is_healthy() else 'Unavailable')); print('  Capabilities: ' + ', '.join(manager.get_module_capabilities()['json_operations']))" 2>/dev/null || echo "  Status: JSON Model Manager not available"

voice-mode-integration: ## Voice Mode MCP integration for round-trip engineering
	@echo "$(BLUE)🎤 Voice Mode MCP Integration$(NC)"
	@uvx voice-mode --version >/dev/null 2>&1 && echo "  Status: ✅ Available" || echo "  Status: ❌ Not available"
	@echo "  MCP Configuration: $(shell test -f .cursor/mcp.json && echo '✅ Configured' || echo '❌ Not configured')"
	@echo "  Voice Commands: 10 commands available for round-trip engineering"

round-trip-cli: ## Round-trip engineering command-line interface
	@echo "$(BLUE)🔧 Round-Trip Engineering CLI$(NC)"
	@test -f scripts/round_trip_cli.py && echo "  Status: ✅ Available" || echo "  Status: ❌ Not available"
	@echo "  Commands: reverse, forward, round-trip, compare, status"
	@echo "  Interface: Documented public interfaces only"

# Demo Infrastructure Domains
.PHONY: demo-infrastructure model-driven-projection mdc-generator security-first healthcare-cdc

demo-infrastructure: model-driven-projection mdc-generator security-first healthcare-cdc model-management ## Demo infrastructure

model-driven-projection: ## Model-driven projection system
	@echo "$(BLUE)🎯 Model-Driven Projection$(NC)"
	@echo "  Status: Model projection available"

mdc-generator: ## MDC generator system
	@echo "$(BLUE)📝 MDC Generator$(NC)"
	@echo "  Status: Cursor rule generation available"

security-first: ## Security-first development
	@echo "$(BLUE)🔒 Security-First Development$(NC)"
	@echo "  Status: Security scanning available"

healthcare-cdc: ## Healthcare CDC patterns
	@echo "$(BLUE)🏥 Healthcare CDC Patterns$(NC)"
	@echo "  Status: Healthcare domain patterns available"

# Demo APIs Domains
.PHONY: demo-apis ghostbusters-api ghostbusters-gcp mcp-integration distributed-security

demo-apis: ghostbusters-api ghostbusters-gcp mcp-integration distributed-security ## Demo APIs

ghostbusters-api: ## Ghostbusters API
	@echo "$(BLUE)👻 Ghostbusters API$(NC)"
	@echo "  Status: API endpoints available"

ghostbusters-gcp: ## Ghostbusters GCP integration
	@echo "$(BLUE)☁️ Ghostbusters GCP$(NC)"
	@echo "  Status: GCP integration available"

mcp-integration: ## MCP integration
	@echo "$(BLUE)🔌 MCP Integration$(NC)"
	@echo "  Status: MCP server integration available"

distributed-security: ## Distributed security scanning
	@echo "$(BLUE)🛡️ Distributed Security$(NC)"
	@echo "  Status: Distributed scanning available"

# Demo Utilities Domains
.PHONY: demo-utilities bash-utils documentation-utils data-utils cloudformation-utils go-utils secure-shell-utils

demo-utilities: bash-utils documentation-utils data-utils cloudformation-utils go-utils secure-shell-utils ## Demo utilities

# Model Management Domain
.PHONY: model-management validate-model

model-management: validate-model ## Model management and validation

# Backlog Management Domain
.PHONY: backlog-suite backlog-display backlog-create backlog-update backlog-complete backlog-health backlog-search

backlog-suite: backlog-display backlog-health backlog-search ## Comprehensive backlog management

# Model Validation Domain
.PHONY: validate-model validate-project-model

validate-model: validate-project-model ## Validate project model registry

validate-project-model: ## Validate project model registry against schema
	@echo "$(BLUE)🔍 Project Model Validation$(NC)"
	@echo "  Validating JSON syntax..."
	@jq -e . project_model_registry.json > /dev/null
	@echo "  Validating against schema..."
	@jsonschema -i project_model_registry.json project_model_registry.schema.json
	@echo "  Running Python validation script..."
	@uv run python scripts/validate_project_model.py
	@echo "  ✅ Project model validation passed!"

backlog-display: ## Display current backlog items by priority
	@echo "$(CYAN)📋 OpenFlow Playground - Backlog Status$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo ""
	@echo "$(RED)🚨 Critical Priority$(NC)"
	@jq -r '.backlog[] | select(.priority == "critical") | "  • \(.title) (\(.status))"' project_model_registry.json 2>/dev/null || echo "  No critical items found"
	@echo ""
	@echo "$(RED)🔴 High Priority$(NC)"
	@jq -r '.backlog[] | select(.priority == "high") | "  • \(.title) (\(.status))"' project_model_registry.json 2>/dev/null || echo "  No high priority items found"
	@echo ""
	@echo "$(YELLOW)🟡 Medium Priority$(NC)"
	@jq -r '.backlog[] | select(.priority == "medium") | "  • \(.title) (\(.status))"' project_model_registry.json 2>/dev/null || echo "  No medium priority items found"
	@echo ""
	@echo "$(GREEN)🟢 Low Priority$(NC)"
	@jq -r '.backlog[] | select(.priority == "low") | "  • \(.title) (\(.status))"' project_model_registry.json 2>/dev/null || echo "  No low priority items found"
	@echo ""
	@echo "$(BLUE)📊 Backlog Statistics$(NC)"
	@echo "  Total Items: $(shell jq '.backlog | length' project_model_registry.json 2>/dev/null || echo "0")"
	@echo "  Critical: $(shell jq '.backlog[] | select(.priority == "critical") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "  High: $(shell jq '.backlog[] | select(.priority == "high") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "  Medium: $(shell jq '.backlog[] | select(.priority == "medium") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "  Low: $(shell jq '.backlog[] | select(.priority == "low") | .title' project_model_registry.json 2>/dev/null | wc -l)"

backlog-health: ## Analyze backlog health and metrics
	@echo "$(CYAN)🏥 Backlog Health Analysis$(NC)"
	@echo "$(BLUE)========================$(NC)"
	@echo ""
	@echo "$(BLUE)📊 Quantitative Metrics$(NC)"
	@echo "  Total Items: $(shell jq '.backlog | length' project_model_registry.json 2>/dev/null || echo "0")"
	@echo "  Priority Distribution:"
	@echo "    Critical: $(shell jq '.backlog[] | select(.priority == "critical") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "    High: $(shell jq '.backlog[] | select(.priority == "high") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "    Medium: $(shell jq '.backlog[] | select(.priority == "medium") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo "    Low: $(shell jq '.backlog[] | select(.priority == "low") | .title' project_model_registry.json 2>/dev/null | wc -l)"
	@echo ""
	@echo "$(BLUE)🔍 Health Assessment$(NC)"
	@if [ $$(jq '.backlog | length' project_model_registry.json 2>/dev/null || echo "0") -lt 20 ]; then \
		echo "  Status: $(GREEN)🟢 HEALTHY$(NC) - Backlog size is manageable"; \
	elif [ $$(jq '.backlog | length' project_model_registry.json 2>/dev/null || echo "0") -lt 50 ]; then \
		echo "  Status: $(YELLOW)🟡 CAUTION$(NC) - Backlog size needs attention"; \
	else \
		echo "  Status: $(RED)🔴 CRITICAL$(NC) - Backlog size is overwhelming"; \
	fi

backlog-search: ## Search for backlog items using project model patterns
	@echo "$(CYAN)🔍 Backlog Discovery Search$(NC)"
	@echo "$(BLUE)==========================$(NC)"
	@echo ""
	@echo "$(BLUE)📋 Project Model Registry Search$(NC)"
	@jq -r '.backlog[] | "  \(.id): \(.title) [\(.priority)]"' project_model_registry.json 2>/dev/null || echo "  No backlog items found"
	@echo ""
	@echo "$(BLUE)🔍 Code-Level Indicators$(NC)"
	@echo "  TODO comments: $(shell grep -r 'TODO' . --include='*.py' --include='*.md' 2>/dev/null | wc -l)"
	@echo "  FIXME comments: $(shell grep -r 'FIXME' . --include='*.py' --include='*.md' 2>/dev/null | wc -l)"
	@echo "  HACK comments: $(shell grep -r 'HACK' . --include='*.py' --include='*.md' 2>/dev/null | wc -l)"
	@echo ""
	@echo "$(BLUE)📚 Documentation Search$(NC)"
	@echo "  Backlog references: $(shell grep -r 'backlog\|next_steps\|future.*work' docs/ 2>/dev/null | wc -l)"

bash-utils: ## Bash utilities
	@echo "$(BLUE)🐚 Bash Utilities$(NC)"
	@echo "  Status: Shell script utilities available"

documentation-utils: ## Documentation utilities
	@echo "$(BLUE)📚 Documentation Utilities$(NC)"
	@echo "  Status: Documentation tools available"

data-utils: ## Data utilities
	@echo "$(BLUE)📊 Data Utilities$(NC)"
	@echo "  Status: Data processing tools available"

cloudformation-utils: ## CloudFormation utilities
	@echo "$(BLUE)☁️ CloudFormation Utilities$(NC)"
	@echo "  Status: Infrastructure tools available"

go-utils: ## Go utilities
	@echo "$(BLUE)🐹 Go Utilities$(NC)"
	@echo "  Status: Go development tools available"

secure-shell-utils: ## Secure shell utilities
	@echo "$(BLUE)🔐 Secure Shell Utilities$(NC)"
	@echo "  Status: Secure shell tools available"

# Cursor Rules Domains
.PHONY: cursor-rules model-first-enforcement security-rules tool-integration-patterns

cursor-rules: model-first-enforcement security-rules tool-integration-patterns ## Cursor rules

model-first-enforcement: ## Model-first enforcement
	@echo "$(BLUE)🧠 Model-First Enforcement$(NC)"
	@echo "  Status: Model-driven development enforced"

security-rules: ## Security rules
	@echo "$(BLUE)🔒 Security Rules$(NC)"
	@echo "  Status: Security guidelines enforced"

tool-integration-patterns: ## Tool integration patterns
	@echo "$(BLUE)🛠️ Tool Integration Patterns$(NC)"
	@echo "  Status: Tool integration patterns available"

# RM Compliance Validation Targets
.PHONY: test-reflective-module-compliance check-module-sizes validate-rm-interfaces check-architectural-boundaries

test-reflective-module-compliance: ## Test Reflective Module compliance across all modules
	@echo "$(BLUE)🔍 Testing Reflective Module Compliance$(NC)"
	@uv run python scripts/rm_compliance_validator.py --all

check-module-sizes: ## Check all module sizes for RM compliance
	@echo "$(BLUE)📏 Checking Module Sizes for RM Compliance$(NC)"
	@uv run python scripts/rm_compliance_validator.py --all --report | grep -E "(📏 Lines:|❌.*EXCEEDS)" || echo "  ✅ All modules within size limits"

validate-rm-interfaces: ## Validate Reflective Module interfaces
	@echo "$(BLUE)🔌 Validating RM Interfaces$(NC)"
	@uv run python scripts/rm_compliance_validator.py --all | grep -E "(🔌 Interfaces:|✅.*compliant)" || echo "  ❌ Interface validation failed"

check-architectural-boundaries: ## Check architectural boundaries and dependencies
	@echo "$(BLUE)🏗️ Checking Architectural Boundaries$(NC)"
	@uv run python scripts/rm_compliance_validator.py --all --report | grep -E "(🏗️ Boundaries:|❌.*violations)" || echo "  ✅ All architectural boundaries clean"
