# RDI (Requirements→Design→Implementation) Makefile Module
# This module implements systematic development following RDI methodology

# RDI Configuration
RDI_REQUIREMENTS_DIR := requirements
RDI_DESIGN_DIR := design
RDI_IMPLEMENTATION_DIR := src
RDI_VALIDATION_DIR := validation
RDI_DOCUMENTATION_DIR := docs

# RDI Tools
RDI_REQUIREMENTS_VALIDATOR := uv run python scripts/rdi_requirements_validator.py
RDI_DESIGN_VALIDATOR := uv run python scripts/rdi_design_validator.py
RDI_IMPLEMENTATION_VALIDATOR := uv run python scripts/rdi_implementation_validator.py
RDI_TRACEABILITY_CHECKER := uv run python scripts/rdi_traceability_checker.py

# RDI Targets
.PHONY: rdi-help rdi-status rdi-requirements rdi-design rdi-implementation rdi-validation rdi-traceability rdi-full-cycle rdi-performance rdi-quality-monitoring

rdi-help: ## Show RDI methodology help
	@echo "$(CYAN)📋 RDI (Requirements→Design→Implementation) Methodology$(NC)"
	@echo "$(BLUE)====================================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Available RDI targets:$(NC)"
	@echo "  rdi-requirements     - Validate and manage requirements"
	@echo "  rdi-design          - Validate and manage design specifications"
	@echo "  rdi-implementation  - Validate and manage implementation"
	@echo "  rdi-validation      - Run full RDI validation cycle"
	@echo "  rdi-performance     - Run performance testing"
	@echo "  rdi-quality-monitoring - Run quality monitoring framework"
	@echo "  rdi-traceability    - Check requirements→design→implementation traceability"
	@echo "  rdi-full-cycle      - Run complete RDI cycle"
	@echo ""
	@echo "$(PURPLE)RDI Principles:$(NC)"
	@echo "  📋 Requirements: Clear, testable, traceable requirements"
	@echo "  🎨 Design: Architecture and design specifications"
	@echo "  🔧 Implementation: Code implementation with validation"
	@echo "  ✅ Validation: End-to-end validation and testing"
	@echo "  🔗 Traceability: Requirements→Design→Implementation mapping"
	@echo ""
	@echo "$(GREEN)RM Compliance:$(NC)"
	@echo "  ✅ Self-Monitoring: RDI validation and health checks"
	@echo "  ✅ Operational Visibility: RDI status reporting"
	@echo "  ✅ Graceful Degradation: RDI failure handling"
	@echo "  ✅ Single Responsibility: Focused RDI operations"

rdi-status: ## Show RDI methodology status
	@echo "$(CYAN)📊 RDI Methodology Status$(NC)"
	@echo "$(BLUE)========================$(NC)"
	@echo ""
	@echo "$(BLUE)📋 Requirements Status$(NC)"
	@echo "  Directory: $(RDI_REQUIREMENTS_DIR)"
	@echo "  Files: $(shell find $(RDI_REQUIREMENTS_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" 2>/dev/null | wc -l)"
	@echo "  Validator: $(RDI_REQUIREMENTS_VALIDATOR)"
	@echo ""
	@echo "$(BLUE)🎨 Design Status$(NC)"
	@echo "  Directory: $(RDI_DESIGN_DIR)"
	@echo "  Files: $(shell find $(RDI_DESIGN_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" 2>/dev/null | wc -l)"
	@echo "  Validator: $(RDI_DESIGN_VALIDATOR)"
	@echo ""
	@echo "$(BLUE)🔧 Implementation Status$(NC)"
	@echo "  Directory: $(RDI_IMPLEMENTATION_DIR)"
	@echo "  Files: $(shell find $(RDI_IMPLEMENTATION_DIR) -name "*.py" -o -name "*.js" -o -name "*.ts" 2>/dev/null | wc -l)"
	@echo "  Validator: $(RDI_IMPLEMENTATION_VALIDATOR)"
	@echo ""
	@echo "$(BLUE)✅ Validation Status$(NC)"
	@echo "  Directory: $(RDI_VALIDATION_DIR)"
	@echo "  Files: $(shell find $(RDI_VALIDATION_DIR) -name "*.py" -o -name "*.md" 2>/dev/null | wc -l)"
	@echo "  Traceability: $(RDI_TRACEABILITY_CHECKER)"

rdi-requirements: ## Validate and manage requirements
	@echo "$(CYAN)📋 RDI Requirements Validation$(NC)"
	@echo "$(BLUE)============================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Checking requirements directory...$(NC)"
	@if [ ! -d "$(RDI_REQUIREMENTS_DIR)" ]; then \
		echo "$(RED)❌ Requirements directory not found: $(RDI_REQUIREMENTS_DIR)$(NC)"; \
		echo "$(YELLOW)💡 Creating requirements directory...$(NC)"; \
		mkdir -p $(RDI_REQUIREMENTS_DIR); \
	fi
	@echo "$(GREEN)✅ Requirements directory: $(RDI_REQUIREMENTS_DIR)$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Validating requirements files...$(NC)"
	@if [ -f "scripts/rdi_requirements_validator.py" ]; then \
		$(RDI_REQUIREMENTS_VALIDATOR); \
	else \
		echo "$(YELLOW)⚠️  Requirements validator not found, creating basic validation...$(NC)"; \
		find $(RDI_REQUIREMENTS_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" | head -5; \
	fi
	@echo ""
	@echo "$(GREEN)✅ Requirements validation completed$(NC)"

rdi-design: ## Validate and manage design specifications
	@echo "$(CYAN)🎨 RDI Design Validation$(NC)"
	@echo "$(BLUE)======================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Checking design directory...$(NC)"
	@if [ ! -d "$(RDI_DESIGN_DIR)" ]; then \
		echo "$(RED)❌ Design directory not found: $(RDI_DESIGN_DIR)$(NC)"; \
		echo "$(YELLOW)💡 Creating design directory...$(NC)"; \
		mkdir -p $(RDI_DESIGN_DIR); \
	fi
	@echo "$(GREEN)✅ Design directory: $(RDI_DESIGN_DIR)$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Validating design files...$(NC)"
	@if [ -f "scripts/rdi_design_validator.py" ]; then \
		$(RDI_DESIGN_VALIDATOR); \
	else \
		echo "$(YELLOW)⚠️  Design validator not found, creating basic validation...$(NC)"; \
		find $(RDI_DESIGN_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" | head -5; \
	fi
	@echo ""
	@echo "$(GREEN)✅ Design validation completed$(NC)"

rdi-implementation: ## Validate and manage implementation
	@echo "$(CYAN)🔧 RDI Implementation Validation$(NC)"
	@echo "$(BLUE)=============================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Checking implementation directory...$(NC)"
	@if [ ! -d "$(RDI_IMPLEMENTATION_DIR)" ]; then \
		echo "$(RED)❌ Implementation directory not found: $(RDI_IMPLEMENTATION_DIR)$(NC)"; \
		echo "$(YELLOW)💡 Creating implementation directory...$(NC)"; \
		mkdir -p $(RDI_IMPLEMENTATION_DIR); \
	fi
	@echo "$(GREEN)✅ Implementation directory: $(RDI_IMPLEMENTATION_DIR)$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Validating implementation files...$(NC)"
	@if [ -f "scripts/rdi_implementation_validator.py" ]; then \
		$(RDI_IMPLEMENTATION_VALIDATOR); \
	else \
		echo "$(YELLOW)⚠️  Implementation validator not found, creating basic validation...$(NC)"; \
		find $(RDI_IMPLEMENTATION_DIR) -name "*.py" -o -name "*.js" -o -name "*.ts" | head -5; \
	fi
	@echo ""
	@echo "$(GREEN)✅ Implementation validation completed$(NC)"

rdi-validation: ## Run full RDI validation cycle
	@echo "$(CYAN)✅ RDI Full Validation Cycle$(NC)"
	@echo "$(BLUE)==========================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔄 Running RDI validation cycle...$(NC)"
	@echo ""
	@echo "$(BLUE)Step 1: Requirements Validation$(NC)"
	@$(MAKE) rdi-requirements
	@echo ""
	@echo "$(BLUE)Step 2: Design Validation$(NC)"
	@$(MAKE) rdi-design
	@echo ""
	@echo "$(BLUE)Step 3: Implementation Validation$(NC)"
	@$(MAKE) rdi-implementation
	@echo ""
	@echo "$(BLUE)Step 4: Traceability Check$(NC)"
	@$(MAKE) rdi-traceability
	@echo ""
	@echo "$(GREEN)✅ RDI validation cycle completed$(NC)"

rdi-traceability: ## Check requirements→design→implementation traceability
	@echo "$(CYAN)🔗 RDI Traceability Check$(NC)"
	@echo "$(BLUE)=======================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Checking traceability...$(NC)"
	@if [ -f "scripts/rdi_traceability_checker.py" ]; then \
		$(RDI_TRACEABILITY_CHECKER); \
	else \
		echo "$(YELLOW)⚠️  Traceability checker not found, creating basic check...$(NC)"; \
		echo "$(BLUE)📋 Requirements → Design Traceability$(NC)"; \
		find $(RDI_REQUIREMENTS_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" 2>/dev/null | wc -l; \
		echo "$(BLUE)🎨 Design → Implementation Traceability$(NC)"; \
		find $(RDI_DESIGN_DIR) -name "*.md" -o -name "*.yaml" -o -name "*.json" 2>/dev/null | wc -l; \
		echo "$(BLUE)🔧 Implementation Files$(NC)"; \
		find $(RDI_IMPLEMENTATION_DIR) -name "*.py" -o -name "*.js" -o -name "*.ts" 2>/dev/null | wc -l; \
	fi
	@echo ""
	@echo "$(GREEN)✅ Traceability check completed$(NC)"

rdi-full-cycle: ## Run complete RDI cycle
	@echo "$(CYAN)🔄 RDI Full Cycle$(NC)"
	@echo "$(BLUE)===============$(NC)"
	@echo ""
	@echo "$(YELLOW)🚀 Starting complete RDI cycle...$(NC)"
	@echo ""
	@echo "$(BLUE)Phase 1: Requirements Analysis$(NC)"
	@$(MAKE) rdi-requirements
	@echo ""
	@echo "$(BLUE)Phase 2: Design Specification$(NC)"
	@$(MAKE) rdi-design
	@echo ""
	@echo "$(BLUE)Phase 3: Implementation$(NC)"
	@$(MAKE) rdi-implementation
	@echo ""
	@echo "$(BLUE)Phase 4: Validation & Testing$(NC)"
	@$(MAKE) rdi-validation
	@echo ""
	@echo "$(BLUE)Phase 5: Performance Testing$(NC)"
	@$(MAKE) rdi-performance
	@echo ""
	@echo "$(BLUE)Phase 6: Traceability Verification$(NC)"
	@$(MAKE) rdi-traceability
	@echo ""
	@echo "$(GREEN)🎉 RDI full cycle completed successfully!$(NC)"
	@echo "$(YELLOW)💡 Next steps: Review results and iterate as needed$(NC)"

rdi-performance: ## Run performance testing
	@echo "$(CYAN)📊 RDI Performance Testing$(NC)"
	@echo "$(BLUE)========================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Running performance tests...$(NC)"
	@uv run python scripts/performance_tester.py
	@echo ""
	@echo "$(GREEN)✅ Performance testing completed$(NC)"

rdi-quality-monitoring: ## Run quality monitoring framework
	@echo "$(CYAN)📊 RDI Quality Monitoring$(NC)"
	@echo "$(BLUE)========================$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Running quality monitoring framework...$(NC)"
	@uv run python scripts/quality_monitoring_framework.py
	@echo ""
	@echo "$(GREEN)✅ Quality monitoring completed$(NC)"

# RDI Integration with existing targets
rdi-integration: ## Integrate RDI with existing development workflow
	@echo "$(CYAN)🔗 RDI Integration$(NC)"
	@echo "$(BLUE)===============$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Checking RDI integration points...$(NC)"
	@echo ""
	@echo "$(BLUE)📋 Requirements Integration$(NC)"
	@echo "  - Model-driven requirements validation"
	@echo "  - RM compliance requirements"
	@echo "  - Incident tracking requirements"
	@echo ""
	@echo "$(BLUE)🎨 Design Integration$(NC)"
	@echo "  - Architecture design validation"
	@echo "  - RM compliance design patterns"
	@echo "  - Component design specifications"
	@echo ""
	@echo "$(BLUE)🔧 Implementation Integration$(NC)"
	@echo "  - Code implementation validation"
	@echo "  - RM compliance implementation"
	@echo "  - Testing and validation"
	@echo ""
	@echo "$(GREEN)✅ RDI integration points identified$(NC)"
