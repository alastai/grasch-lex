#!/usr/bin/env python3
"""Test minimal graphSchema."""
import json
from jsonschema import Draft202012Validator

schema_path = "src/grasch/schemas/lex-2026.0.3.2.schema.json"
with open(schema_path, 'r') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Test with subtypesOf
test_doc = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {},
            "nodeTypes": [
                {
                    "subtypesOf": {
                        "abstract": {
                            "nodeTypes": [
                                {
                                    "nodeType": {
                                        "typeLabel": "Test",
                                        "implies": {
                                            "propertyTypes": []
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }
}

errors = list(validator.iter_errors(test_doc))
if errors:
    print(f"Found {len(errors)} errors:")
    for i, error in enumerate(errors[:3]):
        print(f"\nError {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:300]}")
else:
    print("✓ Minimal validation passed!")
