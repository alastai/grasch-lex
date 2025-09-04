"""
Enhanced value type system for property graph schema validation.

This module provides comprehensive type validation for GQL primitive types,
temporal types, and complex types with configurable validation rules.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Union, Optional, List, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
import json
from datetime import datetime, date, time
import math


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


class ValueType(Enum):
    """Enumeration of all supported value types with validation methods"""
    
    # Primitive Types
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    
    # Temporal Types (to be implemented in Task 1.2)
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    DURATION = "DURATION"
    
    # Complex Types (to be implemented in Task 1.3)
    JSON = "JSON"
    ARRAY = "ARRAY"
    MAP = "MAP"
    
    def validate(self, value: Any) -> ValidationResult:
        """Validate a value against this type"""
        if value is None:
            return ValidationResult.failure(f"Value cannot be null for type {self.value}")
        
        # Dispatch to specific validation method
        validator_map = {
            ValueType.STRING: self._validateString,
            ValueType.INTEGER: self._validateInteger,
            ValueType.FLOAT: self._validateFloat,
            ValueType.BOOLEAN: self._validateBoolean,
            # Temporal and complex types will be added in later tasks
        }
        
        validator = validator_map.get(self)
        if validator is None:
            return ValidationResult.failure(f"Validation not yet implemented for type {self.value}")
        
        return validator(value)
    
    def _validateString(self, value: Any) -> ValidationResult:
        """Validate STRING type"""
        if isinstance(value, str):
            return ValidationResult.success()
        
        # Check if it's a type that can be reasonably converted to string
        if isinstance(value, (int, float, bool)):
            return ValidationResult.failure(
                f"Expected STRING, got {type(value).__name__}. "
                f"Use explicit string conversion if intended."
            )
        
        return ValidationResult.failure(
            f"Expected STRING, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateInteger(self, value: Any) -> ValidationResult:
        """Validate INTEGER type"""
        if isinstance(value, int) and not isinstance(value, bool):
            # Check for integer overflow (GQL integers are 64-bit signed)
            if -9223372036854775808 <= value <= 9223372036854775807:
                return ValidationResult.success()
            else:
                return ValidationResult.failure(
                    f"Integer value {value} is outside the valid range "
                    f"[-9223372036854775808, 9223372036854775807]"
                )
        
        if isinstance(value, float):
            if value.is_integer() and not (math.isinf(value) or math.isnan(value)):
                int_value = int(value)
                if -9223372036854775808 <= int_value <= 9223372036854775807:
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
    
    def _validateFloat(self, value: Any) -> ValidationResult:
        """Validate FLOAT type"""
        if isinstance(value, float):
            # Check for valid float values (including NaN and Infinity)
            return ValidationResult.success()
        
        if isinstance(value, int) and not isinstance(value, bool):
            return ValidationResult.failure(
                f"Expected FLOAT, got INTEGER {value}. "
                f"Use explicit float conversion if intended."
            )
        
        return ValidationResult.failure(
            f"Expected FLOAT, got {type(value).__name__}: {repr(value)}"
        )
    
    def _validateBoolean(self, value: Any) -> ValidationResult:
        """Validate BOOLEAN type"""
        if isinstance(value, bool):
            return ValidationResult.success()
        
        # Be strict about boolean validation - no automatic conversion
        if isinstance(value, (int, str)):
            return ValidationResult.failure(
                f"Expected BOOLEAN, got {type(value).__name__} {repr(value)}. "
                f"Use explicit boolean conversion if intended."
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


# Utility functions for type validation
def validateValue(value: Any, valueType: ValueType) -> ValidationResult:
    """Convenience function to validate a value against a type"""
    return valueType.validate(value)


def isValidValue(value: Any, valueType: ValueType) -> bool:
    """Convenience function to check if a value is valid for a type"""
    return valueType.validate(value).isValid


def getTypeForValue(value: Any) -> Optional[ValueType]:
    """Infer the most appropriate ValueType for a given value"""
    if value is None:
        return None
    
    if isinstance(value, bool):
        return ValueType.BOOLEAN
    elif isinstance(value, int):
        return ValueType.INTEGER
    elif isinstance(value, float):
        return ValueType.FLOAT
    elif isinstance(value, str):
        return ValueType.STRING
    elif isinstance(value, (list, tuple)):
        return ValueType.ARRAY
    elif isinstance(value, dict):
        return ValueType.MAP
    else:
        # For other types, try JSON serialization
        try:
            json.dumps(value)
            return ValueType.JSON
        except (TypeError, ValueError):
            return None