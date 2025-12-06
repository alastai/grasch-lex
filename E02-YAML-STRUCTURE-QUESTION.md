# E.0.2 - YAML Structure Clarification Needed

**Issue**: How to represent edge label with properties in YAML

## The Problem

You stated: "`implies:` is a child of `via:`"

But in YAML, a property cannot be both a scalar AND have children.

## Current (Wrong) Structure
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS  # String at directed level
  implies:  # Sibling of directed
    propertyTypes:
    - name: since
```

## Possible Correct Structures

### Option A: via becomes object, label is implicit
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:  # Object (no label value specified?)
      implies:
        propertyTypes:
        - name: since
```
**Question**: Where does the label value "KNOWS" go?

### Option B: via has label property
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      label: KNOWS
      implies:
        propertyTypes:
        - name: since
```

### Option C: Label is key in via object
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via:
      KNOWS:
        implies:
          propertyTypes:
          - name: since
```

## Need Clarification

**Please provide a complete YAML example showing**:
1. Simple edge (via as string, no properties)
2. Edge with properties (via with implies child)

Showing exactly how the label value and properties are structured.

