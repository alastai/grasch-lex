# Design and Tasks Documents Need Correction

**Date**: 2024-12-06  
**Status**: ⚠️ CRITICAL - Must correct before Phase 2  
**Issue**: Phase 1 findings contradict current design/tasks documents

## Problem Summary

Our Phase 1 analysis (Tasks 1-3) revealed that **Location 1 is ALREADY CORRECT**, but the design and tasks documents still say it needs fixing. This creates a contradiction that must be resolved before proceeding to Phase 2.

---

## Discrepancies Found

### 1. Design Document (`.kiro/specs/ti-ordering-refactor/design.md`)

**Current (INCORRECT)**:
- Line ~220: Table shows Location 1 as "✗ WRONG | Add TI support"
- Line ~230: "Key Discovery: Location 1 (GraphSchemaContent) does NOT currently support TI wrappers"
- Overview: "fix incorrect Type Interpretation (TI) wrapper ordering at 6 out of 8 locations"
- Phase 2 Scope: "fixes **7 broken locations** (1-7)"

**Should Be (CORRECT)**:
- Location 1 status: "✓ CORRECT | Reference pattern"
- Location 1 already supports TI wrappers correctly (verified in Phase 1)
- Overview: "fix incorrect Type Interpretation (TI) wrapper ordering at **6 out of 8 locations**"
- Phase 2 Scope: "fixes **6 broken locations** (2-7)"

### 2. Tasks Document (`.kiro/specs/ti-ordering-refactor/tasks.md`)

**Current (MIXED - Partially Correct)**:
- Task 1: ✅ Correctly marked as "ALREADY COMPLETE"
- Task 5: ✅ Correctly marked as "ALREADY COMPLETE"  
- Task 7: ✅ Correctly marked as "ALREADY COMPLETE"
- Phase 2 header: Says "6 Locations - CORRECTED" ✅
- But references to "7 locations" appear in some places

**Needs Verification**:
- Ensure all task descriptions are consistent
- Confirm Phase 2 scope is clear: 6 broken locations (2-7)

---

## Phase 1 Findings (Ground Truth)

### ✅ Location 1: GraphSchemaContent
**Status**: ALREADY CORRECT  
**Line**: 203-260 in schema  
**Evidence**:
- Has `patternProperties` for TI wrappers
- Supports 0/1/2-level TI syntax
- Test file `test_location_1_verification.py` passes all three levels
- Documented in `LOCATION-1-ALREADY-CORRECT.md`

**This is our REFERENCE PATTERN for fixing other locations.**

### ❌ Locations 2-7: Need Fixes
**Status**: BROKEN  
**Count**: 6 locations  
**Details**: Documented in `TASK-2-SCHEMA-LOCATION-ANALYSIS.md`

### ✅ Location 8: EndpointReference
**Status**: ALREADY CORRECT (from Phases C-D)  
**No action needed**

---

## Required Corrections

### A. Design Document Updates

**File**: `.kiro/specs/ti-ordering-refactor/design.md`

#### 1. Overview Section (Line ~10)
```markdown
# CURRENT (WRONG):
This document describes the design for refactoring the LEX-2026.0.3.2 JSON Schema 
to fix incorrect Type Interpretation (TI) wrapper ordering at 6 out of 8 locations.

# SHOULD BE (CORRECT):
This document describes the design for refactoring the LEX-2026.0.3.2 JSON Schema 
to fix incorrect Type Interpretation (TI) wrapper ordering at 6 out of 8 locations.
Location 1 and Location 8 are already correct and serve as reference patterns.
```

#### 2. Phase 2 Scope Summary (Line ~100)
```markdown
# CURRENT (WRONG):
**What Phase 2 Fixes**: **7 broken locations** (Locations 1-7)

**Critical Discovery - Location 1 Needs Fixing**:
- GraphSchemaContent currently does NOT support TI wrappers around `graphType`

# SHOULD BE (CORRECT):
**What Phase 2 Fixes**: **6 broken locations** (Locations 2-7)

**Critical Discovery - Location 1 Already Correct**:
- GraphSchemaContent ALREADY supports TI wrappers around `graphType` correctly
- Verified in Phase 1 with test_location_1_verification.py
- Location 1 serves as the REFERENCE PATTERN for fixing other locations
```

#### 3. Eight TI Locations Table (Line ~220)
```markdown
# CURRENT (WRONG):
| 1 | `graphTypeInterpretation` | Wraps the graphType property | ✗ WRONG | Add TI support |

# SHOULD BE (CORRECT):
| 1 | `graphTypeInterpretation` | Wraps the graphType property | ✓ CORRECT | Reference pattern |
```

#### 4. Component Design Section (Line ~300+)
```markdown
# CURRENT (WRONG):
Phase 2 fixes **7 broken locations** identified during analysis.

#### Location 1: graphTypeInterpretation
**Current**: GraphSchemaContent only allows ONE bare `graphType` property  
**Target**: Add `patternProperties` to allow TI wrappers (0/1/2-level) around `graphType`  
**Phase 2 Task**: **NEW - Add TI support to GraphSchemaContent**

# SHOULD BE (CORRECT):
Phase 2 fixes **6 broken locations** identified during analysis. Location 1 is already correct.

#### Location 1: graphTypeInterpretation
**Status**: ✅ ALREADY CORRECT - No changes needed  
**Current**: GraphSchemaContent already supports TI wrappers correctly via `patternProperties`  
**Verified**: test_location_1_verification.py passes all 0/1/2-level TI tests  
**Usage**: Serves as REFERENCE PATTERN for fixing Locations 2-7  
**Phase 2 Task**: None - skip Tasks 5 and 7
```

### B. Tasks Document Updates

**File**: `.kiro/specs/ti-ordering-refactor/tasks.md`

#### 1. Phase 2 Header
```markdown
# CURRENT (MOSTLY CORRECT):
## Phase 2: Schema Fixes (6 Locations - CORRECTED)

**Phase 2 Scope - CORRECTED**: Fix **6 broken locations** (2-7) identified in Phase 1 analysis.

# VERIFY THIS IS CONSISTENT THROUGHOUT
```

#### 2. Ensure All References Are Consistent
- Search for "7 locations" and replace with "6 locations" where referring to broken locations
- Confirm Tasks 5 and 7 are marked as "ALREADY COMPLETE"
- Confirm Task 1 is marked as "ALREADY COMPLETE"

---

## Recommendation

**Before proceeding to Phase 2 execution, we should:**

1. ✅ **Update design.md** to reflect that Location 1 is CORRECT (not broken)
2. ✅ **Verify tasks.md** is consistent (mostly correct already)
3. ✅ **Confirm scope**: 6 broken locations (2-7), not 7
4. ✅ **Clarify**: Location 1 is the REFERENCE PATTERN, not a fix target

**This ensures our authoritative documents match our verified Phase 1 findings.**

---

## Impact if Not Corrected

If we proceed without correcting the design document:

1. ❌ **Confusion**: Team members reading design will think Location 1 needs fixing
2. ❌ **Wasted effort**: Someone might try to "fix" Location 1 (which is already correct)
3. ❌ **Breaking changes**: "Fixing" Location 1 could break what's already working
4. ❌ **Documentation debt**: Future readers will be misled

---

## Proposed Action

**Option 1: Update Documents Now (RECOMMENDED)**
- Update design.md to reflect Phase 1 findings
- Verify tasks.md consistency
- Then proceed to Phase 2 with confidence

**Option 2: Proceed with Caution**
- Note the discrepancy
- Rely on Phase 1 analysis documents as ground truth
- Update design.md after Phase 2 completion

**I recommend Option 1** - correcting the documents now ensures everyone is working from the same accurate understanding.

---

## User Decision Required

**Should I update the design.md and tasks.md documents to reflect our Phase 1 findings before we proceed to Phase 2?**

This will ensure:
- ✅ Location 1 is documented as CORRECT (reference pattern)
- ✅ Phase 2 scope is clear: 6 broken locations (2-7)
- ✅ No confusion about what needs fixing
- ✅ Authoritative documents match verified reality
