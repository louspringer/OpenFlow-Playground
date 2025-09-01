# OpenFlow Playground - Project Setup Guide

## 🚀 Quick Start

### Prerequisites

- **Git**: Ensure you have git installed and initialized
- **Python 3.11+**: The project requires Python 3.11 or higher
- **UV Package Manager**: We use UV for Python package management

### Automatic Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd OpenFlow-Playground

# Run the automatic setup script
python scripts/setup_project.py
```

The setup script will:

1. ✅ Check if UV is installed (install if needed)
1. ✅ Install all project dependencies
1. ✅ Configure pre-commit hooks
1. ✅ Verify the setup is working

### Manual Setup

If you prefer to set up manually:

```bash
# 1. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install project dependencies
uv sync --all-extras

# 3. Install pre-commit
uv add --dev pre-commit

# 4. Install pre-commit hooks
uv run pre-commit install
```

## 🔧 Environment Configuration

### Why UV?

- **Fast**: UV is significantly faster than pip/poetry
- **Reliable**: Deterministic dependency resolution
- **Modern**: Built for modern Python development
- **Consistent**: Same environment across all team members

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

- **Security Scanning**: Bandit, Semgrep, Safety
- **Code Formatting**: Black, Ruff, mdformat
- **Quality Checks**: Linting, validation, model compliance
- **Model Validation**: Ensures RM compliance

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your configuration
nano .env
```

## 🧪 Testing Your Setup

After setup, verify everything is working:

```bash
# Run pre-commit hooks
uv run pre-commit run --all-files

# Run tests
make test

# Check project status
make status
```

## 🚨 Troubleshooting

### Common Issues

#### Pre-commit hooks not found

```bash
# Reinstall pre-commit hooks
uv run pre-commit install
```

#### UV not found

```bash
# Install UV manually
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your shell
source ~/.bashrc  # or ~/.zshrc
```

#### Permission denied errors

```bash
# Fix permissions
chmod +x scripts/*.py
chmod +x .git/hooks/*
```

#### Virtual environment conflicts

```bash
# Remove conflicting virtual environments
rm -rf .venv venv env/
# Reinstall with UV
uv sync --all-extras
```

### Getting Help

1. **Check the logs**: Look for error messages in the setup output
1. **Verify prerequisites**: Ensure git, Python, and UV are properly installed
1. **Check permissions**: Ensure you have write access to the project directory
1. **Review environment**: Make sure you're not in a conflicting virtual environment

## 📚 Next Steps

After successful setup:

1. **Explore the project**: Run `make help` to see available commands
1. **Run tests**: Execute `make test` to verify functionality
1. **Check quality**: Run `make quality-check` to ensure code standards
1. **Start developing**: Begin working on your features!

## 🔄 Updating the Setup

To update your setup when the project changes:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv sync --upgrade

# Reinstall pre-commit hooks
uv run pre-commit install
```

## 📝 Development Workflow

### Daily Development

```bash
# 1. Check out a feature branch
git checkout -b feature/your-feature

# 2. Make your changes
# ... edit files ...

# 3. Run quality checks
make quality-check

# 4. Run tests
make test

# 5. Commit with pre-commit hooks
git add .
git commit -m "feat: your feature description"
```

### Pre-commit Workflow

The project uses a smart commit workflow:

```bash
# Smart commit (recommended)
make smart-commit

# Or manual workflow
make pre-commit-preprocess  # Format and fix issues
git add .                    # Stage changes
git commit -m "message"      # Commit (hooks run automatically)
```

## 🎯 Success Criteria

Your setup is successful when:

- ✅ `uv run pre-commit --version` works
- ✅ `make test` runs successfully
- ✅ `make quality-check` passes
- ✅ Pre-commit hooks run on commit
- ✅ All dependencies are properly installed

## 🆘 Still Having Issues?

If you're still experiencing problems:

1. **Check the issue tracker** for known problems
1. **Review the logs** for specific error messages
1. **Verify your environment** matches the requirements
1. **Ask for help** in the project discussions

Remember: The setup script is designed to handle most common issues automatically!
