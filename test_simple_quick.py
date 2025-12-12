#!/usr/bin/env python3
import json
import yaml
from jsonschema import Draft202012Validator, RefResolver

with open('src/grasch/schemas/lex-2026.0.3.2.schema.json', 'r') as f:
    schema = json.load(f)

with open('test_simple_graphschema.yaml', 'r') as f:
    test_data = yaml.safe_load(f)

resolver = RefResolver.from_schema(schema)
validator = Draft202012Validator(schema, resolver=resolver)

errors = list(validator.iter_errors(test_data))

if errors:
    print(f"❌ FAILED with {len(errors)} error(s)\n")
    for error in errors:
        print(f"Path: {' -> '.join(str(p) for p in error.path) or 'ROOT'}")
        print(f"Message: {error.message[:200]}")
        print()
else:
    print("✓ PASSED")
