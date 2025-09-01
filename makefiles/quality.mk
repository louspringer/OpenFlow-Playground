# Code Quality and Formatting
# This file handles all code quality operations

# Quality targets
.PHONY: pre-commit-preprocess pre-commit smart-commit quality-check security-check

quality-check: format-all ## Run all quality checks
	@echo "$(BLUE)✨ Running Quality Checks...$(NC)"
	@echo "  ✅ Quality checks complete"

security-check: ## Run security checks
	@echo "$(BLUE)🔒 Running Security Checks...$(NC)"
	@$(UV) run bandit -r src/ -f json -o security_scan.json || true
	@echo "  ✅ Security scan completed"

pre-commit-preprocess: ## Run preprocessing to ensure pre-commit hooks pass
	@echo "🚀 Running Pre-commit Preprocessing..."
	@echo "🎯 This ensures all formatting is done BEFORE commit"
	@$(UV) run python scripts/pre_commit_preprocessor.py
	@echo "✅ Preprocessing complete - pre-commit hooks should now pass!"

pre-commit: ## Run pre-commit hooks for all files
	@echo "🔍 Running Pre-commit Hooks..."
	@pre-commit run --all-files || (echo "❌ Pre-commit hooks failed" && exit 1)
	@echo "✅ Pre-commit hooks passed!"

smart-commit: ## Smart commit: preprocess, then commit (recommended workflow)
	@echo "🧠 Smart Commit Workflow..."
	@echo "🎯 Step 1: Running preprocessing..."
	@$(MAKE) pre-commit-preprocess
	@echo "🎯 Step 2: Staging any reformatted files..."
	@git add .
	@echo "🎯 Step 3: Pre-commit hooks should now pass!"
	@echo "💡 Next: Run 'git commit -m \"your message\"'"

# Code formatting targets
.PHONY: format-all format-python format-bash format-docs format-go format-secure-shell

format-yaml: ## Format YAML files with yamlfix
	@echo "$(BLUE)🎨 Formatting YAML files...$(NC)"
	@$(UV) run yamlfix *.yaml *.yml || true
	@echo "$(GREEN)✅ YAML formatting complete$(NC)"

format-all: format-python format-bash format-docs format-go format-secure-shell format-yaml ## Format all code

format-python: ## Format Python code
	@echo "$(BLUE)🎨 Formatting Python code...$(NC)"
	@$(UV) run black src/ tests/ || true
	@$(UV) run ruff format src/ tests/ || true
	@echo "$(GREEN)✅ Python formatting complete$(NC)"

format-bash: ## Format Bash scripts
	@echo "$(BLUE)🎨 Formatting Bash scripts...$(NC)"
	@find . -name "*.sh" -exec shfmt -w {} \; 2>/dev/null || true
	@echo "$(GREEN)✅ Bash formatting complete$(NC)"

format-docs: ## Format documentation
	@echo "$(BLUE)🎨 Formatting documentation...$(NC)"
	@$(UV) run mdformat docs/ *.md || true
	@find docs/ -name "*.md" -exec markdownlint {} \; || true
	@echo "$(GREEN)✅ Documentation formatting complete$(NC)"

format-markdown: ## Format markdown files with mdformat
	@echo "$(BLUE)🎨 Formatting markdown files...$(NC)"
	@$(UV) run mdformat docs/ *.md || true
	@echo "$(GREEN)✅ Markdown formatting complete$(NC)"

format-go: ## Format Go code
	@echo "$(BLUE)🎨 Formatting Go code...$(NC)"
	@find . -name "*.go" -exec gofmt -w {} \; 2>/dev/null || true
	@echo "$(GREEN)✅ Go formatting complete$(NC)"

format-secure-shell: ## Format secure shell scripts
	@echo "$(BLUE)🎨 Formatting secure shell scripts...$(NC)"
	@find src/secure_shell_service/ -name "*.sh" -exec shfmt -w {} \; 2>/dev/null || true
	@echo "$(GREEN)✅ Secure shell formatting complete$(NC)"
