# LEX-2026.0.3.2 Schema Update Status

## Summary
- **Total files**: 13
- **Valid**: 6 (46%)
- **Invalid**: 7 (54%)

## Completed Work

### Phase 1: JSON Schema Updates ✅ COMPLETE
- Updated top-level document types to use `catalog:`, `graphSchema:`, and `graph:` roots
- Added import support to all 7 importable locations
- Updated GraphType to make nodeTypes/edgeTypes optional
- Added pathName property to GraphType
- Updated catalog structure with graphReferences and graphSchemaReferences
- Kept Constraint and ConstraintRule definitions

### Phase 2: Example File Updates ⏳ IN PROGRESS

#### Valid Files (6):
1. ✅ lex-2026.0.3.2-all-import-patterns.yaml
2. ✅ lex-2026.0.3.2-complete-import-example.yaml
3. ✅ lex-2026.0.3.2-example-catalog-no-iri.yaml
4. ✅ lex-2026.0.3.2-example-catalog.yaml
5. ✅ lex-2026.0.3.2-finbench-sf1-graph.yaml
6. ✅ lex-2026.0.3.2-minimal-test.yaml

#### Invalid Files (7):
1. ❌ lex-2026.0.3.2-comprehensive-import-example.yaml - YAML parsing error
2. ❌ lex-2026.0.3.2-finbench-schema.yaml - Schema validation error
3. ❌ lex-2026.0.3.2-minimal-import-example.yaml - Schema validation error
4. ❌ lex-2026.0.3.2-mixed-import-example.yaml - Schema validation error
5. ❌ lex-2026.0.3.2-snb-schema.yaml - YAML parsing error
6. ❌ lex-2026.0.3.2-snb-special-identification-example.yaml - Schema validation error
7. ❌ lex-2026.0.3.2-type-definition-syntax-examples.yaml - Schema validation error

## Changes Made

### Schema Changes:
- Restructured top-level oneOf to require `catalog:`, `graphSchema:`, or `graph:` roots
- Created CatalogContent, GraphSchemaContent, GraphContent definitions
- Updated Directory structure with graphReferences and graphSchemaReferences
- Added import oneOf patterns to: graphSchema, graphStorageSchema, nodeTypes, edgeTypes, directories
- Made nodeTypes and edgeTypes optional in GraphType
- Added optional pathName to GraphType

### Example File Changes:
- Updated catalog files to use new reference structure (graphReferences, graphSchemaReferences)
- Added required qualifiedName fields to all references
- Wrapped graph examples in `graph:` root
- Wrapped graphSchema examples in `graphSchema:` root
- Fixed numerous YAML indentation issues
- Renamed storageSchema to graphStorageSchema in graph files

## Remaining Issues

### Common Problems:
1. **YAML indentation errors** - nodeTypes/edgeTypes items not properly indented under graphType
2. **Missing defaults** - Some graphType definitions missing required defaults property
3. **Constraint indentation** - Constraint definitions have incorrect indentation
4. **Import syntax** - Some files have malformed import statements

### Next Steps:
1. Fix remaining YAML parsing errors in comprehensive-import-example and snb-schema
2. Fix schema validation errors in the 5 remaining invalid files
3. Ensure all graphType definitions have required defaults
4. Verify all nodeType/edgeType structures are properly nested
5. Run full validation suite

## Notes
- Archived lex-2026.0.3.2-snb-schema-alt.yaml
- Preserved Constraint and ConstraintRule definitions (not removed)
- All changes maintain backward compatibility where possible
