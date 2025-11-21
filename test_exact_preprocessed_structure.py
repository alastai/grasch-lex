#!/usr/bin/env python3
"""Test with exact structure from preprocessed file."""
import json
from jsonschema import Draft202012Validator

schema_path = "src/grasch/schemas/lex-2026.0.3.2.schema.json"
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Load the exact nodeTypes from preprocessed file
with open('preprocessed_minimal.json', 'r') as f:
    preprocessed = json.load(f)

validator = Draft202012Validator(schema)

# Test with exact structure
test_doc = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {},
            "nodeTypes": preprocessed['graphSchema']['graphType']['nodeTypes']
        }
    }
}

errors = list(validator.iter_errors(test_doc))
if errors:
    print(f"Found {len(errors)} errors:")
    for i, error in enumerate(errors[:5]):
        print(f"\nError {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:200]}")
        if error.context and len(error.context) < 20:
            print(f"  Context: {len(error.context)} sub-errors")
            for j, ctx in enumerate(error.context[:3]):
                print(f"    {j+1}. Path: {'.'.join(str(p) for p in ctx.absolute_path)}")
                print(f"       {ctx.validator}: {ctx.message[:150]}")
else:
    print("✓ Validation passed!")
