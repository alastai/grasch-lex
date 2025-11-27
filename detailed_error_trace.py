#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

test_data = {
    "graphSchema": {
        "pathName": "test_schema",
        "graphType": {
            "propertyGraphDataModel": {
                "valueTypeSystemName": "CANONICAL"
            },
            "nodeTypes": [{
                "nodeType": {
                    "typeLabel": "Person",
                    "implies": {
                        "labels": ["Person"],
                        "properties": {"name": "STRING"}
                    }
                }
            }]
        }
    }
}

resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)

print("Collecting ALL validation errors...\n")
errors = sorted(validator.iter_errors(test_data), key=lambda e: len(e.path))

print(f"Total errors: {len(errors)}\n")

for i, error in enumerate(errors[:10]):
    print(f"Error {i+1}:")
    print(f"  Path: {' -> '.join(str(p) for p in error.path) if error.path else 'ROOT'}")
    print(f"  Schema path: {' -> '.join(str(p) for p in error.schema_path)}")
    print(f"  Validator: {error.validator}")
    print(f"  Message: {error.message[:150]}")
    print()
