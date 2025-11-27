#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator, RefResolver

with open("src/grasch/schemas/lex-2026.0.3.2.schema.json", 'r') as f:
    schema = json.load(f)

test_data = {
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

print("Testing root oneOf options...\n")

for i, option in enumerate(schema["oneOf"]):
    required = option.get("required", [])
    print(f"Option {i+1}: requires {required}")
    
    has_required = all(req in test_data for req in required)
    print(f"  Has required: {has_required}")
    
    if has_required:
        resolver = RefResolver.from_schema(schema)
        validator = Draft202012Validator(option, resolver=resolver)
        errors = list(validator.iter_errors(test_data))
        
        if errors:
            print(f"  ❌ FAIL ({len(errors)} errors)")
            for j, error in enumerate(errors[:2]):
                print(f"    {j+1}. Path: {list(error.path)}, Validator: {error.validator}")
                print(f"       {error.message[:80]}")
        else:
            print(f"  ✅ PASS")
    print()
