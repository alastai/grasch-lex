# Type Interpretation (TI) Semantics - Complete Specification

## Purpose

This document consolidates ALL clarifications about Type Interpretation (TI) semantics, valid combinations, wrappable locations, and import behavior. This serves as the authoritative reference before updating the import-schema-consistency spec documents.

## 1. TI Wrapper Fundamentals

### 1.1 TI as Atomic Unit of Import
- **Type Interpretations are the unit of import** - you import at the TI level, not at individual type level
- **TIs wrap sets of types** (partition blocks), not individual types
- **Indentation delimits type sets** - types at the same indentation level under a TI belong to the same set
- **Single-element TIs are supported** - A TI can wrap a single type OR multiple types
- **YAML syntax distinction**: Natural YAML for a single element is `nodeType: {...}` (not in array), but array syntax `[nodeType: {...}]` is also valid
- **Schema must support both**: Use `anyOf` pattern to accept both single element and array representations
- **You cannot cherry-pick** individual types from within a partition block - you import the whole set

### 1.2 TI Scope and Extent
- **TI scope extends to contained types**: A TI wrapper applies to all node types and/or edge types within its indentation boundary
- **Default TI at graphType level**: `exactlyOf:concrete:` (implicit, can be overridden)
- **TI Override Rule**: At any level from `nodeTypes`/`edgeTypes` downwards, a different TI can override the one from above
  - Example: If `nodeTypes` is `concrete:`, a contained `-nodeType` can be `abstract:`
  - Example: If `edgeTypes` is `abstract:`, a contained `-edgeType` can be `final:`
- **Edge endpoint overrides**: Edge type endpoints (from/to) can have their own TI wrappers that override the edge type's TI
  - Syntax for endpoint TI placement is unaffected by the general override rule
  - Endpoints follow the same override principle

## 2. Valid TI Combinations

### 2.1 Two-Level TI Structure

TI wrappers have two levels:
1. **Interpretation Level**: `exactlyOf`, `subtypesOf`, `properSubtypesOf`
2. **Concreteness Level**: `abstract`, `concrete`, `final`, `sealed`, `extensible`

### 2.2 Valid Combinations

| Interpretation | Concreteness | Valid? | Semantics |
|----------------|--------------|--------|-----------|
| `exactlyOf` | `concrete` | ✅ | Exact match required, can be instantiated |
| `exactlyOf` | `abstract` | ✅ | Exact match required, cannot be instantiated |
| `exactlyOf` | `final` | ✅ | Exact match, cannot be extended |
| `exactlyOf` | `sealed` | ✅ | Exact match, closed hierarchy |
| `subtypesOf` | `concrete` | ✅ | Allows subtypes, can be instantiated |
| `subtypesOf` | `abstract` | ✅ | Allows subtypes, cannot be instantiated |
| `subtypesOf` | `final` | ✅ | Allows subtypes, but this type cannot be extended |
| `subtypesOf` | `sealed` | ✅ | Allows subtypes within sealed hierarchy |
| `properSubtypesOf` | `concrete` | ✅ | Proper subtypes only, can be instantiated |
| `properSubtypesOf` | `abstract` | ✅ | Proper subtypes only, cannot be instantiated |

**Note**: `extensible` is the default and typically omitted.

### 2.3 Shorthands

| Shorthand | Expands To | Semantics |
|-----------|------------|-----------|
| `abstract:` | `subtypesOf: abstract:` | Allows subtypes, cannot be instantiated |
| `concrete:` | `exactlyOf: concrete:` | Exact match, can be instantiated |
| `final:` | `exactlyOf: final:` | Cannot be extended |
| `properSubtypesOf:` | `subtypesOf: abstract:` | Proper subtypes only (implies abstract) |

## 3. Sealed Semantics (CRITICAL CORRECTION)

### 3.1 Core Sealed Behavior

**It is NOT possible to seal a set of abstract types.**

**Sealing makes all non-abstract types final.**

### 3.2 Sealed with Mixed Abstract/Concrete

```yaml
# This pattern:
sealed:
  abstract:
    nodeType: {typeLabel: A}
  concrete:
    nodeType: {typeLabel: B, extends: A}

# Is equivalent to:
abstract:
  nodeType: {typeLabel: A}
final:
  nodeType: {typeLabel: B, extends: A}
# PLUS the semantic: "no other subtypes of A can be defined"
```

### 3.3 Sealed Semantics Summary

1. **Sealing makes non-abstract types final**: All concrete types in a sealed block become final
2. **Hierarchy closure**: No additional subtypes can be defined outside the sealed block
3. **Abstract types remain abstract**: Sealing doesn't change the abstractness of abstract types
4. **Semantic enforcement**: The "no other subtypes" rule requires application-level validation

### 3.4 Examples

**Valid Sealed Pattern:**
```yaml
sealed:
  nodeTypes:
    - subtypesOf:
        abstract:
          nodeType: {typeLabel: Place}
    - nodeType: {typeLabel: City, extends: Place}
    - nodeType: {typeLabel: Country, extends: Place}

# Semantics:
# - Place is abstract (can have subtypes)
# - City is final (cannot be extended) - made final by sealed
# - Country is final (cannot be extended) - made final by sealed
# - No other subtypes of Place can be defined
```

**Invalid Pattern (Cannot Seal Only Abstract Types):**
```yaml
# ❌ INVALID - Cannot seal a set containing only abstract types
sealed:
  abstract:
    nodeTypes:
      - nodeType: {typeLabel: A}
      - nodeType: {typeLabel: B}
```

## 4. TI Override Hierarchy

### 4.1 Default TI at GraphType Level

**Implicit Default**: `exactlyOf:concrete:`

All types at the `graphType` level are implicitly `exactlyOf:concrete:` unless explicitly overridden.

### 4.2 Override Rules

**General Rule**: At any level from `nodeTypes`/`edgeTypes` downwards, a different TI can override the one from above.

**Override Hierarchy**:
```
graphType (default: exactlyOf:concrete:)
  ↓ can be overridden by
nodeTypes/edgeTypes level TI
  ↓ can be overridden by
individual -nodeType/-edgeType TI
  ↓ can be overridden by (for edge types only)
endpoint (from/to) TI
```

### 4.3 Override Examples

**Example 1: Override at nodeTypes level**
```yaml
graphType:
  nodeTypes:  # Inherits exactlyOf:concrete: from graphType
    - nodeType: {typeLabel: Person}  # exactlyOf:concrete: (inherited)
    - abstract:  # Override to abstract
        nodeType: {typeLabel: Vehicle}
```

**Example 2: Override at individual type level**
```yaml
graphType:
  concrete:  # Explicit concrete at nodeTypes level
    nodeTypes:
      - nodeType: {typeLabel: Person}  # concrete (inherited)
      - abstract:  # Override to abstract
          nodeType: {typeLabel: Vehicle}
```

**Example 3: Edge endpoint override**
```yaml
graphType:
  edgeTypes:
    - abstract:  # Edge type is abstract
        edgeType:
          from:
            concrete:  # Override: endpoint is concrete
              nodeType: {typeLabel: Person}
          to:
            abstract:  # Override: endpoint is abstract
              nodeType: {typeLabel: Company}
```

### 4.4 Override Semantics

- **Overrides are local**: They only affect the specific type or subtree
- **No upward propagation**: Overriding a child doesn't change the parent's TI
- **Explicit wins**: An explicit TI always overrides an inherited one
- **Endpoint independence**: Edge endpoint TIs are independent of each other and the edge type's TI

## 5. TI-Wrappable Locations

### 4.1 Location Categories

Based on TI-LOCATION-AUDIT.md, there are 47 TI-wrappable locations across 7 categories:

#### Category 1: Top-Level xTypes Properties (2 locations)
- `GraphType.nodeTypes`
- `GraphType.edgeTypes`

#### Category 2: GraphType Pattern Properties (12 locations)
- `GraphType.abstract.nodeTypes`
- `GraphType.abstract.edgeTypes`
- `GraphType.exactlyOf.concrete.nodeTypes`
- `GraphType.exactlyOf.abstract.nodeTypes`
- `GraphType.subtypesOf.concrete.nodeTypes`
- `GraphType.subtypesOf.abstract.nodeTypes`
- (Same 6 patterns for edgeTypes)

#### Category 3: GraphType.subtypesOf Nested Properties (4 locations)
- `GraphType.subtypesOf.abstract.nodeTypes`
- `GraphType.subtypesOf.abstract.edgeTypes`
- `GraphType.subtypesOf.nodeTypes`
- `GraphType.subtypesOf.edgeTypes`

#### Category 4: NodeTypeItem TI Wrappers (5 locations)
- `NodeTypeItem.exactlyOf.concrete`
- `NodeTypeItem.exactlyOf.abstract`
- `NodeTypeItem.subtypesOf.concrete`
- `NodeTypeItem.subtypesOf.abstract`
- `NodeTypeItem.sealed.nodeTypes`

#### Category 5: EdgeTypeItem TI Wrappers (5 locations)
- (Same 5 patterns as NodeTypeItem)

#### Category 6: NodeTypesProperty TI Wrappers (9 locations)
- `NodeTypesProperty.abstract`
- `NodeTypesProperty.concrete`
- `NodeTypesProperty.properSubtypesOf`
- `NodeTypesProperty.exactlyOf.concrete`
- `NodeTypesProperty.exactlyOf.abstract`
- `NodeTypesProperty.subtypesOf.concrete`
- `NodeTypesProperty.subtypesOf.abstract`
- `NodeTypesProperty.final`
- `NodeTypesProperty.sealed`

#### Category 7: EdgeTypesProperty TI Wrappers (9 locations)
- (Same 9 patterns as NodeTypesProperty)

### 5.2 Edge Endpoint TI Placement

Edge type endpoints (from/to) can have their own TI wrappers that override the edge type's TI:

```yaml
edgeTypes:
  - exactlyOf:
      concrete:
        - edgeType:
            from:
              subtypesOf:  # Endpoint-specific TI override
                abstract:
                  - nodeType: {typeLabel: Person}
            to:
              exactlyOf:  # Another endpoint-specific TI override
                concrete:
                  - nodeType: {typeLabel: Company}
```

**Note**: Endpoint TI overrides follow the general override rule but have specific syntax for placement within the edge type structure.

## 5. Two-Phase Import Mechanism

### 5.1 Phase 1: Import Entire TI Wrapper + Content

**Location**: At partition block level (array items)

**Behavior**: Preserves the TI wrapper and its interpretation

**Example**:
```yaml
nodeTypes:
  - import: "person-types.yaml"  # Imports TI wrapper + types

# person-types.yaml contains:
subtypesOf:
  abstract:
    - nodeType: {typeLabel: Person}
    - nodeType: {typeLabel: Employee, extends: Person}

# Result after import:
nodeTypes:
  - subtypesOf:
      abstract:
        - nodeType: {typeLabel: Person}
        - nodeType: {typeLabel: Employee, extends: Person}
```

### 5.2 Phase 2: Import Content Only, Strip TI

**Location**: At TI wrapper content level

**Behavior**: Strips the TI wrapper from imported content, allows outer TI to reinterpret

**Example**:
```yaml
nodeTypes:
  - exactlyOf:
      concrete:
        import: "person-types.yaml"  # Imports types only, strips TI

# person-types.yaml contains:
subtypesOf:
  abstract:
    - nodeType: {typeLabel: Person}
    - nodeType: {typeLabel: Employee, extends: Person}

# Result after import (TI override):
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person}
        - nodeType: {typeLabel: Employee, extends: Person}
```

**Key Insight**: Phase 2 enables **TI override** - you can import type definitions and reinterpret them with a different TI.

## 6. Singleton vs Array Distinction in YAML

### 6.1 Singleton Set (Cardinality 1)

**YAML Representation**: Single type (not in array)

```yaml
nodeTypes:
  - exactlyOf:
      concrete:
        nodeType: {typeLabel: Person}  # Singleton - no array brackets
```

### 6.2 Multi-Element Set (Cardinality > 1)

**YAML Representation**: Array of types

```yaml
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person}  # Array with multiple elements
        - nodeType: {typeLabel: Company}
```

### 6.3 Array with One Member vs Singleton

These are DIFFERENT in YAML:

```yaml
# Singleton set (preferred for single type)
concrete:
  nodeType: {typeLabel: Person}

# Array with one member (valid but verbose)
concrete:
  - nodeType: {typeLabel: Person}
```

**Schema Requirement**: Must use `anyOf` pattern to accept both:
```json
{
  "anyOf": [
    {
      "description": "Singleton set",
      "$ref": "#/$defs/NodeType"
    },
    {
      "description": "Multi-element set",
      "type": "array",
      "items": { "$ref": "#/$defs/NodeType" }
    }
  ]
}
```

## 7. Canonicalization Behavior

### 7.1 Two-Level Consolidation

**Level 1: Collection Consolidation (Union of All Instances)**
- **All `nodeTypes` instances** throughout the document → **ONE `nodeTypes` collection**
- **All `edgeTypes` instances** throughout the document → **ONE `edgeTypes` collection**
- This is a **union operation** - all node types from all locations are gathered together
- All edge types from all locations are gathered together

**Level 2: TI Amalgamation (Grouping by Interpretation)**
- Within the single consolidated collection, **all types with the same TI** → **ONE partition block**
- Multiple `exactlyOf:concrete` blocks → merged into one `exactlyOf:concrete` block
- Multiple `subtypesOf:abstract` blocks → merged into one `subtypesOf:abstract` block
- Result: Single `nodeTypes` array containing TI-partitioned subsets
- Result: Single `edgeTypes` array containing TI-partitioned subsets

### 7.2 Detailed Consolidation Process

**Step 1: Gather all nodeTypes/edgeTypes**
- Find every `nodeTypes` property in the document
- Find every `edgeTypes` property in the document
- Union all the types together

**Step 2: Group by TI**
- All `nodeType` instances with `exactlyOf:concrete` → one group
- All `nodeType` instances with `subtypesOf:abstract` → one group
- All `nodeType` instances with `final:` → one group
- (Same for edgeType instances)

**Step 3: Create consolidated structure**
- One `nodeTypes` array with one partition block per unique TI
- One `edgeTypes` array with one partition block per unique TI

### 7.3 Example Transformation

```yaml
# PC Form (multiple nodeTypes instances, scattered TIs)
graphType:
  nodeTypes:
    abstract: [type_a]
  concrete: [type_b]
  abstract:
    nodeTypes: [type_c]
  subtypesOf:
    abstract:
      nodeTypes: [type_d]

# C Form (consolidated and amalgamated)
graphType:
  nodeTypes:
    - abstract: [type_a, type_c, type_d]  # All abstract types amalgamated
    - concrete: [type_b]                   # All concrete types amalgamated
```

### 7.4 Key Consolidation Behaviors

1. **Union, not replacement**: All instances are combined, not overwritten
2. **TI-based grouping**: Types are grouped by their interpretation
3. **Single collection**: Result is always one `nodeTypes` and one `edgeTypes`
4. **Partition blocks**: Each unique TI becomes one partition block in the array
5. **Order preservation**: Within each partition block, order may be preserved or normalized

## 8. Schema Structure Alignment

### 8.1 GraphType Structure

```
GraphType
├── properties
│   ├── nodeTypes (NodeTypesProperty)
│   ├── edgeTypes (EdgeTypesProperty)
│   └── subtypesOf
│       ├── abstract
│       │   ├── nodeTypes
│       │   └── edgeTypes
│       ├── nodeTypes
│       └── edgeTypes
└── patternProperties
    ├── ^(abstract|sealed|final|concrete)$
    │   ├── nodeTypes (NodeTypesArray)
    │   └── edgeTypes (EdgeTypesArray)
    └── ^(exactlyOf|subtypesOf)$
        └── oneOf
            ├── patternProperties
            │   └── ^(abstract|concrete)$
            │       ├── nodeTypes (NodeTypesArray)
            │       └── edgeTypes (EdgeTypesArray)
            └── import option
```

### 8.2 Array Item Structure

```
NodeTypesArray
└── items (NodeTypeItem)
    └── oneOf
        ├── NodeType (bare type)
        ├── TI-wrapped partition block
        │   └── patternProperties
        │       └── ^(exactlyOf|subtypesOf|properSubtypesOf)$
        │           └── patternProperties
        │               └── ^(abstract|concrete|final|sealed)$
        │                   └── TIWrapperContent
        └── import option (Phase 1)
```

## 9. Required Schema Patterns

### 9.1 TI Wrapper Content Pattern

**Purpose**: Content within TI wrappers (the actual type sets)

**Supports**:
- Singleton sets (single type)
- Multi-element sets (array of types)
- Phase 2 imports (import content only, strip TI)

```json
"TIWrapperContentNode": {
  "oneOf": [
    {
      "description": "Inline type set",
      "anyOf": [
        {
          "description": "Singleton set",
          "$ref": "#/$defs/NodeType"
        },
        {
          "description": "Multi-element set",
          "type": "array",
          "items": { "$ref": "#/$defs/NodeType" }
        }
      ]
    },
    {
      "description": "Phase 2: Import type definitions only",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": { "type": "string" }
      },
      "additionalProperties": false
    }
  ]
}
```

### 9.2 Partition Block Item Pattern

**Purpose**: Items in nodeTypes/edgeTypes arrays

**Supports**:
- Bare types (singleton with implicit TI)
- TI-wrapped partition blocks
- Phase 1 imports (import entire TI wrapper + content)

```json
"PartitionBlockItemNode": {
  "oneOf": [
    {
      "description": "Bare node type",
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
              }
            },
            {
              "description": "Phase 1: Import entire TI wrapper",
              "type": "object",
              "required": ["import"],
              "properties": {
                "import": { "type": "string" }
              },
              "additionalProperties": false
            }
          ]
        }
      }
    },
    {
      "description": "Phase 1: Import partition block",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": { "type": "string" }
      },
      "additionalProperties": false
    }
  ]
}
```

## 10. Summary Checklist

Before proceeding with spec updates, verify:

- [ ] Sealed semantics correctly documented (makes non-abstract types final)
- [ ] All 47 TI-wrappable locations identified
- [ ] Valid TI combinations table complete
- [ ] Two-phase import mechanism clearly explained
- [ ] Singleton vs array distinction documented
- [ ] Edge endpoint exception noted
- [ ] Canonicalization behavior specified
- [ ] Schema structure alignment verified
- [ ] Required schema patterns defined

## Next Steps

1. Update `.kiro/specs/import-schema-consistency/requirements.md` with sealed semantics
2. Update `.kiro/specs/import-schema-consistency/design.md` with complete TI semantics
3. Add examples showing sealed behavior
4. Proceed with Task 2 implementation using correct patterns
