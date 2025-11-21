# Implementation Plan

- [x] 1. Create new schema component definitions
  - Create `NodeTypeItem`, `NodeTypesArray`, `NodeTypesProperty` definitions in JSON Schema
  - Create `EdgeTypeItem`, `EdgeTypesArray`, `EdgeTypesProperty` definitions in JSON Schema
  - Ensure terminal `NodeType` and `EdgeType` definitions never contain type arrays
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 3.1, 3.2, 3.3_

- [x] 2. Replace existing nodeTypes schema structure
  - Remove complex nested oneOf patterns from lines 448-750
  - Replace with clean layered structure using new component definitions
  - Ensure `nodeTypes` property in GraphSchemaContent uses `NodeTypesProperty`
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 3.4_

- [x] 3. Replace existing edgeTypes schema structure
  - Apply same pattern to edgeTypes as nodeTypes
  - Use `EdgeTypesProperty` for edgeTypes property in GraphSchemaContent
  - Ensure consistency between node and edge type handling
  - _Requirements: 1.5, 3.2_

- [x] 4. Add import support at all levels
  - Ensure `import` can appear in `NodeTypeItem` and `EdgeTypeItem`
  - Ensure `import` can appear in `NodeTypesProperty` and `EdgeTypesProperty`
  - Validate import structure matches expected patterns
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Validate schema structure
  - Run JSON Schema validation on the schema itself
  - Verify no recursion is possible in the schema definitions
  - Check that all oneOf patterns are mutually exclusive
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 6. Correct snb-place-hierarchy.yaml example
  - Change from nested `subtypesOf.abstract.nodeTypes` structure
  - Use proper pattern with abstract/final wrappers at item level
  - Ensure Place is abstract and City/Country/Continent are final
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 7. Correct snb-organisation-hierarchy.yaml example
  - Apply same corrections as snb-place-hierarchy
  - Ensure Organisation is abstract with proper subtypes
  - Validate the corrected structure
  - _Requirements: 5.1, 5.2_

- [x] 8. Validate all 14 example files
  - Run validation on all example files with corrected schema
  - Identify any remaining validation failures
  - Document validation results
  - _Requirements: 5.3, 5.4_

- [x] 9. Fix any remaining example file issues
  - Correct any other examples that fail validation
  - Ensure all examples use proper type interpretation patterns
  - Verify no examples use recursive nesting
  - _Requirements: 5.3_

- [x] 10. Final validation and documentation
  - Confirm all 14 examples validate successfully
  - Update any documentation referencing type interpretation patterns
  - Create summary of changes made
  - _Requirements: 5.3, 5.4_
