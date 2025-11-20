#!/usr/bin/env python3
"""
Allow multiple nodeTypes and edgeTypes properties in GraphType using type interpretation wrappers.
This enables patterns like:
  graphType:
    abstract:
      nodeTypes: [...]
    sealed:
      edgeTypes: [...]
    concrete:
      nodeTypes: [...]
"""

import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path) as f:
    schema = json.load(f)

# Find GraphType definition
graph_type = schema["$defs"]["GraphType"]

# Currently it has "additionalProperties": true
# We need to change this to allow type interpretation wrappers

# Create a pattern that allows abstract/sealed/final/concrete/subtypesOf properties
# Each can contain nodeTypes or edgeTypes

type_interpretation_wrapper = {
    "type": "object",
    "description": "Type interpretation wrapper containing nodeTypes or edgeTypes",
    "properties": {
        "nodeTypes": {
            "$ref": "#/$defs/NodeTypesProperty"
        },
        "edgeTypes": {
            "$ref": "#/$defs/EdgeTypesProperty"
        }
    },
    "additionalProperties": False,
    "minProperties": 1
}

# Update GraphType to use patternProperties
# This allows properties matching the pattern to have the wrapper structure
graph_type["patternProperties"] = {
    "^(abstract|sealed|final|concrete|subtypesOf)$": type_interpretation_wrapper
}

# Keep additionalProperties as true for other properties
# (or set to false if we want strict validation)
graph_type["additionalProperties"] = True

# Write back
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("✓ GraphType updated to allow multiple nodeTypes/edgeTypes properties")
print("  Supported patterns:")
print("    - abstract: nodeTypes: [...]")
print("    - sealed: edgeTypes: [...]")
print("    - final: nodeTypes: [...]")
print("    - concrete: nodeTypes: [...]")
print("    - subtypesOf: nodeTypes: [...]")
print("  These can appear multiple times in any order")
