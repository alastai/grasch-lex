# Import Schema Consistency Tasks

## Overview

This document outlines the specific tasks needed to implement TI-based import consistency in the LEX-2026.0.3.2 JSON Schema, with proper understanding that **sets of types (including singleton sets) are delimited by indentation under type interpretations**.

## Task Breakdown

### Phase 1: Analysis and Preparation

- [x] 1. Complete TI Location Audit
  - Systematically identify all locations in the schema where TI wrappers can contain importable content
  - Categorize by context (top-level, array items, nested)
  - Document current import support status for each location
  - Identify how indentation delimits type sets at each location
  - Create gap analysis document
  - **Deliverables**: `TI-LOCATION-AUDIT.md` with comprehensive mapping and indentation analysis
  - _Requirements: FR-2, FR-3_

- [ ] 2. Create Reusable Schema Definitions (REVISED)
  - Create reusable JSON Schema definitions for two-phase import patterns
  - Define `TIWrapperContent` pattern (anyOf singleton/array + import for type sets)
  - Define `TIWrapperContentNode` and `TIWrapperContentEdge` variants
  - Define `PartitionBlockItem` pattern (TI wrapper + Phase 1 import)
  - Define `PartitionBlockItemNode` and `PartitionBlockItemEdge` variants
  - Ensure patterns support indentation-based set delimitation
  - Document how anyOf handles both singleton and array forms
  - Document two-phase import mechanism (Phase 1: import TI+content, Phase 2: import content only)
  - **Deliverables**: Updated schema with new `$defs` section containing reusable patterns
  - _Requirements: FR-1, FR-3_
  - **Key Insight**: Must align with actual schema structure:
    - `GraphType.properties.nodeTypes` → can be array of partition blocks
    - `GraphType.properties.edgeTypes` → can be array of partition blocks
    - `GraphType.subtypesOf.abstract.nodeTypes` → nested TI context
    - `NodeTypeItem` → items in nodeTypes arrays
    - `EdgeTypeItem` → items in edgeTypes arrays

### Phase 2: Schema Updates

- [ ] 3. Fix NodeTypes Import Patterns
  - Update `NodeTypesProperty` to support imports at all TI levels
  - Update `NodeTypeItem` TI wrapper contents to support imports
  - Update `GraphType.subtypesOf.abstract.nodeTypes` to support imports
  - Update `GraphType.subtypesOf.nodeTypes` to support imports
  - Ensure all nested TI contexts support imports
  - Support both singleton and multi-element type sets
  - Validate indentation-based set delimitation
  - **Deliverables**: Updated NodeTypes definitions with test cases
  - _Requirements: FR-2, FR-3, FR-4_

- [ ] 4. Fix EdgeTypes Import Patterns
  - Update `EdgeTypesProperty` to support imports at all TI levels
  - Update `EdgeTypeItem` TI wrapper contents to support imports
  - Update `GraphType.subtypesOf.abstract.edgeTypes` to support imports
  - Update `GraphType.subtypesOf.edgeTypes` to support imports
  - Ensure all nested TI contexts support imports
  - Support both singleton and multi-element type sets
  - Validate indentation-based set delimitation
  - **Deliverables**: Updated EdgeTypes definitions with test cases
  - _Requirements: FR-2, FR-3, FR-4_

- [ ] 5. Fix Sealed and Final Wrapper Contents
  - Ensure `NodeTypeItem.sealed.nodeTypes` supports imports
  - Ensure `EdgeTypeItem.sealed.edgeTypes` supports imports
  - Ensure `final` wrapper contents support imports
  - Pattern properties handle all wrapper types
  - Support singleton sets (single type under wrapper)
  - **Deliverables**: Updated sealed/final wrapper definitions
  - _Requirements: FR-2, FR-4_

- [ ] 6. Fix Remaining Nested Contexts
  - Address any remaining nested contexts that need import support
  - Ensure `Directory.directories` supports imports (if applicable)
  - Update any other nested TI contexts
  - Ensure pattern properties are comprehensive
  - Validate all indentation-based set boundaries
  - **Deliverables**: Updated definitions for all remaining contexts
  - _Requirements: FR-2, FR-3_

### Phase 3: Validation and Testing

- [ ] 7. Create TI Import Test Cases
  - Create coarse partition tests (one TI, multiple types)
  - Create fine partition tests (each type in own TI - singleton sets)
  - Create mixed partition tests (combination of cardinalities)
  - Create nested TI import tests
  - Create PC and C form validation tests
  - Test indentation-based set delimitation
  - **Deliverables**: `test_ti_import_patterns.py` with comprehensive test suite
  - _Requirements: All FRs_

- [ ] 8. Update Validation Pipeline
  - Update `validate_pc_and_c_forms.py` to include TI import tests
  - Test all partition granularities
  - Test singleton sets vs multi-element sets
  - Clear reporting of TI-specific validation results
  - Performance benchmarking included
  - **Deliverables**: Updated validation pipeline with TI import test results
  - _Requirements: All FRs, NFR-3_

- [ ] 9. Regression Testing
  - Ensure all existing test cases pass
  - No performance degradation
  - Backward compatibility maintained
  - All example files validate
  - Indentation patterns work correctly
  - **Deliverables**: Regression test results and performance comparison
  - _Requirements: NFR-2, NFR-3_

### Phase 4: Documentation and Cleanup

- [ ] 10. Update Schema Documentation
  - Update schema comments to explain TI import patterns
  - Add import pattern examples showing indentation-based set delimitation
  - Document TI partition flexibility (coarse, fine, mixed)
  - Explain singleton sets as special case (cardinality 1)
  - Create migration guide (if needed)
  - **Deliverables**: Updated schema with comprehensive comments
  - _Requirements: C-4_

- [ ] 11. Create Example Files
  - Create coarse partition example (multi-element sets)
  - Create fine partition example (singleton sets)
  - Create mixed partition example (mixed cardinalities)
  - Create nested TI import example
  - Show indentation clearly delimiting type sets
  - All examples validate in both PC and C forms
  - **Deliverables**: Example YAML files in `src/grasch/examples/`
  - _Requirements: C-4_

- [ ] 12. Final Validation and Cleanup
  - Schema passes all validation tests
  - Code is clean and well-commented
  - All deliverables are complete
  - Documentation is accurate and complete
  - Indentation-based set delimitation is clear
  - **Deliverables**: Final schema file, complete test suite, final documentation
  - _Requirements: All requirements_

## Key Concepts to Validate

### Indentation-Based Set Delimitation
Each task must validate that:
- Types at the same indentation level under a TI belong to the same set
- TI wrapper keywords establish set boundaries
- Concreteness/abstractness keywords further delimit sets
- Singleton sets (cardinality 1) are properly supported
- Multi-element sets (cardinality > 1) are properly supported

### Partition Flexibility
Each task must ensure:
- Coarsest partition: One TI wraps all N types (1 partition block)
- Finest partition: Each type gets its own TI (N singleton sets)
- Intermediate partitions: Any valid grouping in between
- Mixed partitions: Combination of different cardinalities

## Success Criteria

### Functional Success
- [ ] All PC forms with TI imports validate successfully
- [ ] All C forms (canonicalized) validate successfully
- [ ] All partition granularities (coarse, fine, mixed) work
- [ ] Singleton sets (cardinality 1) validate correctly
- [ ] Multi-element sets (cardinality > 1) validate correctly
- [ ] Indentation-based set delimitation works correctly
- [ ] No regression in existing functionality

### Quality Success
- [ ] Schema is consistent and maintainable
- [ ] Import patterns are uniform across all TI locations
- [ ] Documentation clearly explains indentation-based set delimitation
- [ ] Examples show various partition cardinalities
- [ ] Test coverage is complete

### Performance Success
- [ ] Validation performance is acceptable
- [ ] No significant degradation from baseline
- [ ] Complex partition structures validate efficiently

## Timeline

**Total Estimated Effort**: 32 hours

**Phase 1**: 5 hours (Analysis and Preparation)
**Phase 2**: 13 hours (Schema Updates)
**Phase 3**: 9 hours (Validation and Testing)
**Phase 4**: 5 hours (Documentation and Cleanup)

**Recommended Schedule**: 2-3 weeks with parallel work where possible

## Dependencies

**External Dependencies**:
- Access to existing validation pipeline
- Ability to modify schema files
- Test environment for validation

**Internal Dependencies**:
- Understanding of TI semantics (complete)
- Understanding that indentation delimits type sets (complete)
- Understanding that singleton sets are special cases (complete)
- Knowledge of existing schema structure (available)
- Canonicalization process understanding (available)

## Risk Management

### High Risk: Schema Complexity
**Mitigation**: 
- Use reusable definitions extensively
- Create clear documentation emphasizing indentation-based set delimitation
- Test incrementally

### Medium Risk: Backward Compatibility
**Mitigation**:
- Extensive regression testing
- Careful review of existing examples
- Gradual rollout if needed

### Low Risk: Performance Impact
**Mitigation**:
- Performance benchmarking
- Optimization if needed
- Monitoring in production

### Medium Risk: Indentation Ambiguity
**Mitigation**:
- Clear examples showing set delimitation
- Comprehensive documentation
- Validation error messages that reference indentation
