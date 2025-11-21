# Schema oneOf Pattern Analysis

## Current Status

**Validation Output**: ✅ Improved to show "BEFORE IMPORTS: SUCCESS/FAILURE" and "AFTER IMPORTS: SUCCESS/FAILURE"

**Validation Results**: 7/14 files passing (50%)
- All files pass BEFORE IMPORTS validation ✅
- Some files fail AFTER IMPORTS validation ✗

## The Pattern: propertyGraphDataModel

The `propertyGraphDataModel` uses a simple oneOf pattern:

```json
"propertyGraphDataModel": {
  "oneOf": [
    {
      "type": "object",
      "properties": {"import": {"type": "string"}},
      "required": ["import"],
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "Inline values",
      "properties": {
        "valueTypeSystemName": {...},
        "graphPreferredName": {...},
        // ... all inline properties
      },
      "additionalProperties": false
    }
  ]
}
```

**This pattern works for**:
- BEFORE: `{import: "file.yaml"}` → matches option 1
- AFTER: `{valueTypeSystemName: "...", graphPreferredName: "...", ...}` → matches option 2

## Other Importable Locations

According to LEX-2026.0.3.2-DOCUMENT-TYPES-AND-IMPORTS.md, these elements support imports:

1. ✅ **propertyGraphDataModel** - Has oneOf pattern (works!)
2. ⚠️ **nodeTypes** - Has complex oneOf pattern (partially works)
3. ⚠️ **edgeTypes** - Has complex oneOf pattern (partially works)
4. ❓ **directories** (in Catalog) - Need to check
5. ❓ **graphSchema** (in Graph document) - Need to check
6. ❓ **graphStorageSchema** (in Graph document) - Need to check

## nodeTypes/edgeTypes Pattern

Current pattern:
```json
"nodeTypes": {
  "oneOf": [
    {
      "type": "array",
      "items": {
        "oneOf": [
          {"$ref": "#/$defs/NodeType"},
          {
            "type": "object",
            "properties": {"import": {"type": "string"}},
            "required": ["import"]
          }
        ]
      }
    },
    {
      "type": "object",
      "properties": {"import": {"type": "string"}},
      "required": ["import"],
      "maxProperties": 1
    }
  ]
}
```

**This pattern handles**:
- BEFORE: `{import: "file.yaml"}` → matches option 2 (import whole array)
- BEFORE: `[{nodeType: {...}}, {import: "file.yaml"}]` → matches option 1 (mixed array)
- AFTER: `[{nodeType: {...}}, ...]` → should match option 1

## Why Some Files Fail After Preprocessing

The validation errors show:
- Error at root level with `oneOf` validator
- Message: "not valid under any of the given schemas"

**Possible causes**:
1. The preprocessed content has structures that don't match any oneOf option
2. There might be `additionalProperties: false` constraints that are too restrictive
3. Complex nested structures (like edge types with different endpoint syntaxes) might not validate

## Files Failing AFTER IMPORTS

1. ✗ lex-2026.0.3.2-all-import-patterns.yaml
2. ✗ lex-2026.0.3.2-complete-import-example.yaml
3. ✗ lex-2026.0.3.2-finbench-sf1-graph.yaml
4. ✗ lex-2026.0.3.2-minimal-import-example.yaml
5. ✗ lex-2026.0.3.2-mixed-import-example.yaml
6. ✗ lex-2026.0.3.2-snb-schema.yaml
7. ✗ lex-2026.0.3.2-type-definition-syntax-examples.yaml

## Investigation Needed

### 1. Check Edge Type Definitions
The `all-import-patterns` file imports comprehensive edge type examples that use various endpoint syntaxes:
- `from/to`
- `src/dst`
- `tail/head`
- `between/and`

These might not all be properly defined in the schema.

### 2. Check for Missing oneOf Patterns
Some importable locations might not have proper oneOf patterns:
- `graphSchema` import in Graph documents
- `graphStorageSchema` import
- `directories` import in Catalog

### 3. Check additionalProperties Constraints
Some definitions might have `additionalProperties: false` that reject valid preprocessed content.

## Recommended Next Steps

### Step 1: Identify Specific Validation Failures
For each failing file, determine:
- What specific schema path is failing?
- Which oneOf option is it trying to match?
- What property or structure is causing the mismatch?

### Step 2: Fix Schema Definitions
Based on findings, update schema to:
- Ensure all oneOf patterns accept both pre and post-import structures
- Remove overly restrictive `additionalProperties: false` where needed
- Add missing oneOf patterns for importable elements

### Step 3: Test Incrementally
After each schema fix:
- Run validation
- Check if more files pass
- Document what was fixed

## Tools Created

1. `debug_validation_failure.py` - Compare passing vs failing files
2. `detailed_error_check.py` - Get detailed oneOf error context
3. `compare_structures.py` - Compare preprocessed structures

---

**Date**: November 19, 2024
**Status**: Analysis complete, validation output improved
**Next**: Detailed investigation of specific validation failures
