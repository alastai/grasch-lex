#!/usr/bin/env python3
"""Analyze the pre-import schema structure to understand where wrappers need to be added."""

import json

with open('src/grasch/schemas/lex-2026.0.3.2-pre-import.schema.json', 'r') as f:
    schema = json.load(f)

# Find all definitions
print("=== Top-level definitions ===")
for key in schema.get('$defs', {}).keys():
    print(f"  - {key}")

# Look at NodeType definition
print("\n=== NodeType definition structure ===")
node_type = schema['$defs'].get('NodeType', {})
print(json.dumps(node_type, indent=2)[:1000])

# Look at EdgeType definition
print("\n=== EdgeType definition structure ===")
edge_type = schema['$defs'].get('EdgeType', {})
print(json.dumps(edge_type, indent=2)[:1000])

# Look at GraphType to see how nodeTypes array is defined
print("\n=== GraphType nodeTypes property ===")
graph_type = schema['$defs'].get('GraphType', {})
node_types_prop = graph_type.get('properties', {}).get('nodeTypes', {})
print(json.dumps(node_types_prop, indent=2)[:2000])

# Check if there are wrapper keywords already
print("\n=== Checking for existing wrapper keywords ===")
schema_str = json.dumps(schema)
for keyword in ['abstract', 'concrete', 'properSubtypesOf', 'exactlyOf', 'subtypesOf']:
    if keyword in schema_str:
        print(f"  Found: {keyword}")
    else:
        print(f"  NOT found: {keyword}")
