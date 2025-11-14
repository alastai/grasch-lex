# Amendment: Added `implies` Container Structure

## Change Applied
Restructured node and edge types to use an `implies` container for `supertypes`, `labels`, and `propertyTypes` as specified in LEX-100r3.

## Rationale
LEX-100r3 specifies that identified node/edge types should have an `implies` descriptor that contains the supertypes, labels, and property types. This structure better reflects the semantic meaning that these attributes are "implied" by the type identifier.

## Structure Change

### Before (Incorrect)
```yaml
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Person"
    labels: ["Person"]
    supertypes: ["Entity"]  # if present
    propertyTypes: [...]
```

### After (Correct - LEX-100r3)
```yaml
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Person"
    implies:
      supertypes: ["Entity"]  # optional
      labels: ["Person"]
      propertyTypes: [...]
```

## Files Updated

### 1. JSON Schema
- `src/grasch/schemas/lex-2026.0.3.1.schema.json`
  - Added `implies` object container to `NodeType`
  - Added `implies` object container to `EdgeType`
  - Moved `labels`, `supertypes`, `propertyTypes`, and `extensionInterpretation` inside `implies`
  - Updated required fields: `["nodeTypeIdentifier", "implies"]`

### 2. YAML Examples
- `src/grasch/examples/finbench-lex-2026.0.3.1-schema.yaml`
  - Restructured all 5 node types with `implies`
  - Restructured all 9 edge types with `implies`

- `src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml`
  - Restructured all 8 node types with `implies`
  - Restructured all 15 edge types with `implies`

### 3. Validation Scripts
- `tests/validate_finbench_lex_0_3_1_schema.py`
  - Updated to access properties via `node_type.get('implies', {})`
  - Updated to access supertypes via `implies.get('supertypes')`

- `tests/validate_snb_lex_0_3_1_schema.py`
  - Updated to access properties via `node_type.get('implies', {})`
  - Updated to access supertypes via `implies.get('supertypes')`

## Validation Status
✅ All validation tests pass:
- FinBench schema validation: PASSED (5 node types, 9 edge types, 50 properties)
- SNB schema validation: PASSED (8 node types, 15 edge types, 46 properties)
- Catalog with IRI validation: PASSED
- Catalog without IRI validation: PASSED

## Example: Complete Node Type

```yaml
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Person"
    implies:
      labels:
        - "Person"
      propertyTypes:
        - name: "id"
          valueType:
            name: "INTEGER"
            parameters:
              nullable: false
        - name: "name"
          valueType:
            name: "STRING"
            parameters:
              nullable: false
```

## Example: Node Type with Supertypes

```yaml
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Employee"
    implies:
      supertypes:
        - "Person"
      labels:
        - "Employee"
      propertyTypes:
        - name: "employeeId"
          valueType:
            name: "INTEGER"
```

## LEX-100r3 Reference

From the specification (lines 470-510):
```
– node type            
    – identified node type
  – type identifier 
  – implies
      – ? supertypes <set <type label>>
      – ? labels <set <identifier>>
      – ? property types <set <property type>>
```

This structure makes it clear that the labels and property types are "implied" by the type identifier, and that supertypes contribute to what is implied.

## Impact
- **Breaking Change**: All existing 0.3.1 schemas must be updated to use the `implies` structure
- **Semantic Clarity**: Better reflects the meaning that these attributes are implied by the type
- **Spec Compliance**: Now fully compliant with LEX-100r3 abstract syntax
