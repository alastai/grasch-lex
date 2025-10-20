"""
Comprehensive tests for the ValueType system.

Tests cover all primitive types with valid/invalid inputs, edge cases,
error messages, and performance requirements.
"""

import pytest
import math
import time
from typing import Any, List

from grasch.value_types import (
    ValueType, ValidationResult, ValidationError, ILVTType, LanguageTypeMapper,
    validateValue, isValidValue, getTypeForValue, convertLegacyDatatype, 
    getLanguageTypeName, translateType, isTypeCompatible, inferPreciseType
)
from grasch.core import LanguageLevel, LanguageTypes


class TestValueTypeEnum:
    """Test ValueType enumeration basic functionality"""
    
    def test_valueTypeEnumValues(self):
        """Test that all expected value types are defined"""
        expected_types = {
            'STRING', 'INTEGER', 'FLOAT', 'BOOLEAN',
            'DATE', 'TIME', 'DATETIME', 'DURATION',
            'JSON', 'ARRAY', 'MAP'
        }
        actual_types = {vt.value for vt in ValueType}
        assert actual_types == expected_types
    
    def test_fromStringValidTypes(self):
        """Test creating ValueType from valid string representations"""
        assert ValueType.fromString('STRING') == ValueType.STRING
        assert ValueType.fromString('string') == ValueType.STRING
        assert ValueType.fromString('Integer') == ValueType.INTEGER
        assert ValueType.fromString('BOOLEAN') == ValueType.BOOLEAN
    
    def test_fromStringInvalidType(self):
        """Test creating ValueType from invalid string raises error"""
        with pytest.raises(ValidationError) as exc_info:
            ValueType.fromString('INVALID_TYPE')
        
        assert "Unknown value type: INVALID_TYPE" in str(exc_info.value)
        assert "Valid types are:" in str(exc_info.value)
    
    def test_getDescription(self):
        """Test that all types have meaningful descriptions"""
        for value_type in ValueType:
            description = value_type.getDescription()
            assert isinstance(description, str)
            assert len(description) > 0
            assert value_type.value.lower() in description.lower() or "value" in description.lower()


class TestStringValidation:
    """Test STRING type validation"""
    
    def test_validStrings(self):
        """Test validation of valid string values"""
        valid_strings = [
            "",  # Empty string
            "hello",  # Simple string
            "Hello, World!",  # String with punctuation
            "123",  # Numeric string
            "true",  # Boolean string
            "multi\nline\nstring",  # Multi-line string
            "unicode: 🚀 αβγ",  # Unicode characters
            " \t\n ",  # Whitespace string
        ]
        
        for test_string in valid_strings:
            # Test with both language type systems
            for lang_type in [LanguageTypes.GQL, LanguageTypes.CYPHER]:
                result = ValueType.STRING.validate(test_string, lang_type)
                assert result.isValid, f"String '{test_string}' should be valid for {lang_type.value}"
                assert len(result.errors) == 0
    
    def test_invalidStrings(self):
        """Test validation of invalid string values"""
        invalid_values = [
            123,  # Integer
            45.67,  # Float
            True,  # Boolean
            [],  # List
            {},  # Dict
        ]
        
        for invalid_value in invalid_values:
            result = ValueType.STRING.validate(invalid_value)
            assert not result.isValid, f"Value {invalid_value} should be invalid for STRING"
            assert len(result.errors) > 0
            assert "Expected STRING" in result.errors[0]
        
        # Test None separately since it has a different error message
        result = ValueType.STRING.validate(None)
        assert not result.isValid
        assert "cannot be null" in result.errors[0]
    
    def test_stringErrorMessages(self):
        """Test that string validation provides helpful error messages"""
        result = ValueType.STRING.validate(123)
        assert "Expected STRING, got int" in result.errors[0]
        assert "explicit string conversion" in result.errors[0]
        
        result = ValueType.STRING.validate(True)
        assert "Expected STRING, got bool" in result.errors[0]


class TestIntegerValidation:
    """Test INTEGER type validation"""
    
    def test_validIntegers(self):
        """Test validation of valid integer values"""
        valid_integers = [
            0,  # Zero
            1,  # Positive integer
            -1,  # Negative integer
            9223372036854775807,  # Max 64-bit signed integer
            -9223372036854775808,  # Min 64-bit signed integer
            42,  # Random positive
            -42,  # Random negative
        ]
        
        for test_int in valid_integers:
            result = ValueType.INTEGER.validate(test_int)
            assert result.isValid, f"Integer {test_int} should be valid"
            assert len(result.errors) == 0
    
    def test_invalidIntegers(self):
        """Test validation of invalid integer values"""
        invalid_values = [
            "123",  # String
            45.67,  # Float (non-integer)
            45.0,   # Float that is integer value
            True,   # Boolean (subclass of int in Python)
            False,  # Boolean
            [],     # List
            None,   # None
        ]
        
        for invalid_value in invalid_values:
            result = ValueType.INTEGER.validate(invalid_value)
            assert not result.isValid, f"Value {invalid_value} should be invalid for INTEGER"
            assert len(result.errors) > 0
    
    def test_integerOverflow(self):
        """Test integer overflow detection"""
        # Test values outside 64-bit signed integer range
        overflow_values = [
            9223372036854775808,   # Max + 1
            -9223372036854775809,  # Min - 1
        ]
        
        for overflow_value in overflow_values:
            result = ValueType.INTEGER.validate(overflow_value)
            assert not result.isValid
            assert "outside the valid range" in result.errors[0]
    
    def test_booleanRejection(self):
        """Test that booleans are rejected for integers"""
        result = ValueType.INTEGER.validate(True)
        assert not result.isValid
        assert "Expected INTEGER" in result.errors[0]
        
        result = ValueType.INTEGER.validate(False)
        assert not result.isValid
    
    def test_floatRejection(self):
        """Test that floats are rejected with helpful messages"""
        # Integer-valued float
        result = ValueType.INTEGER.validate(42.0)
        assert not result.isValid
        assert "Expected INTEGER, got FLOAT" in result.errors[0]
        assert "explicit integer conversion" in result.errors[0]
        
        # Non-integer float
        result = ValueType.INTEGER.validate(42.5)
        assert not result.isValid
        assert "not a whole number" in result.errors[0]


class TestFloatValidation:
    """Test FLOAT type validation"""
    
    def test_validFloats(self):
        """Test validation of valid float values"""
        valid_floats = [
            0.0,  # Zero
            1.0,  # Positive float
            -1.0,  # Negative float
            3.14159,  # Pi
            -2.71828,  # Negative e
            1e10,  # Scientific notation
            -1e-10,  # Negative scientific notation
            float('inf'),  # Positive infinity
            float('-inf'),  # Negative infinity
            float('nan'),  # Not a number
        ]
        
        for test_float in valid_floats:
            result = ValueType.FLOAT.validate(test_float)
            assert result.isValid, f"Float {test_float} should be valid"
            assert len(result.errors) == 0
    
    def test_invalidFloats(self):
        """Test validation of invalid float values"""
        invalid_values = [
            "3.14",  # String
            42,      # Integer
            True,    # Boolean
            [],      # List
            None,    # None
        ]
        
        for invalid_value in invalid_values:
            result = ValueType.FLOAT.validate(invalid_value)
            assert not result.isValid, f"Value {invalid_value} should be invalid for FLOAT"
            assert len(result.errors) > 0
    
    def test_integerRejection(self):
        """Test that integers are rejected with helpful messages"""
        result = ValueType.FLOAT.validate(42)
        assert not result.isValid
        assert "Expected FLOAT, got INTEGER" in result.errors[0]
        assert "explicit float conversion" in result.errors[0]
    
    def test_specialFloatValues(self):
        """Test that special float values (NaN, Infinity) are handled correctly"""
        special_values = [float('inf'), float('-inf'), float('nan')]
        
        for special_value in special_values:
            result = ValueType.FLOAT.validate(special_value)
            assert result.isValid, f"Special float {special_value} should be valid"


class TestBooleanValidation:
    """Test BOOLEAN type validation"""
    
    def test_validBooleans(self):
        """Test validation of valid boolean values"""
        valid_booleans = [True, False]
        
        for test_bool in valid_booleans:
            result = ValueType.BOOLEAN.validate(test_bool)
            assert result.isValid, f"Boolean {test_bool} should be valid"
            assert len(result.errors) == 0
    
    def test_invalidBooleans(self):
        """Test validation of invalid boolean values"""
        invalid_values = [
            "true",  # String
            "false", # String
            1,       # Integer
            0,       # Integer
            1.0,     # Float
            [],      # List
            None,    # None
        ]
        
        for invalid_value in invalid_values:
            result = ValueType.BOOLEAN.validate(invalid_value)
            assert not result.isValid, f"Value {invalid_value} should be invalid for BOOLEAN"
            assert len(result.errors) > 0
    
    def test_booleanErrorMessages(self):
        """Test that boolean validation provides helpful error messages"""
        result = ValueType.BOOLEAN.validate(1)
        assert "Expected BOOLEAN, got int" in result.errors[0]
        assert "explicit boolean conversion" in result.errors[0]
        
        result = ValueType.BOOLEAN.validate("true")
        assert "Expected BOOLEAN, got str" in result.errors[0]


class TestNullValidation:
    """Test null value handling across all types"""
    
    def test_nullRejection(self):
        """Test that null values are rejected for all primitive types"""
        primitive_types = [ValueType.STRING, ValueType.INTEGER, ValueType.FLOAT, ValueType.BOOLEAN]
        
        for value_type in primitive_types:
            result = value_type.validate(None)
            assert not result.isValid, f"None should be invalid for {value_type.value}"
            assert "cannot be null" in result.errors[0]


class TestTypeCompatibility:
    """Test type compatibility checking"""
    
    def test_selfCompatibility(self):
        """Test that all types are compatible with themselves"""
        for value_type in ValueType:
            assert value_type.isCompatibleWith(value_type)
    
    def test_numericCompatibility(self):
        """Test numeric type compatibility rules"""
        # INTEGER should be compatible with FLOAT (widening conversion)
        assert ValueType.INTEGER.isCompatibleWith(ValueType.FLOAT)
        
        # FLOAT should not be compatible with INTEGER (narrowing conversion)
        assert not ValueType.FLOAT.isCompatibleWith(ValueType.INTEGER)
    
    def test_stringIncompatibility(self):
        """Test that strings are not automatically compatible with other types"""
        other_types = [ValueType.INTEGER, ValueType.FLOAT, ValueType.BOOLEAN]
        
        for other_type in other_types:
            assert not ValueType.STRING.isCompatibleWith(other_type)
            assert not other_type.isCompatibleWith(ValueType.STRING)
    
    def test_booleanIncompatibility(self):
        """Test that booleans are not compatible with other types"""
        other_types = [ValueType.STRING, ValueType.INTEGER, ValueType.FLOAT]
        
        for other_type in other_types:
            assert not ValueType.BOOLEAN.isCompatibleWith(other_type)
            assert not other_type.isCompatibleWith(ValueType.BOOLEAN)


class TestUtilityFunctions:
    """Test utility functions for type validation"""
    
    def test_validateValue(self):
        """Test validateValue convenience function"""
        result = validateValue("hello", ValueType.STRING, LanguageTypes.GQL)
        assert result.isValid
        
        result = validateValue(123, ValueType.STRING, LanguageTypes.GQL)
        assert not result.isValid
        
        # Test with Cypher type system
        result = validateValue("hello", ValueType.STRING, LanguageTypes.CYPHER)
        assert result.isValid
    
    def test_isValidValue(self):
        """Test isValidValue convenience function"""
        assert isValidValue("hello", ValueType.STRING, LanguageTypes.GQL)
        assert isValidValue(123, ValueType.INTEGER, LanguageTypes.GQL)
        assert isValidValue(3.14, ValueType.FLOAT, LanguageTypes.GQL)
        assert isValidValue(True, ValueType.BOOLEAN, LanguageTypes.GQL)
        
        assert not isValidValue(123, ValueType.STRING, LanguageTypes.GQL)
        assert not isValidValue("hello", ValueType.INTEGER, LanguageTypes.GQL)
        
        # Test with Cypher type system
        assert isValidValue("hello", ValueType.STRING, LanguageTypes.CYPHER)
        assert isValidValue(123, ValueType.INTEGER, LanguageTypes.CYPHER)
    
    def test_getTypeForValue(self):
        """Test type inference for values"""
        assert getTypeForValue("hello", LanguageTypes.GQL) == ValueType.STRING
        assert getTypeForValue(123, LanguageTypes.GQL) == ValueType.INTEGER
        assert getTypeForValue(3.14, LanguageTypes.GQL) == ValueType.FLOAT
        assert getTypeForValue(True, LanguageTypes.GQL) == ValueType.BOOLEAN
        assert getTypeForValue(False, LanguageTypes.GQL) == ValueType.BOOLEAN
        assert getTypeForValue([1, 2, 3], LanguageTypes.GQL) == ValueType.ARRAY
        assert getTypeForValue({"key": "value"}, LanguageTypes.GQL) == ValueType.MAP
        assert getTypeForValue(None, LanguageTypes.GQL) is None
        
        # Test with Cypher type system
        assert getTypeForValue("hello", LanguageTypes.CYPHER) == ValueType.STRING
        assert getTypeForValue(123, LanguageTypes.CYPHER) == ValueType.INTEGER


class TestValidationResult:
    """Test ValidationResult class functionality"""
    
    def test_successResult(self):
        """Test creating successful validation results"""
        result = ValidationResult.success()
        assert result.isValid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
        
        result = ValidationResult.success(warnings=["test warning"])
        assert result.isValid
        assert len(result.warnings) == 1
        assert result.warnings[0] == "test warning"
    
    def test_failureResult(self):
        """Test creating failed validation results"""
        result = ValidationResult.failure("test error")
        assert not result.isValid
        assert len(result.errors) == 1
        assert result.errors[0] == "test error"
    
    def test_addError(self):
        """Test adding errors to validation results"""
        result = ValidationResult.success()
        result.addError("new error")
        
        assert not result.isValid
        assert len(result.errors) == 1
        assert result.errors[0] == "new error"
    
    def test_addWarning(self):
        """Test adding warnings to validation results"""
        result = ValidationResult.success()
        result.addWarning("new warning")
        
        assert result.isValid
        assert len(result.warnings) == 1
        assert result.warnings[0] == "new warning"


class TestPerformance:
    """Test performance requirements"""
    
    def test_validationPerformance(self):
        """Test that validation meets performance requirements (<0.1ms per call)"""
        test_values = [
            ("hello", ValueType.STRING),
            (123, ValueType.INTEGER),
            (3.14, ValueType.FLOAT),
            (True, ValueType.BOOLEAN),
        ]
        
        # Warm up
        for value, value_type in test_values:
            value_type.validate(value)
        
        # Measure performance
        iterations = 1000
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            for value, value_type in test_values:
                value_type.validate(value)
        
        end_time = time.perf_counter()
        avg_time_ms = ((end_time - start_time) / (iterations * len(test_values))) * 1000
        
        # Should be less than 0.1ms per validation
        assert avg_time_ms < 0.1, f"Average validation time {avg_time_ms:.3f}ms exceeds 0.1ms target"


class TestILVTIntegration:
    """Test ILVT integration and language level functionality"""
    
    def test_ilvtTypeMapping(self):
        """Test that ValueTypes map correctly to ILVT types"""
        mappings = {
            ValueType.STRING: ILVTType.STRING,
            ValueType.INTEGER: ILVTType.INT64,
            ValueType.FLOAT: ILVTType.FLOAT64,
            ValueType.BOOLEAN: ILVTType.BOOLEAN,
        }
        
        for value_type, expected_ilvt in mappings.items():
            ilvt_type = value_type.getILVTType(LanguageTypes.GQL)
            assert ilvt_type == expected_ilvt, f"{value_type} should map to {expected_ilvt}"
    
    def test_languageLevelMapping(self):
        """Test language-specific type name mapping"""
        # Test GQL mappings (lowercase)
        assert LanguageTypeMapper.getILVTFromLanguageType("integer", LanguageTypes.GQL) == ILVTType.INT32
        assert LanguageTypeMapper.getILVTFromLanguageType("bigint", LanguageTypes.GQL) == ILVTType.INT64
        assert LanguageTypeMapper.getILVTFromLanguageType("string", LanguageTypes.GQL) == ILVTType.STRING
        
        # Test Cypher type system (uppercase)
        assert LanguageTypeMapper.getILVTFromLanguageType("INTEGER", LanguageTypes.CYPHER) == ILVTType.INT64
        assert LanguageTypeMapper.getILVTFromLanguageType("FLOAT", LanguageTypes.CYPHER) == ILVTType.FLOAT64
        
        # Test JSON type system (lowercase)
        assert LanguageTypeMapper.getILVTFromLanguageType("number", LanguageTypes.JSON) == ILVTType.INT8  # First integer type in mapping
        assert LanguageTypeMapper.getILVTFromLanguageType("string", LanguageTypes.JSON) == ILVTType.STRING
        assert LanguageTypeMapper.getILVTFromLanguageType("boolean", LanguageTypes.JSON) == ILVTType.BOOLEAN
        assert LanguageTypeMapper.getILVTFromLanguageType("json", LanguageTypes.JSON) is None  # JSON type not available in basic JSON
        # Test DATABASE_JSON type system (lowercase, 1:1 with GQL)
        assert LanguageTypeMapper.getILVTFromLanguageType("bigint", LanguageTypes.DATABASE_JSON) == ILVTType.INT64
        assert LanguageTypeMapper.getILVTFromLanguageType("json", LanguageTypes.DATABASE_JSON) == ILVTType.JSON  # JSON type available in DATABASE_JSON
        assert LanguageTypeMapper.getILVTFromLanguageType("json", LanguageTypes.GQL) is None  # Not available in GQL
    
    def test_cypherCompatibility(self):
        """Test Cypher compatibility mapping"""
        # Test that various integer types map to INT64 for Cypher compatibility
        cypher_int_types = [ILVTType.INT8, ILVTType.INT16, ILVTType.INT32, ILVTType.UINT32]
        for int_type in cypher_int_types:
            cypher_type = LanguageTypeMapper.getCypherCompatibleILVT(int_type)
            assert cypher_type == ILVTType.INT64, f"{int_type} should map to INT64 for Cypher"
        
        # Test that various float types map to FLOAT64 for Cypher compatibility
        cypher_float_types = [ILVTType.FLOAT16, ILVTType.FLOAT32, ILVTType.DECIMAL]
        for float_type in cypher_float_types:
            cypher_type = LanguageTypeMapper.getCypherCompatibleILVT(float_type)
            assert cypher_type == ILVTType.FLOAT64, f"{float_type} should map to FLOAT64 for Cypher"
    
    def test_legacyDatatypeConversion(self):
        """Test conversion from legacy string datatypes"""
        legacy_mappings = {
            "STRING": ValueType.STRING,
            "INTEGER": ValueType.INTEGER,
            "FLOAT": ValueType.FLOAT,
            "BOOLEAN": ValueType.BOOLEAN,
        }
        
        for legacy_type, expected_value_type in legacy_mappings.items():
            converted = convertLegacyDatatype(legacy_type, LanguageTypes.GQL)
            assert converted == expected_value_type, f"Legacy {legacy_type} should convert to {expected_value_type}"
    
    def test_languageTypeNames(self):
        """Test getting language-specific type names"""
        # Test GQL type names (lowercase)
        assert getLanguageTypeName(ValueType.INTEGER, LanguageTypes.GQL) == "bigint"  # INT64 -> bigint in GQL
        assert getLanguageTypeName(ValueType.FLOAT, LanguageTypes.GQL) == "double"
        
        # Test Cypher type names
        assert getLanguageTypeName(ValueType.INTEGER, LanguageTypes.CYPHER) == "INTEGER"
        assert getLanguageTypeName(ValueType.FLOAT, LanguageTypes.CYPHER) == "FLOAT"
    
    def test_preciseTypeInference(self):
        """Test precise type inference based on language level"""
        # Test integer value 128
        # In GQL/LEX: should infer UINT8 (most precise)
        # In Cypher: should infer INTEGER (only integer type available)
        
        assert inferPreciseType(128, LanguageTypes.GQL) == "uint8"
        assert inferPreciseType(128, LanguageTypes.JSON) == "number"  # JSON basic type  
        assert inferPreciseType(128, LanguageTypes.CYPHER) == "INTEGER"
        
        # Test larger integer value 70000
        assert inferPreciseType(70000, LanguageTypes.GQL) == "uint32"  # Fits in UINT32 (70000 > 65535)
        assert inferPreciseType(70000, LanguageTypes.CYPHER) == "INTEGER"
        
        # Test negative integer -100
        assert inferPreciseType(-100, LanguageTypes.GQL) == "int8"  # Fits in INT8
        assert inferPreciseType(-100, LanguageTypes.CYPHER) == "INTEGER"
    
    def test_typeTranslation(self):
        """Test type translation between language type systems"""
        # Translate Cypher INTEGER to GQL - should return all compatible integer types (lowercase)
        gql_equivalents = translateType("INTEGER", LanguageTypes.CYPHER, LanguageTypes.GQL)
        assert "int64" in gql_equivalents or "bigint" in gql_equivalents
        
        # Translate GQL uint8 to Cypher - should return INTEGER (uppercase)
        cypher_equivalents = translateType("uint8", LanguageTypes.GQL, LanguageTypes.CYPHER)
        assert "INTEGER" in cypher_equivalents
    
    def test_typeCompatibility(self):
        """Test type compatibility checking"""
        # Cypher INTEGER should be compatible with GQL bigint (lowercase)
        assert isTypeCompatible("INTEGER", LanguageTypes.CYPHER, "bigint", LanguageTypes.GQL)
        
        # GQL uint8 should be compatible with Cypher INTEGER
        assert isTypeCompatible("uint8", LanguageTypes.GQL, "INTEGER", LanguageTypes.CYPHER)


class TestLanguageLevelValidation:
    """Test validation behavior differences between language levels"""
    
    def test_integerValidationByLanguageLevel(self):
        """Test that integer validation respects language level"""
        test_value = 42
        
        # Should work for all language type systems
        cypher_result = ValueType.INTEGER.validate(test_value, LanguageTypes.CYPHER)
        gql_result = ValueType.INTEGER.validate(test_value, LanguageLevel.GQL)
        lex_result = ValueType.INTEGER.validate(test_value, LanguageLevel.LEX)
        
        assert cypher_result.isValid
        assert gql_result.isValid
        assert lex_result.isValid
    
    def test_errorMessagesByLanguageLevel(self):
        """Test that error messages are appropriate for language type system"""
        # Test with invalid boolean value
        cypher_result = ValueType.BOOLEAN.validate("true", LanguageTypes.CYPHER)
        gql_result = ValueType.BOOLEAN.validate("true", LanguageTypes.GQL)
        json_result = ValueType.BOOLEAN.validate("true", LanguageTypes.JSON)
        
        assert not cypher_result.isValid
        assert not gql_result.isValid
        assert not json_result.isValid
        
        # Error messages should mention the appropriate language type system
        assert "CYPHER" in cypher_result.errors[0]
        assert "GQL" in gql_result.errors[0]
        assert "JSON" in json_result.errors[0]


class TestUnimplementedTypes:
    """Test behavior of not-yet-implemented types"""
    
    def test_temporalTypesNotImplemented(self):
        """Test that temporal types return appropriate error messages"""
        temporal_types = [ValueType.DATE, ValueType.TIME, ValueType.DATETIME, ValueType.DURATION]
        
        for temporal_type in temporal_types:
            result = temporal_type.validate("2023-01-01")
            assert not result.isValid
            assert "not yet implemented" in result.errors[0]
    
    def test_complexTypesNotImplemented(self):
        """Test that complex types return appropriate error messages"""
        # Test ARRAY and MAP with GQL (should have ILVT mapping but no validator)
        for complex_type in [ValueType.ARRAY, ValueType.MAP]:
            result = complex_type.validate({})
            assert not result.isValid
            assert "not yet implemented" in result.errors[0]
        
        # Test JSON with JSON language type (should have ILVT mapping but no validator)
        result = ValueType.JSON.validate({}, LanguageTypes.JSON)
        assert not result.isValid
        assert "not yet implemented" in result.errors[0]


# Integration tests
class TestIntegration:
    """Integration tests combining multiple features"""
    
    def test_multipleValidations(self):
        """Test validating multiple values of different types"""
        test_cases = [
            ("hello", ValueType.STRING, True),
            (123, ValueType.INTEGER, True),
            (3.14, ValueType.FLOAT, True),
            (True, ValueType.BOOLEAN, True),
            (123, ValueType.STRING, False),
            ("hello", ValueType.INTEGER, False),
        ]
        
        for value, value_type, expected_valid in test_cases:
            result = value_type.validate(value)
            assert result.isValid == expected_valid, \
                f"Validation of {value} as {value_type.value} should be {expected_valid}"
    
    def test_errorMessageQuality(self):
        """Test that error messages are helpful and informative"""
        # Test various error scenarios
        error_cases = [
            (123, ValueType.STRING),
            ("hello", ValueType.INTEGER),
            (42, ValueType.FLOAT),
            ("true", ValueType.BOOLEAN),
        ]
        
        for value, value_type in error_cases:
            result = value_type.validate(value)
            assert not result.isValid
            assert len(result.errors) > 0
            
            error_msg = result.errors[0]
            # Error message should contain expected type and actual type
            assert value_type.value in error_msg
            assert type(value).__name__ in error_msg or str(type(value).__name__).lower() in error_msg.lower()