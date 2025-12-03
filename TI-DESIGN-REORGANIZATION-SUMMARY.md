# Type Interpretation Design Document Reorganization

## Summary

Completed reorganization of Type Interpretation (TI) design documentation to establish clear design authority and integration with broader Grasch architecture.

## Actions Taken

### 1. Deprecated Outdated Documents

Moved superseded documents to `archive/deprecated-design-docs/`:
- `TYPE-INTERPRETATION-DESIGN-deprecated-2024-11-19.md` (Nov 19, 2024 - earlier iteration)
- `type-interpretation-flexibility-design-deprecated-2024-11-19.md` (Nov 19, 2024 - earlier approach)

### 2. Established Design Authority

**Current Authoritative Design**: `.kiro/specs/type-interpretation-wrappers/design.md` (Nov 27, 2024)

This document is authoritative because it:
- **Matches the actual implementation** in Phases A-D (locations 6, 7, 8, 9)
- Uses the exact wrapper syntax implemented: `abstract:`, `concrete:`, `properSubtypesOf:`, `exactlyOf:`, `subtypesOf:`
- Describes 0-level (bare), 1-level (shorthand), and 2-level (explicit) patterns that are actually in the code
- Matches test files like `test-phase-a-corrected.yaml`
- **Most comprehensive**: Defines all 8 TI locations explicitly
- Includes single-schema architecture with pre-canonical and canonical forms
- Describes canonicalization process
- Includes analogy to edge type endpoint syntax
- Has detailed JSON Schema patterns
- **Most recent**: November 27 vs November 19 for the deprecated documents

### 3. Updated Implementation Plan

Updated `SCHEMA-TI-FIX-IMPLEMENTATION-PLAN.md` to:
- Reference the correct authoritative design document at the top
- Show integration with broader Grasch architecture:
  - **Schema Architecture**: `.kiro/specs/property-graph-schema/design.md`
  - **Import System**: `.kiro/specs/import-schema-consistency/design.md`
  - **Requirements**: `.kiro/specs/property-graph-schema/requirements.md`
- Document deprecated materials
- Maintain clear traceability from design to implementation
- Update location numbering to match design document (9 locations, not 8)
- Clarify completed phases (A-D) and current phase (E)
- Add design compliance section
- Reference specific files and artifacts

### 4. Design Integration Analysis

The TI design integrates with broader Grasch architecture:

**Property Graph Schema Design** (`.kiro/specs/property-graph-schema/design.md`):
- Overall schema architecture
- Profile + Language Level system
- Three-layer API model
- Storage layer (Kuzu)

**Import Schema Consistency** (`.kiro/specs/import-schema-consistency/design.md`):
- Import resolution and merging
- Pre-canonical to canonical transformation
- Import preprocessing coordination

**Requirements** (`.kiro/specs/property-graph-schema/requirements.md`):
- System-level requirements
- Constraint specifications
- Validation requirements

## Current State

- **Authoritative Design**: `.kiro/specs/type-interpretation-wrappers/design.md` (Nov 27, 2024)
- **Implementation Plan**: Updated with proper references and integration context
- **Deprecated Materials**: Safely archived in `archive/deprecated-design-docs/`
- **Implementation Status**: Phases A-D complete (locations 6, 7, 8, 9), Phase E in progress (locations 4, 5)

## Key Design Principles (from Authoritative Document)

1. **Single Schema Architecture**: One JSON Schema validates both pre-canonical and canonical forms
2. **Three-Level TI Architecture**: 
   - Level 1: TI Locations (where TI can appear)
   - Level 2: TI Structure (how TI is expressed: 0/1/2-level)
   - Level 3: Type Definition (actual element type specification)
3. **Two Independent Facets**:
   - Subtype Interpretation: `subtypeOf`, `properSubtypesOf`, `exactlyOf`
   - Concreteness: `abstract`, `concrete`, `final`, `sealed`
4. **Fixed Wrapper Order**: Subtype matching mode → concreteness → property
5. **Canonicalization**: Import preprocessor transforms pre-canonical to canonical forms

## Next Steps

With clean design authority established, we can proceed with:
- **Phase E**: Array subsequence TI implementation (locations 4+5)
- Following the authoritative design specification
- Maintaining consistency with broader Grasch architecture
- Clear traceability from requirements → design → implementation
