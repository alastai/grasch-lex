# Task 2 Revision - Alignment with Schema Structure

## Issue Identified

The previous attempt at Task 2 created reusable definitions that **don't align with the actual LEX-2026.0.3.2 schema structure**. The TI Location Audit revealed critical details about how the schema is organized that weren't reflected in the initial Task 2 approach.

## Key Misalignments

### 1. GraphType Structure Misunderstood
**Reality**: 
- `GraphType.properties.nodeTypes` is a top-level property that can contain:
  - A simple array of node types
  - TI-wrapped partition blocks
  - Import statements
- `GraphType.properties.edgeTypes` follows the same pattern

**Previous Approach**: Created generic `TIContentWithTwoPhaseImport` without considering the specific GraphType structure

### 2. Sub-Array Structure Overlooked
**Reality**:
- `nodeTypes` and `edgeTypes` can be **arrays of partition blocks**
- Each array item can be:
  - A bare node/edge type (singleton with implicit TI)
  - A TI-wrapped partition block (e.g., `exactlyOf:concrete: [type1, type2]`)
  - An import statement
- This is defined by `NodeTypeItem` and `EdgeTypeItem` in the schema

**Previous Approach**: Didn't account for the array-of-partition-blocks structure

### 3. Nested TI Contexts Not Addressed
**Reality**:
- `GraphType.subtypesOf.abstract.nodeTypes` is a nested TI context
- `GraphType.subtypesOf.nodeTypes` is another nested context
- These have different import semantics than top-level properties

**Previous Approach**: Treated all TI contexts uniformly

### 4. Two-Phase Import Mechanism Incomplete
**Reality**:
- **Phase 1**: Import entire TI wrapper + content (at partition block level)
  - Example: `- import: "person-types.yaml"` in a nodeTypes array
- **Phase 2**: Import content only, strip TI (at TI wrapper content level)
  - Example: `exactlyOf:concrete: import: "person-types.yaml"`

**Previous Approach**: Created definitions but didn't properly distinguish between the two phases or where each applies

## What the Audit Revealed

From `TI-LOCATION-AUDIT.md`, we learned:

### Category 1: Top-Level Properties
- `GraphType.nodeTypes` - Has oneOf with import, needs two-phase support
- `GraphType.edgeTypes` - Has oneOf with import, needs two-phase support

### Category 2: GraphType Pattern Properties (TI Wrappers)
- `GraphType.abstract.nodeTypes` - References `NodeTypesArray`, needs two-phase support
- `GraphType.exactlyOf.concrete.nodeTypes` - References `NodeTypesArray`, needs two-phase support
- Similar patterns for edgeTypes

### Category 3: Nested Properties
- `GraphType.subtypesOf.abstract.nodeTypes` - Has oneOf with import, needs two-phase support
- `GraphType.subtypesOf.nodeTypes` - Has oneOf with import, needs two-phase support

### Category 4: Array Items
- `NodeTypeItem` - Items in nodeTypes arrays, needs two-phase support in TI wrapper contents
- `EdgeTypeItem` - Items in edgeTypes arrays, needs two-phase support in TI wrapper contents

### Category 5: Property-Level TI Wrappers
- `NodeTypesProperty` - Top-level property with TI wrappers, needs two-phase support
- `EdgeTypesProperty` - Top-level property with TI wrappers, needs two-phase support

## Correct Approach for Task 2

### Required Reusable Definitions

#### 1. TI Wrapper Content Pattern
**Purpose**: Content within TI wrappers (the actual type sets)
**Supports**: 
- Singleton sets (single type)
- Multi-element sets (array of types)
- Phase 2 imports (import content only, strip TI)

```json
"TIWrapperContentNode": {
  "description": "Content within TI wrappers for node types (set delimited by indentation)",
  "oneOf": [
    {
      "description": "Inline type set",
      "anyOf": [
        {
          "description": "Singleton set (single type)",
          "$ref": "#/$defs/NodeType"
        },
        {
          "description": "Multi-element set (array of types)",
          "type": "array",
          "items": { "$ref": "#/$defs/NodeType" }
        }
      ]
    },
    {
      "description": "Phase 2: Import type definitions only (strip TI, allow reinterpretation)",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import type definitions (TI will be stripped/merged)"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

#### 2. Partition Block Item Pattern
**Purpose**: Items in nodeTypes/edgeTypes arrays (partition blocks)
**Supports**:
- Bare types (singleton with implicit TI)
- TI-wrapped partition blocks
- Phase 1 imports (import entire TI wrapper + content)

```json
"PartitionBlockItemNode": {
  "description": "Item in nodeTypes array (partition block with TI wrapper)",
  "oneOf": [
    {
      "description": "Bare node type (singleton set with implicit TI)",
      "$ref": "#/$defs/NodeType"
    },
    {
      "description": "TI-wrapped partition block",
      "type": "object",
      "patternProperties": {
        "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
          "oneOf": [
            {
              "type": "object",
              "patternProperties": {
                "^(abstract|concrete|final|sealed)$": {
                  "$ref": "#/$defs/TIWrapperContentNode"
                }
              },
              "additionalProperties": false
            },
            {
              "description": "Phase 1: Import entire TI wrapper",
              "type": "object",
              "required": ["import"],
              "properties": {
                "import": {
                  "type": "string",
                  "description": "Import TI wrapper with its type definitions"
                }
              },
              "additionalProperties": false
            }
          ]
        }
      },
      "additionalProperties": false
    },
    {
      "description": "Phase 1: Import partition block",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import TI-wrapped partition block"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

#### 3. Similar Patterns for Edge Types
- `TIWrapperContentEdge` - Same as TIWrapperContentNode but for EdgeType
- `PartitionBlockItemEdge` - Same as PartitionBlockItemNode but for EdgeType

## Revised Task 2 Deliverables

1. **TIWrapperContentNode** - Content within node type TI wrappers
2. **TIWrapperContentEdge** - Content within edge type TI wrappers
3. **PartitionBlockItemNode** - Items in nodeTypes arrays
4. **PartitionBlockItemEdge** - Items in edgeTypes arrays
5. **Documentation** - Clear explanation of two-phase import mechanism
6. **Test Cases** - Validation that patterns work correctly

## Next Steps

1. **Revise Task 2** to create the correct reusable definitions
2. **Update Tasks 3-6** to use these definitions correctly
3. **Ensure alignment** with actual schema structure throughout

## Key Takeaways

- **Schema structure matters**: Can't create generic patterns without understanding the specific structure
- **Two-phase imports are distinct**: Phase 1 (import TI+content) vs Phase 2 (import content only) apply at different levels
- **Arrays of partition blocks**: The nodeTypes/edgeTypes arrays are arrays of partition blocks, not arrays of types
- **Indentation delimits sets**: Types at the same indentation level under a TI belong to the same set
- **Singleton sets are special cases**: Single types are partition blocks with cardinality 1

