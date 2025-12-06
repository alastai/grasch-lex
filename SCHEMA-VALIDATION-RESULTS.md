# LEX-2026.0.3.2 Schema Validation Results

## Overview

This validation uses the single LEX-2026.0.3.2 schema which validates both:
- **Pre-canonical form**: Files with convenience syntax (wrappers, imports, etc.)
- **Canonical form**: Files after canonicalization (normalized, imports resolved)

**Total files tested:** 14

**Valid:** 12

**Invalid:** 2

**Pre-canonical files:** 12

**Canonical files:** 2

## ✅ Valid Files

- lex-2026.0.3.2-minimal-test.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-complete-import-example.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-comprehensive-import-example.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-example-catalog-no-iri.yaml
  - Canonical validation: **passed**
- lex-2026.0.3.2-example-catalog.yaml
  - Canonical validation: **passed**
- lex-2026.0.3.2-finbench-schema.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-finbench-sf1-graph.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-minimal-import-example.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-mixed-import-example.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-snb-schema.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-snb-special-identification-example.yaml
  - Pre-canonical validation: **passed**
- lex-2026.0.3.2-subtype-abstract-test.yaml
  - Pre-canonical validation: **passed**

## ❌ Invalid Files

### lex-2026.0.3.2-all-import-patterns.yaml

  Path:  - {'graphSchema': {'pathName': '/examples/all-import-patterns', 'graphType': {'propertyGraphDataModel': {'import': 'imports/lex-2026.0.3.2-property-graph-data-model.yaml'}, 'nodeTypes': {'import': 'imports/lex-2026.0.3.2-node-type-syntax-examples.yaml'}, 'edgeTypes': {'import': 'imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml'}}}} is not valid under any of the given schemas

### lex-2026.0.3.2-type-definition-syntax-examples.yaml

  Path:  - {'graphSchema': {'pathName': '/examples/type-definition-syntax', 'graphType': {'propertyGraphDataModel': {'import': 'imports/lex-2026.0.3.2-property-graph-data-model.yaml'}, 'nodeTypes': {'import': 'imports/lex-2026.0.3.2-node-type-syntax-examples.yaml'}, 'edgeTypes': {'import': 'imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml'}}}} is not valid under any of the given schemas

