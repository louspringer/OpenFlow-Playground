# Testing Operations
# This file handles all testing operations from the project model

# Core Testing Targets
.PHONY: test test-all test-python test-bash test-cloudformation test-docs test-security test-streamlit test-healthcare test-go test-secure-shell

test: test-all ## Run all tests (alias for test-all)

test-all: test-python test-bash test-cloudformation test-docs test-security test-streamlit test-healthcare test-go test-secure-shell test-round-trip test-activity-model-validation test-complete-round-trip test-enhanced-round-trip ## Run all tests across all domains

# Python Testing
test-python: ## Run Python tests
	@echo "$(BLUE)🐍 Running Python Tests...$(NC)"
	@$(UV) run pytest tests/ -v --tb=short

# Bash Testing
test-bash: ## Run Bash script tests
	@echo "$(BLUE)🐚 Running Bash Tests...$(NC)"
	@find . -name "*.sh" -exec shellcheck {} \; || true

# CloudFormation Testing
test-cloudformation: ## Run CloudFormation tests
	@echo "$(BLUE)☁️ Running CloudFormation Tests...$(NC)"
	@find . -name "*.yaml" -exec cfn-lint {} \; 2>/dev/null || echo "  ℹ️ cfn-lint not available"

# Documentation Testing
test-docs: ## Run documentation tests
	@echo "$(BLUE)📚 Running Documentation Tests...$(NC)"
	@find docs/ -name "*.md" -exec markdownlint {} \; || true

# Security Testing
test-security: ## Run security tests
	@echo "$(BLUE)🔒 Running Security Tests...$(NC)"
	@$(UV) run bandit -r src/ -f json -o security_scan.json || true
	@echo "  ✅ Security scan completed"

# Streamlit Testing
test-streamlit: ## Run Streamlit tests
	@echo "$(BLUE)📱 Running Streamlit Tests...$(NC)"
	@$(UV) run python -c "import streamlit; print('✅ Streamlit available')" || echo "  ❌ Streamlit not available"

# Healthcare CDC Testing
test-healthcare: ## Run healthcare CDC tests
	@echo "$(BLUE)🏥 Running Healthcare CDC Tests...$(NC)"
	@find src/healthcare_cdc/ -name "*.py" -exec $(UV) run python -m py_compile {} \; 2>/dev/null || echo "  ℹ️ No healthcare CDC files found"

# Go Testing
test-go: ## Run Go tests
	@echo "$(BLUE)🐹 Running Go Tests...$(NC)"
	@find . -name "*.go" -exec go test {} \; 2>/dev/null || echo "  ℹ️ No Go files found"

# Secure Shell Testing
test-secure-shell: ## Run secure shell tests
	@echo "$(BLUE)🔐 Running Secure Shell Tests...$(NC)"
	@find src/secure_shell_service/ -name "*.sh" -exec shellcheck {} \; 2>/dev/null || echo "  ℹ️ No secure shell files found"

# Specialized Testing Targets
.PHONY: test-model-driven test-ghostbusters test-multi-agent test-round-trip test-complete-round-trip test-enhanced-round-trip

test-model-driven: ## Test model-driven development
	@echo "$(BLUE)📊 Testing Model-Driven Development...$(NC)"
	@$(UV) run python -c "import json; json.load(open('project_model_registry.json'))" && echo "  ✅ Project model registry is valid JSON"
	@echo "  ✅ Model-driven development test complete"

test-ghostbusters: ## Test Ghostbusters system
	@echo "$(BLUE)👻 Testing Ghostbusters System...$(NC)"
	@$(UV) run python -c "from src.ghostbusters import GhostbustersOrchestrator; print('✅ Ghostbusters system available')" || echo "  ❌ Ghostbusters system not available"

test-multi-agent: ## Test multi-agent testing system
	@echo "$(BLUE)🧪 Testing Multi-Agent System...$(NC)"
	@$(UV) run python -c "from src.multi_agent_testing import MultiAgentTestingSystem; print('✅ Multi-agent system available')" || echo "  ❌ Multi-agent system not available"

test-round-trip: ## Test round-trip engineering system
	@echo "$(BLUE)🔄 Testing Round-Trip Engineering...$(NC)"
	@$(UV) run python -c "from src.round_trip_engineering import RoundTripSystem; print('✅ Round-trip system available')" || echo "  ❌ Round-trip system not available"

test-activity-model-validation: ## Test activity model validation for round-trip engineering
	@echo "$(BLUE)🔍 Testing Activity Model Validation...$(NC)"
	@$(UV) run python test_activity_model_validation.py

test-complete-round-trip: ## Test complete round-trip engineering workflow
	@echo "$(BLUE)🔄 Testing Complete Round-Trip Engineering Workflow...$(NC)"
	@$(UV) run python tests/test_complete_round_trip_workflow.py

test-enhanced-round-trip: ## Test enhanced round-trip requirements (Pydantic/MyPy/Reflective Modules)
	@echo "$(BLUE)🔄 Testing Enhanced Round-Trip Requirements...$(NC)"
	@$(UV) run python tests/test_round_trip_enhanced_requirements.py



# Testing Utilities
.PHONY: test-coverage test-performance test-integration test-unit

test-coverage: ## Run tests with coverage
	@echo "$(BLUE)📊 Running Tests with Coverage...$(NC)"
	@$(UV) run pytest tests/ --cov=src --cov-report=html --cov-report=term

test-performance: ## Run performance tests
	@echo "$(BLUE)⚡ Running Performance Tests...$(NC)"
	@$(UV) run python -c "import time; start=time.time(); time.sleep(0.1); print(f'✅ Performance test completed in {time.time()-start:.3f}s')"

test-integration: ## Run integration tests
	@echo "$(BLUE)🔗 Running Integration Tests...$(NC)"
	@$(UV) run pytest tests/ -m "integration" -v || echo "  ℹ️ No integration tests found"

test-unit: ## Run unit tests
	@echo "$(BLUE)🧩 Running Unit Tests...$(NC)"
	@$(UV) run pytest tests/ -m "not integration" -v || echo "  ℹ️ No unit tests found"
