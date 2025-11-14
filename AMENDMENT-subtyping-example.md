# Amendment: Added Subtyping Example to SNB Schema

## Change Applied
Added a `Message` supertype to the SNB schema, with `Post` and `Comment` as subtypes that inherit from it. This demonstrates the LEX:2026.0.3 subtyping feature using the `implies.supertypes` structure.

## Rationale
The LDBC Social Network Benchmark naturally has a concept where both Posts and Comments are types of Messages. This is a perfect use case to demonstrate the subtyping capability introduced in LEX:2026.0.3.

## Type Hierarchy

```
Message (supertype)
├── Post (subtype)
└── Comment (subtype)
```

## Implementation

### Message (Supertype)
```yaml
- nodeTypeIdentifier:
    typeLabel: "Message"
  implies:
    labels:
      - "Message"
    propertyTypes:
      - name: "id"
        valueType: {name: "INTEGER", parameters: {nullable: false}}
      - name: "creationDate"
        valueType: {name: "ZONED DATETIME", parameters: {nullable: false}}
      - name: "locationIP"
        valueType: {name: "STRING", parameters: {nullable: false}}
      - name: "browserUsed"
        valueType: {name: "STRING", parameters: {nullable: false}}
      - name: "content"
        valueType: {name: "STRING", parameters: {nullable: true}}
      - name: "length"
        valueType: {name: "INTEGER", parameters: {nullable: false}}
```

### Post (Subtype of Message)
```yaml
- nodeTypeIdentifier:
    typeLabel: "Post"
  implies:
    supertypes:
      - "Message"  # Inherits all Message properties
    labels:
      - "Post"
    propertyTypes:
      # Only Post-specific properties
      - name: "imageFile"
        valueType: {name: "STRING", parameters: {nullable: true}}
      - name: "language"
        valueType: {name: "STRING", parameters: {nullable: true}}
```

### Comment (Subtype of Message)
```yaml
- nodeTypeIdentifier:
    typeLabel: "Comment"
  implies:
    supertypes:
      - "Message"  # Inherits all Message properties
    labels:
      - "Comment"
    propertyTypes: []  # No additional properties beyond Message
```

## Property Inheritance

### Message Properties (Inherited by Both)
1. `id`: INTEGER (not null)
2. `creationDate`: ZONED DATETIME (not null)
3. `locationIP`: STRING (not null)
4. `browserUsed`: STRING (not null)
5. `content`: STRING (nullable)
6. `length`: INTEGER (not null)

### Post Additional Properties
7. `imageFile`: STRING (nullable)
8. `language`: STRING (nullable)

### Comment Additional Properties
(None - Comment uses only the inherited Message properties)

## Effective Type Definitions

### Post (with inheritance)
- **Total properties**: 8 (6 from Message + 2 Post-specific)
- **Inherited from**: Message
- **Adds**: imageFile, language

### Comment (with inheritance)
- **Total properties**: 6 (all from Message)
- **Inherited from**: Message
- **Adds**: (none)

## Validation Results

```
✅ Schema validation PASSED

🔗 Subtyping (LEX:2026.0.3):
    • Post extends ['Message']
    • Comment extends ['Message']

Node Types: 9 (was 8, added Message)
Total Properties: 40 (was 46, reduced through inheritance)
```

## Benefits of This Design

1. **DRY Principle**: Common properties defined once in Message
2. **Type Safety**: Clear inheritance hierarchy
3. **Maintainability**: Changes to common properties only need to be made in Message
4. **Semantic Clarity**: Explicitly shows that Post and Comment are types of Messages
5. **Demonstrates LEX:2026.0.3**: Shows the new subtyping feature in action

## Files Updated

- `src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml`
  - Added Message node type
  - Updated Post to extend Message
  - Updated Comment to extend Message
  - Removed duplicate properties from Post and Comment

- `tests/validate_snb_lex_0_3_1_schema.py`
  - Fixed supertypes detection to work with `implies` structure
  - Now correctly reports subtyping relationships

## LEX-100r3 Compliance

This implementation follows the LEX-100r3 specification for subtyping:

> "A node type with supertypes pulls in, or incorporates into the node type being specified, the labels and property types implied by each type label"

The `supertypes` field in the `implies` structure enables Java interface mixin-style composition, where subtypes inherit all properties from their supertypes.
