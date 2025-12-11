# Type Interpretation Simplification Context

**Date**: 2024-12-11  
**Purpose**: Document the four fundamental changes to simplify the Type Interpretation (TI) system for LEX-2026.0.3.2

## Background

During the TI ordering refactor specification work, four critical simplification changes were identified that will fundamentally restructure the TI system from a complex two-level architecture to a simpler single-level system.

## The Four Changes

### Change 1: Eliminate Freestanding Types (NEW)
Remove the possibility of having a freestanding nodeType or edgeType that is contained by a nodeTypes or edgeTypes, but which is not part of an array or sequence of such types.

**Impact**: Only arrays/sequences of types are allowed, no standalone individual types.

### Change 2: Reinforce GraphType Organization (RESTATEMENT)
To restate the organization of a graph type (which is a part of a graph schema): it is made up of zero to many nodeTypes collection objects, and zero to many edgeTypes collection objects. Each of those objects may be subdivided into multiple arrays or subsequences of nodeType or edgeType objects respectively. A type interpretation can surround a graphType, a nodeTypes or an edgeTypes, or an array or subsequence of nodeType or edgeType. There can be no nesting of type interpretations. A type interpretation cannot contain, either directly or indirectly, another type interpretation.

**Impact**: Reinforces the no-nesting rule and clarifies the structural organization.

### Change 3: Prevent Immediate TI Wrapper Containment (NEW)
It is never possible to have two TI wrappers, one immediately containing the other.

**Impact**: Strengthens the no-nesting rule by preventing any direct TI wrapper containment.

### Change 4: Single-Level TI System (NEW - MAJOR ARCHITECTURAL CHANGE)
TIs themselves are to become single-level. This will make things a lot simpler. There are three possible TIs:
- `exactlyOfConcrete`
- `subtypeOfConcrete` 
- `subtypeOfAbstract`

There are synonyms:
- `exactlyOf` and `concrete` are the same as `exactlyOfConcrete`
- `properSubtypeOf` is a synonym for `subtypeOfAbstract`
- `subtypeOf` is a synonym for `subtypeOfConcrete`

Canonicalization will turn the synonyms into their canonical, primary form.

**Impact**: Collapses the complex two-level TI system (interpretation facet + concreteness facet) into a simple single-level system with only 3 primary forms and their synonyms.

## Analysis of Impact

This represents a **major simplification** of the TI system:

### Before (Complex Two-Level System)
- **Interpretation Level**: `exactlyOf`, `subtypesOf`, `properSubtypesOf`
- **Concreteness Level**: `abstract`, `concrete`, `final`, `sealed`
- **Total Combinations**: 6+ valid combinations
- **Syntax Examples**: 
  - 0-level: `typeLabel: Person`
  - 1-level: `concrete: { typeLabel: Person }`
  - 2-level: `exactlyOf: { concrete: { typeLabel: Person } }`

### After (Simple Single-Level System)
- **Primary Forms**: `exactlyOfConcrete`, `subtypeOfConcrete`, `subtypeOfAbstract`
- **Synonyms**: `exactlyOf`, `concrete`, `subtypeOf`, `properSubtypeOf`
- **Total Forms**: 3 primary + 4 synonyms = 7 total keywords
- **Syntax Examples**:
  - 0-level: `typeLabel: Person` (implicit `exactlyOfConcrete`)
  - 1-level: `concrete: { typeLabel: Person }` (synonym for `exactlyOfConcrete`)
  - 1-level: `exactlyOfConcrete: { typeLabel: Person }` (canonical form)

## Documents Requiring Updates

These changes will require comprehensive updates to:

1. **Requirements Document** (`.kiro/specs/ti-ordering-refactor/requirements.md`)
   - All TI-related requirements need revision
   - Glossary updates for new terminology
   - Acceptance criteria updates

2. **Design Document** (`.kiro/specs/ti-ordering-refactor/design.md`)
   - Complete TI architecture section rewrite
   - Schema structure changes
   - Component design updates

3. **Tasks Document** (`.kiro/specs/ti-ordering-refactor/tasks.md`)
   - Implementation approach changes
   - Schema modification tasks
   - Test file update requirements

## Key Principles Maintained

- **Explicit Properties Only**: No `patternProperties` anywhere
- **No Migration/Backwards Compatibility**: Iterating towards good first design
- **No TI Nesting**: Type interpretations cannot contain other type interpretations

## Next Steps

1. ✅ Create this summary document
2. ⏳ Back up existing specification documents
3. ⏳ Update all three specification documents with these changes
4. ⏳ Record this summary in CONTEXT-SUMMARIES document

## Status

- **Summary Created**: ✅ Complete
- **Backups Created**: ⏳ Pending
- **Specs Updated**: ⏳ Pending
- **Context Recorded**: ⏳ Pending