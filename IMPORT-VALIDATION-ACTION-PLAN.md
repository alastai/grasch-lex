# Import Validation Action Plan

## Current Status (Session Start)

**Validation Results**: 2/14 files passing (14%)
- ✅ 2 Catalog documents (no imports)
- ❌ 12 documents with imports failing

## Context from Previous Session

Previous session verified that:
1. ✅ Import preprocessor works correctly per specification
2. ✅ Both wrapper formats handled properly (with/without element wrapper)
3. ✅ Import keys correctly removed and content inlined
4. ⚠️ Some files reference missing import files
5. ⚠️ Some validation failures are schema-related

## Immediate Issues to Fix

### Issue 1: Missing Import Files
**File**: `lex-2026.0.3.2-all-import-patterns.yaml`
**Problem**: References non-existent files:
- `imports/snb-types/all_node_types.yaml`
- `imports/snb-types/all_edge_types.yaml`

**Solution**: Update to use existing comprehensive examples:
```yaml
nodeTypes:
  import: "imports/lex-2026.0.3.2-node-type-syntax-examples.yaml"
edgeTypes:
  import: "imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml"
```

### Issue 2: Validation Approach
**Current**: Single schema used for both raw and preprocessed validation
**Problem**: Schema has oneOf patterns for imports that may not handle all preprocessed cases

**Options**:
A. **Two-schema approach**: Create post-import schema without import patterns
B. **Single flexible schema**: Ensure current schema handles both cases
C. **Investigate specific failures**: Fix schema issues case-by-case

## Recommended Action Sequence

### Step 1: Fix Missing Import References ✅
Update `all-import-patterns.yaml` to use existing files

### Step 2: Run Validation Baseline
Check how many files pass after fixing missing imports

### Step 3: Analyze Remaining Failures
For each failing file:
- Check if it's a missing import file issue
- Check if it's a schema validation issue
- Check if it's a preprocessor issue

### Step 4: Determine Schema Strategy
Based on failure analysis, decide:
- Do we need a post-import schema?
- Or can we fix the existing schema?
- Or are there other issues?

## Expected Outcome

Based on previous session context, after fixing missing imports:
- Expected: 6/14 files passing (43%)
- This would confirm preprocessor is working
- Remaining 8 failures would be schema-related

## Next Actions

1. Fix `all-import-patterns.yaml` import references
2. Run validation to get new baseline
3. Analyze specific failures in detail
4. Create targeted fixes based on analysis

---

**Date**: November 19, 2024
**Status**: Ready to proceed with fixes
**Priority**: HIGH - Core validation functionality
