# Tasks 8 & 9: Edge Endpoint Canonicalization - Progress Summary

## Problem Identified

The canonicalizing preprocessor was not properly wrapping edge endpoint type references with the default `exactlyOf: concrete:` wrapper.

## Root Cause

**Two-part issue:**

1. **Invalid PC Forms**: Example files were using `typeLabel:` and `typeIdentifier:` keys in edge endpoints, which are INVALID syntax
   - Invalid: `from: {typeLabel: Person}`
   - Valid: `from: Person`

2. **Canonicalizer Not Wrapping**: The canonicalizer wasn't inserting default wrappers around edge endpoint values

## Fixes Applied

### 1. Fixed Canonicalizer (`src/grasch/canonicalizing_preprocessor.py`)

Updated `canonicalize_edge_type()` method to:
- Act "dumb" - doesn't parse or understand what a `<node type for endpoint>` is
- Simply checks if a type interpretation wrapper exists
- If NO wrapper, inserts default `exactlyOf: concrete:` around the ENTIRE value
- Treats the value as a black box

**Key change:**
```python
if comp_key in self.EDGE_COMPONENTS:
    wrapper = self.parse_wrapper(comp_value, ...)
    if wrapper:
        # Already has wrapper - canonicalize it
        edge_components[comp_key] = wrapper.to_canonical_dict()
    else:
        # No wrapper - insert default exactlyOf: concrete: wrapper
        # around the ENTIRE value (don't try to understand it)
        edge_components[comp_key] = {
            SubtypeMatchingMode.EXACTLY_OF.value: {
                Concreteness.CONCRETE.value: comp_value
            }
        }
```

### 2. Fixed Example Files

Fixed 7 example YAML files to remove invalid `typeLabel:` and `typeIdentifier:` keys from edge endpoints:

- lex-2026.0.3.2-comprehensive-import-example.yaml
- lex-2026.0.3.2-finbench-schema.yaml
- lex-2026.0.3.2-minimal-import-example.yaml
- lex-2026.0.3.2-mixed-import-example.yaml
- lex-2026.0.3.2-snb-schema.yaml
- lex-2026.0.3.2-snb-special-identification-example.yaml
- lex-2026.0.3.2-subtype-abstract-test.yaml

**Before:**
```yaml
edgeType:
  undirected:
    between:
      typeLabel: Person  # INVALID
    and:
      typeLabel: Person  # INVALID
    via: KNOWS
```

**After:**
```yaml
edgeType:
  undirected:
    between: Person  # VALID
    and: Person      # VALID
    via: KNOWS
```

## Current Status

### ✅ Canonicalizer Working Correctly

The canonicalizer now produces correct canonical forms:

```yaml
# PC form
from: Person

# C form (produced by canonicalizer)
from:
  exactlyOf:
    concrete: Person  # ✅ Correct!
```

### ❌ Schema Validation Still Failing

All 12 importing files still fail C form validation. This is because:

**The JSON Schema doesn't accept the canonical forms**

The schema needs to be updated to accept edge endpoint structures like:
```yaml
from:
  exactlyOf:
    concrete: Person
```

## Next Steps

### Option 1: Update JSON Schema (RECOMMENDED)

Update `src/grasch/schemas/lex-2026.0.3.2.schema.json` to accept canonical edge endpoint structures.

The schema needs to define edge endpoint patterns that accept:
- Bare references: `Person`, `0`, `['Person', 'Employee']`
- Wrapped references: `{exactlyOf: {concrete: Person}}`
- Inline definitions: `{nodeType: {typeLabel: Person, ...}}`
- Wrapped inline: `{exactlyOf: {concrete: {nodeType: {...}}}}`

### Option 2: Investigate Schema Structure

Examine the current schema to understand why it's rejecting the canonical forms and identify the specific pattern that needs to be added or fixed.

## Files Modified

1. `src/grasch/canonicalizing_preprocessor.py` - Fixed canonicalize_edge_type() method
2. `fix_edge_endpoint_syntax.py` - Script to fix example files
3. 7 example YAML files - Removed invalid typeLabel/typeIdentifier keys

## Validation Results

- **PC forms**: 14/14 passing ✅
- **C forms**: 2/14 passing (only no-import files) ❌
- **Issue**: Schema doesn't accept canonical edge endpoint structures

## Key Insight

The canonicalizer is now working correctly. The remaining issue is that the JSON Schema needs to be updated to validate the canonical forms it produces. This is a schema definition problem, not a canonicalizer problem.

---

**Date**: 2024-11-21
**Tasks**: 8 & 9 from type-interpretation-flexibility spec
**Status**: Canonicalizer fixed, schema update needed
