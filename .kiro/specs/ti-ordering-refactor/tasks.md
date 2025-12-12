# Implementation Plan: TI System Simplification

This implementation plan breaks down the TI system simplification into discrete, manageable tasks. Each task builds incrementally toward the single-level TI architecture with array-only organization.

## Complete Phase Structure Overview

This spec is part of the broader Type Interpretation & Edge Syntax implementation:

### **Phase A: NodeType TI Wrappers** ✅ COMPLETE
- Location 6: Individual nodeType TI wrappers

### **Phase B: EdgeType TI Wrappers** ✅ COMPLETE
- Location 7: Individual edgeType TI wrappers

### **Phase C: Endpoint TI Wrappers (Directed)** ✅ COMPLETE
- Location 8: Directed edge endpoint TI wrappers

### **Phase D: Endpoint TI Wrappers (Undirected)** ✅ COMPLETE
- Location 9: Undirected edge endpoint TI wrappers

### **Phase E: TI System Simplification** 🔄 THIS SPEC
- **Stage 1: Single-Level TI Implementation** 
  - **Phase 1: Schema Simplification** (Tasks 1-10)
    - Implement three primary TI forms
    - Add synonym support with canonicalization
    - Eliminate two-level architecture
  - **Phase 2: Array-Only Organization** (Tasks 11-15)
    - Remove freestanding type support
    - Implement consistent array-based organization
  - **Phase 3: TI Nesting Prevention** (Tasks 16-20)
    - Add validation to prevent TI nesting
    - Update schema to reject nested patterns
  - **Phase 4: Test Updates and Validation** (Tasks 21-30)
    - Update test files for simplified syntax
    - Validate canonicalization behavior

### **Phase F: Type Finalization** (FUTURE)
- **Stage 1**: Schema design for `final:` and `sealed:` keywords
- **Stage 2**: Schema implementation for finalization
- **Stage 3**: Test file creation and validation
- **Stage 4**: Documentation and integration

### **Phase G: Import Processing** (FUTURE)
### **Phase H: Canonicalization** (FUTURE)

**E02 Integration**: Edge Label Container Structure Fix is now Task 4 (Phase E / Stage 0 / Phase 1)

---

## Task Overview

- **Phase 1**: Single-Level TI Schema Implementation (3-4 hours)
- **Phase 2**: Array-Only Organization Implementation (2-3 hours)  
- **Phase 3**: TI Nesting Prevention (1-2 hours)
- **Phase 4**: Test Updates and Validation (3-4 hours)

**Total Estimated Time**: 9-13 hours

---

## Phase 1: Single-Level TI Schema Implementation

### - [ ] 1. Implement Primary TI Forms in Schema

Replace the complex two-level TI architecture with three primary single-level forms

- Locate all TI-related definitions in `src/grasch/schemas/lex-2026.0.3.2.schema.json`
- Replace two-level patterns with single-level primary forms:
  - `exactlyOfConcrete`: Exact matching, concrete types
  - `subtypeOfConcrete`: Subtype matching, concrete types  
  - `subtypeOfAbstract`: Subtype matching, abstract types
- Remove all nested interpretation/concreteness facet patterns
- Implement explicit properties for each primary form
- Validate JSON syntax after changes
- _Requirements: 1.1, 1.2, 1.5_

### - [ ] 2. Add TI Synonym Support

Implement synonym keywords that map to primary forms during canonicalization

- Add explicit properties for TI synonyms:
  - `concrete` → maps to `exactlyOfConcrete`
  - `exactlyOf` → maps to `exactlyOfConcrete`
  - `subtypeOf` → maps to `subtypeOfConcrete`
  - `properSubtypeOf` → maps to `subtypeOfAbstract`
- Ensure synonyms have identical structure to their primary forms
- Add schema descriptions documenting the synonym mappings
- Validate JSON syntax after changes
- _Requirements: 1.2, 5.1-5.3_

### - [ ] 3. Create Schema Backup

Backup the current schema before making major changes

- Copy `src/grasch/schemas/lex-2026.0.3.2.schema.json` to `src/grasch/schemas/lex-2026.0.3.2.schema.json.backup-simplified`
- Verify backup is complete and valid JSON
- Document backup creation in change log
- _Requirements: Pattern Consistency_

---

## Phase 2: Array-Only Organization Implementation

**Phase 2 Scope**: Implement consistent array-only organization across all TI locations, eliminating freestanding types and ensuring all types are contained within arrays or subsequences.

### - [ ] 11. Remove Freestanding Type Support

Eliminate all schema patterns that allow individual types outside of arrays

- Identify all locations that currently allow freestanding `nodeType` or `edgeType` definitions
- Remove schema support for individual type definitions not in arrays
- Ensure all type definitions must be within `nodeTypes` or `edgeTypes` arrays
- Update schema to reject freestanding type patterns
- Validate JSON syntax after changes
- _Requirements: 2.1, 2.2, 2.3_

### - [ ] 12. Implement Array Subsequence TI Support

Update array definitions to support TI-wrapped subsequences using single-level TI forms

- Locate `NodeTypesArray` and `EdgeTypesArray` definitions in schema
- Add support for TI-wrapped subsequences within arrays
- Allow array elements to be either bare types OR TI-wrapped subsequences
- Use single-level TI forms for subsequence wrappers
- Ensure subsequences are siblings within arrays (not nested)
- Validate JSON syntax after changes
- _Requirements: 2.4, 2.5, 2.6_

### - [ ] 13. Update GraphType Organization

Implement array-only organization at the GraphType level with single-level TI support

- Locate GraphType definition in schema
- Remove any remaining support for freestanding types at GraphType level
- Ensure `nodeTypes` and `edgeTypes` are always arrays
- Add single-level TI wrapper support for GraphType collections
- Support sibling TI-wrapped collections (e.g., `exactlyOfConcrete: { nodeTypes: [...] }`)
- Validate JSON syntax after changes
- _Requirements: 2.7, 8.4_

### - [ ] 14. Validate Array-Only Organization

Test that the schema correctly enforces array-only organization

- Create test files with freestanding types (should fail validation)
- Create test files with proper array organization (should pass validation)
- Test TI-wrapped array subsequences
- Test sibling TI-wrapped collections at GraphType level
- Verify all array-only patterns work correctly
- Document validation results
- _Requirements: 2.1-2.7_



### - [ ] 15. Update All TI Locations for Array-Only

Apply array-only organization consistently across all 8 TI locations

- Update Location 1 (GraphSchemaContent) for array-only GraphType organization
- Update Location 2 (nodeTypesInterpretation) for array-only nodeTypes
- Update Location 3 (edgeTypesInterpretation) for array-only edgeTypes  
- Update Location 4 (nodeTypeArrayInterpretation) for subsequence support
- Update Location 5 (edgeTypeArrayInterpretation) for subsequence support
- Update Location 6 (nodeTypeInterpretation) - eliminate (array-only)
- Update Location 7 (edgeTypeInterpretation) - eliminate (array-only)
- Verify Location 8 (EndpointReference) remains compatible
- _Requirements: 2.1-2.7, 8.1-8.6_

## Phase 3: TI Nesting Prevention

**Phase 3 Scope**: Implement comprehensive validation to prevent any form of TI nesting, ensuring the single-level architecture is maintained throughout the system.

### - [ ] 16. Add TI Nesting Validation Rules

Implement schema validation that prevents any TI wrapper from containing another TI wrapper

- Add validation rules to reject immediate TI wrapper containment
- Add validation rules to reject indirect TI wrapper containment  
- Ensure validation covers all TI forms (primary and synonyms)
- Add clear error messages for TI nesting attempts
- Test validation with nested TI patterns (should fail)
- _Requirements: 3.1, 3.2, 3.3_

### - [ ] 17. Implement Flat TI Architecture Enforcement

Ensure the schema architecture prevents any nested TI patterns

- Review all TI-related schema definitions for potential nesting points
- Implement flat, single-level structure throughout
- Remove any remaining two-level TI architecture remnants
- Ensure all TI keywords are at the same structural level as content
- Add schema constraints that enforce flat architecture
- _Requirements: 3.4, 3.5, 3.6_

### - [ ] 18. Create TI Nesting Test Cases

Develop comprehensive test cases to verify TI nesting prevention

- Create negative test cases with immediate TI nesting (should fail)
- Create negative test cases with indirect TI nesting (should fail)
- Create positive test cases with proper single-level TI usage (should pass)
- Test all combinations of primary forms and synonyms
- Verify error messages are clear and helpful
- _Requirements: 7.5, 7.6_

### - [ ] 19. Validate TI Nesting Prevention

Test that the schema successfully prevents all forms of TI nesting

- Run validation tests with nested TI patterns (should all fail)
- Verify error messages clearly indicate TI nesting violations
- Test edge cases and complex nesting scenarios
- Confirm single-level TI patterns work correctly
- Document validation behavior and error messages
- _Requirements: 3.1-3.6_

### - [ ] 20. Clean Up Legacy TI Architecture

Remove any remaining artifacts from the old two-level TI system

- Remove vestigial schema definitions from old TI architecture
- Clean up unused pattern properties and complex nesting structures
- Remove outdated comments and documentation references
- Ensure schema is clean and focused on single-level architecture
- Validate JSON syntax after cleanup
- _Requirements: Pattern Consistency_

### - [ ] 11. Test Level-1 TI Wrappers in GraphType

Validate that Level-1 TI wrappers work correctly in GraphType

- Create test file `src/grasch/examples/test-graphtype-1-level-ti.yaml`
- Test `concrete: { nodeTypes: [...] }` syntax
- Test `abstract: { edgeTypes: [...] }` syntax
- Test combination: `concrete: { nodeTypes: [...] }` with `abstract: { edgeTypes: [...] }`
- Validate all test files pass schema validation
- Run existing Phase A-D tests to ensure no regressions
- _Requirements: 1.3, 8.1_
- _Reference: TASKS-10-11-CORRECTION-ANALYSIS.md_

### - [ ] 12. Fix Location 4 (nodeTypeArrayInterpretation)

Apply array subsequence model to nodeTypeArrayInterpretation (subsequences within nodeTypes array)

- Locate NodeTypeArray definition in schema (~line 2200)
- Note: Schema incorrectly names this "NodeTypeItem" but it handles array-level TI, not individual elements
- Allow array elements to be EITHER bare types OR TI-wrapped subsequences
- Subsequences are siblings within the array (not nested)
- Each subsequence contains an array of types (cardinality ≥ 1)
- Distinguish array subsequences (Location 4) from single types (Location 6)
- **Key Distinction**: An array subsequence is NOT the same as a single type (Location 6)
  - Array subsequence with 1 element: `abstract: [{ typeLabel: X }]` (Location 4)
  - Single type: `abstract: { typeLabel: X }` (Location 6)
  - These are DIFFERENT structures with different semantics
- Add support for 0-level, 1-level, 2-level syntax
- Validate JSON syntax
- _Requirements: 1.1, 2.4, 9.1_
- _Note: Array subsequence model (dividing arrays into sibling subsequences), NOT nesting model (recursive arrays)_

### - [ ] 13. Fix Location 5 (edgeTypeArrayInterpretation)

**DEPENDS ON**: Task 4 (Edge Label Container Fix) must be complete first

Apply array subsequence model to edgeTypeArrayInterpretation (subsequences within edgeTypes array)

- Locate EdgeTypeArray definition in schema (~line 2900)
- Note: Schema incorrectly names this "EdgeTypeItem" but it handles array-level TI, not individual elements
- Allow array elements to be EITHER bare types OR TI-wrapped subsequences
- Subsequences are siblings within the array (not nested)
- Each subsequence contains an array of types (cardinality ≥ 1)
- Distinguish array subsequences (Location 5) from single types (Location 7)
- **Key Distinction**: An array subsequence is NOT the same as a single type (Location 7)
  - Array subsequence with 1 element: `abstract: [{ typeLabel: X }]` (Location 5)
  - Single type: `abstract: { typeLabel: X }` (Location 7)
  - These are DIFFERENT structures with different semantics
- Add support for 0-level, 1-level, 2-level syntax
- Ensure edge label containers use correct object form (from Task 4)
- Validate JSON syntax
- _Requirements: 1.1, 2.5, 9.1_
- _Note: Array subsequence model (dividing arrays into sibling subsequences), NOT nesting model (recursive arrays)_

### - [ ] 14. Test Locations 4-5 Fixes

Validate that Locations 4-5 fixes work correctly

- Run `python validate_phase_e_locations_4_5.py`
- Expect failures (tests use wrong syntax)
- Document which test files need updates
- _Requirements: 8.1_

### - [ ] 15. Fix Location 6 (nodeTypeInterpretation)

Add TI support to nodeTypeInterpretation (wraps a single nodeType)

- Locate Individual NodeType definition in schema (lines 1009-1310)
- Add sibling properties pattern wrapping NodeType content
- Implement full 2-level TI pattern
- Add support for 0-level, 1-level, 2-level syntax
- Validate JSON syntax
- _Requirements: 1.1, 2.6, 9.1_

### - [ ] 16. Fix Location 7 (edgeTypeInterpretation)

**DEPENDS ON**: Task 4 (Edge Label Container Fix) must be complete first

Add TI support to edgeTypeInterpretation (wraps a single edgeType)

- Locate EdgeType Content definition in schema (lines 1313-1800)
- Add sibling properties pattern wrapping EdgeType content
- Implement full 2-level TI pattern
- Add support for 0-level, 1-level, 2-level syntax
- Ensure edge label containers use correct object form (from Task 4)
- Validate JSON syntax
- _Requirements: 1.1, 2.7, 9.1_

### - [ ] 17. Verify Location 8 (edgeTypeEndpointNodeTypeInterpretation) Unchanged

Confirm Location 8 (edgeTypeEndpointNodeTypeInterpretation - wraps endpoint references) still works correctly

- Verify EndpointReference definition unchanged (lines 3168, 3443)
- Run `python validate_phase_c.py` (tests Location 8)
- Confirm all tests still pass
- _Requirements: 6.1_

---

## Phase 4: Test Updates and Validation

**Phase 4 Scope**: Update all test files to use the simplified single-level TI syntax and validate the complete system works correctly.

### - [ ] 21. Identify Test Files Requiring Updates

Analyze existing test files to determine which need updates for the simplified TI system

- Run validation to identify files using old two-level TI syntax
- Identify files using freestanding types (need array conversion)
- Identify files using nested TI patterns (need flattening)
- Categorize files by type of update needed
- Document the scope of test file changes required
- _Requirements: 6.1, 6.2_

### - [ ] 22. Update Test Files for Single-Level TI

Convert existing test files to use the simplified single-level TI syntax

- Update files using two-level TI syntax to single-level primary forms
- Convert synonym usage to demonstrate canonicalization
- Update complex TI patterns to use simplified forms
- Ensure all TI usage follows single-level architecture
- Validate updated files pass schema validation
- _Requirements: 6.3, 6.4_

### - [ ] 23. Convert Test Files to Array-Only Organization

Update test files to use consistent array-only type organization

- Convert freestanding types to array-based organization
- Update test files to use proper array subsequence patterns
- Ensure all types are contained within arrays or subsequences
- Remove any remaining freestanding type examples
- Validate array-only organization works correctly
- _Requirements: 6.3, 2.1-2.7_

### - [ ] 20. Update Phase E Location 2 Test Files

Fix test files for Location 2 (NodeTypesProperty)

- Update `src/grasch/examples/test-phase-e-location-2.yaml`
- Update `src/grasch/examples/test-phase-e-location-2-two-level.yaml`
- Move TI wrappers from inside nodeTypes to outside
- Preserve test semantics
- Validate updated files
- _Requirements: 3.3, 3.4_

### - [ ] 21. Update Phase E Location 3 Test Files

**DEPENDS ON**: Task 6 (Edge Label Container Test) must be complete first

Fix test files for Location 3 (EdgeTypesProperty)

- Update `src/grasch/examples/test-phase-e-location-3.yaml`
- Update `src/grasch/examples/test-phase-e-location-3-two-level.yaml`
- Move TI wrappers from inside edgeTypes to outside
- Ensure edge labels use correct object form
- Preserve test semantics
- Validate updated files
- _Requirements: 3.3, 3.4_

### - [ ] 22. Update Phase E Locations 2-3 Combined Test Files

Fix combined test files for Locations 2-3

- Update `src/grasch/examples/test-phase-e-locations-2-3.yaml`
- Update `src/grasch/examples/test-phase-e-locations-2-3-advanced.yaml`
- Move TI wrappers to correct positions
- Preserve test semantics
- Validate updated files
- _Requirements: 3.3, 3.4_

### - [ ] 23. Update Phase E Locations 4-5 Test Files

Fix test files for Locations 4-5 (array items)

- Update `src/grasch/examples/test-phase-e-locations-4-5.yaml`
- Move TI wrappers to correct positions for array items
- Preserve test semantics
- Validate updated files
- _Requirements: 3.3, 3.4_

### - [ ] 24. Update Complex Schema Files (E02)

**DEPENDS ON**: Task 6 (Edge Label Container Test) must be complete first

Update complex schema files with correct edge label structure

- Update `imports/lex-2026.0.3.2-edge-type-syntax-examples.yaml` (~50+ edges)
- Update `lex-2026.0.3.2-snb-schema.yaml`
- Update `lex-2026.0.3.2-finbench-schema.yaml`
- Update `lex-2026.0.3.2-finbench-sf1-graph.yaml`
- Ensure all edge labels use object form with `typeLabel:` child
- Validate updated files
- _Requirements: 3.3, 3.4_
- _Reference: E02-COMPREHENSIVE-FIX-PLAN.md Phase 2 Priority 3_

### - [ ] 24. Create Canonicalization Test Files

Develop test files to validate synonym-to-canonical mapping behavior

- Create test files using TI synonyms (`concrete`, `subtypeOf`, `properSubtypeOf`, `exactlyOf`)
- Create expected canonical form versions using primary forms
- Test canonicalization process converts synonyms correctly
- Verify all synonym mappings work as specified
- Document canonicalization behavior
- _Requirements: 5.1-5.7_

### - [ ] 25. Create Comprehensive TI Test Suite

Develop comprehensive test files covering all aspects of the simplified TI system

- Create positive test files for all three primary TI forms
- Create positive test files demonstrating sibling TI usage
- Create negative test files for prohibited TI nesting
- Create test files for array-only organization validation
- Create edge case test files for complex scenarios
- _Requirements: 7.1-7.7_

### - [ ] 26. Create Validation Test Scripts

Develop automated validation scripts for the simplified TI system

- Create `test_single_level_ti_validation.py` for primary form testing
- Create `test_canonicalization_validation.py` for synonym mapping testing
- Create `test_array_only_validation.py` for organization testing
- Create `test_nesting_prevention_validation.py` for nesting prevention testing
- Implement comprehensive pass/fail reporting
- _Requirements: 7.7, 10.1-10.6_

---

### - [ ] 27. Run Comprehensive System Validation

Validate the complete simplified TI system works correctly

- Run all validation scripts created in previous tasks
- Validate all test files pass with the simplified schema
- Confirm negative test cases fail with appropriate error messages
- Test canonicalization behavior across all synonym mappings
- Verify array-only organization is enforced consistently
- Document comprehensive validation results
- _Requirements: 10.1-10.6_

### - [ ] 28. Run Location-Specific Validation

Validate each location independently

- Run validation for Location 1 (new tests)
- Run `python validate_phase_e_locations_2_3.py` - should pass
- Run `python validate_phase_e_locations_4_5.py` - should pass
- Run `python test_sibling_validation.py` - should pass
- Document results
- _Requirements: 8.1, 8.5_

### - [ ] 29. Verify Phases A-D Still Pass

Confirm no regressions in previously working locations

- Run `python validate_phase_a_corrected.py` - should pass
- Run `python validate_phase_b.py` - should pass
- Run `python validate_phase_c.py` - should pass
- Run `python validate_phase_d.py` - should pass
- Confirm Locations 6, 7, 8 still work correctly
- _Requirements: 6.2, 6.4_

### - [ ] 30. Document Schema Changes

Create documentation of all schema changes made

- List each location fixed (6 locations: 2-7; Location 1 already working)
- Document pattern applied at each location
- Note line numbers changed
- Explain rationale for each change
- Note Location 1 was verified as already correct
- _Requirements: 7.2_

### - [ ] 31. Document Test File Changes

Create documentation of all test file changes

- List each test file updated
- Document syntax changes made
- Explain why changes were necessary
- Note semantic preservation
- Note Location 1 tests already exist and pass
- _Requirements: 7.3_

### - [ ] 30. Create Simplification Completion Summary

Write comprehensive summary of the TI system simplification

- Document the transformation from two-level to single-level architecture
- Summarize the three primary TI forms and their semantics
- Document synonym mappings and canonicalization behavior
- Report on array-only organization implementation
- Summarize TI nesting prevention measures
- Document validation results and test coverage
- Report on all success criteria achievement
- _Requirements: 10.1-10.6_

### - [ ] 30. Update TI Documentation Index

Update the TI documentation index to reflect completed work

- Mark this spec as complete
- Update status of TI implementation roadmap
- Link completion summary
- Archive any superseded documents
- _Requirements: 7.5, 7.6_

---

## Success Criteria Checklist

After completing all tasks, verify these criteria are met:

- [ ] Single-level TI system implemented with three primary forms (`exactlyOfConcrete`, `subtypeOfConcrete`, `subtypeOfAbstract`)
- [ ] TI synonyms implemented with correct canonicalization mapping (`concrete`, `exactlyOf`, `subtypeOf`, `properSubtypeOf`)
- [ ] Array-only organization enforced across all locations (no freestanding types)
- [ ] TI nesting completely prevented throughout the system
- [ ] All 8 TI locations support the simplified single-level architecture
- [ ] Sibling TI wrappers work correctly with different TI forms
- [ ] Canonicalization correctly maps synonyms to primary forms
- [ ] All test files validate with the simplified schema
- [ ] Comprehensive validation suite passes all tests
- [ ] System complexity significantly reduced while maintaining full semantic expressiveness

---

## Notes

- **Incremental Testing**: Test after each location fix to catch issues early
- **Backup**: Keep schema backup until all validation passes
- **Expected Failures**: Test failures after schema fixes are CORRECT - they indicate tests need updating
- **Mindset**: Fix the schema to match the design, then fix the tests to match the design
- **Documentation**: Document as you go - don't wait until the end

---

## Phase F: Type Finalization (FUTURE WORK)

**Status**: To be implemented after Phase E (Type Interpretations) is complete.

**Scope**: Implement `final:` and `sealed:` keywords as a separate system from type interpretation.

### Stage 1: Design and Requirements

- [ ] F.1 Create requirements document for type finalization
  - Define `final:` semantics (prevents subtyping)
  - Define `sealed:` semantics (restricts where subtypes can be defined)
  - Clarify orthogonality with type interpretation
  - _Requirements: TBD_

- [ ] F.2 Create design document for type finalization
  - Schema structure for finalization keywords
  - Validation rules for finalization constraints
  - Interaction with type interpretation system
  - _Requirements: TBD_

### Stage 2: Schema Implementation

- [ ] F.3 Add `final:` keyword support to schema
  - Define `final:` pattern in JSON Schema
  - Add validation rules
  - Test with type interpretation combinations
  - _Requirements: TBD_

- [ ] F.4 Add `sealed:` keyword support to schema
  - Define `sealed:` pattern in JSON Schema
  - Add validation rules
  - Test with type interpretation combinations
  - _Requirements: TBD_

### Stage 3: Test Files and Validation

- [ ] F.5 Create test files for `final:` keyword
  - Positive tests (valid final types)
  - Negative tests (invalid subtyping attempts)
  - Combined with type interpretation
  - _Requirements: TBD_

- [ ] F.6 Create test files for `sealed:` keyword
  - Positive tests (valid sealed types)
  - Negative tests (invalid extension locations)
  - Combined with type interpretation
  - _Requirements: TBD_

### Stage 4: Documentation and Integration

- [ ] F.7 Update documentation
  - Add finalization section to LEX-2026 spec
  - Update TI documentation to clarify separation
  - Create examples showing combined usage
  - _Requirements: TBD_

- [ ] F.8 Integration validation
  - Verify no conflicts with type interpretation
  - Test all combinations
  - Update validation scripts
  - _Requirements: TBD_

