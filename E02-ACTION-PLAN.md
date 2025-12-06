# E.0.2 Action Plan: Edge Label Structure Fix

**Date**: 2024-12-04  
**Status**: READY TO EXECUTE

## The Issue

Edge label properties (`via:`, `arc:`, `typeLabel:`) must be:
- **String** when no properties
- **Object with `implies:` child** when properties are specified

## Correct Syntax

### String Form (No Properties)
```yaml
via: KNOWS  # Simple string
```

### Object Form (With Properties)
```yaml
via: KNOWS
  implies:
    propertyTypes:
    - name: since
      valueType: INTEGER
```

## Action Items

### 1. JSON Schema Fix (CRITICAL)
**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`

Update edge label properties to `oneOf`:
- String form
- Object form with `implies:` or `extends:`/`adding:`

### 2. Simple Test Files (6 files)
- Fix inline node types → type references
- Fix `implies:` structure

### 3. New Test Files (5 files)
- Fix `implies:` structure
- Fix `extends:`/`adding:` structure

### 4. Phase E Location 3 (2 files)
- Fix all structural issues

### 5. Complex Files (4 files)
- Systematic review and fix

### 6. Design Documentation
- Update all examples
- Clarify structure

## Next Step

**READY**: Start with JSON Schema fix

Awaiting confirmation to proceed.

