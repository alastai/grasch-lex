# pathName Error Identification

## Issue Summary

The JSON Schema incorrectly includes `pathName` as an optional property on `GraphType`. This is an error that needs to be corrected.

---

## Correct Usage of pathName

| Document Type | Has pathName? | Notes |
|---------------|---------------|-------|
| **catalog** | ❌ NO | Uses `IRI` instead for identification |
| **graphSchema** | ✅ YES | Identity of the schema (e.g., `/benchmarks/ldbc/snb`) |
| **graph** | ✅ YES | Identity of the graph instance (e.g., `/benchmarks/ldbc/snb-sf1`) |
| **graphType** | ❌ NO | Contained within graphSchema; has no independent identity |

---

## Error in JSON Schema

**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
**Line**: 341

**Current (INCORRECT)**:
```json
"GraphType": {
  "type": "object",
  "description": "Graph type descriptor defining the structural graph type",
  "required": ["defaults"],
  "properties": {
    "pathName": {
      "type": "string",
      "description": "Optional path name (only present if graphType is imported)"
    },
    ...
  }
}
```

**Should Be (CORRECT)**:
```json
"GraphType": {
  "type": "object",
  "description": "Graph type descriptor defining the structural graph type",
  "required": ["defaults"],
  "properties": {
    // pathName property should be REMOVED entirely
    "graphPreferredName": {
      ...
    },
    ...
  }
}
```

---

## Verification

### Requirements ✅ CORRECT
- LEX-9 criterion #3: "graphSchema document SHALL require... pathName and graphType"
- LEX-9 criterion #4: "graph instance document SHALL require... pathName and optional graphSchema"
- LEX-9 does NOT mention pathName for graphType
- **Status**: Requirements are already correct

### Examples ✅ CORRECT
Checked multiple examples:
- `lex-2026.0.3.2-snb-schema.yaml`: pathName on graphSchema, NOT on graphType ✅
- `lex-2026.0.3.2-minimal-test.yaml`: pathName on graphSchema, NOT on graphType ✅
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`: pathName on graph, NOT on graphType ✅
- **Status**: All examples are correct

### JSON Schema ❌ INCORRECT
- GraphType definition includes pathName property (line 341)
- Description mentions "only present if graphType is imported" - this is wrong
- **Status**: JSON Schema needs correction

---

## Rationale

**Why graphType should NOT have pathName:**

1. **Identity belongs to the container**: The `pathName` identifies the graphSchema document, not the graphType within it
2. **graphType is not a top-level document**: It's always contained within a graphSchema
3. **No independent existence**: A graphType cannot exist standalone, so it doesn't need its own path identity
4. **Import confusion**: The note "only present if graphType is imported" suggests confusion about import mechanics

**Correct model:**
```yaml
graphSchema:              # This is a document
  pathName: /my/schema    # Document identity
  graphType:              # This is content within the document
    defaults: ...         # No pathName here
    nodeTypes: ...
```

---

## Action Required

### 1. Update JSON Schema ⚠️ HIGH PRIORITY
- Remove `pathName` property from GraphType definition
- File: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
- Line: ~341

### 2. Validate Examples ✅ ALREADY DONE
- Verified examples don't use pathName on graphType
- No changes needed to examples

### 3. Update Documentation
- Requirements: ✅ Already correct (no changes needed)
- Design documents: Update to clarify pathName usage (Phase 3)
- API Design: Update to clarify pathName usage (Phase 3)

---

## Impact Assessment

**Breaking Change**: NO
- Examples already follow correct pattern
- Requirements already specify correct behavior
- Only the JSON Schema validation is too permissive

**Risk**: LOW
- No code changes needed
- No example changes needed
- Only schema validation needs tightening

**Benefit**: HIGH
- Prevents future confusion about pathName usage
- Aligns schema validation with actual requirements
- Clarifies document identity model

---

## Related Requirements

- **LEX-9**: Document Type Discrimination (correctly specifies pathName usage)
- **LEX-10**: Import Patterns (import mechanism doesn't require pathName on graphType)
- **LEX-16**: Catalog References (uses qualifiedName, not pathName)

---

**Date**: November 19, 2024
**Version**: LEX-2026.0.3.2
**Status**: ⚠️ ERROR IDENTIFIED - JSON Schema correction required
**Priority**: HIGH - Incorrect schema definition
