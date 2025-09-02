# Intermediate Language Value Types (ILVT) Specification

**Version**: 1.0  
**Date**: 2025-08-22  
**Purpose**: Universal type mapping system for interoperability between GQL, SQL Foundation, JSON Schema extensions, and future type systems.

## Architecture Overview

The ILVT system creates a union of all supported value types from different systems and provides bidirectional mappings through a centralized intermediate representation:

```
┌─────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│ GQL Property│◄──►│ Intermediate        │◄──►│ SQL Foundation  │
│ Value Types │    │ Language Value      │    │ Data Types      │
└─────────────┘    │ Types (ILVT)        │    └─────────────────┘
                   │                     │
┌─────────────┐    │                     │    ┌─────────────────┐
│ JSON Schema │◄──►│                     │◄──►│ Future Type     │
│ Extensions  │    │                     │    │ Systems         │
└─────────────┘    └─────────────────────┘    └─────────────────┘
```

## Core ILVT Type Registry

| **ILVT Type** | **Category** | **Description** | **Parameters** |
|---------------|--------------|-----------------|----------------|
| **Boolean Types** | | | |
| `boolean` | Logical | Boolean true/false values | - |
| **Integer Types** | | | |
| `int8` | Signed Integer | 8-bit signed integer (-128 to 127) | - |
| `int16` | Signed Integer | 16-bit signed integer | - |
| `int32` | Signed Integer | 32-bit signed integer | - |
| `int64` | Signed Integer | 64-bit signed integer | - |
| `int128` | Extended Integer | 128-bit signed integer | - |
| `int256` | Extended Integer | 256-bit signed integer | - |
| `uint8` | Unsigned Integer | 8-bit unsigned integer (0 to 255) | - |
| `uint16` | Unsigned Integer | 16-bit unsigned integer | - |
| `uint32` | Unsigned Integer | 32-bit unsigned integer | - |
| `uint64` | Unsigned Integer | 64-bit unsigned integer | - |
| `uint128` | Extended Integer | 128-bit unsigned integer | - |
| `uint256` | Extended Integer | 256-bit unsigned integer | - |
| **Decimal Types** | | | |
| `decimal` | Exact Numeric | Arbitrary precision decimal | `precision`, `scale` |
| `numeric` | Exact Numeric | Alias for decimal | `precision`, `scale` |
| **Floating Point Types** | | | |
| `float16` | Binary Float | 16-bit IEEE 754 floating point | - |
| `float32` | Binary Float | 32-bit IEEE 754 floating point | - |
| `float64` | Binary Float | 64-bit IEEE 754 floating point | - |
| `float128` | Extended Float | 128-bit IEEE 754 floating point | - |
| `float256` | Extended Float | 256-bit IEEE 754 floating point | - |
| `decfloat32` | Decimal Float | 32-bit decimal floating point | - |
| `decfloat64` | Decimal Float | 64-bit decimal floating point | - |
| `decfloat128` | Decimal Float | 128-bit decimal floating point | - |
| **String Types** | | | |
| `string` | Character String | Variable-length Unicode string | `max_length` |
| `char` | Character String | Fixed-length Unicode string | `length` |
| **Binary Types** | | | |
| `bytes` | Binary String | Variable-length binary data | `max_length` |
| `binary` | Binary String | Fixed-length binary data | `length` |
| **Temporal Types** | | | |
| `date` | Date/Time | Calendar date (year, month, day) | - |
| `time` | Date/Time | Time of day without timezone | `precision` |
| `time_tz` | Date/Time | Time of day with timezone | `precision` |
| `datetime` | Date/Time | Date and time without timezone | `precision` |
| `datetime_tz` | Date/Time | Date and time with timezone | `precision` |
| `duration` | Date/Time | Time interval/duration | `fields` |
| **Structured Types** | | | |
| `record` | Structured | Named field collection | `fields` |
| `array` | Collection | Ordered collection of same type | `element_type`, `max_cardinality` |
| `multiset` | Collection | Unordered collection with duplicates | `element_type` |
| **Special Types** | | | |
| `json` | Semi-Structured | JSON document | - |
| `vector` | Numeric Array | Fixed-size numeric vector | `dimension`, `element_type` |
| `null` | Special | Null/missing value | - |

## 4-Way Type Mapping Tables

### Boolean Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `boolean` | `BOOLEAN`, `BOOL` | `BOOLEAN` | `data.boolean` |

### Integer Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `int8` | *No GQL equivalent* | *No SQL equivalent* | `data.int8` |
| `int16` | `SMALLINT`, `INT16` | `SMALLINT` | `data.int16` |
| `int32` | `INTEGER`, `INT`, `INT32` | `INTEGER`, `INT` | `data.int32` |
| `int64` | `BIGINT`, `INT64` | `BIGINT` | `data.int64` |
| `int128` | `INT128` | *No SQL equivalent* | `data.int128` |
| `int256` | `INT256` | *No SQL equivalent* | `data.int256` |
| `uint8` | *No GQL equivalent* | *No SQL equivalent* | `data.uint8` |
| `uint16` | `UINT16` | *No SQL equivalent* | `data.uint16` |
| `uint32` | `UINT32` | *No SQL equivalent* | `data.uint32` |
| `uint64` | `UINT64` | *No SQL equivalent* | `data.uint64` |
| `uint128` | `UINT128` | *No SQL equivalent* | `data.uint128` |
| `uint256` | `UINT256` | *No SQL equivalent* | `data.uint256` |

### Decimal and Floating Point Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `decimal` | `DECIMAL`, `DEC` | `DECIMAL`, `NUMERIC`, `DEC` | `data.decimal` |
| `numeric` | `NUMERIC` | `NUMERIC` | `data.numeric` |
| `float16` | `FLOAT16` | *No SQL equivalent* | `data.float16` |
| `float32` | `FLOAT`, `REAL`, `FLOAT32` | `REAL` | `data.float32` |
| `float64` | `DOUBLE`, `DOUBLE PRECISION`, `FLOAT64` | `DOUBLE PRECISION` | `data.float64` |
| `float128` | `FLOAT128` | *No SQL equivalent* | `data.float128` |
| `float256` | `FLOAT256` | *No SQL equivalent* | `data.float256` |
| `decfloat32` | *No GQL equivalent* | `DECFLOAT(7)` | `data.decfloat32` |
| `decfloat64` | *No GQL equivalent* | `DECFLOAT(16)` | `data.decfloat64` |
| `decfloat128` | *No GQL equivalent* | `DECFLOAT(34)` | `data.decfloat128` |

### String and Binary Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `string` | `STRING` | `VARCHAR`, `CHARACTER VARYING` | `data.string` |
| `char` | `CHAR` | `CHAR`, `CHARACTER` | `data.char` |
| `bytes` | `BYTES` | `BLOB`, `BINARY LARGE OBJECT` | `data.bytes` |
| `binary` | `BINARY` | `BINARY` | `data.binary` |

### Temporal Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `date` | `DATE` | `DATE` | `data.date` |
| `time` | `LOCAL TIME` | `TIME` | `data.time` |
| `time_tz` | `ZONED TIME` | `TIME WITH TIME ZONE` | `data.timeWithTimezone` |
| `datetime` | `LOCAL DATETIME` | `TIMESTAMP` | `data.datetime` |
| `datetime_tz` | `ZONED DATETIME` | `TIMESTAMP WITH TIME ZONE` | `data.datetimeWithTimezone` |
| `duration` | `DURATION` | `INTERVAL` | `data.duration` |

### Structured and Special Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `record` | `RECORD` | `ROW` | `data.record` |
| `array` | `LIST` | `ARRAY` | `data.array` |
| `multiset` | *No GQL equivalent* | `MULTISET` | `data.multiset` |
| `json` | `JSON` | `JSON` | `data.json` |
| `vector` | `VECTOR` | *No SQL equivalent* | `data.vector` |
| `null` | `NULL` | `NULL` | `data.null` |

## Type System Coverage Analysis

### Universal Types (Supported by All Systems)
- `boolean` - Boolean values
- `int32` - Standard 32-bit integers  
- `int64` - 64-bit integers
- `float64` - Double precision floating point
- `string` - Variable-length strings
- `date` - Calendar dates
- `json` - JSON documents
- `array` - Ordered collections

### GQL-Specific Types (No SQL Foundation Equivalent)
- `int128`, `int256` - Extended precision integers
- `uint16`, `uint32`, `uint64`, `uint128`, `uint256` - Unsigned integers
- `float16`, `float32`, `float128`, `float256` - Extended precision floats
- `vector` - Numeric vectors

### SQL-Specific Types (No GQL Equivalent)
- `int8` - 8-bit integers
- `uint8` - 8-bit unsigned integers
- `decfloat32`, `decfloat64`, `decfloat128` - Decimal floating point
- `multiset` - Unordered collections with duplicates

### Future Extension Types
The ILVT system is designed to accommodate additional type systems:
- **Apache Arrow**: Columnar data types
- **Apache Parquet**: File format types
- **Apache Avro**: Schema evolution types
- **Protocol Buffers**: Message types
- **Database-Specific**: Vendor extensions

## JSON Schema Extension Format

All ILVT types map to JSON Schema extensions using the `data.` prefix:

```json
{
  "type": "integer",
  "databaseType": "data.int32",
  "minimum": -2147483648,
  "maximum": 2147483647
}
```

```json
{
  "type": "string", 
  "databaseType": "data.string",
  "maxLength": 255
}
```

```json
{
  "type": "number",
  "databaseType": "data.decimal",
  "precision": 10,
  "scale": 2
}
```

## Implementation Notes

### Type Registry Structure
- **Central Registry**: Single source of truth for all type definitions
- **Bidirectional Mappings**: Convert between any supported type systems
- **Parameter Support**: Handle type constraints (precision, scale, length)
- **Validation**: Ensure type compatibility across systems

### Conversion Strategies
- **Direct Mapping**: 1:1 correspondence where possible
- **Best Fit Mapping**: Choose closest equivalent type
- **Parameterized Mapping**: Apply constraints and parameters
- **Fallback Handling**: Graceful degradation for unsupported types

### Extension Points
- **New Type Systems**: Add via registry without breaking existing mappings
- **Custom Types**: Support domain-specific type extensions
- **Vendor Extensions**: Handle database-specific type variations
- **Version Evolution**: Support type system versioning

---

**References**:
- GQL Property Value Types: ISO/IEC 39075 (Graph Query Language)
- SQL Foundation Types: ISO/IEC 9075-2 (SQL Foundation)
- JSON Schema: draft-2020-12 specification
- IEEE 754: Floating-point arithmetic standard