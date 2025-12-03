#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

# Test just the graphType content
graphtype_content = {
    "propertyGraphDataModel": {
        "valueTypeSystemName": "CANONICAL"
    },
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

# Get the GraphType definition
gt_def = schema["$defs"]["GraphType"]

# Create a temporary schema
temp_schema = {
    "$schema": schema["$schema"],
    **gt_def,
    "$defs": schema["$defs"]
}

resolver = RefResolver.from_schema(temp_schema)
validator = Draft202012Validator(temp_schema, resolver=resolver)

print("Testing graphType content against GraphType definition...\n")
errors = list(validator.iter_errors(graphtype_content))

if errors:
    print(f"❌ FAIL ({len(errors)} errors)\n")
    for i, error in enumerate(errors[:5]):
        print(f"Error {i+1}:")
        print(f"  Path: {' -> '.join(str(p) for p in error.path) if error.path else 'ROOT'}")
        print(f"  Validator: {error.validator}")
        if error.validator == "required":
            print(f"  Required: {error.validator_value}")
            print(f"  Missing: {error.message}")
        else:
            print(f"  Message: {error.message[:150]}")
        print()
else:
    print("✅ PASS - graphType content validates against GraphType!")
