.PHONY: help install install-dev format lint test clean docs

help:
	@echo "Available commands:"
	@echo "  install      Install package in production mode"
	@echo "  install-dev  Install package in development mode with dev dependencies"
	@echo "  format       Format code with black and isort"
	@echo "  lint         Run linting with flake8 and mypy"
	@echo "  test         Run tests with pytest"
	@echo "  clean        Clean up build artifacts"
	@echo "  docs         Build documentation"
	@echo "  pre-commit   Install and run pre-commit hooks"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

format:
	black agent_test/ tests/ examples/
	isort agent_test/ tests/ examples/

lint:
	flake8 agent_test/ tests/ examples/
	mypy agent_test/

test:
	pytest tests/ -v --cov=agent_test --cov-report=html --cov-report=term

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	mkdocs build

pre-commit:
	pre-commit install
	pre-commit run --all-files
