# Activity Model Generation
# This file handles activity model generation and related operations

# Activity model targets
.PHONY: activity-models activity-models-quick ci-activity-models

activity-models: ## Generate activity models for round-trip engineering system
	@echo "🎨 Generating Activity Models..."
	@echo "=============================================="
	@$(UV) run python src/round_trip_engineering/activity_model_integration.py src/round_trip_engineering/ --output-dir generated_activity_models --verbose

activity-models-quick: ## Generate activity models without round-trip integration
	@echo "🎨 Generating Activity Models (Quick Mode)..."
	@echo "=============================================="
	@$(UV) run python src/round_trip_engineering/activity_model_integration.py src/round_trip_engineering/ --output-dir generated_activity_models --no-round-trip --verbose

ci-activity-models: ## Run CI/CD activity model generation
	@echo "🔧 Running CI/CD Activity Model Generation..."
	@echo "=============================================="
	@$(UV) run python scripts/ci_activity_models.py --verbose
