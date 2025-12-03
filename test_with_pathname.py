#!/usr/bin/env python3
"""Test if adding pathName fixes the validation"""

import json
from jsonschema import Draft202012Validator, RefResolver

# Load schema
with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)

# Test WITHOUT pathName (should fail)
print("Test 1: graphSchema WITHOUT pathName")
gs_no_pathname = {
    "graphSchema": {
        "graphType": {
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

errors = list(validator.iter_errors(gs_no_pathname))
print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")
if errors:
    print(f"  Error: {errors[0].message[:100]}")

# Test WITH pathName (should pass)
print("\nTest 2: graphSchema WITH pathName")
gs_with_pathname = {
    "graphSchema": {
        "pathName": "test_schema",
        "graphType": {
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

errors = list(validator.iter_errors(gs_with_pathname))
print(f"  Result: {'✅ PASS' if not errors else f'❌ FAIL ({len(errors)} errors)'}")
if errors:
    for i, e in enumerate(errors[:3]):
        print(f"\n  Error {i+1}:")
        print(f"    Path: {list(e.path)}")
        print(f"    Message: {e.message[:120]}")
