# Implementation Plan

- [ ] 1. Implement catalog root IRI configuration system
  - Create CatalogRootConfiguration class with IRI validation and path resolution
  - Implement support for file: IRI scheme with current directory default ("file:.")
  - Add validation for supported IRI schemes
  - _Requirements: 6.20, 6.21, 6.22, 6.26, 6.27_

- [ ] 2. Update SessionConfiguration to include catalog_root
  - Add catalog_root field to SessionConfiguration class
  - Set default value to "file:." for current directory
  - Integrate with existing default_catalog_path configuration
  - _Requirements: 6.20, 6.22_

- [ ] 3. Implement CatalogRootResolver component
  - Create ICatalogRootResolver interface for path resolution operations
  - Implement concrete CatalogRootResolver class
  - Add methods for combining catalog_root IRI with relative paths
  - _Requirements: 6.23, 6.24, 6.25_

- [ ] 4. Update Catalog component to use catalog_root configuration
  - Modify Catalog class to accept CatalogRootConfiguration
  - Update path resolution logic to use catalog_root IRI
  - Ensure backward compatibility with existing path handling
  - _Requirements: 6.24, 6.25_

- [ ] 5. Add IRI scheme validation and extensibility
  - Implement IRI scheme validation in CatalogRootConfiguration
  - Create extensible framework for supporting additional IRI schemes
  - Add clear error messages for unsupported schemes
  - _Requirements: 6.26, 6.27_

- [ ] 6. Update test configuration to use file: IRI scheme
  - Modify test_functional.py to use catalog_root="file:." instead of default_catalog_path="/"
  - Ensure tests validate IRI-based path resolution
  - Add test cases for different IRI schemes and path combinations
  - _Requirements: 6.22, 6.23, 6.24_

- [ ] 7. Update nested record schema processor configuration
  - Replace single json_schema_processor field with nested_record_schema_processor_type and nested_record_schema_processor fields
  - Update SessionConfiguration class to use the new two-field approach
  - Modify all test files to use the new configuration format
  - _Requirements: 6.6, 6.7, 8.8, 8.9, 8.10_

- [ ] 8. Implement ILVT (Intermediate Language Value Types) system
  - Create ILVT type registry with all supported types from value_types.md specification
  - Implement type mapping functions between GQL, SQL Foundation, and JSON Schema
  - Add support for implementation-defined parameters (precision, scale, length, etc.)
  - Create validation functions for ILVT type constraints and ranges
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11_

- [ ] 9. Integrate ILVT with existing type system
  - Update PropertyType class to use ILVT type definitions
  - Modify ContentRecordType to validate against ILVT constraints
  - Add ILVT type compatibility checking for type hierarchies
  - Update builders to accept ILVT type specifications
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 5.1, 5.2, 5.3_

- [ ] 10. Add comprehensive testing for catalog root functionality
  - Create unit tests for CatalogRootConfiguration path resolution
  - Test IRI validation with valid and invalid schemes
  - Test path combination logic with various relative paths
  - _Requirements: 6.20, 6.21, 6.22, 6.23, 6.24, 6.25, 6.26, 6.27_

- [ ] 9. Research and evaluate EERM/FCA design tools
  - Research open-source tools that support Extended Entity-Relationship Modeling (EERM) with subtyping/subclassing
  - Evaluate tools that support Formal Concept Analysis (FCA) for lattice-based modeling
  - Identify tools that support attributes on both entities and relationships
  - Test import/export capabilities and file formats for selected tools
  - Document findings and recommend best tool for EERM-to-LEX transformation prototype
  - _Requirements: 52.14, 52.15, 52.16, 52.17_

- [ ] 10. Replace Kuzu mock with actual Kuzu embedded database
  - Remove kuzu_mock.py and replace with actual Kuzu Python library integration
  - Implement KuzuDatabaseClient class that uses real Kuzu embedded database
  - Update all catalog and schema storage operations to use actual Kuzu database files
  - Implement proper transaction handling and error management for Kuzu operations
  - Update tests to work with real Kuzu databases instead of mock objects
  - _Requirements: 11.1, 11.2, 11.8, 11.9, 53.1, 53.2, 53.3, 53.4, 53.5_

- [ ] 11. Implement pluggable graph database architecture
  - Create IGraphDatabaseClient interface for abstracting database operations
  - Implement KuzuEmbeddedClient as the default implementation
  - Design database client factory for selecting appropriate client based on configuration
  - Add support for Bolt driver connections to external graph databases
  - Implement connection string parsing and validation for different database types
  - _Requirements: 53.6, 53.7, 53.8, 53.9, 53.10, 53.11, 53.12, 53.20, 53.21, 53.22_

- [ ] 12. Create EERM-to-LEX transformation prototype
  - Implement basic EERM model parser for selected tool format
  - Create transformation engine that maps EERM entities to LEX node types
  - Implement relationship mapping from EERM relationships to LEX edge types
  - Add support for EERM generalization/specialization hierarchies to content type lattices
  - Generate LEX schema output with proper subtyping relationships
  - Create validation and testing framework for transformation accuracy
  - _Requirements: 52.8, 52.9, 52.10, 52.11, 52.19, 52.20, 52.21_

- [ ] 13. Refactor codebase to match grasch-main coding style
  - Convert all method names from snake_case to camelCase throughout src/grasch/
  - Add comprehensive type hints to all parameters, return values, and properties
  - Update class structure to match grasch-main patterns (nested result classes, property access)
  - Refactor test files to use camelCase method names and strong typing
  - Update import organization to match style guide
  - Ensure all magic methods follow grasch-main patterns
  - _Requirements: Python style consistency with reference implementation_