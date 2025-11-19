# Type Interpretation System Analysis

## Overview
LEX-2026 has a type interpretation wrapper system that qualifies how types are understood.

## Default Interpretation
Any unwrapped type is implicitly: `exactlyOfThisType: concrete:`

## Available Interpretations

### 1. exactlyOfThisType
Default interpretation (can be explicit).

### 2. abstract
By definition means `allowsSubtypesOf: abstract:`

### 3. allowsSubtypesOf
Can wrap `concrete:` or `abstract:` types.
If inner qualifier omitted, `concrete:` is assumed.

### 4. final
Cannot combine with `abstract:` or `allowsSubtypesOf:`.
Cannot appear inside `extends:` wrapper.

### 5. sealed
Applied to nodeTypes/edgeTypes sequences.
Every concrete class is deemed final.

## Subtyping Semantics
- Subtype of concrete type: contains the concrete type
- Subtype of abstract type: one of its proper subtypes

## Import Interpretation
An import is a defaulted interpretation that can be wrapped:
```yaml
- import: path.yaml  # default: exactlyOfThisType: concrete:
- allowsSubtypesOf:
    import: path.yaml
- sealed:
    import: path.yaml
```

## Current Schema Issue
Current schema has `allowSubtypesOf: abstractSupertypes:` pattern.
Should be simpler: interpretations wrap types directly.

Correct pattern:
```yaml
- allowsSubtypesOf:
    abstract:
      nodeType: {...}
```

Not:
```yaml
- allowSubtypesOf:
    abstractSupertypes:
      nodeTypes:
      - nodeType: {...}
```
