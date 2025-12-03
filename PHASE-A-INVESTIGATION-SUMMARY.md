# Phase A Investigation Summary

## What We Accomplished

### 1. Analyzed Current TI Support
We discovered that the schema **already has comprehensive TI wrapper support** for nodeTypes through the `NodeTypeItem` definition (lines 1311-1620):

**Existing Support:**
- ✅ 0-level (bare): `nodeType: { ... }`
- ✅ 1-level: `abstract: { nodeType: ... }`, `concrete: { nodeType: ... }`, `final: { nodeType: ... }`, `sealed: { ... }`
- ✅ 1-level: `properSubtypesOf: { nodeType: ... }` (shorthand)
- ✅ 2-level: `exactlyOf: { concrete/abstract: { nodeType: ... } }`
- ✅ 2-level: `subtypesOf: { concrete/abstract: { nodeType: ... } }`

### 2. Added Missing 2-Level properSubtypesOf
We added the missing 2-level `properSubtypesOf` wrapper with concreteness facet:
```json
{
  "properSubtypesOf": {
    "oneOf": [
      {
        "concrete": { "nodeType": { ... } }
      },
      {
        "abstract": { "nodeType": { ... } }
      }
    ]
  }
}
```

### 3. Created Comprehensive Test File
Created `src/grasch/examples/test-phase-a-nodetype-ti.yaml` with examples of all TI wrapper patterns.

## Critical Discovery: Pre-Existing Schema Validation Issue

**The schema has a fundamental validation problem that prevents ANY graphSchema from validating!**

### Evidence
Even the simplest possible graphSchema fails validation:
```yaml
graphSchema:
  graphType:
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            labels: [Person]
            properties:
              name: STRING
```

**Error:** `is not valid under any of the given schemas` (at root level)

### Investigation Results
- ✅ Tested with current schema: FAILS
- ✅ Tested with commit 2ae9c68 (before PartitionBlockItem changes): FAILS  
- ✅ Tested with commit b31025d (before endpoint TI wrappers): FAILS
- ❌ This is a **long-standing issue**, not caused by recent changes

### Possible Root Causes

1. **Circular Reference in sealed Wrapper**
   - `NodeTypeItem` → `sealed` → `NodeTypeSetOrImport` → `NodeTypesArray` → `NodeTypeItem`
   - This creates a valid but complex circular reference

2. **Meta-Schema Compatibility**
   - Validator warns: "The schema uses meta-schema features ($dynamicRef) that are not yet supported"
   - The schema uses Draft 2020-12, but validator may not fully support it

3. **GraphSchemaContent Definition Issue**
   - The root-level validation failure suggests something in `GraphSchemaContent` is malformed

## Phase A Status

### Completed
- ✅ Analyzed existing TI support in NodeTypeItem
- ✅ Added missing 2-level properSubtypesOf wrapper
- ✅ Created comprehensive test file
- ✅ Identified pre-existing validation issue

### Blocked
- ❌ Cannot validate test file due to schema validation issue
- ❌ Cannot proceed to Phase B until root issue is resolved

## Recommendations

### Option 1: Fix Root Validation Issue First (RECOMMENDED)
1. Investigate why the schema fails at root level
2. Check if it's a validator compatibility issue (Draft 2020-12 vs validator version)
3. Test with a different JSON Schema validator
4. Fix the root cause
5. Then validate Phase A test file

### Option 2: Proceed with Schema Development
1. Assume the TI wrapper support is correct (it looks correct structurally)
2. Continue to Phase B (EdgeType TI wrappers)
3. Address validation issues later with a comprehensive fix

### Option 3: Simplify Schema Structure
1. Remove or simplify the circular reference in sealed wrapper
2. Test if that resolves the validation issue
3. Continue with Phase A validation

## Next Actions

**Immediate:**
1. Test schema with a different validator (e.g., `ajv` in Node.js)
2. Check if existing examples ever validated successfully
3. Review git history to find when validation last worked

**If Validation Can't Be Fixed Quickly:**
1. Document that Phase A structural changes are complete
2. Move to Phase B (EdgeType TI wrappers)
3. Create a separate task to fix schema validation

## Files Created

- `PHASE-A-STATUS.md` - Initial status report
- `PHASE-A-INVESTIGATION-SUMMARY.md` - This file
- `phase_a_fix_nodetype_ti_v2.py` - Script that adds 2-level properSubtypesOf
- `src/grasch/examples/test-phase-a-nodetype-ti.yaml` - Comprehensive test file
- `validate_phase_a.py` - Validation script
- `test_simple_nodetype.py` - Minimal test case
- Various debug scripts

## Conclusion

**Phase A is structurally complete** - the schema has all the necessary TI wrapper support for nodeTypes. However, we cannot validate this due to a pre-existing schema validation issue that affects even the simplest graphSchemas.

The TI wrapper definitions in `NodeTypeItem` are well-structured and comprehensive. Once the root validation issue is resolved, Phase A should pass validation immediately.
