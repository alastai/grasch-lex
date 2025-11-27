#!/usr/bin/env python3
"""Add TI Content Import Definitions to Schema"""

import json
from pathlib import Path

SCHEMA_PATH = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")

# Load schema
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

# Add TIWrapperContentNode
schema["$defs"]["TIWrapperContentNode"] = {
    "description": "Content within TI wrappers for node types",
    "oneOf": [
        {
            "description": "Inline type set",
            "anyOf": [
                {
                    "description": "Singleton set",
                    "$ref": "#/$defs/NodeType"
                },
                {
                    "description": "Multi-element set",
                    "type": "array",
                    "items": {"$ref": "#/$defs/NodeType"}
                }
            ]
        },
        {
            "description": "Phase 2: Import type definitions only",
            "type": "object",
            "required": ["import"],
            "properties": {
                "import": {
                    "type": "string",
                    "description": "Import type definitions"
                }
            },
            "additionalProperties": False
        }
    ]
}

# Add TIWrapperContentEdge
schema["$defs"]["TIWrapperContentEdge"] = {
    "description": "Content within TI wrappers for edge types",
    "oneOf": [
        {
            "description": "Inline type set",
            "anyOf": [
                {
                    "description": "Singleton set",
                    "$ref": "#/$defs/EdgeType"
                },
                {
                    "description": "Multi-element set",
                    "type": "array",
                    "items": {"$ref": "#/$defs/EdgeType"}
                }
            ]
        },
        {
            "description": "Phase 2: Import type definitions only",
            "type": "object",
            "required": ["import"],
            "properties": {
                "import": {
                    "type": "string",
                    "description": "Import type definitions"
                }
            },
            "additionalProperties": False
        }
    ]
}

print("✅ Added TIWrapperContentNode")
print("✅ Added TIWrapperContentEdge")

# Save schema
with open(SCHEMA_PATH, "w") as f:
    json.dump(schema, f, indent=2)

print(f"✅ Schema updated: {SCHEMA_PATH}")
