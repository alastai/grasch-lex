#!/usr/bin/env python3
"""
Update sealed/final wrapper definitions to use the new NodeTypeSetOrImport/EdgeTypeSetOrImport.
This allows both PC form (with wrapper) and C form (without wrapper) to validate.
"""

import json
from pathlib import Path

def update_sealed_definitions():
    """Update sealed/final to use new definitions that support wrapper duplication/stripping."""
    
    schema_path = Path("src/grasch/schemas/lex-2026.0.3.2.schema.json")
    
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Find and update NodeTypeItem sealed definition
    node_type_item = schema["$defs"]["NodeTypeItem"]
    
    for i, option in enumerate(node_type_item["oneOf"]):
        if isinstance(option, dict) and "properties" in option:
            if "sealed" in option["properties"]:
                # Update to use NodeTypeSetOrImport
                node_type_item["oneOf"][i] = {
                    "type": "object",
                    "description": "Sealed hierarchy of node types",
                    "required": ["sealed"],
                    "properties": {
                        "sealed": {
                            "$ref": "#/$defs/NodeTypeSetOrImport"
                        }
                    },
                    "additionalProperties": False
                }
                print("✓ Updated NodeTypeItem.sealed to use NodeTypeSetOrImport")
    
    # Find and update EdgeTypeItem sealed definition
    edge_type_item = schema["$defs"]["EdgeTypeItem"]
    
    for i, option in enumerate(edge_type_item["oneOf"]):
        if isinstance(option, dict) and "properties" in option:
            if "sealed" in option["properties"]:
                # Update to use EdgeTypeSetOrImport
                edge_type_item["oneOf"][i] = {
                    "type": "object",
                    "description": "Sealed hierarchy of edge types",
                    "required": ["sealed"],
                    "properties": {
                        "sealed": {
                            "$ref": "#/$defs/EdgeTypeSetOrImport"
                        }
                    },
                    "additionalProperties": False
                }
                print("✓ Updated EdgeTypeItem.sealed to use EdgeTypeSetOrImport")
    
    # Write back
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("\n✓ Sealed definitions now support both PC and C forms")
    print("  - PC form: sealed: { nodeTypes: [...] }")
    print("  - C form: sealed: [...]")

if __name__ == "__main__":
    update_sealed_definitions()
