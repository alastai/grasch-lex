# Design Document: Type Interpretation Wrapper System

## Overview

The type interpretation wrapper system provides a flexible YAML syntax for controlling how element type references are validated in LEX-2026 schemas. The system uses wrapper keywords that surround type reference values to specify two independent semantic dimensions: subtype matching mode (variance) and concreteness (instantiability).

## Architecture

### Single Schema, Two Valid Forms

The LEX-2026 architecture uses **one JSON Schema** that validates both pre-canonical and canonical forms of YAML documents:

1. **Pre-Canonical Form**: The YAML syntax that schema authors write
   - Contains `import:` statements (validated structurally, not by content)
   - Uses convenience syntax: zero-level (bare), one-level, and two-level wrapper patterns
   - Uses implicit defaults and syntax sugar
   - Multiple files reference each other via imports

2. **Canonical Form**: The normalized representation after preprocessing
   - All imports resolved and merged into single document
   - All type interpretation wrappers normalized to explicit two-dimensional form
   - All defaults made explicit
   - All syntax sugar expanded to long forms
   - Ready for semantic validation and API consumption

### Data Flow

```
Pre-Canonical YAML (Multiple Files)
       ↓
JSON Schema Validation (structural)
  - Validates import: statements are well-formed
  - Validates pre-canonical syntax is valid
       ↓
Import Preprocessor (Canonicalization)
  - Import Resolution & Merging
  - Wrapper Normalization
  - Default Expansion
  - Syntax Sugar Expansion
       ↓
Canonical YAML (Single Document)
       ↓
JSON Schema Validation (structural + semantic)
  - Validates canonical syntax is valid
  - Validates all references are resolved
       ↓
Semantic Validator / API
```

### Canonicalization as Architectural Pattern

The import preprocessor performs canonicalization, transforming pre-canonical forms into canonical forms:

- **Import Resolution**: Multiple files with `import:` → Single merged document
- **Wrapper Normalization**: Multiple syntax forms → Canonical two-dimensional form
- **Default Value Expansion**: Implicit defaults → Explicit values
- **Syntax Sugar Expansion**: Convenient shorthands → Explicit long forms

**Key Principle**: The JSON Schema accepts both forms. Pre-canonical files are valid if they use correct syntax (even if imports point to non-existent files). Canonical files are valid if they use correct syntax AND all semantic constraints are satisfied.

### Terminology

- **Pre-Canonical**: The form schema authors write, with imports and convenience syntax
- **Canonical**: The normalized form after preprocessing, ready for semantic validation
- **NOT**: "pre-import" or "post-import" (these terms are deprecated)

Validation reports should state:
- "Pre-canonical validation: passed/failed"
- "Canonical validation: passed/failed"

### Analogy to Edge Type Endpoint Syntax

Type interpretation wrappers follow the same design principles as edge type endpoint specifications:

**Edge Type Endpoints:**
- **Directed**: Pre-canonical forms (`from:`/`to:`, `src:`/`dst:`, `source:`/`destination:`) canonicalize to `tail: arc: head:`
- **Undirected**: Pre-canonical form (`between:` and `and:`) canonicalizes to `between: via: and:`
- **Fixed order**: Keywords must appear in specific order (cannot say `to: from: arc:`)
- **Mutual exclusivity**: `directed:` edges use only directed keywords; `undirected:` edges use only undirected keywords

**Type Interpretation Wrappers:**
- **Pre-canonical forms**: Zero-level (bare), one-level (`abstract:`, `concrete:`, `properSubtypesOf:`)
- **Canonical form**: Two-level (`exactlyOf: concrete:` or `subtypesOf: abstract:`)
- **Fixed order**: Subtype matching mode (outermost) → concreteness (middle) → property (innermost)
- **No reordering**: Cannot say `concrete: exactlyOf: nodeType:` (wrong order)

Both systems use:
- Synonym keywords that canonicalize to standard forms
- Fixed keyword ordering
- Structural validation in pre-canonical form
- Semantic validation in canonical form

## Components and Interfaces

### 1. Edge Type Syntax: Directed and Undirected

**DEPRECATED**: The old pattern with `direction:` property is completely eliminated.

**NEW PATTERN**: Use `directed:` and `undirected:` keywords:

```yaml
# Directed edge type
edgeType:
  directed:
    from: Person
    via: KNOWS
    to: Person

# Undirected edge type
edgeType:
  undirected:
    endpoints: Person
    via: FRIENDS_WITH
```

This new syntax is required for all edge type definitions and references.

### 2. Surface Syntax Patterns

#### Zero-Level Wrapper (Bare Reference)
```yaml
nodeType: Person
```
- No wrapper keyword
- Implies default semantics: exact matching, concrete type

#### One-Level Wrappers
```yaml
# Convenience shortcuts
abstract:
  nodeType: Person

concrete:
  nodeType: Company

properSubtypesOf:
  nodeType: Organization
```
- Single wrapper keyword wraps the entire property
- Maps to specific two-dimensional combinations

#### Two-Level Wrappers
```yaml
# Explicit two-dimensional specification
exactlyOf:
  concrete:
    nodeType: Person

subtypesOf:
  abstract:
    nodeType: Organization
```
- Explicit specification of both dimensions
- Outermost wrapper: subtype matching mode
- Middle wrapper: concreteness
- Innermost: the actual property and value

### 2. Wrapper Application Contexts

#### NodeType: Wrappers Only Wrap (Never Inside)

```yaml
# Wrapping a single nodeType property
abstract:
  nodeType: Person

# Wrapping entire nodeTypes array
abstract:
  nodeTypes:
    - Person
    - Organization
    - Product

# Wrappers around individual array items
nodeTypes:
  - abstract:
      nodeType: Person
  - concrete:
      nodeType: Company
  - nodeType: Product  # no wrapper (zero-level)
```

#### EdgeType: Wrappers Can Wrap Entire Structure OR Individual Components

EdgeType has a compound structure with three components: `from` (source node type), `via`/`arc` (edge content), and `to` (target node type). Type interpretation can be controlled at multiple levels:

**Wrapper Around Entire EdgeType (applies to all components):**
```yaml
abstract:
  edgeType:
    directed:
      from: Person
      via: KNOWS
      to: Person
```

**Wrappers on Individual Components (independent control):**
```yaml
edgeType:
  directed:
    from:
      abstract: Person
    via:
      concrete: KNOWS
    to:
      subtypesOf:
        concrete: Person
```

**Mixed: Wrapper on edgeType + wrapper on specific component:**
```yaml
# This is INVALID - no wrapper inheritance
abstract:
  edgeType:
    directed:
      from: Person  # Does NOT inherit abstract wrapper
      via: KNOWS
      to: Person
```

**Important**: There is NO inheritance of wrappers from higher levels. Each component defaults independently to `exactlyOf: concrete:` if unwrapped.

**Node Type Identifier Forms:**
```yaml
edgeType:
  directed:
    from: Person                    # String
    from: [Person, Organization]    # Array of strings
    from: 0                          # Integer literal (index)
```

#### GraphType: Wrappers Only Wrap

```yaml
# Wrapping a single graphType property
abstract:
  graphType: SocialNetwork
```

#### Array Subsequences

```yaml
# Wrapper around a subsequence of the array
nodeTypes:
  - nodeType: Person
  - abstract:
      nodeTypes:
        - Company
        - Organization
  - nodeType: Product
```

### 3. Normalization Rules

The import preprocessor applies these normalization rules:

| Surface Syntax | Normalized Form | Subtype Matching | Concreteness |
|----------------|-----------------|------------------|--------------|
| `Person` | `exactlyOf: concrete: Person` | exact | concrete |
| `properSubtypesOf: Person` | `subtypesOf: abstract: Person` | covariant | abstract |
| `concrete: Person` | `exactlyOf: concrete: Person` | exact | concrete |
| `abstract: Person` | `subtypesOf: abstract: Person` | covariant | abstract |
| `exactlyOf: concrete: Person` | `exactlyOf: concrete: Person` | exact | concrete |
| `exactlyOf: abstract: Person` | `exactlyOf: abstract: Person` | exact | abstract |
| `subtypesOf: concrete: Person` | `subtypesOf: concrete: Person` | covariant | concrete |
| `subtypesOf: abstract: Person` | `subtypesOf: abstract: Person` | covariant | abstract |

### 4. Logical Model Representation

After normalization, all type references are represented with explicit two-dimensional semantics:

```python
class TypeInterpretation:
    """Normalized type interpretation in the logical model."""
    
    def __init__(self, 
                 typeReference: str,
                 subtypeMatching: SubtypeMatchingMode,
                 concreteness: Concreteness):
        self.__typeReference = typeReference
        self.__subtypeMatching = subtypeMatching
        self.__concreteness = concreteness
    
    @property
    def typeReference(self) -> str:
        return self.__typeReference
    
    @property
    def subtypeMatching(self) -> SubtypeMatchingMode:
        return self.__subtypeMatching
    
    @property
    def concreteness(self) -> Concreteness:
        return self.__concreteness
    
    def isExactMatch(self) -> bool:
        return self.__subtypeMatching == SubtypeMatchingMode.EXACTLY_OF
    
    def allowsSubtypes(self) -> bool:
        return self.__subtypeMatching == SubtypeMatchingMode.SUBTYPES_OF
    
    def isConcrete(self) -> bool:
        return self.__concreteness == Concreteness.CONCRETE
    
    def isAbstract(self) -> bool:
        return self.__concreteness == Concreteness.ABSTRACT


class SubtypeMatchingMode(Enum):
    EXACTLY_OF = "exactlyOf"
    SUBTYPES_OF = "subtypesOf"


class Concreteness(Enum):
    CONCRETE = "concrete"
    ABSTRACT = "abstract"
```

### 5. API Interface

Element types (NodeType, EdgeType, GraphType) expose interpretation properties:

```python
class NodeType:
    """Node type with interpretation semantics."""
    
    def __init__(self, name: str, interpretation: TypeInterpretation, ...):
        self.__name = name
        self.__interpretation = interpretation
        # ... other properties
    
    def isAbstract(self) -> bool:
        """Returns true if this type cannot be directly instantiated."""
        return self.__interpretation.isAbstract()
    
    def isConcrete(self) -> bool:
        """Returns true if this type can be directly instantiated."""
        return self.__interpretation.isConcrete()
    
    def isExactMatch(self) -> bool:
        """Returns true if only exact type matching is allowed."""
        return self.__interpretation.isExactMatch()
    
    def allowsSubtypes(self) -> bool:
        """Returns true if subtype matching is allowed."""
        return self.__interpretation.allowsSubtypes()
```

## Data Models

### JSON Schema Structure

The JSON Schema must support wrappers that surround properties. The key insight is that where we would normally have:

```yaml
nodeType: Person
```

We can instead have a wrapper object that contains the `nodeType` property:

```yaml
abstract:
  nodeType: Person
```

This means the schema needs to accept EITHER a direct property OR a wrapper object at the same level.

#### Conceptual Schema Pattern

For a context that can have a `nodeType` property:

```json
{
  "oneOf": [
    {
      "type": "object",
      "properties": {
        "nodeType": {"type": "string"}
      }
    },
    {
      "type": "object",
      "properties": {
        "abstract": {
          "type": "object",
          "properties": {
            "nodeType": {"type": "string"}
          },
          "required": ["nodeType"]
        }
      },
      "required": ["abstract"]
    },
    {
      "type": "object",
      "properties": {
        "concrete": {
          "type": "object",
          "properties": {
            "nodeType": {"type": "string"}
          },
          "required": ["nodeType"]
        }
      },
      "required": ["concrete"]
    },
    {
      "type": "object",
      "properties": {
        "properSubtypesOf": {
          "type": "object",
          "properties": {
            "nodeType": {"type": "string"}
          },
          "required": ["nodeType"]
        }
      },
      "required": ["properSubtypesOf"]
    },
    {
      "type": "object",
      "properties": {
        "exactlyOf": {
          "type": "object",
          "properties": {
            "concrete": {
              "type": "object",
              "properties": {
                "nodeType": {"type": "string"}
              },
              "required": ["nodeType"]
            }
          },
          "required": ["concrete"]
        }
      },
      "required": ["exactlyOf"]
    }
  ]
}
```

Note: This is a simplified illustration. The actual schema must handle all combinations and all property types (nodeType, edgeType, graphType, nodeTypes, edgeTypes).

### Internal Data Structures

```python
# Type interpretation stored with each type reference
class TypeReferenceWithInterpretation:
    typeReference: str
    subtypeMatching: SubtypeMatchingMode
    concreteness: Concreteness

# Element type definitions include interpretation
class NodeTypeDefinition:
    name: str
    interpretation: TypeInterpretation
    properties: Dict[str, PropertyType]
    supertypes: List[TypeReferenceWithInterpretation]
    # ... other fields
```

## Error Handling

### Validation Errors

1. **Nested Wrapper Error**
   - Detected when: A wrapper keyword appears inside another wrapper
   - Message: "Type interpretation wrappers cannot be nested. Found {outer} wrapper containing {inner} wrapper."

2. **Invalid Wrapper Combination Error**
   - Detected when: Two-level wrapper uses invalid keyword combination
   - Message: "Invalid wrapper combination: {outer}: {inner}:. Valid combinations are exactlyOf/subtypesOf with concrete/abstract."

3. **Wrapper in Type Definition Error**
   - Detected when: Wrapper keyword appears inside a nodeType or edgeType definition
   - Message: "Type interpretation wrappers cannot appear inside type definitions. Wrappers must surround type references."

4. **Abstract Type Instantiation Error**
   - Detected when: Validator encounters direct instance of abstract type
   - Message: "Cannot instantiate abstract type {typeName}. Only subtypes of {typeName} can be instantiated."

5. **Exact Match Violation Error**
   - Detected when: Validator encounters subtype where exact match required
   - Message: "Type {actualType} does not exactly match required type {expectedType}. Exact matching (exactlyOf) is required."

6. **Wrapper Order Violation Error**
   - Detected when: Wrapper keywords appear in incorrect order
   - Message: "Invalid wrapper order. Wrappers must be ordered: subtype matching mode (exactlyOf/subtypesOf), then concreteness (concrete/abstract), then property. Found: {actualOrder}"

## Testing Strategy

### Unit Tests

1. **Normalization Tests**
   - Test each surface syntax pattern normalizes correctly
   - Test all valid two-dimensional combinations
   - Test error detection for invalid patterns

2. **API Method Tests**
   - Test `isAbstract()`, `isConcrete()`, `isExactMatch()`, `allowsSubtypes()` for all wrapper patterns
   - Test methods return correct values after normalization

3. **Validation Tests**
   - Test abstract type rejection
   - Test exact match enforcement
   - Test subtype acceptance
   - Test concrete type acceptance

### Integration Tests

1. **End-to-End Wrapper Tests**
   - Load YAML with various wrapper patterns
   - Verify normalization
   - Validate against test data
   - Query via API

2. **Array Wrapper Tests**
   - Test wrappers around entire arrays
   - Test wrappers around individual items
   - Test mixed wrapped/unwrapped items
   - Test subsequence wrapping

3. **Import Preprocessor Tests**
   - Test wrapper preservation through import resolution
   - Test wrapper application in imported files
   - Test wrapper semantics across import boundaries

### Example Files

Create comprehensive example files demonstrating:
- All surface syntax patterns
- All application contexts (single, array, items, subsequences)
- Valid and invalid patterns
- Real-world use cases (abstract base types, sealed hierarchies, etc.)

## Design Decisions and Rationales

### Decision 0: Single Schema for Both Pre-Canonical and Canonical Forms

**Rationale**: Using one JSON Schema that validates both pre-canonical and canonical forms:
- Simplifies schema maintenance (one source of truth)
- Ensures consistency between what authors write and what processors consume
- Allows pre-canonical files to be validated before import resolution
- Enables canonical files to be validated after preprocessing
- Makes it clear that canonicalization preserves validity
- Avoids confusion about which schema to use when
- Supports incremental validation: structural validation first, semantic validation after canonicalization

**Key Insight**: Import statements are validated structurally (well-formed syntax) in pre-canonical form, but their content is not validated until after resolution. This allows schema authors to work with incomplete or evolving import dependencies.

### Decision 1: EdgeType Component-Level Type Interpretation

**Rationale**: EdgeType has three semantic components (from node type, via/arc edge content, to node type) that need independent type interpretation control:
- Source and target node types may have different interpretation requirements
- Edge content (arc) may have different interpretation than endpoints
- Allows precise control: abstract source, concrete edge, covariant target
- No wrapper inheritance prevents ambiguity and makes interpretation explicit
- Each component defaults independently to `exactlyOf: concrete:`

**Key Insight**: Type interpretation in an edgeType usage can override the type definition. A nodeType defined as concrete can be treated as abstract in a specific edgeType context by wrapping it with `abstract:` in the `from:`, `via:`, or `to:` clause.

**Example Use Case**: A base type `Person` might be defined as concrete (can be instantiated), but in a specific edge type, we want to require only subtypes:
```yaml
edgeType:
  directed:
    from:
      abstract: Person  # Only subtypes of Person allowed as source
    via: MANAGES
    to: Person          # Person or exact instances allowed as target
```

### Decision 2: Fixed Wrapper Order (Analogy to Edge Type Syntax)

**Rationale**: Enforcing fixed wrapper keyword order (subtype matching mode → concreteness → property):
- Provides consistency with edge type endpoint syntax (fixed order: `tail: arc: head:`)
- Eliminates ambiguity about which wrapper applies to what
- Makes schemas easier to read and understand
- Simplifies parser implementation
- Follows established pattern in LEX-2026 (edge types have fixed keyword order)
- Prevents confusion from multiple valid orderings

**Key Insight**: Just as you cannot write `to: from: arc:` for edge endpoints, you cannot write `concrete: exactlyOf: nodeType:` for type interpretations. The order is fixed and enforced by the schema.

### Decision 3: Two Independent Dimensions

**Rationale**: Separating subtype matching from concreteness provides maximum flexibility. Schema authors can specify:
- Concrete types with exact matching (default case)
- Abstract types with subtype matching (common for base types)
- Concrete types with subtype matching (less common but valid)
- Abstract types with exact matching (edge case, but logically consistent)

### Decision 4: Surface Syntax Shortcuts

**Rationale**: One-level wrappers provide convenient shortcuts for the most common patterns:
- `abstract:` covers the common case of abstract base types
- `concrete:` provides explicit documentation of default behavior
- `properSubtypesOf:` clearly expresses the "proper subtype" intent

### Decision 5: Canonicalization in Import Preprocessor

**Rationale**: Treating the import preprocessor as a canonicalization phase that normalizes all patterns to the two-dimensional logical model:
- Simplifies validator logic (only one representation to handle)
- Enables consistent API behavior
- Allows surface syntax evolution without changing core logic
- Makes semantic equivalence explicit
- Establishes a general architectural pattern for other syntax conveniences
- Separates user-facing syntax concerns from validation semantics
- Creates a clear boundary between pre-import and post-import processing

### Decision 6: No Wrapper Nesting

**Rationale**: Forbidding nested wrappers:
- Prevents ambiguous semantics
- Keeps syntax simple and readable
- Avoids complex parsing logic
- Encourages clear, explicit specifications

### Decision 7: Subsequence Wrapping Support

**Rationale**: Allowing wrappers around any contiguous subsequence:
- Provides fine-grained control over interpretation
- Supports heterogeneous arrays with different semantics
- Enables grouping related types with shared interpretation
- Maintains flexibility without requiring separate arrays

## Implementation Notes

### Import Preprocessor Changes (Canonicalization Phase)

The import preprocessor canonicalization phase must:
1. Accept pre-canonical YAML that has already passed JSON Schema validation
2. Detect wrapper keywords at all valid locations in pre-canonical syntax
3. Canonicalize all wrapper forms (zero-level, one-level, two-level) to explicit two-dimensional representation
4. Preserve wrapper semantics through import resolution and merging
5. Validate no wrapper nesting during canonicalization
6. Validate wrapper keywords only surround type reference properties
7. Produce canonical YAML output where all type interpretations are explicit
8. Ensure canonical output also validates against the same JSON Schema

This is part of the broader canonicalization responsibility of the import preprocessor, which also handles import resolution, default value expansion, and other syntax normalizations.

**Important**: The preprocessor does not validate import targets exist or are valid - it only resolves and merges them if they are accessible. Pre-canonical validation passes even if imports are unresolvable.

### JSON Schema Updates

The single JSON Schema must:
1. Define `TypeInterpretationWrapper` pattern with all valid forms (zero-level, one-level, two-level)
2. Apply wrapper pattern to `nodeType`, `edgeType`, `graphType` properties
3. Apply wrapper pattern to `nodeTypes`, `edgeTypes` array items
4. Support wrapper around entire arrays
5. Prevent wrapper nesting through schema constraints
6. Accept `import:` statements in valid locations (structural validation only)
7. Validate both pre-canonical forms (with imports and convenience syntax) and canonical forms (imports resolved, syntax normalized)

**Critical**: There is only ONE schema file (e.g., `lex-2026.0.3.2.schema.json`), not separate pre-import and post-import schemas. The schema is designed to accept both forms.

### API Implementation

Element type classes must:
1. Store normalized `TypeInterpretation` instance
2. Implement query methods (`isAbstract()`, etc.)
3. Expose interpretation for validator use
4. Maintain interpretation through type hierarchy operations

### Validator Implementation

The schema validator must:
1. Check abstract types are not directly instantiated
2. Enforce exact matching when `exactlyOf` specified
3. Allow subtypes when `subtypesOf` specified
4. Apply interpretation rules consistently across all element types
5. Provide clear error messages referencing wrapper semantics
