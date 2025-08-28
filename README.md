# Grasch

*Testing auto commit hook* - GQL Catalog and LEX-2026 Schema Library

Grasch is a Python library that implements a GQL (Graph Query Language) Catalog according to the GQL specification, extended with LEX-2026 (LDBC Extended GQL Schema) capabilities.

## Overview

Grasch provides:

- **GQL Catalog**: Hierarchical filesystem-like structure for managing named primary catalog objects
- **LEX-2026 Schema Language**: Extended schema validation with subtyping, lattices, and constraint definitions
- **Information Schema Graphs (ISGs)**: Standardized representation of graph schemas
- **Multiple Interfaces**: PSO (Programmatic Schema Objects), DDL, and YAML interfaces
- **Kuzu Integration**: Embedded graph database for efficient storage and querying
- **Strong Typing**: Comprehensive type annotations for Python and cross-language portability

## Key Features

### Schema Definition and Validation
- Content record types with nested JSON-like structures
- Content type lattices based on Formal Concept Analysis
- Multiple validation conformance modes (exact-type, subtype, proper-subtype)
- Supertype expressions for compressed validation rules

### Advanced Type System
- Unified attribute types (label types and property types)
- Element types (node types and edge types) with subtyping relationships
- Abstract types with proper-subtype conformance
- Schema derivation from existing graphs through core reduction

### Multiple Definition Formats
- LEX DDL (extends GQL DDL)
- YAML/JSON declarative definitions
- Pydantic model integration
- JSON Schema extensions with GQL/SQL datatypes

### Visualization and Analysis
- g.V() integration for graph visualization
- Schema graphs and content type lattice visualization
- IRI-based addressing for global identification

## Architecture

Grasch implements a three-layer architecture:

1. **PSO Interface**: Low-level programmatic API with fluent builders
2. **DDL Interface**: Higher-level command-based interface
3. **YAML Interface**: Declarative configuration interface

## Requirements

See [Requirements Document](.kiro/specs/property-graph-schema/requirements.md) for detailed specifications.

## Status

This project is currently in the design and specification phase, implementing LEX-2026 as the first version of the LEX (LDBC Extended GQL Schema) standard.