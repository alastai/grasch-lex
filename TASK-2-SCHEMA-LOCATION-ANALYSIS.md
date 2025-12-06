# Task 2: Schema Location Analysis - Complete

**Date**: 2024-12-06  
**Task**: Identify Schema Locations for Fixes  
**Status**: ✅ COMPLETE

## Summary

I have identified the exact line numbers and documented the current structure for each of the 6 locations that need to be fixed (Locations 2-7). Location 1 was already verified as correct in Task 1.

## Schema Locations Identified

### Location 1: graphTypeInterpretation (GraphSchemaContent)
**Status**: ✅ ALREADY CORRECT (verified in Task 1)  
**Line Number**: 203-260  
**Definition Name**: `GraphSchemaContent`

**Current Structure**:
- Has `patternProperties` for TI wrappers: `^(abstract|sealed|final|concrete)$`
- Supports 0-level (bare `graphType`), 1-level, and 2-level TI syntax
- Already implements the correct pattern
- No changes needed

---

### Location 2: nodeTypesInterpretation (NodeTypesProperty)
**Status**: ❌ NEEDS FIX  
**Line Number**: 2316-2380+  
**Definition Name**: `NodeTypesProperty`

**Current Structure**:
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
            {"$ref": "#/$defs/NodeTypesArray"},
            {"type": "object", "required": ["import"], ...}
          ]
        }
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete",
      "required": ["concrete"],
      ...
    }
  ]
}
```

**Problem**: Uses `oneOf` pattern which only allows ONE option at a time. Cannot support sibling TI-wrapped properties.

**Target**: Replace with explicit properties (without oneOf) to allow multiple sibling `nodeTypes` properties with different TI wrappers at GraphType level.

---

### Location 3: edgeTypesInterpretation (EdgeTypesProperty)
**Status**: ❌ NEEDS FIX  
**Line Number**: 3027-3090+  
**Definition Name**: `EdgeTypesProperty`

**Current Structure**:
```json
"EdgeTypesProperty": {
  "description": "The edgeTypes property with optional type interpretation wrappers",
  "oneOf": [
    {
      "$ref": "#/$defs/EdgeTypesArray",
      "description": "Zero-level: bare array"
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract",
      "required": ["abstract"],
      "properties": {
        "abstract": {
          "oneOf": [
            {"$ref": "#/$defs/EdgeTypesArray"},
            {"type": "object", "required": ["import"], ...}
          ]
        }
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete",
      "required": ["concrete"],
      ...
    }
  ]
}
```

**Problem**: Same as Location 2 - uses `oneOf` pattern preventing sibling TI-wrapped properties.

**Target**: Replace with explicit properties (without oneOf) to allow multiple sibling `edgeTypes` properties with different TI wrappers at GraphType level.

**Note**: Depends on Task 4 (Edge Label Container Fix) being complete first.

---

### Location 4: nodeTypeArrayInterpretation (NodeTypeItem)
**Status**: ❌ NEEDS FIX  
**Line Number**: 1918-1980+  
**Definition Name**: `NodeTypeItem`

**Current Structure**:
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
        "abstract": {"$ref": "#/$defs/NodeType"}
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract - for ARRAY subsequence (Location 4)",
      "required": ["abstract"],
      "properties": {
        "abstract": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"},
          "minItems": 1
        }
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete - for SINGLE NodeType",
      "required": ["concrete"],
      "properties": {
        "concrete": {"$ref": "#/$defs/NodeType"}
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete - for ARRAY subsequence (Location 4)",
      "required": ["concrete"],
      "properties": {
        "concrete": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"},
          "minItems": 1
        }
      },
      "additionalProperties": false
    }
  ]
}
```

**Problem**: Mixes Location 4 (partition blocks) with Location 6 (single types) in the same definition. Needs to support 2-level TI syntax for partition blocks.

**Target**: Support partition blocks (TI-wrapped subsequences) as array items with full 0/1/2-level TI syntax. Distinguish partition blocks from single types.

---

### Location 5: edgeTypeArrayInterpretation (EdgeTypeItem)
**Status**: ❌ NEEDS FIX  
**Line Number**: 2629-2690+  
**Definition Name**: `EdgeTypeItem`

**Current Structure**:
```json
"EdgeTypeItem": {
  "description": "A single item in an edgeTypes array - can be a plain EdgeType, wrapped with interpretation, an array subsequence (Location 5), or an import",
  "oneOf": [
    {
      "$ref": "#/$defs/EdgeType",
      "description": "Zero-level wrapper (bare EdgeType)"
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract - for SINGLE EdgeType",
      "required": ["abstract"],
      "properties": {
        "abstract": {"$ref": "#/$defs/EdgeType"}
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: abstract - for ARRAY subsequence (Location 5)",
      "required": ["abstract"],
      "properties": {
        "abstract": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"},
          "minItems": 1
        }
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete - for SINGLE EdgeType",
      "required": ["concrete"],
      "properties": {
        "concrete": {"$ref": "#/$defs/EdgeType"}
      },
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "One-level wrapper: concrete - for ARRAY subsequence (Location 5)",
      "required": ["concrete"],
      "properties": {
        "concrete": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"},
          "minItems": 1
        }
      },
      "additionalProperties": false
    }
  ]
}
```

**Problem**: Same as Location 4 - mixes partition blocks with single types. Needs 2-level TI syntax support.

**Target**: Support partition blocks (TI-wrapped subsequences) as array items with full 0/1/2-level TI syntax. Distinguish partition blocks from single types.

**Note**: Depends on Task 4 (Edge Label Container Fix) being complete first.

---

### Location 6: nodeTypeInterpretation (Individual NodeType)
**Status**: ❌ NEEDS FIX  
**Line Number**: 1501-1560+  
**Definition Name**: `NodeType`

**Current Structure**:
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
            "index": {"type": "integer", "minimum": 0},
            "implies": {"$ref": "#/$defs/ImpliesDescriptor"}
          },
          "required": ["index", "implies"],
          "additionalProperties": false
        },
        {
          "type": "object",
          "properties": {
            "typeLabel": {"type": "string", "pattern": "^[a-zA-Z]"},
            "implies": {"$ref": "#/$defs/ImpliesDescriptor"}
          },
          "required": ["typeLabel"],
          "additionalProperties": false
        },
        {
          "type": "object",
          "properties": {
            "typeLabel": {"type": "string", "pattern": "^[a-zA-Z]"},
            "extends": {...}
          },
          ...
        }
      ]
    }
  },
  "required": ["nodeType"],
  "additionalProperties": false
}
```

**Problem**: No TI wrapper support. Only has bare `nodeType` property.

**Target**: Add sibling properties pattern to wrap NodeType content with full 0/1/2-level TI syntax.

---

### Location 7: edgeTypeInterpretation (EdgeType Content)
**Status**: ❌ NEEDS FIX  
**Line Number**: 1805-1870+  
**Definition Name**: `EdgeType`

**Current Structure**:
```json
"EdgeType": {
  "type": "object",
  "description": "Edge type descriptor using LEX-2026 directed/undirected syntax",
  "properties": {
    "edgeType": {
      "type": "object",
      "description": "Edge type with directed or undirected specification",
      "oneOf": [
        {"$ref": "#/$defs/DirectedEdgeDescriptor"},
        {"$ref": "#/$defs/UndirectedEdgeDescriptor"}
      ]
    }
  },
  "required": ["edgeType"],
  "additionalProperties": false
}
```

**Problem**: No TI wrapper support. Only has bare `edgeType` property.

**Target**: Add sibling properties pattern to wrap EdgeType content with full 0/1/2-level TI syntax.

**Note**: Depends on Task 4 (Edge Label Container Fix) being complete first.

---

### Location 8: edgeTypeEndpointNodeTypeInterpretation
**Status**: ✅ ALREADY CORRECT (from Phases C-D)  
**Note**: Not part of this refactoring - already working from previous implementation phases.

---

## Key Findings

### Pattern Analysis

1. **Location 1 (GraphSchemaContent)**: Uses `patternProperties` correctly - this is our reference pattern
2. **Locations 2-3 (NodeTypesProperty, EdgeTypesProperty)**: Use `oneOf` which prevents sibling TI wrappers
3. **Locations 4-5 (NodeTypeItem, EdgeTypeItem)**: Mix partition blocks with single types, need 2-level TI support
4. **Locations 6-7 (NodeType, EdgeType)**: No TI wrapper support at all

### Dependencies

- **Task 4 (Edge Label Container Fix)** must be completed before:
  - Location 3 (EdgeTypesProperty)
  - Location 5 (EdgeTypeItem)
  - Location 7 (EdgeType)

### Design Decision from Task 10.1

Per the design document and Task 10.1, we will:
- **Abandon `patternProperties` for sibling TI behavior**
- Use **explicit properties** (without oneOf) for Locations 2-3
- Use **oneOf** only for single TI wrapper locations (1, 6, 7, 8)
- Support all TI levels: 0-level (bare), 1-level (concreteness), 2-level (interpretation)

## Next Steps

Task 2 is now complete. The next task (Task 3) is to create a schema backup before making any changes.

**Ready for user approval to proceed to Task 3.**
