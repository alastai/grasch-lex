# Grasch Project Makefile
# Provides convenient commands for development, testing, and building

.PHONY: help setup test test-functional clean lint format type-check build install dev-install

# Default target
help:
	@echo "Grasch Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup and Environment:"
	@echo "  setup           - Set up development environment"
	@echo "  dev-install     - Install package in development mode"
	@echo "  install         - Install package"
	@echo ""
	@echo "Testing:"
	@echo "  test            - Run all tests"
	@echo "  test-functional - Run functional test demonstration"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration- Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint            - Run linting checks"
	@echo "  format          - Format code with black"
	@echo "  type-check      - Run type checking with mypy"
	@echo "  check-all       - Run all code quality checks"
	@echo ""
	@echo "Build and Clean:"
	@echo "  build           - Build package"
	@echo "  clean           - Clean build artifacts"
	@echo ""
	@echo "Environment Info:"
	@echo "  env-info        - Show environment information"

# Environment setup
setup:
	@echo "Setting up Grasch development environment..."
	@echo "Python version: $$(python --version)"
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing dependencies..."
	.venv/bin/pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -e ".[dev,test]"
	@echo "✓ Development environment ready!"
	@echo ""
	@echo "To activate the virtual environment:"
	@echo "  source .venv/bin/activate"

# Development installation
dev-install:
	@echo "Installing Grasch in development mode..."
	python -m pip install -e ".[dev,test]"
	@echo "✓ Development installation complete"

# Regular installation
install:
	@echo "Installing Grasch..."
	python -m pip install .
	@echo "✓ Installation complete"

# Testing targets
test:
	@echo "Running all tests..."
	python -m pytest tests/ -v

test-functional:
	@echo "Running functional test demonstration..."
	@echo "======================================="
	PYTHONPATH=src python tests/test_functional_simple.py

test-unit:
	@echo "Running unit tests..."
	python -m pytest tests/ -m "unit" -v

test-integration:
	@echo "Running integration tests..."
	python -m pytest tests/ -m "integration" -v

# Code quality targets
lint:
	@echo "Running linting checks..."
	python -m ruff check src/ tests/ test_grasch_functional.py
	@echo "✓ Linting complete"

format:
	@echo "Formatting code..."
	python -m black src/ tests/ test_grasch_functional.py
	@echo "✓ Code formatting complete"

type-check:
	@echo "Running type checks..."
	python -m mypy src/
	@echo "✓ Type checking complete"

check-all: lint type-check
	@echo "✓ All code quality checks passed"

# Build targets
build:
	@echo "Building package..."
	python -m build
	@echo "✓ Build complete"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Clean complete"

# Environment info
env-info:
	@echo "Environment Information"
	@echo "======================"
	@echo "Python version: $$(python --version)"
	@echo "Python path: $$(which python)"
	@echo "Pip version: $$(pip --version)"
	@echo "Virtual environment: $${VIRTUAL_ENV:-Not activated}"
	@echo "Current directory: $$(pwd)"
	@echo "Pyenv version: $$(pyenv version 2>/dev/null || echo 'Not using pyenv')"

# Quick development workflow
dev: setup dev-install test-functional
	@echo "✓ Development environment ready and tested!"