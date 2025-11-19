# Terminology Clarification: GQL-schema vs Data-Schema (Leaf) Directory

## Official GQL Specification

**GQL-schema**: The official GQL spec uses "GQL-schema" to refer to a leaf node directory in the catalog that can contain graphs and graph schemas.

## LEX Approach

Instead of using the term "GQL-schema", LEX uses a simpler rule-based approach with clearer terminology:

### Rule
**Graphs and graph schemas can only exist in leaf node directories.**

### Standard LEX Terminology
- **Data-schema (leaf) directory**: The standard LEX term for what GQL calls a "GQL-schema"
- **Leaf directory**: A directory that has no subdirectories
- The parenthetical "(leaf)" clarifies that this is specifically a leaf node in the catalog tree

### Equivalence
```
GQL-schema (GQL spec) ≡ Data-schema (leaf) directory (LEX)
```

## Rationale

1. **Avoid confusion**: "GQL-schema" is confusing because:
   - It's not a schema in the traditional computer science sense
   - It's just a container/directory
   - The term "schema" should be reserved for actual graph schemas

2. **Simpler model**: The rule "graphs/schemas only in leaf directories" is clearer than introducing a special container concept

3. **Consistent terminology**: 
   - "Graph schema" = actual schema (description of graph structure)
   - "Leaf directory" = organizational container
   - "Data-schema directory" = optional clarifying term when needed

## Deprecated Terms

- ❌ "GQL-schema" (GQL spec term, not used in LEX except when referencing the GQL spec)
- ❌ "types-graphs directory" (previous LEX term, now deprecated)
- ❌ "type-graph" (deprecated)
- ❌ "leaf directory" alone (ambiguous - use full term "data-schema (leaf) directory")

## Standard LEX Terms

- ✅ **"Data-schema (leaf) directory"** (primary standard term - equivalent to GQL-schema)
- ✅ "Graph schema" (for actual schemas - the content, not the container)
- ✅ "Graph" (for graph instances)
- ✅ "Leaf directory" (acceptable when context is clear, but prefer the full term)

## Usage in Documentation

### When referring to the container:
- "Graphs and graph schemas must be placed in data-schema (leaf) directories"
- "A data-schema (leaf) directory can contain graph references and graph schema references"
- "Data-schema (leaf) directories are leaf nodes in the catalog tree"
- When context is clear: "leaf directories" is acceptable shorthand

### When referring to actual schemas:
- "A graph schema defines the structure of a graph"
- "The graph schema contains node types and edge types"
- "Graph schemas are stored in data-schema (leaf) directories"

### When referencing the GQL specification:
- "The GQL spec calls this a 'GQL-schema', which LEX refers to as a data-schema (leaf) directory"
- "GQL-schema (in GQL spec terminology) is equivalent to a data-schema (leaf) directory in LEX"

## Impact on Specifications

### Requirements Document ✅ COMPLETED
- ✅ Replaced "GQL-schema" and "types-graphs directory" with "data-schema (leaf) directory"
- ✅ Added terminology note explaining equivalence to GQL-schema
- ✅ Emphasizes the rule: graphs/schemas only in leaf directories

### Design Document (design.md) - TO DO
- Replace "GQL-schema" with "data-schema (leaf) directory"
- Update catalog management component descriptions
- Ensure consistency with requirements terminology

### API Design (LEX-2026.0.3.2-API-DESIGN.md) - TO DO
- Use "data-schema (leaf) directory" in method documentation
- Add note about GQL-schema equivalence
- Update catalog-related interface descriptions

### Modernization Guide (LEX-100r3 modernization.md) - TO DO
- Update terminology throughout
- Clarify GQL-schema vs LEX terminology differences

### Examples and JSON Schema - NO CHANGES NEEDED
- These are the source of truth and remain as-is
- Design documents are being brought into alignment with them

---

**Date**: November 19, 2024
**Version**: LEX-2026.0.3.2
**Status**: Terminology Standard
