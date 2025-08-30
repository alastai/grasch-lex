# Project Structure

## Directory Organization

```
grasch/
├── src/grasch/              # Main package source code
│   ├── __init__.py         # Package exports and version info
│   ├── core.py             # Session management and configuration
│   ├── catalog.py          # Catalog and directory management
│   ├── types.py            # Type system (content types, element types)
│   ├── constraints.py      # Constraint definitions
│   └── kuzu_mock.py        # Mock Kuzu database interface
├── tests/                  # Test suite
│   ├── test_functional.py      # Full functional tests
│   └── test_functional_simple.py # Standalone functional demo
├── .kiro/                  # Kiro IDE configuration
│   ├── specs/              # Feature specifications
│   ├── steering/           # AI assistant guidance
│   └── settings/           # IDE settings
├── ancillary docs/         # External documentation and standards
└── [build files]          # pyproject.toml, Makefile, etc.
```

## Code Organization Patterns

### Module Responsibilities

- **core.py**: Session configuration, language levels, catalog root management
- **catalog.py**: Hierarchical catalog structure, directory operations
- **types.py**: Type system with builders (ContentRecordType, NodeType, EdgeType)
- **constraints.py**: Schema constraints and validation rules
- **kuzu_mock.py**: Database interface abstraction

### Class Design Patterns

- **Builder Pattern**: Used extensively for type construction (ContentRecordTypeBuilder, NodeTypeBuilder)
- **Configuration Objects**: Dataclasses for session and profile configuration
- **Abstract Base Classes**: ElementType as base for NodeType/EdgeType
- **Immutable Types**: Content types use tuples for immutability

### Import Conventions

- All public APIs exported through `__init__.py`
- Relative imports within package modules
- Type annotations using `typing` module conventions
- Optional dependencies handled gracefully

## File Naming Conventions

- **Source files**: Snake_case Python modules
- **Test files**: `test_*.py` pattern for pytest discovery
- **Configuration**: Standard names (pyproject.toml, Makefile, .gitignore)
- **Documentation**: Markdown files with descriptive names

## Testing Structure

- **Functional tests**: End-to-end workflow demonstrations
- **Unit tests**: Individual component testing (planned)
- **Integration tests**: Cross-component testing (planned)
- **Standalone demos**: Self-contained examples without pytest

## Documentation Organization

- **README.md**: Main project documentation
- **ancillary docs/**: External standards and specifications
- **.kiro/specs/**: Feature specifications and requirements
- **Inline docstrings**: Module and class documentation following Python conventions