# Design Document: Type Interpretation System Simplification

**Version**: 2.0  
**Date**: 2024-12-11  
**Status**: Active Design Document  
**Related Requirements**: `.kiro/specs/ti-ordering-refactor/requirements.md`

## Overview

This document describes the design for fundamentally simplifying the LEX-2026.0.3.2 Type Interpretation (TI) system from a complex two-level architecture to a streamlined single-level system. The simplification includes four major architectural changes: eliminating freestanding types, preventing all forms of TI nesting, and consolidating the TI system into three primary forms with synonyms. This represents a major architectural improvement that will significantly reduce complexity while maintaining full semantic expressiveness.

**Context**: This work represents a fundamental redesign of the Type Interpretation system based on lessons learned from the complex two-level implementation. The four simplification changes eliminate architectural complexity while maintaining full semantic capability, making the system significantly easier to understand, implement, and maintain.

## MAJOR SIMPLIFICATION: TI Only Applies to Sub-Arrays

**FUNDAMENTAL DESIGN CHANGE**: TI wrappers are **ELIMINATED** at graphType and collection levels. TI **ONLY** applies to sub-arrays within type collections.

**Type Collections**: Properties like `nodeTypes:`, `edgeTypes:` that contain arrays - **NO TI wrappers allowed**
**Type Arrays**: The actual `[...]` arrays inside collections - **NO TI wrappers at array level**  
**Sub-Arrays**: Subsequences within arrays - **TI wrappers ONLY apply here**

**TI Application - SIMPLIFIED**:
1. **Sub-Array Level ONLY**: TI wraps subsequences within the array content inside collections
2. **Endpoint Level**: TI wraps endpoint references within edge types
3. **Default Behavior**: All types without explicit TI are semantically equivalent to `exactlyOfConcrete`

**Key Insight**: TI wrappers apply **ONLY** to sub-arrays (subsequences) within collections. Collection properties (`nodeTypes:`, `edgeTypes:`) and graphType itself **NEVER** have TI wrappers. This eliminates 3 locations and significantly simplifies the system.

## NodeTypeItem/EdgeTypeItem: Essential for Array Subsequence Model

**CRITICAL CLARIFICATION**: NodeTypeItem and EdgeTypeItem are **NOT redundant** - they are essential for enabling the array subsequence partitioning model.

**What NodeTypeItem/EdgeTypeItem Define**:
- What can appear as elements within `nodeTypes`/`edgeTypes` arrays
- Support for bare types: `{ typeLabel: Person }`
- Support for TI-wrapped individual types: `exactlyOfConcrete: { typeLabel: Person }`
- Support for TI-wrapped array subsequences: `subtypesOfAbstract: [{ typeLabel: Vehicle }, { typeLabel: Car }]`

**Array Subsequence Partitioning Example**:
```yaml
nodeTypes:                              # Collection containing array
  - typeLabel: Person                   # Bare element (NodeTypeItem)
  - subtypesOfAbstract:                 # TI-wrapped subsequence (NodeTypeItem)
      - typeLabel: Vehicle              # Array within subsequence
      - typeLabel: Car
  - exactlyOfConcrete:                  # Another TI-wrapped subsequence (NodeTypeItem)
      - typeLabel: Company
      - typeLabel: Organization
```

**Why NodeTypeItem/EdgeTypeItem Are Essential**:
1. **Array Element Definition**: Define what can be array elements (bare types, TI-wrapped types, TI-wrapped subsequences)
2. **Subsequence Support**: Enable partitioning arrays into TI-wrapped subsequences
3. **Flexible Structure**: Allow mixing bare elements with TI-wrapped subsequences in the same array
4. **Schema Validation**: Provide proper validation for complex array structures

**Without NodeTypeItem/EdgeTypeItem**: Arrays could only contain uniform elements, eliminating the powerful subsequence partitioning capability that makes the TI system flexible and expressive.

## Simplification Rationale

The current two-level TI system has proven overly complex and difficult to implement correctly. This design addresses four fundamental issues:

### Issue 1: Complex Two-Level Architecture
The current system requires understanding both interpretation facets (`exactlyOf`, `subtypesOf`, `properSubtypesOf`) and concreteness facets (`abstract`, `concrete`, `final`, `sealed`), creating 6+ valid combinations.

**Current (Complex)**:
```yaml
# Two-level nesting with multiple facets
exactlyOf:
  concrete:
    nodeTypes: [...]
subtypesOf:
  abstract:
    edgeTypes: [...]
```

**Simplified (Single-Level)**:
```yaml
# Single-level with clear semantics
exactlyOfConcrete:
  nodeTypes: [...]
subtypesOfAbstract:
  edgeTypes: [...]
```

### Issue 2: Freestanding Type Inconsistency
The current system allows both freestanding types and array-based types, creating inconsistent organization patterns.

**Current (Inconsistent)**:
```yaml
graphType:
  nodeType: {...}        # Freestanding type
  nodeTypes: [...]       # Array of types
```

**Simplified (Consistent)**:
```yaml
graphType:
  nodeTypes: [...]       # Only arrays allowed
  subtypesOfConcrete:
    nodeTypes: [...]     # TI-wrapped arrays
```

### Issue 3: TI Nesting Complexity
The current system's two-level architecture inherently allows confusing nesting patterns.

**Current (Confusing)**:
```yaml
exactlyOf:
  concrete:
    subtypesOf:          # Nested TI - confusing semantics
      abstract: [...]
```

**Simplified (Clear)**:
```yaml
exactlyOfConcrete: [...]     # Single level - clear semantics
subtypesOfAbstract: [...]     # No nesting possible
```

### Issue 4: Synonym Proliferation Without Clear Mapping
The current system has multiple synonyms without clear canonical forms, leading to inconsistent usage.

## Phase 2 Scope Summary - MAJOR SIMPLIFICATION

**What Phase 2 Eliminates**: **Locations 1-3** (graphType TI, collection-level TI) - completely removed from the system

**What Phase 2 Fixes**: **2 broken locations** (Locations 4-5) where TI sub-array wrappers are in the wrong order.

**What Phase 2 Does NOT Fix**: 
- Location 8 (edgeTypeEndpointNodeTypeInterpretation) - Already working from previous phases

**Critical Discovery - Tasks 10-11 Correction**:
- **Vestigial Definitions**: `NodeTypesProperty` and `EdgeTypesProperty` definitions exist in schema but are NOT REFERENCED anywhere
  - These are remnants from an earlier design at lines ~2470-2700 and ~3181-3400
  - They must be completely DELETED from the schema
- **Missing Level-1 TI Wrappers**: GraphType definition is missing 1-level TI wrappers
  - GraphType currently has: 0-level (bare) and 2-level (explicit) TI wrappers
  - GraphType is MISSING: 1-level (shorthand) TI wrappers `concrete:` and `abstract:`
  - These must be added as explicit properties in GraphType with both nodeTypes and edgeTypes children

**What GraphType Currently Has**:
```yaml
graphType:
  nodeTypes: [...]              # ✅ 0-level (bare)
  edgeTypes: [...]              # ✅ 0-level (bare)
  exactlyOf:                    # ✅ 2-level
    concrete:
      nodeTypes: [...]
      edgeTypes: [...]
  subtypesOf:                   # ✅ 2-level
    abstract:
      nodeTypes: [...]
      edgeTypes: [...]
  properSubtypesOf:             # ✅ 2-level
    concrete/abstract:
      nodeTypes: [...]
      edgeTypes: [...]
```

**What GraphType Needs (1-level TI wrappers)**:
```yaml
graphType:
  concrete:                     # ❌ MISSING 1-level (shorthand for exactlyOf:concrete:)
    nodeTypes: [...]
    edgeTypes: [...]
  abstract:                     # ❌ MISSING 1-level (shorthand for properSubtypesOf:abstract:)
    nodeTypes: [...]
    edgeTypes: [...]
```

**Reference**: See `TASKS-10-11-CORRECTION-ANALYSIS.md` for detailed analysis.

## CORE DESIGN PRINCIPLE: Explicit Properties Only

**FUNDAMENTAL GUARDRAIL**: This design uses **explicit properties exclusively**. Pattern properties (`patternProperties`) are **NEVER** used anywhere in the schema.

**Why Explicit Properties Are Required**:
1. **Predictable behavior**: Each property is explicitly defined with clear semantics
2. **IDE support**: Better autocomplete, validation, and development experience
3. **No conflicts**: Eliminates JSON Schema conflicts between pattern and regular properties
4. **Maintainability**: Clear, readable schema structure that's easy to understand and modify
5. **Sibling support**: Enables multiple TI wrappers with different facets at the same level

**Pattern Properties Are Prohibited**:
- Pattern properties create unpredictable conflicts with regular properties
- They prevent proper sibling TI wrapper support
- They make the schema harder to understand and maintain
- They are incompatible with our design goals

**The Explicit Properties Approach**:
- **For single-wrapper locations** (Location 1): Use `oneOf` with explicit properties for each TI level
- **For sibling-wrapper locations** (Locations 2-7): Use explicit sibling properties without oneOf
- **All TI keywords**: `concrete`, `abstract`, `exactlyOf`, `subtypesOf`, `properSubtypesOf` are explicit properties
- **Reference pattern**: Phases A-D (Locations 6-8) demonstrate the CORRECT explicit properties approach

**Current Schema Issues to Fix**:
- Location 1 (GraphSchemaContent) currently uses `patternProperties` - this must be **ELIMINATED**
- REMOVE all `patternProperties` from GraphSchemaContent
- ADD explicit properties: `graphType`, `concrete`, `abstract`, `exactlyOf`, `subtypesOf`, `properSubtypesOf`
- Use `oneOf` to ensure exactly one graphType (bare or wrapped) exists
- Each TI property explicitly contains `graphType` as a child

**This Is Non-Negotiable**: Any use of `patternProperties` in the schema is considered a bug and must be replaced with explicit properties.

## Architecture

### Single-Level TI System

Type Interpretations operate at two expression levels:

1. **0-Level (Bare)**: `typeLabel: Person` - No wrapper, implicit `exactlyOfConcrete` semantics
2. **1-Level (Wrapped)**: Single TI wrapper keyword
   - **Primary Forms**: `exactlyOfConcrete: { nodeTypes: [...] }`, `subtypesOfConcrete: { nodeTypes: [...] }`, `subtypesOfAbstract: { nodeTypes: [...] }`
   - **Synonyms**: `concrete: { nodeTypes: [...] }`, `subtypesOf: { nodeTypes: [...] }`, `properSubtypesOf: { nodeTypes: [...] }`, `abstract: { nodeTypes: [...] }`

This is implemented using explicit JSON Schema properties for each TI keyword, with canonicalization mapping synonyms to primary forms.

### Three Primary TI Forms

The simplified system has exactly three primary TI forms with clear semantics:

1. **`exactlyOfConcrete`**: Exact type matching, concrete (instantiable) types
   - **Synonyms**: `exactlyOf`, `concrete`
   - **Semantics**: Types must match exactly, can be instantiated
   - **Example**: `exactlyOfConcrete: { nodeTypes: [{ typeLabel: Person }] }`

2. **`subtypesOfConcrete`**: Subtype matching, concrete (instantiable) types  
   - **Synonyms**: `subtypesOf`
   - **Semantics**: Allows subtypes, can be instantiated
   - **Example**: `subtypesOfConcrete: { nodeTypes: [{ typeLabel: Vehicle }] }`

3. **`subtypesOfAbstract`**: Subtype matching, abstract (non-instantiable) types
   - **Synonyms**: `properSubtypesOf`, `abstract`
   - **Semantics**: Allows subtypes, cannot be instantiated (abstract)
   - **Example**: `subtypesOfAbstract: { nodeTypes: [{ typeLabel: Entity }] }`

**Important Distinction**: The keywords `final:` and `sealed:` are **NOT** part of the type interpretation system. They belong to the **type finalization** system, which is a separate concern that will be addressed in a future phase.

### Synonym Mapping and Canonicalization

The TI synonyms provide convenient shorthand syntax that maps to canonical primary forms during preprocessing:

**Synonym Mappings**:
- **`concrete:`** → **`exactlyOfConcrete:`**
  - Meaning: Exact type matching, concrete (instantiable) types
  - Example: `concrete: { nodeTypes: [...] }` → `exactlyOfConcrete: { nodeTypes: [...] }`

- **`exactlyOf:`** → **`exactlyOfConcrete:`**
  - Meaning: Same as `concrete:`, exact type matching
  - Example: `exactlyOf: { nodeTypes: [...] }` → `exactlyOfConcrete: { nodeTypes: [...] }`

- **`subtypesOf:`** → **`subtypesOfConcrete:`**
  - Meaning: Subtype matching, concrete (instantiable) types
  - Example: `subtypesOf: { nodeTypes: [...] }` → `subtypesOfConcrete: { nodeTypes: [...] }`

- **`properSubtypesOf:`** → **`subtypesOfAbstract:`**
  - Meaning: Subtype matching, abstract (non-instantiable) types
  - Example: `properSubtypesOf: { nodeTypes: [...] }` → `subtypesOfAbstract: { nodeTypes: [...] }`

- **`abstract:`** → **`subtypesOfAbstract:`**
  - Meaning: Same as `properSubtypesOf:`, subtype matching with abstract types
  - Example: `abstract: { nodeTypes: [...] }` → `subtypesOfAbstract: { nodeTypes: [...] }`

**Canonicalization Process**: During preprocessing, all synonyms are automatically converted to their canonical primary forms, ensuring consistent internal representation while maintaining author-friendly syntax.

### Array-Only Organization Model

**All Locations** use a consistent array-only organization model with clear distinction between collections and array content:

**Collection vs Array Structure**:
- **Type Collections**: Properties like `nodeTypes:`, `edgeTypes:` that contain arrays
- **Type Arrays**: The actual `[...]` arrays inside collections
- **Array Content**: Individual elements and subsequences within type arrays
- **TI Application**: TI wrappers apply to collections, array content, and subsequences - NOT to collection properties themselves

**Example - nodeTypes Collection with TI Sub-Arrays (COMPLETE SYNTAX)**:
```yaml
graphType:
  nodeTypes:                             # Type collection (NO TI wrappers at this level)
    - nodeType: Person                   # Abbreviated syntax (simple typeLabel only)
    - nodeType:                          # Full syntax with properties
        typeLabel: Company
        implies:
          propertyTypes:
            - name: founded
              valueType: DATE
    - nodeType:                          # Multiple type labels
        typeLabels: [Cat, Dog]
        implies:
          propertyTypes:
            - name: age
              valueType: INTEGER
    - abstract:                          # TI-wrapped sub-array 1
        - nodeType:
            typeLabel: Entity
            implies:
              propertyTypes:
                - name: id
                  valueType: STRING
        - nodeType:
            typeLabel: Vehicle
            extends: Entity
            adding:
              propertyTypes:
                - name: wheels
                  valueType: INTEGER
    - concrete:                          # TI-wrapped sub-array 2
        - nodeType: Organization         # Abbreviated syntax within TI sub-array
        - nodeType:
            typeLabel: Department
            extends: Organization
    - nodeType: Location                 # Bare elements can continue after TI sub-arrays
    - nodeType:                          # Another bare element with properties
        typeLabel: Event
        implies:
          propertyTypes:
            - name: date
              valueType: DATETIME
```

**Key Organizational Principles**:
1. **Collections Contain Arrays**: `nodeTypes:` and `edgeTypes:` are collection properties containing arrays
2. **TI Wraps Content**: TI wrappers apply to array content and subsequences, not collection properties
3. **Array Subsequences**: Arrays can be partitioned into TI-wrapped subsequences
4. **Sibling Structure**: TI subsequences are siblings within arrays, never nested
5. **No Freestanding Types**: All types must be array elements or subsequence elements

**Eliminated Patterns**:
- ❌ Freestanding types: `nodeType: { typeLabel: Person }`
- ❌ Mixed organization: Some freestanding, some in arrays
- ❌ TI nesting: One TI wrapper containing another
- ❌ TI on collection properties: TI wrappers do not apply to `nodeTypes:` or `edgeTypes:` properties themselves

### Sub-Array TI Within Collections - SIMPLIFIED MODEL

TI wrappers **ONLY** apply to sub-arrays within collections. No TI at graphType or collection level:

```yaml
graphType:
  nodeTypes:                   # Collection (NO TI wrappers allowed at this level)
    - nodeType: Person         # Abbreviated syntax (simple typeLabel only)
    - nodeType:                # Full syntax with properties
        typeLabel: Company
        implies:
          propertyTypes:
            - name: founded
              valueType: DATE
    - nodeType:                # Multiple type labels
        typeLabels: [Cat, Dog]
    - subtypesOfAbstract:      # TI-wrapped sub-array
        - nodeType:
            typeLabel: Entity
            implies:
              propertyTypes:
                - name: id
                  valueType: STRING
        - nodeType: Vehicle     # Abbreviated syntax within TI sub-array
    - exactlyOfConcrete:       # Another TI-wrapped sub-array  
        - nodeType: Organization
        - nodeType:
            typeLabel: Department
            extends: Organization
    - nodeType: Location       # Bare elements can continue after TI sub-arrays
    - nodeType:                # Another bare element with properties
        typeLabel: Event
        implies:
          propertyTypes:
            - name: date
              valueType: DATETIME
    - concrete:                # Another TI-wrapped sub-array (synonym)
        - nodeType: Product
        - nodeType: Service
    - nodeType: User           # More bare elements after TI sub-arrays
  edgeTypes:                   # Collection (NO TI wrappers allowed at this level)
    - edgeType:                # Directed edge - abbreviated syntax
        directed:
          from: Person
          to: Person
          via: KNOWS
    - abstract:                # TI-wrapped sub-array (synonym)
        - edgeType:
            directed:
              from: Entity
              to: Entity
              via:
                typeLabel: RELATIONSHIP
              implies:
                propertyTypes:
                  - name: strength
                    valueType: FLOAT
        - edgeType:
            undirected:
              between: Location
              and: Location
              via: CONNECTED_TO
    - edgeType:                # Bare elements can continue after TI sub-arrays
        directed:
          from: Person
          to: Company
          via:
            typeLabel: WORKS_FOR
          extends: RELATIONSHIP
          adding:
            propertyTypes:
              - name: since
                valueType: DATE
```

**Using Synonyms (Pre-Canonical Form)**:
```yaml
graphType:
  nodeTypes:
    - nodeType:
        typeLabel: Person
    - properSubtypesOf:        # Synonym for subtypesOfAbstract
        - nodeType:
            typeLabel: Entity
    - concrete:                # Synonym for exactlyOfConcrete
        - nodeType:
            typeLabel: Company
```

**Syntax Variations**:
1. **Abbreviated Syntax**: For simple types with only a typeLabel: `- nodeType: Person`
2. **Full Syntax**: For types with properties: `- nodeType: { typeLabel: Person, implies: {...} }`
3. **Multiple Labels**: For types with multiple labels: `- nodeType: { typeLabels: [Cat, Dog] }`
4. **Extension Syntax**: For types that extend others: `- nodeType: { typeLabel: Car, extends: Vehicle, adding: {...} }`

## 🎯 SIMPLIFIED TYPE INTERPRETATION DESIGN

**⭐ CRITICAL DESIGN EXAMPLE ⭐**

This example represents the **SIMPLIFIED TYPE INTERPRETATION DESIGN** - the current inflection point in our TI system architecture. This is the target design that eliminates the complex two-level TI architecture in favor of a streamlined single-level system.

**Complete Example - All Syntax Possibilities with Interleaved Collections**:
```yaml
graphType:
  # Interleaved nodeTypes and edgeTypes collections demonstrate flexible organization
  
  nodeTypes:
    # Abbreviated syntax - simple typeLabel only
    - nodeType: Person
    
    # Full syntax with single typeLabel and implies (labels + propertyTypes)
    - nodeType:
        typeLabel: Company
        implies:
          labels: [Organization, Entity]
          propertyTypes:
            - name: founded
              valueType: DATE
            - name: employees
              valueType: INTEGER
  
  edgeTypes:
    # Directed edge - abbreviated syntax
    - edgeType:
        from: Person
        to: Person
        via: KNOWS
    
    # Directed edge - full syntax with implies
    - edgeType:
        from: Person
        to: Company
        via:
          typeLabel: WORKS_FOR
          implies:
            labels: [Employment, Relationship]
            propertyTypes:
              - name: since
                valueType: DATE
              - name: position
                valueType: STRING
  
  nodeTypes:
    # Multiple typeLabels with implies
    - nodeType:
        typeLabels: [Cat, Dog, Pet]
        implies:
          labels: [Animal, LivingThing]
          propertyTypes:
            - name: age
              valueType: INTEGER
            - name: name
              valueType: STRING
    
    # Extension with adding (labels + propertyTypes)
    - nodeType:
        typeLabel: Employee
        extends: Person
        adding:
          labels: [Worker, Staff]
          propertyTypes:
            - name: employeeId
              valueType: STRING
            - name: salary
              valueType: DECIMAL
    
    # TI-wrapped sub-array with abstract types
    - abstract:
        - nodeType:
            typeLabel: Vehicle
            implies:
              labels: [Transport, Machine]
              propertyTypes:
                - name: wheels
                  valueType: INTEGER
        - nodeType: Engine  # Abbreviated within TI sub-array
  
  edgeTypes:
    # Undirected edge - abbreviated syntax
    - edgeType:
        between: Person
        and: Person
        via: FRIENDS_WITH
    
    # Undirected edge - full syntax
    - edgeType:
        between: Person
        and: Person
        via:
          typeLabel: MARRIED_TO
          implies:
            labels: [Friendship, SocialConnection]
            propertyTypes:
              - name: since
                valueType: DATE
              - name: closeness
                valueType: FLOAT
    
    # TI-wrapped sub-array for edge types
    - abstract:
        - edgeType:
            from: Entity
            to: Entity
            via:
              typeLabel: RELATIONSHIP
              implies:
                labels: [Connection, Link]
                propertyTypes:
                  - name: strength
                    valueType: FLOAT
        - edgeType:
            between: Location
            and: Location
            via: CONNECTED_TO
  
  nodeTypes:
    # More bare elements after TI sub-array
    - nodeType: Location
    
    # Another TI-wrapped sub-array with concrete types
    - concrete:
        - nodeType:
            typeLabel: Car
            extends: Vehicle
            adding:
              labels: [Automobile]
              propertyTypes:
                - name: model
                  valueType: STRING
        - nodeType:
            typeLabels: [Truck, Lorry]
            extends: Vehicle
    
    # Final bare elements
    - nodeType: Event
  
  edgeTypes:
    # Extension syntax for edge types
    - edgeType:
        from: Person
        to: Company
        via:
          typeLabel: MANAGES
          extends: WORKS_FOR
          adding:
            labels: [Leadership]
            propertyTypes:
              - name: teamSize
                valueType: INTEGER
    
    # Final edge type
    - edgeType:
        from: Vehicle
        to: Location
        via: LOCATED_AT
```

**🎯 END OF SIMPLIFIED TYPE INTERPRETATION DESIGN EXAMPLE**

This example demonstrates the complete simplified TI architecture with:
- ✅ Single-level TI wrappers (no nesting)
- ✅ Array-only organization (no freestanding types)  
- ✅ TI sub-arrays within collections only
- ✅ Clear syntax variations (abbreviated, full, extension)
- ✅ Mixed bare elements and TI-wrapped subsequences
- ✅ Interleaved type collections (nodeTypes and edgeTypes mixed)
- ✅ Corrected edge abbreviated syntax (`via: KNOWS`)

### Complete Synonym Demonstration

**All TI Canonical Forms and Synonyms**:
```yaml
graphType:
  nodeTypes:
    # Primary canonical forms
    - exactlyOfConcrete:
        - nodeType: Person
        - nodeType: Company
    
    - subtypesOfConcrete:
        - nodeType: Vehicle
        - nodeType: Machine
    
    - subtypesOfAbstract:
        - nodeType: Entity
        - nodeType: Thing
    
    # Synonym forms (equivalent to above)
    - concrete:              # → exactlyOfConcrete
        - nodeType: Product
        - nodeType: Service
    
    - exactlyOf:             # → exactlyOfConcrete  
        - nodeType: Location
        - nodeType: Address
    
    - subtypesOf:            # → subtypesOfConcrete
        - nodeType: Animal
        - nodeType: Plant
    
    - properSubtypesOf:      # → subtypesOfAbstract
        - nodeType: Concept
        - nodeType: Idea
    
    - abstract:              # → subtypesOfAbstract
        - nodeType: BaseType
        - nodeType: Interface
  
  edgeTypes:
    # Synonyms work the same way for edge types
    - concrete:
        - edgeType:
            from: Person
            to: Company
            via: WORKS_FOR
    
    - abstract:
        - edgeType:
            from: Entity
            to: Entity
            via: RELATES_TO
```

**⚠️ IMPLEMENTATION NOTE**: When agreeing to any implementation, remind the user to create an example that fully demonstrates synonyms (`concrete:`, `subtypesOf:`, `properSubtypesOf:`, `abstract:`, `exactlyOf:`) in addition to the primary forms (`exactlyOfConcrete:`, `subtypesOfConcrete:`, `subtypesOfAbstract:`).

**Key Syntax Rules**:
- `implies:` can contain both `labels:` and `propertyTypes:` (both optional)
- `adding:` works the same way: can add both `labels:` and `propertyTypes:` to existing sets
- Abbreviated syntax `- nodeType: Person` is equivalent to `- nodeType: { typeLabel: Person }`
- TI sub-arrays can contain any mix of abbreviated and full syntax
- Bare elements and TI sub-arrays can be freely intermixed

**Default 0-Level Behavior - SIMPLIFIED**:
When no TI wrapper is specified around a sub-array, elements are semantically equivalent to `exactlyOfConcrete`. This provides clear default behavior with no ambiguity.

## Default 0-Level Behavior: Semantic Equivalence to exactlyOfConcrete

**CRITICAL DESIGN DECISION**: When no TI wrapper is specified, the behavior is **semantically equivalent** to `exactlyOfConcrete`, not merely "implicit" or "default".

**What This Means**:
- `nodeTypes: [{ typeLabel: Person }]` is functionally identical to `exactlyOfConcrete: { nodeTypes: [{ typeLabel: Person }] }`
- The system processes both forms with identical semantics
- No ambiguity exists about the interpretation of bare (0-level) types
- The default provides concrete, instantiable type matching behavior

**Implementation**:
- Schema validation treats both forms as valid
- Canonicalization may normalize bare forms to explicit `exactlyOfConcrete` wrappers
- Runtime behavior is identical between bare and explicitly wrapped forms
- Documentation clearly states the semantic equivalence

**Rationale**:
- Eliminates confusion about "what does bare mean?"
- Provides sensible default behavior (concrete, exact matching)
- Maintains backward compatibility with existing schemas
- Simplifies mental model: bare = exactlyOfConcrete

### Three TI Locations - MAJOR SIMPLIFICATION

The dramatically simplified location taxonomy - TI only applies to sub-arrays:

| # | Location Name | Description | Current Status | Fix Required |
|---|---------------|-------------|----------------|--------------|
| 1 | **ELIMINATED** | graphType TI → No TI at graphType level | N/A | N/A |
| 2 | **ELIMINATED** | nodeTypes collection TI → No TI at collection level | N/A | N/A |
| 3 | **ELIMINATED** | edgeTypes collection TI → No TI at collection level | N/A | N/A |
| 4 | `nodeTypeSubArrayInterpretation` | TI wraps sub-arrays within nodeTypes collection | ✗ WRONG | Fix pattern |
| 5 | `edgeTypeSubArrayInterpretation` | TI wraps sub-arrays within edgeTypes collection | ✗ WRONG | Fix pattern |
| 7 | `edgeTypeEndpointNodeTypeInterpretation` | TI wraps endpoint references | ✓ CORRECT | None - already working |

**Phase 2 Scope - MAJOR SIMPLIFICATION**: This refactoring fixes **2 broken locations** (4-5). Location 7 is already working. Locations 1-3 are **ELIMINATED** entirely.

**Key Insight**: TI complexity is dramatically reduced by eliminating graphType-level and collection-level TI. TI **ONLY** applies to sub-arrays within collections and endpoint references.

**Key Discovery**: Location 1 (GraphSchemaContent) does NOT currently support TI wrappers around `graphType`. It only allows ONE bare `graphType` property. We need to add `patternProperties` to enable TI wrappers.

**CRITICAL CORRECTION**: GraphType's `patternProperties` pattern is WRONG and violates our core design principle. The correct reference pattern is the explicit properties with oneOf approach used in Phases A-D (Locations 6-8). We must ELIMINATE all pattern properties and use explicit properties exclusively.

## Design Solution

### Core Pattern: Explicit Properties for Single-Level TI

**Design Decision**: Use explicit properties for each TI keyword in a flat, single-level structure.

**Rationale**:
- **Simplicity**: Single-level structure eliminates complex nesting patterns
- **Clarity**: Each TI form has clear, unambiguous semantics
- **Sibling support**: Allows multiple TI wrappers with different forms at the same level
- **IDE support**: Better autocomplete and validation with explicit properties
- **Consistency**: Same pattern applies to all locations

**Pattern for Sibling TI Wrappers** (e.g., at GraphType level):

```json
{
  "type": "object",
  "properties": {
    "nodeTypes": {
      "type": "array",
      "items": {"$ref": "#/$defs/NodeType"}
    },
    "edgeTypes": {
      "type": "array", 
      "items": {"$ref": "#/$defs/EdgeType"}
    },
    "exactlyOfConcrete": {
      "type": "object",
      "properties": {
        "nodeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"}
        },
        "edgeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"}
        }
      }
    },
    "subtypesOfConcrete": {
      "type": "object",
      "properties": {
        "nodeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"}
        },
        "edgeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"}
        }
      }
    },
    "subtypesOfAbstract": {
      "type": "object",
      "properties": {
        "nodeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/NodeType"}
        },
        "edgeTypes": {
          "type": "array",
          "items": {"$ref": "#/$defs/EdgeType"}
        }
      }
    },
    "concrete": {
      "type": "object",
      "description": "Synonym for exactlyOfConcrete",
      "properties": {
        "nodeTypes": {"type": "array", "items": {"$ref": "#/$defs/NodeType"}},
        "edgeTypes": {"type": "array", "items": {"$ref": "#/$defs/EdgeType"}}
      }
    },
    "subtypesOf": {
      "type": "object", 
      "description": "Synonym for subtypesOfConcrete",
      "properties": {
        "nodeTypes": {"type": "array", "items": {"$ref": "#/$defs/NodeType"}},
        "edgeTypes": {"type": "array", "items": {"$ref": "#/$defs/EdgeType"}}
      }
    },
    "properSubtypesOf": {
      "type": "object",
      "description": "Synonym for subtypesOfAbstract", 
      "properties": {
        "nodeTypes": {"type": "array", "items": {"$ref": "#/$defs/NodeType"}},
        "edgeTypes": {"type": "array", "items": {"$ref": "#/$defs/EdgeType"}}
      }
    },
    "abstract": {
      "type": "object",
      "description": "Synonym for subtypesOfAbstract", 
      "properties": {
        "nodeTypes": {"type": "array", "items": {"$ref": "#/$defs/NodeType"}},
        "edgeTypes": {"type": "array", "items": {"$ref": "#/$defs/EdgeType"}}
      }
    }
  }
}
```

**Pattern for Single TI Wrapper** (e.g., around `graphType` in GraphSchemaContent):

Use `oneOf` to allow exactly one option:

```json
{
  "oneOf": [
    {
      "properties": {
        "graphType": {"$ref": "#/$defs/GraphType"}
      }
    },
    {
      "properties": {
        "concrete": {
          "type": "object",
          "properties": {
            "graphType": {"$ref": "#/$defs/GraphType"}
          }
        }
      }
    },
    {
      "properties": {
        "abstract": {
          "type": "object",
          "properties": {
            "graphType": {"$ref": "#/$defs/GraphType"}
          }
        }
      }
    }
  ]
}
```

**Supported TI Levels**:
- **0-level**: Bare properties (e.g., `nodeTypes:`, `edgeTypes:`) - implicit `exactlyOfConcrete`
- **1-level**: Single TI wrappers using primary forms (`exactlyOfConcrete:`, `subtypesOfConcrete:`, `subtypesOfAbstract:`)
- **1-level**: Single TI wrappers using synonyms (`concrete:`, `subtypesOf:`, `properSubtypesOf:`, `abstract:`, `exactlyOf:`)

### Key Principles

1. **Single-Level Structure**: TI wrappers are single keywords with no nesting
2. **Wrapper Before Content**: TI wrappers must appear at the same level as content properties  
3. **Array-Only Organization**: All types must be contained in arrays, no freestanding types
4. **No TI Nesting**: TI wrappers cannot contain other TI wrappers at any level
5. **Pattern Consistency**: Same single-level structure at all locations
6. **Sibling Support**: Different TI forms can be siblings using explicit properties
7. **Canonicalization**: Synonyms are automatically mapped to primary forms

## Component Design

### Schema Modifications (Phase 2 Scope: 2 Locations)

Phase 2 fixes **2 broken locations** (4-5) and **eliminates 3 locations** (1-3) entirely. Location 7 (endpoint TI) is already working from previous implementation phases.

**CRITICAL: Pattern Properties Violate Design Principle**: GraphType's `patternProperties` implementation (lines 433-800) violates our core design principle and must be eliminated. The correct reference pattern is the explicit properties with oneOf approach from Phases A-D (Locations 6-8).

#### Location 1: ELIMINATED - graphTypeInterpretation
**Status**: **COMPLETELY ELIMINATED** - No TI wrappers allowed at graphType level  
**Rationale**: Simplifies system by removing graphType-level TI complexity  
**Implementation**: Remove any existing graphType TI support from schema  
**Semantics**: graphType contains only bare collections with no TI wrappers  
**Phase 2 Task**: **ELIMINATE all graphType TI support**

#### Location 2: ELIMINATED - nodeTypesInterpretation  
**Status**: **COMPLETELY ELIMINATED** - No TI wrappers allowed at collection level  
**Rationale**: Simplifies system by removing collection-level TI complexity  
**Implementation**: Remove any existing collection-level TI support from schema  
**Semantics**: nodeTypes collection contains only array elements and sub-arrays  
**Phase 2 Task**: **ELIMINATE all collection-level TI support**

#### Location 3: ELIMINATED - edgeTypesInterpretation
**Status**: **COMPLETELY ELIMINATED** - No TI wrappers allowed at collection level  
**Rationale**: Simplifies system by removing collection-level TI complexity  
**Implementation**: Remove any existing collection-level TI support from schema  
**Semantics**: edgeTypes collection contains only array elements and sub-arrays  
**Phase 2 Task**: **ELIMINATE all collection-level TI support**

#### Location 4: nodeTypeSubArrayInterpretation
**Current**: TI wrappers in wrong order (inside content instead of outside)  
**Target**: Support TI wrappers around sub-arrays within `nodeTypes` collection  
**Change**: Fix TI wrapper ordering - TI keywords must wrap sub-arrays, not be inside them  
**Schema Definition**: NodeTypeItem allows bare types OR TI-wrapped sub-arrays  
**Semantics**: Partitions the nodeTypes array into sub-arrays, each with its own TI  
**Example**: `nodeTypes: [{ nodeType: { typeLabel: Person } }, abstract: [{ nodeType: { typeLabel: Entity } }]]`  
**Phase 2 Task**: Fix TI wrapper ordering for sub-arrays

#### Location 5: edgeTypeSubArrayInterpretation  
**Current**: TI wrappers in wrong order (inside content instead of outside)  
**Target**: Support TI wrappers around sub-arrays within `edgeTypes` collection  
**Change**: Fix TI wrapper ordering - TI keywords must wrap sub-arrays, not be inside them  
**Schema Definition**: EdgeTypeItem allows bare types OR TI-wrapped sub-arrays  
**Semantics**: Partitions the edgeTypes array into sub-arrays, each with its own TI  
**Example**: `edgeTypes: [{ edgeType: { via: { typeLabel: KNOWS } } }, concrete: [{ edgeType: { via: { typeLabel: WORKS_FOR } } }]]`  
**Phase 2 Task**: Fix TI wrapper ordering for sub-arrays

#### Location 6: ELIMINATED - Single NodeType Interpretation
**Status**: **ELIMINATED** - Single nodeTypes are replaced by singleton subsequences within arrays  
**Rationale**: Individual nodeType TI is a special case of Location 4 (array subsequence TI)  
**Implementation**: Use singleton array subsequence: `exactlyOfConcrete: [{ typeLabel: Person }]`  
**Phase 2 Task**: No separate implementation needed - covered by Location 4

#### Location 7: edgeTypeEndpointNodeTypeInterpretation (Renumbered from Location 9)
**Current**: Already working from previous phases  
**Target**: No changes needed  
**Change**: None - this location is already correctly implemented  
**Semantics**: Wraps endpoint node type references within edge types  
**Phase 2 Task**: None - already working

### Edge Label Container Structure (E02 Integration)

**Critical Prerequisite**: Before implementing TI wrappers at Locations 3, 5, and 7, edge label containers must be corrected.

**Current Issue**: Edge label containers (`via:`, `arc:`) are incorrectly defined as polymorphic (string OR object).

**Correct Structure**: Edge label containers are ALWAYS objects with `typeLabel:` as required child property.

**Pattern 1 - Simple Edge (No Properties)**:
```yaml
via:
  typeLabel: KNOWS  # Required child of via
```

**Pattern 2 - Edge with Properties**:
```yaml
via:
  typeLabel: KNOWS  # Required child
  implies:          # Sibling to typeLabel
    propertyTypes:
      - name: since
        valueType: INTEGER
```

**Pattern 3 - Edge with Subtyping**:
```yaml
via:
  typeLabel: KNOWS
  extends: RELATIONSHIP  # Sibling to typeLabel
  adding:                # Sibling to extends
    propertyTypes:
      - name: since
        valueType: INTEGER
```

**Schema Changes Required**:
1. Redefine `via:` and `arc:` as ALWAYS objects (not oneOf string/object)
2. Make `typeLabel:` a REQUIRED child property
3. Remove `typeLabel:` from synonym group (it's now a child property only)
4. Move `implies:`, `extends:`, `adding:` to be children of edge label container

**Rationale**: This makes edge label containers consistent with `nodeType` pattern (always an object with `typeLabel:` child).

### Test File Updates

Test YAML files currently use wrong-order syntax because they were written for the broken schema. After fixing the schema, these files must be updated:

**Files Requiring Updates**:
- `src/grasch/examples/test-phase-e-location-2*.yaml`
- `src/grasch/examples/test-phase-e-location-3*.yaml`
- `src/grasch/examples/test-phase-e-locations-2-3*.yaml`
- `src/grasch/examples/test-phase-e-locations-4-5*.yaml`
- Any other files using array-level TI wrappers

**Update Pattern**:
- Move TI wrappers from inside content to outside content
- Preserve semantic meaning
- Maintain test coverage

### Sibling TI Wrapper Support - Schema Fix Required

**THE CRITICAL FIX**: The schema must be restructured to use explicit properties exclusively for all TI wrappers. This requires:

1. **Replace all `patternProperties`** with explicit properties for each TI keyword
2. **Use explicit sibling properties** to allow multiple TI wrappers with different facets
3. **Use `oneOf` constraints** where only one TI wrapper is allowed (single-wrapper locations)
4. **Test extensively** with positive and negative test cases to ensure sibling behavior works correctly

The schema will support multiple sibling TI wrappers with different interpretation facets at multiple levels:

**Location 1 (graphTypeInterpretation) - Siblings at GraphType Level**:
```yaml
graphType:
  nodeTypes:        # Bare nodeTypes (Location 2)
    - typeLabel: Person
  exactlyOf:        # TI-wrapped nodeTypes (sibling to bare)
    concrete:
      nodeTypes:
        - typeLabel: Company
  edgeTypes:        # Bare edgeTypes (Location 3)
    - typeLabel: WORKS_FOR
  subtypesOf:       # TI-wrapped edgeTypes (sibling to bare)
    abstract:
      edgeTypes:
        - typeLabel: RELATIONSHIP
```

**Locations 2-3 (nodeTypesInterpretation/edgeTypesInterpretation) - Multiple Array Interpretations as Siblings**:
```yaml
nodeTypes:          # Bare nodeTypes array
  - typeLabel: Person
exactlyOf:          # TI-wrapped nodeTypes array (sibling)
  concrete:
    nodeTypes:
      - typeLabel: Company
subtypesOf:         # Another TI-wrapped nodeTypes array (sibling)
  abstract:
    nodeTypes:
      - typeLabel: Entity
```

**Locations 4-5 (nodeTypeArrayInterpretation/edgeTypeArrayInterpretation) - Array Subsequences as Siblings**:
```yaml
nodeTypes:          # Array divided into subsequences
  - typeLabel: Person                    # Bare array element
  - exactlyOf:                          # Array subsequence 1 (TI-wrapped)
      concrete:
        - typeLabel: Company
        - typeLabel: Organization
  - subtypesOf:                         # Array subsequence 2 (TI-wrapped)
      abstract:
        - typeLabel: Entity
        - typeLabel: Thing
```

**Invalid (YAML Constraint)**:
```yaml
nodeTypes:
  - typeLabel: Person
exactlyOf:          # Same interpretation facet
  concrete:
    nodeTypes:
      - typeLabel: Company
exactlyOf:          # ERROR: Duplicate YAML key
  abstract:
    nodeTypes:
      - typeLabel: Entity
```

## Data Models

### Schema Structure

```
GraphSchema
├── properties
│   ├── nodeTypes: array
│   └── edgeTypes: array
└── patternProperties
    └── ^(exactlyOf|subtypesOf|properSubtypesOf)$
        └── oneOf
            ├── properties (1-level shorthand)
            │   ├── nodeTypes: array
            │   └── edgeTypes: array
            └── patternProperties (2-level explicit)
                └── ^(abstract|concrete|final|sealed)$
                    └── properties
                        ├── nodeTypes: array
                        └── edgeTypes: array
```

### Validation Flow

1. **Pre-Canonical Validation**: YAML file validates against schema (with TI wrappers)
2. **Canonicalization**: Preprocessor normalizes to 2-level explicit form
3. **Canonical Validation**: Normalized form validates against same schema
4. **Semantic Validation**: Business rules applied to canonical form

## Error Handling

### Schema Validation Errors

**Wrong-Order Syntax**:
- Error: "Additional properties not allowed"
- Cause: TI wrapper inside content instead of outside
- Fix: Move TI wrapper to correct level

**Duplicate Interpretation Facets**:
- Error: "Duplicate key in YAML"
- Cause: Same interpretation facet appears twice
- Fix: Use different interpretation facets or nest under one

**Missing Content**:
- Error: "Required property missing"
- Cause: TI wrapper without content property
- Fix: Add content property inside TI wrapper

### Test Validation Strategy

1. **Expect Failures**: After schema fix, wrong-syntax tests will fail (this is correct)
2. **Identify Failures**: Run validation to find which files need updates
3. **Update Syntax**: Fix YAML files to use correct TI placement
4. **Re-validate**: Confirm all tests pass with corrected syntax
5. **Regression Check**: Verify Phases A-D still work (should be unchanged)

## Testing Strategy

### Unit Tests

**Schema Structure Tests**:
- Verify `patternProperties` at correct level
- Verify content properties inside wrappers
- Verify 0/1/2-level syntax support

**Location-Specific Tests**:
- Test each of 8 locations independently
- Test 0-level, 1-level, 2-level at each location
- Test sibling patterns at each location

### Integration Tests

**Cross-Location Tests**:
- Test TI at multiple locations simultaneously
- Test partition blocks within collections (Locations 4-5)
- Test mixed bare and wrapped syntax at all levels

**Sibling Behavior Tests**:
- Test multiple different interpretation facets as siblings
- Test YAML duplicate key prevention
- Test nested concreteness facets

### Validation Tests

**Positive Tests** (should pass):
- `test-siblings-graphtype-level.yaml`
- `test-siblings-array-level.yaml`
- `test-siblings-mixed.yaml`
- All Phase A-D test files (unchanged)

**Negative Tests** (should fail):
- `test-siblings-duplicate-nodetypes-INVALID.yaml`
- `test-siblings-duplicate-interpretation-INVALID.yaml`

## Implementation Phases

### Phase 1: Schema Analysis (1 hour)
1. Read Location 1 (GraphType) pattern in detail
2. Identify exact line numbers for Locations 2-7
3. Document current vs. target structure for each location
4. Create backup of original schema

### Phase 2: Schema Fixes (3-4 hours)
1. Fix Location 2 (NodeTypesProperty)
2. Fix Location 3 (EdgeTypesProperty)
3. Fix Location 4 (NodeTypeArray - array-level partition blocks)
4. Fix Location 5 (EdgeTypeArray - array-level partition blocks)
5. Fix Location 6 (Individual NodeType)
6. Fix Location 7 (EdgeType Content)
7. Test after each fix

### Phase 3: Test File Updates (2-3 hours)
1. Run validation to identify failing files
2. Update Phase E test files to correct syntax
3. Create sibling behavior test files
4. Validate all updated files

### Phase 4: Validation & Documentation (1-2 hours)
1. Run comprehensive validation suite
2. Verify Phases A-D still pass
3. Document changes and results
4. Create completion summary

## Success Criteria

1. ✓ Locations 1-3 completely eliminated (no graphType or collection-level TI)
2. ✓ Locations 4-5 support TI wrappers around sub-arrays with correct ordering
3. ✓ Location 7 (endpoint TI) continues working (no changes needed)
4. ✓ TI wrappers appear BEFORE content at remaining locations
5. ✓ Default exactlyOfConcrete semantics for bare elements
6. ✓ All test files validate with simplified syntax
7. ✓ No regressions in existing functionality

## Risks & Mitigation

**Risk**: Breaking existing valid YAML files  
**Mitigation**: Files using correct syntax will continue to work; only wrong-syntax files need updates

**Risk**: Introducing new validation errors  
**Mitigation**: Test incrementally after each location fix; maintain backup

**Risk**: Sibling behavior not working as expected  
**Mitigation**: Comprehensive sibling tests; validate against YAML spec

**Risk**: Preprocessor incompatibility  
**Mitigation**: Preprocessor already handles correct syntax; no changes needed

## Type Finalization (Future Work)

**Status**: Out of scope for this specification - to be addressed in a separate phase/stage.

Type finalization is a **separate system** from type interpretation. While type interpretation controls how types are validated and instantiated (exact match vs. subtype matching), type finalization controls inheritance and extension behavior.

### Finalization Keywords

- `final:` - Prevents further subtyping (no types can extend this type)
- `sealed:` - Allows subtyping but restricts where subtypes can be defined

### Relationship to Type Interpretation

Type finalization and type interpretation are **orthogonal concerns**:
- Type interpretation: Controls matching semantics (exact, subtype, proper subtype)
- Type finalization: Controls inheritance/extension permissions

They can be combined:
```yaml
# Example: Abstract type that is also final (can be matched by subtypes, but no new subtypes allowed)
final:
  abstract:
    nodeTypes:
      - typeLabel: BaseEntity
```

### Implementation Plan

Type finalization will be addressed in **Phase F** (or a dedicated stage) after type interpretations (Phases A-E) are complete. This will include:
1. Schema changes to support `final:` and `sealed:` keywords
2. Validation rules for finalization constraints
3. Test files demonstrating finalization behavior
4. Documentation updates

## Relationship to Existing Work

This design document is part of the broader Type Interpretation implementation effort documented in:

**Parent Specifications**:
- `.kiro/specs/type-interpretation-wrappers/` - Original TI wrapper system spec
- `.kiro/specs/type-interpretation-flexibility/` - TI flexibility requirements

**Authoritative Design Documents**:
- `TI-SCHEMA-ORDERING-FIX-DESIGN.md` - Root-level design (this spec implements it)
- `LEX-2026.0.3.2-INTERPRETATION-DESCRIPTORS.md` - Official TI specification
- `TI-IMPLEMENTATION-ROADMAP.md` - Overall TI implementation plan

**Implementation Context**:
- `PHASES-A-D-COMPLETE.md` - Completed work (Locations 6, 7, 8 working)
- `PHASE-E-IMPLEMENTATION-PLAN.md` - Array-level TI (what we're fixing)
- `MORNING-CHECKPOINT-TI-ORDERING-FIX.md` - Ready-to-execute checkpoint

**Related Specs**:
- `.kiro/specs/type-interpretation-wrappers/design.md` - Original TI design
- `.kiro/specs/type-interpretation-wrappers/tasks.md` - Original TI tasks

This refactoring completes the TI implementation by fixing the 6 broken locations identified during Phases A-D implementation.

## Design Note: Double Wrapping and TI Override (Future - Canonicalization Phase)

**Context**: At every location where TI wrappers are permitted, the schema will allow "double wrapping" where TI wrappers can be nested.

**Example of Double Wrapping**:
```yaml
subtypesOf:
  abstract:
    exactlyOf:
      concrete:
        nodeType:
          typeLabel: Person
```

**Semantics**:
- When double wrapping occurs, the **outer TI wrapper overrides the inner TI wrapper**
- In the example above, `subtypesOf: abstract:` overrides `exactlyOf: concrete:`
- The effective interpretation is `subtypesOf` with `abstract` concreteness

**Purpose**:
- This supports **importation of definitions that include TI wrappers**
- When importing a type definition that already has a TI wrapper, you can wrap it with a different TI to override the imported interpretation
- Example: Import a `concrete` type but use it as `abstract` in your schema

**Canonicalization**:
- This is **not normal behavior** and would never appear in a canonicalized YAML document
- During canonicalization, the inner TI wrapper would be removed, leaving only the outer (effective) wrapper
- Canonical form: `subtypesOf: { abstract: { nodeType: { typeLabel: Person } } }`

**Implementation Status**:
- ⏸️ **Deferred to Phase H (Canonicalization)**
- No implementation required at this stage (Phase E)
- The schema will naturally permit this structure (it won't explicitly prevent nested TI wrappers)
- Canonicalization logic will handle the override semantics and simplification

**Applies To**:
- All locations where TI wrappers are permitted (Locations 1-9)
- Both single TI wrapper locations (1, 6, 7, 8, 9) and sibling TI wrapper locations (2, 3, 4, 5)
