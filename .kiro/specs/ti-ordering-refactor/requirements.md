# Requirements Document: Type Interpretation Ordering Refactor

## Introduction

The LEX-2026.0.3.2 JSON Schema currently has 6 out of 8 Type Interpretation (TI) locations with incorrect ordering patterns where TI wrappers appear AFTER content instead of BEFORE. This violates the fundamental 0-level/1-level/2-level TI architecture. This specification defines the requirements for correcting the schema structure and updating affected test files to match the correct design.

## Glossary

- **Type Interpretation (TI)**: A semantic modifier that controls how element types are validated and instantiated
- **TI Location**: The structural position where a TI can be applied (8 total locations in LEX-2026)
- **TI Wrapper**: The keyword syntax that wraps content (e.g., `abstract:`, `exactlyOf:`, `subtypesOf:`)
- **0-level (bare)**: No wrapper - `typeLabel: Person`
- **1-level (shorthand)**: One wrapper - `abstract: { typeLabel: Person }`
- **2-level (explicit)**: Two wrappers - `subtypesOf: { abstract: { typeLabel: Person } }`
- **Wrong-order pattern**: TI wrapper appears inside content (current broken state)
- **Correct-order pattern**: TI wrapper appears outside content (target state)
- **patternProperties**: JSON Schema mechanism for matching TI keywords
- **Sibling TI wrappers**: Multiple TI wrappers at the same structural level with different interpretation facets
- **Pre-canonical form**: YAML syntax as written by schema authors
- **Canonical form**: Normalized representation after preprocessing

## Requirements

### Requirement 1: Schema Structure Correction

**User Story:** As a schema implementer, I want the JSON Schema to enforce correct TI wrapper ordering at all 8 locations, so that the schema matches the documented TI architecture.

#### Acceptance Criteria

1. THE JSON Schema SHALL enforce that TI wrappers appear BEFORE (outside) content at all 8 TI locations
2. THE JSON Schema SHALL use `patternProperties` to match TI keywords at the correct structural level
3. THE JSON Schema SHALL support 0-level (bare), 1-level (shorthand), and 2-level (explicit) TI syntax at all locations
4. THE JSON Schema SHALL use Location 1 (GraphType) as the reference pattern for correct ordering
5. THE JSON Schema SHALL apply the same correct pattern to Locations 2-7
6. THE JSON Schema SHALL preserve the already-correct pattern at Location 8 (EndpointReference)
7. THE JSON Schema SHALL reject TI wrappers that appear inside content (wrong-order pattern)

### Requirement 2: Location-Specific Corrections

**User Story:** As a schema implementer, I want each of the 6 broken TI locations to be fixed individually, so that I can verify correctness incrementally.

#### Acceptance Criteria

1. WHEN fixing Location 2 (NodeTypesProperty), THE Schema SHALL allow TI wrappers to wrap the `nodeTypes` array property
2. WHEN fixing Location 3 (EdgeTypesProperty), THE Schema SHALL allow TI wrappers to wrap the `edgeTypes` array property
3. WHEN fixing Location 4 (NodeTypeItem), THE Schema SHALL allow TI wrappers to wrap individual items within `nodeTypes` arrays
4. WHEN fixing Location 5 (EdgeTypeItem), THE Schema SHALL allow TI wrappers to wrap individual items within `edgeTypes` arrays
5. WHEN fixing Location 6 (Individual NodeType), THE Schema SHALL allow TI wrappers to wrap single `nodeType` property values
6. WHEN fixing Location 7 (EdgeType Content), THE Schema SHALL allow TI wrappers to wrap single `edgeType` structures
7. THE Schema SHALL maintain Location 8 (EndpointReference) without changes as it is already correct

### Requirement 3: Test File Updates

**User Story:** As a test maintainer, I want test YAML files to use correct TI syntax, so that tests validate the actual design.

#### Acceptance Criteria

1. WHEN the schema is fixed, THE System SHALL identify which test YAML files use wrong-order TI syntax
2. THE System SHALL update identified test files to use correct TI placement (wrappers outside content)
3. THE System SHALL validate that corrected test files pass validation with the fixed schema

### Requirement 4: Sibling TI Wrapper Support (CRITICAL - CURRENTLY BROKEN)

**User Story:** As a schema author, I want to use multiple TI wrappers with different interpretation facets at the same structural level, so that I can express complex type hierarchies.

**CURRENT STATUS**: ❌ BROKEN - The schema currently REJECTS valid sibling patterns due to incorrect use of `patternProperties` that conflict with regular `properties`. This is a critical bug that must be fixed.

#### Acceptance Criteria

1. THE Schema SHALL support multiple sibling `nodeTypes` properties, each with DIFFERENT TI wrappers (e.g., bare `nodeTypes:`, `abstract: { nodeTypes: }`, `exactlyOf: { concrete: { nodeTypes: } }`)
2. THE Schema SHALL support multiple sibling `edgeTypes` properties, each with DIFFERENT TI wrappers
3. THE Schema SHALL support interleaved patterns like `nodeTypes`, `edgeTypes`, `nodeTypes`, `edgeTypes` as siblings at GraphType level
4. THE Schema SHALL support sibling partition blocks within `nodeTypes` and `edgeTypes` arrays (Locations 4-5)
5. THE Schema SHALL rely on YAML's duplicate key prevention to reject same interpretation facet appearing twice
6. THE Schema SHALL allow nested concreteness facets under the same interpretation facet (e.g., `exactlyOf: { concrete: {...}, abstract: {...} }`)
7. THE Schema SHALL NOT use `additionalProperties: false` or similar constraints that prevent sibling TI wrappers from coexisting with regular properties

### Requirement 5: Validation Testing

**User Story:** As a quality assurance engineer, I want comprehensive tests for sibling TI wrapper behavior, so that I can verify the schema works correctly.

#### Acceptance Criteria

1. THE System SHALL provide positive test cases demonstrating valid sibling patterns at GraphType level
2. THE System SHALL provide positive test cases demonstrating valid sibling patterns at array level
3. THE System SHALL provide positive test cases demonstrating mixed sibling patterns across levels
4. THE System SHALL provide negative test cases demonstrating invalid duplicate property patterns
5. THE System SHALL provide a validation script that tests both positive and negative cases
6. THE System SHALL validate that all positive test cases pass
7. THE System SHALL validate that all negative test cases fail with appropriate error messages



### Requirement 6: Documentation and Traceability

**User Story:** As a future maintainer, I want clear documentation of what was changed and why, so that I can understand the refactoring rationale.

#### Acceptance Criteria

1. THE System SHALL document the specific schema changes made at each of the 6 locations
2. THE System SHALL document which test YAML files were updated and what syntax changes were made
3. THE System SHALL document the validation results before and after the fix
4. THE System SHALL create a completion summary explaining the refactoring impact
5. THE System SHALL archive superseded analysis documents to prevent confusion
6. THE System SHALL update the TI documentation index to reflect current authoritative documents

### Requirement 7: Incremental Validation

**User Story:** As a schema implementer, I want to validate changes incrementally, so that I can catch errors early and isolate issues.

#### Acceptance Criteria

1. THE System SHALL support validating individual location fixes before proceeding to the next
2. THE System SHALL provide location-specific validation scripts (e.g., `validate_phase_e_locations_2_3.py`)
3. THE System SHALL validate that fixing one location does not break other locations
4. THE System SHALL validate all examples after each location fix
5. THE System SHALL provide clear error messages indicating which location has issues

### Requirement 8: Pattern Consistency

**User Story:** As a schema designer, I want all TI locations to use the same structural pattern, so that the schema is internally consistent and maintainable.

#### Acceptance Criteria

1. THE Schema SHALL use the same `patternProperties` approach at all TI locations
2. THE Schema SHALL use the same wrapper keyword matching pattern at all locations
3. THE Schema SHALL use the same nesting structure (interpretation facet → concreteness facet → content) at all locations
4. THE Schema SHALL use consistent property names and structure across all locations
5. THE Schema SHALL follow the same ordering principle as edge type endpoint specifications

### Requirement 9: Success Criteria Validation

**User Story:** As a project manager, I want clear success criteria to determine when the refactoring is complete, so that I know when to proceed to the next phase.

#### Acceptance Criteria

1. WHEN all 8 locations support 0/1/2-level TI syntax, THE Refactoring SHALL be considered structurally complete
2. WHEN all test YAML files validate with the fixed schema, THE Refactoring SHALL be considered functionally complete
3. WHEN sibling TI wrapper tests pass, THE Refactoring SHALL be considered feature-complete
4. WHEN documentation is updated, THE Refactoring SHALL be considered delivery-ready
5. THE System SHALL validate all 4 completion criteria before declaring the refactoring done
