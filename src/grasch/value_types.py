"""
ILVT-based value type system for property graph schema validation.

This module implements the Intermediate Language Value Types (ILVT) specification
with language-level translation for GQL, SQL Foundation, and Cypher compatibility.
Supports configurable validation rules based on language level settings.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Union, Optional, List, Dict, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
import json
from datetime import datetime, date, time
import math

# Import language level from core module
from .core import LanguageLevel


class ValidationError(Exception):
    """Raised when value validation fails"""
    
    def __init__(self, message: str, path: str = "", 
                 expectedType: str = None, actualValue: Any = None):
        super().__init__(message)
        self.path = path
        self.expectedType = expectedType
        self.actualValue = actualValue


@dataclass
class ValidationResult:
    """Result of a validation operation"""
    isValid: bool
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
    
    @classmethod
    def success(cls, warnings: List[str] = None) -> 'ValidationResult':
        """Create a successful validation result"""
        return cls(isValid=True, warnings=warnings or [])
    
    @classmethod
    def failure(cls, error: str, warnings: List[str] = None) -> 'ValidationResult':
        """Create a failed validation result"""
        return cls(isValid=False, errors=[error], warnings=warnings or [])
    
    def addError(self, error: str) -> 'ValidationResult':
        """Add an error to this result"""
        self.errors.append(error)
        self.isValid = False
        return self
    
    def addWarning(self, warning: str) -> 'ValidationResult':
        """Add a warning to this result"""
        self.warnings.append(warning)
        return self


class ILVTType(Enum):
    """
    Intermediate Language Value Types (ILVT) enumeration.
    
    This enum represents the universal type system that maps between
    GQL, SQL Foundation, Cypher, and other type systems.
    """
    
    # Boolean Types
    BOOLEAN = "boolean"
    
    # Integer Types
    INT8 = "int8"
    INT16 = "int16" 
    INT32 = "int32"
    INT64 = "int64"
    INT128 = "int128"
    INT256 = "int256"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    UINT128 = "uint128"
    UINT256 = "uint256"
    
    # Decimal Types
    DECIMAL = "decimal"
    NUMERIC = "numeric"
    
    # Floating Point Types
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    FLOAT64 = "float64"
    FLOAT128 = "float128"
    FLOAT256 = "float256"
    DECFLOAT32 = "decfloat32"
    DECFLOAT64 = "decfloat64"
    DECFLOAT128 = "decfloat128"
    
    # String Types
    STRING = "string"
    CHAR = "char"
    
    # Binary Types
    BYTES = "bytes"
    BINARY = "binary"
    
    # Temporal Types
    DATE = "date"
    TIME = "time"
    TIME_TZ = "time_tz"
    DATETIME = "datetime"
    DATETIME_TZ = "datetime_tz"
    DURATION = "duration"
    
    # Structured Types
    RECORD = "record"
    ARRAY = "array"
    MULTISET = "multiset"
    
    # Special Types
    JSON = "json"
    VECTOR = "vector"
    NULL = "null"


# Language-specific type mappings
class LanguageTypeMapper:
    """
    Maps between ILVT types and language-specific type names.
    
    Language Level Hierarchy: Cypher ⊆ GSQL ⊆ GQL ⊆ LEX
    - Cypher: Limited type system (INTEGER=64bit, FLOAT=64bit, STRING, BOOLEAN, etc.)
    - GQL: Full precision type system (INT8, UINT8, FLOAT32, etc.)
    - LEX: GQL + extensions (JSON type)
    """
    
    # Cypher Data Type mappings (most restrictive)
    CYPHER_MAPPINGS = {
        ILVTType.BOOLEAN: ["BOOLEAN"],
        ILVTType.INT64: ["INTEGER"],  # Cypher only has 64-bit integers
        ILVTType.FLOAT64: ["FLOAT"],  # Cypher only has 64-bit floats
        ILVTType.STRING: ["STRING"],
        ILVTType.DATE: ["DATE"],
        ILVTType.TIME: ["TIME"],
        ILVTType.DATETIME: ["DATETIME"],
        ILVTType.DURATION: ["DURATION"],
        ILVTType.ARRAY: ["LIST"],
        ILVTType.NULL: ["NULL"],
    }
    
    # GQL Property Value Type mappings (full precision)
    GQL_MAPPINGS = {
        ILVTType.BOOLEAN: ["BOOLEAN", "BOOL"],
        ILVTType.INT8: ["INT8"],
        ILVTType.INT16: ["SMALLINT", "INT16"],
        ILVTType.INT32: ["INTEGER", "INT", "INT32"],
        ILVTType.INT64: ["BIGINT", "INT64"],
        ILVTType.INT128: ["INT128"],
        ILVTType.INT256: ["INT256"],
        ILVTType.UINT8: ["UINT8"],
        ILVTType.UINT16: ["UINT16"],
        ILVTType.UINT32: ["UINT32"],
        ILVTType.UINT64: ["UINT64"],
        ILVTType.UINT128: ["UINT128"],
        ILVTType.UINT256: ["UINT256"],
        ILVTType.DECIMAL: ["DECIMAL", "DEC"],
        ILVTType.NUMERIC: ["NUMERIC"],
        ILVTType.FLOAT16: ["FLOAT16"],
        ILVTType.FLOAT32: ["FLOAT", "REAL", "FLOAT32"],
        ILVTType.FLOAT64: ["DOUBLE", "DOUBLE PRECISION", "FLOAT64"],
        ILVTType.FLOAT128: ["FLOAT128"],
        ILVTType.FLOAT256: ["FLOAT256"],
        ILVTType.STRING: ["STRING"],
        ILVTType.CHAR: ["CHAR"],
        ILVTType.BYTES: ["BYTES"],
        ILVTType.BINARY: ["BINARY"],
        ILVTType.DATE: ["DATE"],
        ILVTType.TIME: ["LOCAL TIME"],
        ILVTType.TIME_TZ: ["ZONED TIME"],
        ILVTType.DATETIME: ["LOCAL DATETIME"],
        ILVTType.DATETIME_TZ: ["ZONED DATETIME"],
        ILVTType.DURATION: ["DURATION"],
        ILVTType.RECORD: ["RECORD"],
        ILVTType.ARRAY: ["LIST"],
        ILVTType.VECTOR: ["VECTOR"],
        ILVTType.NULL: ["NULL"],
    }
    
    # LEX extensions (GQL + additional types)
    LEX_EXTENSIONS = {
        ILVTType.JSON: ["JSON"],  # JSON type is LEX-specific extension
    }
    
    # SQL Foundation mappings (for reference)
    SQL_MAPPINGS = {
        ILVTType.BOOLEAN: ["BOOLEAN"],
        ILVTType.INT16: ["SMALLINT"],
        ILVTType.INT32: ["INTEGER", "INT"],
        ILVTType.INT64: ["BIGINT"],
        ILVTType.DECIMAL: ["DECIMAL", "NUMERIC", "DEC"],
        ILVTType.NUMERIC: ["NUMERIC"],
        ILVTType.FLOAT32: ["REAL"],
        ILVTType.FLOAT64: ["DOUBLE PRECISION"],
        ILVTType.DECFLOAT32: ["DECFLOAT(7)"],
        ILVTType.DECFLOAT64: ["DECFLOAT(16)"],
        ILVTType.DECFLOAT128: ["DECFLOAT(34)"],
        ILVTType.STRING: ["VARCHAR", "CHARACTER VARYING"],
        ILVTType.CHAR: ["CHAR", "CHARACTER"],
        ILVTType.BYTES: ["BLOB", "BINARY LARGE OBJECT"],
        ILVTType.BINARY: ["BINARY"],
        ILVTType.DATE: ["DATE"],
        ILVTType.TIME: ["TIME"],
        ILVTType.TIME_TZ: ["TIME WITH TIME ZONE"],
        ILVTType.DATETIME: ["TIMESTAMP"],
        ILVTType.DATETIME_TZ: ["TIMESTAMP WITH TIME ZONE"],
        ILVTType.DURATION: ["INTERVAL"],
        ILVTType.RECORD: ["ROW"],
        ILVTType.ARRAY: ["ARRAY"],
        ILVTType.MULTISET: ["MULTISET"],
        ILVTType.JSON: ["JSON"],
        ILVTType.VECTOR: ["VECTOR"],
        ILVTType.NULL: ["NULL"],
    }
    
    @classmethod
    def getAvailableTypesForLanguageLevel(cls, languageLevel: LanguageLevel) -> Dict[ILVTType, List[str]]:
        """Get all available types for a given language level"""
        if languageLevel == LanguageLevel.LEX:
            # LEX = GQL + extensions
            return {**cls.GQL_MAPPINGS, **cls.LEX_EXTENSIONS}
        elif languageLevel == LanguageLevel.GQL:
            # GQL has full type system
            return cls.GQL_MAPPINGS.copy()
        else:
            # Cypher has limited type system
            return cls.CYPHER_MAPPINGS.copy()
    
    @classmethod
    def getILVTFromLanguageType(cls, languageType: str, languageLevel: LanguageLevel) -> Optional[ILVTType]:
        """Convert a language-specific type name to ILVT type"""
        languageType = languageType.upper()
        available_types = cls.getAvailableTypesForLanguageLevel(languageLevel)
        
        for ilvt_type, type_names in available_types.items():
            if languageType in type_names:
                return ilvt_type
        
        return None
    
    @classmethod
    def getLanguageTypeFromILVT(cls, ilvtType: ILVTType, languageLevel: LanguageLevel) -> Optional[str]:
        """Convert ILVT type to language-specific type name"""
        available_types = cls.getAvailableTypesForLanguageLevel(languageLevel)
        type_names = available_types.get(ilvtType)
        return type_names[0] if type_names else None
    
    @classmethod
    def inferMostPreciseType(cls, value: Any, languageLevel: LanguageLevel) -> Optional[ILVTType]:
        """
        Infer the most precise ILVT type for a value based on language level.
        
        Higher language levels (GQL, LEX) can infer more precise types.
        Lower language levels (Cypher) infer broader types.
        """
        if value is None:
            return ILVTType.NULL
        
        if isinstance(value, bool):
            return ILVTType.BOOLEAN
        elif isinstance(value, int):
            if languageLevel == LanguageLevel.LEX or languageLevel == LanguageLevel.GQL:
                # GQL/LEX can infer precise integer types based on value range
                if 0 <= value <= 255:
                    return ILVTType.UINT8
                elif -128 <= value <= 127:
                    return ILVTType.INT8
                elif 0 <= value <= 65535:
                    return ILVTType.UINT16
                elif -32768 <= value <= 32767:
                    return ILVTType.INT16
                elif 0 <= value <= 4294967295:
                    return ILVTType.UINT32
                elif -2147483648 <= value <= 2147483647:
                    return ILVTType.INT32
                elif 0 <= value <= 18446744073709551615:
                    return ILVTType.UINT64
                else:
                    return ILVTType.INT64
            else:
                # Cypher only has 64-bit integers
                return ILVTType.INT64
        elif isinstance(value, float):
            if languageLevel == LanguageLevel.LEX or languageLevel == LanguageLevel.GQL:
                # Could infer FLOAT32 vs FLOAT64 based on precision, but default to FLOAT64
                return ILVTType.FLOAT64
            else:
                # Cypher only has 64-bit floats
                return ILVTType.FLOAT64
        elif isinstance(value, str):
            return ILVTType.STRING
        elif isinstance(value, (list, tuple)):
            return ILVTType.ARRAY
        elif isinstance(value, dict):
            if languageLevel == LanguageLevel.LEX:
                # LEX supports JSON type
                return ILVTType.JSON
            else:
                # Fall back to RECORD for other levels
                return ILVTType.RECORD
        
        return None
    
    @classmethod
    def getEquivalentTypes(cls, sourceType: str, sourceLanguage: LanguageLevel, 
                          targetLanguage: LanguageLevel) -> List[str]:
        """
        Get all equivalent types when translating between language levels.
        
        For example: Cypher.INTEGER -> GQL returns [INT64, BIGINT] and supertypes
        """
        # First convert source type to ILVT
        source_ilvt = cls.getILVTFromLanguageType(sourceType, sourceLanguage)
        if source_ilvt is None:
            return []
        
        # Get available types in target language
        target_types = cls.getAvailableTypesForLanguageLevel(targetLanguage)
        
        # Find direct equivalent
        direct_equivalent = target_types.get(source_ilvt, [])
        
        # For integer types, also include supertypes and subtypes
        if source_ilvt in [ILVTType.INT8, ILVTType.INT16, ILVTType.INT32, ILVTType.INT64, 
                          ILVTType.UINT8, ILVTType.UINT16, ILVTType.UINT32, ILVTType.UINT64]:
            
            # Define integer type hierarchy (smaller -> larger)
            int_hierarchy = [
                ILVTType.INT8, ILVTType.UINT8,
                ILVTType.INT16, ILVTType.UINT16, 
                ILVTType.INT32, ILVTType.UINT32,
                ILVTType.INT64, ILVTType.UINT64,
                ILVTType.INT128, ILVTType.INT256
            ]
            
            # Find position of source type
            try:
                source_pos = int_hierarchy.index(source_ilvt)
                # Include all supertypes (larger types that can hold the value)
                for supertype in int_hierarchy[source_pos:]:
                    if supertype in target_types:
                        direct_equivalent.extend(target_types[supertype])
            except ValueError:
                pass
        
        # Remove duplicates and return
        return list(dict.fromkeys(direct_equivalent))
    
    @classmethod
    def isTypeCompatible(cls, sourceType: str, sourceLanguage: LanguageLevel,
                        targetType: str, targetLanguage: LanguageLevel) -> bool:
        """Check if source type is compatible with target type"""
        equivalent_types = cls.getEquivalentTypes(sourceType, sourceLanguage, targetLanguage)
        return targetType.upper() in [t.upper() for t in equivalent_types]


class ValueType(Enum):
    """
    Backward-compatible ValueType enum that maps to ILVT types.
    
    This maintains the existing API while using ILVT internally.
    """
    
    # Primitive Types (map to ILVT)
    STRING = "STRING"
    INTEGER = "INTEGER" 
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    
    # Temporal Types
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    DURATION = "DURATION"
    
    # Complex Types
    JSON = "JSON"
    ARRAY = "ARRAY"
    MAP = "MAP"
    
    def getILVTType(self, languageLevel: LanguageLevel = LanguageLevel.GQL) -> ILVTType:
        """Get the corresponding ILVT type for this ValueType based on language level"""
        # Base mapping - these are the "default" ILVT types for each ValueType
        base_mapping = {
            ValueType.STRING: ILVTType.STRING,
            ValueType.INTEGER: ILVTType.INT64,  # Default to 64-bit
            ValueType.FLOAT: ILVTType.FLOAT64,  # Default to 64-bit
            ValueType.BOOLEAN: ILVTType.BOOLEAN,
            ValueType.DATE: ILVTType.DATE,
            ValueType.TIME: ILVTType.TIME,
            ValueType.DATETIME: ILVTType.DATETIME,
            ValueType.DURATION: ILVTType.DURATION,
            ValueType.JSON: ILVTType.JSON,
            ValueType.ARRAY: ILVTType.ARRAY,
            ValueType.MAP: ILVTType.RECORD,
        }
        
        ilvt_type = base_mapping.get(self)
        
        # Adjust based on language level capabilities
        if ilvt_type == ILVTType.JSON and languageLevel != LanguageLevel.LEX:
            # JSON is only available in LEX level
            return None
        
        return ilvt_type
    
    def validate(self, value: Any, languageLevel: LanguageLevel = LanguageLevel.GQL) -> ValidationResult:
        """Validate a value against this type with language-level awareness"""
        if value is None:
            return ValidationResult.failure(f"Value cannot be null for type {self.value}")
        
        # Get the ILVT type for validation
        ilvt_type = self.getILVTType(languageLevel)
        if ilvt_type is None:
            return ValidationResult.failure(f"No ILVT mapping for type {self.value}")
        
        # Dispatch to ILVT validation
        return self._validateILVTType(value, ilvt_type, languageLevel)
    
    def _validateILVTType(self, value: Any, ilvtType: ILVTType, languageLevel: LanguageLevel) -> ValidationResult:
        """Validate a value against an ILVT type"""
        validator_map = {
            ILVTType.BOOLEAN: self._validateBoolean,
            ILVTType.INT64: self._validateInteger64,
            ILVTType.FLOAT64: self._validateFloat64,
            ILVTType.STRING: self._validateString,
            # Other types will be implemented in later tasks
        }
        
        validator = validator_map.get(ilvtType)
        if validator is None:
            return ValidationResult.failure(f"Validation not yet implemented for ILVT type {ilvtType.value}")
        
        return validator(value, languageLevel)
    
    def _validateString(self, value: Any, languageLevel: LanguageLevel) -> ValidationResult:
        """Validate STRING type (ILVT string)"""
        if isinstance(value, str):
            return ValidationResult.success()
        
        # Language-level specific behavior
        if languageLevel == LanguageLevel.LEX:
            # LEX level (Cypher compatibility) is more permissive
            if isinstance(value, (int, float, bool)):
                return ValidationResult.failure(
                    f"Expected STRING, got {type(value).__name__} {repr(value)}. "
                    f"Cypher requires explicit string conversion."
                )
        else:
            # GQL level is strict
            if isinstance(value, (int, float, bool)):
                return ValidationResult.failure(
                    f"Expected STRING, got {type(value).__name__}. "
                    f"Use explicit string conversion if intended."
                )
        
        return ValidationResult.failure(
            f"Expected STRING, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateInteger64(self, value: Any, languageLevel: LanguageLevel) -> ValidationResult:
        """Validate 64-bit INTEGER type (ILVT int64)"""
        if isinstance(value, int) and not isinstance(value, bool):
            # Check for 64-bit signed integer range
            if -9223372036854775808 <= value <= 9223372036854775807:
                return ValidationResult.success()
            else:
                return ValidationResult.failure(
                    f"Integer value {value} is outside the 64-bit signed range "
                    f"[-9223372036854775808, 9223372036854775807]"
                )
        
        # Handle float-to-integer conversion based on language level
        if isinstance(value, float):
            if value.is_integer() and not (math.isinf(value) or math.isnan(value)):
                int_value = int(value)
                if -9223372036854775808 <= int_value <= 9223372036854775807:
                    if languageLevel == LanguageLevel.LEX:
                        # LEX level might be more permissive with conversions
                        return ValidationResult.failure(
                            f"Expected INTEGER, got FLOAT {value}. "
                            f"Cypher requires explicit integer conversion."
                        )
                    else:
                        return ValidationResult.failure(
                            f"Expected INTEGER, got FLOAT {value}. "
                            f"Use explicit integer conversion if intended."
                        )
            return ValidationResult.failure(
                f"Cannot convert FLOAT {value} to INTEGER: not a whole number"
            )
        
        return ValidationResult.failure(
            f"Expected INTEGER, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateFloat64(self, value: Any, languageLevel: LanguageLevel) -> ValidationResult:
        """Validate 64-bit FLOAT type (ILVT float64)"""
        if isinstance(value, float):
            # Check for valid float values (including NaN and Infinity)
            return ValidationResult.success()
        
        # Handle integer-to-float conversion based on language level
        if isinstance(value, int) and not isinstance(value, bool):
            if languageLevel == LanguageLevel.LEX:
                # LEX level (Cypher) might be more permissive
                return ValidationResult.failure(
                    f"Expected FLOAT, got INTEGER {value}. "
                    f"Cypher requires explicit float conversion."
                )
            else:
                return ValidationResult.failure(
                    f"Expected FLOAT, got INTEGER {value}. "
                    f"Use explicit float conversion if intended."
                )
        
        return ValidationResult.failure(
            f"Expected FLOAT, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateBoolean(self, value: Any, languageLevel: LanguageLevel) -> ValidationResult:
        """Validate BOOLEAN type (ILVT boolean)"""
        if isinstance(value, bool):
            return ValidationResult.success()
        
        # Both GQL and LEX levels are strict about boolean validation
        if isinstance(value, (int, str)):
            lang_name = "Cypher" if languageLevel == LanguageLevel.LEX else "GQL"
            return ValidationResult.failure(
                f"Expected BOOLEAN, got {type(value).__name__} {repr(value)}. "
                f"{lang_name} requires explicit boolean conversion."
            )
        
        return ValidationResult.failure(
            f"Expected BOOLEAN, got {type(value).__name__}: {repr(value)}"
        )
    
    def getDescription(self) -> str:
        """Get a human-readable description of this type"""
        descriptions = {
            ValueType.STRING: "Text string value",
            ValueType.INTEGER: "64-bit signed integer (-9223372036854775808 to 9223372036854775807)",
            ValueType.FLOAT: "IEEE 754 double-precision floating-point number",
            ValueType.BOOLEAN: "Boolean value (true or false)",
            ValueType.DATE: "ISO 8601 date (YYYY-MM-DD)",
            ValueType.TIME: "ISO 8601 time (HH:MM:SS[.fff])",
            ValueType.DATETIME: "ISO 8601 datetime with optional timezone",
            ValueType.DURATION: "ISO 8601 duration (P[n]Y[n]M[n]DT[n]H[n]M[n]S)",
            ValueType.JSON: "JSON object or array",
            ValueType.ARRAY: "Array of values with specified element type",
            ValueType.MAP: "Map/dictionary with specified key and value types",
        }
        return descriptions.get(self, f"Value of type {self.value}")
    
    def isCompatibleWith(self, other: 'ValueType') -> bool:
        """Check if this type is compatible with another type"""
        if self == other:
            return True
        
        # Define compatibility rules
        compatibility_rules = {
            # Numeric compatibility
            (ValueType.INTEGER, ValueType.FLOAT): True,
            (ValueType.FLOAT, ValueType.INTEGER): False,  # Lossy conversion
            
            # String compatibility (strings can represent anything)
            (ValueType.STRING, ValueType.INTEGER): False,  # Requires parsing
            (ValueType.STRING, ValueType.FLOAT): False,    # Requires parsing
            (ValueType.STRING, ValueType.BOOLEAN): False,  # Requires parsing
            
            # No automatic boolean conversions
            (ValueType.BOOLEAN, ValueType.INTEGER): False,
            (ValueType.INTEGER, ValueType.BOOLEAN): False,
        }
        
        return compatibility_rules.get((self, other), False)
    
    @classmethod
    def fromString(cls, typeString: str) -> 'ValueType':
        """Create ValueType from string representation"""
        try:
            return cls(typeString.upper())
        except ValueError:
            raise ValidationError(
                f"Unknown value type: {typeString}. "
                f"Valid types are: {', '.join([vt.value for vt in cls])}"
            )


# Utility functions for type validation with language level support
def validateValue(value: Any, valueType: ValueType, languageLevel: LanguageLevel = LanguageLevel.GQL) -> ValidationResult:
    """Convenience function to validate a value against a type with language level"""
    return valueType.validate(value, languageLevel)


def isValidValue(value: Any, valueType: ValueType, languageLevel: LanguageLevel = LanguageLevel.GQL) -> bool:
    """Convenience function to check if a value is valid for a type with language level"""
    return valueType.validate(value, languageLevel).isValid


def getTypeForValue(value: Any, languageLevel: LanguageLevel = LanguageLevel.GQL) -> Optional[ValueType]:
    """Infer the most appropriate ValueType for a given value based on language level"""
    # Use the precise ILVT inference, then map back to ValueType
    ilvt_type = LanguageTypeMapper.inferMostPreciseType(value, languageLevel)
    
    if ilvt_type is None:
        return None
    
    # Map ILVT type back to ValueType
    ilvt_to_valuetype = {
        ILVTType.BOOLEAN: ValueType.BOOLEAN,
        ILVTType.INT8: ValueType.INTEGER,
        ILVTType.INT16: ValueType.INTEGER,
        ILVTType.INT32: ValueType.INTEGER,
        ILVTType.INT64: ValueType.INTEGER,
        ILVTType.UINT8: ValueType.INTEGER,
        ILVTType.UINT16: ValueType.INTEGER,
        ILVTType.UINT32: ValueType.INTEGER,
        ILVTType.UINT64: ValueType.INTEGER,
        ILVTType.FLOAT16: ValueType.FLOAT,
        ILVTType.FLOAT32: ValueType.FLOAT,
        ILVTType.FLOAT64: ValueType.FLOAT,
        ILVTType.STRING: ValueType.STRING,
        ILVTType.DATE: ValueType.DATE,
        ILVTType.TIME: ValueType.TIME,
        ILVTType.DATETIME: ValueType.DATETIME,
        ILVTType.DURATION: ValueType.DURATION,
        ILVTType.ARRAY: ValueType.ARRAY,
        ILVTType.RECORD: ValueType.MAP,
        ILVTType.JSON: ValueType.JSON,
        ILVTType.NULL: None,
    }
    
    return ilvt_to_valuetype.get(ilvt_type)


def convertLegacyDatatype(datatype: str, languageLevel: LanguageLevel = LanguageLevel.GQL) -> Optional[ValueType]:
    """
    Convert legacy string datatypes to ValueType enum.
    
    This function provides backward compatibility for existing PropertyType usage
    that uses string datatypes like "STRING", "INTEGER", etc.
    """
    # First try to get ILVT type from the language-specific type name
    ilvt_type = LanguageTypeMapper.getILVTFromLanguageType(datatype, languageLevel)
    
    if ilvt_type is None:
        return None
    
    # Map ILVT type back to ValueType
    ilvt_to_valuetype = {
        ILVTType.BOOLEAN: ValueType.BOOLEAN,
        ILVTType.INT8: ValueType.INTEGER,
        ILVTType.INT16: ValueType.INTEGER,
        ILVTType.INT32: ValueType.INTEGER,
        ILVTType.INT64: ValueType.INTEGER,
        ILVTType.INT128: ValueType.INTEGER,
        ILVTType.INT256: ValueType.INTEGER,
        ILVTType.UINT8: ValueType.INTEGER,
        ILVTType.UINT16: ValueType.INTEGER,
        ILVTType.UINT32: ValueType.INTEGER,
        ILVTType.UINT64: ValueType.INTEGER,
        ILVTType.UINT128: ValueType.INTEGER,
        ILVTType.UINT256: ValueType.INTEGER,
        ILVTType.FLOAT16: ValueType.FLOAT,
        ILVTType.FLOAT32: ValueType.FLOAT,
        ILVTType.FLOAT64: ValueType.FLOAT,
        ILVTType.FLOAT128: ValueType.FLOAT,
        ILVTType.FLOAT256: ValueType.FLOAT,
        ILVTType.DECIMAL: ValueType.FLOAT,
        ILVTType.NUMERIC: ValueType.FLOAT,
        ILVTType.DECFLOAT32: ValueType.FLOAT,
        ILVTType.DECFLOAT64: ValueType.FLOAT,
        ILVTType.DECFLOAT128: ValueType.FLOAT,
        ILVTType.STRING: ValueType.STRING,
        ILVTType.CHAR: ValueType.STRING,
        ILVTType.DATE: ValueType.DATE,
        ILVTType.TIME: ValueType.TIME,
        ILVTType.TIME_TZ: ValueType.TIME,
        ILVTType.DATETIME: ValueType.DATETIME,
        ILVTType.DATETIME_TZ: ValueType.DATETIME,
        ILVTType.DURATION: ValueType.DURATION,
        ILVTType.ARRAY: ValueType.ARRAY,
        ILVTType.RECORD: ValueType.MAP,
        ILVTType.JSON: ValueType.JSON,
    }
    
    return ilvt_to_valuetype.get(ilvt_type)


def getLanguageTypeName(valueType: ValueType, languageLevel: LanguageLevel = LanguageLevel.GQL) -> Optional[str]:
    """Get the language-specific type name for a ValueType"""
    ilvt_type = valueType.getILVTType(languageLevel)
    if ilvt_type is None:
        return None
    
    return LanguageTypeMapper.getLanguageTypeFromILVT(ilvt_type, languageLevel)


def translateType(sourceType: str, sourceLanguage: LanguageLevel, 
                 targetLanguage: LanguageLevel) -> List[str]:
    """
    Translate a type from one language level to another.
    
    Returns all equivalent types in the target language.
    For example: translateType("INTEGER", LanguageLevel.LEX, LanguageLevel.GQL) 
    might return ["INT64", "BIGINT"] and supertypes.
    """
    return LanguageTypeMapper.getEquivalentTypes(sourceType, sourceLanguage, targetLanguage)


def isTypeCompatible(sourceType: str, sourceLanguage: LanguageLevel,
                    targetType: str, targetLanguage: LanguageLevel) -> bool:
    """Check if a source type is compatible with a target type across language levels"""
    return LanguageTypeMapper.isTypeCompatible(sourceType, sourceLanguage, targetType, targetLanguage)


def inferPreciseType(value: Any, languageLevel: LanguageLevel = LanguageLevel.GQL) -> Optional[str]:
    """
    Infer the most precise type name for a value at a given language level.
    
    Examples:
    - inferPreciseType(128, LanguageLevel.LEX) -> "UINT8" (most precise)
    - inferPreciseType(128, LanguageLevel.CYPHER) -> "INTEGER" (Cypher only has INTEGER)
    """
    ilvt_type = LanguageTypeMapper.inferMostPreciseType(value, languageLevel)
    if ilvt_type is None:
        return None
    
    return LanguageTypeMapper.getLanguageTypeFromILVT(ilvt_type, languageLevel)