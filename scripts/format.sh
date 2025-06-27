#!/bin/bash

# Code formatting and quality script for AgentTest
# This script formats code and runs quality checks

set -e

echo "🔍 Running code formatting and quality checks..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: You're not in a virtual environment. Activating .venv..."
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    else
        echo "❌ No virtual environment found. Please create and activate a virtual environment."
        exit 1
    fi
fi

echo "📦 Installing/updating development dependencies..."
pip install -e ".[dev]"

echo "🖤 Running Black (code formatter)..."
black agent_test/ tests/ examples/

echo "📚 Running isort (import sorter)..."
isort agent_test/ tests/ examples/

echo "🔍 Running flake8 (linter)..."
flake8 agent_test/ tests/ examples/ --max-line-length=88 --extend-ignore=E203,W503 || echo "⚠️  Some linting issues found"

echo "🔬 Running mypy (type checker)..."
mypy agent_test/ --ignore-missing-imports --no-strict-optional || echo "⚠️  Some type checking issues found"

echo "🧪 Running tests..."
pytest tests/ -v || echo "⚠️  Some tests failed"

echo "✅ Code formatting and quality checks completed!"
echo ""
echo "💡 To run pre-commit hooks: pre-commit run --all-files"
echo "💡 To install pre-commit hooks: pre-commit install"
