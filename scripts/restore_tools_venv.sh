#!/bin/bash
# Restore original tools in virtual environment
set -e

echo "🔄 Restoring original tools in virtual environment..."

VENV_PATH=".venv"
if [ ! -d ""VENV_PAT"H" ]; then
    echo "❌ Virtual environment not found at "VENV_PAT"H"
    exit 1
fi

# Restore original tools
if [ -f ""VENV_PATH"/bin/pytest.original" ]; then
    echo "📦 Restoring pytest..."
    cp ""VENV_PATH"/bin/pytest.original" ""VENV_PATH"/bin/pytest"
    rm ""VENV_PATH"/bin/pytest.original"
fi

if [ -f ""VENV_PATH"/bin/flake8.original" ]; then
    echo "📦 Restoring flake8..."
    cp ""VENV_PATH"/bin/flake8.original" ""VENV_PATH"/bin/flake8"
    rm ""VENV_PATH"/bin/flake8.original"
fi

if [ -f ""VENV_PATH"/bin/black.original" ]; then
    echo "📦 Restoring black..."
    cp ""VENV_PATH"/bin/black.original" ""VENV_PATH"/bin/black"
    rm ""VENV_PATH"/bin/black.original"
fi

if [ -f ""VENV_PATH"/bin/mypy.original" ]; then
    echo "📦 Restoring mypy..."
    cp ""VENV_PATH"/bin/mypy.original" ""VENV_PATH"/bin/mypy"
    rm ""VENV_PATH"/bin/mypy.original"
fi

echo "✅ Original tools restored!"
echo "🔓 Tools can now be executed directly again." 