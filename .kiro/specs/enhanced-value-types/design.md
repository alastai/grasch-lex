# Enhanced Value Types System Design

## Overview

This design document outlines the architecture for implementing the Intermediate Language Value Types (ILVT) system as defined in the property-graph-schema specification. The system provides universal type mapping and validation capabilities for interoperability between GQL, SQL Foundation, JSON Schema extensions, and future type systems. The design maintains backward compatibility while implementing the complete ILVT type registry and cross-language mapping capabilities.

## Architecture

### Core Components

```
ILVT-Based Value Types System
├── ILVTType (Enum)
│   ├── Boolean Types (boolean)
│   ├── Integer Types (int8, int16, int32, int64, int128, int256, uint8, uint16, uint32, uint64, uint128, uint256)
│   ├── Decimal Types (decimal, numeric)
│   ├── Floating Point Types (float16, float32, float64, float128, float256, decfloat32, decfloat64, decfloat128)
│   ├── String Types (string, char)
│   ├── Binary Types (bytes, binary)
│   ├── Temporal Types (date, time, time_tz, datetime, datetime_tz, duration)
│   ├── Structured Types (record, array, multiset)
│   └── Special Types (json, vector, null)
├── LanguageTypeMapper
│   ├── GQLTypeMapper
│   ├── SQLTypeMapper
│   ├── CypherTypeMapper
│   └── JSONSchemaMapper
├── PropertyConstraint (Abstract Base)
│   ├── NotNullConstraint
│   ├── DefaultValueConstraint
│   ├── UniqueConstraint
│   └── CustomConstraint
├── ValidationEngine
│   ├── PropertyValidator
│   ├── GraphValidator
│   └── ValidationResult
└── TypeCoercion
    ├── LanguageLevelAdapter
    ├── CoercionRules
    ├── CoercionResult
    └── CoercionConfig
```

## Components and Interfaces

### 1. ILVT Type Registry

```python
from enum import Enum
from typing import Any, Union, Optional, Dict, List
from abc import ABC, abstractmethod
from dataclasses import dataclass

class ILVTType(Enum):
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
    
    def getValueRange(self) -> Optional[tuple]:
        """Get the valid value range for this type"""
        ranges = {
            ILVTType.INT8: (-128, 127),
            ILVTType.INT16: (-32768, 32767),
            ILVTType.INT32: (-2147483648, 2147483647),
            ILVTType.INT64: (-9223372036854775808, 9223372036854775807),
            ILVTType.UINT8: (0, 255),
            ILVTType.UINT16: (0, 65535),
            ILVTType.UINT32: (0, 4294967295),
            ILVTType.UINT64: (0, 18446744073709551615),
            ILVTType.FLOAT16: (-65504, 65504),
        }
        return ranges.get(self)
    
    def getCategory(self) -> str:
        """Get the category this type belongs to"""
        categories = {
            ILVTType.BOOLEAN: "Logical",
            ILVTType.INT8: "Signed Integer", ILVTType.INT16: "Signed Integer", 
            ILVTType.INT32: "Signed Integer", ILVTType.INT64: "Signed Integer",
            ILVTType.INT128: "Extended Integer", ILVTType.INT256: "Extended Integer",
            ILVTType.UINT8: "Unsigned Integer", ILVTType.UINT16: "Unsigned Integer",
            ILVTType.UINT32: "Unsigned Integer", ILVTType.UINT64: "Unsigned Integer",
            ILVTType.UINT128: "Extended Integer", ILVTType.UINT256: "Extended Integer",
            ILVTType.DECIMAL: "Exact Numeric", ILVTType.NUMERIC: "Exact Numeric",
            ILVTType.FLOAT32: "Binary Float", ILVTType.FLOAT64: "Binary Float",
            ILVTType.STRING: "Character String", ILVTType.CHAR: "Character String",
            ILVTType.DATE: "Date/Time", ILVTType.TIME: "Date/Time",
            ILVTType.ARRAY: "Collection", ILVTType.RECORD: "Structured",
            ILVTType.JSON: "Semi-Structured", ILVTType.VECTOR: "Numeric Array"
        }
        return categories.get(self, "Unknown")
```

### 2. Language Type Mapper

```python
from typing import List, Optional, Any, Dict, Set
from dataclasses import dataclass
from enum import Enum

class LanguageTypes(Enum):
    GQL = "GQL"
    SQL_FOUNDATION = "SQL_FOUNDATION"
    CYPHER = "CYPHER"
    JSON = "JSON"
    DATABASE_JSON = "DATABASE_JSON"

@dataclass
class TypeMapping:
    ilvtType: ILVTType
    gqlType: Optional[str]
    sqlType: Optional[str]
    cypherType: Optional[str]
    jsonSchemaType: Dict[str, Any]

class LanguageTypeMapper:
    """Handles bidirectional type mappings between different type systems"""
    
    def __init__(self):
        self._mappings = self._initializeMappings()
    
    def _initializeMappings(self) -> Dict[ILVTType, TypeMapping]:
        """Initialize the complete ILVT mapping table"""
        return {
            ILVTType.BOOLEAN: TypeMapping(
                ilvtType=ILVTType.BOOLEAN,
                gqlType="BOOLEAN",
                sqlType="BOOLEAN", 
                cypherType="BOOLEAN",
                jsonSchemaType={
                    "data.boolean": {"type": "boolean"},
                    "gql.boolean": "BOOLEAN",
                    "sql.boolean": "BOOLEAN"
                }
            ),
            ILVTType.INT8: TypeMapping(
                ilvtType=ILVTType.INT8,
                gqlType="INT8",
                sqlType=None,  # No SQL equivalent
                cypherType=None,  # No Cypher equivalent
                jsonSchemaType={
                    "data.int8": {"type": "integer", "minimum": -128, "maximum": 127},
                    "gql.int8": "INT8",
                    "sql.int8": "undefined"
                }
            ),
            ILVTType.VECTOR: TypeMapping(
                ilvtType=ILVTType.VECTOR,
                gqlType="VECTOR",
                sqlType="VECTOR",
                cypherType=None,  # No Cypher equivalent
                jsonSchemaType={
                    "data.vector": {
                        "type": "array",
                        "items": {"type": "number"},
                        "dimension": {"type": "integer", "minimum": 1},
                        "elementType": {"type": "string", "enum": ["float32", "float64", "int32", "int64"]}
                    },
                    "gql.vector": "VECTOR",
                    "sql.vector": "VECTOR"
                }
            )
            # ... complete mapping table for all ILVT types
        }
    
    def getEquivalentTypes(self, sourceType: str, sourceLanguage: LanguageTypes, 
                          targetLanguage: LanguageTypes) -> List[str]:
        """Get equivalent types in target language"""
        pass
    
    def getILVTType(self, languageType: str, language: LanguageTypes) -> Optional[ILVTType]:
        """Convert language-specific type to ILVT type"""
        pass
    
    def getLanguageType(self, ilvtType: ILVTType, targetLanguage: LanguageTypes) -> Optional[str]:
        """Convert ILVT type to language-specific type"""
        pass
    
    def generateJSONSchema(self, ilvtType: ILVTType) -> Dict[str, Any]:
        """Generate JSON Schema definition for an ILVT type"""
        pass

### 3. Enhanced PropertyType with ILVT Integration

@dataclass(frozen=True)
class EnhancedPropertyType:
    name: str
    ilvtType: ILVTType
    constraints: FrozenSet[PropertyConstraint] = frozenset()
    parameters: Dict[str, Any] = None  # For parameterized types (precision, scale, length, dimension)
    elementType: Optional['EnhancedPropertyType'] = None  # For ARRAY types
    keyType: Optional['EnhancedPropertyType'] = None      # For RECORD key types
    valueTypeForRecord: Optional['EnhancedPropertyType'] = None  # For RECORD value types
    
    def __post_init__(self):
        if self.parameters is None:
            object.__setattr__(self, 'parameters', {})
    
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate a value against this property type and all constraints"""
        pass
    
    def getLanguageType(self, language: LanguageTypes) -> Optional[str]:
        """Get the equivalent type in a specific language"""
        mapper = LanguageTypeMapper()
        return mapper.getLanguageType(self.ilvtType, language)
    
    def generateJSONSchema(self) -> Dict[str, Any]:
        """Generate JSON Schema definition for this property type"""
        mapper = LanguageTypeMapper()
        return mapper.generateJSONSchema(self.ilvtType)
```

### 3. Property Constraints

```python
from abc import ABC, abstractmethod
from typing import Any, Optional

class PropertyConstraint(ABC):
    """Base class for all property constraints"""
    
    @abstractmethod
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate the constraint against a value"""
        pass
    
    @abstractmethod
    def getDescription(self) -> str:
        """Get a human-readable description of this constraint"""
        pass

class NotNullConstraint(PropertyConstraint):
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        if value is None:
            return ValidationResult.failure(f"Value cannot be null")
        return ValidationResult.success()
    
    def getDescription(self) -> str:
        return "NOT NULL"

class DefaultValueConstraint(PropertyConstraint):
    def __init__(self, defaultValue: Any):
        self.defaultValue = defaultValue
    
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        # Default constraints don't validate, they provide values
        return ValidationResult.success()
    
    def getDefaultValue(self) -> Any:
        return self.defaultValue
    
    def getDescription(self) -> str:
        return f"DEFAULT {self.defaultValue}"

class UniqueConstraint(PropertyConstraint):
    def __init__(self, scope: UniqueScope = UniqueScope.GLOBAL):
        self.scope = scope
    
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        # Uniqueness validation requires access to existing data
        # Implementation depends on the validation context
        pass
    
    def getDescription(self) -> str:
        return f"UNIQUE ({self.scope.value})"
```

### 4. Validation Engine

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    isValid: bool
    errors: List[ValidationError] = None
    warnings: List[ValidationWarning] = None
    
    @classmethod
    def success(cls) -> 'ValidationResult':
        return cls(isValid=True, errors=[], warnings=[])
    
    @classmethod
    def failure(cls, error: str, path: str = "") -> 'ValidationResult':
        return cls(isValid=False, errors=[ValidationError(error, path)])
    
    def combine(self, other: 'ValidationResult') -> 'ValidationResult':
        """Combine two validation results"""
        pass

@dataclass
class ValidationError:
    message: str
    path: str
    expectedType: Optional[str] = None
    actualValue: Optional[Any] = None
    constraint: Optional[str] = None

class PropertyValidator:
    """Validates individual properties against their types and constraints"""
    
    def validateProperty(self, value: Any, propertyType: EnhancedPropertyType, 
                        context: ValidationContext) -> ValidationResult:
        """Validate a single property value"""
        pass
    
    def validateWithCoercion(self, value: Any, propertyType: EnhancedPropertyType,
                           coercionConfig: CoercionConfig,
                           context: ValidationContext) -> ValidationResult:
        """Validate with optional type coercion"""
        pass

class GraphValidator:
    """Validates complete graphs against schemas"""
    
    def validateGraph(self, graphData: Any, graphType: GraphType,
                     config: ValidationConfig) -> ValidationResult:
        """Validate an entire graph against its schema"""
        pass
    
    def validateNode(self, nodeData: Any, nodeType: NodeType,
                    context: ValidationContext) -> ValidationResult:
        """Validate a single node"""
        pass
    
    def validateEdge(self, edgeData: Any, edgeType: EdgeType,
                    context: ValidationContext) -> ValidationResult:
        """Validate a single edge"""
        pass
```

### 5. Language Level Adaptation and Type Coercion

```python
from enum import Enum
from typing import Any, Optional, Union, Dict, List
from dataclasses import dataclass

class LanguageLevel(Enum):
    GQL = "GQL"           # Full ILVT type system with precise mappings
    LEX = "LEX"           # Cypher-compatible subset with relaxed constraints

class CoercionMode(Enum):
    STRICT = "STRICT"      # No coercion allowed
    SAFE = "SAFE"          # Only safe coercions (no data loss)
    PERMISSIVE = "PERMISSIVE"  # Allow lossy coercions with warnings

@dataclass
class CoercionConfig:
    mode: CoercionMode = CoercionMode.SAFE
    languageLevel: LanguageLevel = LanguageLevel.GQL
    dateFormats: List[str] = None
    numberFormats: List[str] = None
    booleanValues: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.dateFormats is None:
            self.dateFormats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"]
        if self.booleanValues is None:
            self.booleanValues = {
                "true": True, "false": False, "yes": True, "no": False,
                "1": True, "0": False, "on": True, "off": False
            }

class LanguageLevelAdapter:
    """Adapts types based on language level capabilities"""
    
    def adaptType(self, ilvtType: ILVTType, targetLevel: LanguageLevel) -> ILVTType:
        """Adapt an ILVT type to the target language level"""
        if targetLevel == LanguageLevel.LEX:
            # Map to Cypher-compatible subset
            integer_types = {ILVTType.INT8, ILVTType.INT16, ILVTType.INT32, 
                           ILVTType.INT64, ILVTType.INT128, ILVTType.INT256,
                           ILVTType.UINT8, ILVTType.UINT16, ILVTType.UINT32, 
                           ILVTType.UINT64, ILVTType.UINT128, ILVTType.UINT256}
            float_types = {ILVTType.FLOAT16, ILVTType.FLOAT32, ILVTType.FLOAT64,
                          ILVTType.FLOAT128, ILVTType.FLOAT256, ILVTType.DECFLOAT32,
                          ILVTType.DECFLOAT64, ILVTType.DECFLOAT128, ILVTType.DECIMAL, ILVTType.NUMERIC}
            
            if ilvtType in integer_types:
                return ILVTType.INT64  # Cypher INTEGER
            elif ilvtType in float_types:
                return ILVTType.FLOAT64  # Cypher FLOAT
            elif ilvtType in {ILVTType.CHAR}:
                return ILVTType.STRING  # Cypher STRING
            elif ilvtType == ILVTType.MULTISET:
                return ILVTType.ARRAY  # Cypher LIST
        
        return ilvtType  # No adaptation needed for GQL level
    
    def supportsHeterogeneousCollections(self, level: LanguageLevel) -> bool:
        """Check if language level supports heterogeneous collections"""
        return level == LanguageLevel.LEX  # Cypher allows mixed-type lists

class TypeCoercion:
    """Handles type coercion between different ILVT types"""
    
    def __init__(self):
        self.adapter = LanguageLevelAdapter()
        self.mapper = LanguageTypeMapper()
    
    def coerceValue(self, value: Any, targetType: ILVTType, 
                   config: CoercionConfig) -> CoercionResult:
        """Attempt to coerce a value to the target ILVT type"""
        # Apply language level adaptation first
        adaptedType = self.adapter.adaptType(targetType, config.languageLevel)
        
        # Perform type-specific coercion
        if adaptedType == ILVTType.BOOLEAN:
            return self._coerceToBoolean(value, config)
        elif adaptedType in {ILVTType.INT8, ILVTType.INT16, ILVTType.INT32, ILVTType.INT64}:
            return self._coerceToInteger(value, adaptedType, config)
        elif adaptedType in {ILVTType.FLOAT32, ILVTType.FLOAT64}:
            return self._coerceToFloat(value, adaptedType, config)
        elif adaptedType == ILVTType.STRING:
            return self._coerceToString(value, config)
        elif adaptedType == ILVTType.DATE:
            return self._coerceToDate(value, config)
        # ... additional type-specific coercion methods
        
        return CoercionResult.failure(value, f"No coercion available for {adaptedType}")
    
    def _coerceToBoolean(self, value: Any, config: CoercionConfig) -> CoercionResult:
        """Coerce value to boolean using configured boolean values"""
        if isinstance(value, bool):
            return CoercionResult.success(value, value)
        elif isinstance(value, str):
            lower_val = value.lower()
            if lower_val in config.booleanValues:
                return CoercionResult.success(config.booleanValues[lower_val], value)
        elif isinstance(value, (int, float)):
            if config.mode != CoercionMode.STRICT:
                return CoercionResult.success(bool(value), value, 
                                            ["Numeric to boolean coercion"])
        
        return CoercionResult.failure(value, f"Cannot coerce {type(value)} to boolean")
    
    def canCoerce(self, fromType: ILVTType, toType: ILVTType, 
                 config: CoercionConfig) -> bool:
        """Check if coercion is possible between two ILVT types"""
        pass
```

## Data Models

### Enhanced PropertyType Integration

The enhanced PropertyType will extend the existing PropertyType class while maintaining backward compatibility:

```python
# Backward compatible extension
class PropertyType:
    def __init__(self, name: str, datatype: Union[str, ValueType] = None, 
                 valueType: ValueType = None, constraints: List[PropertyConstraint] = None):
        # Support both old datatype parameter and new valueType parameter
        if valueType is None and datatype is not None:
            # Convert old string datatype to ValueType
            valueType = self._convertDatatypeToValueType(datatype)
        
        self._name = name
        self._valueType = valueType or ValueType.STRING
        self._constraints = frozenset(constraints or [])
    
    # Maintain existing API
    @property
    def datatype(self) -> str:
        """Legacy property for backward compatibility"""
        return self._valueType.value
    
    # New enhanced API
    @property
    def valueType(self) -> ValueType:
        return self._valueType
    
    @property
    def constraints(self) -> FrozenSet[PropertyConstraint]:
        return self._constraints
```

### Builder Pattern Integration with ILVT

```python
class PropertyTypeBuilder:
    def __init__(self):
        self._name: Optional[str] = None
        self._ilvtType: Optional[ILVTType] = None
        self._constraints: List[PropertyConstraint] = []
        self._parameters: Dict[str, Any] = {}
        self._elementType: Optional[EnhancedPropertyType] = None
        self._keyType: Optional[EnhancedPropertyType] = None
        self._valueTypeForRecord: Optional[EnhancedPropertyType] = None
    
    def withName(self, name: str) -> 'PropertyTypeBuilder':
        return self._copy(name=name)
    
    def withILVTType(self, ilvtType: ILVTType) -> 'PropertyTypeBuilder':
        return self._copy(ilvtType=ilvtType)
    
    # Boolean Types
    def withBooleanType(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.BOOLEAN)
    
    # Integer Types
    def withInt8Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.INT8)
    
    def withInt16Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.INT16)
    
    def withInt32Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.INT32)
    
    def withInt64Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.INT64)
    
    def withUInt8Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.UINT8)
    
    def withUInt16Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.UINT16)
    
    def withUInt32Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.UINT32)
    
    def withUInt64Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.UINT64)
    
    # Floating Point Types
    def withFloat32Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.FLOAT32)
    
    def withFloat64Type(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.FLOAT64)
    
    def withDecimalType(self, precision: int = None, scale: int = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if precision is not None:
            parameters['precision'] = precision
        if scale is not None:
            parameters['scale'] = scale
        return self._copy(ilvtType=ILVTType.DECIMAL, parameters=parameters)
    
    # String Types
    def withStringType(self, maxLength: int = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if maxLength is not None:
            parameters['max_length'] = maxLength
        return self._copy(ilvtType=ILVTType.STRING, parameters=parameters)
    
    def withCharType(self, length: int) -> 'PropertyTypeBuilder':
        return self._copy(ilvtType=ILVTType.CHAR, parameters={'length': length})
    
    # Temporal Types
    def withDateType(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.DATE)
    
    def withTimeType(self, precision: int = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if precision is not None:
            parameters['precision'] = precision
        return self._copy(ilvtType=ILVTType.TIME, parameters=parameters)
    
    def withDateTimeType(self, precision: int = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if precision is not None:
            parameters['precision'] = precision
        return self._copy(ilvtType=ILVTType.DATETIME, parameters=parameters)
    
    def withDurationType(self, fields: List[str] = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if fields is not None:
            parameters['fields'] = fields
        return self._copy(ilvtType=ILVTType.DURATION, parameters=parameters)
    
    # Structured Types
    def withArrayType(self, elementType: EnhancedPropertyType, maxCardinality: int = None) -> 'PropertyTypeBuilder':
        parameters = {}
        if maxCardinality is not None:
            parameters['max_cardinality'] = maxCardinality
        return self._copy(ilvtType=ILVTType.ARRAY, elementType=elementType, parameters=parameters)
    
    def withRecordType(self, fields: Dict[str, EnhancedPropertyType]) -> 'PropertyTypeBuilder':
        return self._copy(ilvtType=ILVTType.RECORD, parameters={'fields': fields})
    
    def withVectorType(self, dimension: int, elementType: ILVTType = ILVTType.FLOAT32) -> 'PropertyTypeBuilder':
        parameters = {'dimension': dimension, 'element_type': elementType.value}
        return self._copy(ilvtType=ILVTType.VECTOR, parameters=parameters)
    
    # Special Types
    def withJSONType(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.JSON)
    
    def withNullType(self) -> 'PropertyTypeBuilder':
        return self.withILVTType(ILVTType.NULL)
    
    # Constraints
    def addNotNullConstraint(self) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [NotNullConstraint()])
    
    def addDefaultValue(self, defaultValue: Any) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [DefaultValueConstraint(defaultValue)])
    
    def addUniqueConstraint(self, scope: UniqueScope = UniqueScope.GLOBAL) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [UniqueConstraint(scope)])
    
    # Backward Compatibility Methods
    def withValueType(self, valueType: Union[str, ILVTType]) -> 'PropertyTypeBuilder':
        """Backward compatibility method for legacy string-based types"""
        if isinstance(valueType, str):
            # Convert legacy string types to ILVT types
            legacy_mapping = {
                "STRING": ILVTType.STRING,
                "INTEGER": ILVTType.INT32,
                "FLOAT": ILVTType.FLOAT64,
                "BOOLEAN": ILVTType.BOOLEAN,
                "DATE": ILVTType.DATE,
                "TIME": ILVTType.TIME,
                "DATETIME": ILVTType.DATETIME,
                "JSON": ILVTType.JSON,
                "ARRAY": ILVTType.ARRAY
            }
            ilvtType = legacy_mapping.get(valueType.upper())
            if ilvtType is None:
                raise ValueError(f"Unknown legacy type: {valueType}")
            return self.withILVTType(ilvtType)
        else:
            return self.withILVTType(valueType)
    
    def buildPropertyType(self) -> EnhancedPropertyType:
        if self._name is None:
            raise ValueError("Property name is required")
        if self._ilvtType is None:
            raise ValueError("ILVT type is required")
        
        return EnhancedPropertyType(
            name=self._name,
            ilvtType=self._ilvtType,
            constraints=frozenset(self._constraints),
            parameters=self._parameters,
            elementType=self._elementType,
            keyType=self._keyType,
            valueTypeForRecord=self._valueTypeForRecord
        )
```

## Error Handling

### Validation Error Hierarchy

```python
class ValidationError(Exception):
    def __init__(self, message: str, path: str = "", 
                 expectedType: str = None, actualValue: Any = None):
        super().__init__(message)
        self.path = path
        self.expectedType = expectedType
        self.actualValue = actualValue

class TypeValidationError(ValidationError):
    """Raised when a value doesn't match its expected type"""
    pass

class ConstraintValidationError(ValidationError):
    """Raised when a value violates a constraint"""
    def __init__(self, message: str, constraint: PropertyConstraint, **kwargs):
        super().__init__(message, **kwargs)
        self.constraint = constraint

class CoercionError(ValidationError):
    """Raised when type coercion fails"""
    def __init__(self, message: str, fromType: ValueType, toType: ValueType, **kwargs):
        super().__init__(message, **kwargs)
        self.fromType = fromType
        self.toType = toType
```

## Testing Strategy

### Unit Testing Approach

1. **Value Type Validation Tests**
   - Test each ValueType enum member with valid and invalid inputs
   - Test edge cases (null, empty, boundary values)
   - Test type-specific validation rules

2. **Constraint Testing**
   - Test each constraint type independently
   - Test constraint combinations
   - Test constraint violation reporting

3. **Coercion Testing**
   - Test successful coercions between compatible types
   - Test coercion failures with appropriate error messages
   - Test coercion configuration options

4. **Integration Testing**
   - Test complete validation workflows
   - Test performance with large datasets
   - Test backward compatibility with existing schemas

### Performance Testing

1. **Validation Performance**
   - Benchmark individual property validation (<1ms target)
   - Benchmark graph validation with various sizes
   - Memory usage profiling for streaming validation

2. **Coercion Performance**
   - Benchmark type coercion operations
   - Test caching effectiveness
   - Profile memory allocation patterns

## Migration Strategy

### Backward Compatibility

1. **Existing PropertyType Support**
   - Maintain all existing constructor signatures
   - Provide automatic migration from string datatypes to ValueType enums
   - Preserve all existing method signatures and return types

2. **Deprecation Path**
   - Mark old string-based datatype methods as deprecated
   - Provide clear migration guidance in deprecation warnings
   - Maintain deprecated methods for at least two major versions

3. **Schema Migration**
   - Automatic detection and migration of legacy schemas
   - Optional validation to ensure migration correctness
   - Rollback capabilities for failed migrations

## Performance Considerations

### Optimization Strategies

1. **Validation Caching**
   - Cache validation results for identical inputs
   - Use weak references to avoid memory leaks
   - Implement cache eviction policies

2. **Lazy Evaluation**
   - Defer expensive validations until required
   - Use generators for streaming validation
   - Implement short-circuit evaluation for constraint checking

3. **Parallel Processing**
   - Support parallel validation of independent graph elements
   - Use thread pools for CPU-intensive validation
   - Implement work-stealing for load balancing

### Memory Management

1. **Immutable Design**
   - Use immutable data structures to enable safe sharing
   - Implement copy-on-write for builder patterns
   - Use flyweight pattern for common constraint instances

2. **Streaming Support**
   - Support validation of data streams without loading entire datasets
   - Implement incremental validation for large graphs
   - Use iterators and generators to minimize memory footprint