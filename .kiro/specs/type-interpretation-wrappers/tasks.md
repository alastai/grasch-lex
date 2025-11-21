# Implementation Plan: Type Interpretation Wrapper System

- [x] 1. Update JSON Schema for type interpretation wrappers
  - Update `lex-2026.0.3.2.schema.json` (the single schema) to accept wrapper syntax around type reference properties
  - Define patterns for zero-level (bare), one-level, and two-level wrappers
  - Enforce fixed wrapper order: subtype matching mode → concreteness → property
  - Support wrappers around `nodeType`, `graphType` properties
  - Support wrappers around `nodeTypes`, `edgeTypes` array properties
  - Support wrappers around individual array items
  - Support wrappers around entire edgeType structures
  - Support wrappers around individual edgeType components (from, via/arc, to)
  - Support node type identifiers as strings, arrays, or integer literals in edgeType components
  - Remove deprecated `direction:` property pattern
  - Add support for `directed:` and `undirected:` keywords
  - Add validation to prevent wrapper nesting
  - Add validation to reject incorrect wrapper order
  - Ensure schema validates both pre-canonical forms (with convenience syntax) and canonical forms (normalized)
  - Validate `import:` statements structurally in pre-canonical form
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14, 3.15, 6.1, 6.2, 6.3, 6.4, 6.5, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [x] 2. Implement canonicalization logic in import preprocessor
- [x] 2.1 Add wrapper detection and parsing
  - Detect wrapper keywords (`abstract`, `concrete`, `properSubtypesOf`, `exactlyOf`, `subtypesOf`) at valid locations
  - Parse wrapper structure to extract type reference and interpretation dimensions
  - Handle wrappers around single properties and array properties
  - Handle wrappers around individual array items
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [x] 2.2 Implement wrapper canonicalization rules
  - Canonicalize zero-level (bare) references to `exactlyOf: concrete:` form
  - Canonicalize `properSubtypesOf:` to `subtypesOf: abstract:` form
  - Canonicalize `concrete:` to `exactlyOf: concrete:` form
  - Canonicalize `abstract:` to `subtypesOf: abstract:` form
  - Preserve two-level wrappers as-is (already canonical)
  - Follow same canonicalization pattern as edge type endpoints (synonym keywords → canonical form)
  - Handle edgeType-level wrappers (apply to all components)
  - Handle edgeType component-level wrappers (independent of edgeType-level)
  - Ensure no wrapper inheritance from edgeType to components
  - Default unwrapped edgeType components to `exactlyOf: concrete:`
  - Validate wrapper keyword order during canonicalization
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 10.1, 10.2, 10.3, 10.4_

- [x] 2.3 Add wrapper nesting validation
  - Detect nested wrapper patterns during canonicalization
  - Raise clear error when wrapper nesting is detected
  - _Requirements: 3.11, 7.1_

- [x] 2.4 Preserve wrapper semantics through import resolution
  - Ensure wrapper interpretation is maintained when merging imported files
  - Apply wrapper semantics consistently across import boundaries
  - _Requirements: 6.6_

- [x] 3. Define logical model data structures
- [x] 3.1 Create SubtypeMatchingMode enumeration
  - Define `EXACTLY_OF` and `SUBTYPES_OF` values
  - _Requirements: 1.2, 1.3_

- [x] 3.2 Create Concreteness enumeration
  - Define `CONCRETE` and `ABSTRACT` values
  - _Requirements: 1.4, 1.5_

- [x] 3.3 Create TypeInterpretation class
  - Store type reference string
  - Store subtype matching mode
  - Store concreteness
  - Implement `isExactMatch()` method
  - Implement `allowsSubtypes()` method
  - Implement `isConcrete()` method
  - Implement `isAbstract()` method
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 4. Update element type classes with interpretation support
- [x] 4.1 Add TypeInterpretation to NodeType
  - Add `interpretation` property to NodeType class
  - Implement `isAbstract()` method
  - Implement `isConcrete()` method
  - Implement `isExactMatch()` method
  - Implement `allowsSubtypes()` method
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 4.2 Add TypeInterpretation to EdgeType
  - Add `interpretation` property to EdgeType class for edgeType-level interpretation
  - Add `fromInterpretation` property for source node type interpretation
  - Add `viaInterpretation` property for edge content interpretation
  - Add `toInterpretation` property for target node type interpretation
  - Implement `isAbstract()` method (for edgeType-level)
  - Implement `isConcrete()` method (for edgeType-level)
  - Implement `isExactMatch()` method (for edgeType-level)
  - Implement `allowsSubtypes()` method (for edgeType-level)
  - Implement component-specific query methods (e.g., `fromIsAbstract()`, `viaIsConcrete()`, `toAllowsSubtypes()`)
  - _Requirements: 4.5, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7_

- [x] 4.3 Add TypeInterpretation to GraphType
  - Add `interpretation` property to GraphType class
  - Implement `isAbstract()` method
  - Implement `isConcrete()` method
  - Implement `isExactMatch()` method
  - Implement `allowsSubtypes()` method
  - _Requirements: 4.6_

- [x] 5. Implement validation logic for type interpretations
- [x] 5.1 Add abstract type validation
  - Check that abstract types are not directly instantiated
  - Raise error when direct instantiation of abstract type is detected
  - _Requirements: 5.4, 7.4_

- [x] 5.2 Add exact match validation
  - Check that exact match types do not accept subtypes
  - Raise error when subtype is provided where exact match required
  - _Requirements: 5.1, 7.5_

- [x] 5.3 Add subtype match validation
  - Check that subtype match types accept the type or any subtype
  - Allow instances of the type or proper subtypes
  - _Requirements: 5.2_

- [x] 5.4 Add concrete type validation
  - Check that concrete types can be directly instantiated
  - Allow direct instances of concrete types
  - _Requirements: 5.3_

- [x] 5.5 Apply validation consistently across element types
  - Use same validation logic for nodeType, edgeType, and graphType references
  - _Requirements: 5.5_

- [x] 6. Create comprehensive example files
- [x] 6.1 Create zero-level wrapper examples
  - Example with bare `nodeType` reference
  - Example with bare `edgeType` reference
  - Example with bare `nodeTypes` array
  - _Requirements: 8.1_

- [x] 6.2 Create one-level wrapper examples
  - Example with `abstract:` wrapper
  - Example with `concrete:` wrapper
  - Example with `properSubtypesOf:` wrapper
  - _Requirements: 8.2_

- [x] 6.3 Create two-level wrapper examples
  - Example with `exactlyOf: concrete:` wrapper
  - Example with `subtypesOf: abstract:` wrapper
  - Example with all four valid two-level combinations
  - _Requirements: 8.3_

- [x] 6.4 Create single property wrapper examples
  - Example wrapping single `nodeType` property
  - Example wrapping single `edgeType` property
  - Example wrapping single `graphType` property
  - _Requirements: 8.4_

- [x] 6.5 Create array wrapper examples
  - Example wrapping entire `nodeTypes` array
  - Example wrapping entire `edgeTypes` array
  - _Requirements: 8.5_

- [x] 6.6 Create array item wrapper examples
  - Example with wrappers around individual `nodeTypes` items
  - Example with wrappers around individual `edgeTypes` items
  - _Requirements: 8.6_

- [x] 6.7 Create subsequence wrapper examples
  - Example with wrapper around contiguous subsequence of `nodeTypes`
  - Example with wrapper around contiguous subsequence of `edgeTypes`
  - _Requirements: 8.7_

- [x] 6.8 Create mixed wrapper examples
  - Example with mixed wrapped and unwrapped items in same array
  - Example with different wrapper types in same schema
  - _Requirements: 8.8_

- [x] 6.9 Create edgeType-specific wrapper examples
  - Example with wrapper around entire edgeType structure
  - Example with wrappers on individual edgeType components
  - Example demonstrating no wrapper inheritance from edgeType to components
  - Example with usage-level interpretation override (concrete type treated as abstract)
  - Example using `directed:` syntax
  - Example using `undirected:` syntax
  - Example with `via:` and `arc:` synonyms
  - _Requirements: 8.10, 8.11, 8.12, 8.13, 8.14, 9.1, 9.2, 9.5, 9.6_

- [x] 6.10 Create invalid wrapper examples
  - Example demonstrating nested wrapper error
  - Example demonstrating wrapper inside nodeType definition error
  - Example demonstrating deprecated `direction:` property error
  - _Requirements: 8.9, 9.3_

- [x] 6.11 Validate all example files
  - Run schema validation on all valid examples
  - Verify invalid examples produce expected errors
  - _Requirements: 8.15_

- [x] 7. Update validation test reporting
  - Update test scripts to report "pre-canonical validation: passed/failed"
  - Update test scripts to report "canonical validation: passed/failed"
  - Remove all references to deprecated "pre-import" and "post-import" terminology
  - Ensure tests validate files in both pre-canonical and canonical forms against the same single schema
  - Test that pre-canonical files with unresolvable imports still pass structural validation
  - Test that canonical files pass both structural and semantic validation
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7_

- [ ] 8. Update documentation
  - Document type interpretation wrapper system in main README
  - Document single-schema architecture (one schema validates both pre-canonical and canonical forms)
  - Document canonicalization architecture pattern
  - Document analogy to edge type endpoint syntax (fixed order, synonym canonicalization)
  - Document wrapper syntax and semantics
  - Document fixed wrapper order requirement
  - Document API methods for querying interpretation
  - Use correct terminology: "pre-canonical" and "canonical" (not deprecated "pre-import" and "post-import")
  - Provide usage examples and best practices
  - Document edge type component-level interpretation
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.7, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.13, 12.14, 12.15_
