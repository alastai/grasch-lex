# Technology Stack

## Core Technologies

- **Python**: 3.10+ required, supports 3.10, 3.11, 3.12
- **Build System**: setuptools with pyproject.toml configuration
- **Package Management**: pip with optional dependencies for dev/test environments

## Key Dependencies (Planned)

- **kuzu**: Embedded graph database (>=0.0.8)
- **pydantic**: Data validation and settings management (>=2.0.0)
- **pyarrow**: Arrow schema support for tabular representations (>=12.0.0)
- **jsonschema**: JSON Schema validation (>=4.0.0)
- **pyyaml**: YAML serialization support (>=6.0.0)
- **typing-extensions**: Enhanced type annotations (>=4.0.0)

## Development Tools

- **Testing**: pytest with coverage reporting
- **Code Formatting**: black (line length 88)
- **Linting**: ruff with comprehensive rule set
- **Type Checking**: mypy with strict configuration
- **Package Building**: build module

## Common Commands

### Environment Setup
```bash
make setup          # Set up development environment with venv
make dev-install    # Install in development mode
```

### Testing
```bash
make test                # Run all tests
make test-functional     # Run functional demonstration
make test-unit          # Run unit tests only
make test-integration   # Run integration tests only
```

### Code Quality
```bash
make lint           # Run ruff linting
make format         # Format with black
make type-check     # Run mypy type checking
make check-all      # Run all quality checks
```

### Build & Clean
```bash
make build          # Build package
make clean          # Clean build artifacts
make env-info       # Show environment information
```

### Quick Development Workflow
```bash
make dev            # Complete setup + install + test
```

## Configuration Standards

- **Line Length**: 88 characters (black/ruff)
- **Python Versions**: Target 3.10+ with type annotations
- **Import Sorting**: Handled by ruff
- **Type Checking**: Strict mypy configuration with comprehensive checks
- **Test Markers**: unit, integration, slow for test categorization