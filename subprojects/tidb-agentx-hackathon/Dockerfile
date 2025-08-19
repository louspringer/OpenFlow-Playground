# 🚀 TiDB AgentX Hackathon - OpenFlow Tools Integration Dockerfile
# Multi-stage build for development and production

# Base stage with Python and system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Create app directory
WORKDIR /app

# Copy project configuration files
COPY pyproject.toml uv.lock ./
COPY tidb_project_model_registry.json ./

# Development stage
FROM base as development

# Install development dependencies
RUN uv sync --extra dev --extra security --extra docs

# Copy OpenFlow tools from parent project
COPY --from=base /app /app
COPY ../../generated_packages ./generated_packages

# Install OpenFlow tools as editable packages
RUN uv pip install -e ./generated_packages/openflow-ghostbusters \
    && uv pip install -e ./generated_packages/openflow-code-quality \
    && uv pip install -e ./generated_packages/openflow-security-first \
    && uv pip install -e ./generated_packages/openflow-mdc-generator

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY docs/ ./docs/

# Install pre-commit hooks
RUN pre-commit install

# Expose development ports
EXPOSE 8501 8000 5432

# Development command
CMD ["uv", "run", "streamlit", "run", "src/streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Testing stage
FROM development as testing

# Install testing dependencies
RUN uv sync --extra dev --extra testing

# Run tests
CMD ["uv", "run", "pytest", "tests/", "-v", "--cov=src", "--cov-report=html"]

# Production stage
FROM base as production

# Install production dependencies only
RUN uv sync --production

# Copy OpenFlow tools
COPY --from=base /app /app
COPY ../../generated_packages ./generated_packages

# Install OpenFlow tools
RUN uv pip install -e ./generated_packages/openflow-ghostbusters \
    && uv pip install -e ./generated_packages/openflow-code-quality \
    && uv pip install -e ./generated_packages/openflow-security-first \
    && uv pip install -e ./generated_packages/openflow-mdc-generator

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose production port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Production command
CMD ["uv", "run", "streamlit", "run", "src/streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# CI/CD stage
FROM base as ci

# Install CI dependencies
RUN uv sync --extra dev --extra security --extra testing

# Copy OpenFlow tools
COPY --from=base /app /app
COPY ../../generated_packages ./generated_packages

# Install OpenFlow tools
RUN uv pip install -e ./generated_packages/openflow-ghostbusters \
    && uv pip install -e ./generated_packages/openflow-code-quality \
    && uv pip install -e ./generated_packages/openflow-security-first \
    && uv pip install -e ./generated_packages/openflow-mdc-generator

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY scripts/ ./scripts/

# Run CI pipeline
CMD ["uv", "run", "make", "ci"]

# Documentation stage
FROM base as docs

# Install documentation dependencies
RUN uv sync --extra docs

# Copy OpenFlow tools
COPY --from=base /app /app
COPY ../../generated_packages ./generated_packages

# Install OpenFlow tools
RUN uv pip install -e ./generated_packages/openflow-ghostbusters \
    && uv pip install -e ./generated_packages/openflow-code-quality \
    && uv pip install -e ./generated_packages/openflow-security-first \
    && uv pip install -e ./generated_packages/openflow-mdc-generator

# Copy source code and documentation
COPY src/ ./src/
COPY docs/ ./docs/

# Generate documentation
CMD ["uv", "run", "make", "docs"]







