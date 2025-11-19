# Abstract Types and Subtypes Analysis

## Overview

This document analyzes all abstract types and subtype relationships found in the LEX-2026.0.3.2 examples and documents what the JSON Schema can validate.

---

## Node Type Hierarchies from Examples

### 1. Person Hierarchy (Multiple Patterns)

**Using `implies` with `supertypes`:**
```yaml
- nodeType:
    typeLabel: Employee
    implies:
      supertypes: Person  # or [Person]
      propertyTypes: [...]

- nodeType:
    typeLabel: Contractor
    implies:
      supertypes: [Person]
      propertyTypes: [...]

- nodeType:
    typeLabel: Manager
    implies:
      supertypes: [Employee, Person]  # Multiple supertypes
      propertyTypes: [...]
```

**Using `extends` with `adding`:**
```yaml
- nodeType:
    typeLabel: Director
    extends: Manager  # or [Manager]
    adding:
      propertyTypes: [...]

- nodeType:
    typeLabel: VicePresident
    extends: [Director]
    adding:
      propertyTypes: [...]

- nodeType:
    typeLabel: CEO
    extends: VicePresident
    adding:
      labels: [Executive, BoardMember]
      propertyTypes: [...]
```

**Hierarchy:**
```
Person (base)
├── Employee (implies)
│   ├── Manager (implies)
│   │   ├── Director (extends)
│   │   │   └── VicePresident (extends)
│   │   │       └── CEO (extends)
│   │   └── SeniorManager (implies)
│   │       └── ExecutiveManager (extends)
└── Contractor (implies)
```

---

### 2. Vehicle Hierarchy (Abstract Base)

```yaml
# Abstract base type
- abstract:
    nodeType:
      typeLabel: Vehicle
      implies:
        propertyTypes:
        - name: id
          valueType: INTEGER
        - name: manufacturer
          valueType: STRING

# Concrete subtype
- nodeType:
    typeLabel: Car
    implies:
      supertypes: Vehicle
      propertyTypes:
      - name: doors
        valueType: INTEGER
```

**Hierarchy:**
```
Vehicle (abstract)
└── Car (concrete)
```

---

### 3. Asset Hierarchy (Abstract with Synonym)

```yaml
# Using abstractSupertype: synonym
- abstractSupertype:
    nodeType:
      typeLabel: Asset
      implies:
        propertyTypes: [...]

# Concrete subtype using extends
- nodeType:
    typeLabel: RealEstate
    extends: Asset
    adding:
      propertyTypes:
      - name: address
        valueType: STRING
```

**Hierarchy:**
```
Asset (abstract)
└── RealEstate (concrete)
```

---

### 4. Place Hierarchy (Sealed)

```yaml
- sealed:
    nodeTypes:
    - abstract:
        nodeType:
          typeLabel: Place
          implies:
            propertyTypes: [...]
    
    - nodeType:
        typeLabel: Continent
        extends: Place
        adding:
          propertyTypes: [...]
    
    - nodeType:
        typeLabel: Country
        extends: Place
        adding:
          propertyTypes: [...]
    
    - nodeType:
        typeLabel: City
        extends: Place
        adding:
          propertyTypes: [...]
```

**Hierarchy:**
```
Place (abstract, sealed)
├── Continent (concrete)
├── Country (concrete)
└── City (concrete)
```

**Note:** `sealed` means no subtypes can be added outside this definition.

---

### 5. Message Hierarchy (Sealed)

```yaml
- sealed:
    nodeTypes:
    - abstract:
        nodeType:
          typeLabel: Message
          implies:
            propertyTypes: [...]
    
    - nodeType:
        typeLabel: Post
        extends: Message
        adding:
          propertyTypes: [...]
    
    - nodeType:
        typeLabel: Comment
        extends: Message
        adding:
          propertyTypes: [...]
```

**Hierarchy:**
```
Message (abstract, sealed)
├── Post (concrete)
└── Comment (concrete)
```

---

### 6. Organisation Hierarchy (Final Subtypes)

```yaml
# Abstract base
- abstract:
    nodeType:
      typeLabel: Organisation
      implies:
        propertyTypes: [...]

# Final concrete types (cannot be extended)
- final:
    nodeType:
      typeLabel: Company
      extends: Organisation
      adding:
        propertyTypes: [...]

- final:
    nodeType:
      typeLabel: University
      extends: Organisation
      adding:
        propertyTypes: [...]
```

**Hierarchy:**
```
Organisation (abstract)
├── Company (final)
└── University (final)
```

**Note:** `final` means these types cannot be further subtyped.

---

## Edge Type Hierarchies from Examples

### 1. Friendship Hierarchy (Undirected)

```yaml
# Base edge type
- edgeType:
    undirected:
      between: Person
      via: KNOWS
      and: Person
    implies:
      propertyTypes:
      - name: since
        valueType: DATE

# Subtype using extends
- edgeType:
    undirected:
      between: Person
      arc: CLOSE_FRIEND
      and: Person
    extends: KNOWS
    adding:
      propertyTypes:
      - name: closeness
        valueType: FLOAT

# Further subtype
- edgeType:
    undirected:
      between: Person
      via: BEST_FRIEND
      and: Person
    extends: [CLOSE_FRIEND]
    adding:
      propertyTypes:
      - name: yearsKnown
        valueType: INTEGER
```

**Hierarchy:**
```
KNOWS (base)
└── CLOSE_FRIEND (extends)
    └── BEST_FRIEND (extends)
```

---

### 2. Relationship Hierarchy (Abstract Base, Directed)

```yaml
# Abstract base edge type
- abstract:
    edgeType:
      directed:
        from: Person
        via: RELATIONSHIP
        to: Person
      implies:
        propertyTypes:
        - name: since
          valueType: DATE

# Concrete subtypes using implies
- edgeType:
    directed:
      from: Person
      via: FRIENDSHIP
      to: Person
    implies:
      supertypes: [RELATIONSHIP]
      propertyTypes:
      - name: closeness
        valueType: FLOAT

- edgeType:
    directed:
      from: Person
      via: PROFESSIONAL_RELATIONSHIP
      to: Person
    implies:
      supertypes: RELATIONSHIP  # Singleton as string
      propertyTypes:
      - name: context
        valueType: STRING

# Concrete subtypes using extends
- edgeType:
    directed:
      from: Person
      arc: MARRIED_TO
      to: Person
    extends: RELATIONSHIP
    adding:
      propertyTypes:
      - name: weddingDate
        valueType: DATE

- edgeType:
    directed:
      from: Person
      via: ENGAGED_TO
      to: Person
    extends: RELATIONSHIP
    adding:
      propertyTypes:
      - name: engagementDate
        valueType: DATE
```

**Hierarchy:**
```
RELATIONSHIP (abstract)
├── FRIENDSHIP (implies)
├── PROFESSIONAL_RELATIONSHIP (implies)
├── MARRIED_TO (extends)
└── ENGAGED_TO (extends)
```

---

### 3. Partnership Hierarchy (Abstract, Undirected)

```yaml
# Abstract using abstractSupertype: synonym
- abstractSupertype:
    edgeType:
      undirected:
        between: Company
        via: PARTNERSHIP
        and: Company
      implies:
        propertyTypes:
        - name: startDate
          valueType: DATE

# Concrete subtype
- edgeType:
    undirected:
      between: Company
      via: STRATEGIC_PARTNERSHIP
      and: Company
    implies:
      supertypes: PARTNERSHIP
      propertyTypes:
      - name: value
        valueType: FLOAT
```

**Hierarchy:**
```
PARTNERSHIP (abstract)
└── STRATEGIC_PARTNERSHIP (concrete)
```

---

## Schema Validation Capabilities

### What the JSON Schema CAN Validate

#### ✓ Supertypes Property
```json
{
  "supertypes": {
    "type": "array",
    "description": "Set of supertype labels (LEX:2026.0.3 - enables subtyping)",
    "items": {"type": "string"},
    "uniqueItems": true
  }
}
```

**Usage in YAML:**
```yaml
implies:
  supertypes: [Message]  # or supertypes: Message
  propertyTypes: [...]
```

---

#### ✓ Extends Property
```json
{
  "extends": {
    "type": "array",
    "description": "Supertypes this type extends (synonym for supertypes)",
    "items": {"type": "string"},
    "uniqueItems": true,
    "minItems": 1
  }
}
```

**Usage in YAML:**
```yaml
extends: [Message]  # or extends: Message
adding:
  propertyTypes: [...]
```

---

#### ✓ Adding Descriptor
```json
{
  "AddingDescriptor": {
    "type": "object",
    "properties": {
      "labels": {
        "type": "array",
        "description": "Additional labels beyond typeLabel",
        "items": {"type": "string"},
        "uniqueItems": true,
        "minItems": 1
      },
      "propertyTypes": {
        "type": "array",
        "description": "New property types being added",
        "items": {"$ref": "#/$defs/PropertyType"}
      }
    }
  }
}
```

**Usage in YAML:**
```yaml
extends: Manager
adding:
  labels: [Executive, BoardMember]
  propertyTypes: [...]
```

---

#### ✓ AllowSubtypesOf (Abstract Supertypes in GraphType)
```json
{
  "allowSubtypesOf": {
    "type": "object",
    "description": "Allow subtypes of specified element types",
    "properties": {
      "abstractSupertypes": {
        "properties": {
          "nodeTypes": {"type": "array"},
          "edgeTypes": {"type": "array"}
        }
      }
    }
  }
}
```

**Usage in YAML:**
```yaml
graphType:
  allowSubtypesOf:
    abstractSupertypes:
      nodeTypes:
      - nodeType:
          typeLabel: Message
          implies: [...]
```

---

### What the JSON Schema CANNOT Validate

#### ✗ Abstract Wrapper (Syntactic Marker)
```yaml
- abstract:
    nodeType:
      typeLabel: Vehicle
      implies: [...]
```

**Why:** JSON Schema can validate the structure but cannot enforce that:
- Abstract types cannot be instantiated
- Only subtypes can be used in actual data

**Solution:** Application logic must interpret the `abstract:` wrapper.

---

#### ✗ Sealed Wrapper (Syntactic Marker)
```yaml
- sealed:
    nodeTypes:
    - abstract: [...]
    - nodeType: [...]
```

**Why:** JSON Schema cannot enforce that:
- No additional subtypes can be defined elsewhere
- The hierarchy is closed

**Solution:** Application logic must track sealed hierarchies.

---

#### ✗ Final Wrapper (Syntactic Marker)
```yaml
- final:
    nodeType:
      typeLabel: Company
      extends: Organisation
```

**Why:** JSON Schema cannot enforce that:
- This type cannot be further subtyped
- No extensions are allowed

**Solution:** Application logic must prevent subtyping of final types.

---

#### ✗ Actual Subtype Relationships
```yaml
supertypes: [Employee, Person]
```

**Why:** JSON Schema can validate the syntax but cannot:
- Verify that Employee and Person actually exist
- Check that the subtype relationship is valid
- Enforce property inheritance rules
- Detect circular dependencies

**Solution:** Semantic validation layer required.

---

#### ✗ Abstract Endpoint Types
```yaml
edgeType:
  directed:
    from:
      abstract: Person
    via: MANAGES
    to: Person
```

**Why:** JSON Schema cannot enforce that:
- Only proper subtypes of Person can be used at the source endpoint
- Person itself cannot be used

**Solution:** Runtime validation during graph construction.

---

## Summary Statistics

### From Examples

**Node Types:**
- Abstract types: 3 (Vehicle, Asset, Organisation)
- Sealed hierarchies: 2 (Place, Message)
- Subtypes using `implies`: 5
- Subtypes using `extends`: 6
- Final types: 2 (Company, University)

**Edge Types:**
- Abstract types: 2 (RELATIONSHIP, PARTNERSHIP)
- Subtypes using `implies`: 3
- Subtypes using `extends`: 4

### Schema Capabilities

**Can Validate (Syntax):**
- ✓ `supertypes` property
- ✓ `extends` property
- ✓ `adding` property
- ✓ `allowSubtypesOf` structure

**Cannot Validate (Semantics):**
- ✗ Abstract type instantiation prevention
- ✗ Sealed hierarchy enforcement
- ✗ Final type extension prevention
- ✗ Subtype relationship validity
- ✗ Property inheritance correctness

---

## Recommendations

1. **Use `abstract:` wrapper** for types that should not be instantiated
2. **Use `sealed:` wrapper** for closed hierarchies
3. **Use `final:` wrapper** for types that cannot be extended
4. **Implement semantic validation** in application logic to enforce these constraints
5. **Document** which types are abstract/sealed/final in schema comments
6. **Test** subtype relationships with actual graph data

---

## Pattern Comparison

### `implies` with `supertypes` vs `extends` with `adding`

**`implies` with `supertypes`:**
- Complete redefinition of the type
- Must list ALL properties (inherited + new)
- More verbose but explicit
- Better for documentation

**`extends` with `adding`:**
- Incremental definition
- Only lists NEW properties and labels
- More concise
- Better for maintenance

**Both are semantically equivalent** - choose based on your preference for verbosity vs. conciseness.
