# Context: Syntax Redesign for LEX-2026.0.4.0

**Created**: 2024-12-18  
**Status**: Active - Current Phase  
**Purpose**: Document the iterative process of updating design.md, comprehensive syntax example, and SNB inline example for LEX-2026.0.4.0  
**Phase**: Syntax Redesign and Documentation Update  

## Current Context

We are embarking on an **iterative process** of updating three critical documents to reflect the corrected edge type syntax and simplified Type Interpretation (TI) system:

1. **`.kiro/specs/ti-ordering-refactor/design.md`** - Primary design document
2. **Design.md comprehensive syntax example** - The complete example within the design document
3. **`src/grasch/examples/lex-2026.0.3.2-snb-schema-inline-comprehensive.yaml`** - SNB inline example

## Current State Analysis

### SNB Inline Schema Status: ✅ COMPLETE
The SNB inline schema has been **successfully corrected** and is ready:
- ✅ **Proper short form syntax**: `via: LABEL_NAME` for edges without properties (11 edges)  
- ✅ **Proper long form syntax**: Nested `typeLabel:` and `implies:` for edges with properties (5 edges)  
- ✅ **Correct indentation structure**: All levels properly indented according to LEX-2026.0.3.2 specification  
- ✅ **Valid YAML**: No syntax errors or diagnostic issues  
- ✅ **IDE compatible**: Survived autofix/formatting without issues  
- ✅ **Abstract supertype references**: Proper use of `properSubtypesOf: Message/Organisation/Place`

### Design Document Status: 🔄 NEEDS UPDATE
The design document requires updates to:
- Document the correct edge type syntax patterns (short form vs long form)
- Update the comprehensive syntax example to use correct edge type syntax
- Ensure consistency with the corrected SNB inline schema

## Iterative Update Process

### Phase 1: Design Document Updates
1. **Document edge type syntax patterns** in design.md
   - Short form: `via: LABEL_NAME` (for edges without properties)
   - Long form: Nested `typeLabel:` and `implies:` (for edges with properties)
   - Correct indentation levels and structure

2. **Update comprehensive syntax example** in design.md
   - Apply correct edge type syntax throughout the example
   - Ensure consistency with documented patterns
   - Maintain all TI wrapper demonstrations

### Phase 2: Consistency Verification
1. **Cross-reference all three documents** for consistency
2. **Verify syntax patterns** are uniform across examples
3. **Ensure TI wrapper usage** is consistent

### Phase 3: Consequential Changes (Future)
**ONLY AFTER** the three core documents are consistent and updated:
- JSON Schema updates
- Other example files and test updates
- Validation and regression testing

## Back-References to Previous Context

This document continues work from:

### Primary Context Documents
- **`SIMPLIFY-TYPE-INTERPRETATION.md`** (2024-12-15) - TI system simplification summary
  - **Status**: Edge Type Syntax Corrections Applied
  - **Achievement**: Fixed fundamental edge type syntax issues
  - **Authority**: design.md is primary authority for implementation

- **`SIMPLIFY-TI-CONTEXT.md`** (2024-12-11) - Four fundamental TI system changes
  - **Change 1**: Eliminate freestanding types (arrays/sequences only)
  - **Change 2**: Reinforce GraphType organization (no TI nesting)
  - **Change 3**: Prevent immediate TI wrapper containment
  - **Change 4**: Single-level TI system (3 primary forms + synonyms)

### Completed Work References
- **`SNB-INLINE-SCHEMA-CORRECTION-COMPLETE.md`** - Documents the successful correction of SNB inline schema
- **`.kiro/specs/ti-ordering-refactor/requirements.md`** - Updated with single-level TI system
- **`.kiro/specs/ti-ordering-refactor/tasks.md`** - Updated with new implementation plan

### Implementation Status
- ✅ Requirements document updated with single-level TI system
- ✅ Design document updated with simplified architecture (CORRECTED 2024-12-15)
- ✅ Design document corrected: NodeTypeArray/EdgeTypeArray terminology
- ✅ Design document corrected: Pattern properties absolutely excluded
- ✅ Tasks document updated with new implementation plan
- ✅ SNB inline schema corrected with proper edge type syntax

## Critical Principles

### Careful Change Management
- **No changes without explicit user approval**
- **Iterative approach**: Complete each document before moving to the next
- **Consistency verification**: Ensure all three documents align before consequential changes
- **Ripple effect management**: Address broader changes only after core documents are stable

### Design Authority
- **`design.md` is the primary authority** for all implementation decisions
- **SNB inline schema** serves as the reference implementation example
- **Comprehensive syntax example** in design.md demonstrates all syntax possibilities

## Next Steps

1. **Update design.md** with correct edge type syntax documentation
2. **Update comprehensive syntax example** in design.md
3. **Verify consistency** across all three documents
4. **Only then proceed** to consequential changes (JSON Schema, other examples, tests)

## Success Criteria

- [ ] Design.md documents correct edge type syntax patterns
- [ ] Comprehensive syntax example uses correct edge type syntax
- [ ] All three documents are consistent with each other
- [ ] Ready for consequential changes phase

## Risk Management

**Risk**: Introducing inconsistencies between documents  
**Mitigation**: Complete each document fully before moving to the next

**Risk**: Breaking existing functionality during updates  
**Mitigation**: Focus on documentation first, implementation changes later

**Risk**: Losing track of interdependencies  
**Mitigation**: Maintain clear back-references and status tracking

---

**This document represents the current active context for LEX-2026.0.4.0 syntax redesign work.**