# Complete Subtype, Supertype, and Abstract Analysis

## Search Results Summary

**In Examples:** 59 occurrences
**In Schema:** 15+ occurrences

---

## EXAMPLES: All Fragments with subtype/supertype/abstract

### From node-type-syntax-examples.yaml

#### Pattern 4: Subtype with singleton supertype (string form)
```yaml
# Pattern 4: Subtype with singleton supertype (string form)
- nodeType:
    typeLabel: Employee
    implies:
      supertypes: Person
      propertyTypes:
      - name: employeeId
        valueType: STRING
        notNull: true
```

#### Pattern 5: Subtype with singleton supertype (array form)
```yaml
# Pattern 5: Subtype with singleton supertype (array form)
- nodeType:
    typeLabel: Contractor
    implies:
      supertypes: [Person]
      propertyTypes:
      - name: contractId
        valueType: STRING
        notNull: true
```

#### Pattern 6: Subtype with multiple supertypes
```yaml
# Pattern 6: Subtype with multiple supertypes
- nodeType:
    typeLabel: Manager
    implies:
      supertypes: [Employee, Person]
      propertyTypes:
      - name: department
        valueType: STRING
        notNull: true
```

#### Pattern 7-9: Subtypes using extends
```yaml
# Pattern 7: Subtype using extends (singleton string)
- nodeType:
    typeLabel: Director
    extends: Manager
    adding:
      propertyTypes:
      - name: division
        valueType: STRING
        notNull: true

# Pattern 8: Subtype using extends (array form)
- nodeType:
    typeLabel: VicePresident
    extends: [Director]
    adding:
      propertyTypes:
      - name: region
        valueType: STRING

# Pattern 9: Subtype with extends and additional labels
- nodeType:
    typeLabel: CEO
    extends: VicePresident
    adding:
      labels:
      - Executive
      - BoardMember
      propertyTypes:
      - name: boardSeat
        valueType: INTEGER
```

#### Pattern 10: Abstract type using abstract: wrapper
```yaml
# ABSTRACT TYPES
# Pattern 10: Abstract type using abstract: wrapper
- abstract:
    nodeType:
      typeLabel: Vehicle
      implies:
        propertyTypes:
        - name: id
          valueType: INTEGER
          notNull: true
        - name: manufacturer
          valueType: STRING
```

#### Pattern 11: Concrete subtype of abstract type
```yaml
# Pattern 11: Concrete subtype of abstract type
- nodeType:
    typeLabel: Car
    implies:
      supertypes: Vehicle
      propertyTypes:
      - name: doors
        valueType: INTEGER
```

#### Pattern 12: Abstract type using abstractSupertype: synonym
```yaml
# Pattern 12: Abstract type using abstractSupertype: synonym
- abstractSupertype:
    nodeType:
      typeLabel: Asset
      implies:
        propertyTypes:
        - name: id
          valueType: INTEGER
          notNull: true
        - name: value
          valueType: FLOAT
```

#### Pattern 13: Concrete subtype of abstract Asset
```yaml
# Pattern 13: Concrete subtype of abstract Asset
- nodeType:
    typeLabel: RealEstate
    extends: Asset
    adding:
      propertyTypes:
      - name: address
        valueType: STRING
```

#### Sealed Hierarchies with Abstract Base
```yaml
# Pattern 16: Sealed hierarchy - no subtypes can be added outside this definition
- sealed:
    nodeTypes:
    - abstract:
        nodeType:
          typeLabel: Place
          implies:
            propertyTypes:
            - name: id
              valueType: INTEGER
              notNull: true
            - name: name
              valueType: STRING
              notNull: true
    
    - nodeType:
        typeLabel: Continent
        extends: Place
        adding:
          propertyTypes:
          - name: area
            valueType: FLOAT
    
    - nodeType:
        typeLabel: Country
        extends: Place
        adding:
          propertyTypes:
          - name: population
            valueType: INTEGER
    
    - nodeType:
        typeLabel: City
        extends: Place
        adding:
          propertyTypes:
          - name: population
            valueType: INTEGER
          - name: coordinates
            valueType: STRING
```

#### Another Sealed Hierarchy (Message types)
```yaml
# Pattern 17: Another sealed hierarchy (Message types)
- sealed:
    nodeTypes:
    - abstract:
        nodeType:
          typeLabel: Message
          implies:
            propertyTypes:
            - name: id
              valueType: INTEGER
              notNull: true
            - name: content
              valueType: STRING
            - name: creationDate
              valueType: ZONED DATETIME
              notNull: true
    
    - nodeType:
        typeLabel: Post
        extends: Message
        adding:
          propertyTypes:
          - name: imageFile
            valueType: STRING
          - name: language
            valueType: STRING
    
    - nodeType:
        typeLabel: Comment
        extends: Message
        adding:
          propertyTypes:
          - name: replyCount
            valueType: INTEGER
```

#### Organisation Hierarchy with Abstract Base
```yaml
# Pattern 18: Organisation hierarchy with final concrete types
# Organisation can be extended, but Company and University cannot
- abstract:
    nodeType:
      typeLabel: Organisation
      implies:
        propertyTypes:
        - name: id
          valueType: INTEGER
          notNull: true
        - name: name
          valueType: STRING
          notNull: true

- final:
    nodeType:
      typeLabel: Company
      extends: Organisation
      adding:
        propertyTypes:
        - name: industry
          valueType: STRING

- final:
    nodeType:
      typeLabel: University
      extends: Organisation
      adding:
        propertyTypes:
        - name: ranking
          valueType: INTEGER
```

#### Multi-level Inheritance
```yaml
# Pattern 19: Multi-level inheritance (unsealed)
- nodeType:
    typeLabel: SeniorManager
    implies:
      supertypes: Manager
      propertyTypes:
      - name: yearsExperience
        valueType: INTEGER

- nodeType:
    typeLabel: ExecutiveManager
    extends: SeniorManager
    adding:
      labels:
      - Leadership
      propertyTypes:
      - name: strategicInitiatives
        valueType: LIST
```

---

### From edge-type-syntax-examples.yaml

#### Edge Subtype using extends
```yaml
# Subtype using extends with adding (singleton string)
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
      - name: sharedInterests
        valueType: LIST

# Another subtype using extends (array form)
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

#### Edge Subtypes with Directed Edges
```yaml
# Subtype: MARRIED_TO extends RELATIONSHIP
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
        notNull: true
      - name: location
        valueType: STRING

# Another relationship subtype
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
      - name: weddingPlanned
        valueType: BOOLEAN
```

#### Abstract Edge Types
```yaml
# ABSTRACT EDGE TYPES
# Abstract edge type - only subtypes can be instantiated
# Using abstract: keyword
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

# Concrete subtype of abstract RELATIONSHIP
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

# Another concrete subtype - singleton supertype as string
- edgeType:
    directed:
      from: Person
      via: PROFESSIONAL_RELATIONSHIP
      to: Person
    implies:
      supertypes: RELATIONSHIP
      propertyTypes:
      - name: context
        valueType: STRING
```

#### Abstract Edge Type with Synonym
```yaml
# Abstract edge type using abstractSupertype: synonym
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

# Concrete subtype of PARTNERSHIP - singleton as string
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

#### Abstract Endpoint Types
```yaml
# ABSTRACT ENDPOINT TYPES
# Edge requiring proper subtype of Person at target
# Person can exist as isolated node, but edge requires subtype
- edgeType:
    directed:
      from: Employee
      via: MANAGES
      to:
        abstract: Person
    implies:
      propertyTypes:
      - name: startDate
        valueType: DATE

# Same using abstractSupertype: synonym
- edgeType:
    directed:
      from: Manager
      via: SUPERVISES
      to:
        abstractSupertype: Person
    implies:
      propertyTypes:
      - name: role
        valueType: STRING

# Both endpoints can be abstract
- edgeType:
    directed:
      from:
        abstract: Person
      via: REPORTS_TO
      to:
        abstract: Person
    implies:
      propertyTypes: []

# Undirected with abstract endpoint
- edgeType:
    undirected:
      between:
        abstract: Person
      via: COLLABORATES_ON
      and: Company
    implies:
      propertyTypes:
      - name: projectName
        valueType: STRING
```

---

### From comprehensive-import-example.yaml

```yaml
# Level 2: allowSubtypesOf with abstract supertypes
allowSubtypesOf:
  abstractSupertypes:
    nodeTypes:
      - nodeType:
          typeLabel: Message
          implies:
            propertyTypes:
              - name: id
                valueType: INTEGER
                notNull: true
```

---

### From complete-import-example.yaml

```yaml
subtypesOfSchemaType:
  # (preserved for future work)
```

---

## SCHEMA: All Fragments with subtype/supertype/abstract

### Type Interpretation (Subtype Matching)
```json
{
  "typeInterpretation": {
    "type": "string",
    "enum": [
      "exactlyOfThisType",
      "anySubtypeOf",
      "anyProperSubtypeOf"
    ],
    "default": "exactlyOfThisType",
    "description": "How types are interpreted during validation (LEX:2026.0.3)"
  }
}
```

### AllowSubtypesOf Structure
```json
{
  "allowSubtypesOf": {
    "type": "object",
    "description": "Allow subtypes of specified element types (covariant matching)",
    "properties": {
      "abstractSupertypes": {
        "type": "object",
        "description": "Abstract supertypes that cannot be instantiated directly",
        "properties": {
          "nodeTypes": {
            "type": "array",
            "description": "Node types that allow subtypes (supertype can be instantiated)",
            "items": {
              "$ref": "#/$defs/NodeType"
            }
          },
          "edgeTypes": {
            "type": "array",
            "description": "Edge types that allow subtypes (supertype can be instantiated)",
            "items": {
              "$ref": "#/$defs/EdgeType"
            }
          }
        }
      }
    }
  }
}
```

### Supertypes Property in ImpliesDescriptor
```json
{
  "ImpliesDescriptor": {
    "type": "object",
    "description": "Container for supertypes, labels, and property types (LEX:2026.0.3 structure)",
    "properties": {
      "supertypes": {
        "type": "array",
        "description": "Set of supertype labels (LEX:2026.0.3 - enables subtyping)",
        "items": {
          "type": "string"
        },
        "uniqueItems": true
      }
    }
  }
}
```

### Extends Property (Synonym for Supertypes)
```json
{
  "extends": {
    "type": "array",
    "description": "Supertypes this type extends (synonym for supertypes)",
    "items": {
      "type": "string"
    },
    "uniqueItems": true,
    "minItems": 1
  }
}
```

### AddingDescriptor (Used with Extends)
```json
{
  "AddingDescriptor": {
    "type": "object",
    "description": "Container for labels and property types being added to a supertype (used with extends)",
    "properties": {
      "labels": {
        "type": "array",
        "description": "Additional labels beyond typeLabel (typeLabel never included)",
        "items": {
          "type": "string"
        },
        "uniqueItems": true,
        "minItems": 1
      },
      "propertyTypes": {
        "type": "array",
        "description": "New property types being added (inherited properties not included)",
        "items": {
          "$ref": "#/$defs/PropertyType"
        }
      }
    },
    "additionalProperties": false
  }
}
```

### SubtypesOfSchemaType (Future Work)
```json
{
  "subtypesOfSchemaType": {
    "type": "string",
    "description": "Preserved for future work - subtype relationships"
  }
}
```

### Extension Interpretation Properties
```json
{
  "allowUndefinedSubtypes": {
    "type": "boolean",
    "description": "If true, allows undefined subtypes"
  },
  "onlyDefinedSubtypes": {
    "type": "boolean",
    "description": "If true, only defined subtypes allowed (default)"
  }
}
```

---

## Pattern Summary

### Subtype Declaration Patterns

**Pattern 1: Using `supertypes` in `implies` (string)**
```yaml
implies:
  supertypes: Person
  propertyTypes: [...]
```

**Pattern 2: Using `supertypes` in `implies` (array)**
```yaml
implies:
  supertypes: [Employee, Person]
  propertyTypes: [...]
```

**Pattern 3: Using `extends` (string)**
```yaml
extends: Manager
adding:
  propertyTypes: [...]
```

**Pattern 4: Using `extends` (array)**
```yaml
extends: [Director]
adding:
  labels: [...]
  propertyTypes: [...]
```

### Abstract Type Patterns

**Pattern 1: Using `abstract:` wrapper**
```yaml
- abstract:
    nodeType:
      typeLabel: Vehicle
      implies: [...]
```

**Pattern 2: Using `abstractSupertype:` synonym**
```yaml
- abstractSupertype:
    nodeType:
      typeLabel: Asset
      implies: [...]
```

**Pattern 3: Abstract endpoint in edge**
```yaml
edgeType:
  directed:
    from:
      abstract: Person
    via: MANAGES
    to: Person
```

**Pattern 4: Using `allowSubtypesOf.abstractSupertypes`**
```yaml
graphType:
  allowSubtypesOf:
    abstractSupertypes:
      nodeTypes:
      - nodeType:
          typeLabel: Message
          implies: [...]
```

### Sealed/Final Patterns

**Sealed Hierarchy:**
```yaml
- sealed:
    nodeTypes:
    - abstract: [...]
    - nodeType: [...]
```

**Final Type:**
```yaml
- final:
    nodeType:
      typeLabel: Company
      extends: Organisation
```

---

## Schema Validation Capabilities

### ✓ Can Validate (Syntax)

1. **`supertypes` property** - array of strings or single string
2. **`extends` property** - array of strings with minItems: 1
3. **`adding` property** - object with labels and propertyTypes
4. **`allowSubtypesOf` structure** - with abstractSupertypes
5. **`typeInterpretation`** - enum with subtype matching modes

### ✗ Cannot Validate (Semantics)

1. **`abstract:` wrapper** - structural pattern only
2. **`abstractSupertype:` wrapper** - structural pattern only
3. **`sealed:` wrapper** - structural pattern only
4. **`final:` wrapper** - structural pattern only
5. **Actual subtype relationships** - requires semantic analysis
6. **Abstract type instantiation prevention** - runtime concern
7. **Sealed hierarchy enforcement** - requires global analysis
8. **Final type extension prevention** - requires global analysis

---

## Key Insights

1. **Two equivalent syntaxes** for declaring subtypes:
   - `implies` + `supertypes` (complete redefinition)
   - `extends` + `adding` (incremental definition)

2. **Two equivalent keywords** for abstract types:
   - `abstract:` (primary)
   - `abstractSupertype:` (synonym)

3. **Abstract can appear in three contexts**:
   - As wrapper for node/edge type definitions
   - As property in edge endpoint references
   - In `allowSubtypesOf.abstractSupertypes`

4. **Schema validates structure, not semantics**:
   - JSON Schema ensures correct syntax
   - Application logic must enforce abstract/sealed/final constraints
   - Semantic validation layer needed for relationship validity

5. **Type interpretation modes** control subtype matching:
   - `exactlyOfThisType` - no subtype matching
   - `anySubtypeOf` - includes the type and all subtypes
   - `anyProperSubtypeOf` - only subtypes, not the type itself
