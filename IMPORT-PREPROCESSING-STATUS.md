# Import Preprocessing Status

## Current Situation

### ✅ What's Working
1. **Import preprocessor exists** (`src/grasch/import_preprocessor.py`) and is functional
2. **Validation script updated** to use two-phase validation:
   - Phase 1: Validate raw files (with `import:` statements)
   - Phase 2: Preprocess imports and validate resolved files
3. **Raw validation passes**: All 14 files validate successfully with imports
4. **Preprocessing works**: Import resolution is functioning correctly

### ❌ What's Not Working
**Preprocessed validation fails** because we're using the same schema for both phases.

**The Problem**: The current JSON Schema (`lex-2026.0.3.2.schema.json`) allows `import:` statements using oneOf patterns. When we preprocess files and resolve imports, the `import:` keys are removed and replaced with actual content. But the schema still expects the oneOf pattern (either inline content OR import), so the fully-resolved content doesn't validate correctly.

---

## The Solution: Two-Schema Approach

### Schema 1: Pre-Import Schema (Current)
**File**: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
**Purpose**: Validate raw YAML files that may contain `import:` directives
**Allows**: 
- `import:` keys in IMPORTABLE elements
- oneOf patterns: inline | import-only | mixed

### Schema 2: Post-Import Schema (NEEDED)
**File**: `src/grasch/schemas/lex-2026.0.3.2-post-import.schema.json` (to be created)
**Purpose**: Validate fully-resolved documents after import preprocessing
**Does NOT allow**:
- No `import:` keys anywhere
- Only inline content (no oneOf patterns for imports)

---

## IMPORTABLE Elements (Need Two Versions)

According to LEX-2026.0.3.2-DOCUMENT-TYPES-AND-IMPORTS.md, these elements support imports:

1. **defaults** (in GraphType)
2. **nodeTypes** (array in GraphType)
3. **edgeTypes** (array in GraphType)
4. **directories** (array in Catalog)
5. **graphSchema** (in Graph document)
6. **graphStorageSchema** (in Graph document)
7. **graphType** (in GraphSchema document)

Each of these has a oneOf pattern in the pre-import schema:
```json
"oneOf": [
  {"type": "array/object", ...},  // Inline
  {"required": ["import"], "maxProperties": 1},  // Import-only
  {"required": ["import"], "minProperties": 2}   // Mixed
]
```

In the post-import schema, these should just be:
```json
{"type": "array/object", ...}  // Only inline, no import option
```

---

## Current Validation Results

### Raw Validation (Phase 1): ✅ 14/14 PASS
All files validate with imports present.

### Preprocessed Validation (Phase 2): ❌ 3/14 PASS
- ✅ 2 Catalog documents (no imports to resolve)
- ❌ 12 documents with imports (fail because schema still expects import patterns)

**Files failing preprocessed validation**:
1. lex-2026.0.3.2-all-import-patterns.yaml
2. lex-2026.0.3.2-complete-import-example.yaml
3. lex-2026.0.3.2-comprehensive-import-example.yaml
4. lex-2026.0.3.2-finbench-schema.yaml
5. lex-2026.0.3.2-finbench-sf1-graph.yaml
6. lex-2026.0.3.2-minimal-import-example.yaml
7. lex-2026.0.3.2-minimal-test.yaml
8. lex-2026.0.3.2-mixed-import-example.yaml
9. lex-2026.0.3.2-snb-schema.yaml
10. lex-2026.0.3.2-snb-special-identification-example.yaml
11. lex-2026.0.3.2-subtype-abstract-test.yaml
12. lex-2026.0.3.2-type-definition-syntax-examples.yaml

---

## Next Steps

### Option 1: Create Post-Import Schema (Recommended)
1. Copy `lex-2026.0.3.2.schema.json` to `lex-2026.0.3.2-post-import.schema.json`
2. Remove all oneOf patterns for IMPORTABLE elements
3. Keep only the inline content option
4. Update validation script to use post-import schema for phase 2
5. Verify all 14 files pass both phases

### Option 2: Modify Existing Schema (Not Recommended)
Make the schema accept both patterns (with and without imports) - this is complex and error-prone.

---

## Implementation Plan for Option 1

### Step 1: Create Post-Import Schema
```bash
cp src/grasch/schemas/lex-2026.0.3.2.schema.json \
   src/grasch/schemas/lex-2026.0.3.2-post-import.schema.json
```

### Step 2: Modify Post-Import Schema
For each IMPORTABLE element, change from:
```json
"oneOf": [
  {"type": "object", "properties": {...}},
  {"required": ["import"]},
  {"required": ["import"], "minProperties": 2}
]
```

To:
```json
{"type": "object", "properties": {...}}
```

**Elements to modify**:
1. GraphType.defaults
2. GraphType.nodeTypes
3. GraphType.edgeTypes
4. CatalogContent.directories
5. GraphContent.graphSchema
6. GraphContent.graphStorageSchema
7. GraphSchemaContent.graphType

### Step 3: Update Validation Script
```python
# Load both schemas
pre_import_schema = load_schema("lex-2026.0.3.2.schema.json")
post_import_schema = load_schema("lex-2026.0.3.2-post-import.schema.json")

# Phase 1: Validate raw with pre-import schema
validate_file(yaml_file, pre_import_schema, ...)

# Phase 2: Validate preprocessed with post-import schema
validate_file(yaml_file, post_import_schema, ..., preprocess=True)
```

### Step 4: Test
Run validation and verify all 14 files pass both phases.

---

## Expected Final Result

```
Total files: 14
Phase 1 (Raw): 14/14 PASS ✅
Phase 2 (Preprocessed): 14/14 PASS ✅
Overall: 14/14 PASS ✅
```

---

**Date**: November 19, 2024
**Status**: ⚠️ Import preprocessing implemented but needs post-import schema
**Priority**: HIGH - Required for proper validation
**Recommendation**: Create post-import schema (Option 1)
