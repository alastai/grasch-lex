# Task 9.1: C Form Validation Failure Analysis

## File Analyzed
`CANON_lex-2026.0.3.2-minimal-import-example.yaml`

## Root Cause Identified

The canonicalizer is producing **INVALID** edge endpoint syntax in C form.

### The Problem

**Current C Form Output** (WRONG):
```yaml
edgeTypes:
  - edgeType:
      directed:
        from:
          typeLabel: Person    # ❌ WRONG - typeLabel: is not a type definition
        to:
          typeLabel: Post      # ❌ WRONG
        via:
          exactlyOf:
            concrete: AUTHORED
```

**Expected C Form** (CORRECT):
```yaml
edgeTypes:
  - edgeType:
      directed:
        from:
          exactlyOf:
            concrete: Person   # ✅ CORRECT - wraps the type reference
        to:
          exactlyOf:
            concrete: Post     # ✅ CORRECT
        via:
          exactlyOf:
            concrete: AUTHORED
```

### Why This Fails Validation

The JSON Schema expects edge endpoints to be either:
1. **By reference**: `Person` (string), `[X, Y]` (array), or `0` (integer)
2. **Inline**: `nodeType: typeLabel: Person` (object with nodeType key)
3. **Wrapped reference**: `exactlyOf: concrete: Person`
4. **Wrapped inline**: `exactlyOf: concrete: nodeType: typeLabel: Person`

But the canonicalizer is producing:
- `typeLabel: Person` - which is **neither** a valid reference **nor** a valid inline definition

This is an **invalid intermediate form** that doesn't match any schema pattern.

## Canonicalizer Bug Analysis

### What's Happening

The canonicalizer appears to be:
1. Starting with PC form: `from: Person`
2. Trying to add a wrapper
3. But incorrectly expanding `Person` to `typeLabel: Person`
4. Then failing to wrap it properly

### What Should Happen

**Scenario 1: By-Reference Endpoint**

```yaml
# PC form
from: Person

# Canonicalization steps:
# 1. Recognize "Person" as a type reference (string)
# 2. Wrap it with default wrapper
# 3. Result:
from:
  exactlyOf:
    concrete: Person
```

**Scenario 2: Inline Endpoint**

```yaml
# PC form
from:
  nodeType:
    typeLabel: Person
    implies: {...}

# Canonicalization steps:
# 1. Recognize nodeType: {...} as inline definition
# 2. Wrap entire definition with default wrapper
# 3. Result:
from:
  exactlyOf:
    concrete:
      nodeType:
        typeLabel: Person
        implies: {...}
```

## Impact

This bug affects **ALL** edge types in **ALL** importing files:
- 12 files fail C form validation
- All failures likely due to this same issue
- Edge endpoints are malformed in canonical output

## Fix Required

Update `canonicalizing_preprocessor.py` to:

1. **Detect type definition form**:
   - Is it a string/array/int? → By reference
   - Is it `nodeType: {...}`? → Inline definition

2. **Wrap correctly**:
   - By reference: wrap the value directly
   - Inline: wrap the entire `nodeType: {...}` structure

3. **Never produce** `typeLabel: X` as a standalone form

## Next Steps

1. Fix the canonicalizer (Task 9.2)
2. Re-run validation to verify fix
3. Ensure all 14 files pass C form validation

---

**Status**: Root cause identified
**Location**: `src/grasch/canonicalizing_preprocessor.py`
**Issue**: Edge endpoints incorrectly canonicalized to invalid `typeLabel: X` form
**Fix**: Update wrapper logic to handle by-reference vs inline correctly
