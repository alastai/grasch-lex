# Type Definition Canonicalization Rules

## Core Principle

**Type interpretation wrappers surround type definitions, NOT type definition structures.**

A type definition can be:
1. **By reference**: `Person`, `[Person, Employee]`, or `0` (type label, labels set, or index)
2. **Inline**: `nodeType: typeLabel: Person` (full node type specification)

## Type Definition Locations

### In `nodeTypes` Block
**Always inline** - full node type specification:
```yaml
nodeTypes:
  - nodeType:
      typeLabel: Person
      implies:
        propertyTypes: [...]
```

### In Edge Type Endpoints
**By reference OR inline**:

**By Reference** (most common):
```yaml
edgeType:
  directed:
    from: Person              # Reference to nodeType defined in nodeTypes block
    via: KNOWS
    to: Person
```

**Inline** (edge-only node type):
```yaml
edgeType:
  directed:
    from:
      nodeType:
        typeLabel: TempNode   # Inline definition - only exists as endpoint
        implies:
          propertyTypes: [...]
    via: CONNECTS
    to: Company
```

## Node Type Scoping Rules

1. **nodeTypes block**: Defines node types that can exist independently
2. **Inline in edgeType**: Defines node types that ONLY exist as endpoints of that edge type
3. **Cross-reference**: An edgeType can reference a nodeType defined inline in another edgeType
4. **No duplication**: An inline nodeType cannot repeat one defined in nodeTypes block

## Node Type Categories

1. **Freestanding**: Defined in nodeTypes block, can exist without edges
2. **Edge-only**: Defined inline in edgeType, only exists as endpoint
3. **Isolated**: Defined in nodeTypes but never referenced by any edge (valid but unusual)

## Canonicalization Rules

### Rule 1: Wrappers Surround Definitions

**WRONG PC** (invalid - wrapper on structure):
```yaml
from:
  typeLabel: Person           # ❌ This is NOT a type definition
```

**CORRECT PC** (by reference):
```yaml
from: Person                  # ✅ Type definition by reference
```

**CORRECT PC** (inline):
```yaml
from:
  nodeType:                   # ✅ Type definition inline
    typeLabel: Person
    implies: {...}
```

### Rule 2: PC → C Adds Default Wrappers

**By Reference**:
```yaml
# PC form
from: Person

# C form (add default wrapper)
from:
  exactlyOf:
    concrete: Person
```

**Inline**:
```yaml
# PC form
from:
  nodeType:
    typeLabel: Person
    implies: {...}

# C form (add default wrapper around entire definition)
from:
  exactlyOf:
    concrete:
      nodeType:
        typeLabel: Person
        implies: {...}
```

### Rule 3: Explicit Wrappers Preserved

**By Reference with Wrapper**:
```yaml
# PC form
from:
  subtypesOf:
    abstract: Person

# C form (already canonical)
from:
  subtypesOf:
    abstract: Person
```

**Inline with Wrapper**:
```yaml
# PC form
from:
  subtypesOf:
    abstract:
      nodeType:
        typeLabel: Message
        implies: {...}

# C form (already canonical)
from:
  subtypesOf:
    abstract:
      nodeType:
        typeLabel: Message
        implies: {...}
```

## Complete Examples

### Example 1: Simple Edge (By Reference)

**PC Form**:
```yaml
edgeType:
  directed:
    from: Person
    via: KNOWS
    to: Person
  implies:
    propertyTypes:
      - name: since
        valueType: DATE
```

**C Form**:
```yaml
edgeType:
  directed:
    from:
      exactlyOf:
        concrete: Person
    via:
      exactlyOf:
        concrete: KNOWS
    to:
      exactlyOf:
        concrete: Person
  implies:
    propertyTypes:
      - name: since
        valueType: DATE
```

### Example 2: Edge with Inline Node Type

**PC Form**:
```yaml
edgeType:
  directed:
    from: Person
    via: CONNECTS_TO
    to:
      nodeType:
        typeLabel: Endpoint
        implies:
          propertyTypes:
            - name: id
              valueType: INTEGER
```

**C Form**:
```yaml
edgeType:
  directed:
    from:
      exactlyOf:
        concrete: Person
    via:
      exactlyOf:
        concrete: CONNECTS_TO
    to:
      exactlyOf:
        concrete:
          nodeType:
            typeLabel: Endpoint
            implies:
              propertyTypes:
                - name: id
                  valueType: INTEGER
```

### Example 3: Abstract Type with Subtypes

**PC Form**:
```yaml
nodeTypes:
  - abstract:
      nodeType:
        typeLabel: Message
        implies:
          propertyTypes:
            - name: id
              valueType: INTEGER
  - nodeType:
      typeLabel: Post
      extends: Message
```

**C Form**:
```yaml
nodeTypes:
  - subtypesOf:
      abstract:
        nodeType:
          typeLabel: Message
          implies:
            propertyTypes:
              - name: id
                valueType: INTEGER
  - exactlyOf:
      concrete:
        nodeType:
          typeLabel: Post
          extends: Message
```

## Validation Implications

The JSON Schema must accept:

1. **Both PC and C forms** for type definitions
2. **By-reference** type definitions: `Person`, `[X, Y]`, `0`
3. **Inline** type definitions: `nodeType: {...}`
4. **Wrapped** type definitions: `exactlyOf: concrete: Person`
5. **Wrapped inline**: `exactlyOf: concrete: nodeType: {...}`

## Common Mistakes

❌ **WRONG**: Wrapper on structure key
```yaml
from:
  typeLabel: Person           # typeLabel: is NOT a type definition
```

❌ **WRONG**: Changing inline to reference during canonicalization
```yaml
# PC
from:
  nodeType:
    typeLabel: Person

# WRONG C (lost inline definition)
from:
  exactlyOf:
    concrete: Person
```

✅ **CORRECT**: Wrapper surrounds entire definition
```yaml
# PC
from:
  nodeType:
    typeLabel: Person

# CORRECT C (preserves inline definition)
from:
  exactlyOf:
    concrete:
      nodeType:
        typeLabel: Person
```

## Summary

- **Type definitions** = references (`Person`) OR inline (`nodeType: {...}`)
- **Wrappers** = surround the definition, not the structure
- **Canonicalization** = adds default wrappers, preserves definition form
- **Schema** = must validate both PC and C forms
- **Node types** = can be freestanding, edge-only, or isolated

---

**Status**: Correct understanding documented
**Key Insight**: Wrappers wrap definitions, definitions can be references or inline
