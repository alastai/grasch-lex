# Phase 2 Scope Clarification

**Date**: 2024-12-02  
**Status**: Clarified and Ready for Execution

## Summary

Phase 2 of the TI Ordering Refactor fixes **6 broken locations** (Locations 2-7) where Type Interpretation wrappers appear in the wrong order. This document clarifies what is and is not included in Phase 2.

## Phase 2 Scope: 6 Locations to Fix

| Location # | Location Name | Description | Status | Action |
|------------|---------------|-------------|--------|--------|
| 2 | `nodeTypesInterpretation` | Wraps ENTIRE nodeTypes array property | ✗ WRONG | **FIX IN PHASE 2** |
| 3 | `edgeTypesInterpretation` | Wraps ENTIRE edgeTypes array property | ✗ WRONG | **FIX IN PHASE 2** |
| 4 | `nodeTypeArrayInterpretation` | Wraps SUBSEQUENCE within nodeTypes array | ✗ WRONG | **FIX IN PHASE 2** |
| 5 | `edgeTypeArrayInterpretation` | Wraps SUBSEQUENCE within edgeTypes array | ✗ WRONG | **FIX IN PHASE 2** |
| 6 | `nodeTypeInterpretation` | Wraps a single nodeType | ✗ WRONG | **FIX IN PHASE 2** |
| 7 | `edgeTypeInterpretation` | Wraps a single edgeType | ✗ WRONG | **FIX IN PHASE 2** |

## Not in Phase 2 Scope

### Location 1: graphTypeInterpretation
**Status**: ✓ Already Correct  
**Action**: None - serves as reference pattern  
**Current Behavior**: 
- GraphSchemaContent enforces only ONE `graphType` property
- This is enforced by `"additionalProperties": false` in the schema
- This is the **status quo** and requires no changes

**Important Clarification**:
- WITHIN the graphType, multiple sibling TI wrappers with different interpretation facets ARE allowed
- Example:
  ```yaml
  graphType:
    nodeTypes:           # Bare nodeTypes
      - typeLabel: Person
    exactlyOf:           # TI-wrapped nodeTypes (sibling)
      concrete:
        nodeTypes:
          - typeLabel: Company
    subtypesOf:          # Another TI-wrapped nodeTypes (sibling)
      abstract:
        nodeTypes:
          - typeLabel: Entity
  ```

**If Multiple graphType Properties Are Needed**:
- That would require changes to `GraphSchemaContent` definition
- That would be a DIFFERENT fix, not part of this Phase 2 refactoring
- That would need a separate spec and implementation plan

### Location 8: edgeTypeEndpointNodeTypeInterpretation
**Status**: ✓ Already Working  
**Action**: None - verify it still works after Phase 2 changes  
**Context**: Fixed in previous implementation phases (Phases A-D)

## Phase 2 Implementation Strategy

1. **Use Location 1 as Reference**: Location 1 (GraphType) has the correct TI pattern
2. **Fix 6 Locations**: Apply the correct pattern to Locations 2-7
3. **Verify Location 8**: Confirm Location 8 still works after changes
4. **Update Tests**: Fix test files to use correct TI syntax
5. **Validate**: Ensure all tests pass with corrected schema and syntax

## Key Principles

1. **TI Wrappers Before Content**: TI wrappers must appear BEFORE the content they wrap
2. **Two-Level Nesting**: Interpretation facet → Concreteness facet → Content
3. **Sibling Support**: Different interpretation facets can be siblings (YAML allows this)
4. **No Duplicate Keys**: Same interpretation facet cannot appear twice (YAML constraint)

## Success Criteria

After Phase 2 completion:
- ✓ All 6 broken locations (2-7) support correct TI ordering
- ✓ Location 1 remains unchanged (already correct)
- ✓ Location 8 still works (no regressions)
- ✓ All test files validate with corrected syntax
- ✓ Sibling TI wrappers work at all locations

## Next Steps

1. Execute Phase 2 tasks as defined in `.kiro/specs/ti-ordering-refactor/tasks.md`
2. Fix schema at 6 locations (tasks 4-12)
3. Update test files (tasks 14-20)
4. Validate and document (tasks 21-27)

## Related Documents

- **Design**: `.kiro/specs/ti-ordering-refactor/design.md`
- **Tasks**: `.kiro/specs/ti-ordering-refactor/tasks.md`
- **Requirements**: `.kiro/specs/ti-ordering-refactor/requirements.md`
- **Phase 1 Complete**: `PHASE-1-ANALYSIS-COMPLETE.md`
- **Location Taxonomy**: `TEMP-NESTING-IDEAS.md`
