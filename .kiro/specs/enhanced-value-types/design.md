# Enhanced Value Types System Design

## Overview

This design document outlines the architecture for implementing a comprehensive value type system that extends the current property graph schema with robust type validation, constraints, and runtime validation capabilities. The design maintains backward compatibility while adding powerful new features for data integrity and validation.

## Architecture

### Core Components

```
Enhanced Value Types System
├── ValueType (Enum)
│   ├── Primitive Types (STRING, INTEGER, FLOAT, BOOLEAN)
│   ├── Temporal Types (DATE, TIME, DATETIME, DURATION)
│   └── Complex Types (JSON, ARRAY, MAP)
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
    ├── CoercionRules
    ├── CoercionResult
    └── CoercionConfig
```

## Components and Interfaces

### 1. ValueType Enumeration

```python
from enum import Enum
from typing import Any, Union, Optional
from abc import ABC, abstractmethod

class ValueType(Enum):
    # Primitive Types
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
    
    @abstractmethod
    def validate(self, value: Any) -> ValidationResult:
        """Validate a value against this type"""
        pass
    
    @abstractmethod
    def coerce(self, value: Any, config: CoercionConfig) -> CoercionResult:
        """Attempt to coerce a value to this type"""
        pass
```

### 2. Enhanced PropertyType

```python
from typing import List, Optional, Any, FrozenSet
from dataclasses import dataclass

@dataclass(frozen=True)
class EnhancedPropertyType:
    name: str
    valueType: ValueType
    constraints: FrozenSet[PropertyConstraint] = frozenset()
    elementType: Optional['EnhancedPropertyType'] = None  # For ARRAY types
    keyType: Optional['EnhancedPropertyType'] = None      # For MAP types
    valueTypeForMap: Optional['EnhancedPropertyType'] = None  # For MAP types
    
    def validate(self, value: Any, context: ValidationContext) -> ValidationResult:
        """Validate a value against this property type and all constraints"""
        pass
    
    def hasConstraint(self, constraintType: type) -> bool:
        """Check if this property has a specific constraint type"""
        pass
    
    def getConstraint(self, constraintType: type) -> Optional[PropertyConstraint]:
        """Get a specific constraint if it exists"""
        pass
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

### 5. Type Coercion System

```python
from enum import Enum
from typing import Any, Optional, Union
from dataclasses import dataclass

class CoercionMode(Enum):
    STRICT = "STRICT"      # No coercion allowed
    SAFE = "SAFE"          # Only safe coercions (no data loss)
    PERMISSIVE = "PERMISSIVE"  # Allow lossy coercions with warnings

@dataclass
class CoercionConfig:
    mode: CoercionMode = CoercionMode.SAFE
    dateFormats: List[str] = None
    numberFormats: List[str] = None
    booleanValues: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.dateFormats is None:
            self.dateFormats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
        if self.booleanValues is None:
            self.booleanValues = {
                "true": True, "false": False, "yes": True, "no": False,
                "1": True, "0": False, "on": True, "off": False
            }

@dataclass
class CoercionResult:
    success: bool
    value: Any = None
    warnings: List[str] = None
    originalValue: Any = None
    
    @classmethod
    def success(cls, value: Any, originalValue: Any = None, 
                warnings: List[str] = None) -> 'CoercionResult':
        return cls(success=True, value=value, originalValue=originalValue, 
                  warnings=warnings or [])
    
    @classmethod
    def failure(cls, originalValue: Any, reason: str) -> 'CoercionResult':
        return cls(success=False, originalValue=originalValue, 
                  warnings=[reason])

class TypeCoercion:
    """Handles type coercion between different value types"""
    
    def coerceValue(self, value: Any, targetType: ValueType, 
                   config: CoercionConfig) -> CoercionResult:
        """Attempt to coerce a value to the target type"""
        pass
    
    def canCoerce(self, fromType: ValueType, toType: ValueType, 
                 config: CoercionConfig) -> bool:
        """Check if coercion is possible between two types"""
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

### Builder Pattern Integration

```python
class PropertyTypeBuilder:
    def __init__(self):
        self._name: Optional[str] = None
        self._valueType: Optional[ValueType] = None
        self._constraints: List[PropertyConstraint] = []
        self._elementType: Optional[PropertyType] = None
        self._keyType: Optional[PropertyType] = None
        self._valueTypeForMap: Optional[PropertyType] = None
    
    def withName(self, name: str) -> 'PropertyTypeBuilder':
        return self._copy(name=name)
    
    def withValueType(self, valueType: ValueType) -> 'PropertyTypeBuilder':
        return self._copy(valueType=valueType)
    
    def withStringType(self) -> 'PropertyTypeBuilder':
        return self.withValueType(ValueType.STRING)
    
    def withIntegerType(self) -> 'PropertyTypeBuilder':
        return self.withValueType(ValueType.INTEGER)
    
    def withArrayType(self, elementType: PropertyType) -> 'PropertyTypeBuilder':
        return self._copy(valueType=ValueType.ARRAY, elementType=elementType)
    
    def withMapType(self, keyType: PropertyType, valueType: PropertyType) -> 'PropertyTypeBuilder':
        return self._copy(valueType=ValueType.MAP, keyType=keyType, 
                         valueTypeForMap=valueType)
    
    def addNotNullConstraint(self) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [NotNullConstraint()])
    
    def addDefaultValue(self, defaultValue: Any) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [DefaultValueConstraint(defaultValue)])
    
    def addUniqueConstraint(self, scope: UniqueScope = UniqueScope.GLOBAL) -> 'PropertyTypeBuilder':
        return self._copy(constraints=self._constraints + [UniqueConstraint(scope)])
    
    def buildPropertyType(self) -> PropertyType:
        if self._name is None:
            raise ValueError("Property name is required")
        if self._valueType is None:
            raise ValueError("Value type is required")
        
        return PropertyType(
            name=self._name,
            valueType=self._valueType,
            constraints=self._constraints,
            elementType=self._elementType,
            keyType=self._keyType,
            valueTypeForMap=self._valueTypeForMap
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