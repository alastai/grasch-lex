# Task 2: Schema Locations Identified

**Date**: 2024-12-06  
**Task**: Identify Schema Locations for Fixes  
**Status**: ✅ COMPLETE

## Summary

Successfully identified exact line numbers and current structure for all 6 broken TI locations in `src/grasch/schemas/lex-2026.0.3.2.schema.json`.

## Location Details

### Location 2: NodeTypesProperty
**Line Number**: 2316  
**Definition Name**: `NodeTypesProperty`  
**Current Structure**: Uses `oneOf` pattern with multiple options  
**Problem**: Only allows ONE nodeTypes property at GraphType level (cannot have siblings)  
**Target**: Support multiple sibling TI-wrapped nodeTypes properties at GraphType level

**Current Pattern**:
```json
"NodeTypesProperty": {
  "description": "The nodeTypes property with optional type interpretation wrappers",
  "oneOf": [
    {
      "$ref": "#/$defs/NodeTypesArray",
      "description": "Zero-level: bare array"
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract",
      "required": ["abstract"],
      "properties": {
        "abstract": {
          "oneOf": [
            { "$ref": "#/$defs/NodeTypesArray" },
            { "import": ... }
          ]
        }
      }
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete",
      ...
    }
  ]
}
```

### Location 3: EdgeTypesProperty
**Line Number**: 3027  
**Definition Name**: `EdgeTypesProperty`  
**Current Structure**: Uses `oneOf` pattern with multiple options  
**Problem**: Only allows ONE edgeTypes property at GraphType level (cannot have siblings)  
**Target**: Support multiple sibling TI-wrapped edgeTypes properties at GraphType level

**Current Pattern**: Same structure as NodeTypesProperty but for edgeTypes

### Location 4: NodeTypeArray
**Line Number**: 1918  
**Definition Name**: `NodeTypeItem` (schema internal name)  
**Current Structure**: Uses `oneOf` pattern with options for single types and array subsequences  
**Problem**: TI wrappers are inside array items (wrong order)  
**Target**: Support TI-wrapped subsequences within nodeTypes arrays

**Current Pattern**:
```json
"NodeTypeItem": {
  "description": "A single item in a nodeTypes array - can be a plain NodeType, wrapped with interpretation, an array subsequence (Location 4), or an import",
  "oneOf": [
    {
      "$ref": "#/$defs/NodeType",
      "description": "Zero-level wrapper (bare NodeType)"
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract - for SINGLE NodeType",
      "required": ["abstract"],
      "properties": {
        "abstract": { "$ref": "#/$defs/NodeType" }
      }
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract - for ARRAY subsequence (Location 4)",
      "required": ["abstract"],
      "properties": {
        "abstract": {
          "type": "array",
          "items": { "$ref": "#/$defs/NodeType" },
          "minItems": 1
        }
      }
    },
    ...
  ]
}
```

**Note**: This location already has some support for array subsequences, but needs refinement. Array items can be either bare types OR TI-wrapped subsequences (arrays within the array).

### Location 5: EdgeTypeArray
**Line Number**: 2629  
**Definition Name**: `EdgeTypeItem` (schema internal name)  
**Current Structure**: Uses `oneOf` pattern with options for single types and array subsequences  
**Problem**: TI wrappers are inside array items (wrong order)  
**Target**: Support TI-wrapped subsequences within edgeTypes arrays

**Current Pattern**: Same structure as Location 4 but for EdgeTypes

**Note**: This location already has some support for array subsequences, but needs refinement. Array items can be either bare types OR TI-wrapped subsequences (arrays within the array).

### Location 6: NodeType (Individual)
**Line Number**: 1501  
**Definition Name**: `NodeType`  
**Current Structure**: Object with `nodeType` property containing type definition  
**Problem**: No TI wrapper support at this level  
**Target**: Add TI wrapper support around individual NodeType content

**Current Pattern**:
```json
"NodeType": {
  "type": "object",
  "description": "Node type descriptor with flexible identification",
  "properties": {
    "nodeType": {
      "type": "object",
      "description": "Node type container with identifier and implies or extends",
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "index": { "type": "integer", ... },
            "implies": { "$ref": "#/$defs/ImpliesDescriptor" }
          },
          "required": ["index", "implies"]
        },
        {
          "type": "object",
          "properties": {
            "typeLabel": { "type": "string", ... },
            "implies": { "$ref": "#/$defs/ImpliesDescriptor" }
          },
          "required": ["typeLabel"]
        },
        ...
      ]
    }
  },
  "required": ["nodeType"],
  "additionalProperties": false
}
```

**Note**: This is the definition for a single NodeType. It currently has no TI wrapper support.

### Location 7: EdgeType (Individual)
**Line Number**: 1805  
**Definition Name**: `EdgeType`  
**Current Structure**: Object with `edgeType` property containing type definition  
**Problem**: No TI wrapper support at this level  
**Target**: Add TI wrapper support around individual EdgeType content

**Current Pattern**:
```json
"EdgeType": {
  "type": "object",
  "description": "Edge type descriptor using LEX-2026 directed/undirected syntax",
  "properties": {
    "edgeType": {
      "type": "object",
      "description": "Edge type with directed or undirected specification",
      "oneOf": [
        { "$ref": "#/$defs/DirectedEdgeDescriptor" },
        { "$ref": "#/$defs/UndirectedEdgeDescriptor" }
      ]
    }
  },
  "required": ["edgeType"],
  "additionalProperties": false
}
```

**Note**: This is the definition for a single EdgeType. It currently has no TI wrapper support.

## Key Observations

### Locations 2-3 (NodeTypesProperty / EdgeTypesProperty)
- **Current Issue**: Use `oneOf` pattern which only allows ONE property at GraphType level
- **Fix Required**: Replace with explicit properties approach (without oneOf) to allow siblings
- **Pattern to Use**: Explicit properties for `concrete:`, `abstract:`, `sealed:`, `final:`, `exactlyOf:`, `subtypesOf:`, `properSubtypesOf:`

### Locations 4-5 (NodeTypeArray / EdgeTypeArray)
- **Current Issue**: Already have some array subsequence support, but structure needs refinement
- **Fix Required**: Support TI-wrapped subsequences as array items (dividing the array into segments)
- **Key Distinction**: TI-wrapped subsequence with 1 item ≠ single type (Location 6/7)

### Locations 6-7 (NodeType / EdgeType)
- **Current Issue**: No TI wrapper support at all
- **Fix Required**: Add complete TI pattern wrapping the type content
- **Pattern to Use**: oneOf pattern allowing bare type OR TI-wrapped type

## Reference Pattern

**GraphType** (lines 433-800) already has the CORRECT `patternProperties` pattern. This should be used as the reference for all fixes.

## Next Steps

1. ✅ Task 2 Complete - All locations identified
2. ⏭️ Task 3 - Create schema backup
3. ⏭️ Task 4 - Fix Edge Label Container Structure (E02 - PREREQUISITE)
4. ⏭️ Tasks 8-16 - Fix each location using the patterns documented above

## Files Referenced

- `src/grasch/schemas/lex-2026.0.3.2.schema.json` - Main schema file
- `.kiro/specs/ti-ordering-refactor/design.md` - Design document with target patterns
- `.kiro/specs/ti-ordering-refactor/tasks.md` - Task list

## Requirements Satisfied

- _Requirements: 2.1-2.7_ - All 6 broken locations identified with exact line numbers and current structure documented
