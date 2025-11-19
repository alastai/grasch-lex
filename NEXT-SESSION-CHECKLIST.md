# Next Session Implementation Checklist

## Context Documents to Review
- `LEX-2026.0.3.2-DOCUMENT-TYPES-AND-IMPORTS.md` - Design specification
- `LEX-2026.0.3.2-SCHEMA-GAP-ANALYSIS.md` - Gap analysis
- This checklist

## Key Decisions Made
- ✓ Use `pathName` (mixed case), NOT `pathname`
- ✓ Preserve all `abstract...` and `subTypesOf...` properties (for later work)
- ✓ Wrap all graphSchema examples in `graphSchema:` root
- ✓ Fix graph examples to use `graph:` root
- ✓ Fix catalog examples to use proper reference structure

---

## Phase 1: Update JSON Schema (Priority: CRITICAL)

### 1.1 Fix Top-Level Document Types
- [ ] Change oneOf to use correct root properties:
  - `graph:` (not `pathName + graph`)
  - `graphSchema:` (not `pathName + graphSchema`)
  - `catalog:` (keep as-is)
- [ ] Use `pathName` (mixed case) in all document types
- [ ] Remove old `required` and `properties` at top level (now in oneOf)

### 1.2 Define Graph Document Type
```json
{
  "required": ["graph"],
  "properties": {
    "graph": {
      "type": "object",
      "required": ["pathName"],
      "properties": {
        "pathName": {"type": "string", "pattern": "^/.*"},
        "graphSchema": {...},  // IMPORTABLE - add oneOf
        "graphStorageSchema": {...},  // IMPORTABLE - add oneOf
        "subtypesOfSchemaType": {...}  // PRESERVE - for later
      }
    }
  }
}
```

### 1.3 Define GraphSchema Document Type
```json
{
  "required": ["graphSchema"],
  "properties": {
    "graphSchema": {
      "type": "object",
      "required": ["pathName", "graphType"],
      "properties": {
        "pathName": {"type": "string", "pattern": "^/.*"},
        "graphType": {"$ref": "#/$defs/GraphType"}  // IMPORTABLE - add oneOf
      }
    }
  }
}
```

### 1.4 Update GraphType Definition
- [ ] Add optional `pathName` property
- [ ] Make `nodeTypes` optional (remove from required)
- [ ] Make `edgeTypes` optional (remove from required)
- [ ] Keep `defaults` required with existing oneOf
- [ ] Add import support to `nodeTypes` (oneOf pattern)
- [ ] Add import support to `edgeTypes` (oneOf pattern)

### 1.5 Define Catalog Document Type
```json
{
  "required": ["catalog"],
  "properties": {
    "catalog": {
      "type": "object",
      "required": ["IRI"],
      "properties": {
        "IRI": {"type": "string", "format": "iri"},
        "directories": {...}  // IMPORTABLE - add oneOf, recursive structure
      }
    }
  }
}
```

### 1.6 Define Directory Structure (Recursive)
```json
"Directory": {
  "type": "object",
  "required": ["name"],
  "properties": {
    "name": {"type": "string"},
    "directories": {
      "type": "array",
      "items": {"$ref": "#/$defs/Directory"}
    },
    "graphReferences": {
      "type": "array",
      "items": {"$ref": "#/$defs/GraphReference"}
    },
    "graphSchemaReferences": {
      "type": "array",
      "items": {"$ref": "#/$defs/GraphSchemaReference"}
    }
  }
}
```

### 1.7 Define Reference Types
```json
"GraphReference": {
  "type": "object",
  "required": ["name", "qualifiedName"],
  "properties": {
    "name": {"type": "string"},
    "qualifiedName": {"type": "string"},
    "filePath": {"type": "string"}
  }
},
"GraphSchemaReference": {
  "type": "object",
  "required": ["name", "qualifiedName"],
  "properties": {
    "name": {"type": "string"},
    "qualifiedName": {"type": "string"},
    "filePath": {"type": "string"}
  }
}
```

### 1.8 Add Import Support Pattern (Reusable)
For each IMPORTABLE element, use this oneOf pattern:
```json
{
  "oneOf": [
    {
      "type": "object",
      "description": "Inline definition",
      "properties": {...inline properties...},
      "not": {"required": ["import"]}
    },
    {
      "type": "object",
      "description": "Import only",
      "required": ["import"],
      "properties": {
        "import": {"type": "string"}
      },
      "maxProperties": 1
    },
    {
      "type": "object",
      "description": "Mixed: import with overrides",
      "required": ["import"],
      "properties": {
        "import": {"type": "string"},
        ...inline properties...
      },
      "minProperties": 2
    }
  ]
}
```

### 1.9 Test JSON Schema
- [ ] Validate schema itself is valid JSON Schema
- [ ] Test with simple examples of each document type
- [ ] Verify import patterns work

---

## Phase 2: Update GraphSchema Examples (10 files)

### Files to Update:
1. `lex-2026.0.3.2-all-import-patterns.yaml`
2. `lex-2026.0.3.2-comprehensive-import-example.yaml`
3. `lex-2026.0.3.2-finbench-schema.yaml`
4. `lex-2026.0.3.2-minimal-import-example.yaml`
5. `lex-2026.0.3.2-minimal-test.yaml`
6. `lex-2026.0.3.2-mixed-import-example.yaml`
7. `lex-2026.0.3.2-snb-schema.yaml`
8. `lex-2026.0.3.2-snb-schema-alt.yaml`
9. `lex-2026.0.3.2-snb-special-identification-example.yaml`
10. `lex-2026.0.3.2-type-definition-syntax-examples.yaml`

### Transformation Pattern:
**FROM:**
```yaml
pathName: /path
graphType:
  defaults: ...
  nodeTypes: ...
```

**TO:**
```yaml
graphSchema:
  pathName: /path
  graphType:
    defaults: ...
    nodeTypes: ...
```

### Steps for Each File:
- [ ] Read current content
- [ ] Wrap in `graphSchema:` root
- [ ] Indent all content by 2 spaces
- [ ] Validate against new schema
- [ ] Mark as complete

---

## Phase 3: Update Graph Examples (2 files)

### Files to Update:
1. `lex-2026.0.3.2-complete-import-example.yaml`
2. `lex-2026.0.3.2-finbench-sf1-graph.yaml`

### File 1: complete-import-example.yaml
**Changes:**
- [ ] Remove top-level `pathName`
- [ ] Keep `graph:` root (already correct)
- [ ] Remove redundant `graph: pathName:` (use top-level only)
- [ ] Rename `storageSchema:` to `graphStorageSchema:`
- [ ] PRESERVE `subtypesOfSchemaType:` (for later work)

**FROM:**
```yaml
pathName: /examples/...
graph:
  pathName: "/examples/..."
  subtypesOfSchemaType: ...
  storageSchema: ...
```

**TO:**
```yaml
graph:
  pathName: /examples/...
  subtypesOfSchemaType: ...  # PRESERVED
  graphStorageSchema: ...
```

### File 2: finbench-sf1-graph.yaml
**Changes:**
- [ ] Wrap everything in `graph:` root
- [ ] Keep `pathName` inside graph
- [ ] Rename `storageSchema:` to `graphStorageSchema:`
- [ ] Keep `graphSchema:` and `constraints:` as-is

**FROM:**
```yaml
pathName: /benchmarks/ldbc/finbench-sf1
graphSchema: ...
constraints: ...
storageSchema: ...
```

**TO:**
```yaml
graph:
  pathName: /benchmarks/ldbc/finbench-sf1
  graphSchema: ...
  constraints: ...
  graphStorageSchema: ...
```

---

## Phase 4: Update Catalog Examples (2 files)

### Files to Update:
1. `lex-2026.0.3.2-example-catalog.yaml`
2. `lex-2026.0.3.2-example-catalog-no-iri.yaml`

### Changes for Both Files:
- [ ] Remove top-level `pathName`
- [ ] Keep `catalog:` root
- [ ] Rename `graphSchemas:` to `graphSchemaReferences:`
- [ ] Rename `graphs:` to `graphReferences:`
- [ ] Add `qualifiedName:` to each reference
- [ ] Add optional `filePath:` where appropriate

**FROM:**
```yaml
pathName: /examples/...
catalog:
  IRI: https://...
  directories:
  - name: ldbc
    graphSchemas:
    - name: snb
    graphs:
    - name: snb-sf1
```

**TO:**
```yaml
catalog:
  IRI: https://...
  directories:
  - name: ldbc
    graphSchemaReferences:
    - name: snb
      qualifiedName: /benchmarks/ldbc/snb
      filePath: schemas/snb-schema.yaml
    graphReferences:
    - name: snb-sf1
      qualifiedName: /benchmarks/ldbc/snb-sf1
      filePath: graphs/snb-sf1.yaml
```

---

## Phase 5: Update Other Files (5 files)

### Files to Check:
1. `lex-2026.0.3.2-graph-type-defaults.yaml` - Standalone defaults (no changes needed)
2. `lex-2026.0.3.2-snb-message-hierarchy.yaml` - Partial type definition (check structure)
3. `lex-2026.0.3.2-snb-organisation-hierarchy.yaml` - Partial type definition (check structure)
4. `lex-2026.0.3.2-snb-place-hierarchy.yaml` - Partial type definition (check structure)

### Actions:
- [ ] Verify these are meant to be imported fragments (not standalone documents)
- [ ] If standalone, determine correct document type
- [ ] Update if needed

---

## Phase 6: Validation and Testing

### 6.1 Validate All Examples
- [ ] Run schema validation on all updated examples
- [ ] Fix any validation errors
- [ ] Document any issues

### 6.2 Run Test Suite
- [ ] Run `python -m pytest tests/ -v`
- [ ] Check for failures related to schema changes
- [ ] Update tests if needed (likely in `test_schema_validation.py`)

### 6.3 Check Coverage
- [ ] Verify all 3 document types have working examples
- [ ] Verify all import patterns work
- [ ] Test mixed mode (import + inline)

---

## Phase 7: Documentation Updates

### 7.1 Update Design Document
- [ ] Fix `pathname` to `pathName` in design doc
- [ ] Add note about abstract/subTypesOf being preserved

### 7.2 Update API Design
- [ ] Review `LEX-2026.0.3.2-API-DESIGN.md`
- [ ] Update to reflect new document structure
- [ ] Note any API changes needed

### 7.3 Create Migration Guide
- [ ] Document breaking changes
- [ ] Provide before/after examples
- [ ] List all affected files

---

## Success Criteria

- [ ] JSON Schema validates successfully
- [ ] All 3 document types have correct structure
- [ ] All 14+ examples validate against new schema
- [ ] All tests pass
- [ ] Import mechanism works for all 7 locations
- [ ] abstract/subTypesOf properties preserved

---

## Estimated Time

- Phase 1 (JSON Schema): 2-3 hours
- Phase 2 (GraphSchema examples): 1-2 hours
- Phase 3 (Graph examples): 30 minutes
- Phase 4 (Catalog examples): 30 minutes
- Phase 5 (Other files): 30 minutes
- Phase 6 (Validation): 1 hour
- Phase 7 (Documentation): 30 minutes

**Total: 6-8 hours**

---

## Notes for Next Session

- Start with JSON Schema update (most critical)
- Test incrementally after each phase
- Keep backup of original schema
- Use validation to catch issues early
- Preserve all abstract/subTypesOf properties
- Use pathName (mixed case) everywhere
