# Implementation Plan

- [x] 1. Audit current examples for aesthetic issues
  - Scan all YAML files in `src/grasch/examples/`
  - Document verbose patterns that need cleanup
  - Identify files requiring updates
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 2. Update SNB hierarchy import files
  - [x] 2.1 Update organisation hierarchy
    - Remove redundant typeLabel from implies/adding
    - Simplify extends syntax to scalar form
    - _Requirements: 1.1, 1.3, 2.1, 2.3_
  
  - [x] 2.2 Update place hierarchy
    - Apply same aesthetic cleanup
    - _Requirements: 1.1, 1.3, 2.1, 2.3_
  
  - [ ] 2.3 Update message hierarchy
    - Apply same aesthetic cleanup
    - _Requirements: 1.1, 1.3, 2.1, 2.3_

- [ ] 3. Update main example files
  - [-] 3.1 Update type-definition-syntax-examples.yaml
    - Clean up all type definitions
    - Use bracketed arrays for label sets
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
  
  - [ ] 3.2 Update snb-schema.yaml
    - Apply aesthetic cleanup throughout
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
  
  - [ ] 3.3 Update finbench-schema.yaml
    - Apply aesthetic cleanup throughout
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
  
  - [ ] 3.4 Update other example files
    - Review and clean remaining examples
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 4. Update JSON schema validation rules
  - [ ] 4.1 Make extends accept scalar or object
    - Modify extends definition to use oneOf pattern
    - Test with both scalar and object forms
    - _Requirements: 2.1, 2.5, 6.1_
  
  - [ ] 4.2 Make implies.labels optional
    - Update schema to not require labels when typeLabel present
    - _Requirements: 1.4, 4.3, 6.2_
  
  - [ ] 4.3 Make adding.labels optional
    - Update schema to not require labels in adding section
    - _Requirements: 1.3, 4.2, 6.3_
  
  - [ ] 4.4 Accept both array formats for labels
    - Ensure flow-style and block-style both validate
    - _Requirements: 3.4, 6.4_

- [ ] 5. Validate all examples
  - Run validation suite on all updated examples
  - Ensure backward compatibility maintained
  - Fix any validation failures
  - _Requirements: 5.5, 6.5_

- [ ] 6. Refactor nullability syntax
  - [ ] 6.1 Update JSON schema for nullability
    - Remove `notNull:` key from schema
    - Add validation for `?` suffix in property names
    - _Requirements: 7.4, 7.5_
  
  - [ ] 6.2 Update property type parsing
    - Parse `name: identifier` as NOT NULL
    - Parse `name: identifier?` as NULLABLE
    - _Requirements: 7.1, 7.2_
  
  - [ ] 6.3 Implement API methods
    - Add `isNullable()` method
    - Add `isNotNull()` method
    - Add `isNotNullable()` method (synonym for isNotNull)
    - _Requirements: 7.3_
  
  - [ ] 6.4 Update all examples for nullability
    - Replace `notNull: true` with plain `name: identifier`
    - Replace `notNull: false` or omitted with `name: identifier?`
    - Update all YAML examples
    - _Requirements: 7.6_
  
  - [ ]* 6.5 Write property tests for nullability
    - **Property 6: Nullability Syntax Round-Trip**
    - **Validates: Requirements 7.1, 7.3**
  
  - [ ]* 6.6 Write property tests for nullable syntax
    - **Property 7: Nullable Syntax Round-Trip**
    - **Validates: Requirements 7.2, 7.3**
  
  - [ ]* 6.7 Write validation tests for notNull rejection
    - **Property 8: notNull Key Rejection**
    - **Validates: Requirements 7.4, 7.5**

- [ ] 7. Update documentation
  - Update any guides referencing old syntax
  - Add aesthetic principles to documentation
  - Document new nullability syntax
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.6_

- [ ] 8. Final checkpoint
  - Ensure all tests pass, ask the user if questions arise.
