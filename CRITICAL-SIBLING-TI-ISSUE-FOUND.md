# CRITICAL: Sibling TI Wrappers Not Supported

**Date**: 2024-12-06  
**Severity**: CRITICAL - Blocks Phase E implementation  
**Status**: Schema design flaw identified

## Problem Statement

The current GraphType schema **does NOT support** sibling TI wrappers with different interpretation facets, such as:

```yaml
graphType:
  abstract:           # 1-level TI wrapper
    nodeTypes: [...]
  concrete:           # Different 1-level TI wrapper (sibling)
    edgeTypes: [...]
```

## Current Schema Structure

The GraphType schema (lines 589-750) has this structure:

```json
{
  "properties": {
    "nodeTypes": {...},        // Bare property
    "subtypesOf": {            // Interpretation facet property
      "properties": {
        "abstract": {          // Concreteness facet nested INSIDE
          "properties": {
            "nodeTypes": {...},
            "edgeTypes": {...}
          }
        },
        "nodeTypes": {...}     // Also nested inside subtypesOf
      }
    }
  }
}
```

This means:
- ❌ Cannot have `abstract: { nodeTypes: [...] }` at GraphType level
- ❌ Cannot have `concrete: { edgeTypes: [...] }` at GraphType level
- ❌ Cannot mix different TI wrappers as siblings
- ✅ Can only have `subtypesOf: { abstract: { nodeTypes: [...] } }`

## What We Need

According to the design document and user requirements, we need:

```yaml
graphType:
  # 0-level (bare)
  nodeTypes: [...]
  
  # 1-level TI wrappers as siblings
  abstract:
    nodeTypes: [...]
  
  concrete:
    edgeTypes: [...]
  
  # 2-level TI wrappers as siblings
  exactlyOf:
    concrete:
      nodeTypes: [...]
  
  subtypesOf:
    abstract:
      edgeTypes: [...]
```

## Root Cause

The schema uses a **nested structure** where:
1. Interpretation facets (`exactlyOf`, `subtypesOf`, `properSubtypesOf`) are properties
2. Concreteness facets (`abstract`, `concrete`) are nested inside interpretation facets
3. Content properties (`nodeTypes`, `edgeTypes`) are nested inside concreteness facets

This prevents having `abstract:` or `concrete:` as **top-level siblings** at the GraphType level.

## Required Fix

The schema needs to use `patternProperties` to match TI keywords at the GraphType level:

```json
{
  "properties": {
    "nodeTypes": {...},
    "edgeTypes": {...}
  },
  "patternProperties": {
    "^(abstract|concrete)$": {
      "type": "object",
      "properties": {
        "nodeTypes": {...},
        "edgeTypes": {...}
      }
    },
    "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
      "type": "object",
      "patternProperties": {
        "^(abstract|concrete)$": {
          "type": "object",
          "properties": {
            "nodeTypes": {...},
            "edgeTypes": {...}
          }
        }
      }
    }
  }
}
```

## Impact

**This affects ALL TI locations (2-7)**:
- Location 2 (nodeTypesInterpretation) - Cannot wrap nodeTypes property
- Location 3 (edgeTypesInterpretation) - Cannot wrap edgeTypes property  
- Locations 4-7 - Similar issues

**This is why Task 11 validation failed** - the test files use correct syntax that the schema doesn't support yet.

## Action Required

1. **Immediate**: Update design.md to clarify this is a schema bug, not a test file issue
2. **Task 8-16**: Must implement `patternProperties` pattern at ALL locations
3. **Critical**: This is not just "fixing wrong order" - it's implementing a completely different schema pattern

## Test Results

Ran `test_sibling_ti_wrappers.py`:
- ❌ Test 1: `abstract:nodeTypes` + `concrete:edgeTypes` as siblings - FAILS
- ❌ Test 2: bare `nodeTypes` + `concrete:edgeTypes` - FAILS
- ❌ Test 3: `subtypesOf:abstract` with both nested - FAILS (edge syntax issue)

**Conclusion**: The schema fundamentally does not support the TI wrapper pattern described in the design document.

## Next Steps

1. Re-read the schema more carefully to understand current pattern
2. Design the correct `patternProperties` structure
3. Implement at Location 2 first (as reference)
4. Apply same pattern to Locations 3-7
5. Update all test files to match working pattern
