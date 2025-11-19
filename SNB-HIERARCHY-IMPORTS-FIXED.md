# SNB Hierarchy Import References Fixed ✅

## Summary

Fixed incorrect import file references for SNB hierarchy files. All files now reference the correct full filenames.

---

## Problem

Three files were referencing SNB hierarchy imports with old short names:
- `imports/snb-types/message_hierarchy.yaml` ❌
- `imports/snb-types/organisation_hierarchy.yaml` ❌  
- `imports/snb-types/place_hierarchy.yaml` ❌

But the actual files have full LEX naming convention:
- `imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml` ✅
- `imports/snb-types/lex-2026.0.3.2-snb-organisation-hierarchy.yaml` ✅
- `imports/snb-types/lex-2026.0.3.2-snb-place-hierarchy.yaml` ✅

This caused "File not found" errors during preprocessing.

---

## Files Fixed

### 1. lex-2026.0.3.2-minimal-import-example.yaml
**Before**:
```yaml
nodeTypes:
- import: imports/snb-types/message_hierarchy.yaml
```

**After**:
```yaml
nodeTypes:
- import: imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml
```

### 2. lex-2026.0.3.2-mixed-import-example.yaml
**Before**:
```yaml
nodeTypes:
- import: imports/snb-types/message_hierarchy.yaml
```

**After**:
```yaml
nodeTypes:
- import: imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml
```

### 3. lex-2026.0.3.2-snb-schema.yaml
Already had correct references ✅

---

## Verification

### Before Fix
```
File reading/preprocessing error: [Errno 2] No such file or directory: 
'src/grasch/examples/imports/snb-types/message_hierarchy.yaml'
```

### After Fix
```
[1/2] Raw validation (with imports)...
    ✓ Raw file valid
[2/2] Preprocessed validation (imports resolved)...
    ✗ Preprocessed file invalid (4 errors)
```

**Result**: Import files now found and preprocessing works! ✅

The remaining validation errors are due to the oneOf schema pattern issue (not import problems).

---

## Current Status

### Import File Issues: ✅ FIXED
- All SNB hierarchy import references corrected
- All import files found successfully
- Preprocessing completes without file errors

### Validation Status: 7/14 passing (50%)
**Files affected by this fix**:
- ✅ lex-2026.0.3.2-minimal-import-example.yaml - Now preprocesses (still has oneOf validation issue)
- ✅ lex-2026.0.3.2-mixed-import-example.yaml - Now preprocesses (still has oneOf validation issue)

**Remaining issues** (not related to SNB imports):
- oneOf validation errors in preprocessed files (schema pattern issue)
- Other import path issues in different files

---

## Related Files

**SNB Hierarchy Import Files** (all exist and working):
1. `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-message-hierarchy.yaml`
2. `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-organisation-hierarchy.yaml`
3. `src/grasch/examples/imports/snb-types/lex-2026.0.3.2-snb-place-hierarchy.yaml`

**Files Using These Imports**:
1. lex-2026.0.3.2-minimal-import-example.yaml ✅
2. lex-2026.0.3.2-mixed-import-example.yaml ✅
3. lex-2026.0.3.2-snb-schema.yaml ✅

---

**Date**: November 19, 2024  
**Status**: ✅ SNB hierarchy import references fixed  
**Impact**: 2 files now preprocess successfully  
**Next**: Address oneOf validation schema issues

