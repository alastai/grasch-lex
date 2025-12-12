# Task 11 Root Cause Analysis - FOUND

**Date**: 2024-12-06  
**Status**: Root cause identified  
**Issue**: Test files have incorrect edge type structure

## Root Cause

The validation failures for Location 3 test files are **NOT** caused by TI wrapper issues. The TI wrappers (`concrete: { edgeTypes: [...] }`) work correctly.

**The actual problem**: The edge type structures in the test files are **invalid** because they have `typeLabel` at the wrong level.

## Invalid Structure (Current Test Files)

```yaml
edgeType:
  typeLabel: KNOWS        # ❌ WRONG - typeLabel at edgeType level
  directed:
    from: ...
    to: ...
    via:
      typeLabel: KNOWS    # This is correct, but the above is wrong
```

## Valid Structure (E02 Compliant)

```yaml
edgeType:
  directed:
    from: ...
    to: ...
    via:
      typeLabel: KNOWS    # ✅ CORRECT - typeLabel ONLY inside via
```

## Evidence

### Test 1: Minimal Document with Correct Structure
Created `test_location_3_minimal.py` with correct edge structure:
- Result: ✅ **VALIDATES SUCCESSFULLY**
- Conclusion: TI wrapper `concrete: { edgeTypes: [...] }` works fine

### Test 2: Actual Test File
File: `test-phase-e-location-3.yaml`
- Has: `typeLabel` at edgeType level (line 23)
- Result: ❌ **VALIDATION FAILS**
- Error: "Additional properties are not allowed ('typeLabel' was unexpected)"

## Why This Happened

The test files were created **before** the E02 edge label container fix was completed. They use the old (incorrect) edge type syntax where `typeLabel` could appear at multiple levels.

After E02 (Task 4), the schema was updated to require:
- Edge label containers (`via:`, `arc:`) are ALWAYS objects
- `typeLabel:` is a REQUIRED child property of the edge label container
- `typeLabel:` should NOT appear at the edgeType level

## Impact

**Files Affected**:
1. `src/grasch/examples/test-phase-e-location-3.yaml`
2. `src/grasch/examples/test-phase-e-location-3-two-level.yaml`

Both files need to be updated to remove `typeLabel` from the edgeType level.

## Fix Required

### For test-phase-e-location-3.yaml

**Change from**:
```yaml
- edgeType:
    typeLabel: KNOWS      # Remove this line
    directed:
      from:
        nodeType:
          typeLabel: Person
      to:
        nodeType:
          typeLabel: Person
      via:
        typeLabel: KNOWS
        implies:
          propertyTypes:
          - name: since
            valueType: INTEGER
```

**Change to**:
```yaml
- edgeType:
    directed:
      from:
        nodeType:
          typeLabel: Person
      to:
        nodeType:
          typeLabel: Person
      via:
        typeLabel: KNOWS
        implies:
          propertyTypes:
          - name: since
            valueType: INTEGER
```

Apply the same fix to both edge types (KNOWS and WORKS_AT) in both test files.

## Validation After Fix

After removing the duplicate `typeLabel` from edgeType level:
1. Re-run `python validate_phase_e_locations_2_3.py`
2. Expected result: All 4 files should pass (2/2 Location 2 + 2/2 Location 3)

## Conclusion

**The TI wrapper system at Location 3 is working correctly.**

The validation failures were caused by **test file content errors** (incorrect edge type structure), not by schema issues with TI wrappers.

**Next Action**: Update the two test files to use correct E02-compliant edge type syntax, then re-validate.
