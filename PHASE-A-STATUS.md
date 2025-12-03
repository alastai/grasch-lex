# Phase A Status Report

## Objective
Fix schema to support TI wrappers for single nodeType (Location 6: nodeTypeInterpretation)

## What We Discovered

### Good News
The schema **already has** TI wrapper support for nodeTypes via the `NodeTypeItem` definition!

`NodeTypeItem` (lines 1311-1620) supports:
- ✅ 0-level (bare): Direct `NodeType` reference
- ✅ 1-level shortcuts: `abstract`, `concrete`, `properSubtypesOf`, `final`, `sealed`
- ✅ 2-level explicit: `exactlyOf`, `subtypesOf`
- ✅ Import: `import` for external files

### What We Added
- ✅ 2-level `properSubtypesOf` with concreteness facet (was missing)
  - Added support for `properSubtypesOf: { concrete: ... }` and `properSubtypesOf: { abstract: ... }`

### The Real Problem
**The schema has a pre-existing validation issue that prevents ANY graphSchema from validating!**

Even the simplest possible graphSchema fails:
```yaml
graphSchema:
  graphType:
    nodeTypes:
      - nodeType:
          typeLabel: Person
          implies:
            labels: [Person]
            properties:
              name: STRING
```

Error: `is not valid under any of the given schemas` at root level

## Root Cause Investigation Needed

The validation failure is at the **root level** (the document oneOf), not at the nodeType level. This suggests:

1. **Possible circular reference issue** - The `sealed` wrapper in `NodeTypeItem` references `NodeTypeSetOrImport`, which references `NodeTypesArray`, which contains `NodeTypeItem` - creating a cycle
2. **Schema meta-schema issue** - The validator warns about unsupported `$dynamicRef` features
3. **GraphSchemaContent definition issue** - Something in the GraphSchemaContent definition is preventing validation

## Next Steps

Before continuing with Phase A testing, we need to:

1. **Fix the root validation issue** - Investigate why even simple graphSchemas fail
2. **Test with existing examples** - Run `validate_all_examples.py` to see if this is a regression
3. **Identify the breaking change** - Use git bisect or review recent schema changes

## Phase A Completion Criteria

Once the root issue is fixed, Phase A will be complete when:
- [ ] Simple bare nodeType validates
- [ ] 1-level TI wrappers validate (abstract, concrete, final, sealed, properSubtypesOf)
- [ ] 2-level TI wrappers validate (exactlyOf, subtypesOf, properSubtypesOf with concreteness)
- [ ] Test file `test-phase-a-nodetype-ti.yaml` validates successfully
- [ ] No regressions in existing examples

## Files Created

- `phase_a_fix_nodetype_ti.py` - Initial attempt (incorrect approach)
- `phase_a_fix_nodetype_ti_v2.py` - Corrected approach (added 2-level properSubtypesOf)
- `src/grasch/examples/test-phase-a-nodetype-ti.yaml` - Comprehensive test file
- `validate_phase_a.py` - Validation script
- `test_simple_nodetype.py` - Minimal test to isolate issue
- Various debug scripts

## Recommendation

**PAUSE Phase A** and fix the root validation issue first. The TI wrapper support is already in place; we just need the schema to validate correctly.
