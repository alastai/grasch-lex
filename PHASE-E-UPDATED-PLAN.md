# Phase E Implementation Plan: UPDATED with Edge Type Syntax Corrections

**Date**: 2024-12-03  
**Status**: UPDATED - Integrating Edge Type Syntax Corrections  
**Goal**: Complete Phase E (Locations 1-5) with correct edge type syntax throughout

## Context

### Phases A-D Status
✅ **COMPLETE** - Locations 6-9 implemented and tested

### Phase E Original Scope
Implement Locations 1-5 (array-level and graph-level TI support)

### NEW: Edge Type Syntax Corrections Integration

**Critical Discovery**: During Phase E work, we identified systematic edge type syntax errors that must be corrected.

**Impact on Phase E**: Since Phase E involves edge types (Locations 3, 5, 7, 8, 9), we must integrate edge syntax corrections.

## Edge Type Syntax Corrections Summary

### Key Corrections
1. **`and:` is NOT a synonym** - Distinct required property for undirected edges
2. **Property ordering rules** - Endpoints → `via:` → subtyping → `propertyTypes:`
3. **Subtyping options** - `implies:` XOR (`extends:`/`adding:`)
4. **Endpoint specifications** - Type references OR inline node type definitions
5. **Synonym groups** - Three distinct mutually exclusive groups

### Documentation Status
✅ **Design Document Updated** - Comprehensive edge type syntax specification added
✅ **Implementation Plan Created** - Detailed change analysis document created

## Integrated Phase E Implementation Stages

### Stage 0: Edge Type Syntax Foundation (NEW - PREREQUISITE)
**Goal**: Fix edge type syntax in schema and core examples BEFORE implementing remaining TI locations

**Why First**: Locations 3, 5, 7, 8, 9 all involve edge types - must have correct syntax first

**Tasks**:
1. Update JSON Schema for correct edge type syntax
2. Fix core edge type examples
3. Update edge type validators
4. Test Phases A-D regression

**Deliverables**: 📄 `PHASE-E-STAGE-0-EDGE-SYNTAX-COMPLETE.md`

---

### Stage 1: Locations 4+5 with Correct Edge Syntax
**Goal**: Array subsequence TIs with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-1-COMPLETE.md`

---

### Stage 2: Locations 2+3 with Correct Edge Syntax
**Goal**: Property-level TIs with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-2-COMPLETE.md`

---

### Stage 3: Location 1 with Correct Edge Syntax
**Goal**: Graph-level TIs with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-3-COMPLETE.md`

---

### Stage 4: Complex Schema Updates
**Goal**: Update SNB, FinBench schemas with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-4-COMPLEX-SCHEMAS-COMPLETE.md`

---

### Stage 5: Preprocessor Updates
**Goal**: Update preprocessors to handle correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-5-PREPROCESSORS-COMPLETE.md`

---

### Stage 6: Nesting Semantics
**Goal**: Implement nesting principles with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-STAGE-6-NESTING-COMPLETE.md`

---

### Stage 7: Integration & Final Validation
**Goal**: All locations working together with correct edge type syntax

**Deliverables**: 📄 `PHASE-E-COMPLETE.md`

---

## Success Criteria

Phase E is complete when:
1. ✅ All 9 TI locations implemented and tested
2. ✅ Nesting semantics work correctly
3. ✅ Canonicalization works correctly
4. ✅ Import processing works correctly
5. ✅ **NEW**: All edge types use correct LEX-2026.0.3.2 syntax
6. ✅ **NEW**: JSON Schema enforces correct edge type syntax
7. ✅ **NEW**: All validators check correct edge type syntax
8. ✅ **NEW**: Preprocessors handle correct edge type syntax
9. ✅ All test files validate successfully
10. ✅ Documentation complete and accurate

## Dependencies

```
Stage 0 (Edge Syntax Foundation) - MUST COMPLETE FIRST
    ↓
    ├─→ Stage 1 (Locations 4+5)
    ├─→ Stage 2 (Locations 2+3)
    └─→ Stage 3 (Location 1)
         ↓
    Stage 4 (Complex Schemas)
         ↓
    Stage 5 (Preprocessors)
         ↓
    Stage 6 (Nesting Semantics)
         ↓
    Stage 7 (Integration)
```

## Next Steps

**READY TO START STAGE 0**: Edge Type Syntax Foundation

This is the critical prerequisite for all Phase E work.

## References

- Design Document: `.kiro/specs/property-graph-schema/design.md`
- Edge Syntax Corrections: `LEX-2026.0.3.2-EDGE-TYPE-SYNTAX-CORRECTIONS.md`
- Original Phase E Plan: `PHASE-E-IMPLEMENTATION-PLAN.md`
