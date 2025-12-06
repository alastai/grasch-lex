# Tasks 4 & 6 Progress Update

**Date**: 2024-12-06  
**Status**: PARTIAL COMPLETION - 11 of 24 files updated

## Completed Files (11/24)

### Initial 8 Files ✅ (Task 6 - Initial)
1. test-edge-directed-via.yaml
2. test-edge-directed-arc.yaml
3. test-edge-directed-typelabel.yaml
4. test-edge-undirected-via.yaml
5. test-edge-undirected-typelabel.yaml
6. test-edge-mixed-synonyms.yaml
7. test-edge-property-ordering.yaml
8. test-edge-extends-adding.yaml

### Additional 3 Files ✅ (Subtask 6.2)
9. test-siblings-bare-only.yaml
10. test-siblings-complex.yaml
11. test-siblings-interleaved.yaml

**All 11 files validate successfully against updated schema.**

## Remaining Files (13/24)

### High Priority - Test Files (7 files)
These test specific functionality and should be updated:

1. **test-phase-b-edgetype-ti.yaml** - Phase B: EdgeType TI wrappers (12 edges to update)
2. **test-phase-e-locations-4-5.yaml** - Phase E: Array-level TI
3. **test-edge-invalid-adding-without-extends-INVALID.yaml** - Negative test
4. **test-edge-invalid-implies-with-extends-INVALID.yaml** - Negative test  
5. **test-edge-invalid-ordering-INVALID.yaml** - Negative test
6. **test-edge-invalid-multiple-synonyms-INVALID.yaml** - Negative test
7. **test-edge-inline-nodetype.yaml** - Tests endpoint polymorphism

### Medium Priority - Example Schema Files (6 files)
Large schema files with many edges:

8. **lex-2026.0.3.2-minimal-test.yaml** - Basic example
9. **lex-2026.0.3.2-finbench-schema.yaml** - FinBench benchmark (~9 edges)
10. **lex-2026.0.3.2-snb-schema.yaml** - SNB benchmark (~15 edges)
11. **lex-2026.0.3.2-subtype-abstract-test.yaml** - Subtyping examples (~5 edges)
12. **lex-2026.0.3.2-minimal-import-example.yaml** - Import example
13. **lex-2026.0.3.2-mixed-import-example.yaml** - Mixed imports

## Git Commits

- `11a8af7` - Initial schema changes and 8 test files
- `f7a98c6` - Mark tasks complete (reverted)
- `6d02592` - Revert to incomplete, add subtasks
- `f0812be` - Update 3 test-siblings files

## Next Steps

1. **Complete test-phase-b-edgetype-ti.yaml** - Most complex test file (12 edges)
2. **Update remaining test files** (6 files) - Critical for test coverage
3. **Update example schema files** (6 files) - Important for documentation
4. **Final validation** - Run comprehensive validation on all 24 files
5. **Mark tasks complete** - Update tasks.md when all files validated

## Estimated Remaining Work

- Test files: ~30-45 minutes (7 files, varying complexity)
- Example schemas: ~45-60 minutes (6 files, many edges each)
- Validation & documentation: ~15 minutes

**Total remaining: ~1.5-2 hours**

## Pattern for Updates

For each file with edgeTypes:
1. Change `via: LABEL` to `via: { typeLabel: LABEL }`
2. Move `implies:` from edgeType level to inside `via:` object
3. Move `extends:` and `adding:` to inside `via:` object (if present)
4. Simplify endpoints from inline nodeType to string references (where appropriate)
5. Validate file passes schema validation

## Success Criteria

- [ ] All 24 files with edgeTypes updated
- [ ] All updated files pass schema validation
- [ ] No regression in existing passing tests
- [ ] Tasks 4 and 6 marked complete in tasks.md
- [ ] Changes committed and pushed to GitHub
