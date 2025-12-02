# Final Location Clarification

**Date**: 2024-12-02  
**Status**: User Clarification - Definitive Understanding

## User's Definitive Statement

> "At Location 1 we need to have a TI, i.e. 0- 1- or 2-level statements about type interpretation, surrounding one and only one graphType. At Locations 2 and 3 we need to have a TI (same structure) surrounding any one of (all) nodeType and edgeType objects, these are siblings and they may occur in any order."

## Interpretation

### Location 1: graphTypeInterpretation

**What wraps what**: TI wrappers (0/1/2-level) wrap ONE `graphType` object

**YAML Example**:
```yaml
graphSchema:
  pathName: /mySchema
  # Option 1: Bare graphType (0-level TI)
  graphType:
    nodeTypes: [...]
    edgeTypes: [...]
  
  # OR Option 2: 1-level TI wrapping graphType
  abstract:
    graphType:
      nodeTypes: [...]
      edgeTypes: [...]
  
  # OR Option 3: 2-level TI wrapping graphType
  subtypesOf:
    abstract:
      graphType:
        nodeTypes: [...]
        edgeTypes: [...]
```

**Key Point**: Only ONE graphType (but it can be wrapped in 0/1/2-level TI)

### Locations 2-3: nodeTypesInterpretation / edgeTypesInterpretation

**What wraps what**: TI wrappers (0/1/2-level) wrap EACH `nodeTypes` or `edgeTypes` property

**YAML Example** (WITHIN graphType):
```yaml
graphType:
  # Multiple nodeTypes properties as siblings, each with its own TI
  nodeTypes: [...]              # Bare nodeTypes (0-level TI)
  
  abstract:                     # 1-level TI wrapping nodeTypes
    nodeTypes: [...]
  
  exactlyOf:                    # 2-level TI wrapping nodeTypes
    concrete:
      nodeTypes: [...]
  
  subtypesOf:                   # 2-level TI wrapping nodeTypes
    abstract:
      nodeTypes: [...]
  
  # Multiple edgeTypes properties as siblings, each with its own TI
  edgeTypes: [...]              # Bare edgeTypes (0-level TI)
  
  concrete:                     # 1-level TI wrapping edgeTypes
    edgeTypes: [...]
  
  exactlyOf:                    # 2-level TI wrapping edgeTypes
    concrete:
      edgeTypes: [...]
```

**Key Point**: Multiple `nodeTypes` and `edgeTypes` properties as siblings, each wrapped in its own 0/1/2-level TI, in any order

## Schema Analysis Result

### Location 1 Status

Looking at GraphSchemaContent:
```json
"GraphSchemaContent": {
  "properties": {
    "graphType": { "$ref": "#/$defs/GraphType" }
  },
  "additionalProperties": false
}
```

**Current Behavior**: Only allows ONE bare `graphType` property
**Needed Behavior**: Should allow TI wrappers (0/1/2-level) to wrap the graphType
**Status**: ❓ NEEDS INVESTIGATION - Does GraphSchemaContent support TI wrappers?

### Locations 2-3 Status

Looking at GraphType (where nodeTypes/edgeTypes live):
```json
"GraphType": {
  "properties": {
    "nodeTypes": { "$ref": "#/$defs/NodeTypesProperty" }
  },
  "patternProperties": {
    "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
      "properties": {
        "nodeTypes": { ... }
      }
    }
  },
  "additionalProperties": true
}
```

**Current Behavior**: GraphType DOES support multiple sibling TI-wrapped properties
**Needed Behavior**: Same as current
**Status**: ✓ ALREADY CORRECT at GraphType level

**BUT**: NodeTypesProperty uses `oneOf` pattern (wrong!)
**Status**: ✗ NEEDS FIXING - NodeTypesProperty/EdgeTypesProperty definitions

## The Real Problem

1. **Location 1**: Need to verify if GraphSchemaContent supports TI wrappers around graphType
2. **Locations 2-3**: GraphType level is correct, but NodeTypesProperty/EdgeTypesProperty use wrong `oneOf` pattern

## Next Steps

1. Check if GraphSchemaContent needs TI wrapper support for Location 1
2. Fix NodeTypesProperty and EdgeTypesProperty to use `patternProperties` instead of `oneOf`
3. This will enable the sibling behavior the user described
