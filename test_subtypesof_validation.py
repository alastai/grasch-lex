#!/usr/bin/env python3
"""Test if subtypesOf validation works"""
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))

# Test data matching our import structure
test_data = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {
                "valueTypeSystemName": "CANONICAL"
            },
            "nodeTypes": [
                {
                    "subtypesOf": {
                        "abstract": {
                            "nodeTypes": [
                                {
                                    "nodeType": {
                                        "typeLabel": "Message",
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

validator = Draft202012Validator(schema)
errors = list(validator.iter_errors(test_data))

if errors:
    print(f"Validation FAILED with {len(errors)} error(s)\n")
    for err in errors[:3]:
        print(f"  {err.validator}: {err.message[:150]}")
else:
    print("✓ Validation PASSED!")
