# Requirements Document: Type Interpretation System Simplification

## Introduction

This specification defines the requirements for fundamentally simplifying the Type Interpretation (TI) system in LEX-2026.0.3.2 from a complex two-level architecture to a streamlined single-level system. The simplification includes four major changes: eliminating freestanding types, preventing TI nesting, and consolidating the TI system into three primary forms with synonyms. This represents a major architectural improvement that will make the system significantly easier to understand, implement, and maintain.

## Glossary

- **Type Interpretation (TI)**: A semantic modifier that controls how element types are validated and instantiated using a single-level keyword system
- **TI Location**: The structural position where a TI can be applied (8 total locations in LEX-2026)
- **TI Wrapper**: A single keyword that wraps content (e.g., `exactlyOfConcrete:`, `subtypeOfConcrete:`, `subtypeOfAbstract:`)
- **Primary TI Forms**: The three canonical TI keywords: `exactlyOfConcrete`, `subtypeOfConcrete`, `subtypeOfAbstract`
- **TI Synonyms**: Alternative keywords that map to primary forms: `exactlyOf`, `concrete`, `subtypeOf`, `properSubtypeOf`
- **0-level (bare)**: No wrapper - `typeLabel: Person` - Implicit `exactlyOfConcrete` semantics
- **1-level (wrapped)**: Single TI wrapper - `concrete: { typeLabel: Person }` or `exactlyOfConcrete: { typeLabel: Person }`
- **Canonical form**: Normalized representation using primary TI forms after preprocessing
- **Pre-canonical form**: YAML syntax as written by schema authors using synonyms
- **Sibling TI wrappers**: Multiple TI wrappers at the same structural level with different TI forms
- **Array/Sequence**: A collection of element types (nodeTypes or edgeTypes) that can be partitioned into subsequences, each with its own TI wrapper
- **Freestanding type**: Individual nodeType or edgeType not part of an array (ELIMINATED in this specification)
- **TI Nesting**: One TI wrapper containing another TI wrapper (PROHIBITED in this specification)
- **Type Finalization**: A separate system from type interpretation using `final:` and `sealed:` keywords (out of scope for this specification)

## Requirements

### Requirement 1: Single-Level TI System Implementation

**User Story:** As a schema implementer, I want the JSON Schema to implement a simplified single-level TI system with three primary forms, so that the system is easier to understand and maintain.

#### Acceptance Criteria

1. THE JSON Schema SHALL support exactly three primary TI forms: `exactlyOfConcrete`, `subtypeOfConcrete`, `subtypeOfAbstract`
2. THE JSON Schema SHALL support four TI synonyms that map to primary forms: `exactlyOf` and `concrete` (both map to `exactlyOfConcrete`), `subtypeOf` (maps to `subtypeOfConcrete`), `properSubtypeOf` (maps to `subtypeOfAbstract`)
3. THE JSON Schema SHALL support 0-level (bare) and 1-level (wrapped) TI syntax at all locations
4. THE JSON Schema SHALL use explicit properties exclusively for all TI keywords
5. THE JSON Schema SHALL eliminate the complex two-level TI architecture (interpretation facet + concreteness facet)
6. THE JSON Schema SHALL ensure TI wrappers appear BEFORE (outside) content at all locations
7. THE JSON Schema SHALL reject any nested TI wrapper patterns

### Requirement 2: Array-Only Type Organization

**User Story:** As a schema author, I want all types to be organized in arrays or sequences, so that the structure is consistent and freestanding types are eliminated.

#### Acceptance Criteria

1. THE Schema SHALL eliminate all freestanding nodeType or edgeType definitions that are not part of an array or sequence
2. THE Schema SHALL require all nodeTypes to be contained within nodeTypes arrays or subsequences
3. THE Schema SHALL require all edgeTypes to be contained within edgeTypes arrays or subsequences
4. THE Schema SHALL support TI wrappers around entire arrays (collection-level TI)
5. THE Schema SHALL support TI wrappers around subsequences within arrays (subsequence-level TI)
6. THE Schema SHALL maintain the array subsequence model for partitioning type collections
7. THE Schema SHALL ensure consistent structural organization across all TI locations

### Requirement 3: TI Nesting Prevention

**User Story:** As a schema author, I want the system to prevent any form of TI nesting, so that the structure remains simple and predictable.

#### Acceptance Criteria

1. THE Schema SHALL prohibit any TI wrapper from containing another TI wrapper directly
2. THE Schema SHALL prohibit any TI wrapper from containing another TI wrapper indirectly
3. THE Schema SHALL reject any immediate TI wrapper containment patterns
4. THE Schema SHALL enforce that type interpretations cannot contain other type interpretations at any level
5. THE Schema SHALL provide clear validation errors when TI nesting is attempted
6. THE Schema SHALL maintain the flat, non-nested TI architecture throughout the system

### Requirement 4: Sibling TI Wrapper Support

**User Story:** As a schema author, I want to use multiple TI wrappers with different TI forms at the same structural level, so that I can express different type interpretation semantics.

#### Acceptance Criteria

1. THE Schema SHALL support multiple sibling TI wrappers with different primary forms (e.g., `exactlyOfConcrete:`, `subtypeOfConcrete:`, `subtypeOfAbstract:`)
2. THE Schema SHALL support multiple sibling TI wrappers using synonyms (e.g., `concrete:`, `subtypeOf:`, `properSubtypeOf:`)
3. THE Schema SHALL support sibling TI-wrapped collections at GraphType level (e.g., `concrete: { nodeTypes: [...] }`, `subtypeOfAbstract: { edgeTypes: [...] }`)
4. THE Schema SHALL support sibling TI-wrapped subsequences within arrays
5. THE Schema SHALL rely on YAML's duplicate key prevention to reject duplicate TI forms
6. THE Schema SHALL use explicit properties exclusively to enable sibling TI wrapper coexistence
7. THE Schema SHALL support interleaved patterns of different TI forms as siblings

### Requirement 5: Canonicalization and Synonym Mapping

**User Story:** As a system implementer, I want TI synonyms to be automatically converted to their canonical primary forms during processing, so that the system has consistent internal representation.

#### Acceptance Criteria

1. THE System SHALL map `exactlyOf` and `concrete` synonyms to the canonical `exactlyOfConcrete` form
2. THE System SHALL map `subtypeOf` synonym to the canonical `subtypeOfConcrete` form  
3. THE System SHALL map `properSubtypeOf` synonym to the canonical `subtypeOfAbstract` form
4. THE System SHALL perform canonicalization during preprocessing before validation
5. THE System SHALL maintain synonym support in pre-canonical YAML for author convenience
6. THE System SHALL use only canonical forms in the internal representation
7. THE System SHALL document the mapping between synonyms and canonical forms clearly



### Requirement 6: Test File Updates

**User Story:** As a test maintainer, I want test YAML files to use the simplified TI syntax, so that tests validate the new single-level system.

#### Acceptance Criteria

1. THE System SHALL identify test files using the old two-level TI syntax
2. THE System SHALL update test files to use the new single-level TI syntax
3. THE System SHALL update test files to use only array-based type organization
4. THE System SHALL ensure test files demonstrate proper sibling TI wrapper usage
5. THE System SHALL create test files for canonical form validation
6. THE System SHALL create test files for synonym-to-canonical mapping
7. THE System SHALL validate that all updated test files pass with the new schema

### Requirement 7: Validation Testing

**User Story:** As a quality assurance engineer, I want comprehensive tests for the simplified TI system, so that I can verify all functionality works correctly.

#### Acceptance Criteria

1. THE System SHALL provide positive test cases for all three primary TI forms
2. THE System SHALL provide positive test cases for all four TI synonyms
3. THE System SHALL provide test cases demonstrating sibling TI wrapper patterns
4. THE System SHALL provide test cases demonstrating array-only type organization
5. THE System SHALL provide negative test cases for prohibited TI nesting patterns
6. THE System SHALL provide test cases for canonicalization and synonym mapping
7. THE System SHALL validate that all test cases produce expected results

### Requirement 8: Pattern Consistency

**User Story:** As a schema designer, I want all TI locations to use the same simplified structural pattern, so that the schema is internally consistent and maintainable.

#### Acceptance Criteria

1. THE Schema SHALL use explicit properties exclusively at all TI locations
2. THE Schema SHALL use the same single-level TI pattern at all locations
3. THE Schema SHALL use consistent TI keyword naming across all locations
4. THE Schema SHALL apply the same array-only organization principle at all locations
5. THE Schema SHALL maintain the same TI-before-content ordering at all locations
6. THE Schema SHALL use the same canonicalization rules at all locations

### Requirement 9: Explicit Properties Design Principle

**User Story:** As a schema maintainer, I want the schema to use explicit properties exclusively for all TI wrappers, so that the schema is predictable, maintainable, and supports proper sibling TI wrapper behavior.

#### Acceptance Criteria

1. THE Schema SHALL use explicit properties exclusively for all TI keywords (`exactlyOfConcrete`, `subtypeOfConcrete`, `subtypeOfAbstract`, `exactlyOf`, `concrete`, `subtypeOf`, `properSubtypeOf`)
2. THE Schema SHALL NOT use `patternProperties` anywhere in the TI wrapper implementation
3. THE Schema SHALL define each TI keyword as an explicit property with clear semantics
4. THE Schema SHALL enable sibling TI wrappers through explicit property definitions
5. THE Schema SHALL use `oneOf` constraints only where exactly one TI wrapper is permitted
6. THE Schema SHALL provide better IDE support through explicit property definitions
7. THE Schema SHALL eliminate all conflicts between pattern properties and regular properties

### Requirement 10: Success Criteria Validation

**User Story:** As a project manager, I want clear success criteria to determine when the TI simplification is complete, so that I know when to proceed to the next phase.

#### Acceptance Criteria

1. WHEN all 8 locations support the single-level TI system with three primary forms, THE Simplification SHALL be considered structurally complete
2. WHEN all types are organized in arrays with no freestanding types, THE Simplification SHALL be considered organizationally complete
3. WHEN TI nesting is completely prevented throughout the system, THE Simplification SHALL be considered architecturally complete
4. WHEN canonicalization correctly maps all synonyms to primary forms, THE Simplification SHALL be considered functionally complete
5. WHEN all test files validate with the simplified schema, THE Simplification SHALL be considered validation-complete
6. THE System SHALL validate all 5 completion criteria before declaring the simplification done
