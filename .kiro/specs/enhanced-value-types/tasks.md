# Enhanced Value Types Implementation Tasks

## Implementation Plan

This document provides a detailed breakdown of implementation tasks for the ILVT-based Enhanced Value Types system, organized into discrete, manageable coding steps that build incrementally on the existing foundation and align with the Intermediate Language Value Types (ILVT) specification.

## Task Breakdown

### Epic 1: ILVT Type Registry and Core System

#### Task 1.1: ILVT Type Registry Implementation

**Objective**: Implement the complete ILVT type registry with all 32 standardized types and their validation methods.

**Implementation Details**:
- Create `ILVTType` enum in `src/grasch/value_types.py` with all ILVT types: boolean, int8-int256, uint8-uint256, decimal, numeric, float16-float256, decfloat32-decfloat128, string, char, bytes, binary, date, time, time_tz, datetime, datetime_tz, duration, record, array, multiset, json, vector, null
- Add type categorization methods (getCategory, getValueRange)
- Implement value range validation for integer and float types
- Create LanguageTypes enum for GQL, SQL_FOUNDATION, CYPHER, JSON, DATABASE_JSON
- Add comprehensive unit tests for all ILVT types

**Files to Create/Modify**:
- `src/grasch/value_types.py` (new)
- `tests/test_ilvt_types.py` (new)
- `src/grasch/__init__.py` (update exports)

**Acceptance Criteria**:
- All 32 ILVT types are defined with correct value ranges and categories
- Type validation works correctly for all supported types
- Extended precision types (int128, int256, uint128, uint256) validate correctly
- Performance <0.1ms per type validation call

**Requirements**: _R1.1, R1.2, R1.3, R1.4, R1.5_

---

#### Task 1.2: Language Type Mapping System

**Objective**: Implement the complete 5-way type mapping system between ILVT, GQL, SQL Foundation, Cypher, and JSON Schema.

**Implementation Details**:
- Create `TypeMapping` dataclass with ilvtType, gqlType, sqlType, cypherType, jsonSchemaType fields
- Implement `LanguageTypeMapper` class with complete mapping table initialization
- Add bidirectional mapping methods (getEquivalentTypes, getILVTType, getLanguageType)
- Implement mapping for all ILVT types according to the specification tables
- Handle undefined mappings (e.g., GQL UINT8 has no SQL equivalent)
- Create comprehensive mapping tests

**Files to Create/Modify**:
- `src/grasch/language_mapper.py` (new)
- `tests/test_language_mapping.py` (new)

**Acceptance Criteria**:
- Complete 5-way mapping table implemented for all ILVT types
- Bidirectional mappings work correctly between all supported languages
- Undefined mappings are handled appropriately (return None or "undefined")
- Cross-language type conversion preserves semantic meaning

**Requirements**: _R2.1, R2.2, R2.3, R2.4, R2.5_

---

#### Task 1.3: JSON Schema Integration with Triple Naming

**Objective**: Implement JSON Schema generation using the triple naming convention (data.xxx, gql.xxx, sql.xxx).

**Implementation Details**:
- Extend `LanguageTypeMapper` with `generateJSONSchema` method
- Implement triple naming convention for all ILVT types
- Add type-specific JSON Schema constraints (integer ranges, string lengths, precision/scale)
- Handle parameterized types (decimal precision/scale, vector dimension, string maxLength)
- Set undefined language mappings to "undefined" in JSON Schema
- Create comprehensive JSON Schema generation tests

**Files to Create/Modify**:
- `src/grasch/language_mapper.py` (extend)
- `src/grasch/json_schema_generator.py` (new)
- `tests/test_json_schema_generation.py` (new)

**Acceptance Criteria**:
- JSON Schema uses triple naming convention consistently
- Type constraints are properly represented (min/max values, lengths, formats)
- Parameterized types include parameter specifications
- Undefined mappings are clearly marked as "undefined"
- Generated schemas validate correctly against JSON Schema specification

**Requirements**: _R3.1, R3.2, R3.3, R3.4, R3.5_

---

### Epic 2: Enhanced PropertyType with ILVT Integration

#### Task 2.1: ILVT-Based PropertyType Implementation

**Objective**: Replace the existing ValueType system with ILVT-based EnhancedPropertyType.

**Implementation Details**:
- Create `EnhancedPropertyType` dataclass with ilvtType field (replacing valueType)
- Add parameters field for type constraints (precision, scale, length, dimension)
- Implement getLanguageType and generateJSONSchema methods
- Add support for structured types (array elementType, record fields)
- Maintain backward compatibility with existing PropertyType
- Create comprehensive property type tests

**Files to Create/Modify**:
- `src/grasch/types.py` (extend with EnhancedPropertyType)
- `tests/test_enhanced_property_type.py` (new)

**Acceptance Criteria**:
- EnhancedPropertyType supports all ILVT types with proper parameter handling
- Language type conversion works correctly for all supported languages
- JSON Schema generation produces valid schemas with triple naming
- Backward compatibility is maintained with existing PropertyType usage

**Requirements**: _R1.1, R1.2, R3.1, R3.2, R9.1, R9.2, R10.1, R10.2_

---

#### Task 2.2: ILVT-Enhanced PropertyTypeBuilder

**Objective**: Extend PropertyTypeBuilder with ILVT-specific methods and parameterized type support.

**Implementation Details**:
- Add `withILVTType` method and type-specific builder methods (withInt8Type, withFloat32Type, etc.)
- Implement parameterized type builders (withDecimalType, withVectorType, withStringType with maxLength)
- Add structured type builders (withArrayType, withRecordType)
- Implement backward compatibility withValueType method for legacy string types
- Add constraint integration methods
- Create comprehensive builder tests

**Files to Create/Modify**:
- `src/grasch/types.py` (extend PropertyTypeBuilder)
- `tests/test_ilvt_builder.py` (new)

**Acceptance Criteria**:
- Builder supports all ILVT types with fluent method chaining
- Parameterized types can be configured with appropriate parameters
- Structured types support nested type definitions
- Legacy string type conversion works correctly
- Builder validation catches configuration errors at build time

**Requirements**: _R1.1, R1.2, R9.1, R9.2, R9.3, R10.1, R10.2_

---

### Epic 3: Language Level Adaptation System

#### Task 3.1: Language Level Adapter Implementation

**Objective**: Implement language level adaptation for GQL and LEX (Cypher-compatible) levels.

**Implementation Details**:
- Create `LanguageLevel` enum with GQL and LEX values
- Implement `LanguageLevelAdapter` class with adaptType method
- Add type adaptation rules (all integers -> int64 for LEX, all floats -> float64 for LEX)
- Implement supportsHeterogeneousCollections method
- Add language level consideration in type validation
- Create comprehensive adaptation tests

**Files to Create/Modify**:
- `src/grasch/language_adapter.py` (new)
- `tests/test_language_adaptation.py` (new)

**Acceptance Criteria**:
- GQL level supports full ILVT type system with precise mappings
- LEX level maps to Cypher-compatible subset correctly
- Type adaptation preserves semantic meaning while ensuring compatibility
- Heterogeneous collection support varies correctly by language level

**Requirements**: _R6.1, R6.2, R6.3_

---

#### Task 3.2: Enhanced Type Coercion with Language Levels

**Objective**: Integrate language level adaptation with the type coercion system.

**Implementation Details**:
- Update `TypeCoercion` class to use `LanguageLevelAdapter`
- Implement type-specific coercion methods (_coerceToBoolean, _coerceToInteger, etc.)
- Add language level consideration in coercion decisions
- Implement safe coercion rules between ILVT types
- Add coercion result reporting with warnings for potentially lossy conversions
- Create comprehensive coercion tests

**Files to Create/Modify**:
- `src/grasch/coercion.py` (extend existing or new)
- `tests/test_ilvt_coercion.py` (new)

**Acceptance Criteria**:
- Type coercion respects language level constraints
- Safe coercions work correctly between compatible ILVT types
- Lossy coercions are reported with appropriate warnings
- Coercion failures provide clear error messages with suggestions

**Requirements**: _R6.1, R6.2, R6.3, R6.4, R6.5_

---

### Epic 4: ILVT-Aware Validation Engine

#### Task 4.1: ILVT Property Validation

**Objective**: Update the validation engine to support all ILVT types with parameter validation.

**Implementation Details**:
- Update `PropertyValidator` to handle all ILVT types
- Implement parameter validation for parameterized types (precision, scale, length, dimension)
- Add value range validation for integer and float types
- Integrate with `LanguageTypeMapper` for cross-language validation
- Add structured type validation (array elements, record fields)
- Create comprehensive ILVT validation tests

**Files to Create/Modify**:
- `src/grasch/validation.py` (extend existing)
- `tests/test_ilvt_validation.py` (new)

**Acceptance Criteria**:
- All ILVT types validate correctly with appropriate error messages
- Parameter validation enforces type-specific constraints
- Value range validation works for all numeric types
- Structured type validation handles nested validation correctly

**Requirements**: _R5.1, R5.2, R7.1, R8.1_

---

#### Task 4.2: Graph Validation with ILVT Support

**Objective**: Extend graph validation to work with ILVT-based property types.

**Implementation Details**:
- Update `GraphValidator` to use ILVT-based property validation
- Implement streaming validation for large datasets with ILVT types
- Add parallel validation support for independent graph elements
- Integrate language level adaptation in graph validation
- Add comprehensive graph validation tests with ILVT types

**Files to Create/Modify**:
- `src/grasch/validation.py` (extend GraphValidator)
- `tests/test_ilvt_graph_validation.py` (new)

**Acceptance Criteria**:
- Complete graphs validate correctly against ILVT-based schemas
- Streaming validation supports large datasets without memory issues
- Parallel validation improves performance for large graphs
- Language level adaptation is applied consistently across graph validation

**Requirements**: _R5.1, R5.3, R5.4, R7.2, R7.4_

---

### Epic 5: Property Constraints with ILVT Integration

#### Task 5.1: ILVT-Aware Constraint System

**Objective**: Integrate the property constraint system with ILVT types and validation.

**Implementation Details**:
- Update constraint classes to work with ILVT types
- Add ILVT-specific constraint validation (e.g., range constraints for numeric types)
- Integrate constraints with EnhancedPropertyType
- Add constraint builder methods to PropertyTypeBuilder
- Create comprehensive constraint tests with ILVT types

**Files to Create/Modify**:
- `src/grasch/constraints.py` (extend existing)
- `tests/test_ilvt_constraints.py` (new)

**Acceptance Criteria**:
- All constraint types work correctly with ILVT types
- ILVT-specific constraints (range, precision) are properly validated
- Constraint combinations work correctly with enhanced property types
- Constraint violations provide detailed error messages with ILVT context

**Requirements**: _R4.1, R4.2, R4.3, R4.4, R4.5_

---

### Epic 6: Error Handling and Reporting

#### Task 6.1: ILVT-Enhanced Error Reporting

**Objective**: Update error handling to provide detailed information about ILVT types and cross-language mappings.

**Implementation Details**:
- Update `ValidationError` hierarchy to include ILVT type information
- Add language-specific error messages and suggestions
- Implement hierarchical error reporting for structured ILVT types
- Add error context with parameter information for parameterized types
- Create comprehensive error reporting tests

**Files to Create/Modify**:
- `src/grasch/validation_results.py` (extend existing or new)
- `tests/test_ilvt_error_reporting.py` (new)

**Acceptance Criteria**:
- Error messages include ILVT type information and expected formats
- Cross-language mapping errors provide clear guidance
- Hierarchical errors show full path for nested validation failures
- Parameter validation errors include specific parameter information

**Requirements**: _R8.1, R8.2, R8.3, R8.4, R8.5_

---

### Epic 7: Performance Optimization

#### Task 7.1: ILVT Validation Performance Optimization

**Objective**: Optimize validation performance for ILVT types with caching and parallel processing.

**Implementation Details**:
- Implement validation result caching for ILVT types
- Add lazy evaluation for expensive ILVT validation operations
- Create parallel validation framework for independent elements
- Add performance benchmarking for ILVT validation
- Optimize memory usage for large-scale ILVT validation

**Files to Create/Modify**:
- `src/grasch/validation_cache.py` (new)
- `src/grasch/performance_utils.py` (new)
- `tests/test_ilvt_performance.py` (new)

**Acceptance Criteria**:
- ILVT validation meets <1ms per property performance target
- Caching improves performance for repeated validations
- Parallel validation scales with available CPU cores
- Memory usage remains constant for streaming validation

**Requirements**: _R7.1, R7.2, R7.3, R7.4, R7.5_

---

### Epic 8: Backward Compatibility and Migration

#### Task 8.1: Legacy PropertyType Compatibility

**Objective**: Ensure complete backward compatibility while providing migration to ILVT types.

**Implementation Details**:
- Maintain existing PropertyType constructor signatures
- Add automatic migration from string datatypes to ILVT types
- Implement deprecation warnings with clear migration guidance
- Create compatibility layer for legacy method calls
- Add comprehensive backward compatibility tests

**Files to Create/Modify**:
- `src/grasch/types.py` (extend with compatibility layer)
- `src/grasch/legacy_support.py` (new)
- `tests/test_ilvt_backward_compatibility.py` (new)

**Acceptance Criteria**:
- All existing code continues to work without modification
- String datatypes are automatically converted to appropriate ILVT types
- Deprecation warnings provide clear migration paths
- Legacy schemas migrate correctly to ILVT-based schemas

**Requirements**: _R10.1, R10.2, R10.3, R10.4_

---

#### Task 8.2: ILVT Schema Migration Tools

**Objective**: Create tools for migrating existing schemas to use ILVT types.

**Implementation Details**:
- Create schema migration utilities for ILVT conversion
- Add validation tools for migration correctness
- Implement rollback capabilities for failed migrations
- Create migration reporting with ILVT type information
- Add comprehensive migration tests

**Files to Create/Modify**:
- `src/grasch/ilvt_migration.py` (new)
- `tests/test_ilvt_migration.py` (new)

**Acceptance Criteria**:
- Schema migration correctly converts legacy types to ILVT types
- Migration validation ensures semantic equivalence
- Rollback capabilities allow safe recovery from failed migrations
- Migration reports show detailed ILVT type conversions

**Requirements**: _R10.1, R10.2, R10.3, R10.4, R10.5_

---

### Epic 9: Integration and Final Testing

#### Task 9.1: ILVT Integration with Existing Type System

**Objective**: Integrate ILVT-based enhanced types with existing grasch type system.

**Implementation Details**:
- Update NodeType and EdgeType to use EnhancedPropertyType
- Ensure compatibility with existing catalog and core modules
- Test integration with builder patterns and validation workflows
- Add ILVT support to GraphType and schema definitions
- Create comprehensive integration tests

**Files to Create/Modify**:
- `src/grasch/types.py` (update NodeType, EdgeType)
- `src/grasch/catalog.py` (update if needed)
- `tests/test_ilvt_integration.py` (new)

**Acceptance Criteria**:
- All existing type classes work seamlessly with ILVT-based properties
- Schema definitions support full ILVT type system
- Builder patterns integrate correctly with ILVT types
- Performance impact on existing workflows is minimal

**Requirements**: _R9.1, R9.2, R9.3, R9.4, R10.1, R10.2_

---

#### Task 9.2: Comprehensive ILVT System Testing

**Objective**: Create comprehensive end-to-end tests for the complete ILVT system.

**Implementation Details**:
- Test complete workflows from ILVT type definition to validation
- Verify cross-language type mapping in realistic scenarios
- Test performance with realistic graph data sizes using ILVT types
- Add stress tests for large-scale ILVT validation
- Create comprehensive documentation and examples

**Files to Create/Modify**:
- `tests/test_ilvt_end_to_end.py` (new)
- `tests/test_ilvt_performance_stress.py` (new)
- `examples/ilvt_usage_examples.py` (new)

**Acceptance Criteria**:
- End-to-end workflows demonstrate complete ILVT functionality
- Cross-language mappings work correctly in realistic scenarios
- Performance meets targets with realistic data sizes
- Documentation provides clear guidance for ILVT usage

**Requirements**: _All requirements_

---

## Implementation Schedule

### Sprint 1 (Weeks 1-2): ILVT Foundation
- **Week 1**: Task 1.1 (ILVT Type Registry)
- **Week 2**: Tasks 1.2, 1.3 (Language mapping and JSON Schema)

### Sprint 2 (Weeks 3-4): Enhanced PropertyType
- **Week 3**: Task 2.1 (ILVT-based PropertyType)
- **Week 4**: Task 2.2 (ILVT Builder patterns)

### Sprint 3 (Weeks 5-6): Language Adaptation and Validation
- **Week 5**: Tasks 3.1, 3.2 (Language level adaptation and coercion)
- **Week 6**: Tasks 4.1, 4.2 (ILVT validation engine)

### Sprint 4 (Weeks 7-8): Constraints and Error Handling
- **Week 7**: Tasks 5.1, 6.1 (ILVT constraints and error reporting)
- **Week 8**: Task 7.1 (Performance optimization)

### Sprint 5 (Weeks 9-10): Compatibility and Integration
- **Week 9**: Tasks 8.1, 8.2 (Backward compatibility and migration)
- **Week 10**: Tasks 9.1, 9.2 (Integration and comprehensive testing)

## Success Metrics

### ILVT Compliance
- **Type Coverage**: All 32 ILVT types supported with correct validation
- **Language Mapping**: Complete 5-way mapping between ILVT, GQL, SQL, Cypher, JSON Schema
- **JSON Schema**: Triple naming convention implemented correctly
- **Cross-Language**: Seamless type conversion between supported languages

### Performance Targets
- **Validation Speed**: <1ms per property validation for all ILVT types
- **Memory Usage**: Constant memory for streaming validation regardless of data size
- **Scalability**: Linear scaling with data size, parallel processing support
- **Caching**: Effective caching reduces repeated validation overhead

### Compatibility Requirements
- **Backward Compatibility**: Zero breaking changes to existing public API
- **Migration**: Automatic and safe migration from legacy string types to ILVT
- **Integration**: Seamless integration with existing grasch type system
- **Documentation**: Complete API documentation for all ILVT features

## Risk Mitigation

### Technical Risks
- **ILVT Complexity**: Mitigate through comprehensive testing and clear documentation
- **Performance Impact**: Mitigate through caching, optimization, and benchmarking
- **Cross-Language Mapping**: Mitigate through specification compliance and validation

### Implementation Risks
- **Scope Management**: Mitigate through clear task boundaries and sprint planning
- **Integration Issues**: Mitigate through continuous integration and early testing
- **Backward Compatibility**: Mitigate through extensive compatibility testing and gradual migration