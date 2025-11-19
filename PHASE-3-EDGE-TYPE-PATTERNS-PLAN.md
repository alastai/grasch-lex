# Phase 3: Complex Edge Type Patterns

## Overview

Phase 3 focuses on ensuring the JSON Schema correctly validates all the complex edge type patterns defined in LEX-11 and demonstrated in the comprehensive examples.

## Current Status

### ✅ Requirements (LEX-11)
LEX-11 comprehensively documents all edge type syntax patterns:
- directed:/undirected: wrappers
- via:/arc: keywords (synonyms)
- Multiple endpoint name sets (from/to, tail/head, src/dst/dest)
- between:/and: for undirected edges
- SAME/SELF keywords for self-loops
- Type references (typeLabel, typeIdentifier, index)
- Inline node type definitions
- abstract:/abstractSupertype: wrappers for endpoints
- Anonymous edge types (no via/arc)
- Edge type inheritance (extends/adding)

### ✅ Examples
`lex-2026.0.3.2-edge-type-syntax-examples.yaml` contains 40+ edge type examples covering:
- All endpoint name synonyms
- All direction patterns
- Self-loops (SAME/SELF)
- Type references (labels, identifiers, indices)
- Inline node type definitions
- Abstract endpoint requirements
- Edge type inheritance
- Anonymous edges

### ⚠️ Schema Validation
Current validation status: 7/14 files passing (50%)

Files with complex edge types that are failing AFTER IMPORTS:
- ✗ lex-2026.0.3.2-all-import-patterns.yaml (imports comprehensive edge examples)
- ✗ lex-2026.0.3.2-type-definition-syntax-examples.yaml (imports comprehensive edge examples)

## Edge Type Patterns to Verify

### 1. Direction Wrappers
```yaml
# Directed
edgeType:
  directed:
    from: Person
    via: KNOWS
    to: Person

# Undirected
edgeType:
  undirected:
    between: Person
    via: KNOWS
    and: Person
```

**Schema requirement**: Must support both `directed:` and `undirected:` as top-level wrappers in EdgeType

### 2. Endpoint Name Synonyms

**Directed edges** - Three synonym sets:
- Primary: `from:` / `to:`
- Set 1: `tail:` / `head:`
- Set 2: `src:` / `dst:` or `dest:`

**Undirected edges**:
- Primary: `between:` / `and:`

**Schema requirement**: Must accept ANY of these synonym sets (not require specific ones)

### 3. Label Keywords

- Primary: `via:`
- Synonym: `arc:`

**Schema requirement**: Must accept either `via:` or `arc:` (or neither for anonymous edges)

### 4. Self-Loop Keywords

- `SAME` - second endpoint same as first
- `SELF` - synonym for SAME

**Schema requirement**: Must accept string literals "SAME" or "SELF" as endpoint values

### 5. Type Reference Formats

Endpoints can reference node types in multiple ways:
```yaml
# String (typeLabel)
from: Person

# Array (typeIdentifier)
from: ["Person", "Employee"]

# Integer (index)
from: 0

# Object with typeLabels
from:
  typeLabels:
  - Product
  - Sellable

# Inline node type definition
from:
  nodeType:
    typeLabel: Property
    implies:
      propertyTypes: [...]
```

**Schema requirement**: Must accept all these formats via oneOf pattern

### 6. Abstract Endpoint Wrappers

```yaml
# Using abstract:
to:
  abstract: Person

# Using abstractSupertype:
to:
  abstractSupertype: Person
```

**Schema requirement**: Must support both `abstract:` and `abstractSupertype:` wrappers

### 7. Anonymous Edge Types

```yaml
# No via/arc keyword
edgeType:
  directed:
    from: Person
    to: Company
```

**Schema requirement**: `via:` and `arc:` must be optional

## Schema Verification Tasks

### Task 1: Check EdgeType Definition
Verify the EdgeType schema definition supports:
- ✅ Both `directed:` and `undirected:` wrappers
- ✅ All endpoint name synonyms
- ✅ Both `via:` and `arc:` keywords
- ✅ Optional label keywords (anonymous edges)

### Task 2: Check Endpoint Type References
Verify endpoint schemas accept:
- ✅ String (typeLabel)
- ✅ Array (typeIdentifier)
- ✅ Integer (index)
- ✅ Object with typeLabels
- ✅ Object with inline nodeType
- ✅ String literals "SAME" and "SELF"

### Task 3: Check Abstract Wrappers
Verify endpoint schemas support:
- ✅ `abstract:` wrapper
- ✅ `abstractSupertype:` wrapper

### Task 4: Validate Against Examples
Run validation on files with comprehensive edge examples:
- Test `all-import-patterns.yaml` (after preprocessing)
- Test `type-definition-syntax-examples.yaml` (after preprocessing)
- Identify specific validation failures
- Fix schema to accept valid patterns

## Expected Schema Structure

### EdgeType Definition (Simplified)
```json
{
  "EdgeType": {
    "type": "object",
    "oneOf": [
      {
        "required": ["edgeType"],
        "properties": {
          "edgeType": {
            "oneOf": [
              {"$ref": "#/$defs/DirectedEdgeType"},
              {"$ref": "#/$defs/UndirectedEdgeType"}
            ]
          }
        }
      },
      {
        "required": ["abstract"],
        "properties": {
          "abstract": {
            "type": "object",
            "properties": {
              "edgeType": {"$ref": "#/$defs/EdgeTypeCore"}
            }
          }
        }
      }
    ]
  }
}
```

### DirectedEdgeType (Simplified)
```json
{
  "DirectedEdgeType": {
    "type": "object",
    "required": ["directed"],
    "properties": {
      "directed": {
        "type": "object",
        "properties": {
          "from": {"$ref": "#/$defs/EndpointReference"},
          "tail": {"$ref": "#/$defs/EndpointReference"},
          "src": {"$ref": "#/$defs/EndpointReference"},
          "to": {"$ref": "#/$defs/EndpointReference"},
          "head": {"$ref": "#/$defs/EndpointReference"},
          "dst": {"$ref": "#/$defs/EndpointReference"},
          "dest": {"$ref": "#/$defs/EndpointReference"},
          "via": {"type": "string"},
          "arc": {"type": "string"}
        },
        "oneOf": [
          {"required": ["from", "to"]},
          {"required": ["tail", "head"]},
          {"required": ["src", "dst"]},
          {"required": ["src", "dest"]}
        ]
      }
    }
  }
}
```

### EndpointReference (Simplified)
```json
{
  "EndpointReference": {
    "oneOf": [
      {"type": "string"},  // typeLabel or "SAME"/"SELF"
      {"type": "array", "items": {"type": "string"}},  // typeIdentifier
      {"type": "integer"},  // index
      {
        "type": "object",
        "properties": {
          "typeLabels": {"type": "array", "items": {"type": "string"}}
        }
      },
      {
        "type": "object",
        "properties": {
          "nodeType": {"$ref": "#/$defs/NodeType"}
        }
      },
      {
        "type": "object",
        "properties": {
          "abstract": {"type": "string"}
        }
      },
      {
        "type": "object",
        "properties": {
          "abstractSupertype": {"type": "string"}
        }
      }
    ]
  }
}
```

## Success Criteria

Phase 3 is complete when:
1. ✅ All edge type patterns from LEX-11 are validated by the schema
2. ✅ Files with comprehensive edge examples pass validation (AFTER IMPORTS)
3. ✅ Schema documentation clearly explains all supported patterns
4. ✅ Validation rate improves (target: 10+/14 files passing)

## Next Steps

1. **Analyze current schema**: Read EdgeType definition in `lex-2026.0.3.2.schema.json`
2. **Identify gaps**: Compare schema with LEX-11 requirements
3. **Fix schema**: Update to support all patterns
4. **Test**: Run validation and verify improvements
5. **Document**: Update schema comments and documentation

---

**Date**: November 19, 2024
**Status**: Ready to begin Phase 3
**Focus**: Edge type pattern validation
**Goal**: Support all LEX-11 edge type syntax patterns

