# Phase E - Schema Analysis and Fix Plan

**Date**: 2024-12-02  
**Status**: Analysis Complete - Ready for Implementation

## Test Results Baseline

Ran initial validation of sibling TI wrapper tests:

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| test-siblings-bare-only.yaml | PASS | FAIL | ❌ |
| test-siblings-mixed-0-1-level.yaml | PASS | PASS | ✅ |
| test-siblings-interleaved.yaml | PASS | FAIL | ❌ |

**Key Finding**: `test-siblings-mixed-0-1-level.yaml` PASSES, which means the schema CAN support some sibling patterns. The issue is more nuanced than initially thought.

## Schema Structure Analysis

### GraphType Definition (lines ~600-970)

**Current Structure**:
```json
{
  "properties": {
    "nodeTypes": {"$ref": "#/$defs/NodeTypesProperty"},
    "edgeTypes": {"$ref": "#/$defs/EdgeTypesProperty"},
    ...
  },
  "additionalProperties": true,  // ✅ GOOD - Allows pattern properties
  "patternProperties": {
    "^(abstract|sealed|final|concrete)$": {
      "properties": {
        "nodeTypes": {"$ref": "#/$defs/NodeTypesArray"},
        "edgeTypes": {"$ref": "#/$defs/EdgeTypesArray"}
      },
      "additionalProperties": false,
      "minProperties": 1
    },
    "^(exactlyOf|subtypesOf)$": {
      ...
    }
  }
}
```

### Why test-siblings-mixed-0-1-level.yaml PASSES

This test has:
```yaml
graphType:
  nodeTypes: [...]      # Bare nodeTypes
  abstract:             # Pattern property
    nodeTypes: [...]    # TI-wrapped nodeTypes
```

This works because:
1. Bare `nodeTypes` uses `NodeTypesProperty` reference
2. `abstract:` pattern property contains its own `nodeTypes` using `NodeTypesArray` reference
3. These are DIFFERENT schema paths, so no conflict

### Why test-siblings-bare-only.yaml FAILS

This test has:
```yaml
graphType:
  nodeTypes: [...]
  edgeTypes: [...]
```

This fails because... actually, this SHOULD work! Let me investigate further.

### Why test-siblings-interleaved.yaml FAILS

This test has:
```yaml
graphType:
  nodeTypes: [...]      # Bare
  edgeTypes: [...]      # Bare
  abstract:             # Pattern property
    nodeTypes: [...]
  concrete:             # Pattern property
    edgeTypes: [...]
```

This likely fails because of validation rules in the pattern properties or their interaction with bare properties.

## Root Cause Investigation Needed

The fact that ONE sibling test passes but others fail suggests the issue is NOT simply "pattern properties conflict with regular properties". Instead, there may be:

1. **Validation rules** in `NodeTypesProperty` or `EdgeTypesProperty` that reject certain combinations
2. **Schema constraints** in the pattern property definitions that are too restrictive
3. **Interaction issues** between multiple pattern properties

## Next Steps

1. ✅ **DONE**: Create comprehensive test suite
2. ✅ **DONE**: Run baseline validation
3. ⏳ **TODO**: Investigate `NodeTypesProperty` and `EdgeTypesProperty` definitions
4. ⏳ **TODO**: Understand why bare-only test fails
5. ⏳ **TODO**: Understand why interleaved test fails
6. ⏳ **TODO**: Identify specific schema constraints causing failures
7. ⏳ **TODO**: Implement fix
8. ⏳ **TODO**: Validate all tests pass

## Test Suite Created

### Positive Tests (7 files)
- ✅ test-siblings-bare-only.yaml
- ✅ test-siblings-mixed-0-1-level.yaml
- ✅ test-siblings-mixed-0-2-level.yaml
- ✅ test-siblings-all-1-level.yaml
- ✅ test-siblings-all-2-level.yaml
- ✅ test-siblings-interleaved.yaml
- ✅ test-siblings-complex.yaml

### Negative Tests (3 files)
- ✅ test-siblings-duplicate-bare-INVALID.yaml
- ✅ test-siblings-duplicate-interpretation-INVALID.yaml
- ✅ test-siblings-wrong-nesting-INVALID.yaml

### Validation Script
- ✅ validate_sibling_ti_wrappers.py

## Conclusion

The schema analysis reveals that sibling TI wrappers CAN work in some cases (test-siblings-mixed-0-1-level.yaml passes). The issue is more specific than a blanket "pattern properties don't work". Further investigation is needed to identify the exact constraints causing the other tests to fail.

**Status**: Ready for detailed investigation of NodeTypesProperty and EdgeTypesProperty definitions.
