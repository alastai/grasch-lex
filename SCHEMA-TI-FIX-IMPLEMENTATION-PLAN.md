# Schema TI Fix - Implementation Plan

## Objective

Fix `src/grasch/schemas/lex-2026.0.3.2.schema.json` to support all 8 TI locations with consistent TI structure options.

## 8 TI Locations to Support

1. **graphTypeInterpretation** - for the graphType property
2. **nodeTypesInterpretation** - for nodeTypes arrays
3. **edgeTypesInterpretation** - for edgeTypes arrays
4. **nodeTypeArrayInterpretation** - for a subsequence within a nodeTypes array
5. **edgeTypeArrayInterpretation** - for a subsequence within an edgeTypes array
6. **nodeTypeInterpretation** - for a single nodeType
7. **edgeTypeInterpretation** - for a single edgeType
8. **edgeTypeEndpointNodeTypeInterpretation** - for from:/to:/between:/and: endpoints

## TI Structure Options (Level 2)

At each location, support:
- **0-level (bare)**: No wrapper - implicit `exactlyOf: concrete:`
- **1-level (shorthand)**: `abstract:`, `concrete:`, `properSubtypesOf:`, `final:`, `sealed:`
- **2-level (explicit)**: `exactlyOf: { concrete: }`, `subtypesOf: { abstract: }`, etc.

## Implementation Strategy - PHASED APPROACH

### Phase A: Single NodeType ⬅️ START HERE
**Goal**: Fix schema to support TI wrappers for a single nodeType

**Scope**:
- Location 6: `nodeTypeInterpretation` - for a single nodeType
- Support 0-level (bare), 1-level (shorthand), 2-level (explicit)
- Test with minimal example

**Steps**:
1. [x] Create reusable TI pattern definitions in `$defs` - Already existed in NodeTypeItem
2. [x] Update `NodeType` definition to support TI wrappers - Added 2-level properSubtypesOf
3. [x] Create minimal test YAML with single nodeType + TI variants - test-phase-a-corrected.yaml
4. [x] Validate test passes - ✅ PASSED
5. [x] Document what was changed - PHASE-A-COMPLETE.md

**Result**: ✅ COMPLETE - Schema already had comprehensive TI support. Added missing 2-level properSubtypesOf wrapper.

**Test Example**:
```yaml
graphSchema:
  graphType:
    nodeTypes:
      - nodeType: {typeLabel: Person}  # 0-level
      - abstract: {nodeType: {typeLabel: Vehicle}}  # 1-level
      - subtypesOf: {abstract: {nodeType: {typeLabel: Entity}}}  # 2-level
```

---

### Phase B: Single EdgeType
**Goal**: Fix schema to support TI wrappers for a single edgeType (no endpoint TIs yet)

**Scope**:
- Location 7: `edgeTypeInterpretation` - for a single edgeType
- Support 0-level, 1-level, 2-level at edgeType level only
- Endpoints use bare nodeType references (no TI)

**Steps**:
1. [x] Update `EdgeType` definition to support TI wrappers - Added 2-level properSubtypesOf
2. [x] Create test YAML with single edgeType + TI variants - test-phase-b-edgetype-ti.yaml
3. [x] Validate test passes - ✅ PASSED
4. [x] Document what was changed - Phase B complete

**Result**: ✅ COMPLETE - Schema already had comprehensive TI support. Added missing 2-level properSubtypesOf wrapper.

**Test Example**:
```yaml
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            from: Person
            via: KNOWS
            to: Person
      - abstract:
          edgeType:
            directed:
              from: Person
              via: MANAGES
              to: Person
```

---

### Phase C: Directed Edge with Endpoint TIs
**Goal**: Fix schema to support TI wrappers on directed edge endpoints

**Scope**:
- Location 8: `edgeTypeEndpointNodeTypeInterpretation` - for from:/to: endpoints
- Support TI wrappers on `from:`, `via:`, `to:` independently
- Test TI override at endpoint level

**Steps**:
1. [ ] Update `DirectedEdgeDescriptor` to support TI on endpoints
2. [ ] Create test YAML with endpoint TI variants
3. [ ] Validate test passes
4. [ ] Document what was changed

**Test Example**:
```yaml
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          directed:
            from:
              abstract: Person  # Endpoint TI
            via: KNOWS
            to:
              subtypesOf:
                concrete: Person  # Endpoint TI
```

---

### Phase D: Undirected Edge with Endpoint TIs
**Goal**: Fix schema to support TI wrappers on undirected edge endpoints

**Scope**:
- Location 8: `edgeTypeEndpointNodeTypeInterpretation` - for between:/and: endpoints
- Support TI wrappers on `between:`, `via:`, `and:` independently
- Test undirected edge patterns

**Steps**:
1. [ ] Update `UndirectedEdgeDescriptor` to support TI on endpoints
2. [ ] Create test YAML with undirected endpoint TI variants
3. [ ] Validate test passes
4. [ ] Document what was changed

**Test Example**:
```yaml
graphSchema:
  graphType:
    edgeTypes:
      - edgeType:
          undirected:
            between:
              abstract: Person  # Endpoint TI
            via: FRIENDS_WITH
            and:
              abstract: Person  # Endpoint TI
```

---

### Phase E: Full Schema Fix (Future)
**Goal**: Complete all 8 TI locations

**Remaining Locations**:
1. graphTypeInterpretation - for the graphType property
2. nodeTypesInterpretation - for nodeTypes arrays
3. edgeTypesInterpretation - for edgeTypes arrays
4. nodeTypeArrayInterpretation - for subsequence in nodeTypes array
5. edgeTypeArrayInterpretation - for subsequence in edgeTypes array

**Steps**: TBD after Phases A-D complete

## Current Schema Issues (from Phase 3 tests)

1. **Multiple TI wrappers not supported** - Schema doesn't allow `nodeTypes` as array of partition blocks
2. **Import in TI content not supported** - Phase 2 imports fail
3. **Sealed with nested nodeTypes not supported** - Sealed wrapper structure incorrect
4. **YAML syntax errors** - Some test files need correction

## Progress Tracking

### Completed Phases
- [x] Phase A: Single NodeType ✅
- [x] Phase B: Single EdgeType ✅
- [ ] Phase C: Directed Edge with Endpoint TIs
- [ ] Phase D: Undirected Edge with Endpoint TIs
- [ ] Phase E: Full Schema Fix (all 8 locations)

### Current Phase
**Phase C: Directed Edge with Endpoint TIs** ⬅️ CURRENT

## Success Criteria

### Phase A-D Success Criteria
- [ ] Each phase's test example validates successfully
- [ ] Schema remains valid JSON after each phase
- [ ] No regressions in existing examples
- [ ] Changes documented in phase completion notes

### Final Success Criteria (Phase E)
- [ ] All 8 TI locations support 0/1/2-level wrappers
- [ ] Phase 3 test files validate successfully
- [ ] All 14 existing examples still validate
- [ ] Schema is valid JSON
- [ ] No regressions in existing functionality

## Session Continuity Notes

**Context Preservation**: This plan documents the phased approach so work can continue across sessions:
- Each phase is self-contained with clear scope
- Test examples demonstrate what must work
- Progress tracking shows what's complete
- Next phase is always clearly identified

## Next Action

**START Phase A**: Fix schema for single nodeType with TI wrappers (Location 6: nodeTypeInterpretation)
