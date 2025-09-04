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

# Import language types from core module
from .core import LanguageLevel, LanguageTypes


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
    
    Language Type Systems (orthogonal to LanguageLevel):
    - Cypher: Limited type system (INTEGER=64bit, FLOAT=64bit, STRING, BOOLEAN, etc.)
    - GQL: Full precision type system (INT8, UINT8, FLOAT32, etc.)
    - SQL: SQL Foundation data types
    - JSON: JSON Schema type system
    - DatabaseJSON: Database-specific JSON extensions
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
        ILVTType.BOOLEAN: ["boolean", "bool"],
        ILVTType.INT8: ["int8"],
        ILVTType.INT16: ["smallint", "int16"],
        ILVTType.INT32: ["integer", "int", "int32"],
        ILVTType.INT64: ["bigint", "int64"],
        ILVTType.INT128: ["int128"],
        ILVTType.INT256: ["int256"],
        ILVTType.UINT8: ["uint8"],
        ILVTType.UINT16: ["uint16"],
        ILVTType.UINT32: ["uint32"],
        ILVTType.UINT64: ["uint64"],
        ILVTType.UINT128: ["uint128"],
        ILVTType.UINT256: ["uint256"],
        ILVTType.DECIMAL: ["decimal", "dec"],
        ILVTType.NUMERIC: ["numeric"],
        ILVTType.FLOAT16: ["float16"],
        ILVTType.FLOAT32: ["float", "real", "float32"],
        ILVTType.FLOAT64: ["double", "double precision", "float64"],
        ILVTType.FLOAT128: ["float128"],
        ILVTType.FLOAT256: ["float256"],
        ILVTType.STRING: ["string"],
        ILVTType.CHAR: ["char"],
        ILVTType.BYTES: ["bytes"],
        ILVTType.BINARY: ["binary"],
        ILVTType.DATE: ["date"],
        ILVTType.TIME: ["local time"],
        ILVTType.TIME_TZ: ["zoned time"],
        ILVTType.DATETIME: ["local datetime"],
        ILVTType.DATETIME_TZ: ["zoned datetime"],
        ILVTType.DURATION: ["duration"],
        ILVTType.RECORD: ["record"],
        ILVTType.ARRAY: ["list"],
        ILVTType.VECTOR: ["vector"],
        ILVTType.NULL: ["null"],
    }
    
    # Basic JSON Schema type mappings (limited precision)
    JSON_SCHEMA_MAPPINGS = {
        # All integers map to "number" (with 64-bit signed limit)
        ILVTType.INT8: ["number"],
        ILVTType.INT16: ["number"], 
        ILVTType.INT32: ["number"],
        ILVTType.INT64: ["number"],
        ILVTType.UINT8: ["number"],
        ILVTType.UINT16: ["number"],
        ILVTType.UINT32: ["number"],
        ILVTType.UINT64: ["number"],    # Note: May lose precision for values > 2^53
        ILVTType.INT128: ["number"],    # Note: Will lose precision
        ILVTType.INT256: ["number"],    # Note: Will lose precision
        # All floats map to "number" (with 54-bit precision limit)
        ILVTType.FLOAT16: ["number"],
        ILVTType.FLOAT32: ["number"],
        ILVTType.FLOAT64: ["number"],
        ILVTType.DECIMAL: ["number"],   # Note: May lose precision
        # Basic types
        ILVTType.STRING: ["string"],
        ILVTType.BOOLEAN: ["boolean"],
        ILVTType.ARRAY: ["array"],
        ILVTType.RECORD: ["object"],
        ILVTType.NULL: ["null"],
        # Complex types that don't have direct JSON equivalents map to string or object
        ILVTType.DATE: ["string"],      # ISO date string
        ILVTType.TIME: ["string"],      # ISO time string  
        ILVTType.DATETIME: ["string"],  # ISO datetime string
        ILVTType.DURATION: ["string"],  # ISO duration string
        ILVTType.BYTES: ["string"],     # Base64 encoded string
    }
    
    # LEX extensions (GQL + additional types)
    LEX_EXTENSIONS = {
        ILVTType.JSON: ["json"],  # JSON type is LEX-specific extension
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
    def getAvailableTypesForLanguageType(cls, languageType: LanguageTypes) -> Dict[ILVTType, List[str]]:
        """Get all available types for a given language type system"""
        if languageType == LanguageTypes.GQL:
            return cls.GQL_MAPPINGS.copy()
        elif languageType == LanguageTypes.CYPHER:
            return cls.CYPHER_MAPPINGS.copy()
        elif languageType == LanguageTypes.SQL:
            return cls.SQL_MAPPINGS.copy()
        elif languageType == LanguageTypes.JSON:
            # Basic JSON Schema types (limited precision)
            return cls.JSON_SCHEMA_MAPPINGS.copy()
        elif languageType == LanguageTypes.DATABASE_JSON:
            # Database JSON - 1:1 mapping with GQL types + JSON type
            # Each GQL type maps to structured JSON: {"type": "basic_json_type", "value": ...}
            # The "type" field references LanguageTypes.JSON basic types
            return {**cls.GQL_MAPPINGS, **cls.LEX_EXTENSIONS}
        else:
            # Default to GQL
            return cls.GQL_MAPPINGS.copy()
    
    @classmethod
    def getILVTFromLanguageType(cls, typeName: str, languageType: LanguageTypes) -> Optional[ILVTType]:
        """Convert a language-specific type name to ILVT type"""
        available_types = cls.getAvailableTypesForLanguageType(languageType)
        
        # Handle case sensitivity based on language type conventions:
        # - JSON, GQL, LEX: case-sensitive (lowercase)
        # - Cypher, SQL: case-insensitive (uppercase)
        if languageType in [LanguageTypes.JSON, LanguageTypes.GQL, LanguageTypes.DATABASE_JSON]:
            # Case-sensitive matching for lowercase type systems
            search_name = typeName.lower()
            for ilvt_type, type_names in available_types.items():
                if search_name in [name.lower() for name in type_names]:
                    return ilvt_type
        else:
            # Case-insensitive matching for uppercase type systems (Cypher, SQL)
            search_name = typeName.upper()
            for ilvt_type, type_names in available_types.items():
                if search_name in [name.upper() for name in type_names]:
                    return ilvt_type
        
        return None
    
    @classmethod
    def getLanguageTypeFromILVT(cls, ilvtType: ILVTType, languageType: LanguageTypes) -> Optional[str]:
        """Convert ILVT type to language-specific type name"""
        available_types = cls.getAvailableTypesForLanguageType(languageType)
        type_names = available_types.get(ilvtType)
        return type_names[0] if type_names else None
    
    @classmethod
    def inferMostPreciseType(cls, value: Any, languageType: LanguageTypes) -> Optional[ILVTType]:
        """
        Infer the most precise ILVT type for a value based on language type system.
        
        More precise type systems (GQL) can infer more specific types.
        Less precise type systems (Cypher) infer broader types.
        """
        if value is None:
            return ILVTType.NULL
        
        if isinstance(value, bool):
            return ILVTType.BOOLEAN
        elif isinstance(value, int):
            if languageType in [LanguageTypes.GQL, LanguageTypes.DATABASE_JSON]:
                # GQL and DATABASE_JSON can infer precise integer types based on value range
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
            elif languageType == LanguageTypes.JSON:
                # JSON has limited precision - safe integers are -2^53 to 2^53
                # All integers map to FLOAT64 (JSON "number" type)
                if -9007199254740991 <= value <= 9007199254740991:  # -2^53 to 2^53
                    return ILVTType.FLOAT64  # JSON "number" type
                else:
                    # Outside safe integer range - would need string representation
                    return ILVTType.STRING
            elif languageType == LanguageTypes.CYPHER:
                # Cypher only has 64-bit integers
                return ILVTType.INT64
            elif languageType == LanguageTypes.SQL:
                # SQL has limited integer types, default to appropriate size
                if -2147483648 <= value <= 2147483647:
                    return ILVTType.INT32
                else:
                    return ILVTType.INT64
            else:
                # Default to INT64 for other type systems
                return ILVTType.INT64
        elif isinstance(value, float):
            if languageType in [LanguageTypes.GQL, LanguageTypes.DATABASE_JSON]:
                # Could infer FLOAT32 vs FLOAT64 based on precision, but default to FLOAT64
                return ILVTType.FLOAT64
            elif languageType == LanguageTypes.JSON:
                # JSON only has "number" type (IEEE 754 double precision)
                return ILVTType.FLOAT64
            elif languageType == LanguageTypes.CYPHER:
                # Cypher only has 64-bit floats
                return ILVTType.FLOAT64
            elif languageType == LanguageTypes.SQL:
                # SQL defaults to DOUBLE PRECISION
                return ILVTType.FLOAT64
            else:
                return ILVTType.FLOAT64
        elif isinstance(value, str):
            return ILVTType.STRING
        elif isinstance(value, (list, tuple)):
            return ILVTType.ARRAY
        elif isinstance(value, dict):
            if languageType == LanguageTypes.JSON:
                # Basic JSON Schema - dict maps to "object" type
                return ILVTType.RECORD
            elif languageType == LanguageTypes.DATABASE_JSON:
                # Extended database JSON - dict can be JSON type
                return ILVTType.JSON
            else:
                # Fall back to RECORD for other type systems
                return ILVTType.RECORD
        
        return None
    
    @classmethod
    def getEquivalentTypes(cls, sourceType: str, sourceLanguageType: LanguageTypes, 
                          targetLanguageType: LanguageTypes) -> List[str]:
        """
        Get all equivalent types when translating between language type systems.
        
        For example: Cypher.INTEGER -> GQL returns [INT64, BIGINT] and supertypes
        """
        # First convert source type to ILVT
        source_ilvt = cls.getILVTFromLanguageType(sourceType, sourceLanguageType)
        if source_ilvt is None:
            return []
        
        # Get available types in target language type system
        target_types = cls.getAvailableTypesForLanguageType(targetLanguageType)
        
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
    def isTypeCompatible(cls, sourceType: str, sourceLanguageType: LanguageTypes,
                        targetType: str, targetLanguageType: LanguageTypes) -> bool:
        """Check if source type is compatible with target type"""
        equivalent_types = cls.getEquivalentTypes(sourceType, sourceLanguageType, targetLanguageType)
        return targetType.upper() in [t.upper() for t in equivalent_types]
    
    @classmethod
    def getCypherCompatibleILVT(cls, ilvtType: ILVTType) -> ILVTType:
        """Get the Cypher-compatible ILVT type for a given ILVT type"""
        # Cypher has a limited type system - map all integer types to INT64
        if ilvtType in [ILVTType.INT8, ILVTType.INT16, ILVTType.INT32, ILVTType.UINT8, 
                       ILVTType.UINT16, ILVTType.UINT32, ILVTType.UINT64, ILVTType.INT128, ILVTType.INT256]:
            return ILVTType.INT64
        
        # Map all float types to FLOAT64
        if ilvtType in [ILVTType.FLOAT16, ILVTType.FLOAT32, ILVTType.DECIMAL]:
            return ILVTType.FLOAT64
        
        # Other types remain the same
        return ilvtType


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
    
    def getILVTType(self, languageType: LanguageTypes = LanguageTypes.GQL) -> ILVTType:
        """Get the corresponding ILVT type for this ValueType based on language type system"""
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
        
        # Adjust based on language type system capabilities
        if ilvt_type == ILVTType.JSON and languageType not in [LanguageTypes.JSON, LanguageTypes.DATABASE_JSON]:
            # JSON type is only available in JSON-based type systems
            return None
        
        return ilvt_type
    
    def validate(self, value: Any, languageType: LanguageTypes = LanguageTypes.GQL) -> ValidationResult:
        """Validate a value against this type with language type system awareness"""
        if value is None:
            return ValidationResult.failure(f"Value cannot be null for type {self.value}")
        
        # Get the ILVT type for validation
        ilvt_type = self.getILVTType(languageType)
        if ilvt_type is None:
            return ValidationResult.failure(f"No ILVT mapping for type {self.value} in {languageType.value}")
        
        # Dispatch to ILVT validation
        return self._validateILVTType(value, ilvt_type, languageType)
    
    def _validateILVTType(self, value: Any, ilvtType: ILVTType, languageType: LanguageTypes) -> ValidationResult:
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
        
        return validator(value, languageType)
    
    def _validateString(self, value: Any, languageType: LanguageTypes) -> ValidationResult:
        """Validate STRING type (ILVT string)"""
        if isinstance(value, str):
            return ValidationResult.success()
        
        # Language type system specific behavior
        if languageType == LanguageTypes.CYPHER:
            if isinstance(value, (int, float, bool)):
                return ValidationResult.failure(
                    f"Expected STRING, got {type(value).__name__} {repr(value)}. "
                    f"Cypher requires explicit string conversion."
                )
        else:
            # Other type systems are strict
            if isinstance(value, (int, float, bool)):
                return ValidationResult.failure(
                    f"Expected STRING, got {type(value).__name__}. "
                    f"Use explicit string conversion if intended."
                )
        
        return ValidationResult.failure(
            f"Expected STRING, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateInteger64(self, value: Any, languageType: LanguageTypes) -> ValidationResult:
        """Validate 64-bit INTEGER type (ILVT int64)"""
        if isinstance(value, int) and not isinstance(value, bool):
            # Check for 64-bit signed integer range
            if -9223372036854775808 <= value <= 9223372036854775807:
                return ValidationResult.success()
            else:
                return ValidationResult.failure(
                    f"Integer value {value} is outside the valid range "
                    f"[-9223372036854775808, 9223372036854775807]"
                )
        
        # Handle float-to-integer conversion based on language type system
        if isinstance(value, float):
            if value.is_integer() and not (math.isinf(value) or math.isnan(value)):
                int_value = int(value)
                if -9223372036854775808 <= int_value <= 9223372036854775807:
                    lang_name = languageType.value.title()
                    return ValidationResult.failure(
                        f"Expected INTEGER, got FLOAT {value}. "
                        f"{lang_name} requires explicit integer conversion."
                    )
            return ValidationResult.failure(
                f"Cannot convert FLOAT {value} to INTEGER: not a whole number"
            )
        
        return ValidationResult.failure(
            f"Expected INTEGER, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateFloat64(self, value: Any, languageType: LanguageTypes) -> ValidationResult:
        """Validate 64-bit FLOAT type (ILVT float64)"""
        if isinstance(value, float):
            # Check for valid float values (including NaN and Infinity)
            return ValidationResult.success()
        
        # Handle integer-to-float conversion based on language type system
        if isinstance(value, int) and not isinstance(value, bool):
            lang_name = languageType.value.title()
            return ValidationResult.failure(
                f"Expected FLOAT, got INTEGER {value}. "
                f"{lang_name} requires explicit float conversion."
            )
        
        return ValidationResult.failure(
            f"Expected FLOAT, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateBoolean(self, value: Any, languageType: LanguageTypes) -> ValidationResult:
        """Validate BOOLEAN type (ILVT boolean)"""
        if isinstance(value, bool):
            return ValidationResult.success()
        
        # All type systems are strict about boolean validation
        if isinstance(value, (int, str)):
            lang_name = languageType.value.upper()
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


# Utility functions for type validation with language type system support
def validateValue(value: Any, valueType: ValueType, languageType: LanguageTypes = LanguageTypes.GQL) -> ValidationResult:
    """Convenience function to validate a value against a type with language type system"""
    return valueType.validate(value, languageType)


def isValidValue(value: Any, valueType: ValueType, languageType: LanguageTypes = LanguageTypes.GQL) -> bool:
    """Convenience function to check if a value is valid for a type with language type system"""
    return valueType.validate(value, languageType).isValid


def getTypeForValue(value: Any, languageType: LanguageTypes = LanguageTypes.GQL) -> Optional[ValueType]:
    """Infer the most appropriate ValueType for a given value based on language type system"""
    # Use the precise ILVT inference, then map back to ValueType
    ilvt_type = LanguageTypeMapper.inferMostPreciseType(value, languageType)
    
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


def convertLegacyDatatype(datatype: str, languageType: LanguageTypes = LanguageTypes.GQL) -> Optional[ValueType]:
    """
    Convert legacy string datatypes to ValueType enum.
    
    This function provides backward compatibility for existing PropertyType usage
    that uses string datatypes like "STRING", "INTEGER", etc.
    """
    # First try to get ILVT type from the language-specific type name
    ilvt_type = LanguageTypeMapper.getILVTFromLanguageType(datatype, languageType)
    
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


def getLanguageTypeName(valueType: ValueType, languageType: LanguageTypes = LanguageTypes.GQL) -> Optional[str]:
    """Get the language-specific type name for a ValueType"""
    ilvt_type = valueType.getILVTType(languageType)
    if ilvt_type is None:
        return None
    
    return LanguageTypeMapper.getLanguageTypeFromILVT(ilvt_type, languageType)


def translateType(sourceType: str, sourceLanguageType: LanguageTypes, 
                 targetLanguageType: LanguageTypes) -> List[str]:
    """
    Translate a type from one language type system to another.
    
    Returns all equivalent types in the target language type system.
    For example: translateType("INTEGER", LanguageTypes.CYPHER, LanguageTypes.GQL) 
    might return ["INT64", "BIGINT"] and supertypes.
    """
    return LanguageTypeMapper.getEquivalentTypes(sourceType, sourceLanguageType, targetLanguageType)


def isTypeCompatible(sourceType: str, sourceLanguageType: LanguageTypes,
                    targetType: str, targetLanguageType: LanguageTypes) -> bool:
    """Check if a source type is compatible with a target type across language type systems"""
    return LanguageTypeMapper.isTypeCompatible(sourceType, sourceLanguageType, targetType, targetLanguageType)


def inferPreciseType(value: Any, languageType: LanguageTypes = LanguageTypes.GQL) -> Optional[str]:
    """
    Infer the most precise type name for a value at a given language type system.
    
    Examples:
    - inferPreciseType(128, LanguageTypes.GQL) -> "UINT8" (most precise)
    - inferPreciseType(128, LanguageTypes.CYPHER) -> "INTEGER" (Cypher only has INTEGER)
    """
    ilvt_type = LanguageTypeMapper.inferMostPreciseType(value, languageType)
    if ilvt_type is None:
        return None
    
    return LanguageTypeMapper.getLanguageTypeFromILVT(ilvt_type, languageType)