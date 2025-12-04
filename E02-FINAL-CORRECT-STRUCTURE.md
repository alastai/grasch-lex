# E.0.2 - Final Correct Edge Label Structure

**Date**: 2024-12-04  
**Status**: CONFIRMED CORRECT

## The Two Forms

Edge label properties (`via:`, `arc:`, `typeLabel:`) can be:

### Form 1: String (Simple - No Properties)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # String - bare label value
```

### Form 2: Object (With Properties/Labels)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:  # Object
      typeLabel: KNOWS  # Label value as child property
      implies:  # Sibling to typeLabel
        propertyTypes:
        - name: since
          valueType: INTEGER
```

## Key Insight: Avoiding Mixed Content

This design avoids the XML "mixed content" problem:
- You can't have both a scalar value AND child properties
- Solution: When you need children, use `typeLabel:` to hold the value
- `typeLabel:` and `implies:` are siblings within the edge label object

## Schema Structure

```json
"via": {
  "oneOf": [
    {
      "type": "string",
      "description": "Simple edge label (no properties)"
    },
    {
      "type": "object",
      "description": "Edge label with properties/labels",
      "properties": {
        "typeLabel": {
          "type": "string",
          "description": "The edge label value"
        },
        "implies": {
          "type": "object",
          "properties": {
            "labels": {...},
            "propertyTypes": {...}
          }
        }
      },
      "required": ["typeLabel", "implies"]
    }
  ]
}
```

## Same Pattern for All Synonyms

This pattern applies to:
- `via:` / `arc:` / `typeLabel:` (edge label synonyms)
- When object form: use `typeLabel:` child + `implies:` sibling

## Examples

### Directed with `via:` (string)
```yaml
edgeType:
  directed:
    from: Person
    to: Company
    via: WORKS_FOR
```

### Directed with `via:` (object)
```yaml
edgeType:
  directed:
    from: Person
    to: Company
    via:
      typeLabel: WORKS_FOR
      implies:
        propertyTypes:
        - name: startDate
          valueType: DATE
```

### Undirected with `arc:` (string)
```yaml
edgeType:
  undirected:
    between: Person
    and: Person
    arc: COLLABORATES_WITH
```

### Undirected with `arc:` (object)
```yaml
edgeType:
  undirected:
    between: Person
    and: Person
    arc:
      typeLabel: COLLABORATES_WITH
      implies:
        propertyTypes:
        - name: projectName
          valueType: STRING
```

## Impact Assessment

This changes EVERYTHING about edge type syntax:

1. **JSON Schema** - Complete rewrite of edge label properties
2. **All examples** - Every edge with properties needs restructuring
3. **Design docs** - All examples need updating
4. **Preprocessors** - Must handle both forms
5. **Validators** - Must validate both forms

## Next Steps

1. Update JSON Schema with correct structure
2. Create test file to verify schema works
3. Update all example files systematically
4. Update design documentation
5. Validate everything passes

