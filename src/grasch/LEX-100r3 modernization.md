# LEX-100r3 Modernization Guide

## Purpose
Update the LEX-100r3 specification document to accurately reflect the LEX:2026.0.3.2 implementation, JSON Schema, examples, and Python API that have been developed.

## Executive Summary
The implementation has run ahead of the specification. This guide identifies where LEX-100r3 needs to be updated to match what we've actually built and validated in LEX:2026.0.3.2.

## Recent Updates (0.3.2)

### New Edge Type Syntax
Complete redesign of edge type syntax for better readability and expressiveness:

**Directed Edges:**
```yaml
- edgeType:
    directed:
      from: Person
      via: KNOWS
      to: Person
    implies:
      propertyTypes: [...]
```

**Undirected Edges:**
```yaml
- edgeType:
    undirected:
      between: Person
      via: COLLABORATES_WITH
      and: Person
```

**Key Features:**
- `via:` replaces separate `typeLabel:` (edge label is part of direction spec)
- `arc:` as synonym for `via:`
- Multiple endpoint synonym sets: `from:`/`to:`, `tail:`/`head:`, `src:`/`dst:`/`dest:`
- `SAME`/`SELF` keywords for self-loops
- `abstract:` and `abstractSupertype:` for abstract edge types and endpoints
- Inline node type definitions for edge-only types
- `implies:` optional when no properties/labels defined

See: `lex-2026.0.3.2-edge-type-syntax-examples.yaml`

### Node Type Enhancements
- `supertypes:` accepts both string (singleton) and array forms
- `abstract:` and `abstractSupertype:` as synonyms
- `extends:` and `supertypes:` as synonyms
- Isolated node types (never referenced by edges)
- Edge-only node types (inline definitions)
- **Type finalization**: `final:` prevents subtyping
- **Sealed hierarchies**: `sealed:` closes a type hierarchy
- Validation rules for abstract interpretations with final/sealed types

See: `lex-2026.0.3.2-node-type-syntax-examples.yaml`

### Type Finalization and Sealing

**Final Types:**
```yaml
- final:
    nodeType:
      typeLabel: Company
      extends: Organisation
```
- Cannot be subtyped
- Marks a type as a leaf in the hierarchy

**Sealed Hierarchies:**
```yaml
- sealed:
    nodeTypes:
    - abstract:
        nodeType:
          typeLabel: Place
    - nodeType:
        typeLabel: City
        extends: Place
```
- Closed set of types
- No external subtypes allowed
- Equivalent to marking all leaves as final

**Validation Rules:**
1. `sealed:` ≡ `final:` on all leaf subtypes
2. `abstract:` interpretation + all `final:` types = INVALID
3. `abstract:` interpretation + all types in `sealed:` = INVALID
4. Rationale: Abstract interpretation requires proper subtypes, but final/sealed types have none

### API Enhancements
- All edge endpoint accessors as synonyms (no canonical form)
- `getTypeLabel()` returns `Optional[str]` for singleton identifiers
- Support for isolated vs edge-only node type distinction

See: `LEX-2026.0.3.2-API-DESIGN.md`

## What We've Actually Implemented (LEX:2026.0.3.1)

### ✅ Implemented Features Beyond LEX-100r3

1. **Hierarchical Type Interpretations** (Not in LEX-100r3)
   - `allowSubtypesOf` with nested `abstractSupertypes` structure
   - Self-recursive type interpretation hierarchies
   - Supports SNB-style Message/Comment/Post patterns
   - See: `LEX-2026.0.3.1-INTERPRETATION-DESCRIPTORS.md`

2. **Enhanced Graph Type Characteristics** (Partially in LEX-100r3)
   - ✅ Implemented: All min/max labels and property types
   - ✅ Implemented: Preferred names (graph/node/edge)
   - ✅ Implemented: Type interpretation modes
   - LEX-100r3 has these but needs better organization

3. **Advanced Import Patterns** (Basic in LEX-100r3)
   - ✅ Implemented: Import entire type collections
   - ✅ Implemented: Import individual types
   - ✅ Implemented: Import property type sets
   - ✅ Implemented: Nested imports in hierarchies
   - See: `LEX-2026.0.3.1-IMPORT-PATTERNS.md`

4. **Comprehensive Python API** (Not in LEX-100r3)
   - ✅ Implemented: Complete interface definitions
   - ✅ Implemented: Concrete implementations
   - ✅ Implemented: Fluent builder pattern
   - ✅ Implemented: Full mypy strict type checking
   - See: `LEX-2026.0.3.2-API-DESIGN.md`

5. **Pathname and Identification System** (Basic in LEX-100r3)
   - ✅ Implemented: LQON (Locally Qualified Object Names)
   - ✅ Implemented: GQON (Globally Qualified Object Names)
   - ✅ Implemented: File references with `$ref` syntax
   - ✅ Implemented: Catalog tree navigation
   - See: `LEX-2026.0.3.1-PATHNAME-AND-IDENTIFICATION.md`

6. **Type Definition Syntax Examples** (Not in LEX-100r3)
   - ✅ Implemented: Comprehensive syntax examples
   - ✅ Implemented: All type identification methods
   - ✅ Implemented: Subtyping patterns
   - See: `lex-2026.0.3.1-type-definition-syntax-examples.yaml`

## Where LEX-100r3 Needs Updates
### 1. Type Interpretation Structure (Major Gap)

**LEX-100r3 Says:**
```
– type interpretation: choice 
    exactlyOfThisType | anySubtypeOf | anyProperSubtypeOf
        default value = exactlyOfThisType
```

**What We Actually Implemented:**
```yaml
graphType:
  typeInterpretation: "exactlyOfThisType"  # Top-level default
  
  # Hierarchical structure with nested interpretations
  allowSubtypesOf:
    abstractSupertypes:
      nodeTypes:
        - nodeTypeIdentifier: {typeLabel: "Message"}
          abstract: true
      # Nested interpretation for concrete subtypes
      allowSubtypesOf:
        nodeTypes:
          - nodeTypeIdentifier: {typeLabel: "Comment"}
          - nodeTypeIdentifier: {typeLabel: "Post"}
```

**Required Spec Update:**
- Add section on hierarchical type interpretation structures
- Document `allowSubtypesOf` with `abstractSupertypes`
- Explain self-recursive nesting
- Reference `LEX-2026.0.3.1-INTERPRETATION-DESCRIPTORS.md`
### 2. Graph Type Characteristics (Needs Better Organization)

**LEX-100r3 Has:** All the characteristics but scattered in the text

**What We Actually Implemented:**
```json
{
  "GraphType": {
    "properties": {
      "graphPreferredName": {"enum": ["GRAPH", "PROPERTY GRAPH"]},
      "nodePreferredName": {"enum": ["NODE", "VERTEX"]},
      "edgePreferredName": {"enum": ["EDGE", "RELATIONSHIP"]},
      "nodeTypeMinimumLabels": {"type": "integer", "default": 1},
      "nodeTypeMaximumLabels": {"type": "integer"},
      "nodeTypeMinimumPropertyTypes": {"type": "integer", "default": 0},
      "nodeTypeMaximumPropertyTypes": {"type": "integer"},
      "edgeTypeMinimumLabels": {"type": "integer", "default": 1},
      "edgeTypeMaximumLabels": {"type": "integer"},
      "edgeTypeMinimumPropertyTypes": {"type": "integer", "default": 0},
      "edgeTypeMaximumPropertyTypes": {"type": "integer"},
      "typeInterpretation": {"enum": ["exactlyOfThisType", "anySubtypeOf", "anyProperSubtypeOf"]},
      "nodeTypes": [...],
      "edgeTypes": [...]
    }
  }
}
```

**Required Spec Update:**
- Consolidate all GraphType characteristics in one clear section
- Show complete descriptor hierarchy
- Match JSON Schema structure exactly
- Remove scattered references throughout document
### 3. Import Syntax (Needs Expansion)

**LEX-100r3 Says:**
```
– descriptor : importable
// means $ref ('<file path>') can be used
```

**What We Actually Implemented:**
```yaml
# Import entire type collection
graphType:
  nodeTypes:
    import: "common-node-types.yaml"

# Import individual types within array
graphType:
  nodeTypes:
    - nodeTypeIdentifier: {typeLabel: "Person"}
      propertyTypes: [...]
    - import: "additional-node-type.yaml"

# Import property types
nodeTypes:
  - nodeTypeIdentifier: {typeLabel: "Person"}
    propertyTypes:
      import: "person-properties.yaml"

# Nested imports in hierarchies
allowSubtypesOf:
  abstractSupertypes:
    nodeTypes:
      import: "abstract-types.yaml"
```

**Required Spec Update:**
- Add comprehensive import patterns section
- Document all import locations (types, properties, hierarchies)
- Show concrete YAML examples
- Reference `LEX-2026.0.3.1-IMPORT-PATTERNS.md`
### 4. Node/Edge Type Structure (Needs Clarification)

**LEX-100r3 Has:** Complex choice between identified/anonymous types

**What We Actually Use:**
```yaml
# Preferred: Type label (used in all examples)
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Person"
    labels: ["Person"]
    propertyTypes: [...]

# Supported but not used: Type identifying labels
nodeTypes:
  - nodeTypeIdentifier:
      typeIdentifyingLabels: ["Person", "Entity"]
    labels: ["Person", "Entity", "Active"]
    propertyTypes: [...]

# Supported but not used: Anonymous with index
nodeTypes:
  - nodeTypeIdentifier:
      nodeTypeIndex: 0
    labels: ["Person"]
    propertyTypes: [...]
```

**Required Spec Update:**
- Clarify that typeLabel is the preferred method
- Show all three identification methods clearly
- Explain when each method is appropriate
- Update examples to primarily use typeLabel
- Reference `lex-2026.0.3.1-type-definition-syntax-examples.yaml`
### 5. Subtyping with `supertypes` (Missing from LEX-100r3)

**LEX-100r3 Has:** Vague mention of "implies" pulling in labels/properties

**What We Actually Implemented:**
```yaml
nodeTypes:
  # Base type
  - nodeTypeIdentifier: {typeLabel: "Entity"}
    labels: ["Entity"]
    propertyTypes:
      - name: "id"
        valueType: {name: "STRING"}

  # Derived type
  - nodeTypeIdentifier: {typeLabel: "Person"}
    labels: ["Person"]
    supertypes: ["Entity"]  # Inherits Entity's properties
    propertyTypes:
      - name: "name"
        valueType: {name: "STRING"}
```

**Required Spec Update:**
- Add explicit `supertypes` descriptor
- Explain inheritance semantics (Java interface mixin style)
- Document that supertypes pull in labels and property types
- Show examples with inheritance chains
- Reference `AMENDMENT-subtyping-example.md`
### 6. Extension Interpretation (Missing from LEX-100r3)

**LEX-100r3 Has:** Brief mention, no details

**What We Actually Implemented:**
```yaml
nodeTypes:
  - nodeTypeIdentifier: {typeLabel: "Person"}
    labels: ["Person"]
    extensionInterpretation:
      open: true  # Allow undefined subtypes
    propertyTypes:
      - name: "id"
        valueType: {name: "STRING"}
    # Separate extension interpretation for properties
    propertyTypesExtensionInterpretation:
      closed: true  # Only defined properties allowed
```

**Required Spec Update:**
- Add `extensionInterpretation` descriptor
- Explain open vs closed semantics
- Document separate control for labels vs properties
- Show GQL:2027 default (closed: true)
- Add examples showing both modes
### 7. Python API (Not in LEX-100r3 at all)

**LEX-100r3 Has:** Nothing about programmatic API

**What We Actually Implemented:**
- Complete interface definitions for all catalog objects
- Concrete implementation classes
- Fluent builder pattern for easy construction
- Full mypy strict type checking
- Hierarchical type structure support (NodeTypes, EdgeTypes, TypeInterpretation)

**Required Spec Update:**
- Add new section on "Programmatic API"
- Reference `LEX-2026.0.3.2-API-DESIGN.md`
- Document interface/implementation pattern
- Show builder usage examples
- Explain relationship to YAML/JSON representations

### 8. Catalog File References (Partially in LEX-100r3)

**LEX-100r3 Has:** Brief mention of `file` descriptor

**What We Actually Implemented:**
```yaml
catalog:
  IRI: "https://example.com/schemas/"
  directories:
    - name: "benchmarks"
      graphSchemas:
        - name: "snb"
          qualifiedName: "https://example.com/schemas/|/benchmarks/snb"
          file: "$ref('schemas/snb-schema.yaml')"
```

**Required Spec Update:**
- Expand file reference section
- Show complete catalog examples
- Explain IRI vs file path separation
- Document when to use file references
- Reference `example-catalog-lex-2026.0.3.1.yaml`

## Recommended Spec Modernization Approach
### Step 1: Reorganize Abstract Syntax Sections
**Priority: HIGH**

Current LEX-100r3 has scattered information. Reorganize into clear sections:

1. **Catalog Structure** - Consolidate all catalog/directory/LQON/GQON material
2. **Value Type Systems** - Keep as is, already good
3. **Graph Schema Structure** - Reorganize to match JSON Schema
4. **Graph Type Characteristics** - New consolidated section
5. **Type Interpretation Hierarchies** - New major section
6. **Node and Edge Types** - Clarify identification methods
7. **Subtyping and Inheritance** - New section
8. **Import Patterns** - Expand significantly
9. **Extension Interpretation** - New section
10. **Constraints** - Keep but note incomplete
11. **Storage Schema** - Keep as placeholder
12. **Programmatic API** - New section

### Step 2: Add Missing Descriptor Definitions
**Priority: HIGH**

Add complete descriptor definitions for:
- `allowSubtypesOf` with `abstractSupertypes`
- `supertypes` array
- `extensionInterpretation` with open/closed
- `abstract` boolean flag
- All import patterns and locations

### Step 3: Update Examples Throughout
**Priority: MEDIUM**

Replace abstract examples with real YAML from:
- `finbench-lex-2026.0.3.1-schema.yaml`
- `snb-lex-2026.0.3.1-schema.yaml`
- `lex-2026.0.3.1-type-definition-syntax-examples.yaml`
- `example-catalog-lex-2026.0.3.1.yaml`

### Step 4: Cross-Reference Implementation Docs
**Priority: MEDIUM**

Add references throughout to:
- `LEX-2026.0.3.1-GUIDE.md` - Main implementation guide
- `LEX-2026.0.3.1-INTERPRETATION-DESCRIPTORS.md` - Type hierarchies
- `LEX-2026.0.3.1-IMPORT-PATTERNS.md` - Import syntax
- `LEX-2026.0.3.1-PATHNAME-AND-IDENTIFICATION.md` - Naming
- `LEX-2026.0.3.2-API-DESIGN.md` - Python API
- `AMENDMENT-subtyping-example.md` - Subtyping patterns
- `AMENDMENT-implies-structure.md` - Inheritance semantics

### Step 5: Align JSON Schema References
**Priority: HIGH**

Ensure spec text matches `lex-2026.0.3.1.schema.json` exactly:
- Property names must match
- Default values must match
- Enum values must match
- Required vs optional must match
- Structure/nesting must match
## Specific Text Changes Needed in LEX-100r3

### Section: "LEX Graph Schema abstract syntax"

**Current Text (LEX-100r3):**
```
A more complete view of a node type descriptor with type labels follows. 
This view allows the explicit definition of subtype relations in a way 
which resembles Java interface mixins.

    – graph type
        — node types <set> : importable 
            – node type            
                – identified node type
              – type identifier 
              – implies
                  – ? supertypes <set <type label>>
                  – ? labels <set <identifier>>
                  – ? property types <set <property type>>
```

**Should Be:**
```
Node types can declare supertypes for inheritance (Java interface mixin style):

    – node type
        – node type identifier : choice
            – type label <identifier>
            – type identifying labels <set <identifier>>
            – node type index <integer>
        – ? abstract <boolean> : default false
        – ? supertypes <set <type label>>
        – labels <set <identifier>> : minimum 1
        – ? property types <set <property type>>
        – ? extension interpretation
            – open <boolean> : default false
            – closed <boolean> : default true

When supertypes are specified, the type inherits all labels and property 
types from its supertypes. This enables type hierarchies like:
  Entity (abstract) → Person, Company
  Message (abstract) → Comment, Post

Subtype Relation Properties (Armstrong's Axioms):
  - Reflexive: Every type is a subtype of itself
  - Transitive: If A <: B and B <: C, then A <: C
  These properties ensure consistent type hierarchy semantics.

Edge Type Subtyping:
  An edge type S is a subtype of edge type T if:
  1. S's property types are a subtype of T's property types (structural)
  2. S's endpoint node types are subtypes of T's endpoint node types:
     - For DIRECTED edges: source <: source AND destination <: destination
     - For UNDIRECTED edges: endpoints match in either order
     - Self-loops (SAME endpoint) require special handling
  3. Direction must be compatible (DIRECTED <: DIRECTED, UNDIRECTED <: UNDIRECTED)
  
  Example:
    CLOSE_FRIEND(Person, Person) <: KNOWS(Person, Person)
    KNOWS(Employee, Employee) <: KNOWS(Person, Person)  // covariant endpoints
```

### Section: "Type Interpretation" (NEW SECTION NEEDED)

**Add After Graph Type Characteristics:**
```
Type Interpretation Hierarchies

LEX:2026.0.3 supports hierarchical type interpretation structures that 
enable abstract supertype patterns common in graph schemas.

Basic Type Interpretation:
    – graph type
        – type interpretation : choice
            – exactly of this type (default)
            – any subtype of
            – any proper subtype of

Hierarchical Type Interpretation:
    – graph type
        – type interpretation : default
        – allow subtypes of
            – abstract supertypes
                – node types <set>
                – edge types <set>
            – allow subtypes of (recursive)
                – node types <set>
                – edge types <set>

This structure supports patterns like:
- Abstract supertypes that cannot be instantiated
- Concrete subtypes that can be instantiated
- Multiple levels of nesting for complex hierarchies

Example: SNB Message Hierarchy
    allow subtypes of:
      abstract supertypes:
        node types:
          - type label: "Message"
            abstract: true
            property types: [id, content, creationDate]
      allow subtypes of:
        node types:
          - type label: "Comment"
            supertypes: ["Message"]
          - type label: "Post"
            supertypes: ["Message"]
```

### Section: "Import Patterns" (EXPAND EXISTING)

**Current Text:** Brief mention of `: importable` qualifier

**Should Be:**
```
Import and Modularization

LEX:2026.0.3 supports comprehensive import patterns using $ref syntax:

1. Import Entire Type Collections:
    node types:
      import: "common-node-types.yaml"

2. Import Individual Types:
    node types:
      - node type identifier: {type label: "Person"}
        property types: [...]
      - import: "additional-type.yaml"

3. Import Property Type Sets:
    node types:
      - node type identifier: {type label: "Person"}
        property types:
          import: "person-properties.yaml"

4. Import in Hierarchies:
    allow subtypes of:
      abstract supertypes:
        node types:
          import: "abstract-types.yaml"

5. Nested Imports:
    Files can import other files, creating a modular schema structure.

See LEX-2026.0.3.1-IMPORT-PATTERNS.md for complete patterns.
```

## Key Terminology Alignments

| LEX-100r3 Term | LEX:2026.0.3.1 Term | Notes |
|----------------|---------------------|-------|
| "implies" | "supertypes" | Clearer inheritance semantics |
| "type name label" | "typeLabel" | Matches JSON Schema property |
| "key label set" | "typeIdentifyingLabels" | Matches JSON Schema |
| "type index" | "nodeTypeIndex" / "edgeTypeIndex" | Separate for clarity |
| "extension interpretation" | "extensionInterpretation" | Matches JSON Schema |
| "finality" | (not implemented) | Future feature |

## Documentation Structure for Updated Spec

Proposed LEX-100r4 structure:

1. **Introduction** (keep as is)
2. **Specification Status** (update to r4)
3. **Concepts and Components** (keep)
4. **Descriptor Syntax** (keep)
5. **LEX Graph Catalog** (consolidate)
6. **LEX Value Type Systems** (keep)
7. **LEX Graph Schema** (reorganize)
   - 7.1 Schema Structure
   - 7.2 Graph Type Characteristics
   - 7.3 Type Interpretation Hierarchies (NEW)
   - 7.4 Node and Edge Types
   - 7.5 Subtyping and Inheritance (NEW)
   - 7.6 Property Types
   - 7.7 Extension Interpretation (NEW)
   - 7.8 Constraints
8. **Import and Modularization** (NEW major section)
9. **LEX Graph Instances** (keep)
10. **Programmatic API** (NEW major section)
11. **JSON Schema** (expand)
12. **Examples** (update with real YAML)
13. **Appendix A: Future Functionality** (keep)

## Timeline for Spec Update

- **Reorganization**: 1-2 days
- **New sections**: 2-3 days
- **Example updates**: 1 day
- **Cross-referencing**: 1 day
- **Review and polish**: 1 day

**Total**: 6-8 days for complete spec modernization