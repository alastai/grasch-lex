# Phase 2 Design and Tasks Updated

**Date**: 2024-12-02  
**Status**: Documents Updated - Ready for Implementation

## Summary of Changes

The design and tasks documents have been updated to reflect the corrected understanding of Phase 2 scope based on user clarification and schema analysis.

## Key Changes

### 1. Phase 2 Scope Corrected

**Previous Understanding**: 6 locations need fixing (2-7)  
**Corrected Understanding**: **7 locations need fixing (1-7)**

### 2. Location 1 Discovery

**Critical Finding**: Location 1 (GraphSchemaContent) does NOT currently support TI wrappers around `graphType`.

**Current Behavior**:
- Only allows ONE bare `graphType` property
- `"additionalProperties": false` prevents TI wrapper properties

**Required Behavior**:
- TI wrappers (0/1/2-level) should be able to wrap the `graphType`
- Example: `abstract: { graphType: {...} }` or `subtypesOf: { abstract: { graphType: {...} } }`

### 3. Locations 2-3 Clarification

**GraphType Level**: Already has correct `patternProperties` pattern (this is the reference!)

**NodeTypesProperty/EdgeTypesProperty**: Use wrong `oneOf` pattern (prevents siblings)

**Required Behavior**:
- Multiple `nodeTypes` and `edgeTypes` properties as siblings
- Each with its own TI wrapper (0/1/2-level)
- Example: `nodeTypes: [...]`, `abstract: { nodeTypes: [...] }`, `exactlyOf: { concrete: { nodeTypes: [...] } }`

## Updated Documents

### Design Document (.kiro/specs/ti-ordering-refactor/design.md)

**Changes**:
- Updated location table to show Location 1 needs fixing
- Added "Phase 2 Scope Summary - CORRECTED" section
- Clarified Location 1 problem and requirements
- Clarified Locations 2-3 problem and requirements
- Updated Component Design to include Location 1 as first task
- Changed scope from "6 locations" to "7 locations"

### Tasks Document (.kiro/specs/ti-ordering-refactor/tasks.md)

**Changes**:
- Added new Task 4: Fix Location 1 (graphTypeInterpretation)
- Added new Task 5: Test Location 1 Fix
- Renumbered all subsequent tasks (old 4→6, old 5→7, etc.)
- Added Task 17: Create Location 1 Test Files
- Updated Phase 2 header to reflect 7 locations
- Updated all task descriptions to reference correct locations
- Updated Success Criteria to include Location 1
- Changed all references from "6 locations" to "7 locations"

## Task Count Changes

**Previous**: 27 tasks total  
**Updated**: 30 tasks total

**New Tasks**:
- Task 4: Fix Location 1 (graphTypeInterpretation)
- Task 5: Test Location 1 Fix
- Task 17: Create Location 1 Test Files

## Reference Pattern

**GraphType's `patternProperties` implementation** (lines 433-800 in schema) is the correct pattern to use for ALL fixes, including:
- Location 1 (GraphSchemaContent)
- Locations 2-3 (NodeTypesProperty/EdgeTypesProperty)
- Locations 4-7 (as previously planned)

## User Requirements Confirmed

1. **Location 1**: TI wrappers (0/1/2-level) surrounding ONE `graphType`
2. **Locations 2-3**: TI wrappers (0/1/2-level) surrounding EACH `nodeTypes`/`edgeTypes` property (multiple siblings, any order)

## Implementation Ready

Both documents are now updated and consistent with:
- User requirements
- Schema analysis findings
- Correct understanding of all 8 TI locations

The spec is ready for Phase 2 implementation.
