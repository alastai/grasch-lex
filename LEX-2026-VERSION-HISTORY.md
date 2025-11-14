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

## Version LEX:2026.0.2.1 (Current)

**Release Date**: November 6, 2025

### New in 0.2.1
- **Enhanced JSON Schema**: Added complete `$defs` section with canonical value type definitions
- **Four-Way Type Mappings**: Each canonical type includes data/gql/sql/canonical mappings  
- **Validation Ready**: JSON Schema now self-validates canonical type usage
- **Cross-System Documentation**: Complete type system interoperability in schema
- **Build Numbering**: Introduced build/revision numbers for iterative delivery

### Artifacts

#### Core Schema Definition
- `lex-2026.0.2.1.schema.json` - Enhanced JSON Schema with embedded canonical type definitions

#### Example Schemas
- `snb-lex-2026.0.2.1-schema.yaml` - LDBC SNB schema (canonical types validated)
- `finbench-lex-2026.0.2.1-schema.yaml` - LDBC FinBench schema (canonical types validated)
- `example-catalog-lex-2026.0.2.1.yaml` - Example catalog specification

#### Example Graph Instances
- `finbench-sf1-graph-lex-2026.0.2.1.yaml` - FinBench SF1 graph instance

#### Validation Tools
- `validate_snb_lex_0_2_1_schema.py` - SNB schema validation script for 0.2.1
- `validate_finbench_lex_0_2_1_schema.py` - FinBench schema validation script for 0.2.1

### Features Enhanced in 0.2.1
- **Canonical Type System**: Complete JSON Schema definitions for all 14 canonical types
- **Type System Interoperability**: Four-way mappings (Universal VTS ↔ GQL ↔ SQL ↔ Canonical)
- **Self-Documenting Schema**: Type definitions embedded in JSON Schema for tooling
- **Validated Examples**: All YAML examples use only canonical types

## Version LEX:2026.0.2 (Superseded)

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

## Versi
on LEX:2026.0.3.1 (Current Release)

**Release Date**: November 12, 2025  
**Specification**: LEX-100r3

### Breaking Changes
- **Mandatory Labels**: All node and edge types must have at least one label (minimum changed from 0 to 1)
- **Type Identification**: Focus on typeNameLabel as preferred identification method

### New Features

#### Subtyping Support
- Types can declare supertypes for inheritance
- Java interface mixin-style composition
- Pulls in labels and property types from supertypes

#### Import/Modularization
- Schemas can be split across files using `$ref` syntax
- Swagger-style imports: `$ref('path/to/file.yaml')`
- Applies to node types, edge types, and property types

#### Type Interpretation Modes
- `exactlyOfThisType` (default): Exact match required
- `anySubtypeOf`: Covariant interpretation
- `anyProperSubtypeOf`: Proper subtype required

#### Extension Interpretation
- Control whether types can be extended
- `open: true` / `closed: false`: Allow undefined subtypes
- `open: false` / `closed: true`: Only defined subtypes (default)
- Applies separately to labels and property types

#### File References in Catalogs
- Catalog entries can reference external files
- Format: `file: $ref('path/to/schema.yaml')`
- Separates IRI from actual file location

### Artifacts

#### Core Schema Definition
- `src/grasch/schemas/lex-2026.0.3.1.schema.json` - JSON Schema with mandatory labels, subtyping, and imports

#### Example Schemas
- `src/grasch/examples/finbench-lex-2026.0.3.1-schema.yaml` - FinBench schema with mandatory labels
- `src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml` - SNB schema with mandatory labels

#### Graph Instance Examples
- `src/grasch/examples/finbench-sf1-graph-lex-2026.0.3.1.yaml` - FinBench SF1 graph instance

#### Catalog Examples
- `src/grasch/examples/example-catalog-lex-2026.0.3.1.yaml` - Catalog with IRI
- `src/grasch/examples/example-catalog-no-iri-lex-2026.0.3.1.yaml` - Catalog without IRI

#### Validation Tools
- `tests/validate_finbench_lex_0_3_1_schema.py` - FinBench validation with subtyping detection
- `tests/validate_snb_lex_0_3_1_schema.py` - SNB validation with subtyping detection
- `tests/validate_catalog_example_0_3_1.py` - Catalog validation with IRI
- `tests/validate_catalog_no_iri_0_3_1.py` - Catalog validation without IRI

### Documentation
- `LEX-2026.0.3.1-GUIDE.md` - Complete implementation guide
- `LEX-2026.0.3-CHANGES.md` - Detailed changelog from 0.2 to 0.3
- `ancillary docs/LEX-100r3 -- LEX_2026 Extended Graph Schema Specification.txt` - Official specification

### Migration from 0.2.1
- All types must have at least one label
- Schemas without labels will fail validation
- New features (subtyping, imports, type interpretation) are optional
- Default behaviors maintain compatibility where possible

### Archive Location
- Previous versions archived in `archive/lex-2026.0.2.1/` and `archive/lex-2026.0.0-0.2.0/`
