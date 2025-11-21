#!/usr/bin/env python3
"""
Allow nested type interpretations in GraphType.
Supports patterns like:
  - sealed: nodeTypes: [...]
  - exactlyOf: concrete: nodeTypes: [...]
  - subtypesOf: abstract: edgeTypes: [...]
"""

import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path) as f:
    schema = json.load(f)

# Define the innermost level: nodeTypes or edgeTypes
element_types_object = {
    "type": "object",
    "description": "Container for nodeTypes or edgeTypes",
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

# Define concreteness wrappers (can wrap element types)
concreteness_wrapper = {
    "type": "object",
    "description": "Concreteness interpretation wrapper",
    "patternProperties": {
        "^(abstract|sealed|final|concrete)$": element_types_object
    },
    "additionalProperties": False,
    "minProperties": 1,
    "maxProperties": 1
}

# Define validation mode wrappers (can wrap concreteness wrappers OR element types)
validation_mode_wrapper = {
    "type": "object",
    "description": "Validation mode interpretation wrapper",
    "patternProperties": {
        "^(exactlyOf|subtypesOf|properSubtypesOf)$": {
            "oneOf": [
                element_types_object,      # Direct: exactlyOf: nodeTypes:
                concreteness_wrapper        # Nested: exactlyOf: concrete: nodeTypes:
            ]
        }
    },
    "additionalProperties": False,
    "minProperties": 1,
    "maxProperties": 1
}

# Update GraphType patternProperties to allow all three patterns:
# 1. Direct concreteness: abstract: nodeTypes:
# 2. Direct validation mode: exactlyOf: nodeTypes:
# 3. Nested: exactlyOf: concrete: nodeTypes:

graph_type = schema["$defs"]["GraphType"]
graph_type["patternProperties"] = {
    # Concreteness interpretations
    "^(abstract|sealed|final|concrete|subtypesOf)$": element_types_object,
    # Validation mode interpretations (can be nested)
    "^(exactlyOf|properSubtypesOf)$": {
        "oneOf": [
            element_types_object,      # Direct
            concreteness_wrapper        # Nested
        ]
    }
}

# Write back
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("✓ GraphType updated to allow nested type interpretations")
print("  Supported patterns:")
print("    Level 1: sealed: nodeTypes: [...]")
print("    Level 1: abstract: edgeTypes: [...]")
print("    Level 2: exactlyOf: concrete: nodeTypes: [...]")
print("    Level 2: subtypesOf: abstract: edgeTypes: [...]")
print("    Level 2: properSubtypesOf: sealed: nodeTypes: [...]")
