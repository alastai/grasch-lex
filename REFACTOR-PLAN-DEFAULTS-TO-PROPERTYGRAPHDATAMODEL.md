# Refactor Plan: defaults → propertyGraphDataModel

## Changes Required

### 1. Terminology Changes
- **Rename**: `defaults` → `propertyGraphDataModel`
- **Move**: `valueTypeSystemName` from `graphSchema` level into `propertyGraphDataModel`

### 2. Structure Change

**Before**:
```yaml
graphSchema:
  pathName: /example
  valueTypeSystemName: GQL  # <-- At graphSchema level
  graphType:
    defaults:  # <-- Old name
      graphPreferredName: GRAPH
      nodePreferredName: NODE
      # ... other settings
```

**After**:
```yaml
graphSchema:
  pathName: /example
  graphType:
    propertyGraphDataModel:  # <-- New name
      valueTypeSystemName: GQL  # <-- Moved inside
      graphPreferredName: GRAPH
      nodePreferredName: NODE
      # ... other settings
```

## Files to Update

### A. JSON Schema Files
1. `src/grasch/schemas/lex-2026.0.3.2.schema.json`
2. `src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json`

### B. Import Files
1. `src/grasch/examples/imports/lex-2026.0.3.2-graph-type-defaults.yaml`
   - Already has `valueTypeSystemName` - good!
   - Just needs to be referenced as `propertyGraphDataModel` in importers

### C. Example YAML Files (14 files)
All files in `src/grasch/examples/` that use `defaults:` or `valueTypeSystemName`

### D. Documentation
- Update any docs that reference `defaults`

## Execution Order

1. Update JSON schemas first
2. Update import files
3. Update all example files
4. Run validation to verify
5. Update documentation

## Search Patterns

- Find `defaults:` in YAML files
- Find `valueTypeSystemName:` at graphSchema level
- Find `"defaults"` in JSON schemas
- Find references in documentation

