# Root Cause - Complete Analysis

## Executive Summary

**The schema is NOT broken!** The validation failures were caused by test data using incorrect LEX-2026 syntax.

## The Problem

Our test data was using:
```yaml
nodeType:
  typeLabel: Person
  implies:
    labels: [Person]
    properties: {name: "STRING"}  # ❌ WRONG
```

But the schema expects:
```yaml
nodeType:
  typeLabel: Person
  implies:
    labels: [Person]
    propertyTypes:  # ✅ CORRECT
      - name: name
        valueType: STRING
```

## Investigation Trail

We systematically traced through the validation chain:

1. ✅ **Root oneOf** - Correctly defines catalog/graphSchema/graph options
2. ✅ **GraphSchemaContent** - Requires `pathName` and `graphType`
3. ✅ **GraphType** - Requires `propertyGraphDataModel`
4. ✅ **NodeTypesProperty** - First option is bare array (NodeTypesArray)
5. ✅ **NodeTypesArray** - Items are NodeTypeItem
6. ✅ **NodeTypeItem** - First option is bare NodeType
7. ✅ **NodeType** - Has `nodeType` property with oneOf of 5 options
8. ❌ **nodeType content** - Failed because:
   - Used `properties` instead of `propertyTypes`
   - Used object syntax `{name: "STRING"}` instead of array of PropertyType objects

## PropertyType Structure

According to the schema (lines 1387-1433), PropertyType is:

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "valueType": {
      "type": "string",
      "enum": ["STRING", "INTEGER", "FLOAT", "BOOLEAN", ...]
    },
    "notNull": {"type": "boolean"}
  },
  "required": ["name", "valueType"]
}
```

## Correct LEX-2026 Syntax

### Minimal Example
```yaml
graphSchema:
  pathName: /test/schema
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            labels: [Person]
            propertyTypes:
              - name: name
                valueType: STRING
              - name: age
                valueType: INTEGER
```

### With TI Wrappers
```yaml
graphSchema:
  pathName: /test/schema
  graphType:
    propertyGraphDataModel:
      valueTypeSystemName: CANONICAL
    nodeTypes:
      # 0-level (bare)
      - nodeType:
          typeLabel: Person
          implies:
            labels: [Person]
            propertyTypes:
              - name: name
                valueType: STRING
      
      # 1-level (abstract)
      - abstract:
          nodeType:
            typeLabel: Vehicle
            implies:
              labels: [Vehicle]
              propertyTypes:
                - name: make
                  valueType: STRING
      
      # 2-level (exactlyOf: concrete:)
      - exactlyOf:
          concrete:
            nodeType:
              typeLabel: Company
              implies:
                labels: [Company]
                propertyTypes:
                  - name: name
                    valueType: STRING
```

## Phase A Status

### What We Accomplished
1. ✅ Added missing 2-level `properSubtypesOf` wrapper to NodeTypeItem
2. ✅ Identified that TI wrapper support already exists in the schema
3. ✅ Discovered the root cause of validation failures (test syntax error)
4. ✅ Documented correct LEX-2026 syntax

### What's Next
1. Update Phase A test file with correct syntax
2. Validate that all TI wrapper patterns work
3. Mark Phase A as complete
4. Move to Phase B (EdgeType TI wrappers)

## Key Learnings

1. **The schema is correct** - It properly implements LEX-2026 syntax
2. **Test data matters** - Always verify syntax against schema definitions
3. **Systematic debugging works** - Tracing through the validation chain level by level found the issue
4. **PropertyTypes vs Properties** - LEX-2026 uses `propertyTypes` as an array, not `properties` as an object

## Files to Update

1. `src/grasch/examples/test-phase-a-nodetype-ti.yaml` - Fix syntax
2. All other test YAML files - Verify they use correct syntax
3. Documentation - Add examples of correct LEX-2026 syntax

## Validation Requirements

For a graphSchema to validate, it must have:
1. `pathName` (string)
2. `graphType` object with:
   - `propertyGraphDataModel` (object with valueTypeSystemName or import)
   - Optional: `nodeTypes`, `edgeTypes`, etc.
3. If nodeTypes present, each must use correct PropertyType array syntax

## Next Action

Create a corrected Phase A test file and validate it successfully!
