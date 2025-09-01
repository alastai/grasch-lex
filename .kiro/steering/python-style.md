# Python Coding Style Guide

Based on analysis of the grasch-main reference implementation, this document defines the coding style and patterns to be used throughout the Grasch project.

## Import Organization

```python
from __future__ import annotations

from typing import List, Set, FrozenSet, Tuple, Protocol
from abc import ABC, abstractmethod
from functools import total_ordering
from enum import Enum

from pydantic import BaseModel
from sortedcontainers import SortedDict, SortedSet

# Local imports last
from data_types import *
from grasch_exceptions import *
```

**Rules:**
- Always use `from __future__ import annotations` for forward references
- Group imports: standard library, third-party, local modules
- Use `from typing import` for type hints
- Local imports use `from module import *` pattern when appropriate
- Import order: future, typing, abc/functools, enum, external libraries, local modules

## Class Design Patterns

### Abstract Base Classes with Protocols

```python
@total_ordering
class OrderableABC(ReportableABC):
    class Relation(Enum):
        EQUAL = "EQUAL"
        LESS_THAN = "LESS_THAN"
        INCOMPARABLE = "INCOMPARABLE"

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass
```

### Nested Result Classes

```python
class AttributeType:
    class Compatible:
        def __init__(Compatible_self, name: str, firstDatatype: Datatype, ...):
            Compatible_self.__name = name
            Compatible_self.__firstDatatype = firstDatatype

        @property
        def name(Compatible_self) -> str:
            return Compatible_self.__name

    class Incompatible:
        def __init__(Incompatible_self, firstName: str, secondName: str, ...):
            Incompatible_self.__firstName = firstName
```

**Rules:**
- Use nested classes for result types (Compatible/Incompatible, Ordered/Unordered)
- Use `Compatible_self`/`Incompatible_self` parameter names in nested classes
- Private attributes with double underscore prefix
- Properties for all attribute access

### Inheritance and Composition

```python
@total_ordering
class ContentType(OrderableABC, ContentTypeInterface):
    def __init__(self, labels: LabelsRecordType = None, ...):
        if labels is None:
            labels = NO_LABELS
        self.__labels = labels

    @property
    def labels(self) -> LabelsRecordType:
        return self.__labels
```

**Rules:**
- Use `@total_ordering` decorator for comparable classes
- Multiple inheritance: ABC first, then interfaces/protocols
- Default parameter handling with explicit None checks
- Use module-level constants for defaults (NO_LABELS, NO_PROPERTY_TYPES)

## Naming Conventions

**CRITICAL: Use camelCase for method names, NOT snake_case**

```python
def compatibleWith(self, other: AttributeType) -> AttributeType.Compatible | AttributeType.Incompatible:
def orderAgainst(self, other: FlatRecordType) -> FlatRecordType.Ordered | FlatRecordType.Unordered:
def confirmDenyActualSupertype(potentialSupertype: FlatRecordType, potentialSubtype: FlatRecordType):
def attributeTypesWithDuplicateNames(attributeTypes: FrozenSet[AttributeType]) -> List[AttributeType]:
```

**Rules:**
- **Method names**: camelCase (compatibleWith, orderAgainst, NOT compatible_with, order_against)
- **Property names**: camelCase (attributeNames, singletonMemberName)
- **Variable names**: camelCase (potentialSupertype, leastCommonSupertype)
- **Class names**: PascalCase (ContentType, AttributeType)
- **Constants**: UPPER_CASE (NO_LABELS, BOOLEAN_PROPERTY_TYPE)

## Strong Typing Requirements

**CRITICAL: Every parameter, return value, and property must have explicit type hints**

```python
def __init__(Compatible_self, name: str, firstDatatype: Datatype, secondDatatype: Datatype, leastCommonSupertype: Datatype):
def orderRecordTypes(first: FlatRecordType, second: FlatRecordType) -> FlatRecordType.Ordered | FlatRecordType.Unordered:
@property
def attributeNames(self) -> SortedSet[str]:
def __init__(self, attributeTypes: FrozenSet[AttributeType]):
```

**Rules:**
- **All parameters**: Must have type hints
- **All return values**: Must have return type annotations
- **All properties**: Must have return type annotations
- **Complex types**: Use full generic syntax (SortedSet[str], FrozenSet[AttributeType])
- **Union types**: Use `|` syntax (str | None, Compatible | Incompatible)
- **Collections**: Always specify element types

## Method Implementation Patterns

### Magic Methods

```python
def __hash__(self):
    return hash((self.name, self.datatype))

def __eq__(self, other: AttributeType):
    return (self.name, self.datatype) == (other.name, other.datatype)

def __lt__(self, other: AttributeType):
    return False  # can never be ordered

def __str__(self):
    return f"{self.__class__.__name__}{': '}{(self.name, str(self.datatype))}"

def __repr__(self) -> object:
    return f"{self.__class__.__name__}(name={repr(self.name)}, datatype={repr(self.datatype)})"
```

**Rules:**
- Always implement `__hash__`, `__eq__`, `__lt__` for orderable classes
- Use tuple comparison for equality and ordering
- `__str__` uses class name with colon separator and readable format
- `__repr__` uses constructor-like format with `repr()` for nested values
- Type hints on magic methods where appropriate

### Property Patterns

```python
@property
def datatype(self) -> Datatype:
    return self.__datatype

@property
def isEmpty(self) -> bool:
    return True if 0 == len(self) else False

@property
def singletonMemberName(self) -> str | None:
    return self.attributeNames[0] if self.isSingleton else None
```

**Rules:**
- Use `@property` decorator for all attribute access
- Return type hints on all properties
- Use `| None` union syntax for optional returns
- Descriptive property names (isEmpty, isSingleton, singletonMemberName)

## Error Handling

```python
class GraphSchemaError(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)

class GraphSchemaTypeInitError(GraphSchemaError):
    def __init__(self, typeClassName: str, reason: str):
        super().__init__(reason)
        self.__typeClassName = typeClassName

    def __str__(self):
        return f"Failed to initialize type {self.typeClassName}: {super().__str__()}"
```

**Rules:**
- Custom exception hierarchy inheriting from base project exception
- Store additional context in exception classes
- Override `__str__` for better error messages
- Use descriptive exception names ending in "Error"

## Type System Patterns

### Enum Definitions

```python
class AtomicPropertyDatatypeEnum(AtomicDatatypeEnum, Enum):
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    INTEGER = "INTEGER"
```

### Constant Definitions

```python
LABEL = LabelDatatype()
BOOLEAN: Datatype = Datatype(BOOLEAN_PROPERTY_TYPE)
STRING: Datatype = Datatype(STRING_PROPERTY_TYPE)

NO_LABELS = LabelsRecordType([])
NO_PROPERTY_TYPES = FlatPropertyTypes(set())
```

**Rules:**
- Module-level constants in UPPER_CASE
- Type-annotated constants where helpful
- Singleton instances for common types
- Default empty instances (NO_LABELS, NO_PROPERTY_TYPES)

## Validation and Initialization

```python
def __init__(self, contentType: ContentType):
    if contentType is None:
        raise GraphSchemaTypeInitError(self.__class__.__name__, "No content type specified")
    self.__contentType = contentType
```

**Rules:**
- Explicit None checks with descriptive error messages
- Use class-specific exceptions with `self.__class__.__name__`
- Validate parameters before assignment
- Store validated parameters in private attributes

## Method Organization

```python
class ContentType:
    def __init__(self, ...):
        # Initialization
    
    def __hash__(self):
        # Magic methods
    
    def __eq__(self, other):
        # Magic methods
    
    @property
    def labels(self):
        # Properties
    
    def compatibleWith(self, other):
        # Public methods
    
    @staticmethod
    def confirmDenyActualSupertype(potential_supertype, potential_subtype):
        # Static methods
```

**Rules:**
- Order: `__init__`, magic methods, properties, public methods, static methods
- Group related functionality together
- Use descriptive method names
- Static methods for utility functions that don't need instance state

## Documentation and Comments

```python
def orderAgainst(self, other: FlatRecordType) -> FlatRecordType.Ordered | FlatRecordType.Unordered:
    # The comparison of two Records S and T must observe these rules:
    # If T.names includes S.names then T is potentially higher than S...
    
    # TODO sort out the orderability reporting
    # @abstractmethod
    # def hasOrder(self) -> [Orderable.Order]:
```

**Rules:**
- Use `# TODO` comments for future work
- Explain complex algorithms with multi-line comments
- Document business rules and constraints
- Use type hints as primary documentation

## String Formatting

```python
def __str__(self):
    return f"{self.__class__.__name__}{': '}{(self.name, str(self.datatype))}"

def __repr__(self):
    return f"{self.__class__.__name__}(name={repr(self.name)}, datatype={repr(self.datatype)})"
```

**Rules:**
- Use f-strings for all string formatting
- `__str__`: readable format with class name and colon
- `__repr__`: constructor-like format
- Use `repr()` for nested object representation in `__repr__`

## Collection Handling

```python
from sortedcontainers import SortedDict, SortedSet

class FlatRecordType(RecordTypeABC, SortedDict[str, Datatype]):
    def __init__(self, attributeTypes: FrozenSet[AttributeType]):
        SortedDict.__init__(self, 
            ((attributeType.name, attributeType.datatype) for attributeType in attributeTypes))

@property
def attributeNames(self) -> SortedSet[str]:
    return SortedSet(self.keys())
```

**Rules:**
- Use `sortedcontainers` for ordered collections
- Prefer `FrozenSet` for immutable collections in constructors
- Use generator expressions in collection constructors
- Type hint collection contents: `SortedSet[str]`, `FrozenSet[AttributeType]`