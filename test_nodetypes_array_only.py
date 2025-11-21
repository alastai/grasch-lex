#!/usr/bin/env python3
import json
from jsonschema import Draft202012Validator

schema_path = "src/grasch/schemas/lex-2026.0.3.2.schema.json"
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Get the nodeTypes schema
node_types_schema = schema['$defs']['GraphType']['properties']['nodeTypes']

# Test data - just the nodeTypes array from the failing file
with open('preprocessed_minimal.json', 'r') as f:
    doc = json.load(f)

node_types_data = doc['graphSchema']['graphType']['nodeTypes']

print(f"Testing nodeTypes array with {len(node_types_data)} items")
print(f"Item 0 keys: {list(node_types_data[0].keys())}")

validator = Draft202012Validator(node_types_schema)

errors = list(validator.iter_errors(node_types_data))
if errors:
    print(f"\nFound {len(errors)} errors:")
    for i, error in enumerate(errors[:3]):
        print(f"\nError {i+1}:")
        print(f"  Path: {'.'.join(str(p) for p in error.absolute_path)}")
        print(f"  Validator: {error.validator}")
        print(f"  Message: {error.message[:300]}")
        if error.context:
            print(f"  Context errors: {len(error.context)}")
else:
    print("\n✓ nodeTypes array validates!")
