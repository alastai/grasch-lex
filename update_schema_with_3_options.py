#!/usr/bin/env python3
"""
Update the schema to support 3 import options for all type interpretations:
1. Inline content
2. Interpretation inline, import content  
3. Import entire interpretation with content
"""

import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

with open(schema_path) as f:
    schema = json.load(f)

# Helper function to create the 3-option pattern for a type interpretation
def create_interpretation_with_import(array_ref):
    """
    Creates a oneOf that allows:
    1. Direct array reference (inline)
    2. Import object (import content only)
    """
    return {
        "oneOf": [
            {"$ref": array_ref},  # Option 1: inline array
            {  # Option 2: import content
                "type": "object",
                "required": ["import"],
                "properties": {
                    "import": {
                        "type": "string",
                        "description": "Import content from file"
                    }
                },
                "additionalProperties": False
            }
        ]
    }

# Update NodeTypesProperty
node_types_property = {
    "description": "The nodeTypes property with optional type interpretation wrappers",
    "oneOf": [
        {"$ref": "#/$defs/NodeTypesArray"},  # Plain array
        {  # abstract wrapper
            "type": "object",
            "required": ["abstract"],
            "properties": {
                "abstract": create_interpretation_with_import("#/$defs/NodeTypesArray")
            },
            "additionalProperties": False
        },
        {  # final wrapper
            "type": "object",
            "required": ["final"],
            "properties": {
                "final": create_interpretation_with_import("#/$defs/NodeTypesArray")
            },
            "additionalProperties": False
        },
        {  # sealed wrapper
            "type": "object",
            "required": ["sealed"],
            "properties": {
                "sealed": create_interpretation_with_import("#/$defs/NodeTypesArray")
            },
            "additionalProperties": False
        },
        {  # subtypesOf wrapper
            "type": "object",
            "required": ["subtypesOf"],
            "properties": {
                "subtypesOf": create_interpretation_with_import("#/$defs/NodeTypesArray")
            },
            "additionalProperties": False
        },
        {  # Option 3: import entire interpretation
            "type": "object",
            "required": ["import"],
            "properties": {
                "import": {
                    "type": "string",
                    "description": "Import nodeTypes with interpretation from file"
                }
            },
            "additionalProperties": False
        }
    ]
}

# Update EdgeTypesProperty with same pattern
edge_types_property = {
    "description": "The edgeTypes property with optional type interpretation wrappers",
    "oneOf": [
        {"$ref": "#/$defs/EdgeTypesArray"},  # Plain array
        {  # abstract wrapper
            "type": "object",
            "required": ["abstract"],
            "properties": {
                "abstract": create_interpretation_with_import("#/$defs/EdgeTypesArray")
            },
            "additionalProperties": False
        },
        {  # final wrapper
            "type": "object",
            "required": ["final"],
            "properties": {
                "final": create_interpretation_with_import("#/$defs/EdgeTypesArray")
            },
            "additionalProperties": False
        },
        {  # sealed wrapper
            "type": "object",
            "required": ["sealed"],
            "properties": {
                "sealed": create_interpretation_with_import("#/$defs/EdgeTypesArray")
            },
            "additionalProperties": False
        },
        {  # subtypesOf wrapper
            "type": "object",
            "required": ["subtypesOf"],
            "properties": {
                "subtypesOf": create_interpretation_with_import("#/$defs/EdgeTypesArray")
            },
            "additionalProperties": False
        },
        {  # Option 3: import entire interpretation
            "type": "object",
            "required": ["import"],
            "properties": {
                "import": {
                    "type": "string",
                    "description": "Import edgeTypes with interpretation from file"
                }
            },
            "additionalProperties": False
        }
    ]
}

# Update the schema
schema["$defs"]["NodeTypesProperty"] = node_types_property
schema["$defs"]["EdgeTypesProperty"] = edge_types_property

# Write back
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("✓ Schema updated with 3-option import pattern")
print("  1. Inline content")
print("  2. Interpretation inline, import content")
print("  3. Import entire interpretation with content")
