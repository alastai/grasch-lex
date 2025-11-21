# Subtype and Abstract Type Test Summary

## Overview

Created `lex-2026.0.3.2-subtype-abstract-test.yaml` to comprehensively test all subtype, supertype, and abstract patterns that the JSON Schema validates.

## Schema Updates

Updated the JSON Schema to allow both string and array formats for:

### 1. `supertypes` property (in ImpliesDescriptor)
```json
"supertypes": {
  "oneOf": [
    {
      "type": "string",
      "description": "Single supertype label"
    },
    {
      "type": "array",
      "description": "Set of supertype labels",
      "items": {"type": "string"},
      "uniqueItems": true,
      "minItems": 1
    }
  ]
}
```

### 2. `extends` property (in NodeType and EdgeType)
```json
"extends": {
  "oneOf": [
    {
      "type": "string",
      "description": "Single supertype this type extends"
    },
    {
      "type": "array",
      "description": "Supertypes this type extends",
      "items": {"type": "string"},
      "uniqueItems": true,
      "minItems": 1
    }
  ]
}
```

## Test File Patterns

The test file demonstrates 13 patterns:

### Node Type Patterns (7)

1. **Base type** - No supertypes
2. **Subtype with supertypes (singleton string)** - `supertypes: Person`
3. **Subtype with supertypes (array, one element)** - `supertypes: [Person]`
4. **Subtype with multiple supertypes** - `supertypes: [Employee, Person]`
5. **Subtype using extends (singleton string)** - `extends: Manager`
6. **Subtype using extends (array, one element)** - `extends: [Director]`
7. **Subtype using extends (multiple elements)** - `extends: [VicePresident, Director]`

### Edge Type Patterns (5)

8. **Base edge type** - No supertypes
9. **Edge subtype with supertypes (singleton string)** - `supertypes: KNOWS`
10. **Edge subtype with supertypes (array)** - `supertypes: [KNOWS]`
11. **Edge subtype using extends (singleton string)** - `extends: FRIENDSHIP`
12. **Edge subtype using extends (array)** - `extends: [CLOSE_FRIEND]`

### GraphType Pattern (1)

13. **allowSubtypesOf with abstractSupertypes** - Defines abstract supertypes at GraphType level

## Validation Results

All 14 example files now validate successfully:

```
Total files: 14
Valid: 14
Invalid: 0
```

## Key Findings

### What the Schema VALIDATES

✓ `supertypes` property (string or array)
✓ `extends` property (string or array)  
✓ `adding` property with labels and propertyTypes
✓ `allowSubtypesOf.abstractSupertypes` structure

### What the Schema DOES NOT VALIDATE

✗ `abstract:` wrapper (syntactic marker only)
✗ `abstractSupertype:` wrapper (syntactic marker only)
✗ `sealed:` wrapper (syntactic marker only)
✗ `final:` wrapper (syntactic marker only)

These wrappers are demonstrated in:
- `lex-2026.0.3.2-node-type-syntax-examples.yaml`
- `lex-2026.0.3.2-edge-type-syntax-examples.yaml`

But they are NOT enforced by JSON Schema validation - they are syntactic markers for application logic to interpret.

## Usage

The test file serves as:

1. **Schema validation test** - Ensures the schema correctly handles all subtype patterns
2. **Documentation** - Shows developers all supported syntax variations
3. **Regression test** - Prevents breaking changes to subtype/supertype support

## Files Modified

1. `src/grasch/schemas/lex-2026.0.3.2.schema.json` - Updated to allow string or array for `supertypes` and `extends`
2. `src/grasch/examples/lex-2026.0.3.2-subtype-abstract-test.yaml` - New comprehensive test file
3. `validate_examples.py` - Added new test file to validation suite

## Conclusion

The schema now properly validates both singleton string and array formats for `supertypes` and `extends`, matching the flexibility shown in the comprehensive pattern examples. All 14 example files validate successfully.
