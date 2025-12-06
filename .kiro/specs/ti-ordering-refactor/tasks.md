# Implementation Plan: TI Ordering Refactor

This implementation plan breaks down the TI ordering refactoring into discrete, manageable tasks. Each task builds incrementally on previous work.

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

### **Phase E: Array-Level & Graph-Level TI + Edge Syntax** 🔄 THIS SPEC
- **Stage 0: Edge Type Syntax Foundation** (PREREQUISITE)
  - **Phase 1: JSON Schema Updates** (Tasks 1-17)
    - **Task 4: Fix Edge Label Container Structure (E02)** ⭐
    - Tasks 10, 13, 16, 21 depend on Task 4
  - **Phase 2: Example File Updates** (Tasks 6-14)
    - **Task 6: Test Edge Label Container Fix (E02)** ⭐
  - **Phase 3: Test File Updates** (Tasks 18-26)
    - **Task 24: Update Complex Schema Files (E02)** ⭐
  - **Phase 4: Validation and Documentation** (Tasks 27-33)
- **Stage 1-7**: Array/Graph-level TI locations (future stages)

### **Phase F: Import Processing** (FUTURE)
### **Phase G: Canonicalization** (FUTURE)

**E02 Integration**: Edge Label Container Structure Fix is now Task 4 (Phase E / Stage 0 / Phase 1)

---

## Task Overview

- **Phase 1**: Schema Analysis and Preparation (1-2 hours)
- **Phase 2**: Schema Fixes (3-4 hours)  
- **Phase 3**: Test File Updates (2-3 hours)
- **Phase 4**: Validation and Documentation (1-2 hours)

**Total Estimated Time**: 7-11 hours

---

## Phase 1: Schema Analysis and Preparation

### - [x] 1. Analyze Location 1 (GraphType) Pattern ✅ ALREADY COMPLETE

**Note**: Location 1 (GraphSchemaContent → graphType) was verified to already support 0/1/2-level TI wrappers correctly. Test validation confirms all three levels pass. No changes needed.

Read and document the CORRECT pattern from Location 1 in the schema

- Open `src/grasch/schemas/lex-2026.0.3.2.schema.json`
- Find Location 1 (GraphType) - approximately lines 433-800
- Document the exact `patternProperties` structure
- Note how interpretation facets wrap concreteness facets wrap content
- Create reference notes for replication
- _Requirements: 1.1, 1.2_

### - [ ] 2. Identify Schema Locations for Fixes

Locate the exact line numbers for each of the 6 broken locations

- Find Location 2 (NodeTypesProperty) definition
- Find Location 3 (EdgeTypesProperty) definition
- Find Location 4 (NodeTypeItem) definition
- Find Location 5 (EdgeTypeItem) definition
- Find Location 6 (Individual NodeType) definition
- Find Location 7 (EdgeType Content) definition
- Document current structure at each location
- _Requirements: 2.1-2.7_

### - [ ] 3. Create Schema Backup

Backup the original schema before making changes

- Copy `src/grasch/schemas/lex-2026.0.3.2.schema.json` to `src/grasch/schemas/lex-2026.0.3.2.schema.json.backup`
- Verify backup is complete and valid JSON
- _Requirements: 7.1_

---

## Phase 2: Schema Fixes (6 Locations - CORRECTED)

**Phase 2 Scope - CORRECTED**: Fix **6 broken locations** (2-7) identified in Phase 1 analysis. Location 1 and Location 8 are already working from previous phases.

**Critical Discovery**: Location 1 (GraphSchemaContent) ALREADY supports TI wrappers around `graphType` correctly. Tests confirm 0/1/2-level TI syntax all pass validation.

**Reference Pattern**: GraphType's `patternProperties` implementation (lines 433-800 in schema) is the CORRECT pattern. Use this as the reference for all fixes.

### - [ ] 4. Fix Edge Label Container Structure (E02 - PREREQUISITE)

**CRITICAL**: Must complete BEFORE Locations 3, 5, 7 (which involve edge types)

**Status**: Schema changes complete, initial test files updated. Additional test files need analysis and updates.

Correct edge label containers to always be objects with `typeLabel:` child

- Locate edge label definitions in schema (`via:`, `arc:`, `typeLabel:`)
- Change from polymorphic (string OR object) to ALWAYS object
- Make `typeLabel:` a REQUIRED child property (not a synonym)
- Update schema structure:
  ```json
  "via": {
    "type": "object",
    "properties": {
      "typeLabel": {"type": "string"},
      "implies": {"$ref": "#/$defs/ImpliesPattern"},
      "extends": {"type": "string"},
      "adding": {"$ref": "#/$defs/AddingPattern"}
    },
    "required": ["typeLabel"]
  }
  ```
- Apply same pattern to `arc:`
- Remove `typeLabel:` from edge label synonym group
- Move `implies:` from edgeType level to edge label container level
- Validate JSON syntax
- _Requirements: 1.1, 8.1_
- _Reference: E02-COMPREHENSIVE-FIX-PLAN.md_

**Sub-tasks to complete:**
- [ ] 4.1 Commit current schema and test file changes to GitHub
- [ ] 4.2 Find all YAML files in workspace (excluding archive/deprecated, LEX < 0.3.2)
- [ ] 4.3 Analyze YAML files to identify those with edgeTypes
- [ ] 4.4 Determine which files are additive (not duplicative) to test suite
- [ ] 4.5 Move additive test files to appropriate test directory location
- [ ] 4.6 Update all identified files with new edge label structure
- [ ] 4.7 Validate all updated files pass schema validation

### - [x] 5. Fix Location 1 (graphTypeInterpretation) ✅ ALREADY COMPLETE

**Note**: Verified that GraphSchemaContent already supports TI wrappers correctly. No schema changes needed.

Add TI wrapper support to GraphSchemaContent (wraps the graphType property)

- Locate GraphSchemaContent definition in schema (lines 203-250)
- Add `patternProperties` to support TI wrappers around `graphType`
- Use GraphType's pattern as reference (lines 433-800)
- Allow 0-level (bare `graphType`), 1-level, and 2-level TI syntax
- Ensure only ONE `graphType` can exist (but it can be TI-wrapped)
- Enable TI wrappers as alternatives to bare `graphType`
- Validate JSON syntax
- _Requirements: 1.1, 2.1, 9.1_

### - [ ] 6. Test Edge Label Container Fix (E02)

**Status**: Initial 8 test files updated and validated. Additional test files need analysis and updates.

Validate that edge label container fix works correctly

- Update simple test files to use object form:
  - `test-edge-directed-via.yaml`
  - `test-edge-directed-arc.yaml`
  - `test-edge-directed-typelabel.yaml`
  - `test-edge-undirected-via.yaml`
  - `test-edge-undirected-typelabel.yaml`
  - `test-edge-mixed-synonyms.yaml`
- Update files with properties:
  - `test-edge-property-ordering.yaml`
  - `test-edge-extends-adding.yaml`
- Run validation on updated files
- Verify schema rejects old string form
- _Requirements: 3.1, 3.2, 3.3_
- _Reference: E02-COMPREHENSIVE-FIX-PLAN.md Phase 2_

**Sub-tasks to complete:**
- [ ] 6.1 Analyze all workspace YAML files with edgeTypes (from task 4.3)
- [ ] 6.2 Update test-siblings-* files and other test files with edgeTypes
- [ ] 6.3 Update test-phase-* files that use edgeTypes
- [ ] 6.4 Update test-edge-invalid-* files (negative test cases)
- [ ] 6.5 Validate all updated test files
- [ ] 6.6 Document which files were updated and why

### - [x] 7. Test Location 1 Fix ✅ ALREADY COMPLETE

**Note**: Ran `test_location_1_verification.py` - all three TI levels (0/1/2) pass validation. Location 1 already works correctly.

Validate that Location 1 fix works correctly

- Create test file `src/grasch/examples/test-location-1-graphtype-ti.yaml`
- Test 0-level: bare `graphType`
- Test 1-level: `abstract: { graphType: {...} }`
- Test 2-level: `subtypesOf: { abstract: { graphType: {...} } }`
- Validate all three forms
- _Requirements: 8.1_

### - [ ] 8. Fix Location 2 (nodeTypesInterpretation)

Fix NodeTypesProperty to support sibling TI-wrapped properties

- Locate NodeTypesProperty definition in schema (lines 1824-2150)
- **Problem**: Currently uses `oneOf` pattern (only one option allowed)
- **Target**: Support inline arrays at GraphType level (GraphType already has correct `patternProperties`)
- Note: GraphType level (lines 433-800) already correct - use as reference
- Fix NodeTypesProperty definition to work with GraphType's pattern
- Validate JSON syntax
- _Requirements: 1.1, 2.2, 9.1_

### - [ ] 9. Test Location 2 Fix

Validate that Location 2 fix works correctly

- Run `python validate_phase_e_locations_2_3.py`
- Expect failures (tests use wrong syntax - this is correct)
- Document which test files need updates
- _Requirements: 8.1_

### - [ ] 10. Fix Location 3 (edgeTypesInterpretation)

**DEPENDS ON**: Task 4 (Edge Label Container Fix) must be complete first

Fix EdgeTypesProperty to support sibling TI-wrapped properties

- Locate EdgeTypesProperty definition in schema (lines 2535-2850)
- **Problem**: Currently uses `oneOf` pattern (only one option allowed)
- **Target**: Support inline arrays at GraphType level (GraphType already has correct `patternProperties`)
- Note: GraphType level already correct - use as reference
- Fix EdgeTypesProperty definition to work with GraphType's pattern
- Ensure edge label containers use correct object form (from Task 4)
- Validate JSON syntax
- _Requirements: 1.1, 2.3, 9.1_

### - [ ] 11. Test Location 3 Fix

Validate that Location 3 fix works correctly

- Run `python validate_phase_e_locations_2_3.py`
- Expect failures (tests use wrong syntax)
- Document which test files need updates
- _Requirements: 8.1_

### - [ ] 12. Fix Location 4 (nodeTypeArrayInterpretation)

Apply correct TI pattern to nodeTypeArrayInterpretation (wraps SUBSEQUENCES within nodeTypes array)

- Locate NodeTypeItem definition in schema (~line 2200)
- Restructure to allow TI wrappers wrapping array subsequences (partition blocks)
- Ensure TI wrappers can wrap individual array items as siblings
- Add support for 0-level, 1-level, 2-level syntax
- Validate JSON syntax
- _Requirements: 1.1, 2.4, 9.1_

### - [ ] 13. Fix Location 5 (edgeTypeArrayInterpretation)

**DEPENDS ON**: Task 4 (Edge Label Container Fix) must be complete first

Apply correct TI pattern to edgeTypeArrayInterpretation (wraps SUBSEQUENCES within edgeTypes array)

- Locate EdgeTypeItem definition in schema (~line 2900)
- Restructure to allow TI wrappers wrapping array subsequences (partition blocks)
- Ensure TI wrappers can wrap individual array items as siblings
- Add support for 0-level, 1-level, 2-level syntax
- Ensure edge label containers use correct object form (from Task 4)
- Validate JSON syntax
- _Requirements: 1.1, 2.5, 9.1_

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

## Phase 3: Test File Updates

### - [ ] 18. Identify Failing Test Files

Run validation to identify which test files need syntax updates

- Run `python validate_all_examples.py`
- Document all failing files
- Categorize by location (1, 2, 3, 4, 5, 6, 7)
- Note: Failures are expected and correct - tests use wrong syntax
- _Requirements: 3.1, 3.2_

### - [x] 19. Create Location 1 Test Files ✅ ALREADY COMPLETE

**Note**: Test file `test_location_1_verification.py` already exists and validates all three TI levels. No additional test files needed.

Create test files for Location 1 (GraphSchemaContent with TI wrappers)

- Create `src/grasch/examples/test-location-1-bare.yaml` (0-level)
- Create `src/grasch/examples/test-location-1-one-level.yaml` (1-level)
- Create `src/grasch/examples/test-location-1-two-level.yaml` (2-level)
- Validate all test files
- _Requirements: 3.3, 3.4_

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

### - [ ] 25. Create Sibling Behavior Test Files

Create new test files to validate sibling TI wrapper behavior

- Create `src/grasch/examples/test-siblings-location-1.yaml` (Location 1 siblings - positive)
- Create `src/grasch/examples/test-siblings-locations-2-3.yaml` (Locations 2-3 siblings - positive)
- Create `src/grasch/examples/test-siblings-mixed.yaml` (mixed locations - positive)
- Create `src/grasch/examples/test-siblings-duplicate-INVALID.yaml` (duplicate keys - negative)
- _Requirements: 4.1-4.7, 5.1-5.7_

### - [ ] 26. Create Sibling Validation Script

Create automated test script for sibling behavior

- Create `test_sibling_validation.py`
- Implement positive test cases (should pass)
- Implement negative test cases (should fail)
- Add clear pass/fail reporting
- _Requirements: 5.5_

---

## Phase 4: Validation and Documentation

### - [ ] 27. Run Comprehensive Validation

Validate all examples with fixed schema and updated tests

- Run `python validate_all_examples.py`
- Confirm all valid examples pass
- Confirm invalid examples fail appropriately
- Document any unexpected results
- _Requirements: 8.2, 8.3, 8.4_

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

### - [ ] 32. Create Completion Summary

Write comprehensive summary of refactoring work

- Summarize schema fixes (7 locations, not 6)
- Highlight Location 1 as critical discovery
- Summarize test updates (number of files)
- Report validation results (pass/fail counts)
- Document success criteria met
- Note any issues or deviations
- _Requirements: 7.4, 10.1-10.6_

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

- [x] All 8 locations support 0/1/2-level TI syntax (6 to fix + 2 already working)
- [x] Location 1 (GraphSchemaContent) supports TI wrappers around graphType ✅ VERIFIED
- [ ] Locations 2-3 support multiple sibling TI-wrapped properties
- [ ] TI wrappers appear BEFORE content at all locations
- [ ] Multiple siblings with different interpretation facets work
- [ ] YAML duplicate key constraint properly enforced
- [ ] All test files validate with corrected syntax
- [ ] Phases A-D validation still passes (no regressions)
- [ ] Sibling behavior tests pass at all levels

---

## Notes

- **Incremental Testing**: Test after each location fix to catch issues early
- **Backup**: Keep schema backup until all validation passes
- **Expected Failures**: Test failures after schema fixes are CORRECT - they indicate tests need updating
- **Mindset**: Fix the schema to match the design, then fix the tests to match the design
- **Documentation**: Document as you go - don't wait until the end

