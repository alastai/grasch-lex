# Stage 0 - Phase 2: Example File Updates Plan

**Date**: 2024-12-03  
**Status**: READY TO START  
**Goal**: Update all example/test YAML files to use corrected edge type syntax

## Context

Phase 1 (E.0.1) completed JSON Schema updates. Now we need to update example files to:
1. Test the new schema constraints
2. Fix any property ordering violations
3. Add examples demonstrating new features
4. Ensure all existing examples validate

## Files to Update

### Priority 1: Edge-Specific Test Files (Simple)

These are focused test files that should be quick to update:

1. **`src/grasch/examples/test-edge-directed-via.yaml`**
   - Check property ordering: `from:` → `to:` → `via:` → subtyping → `propertyTypes:`
   - Verify no violations

2. **`src/grasch/examples/test-edge-directed-arc.yaml`**
   - Check property ordering
   - Verify `arc:` synonym usage

3. **`src/grasch/examples/test-edge-directed-typelabel.yaml`**
   - Check property ordering
   - Verify `typeLabel:` synonym usage

4. **`src/grasch/examples/test-edge-undirected-via.yaml`**
   - Check property ordering: `between:` → `and:` → `via:` → subtyping → `propertyTypes:`
   - Verify `and:` is present and used correctly

5. **`src/grasch/examples/test-edge-undirected-typelabel.yaml`**
   - Check property ordering
   - Verify `and:` is present

6. **`src/grasch/examples/test-edge-mixed-synonyms.yaml`**
   - Verify mixed synonym usage is valid
   - Check property ordering

### Priority 2: Invalid Test Files (Should Remain Invalid)

Verify these still fail validation for the right reasons:

7. **`src/grasch/examples/test-edge-invalid-multiple-synonyms-INVALID.yaml`**
   - Should fail: multiple synonyms from same group
   - Verify error message is clear

8. **`src/grasch/examples/test-edge-invalid-outside-INVALID.yaml`**
   - Should fail: properties outside correct context
   - Verify error message is clear

### Priority 3: New Test Files to Create

Create new examples demonstrating new features:

9. **`src/grasch/examples/test-edge-extends-adding.yaml`** (NEW)
   - Demonstrate `extends:`/`adding:` pattern
   - Show `adding:` with `labels:` and `propertyTypes:`
   - Show `extends:` without `adding:`

10. **`src/grasch/examples/test-edge-inline-nodetype.yaml`** (NEW)
    - Demonstrate inline node type definitions at endpoints
    - Show both `from:` and `to:` with inline definitions

11. **`src/grasch/examples/test-edge-property-ordering.yaml`** (NEW)
    - Demonstrate correct property ordering
    - Include comments explaining the order

12. **`src/grasch/examples/test-edge-invalid-ordering-INVALID.yaml`** (NEW)
    - Demonstrate incorrect property ordering
    - Should fail validation

13. **`src/grasch/examples/test-edge-invalid-adding-without-extends-INVALID.yaml`** (NEW)
    - Demonstrate `adding:` without `extends:`
    - Should fail validation

14. **`src/grasch/examples/test-edge-invalid-implies-with-extends-INVALID.yaml`** (NEW)
    - Demonstrate `implies:` mixed with `extends:`
    - Should fail validation

### Priority 4: Complex Schema Files

These are larger files that may need multiple fixes:

15. **`src/grasch/examples/lex-2026.0.3.2-type-definition-syntax-examples.yaml`**
    - Review all edge type definitions
    - Fix property ordering violations
    - Add `extends:`/`adding:` examples if not present

16. **`src/grasch/examples/lex-2026.0.3.2-snb-schema.yaml`**
    - Review all edge type definitions
    - Fix property ordering violations
    - Large file - may have multiple issues

17. **`src/grasch/examples/lex-2026.0.3.2-finbench-schema.yaml`**
    - Review all edge type definitions
    - Fix property ordering violations

18. **`src/grasch/examples/lex-2026.0.3.2-finbench-sf1-graph.yaml`**
    - Review all edge type definitions
    - Fix property ordering violations

## Implementation Strategy

### Step 1: Quick Wins (Priority 1 Files)
- Review and fix simple edge test files
- These should be straightforward
- Validate each file individually as we go

### Step 2: Create New Examples (Priority 3 Files)
- Create new test files demonstrating new features
- These will serve as documentation
- Include clear comments explaining the syntax

### Step 3: Verify Invalid Files (Priority 2 Files)
- Ensure invalid files still fail for correct reasons
- Update if error messages have changed

### Step 4: Complex Files (Priority 4 Files)
- Tackle larger schema files
- May need multiple passes
- Focus on one file at a time

## Validation Approach

For each file:
1. Read the file to understand current structure
2. Identify any issues (property ordering, missing properties, etc.)
3. Make corrections
4. Validate against schema using `validate_examples.py`
5. Document changes made

## Success Criteria

Phase 2 is complete when:
- ✅ All Priority 1 files reviewed and corrected
- ✅ All Priority 3 new files created
- ✅ All Priority 2 invalid files verified
- ✅ All Priority 4 complex files corrected
- ✅ All valid files pass schema validation
- ✅ All invalid files fail for correct reasons
- ✅ Changes documented

## Notes

- DO NOT run full test suite yet (that's Phase 3)
- Focus on schema validation only
- Document any unexpected issues
- Keep changes minimal and focused

## Next Steps After Phase 2

Phase 3 will involve:
- Running full validation suite
- Updating validators if needed
- Regression testing Phases A-D

## References

- Schema: `src/grasch/schemas/lex-2026.0.3.2.schema.json`
- Design Doc: `.kiro/specs/property-graph-schema/design.md`
- Corrections Doc: `LEX-2026.0.3.2-EDGE-TYPE-SYNTAX-CORRECTIONS.md`
