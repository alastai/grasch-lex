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
    error = errors[0]
    print(f"Main error: {error.validator} at {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
    print(f"\nContext errors ({len(error.context)}):")
    for i, ctx_err in enumerate(error.context):
        print(f"\n{i+1}. Path: {'.'.join(str(p) for p in ctx_err.absolute_path) or 'root'}")
        print(f"   Validator: {ctx_err.validator}")
        print(f"   Message: {ctx_err.message}")
        if ctx_err.validator == 'additionalProperties':
            print(f"   Schema path: {'.'.join(str(p) for p in ctx_err.schema_path)}")
