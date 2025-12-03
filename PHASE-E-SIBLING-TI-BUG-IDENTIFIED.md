# Phase E - Critical Bug Identified: Sibling TI Wrappers Broken

**Date**: 2024-12-02  
**Status**: 🔴 CRITICAL BUG - BLOCKS PHASE E COMPLETION  
**Priority**: P0 - Must fix before proceeding

## Executive Summary

The LEX-2026.0.3.2 JSON Schema has a **critical bug** that prevents required sibling TI wrapper patterns from working. This was incorrectly documented as a "design constraint" but is actually a violation of explicit requirements.

**Impact**: Locations 1-3 cannot support the required pattern of multiple sibling `nodeTypes`/`edgeTypes` properties with different TI wrappers.

## The Bug

### What's Broken

The schema uses `patternProperties` that CONFLICT with regular `properties`, causing valid sibling patterns to be rejected as invalid.

**Required Pattern** (from Requirement 4):
```yaml
graphType:
  nodeTypes: [...]        # Bare nodeTypes (0-level)
  abstract:               # TI-wrapped nodeTypes (sibling)
    nodeTypes: [...]
  edgeTypes: [...]        # Bare edgeTypes (0-level)
  concrete:               # TI-wrapped edgeTypes (sibling)
    edgeTypes: [...]
```

**Current Behavior**: ❌ Schema rejects this as invalid

**Test Evidence**:
- `test-phase-e-location-3.yaml` - FAILS
- `test-phase-e-location-3-two-level.yaml` - FAILS

### Root Cause

The GraphType definition in the schema has:
1. Regular `properties`: `nodeTypes`, `edgeTypes`
2. `patternProperties`: `^(abstract|concrete|...)$` that can contain `nodeTypes`, `edgeTypes`

JSON Schema validation fails when:
- A bare `nodeTypes` property exists (regular property)
- AND a `concrete:` property exists (pattern property) containing `edgeTypes`

This creates a conflict because the schema doesn't properly allow these to coexist as siblings.

## Requirements Violation

From `.kiro/specs/ti-ordering-refactor/requirements.md`, **Requirement 4**:

> **User Story:** As a schema author, I want to use multiple TI wrappers with different interpretation facets at the same structural level, so that I can express complex type hierarchies.

**Acceptance Criteria 4.4**:
> "THE Schema SHALL support interleaved patterns like `nodeTypes`, `edgeTypes`, `nodeTypes`, `edgeTypes` as siblings"

**Current Status**: ❌ VIOLATED - Schema rejects this pattern

## Misleading Documentation

The following documents incorrectly describe this as acceptable:

1. **PHASE-E-STAGE-2-COMPLETE.md** - Says "✅ STAGE 2 COMPLETE" despite tests failing
2. **PHASE-E-STATUS-SUMMARY.md** - Lists Location 3 as "⚠️ DESIGN CONSTRAINT" instead of "❌ BROKEN"

These have been corrected to reflect the actual bug status.

## Required Test Suite

Before fixing the schema, we need a comprehensive test suite:

### Positive Tests (Must Pass)

1. **test-siblings-bare-only.yaml** - Multiple bare `nodeTypes` and `edgeTypes`
   ```yaml
   graphType:
     nodeTypes: [...]
     edgeTypes: [...]
   ```

2. **test-siblings-mixed-0-1-level.yaml** - Bare + 1-level TI
   ```yaml
   graphType:
     nodeTypes: [...]
     abstract:
       nodeTypes: [...]
   ```

3. **test-siblings-mixed-0-2-level.yaml** - Bare + 2-level TI
   ```yaml
   graphType:
     nodeTypes: [...]
     subtypesOf:
       abstract:
         nodeTypes: [...]
   ```

4. **test-siblings-all-1-level.yaml** - Multiple 1-level TI wrappers
   ```yaml
   graphType:
     abstract:
       nodeTypes: [...]
     concrete:
       nodeTypes: [...]
   ```

5. **test-siblings-all-2-level.yaml** - Multiple 2-level TI wrappers
   ```yaml
   graphType:
     exactlyOf:
       concrete:
         nodeTypes: [...]
     subtypesOf:
       abstract:
         nodeTypes: [...]
   ```

6. **test-siblings-interleaved.yaml** - nodeTypes, edgeTypes, nodeTypes, edgeTypes
   ```yaml
   graphType:
     nodeTypes: [...]
     edgeTypes: [...]
     abstract:
       nodeTypes: [...]
     concrete:
       edgeTypes: [...]
   ```

7. **test-siblings-complex.yaml** - All combinations
   ```yaml
   graphType:
     nodeTypes: [...]              # Bare nodeTypes
     edgeTypes: [...]              # Bare edgeTypes
     abstract:                     # 1-level nodeTypes
       nodeTypes: [...]
     concrete:                     # 1-level edgeTypes
       edgeTypes: [...]
     exactlyOf:                    # 2-level nodeTypes
       concrete:
         nodeTypes: [...]
     subtypesOf:                   # 2-level edgeTypes
       abstract:
         edgeTypes: [...]
   ```

### Negative Tests (Must Fail)

1. **test-siblings-duplicate-bare-INVALID.yaml** - Duplicate bare nodeTypes
   ```yaml
   graphType:
     nodeTypes: [...]
     nodeTypes: [...]    # ERROR: Duplicate YAML key
   ```

2. **test-siblings-duplicate-interpretation-INVALID.yaml** - Same interpretation facet twice
   ```yaml
   graphType:
     abstract:
       nodeTypes: [...]
     abstract:           # ERROR: Duplicate YAML key
       edgeTypes: [...]
   ```

3. **test-siblings-wrong-nesting-INVALID.yaml** - TI wrapper in wrong place
   ```yaml
   graphType:
     nodeTypes:
       - abstract:       # ERROR: TI inside array
           typeLabel: Person
   ```

## Schema Fix Strategy

### Step 1: Analyze Current Schema

Read GraphType definition (lines ~600-900 in schema) to understand:
- How `properties` and `patternProperties` are currently structured
- What `additionalProperties` constraints exist
- Why sibling patterns are being rejected

### Step 2: Restructure GraphType

**Option A**: Remove `additionalProperties: false`
- Allow both regular properties and pattern properties to coexist
- Use `unevaluatedProperties: false` if needed for stricter validation

**Option B**: Restructure property definitions
- Make `nodeTypes` and `edgeTypes` optional in both `properties` and `patternProperties`
- Ensure no conflicts between the two

**Option C**: Use `anyOf` or `oneOf` patterns
- Define multiple valid structures that can coexist
- More complex but potentially more explicit

### Step 3: Validate Fix

1. Run all positive tests - must pass
2. Run all negative tests - must fail with appropriate errors
3. Run existing Phase A-D tests - must still pass (no regressions)
4. Run all Phase E tests - must pass

### Step 4: Update Documentation

1. Update PHASE-E-STAGE-2-COMPLETE.md with correct status
2. Update PHASE-E-STATUS-SUMMARY.md with correct status
3. Update design document with schema fix details
4. Create completion summary

## Impact Assessment

### Affected Locations

- **Location 1** (graphTypeInterpretation): Needs TI wrapper support added
- **Location 2** (nodeTypesInterpretation): Sibling patterns broken
- **Location 3** (edgeTypesInterpretation): Sibling patterns broken
- **Locations 4-5**: Unknown - need testing after fix
- **Locations 6-8**: Working correctly (no changes needed)

### Affected Files

**Schema**:
- `src/grasch/schemas/lex-2026.0.3.2.schema.json` - GraphType definition

**Test Files** (currently failing):
- `src/grasch/examples/test-phase-e-location-3.yaml`
- `src/grasch/examples/test-phase-e-location-3-two-level.yaml`

**Documentation** (corrected):
- `PHASE-E-STAGE-2-COMPLETE.md`
- `PHASE-E-STATUS-SUMMARY.md`
- `.kiro/specs/ti-ordering-refactor/requirements.md`
- `.kiro/specs/ti-ordering-refactor/design.md`

## Next Steps

1. ✅ **DONE**: Identify and document the bug
2. ✅ **DONE**: Correct misleading documentation
3. ✅ **DONE**: Update requirements and design documents
4. ⏳ **TODO**: Create comprehensive test suite (positive + negative)
5. ⏳ **TODO**: Analyze GraphType schema structure in detail
6. ⏳ **TODO**: Implement schema fix
7. ⏳ **TODO**: Validate all tests pass
8. ⏳ **TODO**: Create completion summary

## Timeline Estimate

- Test suite creation: 1-2 hours
- Schema analysis: 1 hour
- Schema fix implementation: 2-3 hours
- Validation and testing: 1-2 hours
- Documentation: 1 hour

**Total**: 6-9 hours

## Success Criteria

1. ✅ All positive sibling tests pass
2. ✅ All negative sibling tests fail appropriately
3. ✅ Existing Phase A-D tests still pass (no regressions)
4. ✅ Locations 1-3 support all required sibling patterns
5. ✅ Documentation accurately reflects implementation status

## Conclusion

This is a **critical bug** that must be fixed before Phase E can be considered complete. The bug was incorrectly documented as a "design constraint" when it is actually a violation of explicit requirements. The fix requires restructuring the GraphType schema to allow sibling TI wrappers to coexist with bare properties.

**Status**: 🔴 BLOCKING - Must fix before proceeding with Phase E
