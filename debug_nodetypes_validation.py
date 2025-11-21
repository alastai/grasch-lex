#!/usr/bin/env python3
"""Debug nodeTypes array validation in detail."""
import json
from jsonschema import Draft202012Validator
from pathlib import Path

# Load schema
schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Load preprocessed data
with open('preprocessed_minimal.json', 'r') as f:
    doc = json.load(f)

# Get just the nodeTypes array
node_types_data = doc['graphSchema']['graphType']['nodeTypes']

print(f"NodeTypes array has {len(node_types_data)} items")
print(f"\nItem 0 keys: {list(node_types_data[0].keys())}")
print(f"Item 1 keys: {list(node_types_data[1].keys())}")

# Get the nodeTypes property schema from GraphType
graph_type_schema = schema['$defs']['GraphType']
node_types_prop_schema = graph_type_schema['properties']['nodeTypes']

print(f"\nnodeTypes property has oneOf with {len(node_types_prop_schema['oneOf'])} options")
print(f"Option 0: {node_types_prop_schema['oneOf'][0].get('type')}")
print(f"Option 1: {list(node_types_prop_schema['oneOf'][1].keys())[:3]}")

# Validate the nodeTypes array against the full schema
validator = Draft202012Validator(schema)

# Create a minimal document with just graphSchema
test_doc = {
    "graphSchema": {
        "pathName": "/test",
        "graphType": {
            "propertyGraphDataModel": {},
            "nodeTypes": node_types_data
        }
    }
}

errors = list(validator.iter_errors(test_doc))
print(f"\n{'='*70}")
print(f"Validation errors: {len(errors)}")
print(f"{'='*70}")

for i, error in enumerate(errors[:3]):
    print(f"\nError {i+1}:")
    print(f"  Path: {'.'.join(str(p) for p in error.absolute_path) or 'root'}")
    print(f"  Validator: {error.validator}")
    print(f"  Message: {error.message[:200]}")
    if error.context and len(error.context) < 10:
        print(f"  Context ({len(error.context)} sub-errors):")
        for j, ctx in enumerate(error.context[:3]):
            print(f"    {j+1}. {ctx.validator}: {ctx.message[:100]}")
