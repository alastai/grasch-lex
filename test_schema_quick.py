#!/usr/bin/env python3
"""Quick schema validation test"""

import json
import yaml
from jsonschema import Draft202012Validator, RefResolver

# Load schema
with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

# Load test file
with open('src/grasch/examples/test-phase-a-corrected.yaml', 'r') as f:
    test_data = yaml.safe_load(f)

# Create validator
resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)

# Validate
errors = list(validator.iter_errors(test_data))

if errors:
    print(f"❌ VALIDATION FAILED with {len(errors)} error(s)\n")
    for i, error in enumerate(errors, 1):
        print(f"Error {i}:")
        print(f"  Path: {' -> '.join(str(p) for p in error.path) or 'ROOT'}")
        print(f"  Message: {error.message}")
        print(f"  Validator: {error.validator}")
        if error.context:
            print(f"  Context errors: {len(error.context)}")
            for j, ctx_error in enumerate(error.context[:3], 1):
                print(f"    {j}. {ctx_error.message}")
        print()
else:
    print("✓ VALIDATION PASSED")
