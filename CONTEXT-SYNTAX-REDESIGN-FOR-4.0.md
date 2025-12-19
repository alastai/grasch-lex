# Context: Syntax Redesign for LEX-2026.0.4.0

**Created**: 2024-12-18  
**Status**: Active - Current Phase  
**Purpose**: Document the iterative process of updating design.md, comprehensive syntax example, and SNB inline example for LEX-2026.0.4.0  
**Phase**: Syntax Redesign and Documentation Update  

## Current Context

We are embarking on an **iterative process** of updating the core documents to reflect the corrected edge type syntax and simplified Type Interpretation (TI) system:

1. **`.kiro/specs/ti-ordering-refactor/design.md`** - Primary design document
2. **Design.md comprehensive syntax example** - The complete example within the design document

**IMPORTANT**: The SNB inline example (`src/grasch/examples/lex-2026.0.3.2-snb-schema-inline-comprehensive.yaml`) should be **left alone** until the comprehensive example is finished. It is not up to date with the current syntax redesign and we do not want to change it while the 4.0 redesign is underway.

## Current State Analysis

### SNB Inline Schema Status: 🚫 DEFERRED
The SNB inline schema should be **left alone** during the 4.0 syntax redesign:
- ⚠️ **Not up to date**: Does not reflect current 4.0 syntax redesign changes
- 🚫 **Do not modify**: Should not be changed while comprehensive example work is underway
- ⏳ **Future work**: Will be updated after comprehensive example is complete
- 📝 **Previous state**: Was corrected for 3.2 syntax but needs 4.0 updates later

### Design Document Status: ✅ COMPREHENSIVE EXAMPLE COMPLETE
The design document has been updated with:
- ✅ **External file reference**: Points to `lex-2026.0.4.0-comprehensive-syntax-example.yaml`
- ✅ **Endpoint subtype extension syntax**: 7 detailed examples demonstrating all `<:` operator patterns
- ✅ **All original features preserved**: Complete TI architecture, syntax variations, interleaved collections
- 🔄 **Still needs**: Direct documentation of edge type syntax patterns in design.md text

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
1. **Cross-reference design.md and comprehensive example** for consistency
2. **Verify syntax patterns** are uniform between these two documents
3. **Ensure TI wrapper usage** is consistent
4. **SNB inline example**: Will be addressed in a separate phase after comprehensive example is complete

### Phase 3: SNB Inline Example Update (Future)
**ONLY AFTER** the design.md and comprehensive example are consistent and complete:
- Update SNB inline example to match 4.0 syntax
- Ensure consistency across all three documents

### Phase 4: Consequential Changes (Future)
**ONLY AFTER** all core documents are consistent and updated:
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

## Edge Type Endpoint Subtype Extension Syntax (NEW for LEX-2026.0.4.0)

**CRITICAL NEW FEATURE**: Edge type endpoint subtype extension syntax using the `<:` operator for endpoint properties.

**IMPORTANT TERMINOLOGY**: This should be called "edge type endpoint subtype extension syntax" (not just "subtyping syntax") to distinguish it from the existing "edge type endpoint type interpretation syntax" using TI wrappers.

### Syntax Overview

The new endpoint subtype extension syntax works **alongside** the existing type interpretation wrapper syntax. There is **no contradiction** between them:

- **Edge type endpoint type interpretation syntax**: Uses TI wrappers (`properSubtypesOf:`, `exactlyOf:`, etc.)
- **Edge type endpoint subtype extension syntax**: Uses the `<:` operator to specify subtype extensions

### Combined Syntax Example

```yaml
edgeType:
  typeLabel: SUPERVISES
  extends: WORKS_FOR
  directed:
    from: properSubtypesOf: Person      # Type interpretation wrapper syntax
    to: exactlyOf: LLC <: Company       # BOTH TI wrapper AND subtype extension syntax
  adding:
    labels: [Leadership]
    propertyTypes:
      - name: teamSize
        valueType: INTEGER
```

**Key Insight**: The `<:` operator appears **within** the type interpretation wrapper value, specifying that LLC is a subtype of Company while the `exactlyOf:` wrapper specifies the interpretation mode.

### Syntax Rules

**Pattern**: `WS <: WS` (whitespace around the `<:` operator)

**Scope**: Applies to all endpoint properties:
- `from:`
- `to:`
- `between:`
- `and:`

**Usage Constraint**: This endpoint subtype extension syntax is **ONLY** to be used when the orientation property (`directed:`/`undirected:`) follows the `extends:` property. Otherwise, plain type references should be used.

**Compatibility**: The `<:` operator can be used within any type interpretation wrapper:
- `properSubtypesOf: LLC <: Company`
- `exactlyOf: LLC <: Company`  
- `subtypesOf: LLC <: Company`
- Plain type reference: `LLC <: Company`

**Default Behavior**: Omission of an endpoint property (including if the whole orientation is omitted) is equivalent to:
```yaml
directed:
  from: Person <: Person
  to: Company <: Company
```

### Analysis Completed

- ✅ **Easy to parse**: Pattern can be parsed with regex
- ✅ **Clear semantic intent**: Expresses subtyping relationships explicitly
- ✅ **Backward compatibility**: Maintains compatibility with plain type names
- ✅ **Consistent pattern**: Uses familiar `<:` subtyping operator

### Implementation Status

- **Analysis**: Complete
- **Documentation**: ✅ **COMPLETE** - Added to design.md with external file reference
- **Comprehensive Example**: ✅ **COMPLETE** - `src/grasch/examples/lex-2026.0.4.0-comprehensive-syntax-example.yaml` created with 7 detailed subtyping extension examples
- **Schema Updates**: Pending
- **Examples**: ✅ **COMPLETE** - All subtyping extension patterns demonstrated

## Next Steps

1. **Update design.md** with correct edge type syntax documentation **INCLUDING** the new endpoint subtype extension syntax
2. **Update comprehensive syntax example** in design.md to demonstrate the `<:` operator
3. **Verify consistency** across all three documents
4. **Only then proceed** to consequential changes (JSON Schema, other examples, tests)

## Success Criteria

### Phase 1 (Current Focus)
- [ ] Design.md documents correct edge type syntax patterns
- [ ] Comprehensive syntax example uses correct edge type syntax
- [ ] Design.md and comprehensive example are consistent with each other

### Phase 2 (Future)
- [ ] SNB inline example updated to match 4.0 syntax
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