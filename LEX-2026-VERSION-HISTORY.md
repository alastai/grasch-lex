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

## Version LEX:2026.0.1 (Released)

**Release Date**: November 1, 2025

### Artifacts

#### Core Schema Definition
- `lex-2026.0.1-graph-schema.schema.json` - JSON Schema for LEX:2026.0.1 Graph Schema format

#### Example Schemas
- `snb-lex-2026.0.1-schema.yaml` - LDBC SNB (Social Network Benchmark) schema
- `finbench-lex-2026.0.1-schema.yaml` - LDBC FinBench (Financial Benchmark) schema

#### Validation Tools
- `validate_snb_lex_0_1_schema.py` - SNB schema validation script
- `validate_finbench_lex_0_1_schema.py` - FinBench schema validation script

### Features
- Enhanced identifier structure with directory paths
- Improved value type system integration
- Refined constraint definitions
- Better property type validation

---

## Version LEX:2026.0.2 (Released)

**Release Date**: November 6, 2025

### Artifacts

#### Core Schema Definition
- `lex-2026.0.2.schema.json` - JSON Schema for specifications of graph catalogs, graph schemas and graph instances based on LEX-100r2

#### Example Schemas
- `snb-lex-2026.0.2-schema.yaml` - LDBC SNB schema with flexible type identification
- `finbench-lex-2026.0.2-schema.yaml` - LDBC FinBench schema with GQON addressing
- `example-catalog-lex-2026.0.2.yaml` - Example catalog specification demonstrating hierarchical organization

#### Example Graph Instances
- `finbench-sf1-graph-lex-2026.0.2.yaml` - FinBench SF1 graph instance with schema reference and storage schema

#### Validation Tools
- `validate_snb_lex_0_2_schema.py` - SNB schema validation script for 0.2
- `validate_finbench_lex_0_2_schema.py` - FinBench schema validation script for 0.2
- `validate_catalog_example.py` - Catalog specification validation script
- `validate_finbench_graph_instance.py` - Graph instance validation script

### Major Changes from 0.1

#### Enhanced Catalog Structure
- **LQON/GQON Support**: Locally and Globally Qualified Object Names with IRI-based addressing
- **Flexible Identification**: Support for pipe-delimited IRI|path syntax in GQON
- **Simplified Structure**: Streamlined identifier format

#### Flexible Type Identification System
- **Node Type Identifiers**: Support for `nodeTypeIndex`, `typeNameLabel`, or `typeIdentifyingLabels`
- **Edge Type Identifiers**: Support for `edgeTypeIndex`, `typeNameLabel`, or `typeIdentifyingLabels`
- **Label-Based Identification**: Primary identification through labels with index fallback
- **Mixed Identification**: Can mix different identification methods within same schema

#### Value Type System Updates
- **Canonical VTS Default**: CANONICAL value type system is now the default when not specified
- **Lowercase Parameters**: Changed from "NULLABLE" to "nullable" following LEX-100r2
- **Version Update**: Canonical VTS version changed from "2025.1" to "2025.0"

#### Enhanced Endpoint References
- **Flexible Endpoint Identification**: Edge endpoints can reference node types by any identifier method
- **Type Identifying Labels**: Support for multi-label type identification in endpoints
- **Improved Referencing**: More flexible and robust type referencing system

### Technical Specifications
- Based on LEX-100r2 specification
- JSON Schema Draft 2020-12 compliant
- Enhanced validation with flexible identification support
- Backward compatible constraint system
- Complete coverage of LEX-100r2 Abstract Syntax

### Validation Results
- ✅ SNB Schema: 8 node types, 15 edge types, 2 constraints (LQON addressing)
- ✅ FinBench Schema: 5 node types, 9 edge types, 3 constraints (GQON addressing)
- ✅ Example Catalog: 6 directories, 6 graph schemas, 6 graph instances (IRI-based addressing)
- ✅ FinBench SF1 Graph Instance: Schema reference, 3 constraints, storage schema (LQON addressing)

---

## Future Versions

### LEX:2026.0.3 (Planned)
- TBD: Storage schema integration for GraphAr
- TBD: Enhanced constraint types
- TBD: Additional value type system mappings