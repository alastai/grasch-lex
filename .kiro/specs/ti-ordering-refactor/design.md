# Design Document: Type Interpretation Ordering Refactor

**Version**: 1.0  
**Date**: 2024-12-02  
**Status**: Active Design Document  
**Related Requirements**: `.kiro/specs/ti-ordering-refactor/requirements.md`

## Overview

This document describes the design for refactoring the LEX-2026.0.3.2 JSON Schema to fix incorrect Type Interpretation (TI) wrapper ordering at 6 out of 8 locations. The refactoring will ensure TI wrappers appear BEFORE content (not after), enabling proper 0-level/1-level/2-level TI syntax support across all locations.

**Context**: This work completes the Type Interpretation implementation begun in `.kiro/specs/type-interpretation-wrappers/` and documented in `TI-SCHEMA-ORDERING-FIX-DESIGN.md`. During Phases A-D implementation (see `PHASES-A-D-COMPLETE.md`), we discovered that 6 out of 8 TI locations have wrong-order patterns. This spec defines the refactoring to fix those locations.

## Problem Statement

The current schema has TWO critical bugs:

### Bug 1: Wrong TI Wrapper Ordering
TI wrappers appear AFTER content properties at 6 locations, which breaks the fundamental TI architecture.

**Current (Wrong)**:
```yaml
nodeTypes:
  - exactlyOf:      # TI INSIDE array item
      concrete:
        typeLabel: Person
```

**Target (Correct)**:
```yaml
exactlyOf:          # TI OUTSIDE, wrapping nodeTypes
  concrete:
    nodeTypes:
      - typeLabel: Person
```

### Bug 2: Sibling TI Wrappers Rejected (CRITICAL)
The schema uses `patternProperties` that CONFLICT with regular `properties`, preventing multiple sibling `nodeTypes`/`edgeTypes` with different TI wrappers.

**Current (Broken)**:
```yaml
graphType:
  nodeTypes: [...]        # Regular property
  concrete:               # Pattern property - CONFLICTS!
    edgeTypes: [...]      # Schema rejects this as invalid
```

**Target (Required)**:
```yaml
graphType:
  nodeTypes: [...]        # Bare nodeTypes (0-level)
  abstract:               # TI-wrapped nodeTypes (sibling)
    nodeTypes: [...]
  edgeTypes: [...]        # Bare edgeTypes (0-level)
  concrete:               # TI-wrapped edgeTypes (sibling)
    edgeTypes: [...]
```

**Root Cause**: JSON Schema's `patternProperties` and regular `properties` with the same nested property names create conflicts. The schema needs to be restructured to allow BOTH bare properties AND TI-wrapped properties as siblings.

## Phase 2 Scope Summary - CORRECTED

**What Phase 2 Fixes**: **7 broken locations** (Locations 1-7) where TI wrappers are missing or in the wrong order.

**What Phase 2 Does NOT Fix**: 
- Location 8 (edgeTypeEndpointNodeTypeInterpretation) - Already working from previous phases

**Critical Discovery - Location 1 Needs Fixing**:
- GraphSchemaContent currently does NOT support TI wrappers around `graphType`
- It only allows ONE bare `graphType` property (enforced by `"additionalProperties": false`)
- **User Requirement**: TI wrappers (0/1/2-level) should be able to wrap the ONE `graphType`
- **Example needed**:
  ```yaml
  graphSchema:
    pathName: /mySchema
    # Option 1: Bare (0-level)
    graphType: { ... }
    # OR Option 2: 1-level TI
    abstract:
      graphType: { ... }
    # OR Option 3: 2-level TI
    subtypesOf:
      abstract:
        graphType: { ... }
  ```

**Locations 2-3 Clarification**:
- GraphType (the content WITHIN Location 1) already has correct `patternProperties` pattern
- BUT NodeTypesProperty and EdgeTypesProperty use wrong `oneOf` pattern
- **User Requirement**: Multiple `nodeTypes` and `edgeTypes` properties as siblings, each with its own TI wrapper
- **Example needed**:
  ```yaml
  graphType:
    nodeTypes: [...]        # Bare (0-level)
    abstract:               # 1-level TI (sibling)
      nodeTypes: [...]
    exactlyOf:              # 2-level TI (sibling)
      concrete:
        nodeTypes: [...]
  ```

**Reference Pattern**: GraphType's existing `patternProperties` implementation is the correct pattern to replicate.

## Architecture

### Three-Level TI System

Type Interpretations operate at three expression levels:

1. **0-Level (Bare)**: `typeLabel: Person` - No wrapper, implicit `exactlyOf:concrete:`
2. **1-Level (Shorthand)**: `abstract: { typeLabel: Person }` - One wrapper keyword
3. **2-Level (Explicit)**: `subtypesOf: { abstract: { typeLabel: Person } }` - Two wrapper keywords

This is implemented using JSON Schema `patternProperties` to match TI keywords.

### Eight TI Locations

The authoritative location taxonomy (from `TEMP-NESTING-IDEAS.md`):

| # | Location Name | Description | Current Status | Fix Required |
|---|---------------|-------------|----------------|--------------|
| 1 | `graphTypeInterpretation` | Wraps the graphType property | ✗ WRONG | Add TI support |
| 2 | `nodeTypesInterpretation` | Wraps ENTIRE nodeTypes array property | ✗ WRONG | Fix pattern |
| 3 | `edgeTypesInterpretation` | Wraps ENTIRE edgeTypes array property | ✗ WRONG | Fix pattern |
| 4 | `nodeTypeArrayInterpretation` | Wraps SUBSEQUENCE within nodeTypes array | ✗ WRONG | Reorder pattern |
| 5 | `edgeTypeArrayInterpretation` | Wraps SUBSEQUENCE within edgeTypes array | ✗ WRONG | Reorder pattern |
| 6 | `nodeTypeInterpretation` | Wraps a single nodeType | ✗ WRONG | Add TI support |
| 7 | `edgeTypeInterpretation` | Wraps a single edgeType | ✗ WRONG | Add TI support |
| 8 | `edgeTypeEndpointNodeTypeInterpretation` | Wraps endpoint references | ✓ CORRECT | None - already working |

**Phase 2 Scope - CORRECTED**: This refactoring fixes **7 broken locations** (1-7). Location 8 is already working from previous phases.

**Key Discovery**: Location 1 (GraphSchemaContent) does NOT currently support TI wrappers around `graphType`. It only allows ONE bare `graphType` property. We need to add `patternProperties` to enable TI wrappers.

**Reference Pattern**: GraphType (the CONTENT of Location 1) already has the correct `patternProperties` pattern. We'll use this as the reference for fixing all locations.

## Design Solution

### Core Pattern (from Location 1 - GraphType)

The correct pattern uses `patternProperties` to wrap content:

```json
{
  "properties": {
    "nodeTypes": {"type": "array", "items": {...}}
  },
  "patternProperties": {
    "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
      "oneOf": [
        {
          "properties": {
            "nodeTypes": {"type": "array", "items": {...}}
          }
        },
        {
          "patternProperties": {
            "^(abstract|concrete|final|sealed)$": {
              "properties": {
                "nodeTypes": {"type": "array", "items": {...}}
              }
            }
          }
        }
      ]
    }
  }
}
```

### Key Principles

1. **Wrapper Before Content**: `patternProperties` must appear at the same level as `properties`, wrapping the content property
2. **Two-Level Nesting**: Interpretation facet (outer) → Concreteness facet (inner) → Content property
3. **Pattern Consistency**: Same structure at all 8 locations
4. **Sibling Support**: Different interpretation facets can be siblings (YAML allows this)

## Component Design

### Schema Modifications (Phase 2 Scope: 7 Locations)

Phase 2 fixes **7 broken locations** identified during analysis. Location 8 is already working from previous implementation phases.

**Reference Pattern**: GraphType's `patternProperties` implementation (lines 433-800) is the correct pattern to use for all fixes.

#### Location 1: graphTypeInterpretation
**Current**: GraphSchemaContent only allows ONE bare `graphType` property  
**Target**: Add `patternProperties` to allow TI wrappers (0/1/2-level) around `graphType`  
**Change**: Add `patternProperties` pattern to GraphSchemaContent, similar to GraphType  
**Semantics**: TI wrappers can wrap the single `graphType` property  
**Phase 2 Task**: **NEW - Add TI support to GraphSchemaContent**

#### Location 2: nodeTypesInterpretation
**Current**: `nodeTypes` property with TI inside array items  
**Target**: `patternProperties` wrapping ENTIRE `nodeTypes` array property  
**Change**: Move TI pattern from array item level to property level  
**Semantics**: Wraps the complete nodeTypes collection  
**Phase 2 Task**: Fix this location

#### Location 3: edgeTypesInterpretation
**Current**: `edgeTypes` property with TI inside array items  
**Target**: `patternProperties` wrapping ENTIRE `edgeTypes` array property  
**Change**: Move TI pattern from array item level to property level  
**Semantics**: Wraps the complete edgeTypes collection  
**Phase 2 Task**: Fix this location

#### Location 4: nodeTypeArrayInterpretation
**Current**: Array items with TI inside item content  
**Target**: `patternProperties` wrapping SUBSEQUENCES within `nodeTypes` array  
**Change**: Restructure array item schema to support TI wrappers as partition blocks  
**Semantics**: Wraps subsequences (partition blocks) within the nodeTypes array  
**Phase 2 Task**: Fix this location

#### Location 5: edgeTypeArrayInterpretation
**Current**: Array items with TI inside item content  
**Target**: `patternProperties` wrapping SUBSEQUENCES within `edgeTypes` array  
**Change**: Restructure array item schema to support TI wrappers as partition blocks  
**Semantics**: Wraps subsequences (partition blocks) within the edgeTypes array  
**Phase 2 Task**: Fix this location

#### Location 6: nodeTypeInterpretation
**Current**: No TI support  
**Target**: Add `patternProperties` wrapping single NodeType content  
**Change**: Add complete TI pattern to NodeType definition  
**Semantics**: Wraps a single nodeType definition  
**Phase 2 Task**: Fix this location

#### Location 7: edgeTypeInterpretation
**Current**: No TI support  
**Target**: Add `patternProperties` wrapping single EdgeType content  
**Change**: Add complete TI pattern to EdgeType definition  
**Semantics**: Wraps a single edgeType definition  
**Phase 2 Task**: Fix this location

### Edge Label Container Structure (E02 Integration)

**Critical Prerequisite**: Before implementing TI wrappers at Locations 3, 5, and 7, edge label containers must be corrected.

**Current Issue**: Edge label containers (`via:`, `arc:`) are incorrectly defined as polymorphic (string OR object).

**Correct Structure**: Edge label containers are ALWAYS objects with `typeLabel:` as required child property.

**Pattern 1 - Simple Edge (No Properties)**:
```yaml
via:
  typeLabel: KNOWS  # Required child of via
```

**Pattern 2 - Edge with Properties**:
```yaml
via:
  typeLabel: KNOWS  # Required child
  implies:          # Sibling to typeLabel
    propertyTypes:
      - name: since
        valueType: INTEGER
```

**Pattern 3 - Edge with Subtyping**:
```yaml
via:
  typeLabel: KNOWS
  extends: RELATIONSHIP  # Sibling to typeLabel
  adding:                # Sibling to extends
    propertyTypes:
      - name: since
        valueType: INTEGER
```

**Schema Changes Required**:
1. Redefine `via:` and `arc:` as ALWAYS objects (not oneOf string/object)
2. Make `typeLabel:` a REQUIRED child property
3. Remove `typeLabel:` from synonym group (it's now a child property only)
4. Move `implies:`, `extends:`, `adding:` to be children of edge label container

**Rationale**: This makes edge label containers consistent with `nodeType` pattern (always an object with `typeLabel:` child).

### Test File Updates

Test YAML files currently use wrong-order syntax because they were written for the broken schema. After fixing the schema, these files must be updated:

**Files Requiring Updates**:
- `src/grasch/examples/test-phase-e-location-2*.yaml`
- `src/grasch/examples/test-phase-e-location-3*.yaml`
- `src/grasch/examples/test-phase-e-locations-2-3*.yaml`
- `src/grasch/examples/test-phase-e-locations-4-5*.yaml`
- Any other files using array-level TI wrappers

**Update Pattern**:
- Move TI wrappers from inside content to outside content
- Preserve semantic meaning
- Maintain test coverage

### Sibling TI Wrapper Support - Schema Fix Required

**THE CRITICAL FIX**: The schema must be restructured to allow `patternProperties` to coexist with regular `properties` without conflicts. This requires:

1. **Remove `additionalProperties: false`** constraints that prevent pattern properties
2. **Allow multiple properties with same name** at different nesting levels (bare vs wrapped)
3. **Use `unevaluatedProperties: false`** instead of `additionalProperties: false` where needed
4. **Test extensively** with positive and negative test cases

The schema will support multiple sibling TI wrappers with different interpretation facets at multiple levels:

**Location 1 (graphTypeInterpretation) - Siblings at GraphType Level**:
```yaml
graphType:
  nodeTypes:        # Bare nodeTypes (Location 2)
    - typeLabel: Person
  exactlyOf:        # TI-wrapped nodeTypes (sibling to bare)
    concrete:
      nodeTypes:
        - typeLabel: Company
  edgeTypes:        # Bare edgeTypes (Location 3)
    - typeLabel: WORKS_FOR
  subtypesOf:       # TI-wrapped edgeTypes (sibling to bare)
    abstract:
      edgeTypes:
        - typeLabel: RELATIONSHIP
```

**Locations 2-3 (nodeTypesInterpretation/edgeTypesInterpretation) - Multiple Array Interpretations as Siblings**:
```yaml
nodeTypes:          # Bare nodeTypes array
  - typeLabel: Person
exactlyOf:          # TI-wrapped nodeTypes array (sibling)
  concrete:
    nodeTypes:
      - typeLabel: Company
subtypesOf:         # Another TI-wrapped nodeTypes array (sibling)
  abstract:
    nodeTypes:
      - typeLabel: Entity
```

**Locations 4-5 (nodeTypeArrayInterpretation/edgeTypeArrayInterpretation) - Multiple Item Interpretations as Siblings**:
```yaml
nodeTypes:          # Array containing multiple interpretations as siblings
  - typeLabel: Person                    # Bare item
  - exactlyOf:                          # TI-wrapped item (sibling)
      concrete:
        typeLabel: Company
  - subtypesOf:                         # Another TI-wrapped item (sibling)
      abstract:
        typeLabel: Entity
```

**Invalid (YAML Constraint)**:
```yaml
nodeTypes:
  - typeLabel: Person
exactlyOf:          # Same interpretation facet
  concrete:
    nodeTypes:
      - typeLabel: Company
exactlyOf:          # ERROR: Duplicate YAML key
  abstract:
    nodeTypes:
      - typeLabel: Entity
```

## Data Models

### Schema Structure

```
GraphSchema
├── properties
│   ├── nodeTypes: array
│   └── edgeTypes: array
└── patternProperties
    └── ^(exactlyOf|subtypesOf|properSubtypesOf)$
        └── oneOf
            ├── properties (1-level shorthand)
            │   ├── nodeTypes: array
            │   └── edgeTypes: array
            └── patternProperties (2-level explicit)
                └── ^(abstract|concrete|final|sealed)$
                    └── properties
                        ├── nodeTypes: array
                        └── edgeTypes: array
```

### Validation Flow

1. **Pre-Canonical Validation**: YAML file validates against schema (with TI wrappers)
2. **Canonicalization**: Preprocessor normalizes to 2-level explicit form
3. **Canonical Validation**: Normalized form validates against same schema
4. **Semantic Validation**: Business rules applied to canonical form

## Error Handling

### Schema Validation Errors

**Wrong-Order Syntax**:
- Error: "Additional properties not allowed"
- Cause: TI wrapper inside content instead of outside
- Fix: Move TI wrapper to correct level

**Duplicate Interpretation Facets**:
- Error: "Duplicate key in YAML"
- Cause: Same interpretation facet appears twice
- Fix: Use different interpretation facets or nest under one

**Missing Content**:
- Error: "Required property missing"
- Cause: TI wrapper without content property
- Fix: Add content property inside TI wrapper

### Test Validation Strategy

1. **Expect Failures**: After schema fix, wrong-syntax tests will fail (this is correct)
2. **Identify Failures**: Run validation to find which files need updates
3. **Update Syntax**: Fix YAML files to use correct TI placement
4. **Re-validate**: Confirm all tests pass with corrected syntax
5. **Regression Check**: Verify Phases A-D still work (should be unchanged)

## Testing Strategy

### Unit Tests

**Schema Structure Tests**:
- Verify `patternProperties` at correct level
- Verify content properties inside wrappers
- Verify 0/1/2-level syntax support

**Location-Specific Tests**:
- Test each of 8 locations independently
- Test 0-level, 1-level, 2-level at each location
- Test sibling patterns at each location

### Integration Tests

**Cross-Location Tests**:
- Test TI at multiple locations simultaneously
- Test nested TI (e.g., GraphType + NodeTypeItem)
- Test mixed bare and wrapped syntax

**Sibling Behavior Tests**:
- Test multiple different interpretation facets as siblings
- Test YAML duplicate key prevention
- Test nested concreteness facets

### Validation Tests

**Positive Tests** (should pass):
- `test-siblings-graphtype-level.yaml`
- `test-siblings-array-level.yaml`
- `test-siblings-mixed.yaml`
- All Phase A-D test files (unchanged)

**Negative Tests** (should fail):
- `test-siblings-duplicate-nodetypes-INVALID.yaml`
- `test-siblings-duplicate-interpretation-INVALID.yaml`

## Implementation Phases

### Phase 1: Schema Analysis (1 hour)
1. Read Location 1 (GraphType) pattern in detail
2. Identify exact line numbers for Locations 2-7
3. Document current vs. target structure for each location
4. Create backup of original schema

### Phase 2: Schema Fixes (3-4 hours)
1. Fix Location 2 (NodeTypesProperty)
2. Fix Location 3 (EdgeTypesProperty)
3. Fix Location 4 (NodeTypeItem)
4. Fix Location 5 (EdgeTypeItem)
5. Fix Location 6 (Individual NodeType)
6. Fix Location 7 (EdgeType Content)
7. Test after each fix

### Phase 3: Test File Updates (2-3 hours)
1. Run validation to identify failing files
2. Update Phase E test files to correct syntax
3. Create sibling behavior test files
4. Validate all updated files

### Phase 4: Validation & Documentation (1-2 hours)
1. Run comprehensive validation suite
2. Verify Phases A-D still pass
3. Document changes and results
4. Create completion summary

## Success Criteria

1. ✓ All 8 locations support 0/1/2-level TI syntax
2. ✓ TI wrappers appear BEFORE content at all locations
3. ✓ Multiple siblings with different interpretation facets work
4. ✓ YAML duplicate key constraint properly enforced
5. ✓ All test files validate with corrected syntax
6. ✓ Phases A-D validation still passes (no regressions)
7. ✓ Sibling behavior tests pass

## Risks & Mitigation

**Risk**: Breaking existing valid YAML files  
**Mitigation**: Files using correct syntax will continue to work; only wrong-syntax files need updates

**Risk**: Introducing new validation errors  
**Mitigation**: Test incrementally after each location fix; maintain backup

**Risk**: Sibling behavior not working as expected  
**Mitigation**: Comprehensive sibling tests; validate against YAML spec

**Risk**: Preprocessor incompatibility  
**Mitigation**: Preprocessor already handles correct syntax; no changes needed

## Relationship to Existing Work

This design document is part of the broader Type Interpretation implementation effort documented in:

**Parent Specifications**:
- `.kiro/specs/type-interpretation-wrappers/` - Original TI wrapper system spec
- `.kiro/specs/type-interpretation-flexibility/` - TI flexibility requirements

**Authoritative Design Documents**:
- `TI-SCHEMA-ORDERING-FIX-DESIGN.md` - Root-level design (this spec implements it)
- `LEX-2026.0.3.2-INTERPRETATION-DESCRIPTORS.md` - Official TI specification
- `TI-IMPLEMENTATION-ROADMAP.md` - Overall TI implementation plan

**Implementation Context**:
- `PHASES-A-D-COMPLETE.md` - Completed work (Locations 6, 7, 8 working)
- `PHASE-E-IMPLEMENTATION-PLAN.md` - Array-level TI (what we're fixing)
- `MORNING-CHECKPOINT-TI-ORDERING-FIX.md` - Ready-to-execute checkpoint

**Related Specs**:
- `.kiro/specs/type-interpretation-wrappers/design.md` - Original TI design
- `.kiro/specs/type-interpretation-wrappers/tasks.md` - Original TI tasks

This refactoring completes the TI implementation by fixing the 6 broken locations identified during Phases A-D implementation.
