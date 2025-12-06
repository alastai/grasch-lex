# TI Ordering Refactor Spec Updates Summary

## Overview

This document summarizes the updates made to the `.kiro/specs/ti-ordering-refactor/` specification to reflect three critical changes:

1. **Terminology Standardization**: Replace "partition block" and "item" vocabulary with "Array" terminology
2. **Task 10.0 Addition**: Create prerequisite task to fix Location 1 (eliminate pattern properties)
3. **Tasks 10 & 11 Restructuring**: Handle Locations 2 & 3 together as multi-wrapper sibling TI locations

## Changes Made

### 1. Terminology Updates

**Replaced**: "partition block", "item", "NodeTypeItem", "EdgeTypeItem"  
**With**: "Array", "array subsequence", "NodeTypeArray", "EdgeTypeArray"

#### Requirements Document Changes

- Added "Array" to Glossary definition
- Updated Requirement 2 acceptance criteria to use "NodeTypeArray" and "EdgeTypeArray" instead of "Item"
- Updated Requirement 4 to use "sibling TI-wrapped subsequences" instead of "sibling partition blocks"

#### Design Document Changes

- Renamed section from "Partition Model for Array-Level TIs" to "Array Subsequence Model for Array-Level TIs"
- Updated all references from "partition block" to "array subsequence"
- Updated all references from "item" to "array element"
- Updated Location 4 & 5 descriptions to use "subsequence" terminology
- Updated example comments to use "array element" and "array subsequence"

#### Tasks Document Changes

- Updated Task 12 (Location 4) to use "array subsequence model" and "subsequence" terminology
- Updated Task 13 (Location 5) to use "array subsequence model" and "subsequence" terminology
- Updated all task descriptions to use consistent "array" terminology

### 2. Task 10.0 Addition (Prerequisite)

**New Task**: `10.0 Fix Location 1 (graphTypeInterpretation) - Eliminate Pattern Properties`

**Purpose**: Fix Location 1 FIRST before it can serve as a reference pattern for other locations

**Key Points**:
- CRITICAL PREREQUISITE for Tasks 10 & 11
- Eliminates ALL pattern properties from GraphSchemaContent (lines 203-420)
- Replaces with explicit properties: `graphType`, `concrete`, `abstract`, `exactlyOf`, `subtypesOf`, `properSubtypesOf`
- Uses `oneOf` to ensure exactly ONE graphType (bare or wrapped) exists
- Follows explicit properties pattern from Phases A-D (NOT Location 1's current broken pattern)

**Placement**: Inserted between Task 7 and Task 8 (now Task 10)

### 3. Tasks 10 & 11 Restructuring

**Old Structure**:
- Task 8: Fix Location 2 (nodeTypesInterpretation)
- Task 9: Test Location 2 Fix
- Task 10: Fix Location 3 (edgeTypesInterpretation)
- Task 11: Test Location 3 Fix

**New Structure**:
- Task 10.0: Fix Location 1 (PREREQUISITE)
- Task 10: Fix Locations 2 & 3 together (nodeTypesInterpretation & edgeTypesInterpretation)
- Task 11: Test Locations 2 & 3 together

**Rationale**:
- Locations 2 & 3 are both multi-wrapper sibling TI locations
- They should use the SAME pattern (explicit sibling properties WITHOUT oneOf)
- They are aligned in structure and should be fixed together
- Both depend on Location 1 being fixed first (Task 10.0)
- Location 3 also depends on Task 4 (Edge Label Container Fix)

**Task 10 Details**:
- **DEPENDS ON**: Task 10.0 (Location 1 fix) AND Task 4 (Edge Label Container fix for Location 3)
- Fixes BOTH Locations 2 & 3 using explicit sibling properties WITHOUT oneOf
- Uses corrected Location 1 (from Task 10.0) as reference
- Adds explicit properties for both `nodeTypes` and `edgeTypes`
- Supports all TI levels (0-level, 1-level, 2-level)
- Allows multiple siblings with different interpretation facets

**Task 11 Details**:
- Tests BOTH Locations 2 & 3 together
- Runs `validate_phase_e_locations_2_3.py`
- Expects initial failures (tests use wrong syntax)
- Re-validates after test file updates (Tasks 20-22)

### 4. Phase 2 Section Updates

Updated Phase 2 header to reflect new task structure:

**Task Structure**:
- **Task 10.0**: Fix Location 1 FIRST (eliminate pattern properties) - PREREQUISITE
- **Task 10**: Fix Locations 2 & 3 together (multi-wrapper sibling TI locations)
- **Task 11**: Test Locations 2 & 3 together
- **Tasks 12-16**: Continue with individual location fixes (4-7)

**Pattern to Fix**:
- **Location 1 (Task 10.0)**: ELIMINATE pattern properties; use explicit properties with oneOf
- **Locations 2-3 (Task 10)**: Use explicit sibling properties without oneOf
- **Locations 4-7**: Continue with individual fixes
- **Reference Pattern**: Phases A-D (Locations 6-8) use the CORRECT explicit properties approach

### 5. Success Criteria Updates

Updated success criteria to reflect:
- Location 1 has pattern properties eliminated
- Locations 2-3 use explicit properties without oneOf
- Locations 4-5 support array subsequences (not "partition blocks")

## Key Insights

### Why Location 1 Must Be Fixed First

**Current State**: Location 1 (GraphSchemaContent) uses `patternProperties` which is WRONG
**Problem**: Pattern properties create JSON Schema conflicts and prevent proper sibling TI support
**Solution**: Eliminate pattern properties and use explicit properties with oneOf
**Impact**: Once fixed, Location 1 becomes the correct reference pattern for other locations

### Why Locations 2 & 3 Should Be Fixed Together

**Similarity**: Both are multi-wrapper sibling TI locations at the GraphType level
**Pattern**: Both should use explicit sibling properties WITHOUT oneOf
**Alignment**: Fixing them together ensures consistency and reduces duplication
**Dependencies**: Both depend on Location 1 being fixed first

### Terminology Clarity

**Old**: "partition block", "item", "NodeTypeItem", "EdgeTypeItem"
**New**: "array subsequence", "array element", "NodeTypeArray", "EdgeTypeArray"
**Rationale**: 
- "Array" is clearer and more accurate
- "Subsequence" better describes the division of arrays
- "Element" is standard terminology for array contents
- Eliminates confusion with "item" which could mean many things

## Files Modified

1. `.kiro/specs/ti-ordering-refactor/requirements.md`
   - Added "Array" to Glossary
   - Updated Requirement 2 acceptance criteria
   - Updated Requirement 4 terminology

2. `.kiro/specs/ti-ordering-refactor/design.md`
   - Renamed section to "Array Subsequence Model"
   - Updated all terminology throughout
   - Updated Location 4 & 5 descriptions
   - Updated Location 1 fix requirement in table

3. `.kiro/specs/ti-ordering-refactor/tasks.md`
   - Added Task 10.0 (Location 1 prerequisite)
   - Restructured Tasks 10 & 11 (Locations 2 & 3 together)
   - Updated Phase 2 header with new task structure
   - Updated all terminology in Tasks 12-13
   - Updated success criteria

## Next Steps

**For Review**:
1. Review terminology changes - is "array subsequence" clear and accurate?
2. Review Task 10.0 placement and description - is it clear this is a prerequisite?
3. Review Tasks 10 & 11 restructuring - does it make sense to fix Locations 2 & 3 together?
4. Confirm the dependency chain: Task 10.0 → Task 10 (also depends on Task 4 for Location 3) → Task 11

**After Approval**:
1. Begin implementation with Task 10.0 (fix Location 1)
2. Proceed to Task 10 (fix Locations 2 & 3 together)
3. Continue with remaining tasks in sequence

## Questions for User

1. **Terminology**: Is "array subsequence" the right term, or would you prefer something else?
2. **Task 10.0**: Should this be a separate top-level task or a sub-task of Task 10?
3. **Locations 2 & 3**: Confirm that fixing these together makes sense given their similarity
4. **Dependencies**: Confirm the dependency chain is correct (10.0 → 10 → 11)
