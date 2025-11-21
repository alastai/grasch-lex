#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

# Test with just the subtypesOf
test1 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {"valueTypeSystemName": "CANONICAL"},
            "nodeTypes": [
                {
                    "subtypesOf": {
                        "abstract": {
                            "nodeTypes": [
                                {"nodeType": {"typeLabel": "Test", "implies": {"propertyTypes": []}}}
                            ]
                        }
                    }
                }
            ]
        }
    }
}

# Test with both subtypesOf and regular nodeType
test2 = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {"valueTypeSystemName": "CANONICAL"},
            "nodeTypes": [
                {
                    "subtypesOf": {
                        "abstract": {
                            "nodeTypes": [
                                {"nodeType": {"typeLabel": "Test", "implies": {"propertyTypes": []}}}
                            ]
                        }
                    }
                },
                {
                    "nodeType": {
                        "typeLabel": "Person",
                        "implies": {"propertyTypes": []}
                    }
                }
            ]
        }
    }
}

print("Test 1 (just subtypesOf):")
errors = list(validator.iter_errors(test1))
print(f"  {'✓ PASSED' if not errors else f'✗ FAILED ({len(errors)} errors)'}")

print("\nTest 2 (subtypesOf + regular nodeType):")
errors = list(validator.iter_errors(test2))
print(f"  {'✓ PASSED' if not errors else f'✗ FAILED ({len(errors)} errors)'}")
