#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)

# Test WITH propertyGraphDataModel
print("Test: graphSchema WITH propertyGraphDataModel")
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
                        "propertyTypes": {"name": "STRING"}
                    }
                }
            }]
        }
    }
}

errors = list(validator.iter_errors(test_data))
print(f"Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")

if errors:
    for i, e in enumerate(errors[:3]):
        print(f"\nError {i+1}:")
        print(f"  Path: {list(e.path)}")
        print(f"  Validator: {e.validator}")
        print(f"  Message: {e.message[:120]}")
else:
    print("\n🎉 SUCCESS! The schema validates when propertyGraphDataModel is included!")
