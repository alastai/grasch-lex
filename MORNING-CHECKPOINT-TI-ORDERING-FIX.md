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

## Expected YAML Changes

**WRONG (current - TI inside content)**:
```yaml
graphType:
  nodeTypes:
    - exactlyOf:        # TI INSIDE the array item
        concrete:
          typeLabel: Person
```

**CORRECT (after fix - TI outside content)**:
```yaml
graphType:
  exactlyOf:            # TI OUTSIDE, wrapping nodeTypes
    concrete:
      nodeTypes:
        - typeLabel: Person
```

**Files Likely Needing Updates**:
- Phase E test files (locations 2-5)
- Any files using array-level TI wrappers
- Import test files using wrong-order syntax

**Files Likely OK**:
- Phase A-D test files (locations 6-8 already correct)
- Files using only bare (0-level) syntax

## Commands to Run (After Fix)

```bash
# First: Check which files fail with new schema
python validate_all_examples.py  # Will show which files need YAML updates

# After updating YAML: Validate specific locations
python validate_phase_e_locations_2_3.py
python validate_phase_e_locations_4_5.py

# Verify Phases A-D still work (should be unchanged)
python validate_phase_a_corrected.py
python validate_phase_b.py
python validate_phase_c.py
python validate_phase_d.py
```

## Next Steps for Morning Session

1. **Read Location 1 pattern** from schema (lines ~433-800)
2. **Identify Locations 2-7** in schema
3. **Apply correct pattern** to each location
4. **Test validation** - expect failures (this is GOOD)
5. **Identify which YAML files use wrong syntax**
6. **Update YAML files** to use correct TI placement
7. **Re-test validation** - should now pass
8. **Create completion summary**
9. **Checkpoint** for next phase (imports)

## Key Mindset Shift

**OLD thinking**: "Don't break the tests"
**CORRECT thinking**: "Fix the schema to match the design, then fix the tests to match the design"

The tests were written to pass a broken schema. After fixing the schema, we fix the tests. This is progress, not regression.

## Notes

- Don't rush this - schema surgery requires precision
- Test incrementally (fix one location, test, repeat)
- Keep backup of original schema
- Document any unexpected issues
- The pattern is already proven at Location 1 - just replicate it

---

**Ready to execute in morning session** ✓


---

## CRITICAL ADDITION: Sibling Testing Requirements

After fixing the ordering, we MUST test sibling behavior at all three interpretation levels:

### 1. GraphType Level (Location 1)
**Test**: Multiple sibling TI wrappers with different interpretation facets

```yaml
# SHOULD PASS - Different interpretation facets as siblings
graphType:
  propertyGraphDataModel: true
  nodeTypes:
    - typeLabel: Person
  exactlyOf:
    nodeTypes:
      - typeLabel: Company
  subtypesOf:
    abstract:
      nodeTypes:
        - typeLabel: Entity
  edgeTypes:
    - typeLabel: WORKS_FOR
```

```yaml
# SHOULD FAIL - Duplicate nodeTypes property (YAML limitation)
graphType:
  nodeTypes:
    - typeLabel: Person
  nodeTypes:  # ERROR - duplicate key in YAML
    - typeLabel: Company
```

### 2. Array Level (Locations 4-5: PartitionBlockItem)
**Test**: Multiple sibling partition blocks in nodeTypes/edgeTypes arrays

```yaml
# SHOULD PASS - Different TI wrappers as array items
graphType:
  nodeTypes:
    - typeLabel: Person  # 0-level (bare)
    - abstract:  # 1-level
        typeLabel: Entity
    - exactlyOf:  # 2-level
        concrete:
          typeLabel: Company
    - subtypesOf:  # 2-level, different facet
        abstract:
          typeLabel: Thing
```

### 3. Individual Type Level (Locations 6-7)
**Test**: TI wrappers on individual NodeType/EdgeType definitions

```yaml
# SHOULD PASS - TI wrapper on individual type
nodeTypes:
  - subtypesOf:
      abstract:
        typeLabel: Entity
        implies:
          propertyTypes:
            - name: id
              valueType: INTEGER
```

### Test Files to Create

**Positive Tests** (should validate):
1. `test-siblings-graphtype-level.yaml` - Multiple TI siblings at GraphType
2. `test-siblings-array-level.yaml` - Multiple partition blocks in arrays  
3. `test-siblings-mixed.yaml` - Combination of all levels
4. `test-siblings-interleaved.yaml` - nodeTypes, edgeTypes, nodeTypes, edgeTypes pattern

**Negative Tests** (should fail validation):
1. `test-siblings-duplicate-nodetypes-INVALID.yaml` - Duplicate nodeTypes property
2. `test-siblings-duplicate-edgetypes-INVALID.yaml` - Duplicate edgeTypes property
3. `test-siblings-duplicate-interpretation-INVALID.yaml` - Same interpretation facet twice

### Validation Script

Create `test_sibling_validation.py`:

```python
"""Test sibling TI wrapper behavior."""

def test_positive_siblings():
    """Test that valid sibling patterns pass."""
    files = [
        "test-siblings-graphtype-level.yaml",
        "test-siblings-array-level.yaml",
        "test-siblings-mixed.yaml",
        "test-siblings-interleaved.yaml"
    ]
    for f in files:
        result = validate_yaml(f)
        assert result.valid, f"{f} should validate but failed"
        print(f"✅ {f} - PASSED")

def test_negative_siblings():
    """Test that invalid sibling patterns fail."""
    files = [
        "test-siblings-duplicate-nodetypes-INVALID.yaml",
        "test-siblings-duplicate-edgetypes-INVALID.yaml",
        "test-siblings-duplicate-interpretation-INVALID.yaml"
    ]
    for f in files:
        result = validate_yaml(f)
        assert not result.valid, f"{f} should fail but passed"
        print(f"✅ {f} - FAILED AS EXPECTED")
```

## Updated Success Criteria

After schema fix, ALL of these must work:

1. ✓ All 8 locations support 0/1/2-level TI syntax
2. ✓ Multiple siblings with DIFFERENT interpretation facets work
3. ✓ Duplicate properties correctly fail (YAML constraint)
4. ✓ Interleaved nodeTypes/edgeTypes siblings work
5. ✓ All existing examples validate
6. ✓ No regressions in Phases A-D

## Morning Session Expanded Tasks

1. Fix schema ordering at 6 locations
2. Create sibling test examples (positive + negative)
3. Create validation script for siblings
4. Run comprehensive validation
5. Document results
6. Checkpoint for import system work
