# Stage 0 - Phase 2: Critical Issues Identified

**Date**: 2024-12-03  
**Status**: WORK NOT COMPLETE - Critical issues found

## Issue 1: Unnecessary Inline Node Type Definitions

### Problem
The simple edge test files are using **inline node type definitions** when they should use **type reference by label**.

### Examples of the Problem

**Current (WRONG)**:
```yaml
nodeTypes:
  - nodeType:
      typeLabel: Person

edgeTypes:
  - edgeType:
      directed:
        from:
          nodeType:
            typeLabel: Person  # WRONG: Inline definition
        to:
          nodeType:
            typeLabel: Person  # WRONG: Inline definition
        via: KNOWS
```

**Should be (CORRECT)**:
```yaml
nodeTypes:
  - nodeType:
      typeLabel: Person

edgeTypes:
  - edgeType:
      directed:
        from: Person  # CORRECT: Type reference
        to: Person    # CORRECT: Type reference
        via: KNOWS
```

### Why This Matters
- **Inline form** should only be used when defining a node type that doesn't exist in `nodeTypes`
- **Type reference form** should be used when referencing an already-defined type
- The simple test files are meant to test edge syntax, not inline node type definitions
- We have a dedicated file `test-edge-inline-nodetype.yaml` for testing inline definitions

### Files Affected
All simple edge test files:
1. `test-edge-directed-via.yaml`
2. `test-edge-directed-arc.yaml`
3. `test-edge-directed-typelabel.yaml`
4. `test-edge-undirected-via.yaml`
5. `test-edge-undirected-typelabel.yaml`
6. `test-edge-mixed-synonyms.yaml`

### Action Required
Change all endpoint specifications from inline form to type reference form.

---

## Issue 2: Phase E Location 3 Failures Not Properly Investigated

### Problem
The baseline status document reports Phase E Location 3 test failures but dismisses them as "pre-existing" without proper investigation.

### The Failures
**Files**:
- `test-phase-e-location-3.yaml`
- `test-phase-e-location-3-two-level.yaml`

**Error**:
```
'catalog' is a required property
Additional properties are not allowed ('graphSchema' was unexpected)
'graph' is a required property
```

### Root Cause Analysis

#### Issue 2a: Document Structure
The files use `graphSchema:` at the root, but the error suggests they should use `catalog:` and `graph:` instead. This indicates:
- These files may be using the wrong document type
- OR the schema validation is checking against the wrong document type
- This needs investigation - what document type should Location 3 tests use?

#### Issue 2b: Edge Type Syntax Errors
Looking at the files, there are **serious edge type syntax errors**:

**Current (WRONG)**:
```yaml
edgeTypes:
  - edgeType:
      typeLabel: KNOWS
      directed:
        from:
          nodeType:
            typeLabel: Person
        to:
          nodeType:
            typeLabel: Person
        via:  # WRONG: via should be a string, not an object
          implies:
            propertyTypes:
              - name: since
                valueType: INTEGER
```

**Should be (CORRECT)**:
```yaml
edgeTypes:
  - edgeType:
      directed:
        from: Person
        to: Person
        via: KNOWS  # CORRECT: via is a string label
      implies:  # CORRECT: implies is at edgeType level
        propertyTypes:
          - name: since
            valueType: INTEGER
```

#### Issue 2c: Inline Node Types (Again)
These files also use inline node type definitions unnecessarily.

### Why This Matters
- These are **not** pre-existing issues unrelated to edge syntax
- These files have **multiple edge syntax errors** that need fixing
- The document structure issue may indicate a deeper problem
- We cannot claim Phase 2 is complete with these files broken

### Action Required
1. Investigate what document type Location 3 tests should use
2. Fix the edge type syntax errors (via: should be string, implies: at correct level)
3. Change inline node types to type references
4. Re-validate these files
5. Understand why they were passing before (if they were)

---

## Issue 3: Property Ordering in Location 3 Files

### Problem
Even after fixing the `via:` syntax, these files have property ordering issues:

**Current**:
```yaml
edgeType:
  typeLabel: KNOWS  # typeLabel at edgeType level
  directed:
    from: Person
    to: Person
    via: KNOWS  # This would be redundant with typeLabel above
```

**Questions**:
- Should `typeLabel` be at `edgeType` level or inside `directed:`?
- If at `edgeType` level, is `via:` inside `directed:` redundant?
- What's the correct pattern for Location 3 tests?

---

## Summary

### Work Status: NOT COMPLETE

The Phase 2 work cannot be considered complete because:

1. ✅ Property ordering was fixed in simple files
2. ❌ But simple files use wrong form (inline vs reference)
3. ❌ Phase E Location 3 files have multiple serious errors
4. ❌ Phase E Location 3 failures were not properly investigated
5. ❌ Document structure issues not understood

### Next Steps (Revised)

1. **Fix simple test files**: Change inline node types to type references
2. **Investigate Location 3 document structure**: Understand catalog vs graphSchema
3. **Fix Location 3 edge syntax**: Correct via: and implies: placement
4. **Fix Location 3 node types**: Change to type references
5. **Validate all files**: Ensure they actually pass schema validation
6. **Document findings**: Understand what was wrong and why

### Lessons Learned

- Don't dismiss test failures as "pre-existing" without investigation
- Check that fixes use the correct form (reference vs inline)
- Validate files actually pass, don't just assume they will
- Read error messages carefully - they often indicate multiple issues

---

## References

- Baseline Status: `STAGE-0-BASELINE-STATUS.md`
- Edge Syntax Corrections: `LEX-2026.0.3.2-EDGE-TYPE-SYNTAX-CORRECTIONS.md`
- Design Doc: `.kiro/specs/property-graph-schema/design.md`
