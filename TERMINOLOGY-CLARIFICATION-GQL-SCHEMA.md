# Terminology Clarification: GQL-schema vs Data-Schema Directory

## Official GQL Specification

**GQL-schema**: The official GQL spec uses "GQL-schema" to refer to a leaf node directory in the catalog that can contain graphs and graph schemas.

## LEX Approach

Instead of using the term "GQL-schema", LEX uses a simpler rule-based approach:

### Rule
**Graphs and graph schemas can only exist in leaf node directories.**

### Terminology
- **Leaf node directory**: A directory that has no subdirectories
- **Data-schema directory**: Optional differentiating name for a leaf node directory (when needed for clarity)

### Equivalence
```
GQL-schema (GQL spec) ≡ Leaf node directory containing graphs/schemas (LEX)
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

- ❌ "GQL-schema" (GQL spec term, not used in LEX)
- ❌ "types-graphs directory" (previous LEX term, now deprecated)
- ❌ "type-graph" (should go away)

## Preferred Terms

- ✅ "Leaf directory" or "leaf node directory" (primary)
- ✅ "Data-schema directory" (when differentiation needed)
- ✅ "Graph schema" (for actual schemas)
- ✅ "Graph" (for graph instances)

## Usage in Documentation

### When referring to the container:
- "Graphs and graph schemas must be placed in leaf directories"
- "A leaf directory can contain graph references and graph schema references"
- "Data-schema directories are leaf nodes in the catalog tree"

### When referring to actual schemas:
- "A graph schema defines the structure of a graph"
- "The graph schema contains node types and edge types"
- "Graph schemas are stored in leaf directories"

## Impact on Specifications

### Requirements Document
- Replace "GQL-schema" with "leaf directory" or "data-schema directory"
- Emphasize the rule: graphs/schemas only in leaf directories
- Remove references to "types-graphs directory"

### API Design
- Use "leaf directory" in method names and documentation
- Avoid "GQL-schema" terminology
- Use "data-schema directory" only when clarification is needed

### Examples
- Catalog examples should show leaf directories containing references
- Documentation should explain the leaf directory rule clearly

---

**Date**: November 19, 2024
**Version**: LEX-2026.0.3.2
**Status**: Terminology Standard
