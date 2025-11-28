# Schema Type Interpretation Fix - Implementation Plan

## Design Authority

This implementation plan is based on the authoritative design specification:
- **Primary Design Document**: `.kiro/specs/type-interpretation-wrappers/design.md` (Nov 27, 2024)
- **Requirements Document**: `.kiro/specs/type-interpretation-wrappers/requirements.md`
- **Tasks Document**: `.kiro/specs/type-interpretation-wrappers/tasks.md`

### Design Integration

The Type Interpretation (TI) system integrates with broader Grasch architecture:
- **Schema Architecture**: Defined in `.kiro/specs/property-graph-schema/design.md`
- **Import System**: Coordinated with `.kiro/specs/import-schema-consistency/design.md`
- **Overall Requirements**: `.kiro/specs/property-graph-schema/requirements.md`

### Deprecated Documents

The following documents have been superseded and moved to `archive/deprecated-design-docs/`:
- `TYPE-INTERPRETATION-DESIGN-deprecated-2024-11-19.md` (earlier iteration)
- `type-interpretation-flexibility-design-deprecated-2024-11-19.md` (earlier approach)

## Objective

Fix `src/grasch/schemas/lex-2026.0.3.2.schema.json` to support all 8 TI locations with consistent TI structure options, following the authoritative design in `.kiro/specs/type-interpretation-wrappers/design.md`.

## 8 TI Locations (from Design Document)

Per the authoritative design document, Type Interpretation can be applied at 8 distinct locations:

1. **Location 1**: `graphSchema.graphType.typeInterpretation` (root-level TI)
2. **Location 2**: `graphSchema.graphType.import` (import-level TI)
3. **Location 3**: `graphSchema.graphType.import.typeInterpretation` (import TI content)
4. **Location 4**: `graphSchema.graphType.nodeTypes` (nodeTypes array TI)
5. **Location 5**: `graphSchema.graphType.edgeTypes` (edgeTypes array TI)
6. **Location 6**: Individual `NodeType.typeInterpretation` (single node TI)
7. **Location 7**: Individual `EdgeType.typeInterpretation` (single edge TI)
8. **Location 8**: `EdgeType.endpoints[].typeInterpretation` (endpoint TI)
9. **Location 9**: `EdgeType.endpoints[].directed.typeInterpretation` (directed endpoint TI)

## TI Structure Options (from Design Document)

At each location, the design specifies three wrapper levels:

- **0-level (bare)**: No wrapper - implicit `exactlyOf: concrete:`
- **1-level (shorthand)**: `abstract:`, `concrete:`, `properSubtypesOf:`, `final:`, `sealed:`
- **2-level (explicit)**: `exactlyOf: { concrete: }`, `subtypesOf: { abstract: }`, etc.

### Design Patterns

The design document specifies:
- **Subtype Interpretation Facet**: `subtypeOf`, `properSubtypesOf`, or `exactlyOf`
- **Concreteness Facet**: `abstract`, `concrete`, `final`, or `sealed`
- **Fixed Wrapper Order**: Subtype matching mode (outermost) → concreteness (middle) → property (innermost)
- **No Wrapper Nesting**: Wrappers cannot be nested beyond the 2-level pattern

### Invalid Combinations (Design Constraint)

Per the design document, certain combinations are logically invalid:
- `exactlyOf` + `abstract` (cannot instantiate abstract types exactly)
- Other invalid patterns as defined in the design specification

## Implementation Strategy - PHASED APPROACH

### COMPLETED PHASES (A-D): Locations 6, 7, 8, 9

#### Phase A: Location 6 - Single NodeType ✅ COMPLETE
**Goal**: Fix schema to support TI wrappers for a single nodeType

**Scope**: Location 6 - Individual `NodeType.typeInterpretation`

**Result**: ✅ COMPLETE - Schema already had comprehensive TI support. Added missing 2-level properSubtypesOf wrapper.

**Test File**: `src/grasch/examples/test-phase-a-corrected.yaml`

**Validation Script**: `validate_phase_a.py`

**Documentation**: `PHASE-A-COMPLETE.md`

---

#### Phase B: Location 7 - Single EdgeType ✅ COMPLETE
**Goal**: Fix schema to support TI wrappers for a single edgeType (no endpoint TIs yet)

**Scope**: Location 7 - Individual `EdgeType.typeInterpretation`

**Result**: ✅ COMPLETE - Schema already had comprehensive TI support. Added missing 2-level properSubtypesOf wrapper.

**Test File**: `src/grasch/examples/test-phase-b-edgetype-ti.yaml`

**Validation Script**: `validate_phase_b.py`

**Documentation**: `PHASE-B-EDGETYPE-TI.md`

---

#### Phase C: Location 8 - Undirected Edge Endpoint TIs ✅ COMPLETE
**Goal**: Fix schema to support TI wrappers on undirected edge endpoints

**Scope**: Location 8 - `EdgeType.endpoints[].typeInterpretation` (undirected: between:/and:)

**Result**: ✅ COMPLETE - Implemented TI wrappers for undirected edge endpoints

**Test File**: `src/grasch/examples/test-phase-c-endpoint-ti.yaml`

**Validation Script**: `validate_phase_c.py`

**Implementation Script**: `phase_c_fix_endpoint_ti.py`

---

#### Phase D: Location 9 - Directed Edge Endpoint TIs ✅ COMPLETE
**Goal**: Fix schema to support TI wrappers on directed edge endpoints

**Scope**: Location 9 - `EdgeType.endpoints[].directed.typeInterpretation` (directed: from:/to:)

**Result**: ✅ COMPLETE - Implemented TI wrappers for directed edge endpoints

**Test File**: `src/grasch/examples/test-phase-d-directed-endpoint-ti.yaml`

**Validation Script**: `validate_phase_d.py`

**Documentation**: `PHASES-A-D-COMPLETE.md`

---

### CURRENT PHASE: Phase E - Array Subsequence TIs (Locations 4+5)

#### Phase E: Locations 4+5 - Array Subsequence TIs 🔄 IN PROGRESS
**Goal**: Support TI wrappers for subsequences within nodeTypes/edgeTypes arrays

**Scope**:
- Location 4: `graphSchema.graphType.nodeTypes` (nodeTypes array TI)
- Location 5: `graphSchema.graphType.edgeTypes` (edgeTypes array TI)
- Allows partitioning arrays with different TI semantics per partition

**Key Requirements** (from design document):
- Support 0-level, 1-level, and 2-level TI wrappers for array properties
- Maintain backward compatibility with existing patterns
- Ensure proper canonicalization
- Validate against invalid combinations

**Steps**:
1. [ ] Analyze current array structure in schema
2. [ ] Design partition block syntax following design document patterns
3. [ ] Update schema to support TI-wrapped subsequences
4. [ ] Create test YAML with array partition examples
5. [ ] Validate test passes
6. [ ] Document what was changed

**Implementation Script**: `phase_e_fix_array_subsequence_ti.py`

**Analysis Document**: `PHASE-E-ARRAY-SUBSEQUENCE-ANALYSIS.md`

---

### FUTURE PHASES

#### Phase F: Locations 2+3 - Import-Level TIs
**Goal**: Support TI wrappers for import statements

**Scope**:
- Location 2: `graphSchema.graphType.import` (import-level TI)
- Location 3: `graphSchema.graphType.import.typeInterpretation` (import TI content)
- Coordinate with import system design

**Steps**: TBD - coordinate with `.kiro/specs/import-schema-consistency/design.md`

---

#### Phase G: Location 1 - Root-Level TI
**Goal**: Support TI wrappers for the entire graphType

**Scope**:
- Location 1: `graphSchema.graphType.typeInterpretation` (root-level TI)
- Most complex location - wraps the entire type structure

**Steps**: TBD

---

#### Phase H: Validation and Testing
**Goal**: Comprehensive testing of TI cascade, override, and default behavior

**Scope**:
- TI cascade rules (outer TI → inner TI precedence)
- Default TI semantics (implicit exactlyOf: concrete:)
- Override behavior at different nesting levels
- Complex nested scenarios with all 8 TI locations

**Steps**: TBD

---

#### Phase I: Documentation and Examples
**Goal**: Complete documentation and comprehensive examples

**Scope**:
- Update all design documents
- Create comprehensive example files
- Document canonicalization process
- Integration with broader Grasch architecture

**Steps**: TBD

## Current Schema Issues (from Phase 3 tests)

1. **Multiple TI wrappers not supported** - Schema doesn't allow `nodeTypes` as array of partition blocks
2. **Import in TI content not supported** - Phase 2 imports fail
3. **Sealed with nested nodeTypes not supported** - Sealed wrapper structure incorrect
4. **YAML syntax errors** - Some test files need correction

## Progress Tracking

### Completed Phases
- [x] **Phase A**: Location 6 - Single NodeType ✅
- [x] **Phase B**: Location 7 - Single EdgeType ✅
- [x] **Phase C**: Location 8 - Undirected Edge Endpoint TIs ✅
- [x] **Phase D**: Location 9 - Directed Edge Endpoint TIs ✅

### Current Phase
- 🔄 **Phase E**: Locations 4+5 - Array Subsequence TIs (IN PROGRESS)

### Future Phases
- [ ] **Phase F**: Locations 2+3 - Import-Level TIs
- [ ] **Phase G**: Location 1 - Root-Level TI
- [ ] **Phase H**: Validation and Testing
- [ ] **Phase I**: Documentation and Examples

## Design Compliance

This implementation strictly follows:
- **Architecture**: Single-schema approach with canonicalization (pre-canonical and canonical forms)
- **Patterns**: 0/1/2-level wrapper hierarchy as specified in design document
- **Validation**: JSON Schema enforcement of design constraints
- **Integration**: Coordination with import preprocessing and broader schema architecture

All changes maintain consistency with the broader Grasch design as specified in `.kiro/specs/property-graph-schema/design.md` and related specifications.

## Success Criteria

### Phases A-D Success Criteria ✅ ACHIEVED
- [x] Each phase's test example validates successfully
- [x] Schema remains valid JSON after each phase
- [x] No regressions in existing examples
- [x] Changes documented in phase completion notes

### Phase E Success Criteria (Current)
- [ ] Array-level TI wrappers support 0/1/2-level patterns
- [ ] Test examples validate successfully
- [ ] Backward compatibility maintained
- [ ] Canonicalization works correctly

### Final Success Criteria (All Phases)
- [ ] All 8 TI locations support 0/1/2-level wrappers per design document
- [ ] All test files validate successfully
- [ ] All existing examples still validate
- [ ] Schema is valid JSON
- [ ] No regressions in existing functionality
- [ ] Design document patterns fully implemented

## Files and Artifacts

### Schema Files
- `src/grasch/schemas/lex-2026.0.3.2.schema.json` (main schema)
- `src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json` (pre-import schema)

### Phase Implementation Files
- `phase_a_fix_nodetype_ti.py` (Location 6)
- `phase_b_fix_edgetype_ti.py` (Location 7)
- `phase_c_fix_endpoint_ti.py` (Location 8)
- `validate_phase_d.py` (Location 9)
- `phase_e_fix_array_subsequence_ti.py` (Locations 4+5) - **CURRENT**

### Test Files
- `src/grasch/examples/test-phase-a-corrected.yaml`
- `src/grasch/examples/test-phase-b-edgetype-ti.yaml`
- `src/grasch/examples/test-phase-c-endpoint-ti.yaml`
- `src/grasch/examples/test-phase-d-directed-endpoint-ti.yaml`

### Validation Scripts
- `validate_phase_a.py`
- `validate_phase_b.py`
- `validate_phase_c.py`
- `validate_phase_d.py`

## Session Continuity Notes

**Context Preservation**: This plan documents the phased approach so work can continue across sessions:
- Each phase is self-contained with clear scope
- Test examples demonstrate what must work
- Progress tracking shows what's complete
- Next phase is always clearly identified
- Design authority is explicitly documented

## Next Action

**CONTINUE Phase E**: Implement array subsequence TI wrappers (Locations 4+5) following the authoritative design patterns in `.kiro/specs/type-interpretation-wrappers/design.md`
