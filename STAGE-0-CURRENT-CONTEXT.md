# Stage 0 - Current Context and Status Report

**Date**: 2024-12-04  
**Session**: Reconnecting after abort  
**Current Phase**: Stage 0, Phase 2 - Critical Issues Identified

## Where We Are

### Overall Context: Phase E of Type Interpretation Implementation

We are in **Stage 0** of **Phase E**, which is the prerequisite work to fix edge type syntax BEFORE implementing the remaining Type Interpretation (TI) locations.

**Phase E Goal**: Implement TI Locations 1-5 (array-level and graph-level TI support)

**Stage 0 Goal**: Fix edge type syntax foundation across schema, examples, and tests

### Phases A-D Status
✅ **COMPLETE** - All passing:
- Phase A: NodeType TI Wrappers
- Phase B: EdgeType TI Wrappers  
- Phase C: Endpoint TI Wrappers (Directed)
- Phase D: Endpoint TI Wrappers (Undirected)

### Phase E Status
⚠️ **IN PROGRESS** - Stage 0 (Edge Syntax Foundation)

## Stage 0 Progress

### Phase 1: Schema Updates ✅ COMPLETE
- JSON Schema updated to enforce property ordering
- `extends:`/`adding:` pattern support added
- `and:` separated from edge label synonym group
- Inline node type definitions supported

### Phase 2: Example Updates ⚠️ PARTIAL - CRITICAL ISSUES FOUND

**What Was Done**:
- ✅ 6 simple edge test files updated with correct property ordering
- ✅ 2 invalid test files verified/fixed
- ✅ 6 new test files created (extends/adding, inline, ordering tests)

**Critical Issues Discovered** (Dec 4, 2024):

#### Issue 1: Inline vs Reference Form Misuse
**Problem**: Simple test files use **inline node type definitions** when they should use **type references**.

**Current (WRONG)**:
```yaml
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
edgeTypes:
  - edgeType:
      directed:
        from: Person  # CORRECT: Type reference
        to: Person    # CORRECT: Type reference
        via: KNOWS
```

**Files Affected**: All 6 simple edge test files

#### Issue 2: Phase E Location 3 Failures Not Investigated
**Problem**: Location 3 test files have multiple serious errors that were dismissed as "pre-existing".

**Files**:
- `test-phase-e-location-3.yaml`
- `test-phase-e-location-3-two-level.yaml`

**Errors Found**:
1. Document structure issues (graphSchema vs catalog/graph)
2. **Edge type syntax errors**: `via:` as object instead of string
3. `implies:` placement errors
4. Unnecessary inline node type definitions

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
        via: KNOWS  # When no implies, via is a string
          implies:  # CORRECT: implies is a child of via
            propertyTypes:  # CORRECT: propertyTypes is a child of implies
            - name: since
              valueType: INTEGER
```

#### Issue 3: Complex Files Not Yet Addressed
**Files Identified** (need systematic updates):
1. `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` (~50+ edge definitions)
2. `lex-2026.0.3.2-snb-schema.yaml`
3. `lex-2026.0.3.2-finbench-schema.yaml`
4. `lex-2026.0.3.2-finbench-sf1-graph.yaml`

## Latest User Correction (Dec 4, 2024)

**NEW CRITICAL ISSUE**: `implies:` nesting structure is WRONG

**User stated**:
> "the labels: and propertyTypes: under implies: should be children of implies:, nested."

**Current (WRONG)**:
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS
  implies:  # At edgeType level
  propertyTypes:  # WRONG: Sibling of implies
  - name: since
    valueType: INTEGER
```

**Should be (CORRECT)**:
```yaml
edgeType:
  directed:
    from: Person
    to: Person
    via: KNOWS
  implies:  # At edgeType level
    propertyTypes:  # CORRECT: Child of implies
    - name: since
      valueType: INTEGER
```

**Impact**: This affects:
- JSON Schema definition of `implies:`
- All example files using `implies:`
- Design documentation
- Test files

## Current Task List

### Immediate Actions Required

1. **Fix `implies:` nesting in JSON Schema**
   - Update schema to require `propertyTypes:` and `labels:` as children of `implies:`
   - Not as siblings

2. **Fix `implies:` nesting in all examples**
   - Simple test files
   - Complex schema files
   - Edge type syntax examples file

3. **Fix inline vs reference form in simple test files**
   - Change all 6 simple test files to use type references
   - Keep inline definitions only in dedicated test file

4. **Investigate and fix Phase E Location 3 files**
   - Fix document structure issues
   - Fix edge type syntax errors
   - Fix `implies:` nesting
   - Change to type references

5. **Update design documentation**
   - Correct all examples to show proper `implies:` nesting
   - Clarify the structure explicitly

## Key Assumptions and Corrections Accumulated

### Edge Type Syntax Rules (Confirmed)

1. **Property Ordering**:
   - Directed: `from:` → `to:` → `via:`/`arc:`/`typeLabel:` → `implies:` OR `extends:`/`adding:`
   - Undirected: `between:` → `and:` → `via:`/`arc:`/`typeLabel:` → `implies:` OR `extends:`/`adding:`

2. **`and:` is NOT a synonym** - It's a distinct required property for undirected edges

3. **Synonym Groups** (mutually exclusive):
   - Edge labels: `via:`, `arc:`, `typeLabel:`
   - Source endpoints: `from:`, `src:`, `source:`, `tail:`
   - Destination endpoints: `to:`, `dst:`, `dest:`, `destination:`, `head:`

4. **Subtyping Options** (mutually exclusive):
   - `implies:` with nested `propertyTypes:` and `labels:`
   - OR `extends:` with optional `adding:` (which has nested `propertyTypes:` and `labels:`)

5. **Endpoint Specifications**:
   - Type reference: Simple string (e.g., `Person`)
   - Inline definition: Object with `nodeType:` key

6. **CRITICAL: `implies:` Structure**:
   - `implies:` is a **child of the edge label property** (`via:`, `arc:`, or `typeLabel:`)
   - `propertyTypes:` and `labels:` are **children** of `implies:`
   - This means `via:` (and synonyms) is an **object**, not a string, when `implies:` is present

## Files Requiring Updates

### High Priority (Immediate)
1. `src/grasch/schemas/lex-2026.0.3.2.schema.json` - Fix `implies:` nesting
2. All 6 simple edge test files - Fix inline vs reference + `implies:` nesting
3. `test-phase-e-location-3.yaml` - Multiple fixes
4. `test-phase-e-location-3-two-level.yaml` - Multiple fixes
5. `.kiro/specs/property-graph-schema/design.md` - Update examples

### Medium Priority (After immediate fixes)
6. `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` - Systematic review
7. `test-edge-extends-adding.yaml` - Fix `implies:` nesting if present
8. `test-edge-property-ordering.yaml` - Fix `implies:` nesting
9. Other new test files - Review for `implies:` nesting

### Lower Priority (Complex schemas)
10. `lex-2026.0.3.2-snb-schema.yaml`
11. `lex-2026.0.3.2-finbench-schema.yaml`
12. `lex-2026.0.3.2-finbench-sf1-graph.yaml`

## Next Steps

**STOP and await user direction** - Do not proceed with changes until user confirms:

1. Understanding of the `implies:` nesting issue
2. Priority order for fixes
3. Whether to fix all issues together or incrementally
4. Any other corrections or clarifications needed

## References

- **Latest Critical Issues**: `STAGE-0-PHASE-2-CRITICAL-ISSUES-IDENTIFIED.md`
- **Phase 2 Completion**: `STAGE-0-PHASE-2-COMPLETION-SUMMARY.md`
- **Baseline Status**: `STAGE-0-BASELINE-STATUS.md`
- **Updated Plan**: `PHASE-E-UPDATED-PLAN.md`
- **Edge Syntax Corrections**: `LEX-2026.0.3.2-EDGE-TYPE-SYNTAX-CORRECTIONS.md`
- **Design Doc**: `.kiro/specs/property-graph-schema/design.md`

## Status Summary

- **Phase**: Stage 0 of Phase E (Edge Syntax Foundation)
- **Sub-phase**: Phase 2 (Example Updates) - CRITICAL ISSUES FOUND
- **Blocking Issue**: `implies:` nesting structure incorrect throughout codebase
- **Action**: STOPPED - Awaiting user direction on how to proceed

