# Type Interpretation System Design

## Overview

The LEX-2026 type interpretation system provides a compositional framework for defining how types are matched and instantiated in graph schemas. Type interpretations wrap type definitions to control their behavior in schema validation and graph instantiation.

## Core Concepts

### Type Interpretation = Matching Mode + Concreteness

Every type interpretation consists of two orthogonal dimensions:

1. **Matching Mode**: How the type matches against graph elements
2. **Concreteness**: Whether the type can be directly instantiated

## Matching Modes

There are two matching modes:

### 1. `exactlyOf` (default)
- Matches only elements of exactly this type
- No subtype matching allowed
- Used when precise type matching is required

### 2. `subtypesOf`
- Matches elements of this type OR any of its subtypes
- Enables polymorphic matching
- Used when subtype flexibility is needed

## Concreteness

There are two concreteness levels:

### 1. `concrete` (default)
- Type can be directly instantiated
- Elements can have exactly this type
- Normal, instantiable types

### 2. `abstract`
- Type cannot be directly instantiated
- Only subtypes can be instantiated
- Used for defining common supertype structure

## Valid Combinations

### 1. `exactlyOf` + `concrete` (double default)
```yaml
nodeTypes:
  - nodeType:
      typeLabel: Person
      implies: {...}
```
- Default when no interpretation specified
- Exact type matching, instantiable
- Most common case

### 2. `subtypesOf` + `concrete`
```yaml
nodeTypes:
  - subtypesOf:
      nodeTypes:
        - nodeType:
            typeLabel: Person
            implies: {...}
```
- Allows subtypes, supertype is instantiable
- Polymorphic matching with concrete supertype

### 3. `subtypesOf` + `abstract`
```yaml
nodeTypes:
  - subtypesOf:
      abstract:
        nodeTypes:
          - nodeType:
              typeLabel: Message
              implies: {...}
```
- Allows subtypes, supertype is NOT instantiable
- Pure abstract supertype pattern

## Invalid Combination

### `exactlyOf` + `abstract`
This combination is logically invalid:
- Cannot instantiate abstract types exactly
- Would create an impossible constraint
- Schema validation should reject this

## Shorthands

### `abstract:` 
Shorthand for `subtypesOf: { abstract: {...} }`

```yaml
# These are equivalent:
nodeTypes:
  - abstract:
      nodeTypes:
        - nodeType: {...}

nodeTypes:
  - subtypesOf:
      abstract:
        nodeTypes:
          - nodeType: {...}
```

### `properSubtypesOf:`
Shorthand for `subtypesOf: { abstract: {...} }`

```yaml
# These are equivalent:
nodeTypes:
  - properSubtypesOf:
      nodeTypes:
        - nodeType: {...}

nodeTypes:
  - subtypesOf:
      abstract:
        nodeTypes:
          - nodeType: {...}
```

## Additional Modifiers

### `sealed:`
- Defines a closed hierarchy of types
- No additional subtypes can be added outside this definition
- Enables exhaustive pattern matching

```yaml
nodeTypes:
  - sealed:
      nodeTypes:
        - nodeType:
            typeLabel: Red
        - nodeType:
            typeLabel: Green
        - nodeType:
            typeLabel: Blue
```

### `final:`
- Type cannot be subtyped
- Prevents further extension
- Leaf type in hierarchy

```yaml
nodeTypes:
  - final:
      nodeType:
        typeLabel: String
        implies: {...}
```

## Compositional Structure

Type interpretations can wrap:
- Single types (set size = 1)
- Multiple types (set size > 1)
- Type sequences (`nodeTypes:`, `edgeTypes:`, `graphType:`)

### General Pattern
```yaml
<matching-mode>:           # exactlyOf (default) or subtypesOf
  <concreteness>:          # concrete (default) or abstract
    <type-sequence>:       # nodeTypes, edgeTypes, etc.
      - <type-definition>
```

### Nesting
Interpretations can be nested up to two levels deep:
```yaml
subtypesOf:
  abstract:
    nodeTypes:
      - nodeType: {...}
```

When placed around sets, interpretations apply to the set as a whole and cannot be contradicted by contained elements.

## Examples

### Simple Concrete Type (defaults)
```yaml
nodeTypes:
  - nodeType:
      typeLabel: Person
      implies:
        propertyTypes:
          - name: id
            valueType: INTEGER
```

### Abstract Supertype with Concrete Subtypes
```yaml
nodeTypes:
  - abstract:
      nodeTypes:
        - nodeType:
            typeLabel: Message
            implies:
              labels: [Message]
              propertyTypes: [...]
        - nodeType:
            typeLabel: Post
            extends:
              supertypes: [Message]
              adding:
                labels: [Post]
        - nodeType:
            typeLabel: Comment
            extends:
              supertypes: [Message]
              adding:
                labels: [Comment]
```

### Sealed Hierarchy
```yaml
nodeTypes:
  - sealed:
      nodeTypes:
        - abstract:
            nodeTypes:
              - nodeType:
                  typeLabel: Shape
              - nodeType:
                  typeLabel: Circle
                  extends: {supertypes: [Shape]}
              - nodeType:
                  typeLabel: Square
                  extends: {supertypes: [Shape]}
```

### Final Type
```yaml
nodeTypes:
  - final:
      nodeType:
        typeLabel: UUID
        implies:
          propertyTypes:
            - name: value
              valueType: STRING
```

## Terminology Evolution

### Old Names → New Names
- `allowSubtypesOf` → `subtypesOf`
- `allowsProperSubtypesOf` → `properSubtypesOf`
- `exactlyOfThisType` → `exactlyOf`
- `abstractSupertype` → `abstract`

The new names are more concise and align with common programming language terminology.

## Implementation Notes

### Defaults
- When no matching mode is specified: `exactlyOf`
- When no concreteness is specified: `concrete`
- Therefore, bare type definitions are `exactlyOf` + `concrete`

### Validation Rules
1. Schema validator must reject `exactlyOf` + `abstract` combinations
2. `properSubtypesOf` must expand to `subtypesOf` + `abstract`
3. `abstract:` shorthand must expand to `subtypesOf` + `abstract`
4. Nested interpretations limited to 2 levels deep

### Type Sequences
Type interpretations can wrap:
- `nodeTypes:` - array of node type definitions
- `edgeTypes:` - array of edge type definitions
- `graphType:` - single graph type definition
- Individual items: `- nodeType:`, `- edgeType:`

## Benefits

1. **Compositionality**: Interpretations can be nested and combined
2. **Clarity**: Explicit matching and instantiation semantics
3. **Flexibility**: Supports various type system patterns
4. **Safety**: Invalid combinations are rejected
5. **Conciseness**: Shorthands for common patterns
6. **Extensibility**: New modifiers can be added (sealed, final, etc.)

## Related Concepts

- **Subtyping**: Hierarchical type relationships
- **Polymorphism**: Ability to match multiple types
- **Abstract Types**: Non-instantiable supertypes
- **Sealed Hierarchies**: Closed type families
- **Final Types**: Non-extensible types
