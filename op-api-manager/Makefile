# OP API Manager Makefile
# Provides convenient targets for common operations

.PHONY: help install install-dev test test-cov lint format clean build publish docs examples

# Default target
help:
	@echo "🔍 OP API Manager - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "📦 Package Management:"
	@echo "  install      - Install package in development mode"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  build        - Build package distribution files"
	@echo "  clean        - Clean build artifacts and cache"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test         - Run all tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with Black"
	@echo ""
	@echo "🔍 OP Manager Operations:"
	@echo "  op-discover  - Discover API keys from 1Password"
	@echo "  op-summary   - Show summary of discovered keys"
	@echo "  op-cache     - Check cache status"
	@echo "  op-providers - Show provider breakdown"
	@echo "  op-refresh   - Force refresh cache"
	@echo "  op-status    - Show overall status"
	@echo ""
	@echo "📚 Documentation & Examples:"
	@echo "  docs         - Generate documentation"
	@echo "  examples     - Run example scripts"
	@echo ""
	@echo "🚀 Publishing:"
	@echo "  publish      - Build and publish to PyPI (dry-run)"
	@echo "  publish-live - Build and publish to PyPI (live)"

# Package Management
install:
	@echo "📦 Installing OP API Manager in development mode..."
	pip install -e .

install-dev:
	@echo "🔧 Installing with development dependencies..."
	pip install -e ".[dev,test]"

build:
	@echo "🏗️ Building package distribution..."
	python -m build

clean:
	@echo "🧹 Cleaning build artifacts and cache..."
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	rm -f op-api-manager-*.tar.gz op_api_manager-*.whl
	rm -f api_discovery_cache.json example_cache.json

# Testing & Quality
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

test-cov:
	@echo "📊 Running tests with coverage..."
	python -m pytest tests/ -v --cov=op_api_manager --cov-report=html --cov-report=term-missing

lint:
	@echo "🔍 Running linting checks..."
	ruff check src/ tests/ examples/
	black --check src/ tests/ examples/

format:
	@echo "✨ Formatting code..."
	black src/ tests/ examples/
	ruff check --fix src/ tests/ examples/

# OP Manager CLI Operations
op-discover:
	@echo "🔍 Discovering API keys from 1Password..."
	op-api-manager discover

op-discover-fresh:
	@echo "🔄 Discovering API keys (force refresh)..."
	op-api-manager discover --force-refresh

op-discover-save:
	@echo "💾 Discovering API keys and saving to file..."
	op-api-manager discover --output discovery_results.json

op-summary:
	@echo "📊 Showing summary of discovered API keys..."
	op-api-manager summary

op-summary-provider:
	@echo "🎯 Showing summary for specific provider (usage: make op-summary-provider PROVIDER=openai)..."
	@if [ -z "$(PROVIDER)" ]; then \
		echo "❌ Please specify PROVIDER (e.g., make op-summary-provider PROVIDER=openai)"; \
		exit 1; \
	fi
	op-api-manager summary --provider $(PROVIDER)

op-summary-status:
	@echo "📈 Showing summary for specific status (usage: make op-summary-status STATUS=working)..."
	@if [ -z "$(STATUS)" ]; then \
		echo "❌ Please specify STATUS (e.g., make op-summary-status STATUS=working)"; \
		exit 1; \
	fi
	op-api-manager summary --status $(STATUS)

op-cache:
	@echo "💾 Checking cache status..."
	op-api-manager cache

op-providers:
	@echo "🌐 Showing provider breakdown..."
	op-api-manager providers

op-refresh:
	@echo "🔄 Force refreshing cache..."
	op-api-manager refresh

op-status:
	@echo "📊 Overall OP Manager Status"
	@echo "============================"
	@echo ""
	@echo "🔍 Cache Status:"
	@op-api-manager cache 2>/dev/null || echo "  ❌ CLI not available"
	@echo ""
	@echo "🌐 Provider Summary:"
	@op-api-manager providers 2>/dev/null || echo "  ❌ CLI not available"
	@echo ""
	@echo "📈 Key Summary:"
	@op-api-manager summary 2>/dev/null || echo "  ❌ CLI not available"

# Documentation & Examples
docs:
	@echo "📚 Generating documentation..."
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs build; \
	else \
		echo "⚠️  mkdocs not available, skipping documentation generation"; \
	fi

examples:
	@echo "🚀 Running example scripts..."
	@echo ""
	@echo "📖 Basic Usage Example:"
	@python examples/basic_usage.py || echo "  ❌ Example failed"
	@echo ""
	@echo "🔧 Build and Test Script:"
	@python build_and_test.py || echo "  ❌ Build script failed"

# Publishing
publish:
	@echo "📦 Building and publishing to PyPI (DRY RUN)..."
	@echo "⚠️  This is a dry run - no actual publishing will occur"
	python -m build
	python -m twine check dist/*
	@echo "✅ Package built and validated successfully"
	@echo "💡 To publish live, run: make publish-live"

publish-live:
	@echo "🚀 Building and publishing to PyPI (LIVE)..."
	@echo "⚠️  This will actually publish to PyPI!"
	@read -p "Are you sure you want to publish to PyPI? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		python -m build; \
		python -m twine check dist/*; \
		python -m twine upload dist/*; \
		echo "✅ Package published successfully!"; \
	else \
		echo "❌ Publishing cancelled"; \
	fi

# Development Workflow
dev-setup: install-dev
	@echo "🔧 Development environment setup complete!"
	@echo "💡 You can now run:"
	@echo "  • make test        - Run tests"
	@echo "  • make lint        - Check code quality"
	@echo "  • make format      - Format code"
	@echo "  • make op-discover - Test OP Manager"

dev-test: format lint test
	@echo "✅ All development checks passed!"

# Quick Operations
quick: op-discover op-summary
	@echo "✅ Quick OP Manager operations completed!"

status: op-status
	@echo "✅ Status check completed!"

# Helpers
check-cli:
	@echo "🔍 Checking if op-api-manager CLI is available..."
	@if command -v op-api-manager >/dev/null 2>&1; then \
		echo "✅ CLI is available"; \
		op-api-manager --version; \
	else \
		echo "❌ CLI not available - run 'make install' first"; \
		exit 1; \
	fi

check-op:
	@echo "🔍 Checking if 1Password CLI is available..."
	@if command -v op >/dev/null 2>&1; then \
		echo "✅ 1Password CLI is available"; \
		op --version; \
	else \
		echo "❌ 1Password CLI not available"; \
		echo "💡 Install from: https://1password.com/downloads/command-line/"; \
		exit 1; \
	fi

# Integration with main project
link-main:
	@echo "🔗 Linking OP API Manager to main project..."
	@if [ -d "../src" ]; then \
		ln -sf "$(PWD)/src/op_api_manager" "../src/op_api_manager"; \
		echo "✅ Linked to ../src/op_api_manager"; \
	else \
		echo "⚠️  Main project src directory not found"; \
	fi

unlink-main:
	@echo "🔗 Unlinking OP API Manager from main project..."
	@if [ -L "../src/op_api_manager" ]; then \
		rm "../src/op_api_manager"; \
		echo "✅ Unlinked from main project"; \
	else \
		echo "⚠️  No link found in main project"; \
	fi
