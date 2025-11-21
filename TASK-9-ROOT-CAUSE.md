# Task 9: Root Cause Identified

## Problem

All 12 importing files fail C form validation. The error is in `edgeTypes` array.

## Root Cause

**The canonicalizer does NOT wrap edge endpoint type references.**

### Expected
```yaml
from:
  exactlyOf:
    concrete: Person
```

### Actual
```yaml
from:
  typeLabel: Person  # Not canonicalized!
```

## Evidence

From `CANON_lex-2026.0.3.2-minimal-import-example.yaml`:
```yaml
edgeTypes:
- edgeType:
    directed:
      from:
        typeLabel: Person  # Should be wrapped
      to:
        typeLabel: Post    # Should be wrapped
      via:
        exactlyOf:
          concrete: AUTHORED  # This IS wrapped ✅
```

## Fix Required

Update `canonicalizing_preprocessor.py` method `canonicalize_edge_type()` to wrap bare endpoint type references in `exactlyOf: concrete:` form.

Handle all endpoint keywords: `from`, `to`, `between`, `and`, `tail`, `head`, `src`, `dst`, etc.

## Impact

This single fix should resolve validation for all 12 failing files.

---

**Status**: Root cause identified  
**File**: `src/grasch/canonicalizing_preprocessor.py`  
**Method**: `canonicalize_edge_type()`
