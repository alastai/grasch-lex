# LEX:2026 Version History

This document tracks the versions of LEX:2026 Graph Schema artifacts.

## Version LEX:2026.0.0 (Initial Release)

**Release Date**: October 30, 2025

### Artifacts

#### Core Schema Definition
- `lex-2026.0.0-graph-schema.schema.json` - JSON Schema for LEX:2026.0.0 Graph Schema format

#### Example Schemas
- `snb-lex-2026.0.0-schema.yaml` - LDBC SNB (Social Network Benchmark) schema
- `finbench-lex-2026.0.0-schema.yaml` - LDBC FinBench (Financial Benchmark) schema

#### Validation Tools
- `validate_snb_lex_schema.py` - SNB schema validation script
- `validate_finbench_lex_schema.py` - FinBench schema validation script

### Features

#### Graph Schema Structure
- Graph schema identifier with IRI-based addressing
- Support for CYPHER, GQL, and SQL value type systems
- Configurable node and edge type limits
- Complete node and edge type definitions with indexing
- Key label set dictionaries for efficient lookup

#### Type System
- Node types with indexed labels and property types
- Edge types with direction and endpoint specifications
- Property types with flexible value type system integration
- Value types with extensible parameter system

#### Constraint System
- Support for KEY and UNIQUE constraints
- Constraint patterns and property name specifications
- Extensible framework for future constraint types

### Validation Results
- ✅ SNB Schema: 8 node types, 15 edge types, 2 constraints
- ✅ FinBench Schema: 5 node types, 9 edge types, 3 constraints

### Technical Specifications
- JSON Schema Draft 2020-12 compliant
- YAML 1.2 compatible
- Python 3.10+ validation tools
- Complete coverage of LEX-100 Abstract Syntax

---

## Future Versions

### LEX:2026.0.1 (Planned)
- TBD: Minor enhancements and bug fixes
- TBD: Additional example schemas
- TBD: Enhanced validation features