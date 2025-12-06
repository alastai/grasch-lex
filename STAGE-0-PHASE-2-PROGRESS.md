# Stage 0 - Phase 2: Example Updates Progress

**Date**: 2024-12-03  
**Status**: IN PROGRESS

## Completed Tasks

### ✅ Priority 1: Simple Edge Test Files (6 files)

All files updated with correct property ordering:

1. **`test-edge-directed-via.yaml`** - Fixed: `from:` → `to:` → `via:`
2. **`test-edge-directed-arc.yaml`** - Fixed: `from:` → `to:` → `arc:`
3. **`test-edge-directed-typelabel.yaml`** - Fixed: `from:` → `to:` → `typeLabel:`
4. **`test-edge-undirected-via.yaml`** - Fixed: `between:` → `and:` → `via:`
5. **`test-edge-undirected-typelabel.yaml`** - Fixed: `between:` → `and:` → `typeLabel:`
6. **`test-edge-mixed-synonyms.yaml`** - Fixed: All 5 edge definitions with correct ordering

### ✅ Priority 2: Invalid Test Files (2 files)

1. **`test-edge-invalid-multiple-synonyms-INVALID.yaml`** - Verified: Still appropriately invalid
2. **`test-edge-invalid-outside-INVALID.yaml`** - Fixed: File was corrupted, recreated

### ✅ Priority 3: New Test Files (6 files created)

1. **`test-edge-extends-adding.yaml`** - NEW
   - Demonstrates `extends:` without `adding:`
   - Demonstrates `extends:` with `adding:`
   - Shows `adding:` with `propertyTypes:`

2. **`test-edge-inline-nodetype.yaml`** - NEW
   - Demonstrates inline node type definitions at endpoints
   - Shows both directed and undirected examples

3. **`test-edge-property-ordering.yaml`** - NEW
   - Demonstrates correct property ordering with detailed comments
   - Shows both directed and undirected examples
   - Includes all optional properties in correct order

4. **`test-edge-invalid-ordering-INVALID.yaml`** - NEW
   - Demonstrates incorrect property ordering (propertyTypes before via)
   - Should fail validation

5. **`test-edge-invalid-adding-without-extends-INVALID.yaml`** - NEW
   - Demonstrates `adding:` without `extends:`
   - Should fail validation

6. **`test-edge-invalid-implies-with-extends-INVALID.yaml`** - NEW
   - Demonstrates mixing `implies:` with `extends:`
   - Should fail validation

## Remaining Tasks

### Priority 4: Complex Schema Files (4 files)

These files need review and updates:

1. **`lex-2026.0.3.2-type-definition-syntax-examples.yaml`**
   - Need to review all edge type definitions
   - Fix property ordering violations
   - Add `extends:`/`adding:` examples if not present

2. **`lex-2026.0.3.2-snb-schema.yaml`**
   - Large file with many edge types
   - Need systematic review
   - Fix property ordering violations

3. **`lex-2026.0.3.2-finbench-schema.yaml`**
   - Review all edge type definitions
   - Fix property ordering violations

4. **`lex-2026.0.3.2-finbench-sf1-graph.yaml`**
   - Review all edge type definitions
   - Fix property ordering violations

## Summary

- **Files Updated**: 8
- **Files Created**: 6
- **Files Remaining**: 4

## Next Steps

1. Review and update `lex-2026.0.3.2-type-definition-syntax-examples.yaml`
2. Review and update `lex-2026.0.3.2-snb-schema.yaml`
3. Review and update `lex-2026.0.3.2-finbench-schema.yaml`
4. Review and update `lex-2026.0.3.2-finbench-sf1-graph.yaml`
5. Validate all files against schema
6. Document completion

## Notes

- All simple test files now follow correct property ordering
- New test files provide comprehensive coverage of new features
- Invalid test files properly demonstrate constraint violations
- Complex schema files are the final step before validation
