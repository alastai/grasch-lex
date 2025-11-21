#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

actual_data = json.load(open('preprocessed_minimal.json'))

# Test with minimal propertyGraphDataModel
test_minimal_pgdm = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {
                "valueTypeSystemName": "CANONICAL"
            },
            "nodeTypes": actual_data['graphSchema']['graphType']['nodeTypes']
        }
    }
}

errors = list(validator.iter_errors(test_minimal_pgdm))
print(f"With minimal PGDM: {len(errors)} errors")

# Test with full propertyGraphDataModel
test_full_pgdm = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": actual_data['graphSchema']['graphType']['propertyGraphDataModel'],
            "nodeTypes": actual_data['graphSchema']['graphType']['nodeTypes']
        }
    }
}

errors = list(validator.iter_errors(test_full_pgdm))
print(f"With full PGDM: {len(errors)} errors")

if errors:
    print("\nError details:")
    for err in errors[:1]:
        print(f"  {err.validator} at {'.'.join(str(p) for p in err.absolute_path) or 'root'}")
