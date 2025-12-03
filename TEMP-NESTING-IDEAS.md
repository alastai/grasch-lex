# TEMPORARY: Array Type Interpretation Nesting Concepts

**STATUS**: PROVISIONAL - Progressive Refinement in Design Discussion Phase  
**DATE**: 2024-11-29 (Updated)  
**PURPOSE**: Capture evolving understanding of array-level TI structure before finalizing design

**CRITICAL**: This document represents work-in-progress design discussion. NO schema changes should be made until:
1. We complete understanding of TI usage patterns (Locations 1-9)
2. We finalize nested TI semantics (defaults, overrides)
3. We determine how TIs interact with imports
4. User explicitly approves moving to implementation

This is a step in progressive refinement to preserve context across sessions.

## Correct Location Numbering (Authoritative)

**Source**: `PHASES-A-D-DONE.md`, `TI-ARCHITECTURE-SPEC-UPDATE.md`

The authoritative Location numbering for Type Interpretation positions is:

1. **Location 1**: `graphTypeInterpretation` - for the graphType property
2. **Location 2**: `nodeTypesInterpretation` - for nodeTypes arrays (entire collection)
3. **Location 3**: `edgeTypesInterpretation` - for edgeTypes arrays (entire collection)
4. **Location 4**: `nodeTypeArrayInterpretation` - for subsequence within nodeTypes array
5. **Location 5**: `edgeTypeArrayInterpretation` - for subsequence within edgeTypes array
6. **Location 6**: `nodeTypeInterpretation` - for a single nodeType ✅ COMPLETE
7. **Location 7**: `edgeTypeInterpretation` - for a single edgeType ✅ COMPLETE
8. **Location 8**: `edgeTypeEndpointNodeTypeInterpretation` - undirected endpoints ✅ COMPLETE
9. **Location 9**: `edgeTypeEndpointNodeTypeInterpretation` - directed endpoints ✅ COMPLETE

**Note**: `SCHEMA-TI-FIX-IMPLEMENTATION-PLAN.md` contains a DIFFERENT numbering that includes import-related locations. That numbering is INCORRECT for our purposes. Use the above numbering.

## Key Insight: XTypeInterpretation as Recursive Unit

The fundamental unit for array-level type interpretation is **XTypeInterpretation** where X ∈ {nodeType, edgeType}.

### Terminology Alignment

- **Location 2: nodeTypesInterpretation**: Wraps the ENTIRE nodeTypes property/array
- **Location 4: nodeTypeArrayInterpretation**: Wraps a SUBSEQUENCE within the nodeTypes array (recursive unit)
- **Location 3: edgeTypesInterpretation**: Wraps the ENTIRE edgeTypes property/array
- **Location 5: edgeTypeArrayInterpretation**: Wraps a SUBSEQUENCE within the edgeTypes array (recursive unit)

### Structure

An XTypeInterpretation:
1. **Can be nested** (TI wrapping another TI)
2. **Eventually resolves to an array of element types** (which may contain only one element)
3. **Supersedes the "partition block" concept** - nesting is the mechanism, not partitioning

### YAML Examples - Refined Understanding from Prior Session

**User Input (Prior Session)**: Showing the broader picture of Locations 1-5

```yaml
# Location 2: nodeTypesInterpretation (wraps whole nodeTypes property)
# 1-level wrapper around entire array
abstract:
  nodeTypes:
    - nodeType: Person  # Only one element shown, but wraps the whole array

# Location 4: nodeTypeArrayInterpretation (wraps subsequences)
# Two separate subsequences, each with its own interpretation
nodeTypes:
  abstract:
    - nodeType: Person 
    - nodeType: Company
  concrete:
    - nodeType: City

# Location 4: nodeTypeArrayInterpretation (1-level nesting)
# Wrapper around a subsequence within the nodeTypes array
nodeTypes:
  - abstract:
      nodeTypes:  # This subsequence is what the TI interprets
        - nodeType: Vehicle
        - nodeType: Car

# Location 4: nodeTypeArrayInterpretation (2-level nested)
# Multiple nested interpretations within the array
nodeTypes:
  - subtypesOf:
      abstract:
        - nodeType: Message
        - nodeType: Post
  - exactlyOf:
      concrete:
        - nodeType: Company

# Example: Mixed - multiple interpretations in same array
nodeTypes:
  - nodeType: Person  # Bare (0-level, Location 6)
  - abstract:         # 1-level interpretation (Location 4)
      nodeTypes:
        - nodeType: Vehicle
        - nodeType: Car
  - subtypesOf:       # 2-level nested interpretation (Location 4)
      abstract:
        nodeTypes:
          - nodeType: Message
          - nodeType: Post
```

**Key Distinction** (from user's refined examples):
- **Location 2** (`nodeTypesInterpretation`): Wraps the WHOLE `nodeTypes` property
- **Location 4** (`nodeTypeArrayInterpretation`): Wraps SUBSEQUENCES within the `nodeTypes` array
- These are DIFFERENT locations with DIFFERENT purposes

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

## Discrepancy: Implementation Plan vs Correct Numbering

**IMPORTANT**: `SCHEMA-TI-FIX-IMPLEMENTATION-PLAN.md` uses a DIFFERENT numbering scheme:

**Implementation Plan Numbering** (INCORRECT for our purposes):
1. Location 1: `graphSchema.graphType.typeInterpretation` (root-level TI)
2. Location 2: `graphSchema.graphType.import` (import-level TI)
3. Location 3: `graphSchema.graphType.import.typeInterpretation` (import TI content)
4. Location 4: `graphSchema.graphType.nodeTypes` (nodeTypes array TI)
5. Location 5: `graphSchema.graphType.edgeTypes` (edgeTypes array TI)
6. Location 6: Individual `NodeType.typeInterpretation` (single node TI)
7. Location 7: Individual `EdgeType.typeInterpretation` (single edge TI)
8. Location 8: `EdgeType.endpoints[].typeInterpretation` (endpoint TI)
9. Location 9: `EdgeType.endpoints[].directed.typeInterpretation` (directed endpoint TI)

**Correct Numbering** (from PHASES-A-D-DONE.md):
- Locations 2-3 in implementation plan are about IMPORTS
- Our Locations 2-3 are about nodeTypes/edgeTypes arrays
- Our Locations 4-5 are about array subsequences
- Implementation plan doesn't distinguish between whole-array and subsequence interpretations

**Action Required**: Implementation plan needs to be updated to use correct numbering once design is finalized.

## Current Schema Issues

The existing schema uses incorrect terminology:
- ❌ `PartitionBlockItemNode` - implies partitioning, not nesting
- ❌ `PartitionBlockItemEdge` - implies partitioning, not nesting
- ✅ Should be: `NodeTypeArrayInterpretation` and `EdgeTypeArrayInterpretation`

## What Needs to Change (AFTER Design Finalization)

### In Design Document
1. Clarify that **nesting** is the mechanism (not "partition blocks")
2. Use **XTypeArrayInterpretation** as the fundamental recursive unit
3. Explain that arrays can have cardinality 1 or > 1
4. Distinguish Location 2 (whole array) from Location 4 (subsequences)
5. Add examples for all Locations 1-5

### In JSON Schema
1. Rename `PartitionBlockItemNode` → `NodeTypeArrayInterpretation`
2. Rename `PartitionBlockItemEdge` → `EdgeTypeArrayInterpretation`
3. Structure as recursive definition that resolves to array of element types
4. Support nesting (TI wrapping TI wrapping array)
5. Support both whole-array (Locations 2-3) and subsequence (Locations 4-5) patterns

### In Implementation Plan
1. Update to use correct Location numbering (1-9 as documented here)
2. Update Phase E description to use correct terminology
3. Clarify that we're implementing **nested array interpretations**, not "partition blocks"
4. Add phases for Locations 1-3 (currently missing)
5. Reference this document for context

## Open Questions

1. **Maximum nesting depth**: Design doc says 2 levels - is this enforced?
2. **Import interaction**: How do imports work with nested array interpretations?
3. **Canonicalization**: How are nested interpretations canonicalized?
4. **Override semantics**: When outer TI wraps inner TI, does outer override inner?

## Progressive Refinement Roadmap (Phase E Sub-phases)

**Context**: We are in PHASE E of the larger implementation plan (TIs and imports). This design discussion follows three sub-phases:

### Phase E.A: TI Usage Patterns (Locations 1-9) - IN PROGRESS
**Goal**: Understand how TIs are used at each of the 9 locations

**Current Understanding**:
- Locations 6-9: ✅ COMPLETE (individual element types and endpoints)
- Locations 1-5: 🔄 IN DISCUSSION (array-level and graph-level interpretations)

**Key Questions**:
- How does Location 2 (nodeTypesInterpretation) differ from Location 4 (nodeTypeArrayInterpretation)?
- What are the YAML syntax patterns for each location?
- What are the use cases for each location?

### Phase E.B: Nested TI Semantics (Defaults & Overrides) - PENDING
**Goal**: Finalize how TIs interact when nested

**Key Questions**:
- When does TI Override apply? (outer TI knocks out inner TI)
- When does TI Default Cascade apply? (higher-level TI establishes defaults)
- How do these interact with the recursive nodeTypeArrayInterpretation?
- What are the precedence rules?

### Phase E.C: TI and Import Interaction - PENDING
**Goal**: Determine how TIs interact with import system

**Key Questions**:
- How do imports affect TI interpretation?
- Can imports bring in TI wrappers?
- How does Phase 1 vs Phase 2 import affect TIs?

## References

- **Authoritative Location Numbering**: `PHASES-A-D-DONE.md`, `TI-ARCHITECTURE-SPEC-UPDATE.md`
- **Main Design**: `.kiro/specs/type-interpretation-wrappers/design.md`
- **Implementation Plan**: `SCHEMA-TI-FIX-IMPLEMENTATION-PLAN.md` (⚠️ uses different numbering)
- **Current Schema**: `src/grasch/schemas/lex-2026.0.3.2.schema.json` (lines 813-1000)

## Session Continuity

**Context Preservation**: This document captures the current state of design discussion to enable continuation across sessions:

1. **Correct Location Numbering**: Established and documented (Locations 1-9)
2. **Current Phase**: Phase E.A - Understanding TI usage patterns at Locations 1-5
3. **Prior Session Input**: User provided refined YAML examples showing distinction between:
   - `nodeTypesInterpretation` (Location 2) - wraps whole nodeTypes property
   - `nodeTypeArrayInterpretation` (Location 4) - wraps subsequences within array
4. **Next Steps**: Complete Phase E.A before moving to Phase E.B (nested semantics)

## User Guidance from Current Session

**From User Prompt (2024-11-29)**:
> "The ground rules are we are in a design discussion and you should not make any decisions or change anything before I have given you input and agreed to your proposed changes. Here we are looking at some prior input and trying to establish continuity. The task at the end (but read everything before, and absorb it) is to track down a prior numbering scheme for type interpretation locations. We want to use the old scheme, and modify or supplement it for this discussion but numbering is just a technical artefact to get straight, to improve our ability to have an organized discourse. It is not the main point."

**Key Principles**:
- This is a design discussion, not implementation
- No changes without user approval
- Numbering is a technical artifact for organized discourse
- Real focus is conceptual understanding
- Must complete: (a) TI usage, (b) nested semantics, (c) import interaction
- Then we can proceed to schema changes

---

**NOTE**: This document should be deleted once the concepts are properly integrated into the main design document and implementation plan, after completing Phases E.A, E.B, and E.C.
