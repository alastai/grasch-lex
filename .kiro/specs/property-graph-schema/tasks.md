# Implementation Plan

- [ ] 1. Implement catalog root IRI configuration system
  - Create CatalogRootConfiguration class with IRI validation and path resolution
  - Implement support for file: IRI scheme with current directory default ("file:.")
  - Add validation for supported IRI schemes
  - _Requirements: 5.20, 5.21, 5.22, 5.26, 5.27_

- [ ] 2. Update SessionConfiguration to include catalog_root
  - Add catalog_root field to SessionConfiguration class
  - Set default value to "file:." for current directory
  - Integrate with existing default_catalog_path configuration
  - _Requirements: 5.20, 5.22_

- [ ] 3. Implement CatalogRootResolver component
  - Create ICatalogRootResolver interface for path resolution operations
  - Implement concrete CatalogRootResolver class
  - Add methods for combining catalog_root IRI with relative paths
  - _Requirements: 5.23, 5.24, 5.25_

- [ ] 4. Update Catalog component to use catalog_root configuration
  - Modify Catalog class to accept CatalogRootConfiguration
  - Update path resolution logic to use catalog_root IRI
  - Ensure backward compatibility with existing path handling
  - _Requirements: 5.24, 5.25_

- [ ] 5. Add IRI scheme validation and extensibility
  - Implement IRI scheme validation in CatalogRootConfiguration
  - Create extensible framework for supporting additional IRI schemes
  - Add clear error messages for unsupported schemes
  - _Requirements: 5.26, 5.27_

- [ ] 6. Update test configuration to use file: IRI scheme
  - Modify test_functional.py to use catalog_root="file:." instead of default_catalog_path="/"
  - Ensure tests validate IRI-based path resolution
  - Add test cases for different IRI schemes and path combinations
  - _Requirements: 5.22, 5.23, 5.24_

- [ ] 7. Update nested record schema processor configuration
  - Replace single json_schema_processor field with nested_record_schema_processor_type and nested_record_schema_processor fields
  - Update SessionConfiguration class to use the new two-field approach
  - Modify all test files to use the new configuration format
  - _Requirements: 5.6, 5.7, 8.8, 8.9, 8.10_

- [ ] 8. Add comprehensive testing for catalog root functionality
  - Create unit tests for CatalogRootConfiguration path resolution
  - Test IRI validation with valid and invalid schemes
  - Test path combination logic with various relative paths
  - _Requirements: 5.20, 5.21, 5.22, 5.23, 5.24, 5.25, 5.26, 5.27_