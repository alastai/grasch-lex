#!/usr/bin/env python3
"""Revise TI-content import pattern definitions."""

import json
from pathlib import Path

schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

# Read the schema
with open(schema_path, 'r') as f:
    schema = json.load(f)

# Remove incorrect definitions
defs_to_remove = ["NodeTypeOrImport", "EdgeTypeOrImport", "NodeTypeSetOrImport", "EdgeTypeSetOrImport"]

for def_name in defs_to_remove:
    if def_name in schema["$defs"]:
        del schema["$defs"][def_name]
        print(f"Removed: {def_name}")

# Add correct definitions
new_defs = {
    "NodeTypesSetOrImport": {
        "description": "TI wrapper contents: set of NodeTypes (singleton or array) or import",
        "oneOf": [
            {
                "anyOf": [
                    {"$ref": "#/$defs/NodeType"},
                    {"$ref": "#/$defs/NodeTypesArray"}
                ]
            },
            {
                "type": "object",
                "required": ["import"],
                "properties": {"import": {"type": "string"}},
                "additionalProperties": False
            }
        ]
    },
    "EdgeTypesSetOrImport": {
        "description": "TI wrapper contents: set of EdgeTypes (singleton or array) or import",
        "oneOf": [
            {
                "anyOf": [
                    {"$ref": "#/$defs/EdgeType"},
                    {"$ref": "#/$defs/EdgeTypesArray"}
                ]
            },
            {
                "type": "object",
                "required": ["import"],
                "properties": {"import": {"type": "string"}},
                "additionalProperties": False
            }
        ]
    }
}

schema["$defs"].update(new_defs)

# Write back
with open(schema_path, 'w') as f:
    json.dump(schema, f, indent=2)

print("\nAdded:")
print("  - NodeTypesSetOrImport")
print("  - EdgeTypesSetOrImport")
print("\nKept:")
print("  - NodeTypesArrayOrImport")
print("  - EdgeTypesArrayOrImport")
