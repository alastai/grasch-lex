# Product Overview

Grasch is a Python library implementing a GQL (Graph Query Language) Catalog with LEX-2026 (LDBC Extended GQL Schema) capabilities for property graph schema management.

## Core Purpose

- **GQL Catalog Management**: Hierarchical filesystem-like structure for managing named primary catalog objects
- **LEX-2026 Schema Language**: Extended schema validation with subtyping, lattices, and constraint definitions  
- **Information Schema Graphs (ISGs)**: Standardized representation of graph schemas
- **Multi-Interface Support**: PSO (Programmatic Schema Objects), DDL, and YAML interfaces
- **Kuzu Integration**: Embedded graph database for efficient storage and querying

## Key Capabilities

- Content record types with nested JSON-like structures
- Content type lattices based on Formal Concept Analysis
- Multiple validation conformance modes (exact-type, subtype, proper-subtype)
- Unified attribute types (label types and property types)
- Element types (node types and edge types) with subtyping relationships
- Schema derivation from existing graphs through core reduction
- IRI-based addressing for global identification

## Architecture

Three-layer architecture:
1. **PSO Interface**: Low-level programmatic API with fluent builders
2. **DDL Interface**: Higher-level command-based interface  
3. **YAML Interface**: Declarative configuration interface

## Current Status

Project is in design and specification phase, implementing LEX-2026 as the first version of the LEX (LDBC Extended GQL Schema) standard.