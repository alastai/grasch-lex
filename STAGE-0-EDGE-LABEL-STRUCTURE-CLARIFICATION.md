# CRITICAL: Edge Label Structure Clarification

**Date**: 2024-12-04  
**Issue**: E.0.2 - Edge label property structure with `implies:`

## The Correction

**User stated**: "the implies: is a child of the via:"

This means the edge label properties (`via:`, `arc:`, `typeLabel:`) can be EITHER:
1. **Simple string** (when no `implies:`)
2. **Object with `implies:` child** (when properties/labels are specified)

## Correct Structure

### Pattern 1: Edge Label as String (No Properties)
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # String - no properties
```

### Pattern 2: Edge Label as Object with `implies:`
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # This line is the label value
      implies:  # Child of via:
        propertyTypes:  # Child of implies:
        - name: since
          valueType: INTEGER
```

## Impact on Schema

The JSON Schema must define edge label properties as:
```json
"via": {
  "oneOf": [
    {"type": "string"},  // Simple label
    {
      "type": "object",  // Label with implies
      "properties": {
        "implies": {
          "type": "object",
          "properties": {
            "labels": {...},
            "propertyTypes": {...}
          }
        }
      }
    }
  ]
}
```

## Files Requiring Major Changes

ALL files with edge types need review because this changes the fundamental structure.

