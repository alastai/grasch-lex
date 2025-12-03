# Design Document

## Overview

This design implements flexible type interpretation wrappers in the LEX-2026.0.3.2 JSON Schema and corrects all YAML examples to use the proper patterns. The core principle is that type interpretations (`abstract`, `final`, `sealed`, `subtypesOf`) can wrap at multiple levels but never create recursion.

## Architecture

### Schema Structure Layers

1. **GraphSchemaContent Level**: Contains top-level `nodeTypes` and `edgeTypes` properties
2. **Type Array Level**: The `nodeTypes:` or `edgeTypes:` arrays that contain type items
3. **Type Item Level**: Individual `- nodeType:` or `- edgeType:` items
4. **Type Interpretation Level**: Wrappers like `abstract`, `final` that modify interpretation

### Wrapping Patterns

Type interpretations can be applied at three levels:

```yaml
# Pattern 1: Wrap entire array
graphType:
  abstract:
    nodeTypes:
      - nodeType: TypeA
      - nodeType: TypeB

# Pattern 2: Wrap individual items
graphType:
  nodeTypes:
    - abstract:
        nodeType: TypeA
    - final:
        nodeType: TypeB

# Pattern 3: Mixed (wrap some items, leave others plain)
graphType:
  nodeTypes:
    - nodeType: TypeC          # concrete by default
    - abstract:
        nodeType: TypeA
    - final:
        nodeType: TypeB
```

## Components and Interfaces

### JSON Schema Components

#### 1. NodeTypeItem Definition

A new schema definition that represents a single item in a `nodeTypes` array:

```json
"NodeTypeItem": {
  "oneOf": [
    { "$ref": "#/$defs/NodeType" },
    { "type": "object", "required": ["abstract"], "properties": { "abstract": { "$ref": "#/$defs/NodeType" } } },
    { "type": "object", "required": ["final"], "properties": { "final": { "$ref": "#/$defs/NodeType" } } },
    { "type": "object", "required": ["import"], "properties": { "import": { "type": "string" } } }
  ]
}
```

#### 2. NodeTypesArray Definition

The array that contains NodeTypeItem objects:

```json
"NodeTypesArray": {
  "type": "array",
  "items": { "$ref": "#/$defs/NodeTypeItem" }
}
```

#### 3. NodeTypesProperty Definition

The top-level `nodeTypes` property with interpretation wrappers:

```json
"NodeTypesProperty": {
  "oneOf": [
    { "$ref": "#/$defs/NodeTypesArray" },
    { "type": "object", "required": ["abstract"], "properties": { "abstract": { "$ref": "#/$defs/NodeTypesArray" } } },
    { "type": "object", "required": ["final"], "properties": { "final": { "$ref": "#/$defs/NodeTypesArray" } } },
    { "type": "object", "required": ["sealed"], "properties": { "sealed": { "$ref": "#/$defs/NodeTypesArray" } } },
    { "type": "object", "required": ["subtypesOf"], "properties": { "subtypesOf": { "$ref": "#/$defs/NodeTypesArray" } } },
    { "type": "object", "required": ["import"], "properties": { "import": { "type": "string" } } }
  ]
}
```

#### 4. EdgeType Components

Mirror the same structure for edge types:
- `EdgeTypeItem`
- `EdgeTypesArray`
- `EdgeTypesProperty`

### No Recursion Enforcement

The schema enforces no recursion by:
1. `NodeType` definition never contains a `nodeTypes` property
2. `EdgeType` definition never contains an `edgeTypes` property
3. Type interpretation wrappers reference `NodeTypesArray` which contains `NodeTypeItem` which references `NodeType` (terminal)

## Data Models

### Type Interpretation Wrapper Model

```typescript
type TypeInterpretation = 'abstract' | 'final' | 'sealed' | 'subtypesOf';

interface NodeTypeItem {
  nodeType?: NodeTypeDefinition;
  abstract?: NodeTypeDefinition;
  final?: NodeTypeDefinition;
  import?: string;
}

interface NodeTypesProperty {
  // Direct array
  nodeTypes?: NodeTypeItem[];
  
  // Or wrapped
  abstract?: { nodeTypes: NodeTypeItem[] };
  final?: { nodeTypes: NodeTypeItem[] };
  sealed?: { nodeTypes: NodeTypeItem[] };
  subtypesOf?: { nodeTypes: NodeTypeItem[] };
  
  // Or imported
  import?: string;
}
```

## Error Handling

### Validation Errors

1. **Recursive Nesting Error**: If `nodeType` contains `nodeTypes`, reject with clear message
2. **Invalid Wrapper Error**: If interpretation wrapper is used incorrectly
3. **Import Resolution Error**: If imported file doesn't match expected structure

### Error Messages

- "nodeType definitions cannot contain nodeTypes arrays"
- "Type interpretation wrappers cannot be nested"
- "Invalid structure for {interpretation} wrapper"

## Testing Strategy

### Schema Validation Tests

1. Test basic pattern: `nodeTypes: [- nodeType:]`
2. Test array-level wrapping: `abstract: nodeTypes: [...]`
3. Test item-level wrapping: `nodeTypes: [- abstract: nodeType:]`
4. Test mixed wrapping: combination of wrapped and unwrapped items
5. Test import within interpretations
6. Test rejection of recursive patterns

### Example File Corrections

1. **snb-place-hierarchy.yaml**: Change from nested structure to proper wrapping
2. **snb-organisation-hierarchy.yaml**: Apply same corrections
3. **All 14 examples**: Validate after corrections

### Validation Success Criteria

- All 14 example files validate successfully
- Schema correctly rejects invalid patterns
- Clear error messages for common mistakes

## Implementation Notes

### Current Schema Issues

The current schema at lines 448-750 has complex nested oneOf patterns that attempt to handle type interpretations but don't properly separate:
- Array-level wrapping
- Item-level wrapping
- Terminal type definitions

### Correction Strategy

1. Define clean terminal definitions: `NodeType`, `EdgeType`
2. Define item wrappers: `NodeTypeItem`, `EdgeTypeItem`
3. Define array structures: `NodeTypesArray`, `EdgeTypesArray`
4. Define property-level wrappers: `NodeTypesProperty`, `EdgeTypesProperty`
5. Replace complex nested oneOf with clear layered structure

### YAML Example Corrections

For snb-place-hierarchy.yaml, change from:

```yaml
subtypesOf:
  abstract:
    nodeTypes:
    - nodeType: Place
    - nodeType: City
```

To:

```yaml
abstract:
  nodeTypes:
    - abstract:
        nodeType: Place
    - final:
        nodeType: City
    - final:
        nodeType: Country
    - final:
        nodeType: Continent
```

Or alternatively (if Place should be the supertype for a subtypesOf relationship):

```yaml
subtypesOf:
  nodeTypes:
    - abstract:
        nodeType: Place
    - final:
        nodeType: City
    - final:
        nodeType: Country
    - final:
        nodeType: Continent
```

## Design Decisions

### Decision 1: Separate Item and Array Definitions

**Rationale**: Separating `NodeTypeItem` from `NodeTypesArray` makes the schema clearer and prevents accidental recursion.

### Decision 2: Allow Interpretations at Multiple Levels

**Rationale**: Provides maximum flexibility for schema designers while maintaining clear structure.

### Decision 3: No Nested Interpretations

**Rationale**: Prevents complexity and ambiguity. An interpretation wrapper contains plain arrays of items, not more wrappers.

### Decision 4: Import Can Appear at Any Level

**Rationale**: Allows maximum reusability - can import entire arrays, individual types, or wrapped structures.
