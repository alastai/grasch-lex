#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema_path = "src/grasch/schemas/lex-2026.0.3.2.schema.json"
with open(schema_path, 'r') as f:
    schema = json.load(f)

with open('preprocessed_minimal.json', 'r') as f:
    doc = json.load(f)

validator = Draft202012Validator(schema)

errors = list(validator.iter_errors(doc))
if errors:
    print(f"Found {len(errors)} errors:")
    for i, error in enumerate(errors[:5]):
        print(f"\nError {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:500]}")
        if error.context:
            print(f"  Context errors: {len(error.context)}")
            for j, ctx_err in enumerate(error.context[:3]):
                print(f"    Context {j+1}: {ctx_err.message[:200]}")
else:
    print("✓ Validation passed!")
