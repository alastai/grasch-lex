# Refactor Complete: defaults → propertyGraphDataModel

## Summary

Successfully refactored the schema and all example files to:
1. ✅ Rename `defaults` to `propertyGraphDataModel`
2. ✅ Move `valueTypeSystemName` from `graphSchema` level into `propertyGraphDataModel`

---

## Changes Made

### 1. Terminology Change
- **Old**: `defaults:`
- **New**: `propertyGraphDataModel:`

### 2. Structure Change

**Before**:
```yaml
graphSchema:
  pathName: /example
  valueTypeSystemName: GQL  # At graphSchema level
  graphType:
    defaults:  # Old name
      graphPreferredName: GRAPH
      # ... other settings
```

**After**:
```yaml
graphSchema:
  pathName: /example
  graphType:
    propertyGraphDataModel:  # New name
      valueTypeSystemName: GQL  # Moved inside
      graphPreferredName: GRAPH
      # ... other settings
```

---

## Files Updated

### YAML Example Files (10 files)
1. ✅ lex-2026.0.3.2-all-import-patterns.yaml
2. ✅ lex-2026.0.3.2-comprehensive-import-example.yaml
3. ✅ lex-2026.0.3.2-finbench-schema.yaml
4. ✅ lex-2026.0.3.2-minimal-import-example.yaml
5. ✅ lex-2026.0.3.2-minimal-test.yaml
6. ✅ lex-2026.0.3.2-mixed-import-example.yaml
7. ✅ lex-2026.0.3.2-snb-schema.yaml
8. ✅ lex-2026.0.3.2-snb-special-identification-example.yaml
9. ✅ lex-2026.0.3.2-subtype-abstract-test.yaml
10. ✅ lex-2026.0.3.2-type-definition-syntax-examples.yaml

### JSON Schema Files (2 files)
1. ✅ src/grasch/schemas/lex-2026.0.3.2.schema.json
2. ✅ src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json

### Import Files
- ✅ lex-2026.0.3.2-graph-type-defaults.yaml (already had `valueTypeSystemName`)

---

## Validation Results

### Before Refactor: 2/14 files passing (14%)
- Only catalog files (no imports) were passing

### After Refactor: 7/14 files passing (50%) ✅ MAJOR IMPROVEMENT

**Now Passing**:
1. ✅ lex-2026.0.3.2-comprehensive-import-example.yaml (NEW!)
2. ✅ lex-2026.0.3.2-example-catalog-no-iri.yaml
3. ✅ lex-2026.0.3.2-example-catalog.yaml
4. ✅ lex-2026.0.3.2-finbench-schema.yaml (NEW!)
5. ✅ lex-2026.0.3.2-minimal-test.yaml (NEW!)
6. ✅ lex-2026.0.3.2-snb-special-identification-example.yaml (NEW!)
7. ✅ lex-2026.0.3.2-subtype-abstract-test.yaml (NEW!)

**Still Failing (7 files)**:
1. ✗ lex-2026.0.3.2-all-import-patterns.yaml
2. ✗ lex-2026.0.3.2-complete-import-example.yaml
3. ✗ lex-2026.0.3.2-finbench-sf1-graph.yaml
4. ✗ lex-2026.0.3.2-minimal-import-example.yaml
5. ✗ lex-2026.0.3.2-mixed-import-example.yaml
6. ✗ lex-2026.0.3.2-snb-schema.yaml
7. ✗ lex-2026.0.3.2-type-definition-syntax-examples.yaml

---

## Schema Changes Detail

### GraphType Definition
```json
{
  "GraphType": {
    "required": ["propertyGraphDataModel"],  // Changed from "defaults"
    "properties": {
      "propertyGraphDataModel": {  // Renamed from "defaults"
        "oneOf": [
          {
            "type": "object",
            "properties": {
              "import": {
                "type": "string",
                "description": "Import file path for default values"
              }
            }
          },
          {
            "type": "object",
            "description": "Inline default values for graph type",
            "properties": {
              "valueTypeSystemName": {  // MOVED HERE from GraphSchemaContent
                "type": "string",
                "enum": ["CANONICAL", "CYPHER", "GQL", "SQL"],
                "default": "CANONICAL"
              },
              "graphPreferredName": { "type": "string" },
              // ... other properties
            }
          }
        ]
      }
    }
  }
}
```

### GraphSchemaContent Definition
```json
{
  "GraphSchemaContent": {
    "properties": {
      "pathName": { "type": "string" },
      // valueTypeSystemName REMOVED from here
      "graphType": { "$ref": "#/$defs/GraphType" }
    }
  }
}
```

---

## Remaining Issues

The 7 files still failing are due to **preprocessed validation issues** (not the refactoring):
- Raw validation passes ✅
- Preprocessed validation fails ✗

This is the same issue identified earlier - the schema's `oneOf` patterns for imports don't handle all preprocessed structures correctly. This is a separate issue from the refactoring.

---

## Impact on Import Preprocessor

The import preprocessor correctly handles the renamed `propertyGraphDataModel`:
- ✅ Wrapper stripping works with new name
- ✅ Import resolution works correctly
- ✅ Content inlining works as expected

---

## Next Steps

1. ✅ **Refactoring Complete** - All files updated with new terminology
2. ⚠️ **Remaining Validation Issues** - Need to address preprocessed validation failures
   - These are schema oneOf pattern issues
   - Not related to the refactoring
   - May need post-import schema or schema adjustments

---

## Tools Created

1. `refactor_defaults_to_propertygraphdatamodel.py` - Automated refactoring script
2. `REFACTOR-PLAN-DEFAULTS-TO-PROPERTYGRAPHDATAMODEL.md` - Planning document

---

**Date**: November 19, 2024  
**Status**: ✅ REFACTORING COMPLETE  
**Result**: 50% validation success rate (up from 14%)  
**Impact**: Major improvement in validation, clear terminology

