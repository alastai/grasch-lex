# Type Interpretation System - Schema Fix Needed

## Current Problem
3 files failing validation because schema doesn't properly support LEX-2026 type interpretation wrappers.

## What Are Type Interpretations?
Wrappers that qualify how types are understood:
- `exactlyOfThisType:` (default if unwrapped)
- `allowsSubtypesOf:` 
- `abstract:` (shorthand for allowsSubtypesOf: abstract:)
- `final:` (cannot be extended)
- `sealed:` (all concrete types are final)

## Current Schema Issue
Examples use: `allowSubtypesOf: abstractSupertypes: nodeTypes:`
This pattern doesn't match the actual interpretation system.

## Correct Pattern
```yaml
sealed:
  nodeTypes:
  - abstract:
      nodeType: {Message}
  - nodeType: {Post}  # implicitly final
```

Or:
```yaml
- allowsSubtypesOf:
    abstract:
      nodeType: {Message}
```

## Fix Needed
1. Update JSON Schema to support interpretation wrappers
2. Convert examples from old pattern to new pattern
3. Update import preprocessor to handle wrappers

## Impact
Should fix remaining 3 failing validation files.
