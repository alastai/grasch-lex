# Reorganize Imports Plan

## Goal
Move all importable YAML fragments to `src/grasch/examples/imports/` directory and update all import references.

---

## Files to Move

### Already in imports/ ✅
- `lex-2026.0.3.2-graph-type-defaults.yaml`

### Need to Move to imports/
1. `lex-2026.0.3.2-node-type-syntax-examples.yaml` - nodeTypes fragment
2. `lex-2026.0.3.2-edge-type-syntax-examples.yaml` - edgeTypes fragment

### Subdirectory to Move
- `lex-2026.0.3.2-snb-types/` → `imports/snb-types/`

---

## Top-Level Documents (Stay in examples/)

### Catalog Documents
- `lex-2026.0.3.2-example-catalog.yaml`
- `lex-2026.0.3.2-example-catalog-no-iri.yaml`

### GraphSchema Documents
- `lex-2026.0.3.2-all-import-patterns.yaml`
- `lex-2026.0.3.2-comprehensive-import-example.yaml`
- `lex-2026.0.3.2-finbench-schema.yaml`
- `lex-2026.0.3.2-minimal-import-example.yaml`
- `lex-2026.0.3.2-minimal-test.yaml`
- `lex-2026.0.3.2-mixed-import-example.yaml`
- `lex-2026.0.3.2-snb-schema.yaml`
- `lex-2026.0.3.2-snb-special-identification-example.yaml`
- `lex-2026.0.3.2-subtype-abstract-test.yaml`
- `lex-2026.0.3.2-type-definition-syntax-examples.yaml`

### Graph Documents
- `lex-2026.0.3.2-complete-import-example.yaml`
- `lex-2026.0.3.2-finbench-sf1-graph.yaml`

---

## Import Path Updates

### Pattern 1: defaults import (many files)
**Old**: `import: lex-2026.0.3.2-graph-type-defaults.yaml`
**New**: `import: imports/lex-2026.0.3.2-graph-type-defaults.yaml`

### Pattern 2: snb_types directory
**Old**: `import: snb_types/...`
**New**: `import: imports/snb-types/...`

### Pattern 3: Direct snb-types references
**Old**: `import: lex-2026.0.3.2-snb-types/...`
**New**: `import: imports/snb-types/...`

---

## Steps

1. ✅ Create plan document
2. Move node-type-syntax-examples to imports/
3. Move edge-type-syntax-examples to imports/
4. Move lex-2026.0.3.2-snb-types/ to imports/snb-types/
5. Update all import: references in top-level documents
6. Update validation script to only validate top-level documents
7. Run validation regression test
8. Verify all documents still validate

---

## Validation Script Updates

**Current**: Validates all .yaml files in examples/
**New**: Should only validate top-level documents (exclude imports/ directory)

**Files to validate** (12 total):
- 2 catalog documents
- 9 graphSchema documents  
- 2 graph documents (one is complete-import-example)

---

**Status**: Ready to execute
