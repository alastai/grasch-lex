# Phase 1: Schema Analysis and Preparation - COMPLETE

**Date**: 2024-12-06  
**Status**: ✅ ALL TASKS COMPLETE  
**Phase Duration**: ~30 minutes

## Overview

Phase 1 of the TI Ordering Refactor has been successfully completed. All three preparatory tasks have been finished, and we are now ready to proceed to Phase 2 (Schema Fixes).

---

## Task Completion Summary

### ✅ Task 1: Analyze Location 1 (GraphType) Pattern
**Status**: ALREADY COMPLETE (verified in previous work)  
**Documentation**: `LOCATION-1-ALREADY-CORRECT.md`

**Key Findings**:
- Location 1 (GraphSchemaContent → graphType) already supports 0/1/2-level TI wrappers correctly
- Test validation confirms all three levels pass
- Uses `patternProperties` pattern correctly
- This serves as our reference pattern for fixing other locations
- No changes needed

**Reference Pattern Location**: Lines 203-260 in schema (GraphSchemaContent)

---

### ✅ Task 2: Identify Schema Locations for Fixes
**Status**: COMPLETE  
**Documentation**: `TASK-2-SCHEMA-LOCATION-ANALYSIS.md`

**Locations Identified**:

| Location | Line | Definition | Status | Issue |
|----------|------|------------|--------|-------|
| 1 | 203 | GraphSchemaContent | ✅ Correct | Reference pattern |
| 2 | 2316 | NodeTypesProperty | ❌ Broken | Uses oneOf, prevents siblings |
| 3 | 3027 | EdgeTypesProperty | ❌ Broken | Uses oneOf, prevents siblings |
| 4 | 1918 | NodeTypeItem | ❌ Broken | Mixes partition blocks with single types |
| 5 | 2629 | EdgeTypeItem | ❌ Broken | Mixes partition blocks with single types |
| 6 | 1501 | NodeType | ❌ Broken | No TI wrapper support |
| 7 | 1805 | EdgeType | ❌ Broken | No TI wrapper support |
| 8 | N/A | EndpointReference | ✅ Correct | Already working from Phases C-D |

**Summary**: 6 locations need fixes (2-7), 2 locations already working (1, 8)

**Dependencies Identified**:
- Task 4 (Edge Label Container Fix) must complete before fixing Locations 3, 5, 7

---

### ✅ Task 3: Create Schema Backup
**Status**: COMPLETE  
**Documentation**: `TASK-3-SCHEMA-BACKUP-COMPLETE.md`

**Backup Details**:
- **Source**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
- **Backup**: `src/grasch/schemas/lex-2026.0.3.2.schema.json.backup`
- **Size**: 125K (both files match)
- **Validation**: ✅ Backup is valid JSON
- **Timestamp**: Dec 6, 2024 19:18

**Verification**:
```bash
$ python3 -m json.tool src/grasch/schemas/lex-2026.0.3.2.schema.json.backup > /dev/null
✅ Backup is valid JSON

$ ls -lh src/grasch/schemas/lex-2026.0.3.2.schema.json*
-rw-r--r--  125K Dec  6 12:52 lex-2026.0.3.2.schema.json
-rw-r--r--  125K Dec  6 19:18 lex-2026.0.3.2.schema.json.backup
```

---

## Phase 1 Deliverables

1. ✅ **Location 1 Analysis**: Confirmed correct pattern, documented as reference
2. ✅ **Location Inventory**: Complete list of 6 broken locations with line numbers
3. ✅ **Schema Backup**: Safe backup created and verified
4. ✅ **Documentation**: Three detailed analysis documents created

---

## Key Insights from Phase 1

### Reference Pattern (Location 1)
Location 1 uses the CORRECT pattern that we need to replicate:
- Uses `patternProperties` to match TI keywords
- Supports 0-level (bare), 1-level (shorthand), and 2-level (explicit) syntax
- Allows TI wrappers to appear BEFORE content
- Already tested and validated

### Problem Patterns Identified

**Pattern 1: oneOf Prevents Siblings** (Locations 2-3)
- Current: Uses `oneOf` which only allows ONE option
- Problem: Cannot have multiple sibling TI-wrapped properties
- Fix: Replace with explicit properties (without oneOf)

**Pattern 2: Mixed Semantics** (Locations 4-5)
- Current: Mixes partition blocks with single types
- Problem: Needs 2-level TI support for partition blocks
- Fix: Distinguish partition blocks from single types, add full TI support

**Pattern 3: No TI Support** (Locations 6-7)
- Current: No TI wrapper support at all
- Problem: Cannot wrap individual types
- Fix: Add sibling properties pattern with full 0/1/2-level TI syntax

---

## Next Steps: Phase 2 (Schema Fixes)

**Ready to Begin**: Task 4 - Fix Edge Label Container Structure (E02)

**Critical Note**: Task 4 is a PREREQUISITE that must be completed before fixing Locations 3, 5, and 7 (which involve edge types).

**Phase 2 Tasks**:
- Task 4: Fix Edge Label Container Structure (E02 - PREREQUISITE) ⭐
- Task 5: Fix Location 1 (already complete, skip)
- Task 6: Test Edge Label Container Fix
- Task 7: Test Location 1 Fix (already complete, skip)
- Tasks 8-17: Fix and test Locations 2-7

**Estimated Time for Phase 2**: 3-4 hours

---

## Success Criteria Met

✅ All 8 locations identified and documented  
✅ Reference pattern (Location 1) analyzed and confirmed correct  
✅ 6 broken locations identified with exact line numbers  
✅ Current structure documented for each location  
✅ Schema backup created and verified  
✅ Dependencies identified (Task 4 prerequisite)  
✅ Ready to proceed to schema modifications

---

## Phase 1 Complete - Ready for Phase 2

All preparatory work is complete. The schema backup is in place, all locations are documented, and we have a clear reference pattern to follow. 

**Awaiting approval to proceed to Phase 2: Schema Fixes**
