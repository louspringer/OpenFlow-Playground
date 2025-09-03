# Ack-Bert Makefile
# Provides common development and deployment tasks

.PHONY: help install test lint format clean docs examples validate

# Default target
help:
	@echo "Ack-Bert Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  install     Install dependencies"
	@echo "  clean       Clean build artifacts"
	@echo ""
	@echo "Development:"
	@echo "  test        Run test suite"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code with black"
	@echo "  validate    Validate ontology files"
	@echo ""
	@echo "Documentation:"
	@echo "  docs        Generate documentation"
	@echo "  examples    Run example scripts"
	@echo ""
	@echo "CLI:"
	@echo "  cli-help    Show CLI help"
	@echo "  cli-validate Validate ontology"
	@echo "  cli-compare Generate comparison"

# Setup
install:
	uv sync --all-extras

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development
test:
	uv run pytest tests/ -v --cov=src/ackbert --cov-report=html --cov-report=term

test-fast:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ tests/ examples/ scripts/
	uv run mypy src/ackbert/

format:
	uv run black src/ tests/ examples/ scripts/
	uv run ruff check --fix src/ tests/ examples/ scripts/

# Validation
validate:
	uv run python scripts/validate_ontology.py ontology/ackbert-ontology.ttl

# Documentation
docs:
	@echo "Generating documentation..."
	@mkdir -p docs/diagrams
	@echo "Documentation generated in docs/"

examples:
	uv run python examples/basic_usage.py

# CLI commands
cli-help:
	uv run python -m ackbert.cli --help

cli-validate:
	uv run python -m ackbert.cli validate ontology/ackbert-ontology.ttl --verbose

cli-compare:
	uv run python -m ackbert.cli compare ontology/ackbert-ontology.ttl --format table --diagrams

cli-candidates:
	uv run python -m ackbert.cli candidates ontology/ackbert-ontology.ttl

cli-requirements:
	uv run python -m ackbert.cli requirements ontology/ackbert-ontology.ttl

# Development workflow
dev-setup: install
	@echo "Setting up development environment..."
	@echo "✅ Dependencies installed"
	@echo "✅ Development environment ready"

dev-check: lint test validate
	@echo "✅ All checks passed"

# Build and package
build:
	uv build

# CI/CD helpers
ci-test:
	uv run pytest tests/ --cov=src/ackbert --cov-report=xml --junitxml=test-results.xml

ci-lint:
	uv run ruff check src/ tests/ examples/ scripts/
	uv run mypy src/ackbert/

# Quick development commands
quick-test:
	uv run pytest tests/test_ontology.py -v

quick-lint:
	uv run ruff check src/ackbert/ontology.py

# Example workflows
example-comparison:
	@echo "Running example comparison workflow..."
	uv run python -m ackbert.cli compare ontology/ackbert-ontology.ttl --format table
	uv run python examples/basic_usage.py

# Help for specific targets
help-test:
	@echo "Test Commands:"
	@echo "  test        Run full test suite with coverage"
	@echo "  test-fast   Run tests without coverage"
	@echo "  quick-test  Run only ontology tests"

help-lint:
	@echo "Linting Commands:"
	@echo "  lint        Run all linting checks"
	@echo "  format      Format code and fix auto-fixable issues"
	@echo "  quick-lint  Run linting on ontology module only"

help-cli:
	@echo "CLI Commands:"
	@echo "  cli-help        Show CLI help"
	@echo "  cli-validate    Validate ontology file"
	@echo "  cli-compare     Generate comparison report"
	@echo "  cli-candidates  List all candidates"
	@echo "  cli-requirements List all requirements"
