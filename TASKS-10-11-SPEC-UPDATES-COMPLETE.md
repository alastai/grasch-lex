# Tasks 10-11 Spec Updates Complete

## Summary

The spec documents for the ti-ordering-refactor have been updated to reflect the correct understanding of Tasks 10 and 11.

## Changes Made

### 1. Updated tasks.md

**Task 10** - Renamed and corrected:
- **Old**: "Fix Locations 2 & 3 (nodeTypesInterpretation & edgeTypesInterpretation)"
- **New**: "Add Level-1 TI Wrappers to GraphType & Remove Vestigial Definitions"

**Corrected Scope**:
- **Part A**: Remove vestigial `NodeTypesProperty` and `EdgeTypesProperty` definitions (NOT USED)
- **Part B**: Add missing 1-level TI wrappers (`concrete:` and `abstract:`) to GraphType

**Task 11** - Renamed and corrected:
- **Old**: "Test Locations 2 & 3 Fixes"
- **New**: "Test Level-1 TI Wrappers in GraphType"

**Corrected Scope**:
- Create test files for 1-level TI syntax: `concrete: { nodeTypes: [...] }` and `abstract: { edgeTypes: [...] }`
- Validate schema accepts the new syntax
- Ensure no regressions in existing tests

### 2. Updated design.md

**Location 2 Description** - Corrected:
- Clarified that vestigial `NodeTypesProperty` definition must be DELETED
- Identified actual location as GraphType definition (line 743)
- Specified missing 1-level TI wrappers for nodeTypes

**Location 3 Description** - Corrected:
- Clarified that vestigial `EdgeTypesProperty` definition must be DELETED
- Identified actual location as GraphType definition (line 743)
- Specified missing 1-level TI wrappers for edgeTypes

**Phase 2 Scope Summary** - Corrected:
- Removed incorrect information about `patternProperties` being wrong
- Added clear explanation of vestigial definitions that need removal
- Added clear explanation of missing 1-level TI wrappers
- Provided examples of current vs. needed GraphType structure

### 3. Updated requirements.md

**Requirement 2 Acceptance Criteria** - Expanded:
- Split Location 2 into two criteria (concrete and abstract wrappers for nodeTypes)
- Split Location 3 into two criteria (concrete and abstract wrappers for edgeTypes)
- Added two new criteria for removing vestigial definitions
- Renumbered subsequent criteria

## Key Corrections

### What Was Wrong

The original Tasks 10-11 incorrectly assumed:
1. That `NodeTypesProperty` and `EdgeTypesProperty` were actual locations that needed fixing
2. That these definitions were being used somewhere in the schema
3. That the fix involved moving TI wrappers from inside to outside

### What Is Actually Needed

The correct understanding is:
1. `NodeTypesProperty` and `EdgeTypesProperty` are **vestigial definitions** that are NOT REFERENCED anywhere
2. These definitions must be **completely deleted** from the schema
3. The **actual** Locations 2 & 3 are at the **GraphType level** (line 743)
4. GraphType is **missing 1-level TI wrappers** (`concrete:` and `abstract:`)
5. These 1-level wrappers must be **added as explicit properties** with both nodeTypes and edgeTypes children

## Current GraphType Structure

**What exists**:
- ✅ 0-level: bare `nodeTypes` and `edgeTypes`
- ✅ 2-level: `exactlyOf: { concrete/abstract: { nodeTypes/edgeTypes } }`
- ✅ 2-level: `subtypesOf: { abstract: { nodeTypes/edgeTypes } }`
- ✅ 2-level: `properSubtypesOf: { concrete/abstract: { nodeTypes/edgeTypes } }`

**What's missing**:
- ❌ 1-level: `concrete: { nodeTypes/edgeTypes }`
- ❌ 1-level: `abstract: { nodeTypes/edgeTypes }`

## Next Steps

1. ✅ Spec documents updated (this step)
2. ⏭️ Make schema changes:
   - Remove `NodeTypesProperty` definition (lines ~2470-2700)
   - Remove `EdgeTypesProperty` definition (lines ~3181-3400)
   - Add `concrete:` property to GraphType with nodeTypes and edgeTypes children
   - Add `abstract:` property to GraphType with nodeTypes and edgeTypes children
3. ⏭️ Create test files for 1-level TI syntax
4. ⏭️ Validate schema and run tests
5. ⏭️ Update task status in tasks.md

## Reference

- Analysis document: `TASKS-10-11-CORRECTION-ANALYSIS.md`
- Spec location: `.kiro/specs/ti-ordering-refactor/`
