# Phase 2, Step 2: pathName Usage Clarification - COMPLETE ✅

## Summary

Clarified the correct usage of `pathName` and identified an error in the JSON Schema where `pathName` is incorrectly included as an optional property on `GraphType`.

---

## Clarification Received

**Correct usage of `pathName`:**

| Document Type | Has pathName? | Purpose |
|---------------|---------------|---------|
| **catalog** | ❌ NO | Uses `IRI` for identification |
| **graphSchema** | ✅ YES | Identity of the schema (e.g., `/benchmarks/ldbc/snb`) |
| **graph** | ✅ YES | Identity of the graph instance (e.g., `/benchmarks/ldbc/snb-sf1`) |
| **graphType** | ❌ NO | Contained within graphSchema; no independent identity |

---

## Error Identified

**Location**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`, line 341

**Issue**: GraphType definition incorrectly includes `pathName` as an optional property

**Description in schema**: "Optional path name (only present if graphType is imported)"

**Why this is wrong**:
1. graphType is not a top-level document - it's always contained within graphSchema
2. The pathName identifies the graphSchema document, not the graphType within it
3. graphType has no independent existence, so it doesn't need its own path identity
4. The import mechanism doesn't require pathName on graphType

---

## Verification Results

### Requirements ✅ CORRECT
- LEX-9 correctly specifies pathName for graphSchema and graph
- LEX-9 does NOT mention pathName for graphType
- No changes needed to requirements

### Examples ✅ CORRECT
All examples follow the correct pattern:
- `pathName` appears on `graphSchema` wrapper
- `pathName` does NOT appear on `graphType` within it
- No changes needed to examples

### JSON Schema ❌ NEEDS CORRECTION
- GraphType definition includes incorrect `pathName` property
- This property should be removed entirely
- **Action required**: JSON Schema needs to be corrected

---

## Documentation Created

**File**: `PATHNAME-ERROR-IDENTIFICATION.md`
- Complete analysis of the error
- Correct vs incorrect usage examples
- Rationale for why graphType should not have pathName
- Action items for correction
- Impact assessment

---

## Requirements Status

**No changes needed to requirements** - they are already correct:
- LEX-9 criterion #3: graphSchema has pathName ✅
- LEX-9 criterion #4: graph has pathName ✅
- LEX-9 does not mention pathName for graphType ✅

---

## Next Steps

### Immediate (JSON Schema Correction)
This is outside the scope of Phase 2 (requirements updates) but has been documented for future action:
1. Remove `pathName` property from GraphType definition in JSON Schema
2. Validate that all examples still pass (they should, since they don't use it)
3. Update any API code that might reference graphType.pathName

### Phase 2 Continuation
Proceed to Step 3: Update edge type syntax for 0.3.2

---

**Date**: November 19, 2024
**Version**: LEX-2026.0.3.2
**Status**: ✅ COMPLETE - Clarification received, error identified and documented
**Impact**: Requirements are correct; JSON Schema needs correction (separate task)
