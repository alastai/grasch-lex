# Morning Checkpoint: TI Ordering Fix Ready to Execute

**Date**: 2024-12-01 Evening
**Status**: Analysis complete, ready for implementation
**Next Session**: Schema surgery to fix 6 wrong-order locations

## What We Discovered Tonight

### The Problem (Confirmed)
- 6 out of 8 TI locations have **wrong-order** patterns
- TI wrappers appear AFTER content instead of BEFORE
- This breaks the 0-level/1-level/2-level TI structure

### The Correct Understanding
**Type Interpretations have THREE expression levels:**
- **0-level (bare)**: `typeLabel: Person` - No wrapper
- **1-level (shorthand)**: `abstract: { typeLabel: Person }` - One wrapper
- **2-level (explicit)**: `subtypesOf: { abstract: { typeLabel: Person } }` - Two wrappers

These use `patternProperties` to match TI keywords - this is CORRECT and must be preserved.

### Location Status
| Location | Status | Issue |
|----------|--------|-------|
| 1. GraphType | ✓ CORRECT | Pattern to copy from |
| 2. NodeTypesProperty | ✗ WRONG | Wrapper after content |
| 3. EdgeTypesProperty | ✗ WRONG | Wrapper after content |
| 4. NodeTypeItem | ✗ WRONG | Wrapper after content |
| 5. EdgeTypeItem | ✗ WRONG | Wrapper after content |
| 6. Individual NodeType | ✗ WRONG | No TI support |
| 7. EdgeType Content | ✗ WRONG | No TI support |
| 8. EndpointReference | ✓ CORRECT | Already working |

### The Sibling "Issue" (Not a Bug)
- Multiple siblings with DIFFERENT interpretation facets: ✓ WORKS
- Multiple siblings with SAME interpretation facet: ✗ YAML limitation (acceptable)
- This is normal and matches expected use cases

## What Needs to Happen Next

### Task: Fix Schema Ordering at 6 Locations + Update Test YAML

**Files**: 
- `src/grasch/schemas/lex-2026.0.3.2.schema.json` (3803 lines)
- Test YAML files that use wrong-order TI syntax

**CRITICAL INSIGHT**: 
The existing test YAML files likely use the WRONG syntax (TI inside content) because that's what the broken schema accepted. After fixing the schema, we need to update the YAML to use CORRECT syntax (TI outside content).

**This is NOT a regression** - it's fixing the tests to match the actual design.

**Approach**:
1. Read and understand Location 1 (GraphType) pattern - the CORRECT one
2. Apply same pattern to Locations 2-7
3. Ensure `patternProperties` wrap content (not the other way around)
4. **Identify which test YAML files use wrong-order syntax**
5. **Update those YAML files to use correct syntax**
6. Test validation on all updated files

**Estimated Time**: 4-5 hours (includes YAML updates)

**Success Criteria**:
- All 8 locations support 0/1/2-level TI syntax
- Test YAML files use CORRECT TI placement (outside content)
- All updated examples validate
- Tests validate the ACTUAL design, not the broken implementation

## Key Documents

**Active/Authoritative**:
- `TI-SCHEMA-ORDERING-FIX-DESIGN.md` - Implementation plan
- `TI-LEVELS-CORRECTION.md` - Correct understanding of 0/1/2-level structure
- `LEX-2026.0.3.2-INTERPRETATION-DESCRIPTORS.md` - TI specification

**Context**:
- `PHASES-A-D-COMPLETE.md` - What's already working
- `TI-IMPLEMENTATION-ROADMAP.md` - Overall plan
- `PHASE-E-IMPLEMENTATION-PLAN.md` - Array-level TI (what we're fixing)

**Superseded/Archived**:
- `TI-SIBLING-CONSTRAINT-ANALYSIS.md` - Initial (incorrect) analysis
- Earlier analysis documents in `archive/ti-analysis-superseded/`

## Why This Matters

**Current State**: 
- Locations 6, 7, 8 (individual types) work ✓
- Locations 2-5 (array-level) don't work ✗

**After Fix**:
- All YAML files will validate correctly
- Can proceed to import system improvements
- Can then work on validation pipeline

## Commands to Run (After Fix)

```bash
# Validate all examples
python validate_all_examples.py

# Test specific locations
python validate_phase_e_locations_2_3.py
python validate_phase_e_locations_4_5.py

# Check for regressions
python validate_phase_a_corrected.py
python validate_phase_b.py
python validate_phase_c.py
python validate_phase_d.py
```

## Next Steps for Morning Session

1. **Read Location 1 pattern** from schema (lines ~433-800)
2. **Identify Locations 2-7** in schema
3. **Apply correct pattern** to each location
4. **Test validation** on all examples
5. **Create completion summary**
6. **Checkpoint** for next phase (imports)

## Notes

- Don't rush this - schema surgery requires precision
- Test incrementally (fix one location, test, repeat)
- Keep backup of original schema
- Document any unexpected issues
- The pattern is already proven at Location 1 - just replicate it

---

**Ready to execute in morning session** ✓
