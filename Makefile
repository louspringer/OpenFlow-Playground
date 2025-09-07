# Beast Mode Agent Collaboration Network Makefile
# Quick commands for development and testing

.PHONY: help install redis start test lint format clean run-demo run-agent

# Default target
help:
	@echo "Beast Mode Agent Collaboration Network"
	@echo "======================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make redis       - Start Redis server"
	@echo "  make start       - Start the message listener"
	@echo "  make dashboard   - Start web dashboard"
	@echo "  make test        - Run all tests"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with Black"
	@echo "  make clean       - Clean up temporary files"
	@echo "  make run-demo    - Run the demo agent"
	@echo "  make run-agent   - Run a custom agent"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Start Redis server
redis:
	@echo "Starting Redis server..."
	@if command -v redis-server >/dev/null 2>&1; then \
		redis-server --daemonize yes; \
		echo "✅ Redis server started"; \
	else \
		echo "❌ Redis not found. Install with: brew install redis (macOS) or apt-get install redis-server (Ubuntu)"; \
		exit 1; \
	fi

# Start the message listener
start:
	@echo "Starting Beast Mode message listener..."
	uv run python simple_listener.py

# Start web dashboard
dashboard:
	@echo "Starting Beast Mode web dashboard..."
	uv run python web_dashboard.py --port 8080

# Run tests
test:
	@echo "Running tests..."
	uv run python -m pytest tests/ -v
	@echo "✅ Tests completed"

# Run linting
lint:
	@echo "Running linting checks..."
	uv run flake8 src/ tests/ examples/
	uv run mypy src/
	@echo "✅ Linting completed"

# Format code
format:
	@echo "Formatting code..."
	uv run black src/ tests/ examples/
	@echo "✅ Code formatted"

# Clean up
clean:
	@echo "Cleaning up..."
	rm -f bus_messages.log
	rm -f processed_messages.txt
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf examples/__pycache__/
	@echo "✅ Cleanup completed"

# Run demo agent
run-demo:
	@echo "Starting demo agent..."
	uv run python examples/basic_agent_example.py

# Run custom agent (pass AGENT_ID and CAPABILITIES as env vars)
run-agent:
	@echo "Starting custom agent..."
	@if [ -z "$$AGENT_ID" ] || [ -z "$$CAPABILITIES" ]; then \
		echo "Usage: make run-agent AGENT_ID=my_agent CAPABILITIES='python_coding,gcp_optimization'"; \
		exit 1; \
	fi
	uv run python examples/my_agent.py

# Development setup
dev-setup: install redis
	@echo "Development environment ready!"
	@echo "Run 'make start' to begin listening for messages"

# Full test suite
test-all: lint test
	@echo "✅ All checks passed"

# Quick start for new users
quick-start: install redis
	@echo "🚀 Beast Mode Agent Collaboration Network"
	@echo "=========================================="
	@echo ""
	@echo "✅ Dependencies installed"
	@echo "✅ Redis server started"
	@echo ""
	@echo "Next steps:"
	@echo "1. Run 'make start' in one terminal to listen for messages"
	@echo "2. Run 'make run-demo' in another terminal to start a demo agent"
	@echo "3. Watch the collaboration happen!"
	@echo ""
	@echo "For more info, run 'make help'"