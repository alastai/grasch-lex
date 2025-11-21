#!/usr/bin/env python3
"""
Minimal test case to understand the validation failure
"""
import json
from jsonschema import Draft202012Validator

schema = json.load(open('src/grasch/schemas/lex-2026.0.3.2.schema.json'))
validator = Draft202012Validator(schema)

# Minimal test case - just the graphSchema with subtypesOf
minimal_data = {
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

print("Testing minimal case...")
errors = list(validator.iter_errors(minimal_data))

if errors:
    print(f"✗ FAILED with {len(errors)} error(s)")
    for err in errors:
        print(f"  {err.validator} at {'.'.join(str(p) for p in err.absolute_path) or 'root'}")
        if err.context:
            print(f"    {len(err.context)} sub-errors")
else:
    print("✓ PASSED")

# Now test with the full preprocessed data
print("\nTesting full preprocessed data...")
full_data = json.load(open('preprocessed_minimal.json'))
errors = list(validator.iter_errors(full_data))

if errors:
    print(f"✗ FAILED with {len(errors)} error(s)")
else:
    print("✓ PASSED")
