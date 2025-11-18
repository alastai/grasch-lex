# Amendment: typeNameLabel → typeLabel

## Change Applied
Changed the element name from `typeNameLabel` to `typeLabel` throughout all LEX:2026.0.3.1 files.

## Files Updated
1. `src/grasch/schemas/lex-2026.0.3.1.schema.json` - JSON Schema definition
2. `src/grasch/examples/finbench-lex-2026.0.3.1-schema.yaml` - FinBench example
3. `src/grasch/examples/snb-lex-2026.0.3.1-schema.yaml` - SNB example
4. `tests/validate_finbench_lex_0_3_1_schema.py` - FinBench validation script
5. `tests/validate_snb_lex_0_3_1_schema.py` - SNB validation script
6. `LEX-2026.0.3.1-GUIDE.md` - Implementation guide
7. `LEX-2026.0.3-CHANGES.md` - Changelog
8. `LEX-2026.0.3.1-SUMMARY.md` - Summary document

## Validation Status
✅ All validation tests pass:
- FinBench schema validation: PASSED
- SNB schema validation: PASSED
- Catalog with IRI validation: PASSED
- Catalog without IRI validation: PASSED

## Example Usage
```yaml
nodeTypes:
  - nodeTypeIdentifier:
      typeLabel: "Person"  # Changed from typeNameLabel
    labels: ["Person"]
    propertyTypes: [...]
```

## Rationale
Simplified naming to `typeLabel` for clarity and consistency with LEX-100r3 specification.
