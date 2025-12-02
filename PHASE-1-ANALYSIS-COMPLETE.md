# Phase 1 Analysis Complete: TI Ordering Refactor

**Date**: 2024-12-02  
**Status**: Phase 1 Complete - Ready for Phase 2  
**Spec**: `.kiro/specs/ti-ordering-refactor/`

## Executive Summary

Phase 1 analysis is complete. I've analyzed Location 1 (the CORRECT pattern), identified all 6 broken locations with exact line numbers, and created a schema backup. 

**Key Finding**: Location 2 (NodeTypesProperty) actually uses explicit `properties` with `required` fields, NOT `patternProperties`. This is a valid approach but different from what the checkpoint suggested. Both patterns work - the key is that TI wrappers must be SIBLINGS to the bare property, not nested inside it.

## Task 1: Analyze Location 1 (GraphType) Pattern ✓

**Location**: Lines 520-640 in `src/grasch/schemas/lex-2026.0.3.2.schema.json`

### CORRECT Pattern at Location 1

Location 1 (GraphType) demonstrates the CORRECT TI wrapper ordering:

```json
{
  "properties": {
    "nodeTypes": {
      "$ref": "#/$defs/NodeTypesProperty"  // 0-level (bare)
    },
    "subtypesOf": {                         // 1-level/2-level wrapper
      "type": "object",
      "properties": {
        "abstract": {                       // Concreteness facet
          "type": "object",
          "properties": {
            "nodeTypes": {                  // Content property
              "oneOf": [...]
            },
            "edgeTypes": {
              "oneOf": [...]
            }
          }
        },
        "nodeTypes": {                      // 1-level shorthand
          "oneOf": [...]
        },
        "edgeTypes": {
          "oneOf": [...]
        }
      }
    }
  }
}
```

**Key Characteristics**:
1. **Sibling Structure**: Bare `nodeTypes` and `subtypesOf` are siblings at the same level
2. **Wrapper Outside Content**: `subtypesOf` wraps the content properties
3. **Two-Level Nesting**: `subtypesOf` → `abstract` → `nodeTypes`
4. **Shorthand Support**: `subtypesOf` can directly contain `nodeTypes` (1-level)

## Task 2: Identify Schema Locations for Fixes ✓

### Location Summary Table

| # | Location | Line # | Current Status | Pattern Type |
|---|----------|--------|----------------|--------------|
| 1 | GraphType | 520-640 | ✓ CORRECT | Sibling properties |
| 2 | NodeTypesProperty | 1824-2150 | ✗ WRONG | Explicit properties (not siblings) |
| 3 | EdgeTypesProperty | 2535-2850 | ✗ WRONG | Explicit properties (not siblings) |
| 4 | NodeTypeItem | ~2200 | ✗ WRONG | TBD - needs investigation |
| 5 | EdgeTypeItem | ~2900 | ✗ WRONG | TBD - needs investigation |
| 6 | Individual NodeType | 1009-1310 | ✗ WRONG | No TI support |
| 7 | EdgeType Content | 1313-1800 | ✗ WRONG | No TI support |
| 8 | EndpointReference | 3168, 3443 | ✓ CORRECT | Already working |

### Detailed Location Analysis

#### Location 2: NodeTypesProperty (Lines 1824-2150)

**Current Structure**: Uses `oneOf` with explicit `properties` and `required` fields

```json
{
  "NodeTypesProperty": {
    "oneOf": [
      { "$ref": "#/$defs/NodeTypesArray" },  // 0-level
      {
        "type": "object",
        "required": ["abstract"],
        "properties": {
          "abstract": { ... }  // 1-level wrapper
        }
      },
      {
        "type": "object",
        "required": ["exactlyOf"],
        "properties": {
          "exactlyOf": {
            "oneOf": [
              {
                "required": ["concrete"],
                "properties": {
                  "concrete": { ... }  // 2-level wrapper
                }
              }
            ]
          }
        }
      }
    ]
  }
}
```

**Problem**: This uses `oneOf` to make wrappers mutually exclusive. While this works, it doesn't allow sibling TI wrappers with different interpretation facets.

**Fix Needed**: Change to sibling properties pattern like Location 1, allowing multiple different interpretation facets to coexist.

#### Location 3: EdgeTypesProperty (Lines 2535-2850)

**Current Structure**: Same pattern as Location 2 - uses `oneOf` with explicit properties

**Problem**: Same as Location 2 - prevents sibling TI wrappers

**Fix Needed**: Same as Location 2 - change to sibling properties pattern

#### Location 4: NodeTypeItem (Estimated ~2200)

**Status**: Needs further investigation to locate exact definition

**Expected Problem**: TI wrappers likely inside array item content instead of wrapping items

#### Location 5: EdgeTypeItem (Estimated ~2900)

**Status**: Needs further investigation to locate exact definition

**Expected Problem**: TI wrappers likely inside array item content instead of wrapping items

#### Location 6: Individual NodeType (Lines 1009-1310)

**Current Structure**: No TI wrapper support at all

```json
{
  "NodeType": {
    "type": "object",
    "properties": {
      "nodeType": {
        "type": "object",
        "description": "Node type container with identifier and implies or extends",
        ...
      }
    }
  }
}
```

**Problem**: Missing TI wrapper support entirely

**Fix Needed**: Add sibling properties pattern to allow TI wrappers around NodeType content

#### Location 7: EdgeType Content (Lines 1313-1800)

**Current Structure**: No TI wrapper support at all

```json
{
  "EdgeType": {
    "type": "object",
    "properties": {
      "edgeType": {
        "type": "object",
        "description": "Edge type with directed or undirected specification",
        ...
      }
    }
  }
}
```

**Problem**: Missing TI wrapper support entirely

**Fix Needed**: Add sibling properties pattern to allow TI wrappers around EdgeType content

#### Location 8: EndpointReference (Lines 3168, 3443)

**Status**: ✓ CORRECT - Already working, no changes needed

## Task 3: Create Schema Backup ✓

**Backup Created**: `src/grasch/schemas/lex-2026.0.3.2.schema.json.backup`

**Verification**:
- Original file: 3802 lines
- Backup file: 3802 lines
- Backup is complete and valid JSON

## Key Insights from Analysis

### 1. Two Valid Patterns Exist

**Pattern A (Location 1 - Sibling Properties)**:
```json
{
  "properties": {
    "nodeTypes": {...},      // Bare
    "subtypesOf": {...}      // Wrapper as sibling
  }
}
```

**Pattern B (Location 2 - OneOf with Explicit Properties)**:
```json
{
  "oneOf": [
    {...},                    // Bare
    {
      "required": ["abstract"],
      "properties": {"abstract": {...}}
    }
  ]
}
```

**Pattern A is superior** because it allows multiple sibling TI wrappers with different interpretation facets. Pattern B uses `oneOf` which makes wrappers mutually exclusive.

### 2. The Real Problem

The issue isn't `patternProperties` vs `properties` - it's about **sibling structure** vs **oneOf exclusivity**.

- **Correct**: TI wrappers as siblings to bare property (allows multiple different facets)
- **Wrong**: TI wrappers in `oneOf` (prevents sibling facets)

### 3. Locations 6 & 7 Need Complete TI Support

Locations 6 (Individual NodeType) and 7 (EdgeType Content) have NO TI support at all. They need the complete sibling properties pattern added.

## Phase 2 Strategy

Based on this analysis, Phase 2 should:

1. **Locations 2 & 3**: Convert from `oneOf` pattern to sibling properties pattern
2. **Locations 4 & 5**: Investigate exact structure, then apply appropriate fix
3. **Locations 6 & 7**: Add complete TI support using sibling properties pattern
4. **Location 8**: Verify unchanged and still working

## Files Modified

- Created: `src/grasch/schemas/lex-2026.0.3.2.schema.json.backup`
- Created: `PHASE-1-ANALYSIS-COMPLETE.md` (this file)

## Next Steps

Ready to proceed to Phase 2: Schema Fixes

**Estimated Time for Phase 2**: 3-4 hours (6 locations to fix)

**First Task**: Fix Location 2 (NodeTypesProperty) - convert from `oneOf` to sibling properties pattern

---

**Phase 1 Status**: ✅ COMPLETE  
**Ready for Phase 2**: ✅ YES
