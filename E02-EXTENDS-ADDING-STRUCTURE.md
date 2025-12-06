# E.0.2 - Edge Label Structure with `extends:` and `adding:`

**Date**: 2024-12-04  
**Status**: CONFIRMED

## Complete Edge Label Structure Patterns

Edge label properties (`via:`, `arc:`, `typeLabel:`) support THREE forms:

### Form 1: String (Simple - No Properties, No Inheritance)
```yaml
via: KNOWS  # String - bare label value
```

### Form 2: Object with `implies:` (Properties without Inheritance)
```yaml
via:  # Object
  typeLabel: KNOWS  # Label value
  implies:  # Sibling to typeLabel
    propertyTypes:
    - name: since
      valueType: INTEGER
```

### Form 3: Object with `extends:`/`adding:` (Inheritance)
```yaml
via:  # Object
  typeLabel: KNOWS  # Label value
  extends: RELATES  # Sibling to typeLabel
  adding:  # Sibling to typeLabel and extends
    propertyTypes:
    - name: closeness
      valueType: FLOAT
```

## Key Rules

1. **Mutually Exclusive**: Cannot have both `implies:` and `extends:` in same edge label
2. **`adding:` requires `extends:`**: Cannot use `adding:` without `extends:`
3. **`extends:` can be alone**: Can have `extends:` without `adding:`
4. **All are siblings**: `typeLabel:`, `implies:`, `extends:`, `adding:` are all siblings

## Complete Examples

### Simple Edge (String Form)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS
```

### Edge with Properties (Object with `implies:`)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: KNOWS
      implies:
        propertyTypes:
        - name: since
          valueType: DATE
```

### Edge with Inheritance Only (Object with `extends:`)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: KNOWS
      extends: RELATES
```

### Edge with Inheritance and Additional Properties (Object with `extends:`/`adding:`)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      typeLabel: CLOSE_FRIEND
      extends: KNOWS
      adding:
        propertyTypes:
        - name: closeness
          valueType: FLOAT
        labels:
        - TRUSTED
```

### Undirected with `arc:` and `extends:`
```yaml
edgeType:
  undirected:
    between: Company
    and: Company
    arc:
      typeLabel: STRATEGIC_PARTNERSHIP
      extends: PARTNERSHIP
      adding:
        propertyTypes:
        - name: value
          valueType: FLOAT
```

## Schema Structure

```json
"via": {
  "oneOf": [
    {
      "type": "string",
      "description": "Simple edge label"
    },
    {
      "type": "object",
      "description": "Edge label with implies",
      "properties": {
        "typeLabel": {"type": "string"},
        "implies": {
          "type": "object",
          "properties": {
            "labels": {...},
            "propertyTypes": {...}
          }
        }
      },
      "required": ["typeLabel", "implies"],
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "Edge label with extends (no adding)",
      "properties": {
        "typeLabel": {"type": "string"},
        "extends": {
          "oneOf": [
            {"type": "string"},
            {"type": "array", "items": {"type": "string"}}
          ]
        }
      },
      "required": ["typeLabel", "extends"],
      "additionalProperties": false
    },
    {
      "type": "object",
      "description": "Edge label with extends and adding",
      "properties": {
        "typeLabel": {"type": "string"},
        "extends": {
          "oneOf": [
            {"type": "string"},
            {"type": "array", "items": {"type": "string"}}
          ]
        },
        "adding": {
          "type": "object",
          "properties": {
            "labels": {...},
            "propertyTypes": {...}
          }
        }
      },
      "required": ["typeLabel", "extends", "adding"],
      "additionalProperties": false
    }
  ]
}
```

## Summary

All three edge label synonyms (`via:`, `arc:`, `typeLabel:`) follow the same pattern:
- **String form**: For simple edges
- **Object form**: When you need `implies:` OR `extends:`/`adding:`
- **In object form**: Always use `typeLabel:` child to hold the label value

This provides a clean, consistent structure that avoids mixed content issues.

