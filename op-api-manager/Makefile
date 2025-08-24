# OP API Manager Makefile
# Provides convenient targets for common operations

.PHONY: help install install-dev test lint format clean build publish

help: ## Show this help message
	@echo "OP API Manager - Available Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	uv sync

install-dev: ## Install with development dependencies
	uv sync --all-extras

test: ## Run tests
	uv run pytest tests/ -v

test-cov: ## Run tests with coverage
	uv run pytest tests/ --cov=op_api_manager --cov-report=html --cov-report=term

lint: ## Run linting
	uv run ruff check src/ tests/
	uv run mypy src/

format: ## Format code
	uv run black src/ tests/
	uv run ruff check --fix src/ tests/

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/

build: ## Build package
	uv build

publish: ## Publish to PyPI (requires authentication)
	uv publish

cli-test: ## Test the CLI commands
	uv run op-api-manager --help
	uv run op-api-manager discover --help
	uv run op-api-manager test --help

cli-discover: ## Run discovery command
	uv run op-api-manager discover --verbose

cli-test-apis: ## Run API testing command
	uv run op-api-manager test --verbose

cli-summary: ## Show summary of discovered keys
	uv run op-api-manager summary

cli-cache: ## Show cache status
	uv run op-api-manager cache

cli-providers: ## Show provider breakdown
	uv run op-api-manager providers

cli-refresh: ## Force refresh cache
	uv run op-api-manager refresh --force-refresh

dev-install: ## Install in development mode with symlink
	uv pip install -e .

check-deps: ## Check for outdated dependencies
	uv pip list --outdated

update-deps: ## Update dependencies
	uv sync --upgrade

shell: ## Start a shell with the package available
	uv shell

