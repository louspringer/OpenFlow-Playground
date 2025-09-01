# Activity Models Domain
# Handles activity model generation, validation, and visualization

# Lightweight Activity Diagram Generator
lightweight-activity: ## Generate activity diagrams using lightweight generator
	@echo "🎯 Generating activity diagrams with lightweight generator..."
	@$(UV) run python -c "from src.lightweight_activity_generator import LightweightActivityGenerator; g = LightweightActivityGenerator(); print('✅ Lightweight activity generator ready')"
	@echo "Usage: $(UV) run python -c \"from src.lightweight_activity_generator import LightweightActivityGenerator; g = LightweightActivityGenerator(); result = g.generate_activity_diagram('your_file.py')\""

lightweight-activity-demo: ## Demo lightweight activity generator with test file
	@echo "🎯 Demo: Generating activity diagram for test_simple_workflow.py..."
	@$(UV) run python -c "from src.lightweight_activity_generator import LightweightActivityGenerator; g = LightweightActivityGenerator(); result = g.generate_activity_diagram('test_simple_workflow.py'); print('Success:', result['success']); print('Files:', result['output_files'])"

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

# GUI Launch Target
.PHONY: gui
gui: ## Launch Workflow Visualization GUI
	@echo "🚀 Launching Workflow Visualization GUI..."
	@echo "📱 The GUI will open in your default web browser"
	@echo "🔗 If it doesn't open automatically, go to: http://localhost:8501"
	@echo "⏹️  Press Ctrl+C to stop the application"
	@echo "=============================================="
	$(UV) run streamlit run src/workflow_visualization_gui.py --server.port 8501 --server.address localhost

# GUI Test Target
.PHONY: test-gui
test-gui: ## Test GUI functionality
	@echo "🧪 Testing GUI functionality..."
	$(UV) run python test_gui_demo.py

# Quick Launch Target
.PHONY: quick-gui
quick-gui: ## Quick GUI launch using launcher script
	@echo "🚀 Quick GUI launch..."
	python launch_gui.py

# GUI Navigation Testing with Screenshots
.PHONY: test-gui-navigation
test-gui-navigation: ## Run comprehensive GUI navigation tests with screenshots
	@echo "🧪 Running GUI Navigation Tests with Screenshots..."
	@echo "📸 Screenshots will be saved to: test_screenshots/"
	$(UV) run python tests/test_gui_navigation.py

# GUI Test with Playwright
.PHONY: test-gui-playwright
test-gui-playwright: ## Run GUI tests using Playwright
	@echo "🧪 Running GUI tests with Playwright..."
	$(UV) run pytest tests/test_gui_navigation.py -v --tb=short

# Install Playwright Browsers
.PHONY: install-playwright
install-playwright: ## Install Playwright browsers for testing
	@echo "🌐 Installing Playwright browsers..."
	$(UV) run playwright install chromium
