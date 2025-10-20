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
│ Cypher      │◄──►│                     │◄──►│ JSON Schema     │
│ Data Types  │    │                     │    │ Extensions      │
└─────────────┘    └─────────────────────┘    └─────────────────┘
                   │                     │
                   │                     │    ┌─────────────────┐
                   │                     │◄──►│ Future Type     │
                   │                     │    │ Systems         │
                   └─────────────────────┘    └─────────────────┘
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

## 5-Way Type Mapping Tables

### Boolean Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `boolean` | `BOOLEAN`, `BOOL` | `BOOLEAN` | `BOOLEAN` | `data.boolean` |

### Integer Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `int8` | `INT8` | *No SQL equivalent* | *No Cypher equivalent* | `data.int8` |
| `int16` | `SMALLINT`, `INT16` | `SMALLINT` | *No Cypher equivalent* | `data.int16` |
| `int32` | `INTEGER`, `INT`, `INT32` | `INTEGER`, `INT` | *No Cypher equivalent* | `data.int32` |
| `int64` | `BIGINT`, `INT64` | `BIGINT` | `INTEGER` | `data.int64` |
| `int128` | `INT128` | *No SQL equivalent* | *No Cypher equivalent* | `data.int128` |
| `int256` | `INT256` | *No SQL equivalent* | *No Cypher equivalent* | `data.int256` |
| `uint8` | `UINT8` | *No SQL equivalent* | *No Cypher equivalent* | `data.uint8` |
| `uint16` | `UINT16` | *No SQL equivalent* | *No Cypher equivalent* | `data.uint16` |
| `uint32` | `UINT32` | *No SQL equivalent* | *No Cypher equivalent* | `data.uint32` |
| `uint64` | `UINT64` | *No SQL equivalent* | *No Cypher equivalent* | `data.uint64` |
| `uint128` | `UINT128` | *No SQL equivalent* | `data.uint128` |
| `uint256` | `UINT256` | *No SQL equivalent* | `data.uint256` |

#### Implementation-Defined Features for Integer Types

**SQL Foundation INTEGER Precision (Implementation-Defined)**:
- The precision of `SMALLINT`, `INTEGER`, `INT`, and `BIGINT` types is implementation-defined
- All SQL integer types can have equal precision in a given implementation
- An implementation could support `INT8` as an extension with implementation-defined precision
- The actual bit width and value ranges are determined by the SQL implementation

**Affected Types**: `int8`, `int16`, `int32`, `int64` - SQL precision and ranges are implementation-defined

### Decimal and Floating Point Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `decimal` | `DECIMAL`, `DEC` | `DECIMAL`, `NUMERIC`, `DEC` | *No Cypher equivalent* | `data.decimal` |
| `numeric` | `NUMERIC` | `NUMERIC` | *No Cypher equivalent* | `data.numeric` |
| `float16` | `FLOAT16` | *No SQL equivalent* | *No Cypher equivalent* | `data.float16` |
| `float32` | `FLOAT`, `REAL`, `FLOAT32` | `REAL` | *No Cypher equivalent* | `data.float32` |
| `float64` | `DOUBLE`, `DOUBLE PRECISION`, `FLOAT64` | `DOUBLE PRECISION` | `FLOAT` | `data.float64` |
| `float128` | `FLOAT128` | *No SQL equivalent* | *No Cypher equivalent* | `data.float128` |
| `float256` | `FLOAT256` | *No SQL equivalent* | *No Cypher equivalent* | `data.float256` |
| `decfloat32` | *No GQL equivalent* | `DECFLOAT(7)` | *No Cypher equivalent* | `data.decfloat32` |
| `decfloat64` | *No GQL equivalent* | `DECFLOAT(16)` | *No Cypher equivalent* | `data.decfloat64` |
| `decfloat128` | *No GQL equivalent* | `DECFLOAT(34)` | *No Cypher equivalent* | `data.decfloat128` |

### String and Binary Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `string` | `STRING` | `VARCHAR`, `CHARACTER VARYING` | `STRING` | `data.string` |
| `char` | `CHAR` | `CHAR`, `CHARACTER` | *No Cypher equivalent* | `data.char` |
| `bytes` | `BYTES` | `BLOB`, `BINARY LARGE OBJECT` | *No Cypher equivalent* | `data.bytes` |
| `binary` | `BINARY` | `BINARY` | *No Cypher equivalent* | `data.binary` |

### Temporal Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `date` | `DATE` | `DATE` | `DATE` | `data.date` |
| `time` | `LOCAL TIME` | `TIME` | `TIME` | `data.time` |
| `time_tz` | `ZONED TIME` | `TIME WITH TIME ZONE` | *No Cypher equivalent* | `data.timeWithTimezone` |
| `datetime` | `LOCAL DATETIME` | `TIMESTAMP` | `DATETIME` | `data.datetime` |
| `datetime_tz` | `ZONED DATETIME` | `TIMESTAMP WITH TIME ZONE` | *No Cypher equivalent* | `data.datetimeWithTimezone` |
| `duration` | `DURATION` | `INTERVAL` | `DURATION` | `data.duration` |

### Structured and Special Types
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **Cypher Data Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|----------------------|---------------------------|
| `record` | `RECORD` | `ROW` | *No Cypher equivalent* | `data.record` |
| `array` | `LIST` | `ARRAY` | `LIST` | `data.array` |
| `multiset` | *No GQL equivalent* | `MULTISET` | *No Cypher equivalent* | `data.multiset` |
| `json` | *No GQL equivalent* | `JSON` | *No Cypher equivalent* | `data.json` |
| `vector` | `VECTOR` | `VECTOR` | *No Cypher equivalent* | `data.vector` |
| `null` | `NULL` | `NULL` | `NULL` | `data.null` |

## Cypher Data Type System Integration

### Core Cypher Types
Cypher supports a limited but practical set of data types that map to ILVT as follows:

| **Cypher Type** | **ILVT Mapping** | **Description** | **Value Range/Format** |
|-----------------|------------------|-----------------|------------------------|
| `BOOLEAN` | `boolean` | Boolean true/false values | `true`, `false` |
| `INTEGER` | `int64` | 64-bit signed integer | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `FLOAT` | `float64` | IEEE 754 double-precision floating point | ±1.7976931348623157E+308 |
| `STRING` | `string` | Unicode text string | Variable length, UTF-8 encoded |
| `DATE` | `date` | Calendar date | ISO 8601 date format (YYYY-MM-DD) |
| `TIME` | `time` | Time of day | ISO 8601 time format (HH:MM:SS[.fff]) |
| `DATETIME` | `datetime` | Date and time | ISO 8601 datetime format |
| `DURATION` | `duration` | Time interval | ISO 8601 duration format |
| `LIST` | `array` | Ordered collection | Heterogeneous elements allowed |
| `NULL` | `null` | Null/missing value | Single null value |

### Cypher Collection Types
- **LIST**: Cypher lists are heterogeneous (can contain mixed types), unlike strongly-typed arrays in GQL/SQL
- **MAP**: Cypher supports map/dictionary types (key-value pairs) but these map to `record` in ILVT

### Cypher Type Characteristics
- **Dynamic Typing**: Cypher is dynamically typed, allowing mixed-type collections
- **Null Handling**: Cypher has comprehensive null propagation semantics
- **Type Coercion**: Limited automatic type conversion (mainly string-to-number)
- **No Unsigned Types**: Cypher only supports signed integers
- **No Decimal Types**: Cypher uses floating-point for all non-integer numbers

### Language Level Mapping Strategy
When translating between ILVT and Cypher types based on language level:

**GQL Language Level**:
- Use full ILVT type system with precise type mappings
- Support all GQL-specific types (INT8, UINT*, extended precision)
- Strict type validation and constraint enforcement

**LEX Language Level** (Cypher compatibility):
- Map to Cypher-compatible subset of ILVT
- `int64` for all integer types (with range validation)
- `float64` for all floating-point types
- `string` for all text types
- Allow heterogeneous collections (relaxed type constraints)

## Type System Coverage Analysis

### Universal Types (Supported by All Systems)
- `boolean` - Boolean values
- `int16` - 16-bit integers (SMALLINT)
- `int32` - Standard 32-bit integers  
- `int64` - 64-bit integers
- `float32` - Single precision floating point (REAL)
- `float64` - Double precision floating point
- `string` - Variable-length strings
- `date` - Calendar dates
- `vector` - Numeric vectors
- `array` - Ordered collections

### GQL-Specific Types (No SQL Foundation Equivalent)
- `int8`, `uint8` - 8-bit signed and unsigned integers
- `int128`, `int256` - Extended precision integers
- `uint16`, `uint32`, `uint64`, `uint128`, `uint256` - Unsigned integers
- `float16`, `float128`, `float256` - Extended precision floats

### SQL-Specific Types (No GQL Equivalent)
- `json` - JSON documents
- `decfloat32`, `decfloat64`, `decfloat128` - Decimal floating point
- `multiset` - Unordered collections with duplicates

### Future Extension Types
The ILVT system is designed to accommodate additional type systems:
- **Apache Arrow**: Columnar data types
- **Apache Parquet**: File format types
- **Apache Avro**: Schema evolution types
- **Protocol Buffers**: Message types
- **Database-Specific**: Vendor extensions

## Complete JSON Schema Type Definitions

All ILVT types map to JSON Schema extensions with three naming fields:
- `data.<name>`: Universal intermediate representation
- `gql.<name>`: GQL-specific type name (undefined for SQL-only types)  
- `sql.<name>`: SQL Foundation type name (undefined for GQL-only types)

### Boolean Types
```json
{
  "$defs": {
    "boolean": {
      "data.boolean": {
        "type": "boolean"
      },
      "gql.boolean": "BOOLEAN",
      "sql.boolean": "BOOLEAN"
    }
  }
}
```

### Integer Types
```json
{
  "$defs": {
    "int8": {
      "data.int8": {
        "type": "integer",
        "minimum": -128,
        "maximum": 127
      },
      "gql.int8": "INT8",
      "sql.int8": "undefined"
    },
    "int16": {
      "data.int16": {
        "type": "integer", 
        "minimum": -32768,
        "maximum": 32767
      },
      "gql.int16": "SMALLINT",
      "sql.int16": "SMALLINT"
    },
    "int32": {
      "data.int32": {
        "type": "integer",
        "minimum": -2147483648,
        "maximum": 2147483647
      },
      "gql.int32": "INTEGER",
      "sql.int32": "INTEGER"
    },
    "int64": {
      "data.int64": {
        "type": "integer",
        "minimum": -9223372036854775808,
        "maximum": 9223372036854775807
      },
      "gql.int64": "BIGINT", 
      "sql.int64": "BIGINT"
    },
    "int128": {
      "data.int128": {
        "type": "integer",
        "minimum": -170141183460469231731687303715884105728,
        "maximum": 170141183460469231731687303715884105727
      },
      "gql.int128": "INT128",
      "sql.int128": "undefined"
    },
    "int256": {
      "data.int256": {
        "type": "integer",
        "minimum": -57896044618658097711785492504343953926634992332820282019728792003956564819968,
        "maximum": 57896044618658097711785492504343953926634992332820282019728792003956564819967
      },
      "gql.int256": "INT256",
      "sql.int256": "undefined"
    },
    "uint8": {
      "data.uint8": {
        "type": "integer",
        "minimum": 0,
        "maximum": 255
      },
      "gql.uint8": "UINT8",
      "sql.uint8": "undefined"
    },
    "uint16": {
      "data.uint16": {
        "type": "integer",
        "minimum": 0,
        "maximum": 65535
      },
      "gql.uint16": "UINT16",
      "sql.uint16": "undefined"
    },
    "uint32": {
      "data.uint32": {
        "type": "integer",
        "minimum": 0,
        "maximum": 4294967295
      },
      "gql.uint32": "UINT32",
      "sql.uint32": "undefined"
    },
    "uint64": {
      "data.uint64": {
        "type": "integer",
        "minimum": 0,
        "maximum": 18446744073709551615
      },
      "gql.uint64": "UINT64",
      "sql.uint64": "undefined"
    },
    "uint128": {
      "data.uint128": {
        "type": "integer",
        "minimum": 0,
        "maximum": 340282366920938463463374607431768211455
      },
      "gql.uint128": "UINT128",
      "sql.uint128": "undefined"
    },
    "uint256": {
      "data.uint256": {
        "type": "integer",
        "minimum": 0,
        "maximum": 115792089237316195423570985008687907853269984665640564039457584007913129639935
      },
      "gql.uint256": "UINT256",
      "sql.uint256": "undefined"
    }
  }
}
```

### Decimal and Floating Point Types
```json
{
  "$defs": {
    "decimal": {
      "data.decimal": {
        "type": "number",
        "precision": {"type": "integer", "minimum": 1},
        "scale": {"type": "integer", "minimum": 0}
      },
      "gql.decimal": "DECIMAL",
      "sql.decimal": "DECIMAL"
    },
    "numeric": {
      "data.numeric": {
        "type": "number",
        "precision": {"type": "integer", "minimum": 1},
        "scale": {"type": "integer", "minimum": 0}
      },
      "gql.numeric": "NUMERIC",
      "sql.numeric": "NUMERIC"
    },
    "float16": {
      "data.float16": {
        "type": "number",
        "minimum": -65504,
        "maximum": 65504
      },
      "gql.float16": "FLOAT16",
      "sql.float16": "undefined"
    },
    "float32": {
      "data.float32": {
        "type": "number"
      },
      "gql.float32": "FLOAT",
      "sql.float32": "REAL"
    },
    "float64": {
      "data.float64": {
        "type": "number"
      },
      "gql.float64": "DOUBLE",
      "sql.float64": "DOUBLE PRECISION"
    },
    "float128": {
      "data.float128": {
        "type": "number"
      },
      "gql.float128": "FLOAT128",
      "sql.float128": "undefined"
    },
    "float256": {
      "data.float256": {
        "type": "number"
      },
      "gql.float256": "FLOAT256",
      "sql.float256": "undefined"
    },
    "decfloat32": {
      "data.decfloat32": {
        "type": "number"
      },
      "gql.decfloat32": "undefined",
      "sql.decfloat32": "DECFLOAT(7)"
    },
    "decfloat64": {
      "data.decfloat64": {
        "type": "number"
      },
      "gql.decfloat64": "undefined",
      "sql.decfloat64": "DECFLOAT(16)"
    },
    "decfloat128": {
      "data.decfloat128": {
        "type": "number"
      },
      "gql.decfloat128": "undefined",
      "sql.decfloat128": "DECFLOAT(34)"
    }
  }
}
```

### String and Binary Types
```json
{
  "$defs": {
    "string": {
      "data.string": {
        "type": "string",
        "maxLength": {"type": "integer", "minimum": 0}
      },
      "gql.string": "STRING",
      "sql.string": "VARCHAR"
    },
    "char": {
      "data.char": {
        "type": "string",
        "length": {"type": "integer", "minimum": 1}
      },
      "gql.char": "CHAR",
      "sql.char": "CHAR"
    },
    "bytes": {
      "data.bytes": {
        "type": "string",
        "contentEncoding": "base64",
        "maxLength": {"type": "integer", "minimum": 0}
      },
      "gql.bytes": "BYTES",
      "sql.bytes": "BLOB"
    },
    "binary": {
      "data.binary": {
        "type": "string",
        "contentEncoding": "base64",
        "length": {"type": "integer", "minimum": 1}
      },
      "gql.binary": "BINARY",
      "sql.binary": "BINARY"
    }
  }
}
```

### Temporal Types
```json
{
  "$defs": {
    "date": {
      "data.date": {
        "type": "string",
        "format": "date"
      },
      "gql.date": "DATE",
      "sql.date": "DATE"
    },
    "time": {
      "data.time": {
        "type": "string",
        "format": "time",
        "precision": {"type": "integer", "minimum": 0, "maximum": 9}
      },
      "gql.time": "LOCAL TIME",
      "sql.time": "TIME"
    },
    "time_tz": {
      "data.timeWithTimezone": {
        "type": "string",
        "format": "time",
        "precision": {"type": "integer", "minimum": 0, "maximum": 9}
      },
      "gql.timeWithTimezone": "ZONED TIME",
      "sql.timeWithTimezone": "TIME WITH TIME ZONE"
    },
    "datetime": {
      "data.datetime": {
        "type": "string",
        "format": "date-time",
        "precision": {"type": "integer", "minimum": 0, "maximum": 9}
      },
      "gql.datetime": "LOCAL DATETIME",
      "sql.datetime": "TIMESTAMP"
    },
    "datetime_tz": {
      "data.datetimeWithTimezone": {
        "type": "string",
        "format": "date-time",
        "precision": {"type": "integer", "minimum": 0, "maximum": 9}
      },
      "gql.datetimeWithTimezone": "ZONED DATETIME",
      "sql.datetimeWithTimezone": "TIMESTAMP WITH TIME ZONE"
    },
    "duration": {
      "data.duration": {
        "type": "string",
        "format": "duration",
        "fields": {"type": "string", "enum": ["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"]}
      },
      "gql.duration": "DURATION",
      "sql.duration": "INTERVAL"
    }
  }
}
```

### Structured and Special Types
```json
{
  "$defs": {
    "record": {
      "data.record": {
        "type": "object",
        "fields": {"type": "object"}
      },
      "gql.record": "RECORD",
      "sql.record": "ROW"
    },
    "array": {
      "data.array": {
        "type": "array",
        "elementType": {"type": "string"},
        "maxCardinality": {"type": "integer", "minimum": 0}
      },
      "gql.array": "LIST",
      "sql.array": "ARRAY"
    },
    "multiset": {
      "data.multiset": {
        "type": "array",
        "uniqueItems": false,
        "elementType": {"type": "string"}
      },
      "gql.multiset": "undefined",
      "sql.multiset": "MULTISET"
    },
    "json": {
      "data.json": {
        "type": ["object", "array", "string", "number", "boolean", "null"]
      },
      "gql.json": "undefined",
      "sql.json": "JSON"
    },
    "vector": {
      "data.vector": {
        "type": "array",
        "items": {"type": "number"},
        "dimension": {"type": "integer", "minimum": 1},
        "elementType": {"type": "string", "enum": ["float32", "float64", "int32", "int64"]}
      },
      "gql.vector": "VECTOR",
      "sql.vector": "VECTOR"
    },
    "null": {
      "data.null": {
        "type": "null"
      },
      "gql.null": "NULL",
      "sql.null": "NULL"
    }
  }
}
```

## Implementation-Defined Features by Language

### GQL Implementation-Defined Features (Type-Related)

**Numeric Types**:
- `INT8`, `INT16`, `INT32`, `INT64`, `INT128`, `INT256`: Actual precision and value ranges
- `UINT8`, `UINT16`, `UINT32`, `UINT64`, `UINT128`, `UINT256`: Actual precision and value ranges  
- `FLOAT16`, `FLOAT32`, `FLOAT64`, `FLOAT128`, `FLOAT256`: Precision, exponent range, and special value handling
- `DECIMAL`, `NUMERIC`: Maximum precision and scale values supported
- Overflow and underflow behavior for all numeric types

**String Types**:
- `STRING`: Maximum length supported
- `CHAR`: Maximum length supported
- Character set and collation support

**Temporal Types**:
- `DATE`: Supported date range (minimum and maximum years)
- `LOCAL TIME`, `ZONED TIME`: Fractional seconds precision (0-9 digits)
- `LOCAL DATETIME`, `ZONED DATETIME`: Fractional seconds precision and supported date range
- `DURATION`: Supported interval fields and precision
- Time zone database and leap second handling

**Structured Types**:
- `VECTOR`: Maximum dimension supported, supported coordinate types
- `LIST`: Maximum cardinality supported
- `RECORD`: Maximum nesting depth, maximum number of fields

### SQL Foundation Implementation-Defined Features (Type-Related)

**Numeric Types**:
- `SMALLINT`, `INTEGER`, `INT`, `BIGINT`: Actual precision (can be equal across types)
- `DECIMAL`, `NUMERIC`: Maximum precision and scale values
- `REAL`, `DOUBLE PRECISION`: Precision and exponent range
- `DECFLOAT`: Supported precision values beyond standard (7, 16, 34)
- Rounding behavior for exact numeric operations

**String Types**:
- `CHARACTER`, `CHAR`: Maximum length supported
- `VARCHAR`, `CHARACTER VARYING`: Maximum length supported
- `CLOB`: Maximum size supported
- Character repertoire and form-of-use conversion

**Binary Types**:
- `BINARY`: Maximum length supported
- `VARBINARY`, `BINARY VARYING`: Maximum length supported  
- `BLOB`: Maximum size supported

**Temporal Types**:
- `DATE`: Supported date range
- `TIME`, `TIME WITH TIME ZONE`: Fractional seconds precision
- `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`: Fractional seconds precision and supported date range
- `INTERVAL`: Supported interval precision and leading field precision

**Structured Types**:
- `ARRAY`: Maximum cardinality supported, maximum nesting depth
- `MULTISET`: Maximum cardinality supported
- `ROW`: Maximum number of fields, maximum nesting depth
- `VECTOR`: Maximum dimension supported, supported coordinate types

**Special Types**:
- `JSON`: Maximum document size, supported JSON features

### Cross-Language Implementation Considerations

**Type Precision Alignment**:
- When mapping between GQL and SQL integer types, implementations may choose to align precisions
- SQL `SMALLINT` may have the same precision as `INTEGER` and `BIGINT` in some implementations
- GQL `INT8` could be supported as a SQL extension with implementation-defined precision

**Temporal Precision**:
- Fractional seconds precision may vary between GQL and SQL implementations
- Time zone handling and leap second support varies by implementation

**String Length Limits**:
- Maximum string lengths may differ significantly between implementations
- Character encoding support (UTF-8, UTF-16, etc.) is implementation-defined

**Vector Support**:
- Coordinate type support varies (some implementations may only support float32/float64)
- Maximum vector dimensions vary significantly by implementation
- Distance function support is implementation-defined

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

## Annexe: Specification Evidence and Corrections

**IMPORTANT**: This annexe contains the actual specification excerpts that were used to create the ILVT mappings, along with corrections to initial assumptions.

### A.1 Major Corrections to Initial Assumptions

#### A.1.1 SQL Foundation DOES Support Vector Types
**Initial Claim**: "SQL Foundation has no vector equivalent"  
**Correction**: SQL Foundation (ISO/IEC 9075-2) DOES define vector types.

**Evidence from SQL Foundation BNF**:
```bnf
<predefined type> ::=
    <character string type> [ CHARACTER SET <character set specification> ] [ <collate clause> ]
  | <national character string type> [ <collate clause> ]
  | <binary string type>
  | <numeric type>
  | <boolean type>
  | <datetime type>
  | <interval type>
  | <JSON type>
  | <vector type>

<vector type> ::=
    VECTOR <left paren> <dimension> <comma> <coordinate type> <right paren>
```

#### A.1.2 GQL DOES Support INT8 and UINT8 Types
**Initial Claim**: "GQL has no int8 equivalent"  
**Correction**: GQL (ISO/IEC 39075) DOES define INT8 and UINT8 types.

**Evidence from GQL BNF**:
```bnf
<signed binary exact numeric type> ::=
    INT8 [ <not null> ]
  | INT16 [ <not null> ]
  | INT32 [ <not null> ]
  | INT64 [ <not null> ]
  | INT128 [ <not null> ]
  | INT256 [ <not null> ]
  | SMALLINT [ <not null> ]
  | INT [ <left paren> <precision> <right paren> ] [ <not null> ]
  | BIGINT [ <not null> ]
  | [ SIGNED ] <verbose binary exact numeric type>

<unsigned binary exact numeric type> ::=
    UINT8 [ <not null> ]
  | UINT16 [ <not null> ]
  | UINT32 [ <not null> ]
  | UINT64 [ <not null> ]
  | UINT128 [ <not null> ]
  | UINT256 [ <not null> ]
  | USMALLINT [ <not null> ]
  | UINT [ <left paren> <precision> <right paren> ] [ <not null> ]
  | UBIGINT [ <not null> ]
  | UNSIGNED <verbose binary exact numeric type>
```

#### A.1.3 SQL Foundation DOES NOT Support Unsigned Integer Data Types
**Claim**: "SQL Foundation has no unsigned integer types"  
**Verification**: CORRECT - SQL Foundation only defines signed integer types.

**Evidence from SQL Foundation BNF**:
```bnf
<exact numeric type> ::=
    NUMERIC [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | DECIMAL [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | DEC [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | SMALLINT
  | INTEGER
  | INT
  | BIGINT
```
*Note: No UNSIGNED variants are defined in SQL Foundation.*

#### A.1.4 GQL DOES NOT Support JSON as a Native Type
**Initial Claim**: "GQL supports JSON as a native type"  
**Correction**: GQL (ISO/IEC 39075) does NOT define JSON as a predefined type.

**Evidence**: Search for "JSON" in GQL BNF specification returns no results, indicating JSON is not a predefined type in GQL.

### A.2 Complete Type System Specifications

#### A.2.1 SQL Foundation (ISO/IEC 9075-2) Predefined Types

**Complete Predefined Type Definition**:
```bnf
<predefined type> ::=
    <character string type> [ CHARACTER SET <character set specification> ] [ <collate clause> ]
  | <national character string type> [ <collate clause> ]
  | <binary string type>
  | <numeric type>
  | <boolean type>
  | <datetime type>
  | <interval type>
  | <JSON type>
  | <vector type>

<numeric type> ::=
    <exact numeric type>
  | <approximate numeric type>
  | <decimal floating-point type>

<exact numeric type> ::=
    NUMERIC [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | DECIMAL [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | DEC [ <left paren> <precision> [ <comma> <scale> ] <right paren> ]
  | SMALLINT
  | INTEGER
  | INT
  | BIGINT

<approximate numeric type> ::=
    FLOAT [ <left paren> <precision> <right paren> ]
  | REAL
  | DOUBLE PRECISION

<decimal floating-point type> ::=
    DECFLOAT [ <left paren> <precision> <right paren> ]

<boolean type> ::=
    BOOLEAN

<character string type> ::=
    CHARACTER [ <left paren> <character length> <right paren> ]
  | CHAR [ <left paren> <character length> <right paren> ]
  | CHARACTER VARYING [ <left paren> <character maximum length> <right paren> ]
  | CHAR VARYING [ <left paren> <character maximum length> <right paren> ]
  | VARCHAR [ <left paren> <character maximum length> <right paren> ]
  | <character large object type>

<binary string type> ::=
    BINARY [ <left paren> <length> <right paren> ]
  | BINARY VARYING [ <left paren> <maximum length> <right paren> ]
  | VARBINARY [ <left paren> <maximum length> <right paren> ]
  | <binary large object string type>

<datetime type> ::=
    DATE
  | TIME [ <left paren> <time precision> <right paren> ] [ <with or without time zone> ]
  | TIMESTAMP [ <left paren> <timestamp precision> <right paren> ] [ <with or without time zone> ]

<interval type> ::=
    INTERVAL <interval qualifier>

<JSON type> ::=
    JSON

<vector type> ::=
    VECTOR <left paren> <dimension> <comma> <coordinate type> <right paren>
```

#### A.2.2 GQL (ISO/IEC 39075) Property Value Types

**Complete Exact Numeric Type Definition**:
```bnf
<exact numeric type> ::=
    <binary exact numeric type>
  | <decimal exact numeric type>

<binary exact numeric type> ::=
    <signed binary exact numeric type>
  | <unsigned binary exact numeric type>

<signed binary exact numeric type> ::=
    INT8 [ <not null> ]
  | INT16 [ <not null> ]
  | INT32 [ <not null> ]
  | INT64 [ <not null> ]
  | INT128 [ <not null> ]
  | INT256 [ <not null> ]
  | SMALLINT [ <not null> ]
  | INT [ <left paren> <precision> <right paren> ] [ <not null> ]
  | BIGINT [ <not null> ]
  | [ SIGNED ] <verbose binary exact numeric type>

<unsigned binary exact numeric type> ::=
    UINT8 [ <not null> ]
  | UINT16 [ <not null> ]
  | UINT32 [ <not null> ]
  | UINT64 [ <not null> ]
  | UINT128 [ <not null> ]
  | UINT256 [ <not null> ]
  | USMALLINT [ <not null> ]
  | UINT [ <left paren> <precision> <right paren> ] [ <not null> ]
  | UBIGINT [ <not null> ]
  | UNSIGNED <verbose binary exact numeric type>

<vector type> ::=
    VECTOR <left paren> <dimension> <comma> <coordinate type> <right paren> [ <not null> ]
```

### A.3 Revised ILVT Mappings Based on Specification Evidence

#### A.3.1 Corrected Integer Type Mappings
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `int8` | `INT8` | *No SQL equivalent* | `data.int8` |
| `uint8` | `UINT8` | *No SQL equivalent* | `data.uint8` |

#### A.3.2 Corrected Vector Type Mappings
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `vector` | `VECTOR` | `VECTOR` | `data.vector` |

#### A.3.3 Corrected JSON Type Mappings
| **ILVT Type** | **GQL Property Value Type** | **SQL Foundation Type** | **JSON Schema Extension** |
|---------------|----------------------------|-------------------------|---------------------------|
| `json` | *No GQL equivalent* | `JSON` | `data.json` |

### A.4 Specification Sources

**SQL Foundation (ISO/IEC 9075-2)**:
- File: `sql-foundation.bnf.txt`
- Date: 2025-07-03
- Lines referenced: 830-833 (VECTOR keywords), 1635-1787 (type definitions)

**GQL (ISO/IEC 39075)**:
- File: `gql-standard.bnf.txt` 
- Date: 2025-06-18
- Lines referenced: 1405-1417 (INT8/UINT8), 1497-1498 (VECTOR), 2941-3049 (keywords)

### A.5 Methodology Notes

1. **Specification Analysis**: Direct examination of BNF grammar files from official ISO/IEC standards
2. **Keyword Search**: Systematic grep searches for type names in specification files
3. **Cross-Verification**: Comparison between GQL and SQL Foundation specifications
4. **Error Correction**: Identification and correction of initial incorrect assumptions

**Key Lesson**: Always verify claims against actual specification text rather than making assumptions based on general knowledge or incomplete information.

---

**References**:
- GQL Property Value Types: ISO/IEC 39075 (Graph Query Language)
- SQL Foundation Types: ISO/IEC 9075-2 (SQL Foundation)  
- JSON Schema: draft-2020-12 specification
- IEEE 754: Floating-point arithmetic standard