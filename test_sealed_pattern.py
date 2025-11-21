#!/usr/bin/env python3
"""Test what pattern sealed should use."""

import json
import yaml
from jsonschema import Draft202012Validator

# Load schema
with open("src/grasch/schemas/lex-2026.0.3.2.schema.json") as f:
    schema = json.load(f)

# Test pattern 1: sealed as direct array
test1 = {
    "sealed": [
        {"abstract": {"nodeType": {"typeLabel": "Place", "implies": {"propertyTypes": []}}}},
        {"nodeType": {"typeLabel": "City", "implies": {"propertyTypes": []}}}
    ]
}

# Test pattern 2: sealed with nodeTypes property
test2 = {
    "sealed": {
        "nodeTypes": [
            {"abstract": {"nodeType": {"typeLabel": "Place", "implies": {"propertyTypes": []}}}},
            {"nodeType": {"typeLabel": "City", "implies": {"propertyTypes": []}}}
        ]
    }
}

validator = Draft202012Validator(schema["$defs"]["NodeTypesProperty"])

print("Pattern 1 (sealed: [array]):")
errors1 = list(validator.iter_errors(test1))
if errors1:
    print(f"  ✗ INVALID: {errors1[0].message}")
else:
    print("  ✓ VALID")

print("\nPattern 2 (sealed: nodeTypes: [array]):")
errors2 = list(validator.iter_errors(test2))
if errors2:
    print(f"  ✗ INVALID: {errors2[0].message}")
else:
    print("  ✓ VALID")
