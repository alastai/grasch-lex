#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

# Test just the bare nodeType structure
bare_nodetype = {
    "nodeType": {
        "typeLabel": "Person",
        "implies": {
            "labels": ["Person"],
            "properties": {"name": "STRING"}
        }
    }
}

# Get the NodeType definition
nt_def = schema["$defs"]["NodeType"]

# Create a temporary schema
temp_schema = {
    "$schema": schema["$schema"],
    **nt_def,
    "$defs": schema["$defs"]
}

resolver = RefResolver.from_schema(temp_schema)
validator = Draft202012Validator(temp_schema, resolver=resolver)

print("Testing bare nodeType against NodeType definition...\n")
errors = list(validator.iter_errors(bare_nodetype))

if errors:
    print(f"❌ FAIL ({len(errors)} errors)\n")
    for i, error in enumerate(errors[:5]):
        print(f"Error {i+1}:")
        print(f"  Path: {' -> '.join(str(p) for p in error.path) if error.path else 'ROOT'}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:150]}")
        print()
else:
    print("✅ PASS - bare nodeType validates against NodeType!")
