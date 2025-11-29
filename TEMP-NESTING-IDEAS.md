# TEMPORARY: Array Type Interpretation Nesting Concepts

**STATUS**: PROVISIONAL - Work in Progress  
**DATE**: 2024-11-28  
**PURPOSE**: Capture evolving understanding of array-level TI structure before finalizing design

## Key Insight: XTypeInterpretation as Recursive Unit

The fundamental unit for array-level type interpretation is **XTypeInterpretation** where X ∈ {nodeType, edgeType}.

### Correct Terminology

- **nodeTypeArrayInterpretation**: The recursive unit for interpreting arrays of node types
- **edgeTypeArrayInterpretation**: The recursive unit for interpreting arrays of edge types

### Structure

An XTypeInterpretation:
1. **Can be nested** (TI wrapping another TI)
2. **Eventually resolves to an array of element types** (which may contain only one element)
3. **Supersedes the "partition block" concept** - nesting is the mechanism, not partitioning

### YAML Examples

```yaml
# Example 1: Bare element type (0-level, implicit exactlyOf:concrete)
nodeTypes:
  - nodeType: Person

# Example 2: nodeTypeArrayInterpretation (1-level) wrapping array
nodeTypes:
  - abstract:
      nodeTypes:  # This array is what the TI interprets
        - nodeType: Vehicle
        - nodeType: Car

# Example 3: Nested nodeTypeArrayInterpretation (2-level)
nodeTypes:
  - subtypesOf:
      abstract:
        nodeTypes:  # This array is what the nested TI interprets
          - nodeType: Message
          - nodeType: Post
          - nodeType: Comment

# Example 4: Mixed - multiple interpretations in same array
nodeTypes:
  - nodeType: Person  # Bare (0-level)
  - abstract:         # 1-level interpretation
      nodeTypes:
        - nodeType: Vehicle
        - nodeType: Car
  - subtypesOf:       # 2-level nested interpretation
      abstract:
        nodeTypes:
          - nodeType: Message
          - nodeType: Post
```

## Recursive Definition

```
XTypeArrayInterpretation ::=
  | BareElementType                           // 0-level (implicit exactlyOf:concrete)
  | OneLevelWrapper(XTypeArrayInterpretation) // 1-level (abstract, concrete, etc.)
  | TwoLevelWrapper(XTypeArrayInterpretation) // 2-level (subtypesOf:abstract:, etc.)

where XTypeArrayInterpretation eventually resolves to:
  Array<ElementType>  // cardinality ≥ 1
```

## Key Properties

1. **Recursive**: An XTypeArrayInterpretation can wrap another XTypeArrayInterpretation
2. **Terminal**: Eventually resolves to an array of element types
3. **Cardinality**: The array may have cardinality 1 (singleton) or > 1 (multi-element)
4. **Nesting Depth**: Limited to 2 levels of TI wrappers (per design document)

## Current Schema Issues

The existing schema uses incorrect terminology:
- ❌ `PartitionBlockItemNode` - implies partitioning, not nesting
- ❌ `PartitionBlockItemEdge` - implies partitioning, not nesting
- ✅ Should be: `NodeTypeArrayInterpretation` and `EdgeTypeArrayInterpretation`

## What Needs to Change

### In Design Document
1. Clarify that **nesting** is the mechanism (not "partition blocks")
2. Use **XTypeArrayInterpretation** as the fundamental recursive unit
3. Explain that arrays can have cardinality 1 or > 1

### In JSON Schema
1. Rename `PartitionBlockItemNode` → `NodeTypeArrayInterpretation`
2. Rename `PartitionBlockItemEdge` → `EdgeTypeArrayInterpretation`
3. Structure as recursive definition that resolves to array of element types
4. Support nesting (TI wrapping TI wrapping array)

### In Implementation Plan
1. Update Phase E description to use correct terminology
2. Clarify that we're implementing **nested array interpretations**, not "partition blocks"
3. Reference this document for context

## Open Questions

1. **Maximum nesting depth**: Design doc says 2 levels - is this enforced?
2. **Import interaction**: How do imports work with nested array interpretations?
3. **Canonicalization**: How are nested interpretations canonicalized?
4. **Override semantics**: When outer TI wraps inner TI, does outer override inner?

## References

- **Main Design**: `.kiro/specs/type-interpretation-wrappers/design.md`
- **Implementation Plan**: `SCHEMA-TI-FIX-IMPLEMENTATION-PLAN.md`
- **Current Schema**: `src/grasch/schemas/lex-2026.0.3.2.schema.json` (lines 813-1000)

## Next Steps

1. Discuss and refine this understanding with user
2. Update design document with correct terminology
3. Update implementation plan for Phase E
4. Refactor schema definitions to use correct names
5. Create test examples demonstrating nesting

---

**NOTE**: This document should be deleted once the concepts are properly integrated into the main design document and implementation plan.
