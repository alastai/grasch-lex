#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

# The content inside nodeType: { ... }
nodetype_content = {
    "typeLabel": "Person",
    "implies": {
        "labels": ["Person"],
        "properties": {"name": "STRING"}
    }
}

# Get the NodeType definition and extract the nodeType property oneOf
nt_def = schema["$defs"]["NodeType"]
nodetype_property_oneof = nt_def["properties"]["nodeType"]["oneOf"]

print(f"NodeType.nodeType has {len(nodetype_property_oneof)} oneOf options\n")

# Test against each option
for i, option in enumerate(nodetype_property_oneof):
    temp_schema = {
        "$schema": schema["$schema"],
        **option,
        "$defs": schema["$defs"]
    }
    
    resolver = RefResolver.from_schema(temp_schema)
    validator = Draft202012Validator(temp_schema, resolver=resolver)
    
    errors = list(validator.iter_errors(nodetype_content))
    
    required = option.get("required", [])
    print(f"Option {i+1}: requires {required}")
    
    if errors:
        print(f"  ❌ FAIL ({len(errors)} errors)")
        for j, error in enumerate(errors[:2]):
            print(f"    - {error.validator}: {error.message[:80]}")
    else:
        print(f"  ✅ PASS")
    print()
