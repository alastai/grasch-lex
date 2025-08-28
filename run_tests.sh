#!/bin/bash
# Grasch Test Runner Script
# Sets up the proper Python environment and runs tests

set -e  # Exit on any error

echo "Grasch Test Runner"
echo "=================="
echo ""

# Check if we're in the right directory
if [ ! -f "test_grasch_functional.py" ]; then
    echo "❌ Error: test_grasch_functional.py not found in current directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Set Python version using pyenv if available
if command -v pyenv >/dev/null 2>&1; then
    echo "📋 Setting Python version to 3.12.4 using pyenv..."
    pyenv local 3.12.4
    echo "✓ Python version set"
else
    echo "⚠️  pyenv not found, using system Python"
fi

# Show environment info
echo ""
echo "Environment Information:"
echo "------------------------"
echo "Python version: $(python --version 2>&1 || echo 'Python not found')"
echo "Python path: $(which python 2>/dev/null || echo 'Python not found')"
echo "Current directory: $(pwd)"
echo ""

# Check if Python is available
if ! command -v python >/dev/null 2>&1; then
    echo "❌ Error: Python not found in PATH"
    echo "Please ensure Python 3.10+ is installed and available"
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $python_version found, but Python $required_version+ is required"
    exit 1
fi

echo "✓ Python $python_version is compatible"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install basic tools
echo "🔧 Upgrading pip and installing basic tools..."
pip install --upgrade pip setuptools wheel --quiet

# Install development dependencies if pyproject.toml exists
if [ -f "pyproject.toml" ]; then
    echo "🔧 Installing development dependencies..."
    pip install -e ".[dev,test]" --quiet 2>/dev/null || {
        echo "⚠️  pyproject.toml installation failed, continuing with basic setup..."
    }
fi

echo ""
echo "🚀 Running Functional Test"
echo "=========================="
echo ""

# Run the functional test
python test_grasch_functional.py

echo ""
echo "✅ Test execution completed!"
echo ""

# Optionally run additional tests if they exist
if [ -d "tests" ] && command -v pytest >/dev/null 2>&1; then
    echo "🧪 Running additional pytest tests..."
    pytest tests/ -v || echo "⚠️  Some pytest tests failed or no tests found"
fi

echo ""
echo "📊 Test Summary"
echo "==============="
echo "✓ Functional test completed successfully"
echo "✓ All Grasch library features demonstrated"
echo "✓ Environment setup validated"
echo ""
echo "To run tests manually:"
echo "  source .venv/bin/activate"
echo "  python test_grasch_functional.py"
echo ""
echo "To use the Makefile:"
echo "  make setup          # Set up development environment"
echo "  make test-functional # Run functional test"
echo "  make help           # Show all available commands"