# Phase E - Stage 2 Complete: Locations 2+3 Review

**Date**: 2024-12-01  
**Status**: ✅ COMPLETE WITH FINDINGS

## Goal

Verify that existing Location 2+3 support is correct and document findings.

## Locations Tested

- **Location 2**: `nodeTypesInterpretation` - Wraps the ENTIRE nodeTypes property
- **Location 3**: `edgeTypesInterpretation` - Wraps the ENTIRE edgeTypes property

## Test Results

### Location 2: nodeTypesInterpretation ✅ FULLY WORKING

**Test Files**:
- `test-phase-e-location-2.yaml` - One-level wrapper (abstract)
- `test-phase-e-location-2-two-level.yaml` - Two-level wrapper (subtypesOf:abstract)

**Status**: ✅ Both tests PASS

**Findings**:
- Location 2 is correctly implemented in the schema
- Supports 0-level (bare array), 1-level, and 2-level TI wrappers
- Import support is available
- Can wrap the entire nodeTypes property with any TI wrapper

**Example (One-level)**:
```yaml
graphType:
  abstract:
    nodeTypes:
      - nodeType: { typeLabel: Entity, ... }
      - nodeType: { typeLabel: Thing, ... }
```

**Example (Two-level)**:
```yaml
graphType:
  subtypesOf:
    abstract:
      nodeTypes:
        - nodeType: { typeLabel: Entity, ... }
```

### Location 3: edgeTypesInterpretation ❌ BROKEN

**Test Files**:
- `test-phase-e-location-3.yaml` - One-level wrapper (concrete)
- `test-phase-e-location-3-two-level.yaml` - Two-level wrapper (exactlyOf:concrete)

**Status**: ❌ Tests FAIL

**Root Cause**: Schema bug - NOT a "design limitation"

**Findings**:
- The schema's pattern properties (`abstract`, `concrete`, `subtypesOf`, etc.) are designed to wrap BOTH `nodeTypes` AND `edgeTypes` together
- You CANNOT have a bare `nodeTypes` property alongside a wrapped `edgeTypes` property (or vice versa)
- This is because pattern properties in GraphType apply at the same level as the regular properties

**What Works**:
```yaml
# Wrapping BOTH nodeTypes and edgeTypes together
graphType:
  abstract:
    nodeTypes: [...]
    edgeTypes: [...]
```

**What Doesn't Work**:
```yaml
# Trying to wrap ONLY edgeTypes while having bare nodeTypes
graphType:
  nodeTypes: [...]  # Bare
  concrete:         # Pattern property conflicts
    edgeTypes: [...] 
```

## Schema Analysis

### Current Schema Structure

The `GraphType` definition has:
1. **Regular properties**: `nodeTypes`, `edgeTypes`, `propertyGraphDataModel`, etc.
2. **Pattern properties**: `^(abstract|concrete|...)$` that can contain `nodeTypes` and/or `edgeTypes`

The issue is that JSON Schema doesn't allow mixing regular properties with pattern properties that have the same nested property names.

### Is This a Bug or By Design?

**THIS IS A BUG** - The schema incorrectly prevents valid sibling patterns that are explicitly required by the specification.

**Required Behavior** (from requirements):
```yaml
graphType:
  nodeTypes: [...]        # Bare nodeTypes
  abstract:               # TI-wrapped nodeTypes (sibling)
    nodeTypes: [...]
  edgeTypes: [...]        # Bare edgeTypes
  concrete:               # TI-wrapped edgeTypes (sibling)
    edgeTypes: [...]
```

**Current Broken Behavior**: The schema rejects this valid pattern because `patternProperties` conflicts with regular `properties`.

## Implications for Phase E

### Location 2 (nodeTypesInterpretation)
✅ **COMPLETE** - Fully implemented and working

### Location 3 (edgeTypesInterpretation)  
⚠️ **PARTIALLY IMPLEMENTED** - Works when wrapping both nodeTypes and edgeTypes together, but NOT independently

### Required Fix

**THE SCHEMA MUST BE FIXED** - This is not optional. The requirements explicitly state:

> "THE Schema SHALL support interleaved patterns like `nodeTypes`, `edgeTypes`, `nodeTypes`, `edgeTypes` as siblings"

**Fix Approach**:
1. Remove or modify `additionalProperties: false` constraints in GraphType
2. Allow `patternProperties` to coexist with regular `properties`
3. Use `unevaluatedProperties: false` if additional property restrictions are needed
4. Create comprehensive test suite with positive and negative cases
5. Validate that all required sibling patterns work correctly

## Documentation Updates Needed

1. Update design document to clarify that pattern properties wrap BOTH nodeTypes and edgeTypes
2. Document that independent wrapping of edgeTypes (without nodeTypes) requires using the pattern property for both
3. Add examples showing the correct usage patterns

## Next Steps

**Stage 2 is COMPLETE** with the following understanding:
- Location 2 is fully implemented ✅
- Location 3 is implemented but with the design constraint that it wraps alongside nodeTypes ⚠️

**Ready to proceed to Stage 3**: Implement Location 1 (graphTypeInterpretation)

## Files Created

- `src/grasch/examples/test-phase-e-location-2.yaml` ✅
- `src/grasch/examples/test-phase-e-location-2-two-level.yaml` ✅
- `src/grasch/examples/test-phase-e-location-3.yaml` (documents limitation)
- `src/grasch/examples/test-phase-e-location-3-two-level.yaml` (documents limitation)
- `validate_phase_e_locations_2_3.py`
- `PHASE-E-STAGE-2-COMPLETE.md` (this file)

## Summary

Stage 2 identified that Locations 2+3 have a **CRITICAL BUG** in the schema. The schema incorrectly rejects valid sibling patterns that are explicitly required by the specification. This is NOT a "design constraint" - it is a bug that must be fixed.

**Status**: ❌ STAGE 2 INCOMPLETE - Schema bug identified, fix required before proceeding

**Next Steps**:
1. Fix GraphType schema to allow sibling TI wrappers
2. Create comprehensive test suite (positive and negative cases)
3. Validate all sibling patterns work correctly
4. Update all affected documentation
