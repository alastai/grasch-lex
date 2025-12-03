# Import Schema Consistency Design

## Overview

This document designs the schema changes needed to support Type Interpretation (TI) based imports, where TIs wrap **sets of types** (partition blocks) and imports happen at the TI level. The key insight is that **indentation delimits type sets** under type interpretations, and singleton sets (single types) are special cases of partition blocks with cardinality 1.

## Architectural Principles

### 0. Three-Level TI Architecture

Type Interpretations operate at three distinct conceptual levels:

**Level 1: TI Locations** - Where TI can be applied:
- graphTypeInterpretation, nodeTypesInterpretation, edgeTypesInterpretation
- nodeTypeArrayInterpretation, edgeTypeArrayInterpretation
- nodeTypeInterpretation, edgeTypeInterpretation
- edgeTypeEndpointNodeTypeInterpretation

**Level 2: TI Structure** - How TI is expressed:
- 2-level explicit: `subtypeOf: abstract:` or `exactlyOf: final:`
- 1-level shorthand: `concrete:` or `abstract:`
- 0-level bare: No wrapper (implicit default)

**Level 3: Type Definition** - The actual type specification with labels, properties, etc.

**Key Principles:**
- **TI Override**: Outer TI immediately wrapping inner TI overrides the inner
- **TI Default Cascade**: TI at higher level establishes default that can be overridden at lower levels
- **Facet Independence**: Subtype interpretation facet (`subtypeOf`, `properSubtypesOf`, `exactlyOf`) is a toggle, NOT part of TI location name
- **Exception**: Edge type endpoints can have their own TI wrappers

### 1. TI as Unit of Import
- **Type Interpretations are the unit of import** - you import at the TI level, not at individual type level
- **TIs wrap sets of types** (partition blocks), not individual types
- **Imports happen at the TI level**, importing entire partition blocks with their TI wrapper
- **A TI extends down to its contained types** - the TI wrapper encompasses all node types and/or edge types within it
- **Singleton sets are special cases** of partition blocks (cardinality 1)
- **Indentation delimits type sets** under type interpretations
- **Exception**: Edge type endpoints can override TI at the endpoint level (special case for endpoint-specific type interpretations)

### 2. Partition Flexibility
- Support **any valid partitioning** of types into TI-wrapped blocks
- Enable **coarse partitions** (one TI wraps many types)
- Enable **fine partitions** (each type gets its own TI)
- Enable **mixed partitions** (some TIs wrap multiple types, others wrap singletons)

### 3. Indentation as Set Delimiter
- **Indentation structure defines set membership**
- Types at the same indentation level under a TI belong to the same set
- The TI wrapper keyword (exactlyOf, subtypesOf, etc.) establishes the set boundary
- The concreteness/abstractness keyword (concrete, abstract, sealed, final) further delimits the set

### 4. TI Scope and Extent
- **TI scope extends to contained types**: A TI wrapper applies to all node types and/or edge types within its indentation boundary
- **Two-phase import capability**: Imports can happen at two levels:
  1. **Import entire TI wrapper + enclosed types** (import the partition block as a unit, preserving the TI)
  2. **Import enclosed types only** (import type definitions, strip/merge duplicate TI, allow outer TI to reinterpret)
- **TI override through import**: An imported type definition can be reinterpreted by wrapping it in a different TI
- **Edge endpoint exception**: Edge type endpoints can have their own TI wrappers that override the edge type's TI at the endpoint level
- **No partial imports**: You cannot cherry-pick individual types from within a partition block - you import the whole set

### 5. Canonicalization Consolidation

**Critical Behavior**: Canonicalization performs two levels of consolidation:

**Level 1: Collection Consolidation**
- **All `nodeTypes` instances** → consolidated into **ONE `nodeTypes` collection**
- **All `edgeTypes` instances** → consolidated into **ONE `edgeTypes` collection**
- PC forms can have multiple scattered `nodeTypes`/`edgeTypes` instances
- C forms have exactly one `nodeTypes` and one `edgeTypes` collection

**Level 2: TI Amalgamation**
- Within the single collection, **types with the same TI** → amalgamated into **one partition block**
- Multiple `exactlyOf:concrete` partition blocks → merged into one
- Multiple `subtypesOf:abstract` partition blocks → merged into one
- Result: Single collection with TI-partitioned subsets

**Example Transformation:**
```yaml
# PC: Multiple nodeTypes instances, scattered TIs
graphType:
  nodeTypes:
    abstract: [type_a]
  concrete: [type_b]
  abstract:
    nodeTypes: [type_c]

# C: One nodeTypes, amalgamated TIs
graphType:
  nodeTypes:
    - abstract: [type_a, type_c]  # Amalgamated
    - concrete: [type_b]
```

### 6. Two-Phase Import Mechanism

Imports can occur at two distinct levels, enabling flexible TI management:

**Phase 1: Import Entire TI Wrapper + Content**
```yaml
nodeTypes:
  - import: "person-types.yaml"  # Imports TI wrapper + {Person, Employee, Manager}
```
The imported file contains the TI wrapper and its types - everything is preserved as-is.

**Phase 2: Import Content Only, Strip/Merge TI**
```yaml
nodeTypes:
  - exactlyOf:
      concrete:
        import: "person-types.yaml"  # Imports {Person, Employee, Manager}, strips their TI
```
The imported file contains types with their own TI, but that TI is stripped/merged, and the outer `exactlyOf:concrete` reinterprets them.

**Key Insight**: This allows **TI override** - you can import type definitions and reinterpret them with a different TI than they were originally defined with.

### 7. Schema Consistency
- **Uniform oneOf patterns** at all TI-wrappable locations
- **Consistent import option structure** across all contexts
- **Predictable validation behavior** regardless of partition granularity
- **Two-phase import support** at all TI-wrappable locations
- **Canonicalization support** for both collection consolidation and TI amalgamation

## Design Patterns

### Pattern 1: TI-Wrappable Content OneOf

Every location where TI wrappers can contain importable content:

```json
{
  "oneOf": [
    {
      "description": "Inline TI-wrapped content (set of types delimited by indentation)",
      "$ref": "#/$defs/TIWrapperWithContent"
    },
    {
      "description": "Import TI-wrapped content (import entire partition block)",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import partition block with TI wrapper"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

### Pattern 2: Partition Block Array

Arrays of TI-wrapped partition blocks (nodeTypes, edgeTypes):

```json
{
  "type": "array",
  "description": "Array of TI-wrapped partition blocks (each TI wraps a set of types)",
  "items": {
    "oneOf": [
      {
        "description": "Inline partition block with TI wrapper",
        "$ref": "#/$defs/NodeTypePartitionBlock"
      },
      {
        "description": "Import partition block",
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
}
```

### Pattern 3: TI Wrapper Content (Set of Types)

Content within TI wrappers (the actual type sets, delimited by indentation):

```json
{
  "oneOf": [
    {
      "description": "Inline type set (partition block content delimited by indentation)",
      "anyOf": [
        {
          "description": "Singleton set (single type)",
          "$ref": "#/$defs/NodeType"
        },
        {
          "description": "Multi-element set (multiple types at same indentation level)",
          "type": "array",
          "items": { "$ref": "#/$defs/NodeType" }
        }
      ]
    },
    {
      "description": "Import type set",
      "type": "object",
      "required": ["import"],
      "properties": {
        "import": {
          "type": "string",
          "description": "Import set of types for this TI"
        }
      },
      "additionalProperties": false
    }
  ]
}
```

## Schema Structure Changes

### 1. NodeTypes Property

**Current Issue**: NodeTypesProperty has oneOf but nested TI content doesn't support imports.

**Solution**: Ensure all TI wrapper contents support imports, recognizing that indentation delimits the type sets.

```json
"NodeTypesProperty": {
  "oneOf": [
    {
      "$ref": "#/$defs/NodeTypesArray"
    },
    {
      "description": "TI wrapper patterns with import support (sets delimited by indentation)",
      "type": "object",
      "patternProperties": {
        "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
          "oneOf": [
            {
              "type": "object",
              "patternProperties": {
                "^(abstract|concrete|final|sealed)$": {
                  "oneOf": [
                    {
                      "description": "Inline type set (delimited by indentation)",
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
                      "description": "Import type set",
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
              "description": "Import entire TI wrapper with its type set",
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
      "description": "Import entire nodeTypes property",
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

### 2. NodeTypesArray Items

**Current Issue**: Array items (NodeTypeItem) have import support but TI wrapper contents don't.

**Solution**: Ensure TI wrapper contents within array items support imports, with indentation delimiting type sets.

```json
"NodeTypeItem": {
  "oneOf": [
    { 
      "description": "Bare node type (singleton set with implicit TI)",
      "$ref": "#/$defs/NodeType" 
    },
    {
      "description": "TI wrappers with import-capable contents (sets delimited by indentation)",
      "type": "object",
      "patternProperties": {
        "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
          "type": "object",
          "patternProperties": {
            "^(abstract|concrete|final|sealed)$": {
              "oneOf": [
                {
                  "description": "Inline type set (delimited by indentation)",
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
                  "description": "Import type set",
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
        }
      }
    },
    {
      "description": "Import entire partition block",
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

### 3. GraphType Nested Properties

**Current Issue**: GraphType.subtypesOf.abstract.nodeTypes doesn't support imports.

**Solution**: Apply TI-content import pattern to all nested locations, respecting indentation-based set delimitation.

```json
"GraphType": {
  "type": "object",
  "properties": {
    "subtypesOf": {
      "type": "object",
      "properties": {
        "abstract": {
          "type": "object",
          "properties": {
            "nodeTypes": {
              "oneOf": [
                {
                  "description": "Inline type set (delimited by indentation)",
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
                  "description": "Import type set",
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
        }
      }
    }
  }
}
```

## Implementation Strategy

### Phase 1: Identify All TI-Wrappable Locations
1. **Top-level arrays**: nodeTypes, edgeTypes properties
2. **Array items**: NodeTypeItem, EdgeTypeItem with TI wrappers
3. **Nested TI contexts**: subtypesOf.abstract, sealed contents, etc.
4. **Pattern properties**: All TI wrapper pattern matches
5. **Indentation-delimited sets**: All locations where type sets are defined by indentation

### Phase 2: Apply Uniform OneOf Pattern
1. **Create reusable definitions** for TI-content import patterns
2. **Update all identified locations** with consistent oneOf structure
3. **Ensure $ref chains** resolve correctly with import options
4. **Test partition flexibility** (coarse, fine, mixed partitions)
5. **Validate indentation-based set delimitation** in examples

### Phase 3: Validation and Testing
1. **PC form validation**: All existing examples continue to validate
2. **C form validation**: Canonicalized forms validate successfully
3. **Partition testing**: Test various partition granularities
4. **Import resolution**: Test TI-level import resolution
5. **Indentation testing**: Verify set delimitation by indentation works correctly

## Examples

### Example 1: Coarse Partition (One TI, Multiple Types - Set Delimited by Indentation)

```yaml
# PC Form
nodeTypes:
  - exactlyOf:
      concrete:
        import: "person-hierarchy.yaml"  # Imports {Person, Employee, Manager}

# Imported content (person-hierarchy.yaml)
# Indentation shows these form a single set under the TI
- nodeType: {typeLabel: Person, ...}
- nodeType: {typeLabel: Employee, extends: Person, ...}
- nodeType: {typeLabel: Manager, extends: Employee, ...}

# C Form (after canonicalization)
# The set structure is preserved, delimited by indentation
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person, ...}
        - nodeType: {typeLabel: Employee, extends: Person, ...}
        - nodeType: {typeLabel: Manager, extends: Employee, ...}
```

### Example 2: Fine Partition (Each Type Gets Own TI - Singleton Sets)

```yaml
# PC Form
nodeTypes:
  # Singleton set (cardinality 1)
  - exactlyOf:
      concrete:
        import: "person.yaml"     # Imports {Person}
  # Singleton set (cardinality 1)
  - subtypesOf:
      abstract:
        import: "employee.yaml"   # Imports {Employee}
  # Singleton set (cardinality 1)
  - final:
      import: "manager.yaml"     # Imports {Manager}

# C Form (after canonicalization)
# Each singleton set is delimited by indentation under its TI
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person, ...}
  - subtypesOf:
      abstract:
        - nodeType: {typeLabel: Employee, ...}
  - exactlyOf:  # final → exactlyOf:concrete
      concrete:
        - nodeType: {typeLabel: Manager, ...}
```

### Example 3: Mixed Partition (Some Coarse, Some Fine - Mixed Set Cardinalities)

```yaml
# PC Form
nodeTypes:
  # Multi-element set (cardinality 2) - delimited by indentation
  - exactlyOf:
      concrete:
        import: "core-types.yaml"    # Imports {Person, Company}
  # Singleton set (cardinality 1) - inline
  - subtypesOf:
      abstract:
        - nodeType: {typeLabel: Vehicle, ...}
  # Multi-element set (cardinality 3) - delimited by indentation
  - sealed:
      import: "place-hierarchy.yaml"  # Imports {Place, City, Country}

# C Form shows mixed partition granularities
# Indentation clearly delimits each set under its TI
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person, ...}
        - nodeType: {typeLabel: Company, ...}
  - subtypesOf:
      abstract:
        - nodeType: {typeLabel: Vehicle, ...}
  - exactlyOf:  # sealed → exactlyOf:concrete
      concrete:
        - nodeType: {typeLabel: Place, ...}
        - nodeType: {typeLabel: City, extends: Place, ...}
        - nodeType: {typeLabel: Country, extends: Place, ...}
```

### Example 4: Indentation Showing Set Delimitation

```yaml
# The indentation structure clearly shows set boundaries
graphType:
  nodeTypes:
    # Set 1: {Person, Employee, Manager} under exactlyOf:concrete
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Person, ...}
          - nodeType: {typeLabel: Employee, extends: Person, ...}
          - nodeType: {typeLabel: Manager, extends: Employee, ...}
    
    # Set 2: {Vehicle} under subtypesOf:abstract (singleton)
    - subtypesOf:
        abstract:
          - nodeType: {typeLabel: Vehicle, ...}
    
    # Set 3: {Place, City, Country} under exactlyOf:concrete
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Place, ...}
          - nodeType: {typeLabel: City, extends: Place, ...}
          - nodeType: {typeLabel: Country, extends: Place, ...}
```

### Example 5: TI as Unit of Import - Cannot Import Individual Types

```yaml
# CORRECT: Import at TI level (imports entire partition block)
nodeTypes:
  - exactlyOf:
      concrete:
        import: "person-hierarchy.yaml"  # Imports TI + {Person, Employee, Manager}

# person-hierarchy.yaml contains:
# - nodeType: {typeLabel: Person, ...}
# - nodeType: {typeLabel: Employee, extends: Person, ...}
# - nodeType: {typeLabel: Manager, extends: Employee, ...}

# INCORRECT: Cannot import individual type from within a TI
# This is NOT supported - you cannot cherry-pick types from a partition block
nodeTypes:
  - exactlyOf:
      concrete:
        - import: "person.yaml"      # ❌ Cannot import just Person
        - import: "employee.yaml"    # ❌ Cannot import just Employee
        - import: "manager.yaml"     # ❌ Cannot import just Manager

# The TI is the atomic unit of import - you import the whole partition block or none of it
```

### Example 6: Two-Phase Import - Import Entire TI vs Import Content Only

```yaml
# person-types.yaml (source file with TI wrapper)
subtypesOf:
  abstract:
    - nodeType: {typeLabel: Person, ...}
    - nodeType: {typeLabel: Employee, extends: Person, ...}
    - nodeType: {typeLabel: Manager, extends: Employee, ...}

# PHASE 1: Import entire TI wrapper + content (preserve TI)
nodeTypes:
  - import: "person-types.yaml"  # Imports subtypesOf:abstract + {Person, Employee, Manager}

# Result after import resolution:
nodeTypes:
  - subtypesOf:
      abstract:
        - nodeType: {typeLabel: Person, ...}
        - nodeType: {typeLabel: Employee, extends: Person, ...}
        - nodeType: {typeLabel: Manager, extends: Employee, ...}

# PHASE 2: Import content only, strip TI, reinterpret with outer TI
nodeTypes:
  - exactlyOf:
      concrete:
        import: "person-types.yaml"  # Imports {Person, Employee, Manager}, strips subtypesOf:abstract

# Result after import resolution (TI override):
nodeTypes:
  - exactlyOf:
      concrete:
        - nodeType: {typeLabel: Person, ...}
        - nodeType: {typeLabel: Employee, extends: Person, ...}
        - nodeType: {typeLabel: Manager, extends: Employee, ...}

# The types are now interpreted as exactlyOf:concrete instead of subtypesOf:abstract
```

### Example 7: Edge Type Endpoint TI Override

```yaml
# Edge types can have TI wrappers at the endpoint level that override the edge type's TI
edgeTypes:
  - exactlyOf:
      concrete:
        - edgeType:
            typeLabel: WORKS_FOR
            from:
              # Endpoint-specific TI overrides the edge type's TI
              subtypesOf:
                abstract:
                  - nodeType: {typeLabel: Person, ...}
            to:
              # Another endpoint-specific TI
              exactlyOf:
                concrete:
                  - nodeType: {typeLabel: Company, ...}
            via: {typeLabel: WORKS_FOR, ...}

# The edge type itself has exactlyOf:concrete TI
# But the endpoints (from/to) can have their own TI wrappers
# This is the ONLY exception to "TI extends down to contained types"
```

### Example 8: Canonicalization Consolidation - Multiple nodeTypes Instances to One

```yaml
# PC Form with MULTIPLE nodeTypes instances scattered throughout graphType
graphType:
  nodeTypes:
    abstract:
      - nodeType: {typeLabel: Person, ...}  # a
  concrete:
    - nodeType: {typeLabel: Company, ...}  # b
  abstract:
    nodeTypes:
      - nodeType: {typeLabel: Vehicle, ...}  # c

# C Form after canonicalization
# 1. Consolidates ALL nodeTypes instances into ONE nodeTypes collection
# 2. Amalgamates types with same TI into single partition blocks
graphType:
  nodeTypes:
    - abstract:
        - nodeType: {typeLabel: Person, ...}  # a
        - nodeType: {typeLabel: Vehicle, ...}  # c (amalgamated with a)
    - concrete:
        - nodeType: {typeLabel: Company, ...}  # b

# Key transformations:
# - Multiple nodeTypes instances → ONE nodeTypes collection
# - Types with same TI (abstract) → ONE partition block
# - Result: Single nodeTypes array with TI-partitioned subsets
```

### Example 9: Canonicalization Amalgamation - Same TI Partition Blocks Merged

```yaml
# PC Form with multiple partition blocks of same TI
graphType:
  nodeTypes:
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Person, ...}
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Company, ...}
    - subtypesOf:
        abstract:
          - nodeType: {typeLabel: Vehicle, ...}
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Product, ...}

# C Form after canonicalization (amalgamated by TI)
graphType:
  nodeTypes:
    - exactlyOf:
        concrete:
          - nodeType: {typeLabel: Person, ...}
          - nodeType: {typeLabel: Company, ...}
          - nodeType: {typeLabel: Product, ...}
    - subtypesOf:
        abstract:
          - nodeType: {typeLabel: Vehicle, ...}

# All exactlyOf:concrete types are consolidated into one partition block
# All subtypesOf:abstract types are consolidated into one partition block
```

## Validation Strategy

### 1. Structural Validation
- **OneOf consistency**: All TI-wrappable locations have proper oneOf
- **Import option structure**: All import options follow standard pattern
- **$ref resolution**: All references resolve correctly with import support
- **Indentation validation**: Set boundaries are correctly defined by indentation

### 2. Semantic Validation
- **TI preservation**: Imports preserve type interpretation semantics
- **Partition integrity**: Imported partition blocks maintain coherence
- **Canonicalization compatibility**: C forms validate after PC→C transformation
- **Set delimitation**: Indentation correctly delimits type sets

### 3. Flexibility Testing
- **Coarse partitions**: Single TI wrapping many types
- **Fine partitions**: Each type in its own TI (singleton sets)
- **Mixed partitions**: Combination of coarse and fine
- **Nested imports**: Imports within TI wrapper hierarchies
- **Indentation patterns**: Various indentation structures for set delimitation

## Success Metrics

1. **100% PC validation**: All pre-canonical forms validate
2. **100% C validation**: All canonical forms validate
3. **Partition flexibility**: All valid partitions supported
4. **Import consistency**: Uniform patterns across all TI locations
5. **No regressions**: Existing functionality preserved
6. **Schema coherence**: Consistent structure throughout
7. **Indentation clarity**: Set boundaries clearly defined by indentation

## Risk Mitigation

### Risk 1: Schema Complexity
**Mitigation**: Use reusable definitions and clear documentation emphasizing indentation-based set delimitation

### Risk 2: Performance Impact
**Mitigation**: Test validation performance with complex partition structures

### Risk 3: Backward Compatibility
**Mitigation**: Extensive testing with existing documents

### Risk 4: TI Semantic Correctness
**Mitigation**: Validate that imports preserve type interpretation meaning and set boundaries

### Risk 5: Indentation Ambiguity
**Mitigation**: Clear documentation and examples showing how indentation delimits sets
